#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_vixts_base_rates.py — VIX 期限結構倒掛 base rate（forecast ledger G5 vix-model 機械餵料）。

一次性／季度手動重建（`--if-due` 供 cron 掛「季度自動重建」，慣例照抄
scripts/build_rv_base_rates.py）。獨立自建 raw cache `data/vixts_base_rates_raw_cache.json`
（^VIX／^VIX3M／SPY 各抓 ~10 年日線，yfinance -> stooq fallback），**與
data/statlab_prices.json 完全解耦**（該檔由 scripts/build_statlab.py 另一條 pipeline 維護，
本檔不讀不寫、只自己抓）——原因同 build_rv_base_rates.py 檔頭已寫明的理由：statlab pipeline
另有 session 並行改動中，本檔避免耦合到未定案的變更；且 build_vixts_base_rates.py 需要
~10 年深度，statlab_prices.json 只 rolling ~3 年（850 交易日），深度本來就不夠用。

倒掛 onset 定義（PREREG 凍結，設計稿 §G3／§G5）：slope = ^VIX3M − ^VIX（收盤差）；
onset = 連續 ≥5 個交易日 slope>0，之後首個 slope<0 的交易日。

Base rate（PREREG 凍結，設計稿 §G5）：
  ① onset 後 21 個交易日內，slope 回正（>0）的頻率（any_close 語義：視窗內任一日 slope>0
     即算命中；只有當視窗內未命中且已有完整 21 個交易日資料可看時才算「未命中」，資料不足
     的事件不計入分母——見下方誠實註記）。
  ② onset 後第 63 個交易日，SPY 收盤高於 onset 當日收盤的頻率（at_expiry 語義：只看第 63
     個交易日那一點，不看中途）。

輸出 data/vixts_base_rates.json（事件數、逐事件清單、兩個頻率、資料起訖；事件數必然少
——樣本數誠實列，不足 10 個事件時 meta 標 lo，見設計稿 §G5 與交付清單原文）。

誠實註記（務必讀）
------------------
* **onset 事件彼此不重疊**（不像 rv-model base rate 的重疊 21 日視窗）——每個 onset 是一次
  離散的狀態轉換（從連續 ≥5 日 contango 轉為 inverted），同一次倒掛只算一次，這點與
  build_rv_base_rates.py 的 quintile 轉移表刻意不同，不必套用「重疊樣本」警語。
* **資料缺口會讓 streak 重新起算**：本腳本自建的 raw cache 若在某段期間兩個序列的共同交易
  日之間出現長天期缺口（例如上游 feed 一段時間沒有 ^VIX3M 報價），streak 在缺口處強制歸零
  重新起算——缺口期間實際發生過什麼無法得知，不允許 onset 判定跨過缺口去配對兩端。此safeguard
  的具體天數門檻（10 個曆日）是本腳本自行選定的資料完整性判斷，**非設計稿 PREREG 凍結值**
  （PREREG 凍結的只有 onset 定義本身的「連續 ≥5 日」），做法照抄
  scripts/build_statlab.py 的 `_vix_inversion_events` 已有先例（該檔同一問題已用同一手法
  處理，本檔獨立重寫、不 import，避免耦合到並行開發中的 statlab pipeline）。
* **實測發現（供持有人評估用）**：本腳本開發時（2026-09-01）以 yfinance 即時抓取 ^VIX3M
  10 年歷史，尾端資料本身就有缺口（非本腳本或 stooq fallback造成）——這是上游資料本身的
  限制，不是程式錯誤；若最新可用 slope 日期落後「今日」，`generate_vix_forecasts.py` 會誠實
  印出警告而不是假裝資料完整。
* ^VIX3M 於 stooq 的正確符號是 `^vix3m`（不吃 `.us` 後綴，那只用於美股個股/ETF）——本檔
  `_stooq_daily` 已處理，照抄 scripts/build_statlab.py 已修正過的寫法。

用法
----
  python scripts/build_vixts_base_rates.py                完整重抓 + 重算（預設）
  python scripts/build_vixts_base_rates.py --skip-fetch    離線：只用既有本地快取重算
  python scripts/build_vixts_base_rates.py --if-due        現有輸出 built_at <85 天則跳過
                                                             （cron 用，設計稿 §F3 慣例）
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_CACHE = DATA / "vixts_base_rates_raw_cache.json"  # 本檔專用，與 data/statlab_prices.json 解耦
OUT_JSON = DATA / "vixts_base_rates.json"

SCHEMA = "vixts-base-rates-v1"
TICKERS = ["^VIX", "^VIX3M", "SPY"]
FETCH_PERIOD = "10y"
ONSET_STREAK_DAYS = 5          # PREREG 凍結（設計稿 §G3：連續 ≥5 日 slope>0 後首個 <0）
RECOVERY_WINDOW_TRADING_DAYS = 21   # PREREG 凍結（設計稿 §G5）
SPY_WINDOW_TRADING_DAYS = 63        # PREREG 凍結（設計稿 §G5）
GAP_THRESHOLD_CALENDAR_DAYS = 10    # 本腳本自選的資料完整性 safeguard，非 PREREG 凍結值（見檔頭）
IF_DUE_MAX_AGE_DAYS = 85            # --if-due 門檻（設計稿 §F3：季度自動重建）
LOW_SAMPLE_EVENT_THRESHOLD = 10     # 事件數 <10 → meta 標 lo（任務交付清單原文）


def warn(msg: str) -> None:
    print(f"[vixts-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[vixts-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance -> stooq fallback；獨立實作，不 import build_statlab.py／
# build_rv_base_rates.py，理由見檔頭 docstring）
# ═══════════════════════════════════════════════════════════════════════════

def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 vixts-base-rates"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 vixts-base-rates"})
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
        # 指數代碼（^VIX／^VIX3M）在 stooq 不吃 .us 後綴（那只用於美股個股/ETF）——
        # 照抄 scripts/build_statlab.py 已修正過的寫法。
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
    """回傳升冪 [(date, close), ...]。skip_fetch=True 時只讀本地 cache_path。
    多個 ticker 共用同一 cache_path，累積寫入 cache["series"][ticker]。"""
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
        "tickers": TICKERS,
        "note": "build_vixts_base_rates.py 專用日線快取（獨立於 data/statlab_prices.json），"
                "季度手動重建，非 incremental cron。",
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return bars


def fetch_all(skip_fetch, cache_path=RAW_CACHE):
    return {t: fetch_daily_bars(t, skip_fetch, cache_path) for t in TICKERS}


# ═══════════════════════════════════════════════════════════════════════════
# onset 事件偵測（§G3 PREREG 凍結定義 + 資料缺口 safeguard）
# ═══════════════════════════════════════════════════════════════════════════

def build_slope_series(vix_bars, vix3m_bars):
    """兩序列共同交易日的 slope = vix3m - vix，升冪 [(date, slope), ...]。"""
    vix = dict(vix_bars)
    vix3m = dict(vix3m_bars)
    common = sorted(set(vix) & set(vix3m))
    return [(d, round(vix3m[d] - vix[d], 4)) for d in common]


def find_onset_events(slope_ts, streak_days=ONSET_STREAK_DAYS,
                       gap_threshold_days=GAP_THRESHOLD_CALENDAR_DAYS):
    """slope_ts: 依日期升冪排序的 (date, slope) 序列。
    onset = 連續 ≥streak_days 個交易日 slope>0，之後首個 slope<0 的交易日（PREREG 凍結，
    設計稿 §G3）。回傳 onset 事件的序列索引清單 [(idx, date, slope), ...]。

    資料缺口 safeguard（本腳本自選，非 PREREG）：相鄰兩筆資料日曆日差 > gap_threshold_days
    視為上游 feed 出現長天期缺口，streak 在缺口處強制歸零重新起算，避免把「資料沒有」誤判成
    「連續站在正值」。做法照抄 scripts/build_statlab.py 的 `_vix_inversion_events` 先例。"""
    events = []
    consec_pos = 0
    n = len(slope_ts)
    for i in range(n):
        d, s = slope_ts[i]
        if i > 0:
            prev_d = slope_ts[i - 1][0]
            gap_days = (date.fromisoformat(d) - date.fromisoformat(prev_d)).days
            if gap_days > gap_threshold_days:
                consec_pos = 0
        if s > 0:
            consec_pos += 1
            continue
        if s < 0:
            if consec_pos >= streak_days:
                events.append((i, d, s))
            consec_pos = 0
        else:  # s == 0：既不算正也不算負，中止 streak（罕見，浮點收盤差恰為 0）
            consec_pos = 0
    return events


# ═══════════════════════════════════════════════════════════════════════════
# base rate 計算
# ═══════════════════════════════════════════════════════════════════════════

def evaluate_events(onset_events, slope_ts, spy_bars):
    """對每個 onset 事件算兩個 base rate 觀測值：
    ① 21 個交易日內（slope_ts 上）slope 是否回正（>0）——any_close 語義。
    ② onset 當日起第 63 個交易日（spy_bars 上，需先在 spy_bars 找到 onset 當日或其後最近
       交易日的索引）SPY 收盤是否高於 onset 當日收盤——at_expiry 語義。
    回傳逐事件清單 + 兩個彙總頻率（分母只計「資料足以判定」的事件，見誠實註記）。"""
    n_slope = len(slope_ts)
    spy_dates = [d for d, _ in spy_bars]
    spy_map = dict(spy_bars)

    events_out = []
    n_recovery_valid = n_recovery_hit = 0
    n_spy_valid = n_spy_hit = 0

    for idx, onset_date, onset_slope in onset_events:
        # ① 21 個交易日內 slope 回正
        window_end = min(idx + RECOVERY_WINDOW_TRADING_DAYS, n_slope - 1)
        future = slope_ts[idx + 1:window_end + 1]
        recovered = any(v > 0 for _, v in future)
        full_window_available = (n_slope - 1) >= idx + RECOVERY_WINDOW_TRADING_DAYS
        if recovered:
            recovery_valid = True
            n_recovery_valid += 1
            n_recovery_hit += 1
        elif full_window_available:
            recovery_valid = True
            n_recovery_valid += 1
        else:
            recovery_valid = False  # 資料不足以判定「未回正」，不計入分母

        # ② 第 63 個交易日 SPY 是否高於 onset 當日收盤
        # onset_date 在 spy_bars 上找同日或其後最近交易日（VIX 與 SPY 理論上同交易日曆，
        # 容許極少數不同步時仍能對齊）。
        import bisect
        spy_start_pos = bisect.bisect_left(spy_dates, onset_date)
        spy_valid = False
        spy_hit = None
        spy_ret_pct = None
        if spy_start_pos < len(spy_dates):
            entry_price = spy_map[spy_dates[spy_start_pos]]
            exit_pos = spy_start_pos + SPY_WINDOW_TRADING_DAYS
            if exit_pos < len(spy_dates):
                exit_price = spy_map[spy_dates[exit_pos]]
                spy_valid = True
                spy_hit = exit_price > entry_price
                spy_ret_pct = round((exit_price / entry_price - 1.0) * 100, 2)
                n_spy_valid += 1
                if spy_hit:
                    n_spy_hit += 1

        events_out.append({
            "onset_date": onset_date,
            "onset_slope": onset_slope,
            "recovered_within_21td": recovered if recovery_valid else None,
            "recovery_sample_valid": recovery_valid,
            "spy_higher_63td": spy_hit,
            "spy_return_63td_pct": spy_ret_pct,
            "spy_sample_valid": spy_valid,
        })

    freq_recovery = round(n_recovery_hit / n_recovery_valid, 3) if n_recovery_valid else None
    freq_spy_higher = round(n_spy_hit / n_spy_valid, 3) if n_spy_valid else None

    return events_out, {
        "n_events_total": len(onset_events),
        "n_recovery_valid": n_recovery_valid,
        "n_recovery_hit": n_recovery_hit,
        "freq_recovery_within_21td": freq_recovery,
        "n_spy_valid": n_spy_valid,
        "n_spy_hit": n_spy_hit,
        "freq_spy_higher_after_63td": freq_spy_higher,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="VIX 期限結構倒掛 base rate builder（forecast ledger G5 vix-model 機械餵料）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地快取重算")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/vixts_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建"
                          "（exit 0，印 not due）；供 cron 掛「季度自動重建」用（設計稿 §F3）")
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

    bars = fetch_all(args.skip_fetch)
    vix_bars, vix3m_bars, spy_bars = bars["^VIX"], bars["^VIX3M"], bars["SPY"]

    slope_ts = build_slope_series(vix_bars, vix3m_bars)
    if len(slope_ts) < 30:
        raise SystemExit("^VIX／^VIX3M 共同交易日不足 30 筆，中止（資料異常）")

    onset_events = find_onset_events(slope_ts)
    events_out, summary = evaluate_events(onset_events, slope_ts, spy_bars)

    n_events = summary["n_events_total"]
    confidence = "lo" if n_events < LOW_SAMPLE_EVENT_THRESHOLD else "med"

    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tickers": TICKERS,
        "data_start": {"^VIX": vix_bars[0][0], "^VIX3M": vix3m_bars[0][0], "SPY": spy_bars[0][0]},
        "data_end": {"^VIX": vix_bars[-1][0], "^VIX3M": vix3m_bars[-1][0], "SPY": spy_bars[-1][0]},
        "slope_common_dates_start": slope_ts[0][0],
        "slope_common_dates_end": slope_ts[-1][0],
        "n_slope_obs": len(slope_ts),
        "onset_streak_days": ONSET_STREAK_DAYS,
        "recovery_window_trading_days": RECOVERY_WINDOW_TRADING_DAYS,
        "spy_window_trading_days": SPY_WINDOW_TRADING_DAYS,
        "gap_threshold_calendar_days_note": (
            f"{GAP_THRESHOLD_CALENDAR_DAYS}（本腳本自選之資料完整性 safeguard，非設計稿 PREREG "
            f"凍結值——PREREG 凍結的只有 onset「連續 ≥{ONSET_STREAK_DAYS} 日」本身的定義）"),
        "n_events": n_events,
        "confidence": confidence,
        "confidence_note": (
            f"事件數 {n_events} {'< ' + str(LOW_SAMPLE_EVENT_THRESHOLD) + '，樣本過薄標 lo' if confidence == 'lo' else '≥ ' + str(LOW_SAMPLE_EVENT_THRESHOLD)}"
            "——倒掛 onset 本質上是稀疏事件（離散狀態轉換，非重疊視窗），事件數必然遠少於"
            "rv-model 的五分位轉移表樣本數，此為預期中的資料現實，不是程式錯誤。"),
        "freq_recovery_within_21td": summary["freq_recovery_within_21td"],
        "n_recovery_valid": summary["n_recovery_valid"],
        "n_recovery_hit": summary["n_recovery_hit"],
        "freq_spy_higher_after_63td": summary["freq_spy_higher_after_63td"],
        "n_spy_valid": summary["n_spy_valid"],
        "n_spy_hit": summary["n_spy_hit"],
        "events": events_out,
        "methodology_note": (
            "onset 事件彼此不重疊（離散狀態轉換），與 rv-model base rate 的重疊 21 日視窗性質"
            "不同，不需要「重疊樣本」警語；但兩個 base rate 頻率各自的分母排除「資料不足以判定"
            "」的事件（即視窗尚未走完、且視窗內未提前命中的最近期事件），詳見逐事件清單"
            "recovery_sample_valid／spy_sample_valid 兩個旗標。"),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    info(f"wrote {out_path} — {n_events} 個 onset 事件，slope 共同交易日 "
         f"{slope_ts[0][0]}..{slope_ts[-1][0]}（{len(slope_ts)} 筆）")
    info(f"  freq_recovery_within_21td={summary['freq_recovery_within_21td']} "
         f"(n_valid={summary['n_recovery_valid']}, n_hit={summary['n_recovery_hit']})")
    info(f"  freq_spy_higher_after_63td={summary['freq_spy_higher_after_63td']} "
         f"(n_valid={summary['n_spy_valid']}, n_hit={summary['n_spy_hit']})")
    info(f"  confidence={confidence}")


if __name__ == "__main__":
    main()
