"""
DD Screener — MA Snapshot helper (Sonnet B task).

Public API:
    compute_ma_snapshot(yf_ticker: str, period: str = "5y", *, use_cache=True) -> dict

Returns the `ma` sub-object defined in scripts/dd_screener_schema.md.

CLI:
    python3 scripts/dd_screener_ma.py NVDA AAPL 2330.TW RMS.PA INVALID_TICKER_XYZ
    python3 scripts/dd_screener_ma.py --no-cache NVDA      # bypass weekly_cache

# v1.7: Cache-backed (Phase 2)
  Persistent `data/weekly_cache/{TICKER}.json` removes the need to re-pull 5y
  weekly bars every day. Per build per ticker:
    - Slot day (1/5 of universe per build) → full 5y yfinance pull, overwrite
      cache. Auto-corrects yfinance back-adjustment drift over ~5-day cycle.
    - Off-slot → incremental 2-month pull, splice into cache.
    - Split detected (>=40% bar move vs cached) → emergency full rebackfill.
    - Yfinance failure → fall back to cached bars (unlimited outage tolerance
      as long as cache file exists).
  Behavior is transparent: returns the same `ma` dict shape; derived stats
  computed from the merged-with-cache series are numerically identical to a
  pure fresh pull (modulo yfinance auto-adjustment drift, which the rolling
  rebackfill corrects within 5 days).
"""

import argparse
import json
import logging
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "pandas", "-q"])
    import pandas as pd
    import yfinance as yf

# Make scripts/lib importable when running as a script (not via build_dd_screener)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib import weekly_cache as _wc  # noqa: E402

# Silence yfinance's own logger and urllib3 noise so stdout stays clean
# for the orchestrator.
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("peewee").setLevel(logging.CRITICAL)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ALL_NONE: dict = {
    "price":           None,
    "w52":             None,
    "w104":            None,
    "w250":            None,
    "slope_w250_pct":  None,
    "drift_4w_pct":    None,
    "above_w52":       None,
    "above_w250":      None,
    # v1.6: 5y cycle context for entry-state-machine
    "high_250w_price":       None,
    "dist_250w_high_pct":    None,
    "weeks_since_250w_high": None,
    "is_full_5y":            None,
    "drift_4w_min_in_8w":    None,
}


def _float2(val):
    """Cast to plain Python float, rounded to 2 dp. Returns None if val is None/NaN."""
    try:
        f = float(val)
        if f != f:  # NaN check without importing math
            return None
        return round(f, 2)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

def _bars_to_series(bars: list) -> "pd.Series":
    """Convert weekly_cache bars list → pandas Series indexed by week_end date.

    Empty bars → empty Series. The rest of compute uses positional .iloc[*]
    so the index is informational, not load-bearing.
    """
    if not bars:
        return pd.Series(dtype=float)
    return pd.Series(
        [float(b["close"]) for b in bars],
        index=pd.to_datetime([b["week_end"] for b in bars]),
    )


def _compute_derived(closes: "pd.Series") -> dict:
    """Compute the full `ma` dict from a closes Series.

    Single source of truth for derived-stats logic — called by both the
    fresh-yfinance path and the cache-fallback path. All fields degrade to
    None when history is insufficient.
    """
    n = len(closes)
    if n == 0:
        return dict(_ALL_NONE)

    # --- price ---
    price = _float2(closes.iloc[-1])

    # --- rolling MAs ---
    w52 = _float2(closes.rolling(52).mean().iloc[-1]) if n >= 52 else None
    w104 = _float2(closes.rolling(104).mean().iloc[-1]) if n >= 104 else None
    w250 = _float2(closes.rolling(250).mean().iloc[-1]) if n >= 250 else None

    # --- drift_4w_pct: needs current + 4 bars ago (index -5) ---
    if n >= 5:
        drift_4w_pct = _float2((closes.iloc[-1] / closes.iloc[-5] - 1) * 100)
    else:
        drift_4w_pct = None

    # --- slope_w250_pct: needs W250 now + W250 4 weeks ago ---
    # W250 4w ago requires index position -(4+1)=-5 to have enough
    # history for a 250-bar window, so total bars needed = 250 + 4 = 254.
    if n >= 254:
        rolling_w250 = closes.rolling(250).mean()
        w250_now = rolling_w250.iloc[-1]
        w250_4w_ago = rolling_w250.iloc[-5]
        slope_w250_pct = _float2((w250_now / w250_4w_ago - 1) * 100)
    else:
        slope_w250_pct = None

    # --- above_w52 / above_w250 ---
    above_w52 = (bool(price > w52)) if (price is not None and w52 is not None) else None
    above_w250 = (bool(price > w250)) if (price is not None and w250 is not None) else None

    # --- v1.6: 5y cycle context (true ATH window for entry-state-machine) ---
    high_250w_price = None
    dist_250w_high_pct = None
    weeks_since_250w_high = None
    is_full_5y = None
    if n >= 50:
        window = closes.iloc[-250:] if n >= 250 else closes
        high_p = float(window.max())
        argmax_pos = int(window.values.argmax())
        high_250w_price       = _float2(high_p)
        dist_250w_high_pct    = _float2((float(closes.iloc[-1]) - high_p) / high_p * 100) if high_p else None
        weeks_since_250w_high = len(window) - argmax_pos - 1
        is_full_5y            = bool(n >= 250)

    # --- v1.6: PULLBACK 歷史 lookback — past 8 weeks' deepest 4w drift ---
    drift_4w_min_in_8w = None
    if n >= 12:
        past_drifts = [
            (float(closes.iloc[k]) / float(closes.iloc[k - 4]) - 1) * 100
            for k in range(max(4, n - 8), n)
        ]
        if past_drifts:
            drift_4w_min_in_8w = _float2(min(past_drifts))

    return {
        "price":          price,
        "w52":            w52,
        "w104":           w104,
        "w250":           w250,
        "slope_w250_pct": slope_w250_pct,
        "drift_4w_pct":   drift_4w_pct,
        "above_w52":      above_w52,
        "above_w250":     above_w250,
        "high_250w_price":       high_250w_price,
        "dist_250w_high_pct":    dist_250w_high_pct,
        "weeks_since_250w_high": weeks_since_250w_high,
        "is_full_5y":            is_full_5y,
        "drift_4w_min_in_8w":    drift_4w_min_in_8w,
    }


def compute_ma_snapshot(yf_ticker: str, period: str = "5y", *, use_cache: bool = True) -> dict:
    """Fetch ~5y of weekly closes for yf_ticker (yfinance or cache), compute MA snapshot.

    Returns a dict matching the `ma` sub-object in scripts/dd_screener_schema.md:
      {
        "price":  float | None,
        "w52":    float | None,
        "w104":   float | None,
        "w250":   float | None,
        "slope_w250_pct": float | None,
        "drift_4w_pct":   float | None,
        "above_w52":  bool | None,
        "above_w250": bool | None,
        # v1.6 5y cycle context (additive, for entry-state-machine page):
        "high_250w_price":       float | None,
        "dist_250w_high_pct":    float | None,
        "weeks_since_250w_high": int   | None,
        "is_full_5y":            bool  | None,
        "drift_4w_min_in_8w":    float | None,
      }

    v1.7 cache-backed paths (use_cache=True, default):
      1. Slot-day OR cache-empty → full 5y yfinance pull, overwrite cache.
      2. Off-slot → 2-month incremental pull, splice into cache.
      3. Split detected (incremental's latest vs cached prev close >= 40%) →
         emergency full pull, ignoring rotation.
      4. Any yfinance failure → compute from existing cache (unlimited
         outage tolerance as long as cache file exists).

    Graceful degradation: any field with insufficient history is None.
    Returns all-None dict if both yfinance and cache fail.
    Never raises — catches exceptions and returns all-None.
    """
    # Load existing cache up front (None / empty if first deploy or disabled)
    cache_obj = _wc.read_ticker_cache(yf_ticker) if use_cache else None
    cached_bars = (cache_obj or {}).get("weekly_bars") or []

    # Decide pull strategy
    force_full = (
        not use_cache
        or not cached_bars
        or _wc.is_full_rebackfill_day(yf_ticker)
    )

    bars_to_persist: list | None = None    # cache to write back
    full_refresh_flag = False               # for cache write semantics
    closes: "pd.Series" | None = None        # final closes series for derived stats

    try:
        ticker_obj = yf.Ticker(yf_ticker)

        if force_full:
            df = ticker_obj.history(period=period, interval="1wk")
            if df is not None and not df.empty and "Close" in df.columns:
                closes = df["Close"].dropna()
                if use_cache:
                    bars_to_persist = _wc.df_to_bars(df)
                    full_refresh_flag = True
            elif cached_bars:
                # Yfinance failed on a full-pull day → use cache as-is, don't update
                closes = _bars_to_series(cached_bars)
        else:
            # Incremental: pull last 2 months of weekly bars (enough to update the
            # in-progress current week + catch any recent missed bar).
            small_df = ticker_obj.history(period="2mo", interval="1wk")
            if small_df is None or small_df.empty or "Close" not in small_df.columns:
                # Incremental fetch failed → use cache as-is
                closes = _bars_to_series(cached_bars)
            else:
                # Split detection: compare latest pulled close vs cached prev close
                fresh_closes = small_df["Close"].dropna()
                latest_pulled = float(fresh_closes.iloc[-1]) if not fresh_closes.empty else None
                if _wc.detect_split(latest_pulled, _wc.latest_close(cached_bars)):
                    # Emergency full rebackfill — cached bars are on the wrong scale
                    df = ticker_obj.history(period=period, interval="1wk")
                    if df is not None and not df.empty and "Close" in df.columns:
                        closes = df["Close"].dropna()
                        bars_to_persist = _wc.df_to_bars(df)
                        full_refresh_flag = True
                    else:
                        # Even full-pull failed — last-resort cache fallback
                        closes = _bars_to_series(cached_bars)
                else:
                    # Normal incremental: merge fresh bars into cache
                    merged_bars = _wc.merge_incremental(cached_bars, small_df)
                    closes = _bars_to_series(merged_bars)
                    bars_to_persist = merged_bars
                    full_refresh_flag = False

        if closes is None or len(closes) == 0:
            return dict(_ALL_NONE)

        result = _compute_derived(closes)

        # Persist cache (post-compute, so partial state never lands on disk)
        if bars_to_persist is not None and use_cache:
            try:
                _wc.write_ticker_cache(
                    yf_ticker, bars_to_persist, full_refresh=full_refresh_flag
                )
            except OSError:
                # Cache write failures shouldn't break the build — derived
                # stats are already computed in `result`.
                pass

        return result

    except Exception:
        # Last-resort: try compute from cache (any prior good state beats all-None)
        if use_cache and cached_bars:
            try:
                return _compute_derived(_bars_to_series(cached_bars))
            except Exception:
                pass
        return dict(_ALL_NONE)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _main(tickers, use_cache: bool = True) -> None:
    results = {}
    t_start = time.monotonic()

    for ticker in tickers:
        snap = compute_ma_snapshot(ticker, use_cache=use_cache)
        results[ticker] = snap

    elapsed = time.monotonic() - t_start
    succeeded = sum(1 for s in results.values() if s["price"] is not None)

    cache_summary = _wc.cache_summary()
    mode = "cache-backed" if use_cache else "no-cache"
    print(f"# {succeeded}/{len(tickers)} fetched — {elapsed:.1f}s  ({mode})")
    print(f"# cache: {cache_summary['tickers']} files / {cache_summary['total_kb']} KB")
    for ticker, snap in results.items():
        print(f"{ticker}: {json.dumps(snap)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DD Screener MA snapshot helper")
    parser.add_argument("tickers", nargs="+", help="Ticker symbols to compute")
    parser.add_argument("--no-cache", action="store_true",
                        help="Bypass weekly_cache (always full yfinance pull, no cache write)")
    args = parser.parse_args()
    _main(args.tickers, use_cache=not args.no_cache)
