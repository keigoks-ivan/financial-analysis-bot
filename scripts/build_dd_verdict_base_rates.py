#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_dd_verdict_base_rates.py — DD 裁決 producer 的 base rate 機械餵料（forecast ledger v2
§5.4，包 D）。

供 scripts/generate_dd_verdict_forecasts.py 讀表用，輸出 data/dd_verdict_base_rates.json 兩張表：

  (a) p_clim（pooled 無條件頻率，PREREG 凍結定義，設計稿 §5.4）——對
      data/weekly_cache/ 全部 ticker，取近 5 年（CLIM_WINDOW_YEARS）每個曆月「首個可得週線
      收盤」為取樣點，算「該取樣點起 91／365 曆日後，該 ticker 報酬 > SPY 同窗報酬」的
      pooled（跨全部 ticker、跨全部取樣月）無條件頻率。SPY 收盤自本檔**專用**日線快取
      data/dd_verdict_base_rates_raw_cache.json 讀取（10 年，見下）。任一端缺資料（含視窗
      尚未到期）即跳過該 cell，不補值、不外推。
  (b) 經驗表（設計稿 §5.4 (b)）——對 knowledge/settlement.json 已到期（h91／h365 非 null）
      且 verdict 非 null 的裁決筆，算「跑贏 SPY」頻率，per verdict（進場／觀望／迴避）與 n。
      **目前預期 n≈0**：decisions.jsonl 的 verdict 欄自 2026-06-22 起才普遍存在，距今
      （builder 執行時）尚不足 91／365 曆日成熟，這是設計已知現象，不是 bug。

producer 的 CONFIG 常數 `USE_EMPIRICAL_TABLE` **不在本檔**（見
scripts/generate_dd_verdict_forecasts.py 檔頭）——本檔只負責把兩張表都算出來、誠實列出樣本
數，讀哪張表是 producer 的責任、且只有校準輪能翻旗標。

價格資料：SPY **自建 raw cache** `data/dd_verdict_base_rates_raw_cache.json`（yfinance ->
stooq fallback），與 data/flowmap_prices.json **解耦**——理由同 scripts/build_cot_base_rates.py
／scripts/build_rv_base_rates.py 的既有慣例：data/flowmap_prices.json 只 rolling ~500 交易日
（~2 年），深度不足以支撐本檔 5 年 p_clim 取樣窗，故自抓 10 年日線。與該兩檔不同的是**本檔
採 incremental 抓法**（首次 bootstrap 10 年、之後每次只 topup 近 30 天並與既有序列合併去重，
照抄 scripts/build_flowmap.py 的 build_price_cache() 慣例）——因為 SPY 單檔資料量遠小於逐
市場批次抓取，incremental 對本檔更省流量且不需要每次重驗證整段 10 年歷史。

誠實註記（務必讀）
------------------
* **p_clim 是重疊樣本的 pooled 經驗頻率，不是獨立試驗機率**——同一 ticker 相鄰曆月的取樣點
  彼此高度相關（尤其 365 曆日視窗），不同 ticker 之間也共享同一段 SPY 走勢（系統性風險不可
  分散），本表只報告經驗頻率與樣本數（cell 數／ticker 數），不做假設檢定、不附信賴區間。
* **取樣點＝「每個曆月首個可得週線收盤」，非精確對齊到月初交易日**——weekly_cache 是週線
  （不是日線），故「首個可得」就是該月第一根落在該月的 week_end，可能是月初到月中第一週
  之間任一天，隨 ticker 的週線切點自然浮動，這是設計上的取捨（週線資料本身就沒有更細的
  切點可用）。
* **視窗到期判斷採「ticker 與 SPY 兩邊最後一根資料日皆須 ≥ 目標日」**（照抄
  knowledge/settle_outcomes.py 的 HORIZONS 迴圈邏輯：`if last_date >= tgt: 用 close_at_or_
  before；否則整格跳過`）——避免用「離目標日很遠的最近可得收盤」偷渡成到期值，寧可少一格
  也不要算錯。

用法
----
  python scripts/build_dd_verdict_base_rates.py                完整重抓（bootstrap 或 topup）+ 重算
  python scripts/build_dd_verdict_base_rates.py --skip-fetch    離線：只用既有本地 SPY 快取重算
  python scripts/build_dd_verdict_base_rates.py --if-due        現有輸出 built_at <85 天則跳過
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE_DIR = DATA / "weekly_cache"
RAW_CACHE = DATA / "dd_verdict_base_rates_raw_cache.json"   # 本檔專用 SPY 日線，與 flowmap_prices.json 解耦
OUT_JSON = DATA / "dd_verdict_base_rates.json"
SETTLEMENT = ROOT / "knowledge" / "settlement.json"         # 唯讀消費，knowledge/settle_outcomes.py 維護

SCHEMA = "dd-verdict-base-rates-v1"
SPY_TICKER = "SPY"
FETCH_PERIOD_BOOTSTRAP = "10y"
FETCH_PERIOD_TOPUP = "30d"
IF_DUE_MAX_AGE_DAYS = 85          # --if-due 門檻（設計稿 §5.4：季度自動重建）

CLIM_WINDOW_YEARS = 5             # PREREG 凍結（設計稿 §5.4）
HORIZONS = {"dd_beat_spy_91d": 91, "dd_beat_spy_365d": 365}
VERDICTS = ["進場", "觀望", "迴避"]


def warn(msg):
    print(f"[dd-verdict-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[dd-verdict-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance -> stooq fallback；獨立實作，理由見檔頭 docstring）
# ═══════════════════════════════════════════════════════════════════════════

def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 dd-verdict-base-rates"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 dd-verdict-base-rates"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


def _yf_daily(ticker, period):
    import yfinance as yf
    df = yf.download(ticker, period=period, interval="1d", auto_adjust=True,
                      progress=False, threads=False)
    if df is None or df.empty:
        return None
    close = df["Close"]
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]
    rows = []
    for idx, val in close.items():
        try:
            c = float(val)
        except (TypeError, ValueError):
            continue
        if c != c:  # NaN
            continue
        rows.append((idx.date().isoformat(), round(c, 4)))
    return rows or None


def _stooq_daily(ticker):
    sym = ticker.lower()
    if "." not in sym:
        sym = sym + ".us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
    try:
        raw = _http_get(url, timeout=30).decode("utf-8", "replace")
    except Exception as e:
        warn(f"stooq fetch failed: {e}")
        return None
    lines = raw.strip().splitlines()
    if len(lines) < 2 or not lines[0].lower().startswith("date"):
        return None
    rows = []
    for ln in lines[1:]:
        parts = ln.split(",")
        if len(parts) < 5:
            continue
        try:
            rows.append((parts[0], round(float(parts[4]), 4)))
        except ValueError:
            continue
    return rows or None


def fetch_spy_incremental(skip_fetch, cache_path=RAW_CACHE):
    """回傳升冪 [(date, close), ...]。skip_fetch=True 時只讀本地 cache_path。
    首次（cache 無 SPY 序列）bootstrap 10 年；之後每次只 topup 近 30 天並與既有序列合併去重
    （照抄 scripts/build_flowmap.py build_price_cache() 的 incremental 慣例）。"""
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"could not read {cache_path.name}: {e}")
            cache = {}
    series = cache.get("series", {})
    existing = series.get(SPY_TICKER) or []

    if skip_fetch:
        if not existing:
            raise SystemExit(f"--skip-fetch 但 {cache_path} 無 {SPY_TICKER} 快取，無法離線重算")
        return [(d, c) for d, c in existing]

    has_existing = bool(existing)
    period = FETCH_PERIOD_TOPUP if has_existing else FETCH_PERIOD_BOOTSTRAP
    label = "topup" if has_existing else "bootstrap"

    got, src = None, None
    for attempt in range(3):
        try:
            got = _yf_daily(SPY_TICKER, period=period)
            if got:
                src = "yfinance"
                break
        except Exception as e:
            warn(f"yfinance {label} attempt {attempt + 1} failed: {e}")
    if not got:
        got = _stooq_daily(SPY_TICKER)
        if got:
            src = "stooq"
    if not got:
        if existing:
            warn(f"{SPY_TICKER} 抓取全數失敗（yfinance + stooq），沿用既有快取"
                 f"（{len(existing)} 筆，至 {existing[-1][0]}）")
            return [(d, c) for d, c in existing]
        raise SystemExit(f"{SPY_TICKER} 日線抓取全數失敗（yfinance + stooq）且無既有快取，中止")

    info(f"{SPY_TICKER}: {label} fetched {len(got)} daily bars via {src} ({got[0][0]} .. {got[-1][0]})")

    merged = {d: c for d, c in existing}
    for d, c in got:
        merged[d] = c
    merged_sorted = sorted(merged.items())
    series[SPY_TICKER] = merged_sorted
    cache["series"] = series
    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "build_dd_verdict_base_rates.py 專用 SPY 日線快取（獨立於 data/flowmap_prices.json，"
                "後者僅 rolling ~500 交易日、深度不足 5 年 p_clim 視窗）；incremental：首次 bootstrap "
                "10 年，之後每次只 topup 近 30 天並與既有序列合併去重，不做 rolling 裁切（本檔需要"
                "完整 10 年深度）。",
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return merged_sorted


# ═══════════════════════════════════════════════════════════════════════════
# 收盤查表（bisect，dates 已升冪且為 ISO 字串，字典序＝時間序）
# ═══════════════════════════════════════════════════════════════════════════

def _split(bars):
    return [d for d, _ in bars], [c for _, c in bars]


def _at_or_before(dates, closes, ymd):
    """最近一根 date ≤ ymd 的收盤；無則 None。語意與 knowledge/settle_outcomes.py
    `_close_at_or_before` 逐字一致，這裡用 bisect 加速（dates 已升冪排序）。"""
    idx = bisect.bisect_right(dates, ymd) - 1
    if idx < 0:
        return None
    return dates[idx], closes[idx]


def _plus_days(ymd, n):
    y, m, d = map(int, ymd.split("-"))
    return (date(y, m, d) + timedelta(days=n)).isoformat()


def _minus_years(ymd, n):
    y, m, d = map(int, ymd.split("-"))
    try:
        return date(y - n, m, d).isoformat()
    except ValueError:
        # 2/29 落在非閏年：退一天（僅影響極少數取樣邊界，不影響結論）
        return date(y - n, m, d - 1).isoformat()


# ═══════════════════════════════════════════════════════════════════════════
# weekly_cache 讀法
# ═══════════════════════════════════════════════════════════════════════════

def _load_ticker_bars(path):
    try:
        raw = json.loads(path.read_text(encoding="utf-8")).get("weekly_bars") or []
    except (OSError, json.JSONDecodeError, KeyError):
        return None
    bars = [(b["week_end"], b["close"]) for b in raw if b.get("week_end") and b.get("close")]
    bars.sort(key=lambda x: x[0])
    return bars or None


def _month_first_bars(dates, closes, start_bound, end_bound):
    """回傳每個曆月在 [start_bound, end_bound] 範圍內最早一筆 (date, close)，依月份升冪。"""
    seen = {}
    for d, c in zip(dates, closes):
        if d < start_bound or d > end_bound:
            continue
        mk = d[:7]
        if mk not in seen:
            seen[mk] = (d, c)
    return [seen[mk] for mk in sorted(seen)]


# ═══════════════════════════════════════════════════════════════════════════
# (a) p_clim：pooled 跨全部 weekly_cache ticker 的無條件頻率
# ═══════════════════════════════════════════════════════════════════════════

def compute_p_clim(spy_dates, spy_closes, today_str):
    start_bound = _minus_years(today_str, CLIM_WINDOW_YEARS)
    spy_last = spy_dates[-1] if spy_dates else None
    ticker_files = sorted(CACHE_DIR.glob("*.json"))

    results = {}
    for template, horizon_days in HORIZONS.items():
        n_hit = n_total = 0
        tickers_used = set()
        for path in ticker_files:
            ticker = path.stem
            bars = _load_ticker_bars(path)
            if not bars:
                continue
            t_dates, t_closes = _split(bars)
            last_bar_date = t_dates[-1]
            samples = _month_first_bars(t_dates, t_closes, start_bound, today_str)
            for d0, c0 in samples:
                if not c0:
                    continue
                end_date = _plus_days(d0, horizon_days)
                if last_bar_date < end_date:
                    continue  # 該 ticker 視窗尚未到期
                if not spy_last or spy_last < end_date:
                    continue  # SPY 快取尚未追上
                end_bar = _at_or_before(t_dates, t_closes, end_date)
                spy0 = _at_or_before(spy_dates, spy_closes, d0)
                spy1 = _at_or_before(spy_dates, spy_closes, end_date)
                if not end_bar or not spy0 or not spy1:
                    continue
                _, c1 = end_bar
                _, s0 = spy0
                _, s1 = spy1
                if not c0 or not s0:
                    continue
                ticker_ret = c1 / c0 - 1.0
                spy_ret = s1 / s0 - 1.0
                n_total += 1
                tickers_used.add(ticker)
                if ticker_ret > spy_ret:
                    n_hit += 1
        freq = round(n_hit / n_total, 4) if n_total else None
        results[template] = {"p_clim": freq, "n_cells": n_total, "n_hit": n_hit,
                              "n_tickers": len(tickers_used)}
    return results, start_bound, len(ticker_files)


# ═══════════════════════════════════════════════════════════════════════════
# (b) 經驗表：knowledge/settlement.json 已到期裁決筆
# ═══════════════════════════════════════════════════════════════════════════

def compute_empirical_table(spy_dates, spy_closes):
    key_by_horizon = {"dd_beat_spy_91d": "h91", "dd_beat_spy_365d": "h365"}

    if not SETTLEMENT.exists():
        note = f"{SETTLEMENT} 不存在，經驗表全 null（先跑 python knowledge/settle_outcomes.py）"
        return {t: {v: {"freq": None, "n": 0} for v in VERDICTS} for t in HORIZONS}, note

    try:
        settlement = json.loads(SETTLEMENT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {SETTLEMENT}: {e}")
        note = f"{SETTLEMENT} 讀取失敗（{e}），經驗表全 null"
        return {t: {v: {"freq": None, "n": 0} for v in VERDICTS} for t in HORIZONS}, note

    rows = settlement.get("rows") or []
    out = {}
    for template, hkey in key_by_horizon.items():
        horizon_days = HORIZONS[template]
        buckets = {v: {"n": 0, "hit": 0} for v in VERDICTS}
        for r in rows:
            verdict = r.get("verdict")
            hval = r.get(hkey)
            d0 = r.get("date")
            if verdict not in VERDICTS or hval is None or not d0:
                continue
            end_date = _plus_days(d0, horizon_days)
            spy0 = _at_or_before(spy_dates, spy_closes, d0)
            spy1 = _at_or_before(spy_dates, spy_closes, end_date)
            if not spy0 or not spy1:
                continue
            _, s0 = spy0
            _, s1 = spy1
            if not s0:
                continue
            spy_ret_pct = (s1 / s0 - 1.0) * 100
            buckets[verdict]["n"] += 1
            if hval > spy_ret_pct:
                buckets[verdict]["hit"] += 1
        out[template] = {
            v: {"freq": round(buckets[v]["hit"] / buckets[v]["n"], 4) if buckets[v]["n"] else None,
                "n": buckets[v]["n"]}
            for v in VERDICTS
        }
    note = ("經驗表樣本數以 knowledge/settlement.json 已到期（h91／h365 非 null）且 verdict 非 null "
            "的筆數為準；目前預期 n≈0（decisions.jsonl 的 verdict 欄自 2026-06-22 起才普遍存在，"
            "distance 尚不足 91／365 曆日成熟），隨每週 settle_outcomes.py 重跑自動累積，設計已知"
            "現象非 bug。producer（scripts/generate_dd_verdict_forecasts.py）CONFIG "
            "USE_EMPIRICAL_TABLE 目前恆為 False（只用下方 p_clim + PREREG offset），本表僅供觀察，"
            "只有校準輪能翻旗標改讀本表。")
    return out, note


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="DD 裁決 producer 的 base rate builder（pooled p_clim ＋ settlement.json 經驗表）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地 SPY 快取重算")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/dd_verdict_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建")
    args = ap.parse_args()

    if args.if_due:
        out_path_check = Path(args.out)
        if out_path_check.exists():
            try:
                existing = json.loads(out_path_check.read_text(encoding="utf-8"))
                built_at = existing.get("built_at")
                if built_at:
                    built_dt = datetime.strptime(built_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    age_days = (datetime.now(timezone.utc) - built_dt).total_seconds() / 86400.0
                    if age_days < IF_DUE_MAX_AGE_DAYS:
                        info(f"--if-due: {out_path_check} built_at={built_at}（{age_days:.1f} 天前）< "
                             f"{IF_DUE_MAX_AGE_DAYS} 天門檻，not due，本次不重建")
                        return
                    info(f"--if-due: {out_path_check} built_at={built_at}（{age_days:.1f} 天前）≥ "
                         f"{IF_DUE_MAX_AGE_DAYS} 天門檻，due，繼續重建")
                else:
                    info(f"--if-due: {out_path_check} 無 built_at 欄位，視為需要重建")
            except (OSError, json.JSONDecodeError, ValueError) as e:
                warn(f"--if-due: 無法讀取/解析既有 {out_path_check}（{e}），視為需要重建")
        else:
            info(f"--if-due: {out_path_check} 不存在，視為需要重建")

    if not CACHE_DIR.exists():
        raise SystemExit(f"找不到 {CACHE_DIR}")

    spy_bars = fetch_spy_incremental(args.skip_fetch)
    if not spy_bars:
        raise SystemExit("SPY 日線快取為空，中止")
    spy_dates, spy_closes = _split(spy_bars)

    today_str = datetime.now(timezone.utc).date().isoformat()

    clim_results, start_bound, n_files = compute_p_clim(spy_dates, spy_closes, today_str)
    empirical_table, empirical_note = compute_empirical_table(spy_dates, spy_closes)

    p_clim = {t: clim_results[t]["p_clim"] for t in HORIZONS}

    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "clim_window_years": CLIM_WINDOW_YEARS,
        "clim_window_start": start_bound,
        "clim_window_end": today_str,
        "p_clim": p_clim,
        "p_clim_cells": {t: {"n_cells": clim_results[t]["n_cells"], "n_hit": clim_results[t]["n_hit"],
                              "n_tickers": clim_results[t]["n_tickers"]} for t in HORIZONS},
        "p_clim_definition": (
            "對 data/weekly_cache/ 全部 ticker，取近 5 年（clim_window_years）每個曆月首個可得"
            "週線收盤為取樣點，算「該取樣點起 91／365 曆日後 ticker 報酬 > SPY 同窗報酬」的 "
            "pooled 無條件頻率（跨全部 ticker、跨全部取樣月合併計）；SPY 收盤自本檔專用 "
            "data/dd_verdict_base_rates_raw_cache.json 10 年日線讀取。ticker／SPY 兩端皆採"
            "「目標日或之前最近收盤」（_at_or_before，語意同 knowledge/settle_outcomes.py "
            "_close_at_or_before）；任一端缺資料（含視窗尚未到期，即該 ticker 或 SPY 最後一根"
            "資料日 < 目標日）即跳過該 cell，不補值、不外推。"
        ),
        "empirical_table": empirical_table,
        "empirical_table_note": empirical_note,
        "spy_data_start": spy_dates[0],
        "spy_data_end": spy_dates[-1],
        "n_spy_daily_bars": len(spy_dates),
        "n_weekly_cache_files_scanned": n_files,
        "config_note": (
            "USE_EMPIRICAL_TABLE 是 producer（scripts/generate_dd_verdict_forecasts.py）的 CONFIG "
            "常數，不在本檔——本檔只負責產出上面兩張表；producer 目前恆讀 p_clim（PREREG offset "
            "表），只有校準輪可翻該旗標。"
        ),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")

    info(f"wrote {out_path}")
    info(f"SPY raw cache: {spy_dates[0]} .. {spy_dates[-1]}（{len(spy_dates)} 根日線）；"
         f"weekly_cache 掃描 {n_files} 檔；p_clim 取樣窗 {start_bound} .. {today_str}")
    for t in HORIZONS:
        c = clim_results[t]
        info(f"  p_clim[{t}] = {c['p_clim']}（n_cells={c['n_cells']} n_hit={c['n_hit']} "
             f"n_tickers={c['n_tickers']}）")
    for t in HORIZONS:
        for v in VERDICTS:
            e = empirical_table[t][v]
            info(f"  empirical[{t}][{v}] freq={e['freq']} n={e['n']}")


if __name__ == "__main__":
    main()
