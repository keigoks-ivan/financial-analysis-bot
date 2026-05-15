"""
DD Screener — MA Snapshot helper (Sonnet B task).

Public API:
    compute_ma_snapshot(yf_ticker: str, period: str = "5y") -> dict

Returns the `ma` sub-object defined in scripts/dd_screener_schema.md.

CLI:
    python3 scripts/dd_screener_ma.py NVDA AAPL 2330.TW RMS.PA INVALID_TICKER_XYZ
"""

import json
import logging
import sys
import time
import warnings

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

def compute_ma_snapshot(yf_ticker: str, period: str = "5y") -> dict:
    """Fetch ~5y of weekly closes for yf_ticker via yfinance, compute MA snapshot.

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
      }

    Graceful degradation: any field with insufficient history is None.
    Returns all-None dict if yfinance returns no data at all.
    Never raises — catches exceptions and returns all-None.
    """
    try:
        ticker_obj = yf.Ticker(yf_ticker)
        df = ticker_obj.history(period=period, interval="1wk")

        if df is None or df.empty or "Close" not in df.columns:
            return dict(_ALL_NONE)

        closes = df["Close"].dropna()
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

        return {
            "price":          price,
            "w52":            w52,
            "w104":           w104,
            "w250":           w250,
            "slope_w250_pct": slope_w250_pct,
            "drift_4w_pct":   drift_4w_pct,
            "above_w52":      above_w52,
            "above_w250":     above_w250,
        }

    except Exception:
        return dict(_ALL_NONE)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _main(tickers) -> None:
    results = {}
    t_start = time.monotonic()

    for ticker in tickers:
        snap = compute_ma_snapshot(ticker)
        results[ticker] = snap

    elapsed = time.monotonic() - t_start
    succeeded = sum(1 for s in results.values() if s["price"] is not None)

    print(f"# {succeeded}/{len(tickers)} fetched — {elapsed:.1f}s")
    for ticker, snap in results.items():
        print(f"{ticker}: {json.dumps(snap)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 scripts/dd_screener_ma.py TICKER [TICKER ...]")
        sys.exit(1)
    _main(args)
