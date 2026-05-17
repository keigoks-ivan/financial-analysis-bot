#!/usr/bin/env python3
"""DD Alpha Ranker — six-method ranking + group-based consensus over DD universe.

Pipeline (per TASK §dd_alpha_ranker):
  1. Load universe from docs/dd-screener/latest.json (already enriched with
     ev5y_pct + ma + timing — including yfinance fallback for non-US).
  2. Augment with stress + quality_score from each DD's dd-meta JSON.
  3. Daily momentum layer: re-overlay `timing` from docs/screener/latest.json
     for US tickers; yfinance fallback for non-US tickers absent in screener.
  4. Weekly jensen layer: yfinance batch fetch 5Y weekly closes for universe + SPY.
  5. Fundamental layer (event-hooked on update_dd_index.py success): reads
     dd-meta + ev5y for angles 1/3/4 — no yfinance call needed.
  6. Each layer writes its own state file; render_html merges all 3.

Six ranking angles:
  Angle 1 — 多因子 Composite (return_valuation group)
             0.30·MM(moat_score) + 0.45·MM(EV5Y)
           + 0.10·MM(quality_score) + 0.15·MM(1/fpe_fy2)
  Angle 2 — EV×起漲點 timing breakout (momentum group)
             EV5Y≥12 ∩ dist_52w_high_pct∈[-7,0] ∩ ma50_pct∈[0,5] ∩ rs_score≥80
  Angle 3 — GARP (return_valuation group)
             EV5Y ÷ fpe_fy2   (per 修正 1, no PEG double-count)
  Angle 4 — 護城河複利 (quality group)
             moat_num × stress_pass_rate × val_num
  Angle 5 — RS 動能 (momentum group)
             rs_score (US: screener; non-US: 13W return percentile)
  Angle 6 — Jensen's Alpha (return_valuation group, HISTORICAL_REALIZED)
             OLS regress 5Y weekly returns on SPY → α × 52 (annualized %)

Consensus (per 修正 3):
  品質類 = {4} ; 報酬估值類 = {1,3,6} ; 動能類 = {2,5}
  Tier 1 (重倉候選) = ticker crosses 3 groups
  Tier 2 (衛星候選) = ticker crosses 2 groups

Usage:
  python3 scripts/dd_alpha_ranker.py --layers all
  python3 scripts/dd_alpha_ranker.py --layers fundamental
  python3 scripts/dd_alpha_ranker.py --layers momentum
  python3 scripts/dd_alpha_ranker.py --layers jensen
  python3 scripts/dd_alpha_ranker.py --layers fundamental momentum --no-snapshot
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable, Optional

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

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dd_meta_reader import iter_dd_metas  # noqa: E402

DD_DIR = ROOT / "docs" / "dd"
DD_SCREENER_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
SCREENER_LATEST = ROOT / "docs" / "screener" / "latest.json"
OUTPUT_DIR = ROOT / "docs" / "dd-screener"
HTML_OUT = OUTPUT_DIR / "alpha-rank.html"
JSON_OUT = OUTPUT_DIR / "alpha-rank.json"
STATE_DIR = OUTPUT_DIR / "alpha-rank-state"
SNAPSHOT_DIR = OUTPUT_DIR / "alpha-rank-snapshots"

# ── constants ─────────────────────────────────────────────────────────────────
TAIPEI_TZ = timezone(timedelta(hours=8))
SCHEMA_VERSION = "1.0"
TOP_N = 5

# Sanity gates (per §v1 必做 A + 修正 8)
EV5Y_MIN = -99.0      # 修正 8: IRR formula explodes at -100
EV5Y_MAX = 1000.0
PEG_MIN = 0.1
PEG_MAX = 10.0
FPE_MIN = 0.0         # exclusive (≤0 = loss-making)
FPE_MAX = 200.0
QUALITY_MIN, QUALITY_MAX = 1, 10
MOAT_SCORE_MIN, MOAT_SCORE_MAX = 1, 10

# Angle 2 filter thresholds (per TASK)
A2_EV5Y_MIN = 12.0
A2_DIST_52W = (-7.0, 0.0)
A2_MA50 = (0.0, 5.0)
A2_RS_MIN = 80.0

# Angle 1 composite weights
COMPOSITE_WEIGHTS = {
    "moat": 0.30,
    "growth_ev5y": 0.45,
    "quality_score": 0.10,
    "fwdpe_inv": 0.15,
}

# Angle 6 Jensen window thresholds (two-stage, per FIX 修正 1)
# <104 weeks → n/a (sample too small, post-IPO/spinoff spike not yet mean-reverted)
# 104-250 weeks → compute α, mark short_history=true
# ≥250 weeks → full 5Y window
JENSEN_MIN_WEEKS_NA = 104
JENSEN_MIN_WEEKS_FULL = 250

# Non-US → US ADR alias map. Used only by angle 5 (RS) + angle 6 (Jensen α)
# where same-benchmark cross-comparability matters more than listing purity.
# Angles 1/3/4 keep the original listing's fundamentals (moat / EV5Y / PEG /
# FwdPE are currency-independent — ADR adds FX + premium noise without
# improving signal). Other non-US without an ADR alias remain N/A in angle 6.
NON_US_TO_US_ADR: dict[str, str] = {
    "2330.TW": "TSM",
}

# Moat grade → numeric (for angle 4)
MOAT_GRADE_NUM = {"S": 5, "A": 4, "B": 3, "C": 2, "X": 1}
# Val emoji → numeric (for angle 4)
VAL_NUM = {"🟢": 1.0, "🟡": 0.6, "🟠": 0.3, "🔴": 0.0}

# Consensus groups (per 修正 3)
GROUPS = {
    "quality": ["angle_4"],
    "return_valuation": ["angle_1", "angle_3", "angle_6"],
    "momentum": ["angle_2", "angle_5"],
}

# Angle labels (used in HTML + JSON)
ANGLE_META = {
    "angle_1": {"name": "多因子 Composite", "type": "forward", "group": "return_valuation"},
    "angle_2": {"name": "EV×起漲點",        "type": "forward", "group": "momentum"},
    "angle_3": {"name": "GARP (EV5Y÷FwdPE)", "type": "forward", "group": "return_valuation"},
    "angle_4": {"name": "護城河複利",        "type": "forward", "group": "quality"},
    "angle_5": {"name": "RS 動能",          "type": "forward", "group": "momentum"},
    "angle_6": {"name": "Jensen's Alpha",   "type": "historical_realized", "group": "return_valuation"},
}

LAYER_ANGLES = {
    "fundamental": ["angle_1", "angle_3", "angle_4"],
    "momentum":    ["angle_2", "angle_5"],
    "jensen":      ["angle_6"],
}


# ── helpers ───────────────────────────────────────────────────────────────────

def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def _today() -> str:
    return datetime.now(TAIPEI_TZ).strftime("%Y-%m-%d")


def _ticker_key_no_dots(ticker: str) -> str:
    """Match the convention in DCA filenames + screener rankings (dots stripped)."""
    return ticker.replace(".", "")


def _safe_float(x) -> Optional[float]:
    try:
        f = float(x)
        if np.isnan(f) or np.isinf(f):
            return None
        return f
    except (TypeError, ValueError):
        return None


def _gate(value: Optional[float], lo: float, hi: float, *, strict_lo: bool = False) -> Optional[float]:
    """Return value if within (lo, hi]/[lo, hi], else None."""
    if value is None:
        return None
    if strict_lo:
        if value <= lo or value > hi:
            return None
    else:
        if value < lo or value > hi:
            return None
    return value


def _min_max_normalize(values: dict[str, Optional[float]]) -> dict[str, Optional[float]]:
    """Return {key: normalized in [0,1] or None for missing}. None inputs stay None."""
    vals = [v for v in values.values() if v is not None]
    if not vals:
        return {k: None for k in values}
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {k: (0.5 if v is not None else None) for k, v in values.items()}
    return {k: (None if v is None else (v - lo) / (hi - lo)) for k, v in values.items()}


# ── input loaders ─────────────────────────────────────────────────────────────

def load_universe() -> list[dict]:
    """Read docs/dd-screener/latest.json (pre-enriched with ev5y/ma/timing).

    Falls back to a fresh run via build_dd_screener if file missing (not done in
    this script — error out instead per 修正 7 spirit: never half-data).
    """
    if not DD_SCREENER_LATEST.exists():
        print(f"ERROR: {DD_SCREENER_LATEST} missing — run build_dd_screener.py first",
              file=sys.stderr)
        sys.exit(2)
    with DD_SCREENER_LATEST.open("r", encoding="utf-8") as f:
        doc = json.load(f)
    stocks = doc.get("stocks", [])
    if not stocks:
        print("ERROR: dd-screener latest.json has no stocks[]", file=sys.stderr)
        sys.exit(2)
    return stocks


def load_dd_meta_extras() -> dict[str, dict]:
    """Return {ticker: {stress_pass, stress_total, quality_score}} for every DD."""
    out: dict[str, dict] = {}
    latest_by_ticker: dict[str, tuple[str, dict]] = {}
    for _path, meta in iter_dd_metas(DD_DIR):
        t = meta.get("ticker")
        d = meta.get("date")
        if not t or not d:
            continue
        prev = latest_by_ticker.get(t)
        if prev is None or d > prev[0]:
            latest_by_ticker[t] = (d, meta)
    for ticker, (_d, meta) in latest_by_ticker.items():
        stress = meta.get("stress") or {}
        s_pass = stress.get("pass") if isinstance(stress, dict) else None
        s_total = stress.get("total") if isinstance(stress, dict) else None
        quality = meta.get("quality_score")
        out[ticker] = {
            "stress_pass": s_pass,
            "stress_total": s_total,
            "quality_score": quality,
        }
    return out


def load_screener_timing() -> dict[str, dict]:
    """Read docs/screener/latest.json → {ticker: {rs_score, dist_52w_high_pct, ma50_pct}}."""
    if not SCREENER_LATEST.exists():
        return {}
    with SCREENER_LATEST.open("r", encoding="utf-8") as f:
        doc = json.load(f)
    out: dict[str, dict] = {}
    for r in doc.get("rankings", []):
        t = r.get("ticker")
        if not t:
            continue
        out[t] = {
            "rs_score": _safe_float(r.get("rs_score")),
            "dist_52w_high_pct": _safe_float(r.get("dist_52w_high_pct")),
            "ma50_pct": _safe_float(r.get("ma50_pct")),
        }
    return out


def _yf_fetch_one_weekly(ticker: str, period: str = "5y") -> Optional[pd.Series]:
    """Single-ticker yfinance fetch with 2 retries. Returns weekly close Series or None."""
    last_err = None
    for attempt in range(3):
        try:
            df = yf.Ticker(ticker).history(period=period, interval="1wk")
            if df is None or df.empty or "Close" not in df.columns:
                return None
            s = df["Close"].dropna()
            return s if len(s) > 0 else None
        except Exception as e:  # noqa: BLE001
            last_err = e
            continue
    print(f"WARN yfinance failed for {ticker} after 3 attempts: {last_err}",
          file=sys.stderr)
    return None


def fetch_weekly_closes(tickers: Iterable[str], *, max_workers: int = 8,
                        period: str = "5y") -> dict[str, pd.Series]:
    """Parallel yfinance fetch. Returns {ticker: Series} only for successful pulls.

    Failures are logged but do not raise (per 修正 6).
    """
    tickers = list(tickers)
    results: dict[str, pd.Series] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_yf_fetch_one_weekly, t, period): t for t in tickers}
        for fut in as_completed(futures):
            t = futures[fut]
            try:
                s = fut.result()
            except Exception:  # noqa: BLE001
                s = None
            if s is not None:
                results[t] = s
    return results


# ── sanity gates (§v1 必做 A + 修正 8) ───────────────────────────────────────

def sanitize_row(row: dict, dd_extras: dict) -> dict:
    """Add sanitized numeric fields. Out-of-range values become None.

    Returns a flat dict with keys:
        ticker, name, sector, signal, trap, val, moat_grade, moat_score,
        moat_num, val_num, moat_trend,
        ev5y, peg, fpe, quality_score, stress_pass_rate,
        rs_score, dist_52w_high_pct, ma50_pct,
        ma_state (emoji string for display),
        dd_path, dca_path, weekly_returns (None at this stage)
    """
    ticker = row["ticker"]
    moat_grade = str(row.get("moat_grade") or "").upper()
    val_glyph = row.get("val") or ""

    ev5y = _gate(_safe_float(row.get("ev5y_pct")), EV5Y_MIN, EV5Y_MAX)
    peg = _gate(_safe_float(row.get("peg")), PEG_MIN, PEG_MAX)
    fpe = _safe_float(row.get("fpe_fy2"))
    if fpe is not None and (fpe <= FPE_MIN or fpe > FPE_MAX):
        fpe = None

    extras = dd_extras.get(ticker, {})
    quality = _safe_float(extras.get("quality_score"))
    if quality is not None and (quality < QUALITY_MIN or quality > QUALITY_MAX):
        quality = None
    s_pass = _safe_float(extras.get("stress_pass"))
    s_total = _safe_float(extras.get("stress_total"))
    stress_rate: Optional[float] = None
    if s_pass is not None and s_total is not None and s_total > 0:
        stress_rate = s_pass / s_total

    moat_score = _safe_float(row.get("moat_score"))
    if moat_score is not None and (moat_score < MOAT_SCORE_MIN or moat_score > MOAT_SCORE_MAX):
        moat_score = None

    timing = row.get("timing") or {}
    rs_score = _safe_float(timing.get("rs_score"))
    dist_52w = _safe_float(timing.get("dist_52w_high_pct"))
    ma50 = _safe_float(timing.get("ma50_pct"))

    return {
        "ticker": ticker,
        "name": row.get("name") or ticker,
        "sector": row.get("sector") or "",
        "signal": row.get("signal") or "",
        "trap": row.get("trap") or "",
        "val": val_glyph,
        "moat_grade": moat_grade or "",
        "moat_score": moat_score,
        "moat_num": MOAT_GRADE_NUM.get(moat_grade),
        "val_num": VAL_NUM.get(val_glyph),
        "moat_trend": row.get("moat_trend") or "→",
        "ev5y": ev5y,
        "peg": peg,
        "fpe": fpe,
        "quality_score": quality,
        "stress_pass_rate": stress_rate,
        "stress_pass": int(s_pass) if s_pass is not None else None,
        "stress_total": int(s_total) if s_total is not None else None,
        "rs_score": rs_score,
        "dist_52w_high_pct": dist_52w,
        "ma50_pct": ma50,
        "ma_state": _ma_emoji(row.get("ma") or {}),
        "ma_raw": row.get("ma") or {},
        "timing_source": (row.get("timing") or {}).get("timing_source"),
        "dd_path": row.get("dd_path"),
        "dca_path": row.get("dca_path"),
    }


def _ma_emoji(ma: dict) -> str:
    """Reduce the ma sub-object to a single status emoji.

    🟢 strong: above_w52 AND above_w250 AND slope_w250 > 0
    ✅ healthy: above_w250 AND slope_w250 > 0
    🟡 mixed:   above_w250 but not above_w52  (or vice-versa)
    🟠 weak:    above_w250 but slope_w250 ≤ 0
    ❌ broken:  below w250
    —  insufficient data
    """
    if not ma or ma.get("above_w250") is None:
        return "—"
    above52 = ma.get("above_w52")
    above250 = ma.get("above_w250")
    slope = _safe_float(ma.get("slope_w250_pct"))
    if above250 and above52 and (slope is not None and slope > 0):
        return "🟢"
    if above250 and (slope is not None and slope > 0):
        return "✅"
    if above250 and above52 is False:
        return "🟡"
    if above250 and (slope is None or slope <= 0):
        return "🟠"
    if above250 is False:
        return "❌"
    return "—"


# ── AngleResult dataclass ─────────────────────────────────────────────────────

@dataclass
class AngleResult:
    name: str
    type: str          # "forward" or "historical_realized"
    group: str
    top5: list = field(default_factory=list)
    scores_all: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)

    def to_jsonable(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "group": self.group,
            "top5": self.top5,
            "scores_all": self.scores_all,
            **self.extra,
        }


# ── angle implementations ─────────────────────────────────────────────────────

def angle1_composite(rows: list[dict]) -> AngleResult:
    """0.30·MM(moat) + 0.45·MM(EV5Y) + 0.10·MM(quality) + 0.15·MM(1/fpe)."""
    moat = {r["ticker"]: r["moat_score"] for r in rows}
    ev = {r["ticker"]: r["ev5y"] for r in rows}
    quality = {r["ticker"]: r["quality_score"] for r in rows}
    fpe_inv = {r["ticker"]: (None if r["fpe"] is None else 1.0 / r["fpe"]) for r in rows}

    nm = _min_max_normalize(moat)
    ne = _min_max_normalize(ev)
    nq = _min_max_normalize(quality)
    nf = _min_max_normalize(fpe_inv)

    w = COMPOSITE_WEIGHTS
    scores: dict[str, Optional[float]] = {}
    components: dict[str, dict] = {}
    for r in rows:
        t = r["ticker"]
        parts = [nm[t], ne[t], nq[t], nf[t]]
        if any(p is None for p in parts):
            scores[t] = None
            continue
        s = (parts[0] * w["moat"] + parts[1] * w["growth_ev5y"]
             + parts[2] * w["quality_score"] + parts[3] * w["fwdpe_inv"])
        scores[t] = round(s, 4)
        components[t] = {
            "moat": round(parts[0], 4),
            "ev5y": round(parts[1], 4),
            "quality": round(parts[2], 4),
            "fwdpe_inv": round(parts[3], 4),
        }

    top5 = _top_n(rows, scores, lambda t: components.get(t, {}))
    return AngleResult(
        name=ANGLE_META["angle_1"]["name"],
        type="forward",
        group="return_valuation",
        top5=top5,
        scores_all=scores,
        extra={"weights": w, "normalization": "min-max within current universe"},
    )


def angle2_breakout(rows: list[dict]) -> AngleResult:
    """EV5Y≥12 ∩ dist_52w∈[-7,0] ∩ ma50_pct∈[0,5] ∩ rs_score≥80; sort by EV5Y desc."""
    filtered: list[tuple[float, dict]] = []
    obs_3of4: list[tuple[int, float, dict]] = []  # (failed_count, ev5y, row)

    for r in rows:
        ev, dist, ma50, rs = r["ev5y"], r["dist_52w_high_pct"], r["ma50_pct"], r["rs_score"]
        if any(x is None for x in (ev, dist, ma50, rs)):
            continue
        checks = [
            ev >= A2_EV5Y_MIN,
            A2_DIST_52W[0] <= dist <= A2_DIST_52W[1],
            A2_MA50[0] <= ma50 <= A2_MA50[1],
            rs >= A2_RS_MIN,
        ]
        passed = sum(checks)
        if passed == 4:
            filtered.append((ev, r))
        elif passed == 3:
            obs_3of4.append((1, ev, r))

    filtered.sort(key=lambda x: x[0], reverse=True)
    obs_3of4.sort(key=lambda x: x[1], reverse=True)

    top5: list[dict] = []
    scores: dict[str, Optional[float]] = {}
    for rank, (ev, r) in enumerate(filtered[:TOP_N], 1):
        top5.append({
            "rank": rank,
            "ticker": r["ticker"],
            "name": r["name"],
            "value": ev,
            "key_inputs": {
                "ev5y_pct": r["ev5y"],
                "dist_52w_high_pct": r["dist_52w_high_pct"],
                "ma50_pct": r["ma50_pct"],
                "rs_score": r["rs_score"],
            },
            "ma": r["ma_state"],
            "dd_path": r["dd_path"],
        })
        scores[r["ticker"]] = ev

    observation_3of4 = []
    for _, ev, r in obs_3of4[:10]:
        observation_3of4.append({
            "ticker": r["ticker"],
            "name": r["name"],
            "ev5y_pct": r["ev5y"],
            "dist_52w_high_pct": r["dist_52w_high_pct"],
            "ma50_pct": r["ma50_pct"],
            "rs_score": r["rs_score"],
            "ma": r["ma_state"],
            "dd_path": r["dd_path"],
        })

    return AngleResult(
        name=ANGLE_META["angle_2"]["name"],
        type="forward",
        group="momentum",
        top5=top5,
        scores_all=scores,
        extra={
            "filters": {
                "ev5y_min": A2_EV5Y_MIN,
                "dist_52w_high_pct": list(A2_DIST_52W),
                "ma50_pct": list(A2_MA50),
                "rs_score_min": A2_RS_MIN,
            },
            "observation_3of4": observation_3of4,
            "zero_result": len(filtered) == 0,
        },
    )


def angle3_garp(rows: list[dict]) -> AngleResult:
    """EV5Y ÷ fpe_fy2 (per 修正 1)."""
    scores: dict[str, Optional[float]] = {}
    components: dict[str, dict] = {}
    for r in rows:
        ev, fpe = r["ev5y"], r["fpe"]
        if ev is None or fpe is None or fpe == 0:
            scores[r["ticker"]] = None
            continue
        v = round(ev / fpe, 4)
        scores[r["ticker"]] = v
        components[r["ticker"]] = {"ev5y": ev, "fpe_fy2": fpe}

    top5 = _top_n(rows, scores, lambda t: components.get(t, {}))
    return AngleResult(
        name=ANGLE_META["angle_3"]["name"],
        type="forward",
        group="return_valuation",
        top5=top5,
        scores_all=scores,
        extra={"formula": "EV5Y ÷ fpe_fy2 (per 修正 1 — no PEG double-count)"},
    )


def angle4_moat_compounder(rows: list[dict]) -> AngleResult:
    """moat_num × stress_pass_rate × val_num."""
    scores: dict[str, Optional[float]] = {}
    components: dict[str, dict] = {}
    for r in rows:
        mn, sp, vn = r["moat_num"], r["stress_pass_rate"], r["val_num"]
        if any(x is None for x in (mn, sp, vn)):
            scores[r["ticker"]] = None
            continue
        v = round(mn * sp * vn, 4)
        scores[r["ticker"]] = v
        components[r["ticker"]] = {
            "moat_grade": r["moat_grade"],
            "moat_num": mn,
            "stress_pass_rate": round(sp, 3),
            "val": r["val"],
            "val_num": vn,
        }

    top5 = _top_n(rows, scores, lambda t: components.get(t, {}))
    return AngleResult(
        name=ANGLE_META["angle_4"]["name"],
        type="forward",
        group="quality",
        top5=top5,
        scores_all=scores,
        extra={"formula": "moat_num × stress_pass_rate × val_num",
               "encoding": {"moat_grade": MOAT_GRADE_NUM, "val": VAL_NUM}},
    )


def angle5_rs_momentum(rows: list[dict], weekly_cache: dict[str, pd.Series]) -> AngleResult:
    """US (incl. ADR-aliased non-US): rs_score from screener.
    Non-US without ADR: 13W return percentile within non-US sub-universe.
    """
    us_scores: dict[str, Optional[float]] = {}
    non_us_returns: dict[str, Optional[float]] = {}
    components: dict[str, dict] = {}

    for r in rows:
        t = r["ticker"]
        adr = NON_US_TO_US_ADR.get(t)
        # ADR-aliased non-US tickers ride US screener via _maybe_overlay_screener_timing
        if not _is_non_us(t) or adr is not None:
            us_scores[t] = r["rs_score"]
            components[t] = (
                {"source": f"us_adr_proxy:{adr}", "rs_score": r["rs_score"]}
                if adr else
                {"source": "screener_rs", "rs_score": r["rs_score"]}
            )
            continue
        # Pure non-US (no ADR) — 13W proxy within non-US sub-universe
        s = weekly_cache.get(t)
        if s is None or len(s) < 14:
            non_us_returns[t] = None
        else:
            ret_13w = (s.iloc[-1] / s.iloc[-14] - 1) * 100
            non_us_returns[t] = round(float(ret_13w), 2)
        components[t] = {"source": "yfinance_13w_pct", "ret_13w": non_us_returns.get(t)}

    # Non-US-no-ADR: percentile rank within their sub-universe → 0-100
    non_us_pct: dict[str, Optional[float]] = {}
    non_us_vals = [v for v in non_us_returns.values() if v is not None]
    n_pop = len(non_us_vals)
    for t, v in non_us_returns.items():
        if v is None or n_pop == 0:
            non_us_pct[t] = None
        elif n_pop == 1:
            non_us_pct[t] = 50.0
        else:
            rank = sum(1 for x in non_us_vals if x < v)
            non_us_pct[t] = round(rank / (n_pop - 1) * 100, 1)

    scores: dict[str, Optional[float]] = {**us_scores, **non_us_pct}

    top5 = _top_n(rows, scores, lambda t: components.get(t, {}))
    # Surface ADR-via flag on Top 5 entries
    for entry in top5:
        c = entry.get("components", {})
        src = c.get("source", "")
        if isinstance(src, str) and src.startswith("us_adr_proxy:"):
            entry["via_adr"] = src.split(":", 1)[1]

    return AngleResult(
        name=ANGLE_META["angle_5"]["name"],
        type="forward",
        group="momentum",
        top5=top5,
        scores_all=scores,
        extra={
            "non_us_fallback": "13W return percentile within non-US-no-ADR sub-universe (proxy)",
            "non_us_count": n_pop,
            "adr_aliases": NON_US_TO_US_ADR,
        },
    )


def angle6_jensen_alpha(rows: list[dict], weekly_cache: dict[str, pd.Series],
                        spy_weekly: Optional[pd.Series]) -> AngleResult:
    """OLS regress 5Y weekly returns on SPY → alpha × 52 = annualized %.

    Per 修正 4: type="historical_realized" — labeled explicitly in JSON + HTML.
    Per 修正 6: per-ticker failure degrades to None, doesn't break the run.
    """
    scores: dict[str, Optional[float]] = {}
    components: dict[str, dict] = {}

    if spy_weekly is None or len(spy_weekly) < JENSEN_MIN_WEEKS_NA:
        # SPY itself can't be fetched → all angles 6 blank (degraded but not crashed)
        for r in rows:
            scores[r["ticker"]] = None
        return AngleResult(
            name=ANGLE_META["angle_6"]["name"],
            type="historical_realized",
            group="return_valuation",
            top5=[],
            scores_all=scores,
            extra={
                "benchmark": "SPY",
                "regression_window": "5Y weekly",
                "min_weeks_na": JENSEN_MIN_WEEKS_NA,
                "min_weeks_full": JENSEN_MIN_WEEKS_FULL,
                "warning": "歷史實現值；會均值回歸；不可與前瞻指標無差別並列",
                "fatal": "SPY weekly fetch failed — all alphas blank",
            },
        )

    spy_returns = spy_weekly.pct_change().dropna()
    short_history_excluded: list[str] = []
    non_us_excluded: list[str] = []
    via_adr_used: dict[str, str] = {}  # ticker → ADR symbol used

    for r in rows:
        t = r["ticker"]
        # ADR alias path: non-US ticker with a known US ADR → run OLS on the ADR
        # vs SPY, but report under the original ticker. Marks via_adr in components.
        adr = NON_US_TO_US_ADR.get(t)
        if _is_non_us(t) and adr is None:
            # Pure non-US (no ADR) — SPY-benchmarked α is meaningless. Mark N/A.
            scores[t] = None
            non_us_excluded.append(t)
            continue
        yf_key = adr if adr else t
        s = weekly_cache.get(yf_key)
        if s is None:
            scores[t] = None
            continue
        t_returns = s.pct_change().dropna()
        # Align on common dates
        joined = pd.concat([t_returns, spy_returns], axis=1, join="inner").dropna()
        joined.columns = ["t", "spy"]
        weeks = len(joined)
        # Two-stage threshold (per FIX 修正 1):
        #   <104 weeks → n/a (sample too small, IPO/spinoff spike unrebalanced)
        #   104-250   → compute α, mark short_history=True
        #   ≥250      → full 5Y
        if weeks < JENSEN_MIN_WEEKS_NA:
            scores[t] = None
            short_history_excluded.append(t)
            continue
        x = joined["spy"].values
        y = joined["t"].values
        try:
            slope, intercept = np.polyfit(x, y, 1)
        except Exception:  # noqa: BLE001
            scores[t] = None
            continue
        alpha_annualized_pct = float(intercept) * 52 * 100
        scores[t] = round(alpha_annualized_pct, 2)
        components[t] = {
            "beta": round(float(slope), 3),
            "weeks_used": int(weeks),
            "short_history": weeks < JENSEN_MIN_WEEKS_FULL,
        }
        if adr:
            components[t]["via_adr"] = adr
            via_adr_used[t] = adr

    top5 = _top_n(rows, scores, lambda t: components.get(t, {}))
    # Surface short_history + via_adr flags at top-level of each entry
    for entry in top5:
        c = entry.get("components", {})
        entry["short_history"] = bool(c.get("short_history", False))
        if c.get("via_adr"):
            entry["via_adr"] = c["via_adr"]

    return AngleResult(
        name=ANGLE_META["angle_6"]["name"],
        type="historical_realized",
        group="return_valuation",
        top5=top5,
        scores_all=scores,
        extra={
            "benchmark": "SPY",
            "regression_window": "5Y weekly",
            "min_weeks_na": JENSEN_MIN_WEEKS_NA,
            "min_weeks_full": JENSEN_MIN_WEEKS_FULL,
            "short_history_excluded": sorted(short_history_excluded),
            "non_us_excluded": sorted(non_us_excluded),
            "adr_aliases_used": dict(sorted(via_adr_used.items())),
            "us_only_note": "Jensen's α uses SPY benchmark — US tickers + non-US with US ADR (per NON_US_TO_US_ADR) eligible. Pure non-US tickers get status='not_applicable'.",
            "warning": "歷史實現值；會均值回歸；不可與前瞻指標無差別並列",
        },
    )


def _top_n(rows: list[dict], scores: dict[str, Optional[float]],
           components_fn) -> list[dict]:
    """Return Top-N list of dicts (rank, ticker, name, value, components, ma, dd_path)."""
    by_ticker = {r["ticker"]: r for r in rows}
    sortable = [(t, v) for t, v in scores.items() if v is not None]
    sortable.sort(key=lambda x: x[1], reverse=True)
    out: list[dict] = []
    for rank, (t, v) in enumerate(sortable[:TOP_N], 1):
        r = by_ticker.get(t, {})
        out.append({
            "rank": rank,
            "ticker": t,
            "name": r.get("name", t),
            "value": v,
            "components": components_fn(t),
            "ma": r.get("ma_state", "—"),
            "moat_grade": r.get("moat_grade", ""),
            "signal": r.get("signal", ""),
            "dd_path": r.get("dd_path"),
        })
    return out


# ── consensus computation (修正 3) ────────────────────────────────────────────

def compute_consensus(angles: dict[str, AngleResult],
                      rows_by_ticker: dict[str, dict]) -> dict:
    """Group-based consensus: count how many of {quality, return_val, momentum} the ticker hits."""
    group_top5: dict[str, set[str]] = {}
    for group_name, angle_keys in GROUPS.items():
        s: set[str] = set()
        for ak in angle_keys:
            if ak in angles:
                for entry in angles[ak].top5:
                    s.add(entry["ticker"])
        group_top5[group_name] = s

    # For each ticker that appears in any group, compute its crossings + which angles hit it
    all_tickers = set().union(*group_top5.values())
    consensus_rows: list[dict] = []
    for t in all_tickers:
        groups_hit = [g for g, s in group_top5.items() if t in s]
        angles_hit = []
        for ak, ar in angles.items():
            top_tickers = {e["ticker"] for e in ar.top5}
            if t in top_tickers:
                angles_hit.append(ak)
        r = rows_by_ticker.get(t, {})
        consensus_rows.append({
            "ticker": t,
            "name": r.get("name", t),
            "groups_crossed": len(groups_hit),
            "groups_hit": groups_hit,
            "angles_hit": sorted(angles_hit),
            "ma": r.get("ma_state", "—"),
            "moat_grade": r.get("moat_grade", ""),
            "moat_score": r.get("moat_score"),
            "signal": r.get("signal", ""),
            "ev5y": r.get("ev5y"),
            "dd_path": r.get("dd_path"),
            "dca_path": r.get("dca_path"),
        })

    consensus_rows.sort(
        key=lambda x: (-x["groups_crossed"], -len(x["angles_hit"]),
                       -(x["moat_score"] or 0), x["ticker"])
    )

    tier_1 = [c for c in consensus_rows if c["groups_crossed"] == 3]
    tier_2 = [c for c in consensus_rows if c["groups_crossed"] == 2]
    return {"tier_1_overweight": tier_1, "tier_2_satellite": tier_2}


# ── layer state IO ────────────────────────────────────────────────────────────

def state_path(layer: str) -> Path:
    return STATE_DIR / f"{layer}.json"


def write_layer_state(layer: str, angles: dict[str, AngleResult],
                      rows: list[dict], timestamp: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "layer": layer,
        "timestamp": timestamp,
        "angles": {k: a.to_jsonable() for k, a in angles.items()},
        # Don't repeat full rows — just the per-ticker normalized inputs the layer used.
        "rows_lite": [
            {
                "ticker": r["ticker"],
                "name": r["name"],
                "moat_grade": r["moat_grade"],
                "moat_score": r["moat_score"],
                "signal": r["signal"],
                "ev5y": r["ev5y"],
                "peg": r["peg"],
                "fpe": r["fpe"],
                "quality_score": r["quality_score"],
                "stress_pass_rate": r["stress_pass_rate"],
                "rs_score": r["rs_score"],
                "dist_52w_high_pct": r["dist_52w_high_pct"],
                "ma50_pct": r["ma50_pct"],
                "ma_state": r["ma_state"],
                "dd_path": r["dd_path"],
                "dca_path": r["dca_path"],
            }
            for r in rows
        ],
    }
    with state_path(layer).open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def read_layer_state(layer: str) -> Optional[dict]:
    p = state_path(layer)
    if not p.exists():
        return None
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


# ── output renderers ──────────────────────────────────────────────────────────

def _escape(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _fmt(v, decimals: int = 2, suffix: str = "") -> str:
    if v is None:
        return "—"
    if isinstance(v, (int, float)):
        return f"{v:.{decimals}f}{suffix}"
    return _escape(str(v))


def render_html(merged: dict, out_path: Path) -> None:
    """Render the alpha-rank.html page using InvestMQuest dd-screener conventions."""
    as_of = merged["as_of"]
    ts = merged.get("run_timestamps", {})
    universe = merged["universe"]
    angles = merged["angles"]
    consensus = merged["consensus"]

    # Universe stats
    total = universe.get("total", 0)
    us_count = universe.get("us_count", 0)
    non_us_count = universe.get("non_us_count", 0)

    html: list[str] = []
    html.append(f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alpha Rank — DD 六法共識排名 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f0f5fb;color:#1e3a5f;line-height:1.5}}
.imq-nav-root{{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
.imq-nav-inner{{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}}
.imq-logo{{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}}
.imq-logo:hover{{color:#fff !important;text-decoration:none !important}}
.imq-logo span{{color:#3b82f6}}
.imq-menu{{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}}
.imq-menu > a,.imq-dd-btn{{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}}
.imq-menu > a:hover,.imq-dd-btn:hover{{color:#fff !important;background:rgba(255,255,255,.08)}}
.imq-menu > a.active,.imq-dd.active > .imq-dd-btn{{color:#fff !important;background:rgba(59,130,246,.22);font-weight:600}}
.imq-dd{{position:relative;display:inline-block}}
.imq-dd-menu{{display:none;position:absolute;top:100%;left:0;background:#1e293b;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{{display:block}}
.imq-dd-menu a{{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}}
.imq-dd-menu a:hover{{color:#fff !important;background:rgba(59,130,246,.18)}}
.imq-caret{{font-size:.6rem;opacity:.7;margin-top:1px}}
@media(max-width:768px){{.imq-nav-root{{padding:.55rem 12px}}.imq-menu{{width:100%;justify-content:flex-start;gap:.1rem}}.imq-menu > a,.imq-dd-btn{{font-size:.74rem;padding:.32rem .5rem}}.imq-dd-menu{{position:static;display:none;min-width:auto;box-shadow:none;background:rgba(255,255,255,.04);border:none;padding:.1rem 0 .3rem 1rem;margin:.1rem 0}}.imq-dd.open .imq-dd-menu{{display:block}}}}
.hero{{background:#fff;border-bottom:1px solid #dce8f5;padding:24px 32px 18px}}
.hero-inner{{max-width:min(1400px,96vw);margin:0 auto}}
.hero-h1{{font-size:22px;font-weight:600;color:#0f2a45;margin-bottom:4px}}
.hero-sub{{font-size:12px;color:#5a7a9a;line-height:1.55;max-width:880px}}
.hero-stats{{display:flex;gap:18px;margin-top:10px;flex-wrap:wrap}}
.hero-stat{{background:#f0f5fb;border:1px solid #dce8f5;border-radius:6px;padding:8px 12px;font-size:11px;color:#5a7a9a}}
.hero-stat strong{{color:#1e3a5f;font-size:13px;display:block;margin-bottom:1px}}
.section{{max-width:min(1400px,96vw);margin:0 auto;padding:24px 32px}}
.caveat-panel{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:14px 18px;margin-bottom:20px;font-size:12px;color:#854d0e}}
.caveat-panel strong{{color:#78350f;display:block;margin-bottom:6px;font-size:12px}}
.caveat-panel ul{{margin-left:18px;line-height:1.7}}
.angle-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:18px;margin-bottom:30px}}
.angle-card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:14px 16px;overflow:hidden}}
.angle-card h3{{font-size:14px;font-weight:700;color:#0f2a45;margin-bottom:4px;display:flex;align-items:center;justify-content:space-between;gap:8px}}
.angle-card .meta{{font-size:10px;color:#5a7a9a;margin-bottom:8px}}
.angle-card .meta .grp{{display:inline-block;padding:1px 6px;border-radius:4px;background:#eff6ff;color:#1e40af;margin-right:4px;font-weight:600}}
.angle-card .meta .hist{{display:inline-block;padding:1px 6px;border-radius:4px;background:#fef3c7;color:#92400e;font-weight:600;margin-right:4px}}
.angle-card table{{width:100%;border-collapse:collapse;font-size:11px}}
.angle-card th{{background:#f0f6ff;color:#5a7a9a;font-weight:700;padding:5px 6px;text-align:right;border-bottom:1px solid #dce8f5;font-size:9px;letter-spacing:.04em;text-transform:uppercase}}
.angle-card th.left{{text-align:left}}
.angle-card td{{padding:5px 6px;text-align:right;border-bottom:1px solid #f0f5fb;font-variant-numeric:tabular-nums}}
.angle-card td.left{{text-align:left;font-weight:600;color:#0f2a45}}
.angle-card td a{{color:#2563eb;text-decoration:none;font-weight:700}}
.angle-card td a:hover{{text-decoration:underline}}
.zero-result{{background:#fef9c3;border:1px solid #fde68a;border-radius:6px;padding:10px 12px;margin:8px 0;font-size:11px;color:#854d0e;line-height:1.5}}
.zero-result strong{{display:block;margin-bottom:4px}}
.consensus-section{{margin-top:30px}}
.consensus-section h2{{font-size:18px;font-weight:700;color:#0f2a45;margin-bottom:6px}}
.consensus-section .desc{{font-size:12px;color:#5a7a9a;margin-bottom:14px;line-height:1.6}}
.tier-card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:14px 18px;margin-bottom:18px}}
.tier-card h3{{font-size:15px;font-weight:700;margin-bottom:8px;display:flex;align-items:center;gap:8px}}
.tier-card.tier-1 h3{{color:#166534}}
.tier-card.tier-2 h3{{color:#854d0e}}
.tier-card h3 .badge{{display:inline-block;padding:2px 8px;border-radius:5px;font-size:11px;font-weight:700}}
.tier-card.tier-1 h3 .badge{{background:#dcfce7;color:#166534}}
.tier-card.tier-2 h3 .badge{{background:#fef3c7;color:#854d0e}}
.tier-card table{{width:100%;border-collapse:collapse;font-size:12px}}
.tier-card th{{background:#f0f6ff;color:#5a7a9a;font-weight:700;padding:7px 10px;text-align:right;border-bottom:2px solid #dce8f5;font-size:10px;letter-spacing:.04em;text-transform:uppercase}}
.tier-card th.left{{text-align:left}}
.tier-card td{{padding:7px 10px;text-align:right;border-bottom:1px solid #f0f5fb;font-variant-numeric:tabular-nums}}
.tier-card td.left{{text-align:left;font-weight:600;color:#0f2a45}}
.tier-card td a{{color:#2563eb;text-decoration:none;font-weight:700}}
.tier-card td a:hover{{text-decoration:underline}}
.empty-row{{padding:14px;text-align:center;color:#94a3b8;font-size:12px;font-style:italic}}
.angles-hit-pill{{display:inline-block;padding:1px 5px;margin-right:3px;border-radius:3px;background:#eff6ff;color:#1e40af;font-size:9px;font-weight:600}}
.footer{{padding:30px 32px;font-size:11px;color:#5a7a9a;line-height:1.7;max-width:min(1400px,96vw);margin:0 auto;border-top:1px solid #dce8f5}}
.footer h4{{color:#1e3a5f;font-size:12px;margin-top:14px;margin-bottom:6px;font-weight:700}}
.footer code{{background:#f0f5fb;padding:1px 5px;border-radius:3px;font-size:10px;color:#1e3a5f}}
.layer-stale{{color:#9a3412;font-weight:600}}
</style>
</head>
<body>
<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/">首頁</a>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">研究<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/research/">個股 DD</a>
          <a href="/pm/">PM 複盤</a>
          <a href="/id/">產業深度 ID</a>
          <a href="/ds/">產業敘述 DS</a>
          <a href="/comparisons/">多股對比</a>
        </div>
      </div>
      <div class="imq-dd active">
        <button type="button" class="imq-dd-btn">工具<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/dd-screener/">DD Screener</a>
          <a href="/dd-screener/alpha-rank.html" class="active">Alpha Rank</a>
          <a href="/backtest/">量化回測</a>
        </div>
      </div>
      <a href="/flow/">🎯 Flow</a>
    </nav>
  </div>
</header>
<script>(function(){{document.querySelectorAll('.imq-dd-btn').forEach(function(btn){{btn.addEventListener('click',function(e){{e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){{if(d!==dd)d.classList.remove('open')}});dd.classList.toggle('open')}})}});document.addEventListener('click',function(e){{if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){{d.classList.remove('open')}});}});}})();</script>

<div class="hero">
  <div class="hero-inner">
    <div class="hero-h1">Alpha Rank — DD 六法共識排名</div>
    <div class="hero-sub">DD universe ({total} 檔) 由六種數學方法獨立排名，再依三組（品質類 / 報酬估值類 / 動能類）算共識交集。Tier 1 = 跨 3 組（重倉候選）；Tier 2 = 跨 2 組（衛星候選）。設計避開「相關因子重複投票」陷阱 (TASK 修正 3)。</div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>{as_of}</strong>快照日期</div>
      <div class="hero-stat"><strong>{total}</strong>universe</div>
      <div class="hero-stat"><strong>{us_count}</strong>美股</div>
      <div class="hero-stat"><strong>{non_us_count}</strong>非美股</div>
      <div class="hero-stat"><strong>{_layer_stamp(ts.get('fundamental_layer'))}</strong>基本面層 (角度 1/3/4)</div>
      <div class="hero-stat"><strong>{_layer_stamp(ts.get('momentum_layer'))}</strong>動能層 (角度 2/5)</div>
      <div class="hero-stat"><strong>{_layer_stamp(ts.get('jensen_layer'))}</strong>Jensen 層 (角度 6)</div>
    </div>
  </div>
</div>

<div class="section">
  <div class="caveat-panel">
    <strong>v1 必讀 caveats</strong>
    <ul>
      <li><b>標準化基準</b>：角度一 min-max 基準隨 universe 改變 — 不同期分數不可直接跨期比較，只有「同批內相對排名」有意義。</li>
      <li><b>角度六歷史性</b>：Jensen's Alpha 為過去 5Y 歷史實現超額報酬，會均值回歸；不可與前瞻指標 (EV/Upside) 無差別並列。</li>
      <li><b>非美股 RS</b>：非美股 (.TW / .T) angle 2/5 timing 來自 yfinance fallback；angle 5 用 13W 報酬率在非美股 sub-universe 內 percentile rank（與 screener 多視窗加權 RS 方法不同）。</li>
      <li><b>MA 燈號</b>：🟢/✅/🟡/🟠/❌ 僅供觀察，<b>未進入共識排序計算</b> — 純 MA 趨勢系統使用者請自行濾除 🔴/❌ 標的。</li>
      <li><b>缺資料 = 留白</b>：缺欄位的標的在該角度不參與排名，共識計數也不計（無中位數補值，避免製造假訊號）。</li>
      <li><b>跨期比較</b>：本期 universe 新增多檔 v12.3 Inception DD，跨期分數變動主要來自新標的進場競爭與 min-max 基準擴大；跨期分數不可直接比較，相對排序仍有效。</li>
      <li><b>角度六樣本門檻</b>：&lt;104 週判 n/a（樣本太少，IPO/分拆 spike 未稀釋）；104-250 週照算 α 並標 <code>short_history</code>；≥250 週完整 5Y。</li>
      <li><b>角度六僅適用美股</b>：基準為 SPY。非美股（台股應對 ^TWII、日股對 ^N225）α 須以本地指數另行計算，列為獨立 roadmap 項；本表純非美股於角度六標示 N/A。</li>
      <li><b>ADR 代理</b>：少數非美股有高流動 US ADR（如 2330.TW ↔ TSM），於角度 5 / 6 使用 ADR 的 US 資料以保跨檔可比；該筆會帶 <code>via XXX</code> 藍色 badge。其餘角度（1/3/4）仍用本地 listing 的基本面（moat/EV5Y/PEG/FwdPE 與幣別無關）。</li>
    </ul>
  </div>

  <div class="angle-grid">
""")

    # Six angle cards
    for ak in ["angle_1", "angle_2", "angle_3", "angle_4", "angle_5", "angle_6"]:
        a = angles.get(ak)
        if a is None:
            html.append(_angle_card_pending(ak))
        else:
            html.append(_angle_card(ak, a))
    html.append("</div>")

    # Consensus section
    html.append(f"""
  <div class="consensus-section">
    <h2>兩層共識交集</h2>
    <div class="desc">
      共識計數按三組 (品質 / 報酬估值 / 動能) 而非 6 角度單獨計票 — 避免相關因子（角度一含護城河 + 成長、角度六含歷史報酬）導致大型權值股自動多角度命中而被誤判「強共識」。
    </div>
    {_tier_table('tier-1', '🔵 Tier 1 — 跨 3 組（重倉候選）', consensus.get('tier_1_overweight', []))}
    {_tier_table('tier-2', '🟡 Tier 2 — 跨 2 組（衛星候選）', consensus.get('tier_2_satellite', []))}
  </div>
</div>

<div class="footer">
  <h4>方法論</h4>
  <ul>
    <li>角度 1 多因子 Composite：<code>0.30·MM(moat_score) + 0.45·MM(EV5Y) + 0.10·MM(quality_score) + 0.15·MM(1/fpe_fy2)</code> (MM = min-max normalize)</li>
    <li>角度 2 EV×起漲點：<code>EV5Y≥12 ∩ dist_52w_high∈[-7,0] ∩ ma50_pct∈[0,5] ∩ rs_score≥80</code>，sort by EV5Y desc</li>
    <li>角度 3 GARP：<code>EV5Y ÷ fpe_fy2</code> (per 修正 1 — 不可 EV×1/PEG 重複計成長)</li>
    <li>角度 4 護城河複利：<code>moat_num × stress_pass_rate × val_num</code> (S=5/A=4/B=3/C=2/X=1；🟢=1/🟡=.6/🟠=.3/🔴=0)</li>
    <li>角度 5 RS 動能：US 用 screener rs_score；非美股 13W 報酬 percentile 於非美股 sub-universe</li>
    <li>角度 6 Jensen's Alpha：5Y 週線對 SPY OLS 迴歸取 α × 52 = annualized %（歷史實現值）</li>
  </ul>
  <h4>更新頻率</h4>
  <ul>
    <li>基本面層 (角度 1/3/4)：DD/DCA 重跑 + <code>scripts/update_dd_index.py</code> 成功後事件驅動</li>
    <li>動能層 (角度 2/5)：每日盤後 (Mon-Fri 22:30 UTC) 由 <code>daily-alpha-momentum.yml</code> 觸發</li>
    <li>Jensen 層 (角度 6)：每週日 19:00 UTC 由 <code>weekly-alpha-jensen.yml</code> 觸發</li>
  </ul>
  <h4>機器可讀</h4>
  <p>JSON sidecar: <a href="/dd-screener/alpha-rank.json"><code>/dd-screener/alpha-rank.json</code></a> · 每日快照: <code>/dd-screener/alpha-rank-snapshots/YYYY-MM-DD.json</code></p>
  <p style="margin-top:16px;color:#94a3b8">Generated by <code>scripts/dd_alpha_ranker.py</code> · schema v{SCHEMA_VERSION}</p>
</div>
</body>
</html>
""")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(html), encoding="utf-8")


def _layer_stamp(ts: Optional[str]) -> str:
    if not ts:
        return "<span class='layer-stale'>未產出</span>"
    # Trim to YYYY-MM-DD HH:MM
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%m-%d %H:%M")
    except (TypeError, ValueError):
        return _escape(ts[:16])


def _angle_card_pending(angle_key: str) -> str:
    meta = ANGLE_META[angle_key]
    return f"""
    <div class="angle-card">
      <h3>{_escape(meta['name'])} <span style="font-size:10px;color:#94a3b8;font-weight:400">({angle_key})</span></h3>
      <div class="meta"><span class="grp">{meta['group']}</span></div>
      <div class="zero-result">資料尚未產出 — 對應 layer 的 state 檔不存在或無效。執行 <code>python3 scripts/dd_alpha_ranker.py --layers all</code> 重生。</div>
    </div>
    """


def _angle_card(angle_key: str, a: dict | AngleResult) -> str:
    if isinstance(a, AngleResult):
        a_dict = a.to_jsonable()
    else:
        a_dict = a
    meta = ANGLE_META[angle_key]
    is_hist = a_dict.get("type") == "historical_realized"
    group_chip = f"<span class='grp'>{a_dict['group']}</span>"
    hist_chip = "<span class='hist'>歷史實現值</span>" if is_hist else ""

    top5 = a_dict.get("top5", [])
    zero = a_dict.get("zero_result", False)
    obs_3of4 = a_dict.get("observation_3of4", [])

    rows_html = ""
    if zero and angle_key == "angle_2":
        rows_html = f"""
        <div class="zero-result">
          <strong>本期無標的符合起漲點（4 條件 AND）</strong>
          過熱或回調期常見零結果。下方為「3/4 條件」次級觀察清單（放寬一條件、按 EV5Y 排序）：
        </div>
        <table>
          <thead><tr><th class="left">#</th><th class="left">標的</th><th>EV5Y</th><th>距 ATH</th><th>50DMA</th><th>RS</th><th>MA</th></tr></thead>
          <tbody>
        """
        for i, e in enumerate(obs_3of4, 1):
            href = f"<a href='{_escape(e.get('dd_path') or '#')}'>{_escape(e['ticker'])}</a>"
            rows_html += (f"<tr><td class='left'>{i}</td><td class='left'>{href} "
                          f"<span style='color:#94a3b8;font-size:9px'>{_escape(e['name'])}</span></td>"
                          f"<td>{_fmt(e.get('ev5y_pct'), 1, '%')}</td>"
                          f"<td>{_fmt(e.get('dist_52w_high_pct'), 1, '%')}</td>"
                          f"<td>{_fmt(e.get('ma50_pct'), 1, '%')}</td>"
                          f"<td>{_fmt(e.get('rs_score'), 1)}</td>"
                          f"<td>{_escape(e.get('ma', '—'))}</td></tr>")
        rows_html += "</tbody></table>"
    elif not top5:
        rows_html = "<div class='zero-result'>本角度尚無資料（缺輸入或 yfinance 失敗）。</div>"
    else:
        # Pick column header based on angle
        value_label = {
            "angle_1": "Score",
            "angle_2": "EV5Y",
            "angle_3": "EV÷FPE",
            "angle_4": "Score",
            "angle_5": "RS",
            "angle_6": "α (%/yr)",
        }.get(angle_key, "Value")
        rows_html += f"""
        <table>
          <thead><tr><th class="left">#</th><th class="left">標的</th><th>{value_label}</th><th>護城河</th><th>訊號</th><th>MA</th></tr></thead>
          <tbody>
        """
        for e in top5:
            href = f"<a href='{_escape(e.get('dd_path') or '#')}'>{_escape(e['ticker'])}</a>"
            # ADR proxy badge (angles 5 + 6): non-US ticker uses its US ADR for data
            if angle_key in ("angle_5", "angle_6") and e.get("via_adr"):
                adr = e["via_adr"]
                href += (f" <span title='角度 {angle_key[-1]} 使用 {adr} (US ADR) 資料 "
                         f"— 美股同基準可比' "
                         f"style='background:#dbeafe;color:#1e40af;padding:1px 5px;"
                         f"border-radius:3px;font-size:9px;font-weight:700;"
                         f"margin-left:3px'>via {_escape(adr)}</span>")
            # Angle 6: short_history badge (104-250 wk window — α computed but flagged)
            if angle_key == "angle_6" and e.get("short_history"):
                weeks = (e.get("components") or {}).get("weeks_used", "?")
                href += (f" <span title='樣本 {weeks} 週 (<250) — 短歷史，α 不穩' "
                         f"style='background:#fef3c7;color:#92400e;padding:1px 5px;"
                         f"border-radius:3px;font-size:9px;font-weight:700;"
                         f"margin-left:3px'>短歷史</span>")
            v = e.get("value")
            v_fmt = _fmt(v, 2) if v is not None else "—"
            if angle_key == "angle_2":
                v_fmt = _fmt(v, 1, "%")
            elif angle_key == "angle_5":
                v_fmt = _fmt(v, 1)
            elif angle_key == "angle_6":
                v_fmt = _fmt(v, 2, "%")
            rows_html += (f"<tr><td class='left'>{e['rank']}</td>"
                          f"<td class='left'>{href} <span style='color:#94a3b8;font-size:9px'>{_escape(e.get('name', ''))}</span></td>"
                          f"<td>{v_fmt}</td>"
                          f"<td>{_escape(e.get('moat_grade', ''))}</td>"
                          f"<td>{_escape(e.get('signal', ''))}</td>"
                          f"<td>{_escape(e.get('ma', '—'))}</td></tr>")
        rows_html += "</tbody></table>"

    return f"""
    <div class="angle-card">
      <h3>{_escape(a_dict['name'])} <span style="font-size:10px;color:#94a3b8;font-weight:400">({angle_key})</span></h3>
      <div class="meta">{group_chip}{hist_chip}</div>
      {rows_html}
    </div>
    """


def _tier_table(css_class: str, header: str, rows: list[dict]) -> str:
    out = f"<div class='tier-card {css_class}'><h3>{header} <span class='badge'>{len(rows)} 檔</span></h3>"
    if not rows:
        out += "<div class='empty-row'>本期此 tier 無標的</div></div>"
        return out
    out += """<table><thead><tr>
      <th class="left">標的</th>
      <th>跨組</th>
      <th class="left">命中角度</th>
      <th>護城河</th>
      <th>訊號</th>
      <th>EV5Y</th>
      <th>MA</th>
      <th class="left">連結</th>
    </tr></thead><tbody>"""
    for r in rows:
        angles_pills = " ".join(
            f"<span class='angles-hit-pill'>{_escape(a.replace('angle_', 'A'))}</span>"
            for a in r.get("angles_hit", [])
        )
        href_dd = f"<a href='{_escape(r.get('dd_path') or '#')}'>DD</a>" if r.get("dd_path") else "—"
        href_dca = f" · <a href='{_escape(r.get('dca_path'))}'>DCA</a>" if r.get("dca_path") else ""
        out += (f"<tr>"
                f"<td class='left'>{_escape(r['ticker'])} <span style='color:#94a3b8;font-size:10px'>{_escape(r.get('name', ''))}</span></td>"
                f"<td><strong>{r['groups_crossed']}/3</strong></td>"
                f"<td class='left'>{angles_pills}</td>"
                f"<td>{_escape(r.get('moat_grade', ''))}</td>"
                f"<td>{_escape(r.get('signal', ''))}</td>"
                f"<td>{_fmt(r.get('ev5y'), 1, '%')}</td>"
                f"<td>{_escape(r.get('ma', '—'))}</td>"
                f"<td class='left'>{href_dd}{href_dca}</td>"
                f"</tr>")
    out += "</tbody></table></div>"
    return out


def write_json(merged: dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2, default=str)


def write_snapshot(merged: dict, rows: list[dict], snapshot_dir: Path) -> None:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    date = merged["as_of"]
    snap_path = snapshot_dir / f"{date}.json"
    snap = dict(merged)
    # Add raw input snapshot for §v1 必做 C
    snap["inputs_raw"] = [
        {k: r[k] for k in (
            "ticker", "name", "moat_grade", "moat_score", "signal", "ev5y",
            "peg", "fpe", "quality_score", "stress_pass", "stress_total",
            "stress_pass_rate", "rs_score", "dist_52w_high_pct", "ma50_pct",
            "ma_state"
        )}
        for r in rows
    ]
    with snap_path.open("w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2, default=str)


# ── orchestration ─────────────────────────────────────────────────────────────

def _is_non_us(ticker: str) -> bool:
    return "." in ticker


def _maybe_overlay_screener_timing(rows: list[dict]) -> None:
    """For US tickers, overwrite timing fields with screener/latest.json (daily-fresh).

    ADR alias: for non-US tickers in NON_US_TO_US_ADR, look up the ADR's
    screener data and overlay it onto the non-US row. Marks adr_proxy.
    """
    screener = load_screener_timing()
    if not screener:
        return
    for r in rows:
        t = r["ticker"]
        adr = NON_US_TO_US_ADR.get(t)
        if adr and adr in screener:
            r["rs_score"] = screener[adr]["rs_score"]
            r["dist_52w_high_pct"] = screener[adr]["dist_52w_high_pct"]
            r["ma50_pct"] = screener[adr]["ma50_pct"]
            r["timing_via_adr"] = adr
            continue
        if _is_non_us(t):
            continue
        if t in screener:
            r["rs_score"] = screener[t]["rs_score"]
            r["dist_52w_high_pct"] = screener[t]["dist_52w_high_pct"]
            r["ma50_pct"] = screener[t]["ma50_pct"]


def _fetch_non_us_timing(rows: list[dict]) -> None:
    """Compute rs_score/dist_52w_high_pct/ma50_pct for non-US tickers via yfinance.

    Skips tickers that already received ADR-proxy timing (NON_US_TO_US_ADR overlay).
    """
    non_us = [r for r in rows if _is_non_us(r["ticker"])
              and r["ticker"] not in NON_US_TO_US_ADR
              and (r["rs_score"] is None or r["dist_52w_high_pct"] is None or r["ma50_pct"] is None)]
    if not non_us:
        return
    tickers = [r["ticker"] for r in non_us]
    print(f"  fetching yfinance fallback timing for {len(tickers)} non-US tickers...",
          file=sys.stderr)
    weekly = fetch_weekly_closes(tickers, max_workers=4, period="2y")
    for r in non_us:
        s = weekly.get(r["ticker"])
        if s is None or len(s) < 14:
            continue
        # dist from 52-week high
        last = float(s.iloc[-1])
        recent = s.iloc[-52:] if len(s) >= 52 else s
        ath = float(recent.max())
        r["dist_52w_high_pct"] = round((last / ath - 1) * 100, 2)
        # 50-day proxy: 10 weeks ≈ 50 trading days
        if len(s) >= 10:
            ma50_proxy = float(s.iloc[-10:].mean())
            r["ma50_pct"] = round((last / ma50_proxy - 1) * 100, 2)
        # rs_score will be set by angle5 itself (it's a different metric)


def run_fundamental_layer(rows: list[dict]) -> dict[str, AngleResult]:
    return {
        "angle_1": angle1_composite(rows),
        "angle_3": angle3_garp(rows),
        "angle_4": angle4_moat_compounder(rows),
    }


def run_momentum_layer(rows: list[dict]) -> dict[str, AngleResult]:
    """Angles 2 + 5. Caller should have ensured rows have fresh timing fields."""
    # Angle 5 13W proxy needs weekly closes only for non-US-without-ADR tickers.
    # ADR-aliased non-US (e.g. 2330.TW → TSM) ride the US screener overlay instead.
    non_us = [r["ticker"] for r in rows
              if _is_non_us(r["ticker"]) and r["ticker"] not in NON_US_TO_US_ADR]
    weekly_cache: dict[str, pd.Series] = {}
    if non_us:
        print(f"  fetching weekly closes for {len(non_us)} non-US-no-ADR tickers (angle 5)...",
              file=sys.stderr)
        weekly_cache = fetch_weekly_closes(non_us, max_workers=4, period="2y")
    return {
        "angle_2": angle2_breakout(rows),
        "angle_5": angle5_rs_momentum(rows, weekly_cache),
    }


def run_jensen_layer(rows: list[dict]) -> dict[str, AngleResult]:
    # FIX2 + ADR alias: fetch US tickers + ADR aliases (for non-US in NON_US_TO_US_ADR).
    # Pure non-US (no ADR) skipped — they will be marked non_us_excluded.
    fetch_set: set[str] = set()
    adr_used: set[str] = set()
    for r in rows:
        t = r["ticker"]
        if not _is_non_us(t):
            fetch_set.add(t)
            continue
        adr = NON_US_TO_US_ADR.get(t)
        if adr:
            fetch_set.add(adr)
            adr_used.add(adr)
    fetch_list = sorted(fetch_set)
    n_skipped = len(rows) - len(fetch_list)
    adr_note = f" (incl. {len(adr_used)} ADR alias: {sorted(adr_used)})" if adr_used else ""
    print(f"  fetching 5Y weekly closes for {len(fetch_list)} US-or-ADR tickers + SPY "
          f"(angle 6; skipping {n_skipped} pure non-US){adr_note}...",
          file=sys.stderr)
    weekly_cache = fetch_weekly_closes(fetch_list, max_workers=8, period="5y")
    spy_series = _yf_fetch_one_weekly("SPY", period="5y")
    if spy_series is None:
        print("ERROR: SPY weekly fetch failed — angle 6 will be all blank", file=sys.stderr)
    return {
        "angle_6": angle6_jensen_alpha(rows, weekly_cache, spy_series),
    }


def merge_layer_states(rows: list[dict]) -> dict:
    """Read all 3 layer state files, merge into final document."""
    fundamental = read_layer_state("fundamental")
    momentum = read_layer_state("momentum")
    jensen = read_layer_state("jensen")

    angles: dict = {}
    if fundamental:
        angles.update(fundamental.get("angles", {}))
    if momentum:
        angles.update(momentum.get("angles", {}))
    if jensen:
        angles.update(jensen.get("angles", {}))

    rows_by_ticker = {r["ticker"]: r for r in rows}
    # Reconstruct AngleResult-like dicts only contain top5 → consensus needs only that
    angle_objs: dict[str, AngleResult] = {}
    for ak, ad in angles.items():
        angle_objs[ak] = AngleResult(
            name=ad.get("name", ak),
            type=ad.get("type", "forward"),
            group=ad.get("group", "return_valuation"),
            top5=ad.get("top5", []),
            scores_all=ad.get("scores_all", {}),
            extra={k: v for k, v in ad.items()
                   if k not in ("name", "type", "group", "top5", "scores_all")},
        )
    consensus = compute_consensus(angle_objs, rows_by_ticker)

    us_count = sum(1 for r in rows if not _is_non_us(r["ticker"]))
    non_us_count = len(rows) - us_count
    non_us_tickers = [r["ticker"] for r in rows if _is_non_us(r["ticker"])]

    return {
        "schema_version": SCHEMA_VERSION,
        "as_of": _today(),
        "run_timestamps": {
            "fundamental_layer": fundamental.get("timestamp") if fundamental else None,
            "momentum_layer": momentum.get("timestamp") if momentum else None,
            "jensen_layer": jensen.get("timestamp") if jensen else None,
        },
        "universe": {
            "total": len(rows),
            "us_count": us_count,
            "non_us_count": non_us_count,
            "non_us_tickers": non_us_tickers,
        },
        "caveats": {
            "normalization": "min-max within current universe; scores not comparable across runs (see angle 1 caveat — v2 plans cross-period z-score)",
            "non_us_timing": "RS / dist_52w / ma50 for non-US via yfinance proxy; methodologically differs from screener's multi-window weighted RS",
            "angle_6_historical": "Jensen's alpha is past-realized; will mean-revert; not directly comparable to forward EV/Upside angles",
            "ma_penalty": "MA traffic-light annotated only; does NOT reduce consensus ranking weight (per user spec choice 2026-05-17)",
        },
        "consensus_groups": GROUPS,
        "angles": {k: a.to_jsonable() for k, a in angle_objs.items()},
        "consensus": consensus,
        "v2_extensions_reserved": [
            "ic_weights", "factor_orthogonalization", "drawdown_factor",
            "momentum_smoothness", "outlier_detection", "kelly_sizing",
        ],
    }


def run_layers(layers: list[str], *, write_snapshot_flag: bool = True) -> int:
    print(f"=== dd_alpha_ranker — layers={layers} ===", file=sys.stderr)
    universe_raw = load_universe()
    dd_extras = load_dd_meta_extras()
    rows = [sanitize_row(r, dd_extras) for r in universe_raw]
    print(f"  loaded {len(rows)} tickers from dd-screener latest.json", file=sys.stderr)

    # Layer-specific freshening
    if "momentum" in layers or "all" in layers:
        _maybe_overlay_screener_timing(rows)
        _fetch_non_us_timing(rows)

    ts = _now_taipei_iso()
    layers_set = set(layers)
    if "all" in layers_set:
        layers_set = {"fundamental", "momentum", "jensen"}

    if "fundamental" in layers_set:
        print("  > fundamental layer (angles 1/3/4)...", file=sys.stderr)
        angles = run_fundamental_layer(rows)
        write_layer_state("fundamental", angles, rows, ts)
    if "momentum" in layers_set:
        print("  > momentum layer (angles 2/5)...", file=sys.stderr)
        angles = run_momentum_layer(rows)
        write_layer_state("momentum", angles, rows, ts)
    if "jensen" in layers_set:
        print("  > jensen layer (angle 6)...", file=sys.stderr)
        angles = run_jensen_layer(rows)
        write_layer_state("jensen", angles, rows, ts)

    merged = merge_layer_states(rows)
    write_json(merged, JSON_OUT)
    render_html(merged, HTML_OUT)
    if write_snapshot_flag:
        write_snapshot(merged, rows, SNAPSHOT_DIR)

    print(f"  wrote {HTML_OUT.relative_to(ROOT)}", file=sys.stderr)
    print(f"  wrote {JSON_OUT.relative_to(ROOT)}", file=sys.stderr)
    if write_snapshot_flag:
        print(f"  wrote snapshot {SNAPSHOT_DIR.relative_to(ROOT)}/{merged['as_of']}.json",
              file=sys.stderr)

    # Sanity-check console summary
    print("\n=== Top 5 summary ===", file=sys.stderr)
    for ak in ["angle_1", "angle_2", "angle_3", "angle_4", "angle_5", "angle_6"]:
        a = merged["angles"].get(ak)
        if a is None:
            print(f"  {ak}: <no state>", file=sys.stderr)
            continue
        tickers = [e["ticker"] for e in a.get("top5", [])]
        print(f"  {ak} {a['name']}: {' · '.join(tickers) if tickers else '(empty)'}",
              file=sys.stderr)
    t1 = [c["ticker"] for c in merged["consensus"]["tier_1_overweight"]]
    t2 = [c["ticker"] for c in merged["consensus"]["tier_2_satellite"]]
    print(f"  Tier 1 (跨3組): {' · '.join(t1) if t1 else '(empty)'}", file=sys.stderr)
    print(f"  Tier 2 (跨2組): {' · '.join(t2) if t2 else '(empty)'}", file=sys.stderr)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="DD Alpha Ranker — 6-method consensus")
    p.add_argument("--layers", nargs="+",
                   choices=["fundamental", "momentum", "jensen", "all"],
                   default=["all"],
                   help="Which layer(s) to recompute. Other layers reused from state files.")
    p.add_argument("--no-snapshot", action="store_true",
                   help="Skip writing dated snapshot (still updates main JSON/HTML).")
    args = p.parse_args()
    return run_layers(args.layers, write_snapshot_flag=not args.no_snapshot)


if __name__ == "__main__":
    sys.exit(main())
