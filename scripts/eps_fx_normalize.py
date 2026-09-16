#!/usr/bin/env python3
"""FX-normalization helpers for cross-snapshot EPS revision comparisons.

Bug this fixes (2026-09-17): Koyfin exports EPS converted to USD at the FX
rate of the export date. When build_dd_screener.py compares the current
xlsx's USD EPS against a prior monthly baseline's USD EPS, any company that
reports in a non-USD currency shows a fake "revision" whenever the FX rate
moved between the two snapshot dates — a pure currency move, not an analyst
revision. compute_funnel_rank()'s veto_all_downgrade rule (all three FY
revisions <= -0.5%) was firing on these FX artifacts (ASML, 2330.TW, RACE,
LVMH, BMO, ONON, MELI).

Fix: compare in the company's REPORTING currency (yfinance
`Ticker(t).info["financialCurrency"]` — the currency of the financial
statements, NOT the trading currency), not raw USD:

    current_local  = current_usd_eps  x FX_local_per_usd(current snapshot date)
    baseline_local = baseline_usd_eps x FX_local_per_usd(baseline snapshot date)
    revision_pct   = current_local / baseline_local - 1

For USD reporters this is a no-op. When the reporting currency or either FX
rate is unavailable, falls back to the raw USD-vs-USD comparison and flags
`fx_normalized=False` so callers/pages can surface that the number may
contain an FX artifact.

Two persistent, process-wide JSON caches (both survive across builds so
rebuilds are deterministic and don't re-hit yfinance for tickers/dates
already resolved):

  data/reporting_currency.json — {ticker: {"currency": "EUR", "checked": "YYYY-MM-DD"}}
      Keyed by the DD-universe ticker (not the yfinance symbol), since that's
      the stable identity used throughout the rest of the pipeline. Only
      successful fetches are cached; a transient yfinance failure leaves the
      ticker absent so the next build retries instead of permanently
      recording "unknown".

  data/fx_daily_cache.json — {currency: {date: {"rate": local_per_usd}}}
      `date` is the requested date (YYYY-MM-DD); the actual rate may come
      from up to 5 calendar days earlier when the requested date has no
      trading data (weekend/holiday).

Both caches are plain dicts the caller loads once, mutates in place (thread-
safe via the module-level locks below — enrich_ticker() in
build_dd_screener.py runs inside a ThreadPoolExecutor), and persists back to
disk once at the end of the run.
"""
from __future__ import annotations

import json
import sys
import threading
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "-q"])
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
REPORTING_CCY_CACHE_PATH = ROOT / "data" / "reporting_currency.json"
FX_DAILY_CACHE_PATH = ROOT / "data" / "fx_daily_cache.json"

_reporting_ccy_lock = threading.Lock()
_fx_cache_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Persistent cache I/O
# ---------------------------------------------------------------------------


def load_reporting_currency_cache(path: Path | None = None) -> dict:
    p = path or REPORTING_CCY_CACHE_PATH
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_reporting_currency_cache(cache: dict, path: Path | None = None) -> None:
    p = path or REPORTING_CCY_CACHE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
                 encoding="utf-8")


def load_fx_daily_cache(path: Path | None = None) -> dict:
    p = path or FX_DAILY_CACHE_PATH
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_fx_daily_cache(cache: dict, path: Path | None = None) -> None:
    p = path or FX_DAILY_CACHE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
                 encoding="utf-8")


# ---------------------------------------------------------------------------
# Reporting currency (financialCurrency)
# ---------------------------------------------------------------------------


def get_reporting_currency(dd_ticker: str, yf_ticker: str, cache: dict) -> str | None:
    """Reporting (financial-statement) currency for `dd_ticker`, e.g. "EUR".

    `yf_ticker` must be the SAME yfinance symbol the rest of the build
    resolves for this ticker (see build_dd_screener.py's `_yf_ticker_for_ma` /
    dd_screener_quality.TICKER_YF_OVERRIDE + EU_SUFFIX_MAP) — ASML trades in
    USD on NASDAQ but reports in EUR, so this is NOT the trading currency.

    Never raises — a yfinance failure returns None (caller falls back to the
    raw USD-vs-USD comparison) rather than aborting the build.
    """
    with _reporting_ccy_lock:
        hit = cache.get(dd_ticker)
    if hit and hit.get("currency"):
        return hit["currency"]
    try:
        info = yf.Ticker(yf_ticker).info
        ccy = info.get("financialCurrency")
    except Exception:
        return None
    if not ccy:
        return None
    ccy = str(ccy).upper()
    with _reporting_ccy_lock:
        cache[dd_ticker] = {"currency": ccy, "checked": datetime.now().strftime("%Y-%m-%d")}
    return ccy


# ---------------------------------------------------------------------------
# Daily FX rate (local currency units per 1 USD)
# ---------------------------------------------------------------------------


def _fetch_fx_close(pair_ticker: str, date_str: str, invert: bool) -> float | None:
    """One yfinance history lookup. Returns local_per_usd (inverted if the
    ticker quotes USD-per-local instead), using the last close at or before
    `date_str` within a 5-day lookback window. None on any failure."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
    except (TypeError, ValueError):
        return None
    start = (d - timedelta(days=5)).strftime("%Y-%m-%d")
    end = (d + timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        hist = yf.Ticker(pair_ticker).history(start=start, end=end)
    except Exception:
        return None
    if hist is None or hist.empty:
        return None
    try:
        on_or_before = hist.loc[hist.index.date <= d.date()]
        sub = on_or_before if not on_or_before.empty else hist
        close = float(sub["Close"].iloc[-1])
    except Exception:
        return None
    if close <= 0:
        return None
    return (1.0 / close) if invert else close


def get_fx_rate(currency: str, date_str: str, cache: dict) -> float | None:
    """Local-currency units per 1 USD, as of `date_str` (or the nearest
    earlier trading day within 5 days). Persistently cached by currency+date.

    Tries yfinance "USD{CUR}=X" first (quotes local-per-USD directly for
    every currency observed in this universe, majors included — e.g.
    "USDEUR=X" returns EUR-per-USD even though "EURUSD=X" is the more
    commonly-quoted pair), then falls back to "{CUR}USD=X" inverted for any
    pair yfinance only serves that way.
    """
    if not currency:
        return None
    currency = currency.upper()
    if currency == "USD":
        return 1.0
    with _fx_cache_lock:
        hit = (cache.get(currency) or {}).get(date_str)
    if hit is not None:
        return hit.get("rate")
    rate = _fetch_fx_close(f"USD{currency}=X", date_str, invert=False)
    if rate is None:
        rate = _fetch_fx_close(f"{currency}USD=X", date_str, invert=True)
    if rate is None:
        return None
    with _fx_cache_lock:
        cache.setdefault(currency, {})[date_str] = {"rate": round(rate, 6)}
    return rate


# ---------------------------------------------------------------------------
# Pure math — unit-testable without any network/cache dependency
# ---------------------------------------------------------------------------


def resolve_fx_normalization(currency: str | None,
                              fx_current_per_usd: float | None,
                              fx_baseline_per_usd: float | None) -> tuple[bool, bool]:
    """Decide whether/how to FX-normalize a USD-basis EPS comparison.

    Returns (use_fx, fx_normalized):
      - USD reporter (currency == "USD"):        (False, True) — already
        apples-to-apples in USD, nothing to normalize.
      - Non-USD reporter with both FX rates available: (True, True).
      - Currency unknown or either FX rate unavailable: (False, False) —
        caller falls back to the raw USD-vs-USD comparison, flagged
        not-normalized so the page/logs can surface it.
    """
    if currency and currency.upper() == "USD":
        return False, True
    if (currency and fx_current_per_usd is not None and fx_baseline_per_usd is not None
            and fx_current_per_usd > 0 and fx_baseline_per_usd > 0):
        return True, True
    return False, False


def compute_fx_normalized_revision(current_usd: float | None, baseline_usd: float | None,
                                    currency: str | None,
                                    fx_current_per_usd: float | None,
                                    fx_baseline_per_usd: float | None) -> tuple[float | None, bool]:
    """% change between two USD EPS snapshots, FX-normalized to the
    reporting currency when possible.

    Returns (revision_pct, fx_normalized). revision_pct is None when either
    input EPS is missing or baseline is zero.
    """
    if current_usd is None or baseline_usd is None or baseline_usd == 0:
        return None, False
    use_fx, fx_normalized = resolve_fx_normalization(currency, fx_current_per_usd, fx_baseline_per_usd)
    if use_fx:
        current_local = current_usd * fx_current_per_usd
        baseline_local = baseline_usd * fx_baseline_per_usd
        if baseline_local == 0:
            return None, False
        return (current_local / baseline_local - 1) * 100, fx_normalized
    return (current_usd / baseline_usd - 1) * 100, fx_normalized
