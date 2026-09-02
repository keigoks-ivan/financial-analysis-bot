#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_vrp_base_rates.py — VRP（波動風險溢酬）三分位 base rate（forecast ledger v2
package C 機械餵料）。

一次性／季度手動重建（`--if-due` 供 cron 掛「季度自動重建」，慣例照抄
scripts/build_rv_base_rates.py／scripts/build_vixts_base_rates.py）。獨立自建 raw cache
`data/vrp_base_rates_raw_cache.json`（^VIX、SPY 各抓 ~10 年日線，yfinance -> stooq
fallback），**與 data/statlab_prices.json 完全解耦**（原因同前兩檔已寫明：statlab pipeline
另有 session 並行改動中，本檔避免耦合到未定案的變更；且本檔需要 ~10 年深度，
statlab_prices.json 只 rolling ~3 年）。

定義（設計稿 `notes/site-internal/root/_forecast_v2_design_20260902.md` §5.3 PREREG 凍結）
--------------------------------------------------------------------------------
  VRP_t = VIX_t² − RV21_t²
    VIX_t   = ^VIX 收盤（年化隱含波動，vol 點／百分比）
    RV21_t  = SPY 21 交易日已實現波動（年化：21 個交易日日對數報酬 sample std（ddof=1）
              ×√252×100，口徑逐字同 scripts/build_rv_base_rates.py 的
              `_sample_std`／`compute_rv21_by_index`——三處口徑必須同步變動）

取樣點：每月首個交易日（在 ^VIX 與 SPY 的共同交易日中，且該日 RV21 已可算）。
三分位切點：取樣點 VRP 的 33.3／66.7 百分位（**in-sample**——用於分類的切點本身就是從
「未來 21 與 63 個交易日皆可驗證」的那個可判斷子樣本算出，做法照抄
build_rv_base_rates.py「五分位切點用同一個可判斷樣本算」的既有慣例，非全樣本硬分位）。

輸出 data/vrp_base_rates.json：
  - per tercile（T1 最低 VRP ～ T3 最高 VRP）：{n, vrp_range, freq_up_21d, freq_up_63d}
  - p_clim = {"vrp_spy_up_21d": ..., "vrp_spy_up_63d": ...}（同一取樣點、同一窗口的無條件頻率）

up_21d／up_63d 定義：SPY 收盤在取樣點 t 之後第 21（resp. 63）個「SPY 自身交易日序列」上
的交易日 > t 當日收盤（前瞻位移用 SPY 自己的交易日曆找，不受 ^VIX 共同交易日子集壓縮，
做法照抄 scripts/build_vixts_base_rates.py 的 `evaluate_events`：用 SPY 自身 bars 的
bisect 而非 slope_ts 的共同交易日序列）。

誠實註記
--------
* **重疊樣本，非獨立樣本**：相鄰月份取樣點的 21／63 日前瞻視窗高度重疊（月頻取樣本身降低
  了重疊密度，但 63 交易日視窗仍可能跨月重疊），本表只報告經驗頻率與樣本數，不做假設檢定。
* **三分位切點 in-sample**：見上，切點來自「未來雙視窗皆可驗證」的子樣本，非滾動／擴張窗口
  即時分位，不能宣稱樣本外預測力——本表定位是 base rate 參照表，不是模型。
* ^VIX 於 stooq 的正確符號是 `^vix`（不吃 `.us` 後綴，那只用於美股個股/ETF），照抄
  scripts/build_vixts_base_rates.py 已修正過的寫法。

用法
----
  python scripts/build_vrp_base_rates.py                 完整重抓 + 重算（預設）
  python scripts/build_vrp_base_rates.py --skip-fetch     離線：只用既有本地快取重算
  python scripts/build_vrp_base_rates.py --if-due         現有輸出 built_at <85 天則跳過
                                                            （cron 用，慣例照抄 rv/vixts）
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_CACHE = DATA / "vrp_base_rates_raw_cache.json"  # 本檔專用，與 data/statlab_prices.json 解耦
OUT_JSON = DATA / "vrp_base_rates.json"

SCHEMA = "vrp-base-rates-v1"
TICKERS = ["^VIX", "SPY"]
FETCH_PERIOD = "10y"
RV_WINDOW_TRADING_DAYS = 21     # PREREG 凍結（設計稿 §5.3；口徑同 build_rv_base_rates.py）
UP_21D_TRADING_DAYS = 21        # PREREG 凍結
UP_63D_TRADING_DAYS = 63        # PREREG 凍結
TERCILE_PCTS = (33.3, 66.7)     # PREREG 凍結（設計稿 §5.3：33.3／66.7 百分位）
IF_DUE_MAX_AGE_DAYS = 85        # --if-due 門檻（慣例照抄 rv/vixts）


def warn(msg: str) -> None:
    print(f"[vrp-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[vrp-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance -> stooq fallback；獨立實作，理由同 build_rv_base_rates.py／
# build_vixts_base_rates.py 檔頭：避免耦合到並行開發中的 statlab/flowmap pipeline）
# ═══════════════════════════════════════════════════════════════════════════

def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 vrp-base-rates"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 vrp-base-rates"})
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
        # 指數代碼（^VIX）在 stooq 不吃 .us 後綴（那只用於美股個股/ETF）——
        # 照抄 scripts/build_vixts_base_rates.py 已修正過的寫法。
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
        "note": "build_vrp_base_rates.py 專用日線快取（獨立於 data/statlab_prices.json），"
                "季度手動重建，非 incremental cron。",
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return bars


def fetch_all(skip_fetch, cache_path=RAW_CACHE):
    return {t: fetch_daily_bars(t, skip_fetch, cache_path) for t in TICKERS}


# ═══════════════════════════════════════════════════════════════════════════
# RV21（年化，日對數報酬 sample std × √252 × 100）— 逐字同 build_rv_base_rates.py
# ═══════════════════════════════════════════════════════════════════════════

def _sample_std(xs):
    n = len(xs)
    if n < 2:
        return None
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / (n - 1)
    return var ** 0.5


def compute_rv21_by_index(closes, window=RV_WINDOW_TRADING_DAYS):
    """closes: 升冪收盤價列表。回傳 list（與 closes 等長）：rv21[d] = 以「日 d」為結尾的
    21 個對數報酬（closes[d-21..d] 兩兩取對數差）的年化 sample std（百分比 vol 點），
    d < window 者為 None（歷史不足）。逐字同 scripts/build_rv_base_rates.py。"""
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
# VRP 序列 + 每月首個交易日取樣
# ═══════════════════════════════════════════════════════════════════════════

def build_vrp_series(vix_bars, spy_bars):
    """回傳升冪 [(date, vrp), ...]：^VIX 與 SPY 共同交易日中、SPY RV21 已可算的日子。
    vrp = vix_close**2 - rv21**2。"""
    spy_dates = [d for d, _ in spy_bars]
    spy_closes = [c for _, c in spy_bars]
    rv21 = compute_rv21_by_index(spy_closes)
    rv21_by_date = {d: rv21[i] for i, d in enumerate(spy_dates) if rv21[i] is not None}
    vix_map = dict(vix_bars)

    common = sorted(set(vix_map) & set(rv21_by_date))
    out = []
    for d in common:
        vix_c = vix_map[d]
        rv = rv21_by_date[d]
        vrp = round(vix_c ** 2 - rv ** 2, 4)
        out.append((d, vrp))
    return out


def month_of(d):
    return d[:7]  # "YYYY-MM-DD" -> "YYYY-MM"


def sample_first_trading_day_of_month(vrp_series):
    """vrp_series: 升冪 [(date, vrp), ...]。回傳每個 YYYY-MM 的第一筆。"""
    seen = set()
    out = []
    for d, vrp in vrp_series:
        m = month_of(d)
        if m in seen:
            continue
        seen.add(m)
        out.append((d, vrp))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 前瞻視窗（用 SPY 自身交易日序列，非 ^VIX∩SPY 共同交易日子集——照抄
# build_vixts_base_rates.py evaluate_events 的 bisect 手法）
# ═══════════════════════════════════════════════════════════════════════════

def build_transition_sample(monthly_samples, spy_bars,
                             up21_days=UP_21D_TRADING_DAYS, up63_days=UP_63D_TRADING_DAYS):
    """對每個月度取樣點，找 SPY 自身交易日序列上第 21／63 個交易日後的收盤，判斷是否
    高於取樣點當日收盤。只有兩個視窗皆可驗證（資料未觸及序列尾端）才收進樣本——與
    build_rv_base_rates.py「切點與轉移頻率用同一個可判斷樣本」的既有慣例一致。
    回傳 [{"date","vrp","up_21d","up_63d"}, ...]。"""
    spy_dates = [d for d, _ in spy_bars]
    spy_closes = [c for _, c in spy_bars]
    n = len(spy_dates)

    rows = []
    for d, vrp in monthly_samples:
        pos = bisect.bisect_left(spy_dates, d)
        if pos >= n or spy_dates[pos] != d:
            # 取樣點日期理論上必為 SPY 自身交易日（來自 SPY RV21 索引），此為防禦性檢查
            continue
        idx21 = pos + up21_days
        idx63 = pos + up63_days
        if idx63 >= n:
            continue  # 63 日視窗未走完，兩個視窗皆用同一可判斷子樣本，一起排除
        base_close = spy_closes[pos]
        up_21d = spy_closes[idx21] > base_close
        up_63d = spy_closes[idx63] > base_close
        rows.append({"date": d, "vrp": vrp, "up_21d": up_21d, "up_63d": up_63d})
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


def _tercile_label(v, cutoffs):
    c33, c67 = cutoffs
    if v <= c33:
        return "T1"
    if v <= c67:
        return "T2"
    return "T3"


TERCILE_DESC = {
    "T1": "隱含波動高於已實現波動最少的一組",
    "T2": "隱含波動高於已實現波動居中的一組",
    "T3": "隱含波動高於已實現波動最多的一組",
}


def build_tercile_table(sample_rows):
    vrp_vals = sorted(r["vrp"] for r in sample_rows)
    c33, c67 = TERCILE_PCTS
    cutoffs = [round(_percentile(vrp_vals, c33), 4), round(_percentile(vrp_vals, c67), 4)]

    buckets = {t: [] for t in ("T1", "T2", "T3")}
    for r in sample_rows:
        buckets[_tercile_label(r["vrp"], cutoffs)].append(r)

    terciles = []
    for t in ("T1", "T2", "T3"):
        rows = buckets[t]
        n = len(rows)
        if n == 0:
            terciles.append({"tercile": t, "n": 0, "vrp_range": None,
                              "freq_up_21d": None, "freq_up_63d": None,
                              "description": TERCILE_DESC[t]})
            continue
        vals = [r["vrp"] for r in rows]
        freq_21 = sum(1 for r in rows if r["up_21d"]) / n
        freq_63 = sum(1 for r in rows if r["up_63d"]) / n
        terciles.append({
            "tercile": t,
            "n": n,
            "vrp_range": [round(min(vals), 2), round(max(vals), 2)],
            "freq_up_21d": round(freq_21, 3),
            "freq_up_63d": round(freq_63, 3),
            "description": TERCILE_DESC[t],
        })
    return terciles, cutoffs


def compute_p_clim(sample_rows):
    n = len(sample_rows)
    if n == 0:
        return {"vrp_spy_up_21d": None, "vrp_spy_up_63d": None}
    freq_21 = sum(1 for r in sample_rows if r["up_21d"]) / n
    freq_63 = sum(1 for r in sample_rows if r["up_63d"]) / n
    return {"vrp_spy_up_21d": round(freq_21, 3), "vrp_spy_up_63d": round(freq_63, 3)}


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="VRP 三分位 base rate builder（forecast ledger v2 package C 機械餵料）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地快取重算")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/vrp_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建"
                          "（exit 0，印 not due）；供 cron 掛「季度自動重建」用")
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
    vix_bars, spy_bars = bars["^VIX"], bars["SPY"]

    vrp_series = build_vrp_series(vix_bars, spy_bars)
    if len(vrp_series) < 60:
        raise SystemExit(f"VRP 可算樣本僅 {len(vrp_series)} 筆（^VIX∩SPY 且 RV21 可算），過少，中止")

    monthly_samples = sample_first_trading_day_of_month(vrp_series)
    sample_rows = build_transition_sample(monthly_samples, spy_bars)
    if not sample_rows:
        raise SystemExit("可驗證的月度取樣點為 0（歷史長度不足以同時算 VRP + 未來 63 交易日 SPY 收盤），中止")

    terciles, cutoffs = build_tercile_table(sample_rows)
    p_clim = compute_p_clim(sample_rows)

    payload = {
        "schema": SCHEMA,
        "tickers": TICKERS,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_start": {"^VIX": vix_bars[0][0], "SPY": spy_bars[0][0]},
        "data_end": {"^VIX": vix_bars[-1][0], "SPY": spy_bars[-1][0]},
        "n_price_days": {"^VIX": len(vix_bars), "SPY": len(spy_bars)},
        "n_vrp_series": len(vrp_series),
        "n_monthly_samples": len(monthly_samples),
        "n_transition_sample": len(sample_rows),
        "rv_window_trading_days": RV_WINDOW_TRADING_DAYS,
        "up_21d_trading_days": UP_21D_TRADING_DAYS,
        "up_63d_trading_days": UP_63D_TRADING_DAYS,
        "vrp_definition": (
            "VRP_t = VIX_t^2 - RV21_t^2；VIX_t=^VIX 收盤（年化隱含波動，vol 點）；"
            "RV21_t=SPY 21 交易日日對數報酬年化 sample std（ddof=1）×sqrt(252)×100（vol 點），"
            "口徑逐字同 scripts/build_rv_base_rates.py"
        ),
        "sampling": "每月首個交易日（^VIX 與 SPY 共同交易日、且該日 RV21 已可算的子集合）",
        "tercile_cutoffs_pct33_67": cutoffs,
        "terciles": terciles,
        "p_clim": p_clim,
        "methodology_note": (
            "三分位切點（tercile_cutoffs）用同一個可驗證子樣本（in-sample：月度取樣點中，"
            "未來 21 與 63 個 SPY 自身交易日皆可驗證者）的 33.3/66.7 百分位算出，非滾動或"
            "擴張窗口即時分位，不能宣稱樣本外預測力——本表定位是 base rate 參照表，不是模型。"
            "up_21d／up_63d 前瞻位移用 SPY 自身交易日序列（bisect 定位），不受 ^VIX 共同交易日"
            "子集壓縮；p_clim 為同一取樣點、同一窗口下的無條件頻率（terciles 與 p_clim 共用"
            "同一個 sample_rows，滿足設計稿 §3.1「同一窗口、同一取樣點」要求）。頻率為重疊"
            "樣本估計（月頻取樣降低但未消除 63 交易日視窗的跨月重疊），不做假設檢定。"
        ),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    info(f"wrote {out_path} — {len(sample_rows)} 筆可驗證月度觀測，"
         f"VRP 序列 {vrp_series[0][0]}..{vrp_series[-1][0]}（{len(vrp_series)} 筆）")
    info(f"  tercile_cutoffs(33.3/66.7)={cutoffs}")
    for t in terciles:
        info(f"  {t['tercile']}: n={t['n']:<4} range={t['vrp_range']}  "
             f"freq_up_21d={t['freq_up_21d']}  freq_up_63d={t['freq_up_63d']}  "
             f"({t['description']})")
    info(f"  p_clim={p_clim}")


if __name__ == "__main__":
    main()
