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
# Use EU_SUFFIX_MAP for the common pattern "{dd_ticker}{suffix}" → yf_ticker.
EU_SUFFIX_MAP = {
    "AENA": ".MC",   # Madrid
    "BESI": ".AS",   # Amsterdam
    "RMS":  ".PA",   # Paris (Hermès)
    "SU":   ".PA",   # Paris (Schneider Electric)
}

# For cases where the yfinance ticker does NOT follow the simple suffix-append
# pattern (e.g. LVMH on Euronext Paris is "MC.PA", not "LVMH.PA"), use an
# explicit override. Checked BEFORE EU_SUFFIX_MAP in resolution helpers.
TICKER_YF_OVERRIDE = {
    "LVMH":    "MC.PA",     # Euronext Paris (primary EUR listing)
    "ABB":     "ABBNY",     # NYSE ADR (USD); ABB on its own returns 404 on yfinance
    "5274.TW": "5274.TWO",  # ASPEED — TPEx OTC, yfinance uses .TWO (not .TW)
    "8299.TW": "8299.TWO",  # Phison 群聯 — TPEx OTC, yfinance uses .TWO (not .TW)
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


# ===== Excel-coverage helpers (shared by 5 dd-screener page builders) ========


def has_excel_cagr(s: dict) -> bool:
    """Universe filter: True iff Excel-derived forward CAGR available.
    Used across all 5 dd-screener pages to enforce Excel-only growth signal —
    tickers without Excel coverage (e.g. 6146.T / 6857.T fallback to yfinance)
    are vetoed from quality-entry / bottom-out / breakout / entry-state /
    earnings-acceleration so the growth signal is consistent everywhere."""
    return (
        s.get("eps_source") == "xlsx"
        and s.get("eps_fy1_fy3_cagr_pct") is not None
    )


def cagr_growth_score(cagr_pct: Optional[float]) -> float:
    """0-1 normalized growth score from FY+1->FY+3 Excel forward CAGR %.

    Used in bottom-out / breakout pillar_floor 15% slot (replacing the old
    eps_rev_safety_score that pulled from yfinance eps_revision_pct).

    Curve: CAGR >= 25% -> 1.0; 0-25% linear; <= 0 -> 0; None -> 0.7 neutral.
    """
    if cagr_pct is None:
        return 0.7
    if cagr_pct >= 25:
        return 1.0
    if cagr_pct <= 0:
        return 0.0
    return cagr_pct / 25.0


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
    # Explicit override (e.g. "LVMH" → "MC.PA") takes precedence
    if dd_ticker in TICKER_YF_OVERRIDE:
        return TICKER_YF_OVERRIDE[dd_ticker]
    # EU: "RMS" → "RMS.PA" via EU_SUFFIX_MAP
    if dd_ticker in EU_SUFFIX_MAP:
        return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}"
    return dd_ticker


def _yf_peg(t) -> Optional[float]:
    """Forward PEG from yfinance .info (with TTM fallback).

    Fallback path: when yfinance doesn't populate pegRatio / trailingPegRatio
    (common after their 2024-2025 schema churn), compute manually as
    forwardPE / eps2y_growth_pct.  Guards:
      - Ignore when EPS 2Y CAGR > 300% (distorted recovery base, e.g. SNDK
        emerging from a near-zero-earnings trough — PEG is meaningless).
      - Ignore when computed PEG > 10 or PEG < 0.
    """
    try:
        info = t.info or {}
        peg = info.get("pegRatio") or info.get("trailingPegRatio")
        if peg is not None and float(peg) > 0:
            return float(peg)
    except Exception:
        pass
    # Manual fallback: forwardPE / eps_growth_pct
    try:
        info = t.info or {}
        fpe = info.get("forwardPE")
        if fpe is None or float(fpe) <= 0:
            return None
        cagr = _forward_2y_cagr(
            t.earnings_estimate, "yearAgoEps", info.get("trailingEps")
        )
        if cagr is None or cagr <= 0:
            return None
        # Guard: skip distorted recovery bases (CAGR > 300% means base ≈ 0)
        if cagr > 3.0:
            return None
        growth_pct = cagr * 100.0
        if growth_pct <= 0:
            return None
        computed = float(fpe) / growth_pct
        # Ignore absurd values — near-zero growth makes PEG meaningless
        if computed <= 0 or computed > 10:
            return None
        return round(computed, 2)
    except Exception:
        pass
    return None


def _yf_de(t) -> Optional[float]:
    """Total Debt / Stockholders Equity from balance sheet, with .info fallback.

    Zero-debt companies (e.g. ANET, ISRG, 6146.T) report Total Debt as NaN in
    yfinance's balance sheet — _row() returns None for NaN.  We detect this by
    checking whether the balance sheet *row exists* (NaN) vs *is absent* (no
    row).  When the row exists but is NaN and equity is positive, D/E = 0.0.

    Negative equity (e.g. FICO, DELL, SBUX — heavy buyback programs) makes D/E
    mathematically undefined and economically misleading; we return None so the
    screener shows "—" rather than a spurious negative ratio.
    """
    try:
        bs = t.balance_sheet
        debt = _row(bs, "Total Debt")
        equity = _row(bs, "Stockholders Equity") or _row(bs, "Total Equity")
        if debt is not None and equity is not None and equity > 0:
            return float(debt) / float(equity)
        # Zero-debt detection: "Total Debt" row present but NaN → debt = 0
        if debt is None and equity is not None and equity > 0:
            # Confirm the row actually exists in the balance sheet (NaN) rather
            # than being absent entirely.  _row() returns None for both cases,
            # so we check the index directly.
            if bs is not None and not bs.empty:
                has_debt_row = any(
                    "total debt" in str(r).lower() for r in bs.index
                )
                if has_debt_row:
                    # Row present but NaN → no financial debt, D/E = 0
                    return 0.0
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
    # Last-resort zero-debt detection: info.totalDebt == 0 with positive equity.
    # Covers tickers (e.g. 6146.T) where no "Total Debt" row appears in the
    # balance sheet at all — not a NaN row but genuinely absent — yet the
    # summary-level info field confirms zero financial debt.
    try:
        info = t.info or {}
        total_debt_info = info.get("totalDebt")
        if total_debt_info is not None and float(total_debt_info) == 0:
            # Verify equity is positive before returning 0.0
            try:
                bs = t.balance_sheet
                equity = _row(bs, "Stockholders Equity") or _row(bs, "Total Equity")
                if equity is not None and equity > 0:
                    return 0.0
            except Exception:
                pass
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
        source_tag ∈ {"qgm-us", "qgm-tw", "qgm-us+yf-de", "yfinance", "yfinance-eu"}

    QGM gap-fill for D/E: QGM sometimes stores debt_to_equity.value = None
    (e.g. ANET — a zero-debt company where QGM uses nd_ebitda as its gate
    metric instead).  nd_ebitda is not a D/E proxy, so when QGM D/E is None
    we fall through to a targeted yfinance D/E fetch and tag the source as
    "qgm-us+yf-de" so the blend is auditable.
    """
    # QGM first
    hit = qgm_index.get(dd_ticker)
    if hit is not None:
        tag, hfd = hit
        quality = _extract_qgm_quality(hfd)
        # Gap-fill: QGM D/E is None → try yfinance for D/E only
        if quality.get("de") is None:
            try:
                yf_t = _yf_ticker_for(dd_ticker)
                t = yf.Ticker(yf_t)
                de_val = _yf_de(t)
                if de_val is not None:
                    quality = dict(quality)
                    quality["de"] = _dec(de_val, 3)
                    tag = f"{tag}+yf-de"
            except Exception:
                pass
        return quality, tag

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
        # Gap-fill regression tests (previously missing PEG or D/E)
        ("ANET",    "QGM D/E gap: expect qgm-us+yf-de, de=0.0 (zero-debt)"),
        ("ALAB",    "yfinance PEG gap: expect manual PEG ~1.08"),
        ("FN",      "yfinance PEG gap: expect manual PEG ~1.43"),
        ("CRDO",    "yfinance PEG gap: expect manual PEG ~0.19"),
        ("VIK",     "yfinance PEG gap: expect manual PEG ~0.78"),
        ("3661.TW", "yfinance PEG gap: expect manual PEG ~0.41"),
        ("SNDK",    "yfinance PEG gap: expect None (657% CAGR = distorted recovery base)"),
        ("FICO",    "yfinance D/E gap: expect None (negative equity)"),
        ("DELL",    "yfinance D/E gap: expect None (negative equity)"),
        ("SBUX",    "yfinance D/E gap: expect None (negative equity)"),
        ("ISRG",    "yfinance D/E gap: expect 0.0 (zero-debt, Total Debt row NaN)"),
        ("6146.T",  "yfinance D/E gap: expect 0.0 (zero-debt, no debt rows)"),
    ]

    for t, note in samples:
        q, src = get_quality_for_ticker(t, idx)
        print(f"  {t:20s}  [{src:11s}]  {q}   # {note}")


if __name__ == "__main__":
    main()
