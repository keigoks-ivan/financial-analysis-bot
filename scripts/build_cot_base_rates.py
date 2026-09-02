#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_cot_base_rates.py — COT 權益三指數極端部位 base rate（forecast ledger G5 cot-model
機械餵料）。

一次性／季度手動重建（`--if-due` 供 cron 掛「季度自動重建」，慣例照抄
scripts/build_rv_base_rates.py／build_vixts_base_rates.py）。**唯讀消費**
data/cot_history.json（由 scripts/build_crowding.py 維護，本檔不寫入該檔），只對權益三指數
（S&P 500 E-mini／Nasdaq-100 E-mini／Russell 2000 E-mini，設計稿 §G4／§G5 凍結範圍）計算：

  ① 每市場 net_pct_oi 的滾動 3 年（156 週）分位（inclusive percentile，口徑照抄
     scripts/build_crowding.py 的 `pctile_incl` 與 scripts/build_statlab.py 的 COT 模組
     ——`vals[i-155:i+1]` 156 週視窗，本腳本獨立重寫、不 import，理由同
     build_rv_base_rates.py 檔頭：避免耦合到並行開發中的其他 pipeline）。
  ② 歷史極端事件（PREREG 凍結，設計稿 §G4：分位 ≥95 或 ≤5）——極端偏多（long）事件的「反向
     」定義為事件後 20 個交易日價格下跌；極端偏空（short）事件為事件後 20 個交易日價格上漲
     （均值回歸方向的最小定義）。
  ③ 每事件後 20 個交易日（≈4 週）價格反向頻率，分市場＋pooled（三市場合併）。

價格資料：**自建 raw cache** `data/cot_base_rates_raw_cache.json`（SPY／QQQ／IWM 各抓 ~6 年
日線，yfinance -> stooq fallback），**與 data/flowmap_prices.json 解耦**——理由：
data/cot_history.json 回溯到 2021-01-05（~5.7 年），但 data/flowmap_prices.json 只 rolling
~500 交易日（~2 年），深度不足以驗證 2021–2024 的早期事件，故自抓 6 年日線（任務交付清單
原文：「歷史深度不足以覆蓋 2021 起全部事件時，改抓自家 raw cache ~6 年日線」）。

輸出 data/cot_base_rates.json（分市場＋pooled，事件數必列，樣本薄標 lo）。

誠實註記（務必讀）
------------------
* **COT 資料自 2021 年起僅約 5.7 年，3 年滾動分位需滿 156 週才成立**——可判定事件集中在
  近 1–3 年，樣本數天生偏少（此為 data/cot_history.json 本身的資料深度限制，非本腳本問題，
  scripts/build_statlab.py 的 COT 模組已有相同 caveat 措辭，本檔重複強調）。
* **同一市場連續數週維持極端時，每週皆各記一筆事件**——事件之間並非互相獨立樣本（與
  build_rv_base_rates.py 的重疊 21 日視窗性質類似，但這裡重疊的是「連續處於極端分位的相鄰
  週」，不是同一種重疊機制，仍屬非獨立樣本，不做假設檢定）。
* 事件的價格驗證窗＝onset 事件日之後 **20 個交易日**（在自建 6 年日線快取上直接用交易日
  索引位移，非曆日近似）——這與 scripts/build_statlab.py 自己的 COT 模組（用 +28 曆日找最
  近可得交易日）是兩種不同但皆合理的「4 週」操作化，本檔刻意採用交易日索引位移法，因為任務
  交付清單原文明寫「20 交易日」。兩種操作化在數值上會有些微差異，非錯誤，屬設計選擇的透明
  揭露（CLAUDE.md「規則衝突不得默默調和」——此處選交易日索引法是因為交付清單明文「20 交易
  日」，statlab 頁面的曆日近似法留在該模組不動，不做混用）。

用法
----
  python scripts/build_cot_base_rates.py                完整重抓 + 重算（預設）
  python scripts/build_cot_base_rates.py --skip-fetch    離線：只用既有本地快取重算
  python scripts/build_cot_base_rates.py --if-due        現有輸出 built_at <85 天則跳過
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
COT_HISTORY = DATA / "cot_history.json"        # 唯讀，scripts/build_crowding.py 維護
RAW_CACHE = DATA / "cot_base_rates_raw_cache.json"  # 本檔專用，與 data/flowmap_prices.json 解耦
OUT_JSON = DATA / "cot_base_rates.json"

SCHEMA = "cot-base-rates-v1"
FETCH_PERIOD = "6y"
IF_DUE_MAX_AGE_DAYS = 85            # --if-due 門檻（設計稿 §F3 慣例）
LOW_SAMPLE_EVENT_THRESHOLD = 20     # 事件數 <20 → confidence=lo（呼應 rv-model／設計稿 §E3 的
                                     # resolved≥20 筆門檻精神；COT 本身樣本天生薄，任務交付清單
                                     # 明文「樣本薄標 lo」，本腳本選定此數字供持有人複審）

# PREREG 凍結（設計稿 §G4）
PCTILE_WINDOW_WEEKS = 156           # 3 年分位視窗（週，52×3）——與 scripts/build_statlab.py
                                     # COT_PCTILE_WINDOW_WEEKS／scripts/build_crowding.py
                                     # win3=vals[-156:] 口徑一致
EXTREME_HI = 95
EXTREME_LO = 5
LOOKAHEAD_TRADING_DAYS = 20         # ≈4 週（任務交付清單原文「20 交易日」）

EQUITY_MARKETS = {
    "13874A": {"label": "S&P 500 E-mini", "proxy": "SPY"},
    "209742": {"label": "Nasdaq-100 E-mini", "proxy": "QQQ"},
    "239742": {"label": "Russell 2000 E-mini", "proxy": "IWM"},
}
PRICE_TICKERS = sorted({m["proxy"] for m in EQUITY_MARKETS.values()})


def warn(msg: str) -> None:
    print(f"[cot-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[cot-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance -> stooq fallback；獨立實作，理由見檔頭 docstring）
# ═══════════════════════════════════════════════════════════════════════════

def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 cot-base-rates"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 cot-base-rates"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


def _yf_daily(ticker, period=FETCH_PERIOD):
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
    if sym.startswith("^"):
        pass
    elif "." not in sym:
        sym = sym + ".us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
    try:
        raw = _http_get(url, timeout=30).decode("utf-8", "replace")
    except Exception as e:
        warn(f"stooq fetch failed for {ticker}: {e}")
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


def fetch_daily_bars(ticker, skip_fetch, cache_path=RAW_CACHE):
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"could not read {cache_path.name}: {e}")
            cache = {}
    series = cache.get("series", {})

    if skip_fetch:
        rows = series.get(ticker)
        if not rows:
            raise SystemExit(f"--skip-fetch 但 {cache_path} 無 {ticker} 快取，無法離線重算")
        return [(d, c) for d, c in rows]

    bars = None
    src = None
    for attempt in range(3):
        try:
            bars = _yf_daily(ticker)
            if bars:
                src = "yfinance"
                break
        except Exception as e:
            warn(f"yfinance attempt {attempt + 1} failed for {ticker}: {e}")
    if not bars:
        bars = _stooq_daily(ticker)
        if bars:
            src = "stooq"
    if not bars:
        raise SystemExit(f"{ticker} 日線抓取全數失敗（yfinance + stooq），中止")

    info(f"{ticker}: fetched {len(bars)} daily bars via {src} ({bars[0][0]} .. {bars[-1][0]})")

    series[ticker] = bars
    cache["series"] = series
    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tickers": PRICE_TICKERS,
        "note": "build_cot_base_rates.py 專用日線快取（獨立於 data/flowmap_prices.json），"
                "季度手動重建，非 incremental cron。",
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return bars


def fetch_all(skip_fetch, cache_path=RAW_CACHE):
    return {t: fetch_daily_bars(t, skip_fetch, cache_path) for t in PRICE_TICKERS}


# ═══════════════════════════════════════════════════════════════════════════
# percentile（照抄 scripts/build_crowding.py pctile_incl 定義）
# ═══════════════════════════════════════════════════════════════════════════

def pctile_incl(values, x):
    """Inclusive percentile rank（≤x 的比例，0..100）——與 scripts/build_crowding.py 的
    pctile_incl 逐字一致（獨立重寫，不 import，理由同檔頭）。"""
    v = [z for z in values if z is not None]
    n = len(v)
    if n == 0 or x is None:
        return None
    return round(100.0 * sum(1 for z in v if z <= x) / n, 1)


# ═══════════════════════════════════════════════════════════════════════════
# 極端事件偵測
# ═══════════════════════════════════════════════════════════════════════════

def find_extreme_events(dates, vals, window=PCTILE_WINDOW_WEEKS, hi=EXTREME_HI, lo=EXTREME_LO):
    """回傳 [(date, direction, pctile), ...]，direction ∈ {"long","short"}。
    只對「有完整 window 週trailing 資料」的週計算分位（i >= window-1），與
    scripts/build_statlab.py cot_module 的 `for i in range(COT_PCTILE_WINDOW_WEEKS-1, len(vals))`
    寫法一致。"""
    events = []
    n = len(vals)
    for i in range(window - 1, n):
        w = vals[i - window + 1:i + 1]
        p = pctile_incl(w, vals[i])
        if p is None:
            continue
        if p >= hi:
            events.append((dates[i], "long", p))
        elif p <= lo:
            events.append((dates[i], "short", p))
    return events


def evaluate_events(events, price_bars, lookahead=LOOKAHEAD_TRADING_DAYS):
    """price_bars: 升冪 [(date, close), ...]。回傳 (events_out, summary)。
    entry：event date 或其後最近一個交易日；exit：entry 之後第 lookahead 個交易日。
    兩者皆須存在於 price_bars 範圍內才計入分母（見誠實註記）。"""
    price_dates = [d for d, _ in price_bars]
    price_map = dict(price_bars)
    events_out = []
    n_valid = n_hit = n_skipped = 0

    for ev_date, direction, pctile in events:
        entry_pos = bisect.bisect_left(price_dates, ev_date)
        if entry_pos >= len(price_dates):
            n_skipped += 1
            events_out.append({"event_date": ev_date, "direction": direction, "pctile": pctile,
                               "valid": False, "skip_reason": "no_price_on_or_after_event"})
            continue
        exit_pos = entry_pos + lookahead
        if exit_pos >= len(price_dates):
            n_skipped += 1
            events_out.append({"event_date": ev_date, "direction": direction, "pctile": pctile,
                               "valid": False, "skip_reason": "insufficient_forward_data"})
            continue
        entry_date, entry_price = price_dates[entry_pos], price_map[price_dates[entry_pos]]
        exit_date, exit_price = price_dates[exit_pos], price_map[price_dates[exit_pos]]
        ret_pct = round((exit_price / entry_price - 1.0) * 100, 2)
        hit = (ret_pct < 0) if direction == "long" else (ret_pct > 0)
        n_valid += 1
        if hit:
            n_hit += 1
        events_out.append({
            "event_date": ev_date, "direction": direction, "pctile": pctile,
            "entry_date": entry_date, "exit_date": exit_date,
            "return_pct_20td": ret_pct, "reversal_hit": hit, "valid": True,
        })

    hit_rate = round(n_hit / n_valid, 3) if n_valid else None
    return events_out, {"n_events_total": len(events), "n_valid": n_valid, "n_hit": n_hit,
                        "n_skipped": n_skipped, "reversal_hit_rate": hit_rate}


# ═══════════════════════════════════════════════════════════════════════════
# forecast v2 設計稿 §5.1：頂層 p_clim（無條件、全樣本日取樣，每檔 SPY/QQQ/IWM 各自算）
# ═══════════════════════════════════════════════════════════════════════════

def compute_unconditional_px_dir_freq(bars, lookahead=LOOKAHEAD_TRADING_DAYS):
    """在 bars（自建 6 年日線快取）的每一個交易日起算：第 lookahead 個交易日後收盤相對今日
    上漲／下跌的無條件頻率——與 evaluate_events() 用同一個 lookahead（20 交易日）、同一份
    價格快取，差別只在取樣點放寬到全樣本日（不需要 COT 極端事件觸發）。"""
    closes = [c for _, c in bars]
    n = len(bars)
    n_valid = n_up = n_down = 0
    for i in range(n):
        j = i + lookahead
        if j >= n:
            continue
        n_valid += 1
        if closes[j] > closes[i]:
            n_up += 1
        elif closes[j] < closes[i]:
            n_down += 1
    freq_up = round(n_up / n_valid, 3) if n_valid else None
    freq_down = round(n_down / n_valid, 3) if n_valid else None
    return freq_up, freq_down, n_valid


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="COT 權益三指數極端部位 base rate builder（forecast ledger G5 cot-model 機械餵料）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地快取重算")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/cot_base_rates.json）")
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

    if not COT_HISTORY.exists():
        raise SystemExit(f"找不到 {COT_HISTORY}（scripts/build_crowding.py 維護），中止")
    cot_history = json.loads(COT_HISTORY.read_text(encoding="utf-8"))
    markets_map = cot_history.get("markets") or {}
    methodology = (cot_history.get("meta") or {}).get("methodology", "")

    price_bars = fetch_all(args.skip_fetch)

    by_market = []
    pooled_n_events = pooled_n_valid = pooled_n_hit = pooled_n_skipped = 0
    all_events_out = {}

    for code, meta in EQUITY_MARKETS.items():
        label, proxy = meta["label"], meta["proxy"]
        m = markets_map.get(code)
        if not m or not m.get("series"):
            warn(f"{COT_HISTORY} 找不到市場 {code}（{label}），略過")
            by_market.append({"code": code, "label": label, "proxy": proxy,
                              "n_events_total": 0, "n_valid": 0, "n_hit": 0,
                              "n_skipped": 0, "reversal_hit_rate": None,
                              "note": "cot_history.json 無此市場資料"})
            continue
        s = sorted(tuple(pt) for pt in m["series"])
        dates = [d for d, _ in s]
        vals = [v for _, v in s]
        if len(vals) < PCTILE_WINDOW_WEEKS:
            warn(f"{label}：COT 週線僅 {len(vals)} 週（<{PCTILE_WINDOW_WEEKS}），"
                 f"尚無法算出任何滿 3 年視窗的分位，事件數將為 0")

        events = find_extreme_events(dates, vals)
        bars = price_bars.get(proxy) or []
        events_out, summary = evaluate_events(events, bars)
        all_events_out[code] = events_out

        by_market.append({
            "code": code, "label": label, "proxy": proxy,
            "n_cot_weeks": len(vals),
            "n_events_total": summary["n_events_total"],
            "n_valid": summary["n_valid"],
            "n_hit": summary["n_hit"],
            "n_skipped": summary["n_skipped"],
            "reversal_hit_rate": summary["reversal_hit_rate"],
        })
        pooled_n_events += summary["n_events_total"]
        pooled_n_valid += summary["n_valid"]
        pooled_n_hit += summary["n_hit"]
        pooled_n_skipped += summary["n_skipped"]

    pooled_hit_rate = round(pooled_n_hit / pooled_n_valid, 3) if pooled_n_valid else None
    confidence = "lo" if pooled_n_valid < LOW_SAMPLE_EVENT_THRESHOLD else "med"

    p_clim_up, p_clim_down, p_clim_n = {}, {}, {}
    for t in PRICE_TICKERS:
        fu, fd, nv = compute_unconditional_px_dir_freq(price_bars.get(t) or [])
        p_clim_up[t] = fu
        p_clim_down[t] = fd
        p_clim_n[t] = nv
    p_clim = {"px_up_20d": p_clim_up, "px_down_20d": p_clim_down}

    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cot_history_methodology": methodology,
        "pctile_window_weeks": PCTILE_WINDOW_WEEKS,
        "extreme_thresholds": {"hi": EXTREME_HI, "lo": EXTREME_LO},
        "lookahead_trading_days": LOOKAHEAD_TRADING_DAYS,
        "definition": ("COT 報告週淨部位 3 年滾動分位（156 週視窗）達 ≥95（極端偏多）或 ≤5"
                       "（極端偏空）時記一筆事件；偏多事件以「事件週最近可得交易日起 20 個"
                       "交易日後價格下跌」為反向命中，偏空事件以「同窗價格上漲」為命中。"),
        "by_market": by_market,
        "pooled": {
            "n_events_total": pooled_n_events, "n_valid": pooled_n_valid,
            "n_hit": pooled_n_hit, "n_skipped": pooled_n_skipped,
            "reversal_hit_rate": pooled_hit_rate,
        },
        "confidence": confidence,
        "confidence_note": (
            f"pooled n_valid={pooled_n_valid} "
            f"{'< ' + str(LOW_SAMPLE_EVENT_THRESHOLD) + '，樣本薄標 lo' if confidence == 'lo' else '≥ ' + str(LOW_SAMPLE_EVENT_THRESHOLD)}"
            "——COT 資料自 2021 年起僅約 5.7 年，3 年滾動分位需滿 156 週才成立，可判定事件"
            "集中在近 1–3 年，樣本數天生偏少；同一市場連續數週維持極端時每週各記一筆，事件"
            "之間並非互相獨立樣本，不做假設檢定。"),
        "price_data_start": {t: price_bars[t][0][0] for t in PRICE_TICKERS if price_bars.get(t)},
        "price_data_end": {t: price_bars[t][-1][0] for t in PRICE_TICKERS if price_bars.get(t)},
        "events_by_market": all_events_out,
        "p_clim": p_clim,
        "p_clim_n": p_clim_n,
        "p_clim_note": (
            "forecast v2 設計稿 §5.1：無條件（unconditional）頻率——在自建 6 年日線快取的每一"
            "個交易日（不需要 COT 極端事件觸發）起算 20 個交易日後價格漲跌，與 lookahead_"
            "trading_days／事件驅動的 reversal_hit_rate 用同一個 lookahead 與同一份價格快取，"
            "差別只在取樣點放寬到全樣本日。"
        ),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    info(f"wrote {out_path}")
    for row in by_market:
        info(f"  {row['label']} ({row['code']}): n_events_total={row['n_events_total']} "
             f"n_valid={row.get('n_valid')} n_hit={row.get('n_hit')} "
             f"reversal_hit_rate={row.get('reversal_hit_rate')}")
    info(f"  pooled: n_valid={pooled_n_valid} n_hit={pooled_n_hit} reversal_hit_rate={pooled_hit_rate} "
         f"confidence={confidence}")
    info(f"  p_clim（unconditional）: {p_clim}（n_valid={p_clim_n}）")


if __name__ == "__main__":
    main()
