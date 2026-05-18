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

OUTPUT_DIR = ROOT / "docs" / "dd-screener"
OUTPUT_PATH = OUTPUT_DIR / "latest.json"
SCREENER_LATEST = ROOT / "docs" / "screener" / "latest.json"

# Locked v1.0 criteria — matches scripts/dd_screener_schema.md
CRITERIA = [
    {"key": "fcf",   "label": "FCF≥10%",  "threshold": 10.0, "invert": False, "unit": "%"},
    {"key": "roic",  "label": "ROIC≥15%", "threshold": 15.0, "invert": False, "unit": "%"},
    {"key": "eps2y", "label": "EPS 2Y CAGR≥15%",  "threshold": 15.0, "invert": False, "unit": "%"},
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

    try:
        raw = yf.download(
            all_yf_tickers,
            period="300d",
            interval="1d",
            group_by="ticker",
            progress=False,
            threads=True,
            auto_adjust=True,
        )
    except Exception as exc:
        print(f"  [fallback] yf.download failed: {exc}", file=sys.stderr)
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


def _compute_live_pe_drift(entry: dict, ma: dict) -> dict:
    """Compute live FwdPE estimate from price drift since DD write.

    Assumption: consensus FY+2 EPS unchanged since DD. Valid for ~30-90 days;
    for stale DDs (> 6 months), drift overstates expensiveness because EPS
    estimates typically grow over time.

    Returns dict with:
      live_fpe_est: fpe_fy2 × (price_now / price_at_dd), None if inputs missing
      pe_drift_pct: % change from DD-time fpe_fy2 (= price drift if EPS static)
      dd_age_days: days since DD write date
      live_pct_5y_est: estimated current 5Y FwdPE percentile (heuristic — assumes
                       typical 60% relative range; cyclicals will be off)
    """
    out = {
        "live_fpe_est": None,
        "pe_drift_pct": None,
        "dd_age_days": None,
        "live_pct_5y_est": None,
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

    drift_factor = p_now / p_dd
    out["live_fpe_est"] = round(fpe * drift_factor, 2)
    out["pe_drift_pct"] = round((drift_factor - 1) * 100, 1)

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


def enrich_ticker(
    entry: dict,
    qgm_index: dict,
    dca_ev_map: dict,
    dca_trend_map: dict,
    screener_timing: dict,
    timing_fallback: dict,
    skip_ma: bool,
    ma_cache: dict | None = None,
) -> dict:
    """Add quality + MA + ev5y_pct + pass_count + fail_criteria + timing to entry.

    Also overrides moat_trend with DCA Phase A1 authoritative arrow (the loader
    defaults all 98 to ↑ because dd-meta rarely carries this field; DCA does).

    `timing` joins `docs/screener/latest.json` by ticker — for tickers not in
    the screener universe (TW/JP/EU + niche US), falls back to `timing_fallback`
    computed by compute_yfinance_timing_fallback() from a yfinance batch fetch.

    v1.3: also computes live_fpe_est / pe_drift_pct / dd_age_days / live_pct_5y_est
    from price drift since DD write (unfreezes valuation columns).
    """
    t = entry["ticker"]
    quality, source = get_quality_for_ticker(t, qgm_index)
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

    pe_drift = _compute_live_pe_drift(entry, ma)

    return {
        **entry,
        **quality,
        "moat_trend": moat_trend,
        "pass_count": pass_count,
        "fail_criteria": fails,
        "quality_source": source,
        "ev5y_pct": _ev5y_for(t, dca_ev_map),
        "ma": ma,
        "ma_from_cache": ma_from_cache,
        "timing": timing,
        **pe_drift,  # live_fpe_est, pe_drift_pct, dd_age_days, live_pct_5y_est
    }


def build(top_n: int | None, skip_ma: bool, dry_run: bool, workers: int) -> dict:
    print(f"=== DD Screener build · {datetime.now().isoformat(timespec='seconds')} ===\n")
    t0 = time.time()

    # Step 0: v1.4 — load previous latest.json's MA snapshots as fallback cache
    ma_cache = load_ma_cache(OUTPUT_PATH)
    print(f"  Step 0    MA cache from prev latest.json: {len(ma_cache)} tickers")

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

    # Step 3 + 4 enrichment, parallel
    print(f"  Step 3-4  enriching (workers={workers}, skip_ma={skip_ma}) ...")
    enriched: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(enrich_ticker, e, qgm_index, dca_ev_map, dca_trend_map, screener_timing, timing_fallback, skip_ma, ma_cache): e["ticker"]
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
