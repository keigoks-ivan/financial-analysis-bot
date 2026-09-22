#!/usr/bin/env python3
"""build_stock_dash.py — zero-LLM, mechanical builder for the individual-stock
dashboard sample page (docs/stock-dash/).

Usage:
    python3.12 scripts/build_stock_dash.py NVDA

Writes docs/stock-dash/data/{TICKER}.json. All numbers are computed directly
from yfinance (price history + info + insider_transactions + option_chain)
and FINRA Reg SHO daily short-volume files. Nothing here is estimated,
guessed, or filled with placeholder values — anywhere a source is
unavailable the corresponding JSON node is written with "status":"no_data"
and a "reason" string instead of a fabricated number.

Data sources:
  - Price history / info / insider transactions / option chain: yfinance
  - Daily short volume: FINRA Reg SHO
    https://cdn.finra.org/equity/regsho/daily/CNMSshvolYYYYMMDD.txt
  - Broad-market risk gauge: docs/cache/risk_gauge.json is read directly by
    the page at /cache/risk_gauge.json (NOT copied into this JSON) — see
    docs/stock-dash/index.html §9.
"""
import argparse
import json
import os
import re
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "stock-dash" / "data"
MARKET_DATA_DIR = ROOT / "docs" / "market" / "data"      # read-only source (owned by market-read pipeline)
MARKET_CONTEXT_PATH = OUT_DIR / "_market.json"           # shared summary this script writes, one per day
SCREENER_LATEST_PATH = ROOT / "docs" / "screener" / "latest.json"  # read-only source (RS+VCP screener universe)
UNIVERSE_DIST_PATH = OUT_DIR / "_universe_dist.json"     # shared percentile-cut file this script writes

# Disk cache dirs for data that is identical across every ticker built on the same
# calendar day (a batch run building all 339 dd-screener tickers would otherwise
# redownload these once *per ticker*). Both are outside docs/ so they never get
# swept into a git commit or the Pages artifact. FINRA caching is always on: each
# daily short-volume file is content-addressed by its own date, so a cached copy
# is never stale. SPY caching only activates when STOCK_DASH_HIST_CACHE_DIR is set
# (batch builder sets it) — unset by default so a plain single-ticker CLI run
# behaves exactly as before (always fetches fresh).
FINRA_CACHE_DIR = Path(os.environ.get("STOCK_DASH_FINRA_CACHE_DIR")
                        or (Path(tempfile.gettempdir()) / "stock_dash_finra_cache"))
HIST_CACHE_DIR = Path(os.environ["STOCK_DASH_HIST_CACHE_DIR"]) if os.environ.get("STOCK_DASH_HIST_CACHE_DIR") else None
# Small committed fallback for _sue_breaks.json when PEAD_EVENTS_CSV (owner's Mac
# only, see below) isn't reachable and no previously-built copy exists yet either
# (e.g. a CI runner's very first run before any artifact/cache carries one forward).
SUE_BREAKS_REFERENCE_PATH = ROOT / "scripts" / "stock_dash_ref" / "sue_breaks_reference.json"

DISPLAY_DAYS = 252          # ~1 trading year shown on the chart
VOL_PROFILE_LOOKBACK = 120  # trading days for the volume-at-price histogram
RANGE_PROJ_LOOKBACK = 250   # trading days of returns feeding the fan chart
SHORT_VOL_LOOKBACK = 60     # trading days of FINRA short-volume files
SHORT_VOL_RECENT = 30       # days actually plotted as bars
INSIDER_WINDOW_DAYS = 182   # ~6 months
OPTION_MAX_DAYS = 45
OPTION_MAX_EXPIRIES = 4


def r2(x, nd=2):
    if x is None:
        return None
    if isinstance(x, (float, np.floating)) and (np.isnan(x) or np.isinf(x)):
        return None
    return round(float(x), nd)


def series_r(s, nd=2):
    return [r2(v, nd) for v in s]


# ───────────────────────────────────────────── price history + indicators ──
def fetch_history(ticker, period="2y"):
    t = yf.Ticker(ticker)
    df = t.history(period=period, interval="1d", auto_adjust=False)
    if df is None or df.empty:
        raise RuntimeError(f"yfinance returned no price history for {ticker}")
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
    # Yahoo 收盤後一段時間，當天那根日 K 可能還沒收完（Close 是 NaN），先丟掉，
    # 否則報酬、均線、百分位全部變 NaN。
    df = df[df["Close"].notna()]
    return df


def fetch_history_cached(ticker, period="2y"):
    """Same as fetch_history but, when STOCK_DASH_HIST_CACHE_DIR is set (a batch
    run building many tickers in one day — see build_stock_dash_all.py), reuses
    one on-disk snapshot per (ticker, period, day) instead of every ticker's
    build re-downloading identical history over the network (used here only for
    SPY, which every single-ticker build fetches independently even though it's
    the same series for all of them). Unset (the default for a plain
    `python3 scripts/build_stock_dash.py TICKER` run), this is byte-identical to
    calling fetch_history directly — always a fresh fetch."""
    if HIST_CACHE_DIR is None:
        return fetch_history(ticker, period)
    today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    cache_path = HIST_CACHE_DIR / f"hist_{ticker}_{period}_{today_str}.pkl"
    if cache_path.exists():
        try:
            return pd.read_pickle(cache_path)
        except Exception:  # noqa: BLE001
            pass  # fall through to a fresh fetch
    df = fetch_history(ticker, period)
    try:
        HIST_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = cache_path.with_suffix(cache_path.suffix + f".tmp{os.getpid()}")
        df.to_pickle(tmp)
        os.replace(tmp, cache_path)
    except OSError:
        pass  # caching is best-effort only; never fail the build over it
    return df


def compute_indicators(df):
    close, high, low, vol = df["Close"], df["High"], df["Low"], df["Volume"]

    df["MA21"] = close.rolling(21).mean()
    df["MA50"] = close.rolling(50).mean()
    df["MA150"] = close.rolling(150).mean()  # Minervini trend template (compute_scores) needs this
    df["MA200"] = close.rolling(200).mean()

    typical = (high + low + close) / 3
    df["VWAP20"] = (typical * vol).rolling(20).sum() / vol.rolling(20).sum()

    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["RSI14"] = 100 - 100 / (1 + rs)
    df["RSI14"] = df["RSI14"].fillna(100)  # avg_loss==0 run -> maximally overbought

    prev_close = close.shift(1)
    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    df["ATR14"] = tr.ewm(alpha=1 / 14, adjust=False).mean()
    df["ATR_PCT"] = df["ATR14"] / close * 100
    return df


# ══════════════════════════════════════ universe distribution (score dims) ═
# The "相對強度" and "量能" score dims are percentiles within a universe, not
# absolute good/bad judgments. Universe = every ticker in docs/screener/
# latest.json's rankings (~518 large caps, RS+VCP screener's own母體).
# This section builds/refreshes a small shared percentile-cut file so a
# single-ticker build (including tickers outside the universe, e.g. TSM)
# can interpolate its percentile without each build re-downloading ~518
# tickers of history.
def calc_return_pct(closes, days):
    """% return over `days` trading days — same formula as scripts/screener.py
    calc_return(), needed so our IBD raw value matches rs_ibd exactly."""
    if len(closes) < days + 1:
        return None
    return float(closes.iloc[-1] / closes.iloc[-(days + 1)] - 1) * 100


def ibd_rs_raw(closes):
    """IBD-style weighted return, identical formula to scripts/screener.py's
    rs_ibd_raw: 2*r63 + r126 + r189 + r252 (percent returns)."""
    r63 = calc_return_pct(closes, 63)
    r126 = calc_return_pct(closes, 126)
    r189 = calc_return_pct(closes, 189)
    r252 = calc_return_pct(closes, 252)
    if None in (r63, r126, r189, r252):
        return None
    return 2 * r63 + r126 + r189 + r252


def compute_volume_ratio(df, window=50):
    """(ratio, log(ratio)) of up-day volume sum ÷ down-day volume sum over the
    trailing `window` trading days. None if either side has zero volume."""
    close = df["Close"]
    prev_close = close.shift(1)
    up_mask = (close > prev_close).tail(window)
    down_mask = (close < prev_close).tail(window)
    vol_tail = df["Volume"].tail(window)
    up_vol = float(vol_tail[up_mask].sum())
    down_vol = float(vol_tail[down_mask].sum())
    if up_vol <= 0 or down_vol <= 0:
        return None
    ratio = up_vol / down_vol
    return ratio, float(np.log(ratio))


def percentile_from_cuts(value, cuts):
    """Interpolate `value`'s percentile (0-100) against a sorted list of 101
    percentile cut points (cuts[p] = value at the p-th percentile). Values
    outside the observed range clamp to 0 or 100 — this is how an
    out-of-universe ticker (e.g. TSM) still gets ranked against the cuts."""
    if value is None or not cuts or len(cuts) < 2 or np.isnan(value):
        return None
    arr = np.asarray(cuts, dtype=float)
    if value <= arr[0]:
        return 0.0
    if value >= arr[-1]:
        return 100.0
    idx = int(np.searchsorted(arr, value))
    lo, hi = arr[idx - 1], arr[idx]
    frac = (value - lo) / (hi - lo) if hi > lo else 0.0
    return float((idx - 1) + frac)


def load_universe_tickers():
    if not SCREENER_LATEST_PATH.exists():
        return [], None
    try:
        d = json.loads(SCREENER_LATEST_PATH.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return [], None
    tickers = sorted({r["ticker"] for r in d.get("rankings", []) if r.get("ticker")})
    return tickers, d.get("as_of")


def build_universe_distribution():
    tickers, screener_as_of = load_universe_tickers()
    if not tickers:
        return {"status": "no_data", "reason": "docs/screener/latest.json 不存在或無 rankings"}

    raw = yf.download(tickers, period="2y", interval="1d", group_by="ticker",
                       threads=True, auto_adjust=False, progress=False)

    ibd_vals, vol_log_vals = [], []
    n_price_ok = 0
    for tk in tickers:
        try:
            sub = raw[tk] if isinstance(raw.columns, pd.MultiIndex) else raw
            sub = sub.dropna(subset=["Close"])
        except Exception:  # noqa: BLE001
            continue
        if sub.empty or len(sub) < 253:
            continue
        n_price_ok += 1
        ibd = ibd_rs_raw(sub["Close"])
        if ibd is not None:
            ibd_vals.append(ibd)
        vr = compute_volume_ratio(sub, window=50)
        if vr is not None:
            vol_log_vals.append(vr[1])

    pct_points = list(range(101))
    ibd_cuts = [round(float(x), 4) for x in np.percentile(ibd_vals, pct_points)] if len(ibd_vals) >= 20 else []
    vol_cuts = [round(float(x), 4) for x in np.percentile(vol_log_vals, pct_points)] if len(vol_log_vals) >= 20 else []

    return {
        "schema": "stock-dash-universe-v1",
        "as_of": screener_as_of,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z",
        "n_tickers_requested": len(tickers),
        "n_price_ok": n_price_ok,
        "n_ibd": len(ibd_vals),
        "n_volume": len(vol_log_vals),
        "ibd_percentile_cuts": ibd_cuts,
        "volume_log_percentile_cuts": vol_cuts,
        "source": (
            "宇宙＝docs/screener/latest.json rankings 全部 ticker；每檔用 yfinance 2 年日線"
            "（yf.download 批次＋多執行緒）算 IBD 原始值（2×r63+r126+r189+r252）與近50日"
            "上漲量/下跌量比值取log，各存101個百分位切點（0-100）供內插。"
        ),
    }


def ensure_universe_distribution(ticker_as_of_str, force=False):
    """Rebuild docs/stock-dash/data/_universe_dist.json only when missing or
    older than the ticker currently being built's own latest trading day (or
    when --refresh-universe forces it)."""
    if not force and UNIVERSE_DIST_PATH.exists():
        try:
            existing = json.loads(UNIVERSE_DIST_PATH.read_text(encoding="utf-8"))
            existing_as_of = existing.get("as_of")
            if existing_as_of and ticker_as_of_str and existing_as_of >= ticker_as_of_str:
                return existing
        except Exception:  # noqa: BLE001
            pass
    ctx = build_universe_distribution()
    if ctx.get("status") != "no_data":
        UNIVERSE_DIST_PATH.parent.mkdir(parents=True, exist_ok=True)
        UNIVERSE_DIST_PATH.write_text(json.dumps(ctx, ensure_ascii=False, indent=1), encoding="utf-8")
    return ctx


# ─────────────────────────────────────────────────────── volume profile ────
def compute_volume_profile(df, current_price, lookback=VOL_PROFILE_LOOKBACK, n_bins=40):
    window = df.tail(lookback)
    typical = (window["High"] + window["Low"] + window["Close"]) / 3
    vol = window["Volume"].values
    price_lo, price_hi = float(window["Low"].min()), float(window["High"].max())
    if price_hi <= price_lo:
        return None
    edges = np.linspace(price_lo, price_hi, n_bins + 1)
    bin_vol = np.zeros(n_bins)
    idx = np.clip(np.digitize(typical.values, edges) - 1, 0, n_bins - 1)
    for i, v in zip(idx, vol):
        bin_vol[i] += v
    total = bin_vol.sum()
    poc_i = int(np.argmax(bin_vol))
    poc_price = (edges[poc_i] + edges[poc_i + 1]) / 2

    # value area: expand outward from POC bin by whichever adjacent bin holds
    # more volume until >=70% of the 120-day volume is enclosed (market-profile
    # convention).
    lo, hi = poc_i, poc_i
    cum = bin_vol[poc_i]
    target = total * 0.70
    while cum < target and (lo > 0 or hi < n_bins - 1):
        left = bin_vol[lo - 1] if lo > 0 else -1
        right = bin_vol[hi + 1] if hi < n_bins - 1 else -1
        if right >= left and hi < n_bins - 1:
            hi += 1
            cum += bin_vol[hi]
        elif lo > 0:
            lo -= 1
            cum += bin_vol[lo]
        else:
            break
    va_low, va_high = float(edges[lo]), float(edges[hi + 1])

    # local-peak nodes (a bin whose volume exceeds both neighbours) used for
    # the support/resistance lines drawn on the main chart (§1).
    peaks = []
    for i in range(n_bins):
        left_ok = i == 0 or bin_vol[i] > bin_vol[i - 1]
        right_ok = i == n_bins - 1 or bin_vol[i] > bin_vol[i + 1]
        if left_ok and right_ok and bin_vol[i] > 0:
            mid = (edges[i] + edges[i + 1]) / 2
            peaks.append((float(mid), float(bin_vol[i])))

    below = [p for p in peaks if p[0] < current_price]
    above = [p for p in peaks if p[0] > current_price]
    support_node = max(below, key=lambda p: p[1]) if below else None
    resistance_node = max(above, key=lambda p: p[1]) if above else None

    bins_out = [
        {"lo": r2(edges[i]), "hi": r2(edges[i + 1]), "volume": int(bin_vol[i])}
        for i in range(n_bins)
    ]
    return {
        "lookback_days": lookback,
        "bins": bins_out,
        "poc_price": r2(poc_price),
        "value_area_low": r2(va_low),
        "value_area_high": r2(va_high),
        "current_price": r2(current_price),
        "support_node": {"price": r2(support_node[0]), "volume": int(support_node[1])}
        if support_node else None,
        "resistance_node": {"price": r2(resistance_node[0]), "volume": int(resistance_node[1])}
        if resistance_node else None,
        "method": (
            f"近{lookback}個交易日，依每日典型價格((高+低+收)/3)分入{n_bins}個等寬價位區間，"
            "區間成交量加總；成交最多的區間為 POC。自 POC 向左右擴張、每次併入量較大的相鄰"
            "區間，直到涵蓋 70% 的區間總成交量，得出主要成交區間（Value Area）。支撐／壓力："
            "在現價下方／上方，找區間成交量高於左右相鄰區間的『節點』，取其中成交量最大者。"
        ),
    }


def resolve_support_resistance(df, current_price, vol_profile):
    reason_bits = []
    support = None
    resistance = None
    if vol_profile and vol_profile["support_node"]:
        support = vol_profile["support_node"]["price"]
    else:
        support = r2(df["Low"].tail(60).min())
        reason_bits.append("支撐：120 日量價分布現價下方無明顯節點，改用近 60 日最低價")
    if vol_profile and vol_profile["resistance_node"]:
        resistance = vol_profile["resistance_node"]["price"]
    else:
        resistance = r2(df["High"].tail(60).max())
        reason_bits.append("壓力：120 日量價分布現價上方無明顯節點，改用近 60 日最高價")
    return support, resistance, reason_bits


# ───────────────────────────────────────────────── statistical range fan ───
def compute_range_projection(df, horizon=10, lookback=RANGE_PROJ_LOOKBACK, n_sims=20000, seed=42, atr_pct=None):
    close = df["Close"]
    if len(close) < lookback + 1:
        lookback = len(close) - 1
    log_ret = np.diff(np.log(close.tail(lookback + 1).values))
    if len(log_ret) < 20:
        return None
    rng = np.random.default_rng(seed)
    draws = rng.choice(log_ret, size=(n_sims, horizon), replace=True)
    cum_path = np.cumsum(draws, axis=1)  # n_sims x horizon, day1..dayN cumulative log return
    current_price = float(close.iloc[-1])

    path = [{
        "day": 0, "p10": r2(current_price), "p25": r2(current_price), "p50": r2(current_price),
        "p75": r2(current_price), "p90": r2(current_price),
    }]
    final_terminal = None
    for d in range(horizon):
        terminal_d = current_price * np.exp(cum_path[:, d])
        if d == horizon - 1:
            final_terminal = terminal_d
        pcts = np.percentile(terminal_d, [10, 25, 50, 75, 90])
        path.append({
            "day": d + 1,
            "p10": r2(pcts[0]), "p25": r2(pcts[1]), "p50": r2(pcts[2]),
            "p75": r2(pcts[3]), "p90": r2(pcts[4]),
        })

    three_state = None
    if atr_pct is not None and final_terminal is not None:
        atr_dollar = atr_pct / 100 * current_price
        upper, lower = current_price + atr_dollar, current_price - atr_dollar
        up_big = float((final_terminal > upper).mean() * 100)
        down_big = float((final_terminal < lower).mean() * 100)
        three_state = {
            "up_beyond_1atr_pct": r2(up_big, 1),
            "within_1atr_pct": r2(100 - up_big - down_big, 1),
            "down_beyond_1atr_pct": r2(down_big, 1),
            "atr_dollar": r2(atr_dollar),
            "method": (
                f"以現價 ± 1 倍 ATR14（{atr_pct:.2f}% × 現價 = {atr_dollar:.2f}）為界，"
                f"統計模擬的第 {horizon} 個交易日終值分別落在上界之上／區間內／下界之下的比例。"
            ),
        }

    final = path[-1]
    return {
        "current_price": r2(current_price),
        "horizon_trading_days": horizon,
        "lookback_days": lookback,
        "n_sims": n_sims,
        "path": path,
        "p10": final["p10"], "p25": final["p25"], "p50": final["p50"],
        "p75": final["p75"], "p90": final["p90"],
        "three_state": three_state,
        "method": (
            f"取近 {lookback} 個交易日的日對數報酬為母體，可重複抽樣，逐日累加模擬 {horizon} 個交易日"
            f"的價格路徑，重複 {n_sims} 次，取每一天的第 10/25/50/75/90 百分位數畫成扇形。"
            "這是用歷史波動度反推的統計區間，不是價格預測。"
        ),
    }


# ───────────────────────────────────────────────────── relative strength ───
def compute_relative_strength(df, spy_df):
    merged = pd.DataFrame({"t": df["Close"], "s": spy_df["Close"]}).dropna()
    out = {}
    for label, n in (("3m", 63), ("6m", 126), ("12m", 252)):
        if len(merged) <= n:
            out[label] = None
            continue
        ret_t = merged["t"].iloc[-1] / merged["t"].iloc[-1 - n] - 1
        ret_s = merged["s"].iloc[-1] / merged["s"].iloc[-1 - n] - 1
        out[label] = r2((ret_t - ret_s) * 100)
    return out


# ─────────────────────────────────────────────────────────── FINRA short ───
def _finra_daily_text(session, date_str):
    """Fetch (or serve from FINRA_CACHE_DIR) one day's full Reg SHO file — the
    same file every ticker built that day would otherwise redownload from
    scratch just to grep out its own symbol. Content is immutable per date_str,
    so the on-disk cache never needs invalidation. Write is atomic (tmp file +
    os.replace) so concurrent ticker builds racing on a cold cache can't hand
    each other a half-written file; a failed/partial download simply isn't
    cached and falls through to a normal per-call fetch next time."""
    cache_path = FINRA_CACHE_DIR / f"CNMSshvol{date_str}.txt"
    if cache_path.exists():
        try:
            return cache_path.read_text(encoding="utf-8", errors="replace"), None
        except OSError:
            pass  # fall through to a fresh download
    url = f"https://cdn.finra.org/equity/regsho/daily/CNMSshvol{date_str}.txt"
    r = session.get(url, timeout=10)
    if r.status_code != 200:
        return None, f"http {r.status_code}"
    text = r.text
    try:
        FINRA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = cache_path.with_suffix(cache_path.suffix + f".tmp{os.getpid()}")
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, cache_path)
    except OSError:
        pass  # caching is best-effort only; never fail the build over it
    return text, None


def _finra_fetch_one(session, date_str, ticker):
    try:
        text, err = _finra_daily_text(session, date_str)
        if text is None:
            return date_str, None, err
        prefix = f"{date_str}|{ticker}|"
        for line in text.splitlines():
            if line.startswith(prefix):
                f = line.split("|")
                short_vol = float(f[2])
                total_vol = float(f[4])
                return date_str, {"short_volume": short_vol, "total_volume": total_vol}, None
        return date_str, None, "symbol not in file"
    except Exception as e:  # noqa: BLE001
        return date_str, None, str(e)


def fetch_short_volume(df, ticker, lookback=SHORT_VOL_LOOKBACK):
    trading_days = [d.strftime("%Y%m%d") for d in df.index[-lookback:]]
    session = requests.Session()
    results = {}
    failures = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(_finra_fetch_one, session, d, ticker): d for d in trading_days}
        for fut in as_completed(futs):
            date_str, val, err = fut.result()
            if val is not None:
                results[date_str] = val
            else:
                failures.append((date_str, err))

    if len(results) < 10:
        return {
            "status": "no_data",
            "reason": f"FINRA Reg SHO 每日檔僅成功抓到 {len(results)}/{len(trading_days)} 天，樣本不足",
            "days_ok": len(results),
            "days_requested": len(trading_days),
        }

    dates_sorted = sorted(results.keys())
    ratio = {d: results[d]["short_volume"] / results[d]["total_volume"] * 100 for d in dates_sorted}
    ratio_series = pd.Series(ratio)
    ma20 = ratio_series.rolling(20, min_periods=10).mean()

    recent_dates = dates_sorted[-SHORT_VOL_RECENT:]
    daily = [
        {
            "date": f"{d[:4]}-{d[4:6]}-{d[6:]}",
            "short_ratio_pct": r2(ratio[d]),
            "ma20_pct": r2(ma20.get(d)),
            "total_volume": int(results[d]["total_volume"]),
        }
        for d in recent_dates
    ]

    recent30 = ratio_series.tail(SHORT_VOL_RECENT)
    all60 = ratio_series
    z = None
    if all60.std(ddof=1) and not np.isnan(all60.std(ddof=1)) and all60.std(ddof=1) > 0:
        z = (recent30.mean() - all60.mean()) / all60.std(ddof=1)

    return {
        "status": "ok" if len(results) == len(trading_days) else "partial",
        "days_ok": len(results),
        "days_requested": len(trading_days),
        "missing_dates": [d for d, _ in failures][:10],
        "daily": daily,
        "z_score_recent30_vs_60": r2(z, 2),
        "method": (
            "每日放空量比率 = ShortVolume / TotalVolume（FINRA Reg SHO 合併披露檔，含造市商放空，"
            "40–50% 為市場常態，非空方訊號）。z 值 = (近 30 日平均比率 − 近 60 日平均比率) / "
            "近 60 日比率標準差，只用來看『跟自己過去比』有沒有明顯偏離。"
        ),
    }


# ──────────────────────────────────────────────────────────── insiders ─────
def classify_insider_text(text):
    t = (text or "").lower()
    if "sale" in t:
        return "sell"
    if "purchase" in t or "buy" in t:
        return "buy"
    return "other"


def fetch_insiders(ticker_obj, as_of_date, window_days=INSIDER_WINDOW_DAYS):
    try:
        raw = ticker_obj.insider_transactions
    except Exception as e:  # noqa: BLE001
        return {"status": "no_data", "reason": f"yfinance insider_transactions 例外：{e}"}
    if raw is None or raw.empty:
        return {"status": "no_data", "reason": "yfinance 未回傳 insider_transactions 資料"}
    required_cols = {"Start Date", "Text", "Position", "Insider", "Shares", "Value"}
    missing_cols = required_cols - set(raw.columns)
    if missing_cols:
        return {"status": "no_data", "reason": f"yfinance insider_transactions 缺欄位：{sorted(missing_cols)}"}

    raw = raw.copy()
    raw["Start Date"] = pd.to_datetime(raw["Start Date"], errors="coerce")
    cutoff = pd.Timestamp(as_of_date) - pd.Timedelta(days=window_days)
    win = raw[raw["Start Date"] >= cutoff].copy()
    # NB: an empty window after a successful fetch means "zero disclosed
    # transactions" (a genuine, informative state), not a data-fetch failure —
    # it is returned as status "ok" with an empty transactions list below,
    # not "no_data" (which is reserved for actual fetch/API failures above).
    # win["kind"] assignment below is safe even when win has zero rows (a plain
    # column assignment on an empty frame, unlike the boolean-mask-on-an-empty-
    # -Series pattern in check_insider_cluster_buy that used to crash on it).

    win["kind"] = win["Text"].apply(classify_insider_text)
    rows = []
    for _, row in win.sort_values("Start Date", ascending=False).iterrows():
        rows.append({
            "date": row["Start Date"].strftime("%Y-%m-%d") if pd.notna(row["Start Date"]) else None,
            "insider": row.get("Insider"),
            "position": row.get("Position"),
            "kind": row["kind"],
            "shares": int(row["Shares"]) if pd.notna(row["Shares"]) else None,
            "value_usd": int(row["Value"]) if pd.notna(row["Value"]) else None,
            "ownership": row.get("Ownership"),
            "text": row.get("Text"),
        })

    sell_shares = sum(r["shares"] or 0 for r in rows if r["kind"] == "sell")
    buy_shares = sum(r["shares"] or 0 for r in rows if r["kind"] == "buy")
    sell_value = sum(r["value_usd"] or 0 for r in rows if r["kind"] == "sell")
    buy_value = sum(r["value_usd"] or 0 for r in rows if r["kind"] == "buy")

    return {
        "status": "ok",
        "window_days": window_days,
        "transactions": rows,
        "summary": {
            "sell_shares": sell_shares,
            "buy_shares": buy_shares,
            "net_shares": buy_shares - sell_shares,
            "sell_value_usd": sell_value,
            "buy_value_usd": buy_value,
            "net_value_usd": buy_value - sell_value,
            "n_transactions": len(rows),
        },
        "note": (
            (f"近 {window_days} 天內 SEC 揭露資料無內部人交易紀錄。" if not rows else "") +
            "分類依 SEC Form 4 文字描述：含『Sale』判為賣出，含『Purchase/Buy』判為買進，"
            "其餘（如 Stock Award/Grant、Stock Gift）歸類為『其他』、不計入淨買賣。"
            "yfinance 回傳欄位未標示是否屬 10b5-1 預先排定計畫，NVDA 高層申報的例行性賣股"
            "多數屬於此類排定計畫，非臨時決策，此處無法逐筆判斷、僅作一般性說明。"
        ),
    }


# ───────────────────────────────────────────────────────────── options ─────
def _atm_iv_for_expiry(ticker_obj, expiry, current_price):
    """ATM IV (%) for one expiry: average of nearest-strike call/put implied vol."""
    try:
        oc = ticker_obj.option_chain(expiry)
    except Exception:  # noqa: BLE001
        return None
    calls, puts = oc.calls, oc.puts
    if calls.empty or puts.empty:
        return None
    c_row = calls.iloc[(calls["strike"] - current_price).abs().argsort().iloc[0]]
    p_row = puts.iloc[(puts["strike"] - current_price).abs().argsort().iloc[0]]
    ivs = [v for v in (c_row.get("impliedVolatility"), p_row.get("impliedVolatility")) if pd.notna(v)]
    return float(np.mean(ivs)) * 100 if ivs else None


def _pick_expiry_near_days(all_exps, today, target_days, min_days):
    """Expiry whose DTE is closest to target_days, excluding DTE < min_days."""
    candidates = []
    for e in all_exps:
        try:
            d = datetime.strptime(e, "%Y-%m-%d").date()
        except ValueError:
            continue
        dte = (d - today).days
        if dte >= min_days:
            candidates.append((e, dte))
    if not candidates:
        return None, None
    return min(candidates, key=lambda x: abs(x[1] - target_days))


def fetch_options(ticker_obj, current_price, hv20):
    try:
        all_exps = list(ticker_obj.options)
    except Exception as e:  # noqa: BLE001
        return {"status": "no_data", "reason": f"yfinance options 例外：{e}"}
    if not all_exps:
        return {"status": "no_data", "reason": "yfinance 未回傳任何到期日"}

    today = datetime.now(timezone.utc).date()
    near = []
    for e in all_exps:
        try:
            d = datetime.strptime(e, "%Y-%m-%d").date()
        except ValueError:
            continue
        dte = (d - today).days
        if 0 <= dte <= OPTION_MAX_DAYS:
            near.append((e, dte))
    near.sort(key=lambda x: x[1])
    near = near[:OPTION_MAX_EXPIRIES]
    if not near:
        return {"status": "no_data", "reason": f"無到期日落在 {OPTION_MAX_DAYS} 天內"}

    expiries = []
    total_call_vol = total_put_vol = total_call_oi = total_put_oi = 0.0
    for exp, dte in near:
        try:
            oc = ticker_obj.option_chain(exp)
        except Exception as e:  # noqa: BLE001
            expiries.append({"expiry": exp, "dte": dte, "status": "no_data", "reason": str(e)})
            continue
        calls, puts = oc.calls, oc.puts
        cv = float(calls["volume"].fillna(0).sum())
        pv = float(puts["volume"].fillna(0).sum())
        coi = float(calls["openInterest"].fillna(0).sum())
        poi = float(puts["openInterest"].fillna(0).sum())
        total_call_vol += cv; total_put_vol += pv
        total_call_oi += coi; total_put_oi += poi

        atm_iv = None
        if not calls.empty and not puts.empty:
            c_row = calls.iloc[(calls["strike"] - current_price).abs().argsort().iloc[0]]
            p_row = puts.iloc[(puts["strike"] - current_price).abs().argsort().iloc[0]]
            ivs = [v for v in (c_row.get("impliedVolatility"), p_row.get("impliedVolatility")) if pd.notna(v)]
            if ivs:
                atm_iv = float(np.mean(ivs)) * 100

        expiries.append({
            "expiry": exp,
            "dte": dte,
            "status": "ok",
            "call_volume": int(cv), "put_volume": int(pv),
            "call_oi": int(coi), "put_oi": int(poi),
            "pc_ratio_volume": r2(pv / cv) if cv > 0 else None,
            "pc_ratio_oi": r2(poi / coi) if coi > 0 else None,
            "atm_iv_pct": r2(atm_iv),
        })

    # ATM IV summary metric uses the expiry closest to 30 days out (excluding
    # anything inside 7 days) instead of the very nearest expiry — 0-7 DTE
    # contracts are too noisy (near-zero theta/vega structure) to represent
    # "current" implied vol. The put/call ratio table above is unaffected.
    atm30_expiry, atm30_dte = _pick_expiry_near_days(all_exps, today, target_days=30, min_days=7)
    atm30_iv = _atm_iv_for_expiry(ticker_obj, atm30_expiry, current_price) if atm30_expiry else None

    # Yahoo 在美股盤前／資料重置時段會回傳未平倉量全 0、隱含波動率接近 0 的占位值
    # （2026-09-21 台北下午重跑時 NVDA／TSM／AMD 全中：IV 0.03–0.39%）。這種快照不能用，
    # 標成 stale 讓頁面顯示無資料，不要把占位值當真。
    oi_total = total_call_oi + total_put_oi
    if oi_total == 0 or (atm30_iv is not None and atm30_iv < 2.0):
        return {
            "status": "stale",
            "reason": (f"Yahoo 選擇權資料看起來是盤前／重置時段的占位值（未平倉量合計 {int(oi_total)}、"
                       f"30 天 ATM 隱含波動率 {atm30_iv if atm30_iv is None else round(atm30_iv, 2)}%），這次快照不採用。"),
            "snapshot_generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z",
        }

    return {
        "status": "ok",
        "snapshot_generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z",
        "expiries": expiries,
        "aggregate": {
            "pc_ratio_volume": r2(total_put_vol / total_call_vol) if total_call_vol > 0 else None,
            "pc_ratio_oi": r2(total_put_oi / total_call_oi) if total_call_oi > 0 else None,
            "call_volume_total": int(total_call_vol),
            "put_volume_total": int(total_put_vol),
            "atm_iv_30d_pct": r2(atm30_iv),
            "atm_iv_30d_expiry": atm30_expiry,
            "atm_iv_30d_dte": atm30_dte,
            "hv20_pct": r2(hv20),
        },
        "note": "選擇權數據為 build 腳本執行當下的市場快照，非收盤價對應的同一時間點；put/call 表取未來 45 天內最近的到期日（最多 4 個）；ATM IV 改取到期日最接近 30 天（排除 7 天內）的合約，避免當週到期雜訊。",
    }


# ──────────────────────────────────────────────────────────────── scores ───
def pct_rank(series, value):
    s = series.dropna()
    if len(s) == 0 or value is None:
        return None
    return float((s < value).mean() * 100)


def compute_scores(df, universe_dist, short_vol_block, info):
    """Three "direction" dims (trend / relative_strength / volume) plus two
    unchanged risk descriptors (volatility / short_pressure). All five are
    status descriptors, not predictions — a 511-name 2014-2025 backtest found
    ~0 rank IC against forward 1-12m excess return for the prior scoring
    system, so nothing here is framed as a signal or verdict (see
    trend_state's policy_note and the removal of any averaged/combined score)."""
    close = df["Close"]
    price = float(close.iloc[-1])
    ma50, ma150, ma200 = df["MA50"], df["MA150"], df["MA200"]

    # ── trend: Minervini trend template, 7 conditions, pass_count/7*100 ──
    ma200_21_ago = float(ma200.iloc[-22]) if len(ma200) > 21 and pd.notna(ma200.iloc[-22]) else None
    low_52w = float(close.tail(252).min())
    high_52w = float(close.tail(252).max())
    conditions = [
        {"key": "price_above_ma150_and_ma200", "label": "價格 > MA150 且 > MA200",
         "pass": bool(price > float(ma150.iloc[-1]) and price > float(ma200.iloc[-1]))},
        {"key": "ma150_above_ma200", "label": "MA150 > MA200",
         "pass": bool(float(ma150.iloc[-1]) > float(ma200.iloc[-1]))},
        {"key": "ma200_rising_21d", "label": "MA200 高於 21 個交易日前的 MA200",
         "pass": bool(ma200_21_ago is not None and float(ma200.iloc[-1]) > ma200_21_ago)},
        {"key": "ma50_above_ma150_and_ma200", "label": "MA50 > MA150 且 > MA200",
         "pass": bool(float(ma50.iloc[-1]) > float(ma150.iloc[-1]) and float(ma50.iloc[-1]) > float(ma200.iloc[-1]))},
        {"key": "price_above_ma50", "label": "價格 > MA50",
         "pass": bool(price > float(ma50.iloc[-1]))},
        {"key": "above_130pct_52w_low", "label": "價格 ≥ 1.30 × 52 週最低收盤",
         "pass": bool(low_52w > 0 and price >= 1.30 * low_52w)},
        {"key": "above_75pct_52w_high", "label": "價格 ≥ 0.75 × 52 週最高收盤",
         "pass": bool(high_52w > 0 and price >= 0.75 * high_52w)},
    ]
    pass_count = sum(1 for c in conditions if c["pass"])
    trend_score = pass_count / 7 * 100
    trend_template = {
        "conditions": conditions,
        "pass_count": pass_count,
        "of": 7,
        "method": (
            "Minervini 趨勢模板 7 條件，通過數 ÷ 7 × 100。本頁用完整 7 條原版分開列示；"
            "站上 scripts/vcp_core.py 的 VCP 篩選器只查其中對應 5 個判斷"
            "（把①②合併成一條「price>MA150>MA200」，且④只查 MA50>MA150、不查 MA50>MA200，"
            "也沒有單獨列⑤價格>MA50 這條）。"
        ),
    }

    # ── relative strength: IBD raw value, percentile within screener universe ──
    ibd_raw = ibd_rs_raw(close)
    ibd_cuts = (universe_dist or {}).get("ibd_percentile_cuts") or []
    rel_pctile = percentile_from_cuts(ibd_raw, ibd_cuts) if ibd_raw is not None else None
    relative_strength_detail = {
        "raw_ibd": r2(ibd_raw, 2) if ibd_raw is not None else None,
        "percentile": r2(rel_pctile, 1) if rel_pctile is not None else None,
        "universe_n": (universe_dist or {}).get("n_ibd"),
        "universe_as_of": (universe_dist or {}).get("as_of"),
        "method": (
            "IBD 算法：原始值 = 2×63個交易日報酬% + 126個交易日報酬% + 189個交易日報酬% + 252個交易日報酬%，"
            "在宇宙（docs/screener/latest.json 全部約518檔）用 2 年日線算出的分布中取百分位（0–100）。"
            "跟站上 scripts/screener.py 的 rs_ibd 同一套算法，數字差異只來自兩邊資料抓取日期不同。"
        ),
    }

    # ── volume: 近50日上漲量/下跌量比值，取log後在宇宙分布中取百分位 ──
    vr = compute_volume_ratio(df, window=50)
    vol_ratio, vol_log = vr if vr is not None else (None, None)
    vol_cuts = (universe_dist or {}).get("volume_log_percentile_cuts") or []
    vol_pctile = percentile_from_cuts(vol_log, vol_cuts) if vol_log is not None else None
    volume_detail = {
        "ratio": r2(vol_ratio, 3) if vol_ratio is not None else None,
        "log_ratio": r2(vol_log, 3) if vol_log is not None else None,
        "percentile": r2(vol_pctile, 1) if vol_pctile is not None else None,
        "window_days": 50,
        "universe_n": (universe_dist or {}).get("n_volume"),
        "universe_as_of": (universe_dist or {}).get("as_of"),
        "method": "近50個交易日「上漲日成交量總和 ÷ 下跌日成交量總和」，取自然對數後在宇宙分布中取百分位（0–100）。",
    }

    # ── volatility: 100 - percentile(ATR% within trailing 252d) — unchanged ──
    atr_pct_series = df["ATR_PCT"].tail(252)
    atr_pct_now = float(df["ATR_PCT"].iloc[-1])
    atr_pctile = pct_rank(atr_pct_series, atr_pct_now)
    vol_score_inv = float(100 - atr_pctile) if atr_pctile is not None else None

    # ── short pressure — unchanged (越低分代表放空壓力越低) ──
    short_score = None
    short_components = {}
    z = None
    if short_vol_block.get("status") in ("ok", "partial"):
        z = short_vol_block.get("z_score_recent30_vs_60")
    spf = info.get("shortPercentOfFloat")
    z_component = np.clip(50 + (z or 0) * 15, 0, 100) if z is not None else None
    spf_component = np.clip((spf or 0) * 100 * 10, 0, 100) if spf is not None else None
    parts = [p for p in (z_component, spf_component) if p is not None]
    if parts:
        if z_component is not None and spf_component is not None:
            pressure_raw = 0.7 * z_component + 0.3 * spf_component
        else:
            pressure_raw = parts[0]
        short_score = float(np.clip(100 - pressure_raw, 0, 100))
        short_components = {
            "z_score": r2(z, 2), "z_component_0to100": r2(z_component),
            "short_pct_of_float": r2(spf * 100 if spf is not None else None, 2),
            "spf_component_0to100": r2(spf_component),
        }

    dims = {
        "trend": r2(trend_score, 1),
        "relative_strength": r2(rel_pctile, 1) if rel_pctile is not None else None,
        "volume": r2(vol_pctile, 1) if vol_pctile is not None else None,
        "volatility": r2(vol_score_inv, 1),
        "short_pressure": r2(short_score, 1),
    }

    return {
        "dims": dims,
        "trend_template": trend_template,
        "relative_strength_detail": relative_strength_detail,
        "volume_detail": volume_detail,
        "short_pressure_components": short_components,
        "footnotes": {
            "trend": trend_template["method"],
            "relative_strength": relative_strength_detail["method"],
            "volume": volume_detail["method"],
            "volatility": "100 − ATR%（14日）於近252日自身分布中的百分位排名；波動相對自己越低分數越高。",
            "short_pressure": "分數越高代表放空壓力越低。壓力原始值 = 0.7×z值分量 + 0.3×佔流通股比例分量"
                               "（z值=放空量比率近30日均值相對近60日的標準化值，映射 50+z×15；"
                               "佔流通股比例映射 (比例%×10)，兩者皆截尾 0–100），分數 = 100 − 壓力原始值。",
        },
        "policy_note": "以上分項是技術面狀態描述，不是預測，也不構成買進、賣出或加碼等操作建議。",
    }


# ────────────────────────────────────────────────────────── trend state ───
def compute_trend_state(ticker, scores, status_summary, short_vol_block, event_days):
    """Replaces the old averaged-score traffic light. Three states (強/中/弱)
    derived only from the trend template pass-count and the relative-strength
    percentile — no averaging across dims, no color implying good/bad."""
    tt = scores.get("trend_template") or {}
    trend_pass = tt.get("pass_count")
    rel_detail = scores.get("relative_strength_detail") or {}
    rel_pctile = rel_detail.get("percentile")
    vol_detail = scores.get("volume_detail") or {}
    vol_ratio = vol_detail.get("ratio")

    if trend_pass is not None and rel_pctile is not None and trend_pass >= 6 and rel_pctile >= 70:
        state, state_zh = "strong", "強"
    elif (trend_pass is not None and trend_pass <= 2) or (rel_pctile is not None and rel_pctile <= 30):
        state, state_zh = "weak", "弱"
    else:
        state, state_zh = "neutral", "中"

    def volume_desc(ratio):
        if ratio is None:
            return "量能比值無資料"
        if ratio >= 1.2:
            return f"上漲日量明顯大於下跌日（比值 {ratio:.2f}）"
        if ratio <= 0.83:
            return f"下跌日量明顯大於上漲日（比值 {ratio:.2f}）"
        return f"上漲日與下跌日量差不多（比值 {ratio:.2f}）"

    dist_52w = status_summary.get("dist_52w_high_pct")
    trend_desc = f"趨勢模板通過 {trend_pass}/7" if trend_pass is not None else "趨勢模板無資料"
    rel_desc = f"相對強度第 {rel_pctile:.0f} 百分位" if rel_pctile is not None else "相對強度無資料"
    dist_desc = f"距 52 週高點 {dist_52w:+.1f}%" if dist_52w is not None else "52 週高點距離無資料"
    event_desc = f"距下次財報 {event_days} 天" if event_days is not None else "下次財報日無資料"

    summary_zh = f"{ticker}：{trend_desc}，{rel_desc}，{volume_desc(vol_ratio)}，{dist_desc}，{event_desc}。"

    rsi14 = status_summary.get("rsi14")
    atr_pctile = status_summary.get("atr_pct_percentile_1y")
    z = short_vol_block.get("z_score_recent30_vs_60") if short_vol_block.get("status") in ("ok", "partial") else None
    price_vs_ma50 = status_summary.get("price_vs_ma50_pct")
    price_vs_ma200 = status_summary.get("price_vs_ma200_pct")

    facts = []

    def add(desc, active):
        facts.append({"desc": desc, "active": bool(active)})

    add("價格站上 MA50", price_vs_ma50 is not None and price_vs_ma50 > 0)
    add("價格跌破 MA50", price_vs_ma50 is not None and price_vs_ma50 <= 0)
    add("價格站上 MA200", price_vs_ma200 is not None and price_vs_ma200 > 0)
    add("價格跌破 MA200", price_vs_ma200 is not None and price_vs_ma200 <= 0)
    add("RSI14 > 70（超買區）", rsi14 is not None and rsi14 > 70)
    add("RSI14 < 30（超賣區）", rsi14 is not None and rsi14 < 30)
    add("距 52 週高點 < 5%", dist_52w is not None and dist_52w > -5)
    add("距 52 週高點 > 20%（顯著回落）", dist_52w is not None and dist_52w < -20)
    add("ATR% 處於近一年自身高檔（>80 百分位）", atr_pctile is not None and atr_pctile > 80)
    add("放空量比率 z 值 > 1.5（相對自身放大）", z is not None and z > 1.5)

    return {
        "state": state,
        "state_zh": state_zh,
        "summary_zh": summary_zh,
        "facts": facts,
        "policy_note": "本狀態僅描述目前技術面現況，不是預測，也不構成買進、賣出或加碼等操作建議。",
    }


# ═══════════════════════════════════════════════ full (18-panel) additions ═
# Everything below feeds docs/stock-dash/full.html only; the simplified
# docs/stock-dash/index.html ignores these extra JSON fields.

# ── panel 5: per-axis text states (no colored lights) ────────────────────
def compute_dim_states(scores, risk_radar):
    """趨勢／相對強度／量能／風險 four axes, each its own text state — no
    red/yellow/green, no implication of good or bad. `code` (-1/0/1) is kept
    only for the internal "how many axes point the same direction" tally in
    compute_data_reliability; it is never rendered as a color on the page."""
    tt = scores.get("trend_template") or {}
    trend_pass = tt.get("pass_count")
    rel_pctile = (scores.get("relative_strength_detail") or {}).get("percentile")
    vol_ratio = (scores.get("volume_detail") or {}).get("ratio")
    risk_vals = [v for v in (risk_radar or {}).get("dims", {}).values() if v is not None]
    risk_avg = sum(risk_vals) / len(risk_vals) if risk_vals else None

    def trend_bucket(n):
        if n is None:
            return ("無資料", None)
        if n >= 6:
            return ("強", 1)
        if n <= 2:
            return ("弱", -1)
        return ("中", 0)

    def pctile_bucket(p):
        if p is None:
            return ("無資料", None)
        if p >= 70:
            return ("強", 1)
        if p <= 30:
            return ("弱", -1)
        return ("中", 0)

    def volume_bucket(ratio):
        if ratio is None:
            return ("無資料", None)
        if ratio >= 1.2:
            return ("買盤較多", 1)
        if ratio <= 0.83:
            return ("賣盤較多", -1)
        return ("差不多", 0)

    def risk_bucket(avg):
        if avg is None:
            return ("無資料", None)
        if avg >= 65:
            return ("偏高", -1)
        if avg <= 35:
            return ("偏低", 1)
        return ("中等", 0)

    trend_label, trend_code = trend_bucket(trend_pass)
    rel_label, rel_code = pctile_bucket(rel_pctile)
    vol_label, vol_code = volume_bucket(vol_ratio)
    risk_label, risk_code = risk_bucket(risk_avg)

    return {
        "trend": {"name_zh": "趨勢", "label": trend_label, "code": trend_code, "value": trend_pass,
                  "rule": "趨勢模板通過數 ≥6 記為「強」、≤2 記為「弱」，其餘「中」。"},
        "relative_strength": {"name_zh": "相對強度", "label": rel_label, "code": rel_code,
                               "value": r2(rel_pctile, 1) if rel_pctile is not None else None,
                               "rule": "相對強度百分位 ≥70 記為「強」、≤30 記為「弱」，其餘「中」。"},
        "volume": {"name_zh": "量能", "label": vol_label, "code": vol_code,
                   "value": r2(vol_ratio, 2) if vol_ratio is not None else None,
                   "rule": "上漲日量/下跌日量比值 ≥1.2 記為「買盤較多」、≤0.83 記為「賣盤較多」，其餘「差不多」。"},
        "risk": {"name_zh": "風險", "label": risk_label, "code": risk_code,
                 "value": r2(risk_avg, 1) if risk_avg is not None else None,
                 "rule": "第7格六軸風險雷達平均分 ≥65 記為「偏高」、≤35 記為「偏低」，其餘「中等」——這是風險程度描述，不是好壞判斷。"},
    }


# ── panel 6: health gauges (insider health score is the one new metric) ──
def compute_insider_health(insiders, avg_dollar_vol_20d, window_days):
    if not insiders or insiders.get("status") != "ok":
        reason = insiders.get("reason") if insiders else "無內部人資料"
        return None, f"無法取得內部人交易資料：{reason}"
    s = insiders["summary"]
    if s["n_transactions"] == 0:
        return 50.0, f"近 {window_days} 天無揭露交易，中性計 50 分。"
    if not avg_dollar_vol_20d or avg_dollar_vol_20d <= 0:
        return 50.0, "缺近20日平均成交金額，無法正規化，中性計 50 分。"
    denom = avg_dollar_vol_20d * window_days
    ratio = s["net_value_usd"] / denom
    score = float(np.clip(50 + ratio * 1000, 0, 100))
    return score, (
        f"分數 = 50 + (淨買賣金額 ÷（近{window_days}天 × 20日均成交金額）) × 1000，截尾 0–100；"
        f"淨買賣金額 {s['net_value_usd']:,} 美元，20日均成交金額約 {avg_dollar_vol_20d:,.0f} 美元/天，"
        f"比值 {ratio:.5f}。分數越低代表內部人淨賣壓相對成交量越顯著。"
    )


def compute_health_gauges(scores, insider_score, insider_note):
    """5 gauges split into two groups for the page: 技術面（技術結構/資金動能，
    直接取新的趨勢/量能分項）與風險面（波動/空單壓力/內部人——這三個是風險程度
    描述，不是健康度或好壞判斷，頁面標題與註腳都要講清楚）。"""
    d = scores["dims"]
    return {
        "gauges": [
            {"key": "technical", "name_zh": "技術結構", "group": "technical", "score": d["trend"]},
            {"key": "capital_momentum", "name_zh": "資金動能", "group": "technical", "score": d["volume"]},
            {"key": "volatility", "name_zh": "波動（低波動高分）", "group": "risk", "score": d["volatility"]},
            {"key": "short_pressure", "name_zh": "空單壓力（低壓力高分）", "group": "risk", "score": d["short_pressure"]},
            {"key": "insider", "name_zh": "內部人（淨賣越多分數越低）", "group": "risk",
             "score": r2(insider_score, 1) if insider_score is not None else None},
        ],
        "footnotes": {
            "technical": "＝第4格『趨勢』分項評分（Minervini 趨勢模板通過數 ÷7×100）。",
            "capital_momentum": "＝第4格『量能』分項評分（近50日上漲量/下跌量比值的宇宙百分位）。",
            "volatility": "＝第4格『波動』分項評分（100 − ATR% 近一年百分位）；風險面描述，非好壞判斷。",
            "short_pressure": "＝第4格『空單壓力』分項評分；風險面描述，非好壞判斷。",
            "insider": insider_note,
            "risk_group_note": "波動／空單壓力／內部人三格合稱「風險面」——描述目前風險程度高低，不是評價這檔股票好不好。",
        },
    }


# ── panel 7: risk radar (6 axes, higher = more risk — inverse of panel 6) ──
def compute_event_risk(ticker_obj, as_of_date):
    try:
        cal = ticker_obj.calendar
    except Exception as e:  # noqa: BLE001
        return None, None, f"yfinance calendar 例外：{e}"
    if not cal or not cal.get("Earnings Date"):
        return None, None, "yfinance calendar 未回傳下次財報日期"
    dates = cal["Earnings Date"]
    future = [dd for dd in dates if dd >= as_of_date]
    target = min(future) if future else min(dates)
    days = (target - as_of_date).days
    return target.strftime("%Y-%m-%d"), days, None


def compute_risk_radar(df, trend_score, atr_pctile_1y, short_z, insider_risk_score, event_days, event_reason):
    dollar_vol = df["Close"] * df["Volume"]
    roll20 = dollar_vol.rolling(20).mean()
    latest_dv = float(roll20.iloc[-1]) if pd.notna(roll20.iloc[-1]) else None
    liquidity_pctile = pct_rank(roll20.tail(252), latest_dv) if latest_dv is not None else None
    liquidity_risk = float(100 - liquidity_pctile) if liquidity_pctile is not None else None

    trend_breakdown_risk = float(100 - trend_score) if trend_score is not None else None
    vol_risk = float(atr_pctile_1y) if atr_pctile_1y is not None else None
    short_change_risk = float(np.clip(50 + abs(short_z) * 15, 0, 100)) if short_z is not None else None

    event_risk = None
    if event_days is not None:
        event_risk = float(np.clip(100 - min(event_days, 30) / 30 * 100, 0, 100))

    dims = {
        "liquidity": r2(liquidity_risk, 1),
        "volatility": r2(vol_risk, 1),
        "trend_breakdown": r2(trend_breakdown_risk, 1),
        "short_change": r2(short_change_risk, 1),
        "insider_selling": r2(insider_risk_score, 1) if insider_risk_score is not None else None,
        "event": r2(event_risk, 1),
    }
    return {
        "dims": dims,
        "event_days": event_days,
        "event_reason": event_reason,
        "note": "本格所有分項『分數越高＝風險越大』，與第4/6格的健康分方向相反。",
        "footnotes": {
            "liquidity": "100 − 近20日均成交金額於近252日自身分布中的百分位；成交金額相對自己越低，風險分越高。",
            "volatility": "＝ATR%（14日）於近252日自身分布中的百分位；波動越高風險分越高。",
            "trend_breakdown": "100 − 第4格『趨勢』分項評分。",
            "short_change": "50 + |z值| × 15，截尾 0–100；z值＝放空量比率近30日均值相對近60日的標準化值。",
            "insider_selling": "100 − 第6格『內部人』健康分。",
            "event": "100 − min(距下次財報天數, 30) ÷ 30 × 100；財報日來源 yfinance calendar，查無資料時本項留白。",
        },
    }


# ── panel 9: price × time heatmap (120d, ~weekly columns, high price top) ──
def compute_price_time_heatmap(df, lookback=120, n_price_bins=16, days_per_col=5):
    window = df.tail(lookback)
    if len(window) < days_per_col:
        return None
    typical = (window["High"] + window["Low"] + window["Close"]) / 3
    price_lo, price_hi = float(window["Low"].min()), float(window["High"].max())
    if price_hi <= price_lo:
        return None
    edges = np.linspace(price_lo, price_hi, n_price_bins + 1)
    n_cols = int(np.ceil(len(window) / days_per_col))
    grid = np.zeros((n_price_bins, n_cols))
    week_labels = []
    for col in range(n_cols):
        seg_typical = typical.iloc[col * days_per_col:(col + 1) * days_per_col]
        seg_vol = window["Volume"].iloc[col * days_per_col:(col + 1) * days_per_col]
        if seg_typical.empty:
            week_labels.append("")
            continue
        week_labels.append(seg_typical.index[0].strftime("%m/%d"))
        idxs = np.clip(np.digitize(seg_typical.values, edges) - 1, 0, n_price_bins - 1)
        for bi, vol in zip(idxs, seg_vol.values):
            grid[bi, col] += vol
    grid_high_to_low = grid[::-1]  # row 0 (rendered top) = highest price bin
    bins_high_to_low = [
        {"lo": r2(edges[i]), "hi": r2(edges[i + 1])} for i in range(n_price_bins - 1, -1, -1)
    ]
    return {
        "weeks": week_labels,
        "price_bins": bins_high_to_low,
        "grid": grid_high_to_low.astype(int).tolist(),
        "max_volume": int(grid.max()) if grid.size else 0,
        "method": (
            f"近{lookback}個交易日，每{days_per_col}個交易日一欄（近似一週）、依典型價格((高+低+收)/3)"
            f"分成{n_price_bins}個等寬價位列（高價在上），格內為當欄當列成交量加總，顏色深淺按全表最大值正規化。"
        ),
    }


# ── panel 10: cost distribution (profit vs underwater, volume-weighted) ──
def compute_cost_distribution(df, lookback=120, series_days=60):
    typical = (df["High"] + df["Low"] + df["Close"]) / 3
    vol = df["Volume"]
    close = df["Close"]
    n = len(df)
    start_idx = max(lookback - 1, n - series_days)
    results = []
    for tt in range(start_idx, n):
        w_typical = typical.iloc[max(0, tt - lookback + 1):tt + 1].values
        w_vol = vol.iloc[max(0, tt - lookback + 1):tt + 1].values
        total_vol = w_vol.sum()
        if total_vol <= 0:
            continue
        close_t = float(close.iloc[tt])
        profit_vol = w_vol[w_typical < close_t].sum()
        profit_pct = float(profit_vol / total_vol * 100)
        results.append({
            "date": df.index[tt].strftime("%Y-%m-%d"),
            "profit_pct": r2(profit_pct, 1),
            "underwater_pct": r2(100 - profit_pct, 1),
        })
    return {
        "current": results[-1] if results else None,
        "series": results,
        "method": (
            f"以近{lookback}個交易日每日典型價格((高+低+收)/3)作為當日『成本』，逐一與該日收盤價比較："
            "成本低於收盤者計入『獲利』成交量、高於者計入『套牢』成交量，兩者依成交量加權；"
            f"取近{series_days}個交易日重複計算，畫出比例隨時間變化。"
        ),
    }


# ── panel 12: up/down day volume ─────────────────────────────────────────
def compute_updown_volume(df, window=20):
    close = df["Close"]
    prev_close = close.shift(1)
    up_mask = (close > prev_close).tail(window)
    down_mask = (close < prev_close).tail(window)
    vol_tail = df["Volume"].tail(window)
    up_vol = float(vol_tail[up_mask].sum())
    down_vol = float(vol_tail[down_mask].sum())
    ratio = (up_vol / down_vol) if down_vol > 0 else None
    return {
        "window_days": window,
        "up_volume": int(up_vol),
        "down_volume": int(down_vol),
        "ratio": r2(ratio, 2) if ratio is not None else None,
        "method": f"近{window}個交易日，依收盤價相對前一日漲跌分類，加總上漲日與下跌日各自的成交量。",
    }


# ── panel 13: up/down strength (3 gauges) ────────────────────────────────
def compute_updown_strength(df, window=20):
    close = df["Close"]
    prev_close = close.shift(1)
    ret = close.pct_change()
    tail_close, tail_prev, tail_ret = close.tail(window), prev_close.tail(window), ret.tail(window)
    up_days = int((tail_close > tail_prev).sum())
    pct_up_days = up_days / window * 100

    up_rets = tail_ret[tail_ret > 0]
    down_rets = tail_ret[tail_ret < 0]
    avg_up = float(up_rets.mean() * 100) if len(up_rets) else None
    avg_down = float(abs(down_rets.mean()) * 100) if len(down_rets) else None
    updown_ratio = (avg_up / avg_down) if (avg_up is not None and avg_down) else None
    strength_score = float(np.clip(50 + np.log(updown_ratio) * 30, 0, 100)) if updown_ratio and updown_ratio > 0 else None

    vol20 = float(df["Volume"].tail(20).mean())
    vol60 = float(df["Volume"].tail(60).mean())
    vol_ratio = (vol20 / vol60) if vol60 > 0 else None
    vol_strength_score = float(np.clip(50 + (vol_ratio - 1) * 100, 0, 100)) if vol_ratio is not None else None

    return {
        "gauges": [
            {"key": "up_days_pct", "name_zh": "近20日上漲天數占比", "score": r2(pct_up_days, 1)},
            {"key": "updown_ratio", "name_zh": "漲跌幅比", "score": r2(strength_score, 1) if strength_score is not None else None},
            {"key": "volume_strength", "name_zh": "量能強度", "score": r2(vol_strength_score, 1) if vol_strength_score is not None else None},
        ],
        "raw": {
            "up_days": up_days, "window_days": window,
            "avg_up_day_pct": r2(avg_up, 2) if avg_up is not None else None,
            "avg_down_day_pct": r2(avg_down, 2) if avg_down is not None else None,
            "updown_ratio": r2(updown_ratio, 2) if updown_ratio is not None else None,
        },
        "footnotes": {
            "up_days_pct": "近20日中收盤價高於前一日的天數 ÷ 20 × 100。",
            "updown_ratio": "分數 = 50 + ln(平均上漲日漲幅% ÷ 平均下跌日跌幅%) × 30，截尾0–100；比值>1代表上漲日平均漲幅大於下跌日平均跌幅。",
            "volume_strength": "分數 = 50 + (近20日均量 ÷ 近60日均量 − 1) × 100，截尾0–100。",
        },
    }


# ── panel 14: overheat check (5 metrics, each with own trailing-1y percentile) ──
def compute_overheat_check(df, shares_outstanding):
    close, high, low, vol, open_ = df["Close"], df["High"], df["Low"], df["Volume"], df["Open"]
    n = len(df)
    items = []

    if shares_outstanding:
        turnover = vol / shares_outstanding * 100
        latest = float(turnover.iloc[-1])
        pctile = pct_rank(turnover.tail(252), latest)
        items.append({"key": "turnover", "name_zh": "換手率", "value": r2(latest, 3), "unit": "%",
                      "percentile_1y": r2(pctile, 1) if pctile is not None else None})
    else:
        items.append({"key": "turnover", "name_zh": "換手率", "status": "no_data",
                      "reason": "yfinance info 缺 sharesOutstanding"})

    intraday = (high - low) / close * 100
    latest = float(intraday.iloc[-1])
    pctile = pct_rank(intraday.tail(252), latest)
    items.append({"key": "intraday_range", "name_zh": "日內振幅", "value": r2(latest, 2), "unit": "%",
                  "percentile_1y": r2(pctile, 1) if pctile is not None else None})

    ma21 = df["MA21"]
    dev = (close / ma21 - 1) * 100
    latest = float(dev.iloc[-1])
    pctile = pct_rank(dev.tail(252), latest)
    items.append({"key": "ma21_deviation", "name_zh": "距MA21乖離", "value": r2(latest, 2), "unit": "%",
                  "percentile_1y": r2(pctile, 1) if pctile is not None else None})

    direction = np.sign((close - close.shift(1)).fillna(0).values)
    streak = np.zeros(n)
    for i in range(1, n):
        if direction[i] == 0:
            streak[i] = 0
        elif streak[i - 1] != 0 and np.sign(streak[i - 1]) == direction[i]:
            streak[i] = streak[i - 1] + direction[i]
        else:
            streak[i] = direction[i]
    streak_series = pd.Series(streak, index=df.index)
    latest_streak = int(streak_series.iloc[-1])
    pctile = pct_rank(streak_series.abs().tail(252), abs(latest_streak))
    items.append({"key": "streak", "name_zh": "連漲/連跌天數", "value": latest_streak, "unit": "天",
                  "percentile_1y": r2(pctile, 1) if pctile is not None else None})

    prev_close = close.shift(1)
    gap_flag = ((open_ - prev_close).abs() / prev_close > 0.005).astype(int)
    gap_count_20 = gap_flag.rolling(20).sum()
    latest_gapcount = int(gap_count_20.iloc[-1]) if pd.notna(gap_count_20.iloc[-1]) else None
    pctile = pct_rank(gap_count_20.tail(252), latest_gapcount) if latest_gapcount is not None else None
    items.append({"key": "gap_count", "name_zh": "跳空次數(近20日)", "value": latest_gapcount, "unit": "次",
                  "percentile_1y": r2(pctile, 1) if pctile is not None else None})

    return {
        "items": items,
        "method": "百分位＝該指標近一年（252個交易日）自身分布中的排名；數值高不代表『壞』，只代表相對自己過去一年偏極端。",
        "footnotes": {
            "turnover": "當日成交量 ÷ 流通股數（yfinance sharesOutstanding）。",
            "intraday_range": "(當日最高 − 最低) ÷ 收盤。",
            "ma21_deviation": "(收盤 ÷ MA21 − 1)。",
            "streak": "連續同方向（收盤價相對前一日漲/跌）天數，正值連漲、負值連跌；百分位以絕對值計。",
            "gap_count": "跳空定義：|開盤 − 前一日收盤| ÷ 前一日收盤 > 0.5%；近20日窗口內出現次數。",
        },
    }


# ── panel 16: chip changes (short interest change / holders) ────────────
def fetch_chip_changes(ticker_obj, short_interest_info):
    out = {}
    cur = short_interest_info.get("sharesShort") if isinstance(short_interest_info, dict) else None
    prior = short_interest_info.get("sharesShortPriorMonth") if isinstance(short_interest_info, dict) else None
    out["short_interest_change_pct"] = r2((cur / prior - 1) * 100, 2) if cur and prior else None

    try:
        mh = ticker_obj.major_holders
        if mh is not None and not mh.empty and "Value" in mh.columns:
            d = mh["Value"].to_dict()
            out["insiders_pct_held"] = r2(d.get("insidersPercentHeld", 0) * 100, 2) if d.get("insidersPercentHeld") is not None else None
            out["institutions_pct_held"] = r2(d.get("institutionsPercentHeld", 0) * 100, 2) if d.get("institutionsPercentHeld") is not None else None
        else:
            out["major_holders_status"] = "no_data"
            out["major_holders_reason"] = "yfinance 未回傳 major_holders"
    except Exception as e:  # noqa: BLE001
        out["major_holders_status"] = "no_data"
        out["major_holders_reason"] = str(e)

    try:
        ih = ticker_obj.institutional_holders
        if ih is not None and not ih.empty:
            rows = []
            for _, row in ih.head(10).iterrows():
                rows.append({
                    "holder": row.get("Holder"),
                    "shares": int(row["Shares"]) if pd.notna(row.get("Shares")) else None,
                    "pct_held": r2(row["pctHeld"] * 100, 2) if pd.notna(row.get("pctHeld")) else None,
                    "pct_change": r2(row["pctChange"] * 100, 2) if pd.notna(row.get("pctChange")) else None,
                    "date_reported": str(row.get("Date Reported"))[:10] if pd.notna(row.get("Date Reported")) else None,
                })
            out["institutional_holders"] = rows
        else:
            out["institutional_holders_status"] = "no_data"
            out["institutional_holders_reason"] = "yfinance 未回傳 institutional_holders"
    except Exception as e:  # noqa: BLE001
        out["institutional_holders_status"] = "no_data"
        out["institutional_holders_reason"] = str(e)

    return out


# ── panel 19: data reliability ────────────────────────────────────────────
# NB: a 511-name 2014-2025 backtest of the whole scoring system found ~0 rank
# IC against forward 1-12m excess return, so there is no backtest here any
# more (removed along with the averaged score it used to test) — the page
# does not claim any predictive value for these descriptors.
def compute_data_reliability(as_of_str, short_vol_block, insiders, options, dim_states):
    insider_as_of = None
    if insiders.get("status") == "ok" and insiders.get("transactions"):
        insider_as_of = insiders["transactions"][0].get("date")  # sorted desc -> latest filing
    options_as_of = None
    if options.get("status") == "ok" and options.get("snapshot_generated_at"):
        options_as_of = options["snapshot_generated_at"][:10]

    sources = [
        {"name_zh": "價格/技術指標", "status": "ok", "as_of": as_of_str},
        {"name_zh": "放空量(FINRA)", "status": short_vol_block.get("status", "no_data"), "as_of": as_of_str},
        {"name_zh": "內部人交易", "status": insiders.get("status", "no_data"), "as_of": insider_as_of},
        {"name_zh": "選擇權", "status": options.get("status", "no_data"), "as_of": options_as_of},
    ]
    codes = [v.get("code") for v in (dim_states or {}).values() if v.get("code") is not None]
    consistency = None
    if codes:
        cnt = Counter(codes)
        _, top_n = cnt.most_common(1)[0]
        consistency = {"same_direction": top_n, "total": len(codes)}
    return {
        "sources": sources,
        "signal_consistency": consistency,
        "note": "各來源狀態為本次 build 當下的抓取結果；訊號一致度看第5格四項分項狀態有幾項同方向（不代表方向本身好壞）。",
    }


# ═══════════════════════════════════════════ market context (from /market/) ═
# 大盤環境格的判定來源：docs/market/data/{state,read,read_status}.json（machine
# state + research read layer owned by the market-read pipeline — read-only,
# never written here). We summarize the handful of fields the dashboard needs
# into a small shared file so 545 tickers don't each re-parse ~470KB of JSON,
# and so the page never fetches those big files client-side.
def _parse_leading_number(s):
    """'64 · 緊張' -> 64.0 ; '46.0 · 升溫' -> 46.0"""
    if not s:
        return None
    m = re.match(r"\s*(-?\d+(?:\.\d+)?)", str(s))
    return float(m.group(1)) if m else None


def _first_clause(text, max_len=24):
    if not text:
        return None
    text = str(text).strip()
    for sep in ("，", "。", "：", "；"):
        idx = text.find(sep)
        if 0 < idx <= max_len:
            return text[:idx]
    return text[:max_len]


def _extract_deviation_reason(why, max_len=160):
    """Pick the sentence in a deviations_from_tables `why` blob that explains
    *why the research judgment differs from the table baseline*.
    Clauses (split on ；) that describe the baseline itself (無條件／表格欄／
    帳上／帳簿／基準逐期) are dropped first, and 可證偽 sentences are skipped.
    Priority among what remains: 我低於/我高於 > 因為 > first remaining.
    Over-long picks are cut at the last ，/、 before max_len with an ellipsis."""
    if not why:
        return None
    baseline_kw = ("無條件", "表格欄", "帳上", "帳簿", "基準逐期")
    sentences = []
    for sent in str(why).split("。"):
        sent = sent.strip()
        if not sent or sent.startswith("可證偽"):
            continue
        kept = [c.strip() for c in sent.split("；")
                if c.strip() and not any(k in c for k in baseline_kw)]
        if kept:
            sentences.append("；".join(kept))
    if not sentences:
        return None
    chosen = next((s for s in sentences if "我低於" in s or "我高於" in s), None)
    if chosen is None:
        chosen = next((s for s in sentences if "因為" in s), None)
    if chosen is None:
        chosen = sentences[0]
    if len(chosen) > max_len:
        head = chosen[:max_len]
        cut = max(head.rfind("，"), head.rfind("、"))
        return (head[:cut] if cut > 0 else head) + "……"
    return chosen + "。"


def build_market_context():
    state_path = MARKET_DATA_DIR / "state.json"
    read_path = MARKET_DATA_DIR / "read.json"
    status_path = MARKET_DATA_DIR / "read_status.json"
    if not state_path.exists():
        return {"status": "no_data", "reason": "docs/market/data/state.json 不存在"}

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"status": "no_data", "reason": f"state.json 讀取失敗：{e}"}
    try:
        read = json.loads(read_path.read_text(encoding="utf-8")) if read_path.exists() else {}
    except Exception:  # noqa: BLE001
        read = {}
    try:
        read_status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    except Exception:  # noqa: BLE001
        read_status = {}

    environment = state.get("environment") or []
    env_out = []
    gauges = {}
    for e in environment:
        env_out.append({
            "key": e.get("key"), "label": e.get("label"), "value": e.get("value"),
            "sub": e.get("sub"), "as_of": e.get("as_of"), "stale": bool(e.get("stale")),
            "tone": e.get("tone"),
        })
        if e.get("key") in ("detective", "monitor"):
            gauges[e["key"]] = {
                "score": _parse_leading_number(e.get("value")),
                "label": e.get("value"),
                "as_of": e.get("as_of"),
                "stale": bool(e.get("stale")),
            }

    council_summary = state.get("council_summary") or {}
    horizons = {h.get("key"): h for h in (read.get("horizons") or [])}
    deviations = read.get("deviations_from_tables") or []

    def find_deviation(*keywords):
        for d in deviations:
            claim = d.get("claim", "")
            if all(k in claim for k in keywords):
                return d
        return None

    def council_prob_row(name_zh, council_key, horizon_key, dev_keywords):
        """1m/3m rows: 機械合議 = council_summary.p, 基準 = council_summary.p_clim."""
        c = council_summary.get(council_key) or {}
        h = horizons.get(horizon_key) if horizon_key else None
        research_p = h.get("p_up") if h else None
        council_p = c.get("p")
        row = {
            "name_zh": name_zh,
            "council_p": r2(council_p * 100, 1) if council_p is not None else None,
            "research_p": r2(research_p * 100, 1) if research_p is not None else None,
            "baseline_p": r2(c.get("p_clim") * 100, 1) if c.get("p_clim") is not None else None,
            "baseline_kind": "council_p_clim",
        }
        if research_p is not None and council_p is not None and abs(research_p - council_p) >= 0.10:
            dev = find_deviation(*dev_keywords) if dev_keywords else None
            if dev and dev.get("why"):
                row["deviation_note"] = _extract_deviation_reason(dev["why"])
        return row

    def research_only_prob_row(name_zh, horizon_key, dev_keywords):
        """6m/12m rows: no council figure exists at these horizons — 基準 comes
        from the research read's own falsification table (table_p in
        deviations_from_tables), a different baseline methodology than
        council_summary's p_clim (see prob_table_note)."""
        h = horizons.get(horizon_key) or {}
        research_p = h.get("p_up")
        dev = find_deviation(*dev_keywords)
        baseline_p = dev.get("table_p") if dev else None
        row = {
            "name_zh": name_zh,
            "council_p": None,
            "research_p": r2(research_p * 100, 1) if research_p is not None else None,
            "baseline_p": r2(baseline_p * 100, 1) if baseline_p is not None else None,
            "baseline_kind": "research_table_p",
        }
        if dev and dev.get("why"):
            row["deviation_note"] = _extract_deviation_reason(dev["why"])
        return row

    prob_table = [
        council_prob_row("一個月 SPY 收高", "spy_up_21d", None, []),
        council_prob_row("三個月 SPY 收高", "spy_up_63d", "3m", ["3 個月", "收高"]),
        research_only_prob_row("六個月 SPY 收高", "6m", ["6 個月", "收高"]),
        research_only_prob_row("十二個月 SPY 收高", "12m", ["12 個月", "收高"]),
        council_prob_row("一個月波動升高", "vol_up_21d", None, []),
    ]
    prob_table_note = (
        "「基準」欄兩種算法：一個月／三個月的基準是機械合議自身的歷史頻率（p_clim）；"
        "六個月／十二個月沒有機械合議數字，基準改用研究判讀證偽表的無條件頻率（table_p，"
        "帳簿基準算法）。兩種基準的計算方式不同，不可直接跨列比較。"
    )

    triggers = []
    for t in (state.get("triggers") or [])[:3]:
        triggers.append({"label": t.get("label"), "level": t.get("level"), "why": t.get("why")})

    read_as_of = read.get("as_of")
    valid_days = read.get("valid_days")
    path_lead = _first_clause(read.get("path_zh"))
    forecasts_by_horizon = {
        k: (r2(h.get("p_up") * 100, 1) if h.get("p_up") is not None else None)
        for k, h in horizons.items()
    }

    return {
        "schema": "stock-dash-market-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z",
        "state_as_of": state.get("as_of"),
        "read_as_of": read_as_of,
        "valid_days": valid_days,
        "path_lead_zh": path_lead,
        "forecasts_pct": forecasts_by_horizon,  # {"3m": 47.0, "6m": 50.0, "12m": 55.0}
        "environment": env_out,
        "gauges": gauges,
        "prob_table": prob_table,
        "prob_table_note": prob_table_note,
        "triggers": triggers,
        "read_status": read_status,
        "market_url": "/market/",
        "sources": (
            "docs/market/data/state.json（機械層，零 LLM，日更）＋ "
            "docs/market/data/read.json（研究判讀層，每日 17:15 台北排程）"
        ),
    }


def ensure_market_context():
    """Write docs/stock-dash/data/_market.json on every build.

    Originally this skipped the rewrite when state.json's `as_of` hadn't
    moved, to avoid 545 tickers/day each re-parsing ~470KB of /market/ JSON.
    But state.json (machine layer) and read.json (research-read layer) are
    written by two independent schedules — state.json's as_of can be
    unchanged on a day read.json's judgment already rolled forward, which
    would silently freeze the dashboard on a stale judgment. The output file
    is only ~3KB, so the simplest correct fix is to always regenerate it;
    the marginal cost of re-parsing two JSON files per ticker build is not
    worth the staleness risk of a two-key freshness check.
    """
    state_path = MARKET_DATA_DIR / "state.json"
    if not state_path.exists():
        return
    ctx = build_market_context()
    MARKET_CONTEXT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Atomic write (tmp + os.replace): this function is called by every single
    # ticker's build and, unlike the other shared files, always rewrites (see
    # docstring above) — a batch run now builds many tickers in parallel
    # (build_stock_dash_all.py), so several processes can call this at the same
    # moment. A plain write_text() from N processes could interleave and hand a
    # concurrent reader/writer a half-written file; os.replace() is atomic on
    # both POSIX and Windows, so every reader always sees a complete JSON body.
    tmp_path = MARKET_CONTEXT_PATH.with_suffix(MARKET_CONTEXT_PATH.suffix + f".tmp{os.getpid()}")
    tmp_path.write_text(json.dumps(ctx, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp_path, MARKET_CONTEXT_PATH)


def compute_market_beta(ticker, df, spy_df, window=252):
    """Trailing-1y beta & correlation of this ticker's daily returns to SPY."""
    r_t = df["Close"].pct_change()
    r_s = spy_df["Close"].pct_change()
    aligned = pd.DataFrame({"t": r_t, "s": r_s}).dropna().tail(window)
    if len(aligned) < 30:
        return None
    var_s = aligned["s"].var()
    if not var_s or var_s <= 0:
        return None
    beta = float(aligned["t"].cov(aligned["s"]) / var_s)
    corr = float(aligned["t"].corr(aligned["s"]))
    direction = "跌" if beta >= 0 else "漲"
    sentence = (
        f"過去一年，大盤每跌 1%，{ticker} 平均{direction}約 {abs(beta):.2f}%"
        f"（相關係數 {corr:.2f}）。"
    )
    return {
        "window_days": len(aligned),
        "beta": r2(beta, 2),
        "correlation": r2(corr, 2),
        "sentence_zh": sentence,
        "method": "近一年（最多252個交易日）逐日報酬對 SPY 做迴歸，斜率＝beta；相關係數為同期報酬的皮爾森相關係數。",
    }


# ═══════════════════════════════════════════════════ 研判核心 (judgment core) ═
# Phase 7 — 7 張卡的資料準備。原則：dd-screener（docs/dd-screener/latest.json）
# 已有的欄位一律直接讀，不重算；FunnelRank 相關公式只做「呈現與拆解」，公式本身
# 抄自 scripts/build_dd_screener.py 供顯示用（唯讀參考，不 import、不改動該檔）。
# yfinance 只補 dd-screener 沒有的東西（財報驚喜、分析師評等異動家數、內部人逐筆
# 交易明細）。
# 2026-09-22 更正：護城河與 ROIC durability 兩塊改回讀 DD 報告的 dd-meta／§護城河
# 內文（見下方「護城河」區塊），其餘卡片仍完全不讀 DD、只用 dd-screener。
DD_SCREENER_LATEST_PATH = ROOT / "docs" / "dd-screener" / "latest.json"      # read-only source
EPS_SNAPSHOT_DIR = ROOT / "docs" / "dd-screener" / "eps-estimates-snapshots"  # read-only source
SUE_BREAKS_PATH = OUT_DIR / "_sue_breaks.json"        # shared file this script writes
PEAD_EVENTS_CSV = Path.home() / "v7-backtest" / "results" / "pead" / "pead_events.csv"  # read-only, outside repo
INSIDER_CLUSTER_WINDOW_DAYS = 90
DD_DIR = ROOT / "docs" / "dd"  # read-only source（不含 docs/dd/brief/，檔名前綴不同天生排除）

# FunnelRank 常數 —— 唯讀抄自 scripts/build_dd_screener.py（不 import、不重算），
# 只用來把 latest.json 已存的分數拆解顯示。若上游調整權重／門檻，這裡要跟著更新。
FUNNEL_WEIGHTS = {"quality": 0.40, "moat": 0.30, "revision": 0.30}
FUNNEL_QUALITY_CRITERIA_DISPLAY = [
    {"key": "fcf", "label": "FCF≥10%", "unit": "%", "threshold": 10.0, "invert": False},
    {"key": "roic", "label": "ROIC≥15%", "unit": "%", "threshold": 15.0, "invert": False},
    {"key": "eps2y", "label": "FY+1→FY+3 CAGR≥15%", "unit": "%", "threshold": 15.0, "invert": False},
    {"key": "peg", "label": "PEG≤2.0x", "unit": "x", "threshold": 2.0, "invert": True},
]
FUNNEL_DE_REFERENCE_DISPLAY = {"key": "de", "label": "D/E≤0.7x（僅參考，不計分）", "unit": "x", "threshold": 0.7}
FUNNEL_MOAT_TREND_MULT_DISPLAY = {"↑": 1.10, "→": 1.00, "↓": 0.80}
FUNNEL_REVISION_THRESHOLD = 0.5
FUNNEL_REVISION_FY_WEIGHTS_DISPLAY = {"fy1": 0.2, "fy2": 0.3, "fy3": 0.5}


# ── dd-screener loader (cached; ~2.85MB, read once per process) ─────────────
_dd_screener_cache = None


def load_dd_screener():
    global _dd_screener_cache
    if _dd_screener_cache is not None:
        return _dd_screener_cache
    if not DD_SCREENER_LATEST_PATH.exists():
        _dd_screener_cache = {"status": "no_data", "reason": "docs/dd-screener/latest.json 不存在", "stocks": []}
        return _dd_screener_cache
    try:
        d = json.loads(DD_SCREENER_LATEST_PATH.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        _dd_screener_cache = {"status": "no_data", "reason": f"docs/dd-screener/latest.json 讀取失敗：{e}", "stocks": []}
        return _dd_screener_cache
    _dd_screener_cache = {
        "status": "ok", "as_of": d.get("as_of"), "universe_size": d.get("universe_size"),
        "stocks": d.get("stocks", []), "roic_decomp_summary": d.get("roic_decomp_summary"),
    }
    return _dd_screener_cache


def find_dd_screener_row(ticker):
    """回傳 (row_or_None, dd_meta)。ticker 不在 339 檔名單就回 None，呼叫端要顯示
    「不在 dd-screener 名單（339 檔）」，不能改用別的資料源頂替。"""
    dd = load_dd_screener()
    if dd.get("status") != "ok":
        return None, dd
    for row in dd["stocks"]:
        if row.get("ticker") == ticker:
            return row, dd
    return None, dd


# ── 財年代號推算（Correction 2：不能再靠 DD dd-meta 的 fy_end_month）───────────
def derive_fy_labels(info, yf_fy_label_note=None):
    """用 yfinance info['nextFiscalYearEnd']（進行中財年的財年結束日）推「今年度／
    明年度／後年度」的財年代號（如 FY27／FY28／FY29）。推不出來就退回泛用名稱。
    yf_fy_label_note 是 dd-screener 該列原始的 yf_fy_label 欄位值，只放進 method
    說明文字供交叉核對，不參與推算（該欄位語意是 xlsx 抓取時的財年位移標記，不是
    人類可讀的財年代號）。"""
    generic = {"curr": "今年度", "next": "明年度", "fy3": "後年度"}
    ts = info.get("nextFiscalYearEnd") if info else None
    if not ts:
        return {**generic, "derived": False,
                "method": "yfinance info 沒有 nextFiscalYearEnd，財年代號推不出來，改用「今年度／明年度／後年度」。"}
    try:
        y = datetime.fromtimestamp(ts, tz=timezone.utc).year
    except Exception:  # noqa: BLE001
        return {**generic, "derived": False,
                "method": "yfinance nextFiscalYearEnd 時間戳解析失敗，改用「今年度／明年度／後年度」。"}
    yy = y % 100
    note = f"（dd-screener 原始欄位 yf_fy_label={yf_fy_label_note}，僅供交叉核對）" if yf_fy_label_note else ""
    return {
        "curr": f"FY{yy:02d}", "next": f"FY{(yy + 1) % 100:02d}", "fy3": f"FY{(yy + 2) % 100:02d}",
        "derived": True,
        "method": f"用 yfinance info['nextFiscalYearEnd']（{y} 年）當進行中的財年，往後推三個財年代號{note}。",
    }


# ── EPS 估值月度快照（docs/dd-screener/eps-estimates-snapshots/）─────────────
_eps_snapshot_cache = {}


def load_eps_snapshot_by_date(snapshot_date):
    if not snapshot_date:
        return None
    if snapshot_date in _eps_snapshot_cache:
        return _eps_snapshot_cache[snapshot_date]
    found = None
    if EPS_SNAPSHOT_DIR.exists():
        for f in sorted(EPS_SNAPSHOT_DIR.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            if d.get("snapshot_date") == snapshot_date:
                found = d
                break
    _eps_snapshot_cache[snapshot_date] = found
    return found


def load_eps_snapshot_before(date_str):
    """護城河追蹤用：找嚴格早於 date_str（如 DD 日期）、snapshot_date 最接近的一份月度
    快照，作為「DD 當時」的 EPS 估值基準。找不到回 None（不外推、不拿更早的湊）。"""
    if not date_str or not EPS_SNAPSHOT_DIR.exists():
        return None
    best = None
    for f in sorted(EPS_SNAPSHOT_DIR.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        sd = d.get("snapshot_date")
        if not sd or sd >= date_str:
            continue
        if best is None or sd > best.get("snapshot_date", ""):
            best = d
    return best


# 快照存的是 Koyfin 原始口徑（ADR 股票是普通股口徑、美元按當天匯率），latest.json 的
# 現值已經過 apply_adr_ratio。比較前要跟 build_dd_screener.py 一樣：基準先換成 ADR
# 口徑，再換回財報幣別算修正率（eps_fx_normalize），否則 TSM 會出現 ×5 的假上修、
# 非美元財報的公司會把匯率波動當成修正。
_SNAP_TO_ADR_KEY = {"eps_fy_curr": "fy1", "eps_fy_next": "fy2", "eps_fy3": "fy3"}
_rep_ccy_cache = None
_fx_cache = None


def _snapshot_eps_adr(ticker, trow):
    """快照列的 eps_fy_curr／eps_fy_next／eps_fy3 → ADR 口徑（非 ADR 股票原樣）。"""
    from load_eps_estimates_xlsx import apply_adr_ratio
    raw = {v: trow.get(k) for k, v in _SNAP_TO_ADR_KEY.items()}
    adj = apply_adr_ratio(ticker, raw) or raw
    return {k: adj.get(v) for k, v in _SNAP_TO_ADR_KEY.items()}


def _fx_pair(ticker, current_date, baseline_date):
    """(財報幣別, 現值日匯率, 基準日匯率)；只讀快取＋必要時抓，不寫回 data/ 快取檔。"""
    global _rep_ccy_cache, _fx_cache
    from eps_fx_normalize import (get_fx_rate, get_reporting_currency,
                                  load_fx_daily_cache, load_reporting_currency_cache)
    if _rep_ccy_cache is None:
        _rep_ccy_cache = load_reporting_currency_cache()
    if _fx_cache is None:
        _fx_cache = load_fx_daily_cache()
    ccy = get_reporting_currency(ticker, ticker, _rep_ccy_cache)
    if not ccy or ccy == "USD":
        return ccy, None, None
    return ccy, get_fx_rate(ccy, current_date, _fx_cache), get_fx_rate(ccy, baseline_date, _fx_cache)


def _fy_revision_pct_from_snapshot(current_val, snapshot, ticker, fy_key, current_date=None):
    if snapshot is None or current_val is None:
        return None
    trow = (snapshot.get("tickers") or {}).get(ticker)
    if not trow:
        return None
    base = _snapshot_eps_adr(ticker, trow).get(fy_key)
    if base in (None, 0):
        return None
    from eps_fx_normalize import compute_fx_normalized_revision
    base_date = str(snapshot.get("snapshot_date") or "")[:10]
    ccy, fx_cur, fx_base = _fx_pair(ticker, current_date, base_date) if current_date else (None, None, None)
    pct, _ = compute_fx_normalized_revision(current_val, base, ccy, fx_cur, fx_base)
    return pct


def build_eps_snapshot_timeseries(ticker):
    """全部 7 份月度快照裡，這檔的 明年度／後年度 EPS 估計，依快照日期排序 —— 給
    第②格「股價 vs EPS 估值」疊圖用。同一天有兩個檔案（如 2026-05.json /
    2026-05-25.json 都是 2026-05-26）時，用檔名排序較後者覆蓋（較新流程產出）。"""
    if not EPS_SNAPSHOT_DIR.exists():
        return {"status": "no_data", "reason": "docs/dd-screener/eps-estimates-snapshots/ 目錄不存在"}
    dedup = {}
    for f in sorted(EPS_SNAPSHOT_DIR.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        sd = str(d.get("snapshot_date") or "")[:10]   # 有些快照日期帶說明文字，只取日期
        trow = (d.get("tickers") or {}).get(ticker)
        if not sd or not trow:
            continue
        adj = _snapshot_eps_adr(ticker, trow)
        dedup[sd] = {"snapshot_date": sd, "eps_fy_next": adj.get("eps_fy_next"), "eps_fy3": adj.get("eps_fy3")}
    # 最後一點＝latest.json 目前值（快照目錄只存過去的基準，不含當期）
    row, dd = find_dd_screener_row(ticker)
    if row is not None and dd.get("as_of"):
        dedup[str(dd["as_of"])[:10]] = {"snapshot_date": str(dd["as_of"])[:10],
                                        "eps_fy_next": row.get("eps_fy_next"), "eps_fy3": row.get("eps_fy3")}
    points = sorted(dedup.values(), key=lambda p: p["snapshot_date"])
    if not points:
        return {"status": "no_data", "reason": f"{ticker} 不在任何月度 EPS 估值快照檔案中"}
    return {"status": "ok", "points": points}


def _price_pct_change_since(df_full, since_date_str, current_price):
    """自 since_date_str 後第一個交易日算到現在的股價漲跌幅（%），回傳
    (漲跌幅, 實際採用的基準交易日)。找不到就回 (None, None)。"""
    if not since_date_str:
        return None, None
    try:
        since_ts = pd.Timestamp(since_date_str)
    except Exception:  # noqa: BLE001
        return None, None
    sub = df_full[df_full.index >= since_ts]
    if sub.empty:
        return None, None
    base_price = float(sub["Close"].iloc[0])
    if base_price == 0:
        return None, None
    return (current_price / base_price - 1) * 100.0, sub.index[0].strftime("%Y-%m-%d")


# ── ①獲利預估與修正 ──────────────────────────────────────────────────────────
def fetch_analyst_revision_counts(ticker_obj, as_of_date, window_days=30):
    """EPS 預估修正家數（yfinance Ticker.eps_revisions）：今年度 0y、明年度 +1y
    各自近 7／30 天上修與下修的分析師家數。不是評等調升／調降。"""
    try:
        er = ticker_obj.eps_revisions
    except Exception as e:  # noqa: BLE001
        return {"status": "no_data", "reason": f"yfinance eps_revisions 例外：{e}"}
    if er is None or er.empty:
        return {"status": "no_data", "reason": "yfinance 未回傳 eps_revisions"}

    def _i(row, col):
        v = row.get(col)
        return int(v) if v is not None and not pd.isna(v) else None

    periods = {}
    for key in ("0y", "+1y"):
        if key not in er.index:
            continue
        row = er.loc[key]
        periods[key] = {
            "up_7d": _i(row, "upLast7days"), "up_30d": _i(row, "upLast30days"),
            "down_7d": _i(row, "downLast7Days"), "down_30d": _i(row, "downLast30days"),
        }
    if not periods:
        return {"status": "no_data", "reason": "eps_revisions 沒有 0y／+1y 列"}
    return {
        "status": "ok",
        "window_days": window_days,
        "periods": periods,
        "method": ("yfinance Ticker.eps_revisions：今年度（0y）與明年度（+1y）EPS 預估，"
                   "近 7／30 天上修與下修的分析師家數。只算獲利預估的修正方向，不是評等異動或目標價。"),
    }


def fetch_prev_fy_actual_eps(ticker_obj, card1):
    """前一財年實際 EPS（yfinance earnings_estimate 的 0y.yearAgoEps，跟分析師預估同口徑；
    dd-screener 內部也用同一欄算成長，但沒寫進 latest.json）。只在 yfinance 的 0y 預估跟
    本頁今年度預估差 3% 以內時採用，避免財年標籤錯位。刻意不放進 eps_revision（判斷層，
    沒觸發不改版），獨立成 judgment_core.eps_prev_fy，每次 build 都更新。"""
    try:
        cur = card1["table"][0]["current_estimate"] if card1.get("status") == "ok" and card1.get("table") else None
        curr_label = (card1.get("fy_labels") or {}).get("curr") or ""
        ee = ticker_obj.earnings_estimate
        if ee is None or "0y" not in ee.index:
            return {"status": "no_data", "reason": "yfinance 沒有 0y 預估"}
        avg, yag = ee.loc["0y"].get("avg"), ee.loc["0y"].get("yearAgoEps")
        if yag is None or pd.isna(yag) or not yag:
            return {"status": "no_data", "reason": "yfinance 沒有前一年實際 EPS"}
        if cur is None or avg is None or pd.isna(avg) or abs(float(avg) / cur - 1) > 0.03:
            return {"status": "no_data", "reason": f"yfinance 今年度預估 {avg} 跟本頁 {cur} 對不上，財年可能錯位，不採用"}
        m = re.match(r"FY(\d+)", curr_label)
        prev_label = f"FY{int(m.group(1)) - 1:02d}" if m else "前一年"
        return {"status": "ok", "fy": prev_label, "actual_eps": round(float(yag), 4),
                "method": "yfinance Ticker.earnings_estimate 的 0y.yearAgoEps（前一財年實際，與預估同口徑）"}
    except Exception as e:  # noqa: BLE001
        return {"status": "no_data", "reason": f"yfinance earnings_estimate 例外：{e}"}


def build_cockpit_status(ticker):
    """選股主控台（/cockpit/）的陣容狀態，讀 docs/engine/arena.json（擁有層引擎週更）。
    分組與主控台「陣容」表一致：核心席 core_seats、等待池 sat_seats、核心板凳 core_bench；
    都不在就看 not_in_pool，再不在就是不在主控台名單。時機燈照抄引擎給的 lamp.label。"""
    path = OUT_DIR.parent.parent / "engine" / "arena.json"
    try:
        a = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"status": "no_data", "reason": f"讀不到 engine/arena.json：{e}"}
    out = {"status": "ok", "as_of": str(a.get("run_timestamp") or "")[:10],
           "regime": (a.get("regime") or {}).get("label"), "group": "不在主控台名單", "position": None, "lamp": None}
    for key, name in (("core_seats", "核心席"), ("sat_seats", "等待池"), ("core_bench", "核心板凳"), ("not_in_pool", "不在席位池")):
        for i, x in enumerate(a.get(key) or [], 1):
            if x.get("ticker") == ticker:
                out.update({"group": name, "position": i if key in ("core_seats", "sat_seats") else None,
                            "lamp": (x.get("lamp") or {}).get("label"), "route_why": x.get("route_why")})
                return out
    return out


def build_analyst_targets(info, price):
    """分析師目標價與 52 週區間，每次 build 都用 yfinance Ticker.info 重新計算。刻意不放
    進 judgment_core／JUDGMENT_SECTIONS：舊的 dd_screener_fields 價格尺（空頭價／DD 時股價／
    多頭價…）來自寫報告當下的 dd-screener 快照，沒觸發版本條件就不會換版；這裡的目標價與
    52 週區間本質上是每天都可能變的行情層資料，所以跟 cockpit／eps_prev_fy 一樣放在
    full 頂層，永遠用最新一次 fetch 的 info 重算，缺欄位就回 None，不沿用舊值。"""
    target_low = info.get("targetLowPrice")
    target_median = info.get("targetMedianPrice")
    target_mean = info.get("targetMeanPrice")
    target_high = info.get("targetHighPrice")
    num_analysts = info.get("numberOfAnalystOpinions")
    week52_low = info.get("fiftyTwoWeekLow")
    week52_high = info.get("fiftyTwoWeekHigh")

    if all(v is None for v in (target_low, target_median, target_mean, target_high, week52_low, week52_high)):
        return {"status": "no_data", "reason": "yfinance info 未回傳分析師目標價／52 週區間欄位"}

    upside_to_mean_pct = r2((target_mean / price - 1) * 100, 2) if target_mean and price else None
    pct_in_52w_range = (
        r2((price - week52_low) / (week52_high - week52_low) * 100, 1)
        if week52_low is not None and week52_high is not None and week52_high > week52_low else None
    )

    return {
        "status": "ok",
        "target_low": r2(target_low), "target_median": r2(target_median),
        "target_mean": r2(target_mean), "target_high": r2(target_high),
        "num_analysts": num_analysts,
        "week52_low": r2(week52_low), "week52_high": r2(week52_high),
        "upside_to_mean_pct": upside_to_mean_pct,
        "pct_in_52w_range": pct_in_52w_range,
        "price_ruler": [
            {"label": "52週低", "value": r2(week52_low)},
            {"label": "目標價低", "value": r2(target_low)},
            {"label": "目前股價", "value": r2(price)},
            {"label": "目標價中位數", "value": r2(target_median)},
            {"label": "目標價平均", "value": r2(target_mean)},
            {"label": "目標價高", "value": r2(target_high)},
            {"label": "52週高", "value": r2(week52_high)},
        ],
        "method": ("yfinance Ticker.info：targetLowPrice／targetMedianPrice／targetMeanPrice／"
                   "targetHighPrice／numberOfAnalystOpinions／fiftyTwoWeekLow／fiftyTwoWeekHigh，"
                   "每次 build 都重抓，不進判斷層版本控制。"),
    }


def build_card_eps_revision(ticker, row, info, analyst_rev):
    fy_labels = derive_fy_labels(info, row.get("yf_fy_label") if row else None)
    if row is None:
        return {"status": "no_data", "reason": "不在 dd-screener 名單（339 檔）", "fy_labels": fy_labels,
                "analyst_revisions_30d": analyst_rev}

    fund = row.get("fund") or {}
    fy_keys = ["eps_fy_curr", "eps_fy_next", "eps_fy3"]
    fy_names = [fy_labels["curr"], fy_labels["next"], fy_labels["fy3"]]
    revision_pct_keys = ["eps_fy_curr_revision_pct", "eps_fy_next_revision_pct", "eps_fy3_revision_pct"]

    dd_as_of = str(load_dd_screener().get("as_of") or "")[:10] or None
    snap_1m = load_eps_snapshot_by_date(row.get("eps_revision_baseline_date"))
    snap_3m = load_eps_snapshot_by_date(row.get("eps_rev_3m_baseline_date"))
    snap_since = load_eps_snapshot_by_date(row.get("eps_rev_since_earnings_baseline_date"))

    table_rows = []
    for name, fk, revk in zip(fy_names, fy_keys, revision_pct_keys):
        cur_val = row.get(fk)
        table_rows.append({
            "fy": name,
            "current_estimate": r2(cur_val, 2),
            "vs_last_month_pct": r2(row.get(revk), 2),
            "vs_3m_ago_pct": r2(_fy_revision_pct_from_snapshot(cur_val, snap_3m, ticker, fk, dd_as_of), 2),
            "vs_since_earnings_pct": r2(_fy_revision_pct_from_snapshot(cur_val, snap_since, ticker, fk, dd_as_of), 2),
        })

    def _snap_val(snap, fk):
        if not snap:
            return None
        trow = snap.get("tickers", {}).get(ticker)
        return r2(_snapshot_eps_adr(ticker, trow).get(fk), 2) if trow else None

    eps_path_chart = {
        "fy_labels": fy_names,
        "series": [
            {"name": "目前共識", "values": [r2(row.get(fk), 2) for fk in fy_keys]},
            {"name": "上個月快照" + (f"（{row['eps_revision_baseline_date']}）" if row.get("eps_revision_baseline_date") else "（無資料）"),
             "values": [_snap_val(snap_1m, fk) for fk in fy_keys]},
            {"name": "3個月前快照" + (f"（{row['eps_rev_3m_baseline_date']}）" if row.get("eps_rev_3m_baseline_date") else "（無資料）"),
             "values": [_snap_val(snap_3m, fk) for fk in fy_keys]},
        ],
    }

    rev_yoy_bars = [
        {"label": "上上上季", "value": r2(fund.get("rev_yoy_fq3_pct"), 2)},
        {"label": "上上季", "value": r2(fund.get("rev_yoy_fq2_pct"), 2)},
        {"label": "上季", "value": r2(fund.get("rev_yoy_fq1_pct"), 2)},
        {"label": "最新季", "value": r2(fund.get("rev_yoy_fq0_pct"), 2)},
    ]

    return {
        "status": "ok",
        "fy_labels": fy_labels,
        "table": table_rows,
        "table_baseline_dates": {
            "vs_last_month": row.get("eps_revision_baseline_date"),
            "vs_3m_ago": row.get("eps_rev_3m_baseline_date"),
            "vs_since_earnings": row.get("eps_rev_since_earnings_baseline_date"),
            "since_earnings_anchor": row.get("eps_rev_anchor"),
            "since_earnings_days": row.get("eps_rev_since_earnings_days"),
        },
        "table_method": (
            "「較上月」直接用 dd-screener 已經算好的逐財年修正百分比；「近 3 個月」與「自上次財報以來」"
            "改用當時的月度 EPS 估值快照（docs/dd-screener/eps-estimates-snapshots/）比對現在的估值，"
            "逐財年重算 (現在−快照)÷|快照|×100%，算法跟 dd-screener 算「較上月」一樣，只是換比較基準日；"
            "快照缺該財年資料就記為無資料。"
        ),
        "eps_path_chart": eps_path_chart,
        "rev_yoy_bars": rev_yoy_bars,
        "cagr_3y": {
            "eps_cagr_3y_pct": r2(fund.get("est_eps_cagr_3y_pct"), 2),
            "rev_cagr_3y_pct": r2(fund.get("est_rev_cagr_3y_pct"), 2),
        },
        "analyst_revisions_30d": analyst_rev,
    }


# ── ②股價趨勢×獲利（含原「趨勢狀態」內容合併）────────────────────────────────
def build_card_price_vs_eps(ticker, row, df_full, current_price, card1):
    if row is None:
        return {"status": "no_data", "reason": "不在 dd-screener 名單（339 檔），股價 vs 獲利估值比較無法進行"}

    fund = row.get("fund") or {}
    fy_next_row = {}
    if card1.get("status") == "ok" and len(card1.get("table", [])) > 1:
        fy_next_row = card1["table"][1]

    # 股價起點＝EPS 基準快照日（dd-screener 取財報前最後一次快照），兩邊同一個起點，
    # 推出來的本益比變化才不會混到兩段不同期間。
    price_chg_since_earn, since_earn_base_date = _price_pct_change_since(
        df_full, row.get("eps_rev_since_earnings_baseline_date") or row.get("last_earnings_date"), current_price)
    price_chg_1m, base_1m_date = _price_pct_change_since(
        df_full, row.get("eps_revision_baseline_date"), current_price)
    price_chg_3m, base_3m_date = _price_pct_change_since(
        df_full, row.get("eps_rev_3m_baseline_date"), current_price)

    def _implied_pe_chg(price_chg, eps_chg):
        if price_chg is None or eps_chg is None or eps_chg <= -99.9:
            return None
        return ((1 + price_chg / 100.0) / (1 + eps_chg / 100.0) - 1) * 100.0

    eps_chg_since_earn = fy_next_row.get("vs_since_earnings_pct")
    eps_chg_1m = fy_next_row.get("vs_last_month_pct")
    eps_chg_3m = fy_next_row.get("vs_3m_ago_pct")

    periods = [
        {
            "label": "上次財報前後",
            "earnings_date": row.get("last_earnings_date"),
            "base_date": since_earn_base_date or row.get("last_earnings_date"),
            "price_chg_pct": r2(price_chg_since_earn, 2),
            "eps_fy_next_chg_pct": eps_chg_since_earn,
            "implied_ntm_pe_chg_pct": r2(_implied_pe_chg(price_chg_since_earn, eps_chg_since_earn), 2),
        },
        {
            "label": "近1個月",
            "base_date": base_1m_date or row.get("eps_revision_baseline_date"),
            "price_chg_pct": r2(price_chg_1m, 2),
            "eps_fy_next_chg_pct": eps_chg_1m,
            "implied_ntm_pe_chg_pct": r2(_implied_pe_chg(price_chg_1m, eps_chg_1m), 2),
        },
        {
            "label": "近3個月",
            "base_date": base_3m_date or row.get("eps_rev_3m_baseline_date"),
            "price_chg_pct": r2(price_chg_3m, 2),
            "eps_fy_next_chg_pct": eps_chg_3m,
            "implied_ntm_pe_chg_pct": r2(_implied_pe_chg(price_chg_3m, eps_chg_3m), 2),
        },
    ]

    eps_ts = build_eps_snapshot_timeseries(ticker)
    price_series = None
    if eps_ts.get("status") == "ok" and eps_ts["points"]:
        start = pd.Timestamp(eps_ts["points"][0]["snapshot_date"])
        sub = df_full[df_full.index >= start]
        price_series = [{"date": idx.strftime("%Y-%m-%d"), "close": r2(row2["Close"])} for idx, row2 in sub.iterrows()]

    return {
        "status": "ok",
        "periods": periods,
        "period_method": (
            "股價漲跌用 yfinance 收盤價，自比較基準日後第一個交易日算到現在；獲利估值變動用明年度"
            "（NTM 代理）EPS 估計的變動，算法跟第①格「較上月／近3個月／自上次財報以來」一樣；隱含本益比變動"
            "≈ (1+股價漲跌%)÷(1+EPS估值變動%)−1，股價漲幅大於獲利估值漲幅代表隱含本益比同步擴張，"
            "反之則收斂，這只是算術換算，不是重新估值。"
        ),
        "pe_bullet": {
            "pe_ntm_x": fund.get("pe_ntm_x"),
            "pe_ntm_5y_avg_x": fund.get("pe_ntm_5y_avg_x"),
            "pct_5y": row.get("pct_5y"),
            "live_peg": row.get("live_peg"),
        },
        "eps_price_overlay": {
            "eps_points": eps_ts.get("points") if eps_ts.get("status") == "ok" else [],
            "eps_status": eps_ts.get("status"), "eps_reason": eps_ts.get("reason"),
            "price_series": price_series or [],
            "method": ("EPS 點：每份月度估值快照的明年度／後年度 EPS 值，依快照日期繪製；股價：yfinance 日"
                       "收盤價，從第一份快照的日期開始，雙軸疊圖，同一張圖時間軸對齊。"),
        },
        "dist_ath_pct": row.get("ma", {}).get("dist_ath_pct") if isinstance(row.get("ma"), dict) else None,
        "dist_ath_source": "dd-screener latest.json 的 ma.dist_ath_pct（近似歷史新高，非本頁自算）",
    }


# ── ③財報驚喜 ────────────────────────────────────────────────────────────────
def fetch_earnings_dates_df(ticker_obj, limit=20):
    try:
        ed = ticker_obj.get_earnings_dates(limit=limit)
    except Exception as e:  # noqa: BLE001
        return None, f"yfinance get_earnings_dates 例外：{e}"
    if ed is None or ed.empty:
        return None, "yfinance 未回傳 earnings_dates"
    ed = ed.sort_index()
    idx = ed.index
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    ed.index = idx
    return ed, None


def fetch_earnings_surprises(ed, err, n=8):
    if ed is None:
        return {"status": "no_data", "reason": err}
    reported = ed[ed["Reported EPS"].notna()].tail(n)
    if reported.empty:
        return {"status": "no_data", "reason": "近期無已公布財報的 Surprise% 資料"}
    quarters = [{
        "date": dt.strftime("%Y-%m-%d"),
        "eps_estimate": r2(r.get("EPS Estimate"), 3),
        "reported_eps": r2(r.get("Reported EPS"), 3),
        "surprise_pct": r2(r.get("Surprise(%)"), 2),
    } for dt, r in reported.iterrows()]
    return {"status": "ok", "quarters": quarters,
            "method": ("yfinance Ticker.get_earnings_dates()，取有 Reported EPS 的最近 8 季，Surprise% 是 "
                       "yfinance 自帶欄位（實際 EPS 對分析師預估 EPS 的百分比差）。")}


def compute_sue(ed, err):
    """SUE（Standardized Unexpected Earnings）＝(本季EPS−去年同季EPS)÷過去8組同季年增差
    的標準差(ddof=1)。年增差需相隔 340–385 天才計入，湊不滿 8 組記為無資料。方法對齊
    ~/v7-backtest 的 PEAD 回測規格；EPS 用 yfinance Reported EPS（分析師慣例口徑），跟
    回測用的 SEC GAAP 稀釋 EPS 口徑不同——分組對照僅供參考，見下方 sue_breaks 說明。"""
    if ed is None:
        return {"status": "no_data", "reason": err}
    reported = ed[ed["Reported EPS"].notna()]
    dates = list(reported.index.to_pydatetime())
    eps_vals = list(reported["Reported EPS"].values)
    n = len(eps_vals)
    if n < 12:
        return {"status": "no_data",
                "reason": f"yfinance 已公布財報季數不足 12 季（僅 {n} 季），無法湊滿 8 組年增差算標準差"}

    season_diffs = []
    for k in range(8):
        i = n - 1 - k
        j = i - 4
        if j < 0:
            return {"status": "no_data", "reason": f"只湊到 {len(season_diffs)} 組年增差，不足 8 組"}
        days = abs((dates[i] - dates[j]).days)
        if not (340 <= days <= 385):
            return {"status": "no_data",
                    "reason": f"第 {k + 1} 組同季年增差的財報間隔為 {days} 天，不在 340–385 天正常範圍，"
                              "可能財報季別不規則"}
        season_diffs.append(eps_vals[i] - eps_vals[j])

    sigma_8q = float(np.std(season_diffs, ddof=1))
    if sigma_8q == 0:
        return {"status": "no_data", "reason": "過去 8 組年增差標準差為 0，SUE 無法計算"}
    sue = season_diffs[0] / sigma_8q
    return {
        "status": "ok", "sue": r2(sue, 3),
        "latest_period_end": dates[-1].strftime("%Y-%m-%d"),
        "latest_reported_eps": r2(eps_vals[-1], 3),
        "latest_season_diff": r2(season_diffs[0], 4),
        "sigma_8q": r2(sigma_8q, 4),
        "n_quarters_used": n,
        "method": ("SUE＝(本季EPS−去年同季EPS)÷過去8組同季年增差的標準差(ddof=1)；年增差需相隔340–385天才計入。"
                   "EPS 用 yfinance Reported EPS（分析師慣例口徑），跟 PEAD 回測用的 SEC GAAP 稀釋 EPS 口徑不同，"
                   "方法對齊 ~/v7-backtest 的 PEAD 回測規格。"),
    }


def build_sue_breaks():
    if not PEAD_EVENTS_CSV.exists():
        # PEAD_EVENTS_CSV only exists on the owner's Mac (v7-backtest is a sibling
        # repo, not checked out in CI). A committed small reference snapshot
        # (percentile cuts only, no raw event rows) keeps the SUE 分組對照 feature
        # working on a CI runner that has never had access to the real file —
        # ensure_sue_breaks() below prefers a previously-built _sue_breaks.json
        # over this when one is available (e.g. restored from the prior daily
        # run's artifact), so this reference is only a cold-start fallback.
        if SUE_BREAKS_REFERENCE_PATH.exists():
            try:
                ref = json.loads(SUE_BREAKS_REFERENCE_PATH.read_text(encoding="utf-8"))
                if ref.get("status") != "no_data":
                    ref = dict(ref)
                    ref["is_reference_fallback"] = True
                    ref["reference_reason"] = (
                        f"找不到 {PEAD_EVENTS_CSV}（v7-backtest 回測結果檔案，repo 外部，CI 環境沒有此檔），"
                        f"改用 commit 內 {SUE_BREAKS_REFERENCE_PATH.relative_to(ROOT)} 的參考切點快照。"
                    )
                    return ref
            except Exception:  # noqa: BLE001
                pass  # fall through to the normal no_data path below
        return {"status": "no_data", "reason": f"找不到 {PEAD_EVENTS_CSV}（v7-backtest 回測結果檔案，repo 外部）"}
    try:
        df = pd.read_csv(PEAD_EVENTS_CSV, usecols=["ticker", "filed", "sue"])
    except Exception as e:  # noqa: BLE001
        return {"status": "no_data", "reason": f"讀取 pead_events.csv 失敗：{e}"}
    df["filed"] = pd.to_datetime(df["filed"], errors="coerce")
    sub = df[(df["filed"] >= "2019-01-01") & df["sue"].notna()]
    if len(sub) < 100:
        return {"status": "no_data", "reason": f"2019 年後可用 SUE 樣本數過少（{len(sub)} 筆）"}
    vals = sub["sue"].values
    cuts = [round(float(x), 4) for x in np.percentile(vals, [20, 40, 60, 80])]
    return {
        "schema": "stock-dash-sue-breaks-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z",
        "source": str(PEAD_EVENTS_CSV), "filter": "filed >= 2019-01-01 且 sue 非缺值",
        "n_events": int(len(sub)),
        "percentile_20": cuts[0], "percentile_40": cuts[1], "percentile_60": cuts[2], "percentile_80": cuts[3],
        "min": r2(float(vals.min()), 2), "max": r2(float(vals.max()), 2),
        "method": ("取 ~/v7-backtest 的 PEAD 回測事件檔（pead_events.csv）已經算好的 sue 欄位（SEC GAAP 稀釋 EPS "
                   "口徑），篩 2019 年後申報的事件，算 20/40/60/80 百分位切點，給本頁個股的 SUE 分組對照——"
                   "分組僅供參考，本頁 SUE 用 yfinance 分析師慣例 EPS 重新計算，口徑跟回測不同。"),
    }


def ensure_sue_breaks(force=False):
    if not force and SUE_BREAKS_PATH.exists():
        try:
            existing = json.loads(SUE_BREAKS_PATH.read_text(encoding="utf-8"))
            if existing.get("status") != "no_data":
                return existing
        except Exception:  # noqa: BLE001
            pass
    breaks = build_sue_breaks()
    if breaks.get("status") != "no_data":
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        SUE_BREAKS_PATH.write_text(json.dumps(breaks, ensure_ascii=False, indent=1), encoding="utf-8")
    return breaks


def sue_group(sue_value, breaks):
    if sue_value is None or breaks.get("status") == "no_data":
        return None, None
    cuts = [breaks["percentile_20"], breaks["percentile_40"], breaks["percentile_60"], breaks["percentile_80"]]
    if sue_value <= cuts[0]:
        return 1, "Q1（最低20%）"
    if sue_value <= cuts[1]:
        return 2, "Q2"
    if sue_value <= cuts[2]:
        return 3, "Q3"
    if sue_value <= cuts[3]:
        return 4, "Q4"
    return 5, "Q5（最高20%）"


def build_card_earnings_surprise(ticker, row, ticker_obj, df_full, spy_full, current_price, as_of):
    ed, err = fetch_earnings_dates_df(ticker_obj)
    surprises = fetch_earnings_surprises(ed, err)
    sue = compute_sue(ed, err)
    breaks = ensure_sue_breaks()
    group_n, group_label = sue_group(sue.get("sue") if sue.get("status") == "ok" else None, breaks)

    last_earnings_date = row.get("last_earnings_date") if row else None
    next_earnings_date = row.get("next_earnings_date") if row else None
    days_to_next = row.get("days_to_next_earnings") if row else None

    trading_days_since = None
    price_vs_spy_since_pct = None
    if last_earnings_date:
        try:
            since_ts = pd.Timestamp(last_earnings_date)
            sub = df_full[df_full.index >= since_ts]
            sub_spy = spy_full[spy_full.index >= since_ts]
            if not sub.empty:
                trading_days_since = len(sub) - 1
            if not sub.empty and not sub_spy.empty and float(sub["Close"].iloc[0]) and float(sub_spy["Close"].iloc[0]):
                stock_chg = current_price / float(sub["Close"].iloc[0]) - 1
                spy_chg = float(spy_full["Close"].iloc[-1]) / float(sub_spy["Close"].iloc[0]) - 1
                price_vs_spy_since_pct = r2((stock_chg - spy_chg) * 100, 2)
        except Exception:  # noqa: BLE001
            pass

    return {
        "status": "ok" if row is not None else "partial",
        "reason": None if row is not None else "不在 dd-screener 名單（339 檔），財報日期改用 yfinance 自算",
        "surprises": surprises,
        "sue": sue,
        "sue_breaks": breaks,
        "sue_group": group_n, "sue_group_label": group_label,
        "last_earnings_date": last_earnings_date,
        "trading_days_since_earnings": trading_days_since,
        "backtest_holding_days": 60,
        "price_vs_spy_since_earnings_pct": price_vs_spy_since_pct,
        "next_earnings_date": next_earnings_date,
        "days_to_next_earnings": days_to_next,
    }


# ── ④ROIC 拆解（原「獲利能不能持續」升級，2026-09-21 追加）───────────────────
def build_roic_quadrant_universe_points(dd_stocks):
    pts = []
    for s in dd_stocks:
        x, y = s.get("ic_turnover_x"), s.get("nopat_margin_pct")
        if x is None or y is None:
            continue
        pts.append({"ticker": s.get("ticker"), "x": r2(x, 3), "y": r2(y, 2)})
    return pts


def build_card_roic_decomposition(row):
    if row is None:
        return {"status": "no_data", "reason": "不在 dd-screener 名單（339 檔）"}
    fund = row.get("fund") or {}
    capital = row.get("capital") or {}
    dd = load_dd_screener()
    summary = dd.get("roic_decomp_summary") or {}

    nopat_margin, ic_turnover = row.get("nopat_margin_pct"), row.get("ic_turnover_x")
    dupont_note = ("拆解式（NOPAT 利潤率 × 投入資本週轉率）用的是財年（FY）數字，roic（LTM）是近 12 個月數字，"
                   "兩者口徑不同、數字會有落差，僅供對照。")
    if row.get("tax_rate_source") == "default21":
        dupont_note += "稅率缺 xlsx 資料，用 21% 預設值代替。"

    return {
        "status": "ok",
        "dupont": {
            "ebit_margin_pct": row.get("ebit_margin_pct"),
            "tax_rate_pct": row.get("tax_rate_pct"),
            "tax_rate_source": row.get("tax_rate_source"),
            "nopat_margin_pct": row.get("nopat_margin_pct"),
            "ic_turnover_x": row.get("ic_turnover_x"),
            "roic_decomposed_pct": r2(nopat_margin * ic_turnover, 2)
            if nopat_margin is not None and ic_turnover is not None else None,
            "roic_ltm_screener_pct": row.get("roic"),
            "note": dupont_note,
        },
        "quadrant": {
            "x_ic_turnover": row.get("ic_turnover_x"),
            "y_nopat_margin": row.get("nopat_margin_pct"),
            "quadrant": row.get("roic_quadrant"),
            "quadrant_code": row.get("roic_quadrant_code"),
            "thresholds": {"nopat_margin_pct": 15.0, "ic_turnover_x": 1.0},
            "universe_counts": {
                "利厚轉快": summary.get("quadrant_hh"), "利厚轉慢": summary.get("quadrant_hl"),
                "利薄轉快": summary.get("quadrant_lh"), "利薄轉慢": summary.get("quadrant_ll"),
            },
            "universe_points": build_roic_quadrant_universe_points(dd.get("stocks", [])),
        },
        "durability": {
            "roic_ltm_pct": row.get("roic"),
            "roic_3y_avg_pct": row.get("roic_3y_avg_pct"),
            "roic_5y_avg_pct": row.get("roic_5y_avg_pct"),
            "roic_vs_5y_x": row.get("roic_vs_5y_x"),
            "roic_trend_5y": row.get("roic_trend_5y"),
            "qgm_roic_5y_stability_pct": row.get("qgm_roic_5y_stability_pct"),
            "durable_5y": row.get("durable_5y"),
            "durable_source": row.get("durable_source"),
        },
        "incremental": {
            "capital": capital,
            "incremental_roic_pct": row.get("incremental_roic_pct"),
            "incremental_roic_clamped": row.get("incremental_roic_clamped"),
            "incremental_roic_note": row.get("incremental_roic_note"),
            "reinvest_rate_pct": row.get("reinvest_rate_pct"),
            "implied_growth_pct": row.get("implied_growth_pct"),
            "consensus_compare": {
                "est_eps_cagr_3y_pct": fund.get("est_eps_cagr_3y_pct"),
                "est_rev_cagr_3y_pct": fund.get("est_rev_cagr_3y_pct"),
                "eps_fy1_fy3_cagr_pct": row.get("eps_fy1_fy3_cagr_pct"),
                "gap_vs_eps_cagr_pct": r2(row.get("implied_growth_pct") - fund.get("est_eps_cagr_3y_pct"), 2)
                if row.get("implied_growth_pct") is not None and fund.get("est_eps_cagr_3y_pct") is not None
                else None,
            },
        },
        "funding": {
            "ccc_days": row.get("ccc_days"),
            "ccc_supplier_financed": row.get("ccc_supplier_financed"),
            "lh_ccc_note": row.get("lh_ccc_note"),
            "capex_pct_rev": row.get("capex_pct_rev"),
            "capex_intensity_label": row.get("capex_intensity_label"),
            "capex_fcf_pct": row.get("capex_fcf_pct"),
            "sbc_pct_rev": row.get("sbc_pct_rev"),
            "sbc_dilution_pct_yr": row.get("sbc_dilution_pct_yr"),
            "buyback_fcf_pct": row.get("buyback_fcf_pct"),
            "capalloc_mech_grade": row.get("capalloc_mech_grade"),
            "fcf_ni_ratio": row.get("fcf_ni_ratio"),
            "net_debt_ltm": fund.get("net_debt_ltm"),
        },
        "gross_margin_line": {
            "ltm": fund.get("gm_ltm_pct"), "fy1": fund.get("gm_fy1_pct"),
            "fy2": fund.get("gm_fy2_pct"), "fy3": fund.get("gm_fy3_pct"),
        },
        "decline_signals": row.get("decline_signals") or [],
        "quality_veto_fails": row.get("quality_veto_fails") or [],
        "quality_veto_level": row.get("quality_veto_level"),
        "decline_signal_light": row.get("decline_signal_light"),
    }


# ── ⑤內部人 ──────────────────────────────────────────────────────────────────
def classify_insider_transaction_kind(text):
    t = (text or "").lower()
    if "sale" in t:
        return "sell"
    if "purchase" in t or "buy" in t:
        return "buy"
    return "other"


def check_insider_cluster_buy(ticker_obj, as_of_date, window_days=INSIDER_CLUSTER_WINDOW_DAYS):
    try:
        raw = ticker_obj.insider_transactions
    except Exception as e:  # noqa: BLE001
        return {"status": "no_data", "reason": f"yfinance insider_transactions 例外：{e}"}
    if raw is None or raw.empty:
        return {"status": "no_data", "reason": "yfinance 未回傳 insider_transactions 資料"}
    required_cols = {"Start Date", "Text", "Position", "Insider", "Shares", "Value"}
    missing_cols = required_cols - set(raw.columns)
    if missing_cols:
        return {"status": "no_data", "reason": f"yfinance insider_transactions 缺欄位：{sorted(missing_cols)}"}

    method = ("依 ~/v7-backtest 內部人回測規格：近 90 天內、2 位以上不同官員／董事（排除 10% 大股東）"
              "在公開市場淨買超（買進金額大於賣出金額），只算 Purchase／Sale 兩類，不含股票獎酬、"
              "選擇權履約、贈與。yfinance 沒有提供 SEC 原始交易代碼，買賣類別是用 Text 欄位文字判斷"
              "（含 Sale 判賣出、含 Purchase／Buy 判買進）。回測顯示這類事件後 60 個交易日超額報酬 "
              "+1.9%（t=4.2，n=1254），但驗證期把它做成投資組合，超額報酬是負的，這裡只當事件提醒，"
              "不是進出場依據；賣出方向沒有驗證過，不解讀。")

    raw = raw.copy()
    raw["Start Date"] = pd.to_datetime(raw["Start Date"], errors="coerce")
    cutoff = pd.Timestamp(as_of_date) - pd.Timedelta(days=window_days)
    win = raw[raw["Start Date"] >= cutoff].copy()
    if win.empty:
        # 近 window_days 天內沒有任何揭露交易——這是「真的零筆」的正常狀態，不是抓取失敗，
        # 直接回傳零值的 ok 結果。刻意不落到下面的 Position 布林篩選：win 是 0 列時
        # win["Position"].apply(...) 產生的空 Series 會讓 win[empty_series] 連欄位一起
        # 篩空（pandas 對「空布林遮罩」的已知行為），下面的 win["kind"] 就會 KeyError。
        return {
            "status": "ok", "window_days": window_days, "n_distinct_buyers": 0,
            "buy_total_usd": 0.0, "sell_total_usd": 0.0, "net_usd": 0.0,
            "cluster_buy_condition_met": False, "purchase_details": [], "method": method,
        }
    win["kind"] = win["Text"].apply(classify_insider_transaction_kind)

    def is_officer_or_director(pos):
        return "10%" not in (pos or "")

    win = win[win["Position"].apply(is_officer_or_director)]
    buys = win[win["kind"] == "buy"] if "kind" in win.columns else win.iloc[0:0]
    sells = win[win["kind"] == "sell"] if "kind" in win.columns else win.iloc[0:0]

    buy_by_insider = {}
    for _, r in buys.iterrows():
        name = r.get("Insider")
        val = r.get("Value")
        val = 0.0 if pd.isna(val) else float(val)
        buy_by_insider[name] = buy_by_insider.get(name, 0.0) + val
    buy_total = float(buys["Value"].fillna(0).sum())
    sell_total = float(sells["Value"].fillna(0).sum())
    n_distinct_buyers = sum(1 for amt in buy_by_insider.values() if amt > 0)
    condition_met = n_distinct_buyers >= 2 and (buy_total - sell_total) > 0

    detail_rows = [{
        "date": r["Start Date"].strftime("%Y-%m-%d") if pd.notna(r["Start Date"]) else None,
        "insider": r.get("Insider"), "position": r.get("Position"),
        "shares": int(r["Shares"]) if pd.notna(r["Shares"]) else None,
        "value_usd": int(r["Value"]) if pd.notna(r["Value"]) else None,
    } for _, r in buys.sort_values("Start Date", ascending=False).iterrows()]

    return {
        "status": "ok",
        "window_days": window_days,
        "n_distinct_buyers": n_distinct_buyers,
        "buy_total_usd": r2(buy_total, 0),
        "sell_total_usd": r2(sell_total, 0),
        "net_usd": r2(buy_total - sell_total, 0),
        "cluster_buy_condition_met": condition_met,
        "purchase_details": detail_rows,
        "method": ("依 ~/v7-backtest 內部人回測規格：近 90 天內、2 位以上不同官員／董事（排除 10% 大股東）"
                   "在公開市場淨買超（買進金額大於賣出金額），只算 Purchase／Sale 兩類，不含股票獎酬、"
                   "選擇權履約、贈與。yfinance 沒有提供 SEC 原始交易代碼，買賣類別是用 Text 欄位文字判斷"
                   "（含 Sale 判賣出、含 Purchase／Buy 判買進）。回測顯示這類事件後 60 個交易日超額報酬 "
                   "+1.9%（t=4.2，n=1254），但驗證期把它做成投資組合，超額報酬是負的，這裡只當事件提醒，"
                   "不是進出場依據；賣出方向沒有驗證過，不解讀。"),
    }


def build_card_insider(ticker, row, ticker_obj, as_of):
    cluster = check_insider_cluster_buy(ticker_obj, as_of)
    fund = (row.get("fund") if row else None) or {}
    return {
        "status": "ok",
        "cluster_buy": cluster,
        "dd_screener_net_buy_3m_usd": fund.get("insider_net_buy_3m"),
        "dd_screener_insider_signal": row.get("insider_signal") if row else None,
        "dd_screener_note": (
            "dd-screener 的近 3 個月淨買超金額跟 insider_signal，是把買進、賣出互抵後的淨額和方向，"
            "賣出本身不當作訊號。上面的「群聚買進」判斷是另外用 yfinance 逐筆資料、照回測規格獨立算的，"
            "兩者算法不同，結論可能不一致。"
        ) if row is not None else "不在 dd-screener 名單（339 檔），只顯示 yfinance 的群聚買進判斷。",
    }


# ── ⑥dd-screener 研究欄位（Correction 2 改名、改內容）────────────────────────
def build_card_dd_screener_fields(row, as_of, current_price):
    if row is None:
        return {"status": "no_data", "reason": "不在 dd-screener 名單（339 檔）"}
    fund = row.get("fund") or {}
    dd_date = row.get("dd_date")
    days_ago = None
    if dd_date:
        try:
            days_ago = (as_of - datetime.strptime(dd_date, "%Y-%m-%d").date()).days
        except ValueError:
            pass
    price_at_dd = row.get("price_at_dd")
    price_chg_since_dd_pct = r2((current_price / price_at_dd - 1) * 100, 2) if price_at_dd else None

    return {
        "status": "ok",
        "dca_verdict": row.get("dca_verdict"), "dca_role": row.get("dca_role"),
        "dd_date": dd_date, "dd_days_ago": days_ago,
        "price_at_dd": price_at_dd, "price_chg_since_dd_pct": price_chg_since_dd_pct,
        "upside_mid_pct": row.get("upside_mid_pct"), "upside_5y_pct": row.get("upside_5y_pct"),
        "bull_5y_price": row.get("bull_5y_price"), "bear_5y_price": row.get("bear_5y_price"),
        "p_bull_pct": row.get("p_bull_pct"), "p_bear_pct": row.get("p_bear_pct"),
        "ev5y_pct": row.get("ev5y_pct"), "live_ev5y_pct": row.get("live_ev5y_pct"),
        "target_upside_pct": row.get("target_upside_pct"),
        "target_low": fund.get("target_low"), "target_avg": fund.get("target_avg"),
        "target_high": fund.get("target_high"),
        "moat_grade": row.get("moat_grade"), "moat_score": row.get("moat_score"),
        "moat_trend": row.get("moat_trend"),
        "signal": row.get("signal"), "trap": row.get("trap"), "val": row.get("val"),
        "ai_risk": row.get("ai_risk"),
        "dd_path": row.get("dd_path"),
        "price_ruler": [
            {"label": "5年空頭價", "value": row.get("bear_5y_price")},
            {"label": "DD時股價", "value": price_at_dd},
            {"label": "目前股價", "value": r2(current_price, 2)},
            {"label": "目標價低", "value": fund.get("target_low")},
            {"label": "目標價均", "value": fund.get("target_avg")},
            {"label": "目標價高", "value": fund.get("target_high")},
            {"label": "5年多頭價", "value": row.get("bull_5y_price")},
        ],
    }


# ── ⑦dd-screener 分數（FunnelRank，presentation-only；不重算）───────────────
def build_card_funnel_rank(row, dd_stocks):
    if row is None:
        return {"status": "no_data", "reason": "不在 dd-screener 名單（339 檔）"}

    all_ranks = sorted(
        [(s.get("ticker"), s.get("funnel_rank")) for s in dd_stocks if s.get("funnel_rank") is not None],
        key=lambda x: x[1], reverse=True,
    )
    total = len(all_ranks)
    rank_pos = next((i + 1 for i, (tk, _) in enumerate(all_ranks) if tk == row.get("ticker")), None)
    percentile = r2((1 - (rank_pos - 1) / total) * 100, 1) if rank_pos and total else None

    quality_gate, moat_adj, revision = row.get("quality_gate"), row.get("moat_score_adj"), row.get("revision_score")
    w = FUNNEL_WEIGHTS
    contributions = {
        "quality": r2(quality_gate * w["quality"], 4) if quality_gate is not None else None,
        "moat": r2(moat_adj * w["moat"], 4) if moat_adj is not None else None,
        "revision": r2(revision * w["revision"], 4) if revision is not None else None,
    }
    weighted_sum = (r2(sum(contributions.values()), 4)
                    if all(v is not None for v in contributions.values()) else None)

    fail_criteria = set(row.get("fail_criteria") or [])
    criteria_display = []
    for c in FUNNEL_QUALITY_CRITERIA_DISPLAY:
        val = row.get(c["key"])
        criteria_display.append({
            **c, "value": val,
            "pass": (c["key"] not in fail_criteria) if val is not None else None,
        })
    de_ref = {**FUNNEL_DE_REFERENCE_DISPLAY, "value": row.get("de")}
    forgivable = fail_criteria == {"peg"}

    def _dir(v):
        if v is None:
            return "無資料"
        if v >= FUNNEL_REVISION_THRESHOLD:
            return "上修"
        if v <= -FUNNEL_REVISION_THRESHOLD:
            return "下修"
        return "持平"

    rev_fy1, rev_fy2, rev_fy3 = (row.get("eps_fy_curr_revision_pct"), row.get("eps_fy_next_revision_pct"),
                                 row.get("eps_fy3_revision_pct"))
    revision_fy = [
        {"fy": "FY1（今年度）", "revision_pct": rev_fy1, "weight": FUNNEL_REVISION_FY_WEIGHTS_DISPLAY["fy1"],
         "direction": _dir(rev_fy1)},
        {"fy": "FY2（明年度）", "revision_pct": rev_fy2, "weight": FUNNEL_REVISION_FY_WEIGHTS_DISPLAY["fy2"],
         "direction": _dir(rev_fy2)},
        {"fy": "FY3（後年度）", "revision_pct": rev_fy3, "weight": FUNNEL_REVISION_FY_WEIGHTS_DISPLAY["fy3"],
         "direction": _dir(rev_fy3)},
    ]
    steepening = (rev_fy1 is not None and rev_fy3 is not None
                  and _dir(rev_fy1) == "上修" and _dir(rev_fy3) == "上修" and rev_fy3 > rev_fy1)

    vetoes = []
    if row.get("veto_all_downgrade"):
        vetoes.append("三個財年獲利預估全數下修，FunnelRank 強制歸零（veto_all_downgrade）")
    if row.get("veto_decline_signal"):
        vetoes.append("衰退訊號命中（機械指標命中5項以上），FunnelRank 強制歸零（veto_decline_signal）")
    if row.get("funnel_cap_moat_down"):
        vetoes.append("護城河趨勢向下且未四項全過，分數封頂 0.50（funnel_cap_moat_down）")
    if row.get("funnel_cap_quality"):
        vetoes.append(f"體質五項出現「{row.get('funnel_cap_quality_level')}」等級，分數封頂（funnel_cap_quality）")
    if row.get("quality_cap_overridden_by_revision"):
        vetoes.append("體質封頂本應生效，但三個財年皆上修，封頂被解除（quality_cap_overridden_by_revision）")

    return {
        "status": "ok",
        "funnel_rank": row.get("funnel_rank"),
        "funnel_rank_x100": r2(row.get("funnel_rank") * 100, 1) if row.get("funnel_rank") is not None else None,
        "rank": rank_pos, "total": total, "percentile": percentile,
        "components": {"quality_gate": quality_gate, "moat_score_adj": moat_adj, "revision_score": revision},
        "weights": w, "contributions": contributions, "weighted_sum_before_caps": weighted_sum,
        "quality_criteria": criteria_display, "de_reference": de_ref,
        "quality_pass_count": row.get("pass_count"),
        "quality_forgivable_peg_only_fail": forgivable,
        "quality_gate_partial": row.get("quality_gate_partial"),
        "revision_fy": revision_fy, "revision_steepening_bonus_applied": steepening,
        "vetoes_and_caps": vetoes,
        "moat_trend_mult": FUNNEL_MOAT_TREND_MULT_DISPLAY.get(row.get("moat_trend")),
        "moat_score_raw": row.get("moat_score"),
        "footnote": (
            "FunnelRank ＝ 0.40×品質關卡 + 0.30×護城河（依趨勢調整）+ 0.30×獲利修正動能，"
            "另外四道否決／封頂規則不進加權公式、直接處置。這是 investmquest.com/dd-screener/ "
            "現在使用中的排序分（2026-07-03、2026-09-17 拍板），品質和護城河反映的是已經發生的體質，"
            "獲利修正動能抓的是分析師剛改變的看法，抓得比較即時。公式與門檻詳見 /dd-screener/。"
        ),
    }


# ═══════════════════════════════════════════ 護城河（DD 基準 + 機械追蹤）═══════
# 2026-09-22：使用者要求把 DD 報告的護城河判斷與 ROIC durability 整合進來，當作
# 「基準」；之後沒有新 DD 時，靠 dd-screener 的機械代理指標自己追蹤有沒有偏離這個
# 基準——頁面本身永遠不會自己改護城河等級／趨勢，那兩個字仍然只來自 DD。
# 其餘卡片（獲利預估／估值／財報驚喜／FunnelRank／內部人／dd-screener 欄位）繼續
# 完全不讀 DD，只用 dd-screener——這裡是唯一讀 DD HTML 的地方。
MOAT_EMOJI_MAP = {"🟢": "穩固", "🟡": "需追蹤", "🔴": "轉弱", "⛔": "架構替代"}
MOAT_EMOJI_COMBOS = {
    "🟢🟡": "穩固／需追蹤", "🟡🟢": "需追蹤／穩固",
    "🟢🔴": "穩固／轉弱", "🔴🟢": "轉弱／穩固",
    "🟡🔴": "需追蹤／轉弱", "🔴🟡": "轉弱／需追蹤",
}


def emoji_to_text(s):
    """DD 表格裡的 🟢🟡🔴⛔ 轉中性文字：穩固／需追蹤／轉弱／架構替代；組合符號
    （如「🟢🟡」）先轉，單一符號再轉，原文括號說明照原樣保留在後面。"""
    if not s:
        return s
    out = s
    for combo, txt in MOAT_EMOJI_COMBOS.items():
        out = out.replace(combo, txt)
    for e, t in MOAT_EMOJI_MAP.items():
        out = out.replace(e, t)
    # DD 原文有時已經在符號後面手動寫了同一個詞（如「⛔ 架構替代（尚未發生…)」），
    # 轉換後會變成「架構替代 架構替代（…)」重複——把緊鄰的重複詞收成一個。
    for txt in list(MOAT_EMOJI_MAP.values()) + list(MOAT_EMOJI_COMBOS.values()):
        out = out.replace(f"{txt} {txt}", txt)
    return out


def find_dd_files(ticker):
    """docs/dd/DD_{ticker}_*.html，依檔名（內含日期）排序。docs/dd/brief/ 底下的快速版
    檔名前綴是 BRIEF_、目錄也不同，這個 glob 天生就掃不到，不用另外排除。"""
    return sorted(DD_DIR.glob(f"DD_{ticker}_*.html"))


def extract_dd_meta(path):
    try:
        html = path.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return None, None
    m = re.search(r'<script id="dd-meta"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None, html
    try:
        return json.loads(m.group(1)), html
    except Exception:  # noqa: BLE001
        return None, html


def build_moat_history(ticker):
    """掃這檔全部 DD 版本，把有 dd-meta 的每一份的護城河欄位收集起來，依日期排序。
    舊版（無 dd-meta，或 schema 早於 v14 沒有 moat_trend／endo_growth_ceiling）就只填
    有的欄位，其餘留 None——不用新版的值回填舊版，避免假造歷史。"""
    history = []
    for f in find_dd_files(ticker):
        meta, _ = extract_dd_meta(f)
        if not meta:
            continue
        history.append({
            "date": meta.get("date"),
            "moat": meta.get("moat"),
            "moat_score": meta.get("moat_score"),
            "moat_execution": meta.get("moat_execution"),
            "moat_pricing_power": meta.get("moat_pricing_power"),
            "moat_trend": meta.get("moat_trend"),
            "growth_durability": meta.get("growth_durability"),
            "endo_growth_ceiling": meta.get("endo_growth_ceiling"),
            "schema": meta.get("schema"),
            "dd_path": f"/dd/{f.name}",
        })
    history.sort(key=lambda h: h["date"] or "")
    return history


def _sections_by_id(html):
    return dict(re.findall(r'<section id="([^"]+)">(.*?)</section>', html, re.S))


def _strip_tags(s):
    return re.sub(r'<[^>]+>', '', s or '').strip()


def _heading_text(inner_html):
    m = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', inner_html or '', re.S)
    return _strip_tags(m.group(1)) if m else ""


def _find_section_by_keyword(sections, keywords):
    for sid, inner in sections.items():
        htext = _heading_text(inner)
        if any(kw in htext for kw in keywords):
            return sid, inner
    return None, None


def _find_subblock(inner_html, keywords, tag="h3"):
    """在一個 section 內找子標題（預設 h3）含任一 keyword 的位置，回傳從該標題結束到
    下一個同層標題開始（或段落結尾）之間的 HTML 片段；找不到回 None。"""
    if not inner_html:
        return None
    pattern = re.compile(rf'<{tag}[^>]*>(.*?)</{tag}>', re.S)
    matches = list(pattern.finditer(inner_html))
    for i, m in enumerate(matches):
        if any(kw in _strip_tags(m.group(1)) for kw in keywords):
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(inner_html)
            return inner_html[start:end]
    return None


def _parse_table(table_html):
    if not table_html:
        return None
    trs = re.findall(r'<tr>(.*?)</tr>', table_html, re.S)
    if not trs:
        return None
    headers = [_strip_tags(h) for h in re.findall(r'<th[^>]*>(.*?)</th>', trs[0], re.S)]
    rows, start_idx = [], (1 if headers else 0)
    for tr in trs[start_idx:]:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if cells:
            rows.append([_strip_tags(c) for c in cells])
    return {"headers": headers, "rows": rows} if rows else None


def _first_table(html_chunk):
    if not html_chunk:
        return None
    m = re.search(r'<table[^>]*>(.*?)</table>', html_chunk, re.S)
    return _parse_table(m.group(0)) if m else None


def _first_paragraph(html_chunk, keywords=None):
    if not html_chunk:
        return None
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', html_chunk, re.S):
        txt = _strip_tags(m.group(1))
        if not txt:
            continue
        if keywords and not any(kw in txt for kw in keywords):
            continue
        return txt
    return None


def parse_dd_moat_section(html, dd_path):
    """從一份 DD 的護城河章節（依標題關鍵字「護城河」定位，不假設固定 §編號——實測
    NVDA/TSM/AMD 三份最新 DD 的章節編號與標題用字都不同）解析六塊內容。抓不到的欄位
    一律回 None，前端顯示「無資料」＋連回 DD 對應段落，不猜測、不用其他資料頂替。"""
    sections = _sections_by_id(html)
    moat_sid, moat_inner = _find_section_by_keyword(sections, ["護城河"])
    out = {
        "found": moat_sid is not None,
        "section_anchor": f"{dd_path}#{moat_sid}" if moat_sid else None,
        "two_dim_para": None, "moat_to_numbers": None, "pricing_defense_para": None,
        "rival_table": None, "rival_interpretation": None,
        "threat_tiers": None, "roic_durability": None,
    }
    if not moat_sid:
        return out

    out["two_dim_para"] = _first_paragraph(moat_inner, ["二維拆解", "Execution", "moat_trend", "護城河"])

    m2n_block = _find_subblock(moat_inner, ["Moat-to-Numbers", "護城河數字驗收", "機制如何轉化為財務"])
    out["moat_to_numbers"] = _first_table(m2n_block)
    if m2n_block:
        after_table = m2n_block.split("</table>", 1)[-1] if "</table>" in m2n_block else m2n_block
        out["pricing_defense_para"] = _first_paragraph(after_table, ["定價權"])

    rival_block = _find_subblock(moat_inner, ["對手損益對照", "損益對照"])
    out["rival_table"] = _first_table(rival_block)
    out["rival_interpretation"] = _first_paragraph(rival_block, ["市佔", "份額"]) if rival_block else None

    threat_block = _find_subblock(moat_inner, ["威脅三級分類", "威脅分類", "瓦解護城河"])
    threat_table = _first_table(threat_block)
    if threat_table:
        for row in threat_table["rows"]:
            if len(row) > 1:
                row[1] = emoji_to_text(row[1])
    out["threat_tiers"] = threat_table

    # §5.R 報酬持續期檢核有時不在護城河章節本身（如 AMD 放在財務品質監測章），跨全部
    # section 找，記下實際落在哪個 section 供連結。
    roic_sid, roic_block = None, None
    for sid, inner in sections.items():
        block = _find_subblock(inner, ["報酬持續期檢核", "ROIC durability", "報酬持續期"])
        if block:
            roic_sid, roic_block = sid, block
            break
    if roic_block:
        positioning_para = _first_paragraph(roic_block, ["當期 ROIC", "ROIC 定位", "ROIC"])
        checkpoints = _first_table(roic_block)
        if checkpoints:
            for row in checkpoints["rows"]:
                if len(row) > 1:
                    row[1] = emoji_to_text(row[1])
        incremental_para = _first_paragraph(roic_block, ["增量 ROIC", "增量NOPAT", "再投資率", "增量 NOPAT"])
        overall_para = _first_paragraph(roic_block, ["綜合定位"])
        inc = {"incremental_roic_pct": None, "reinvest_rate_pct": None, "endo_growth_ceiling_pct": None,
               "consensus_cagr_pct": None, "consensus_cagr_period": None}
        if incremental_para:
            m = re.search(r'增量\s*ROIC\s*([\d.]+)\s*%', incremental_para)
            if m:
                inc["incremental_roic_pct"] = float(m.group(1))
            # 「再投資率」與「內生成長天花板」後面常接英文縮寫/財年號（如 NOPAT、FY26），
            # 用非貪婪 .{0,N}? 而非 [^0-9%] 排除字元類，避免中途遇到數字就斷掉。
            m = re.search(r'再投資率.{0,20}?＝?\s*([\d.]+)\s*%', incremental_para)
            if m:
                inc["reinvest_rate_pct"] = float(m.group(1))
            # 「內生成長天花板＝A%×B%＝C%」要抓最後一個 C%（結果），不是中間的 A%。
            m = re.search(r'內生成長天花板\s*＝?\s*[\d.]+\s*%\s*[×xX*]\s*[\d.]+\s*%\s*＝\s*([\d.]+)\s*%', incremental_para)
            if not m:
                m = re.search(r'內生成長天花板.{0,25}?([\d.]+)\s*%', incremental_para)
            if m:
                inc["endo_growth_ceiling_pct"] = float(m.group(1))
            # 共識 CAGR：先完整抓括號內容（含期間與數字），再從括號內容尾端拆出百分比數字，
            # 避免「（期間 32.7%）」貪婪比對時把數字尾巴誤切給期間欄位。
            m = re.search(r'共識\s*EPS\s*CAGR[（(]([^）)]*)[）)]', incremental_para)
            if m:
                paren = m.group(1)
                m2 = re.search(r'([\d.]+)\s*%\s*$', paren)
                if m2:
                    inc["consensus_cagr_pct"] = float(m2.group(1))
                    inc["consensus_cagr_period"] = paren[:m2.start()].strip()
        out["roic_durability"] = {
            "section_anchor": f"{dd_path}#{roic_sid}" if roic_sid else None,
            "positioning_para": positioning_para,
            "checkpoints": checkpoints,
            "incremental": inc,
            "overall_para": overall_para,
        }
    return out


MOAT_DIR = ROOT / "docs" / "stock-dash" / "data" / "moat"  # 持久化判斷檔：v1 由 DD 建立，
# 之後本腳本永遠不覆寫，只有「護城河複審」skill（另一支程式）會改它。
MOAT_REVIEW_DAYS = 180  # 判斷超過這麼多天，複審觸發之一（見 compute_review_due_v2）


def _table_rows_to_dicts(table, keys):
    """table={"headers":[...],"rows":[[...]]}；把每列依 keys 對應成 dict（欄數不夠的補
    None，不強行對齊到錯的欄）。"""
    if not table:
        return []
    out = []
    for row in table["rows"]:
        out.append({k: (row[i] if i < len(row) else None) for i, k in enumerate(keys)})
    return out


def _rival_tickers_from_table(rival_table, ticker):
    """§5.F 表第一欄除了自己以外的公司代號。欄位常見兩種寫法：純代號「AMD」，或
    「AVGO（Broadcom）」代號＋全名——取開頭連續大寫英文字母當代號，抓不到就跳過。"""
    if not rival_table:
        return []
    out = []
    for row in rival_table["rows"]:
        if not row:
            continue
        cand_raw = row[0].strip()
        m = re.match(r'^([A-Z]{1,6})\b', cand_raw)
        cand = m.group(1) if m else None
        if cand and cand != ticker:
            out.append(cand)
    return out


def fmt_arrow_zh(pct):
    if pct is None:
        return "—"
    if pct <= -0.5:
        return "下修"
    if pct >= 0.5:
        return "上修"
    return "持平"


MOAT_HURDLE_RATE_PCT = 10.0  # 資金成本假設門檻，opus 判斷腳印①ROIC 時的預設值（見 SKILL v1.0）


def _parse_threshold_number_and_direction(threshold_text):
    """從門檻敘述（如「連2季低於70%」）盡量抓一個數字＋方向；抓不到回
    (None, None)——不是每句都能安全解析，抓不到就不自動判斷是否觸及。"""
    if not threshold_text:
        return None, None
    m = re.search(r'([\d.]+)\s*%', threshold_text)
    if not m:
        return None, None
    num = float(m.group(1))
    if any(k in threshold_text for k in ("跌破", "低於", "降至", "低過")):
        return num, "below_bad"
    if any(k in threshold_text for k in ("突破", "超過", "高於")):
        return num, "above_bad"
    return num, None


# metric_key（opus 判斷時自訂，盡量從這組既有名稱挑，見 moat_pipeline.py 判斷
# prompt）→ dd-screener 欄位怎麼抓現在值。對不上的 metric_key（含 opus 自己標
# 的 "manual"）一律 current_value=None、hit=False、needs_manual=True——機械層
# 不亂猜對應關係，也不猜鬆不鬆動（那是判斷的事）。
METRIC_KEY_RESOLVERS = {
    "roic_ltm_pct": lambda row, fund: row.get("roic") if row else None,
    "roic_3y_avg_pct": lambda row, fund: row.get("roic_3y_avg_pct") if row else None,
    "roic_5y_avg_pct": lambda row, fund: row.get("roic_5y_avg_pct") if row else None,
    "gm_ltm_pct": lambda row, fund: fund.get("gm_ltm_pct"),
    "gm_fy1_pct": lambda row, fund: fund.get("gm_fy1_pct"),   # 今年度毛利率共識（年度）；v2.1 加入，key 清單見 check_moat_review.KNOWN_METRIC_KEYS
    "gm_fy2_pct": lambda row, fund: fund.get("gm_fy2_pct"),   # 明年度毛利率共識（年度）
    "incremental_roic_pct": lambda row, fund: row.get("incremental_roic_pct") if row else None,
    "rev_yoy_fq0_pct": lambda row, fund: fund.get("rev_yoy_fq0_pct"),
    "rev_yoy_fq1_pct": lambda row, fund: fund.get("rev_yoy_fq1_pct"),
    "eps_fy_next_revision_pct": lambda row, fund: row.get("eps_fy_next_revision_pct") if row else None,
    "eps_rev_3m_pct": lambda row, fund: row.get("eps_rev_3m_pct") if row else None,
    "pe_ntm_x": lambda row, fund: fund.get("pe_ntm_x"),
}


def _is_moat_v3(moat_doc):
    """moat-v3（SKILL v2.0 三題制）vs moat-v2（舊判斷制）。遷移期兩種都讀。"""
    return (moat_doc or {}).get("schema") == "moat-v3"


def _moat_watch_items(moat_doc):
    """所有「什麼事會改變答案」條件的清單（就地可改的 dict 參照）。
    v3：current.questions[].watch[]；v2：current.q3_review.conditions[]。"""
    cur = (moat_doc or {}).get("current") or {}
    if _is_moat_v3(moat_doc):
        return [w for q in (cur.get("questions") or []) for w in (q.get("watch") or [])]
    return cur.get("q3_review", {}).get("conditions") or []


def _moat_date(cur):
    """出題／判斷日期：v3 叫 date，v2 叫 judgment_date。"""
    return cur.get("date") or cur.get("judgment_date")


def update_moat_conditions(moat_doc, row):
    """v1.0：每天只更新 q3_review.conditions[].current_value／hit，不再做任何
    護城河訊號門檻判定（鬆不鬆動是 opus 判斷的事，機械層只更新「現在的值」，
    不下結論——見 SKILL『數字是證據，不是判決』）。metric_key 對不上已知欄位
    就 current_value=None、hit=False，標 needs_manual=True。就地修改
    moat_doc，不回傳新物件。"""
    if not moat_doc:
        return
    conditions = _moat_watch_items(moat_doc)
    v3 = _is_moat_v3(moat_doc)
    manual_key = "manual" if v3 else "needs_manual"
    fund = (row.get("fund") if row else None) or {}
    for c in conditions:
        key = c.get("metric_key")
        resolver = METRIC_KEY_RESOLVERS.get(key)
        if not resolver:
            c["current_value"], c["hit"], c[manual_key] = None, False, True
            continue
        current_value = resolver(row, fund)
        c[manual_key] = False
        if current_value is None:
            c["current_value"], c["hit"] = None, False
            continue
        c["current_value"] = r2(current_value, 2)
        num, direction = _parse_threshold_number_and_direction(c.get("threshold"))
        if num is None or not direction:
            c["hit"] = False  # 門檻文字解析不出方向，不猜，維持未觸及
        else:
            c["hit"] = (direction == "below_bad" and current_value <= num) or \
                       (direction == "above_bad" and current_value >= num)


def compute_review_due_v2(moat_doc):
    """v1.0：review_due 只看兩件事——任一重看條件現在值觸及，或距判斷日期
    >180 天。程式只管「該不該看」，不管「看了會不會改」。"""
    if not moat_doc:
        return {"due": False, "reasons": []}
    current = moat_doc.get("current") or {}
    reasons = []
    for c in _moat_watch_items(moat_doc):
        if c.get("hit"):
            label = c.get("desc_zh") or c.get("condition")
            reasons.append(f"重看條件觸及：「{label}」（現值 {c.get('current_value')}，門檻 {c.get('threshold')}）")
    try:
        judged = datetime.strptime(_moat_date(current), "%Y-%m-%d").date()
        days_since = (datetime.now(timezone.utc).date() - judged).days
        if days_since > MOAT_REVIEW_DAYS:
            reasons.append(f"判斷已 {days_since} 天未更新（門檻 {MOAT_REVIEW_DAYS} 天）")
    except Exception:  # noqa: BLE001
        pass
    return {"due": bool(reasons), "reasons": reasons}


def build_moat_changes_table(ticker, row, moat_doc):
    """收合區用的「上次判斷以來的變化表」：只有上次值→現在值→箭頭，**沒有判定
    欄**（鬆不鬆動的判斷是 opus 的事，機械層不下結論）。上次值來自判斷當時存的
    mechanical_snapshot_at_judgment（純機械快照，跟 opus 的 q1_shape.footprints
    判斷脫鉤，見 moat_pipeline.py::assemble_current 的同名欄位）。"""
    if not moat_doc:
        return []
    snap = (moat_doc.get("current") or {}).get("mechanical_snapshot_at_judgment") or {}
    fund = (row.get("fund") if row else None) or {}
    rows = []

    def add(proxy, at_judgment, now):
        if at_judgment is None and now is None:
            return
        direction = "—"
        if at_judgment is not None and now is not None:
            delta = now - at_judgment
            direction = "上升" if delta > 0.05 else ("下滑" if delta < -0.05 else "持平")
        rows.append({"proxy": proxy, "at_judgment": r2(at_judgment, 2) if at_judgment is not None else "無資料",
                    "now": r2(now, 2) if now is not None else "無資料", "direction": direction})

    add("毛利率(LTM)", snap.get("gm_ltm_pct"), fund.get("gm_ltm_pct"))
    add("ROIC(LTM)", snap.get("roic_ltm_pct"), row.get("roic") if row else None)
    add("增量ROIC", snap.get("incremental_roic_pct"), row.get("incremental_roic_pct") if row else None)
    add("近4季營收年增(最新季)", snap.get("rev_yoy_fq0_pct"), fund.get("rev_yoy_fq0_pct"))
    add("明年度EPS預估", snap.get("eps_fy_next"), row.get("eps_fy_next") if row else None)
    return rows


def build_moat_rival_comparison(moat_doc, dd_stocks):
    """收合區用的「對手對照（現在值）」：current.rivals 只存 ticker 代號（頁面
    正文不列名字，這裡是收合證據區，可以列），現在值即時從 dd_stocks 查，
    不做 DD 時比較（判斷檔本身沒有存對手的歷史快照）。"""
    if not moat_doc:
        return []
    rivals = (moat_doc.get("current") or {}).get("rivals") or []
    stocks_by_ticker = {s.get("ticker"): s for s in (dd_stocks or [])}
    out = []
    for rt in rivals:
        rr = stocks_by_ticker.get(rt)
        if not rr:
            out.append({"ticker": rt, "gm_ltm_pct": None, "roic": None, "rev_yoy_fq0_pct": None, "pe_ntm_x": None})
            continue
        rf = rr.get("fund") or {}
        out.append({"ticker": rt, "gm_ltm_pct": r2(rf.get("gm_ltm_pct"), 1), "roic": r2(rr.get("roic"), 1),
                    "rev_yoy_fq0_pct": r2(rf.get("rev_yoy_fq0_pct"), 1), "pe_ntm_x": r2(rf.get("pe_ntm_x"), 1)})
    return out


def build_moat_footprint(ticker, row, dd_stocks):
    """2026-09-22 持有人拍板：護城河章不放模型生成的判斷，只放機械數字＋連到研究報告。
    本函式不讀 moat/{T}.json（判斷檔），只用 dd-screener 欄位與研究報告的對手表：
      - 本公司毛利率（近四季）、最新一季總營收年增
      - 對手：研究報告護城河章的對手損益表；沒有就 dd-screener 同 sector 前 3
      - 對手現在值（毛利率／ROIC／營收年增／NTM 本益比）與對手毛利率中位數
      - 研究報告護城河章節的連結（有研究才有）
    ROIC 耐久度與增量 ROIC 已在 roic_decomposition 卡裡，這裡不重複。"""
    fund = (row.get("fund") if row else None) or {}
    out = {"status": "ok" if row else "no_row", "gm_ltm_pct": r2(fund.get("gm_ltm_pct"), 2),
           "rev_yoy_fq0_pct": r2(fund.get("rev_yoy_fq0_pct"), 2),
           "rivals": [], "rival_source": None, "peer_median_gm_pct": None, "research": None}
    rival_tickers = []
    dd_path = (row or {}).get("dd_path")
    if dd_path:
        f = ROOT / "docs" / dd_path.lstrip("/")
        if f.exists():
            try:
                parsed = parse_dd_moat_section(f.read_text(encoding="utf-8"), dd_path)
                out["research"] = {"path": dd_path, "moat_anchor": parsed.get("section_anchor"),
                                   "date": (row or {}).get("dd_date")}
                rival_tickers = _rival_tickers_from_table(parsed.get("rival_table"), ticker)
                if rival_tickers:
                    out["rival_source"] = "研究報告的對手損益表"
            except Exception:  # noqa: BLE001
                pass
    if not rival_tickers and row and row.get("sector"):
        rival_tickers = [x["ticker"] for x in (dd_stocks or [])
                         if x.get("sector") == row.get("sector") and x.get("ticker") != ticker][:3]
        if rival_tickers:
            out["rival_source"] = "同產業分類前三檔"
    by_t = {x.get("ticker"): x for x in (dd_stocks or [])}
    gms = []
    for rt in rival_tickers[:5]:
        rr = by_t.get(rt)
        rf = (rr.get("fund") if rr else None) or {}
        gm = r2(rf.get("gm_ltm_pct"), 1)
        if gm is not None:
            gms.append(gm)
        out["rivals"].append({"ticker": rt, "gm_ltm_pct": gm, "roic": r2(rr.get("roic"), 1) if rr else None,
                              "rev_yoy_fq0_pct": r2(rf.get("rev_yoy_fq0_pct"), 1), "pe_ntm_x": r2(rf.get("pe_ntm_x"), 1)})
    if gms:
        gms.sort()
        n = len(gms)
        out["peer_median_gm_pct"] = r2(gms[n // 2] if n % 2 else (gms[n // 2 - 1] + gms[n // 2]) / 2, 2)
    return out


def build_card_moat(ticker, row, dd_stocks):
    """v1.0：只讀 docs/stock-dash/data/moat/{T}.json（本腳本絕不建立／覆寫判斷
    本身——寫判斷檔是 scripts/moat_pipeline.py 的事），每天更新重看條件現在值／
    review_due 並持久化回檔案（這是 SKILL 明文授權機械層做的兩件事，不算改
    判斷），附一張純機械的「變化表」與「對手對照」供收合區顯示。沒有判斷檔＝
    「缺」，不臨時生一份假判斷（見 SKILL『沒有現成研究的股票一樣做初判』——
    初判是 moat_pipeline.py 的事，不是這裡）。回傳 (moat, changes_table,
    rivals_now)。"""
    path = MOAT_DIR / f"{ticker}.json"
    if not path.exists():
        return {"has_judgment": False, "reason": "站上尚無這檔的護城河判斷（缺）", "judgment": None}, [], []
    try:
        moat_doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"has_judgment": False, "reason": f"moat/{ticker}.json 讀取失敗：{e}", "judgment": None}, [], []

    update_moat_conditions(moat_doc, row)
    moat_doc["review_due"] = compute_review_due_v2(moat_doc)
    try:
        path.write_text(json.dumps(moat_doc, ensure_ascii=False, indent=1), encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass  # 寫不回去不影響本次 build 輸出，只是下次少了持久化的現在值
    changes_table = build_moat_changes_table(ticker, row, moat_doc)
    rivals_now = build_moat_rival_comparison(moat_doc, dd_stocks)
    return {"has_judgment": True, "judgment": moat_doc}, changes_table, rivals_now


# ═══════════════════════════════════════ 兩層改版（行情層每天／判斷層有觸發才動）═══
# 2026-09-22：使用者要求「產生這份報告時，只改動有新的部分或會改變判斷的部分」。
# 行情層（quote／K線／量價分布／選擇權／空單／大盤／股價×獲利卡片裡跟當日股價有關
# 的部分）每次 build 都照算照更新；判斷層（投資摘要句、趨勢狀態、獲利預估表、財報
# 驚喜/SUE、護城河章、ROIC耐久度、FunnelRank、內部人叢集買、dd-screener研究欄位）
# 只有下面 T1-T8 任一條件觸發才換版，沒觸發就整段沿用上一版存的內容——數字不能因為
# 每天重跑就悄悄被新值蓋掉。
STATE_DIR_DEFAULT = OUT_DIR / "state"  # docs/stock-dash/data/state/{T}.json，可用 --state-dir 覆寫（測試用）

JUDGMENT_SECTIONS = ["trend_state", "eps_revision", "earnings_surprise", "moat", "roic_decomposition",
                     "funnel_rank", "insider", "dd_screener_fields"]

# T1-T8 觸發門檻（中文註解＝門檻的意義）。T6（護城河監測指標觸及）併入 T3。
VERSION_TRIGGER_CONFIG = {
    "eps_forecast_change_pct": 2.0,   # T2：今年度或明年度 EPS 預估較上一版變動 ≥ 此百分比
    "funnel_rank_delta": 0.05,        # T4：FunnelRank 分數變動 ≥ 此絕對值
}

# 每條觸發影響哪些「判斷層」小節（版面上的 Exhibit 徽章依此標「本版更新」）。
TRIGGER_SECTIONS = {
    "init": JUDGMENT_SECTIONS, "manual": JUDGMENT_SECTIONS,
    "T1": ["earnings_surprise"], "T2": ["eps_revision"], "T3": ["moat", "dd_screener_fields"],
    "T4": ["funnel_rank"], "T5": ["trend_state"], "T7": ["insider"], "T8": ["roic_decomposition"],
}


def _extract_judgment(out):
    """從剛算好的完整 out dict 抽出「判斷層」子樹，供存進 state 檔／沒觸發時整包沿用。"""
    full = out["full"]
    jc = full["judgment_core"]
    return {
        "trend_state": out.get("trend_state"),
        "eps_revision": jc.get("eps_revision"),
        "earnings_surprise": jc.get("earnings_surprise"),
        "moat": full.get("moat"),
        "roic_decomposition": jc.get("roic_decomposition"),
        "funnel_rank": jc.get("funnel_rank"),
        "insider": jc.get("insider"),
        "dd_screener_fields": jc.get("dd_screener_fields"),
    }


def _inject_judgment(out, judgment):
    """把 judgment dict（沿用舊版或剛算好的新版）寫回 out 對應位置，蓋掉 build() 原本
    算出來的新版判斷層內容（行情層欄位不受影響，維持每次都是新算的）。"""
    full = out["full"]
    jc = full["judgment_core"]
    out["trend_state"] = judgment.get("trend_state")
    jc["eps_revision"] = judgment.get("eps_revision")
    jc["earnings_surprise"] = judgment.get("earnings_surprise")
    full["moat"] = judgment.get("moat")
    jc["roic_decomposition"] = judgment.get("roic_decomposition")
    jc["funnel_rank"] = judgment.get("funnel_rank")
    jc["insider"] = judgment.get("insider")
    jc["dd_screener_fields"] = judgment.get("dd_screener_fields")


def compute_version_snapshot(out):
    """判斷層版本比對用的精簡快照——只留 T1-T8 判斷觸發要看的欄位，不是整份判斷層。"""
    full = out["full"]
    jc = full["judgment_core"]
    c1, c3 = jc.get("eps_revision") or {}, jc.get("earnings_surprise") or {}
    c5, c6, c7 = jc.get("insider") or {}, jc.get("dd_screener_fields") or {}, jc.get("funnel_rank") or {}
    moat, roic = full.get("moat") or {}, jc.get("roic_decomposition") or {}

    def _fy_row(idx):
        return c1["table"][idx] if c1.get("status") == "ok" and len(c1.get("table", [])) > idx else {}

    fy_curr, fy_next = _fy_row(0), _fy_row(1)
    judgment_block = moat.get("judgment") if moat.get("has_judgment") else None
    jcur = judgment_block["current"] if judgment_block else {}
    return {
        "last_earnings_date": c3.get("last_earnings_date"),
        "eps_fy_curr": fy_curr.get("current_estimate"), "eps_fy_next": fy_next.get("current_estimate"),
        "eps_fy_curr_revision_pct": fy_curr.get("vs_last_month_pct"), "eps_fy_next_revision_pct": fy_next.get("vs_last_month_pct"),
        "moat_judgment_date": _moat_date(jcur) if judgment_block else None,
        "moat_leans": "／".join(q.get("lean") or "—" for q in (jcur.get("questions") or [])) or None
                      if judgment_block else None,
        "moat_score": jcur.get("score") if judgment_block else None,
        "moat_width": jcur.get("width") if judgment_block else None,
        "moat_trend": jcur.get("trend") if judgment_block else None,
        "moat_version": jcur.get("version") if judgment_block else None,
        "moat_review_due": (judgment_block.get("review_due") or {}).get("due") if judgment_block else None,
        "dca_verdict": c6.get("dca_verdict") if c6.get("status") == "ok" else None,
        "dca_role": c6.get("dca_role") if c6.get("status") == "ok" else None,
        "funnel_rank": c7.get("funnel_rank") if c7.get("status") == "ok" else None,
        "funnel_vetoes": sorted(c7.get("vetoes_and_caps") or []) if c7.get("status") == "ok" else None,
        "trend_state_code": (out.get("trend_state") or {}).get("state"),
        "cluster_buy_condition_met": (c5.get("cluster_buy") or {}).get("cluster_buy_condition_met"),
        "quality_veto_level": roic.get("quality_veto_level") if roic.get("status") == "ok" else None,
        "decline_signal_light": roic.get("decline_signal_light") if roic.get("status") == "ok" else None,
    }


def check_version_triggers(new_snap, old_snap):
    """回傳這次相對上一版觸發了哪些條件，每條附中文描述＋前後值。"""
    fired = []
    cfg = VERSION_TRIGGER_CONFIG

    if new_snap.get("last_earnings_date") and old_snap.get("last_earnings_date") and \
            new_snap["last_earnings_date"] != old_snap["last_earnings_date"]:
        fired.append({"id": "T1", "desc_zh": "出現新一次財報",
                      "before": old_snap["last_earnings_date"], "after": new_snap["last_earnings_date"]})

    for label, key, rkey in [("今年度", "eps_fy_curr", "eps_fy_curr_revision_pct"), ("明年度", "eps_fy_next", "eps_fy_next_revision_pct")]:
        nv, ov = new_snap.get(key), old_snap.get(key)
        if nv is not None and ov not in (None, 0):
            pct = (nv / ov - 1) * 100
            if abs(pct) >= cfg["eps_forecast_change_pct"]:
                fired.append({"id": "T2", "desc_zh": f"{label} EPS 預估變動 {pct:+.1f}%（門檻 ±{cfg['eps_forecast_change_pct']}%）",
                              "before": ov, "after": nv})
        nr, org = new_snap.get(rkey), old_snap.get(rkey)
        if nr is not None and org is not None and nr != 0 and org != 0 and (nr > 0) != (org > 0):
            fired.append({"id": "T2", "desc_zh": f"{label} EPS 一個月修正方向反轉",
                          "before": f"{org:+.2f}%", "after": f"{nr:+.2f}%"})

    for key, label in [("moat_judgment_date", "護城河判斷日期"), ("moat_leans", "護城河三題證據偏向"), ("moat_score", "護城河分數"),
                        ("moat_width", "護城河寬窄"), ("moat_trend", "moat_trend"),
                        ("moat_version", "moat/{T}.json 版本"), ("moat_review_due", "護城河待複審旗標"),
                        ("dca_verdict", "dd-screener 裁決"), ("dca_role", "dd-screener 角色")]:
        nv, ov = new_snap.get(key), old_snap.get(key)
        if nv != ov and (nv is not None or ov is not None):
            fired.append({"id": "T3", "desc_zh": f"{label}改變", "before": ov, "after": nv})

    nf, of = new_snap.get("funnel_rank"), old_snap.get("funnel_rank")
    if nf is not None and of is not None and abs(nf - of) >= cfg["funnel_rank_delta"]:
        fired.append({"id": "T4", "desc_zh": f"FunnelRank 變動 {nf-of:+.3f}（門檻 {cfg['funnel_rank_delta']}）", "before": of, "after": nf})
    if new_snap.get("funnel_vetoes") != old_snap.get("funnel_vetoes"):
        fired.append({"id": "T4", "desc_zh": "FunnelRank 否決／封頂旗標改變",
                      "before": "、".join(old_snap.get("funnel_vetoes") or []) or "無",
                      "after": "、".join(new_snap.get("funnel_vetoes") or []) or "無"})

    if new_snap.get("trend_state_code") != old_snap.get("trend_state_code"):
        fired.append({"id": "T5", "desc_zh": "趨勢狀態切換",
                      "before": old_snap.get("trend_state_code"), "after": new_snap.get("trend_state_code")})

    if new_snap.get("cluster_buy_condition_met") != old_snap.get("cluster_buy_condition_met"):
        fired.append({"id": "T7", "desc_zh": "內部人群聚買進條件成立與否改變",
                      "before": old_snap.get("cluster_buy_condition_met"), "after": new_snap.get("cluster_buy_condition_met")})

    for key, label in [("quality_veto_level", "體質五項 veto 等級"), ("decline_signal_light", "衰退訊號燈號")]:
        if new_snap.get(key) != old_snap.get(key):
            fired.append({"id": "T8", "desc_zh": f"{label}改變", "before": old_snap.get(key), "after": new_snap.get(key)})

    return fired


def _state_path(ticker, state_dir):
    return state_dir / f"{ticker}.json"


def load_version_state(ticker, state_dir):
    p = _state_path(ticker, state_dir)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def save_version_state(state, state_dir):
    state_dir.mkdir(parents=True, exist_ok=True)
    _state_path(state["ticker"], state_dir).write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def apply_versioning(ticker, out, state_dir=None, force=False, dry_run=False):
    """判斷層版本化主流程：有觸發才改版，沒觸發就沿用舊版判斷層內容，只有行情層照
    新算的值走。就地修改並回傳 out（已經套用版本化的判斷層），加上版本中繼資料。"""
    state_dir = state_dir or STATE_DIR_DEFAULT
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    new_snapshot = compute_version_snapshot(out)
    new_judgment = _extract_judgment(out)
    old_state = load_version_state(ticker, state_dir)

    if old_state is None:
        triggers = [{"id": "init", "desc_zh": "首次建立", "before": None, "after": None}]
        version, judgment, snapshot = 1, new_judgment, new_snapshot
        section_versions = {s: {"last_changed_version": 1, "last_changed_date": today} for s in JUDGMENT_SECTIONS}
        changelog = [{"version": 1, "date": today, "triggers": triggers, "changed_sections": JUDGMENT_SECTIONS}]
    else:
        triggers = [{"id": "manual", "desc_zh": "手動強制改版", "before": None, "after": None}] if force \
            else check_version_triggers(new_snapshot, old_state.get("snapshot") or {})
        if triggers:
            version = old_state.get("version", 0) + 1
            judgment, snapshot = new_judgment, new_snapshot
            changed_sections = sorted(set(s for t in triggers for s in TRIGGER_SECTIONS.get(t["id"], [])))
            section_versions = dict(old_state.get("section_versions") or {})
            for s in changed_sections:
                section_versions[s] = {"last_changed_version": version, "last_changed_date": today}
            changelog = list(old_state.get("changelog") or [])
            changelog.append({"version": version, "date": today, "triggers": triggers, "changed_sections": changed_sections})
        else:
            version = old_state.get("version", 1)
            judgment = old_state.get("judgment") or new_judgment
            snapshot = old_state.get("snapshot") or new_snapshot
            section_versions = old_state.get("section_versions") or {}
            changelog = list(old_state.get("changelog") or [])

    version_date = next((e["date"] for e in changelog if e["version"] == version),
                         old_state.get("version_date") if old_state else today)
    latest_changes = next((e["triggers"] for e in reversed(changelog) if e["version"] == version), [])

    state = {"ticker": ticker, "version": version, "version_date": version_date,
             "judgment": judgment, "snapshot": snapshot, "changelog": changelog, "section_versions": section_versions}
    if not dry_run:
        save_version_state(state, state_dir)

    _inject_judgment(out, judgment)
    out["judgment_version"] = version
    out["judgment_version_date"] = version_date
    out["latest_changes"] = latest_changes
    out["changelog"] = changelog
    out["section_versions"] = section_versions
    return out, triggers if (old_state is not None) else [{"id": "init", "desc_zh": "首次建立"}]


# ──────────────────────────────────────────────────────────────── build ────
def build(ticker, refresh_universe=False, state_dir=None, force_version=False, dry_run=False):
    t = yf.Ticker(ticker)
    df_full = compute_indicators(fetch_history(ticker, "2y"))
    spy_full = compute_indicators(fetch_history_cached("SPY", "2y"))

    as_of = df_full.index[-1].date()
    last = df_full.iloc[-1]
    prev = df_full.iloc[-2]
    price = float(last["Close"])

    try:
        info = t.info or {}
    except Exception:  # noqa: BLE001
        info = {}

    change = price - float(prev["Close"])
    change_pct = change / float(prev["Close"]) * 100

    display = df_full.tail(DISPLAY_DAYS)
    price_history = []
    for idx, row in display.iterrows():
        price_history.append({
            "date": idx.strftime("%Y-%m-%d"),
            "open": r2(row["Open"]), "high": r2(row["High"]),
            "low": r2(row["Low"]), "close": r2(row["Close"]),
            "volume": int(row["Volume"]),
            "ma21": r2(row["MA21"]), "ma50": r2(row["MA50"]), "ma200": r2(row["MA200"]),
            "vwap20": r2(row["VWAP20"]),
        })

    vol_profile = compute_volume_profile(df_full, price)
    support, resistance, sr_notes = resolve_support_resistance(df_full, price, vol_profile)

    rel_strength = compute_relative_strength(df_full, spy_full)

    dist_52w_high = float(df_full["Close"].tail(252).max())
    dist_52w_high_pct = (price / dist_52w_high - 1) * 100
    atr_pct_now = float(df_full["ATR_PCT"].iloc[-1])
    atr_pctile_1y = pct_rank(df_full["ATR_PCT"].tail(252), atr_pct_now)

    status_summary = {
        "price_vs_ma50_pct": r2((price / float(last["MA50"]) - 1) * 100),
        "price_vs_ma200_pct": r2((price / float(last["MA200"]) - 1) * 100),
        "ma50_slope_10d_pct": r2((float(last["MA50"]) / float(df_full["MA50"].iloc[-11]) - 1) * 100)
        if len(df_full) > 11 else None,
        "rsi14": r2(float(last["RSI14"]), 1),
        "price_vs_ma21_pct": r2((price / float(last["MA21"]) - 1) * 100),
        "atr_pct": r2(atr_pct_now, 2),
        "atr_pct_percentile_1y": r2(atr_pctile_1y, 1),
        "dist_52w_high_pct": r2(dist_52w_high_pct),
        "rel_strength_vs_spy": rel_strength,
        "support": support,
        "resistance": resistance,
        "support_resistance_fallback_notes": sr_notes,
    }

    range_proj = compute_range_projection(df_full, atr_pct=atr_pct_now)

    short_vol_block = fetch_short_volume(df_full, ticker)
    short_interest_info = {
        "shortPercentOfFloat_pct": r2(info.get("shortPercentOfFloat") * 100, 2)
        if info.get("shortPercentOfFloat") is not None else None,
        "shortRatio_days_to_cover": r2(info.get("shortRatio"), 2),
        "sharesShort": info.get("sharesShort"),
        "sharesShortPriorMonth": info.get("sharesShortPriorMonth"),
        "dateShortInterest": (
            datetime.fromtimestamp(info["dateShortInterest"], tz=timezone.utc).strftime("%Y-%m-%d")
            if info.get("dateShortInterest") else None
        ),
    }
    if not any(v is not None for v in short_interest_info.values()):
        short_interest_info = {"status": "no_data", "reason": "yfinance info 未回傳放空相關欄位"}

    insiders = fetch_insiders(t, as_of)

    log_ret_20 = np.diff(np.log(df_full["Close"].tail(21).values))
    hv20 = float(np.std(log_ret_20, ddof=1) * np.sqrt(252) * 100) if len(log_ret_20) >= 10 else None
    options = fetch_options(t, price, hv20)

    universe_dist = ensure_universe_distribution(as_of.strftime("%Y-%m-%d"), force=refresh_universe)
    scores = compute_scores(df_full, universe_dist, short_vol_block, info)

    spy_price = float(spy_full["Close"].iloc[-1])
    spy_ma200 = float(spy_full["MA200"].iloc[-1])
    ensure_market_context()  # writes/refreshes docs/stock-dash/data/_market.json (shared across tickers)
    market_beta = compute_market_beta(ticker, df_full, spy_full)
    market_env = {
        "spy_price": r2(spy_price),
        "spy_ma200": r2(spy_ma200),
        "spy_vs_ma200_pct": r2((spy_price / spy_ma200 - 1) * 100),
        "spy_as_of": spy_full.index[-1].strftime("%Y-%m-%d"),
        "market_context_file": "data/_market.json",
        "market_beta": market_beta,
    }

    # ── full (18-panel) additions ──
    avg_dollar_vol_20d = float((df_full["Close"] * df_full["Volume"]).tail(20).mean())
    insider_score, insider_note = compute_insider_health(insiders, avg_dollar_vol_20d, INSIDER_WINDOW_DAYS)
    insider_risk_score = (100 - insider_score) if insider_score is not None else None

    event_date, event_days, event_reason = compute_event_risk(t, as_of)

    short_z_val = short_vol_block.get("z_score_recent30_vs_60") if short_vol_block.get("status") in ("ok", "partial") else None
    risk_radar = compute_risk_radar(
        df_full, scores["dims"]["trend"], atr_pctile_1y, short_z_val,
        insider_risk_score, event_days, event_reason,
    )
    dim_states = compute_dim_states(scores, risk_radar)
    trend_state = compute_trend_state(ticker, scores, status_summary, short_vol_block, event_days)
    health_gauges = compute_health_gauges(scores, insider_score, insider_note)

    price_time_heatmap = compute_price_time_heatmap(df_full)
    cost_distribution = compute_cost_distribution(df_full)
    updown_volume = compute_updown_volume(df_full)
    updown_strength = compute_updown_strength(df_full)
    overheat_check = compute_overheat_check(df_full, info.get("sharesOutstanding"))
    chip_changes = fetch_chip_changes(t, short_interest_info)
    data_reliability = compute_data_reliability(as_of.strftime("%Y-%m-%d"), short_vol_block, insiders, options, dim_states)

    # ── 研判核心 (judgment core, Phase 7) ──
    dd_row, dd_meta = find_dd_screener_row(ticker)
    dd_stocks = dd_meta.get("stocks", []) if dd_meta.get("status") == "ok" else []
    analyst_rev = fetch_analyst_revision_counts(t, as_of)
    jc_card1 = build_card_eps_revision(ticker, dd_row, info, analyst_rev)
    jc_card2 = build_card_price_vs_eps(ticker, dd_row, df_full, price, jc_card1)
    jc_card3 = build_card_earnings_surprise(ticker, dd_row, t, df_full, spy_full, price, as_of)
    jc_card4 = build_card_roic_decomposition(dd_row)
    jc_card5 = build_card_insider(ticker, dd_row, t, as_of)
    jc_card6 = build_card_dd_screener_fields(dd_row, as_of, price)
    jc_card7 = build_card_funnel_rank(dd_row, dd_stocks)
    eps_prev_fy = fetch_prev_fy_actual_eps(t, jc_card1)
    cockpit = build_cockpit_status(ticker)
    analyst_targets = build_analyst_targets(info, price)
    moat, moat_changes, moat_rivals = build_card_moat(ticker, dd_row, dd_stocks)
    moat_footprint = build_moat_footprint(ticker, dd_row, dd_stocks)
    judgment_core = {
        "in_dd_screener": dd_row is not None,
        "eps_revision": jc_card1,
        "price_vs_eps": jc_card2,
        "earnings_surprise": jc_card3,
        "roic_decomposition": jc_card4,
        "insider": jc_card5,
        "dd_screener_fields": jc_card6,
        "funnel_rank": jc_card7,
        "eps_prev_fy": eps_prev_fy,  # 不在 JUDGMENT_SECTIONS，每次 build 都更新
    }

    full = {
        "dim_states": dim_states,
        "health_gauges": health_gauges,
        "risk_radar": risk_radar,
        "price_time_heatmap": price_time_heatmap,
        "cost_distribution": cost_distribution,
        "updown_volume": updown_volume,
        "updown_strength": updown_strength,
        "overheat_check": overheat_check,
        "chip_changes": chip_changes,
        "data_reliability": data_reliability,
        "event": {"next_earnings_date": event_date, "days_to_earnings": event_days, "reason": event_reason},
        "judgment_core": judgment_core,
        "moat": moat,
        "moat_changes": moat_changes,
        "moat_rivals": moat_rivals,
        "moat_footprint": moat_footprint,  # 護城河章實際顯示的內容（機械數字）；上面三個是舊判斷檔資料，頁面不再顯示
        "cockpit": cockpit,  # 主控台陣容狀態，每次 build 都更新
        "analyst_targets": analyst_targets,  # 分析師目標價／52週區間，每次 build 都更新
    }

    out = {
        "schema": "stock-dash-v1",
        "ticker": ticker,
        "as_of": as_of.strftime("%Y-%m-%d"),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z",
        "data_sources": {
            "price": "yfinance Ticker.history(period='2y', interval='1d', auto_adjust=False)",
            "info": "yfinance Ticker.info",
            "short_volume": "FINRA Reg SHO daily short volume (cdn.finra.org)",
            "insiders": "yfinance Ticker.insider_transactions",
            "options": "yfinance Ticker.option_chain",
            "market_env": "docs/market/data/state.json + read.json (summarized into data/_market.json, fetched client-side) + yfinance SPY history",
            "scores": "docs/screener/latest.json universe + yfinance 2y history (summarized into data/_universe_dist.json, shared across tickers)",
            "judgment_core": "docs/dd-screener/latest.json (339 檔既有欄位，presentation-only，不重算) + docs/dd-screener/eps-estimates-snapshots/ + yfinance (earnings surprises / analyst revisions / insider transactions) + ~/v7-backtest/results/pead/pead_events.csv (summarized into data/_sue_breaks.json)",
        },
        "quote": {
            "name": info.get("longName") or info.get("shortName") or ticker,
            "close": r2(price),
            "change": r2(change),
            "change_pct": r2(change_pct),
            "open": r2(float(last["Open"])),
            "high": r2(float(last["High"])),
            "low": r2(float(last["Low"])),
            "volume": int(last["Volume"]),
            "as_of_date": as_of.strftime("%Y-%m-%d"),
        },
        "display_days": DISPLAY_DAYS,
        "price_history": price_history,
        "status_summary": status_summary,
        "scores": scores,
        "volume_profile": vol_profile,
        "range_projection": range_proj,
        "short_volume": short_vol_block,
        "short_interest_info": short_interest_info,
        "insiders": insiders,
        "options": options,
        "market_env": market_env,
        "trend_state": trend_state,
        "full": full,
    }

    state_dir = state_dir or STATE_DIR_DEFAULT
    out, fired_this_build = apply_versioning(ticker, out, state_dir=state_dir, force=force_version, dry_run=dry_run)
    out["_version_dry_run_fired"] = fired_this_build if dry_run else None  # 只有 --dry-run 時才有意義，正式輸出忽略
    return out


def main():
    ap = argparse.ArgumentParser(description="Build stock-dash JSON for one ticker (zero-LLM, mechanical).")
    ap.add_argument("ticker", help="e.g. NVDA")
    ap.add_argument("--refresh-universe", action="store_true",
                     help="force-rebuild docs/stock-dash/data/_universe_dist.json even if it looks fresh")
    ap.add_argument("--force-version", action="store_true",
                     help="判斷層強制改版（原因記「手動」），不管有沒有觸發 T1-T8")
    ap.add_argument("--dry-run", action="store_true",
                     help="只印這次會觸發哪些判斷層版本條件，不寫 state 檔也不寫 {T}.json")
    ap.add_argument("--state-dir", default=None,
                     help="判斷層版本 state 檔目錄（測試用；預設 docs/stock-dash/data/state/）")
    args = ap.parse_args()
    ticker = args.ticker.upper().strip()
    state_dir = Path(args.state_dir) if args.state_dir else None

    t0 = time.time()
    data = build(ticker, refresh_universe=args.refresh_universe, state_dir=state_dir,
                 force_version=args.force_version, dry_run=args.dry_run)

    if args.dry_run:
        fired = data.get("_version_dry_run_fired") or []
        if fired:
            print(f"[dry-run] {ticker}：會觸發 {len(fired)} 條判斷層版本條件：")
            for t in fired:
                extra = f"　{t.get('before')} → {t.get('after')}" if t.get("before") is not None or t.get("after") is not None else ""
                print(f"  {t['id']}：{t['desc_zh']}{extra}")
        else:
            print(f"[dry-run] {ticker}：沒有觸發任何判斷層版本條件，判斷層會沿用舊版（不寫 state 檔）")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{ticker}.json"
    data.pop("_version_dry_run_fired", None)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out_path} ({out_path.stat().st_size} bytes) in {time.time()-t0:.1f}s — "
          f"判斷版本 v{data.get('judgment_version')}（{data.get('judgment_version_date')}）")


if __name__ == "__main__":
    main()
