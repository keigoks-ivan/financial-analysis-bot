"""DD Screener Step 3: hybrid quality data fetcher.

For each DD ticker, return the 5 QGM-MLB quality fields:
    fcf    — TTM FCF / Revenue, percent
    roic   — NOPAT / Invested Capital, percent
    eps2y  — forward 2Y EPS CAGR, percent
    peg    — forward PEG, decimal
    de     — total debt / equity, decimal

Source-priority dispatch:

    1. QGM-US latest.json hard_filter_details          → source = "qgm-us"
    2. QGM-TW latest.json hard_filter_details          → source = "qgm-tw"
    3. yfinance fallback (with EU suffix mapping)      → source = "yfinance" or "yfinance-eu"

All three paths produce the same field shape per schema doc
`scripts/dd_screener_schema.md`. Any individual field may be None when the
underlying source has insufficient data.

QGM stores fields as decimals (0.448 → 44.8 percent). Yfinance helpers in
`fundamentals_us.py` also return decimals. This module multiplies-by-100
exactly once at the boundary.

EU suffix mapping is the per-universe minimum — currently AENA, BESI, RMS.
Add new entries as EU DD tickers grow. Tickers like ASML, ARM, NXPI, STM
trade with US-format tickers in yfinance and don't need a suffix.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

# Import yfinance helpers from existing fundamentals_us.py rather than
# duplicating the FCF / ROIC / EPS-CAGR logic.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "yfinance>=0.2.40", "pandas", "-q"]
    )
    import yfinance as yf
    import pandas as pd

from fundamentals_us import (  # type: ignore
    calc_fcf_margin,
    calc_roic,
    _forward_2y_cagr,
    _row,
)

ROOT = _HERE.parent
QGM_US_PATH = ROOT / "docs" / "qgm" / "latest.json"
QGM_TW_PATH = ROOT / "docs" / "qgm-tw" / "latest.json"

# Empty-field shape (used for "no data" fallback).
_EMPTY_QUALITY = {
    "fcf": None,
    "roic": None,
    "eps2y": None,
    "peg": None,
    "de": None,
}

# Universe-observed EU listings — extend as new EU DD tickers are added.
EU_SUFFIX_MAP = {
    "AENA": ".MC",   # Madrid
    "BESI": ".AS",   # Amsterdam
    "RMS":  ".PA",   # Paris (Hermès)
}


def _pct(v: Optional[float]) -> Optional[float]:
    """Decimal → percent, rounded to 2dp."""
    if v is None:
        return None
    try:
        return round(float(v) * 100.0, 2)
    except (TypeError, ValueError):
        return None


def _dec(v: Optional[float], digits: int = 2) -> Optional[float]:
    """Pass-through decimal, rounded."""
    if v is None:
        return None
    try:
        return round(float(v), digits)
    except (TypeError, ValueError):
        return None


# ===== QGM index =============================================================


def load_qgm_index() -> dict[str, tuple[str, dict]]:
    """Return {ticker: (source_tag, hard_filter_details)} merged from US + TW.

    source_tag ∈ {"qgm-us", "qgm-tw"}. Only entries with a populated
    hard_filter_details dict are indexed — entries that QGM dropped early
    (e.g. data_errors) won't be findable here, falling through to yfinance.
    """
    out: dict[str, tuple[str, dict]] = {}
    for path, tag in ((QGM_US_PATH, "qgm-us"), (QGM_TW_PATH, "qgm-tw")):
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for pool in ("candidates", "watch_list", "quality_pool"):
            for entry in data.get(pool, []) or []:
                if not isinstance(entry, dict):
                    continue
                t = entry.get("ticker")
                hfd = entry.get("hard_filter_details")
                if not t or not hfd:
                    continue
                # First-write-wins: candidates > watch_list > quality_pool
                if t not in out:
                    out[t] = (tag, hfd)
    return out


def _extract_qgm_quality(hfd: dict) -> dict:
    """Transform QGM hard_filter_details (decimals) to schema percent / decimal."""
    return {
        "fcf":   _pct(hfd.get("fcf_margin",       {}).get("value")),
        "roic":  _pct(hfd.get("roic",             {}).get("value")),
        "eps2y": _pct(hfd.get("eps_cagr_2y_fwd",  {}).get("value")),
        "peg":   _dec(hfd.get("peg",              {}).get("value"), 2),
        "de":    _dec(hfd.get("debt_to_equity",   {}).get("value"), 3),
    }


# ===== yfinance fallback =====================================================


def _yf_ticker_for(dd_ticker: str) -> str:
    """Resolve DD ticker → yfinance ticker (handle EU suffix; TW/JP pass through)."""
    # TW: "2330.TW" stays "2330.TW"
    # JP: "6857.T" stays "6857.T"
    # EU: "RMS" → "RMS.PA" via EU_SUFFIX_MAP
    if dd_ticker in EU_SUFFIX_MAP:
        return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}"
    return dd_ticker


def _yf_peg(t) -> Optional[float]:
    """Forward PEG from yfinance .info (with TTM fallback)."""
    try:
        info = t.info or {}
        peg = info.get("pegRatio") or info.get("trailingPegRatio")
        if peg is not None and float(peg) > 0:
            return float(peg)
    except Exception:
        pass
    return None


def _yf_de(t) -> Optional[float]:
    """Total Debt / Stockholders Equity from balance sheet, with .info fallback."""
    try:
        bs = t.balance_sheet
        debt = _row(bs, "Total Debt")
        equity = _row(bs, "Stockholders Equity") or _row(bs, "Total Equity")
        if debt is not None and equity and equity > 0:
            return float(debt) / float(equity)
    except Exception:
        pass
    # Fallback: yfinance .info debtToEquity is expressed as percent (e.g. 70 = 0.7)
    try:
        info = t.info or {}
        de_pct = info.get("debtToEquity")
        if de_pct is not None:
            return float(de_pct) / 100.0
    except Exception:
        pass
    return None


def compute_yfinance_quality(yf_ticker: str) -> dict:
    """Fetch all 5 quality fields from yfinance. Each field None on failure."""
    out = dict(_EMPTY_QUALITY)
    try:
        t = yf.Ticker(yf_ticker)
        try:
            info = t.info or {}
        except Exception:
            info = {}

        # FCF margin
        try:
            v = calc_fcf_margin(t, info=info)
            out["fcf"] = _pct(v)
        except Exception:
            pass

        # ROIC
        try:
            v = calc_roic(t, info=info)
            out["roic"] = _pct(v)
        except Exception:
            pass

        # 2Y EPS CAGR
        try:
            v = _forward_2y_cagr(
                t.earnings_estimate, "yearAgoEps", info.get("trailingEps")
            )
            out["eps2y"] = _pct(v)
        except Exception:
            pass

        # PEG
        out["peg"] = _dec(_yf_peg(t), 2)

        # D/E
        out["de"] = _dec(_yf_de(t), 3)

    except Exception:
        # Total failure (e.g. invalid ticker) → all-None
        pass

    return out


# ===== Public API ============================================================


def get_quality_for_ticker(
    dd_ticker: str,
    qgm_index: dict[str, tuple[str, dict]],
) -> tuple[dict, str]:
    """Resolve quality fields for one DD ticker.

    Returns:
        (quality_dict, source_tag)
        source_tag ∈ {"qgm-us", "qgm-tw", "yfinance", "yfinance-eu"}
    """
    # QGM first
    hit = qgm_index.get(dd_ticker)
    if hit is not None:
        tag, hfd = hit
        return _extract_qgm_quality(hfd), tag

    # yfinance fallback
    yf_t = _yf_ticker_for(dd_ticker)
    quality = compute_yfinance_quality(yf_t)
    src = "yfinance-eu" if dd_ticker in EU_SUFFIX_MAP else "yfinance"
    return quality, src


# ===== CLI self-test =========================================================


def main() -> None:
    """Smoke test against representative tickers from each branch."""
    idx = load_qgm_index()
    print(f"QGM index loaded: {len(idx)} entries")
    print(f"  qgm-us: {sum(1 for s,_ in idx.values() if s=='qgm-us')}")
    print(f"  qgm-tw: {sum(1 for s,_ in idx.values() if s=='qgm-tw')}")
    print()

    samples = [
        ("NVDA", "expect qgm-us"),
        ("LLY", "expect qgm-us"),
        ("2330.TW", "expect qgm-tw"),
        ("AAPL", "expect yfinance (not in QGM watch/quality pools)"),
        ("RMS", "expect yfinance-eu (RMS.PA)"),
        ("AENA", "expect yfinance-eu (AENA.MC)"),
        ("BESI", "expect yfinance-eu (BESI.AS)"),
        ("6857.T", "expect yfinance"),
        ("INVALID_TICKER_XYZ", "expect yfinance all-None"),
    ]

    for t, note in samples:
        q, src = get_quality_for_ticker(t, idx)
        print(f"  {t:20s}  [{src:11s}]  {q}   # {note}")


if __name__ == "__main__":
    main()
