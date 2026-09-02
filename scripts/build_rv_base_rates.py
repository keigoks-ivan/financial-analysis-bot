#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_rv_base_rates.py — RV21 經驗轉移表（forecast ledger 的機械餵料）。

一次性／季度手動重建，不掛 cron。抓 SPY 日線 ~10 年（yfinance -> stooq fallback），
算 RV21（年化：21 個交易日日對數報酬 sample std × √252 × 100，單位＝vol 點／百分比），
建經驗轉移表：把每個歷史交易日依「當日 RV21」分五分位（Q1 最低～Q5 最高，分位切點
用同一組可判斷樣本的 20/40/60/80 百分位），對每一分位統計：

  (a) 21 個交易日後 RV21 高於當日 RV21 的頻率（freq_rv21_higher_after_21d）
  (b) 未來 21 個交易日內（不含當日，含第 21 日）RV21 觸及「當日值 +5 vol 點」以上
      的頻率（freq_touch_plus5_within_21d）

輸出 data/rv_base_rates.json。窗長 21、五分位切法、+5 vol 點門檻皆為設計稿
notes/site-internal/root/_flowmap_forecast_ledger_design_20260901.md §E3 PREREG 凍結值，
不得依單一案例調參。

誠實註記（務必讀）
------------------
* **重疊樣本，非獨立樣本**：相鄰交易日的 21 日視窗高度重疊（t 與 t+1 的 RV21 視窗共用
  20 根日線），這裡的頻率是重疊樣本的經驗估計，不是獨立試驗下的機率——傳統假設檢定的
  信賴區間公式在此不適用，本檔只報告經驗頻率與樣本數，不做顯著性檢定。
* **五分位切點用同一個可判斷樣本（in-sample）算出**，即用於分位歸類的切點本身就是從
  「有未來 21 日資料可驗證」的那個子樣本算的（見下）。這是為了让分位定義與轉移頻率統計
  用同一個母體，不是要拿全樣本（含末端無法驗證的天數）硬分位——但仍是 in-sample 切點，
  不是滾動／擴張窗口的即時分位，故不能用來宣稱「樣本外」預測力。
* **RV21 定義刻意採日對數報酬**（非 scripts/build_flowmap.py 的 vol_control_module 用
  的算術報酬）——設計稿 §E3 原文明寫「日對數報酬」，本檔與 generate_rv_forecasts.py／
  knowledge/settle_forecasts.py 的 rv: 域結算三處都用同一個對數報酬定義以確保口徑一致；
  這與 build_flowmap.py 既有 vol-control 模組的算術報酬是兩個刻意不同的定義，不做混用
  （CLAUDE.md「規則衝突不得默默調和」——此處選對數報酬是因為設計稿明文，build_flowmap.py
  的算術報酬留在原模組不動）。

用法
----
  python scripts/build_rv_base_rates.py                 完整重抓 + 重算（預設）
  python scripts/build_rv_base_rates.py --skip-fetch     離線：只用既有本地快取重算
                                                          （若無本地快取則失敗）
  python scripts/build_rv_base_rates.py --ticker QQQ     指定 ticker（預設 SPY，PREREG
                                                          僅 SPY 是設計稿範圍；其餘 ticker
                                                          供未來擴充手動測試用）
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_CACHE = DATA / "rv_base_rates_raw_cache.json"  # 本檔專用日線快取，不與 flowmap_prices.json 共用
OUT_JSON = DATA / "rv_base_rates.json"

SCHEMA = "rv-base-rates-v1"
WINDOW_TRADING_DAYS = 21          # PREREG 凍結（設計稿 §E3）
VOL_POINT_THRESHOLD = 5.0         # PREREG 凍結（+5 vol 點）
DEFAULT_TICKER = "SPY"
FETCH_PERIOD = "10y"
IF_DUE_MAX_AGE_DAYS = 85          # --if-due 門檻（設計稿 §F3：季度自動重建）


def warn(msg: str) -> None:
    print(f"[rv-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[rv-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance -> stooq fallback；獨立實作，不 import build_flowmap.py，
# 因該檔另有 session 並行改動中，本檔避免耦合到未定案的變更）
# ═══════════════════════════════════════════════════════════════════════════

def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 rv-base-rates"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 rv-base-rates"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


def _yf_daily(ticker, period=FETCH_PERIOD):
    import yfinance as yf
    df = yf.download(ticker, period=period, interval="1d", auto_adjust=True,
                      progress=False, threads=False)
    if df is None or df.empty:
        return None
    close = df["Close"]
    # yfinance 單檔下載偶爾回傳多層欄位（MultiIndex），攤平取第一欄
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


def fetch_daily_bars(ticker, skip_fetch, cache_path=RAW_CACHE):
    """回傳升冪 [(date, close), ...]。skip_fetch=True 時只讀本地 cache_path。"""
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
            warn(f"yfinance attempt {attempt + 1} failed: {e}")
    if not bars:
        bars = _stooq_daily(ticker)
        if bars:
            src = "stooq"
    if not bars:
        raise SystemExit(f"{ticker} 日線抓取全數失敗（yfinance + stooq），中止")

    info(f"{ticker}: fetched {len(bars)} daily bars via {src} "
         f"({bars[0][0]} .. {bars[-1][0]})")

    series[ticker] = bars
    cache["series"] = series
    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "build_rv_base_rates.py 專用日線快取（獨立於 data/flowmap_prices.json），"
                "季度手動重建，非 incremental cron。",
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return bars


# ═══════════════════════════════════════════════════════════════════════════
# RV21（年化，日對數報酬 sample std × √252 × 100）
# ═══════════════════════════════════════════════════════════════════════════

def _sample_std(xs):
    n = len(xs)
    if n < 2:
        return None
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / (n - 1)
    return var ** 0.5


def compute_rv21_by_index(closes, window=WINDOW_TRADING_DAYS):
    """closes: 升冪收盤價列表。回傳 list（與 closes 等長）：rv21[d] = 以「日 d」為結尾的
    21 個對數報酬（closes[d-21..d] 兩兩取對數差）的年化 sample std（百分比 vol 點），
    d < window 者為 None（歷史不足）。"""
    n = len(closes)
    rets = [math.log(closes[i] / closes[i - 1]) for i in range(1, n)
            if closes[i - 1] > 0 and closes[i] > 0]
    if len(rets) != n - 1:
        warn("偵測到非正收盤價，log return 序列長度與價格序列不一致——結果可能有輕微位移，"
             "本資料集（SPY 日線）理論上不應發生，僅防禦性檢查。")
    out = [None] * n
    for d in range(window, n):
        window_rets = rets[d - window:d]
        if len(window_rets) != window:
            continue
        s = _sample_std(window_rets)
        if s is None:
            continue
        out[d] = round(s * math.sqrt(252) * 100, 4)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 轉移表
# ═══════════════════════════════════════════════════════════════════════════

def build_transition_sample(dates, rv21, window=WINDOW_TRADING_DAYS,
                             threshold=VOL_POINT_THRESHOLD):
    """回傳每筆可驗證觀測（當日 RV21 定義、且 未來 window 個交易日的 RV21 全部定義）：
    {"date","rv21","higher_after","touch_plus_threshold"}。"""
    n = len(rv21)
    rows = []
    for d in range(n):
        cur = rv21[d]
        if cur is None:
            continue
        fut_idx = d + window
        if fut_idx >= n:
            continue
        future_window = rv21[d + 1:d + window + 1]
        if any(v is None for v in future_window):
            continue
        fut = rv21[fut_idx]
        higher = fut > cur
        touch = any(v >= cur + threshold for v in future_window)
        rows.append({"date": dates[d], "rv21": cur, "higher_after": higher, "touch_plus_threshold": touch})
    return rows


def _percentile(sorted_vals, q):
    """線性內插百分位（同 numpy 預設 'linear' method），q ∈ [0,100]。"""
    n = len(sorted_vals)
    if n == 0:
        return None
    if n == 1:
        return sorted_vals[0]
    idx = q / 100.0 * (n - 1)
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return sorted_vals[lo]
    frac = idx - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac


def _quintile_label(v, cutoffs):
    q20, q40, q60, q80 = cutoffs
    if v <= q20:
        return "Q1"
    if v <= q40:
        return "Q2"
    if v <= q60:
        return "Q3"
    if v <= q80:
        return "Q4"
    return "Q5"


def compute_pooled_p_clim(sample_rows):
    """forecast v2 設計稿 §5.1：頂層 p_clim（無條件、不分五分位的 pooled 頻率），與五分位
    轉移表用同一批 sample_rows、同一窗口（21 交易日）、同一 +5 vol 點門檻——差別只在不依
    quintile 分組，直接對整個可驗證樣本取頻率。"""
    n = len(sample_rows)
    if n == 0:
        return {"rv21_higher_21d": None, "rv21_touch_plus5_21d": None}
    freq_higher = sum(1 for r in sample_rows if r["higher_after"]) / n
    freq_touch = sum(1 for r in sample_rows if r["touch_plus_threshold"]) / n
    return {"rv21_higher_21d": round(freq_higher, 3), "rv21_touch_plus5_21d": round(freq_touch, 3)}


def build_quintile_table(sample_rows):
    rv_vals = sorted(r["rv21"] for r in sample_rows)
    cutoffs = [
        round(_percentile(rv_vals, 20), 4),
        round(_percentile(rv_vals, 40), 4),
        round(_percentile(rv_vals, 60), 4),
        round(_percentile(rv_vals, 80), 4),
    ]
    buckets = {q: [] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")}
    for r in sample_rows:
        buckets[_quintile_label(r["rv21"], cutoffs)].append(r)

    quintiles = []
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        rows = buckets[q]
        n = len(rows)
        if n == 0:
            quintiles.append({"quintile": q, "n": 0, "rv21_range": None,
                               "freq_rv21_higher_after_21d": None,
                               "freq_touch_plus5_within_21d": None})
            continue
        vals = [r["rv21"] for r in rows]
        freq_higher = sum(1 for r in rows if r["higher_after"]) / n
        freq_touch = sum(1 for r in rows if r["touch_plus_threshold"]) / n
        quintiles.append({
            "quintile": q,
            "n": n,
            "rv21_range": [round(min(vals), 2), round(max(vals), 2)],
            "freq_rv21_higher_after_21d": round(freq_higher, 2),
            "freq_touch_plus5_within_21d": round(freq_touch, 2),
        })
    return quintiles, cutoffs


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="RV21 經驗轉移表 builder（forecast ledger 機械餵料）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地快取重算")
    ap.add_argument("--ticker", default=DEFAULT_TICKER,
                     help=f"預設 {DEFAULT_TICKER}（設計稿 §E3 PREREG 範圍）")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/rv_base_rates.json）")
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

    bars = fetch_daily_bars(args.ticker, args.skip_fetch)
    dates = [d for d, _ in bars]
    closes = [c for _, c in bars]

    rv21 = compute_rv21_by_index(closes)
    sample_rows = build_transition_sample(dates, rv21)
    if not sample_rows:
        raise SystemExit(f"{args.ticker}：可驗證樣本為 0（歷史長度不足以同時算當日 RV21 + "
                          f"未來 {WINDOW_TRADING_DAYS} 交易日 RV21），中止")

    quintiles, cutoffs = build_quintile_table(sample_rows)
    p_clim = compute_pooled_p_clim(sample_rows)

    payload = {
        "schema": SCHEMA,
        "ticker": args.ticker,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_start": dates[0],
        "data_end": dates[-1],
        "n_price_days": len(closes),
        "n_transition_sample": len(sample_rows),
        "window_trading_days": WINDOW_TRADING_DAYS,
        "vol_point_threshold": VOL_POINT_THRESHOLD,
        "rv21_definition": "年化 21 交易日日對數報酬 sample std（ddof=1）× sqrt(252) × 100，單位＝vol 點（百分比）",
        "quintile_cutoffs_pct20_40_60_80": cutoffs,
        "quintiles": quintiles,
        "p_clim": p_clim,
        "p_clim_n": len(sample_rows),
        "p_clim_note": (
            "forecast v2 設計稿 §5.1：無條件（pooled，不分五分位）頻率，供 forecasts.jsonl "
            "逐筆 p_clim 欄位取值——與同檔 quintiles 用同一批可驗證樣本、同一窗口／門檻，"
            "差別只在不依 quintile 分組。"
        ),
        "methodology_note": (
            "頻率為重疊樣本估計（overlapping windows），相鄰交易日的 21 日視窗共用 20 根日線，"
            "非獨立樣本；本表只報告經驗頻率與樣本數 n，不做假設檢定，信賴區間不適用傳統獨立樣本公式。"
            "五分位切點（quintile_cutoffs）用同一個可驗證子樣本（in-sample）的 20/40/60/80 百分位算出，"
            "非滾動或擴張窗口即時分位，不能宣稱樣本外預測力——本表定位是 base rate 參照表，不是模型。"
        ),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    info(f"wrote {out_path} — {len(sample_rows)} 筆可驗證觀測，"
         f"{dates[0]}..{dates[-1]}（{len(closes)} 根日線）")
    for q in quintiles:
        info(f"  {q['quintile']}: n={q['n']:<5} range={q['rv21_range']}  "
             f"freq_higher_after_21d={q['freq_rv21_higher_after_21d']}  "
             f"freq_touch_plus5_within_21d={q['freq_touch_plus5_within_21d']}")
    info(f"  p_clim（pooled，n={len(sample_rows)}）: {p_clim}")


if __name__ == "__main__":
    main()
