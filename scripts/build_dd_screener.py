#!/usr/bin/env python3
"""DD Screener Phase 1 — stateless orchestrator.

Pipeline:
  Step 1-2  load 98 DDs + latest DCA per ticker  (dd_screener_dd_loader)
  Step 3    hybrid quality data (QGM + yfinance)  (dd_screener_quality)
  Step 4    MA snapshot                            (dd_screener_ma)
  Step 5    compute pass/fail per criterion
  Step 6    write docs/dd-screener/latest.json

Output schema: scripts/dd_screener_schema.md (locked v1.0)

Usage:
  python3 scripts/build_dd_screener.py             # full universe, ~6-8 min
  python3 scripts/build_dd_screener.py --top 10    # smoke-test first 10 tickers
  python3 scripts/build_dd_screener.py --dry-run   # don't write file
  python3 scripts/build_dd_screener.py --no-ma     # skip MA fetch (faster smoke)

Timing fallback (added 2026-05-17):
  DD tickers not in the S&P500/NQ100 screener universe (e.g. ALAB, MRVL, SPOT,
  TW/JP local listings) receive timing data from a yfinance batch fetch instead of
  docs/screener/latest.json.

  rs_score methodology for fallback tickers:
    - Fetch 300d daily closes for all missing tickers in one yf.download() call.
    - Use docs/screener/latest.json rankings as the reference population: each
      ranking entry already carries rs_1w/rs_4w/rs_13w (EMA-smoothed percentile
      scores). These are treated as the "anchored" distribution.
    - For each missing ticker compute raw r1w/r4w/r13w returns, then percentile-rank
      them against the union of (screener smoothed scores + missing ticker raw scores).
      This is an approximation (no EMA smoothing for fallback tickers) but consistent
      with the page's existing framing (all scores are relative to the same ~511-stock
      US universe).
    - TW/JP local-listings (2330.TW, etc.) are ranked against the same US universe.
      This is noisy because of JPY/TWD FX effects but chosen for consistency over a
      parallel methodology. The timing_source field is set to "yfinance_fallback" for
      all fallback tickers so the FE can surface caveats if needed.
    - Tickers that yfinance refuses to serve for any metric get timing=null for that
      metric (never raises, graceful degradation).
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
import warnings
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "pandas", "numpy", "-q"])
    import numpy as np
    import pandas as pd
    import yfinance as yf

logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("peewee").setLevel(logging.CRITICAL)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dd_screener_dd_loader import load_dd_universe  # noqa: E402
from dd_screener_quality import (  # noqa: E402
    EU_SUFFIX_MAP,
    get_quality_for_ticker,
    load_qgm_index,
)
from dd_screener_ma import compute_ma_snapshot  # noqa: E402
from update_dd_index import (  # noqa: E402
    collect_dca_ev_map,
    collect_dca_moat_trend_map,
    compute_dca_irr,
)
from load_eps_estimates_xlsx import (  # noqa: E402
    ExcelSnapshot,
    load_latest_excel,
)

OUTPUT_DIR = ROOT / "docs" / "dd-screener"
OUTPUT_PATH = OUTPUT_DIR / "latest.json"
SCREENER_LATEST = ROOT / "docs" / "screener" / "latest.json"

# Locked v1.0 criteria — matches scripts/dd_screener_schema.md
CRITERIA = [
    {"key": "fcf",   "label": "FCF≥10%",  "threshold": 10.0, "invert": False, "unit": "%"},
    {"key": "roic",  "label": "ROIC≥15%", "threshold": 15.0, "invert": False, "unit": "%"},
    {"key": "eps2y", "label": "FY+1→FY+3 CAGR≥15%",  "threshold": 15.0, "invert": False, "unit": "%"},
    {"key": "peg",   "label": "PEG≤2.0",  "threshold": 2.0,  "invert": True,  "unit": "x"},
    {"key": "de",    "label": "D/E≤0.7",  "threshold": 0.7,  "invert": True,  "unit": "x"},
]

PRESETS = {
    "MLB": {"fcf": 10.0, "roic": 15.0, "eps2y": 15.0, "peg": 2.0, "de": 0.7},
}

DEFAULT_FILTER = {"moat_min": 9.5, "directions": ["↑", "→"]}


# ---------------------------------------------------------------------------
# Step 5: pass/fail
# ---------------------------------------------------------------------------


def evaluate_criteria(quality: dict) -> tuple[int, list[str]]:
    """Return (pass_count, fail_criteria) using locked MLB thresholds.

    A null field is treated as a failed criterion (can't verify), recorded
    in fail_criteria so the front-end can show "—" rather than red.
    """
    fails: list[str] = []
    passes = 0
    for c in CRITERIA:
        v = quality.get(c["key"])
        if v is None:
            fails.append(c["key"])
            continue
        ok = (v <= c["threshold"]) if c["invert"] else (v >= c["threshold"])
        if ok:
            passes += 1
        else:
            fails.append(c["key"])
    return passes, fails


# ---------------------------------------------------------------------------
# Step 7: orchestrate
# ---------------------------------------------------------------------------


def _sort_key(s: dict) -> tuple:
    # In-tab ordering: pass_count desc → moat_score desc → 5Y IRR desc (nulls last)
    # → ticker asc. 5Y IRR is preferred over upside_mid_pct because it's
    # the directly investment-decision-relevant metric shown in the FE.
    irr = s.get("ev5y_pct")
    return (
        -s["pass_count"],
        -(s.get("moat_score") or 0),
        -(irr if irr is not None else -1e9),
        s["ticker"],
    )


def _yf_ticker_for_ma(dd_ticker: str) -> str:
    """Same suffix resolution as quality module."""
    return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}" if dd_ticker in EU_SUFFIX_MAP else dd_ticker


def _empty_ma() -> dict:
    return {
        "price": None, "w52": None, "w104": None, "w250": None,
        "slope_w250_pct": None, "drift_4w_pct": None,
        "above_w52": None, "above_w250": None,
        # v1.6: 5y cycle context for entry-state-machine (additive, all None on failure)
        "high_250w_price": None, "dist_250w_high_pct": None,
        "weeks_since_250w_high": None, "is_full_5y": None,
        "drift_4w_min_in_8w": None,
    }


def load_ma_cache(path: Path) -> dict[str, dict]:
    """v1.4: Read existing latest.json's MA snapshots so they can be reused
    when yfinance fails (rate-limit, network blip). Each cache entry carries
    `_stamp` = date of the snapshot it came from, for FE staleness display.

    Without this, a single failed yfinance batch wipes all MA data; with it,
    we degrade gracefully to last known value.
    """
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    stamp = data.get("as_of") or "unknown"
    cache: dict[str, dict] = {}
    for s in data.get("stocks", []) or []:
        t = s.get("ticker")
        ma = s.get("ma") or {}
        # Only cache rows where at least the price + w250 came through last time
        if t and ma.get("price") is not None and ma.get("w250") is not None:
            cache[t] = {**ma, "_stamp": stamp}
    return cache


_QUALITY_FIELDS = ("fcf", "roic", "eps2y", "peg", "de")


def load_quality_cache(path: Path) -> dict[str, dict]:
    """v1.5: Read existing latest.json's quality fields (fcf/roic/eps2y/peg/de)
    so they can be reused when yfinance fails for the quality fetch path.

    Mirrors load_ma_cache(). Only caches yfinance-source rows where at least
    one of the 5 fields was non-None last run (i.e. previous fetch wasn't
    itself a total wipe). QGM-sourced rows are skipped — those load from
    QGM JSON on disk and don't need cache fallback.

    To avoid recursive cache pollution after multi-day outages, we still
    cache rows previously served from cache, but propagate the original
    `_cache_stamp` instead of bumping it — so FE always shows the true
    freshness of the underlying yfinance data.
    """
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    stamp = data.get("as_of") or "unknown"
    cache: dict[str, dict] = {}
    for s in data.get("stocks", []) or []:
        t = s.get("ticker")
        if not t:
            continue
        src = s.get("quality_source") or ""
        # Only cache yfinance-path rows (QGM rows load from JSON, no need)
        if not src.startswith("yfinance"):
            continue
        quality = {k: s.get(k) for k in _QUALITY_FIELDS}
        non_null = sum(1 for v in quality.values() if v is not None)
        if non_null == 0:
            continue
        # Preserve original cache stamp if previous run was already cached
        existing_stamp = s.get("quality_cache_stamp")
        cache[t] = {
            **quality,
            "_stamp": existing_stamp or stamp,
            "_was_cached": bool(s.get("quality_from_cache")),
        }
    return cache


def load_screener_timing_map() -> dict[str, dict]:
    """Build {ticker: {dist_52w_high_pct, ma50_pct, vs_200ma_pct, rs_score,
    rs_1w, rs_4w, rs_13w, timing_source}} from `docs/screener/latest.json`.

    Also carries rs_1w/rs_4w/rs_13w so compute_yfinance_timing_fallback() can
    use the screener's EMA-smoothed sub-scores as the reference population for
    percentile-ranking the 34 DD tickers that aren't in the screener universe.

    Non-US DD tickers (TW/JP/EU) will not appear here — caller falls back to
    compute_yfinance_timing_fallback() for them.
    """
    if not SCREENER_LATEST.exists():
        print(f"  WARN: {SCREENER_LATEST} not found — timing fields will be null", file=sys.stderr)
        return {}
    try:
        data = json.loads(SCREENER_LATEST.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  WARN: failed to parse {SCREENER_LATEST}: {exc}", file=sys.stderr)
        return {}
    out: dict[str, dict] = {}
    for r in data.get("rankings", []) or []:
        t = r.get("ticker")
        if not t:
            continue
        out[t] = {
            "dist_52w_high_pct": r.get("dist_52w_high_pct"),
            "ma50_pct": r.get("ma50_pct"),
            "vs_200ma_pct": r.get("vs_200ma_pct"),
            "rs_score": r.get("rs_score"),
            # Sub-scores for RS reference population (used by fallback only)
            "rs_1w": r.get("rs_1w"),
            "rs_4w": r.get("rs_4w"),
            "rs_13w": r.get("rs_13w"),
            "timing_source": "screener",
        }
    return out


def _calc_return(closes: "pd.Series", days: int) -> float | None:
    """Return % return over last N trading days; None if insufficient history."""
    if len(closes) < days + 1:
        return None
    v = float(closes.iloc[-1])
    vn = float(closes.iloc[-(days + 1)])
    if vn == 0:
        return None
    return (v / vn - 1) * 100.0


def _percentile_rank_value(val: float, population: list[float]) -> float:
    """Percentile rank (0-100) of val within population (including val itself)."""
    if not population:
        return 50.0
    return sum(1 for x in population if x <= val) / len(population) * 100.0


def _chunked_download_with_retry(
    tickers: list[str],
    period: str = "300d",
    interval: str = "1d",
    chunk_size: int = 50,
    max_retries: int = 3,
    backoff_seconds: tuple[int, ...] = (15, 60, 180),
) -> "pd.DataFrame":
    """Batch-fetch daily OHLC for many tickers, robust to yfinance rate-limits.

    Splits the ticker list into chunks of ``chunk_size`` and downloads each
    chunk independently. If a chunk raises ``YFRateLimitError`` or returns an
    empty frame, it is retried up to ``max_retries`` times with exponential
    backoff per ``backoff_seconds``. Successful chunks are concatenated into
    a single multi-index DataFrame (columns = MultiIndex(ticker, ohlc)) that
    matches the shape of ``yf.download(group_by='ticker')``.

    Failed chunks are silently dropped — downstream callers handle missing
    tickers via ``_get_closes() returning None``. Never raises.
    """
    if not tickers:
        return pd.DataFrame()

    chunks: list[pd.DataFrame] = []
    n_chunks = (len(tickers) + chunk_size - 1) // chunk_size
    failed_tickers: list[str] = []

    for chunk_idx in range(n_chunks):
        chunk_tickers = tickers[chunk_idx * chunk_size:(chunk_idx + 1) * chunk_size]
        chunk_df: pd.DataFrame | None = None

        for attempt in range(max_retries):
            try:
                df = yf.download(
                    chunk_tickers,
                    period=period,
                    interval=interval,
                    group_by="ticker",
                    progress=False,
                    threads=True,
                    auto_adjust=True,
                )
                # Empty frame = rate-limited or all tickers invalid — retry.
                if df is None or df.empty:
                    raise RuntimeError("empty frame returned (likely rate-limited)")
                chunk_df = df
                break
            except Exception as exc:
                exc_name = type(exc).__name__
                if attempt < max_retries - 1:
                    delay = backoff_seconds[min(attempt, len(backoff_seconds) - 1)]
                    print(
                        f"  [chunked] chunk {chunk_idx + 1}/{n_chunks} "
                        f"attempt {attempt + 1}/{max_retries} failed "
                        f"({exc_name}); sleeping {delay}s ...",
                        file=sys.stderr,
                    )
                    time.sleep(delay)
                else:
                    print(
                        f"  [chunked] chunk {chunk_idx + 1}/{n_chunks} "
                        f"exhausted {max_retries} retries ({exc_name}); "
                        f"dropping {len(chunk_tickers)} tickers",
                        file=sys.stderr,
                    )
                    failed_tickers.extend(chunk_tickers)

        if chunk_df is not None:
            chunks.append(chunk_df)
            # Small inter-chunk delay to be gentle on yfinance even on success.
            if chunk_idx < n_chunks - 1:
                time.sleep(2)

    if not chunks:
        print(f"  [chunked] all {n_chunks} chunks failed", file=sys.stderr)
        return pd.DataFrame()

    # Concat along columns axis; pandas will align ticker MultiIndex correctly.
    try:
        combined = pd.concat(chunks, axis=1)
    except Exception as exc:
        print(f"  [chunked] concat failed: {exc}", file=sys.stderr)
        return pd.DataFrame()

    succeeded = len(tickers) - len(failed_tickers)
    print(
        f"  [chunked] Done: {succeeded}/{len(tickers)} tickers fetched "
        f"across {n_chunks} chunks (chunk_size={chunk_size})",
        file=sys.stderr,
    )
    return combined


def compute_yfinance_timing_fallback(
    missing_tickers: list[str],
    screener_data: dict[str, dict],
) -> dict[str, dict]:
    """Batch-fetch timing fields for DD tickers not in the screener universe.

    For dist_52w_high_pct / ma50_pct / vs_200ma_pct: computed directly from
    ~300d daily closes via yfinance.

    For rs_score: each missing ticker's r1w/r4w/r13w **raw % returns** are
    percentile-ranked against **raw % returns** from the full screener universe
    (~511 tickers), fetched via yfinance in the same batch.  This is
    methodologically correct — apples-to-apples raw vs raw — unlike the
    previous approach that mixed raw returns against screener's already-EMA-
    smoothed percentile-rank values (0-100 range vs -50/+50 range).

    No EMA smoothing is applied to fallback tickers (no prior history).
    Fallback tickers get timing_source="yfinance_fallback".

    TW/JP local listings are ranked against the same US universe by design
    (consistent methodology; FX noise documented in module docstring).

    Never raises — returns empty dict for tickers that yfinance fails on.
    """
    if not missing_tickers:
        return {}

    # Resolve yfinance tickers (EU suffix mapping) for missing DD tickers
    yf_map: dict[str, str] = {}  # dd_ticker -> yf_ticker
    for t in missing_tickers:
        yf_map[t] = _yf_ticker_for_ma(t)

    # Build full universe: screener tickers + missing DD tickers
    screener_tickers: list[str] = list(screener_data.keys())
    all_yf_tickers = list(set(list(yf_map.values()) + screener_tickers))
    print(
        f"  [fallback] Fetching {len(all_yf_tickers)} tickers "
        f"({len(screener_tickers)} screener universe + {len(yf_map)} missing) ...",
        file=sys.stderr,
    )

    # Chunked download with retry/backoff (added 2026-05-24).
    # Yahoo Finance tightened rate-limits in 2024-2025; a single batch of
    # 500+ tickers reliably trips YFRateLimitError, wiping the entire
    # timing column. Chunks of 50 with exponential backoff make the build
    # resilient without re-runs.
    raw = _chunked_download_with_retry(
        all_yf_tickers,
        period="300d",
        interval="1d",
        chunk_size=50,
        max_retries=3,
        backoff_seconds=(15, 60, 180),
    )
    if raw is None or raw.empty:
        print(f"  [fallback] yf.download returned empty after retries", file=sys.stderr)
        return {}

    # Helper: extract Close series for a yf ticker from the multi-ticker frame.
    # Captures `raw` (the yfinance DataFrame) and `all_yf_tickers` from enclosing scope.
    # IMPORTANT: never use `raw` as a local variable name in this function's outer
    # scope after this point — it would shadow the DataFrame for this closure.
    def _get_closes(yf_ticker: str) -> "pd.Series | None":
        try:
            if len(all_yf_tickers) == 1:
                # Single-ticker download returns flat columns
                closes = raw["Close"].dropna()
            else:
                # Multi-ticker: top level is ticker name
                closes = raw[yf_ticker]["Close"].dropna()
            if closes.empty:
                return None
            return closes
        except (KeyError, TypeError):
            return None

    # Compute raw returns for the full screener universe to use as reference population.
    # These are raw % returns (apples-to-apples with missing tickers' raw returns).
    ref_r1w: list[float] = []
    ref_r4w: list[float] = []
    ref_r13w: list[float] = []
    for sc_t in screener_tickers:
        closes = _get_closes(sc_t)
        if closes is None:
            continue
        v1 = _calc_return(closes, 5)
        v4 = _calc_return(closes, 21)
        v13 = _calc_return(closes, 63)
        if v1 is not None and v4 is not None and v13 is not None:
            ref_r1w.append(v1)
            ref_r4w.append(v4)
            ref_r13w.append(v13)
    print(
        f"  [fallback] Reference population: {len(ref_r1w)} tickers with full raw returns",
        file=sys.stderr,
    )

    # Compute raw returns for missing tickers
    missing_raw: dict[str, dict] = {}  # dd_ticker -> {r1w, r4w, r13w}
    for dd_t, yf_t in yf_map.items():
        closes = _get_closes(yf_t)
        if closes is None:
            continue
        r1w = _calc_return(closes, 5)
        r4w = _calc_return(closes, 21)
        r13w = _calc_return(closes, 63)
        if r1w is not None and r4w is not None and r13w is not None:
            missing_raw[dd_t] = {"r1w": r1w, "r4w": r4w, "r13w": r13w}

    # Combined reference population: screener universe raw returns + missing tickers' raw returns.
    # Both sides are now raw % returns — methodologically correct.
    all_r1w = ref_r1w + [v["r1w"] for v in missing_raw.values()]
    all_r4w = ref_r4w + [v["r4w"] for v in missing_raw.values()]
    all_r13w = ref_r13w + [v["r13w"] for v in missing_raw.values()]

    # Build output
    out: dict[str, dict] = {}
    for dd_t, yf_t in yf_map.items():
        closes = _get_closes(yf_t)
        timing: dict = {
            "dist_52w_high_pct": None,
            "ma50_pct": None,
            "vs_200ma_pct": None,
            "rs_score": None,
            "timing_source": "yfinance_fallback",
        }

        if closes is not None and len(closes) > 1:
            price = float(closes.iloc[-1])

            # dist_52w_high_pct: last close vs trailing 252-day max
            window = min(252, len(closes))
            high_52w = float(closes.iloc[-window:].max())
            if high_52w > 0:
                timing["dist_52w_high_pct"] = round((price / high_52w - 1) * 100, 1)

            # ma50_pct: last close vs 50-day SMA
            if len(closes) >= 50:
                ma50 = float(closes.iloc[-50:].mean())
                if ma50 > 0:
                    timing["ma50_pct"] = round((price / ma50 - 1) * 100, 1)

            # vs_200ma_pct: last close vs 200-day SMA
            if len(closes) >= 200:
                ma200 = float(closes.iloc[-200:].mean())
                if ma200 > 0:
                    timing["vs_200ma_pct"] = round((price / ma200 - 1) * 100, 1)

        # rs_score via percentile rank against combined population
        if dd_t in missing_raw and all_r1w:
            _raw_ret = missing_raw[dd_t]  # renamed to avoid shadowing outer `raw` DataFrame
            pr1w = _percentile_rank_value(_raw_ret["r1w"], all_r1w)
            pr4w = _percentile_rank_value(_raw_ret["r4w"], all_r4w)
            pr13w = _percentile_rank_value(_raw_ret["r13w"], all_r13w)
            # Persistence formula matches screener.py (no EMA — no prior history)
            persistence = pr1w * 0.2 + pr4w * 0.3 + pr13w * 0.5
            # Trend bonus (matches screener.py logic)
            if pr1w > pr4w > pr13w:
                bonus = 5.0
            elif pr1w >= pr4w >= pr13w:
                bonus = 2.0
            elif pr1w < pr4w < pr13w:
                bonus = -5.0
            else:
                bonus = 0.0
            timing["rs_score"] = round(min(100.0, persistence + bonus), 1)

        out[dd_t] = timing

    succeeded = sum(1 for v in out.values() if v.get("dist_52w_high_pct") is not None)
    print(f"  [fallback] Done: {succeeded}/{len(missing_tickers)} tickers got dist_52w_high_pct", file=sys.stderr)
    return out


def _ev5y_for(ticker: str, dca_ev_map: dict) -> float | None:
    """Resolve DCA §4 5Y EV → annualized IRR (%) for one ticker.

    `dca_ev_map` keys are filename-normalized (no dots, e.g. "2330TW"), so
    "2330.TW" must fall back to the dot-stripped form.
    """
    ev = dca_ev_map.get(ticker)
    if ev is None:
        ev = dca_ev_map.get(ticker.replace(".", ""))
    if ev is None:
        return None
    return round(compute_dca_irr(ev), 2)


def _moat_trend_for(ticker: str, dca_trend_map: dict, fallback: str) -> str:
    """Resolve moat trend arrow per DCA Phase A1; fallback when no DCA arrow.

    `dca_trend_map` keys are normalized (no dots, e.g. "2330TW").
    """
    arrow = dca_trend_map.get(ticker)
    if arrow is None:
        arrow = dca_trend_map.get(ticker.replace(".", ""))
    return arrow or fallback


def _fetch_live_fy_eps(
    yf_ticker: str,
    p_at_dd: float,
    fpe_fy2: float,
    excel_record: dict | None = None,
    dd_ticker: str | None = None,
) -> dict:
    """v1.7.1: fetch fresh FY EPS estimate from yfinance, auto-match the FY
    row that the DD anchored on, AND return raw 0y/+1y values + trailingEps
    for proper 2Y CAGR computation.

    v1.8: when `excel_record` is provided (Excel row for this ticker),
    override eps_0y_raw / eps_1y_raw with Excel values. yearAgoEps + trailingEps
    still come from yfinance (historical actual). FY-match (eps_now) is
    recomputed against Excel values. Adds Excel-only fields eps_fy3 +
    growth_fy1_fy2_pct + growth_fy2_fy3_pct + cagr_fy1_fy3_pct.

    DD label "FY+1" vs "FY+2" semantics vary by writer (some count from last
    fiscal year-end, some from current ongoing FY). Instead of guessing, we
    reverse-engineer the implied EPS at DD time (price_at_dd / fpe_fy2) and
    pick whichever yfinance annual row (0y / +1y) is closest. This works
    per-ticker without needing labels.

    2Y CAGR caveat (v1.7.2 fix): yfinance's "0y" and "+1y" rows are 1 year
    apart (current FY vs next FY). The proper 2Y CAGR end is +1y, but the
    base must be on the **same accounting basis** as the estimate (non-GAAP
    for SaaS analysts). info.trailingEps is GAAP TTM — for high-SBC names
    (DDOG, NET, CRWD, MDB, SNOW…) GAAP TTM ≪ non-GAAP forward, which inflates
    the CAGR by 5-10×. We now prefer earnings_estimate's "0y" yearAgoEps
    (last FY actual, same non-GAAP basis as the +1y estimate) and fall back
    to trailingEps only when yearAgoEps is missing.

    Returns dict with:
      live_fpe_real:    price_now / yf_eps_matched (None on failure)
      yf_fy_label:      "0y" | "+1y" — which yfinance row was matched
      eps_at_dd:        DD-implied EPS (price_at_dd / fpe_fy2)
      eps_now:          fresh consensus EPS for matched FY
      eps_revision_pct: (eps_now - eps_at_dd) / eps_at_dd × 100
      eps_0y_raw:       raw 0y avg EPS (current FY estimate) — kept for audit
      eps_1y_raw:       raw +1y avg EPS (next FY estimate) — used as CAGR end
      eps_year_ago:     0y.yearAgoEps (last FY actual, same basis as estimate)
      trailing_eps:     info.trailingEps — GAAP TTM fallback CAGR base
    """
    out = {
        "live_fpe_real": None,
        "yf_fy_label": None,
        "eps_at_dd": None,
        "eps_now": None,
        "eps_revision_pct": None,
        # v1.7: raw values for 2Y CAGR computation (independent of DD match)
        "eps_0y_raw": None,
        "eps_1y_raw": None,
        # v1.7.2: yearAgoEps — same-basis CAGR base (preferred over GAAP TTM)
        "eps_year_ago": None,
        # v1.7.1: trailing EPS — GAAP TTM fallback when yearAgoEps missing
        "trailing_eps": None,
        # v1.8: Excel-derived fields (None when no Excel record for ticker)
        "eps_fy3": None,
        "growth_fy1_fy2_pct": None,
        "growth_fy2_fy3_pct": None,
        "cagr_fy1_fy3_pct": None,
        "eps_source": "yfinance",
        # v1.8.2: True when Excel covers ticker AND yfinance.info.currency !=
        # info.financialCurrency (e.g., TSM ADR USD vs TWD-reported earnings).
        # When True, _compute_live_eps_cagr() switches eps2y_live to use Excel's
        # own forward CAGR (cagr_fy1_fy3_pct) to avoid FX-ratio nonsense.
        "currency_mismatch_xlsx_yf": False,
        # v1.8.5: foreign-listing native-currency display. For .TW/.T/.HK/.KS
        # tickers, Excel reports in USD but local investors think in TWD/JPY/etc.
        # We back-compute an implicit FX from yfinance (financialCurrency) ÷ Excel
        # (USD) for the same FY, then surface local-currency values for display.
        # ADRs (TSM/ASML/LVMH ADR forms) are NOT converted — ADR holders trade USD.
        "eps_display_currency": "USD",
        "eps_fx_rate": None,
        "eps_fy_curr_local": None,
        "eps_fy_next_local": None,
        "eps_fy3_local": None,
        "eps_fy_curr_usd_orig": None,  # original Excel USD value (audit)
        "eps_fy_next_usd_orig": None,
        "eps_fy3_usd_orig": None,
    }
    if not (p_at_dd and fpe_fy2 and p_at_dd > 0 and fpe_fy2 > 0):
        return out
    implied = p_at_dd / fpe_fy2
    out["eps_at_dd"] = round(implied, 4)

    # v1.8: Excel takes priority for FY1/FY2/FY3 + growth fields.
    # yearAgoEps + trailingEps still come from yfinance (historical actuals).
    if excel_record is not None:
        out["eps_source"] = "xlsx"
        out["eps_0y_raw"] = excel_record.get("fy1")
        out["eps_1y_raw"] = excel_record.get("fy2")
        out["eps_fy3"] = excel_record.get("fy3")
        out["growth_fy1_fy2_pct"] = excel_record.get("growth_fy1_fy2_pct")
        out["growth_fy2_fy3_pct"] = excel_record.get("growth_fy2_fy3_pct")
        out["cagr_fy1_fy3_pct"] = excel_record.get("cagr_fy1_fy3_pct")

    # v1.8.1: ALWAYS fetch yfinance 0y/+1y into local vars (independent of Excel
    # override). Used for:
    #   (1) FY-match → eps_now → eps_revision_pct (vs DD-time anchor) — kept on
    #       yfinance baseline for backward compat with v1.7.x (consistent input
    #       to breakout / bottom-out scoring; avoids Excel-vs-yfinance consensus
    #       mean drift falsely showing as "EPS revision").
    #   (2) yearAgoEps (historical actual) — never overridden by Excel.
    #   Excel still overrides eps_0y_raw / eps_1y_raw / eps_fy3 / growth fields
    #   in `out` for DISPLAY purposes only.
    yf_eps_0y = None
    yf_eps_1y = None
    yf_eps_2y = None
    try:
        tk = yf.Ticker(yf_ticker)
        ee = tk.earnings_estimate
        if ee is None or getattr(ee, "empty", True):
            ee = None

        if ee is not None:
            # Always read yfinance 0y / +1y / +2y avg into a dict (audit baseline,
            # never overridden by Excel — used for FY-match below)
            _yf = {"0y": None, "+1y": None, "+2y": None}
            for row_label in _yf:
                try:
                    if row_label in ee.index:
                        val = ee.loc[row_label].get("avg")
                        if val is not None and float(val) > 0:
                            _yf[row_label] = round(float(val), 4)
                except Exception:
                    pass
            yf_eps_0y = _yf["0y"]
            yf_eps_1y = _yf["+1y"]
            yf_eps_2y = _yf["+2y"]

            # Populate display fields: Excel overrides win for eps_0y_raw / eps_1y_raw / eps_fy3
            if out["eps_source"] != "xlsx":
                # yfinance fallback path: copy yfinance locals into display fields
                out["eps_0y_raw"] = yf_eps_0y
                out["eps_1y_raw"] = yf_eps_1y
                if out["eps_fy3"] is None:
                    out["eps_fy3"] = yf_eps_2y
                # Compute growth/CAGR for yfinance-sourced rows
                _fy1 = out["eps_0y_raw"]
                _fy2 = out["eps_1y_raw"]
                _fy3 = out["eps_fy3"]
                if _fy1 and _fy2 and _fy1 > 0:
                    out["growth_fy1_fy2_pct"] = round((_fy2 / _fy1 - 1) * 100, 4)
                if _fy2 and _fy3 and _fy2 > 0:
                    out["growth_fy2_fy3_pct"] = round((_fy3 / _fy2 - 1) * 100, 4)
                if _fy1 and _fy3 and _fy1 > 0 and _fy3 > 0:
                    out["cagr_fy1_fy3_pct"] = round(((_fy3 / _fy1) ** 0.5 - 1) * 100, 4)
            # else: Excel already wrote eps_0y_raw / eps_1y_raw / eps_fy3 + growth/CAGR

            # yearAgoEps (always from yfinance — historical actual, never Excel)
            try:
                if "0y" in ee.index:
                    yag = ee.loc["0y"].get("yearAgoEps")
                    if yag is not None and float(yag) > 0:
                        out["eps_year_ago"] = round(float(yag), 4)
            except Exception:
                pass

        # trailingEps fallback (always yfinance) +
        # v1.8.3: for Excel-covered tickers, probe info.financialCurrency to
        # detect currency mismatch. Excel is *always* in USD (Koyfin export
        # convention), so any ticker whose yfinance financialCurrency ≠ USD
        # has its yearAgoEps in a foreign currency — dividing Excel USD by
        # foreign yearAgo gives FX-ratio nonsense. Covers BOTH:
        #   (a) ADRs where info.currency=USD but financialCurrency=EUR/TWD/CHF
        #       (TSM, ASML, ONON, SPOT)
        #   (b) Foreign local listings where both = TWD/JPY but Excel = USD
        #       (2330.TW, 2454.TW, 2308.TW, etc.)
        # Cost: ~134 extra info calls per build (cached client-side).
        need_info = (
            (out["eps_1y_raw"] is not None and out["eps_year_ago"] is None)
            or excel_record is not None
        )
        if need_info:
            try:
                info = tk.info
                trailing = info.get("trailingEps")
                if trailing is not None and float(trailing) > 0:
                    out["trailing_eps"] = round(float(trailing), 4)
                if excel_record is not None:
                    fc = info.get("financialCurrency")
                    if fc and fc.upper() != "USD":
                        out["currency_mismatch_xlsx_yf"] = True
            except Exception:
                pass

        # v1.8.1: FY-match against yfinance values (NOT Excel) so eps_revision_pct
        # remains apples-to-apples vs DD-time anchor (which was reverse-engineered
        # from frozen price_at_dd / fpe_fy2 — typically anchored on yfinance-era
        # consensus). Mixing Excel (Koyfin-source) consensus with yfinance-anchored
        # DD value introduces ~1-4pp systematic bias that misleads breakout /
        # bottom-out scoring (real-world: 5 ticker demoted out of breakout tier_a).
        best = None
        candidates = [("0y", yf_eps_0y), ("+1y", yf_eps_1y)]
        for row_label, eps in candidates:
            if eps and eps > 0:
                err = abs(eps - implied) / implied
                if best is None or err < best[1]:
                    best = (row_label, err, float(eps))
        if best is None:
            return out
        if best[1] > 0.30:
            return out
        out["yf_fy_label"] = best[0]
        out["eps_now"] = round(best[2], 4)
        out["eps_revision_pct"] = round((best[2] - implied) / implied * 100, 1)
    except Exception:
        pass

    # v1.8.5: foreign-listing native-currency conversion.
    # For .TW/.T/.HK/.KS/.SS/.SZ tickers: Excel reports USD per ord share but
    # local investors think in TWD/JPY/HKD/KRW/etc. Back-compute implicit FX
    # using yfinance native value (in financialCurrency) vs Excel USD value
    # for the same FY (typically FY+1, the "0y" row). Then convert FY1/FY2/FY3.
    # ADRs (no foreign suffix on DD ticker) are skipped — USD is the natural unit.
    _FOREIGN_SUFFIXES_DISPLAY = (".TW", ".T", ".HK", ".KS", ".KQ", ".SS", ".SZ", ".JP")
    if (
        excel_record is not None
        and dd_ticker
        and any(dd_ticker.endswith(s) for s in _FOREIGN_SUFFIXES_DISPLAY)
    ):
        # FX = yfinance native (financialCurrency) ÷ Excel USD, for "0y" FY
        # Prefer yf_eps_0y / excel.fy1; fall back to yf_eps_1y / excel.fy2 if 0y unavailable.
        xlsx_usd_fy1 = excel_record.get("fy1")
        xlsx_usd_fy2 = excel_record.get("fy2")
        xlsx_usd_fy3 = excel_record.get("fy3")
        fx = None
        if yf_eps_0y and xlsx_usd_fy1 and xlsx_usd_fy1 > 0:
            fx = yf_eps_0y / xlsx_usd_fy1
        elif yf_eps_1y and xlsx_usd_fy2 and xlsx_usd_fy2 > 0:
            fx = yf_eps_1y / xlsx_usd_fy2
        if fx and fx > 0:
            # Try to read financialCurrency from yfinance info (typically already
            # fetched above for currency_mismatch detection; this is best-effort).
            local_ccy = None
            try:
                local_ccy = yf.Ticker(yf_ticker).info.get("financialCurrency")
            except Exception:
                pass
            if not local_ccy:
                # Suffix-based default (covers most cases without an extra API call)
                local_ccy = {
                    ".TW": "TWD", ".T": "JPY", ".JP": "JPY",
                    ".HK": "HKD", ".KS": "KRW", ".KQ": "KRW",
                    ".SS": "CNY", ".SZ": "CNY",
                }.get(next(s for s in _FOREIGN_SUFFIXES_DISPLAY if dd_ticker.endswith(s)), "USD")
            out["eps_display_currency"] = local_ccy
            out["eps_fx_rate"] = round(float(fx), 4)
            # Stash USD originals (audit) before overwriting display fields
            out["eps_fy_curr_usd_orig"] = xlsx_usd_fy1
            out["eps_fy_next_usd_orig"] = xlsx_usd_fy2
            out["eps_fy3_usd_orig"] = xlsx_usd_fy3
            # Compute local-currency values
            if xlsx_usd_fy1 is not None:
                out["eps_fy_curr_local"] = round(xlsx_usd_fy1 * fx, 2)
            if xlsx_usd_fy2 is not None:
                out["eps_fy_next_local"] = round(xlsx_usd_fy2 * fx, 2)
            if xlsx_usd_fy3 is not None:
                out["eps_fy3_local"] = round(xlsx_usd_fy3 * fx, 2)
            # OVERWRITE display fields with local-currency values so downstream
            # (latest.json + UI) consistently shows TWD/JPY/etc. for foreign listings.
            # Growth/CAGR percentages are currency-agnostic — leave unchanged.
            if out["eps_fy_curr_local"] is not None:
                out["eps_0y_raw"] = out["eps_fy_curr_local"]
            if out["eps_fy_next_local"] is not None:
                out["eps_1y_raw"] = out["eps_fy_next_local"]
            if out["eps_fy3_local"] is not None:
                out["eps_fy3"] = out["eps_fy3_local"]

    return out


def _compute_live_pe_drift(
    entry: dict, ma: dict, live_fy_result: dict | None = None
) -> dict:
    """Compute live FwdPE — preferring fresh yfinance EPS over price-drift heuristic.

    Primary path (v1.6): live_fpe_real = price_now / yfinance FY EPS estimate
      Captures both price drift AND analyst EPS revisions since DD. Auto-matches
      the right FY row by implied EPS (DD writers use FY+1 vs FY+2 differently).

    Fallback path (v1.3): live_fpe_heur = fpe_fy2 × (price_now / price_at_dd)
      Assumes EPS unchanged since DD. Used when yfinance has no earnings_estimate
      or the match is off (BESI etc).

    v1.7: accepts optional pre-fetched `live_fy_result` to avoid duplicate
    yfinance calls when enrich_ticker also needs eps_0y_raw / eps_1y_raw.
    If not provided, calls _fetch_live_fy_eps() internally (backward-compat).

    Returns dict with:
      live_fpe_est: live FwdPE (real if matched, heuristic otherwise), None if inputs missing
      pe_drift_pct: % change from DD-time fpe_fy2 (combines price drift + EPS revision when method=eps)
      dd_age_days: days since DD write date
      live_pct_5y_est: heuristic current 5Y FwdPE percentile (60% relative range)
      live_fpe_method: "eps" (real path) | "drift" (heuristic) | None
      eps_revision_pct: % change in FY EPS estimate since DD (only when method=eps)
      yf_fy_label: "0y" | "+1y" — which yfinance row was matched (only when method=eps)
    """
    out = {
        "live_fpe_est": None,
        "pe_drift_pct": None,
        "dd_age_days": None,
        "live_pct_5y_est": None,
        "live_fpe_method": None,
        "eps_revision_pct": None,
        "yf_fy_label": None,
    }
    fpe = entry.get("fpe_fy2")
    p_dd = entry.get("price_at_dd")
    p_now = ma.get("price") if ma else None
    pct_5y = entry.get("pct_5y")
    dd_date = entry.get("dd_date")

    if dd_date:
        try:
            d = datetime.strptime(dd_date, "%Y-%m-%d").date()
            out["dd_age_days"] = (datetime.now().date() - d).days
        except (TypeError, ValueError):
            pass

    if fpe is None or p_dd is None or p_now is None or p_dd <= 0 or fpe <= 0:
        return out

    # Primary: real EPS path — use pre-fetched result if provided (v1.7 no-dupe)
    real = live_fy_result if live_fy_result is not None else _fetch_live_fy_eps(
        _yf_ticker_for_ma(entry["ticker"]), p_dd, fpe
    )
    if real["eps_now"] is not None and real["eps_now"] > 0:
        out["live_fpe_est"] = round(p_now / real["eps_now"], 2)
        out["pe_drift_pct"] = round((out["live_fpe_est"] / fpe - 1) * 100, 1)
        out["live_fpe_method"] = "eps"
        out["eps_revision_pct"] = real["eps_revision_pct"]
        out["yf_fy_label"] = real["yf_fy_label"]
    else:
        # Fallback: price-drift heuristic
        drift_factor = p_now / p_dd
        out["live_fpe_est"] = round(fpe * drift_factor, 2)
        out["pe_drift_pct"] = round((drift_factor - 1) * 100, 1)
        out["live_fpe_method"] = "drift"

    # Heuristic live pct_5y: assume the 5Y FwdPE range has relative width ~60%
    # centered on fpe_dd, so [low, high] = [fpe·(1−0.6·pct/100), fpe·(1+0.6·(1−pct/100))].
    # Then live_pct_5y = (live_fpe − low) / (high − low) × 100, clamped [0, 100].
    # Caveat: cyclicals / high-growth stocks have much wider ranges.
    if pct_5y is not None and 0 <= pct_5y <= 100:
        REL_WIDTH = 0.6
        low = fpe * (1 - REL_WIDTH * pct_5y / 100)
        high = fpe * (1 + REL_WIDTH * (100 - pct_5y) / 100)
        if high > low:
            live_pct = (out["live_fpe_est"] - low) / (high - low) * 100
            out["live_pct_5y_est"] = round(max(0, min(100, live_pct)), 1)
    return out


# ---------------------------------------------------------------------------
# EPS 2Y CAGR live compute helpers (v1.7 — EPS revision momentum)
# ---------------------------------------------------------------------------

def _compute_live_eps_cagr(entry: dict, live_fy_result: dict) -> dict:
    """Compute live 2Y EPS CAGR from yfinance earnings_estimate.

    v1.7.2 fix: prior trailingEps-based formula mixed GAAP TTM (denominator)
    with non-GAAP forward estimate (numerator) for high-SBC SaaS names,
    inflating CAGR 5-10× (DDOG observed at 170% vs DD 17.8%). Now prefers
    0y.yearAgoEps — the last FY actual on the same accounting basis as the
    analysts' forward estimate — and falls back to trailingEps only when
    yearAgoEps is missing.

    Formula:
      base = eps_year_ago (preferred) or trailing_eps (fallback)
      cagr = ((eps_+1y / base) ** 0.5 - 1) * 100

    v1.8.2 fix: for Excel-covered ADRs whose ADR currency differs from yfinance
    financialCurrency (TSM USD vs TWD, ASML/SPOT USD vs EUR, ONON USD vs CHF),
    dividing Excel FY+1 (USD) by yfinance yearAgoEps (foreign currency) gives
    FX-ratio nonsense (TSM observed −39.8% vs Excel forward CAGR +25%). When
    `currency_mismatch_xlsx_yf` flag is set upstream, switch to Excel's own
    `cagr_fy1_fy3_pct` (FY+1 → FY+3 forward 2Y CAGR — currency-safe).

    Writes:
      eps2y_live:         live 2Y EPS CAGR % (None on failure)
      eps2y_live_method:  "yearago" (yearAgoEps + +1y, same-basis, preferred)
                          | "xlsx_forward" (Excel FY+1→FY+3 — ADR currency-mismatch path)
                          | "trailing" (trailingEps + +1y, GAAP/non-GAAP risk)
                          | "missing"
    """
    eps_1y = live_fy_result.get("eps_1y_raw")
    year_ago = live_fy_result.get("eps_year_ago")
    trailing = live_fy_result.get("trailing_eps")
    currency_mismatch = live_fy_result.get("currency_mismatch_xlsx_yf", False)
    xlsx_forward_cagr = live_fy_result.get("cagr_fy1_fy3_pct")

    # v1.8.2: ADR currency-mismatch path — use Excel's own forward CAGR
    if currency_mismatch and xlsx_forward_cagr is not None:
        return {
            "eps2y_live": round(float(xlsx_forward_cagr), 2),
            "eps2y_live_method": "xlsx_forward",
        }

    if eps_1y is not None and year_ago is not None and year_ago > 0:
        cagr = ((eps_1y / year_ago) ** 0.5 - 1) * 100
        return {
            "eps2y_live": round(cagr, 2),
            "eps2y_live_method": "yearago",
        }
    if eps_1y is not None and trailing is not None and trailing > 0:
        cagr = ((eps_1y / trailing) ** 0.5 - 1) * 100
        return {
            "eps2y_live": round(cagr, 2),
            "eps2y_live_method": "trailing",
        }
    # v1.8.4: last-resort — Excel covers the ticker but yfinance returned no
    # earnings_estimate / info (e.g., LVMH ticker not in yfinance; LVMUY would
    # be). With no yearAgoEps available we can't compute the anchored CAGR,
    # but Excel's own forward CAGR is still currency-safe and usable.
    if xlsx_forward_cagr is not None:
        return {
            "eps2y_live": round(float(xlsx_forward_cagr), 2),
            "eps2y_live_method": "xlsx_forward",
        }
    return {
        "eps2y_live": None,
        "eps2y_live_method": "missing",
    }


# Module-level cache: avoid re-reading snapshot file on every per-ticker call.
_PREV_MONTH_SNAPSHOT_CACHE: dict = {}
_PREV_MONTH_SNAPSHOT_LOADED: bool = False


def _load_prev_month_snapshot() -> dict:
    """Load the previous month's EPS snapshot (with 60-day grace period).

    Running on 2026-06-15 → looks for 2026-05.json first, then 2026-04.json.
    Returns the full snapshot dict (with "tickers" key), or {} if not found.
    Cached at module level so subsequent per-ticker calls don't re-read disk.
    """
    global _PREV_MONTH_SNAPSHOT_CACHE, _PREV_MONTH_SNAPSHOT_LOADED
    if _PREV_MONTH_SNAPSHOT_LOADED:
        return _PREV_MONTH_SNAPSHOT_CACHE

    _PREV_MONTH_SNAPSHOT_LOADED = True
    snapshot_dir = ROOT / "docs" / "dd-screener" / "eps-estimates-snapshots"

    now = datetime.now(timezone(timedelta(hours=8)))  # Taipei TZ
    for months_back in (1, 2):
        # Compute YYYY-MM for (now - N months)
        m = now.month - months_back
        y = now.year
        while m <= 0:
            m += 12
            y -= 1
        candidate = snapshot_dir / f"{y:04d}-{m:02d}.json"
        if candidate.exists():
            try:
                data = json.loads(candidate.read_text(encoding="utf-8"))
                _PREV_MONTH_SNAPSHOT_CACHE = data
                return _PREV_MONTH_SNAPSHOT_CACHE
            except Exception as exc:
                print(f"  WARN: failed to load EPS snapshot {candidate}: {exc}", file=sys.stderr)

    _PREV_MONTH_SNAPSHOT_CACHE = {}
    return _PREV_MONTH_SNAPSHOT_CACHE


def _compute_eps_revision(entry: dict, eps2y_live: float | None, prev_snapshot: dict) -> dict:
    """Compute EPS revision momentum vs last month's snapshot.

    revision_dir:
      "新增"  — ticker not in last month's snapshot (new to universe or snapshot missing)
      "持平"  — |revision_pp| < 0.5pp
      "上修"  — revision_pp > 0
      "下修"  — revision_pp < 0

    Writes:
      eps2y_prev_month:      last month's eps_cagr_2y value (float or None)
      eps2y_prev_month_date: month key string e.g. "2026-05" (or None)
      eps2y_revision_pp:     eps2y_live - eps2y_prev_month (float or None)
      eps2y_revision_dir:    "新增" | "持平" | "上修" | "下修" | None
    """
    ticker = entry.get("ticker")
    out = {
        "eps2y_prev_month": None,
        "eps2y_prev_month_date": None,
        "eps2y_revision_pp": None,
        "eps2y_revision_dir": None,
    }

    if eps2y_live is None:
        # Can't compute revision without live value
        return out

    if not prev_snapshot:
        # No snapshot at all — can't classify
        return out

    for_month = prev_snapshot.get("for_month")
    prev_tickers = prev_snapshot.get("tickers") or {}
    prev_row = prev_tickers.get(ticker)

    if prev_row is None:
        out["eps2y_revision_dir"] = "新增"
        out["eps2y_prev_month_date"] = for_month
        return out

    prev_cagr = prev_row.get("eps_cagr_2y")
    out["eps2y_prev_month_date"] = for_month

    if prev_cagr is None:
        out["eps2y_revision_dir"] = "新增"
        return out

    out["eps2y_prev_month"] = prev_cagr
    pp = eps2y_live - prev_cagr
    out["eps2y_revision_pp"] = round(pp, 2)

    if abs(pp) < 0.5:
        out["eps2y_revision_dir"] = "持平"
    elif pp > 0:
        out["eps2y_revision_dir"] = "上修"
    else:
        out["eps2y_revision_dir"] = "下修"

    return out


def _compute_live_peg(pe_drift: dict, eps2y_live: float | None) -> dict:
    """Derive live PEG from live_fpe_est / eps2y_live.

    pe_drift: the dict returned by _compute_live_pe_drift() (contains live_fpe_est).

    Writes:
      live_peg: live PEG ratio (None if either input is missing or ≤ 0)
    """
    fpe = pe_drift.get("live_fpe_est")
    if fpe and eps2y_live and fpe > 0 and eps2y_live > 0:
        return {"live_peg": round(fpe / eps2y_live, 2)}
    return {"live_peg": None}


def _compute_live_ev5y(entry: dict, ma: dict) -> dict:
    """Heuristic live 5Y IRR, adjusting for price drift since DD.

    Formula (heuristic — terminal value assumed unchanged):
      live_ev5y = ((1 + ev5y_pct/100) * (price_at_dd / price_now) ** (1/5) - 1) * 100

    This approximates: if price rose but terminal value (EV at year 5) stayed
    the same, the annualized IRR from current price is lower.

    Writes:
      live_ev5y_pct:    adjusted 5Y annualized IRR % (None if inputs missing)
      live_ev5y_method: "heur" (always; indicates heuristic, not re-modelled)
    """
    ev5y = entry.get("ev5y_pct")
    p_dd = entry.get("price_at_dd")
    p_now = ma.get("price") if ma else None

    if ev5y is not None and p_dd and p_now and p_dd > 0 and p_now > 0:
        adj = ((1 + ev5y / 100) * (p_dd / p_now) ** 0.2 - 1) * 100
        return {
            "live_ev5y_pct": round(adj, 2),
            "live_ev5y_method": "heur",
        }
    return {
        "live_ev5y_pct": None,
        "live_ev5y_method": None,
    }


def _compute_fy_eps_revision(ticker: str, eps_curr: float | None,
                              eps_next: float | None, prev_snapshot: dict) -> dict:
    """Compute month-over-month FY1 / FY2 EPS revision % vs previous Excel snapshot.

    Returns dict with eps_fy_curr_revision_pct, eps_fy_next_revision_pct,
    eps_revision_baseline_date. Values None when previous snapshot is missing or
    ticker wasn't in last month's snapshot (new addition).
    """
    out = {
        "eps_fy_curr_revision_pct": None,
        "eps_fy_next_revision_pct": None,
        "eps_revision_baseline_date": None,
    }
    if not prev_snapshot:
        return out
    prev_tickers = prev_snapshot.get("tickers") or {}
    prev_row = prev_tickers.get(ticker)
    out["eps_revision_baseline_date"] = (
        prev_snapshot.get("snapshot_date") or prev_snapshot.get("for_month")
    )
    if prev_row is None:
        return out
    prev_curr = prev_row.get("eps_fy_curr") or prev_row.get("eps_0y")
    prev_next = prev_row.get("eps_fy_next") or prev_row.get("eps_1y")
    if eps_curr and prev_curr and prev_curr > 0:
        out["eps_fy_curr_revision_pct"] = round((eps_curr / prev_curr - 1) * 100, 2)
    if eps_next and prev_next and prev_next > 0:
        out["eps_fy_next_revision_pct"] = round((eps_next / prev_next - 1) * 100, 2)
    return out


def enrich_ticker(
    entry: dict,
    qgm_index: dict,
    dca_ev_map: dict,
    dca_trend_map: dict,
    screener_timing: dict,
    timing_fallback: dict,
    skip_ma: bool,
    ma_cache: dict | None = None,
    quality_cache: dict | None = None,
    prev_snapshot: dict | None = None,
    excel_snapshot: ExcelSnapshot | None = None,
) -> dict:
    """Add quality + MA + ev5y_pct + pass_count + fail_criteria + timing to entry.

    Also overrides moat_trend with DCA Phase A1 authoritative arrow (the loader
    defaults all 98 to ↑ because dd-meta rarely carries this field; DCA does).

    `timing` joins `docs/screener/latest.json` by ticker — for tickers not in
    the screener universe (TW/JP/EU + niche US), falls back to `timing_fallback`
    computed by compute_yfinance_timing_fallback() from a yfinance batch fetch.

    v1.3: also computes live_fpe_est / pe_drift_pct / dd_age_days / live_pct_5y_est
    from price drift since DD write (unfreezes valuation columns).

    v1.5: when yfinance returns all-None quality (rate-limit) for a yfinance-
    source ticker, fall back to previous latest.json's cached values + tag
    quality_from_cache=True + carry quality_cache_stamp. QGM rows never touch
    the cache (they load from JSON on disk). Sister to MA cache fallback (v1.4).

    v1.7: fetches _fetch_live_fy_eps() once per ticker and shares result with
    both _compute_live_pe_drift() and _compute_live_eps_cagr() to avoid a
    duplicate yfinance call. Also computes EPS revision momentum vs prev_snapshot
    (monthly snapshot), live_peg, and live_ev5y_pct.
    """
    t = entry["ticker"]
    quality, source = get_quality_for_ticker(t, qgm_index)

    # v1.5: quality cache fallback for yfinance-path rows on total-wipe outages.
    # Only triggers when ALL 5 fields are None AND source is yfinance (QGM rows
    # come from local JSON, no outage signature). Per-field substitution
    # preserves any partial fresh data when only some fields fail.
    quality_from_cache = False
    quality_cache_stamp = None
    if source.startswith("yfinance") and quality_cache and t in quality_cache:
        non_null_fresh = sum(1 for v in quality.values() if v is not None)
        if non_null_fresh == 0:
            cached = quality_cache[t]
            for k in _QUALITY_FIELDS:
                v = cached.get(k)
                if v is not None:
                    quality[k] = v
            quality_from_cache = True
            quality_cache_stamp = cached.get("_stamp")

    # v1.9: Override `eps2y` with Excel forward CAGR (eps_fy1_fy3_cagr_pct) BEFORE
    # evaluate_criteria, so the QGM "EPS 2Y CAGR ≥ 15%" rule (now labelled
    # "FY+1→FY+3 CAGR ≥ 15%") anchors on Excel buy-side pure forward consensus
    # instead of yfinance YearAgo→FY+1 mixed window.
    _excel_record_for_eps2y = excel_snapshot.get(t) if excel_snapshot else None
    if _excel_record_for_eps2y is not None:
        _excel_cagr = _excel_record_for_eps2y.get("cagr_fy1_fy3_pct")
        if _excel_cagr is not None:
            quality["eps2y"] = round(float(_excel_cagr), 2)

    pass_count, fails = evaluate_criteria(quality)

    if skip_ma:
        ma = _empty_ma()
        ma_from_cache = False
    else:
        try:
            ma = compute_ma_snapshot(_yf_ticker_for_ma(t))
        except Exception:
            ma = _empty_ma()
        # v1.4: 若 yfinance 抓不到（rate-limit / 網路 hiccup）就用上次 latest.json
        # 的 cached MA — 比顯示空白好，且 FE 可以 surface staleness via ma._stamp
        ma_from_cache = False
        if ma.get("price") is None and ma_cache and t in ma_cache:
            cached = ma_cache[t]
            ma = {k: v for k, v in cached.items() if k != "_stamp"}
            ma["_cache_stamp"] = cached.get("_stamp")
            ma_from_cache = True

    # Override the loader's "↑" default with DCA Phase A1 arrow; "→" when DCA
    # has none (conservative — don't assume strengthening without evidence).
    moat_trend = _moat_trend_for(t, dca_trend_map, fallback="→")

    # Timing: prefer screener (EMA-smoothed, consistent); fall back to yfinance
    # batch for tickers not in the screener universe.
    timing = screener_timing.get(t)
    if timing is None:
        timing = timing_fallback.get(t)  # may still be None if yfinance failed

    # Strip internal sub-score fields from timing dict before storing — they
    # are only needed for RS reference population computation, not for the FE.
    if timing is not None:
        timing = {k: v for k, v in timing.items()
                  if k not in ("rs_1w", "rs_4w", "rs_13w")}

    # v1.7: fetch yfinance EPS once; share with both PE drift + 2Y CAGR helpers.
    # Guard: requires fpe_fy2 + price_at_dd (needed to match the right FY row).
    # p_now is NOT required here — CAGR only needs eps_0y/eps_1y, not current price.
    # PE drift will still degrade gracefully when p_now is None.
    # v1.8: pass excel_record so Excel overrides FY1/FY2/FY3 when ticker is covered.
    fpe = entry.get("fpe_fy2")
    p_dd = entry.get("price_at_dd")
    p_now = ma.get("price") if ma else None
    excel_record = excel_snapshot.get(t) if excel_snapshot else None
    live_fy_result: dict | None = None
    if fpe and p_dd and fpe > 0 and p_dd > 0:
        live_fy_result = _fetch_live_fy_eps(
            _yf_ticker_for_ma(t), p_dd, fpe,
            excel_record=excel_record, dd_ticker=t,
        )
    elif excel_record is not None:
        # No DD anchor — still surface Excel FY1/FY2/FY3 (no eps_now / revision)
        live_fy_result = {
            "live_fpe_real": None, "yf_fy_label": None,
            "eps_at_dd": None, "eps_now": None, "eps_revision_pct": None,
            "eps_0y_raw": excel_record.get("fy1"),
            "eps_1y_raw": excel_record.get("fy2"),
            "eps_year_ago": None,
            "trailing_eps": None,
            "eps_fy3": excel_record.get("fy3"),
            "growth_fy1_fy2_pct": excel_record.get("growth_fy1_fy2_pct"),
            "growth_fy2_fy3_pct": excel_record.get("growth_fy2_fy3_pct"),
            "cagr_fy1_fy3_pct": excel_record.get("cagr_fy1_fy3_pct"),
            "eps_source": "xlsx",
        }

    pe_drift = _compute_live_pe_drift(entry, ma, live_fy_result=live_fy_result)

    # v1.7: EPS 2Y CAGR live + revision momentum
    eps2y_live_result = _compute_live_eps_cagr(entry, live_fy_result or {})
    eps2y_live = eps2y_live_result.get("eps2y_live")

    # v1.9: revision MoM diff anchors on Excel forward CAGR (eps_fy1_fy3_cagr_pct)
    # instead of yfinance-derived eps2y_live, so the UI's ↑↓pp delta reflects
    # buy-side consensus shift rather than yfinance YearAgo→FY+1 window noise.
    excel_cagr_for_rev = (live_fy_result or {}).get("cagr_fy1_fy3_pct")
    eps_revision = _compute_eps_revision(entry, excel_cagr_for_rev, prev_snapshot or {})
    live_peg = _compute_live_peg(pe_drift, eps2y_live)  # needs live_fpe_est from pe_drift

    # Compute ev5y_pct before passing to live_ev5y helper (entry doesn't carry it yet)
    ev5y_pct = _ev5y_for(t, dca_ev_map)
    # Build a minimal context dict for _compute_live_ev5y (needs ev5y_pct + price_at_dd)
    ev5y_entry = {**entry, "ev5y_pct": ev5y_pct}
    live_ev5y = _compute_live_ev5y(ev5y_entry, ma)

    # v1.7.2: surface raw EPS estimates so the FE can show per-FY EPS columns
    # (current FY / next FY consensus + TTM EPS used as CAGR base).
    _lfy = live_fy_result or {}

    # v1.8: per-FY EPS revision vs previous month's Excel snapshot
    eps_curr_val = _lfy.get("eps_0y_raw")
    eps_next_val = _lfy.get("eps_1y_raw")
    fy_revision = _compute_fy_eps_revision(t, eps_curr_val, eps_next_val, prev_snapshot or {})

    return {
        **entry,
        **quality,
        "moat_trend": moat_trend,
        "pass_count": pass_count,
        "fail_criteria": fails,
        "quality_source": source,
        "quality_from_cache": quality_from_cache,
        "quality_cache_stamp": quality_cache_stamp,
        "ev5y_pct": ev5y_pct,
        "ma": ma,
        "ma_from_cache": ma_from_cache,
        "timing": timing,
        **pe_drift,         # live_fpe_est, pe_drift_pct, dd_age_days, live_pct_5y_est
        **eps2y_live_result,  # eps2y_live, eps2y_live_method
        **eps_revision,     # eps2y_prev_month, eps2y_prev_month_date, eps2y_revision_pp, eps2y_revision_dir
        **live_peg,         # live_peg
        **live_ev5y,        # live_ev5y_pct, live_ev5y_method
        # v1.7.2: raw yfinance EPS estimates (current FY / next FY / TTM)
        "eps_fy_curr": eps_curr_val,
        "eps_fy_next": eps_next_val,
        "eps_trailing": _lfy.get("trailing_eps"),
        # v1.8: Excel-derived FY3 + growth/CAGR columns + provenance
        "eps_fy3": _lfy.get("eps_fy3"),
        "eps_fy3_yoy_pct": _lfy.get("growth_fy2_fy3_pct"),
        "eps_fy1_fy3_cagr_pct": _lfy.get("cagr_fy1_fy3_pct"),
        "eps_source": _lfy.get("eps_source", "yfinance"),
        # v1.8: month-over-month revision per FY (vs prev Excel snapshot)
        **fy_revision,  # eps_fy_curr_revision_pct, eps_fy_next_revision_pct, eps_revision_baseline_date
        # v1.8.5: foreign-listing native-currency display (TWD/JPY/etc.)
        "eps_display_currency": _lfy.get("eps_display_currency", "USD"),
        "eps_fx_rate": _lfy.get("eps_fx_rate"),
        "eps_fy_curr_usd_orig": _lfy.get("eps_fy_curr_usd_orig"),
        "eps_fy_next_usd_orig": _lfy.get("eps_fy_next_usd_orig"),
        "eps_fy3_usd_orig": _lfy.get("eps_fy3_usd_orig"),
    }


def build(top_n: int | None, skip_ma: bool, dry_run: bool, workers: int) -> dict:
    print(f"=== DD Screener build · {datetime.now().isoformat(timespec='seconds')} ===\n")
    t0 = time.time()

    # Step 0: v1.4 — load previous latest.json's MA snapshots as fallback cache
    ma_cache = load_ma_cache(OUTPUT_PATH)
    print(f"  Step 0    MA cache from prev latest.json: {len(ma_cache)} tickers")

    # Step 0b: v1.5 — load previous latest.json's quality fields as fallback
    # cache for yfinance-source rows (sister to MA cache, same rate-limit cause)
    quality_cache = load_quality_cache(OUTPUT_PATH)
    print(f"  Step 0    quality cache from prev latest.json: {len(quality_cache)} yfinance tickers")

    # Step 1-2
    universe = load_dd_universe()
    if top_n:
        universe = universe[:top_n]
    print(f"  Step 1-2  DD universe: {len(universe)} tickers")

    # Step 3 prep
    qgm_index = load_qgm_index()
    print(f"  Step 3    QGM index: {len(qgm_index)} entries ({sum(1 for s,_ in qgm_index.values() if s=='qgm-us')} US, {sum(1 for s,_ in qgm_index.values() if s=='qgm-tw')} TW)")

    # DCA §4 EV map → 5Y annualized IRR per ticker (96/98 typical coverage)
    dca_ev_map = collect_dca_ev_map()
    print(f"  Step 3    DCA EV map: {len(dca_ev_map)} tickers (for 5Y IRR column)")

    # DCA Phase A1 moat trend arrows (94/98 typical coverage; dd-meta rarely carries this)
    dca_trend_map = collect_dca_moat_trend_map()
    print(f"  Step 3    DCA moat-trend map: {len(dca_trend_map)} tickers")

    # Screener daily-cron timing snapshot — same source as flow/ath-hunter.html.
    # US tickers join here; TW/JP/EU stay null (screener is US-only).
    screener_timing = load_screener_timing_map()
    print(f"  Step 3    screener timing map: {len(screener_timing)} tickers (for 起漲點 detection)")

    # Identify DD tickers missing from the screener universe and compute their
    # timing fields via a yfinance batch fetch (fallback path).
    all_dd_tickers = [e["ticker"] for e in universe]
    missing_from_screener = [t for t in all_dd_tickers if t not in screener_timing]
    print(f"  Step 3    timing fallback needed: {len(missing_from_screener)} tickers not in screener universe")
    timing_fallback: dict[str, dict] = {}
    if missing_from_screener:
        timing_fallback = compute_yfinance_timing_fallback(missing_from_screener, screener_timing)
        fb_ok = sum(1 for v in timing_fallback.values() if v.get("dist_52w_high_pct") is not None)
        print(f"  Step 3    timing fallback: {fb_ok}/{len(missing_from_screener)} tickers backfilled")

    # Step 0c: v1.7 — load previous month's EPS snapshot for revision momentum.
    # Module-level cache (_PREV_MONTH_SNAPSHOT_CACHE) prevents re-read per ticker.
    prev_snapshot = _load_prev_month_snapshot()
    has_prev = bool(prev_snapshot.get("tickers"))
    if has_prev:
        print(f"  Step 0    EPS prev-month snapshot: {prev_snapshot.get('for_month')} "
              f"({prev_snapshot.get('xlsx_covered', prev_snapshot.get('succeeded', '?'))}"
              f"/{prev_snapshot.get('universe_size', '?')} tickers)")
    else:
        print("  Step 0    EPS prev-month snapshot: not found (revision_dir=新增 for all)")

    # Step 0d: v1.8 — load EPS estimates Excel (primary EPS source)
    excel_snapshot = load_latest_excel()
    if excel_snapshot is not None:
        all_dd_tk = [e["ticker"] for e in universe]
        us_adr = {t for t in all_dd_tk if "." not in t}
        # v1.8.3: use alias-aware lookup so 2330.TW resolves to Excel '2330'
        covered = sorted(t for t in all_dd_tk if excel_snapshot.has(t))
        missing_us = sorted(t for t in us_adr if not excel_snapshot.has(t))
        fallback_yf = sorted(t for t in all_dd_tk if not excel_snapshot.has(t))
        print(f"  Step 0    Excel EPS source: {excel_snapshot.source_file} "
              f"(snapshot {excel_snapshot.snapshot_date}, covers {len(covered)}/{len(all_dd_tk)})")
        if missing_us:
            print(f"  Step 0    Excel missing US/ADR ({len(missing_us)}): {', '.join(missing_us)}")
    else:
        print("  Step 0    Excel EPS source: NOT FOUND in data/eps-estimates/ — all tickers fall back to yfinance")
        missing_us = []
        fallback_yf = [e["ticker"] for e in universe]

    # Step 3 + 4 enrichment, parallel
    print(f"  Step 3-4  enriching (workers={workers}, skip_ma={skip_ma}) ...")
    enriched: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(enrich_ticker, e, qgm_index, dca_ev_map, dca_trend_map, screener_timing, timing_fallback, skip_ma, ma_cache, quality_cache, prev_snapshot, excel_snapshot): e["ticker"]
            for e in universe
        }
        for i, fut in enumerate(as_completed(futs), 1):
            t = futs[fut]
            try:
                row = fut.result()
                enriched.append(row)
            except Exception as exc:
                print(f"    ERR {t}: {exc}", file=sys.stderr)
            if i % 10 == 0 or i == len(futs):
                elapsed = time.time() - t0
                print(f"    [{i:>3}/{len(futs)}] {elapsed:.0f}s")

    # Step 5: sort (pass/fail already computed above)
    enriched.sort(key=_sort_key)

    # Source-tag breakdown
    src_counts = Counter(s["quality_source"] for s in enriched)
    print(f"  Step 5    quality sources: {dict(src_counts)}")
    ma_fresh = sum(1 for s in enriched if (s.get("ma") or {}).get("price") is not None and not s.get("ma_from_cache"))
    ma_cached = sum(1 for s in enriched if s.get("ma_from_cache"))
    ma_missing = len(enriched) - ma_fresh - ma_cached
    print(f"  Step 5    MA snapshot: fresh={ma_fresh} cached={ma_cached} missing={ma_missing}")
    yf_rows = [s for s in enriched if (s.get("quality_source") or "").startswith("yfinance")]
    q_cached = sum(1 for s in yf_rows if s.get("quality_from_cache"))
    q_wipe = sum(1 for s in yf_rows if all(s.get(k) is None for k in _QUALITY_FIELDS))
    q_fresh = len(yf_rows) - q_cached - q_wipe
    print(f"  Step 5    quality (yfinance path): fresh={q_fresh} cached={q_cached} wiped={q_wipe} (of {len(yf_rows)})")
    print(f"  Step 5    pass distribution: pass5={sum(1 for s in enriched if s['pass_count']==5)} "
          f"pass4={sum(1 for s in enriched if s['pass_count']==4)} "
          f"pass3={sum(1 for s in enriched if s['pass_count']==3)}")

    # Summary
    pass_counts = Counter(s["pass_count"] for s in enriched)
    no_data = sum(
        1 for s in enriched
        if all(s.get(c["key"]) is None for c in CRITERIA)
    )
    summary = {
        "pass_5":  pass_counts.get(5, 0),
        "pass_4":  pass_counts.get(4, 0),
        "pass_3":  pass_counts.get(3, 0),
        "pass_lt3": sum(v for k, v in pass_counts.items() if k < 3),
        "no_data": no_data,
    }

    # Build final document
    tz_taipei = timezone(timedelta(hours=8))
    now = datetime.now(tz_taipei)
    doc = {
        "schema_version": "1.2",
        "run_timestamp": now.isoformat(timespec="seconds"),
        "as_of": now.strftime("%Y-%m-%d"),
        "universe_size": len(enriched),
        "default_preset": "MLB",
        "criteria": CRITERIA,
        "presets": PRESETS,
        "default_filter": DEFAULT_FILTER,
        "summary": summary,
        "stocks": enriched,
    }
    # v1.8: surface Excel provenance + diff for the FE banner
    if excel_snapshot is not None:
        doc["eps_estimates_source"] = {
            "snapshot_date": excel_snapshot.snapshot_date,
            "source_file": excel_snapshot.source_file,
            "coverage_count": len([t for t in (e["ticker"] for e in universe)
                                    if excel_snapshot.has(t)]),
            "missing_us_adr_tickers": missing_us,
            "fallback_yfinance_tickers": fallback_yf,
        }
    else:
        doc["eps_estimates_source"] = {
            "snapshot_date": None,
            "source_file": None,
            "coverage_count": 0,
            "missing_us_adr_tickers": [],
            "fallback_yfinance_tickers": fallback_yf,
        }

    print(f"\n  ✓ Elapsed: {time.time()-t0:.0f}s")

    if dry_run:
        print(f"  (dry-run) skipping write to {OUTPUT_PATH}")
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Wrote {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size:,} bytes)")

    return doc


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top", type=int, default=None, help="Limit to first N tickers (smoke test)")
    p.add_argument("--no-ma", action="store_true", help="Skip MA fetch (faster smoke)")
    p.add_argument("--dry-run", action="store_true", help="Don't write latest.json")
    p.add_argument("--workers", type=int, default=8, help="Concurrent yfinance fetchers (default 8)")
    args = p.parse_args()
    build(top_n=args.top, skip_ma=args.no_ma, dry_run=args.dry_run, workers=args.workers)


if __name__ == "__main__":
    main()
