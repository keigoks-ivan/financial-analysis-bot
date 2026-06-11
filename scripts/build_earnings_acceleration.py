#!/usr/bin/env python3
"""Earnings Acceleration Screener — EPS 加速 + 分析師上修 + 財報持續 beat.

設計 source-of-truth: /Users/ivanchang/.claude/plans/yfinance-eps-zippy-frost.md

Pipeline:
  1. 讀 docs/dd-screener/latest.json (v1.2+)
  2. Inline yfinance fetch — eps_trend + earnings_history (ThreadPoolExecutor 4)
  3. 每檔套 vetoes (ai_risk 🔴 / moat_grade C/X / trap 🔴 / moat_score < 6 /
     資料缺失 / 連續 miss ≥ 2 / FY0+FY1 同時急速下修 < -5%)
  4. 算 A (Revision Momentum 50%) / B (Beat Track Record 30%) /
     C (Quality Floor 20%) 三支柱
     Final = 0.50·A + 0.30·B + 0.20·C
  5. Tier 切分：
       Tier A — Earnings Re-rating:   Final ≥ 0.65  AND  A ≥ 0.60  AND  B ≥ 0.55
       Tier B — Single-Engine Watch:  Final ≥ 0.65  but A or B short of threshold
  6. 取 Tier A 全部 + Tier B 補到合計 25 檔
  7. 寫 docs/dd-screener/earnings-acceleration.{html,json}
     + docs/dd-screener/earnings-acceleration-snapshots/YYYY-MM-DD.json

Usage:
  python3 scripts/build_earnings_acceleration.py
  python3 scripts/build_earnings_acceleration.py --dry-run     # 不寫檔
  python3 scripts/build_earnings_acceleration.py --no-snapshot # 不寫 daily snapshot
  python3 scripts/build_earnings_acceleration.py --top 20      # smoke-test
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# Shared Excel-coverage helper (universe filter only — scoring unchanged)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dd_screener_quality import has_excel_cagr  # noqa: E402

# ── suppress yfinance noise ───────────────────────────────────────────────────
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("peewee").setLevel(logging.CRITICAL)

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "-q"])
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

# EU suffix map (single source of truth from dd_screener_quality)
try:
    from dd_screener_quality import EU_SUFFIX_MAP
except ImportError:
    EU_SUFFIX_MAP: dict[str, str] = {}

from site_nav import DD_SCREENER_SUBNAV, build_subnav, full_nav_block  # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
LATEST_JSON = ROOT / "docs" / "dd-screener" / "latest.json"
OUTPUT_DIR = ROOT / "docs" / "dd-screener"
HTML_OUT = OUTPUT_DIR / "earnings-acceleration.html"
JSON_OUT = OUTPUT_DIR / "earnings-acceleration.json"
SNAPSHOT_DIR = OUTPUT_DIR / "earnings-acceleration-snapshots"

# Canonical site header + dd-screener sub-nav (single source: scripts/site_nav.py)
NAV_BLOCK = full_nav_block(
    "quant", "dds",
    build_subnav(DD_SCREENER_SUBNAV, "/dd-screener/earnings-acceleration.html"),
)

TAIPEI_TZ = timezone(timedelta(hours=8))
SCHEMA_VERSION = "1.0"

# ── scoring constants ─────────────────────────────────────────────────────────
PILLAR_WEIGHTS = {"revision": 0.50, "beat": 0.30, "floor": 0.20}

# v1.0.2: re-tighten — v1.0.1 (final 0.75, rev 0.60, beat 0.55) produced ~50 Tier A
# in 2026-05 bull market, losing signal. New thresholds yield ~10-15 tickers ("most
# accelerating EPS, top scorers only"): all three pillars must clear high bars
# simultaneously — pure revision strength alone or beat alone is not enough.
TIER_FINAL_MIN = 0.88
TIER_A_REVISION_MIN = 0.85
TIER_A_BEAT_MIN = 0.70
DISPLAY_TOTAL = 25

MOAT_SCORE_MIN = 6
MAX_MISS_COUNT = 2       # ≥ 2 misses in last 4 → veto
VETO_REVISION_BOTH = -5.0  # FY0 AND FY1 both < -5% (30d) → veto


# ── helpers ───────────────────────────────────────────────────────────────────
def _clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def _today() -> str:
    return datetime.now(TAIPEI_TZ).strftime("%Y-%m-%d")


def _safe_float(x) -> Optional[float]:
    if x is None:
        return None
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    if f != f:  # NaN
        return None
    return f


def _yf_ticker_for(dd_ticker: str) -> str:
    """Resolve DD ticker → yfinance ticker (adds EU suffix when needed)."""
    return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}" if dd_ticker in EU_SUFFIX_MAP else dd_ticker


# ── yfinance fetch ────────────────────────────────────────────────────────────
def _fetch_earnings_data(yf_ticker: str) -> Optional[dict]:
    """Fetch eps_trend + earnings_history for one ticker.

    Returns dict with:
      fy0_curr, fy0_30d_ago, fy0_90d_ago   — FY0 EPS estimates
      fy1_curr, fy1_30d_ago, fy1_90d_ago   — FY1 EPS estimates
      surprises  — list of 4 most recent surprisePercent values [oldest→newest]

    Returns None on fatal failure (ticker veto'd downstream).
    """
    try:
        tk = yf.Ticker(yf_ticker)

        # ── eps_trend ─────────────────────────────────────────────────────────
        trend = tk.eps_trend
        if trend is None or getattr(trend, "empty", True):
            return None

        out: dict = {}

        def _get_trend(row_label: str, col: str) -> Optional[float]:
            try:
                if row_label not in trend.index:
                    return None
                val = trend.loc[row_label].get(col)
                return _safe_float(val)
            except Exception:
                return None

        # FY0 = "0y" row; FY1 = "+1y" row
        out["fy0_curr"]    = _get_trend("0y", "current")
        out["fy0_30d_ago"] = _get_trend("0y", "30daysAgo")
        out["fy0_90d_ago"] = _get_trend("0y", "90daysAgo")
        out["fy1_curr"]    = _get_trend("+1y", "current")
        out["fy1_30d_ago"] = _get_trend("+1y", "30daysAgo")
        out["fy1_90d_ago"] = _get_trend("+1y", "90daysAgo")

        # Must have at least fy0_curr and fy1_curr to compute revisions
        if out["fy0_curr"] is None or out["fy1_curr"] is None:
            return None

        # ── earnings_history ──────────────────────────────────────────────────
        hist = tk.earnings_history
        if hist is None or getattr(hist, "empty", True):
            return None

        if "surprisePercent" not in hist.columns:
            return None

        # Sort by index (date) ascending so surprises[0] = oldest, [-1] = newest
        hist_sorted = hist.sort_index(ascending=True)
        surp_col = hist_sorted["surprisePercent"].dropna()

        if len(surp_col) < 4:
            return None  # Need at least 4 quarters

        # Take the 4 most recent quarters: oldest→newest order
        surprises = [_safe_float(v) for v in surp_col.iloc[-4:].tolist()]
        if any(v is None for v in surprises):
            return None

        out["surprises"] = surprises  # list[float], len=4, oldest=0, newest=3
        return out

    except Exception as exc:
        print(f"    [EA] WARN {yf_ticker}: {exc}", file=sys.stderr)
        return None


def _fetch_all_earnings(stocks: list[dict], max_workers: int = 4) -> dict[str, Optional[dict]]:
    """Fetch earnings data for all stocks concurrently.

    Returns dict: dd_ticker → earnings_data (or None on failure).
    """
    results: dict[str, Optional[dict]] = {}
    ticker_map = {s["ticker"]: _yf_ticker_for(s["ticker"]) for s in stocks}

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_fetch_earnings_data, yf_t): dd_t
                for dd_t, yf_t in ticker_map.items()}
        for i, fut in enumerate(as_completed(futs), 1):
            dd_t = futs[fut]
            try:
                results[dd_t] = fut.result(timeout=30)
            except Exception as exc:
                print(f"    [EA] ERR {dd_t}: {exc}", file=sys.stderr)
                results[dd_t] = None
            if i % 20 == 0 or i == len(futs):
                elapsed = time.time() - t0
                ok = sum(1 for v in results.values() if v is not None)
                print(f"    [{i:>3}/{len(futs)}] {elapsed:.0f}s — data ok: {ok}")

    return results


# ── score curves ──────────────────────────────────────────────────────────────
def revision_score(rev_pct: Optional[float]) -> float:
    """Λ function for EPS revision %.

    Anchor points per plan:
      -5%+   → 0
      -2%    → 0.2
       0%    → 0.4
      +2%    → 0.7
      +5%    → 1.0
     +10%+   → 1.0 (cap)
    """
    if rev_pct is None:
        return 0.3  # neutral — missing data
    v = rev_pct
    if v <= -5:
        return 0.0
    if v < -2:
        # -5 → 0; -2 → 0.2
        return (v + 5) / 3 * 0.2
    if v < 0:
        # -2 → 0.2; 0 → 0.4
        return 0.2 + (v + 2) / 2 * 0.2
    if v < 2:
        # 0 → 0.4; +2 → 0.7
        return 0.4 + v / 2 * 0.3
    if v < 5:
        # +2 → 0.7; +5 → 1.0
        return 0.7 + (v - 2) / 3 * 0.3
    return 1.0  # >= +5% → cap 1.0


def eps_rev_safety_score(eps_revision_pct: Optional[float]) -> float:
    """eps_revision_pct: EPS revision % (negative = analysts cutting).

    >= -10%       → 1.0
    -10 to -20%   → 0.5
    -20 to -30%   → 0.2
    < -30%        → 0 (also vetoed upstream in some screeners)
    """
    if eps_revision_pct is None:
        return 0.7  # neutral-positive (not being cut)
    e = eps_revision_pct
    if e >= -10:
        return 1.0
    if e >= -20:
        return 1.0 - (e + 10) / (-10) * 0.5
    if e >= -30:
        return 0.5 - (e + 20) / (-10) * 0.3
    return 0.0


# ── pillars ───────────────────────────────────────────────────────────────────
def _safe_rev_pct(curr: Optional[float], ago: Optional[float]) -> Optional[float]:
    """Compute (curr - ago) / |ago| * 100, guard div-by-zero."""
    if curr is None or ago is None:
        return None
    if ago == 0:
        return None
    return (curr - ago) / abs(ago) * 100


def pillar_revision(ed: dict) -> tuple[float, dict]:
    """A = Revision Momentum (50%).

    4 sub-signals:
      fy0_rev_30d  (weight 0.30)
      fy0_rev_90d  (weight 0.20)
      fy1_rev_30d  (weight 0.30)
      fy1_rev_90d  (weight 0.20)
    """
    fy0_30d = _safe_rev_pct(ed.get("fy0_curr"), ed.get("fy0_30d_ago"))
    fy0_90d = _safe_rev_pct(ed.get("fy0_curr"), ed.get("fy0_90d_ago"))
    fy1_30d = _safe_rev_pct(ed.get("fy1_curr"), ed.get("fy1_30d_ago"))
    fy1_90d = _safe_rev_pct(ed.get("fy1_curr"), ed.get("fy1_90d_ago"))

    s0_30 = revision_score(fy0_30d)
    s0_90 = revision_score(fy0_90d)
    s1_30 = revision_score(fy1_30d)
    s1_90 = revision_score(fy1_90d)

    score = 0.30 * s0_30 + 0.20 * s0_90 + 0.30 * s1_30 + 0.20 * s1_90
    score = _clip01(score)

    return score, {
        "fy0_rev_30d": fy0_30d,
        "fy0_rev_90d": fy0_90d,
        "fy1_rev_30d": fy1_30d,
        "fy1_rev_90d": fy1_90d,
        "s0_30": round(s0_30, 3),
        "s0_90": round(s0_90, 3),
        "s1_30": round(s1_30, 3),
        "s1_90": round(s1_90, 3),
    }


def _linreg_slope(ys: list[float]) -> float:
    """Linear regression slope of ys (x = 1..n). Returns slope."""
    n = len(ys)
    if n < 2:
        return 0.0
    xs = list(range(1, n + 1))
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(xs, ys))
    den = sum((xi - mx) ** 2 for xi in xs)
    return num / den if den != 0 else 0.0


def pillar_beat(ed: dict) -> tuple[float, dict]:
    """B = Beat Track Record (30%).

    Surprises: list[float] len=4, oldest=0, newest=3.

    4 sub-signals:
      beat_count_norm    (0.25) — fraction of quarters with surprise > 0
      beat_acceleration  (0.30) — linreg slope, normalized
      latest_beat_score  (0.25) — most recent surprise score
      beat_consistency   (0.20) — 1 / (1 + stddev)
    """
    surprises: list[float] = ed.get("surprises", [])
    n = len(surprises)
    if n < 4:
        return 0.3, {"error": "insufficient surprises"}

    # beat_count_norm
    beat_count = sum(1 for s in surprises if s > 0)
    beat_count_norm = beat_count / 4.0

    # latest_beat_score (newest quarter = index 3)
    latest = surprises[-1]
    if latest > 5:
        latest_beat = 1.0
    elif latest >= 2:
        latest_beat = 0.7
    elif latest >= 0:
        latest_beat = 0.4
    else:
        latest_beat = 0.0

    # beat_acceleration: linreg slope across 4 quarters
    slope = _linreg_slope(surprises)
    if slope > 1:
        beat_accel = 1.0
    elif slope > 0:
        beat_accel = 0.6
    elif slope == 0:
        beat_accel = 0.4
    else:
        beat_accel = 0.0

    # beat_consistency: 1 / (1 + stddev)
    mean = sum(surprises) / n
    variance = sum((s - mean) ** 2 for s in surprises) / n
    stddev = math.sqrt(variance)
    beat_consistency = _clip01(1.0 / (1.0 + stddev / 10.0))  # scale stddev by 10 for pct units

    score = (0.25 * beat_count_norm + 0.30 * beat_accel
             + 0.25 * latest_beat + 0.20 * beat_consistency)
    score = _clip01(score)

    return score, {
        "beat_count": beat_count,
        "beat_count_norm": round(beat_count_norm, 3),
        "latest_surprise": round(latest, 2),
        "latest_beat_score": round(latest_beat, 3),
        "slope": round(slope, 3),
        "beat_accel": round(beat_accel, 3),
        "stddev": round(stddev, 2),
        "beat_consistency": round(beat_consistency, 3),
        "surprises": surprises,
    }


def pillar_floor(s: dict) -> tuple[float, dict]:
    """C = Quality Floor (20%).

    0.40·moat/10 + 0.30·pass_count/5 + 0.15·quality_score/10 + 0.15·eps_rev_safety

    Reused from build_breakout.py / build_bottom_out.py.
    """
    moat = _safe_float(s.get("moat_score")) or 0
    pass_count = _safe_float(s.get("pass_count")) or 0
    qs = _safe_float(s.get("quality_score"))
    eps_rev = _safe_float(s.get("eps_revision_pct"))

    moat_norm = moat / 10.0
    pass_norm = pass_count / 5.0
    quality_norm = (qs / 10.0) if qs is not None else moat_norm
    eps_safe = eps_rev_safety_score(eps_rev)

    score = 0.40 * moat_norm + 0.30 * pass_norm + 0.15 * quality_norm + 0.15 * eps_safe
    score = _clip01(score)
    return score, {
        "moat_norm": round(moat_norm, 3),
        "pass_norm": round(pass_norm, 3),
        "quality_norm": round(quality_norm, 3),
        "eps_rev_safety": round(eps_safe, 3),
        "eps_revision_pct": eps_rev,
    }


# ── vetoes ────────────────────────────────────────────────────────────────────
def is_vetoed(s: dict, ed: Optional[dict]) -> Optional[str]:
    """Return veto reason string, or None if eligible.

    EA vetoes are intentionally more relaxed than Breakout — no dist_52w_high veto.
    """
    # Excel-coverage veto (cross-page consistency — 5 dd-screener pages use Excel
    # forward CAGR; tickers without Excel coverage are excluded from all 5)
    if not has_excel_cagr(s):
        return "Excel EPS 覆蓋外"
    # Quality vetoes (same as other screeners)
    ai_risk = s.get("ai_risk")
    if ai_risk == "🔴":
        return "AI disrupt 🔴"
    moat_grade = s.get("moat_grade", "")
    if moat_grade in ("C", "X"):
        return f"護城河 {moat_grade}"
    trap = s.get("trap", "")
    if trap == "🔴":
        return "Trap 🔴"
    moat_score = _safe_float(s.get("moat_score"))
    if moat_score is not None and moat_score < MOAT_SCORE_MIN:
        return f"護城河分 {moat_score:.0f} (<{MOAT_SCORE_MIN})"

    # Data availability vetoes
    if ed is None:
        return "EPS data unavailable"
    surprises = ed.get("surprises", [])
    if len(surprises) < 4:
        return "earnings_history < 4 quarters"

    # EA-specific vetoes
    miss_count = sum(1 for s_val in surprises if s_val < 0)
    if miss_count >= MAX_MISS_COUNT:
        return f"連續 miss {miss_count}/4 quarters"

    # Both FY0 and FY1 30d revision < -5% → analyst 急速下修
    fy0_curr = ed.get("fy0_curr")
    fy0_30d = ed.get("fy0_30d_ago")
    fy1_curr = ed.get("fy1_curr")
    fy1_30d = ed.get("fy1_30d_ago")
    fy0_rev_30d = _safe_rev_pct(fy0_curr, fy0_30d)
    fy1_rev_30d = _safe_rev_pct(fy1_curr, fy1_30d)
    if (fy0_rev_30d is not None and fy0_rev_30d < VETO_REVISION_BOTH
            and fy1_rev_30d is not None and fy1_rev_30d < VETO_REVISION_BOTH):
        return (f"急速下修 FY0 {fy0_rev_30d:.1f}% / FY1 {fy1_rev_30d:.1f}% (30d < {VETO_REVISION_BOTH}%)")

    return None


# ── rationale strings ─────────────────────────────────────────────────────────
def ea_rationale(a_breakdown: dict, b_breakdown: dict) -> str:
    """Tier A rationale.

    Example: FY0 +3.1% / FY1 +5.2% (30d) | beat 4/4, latest +6.3%, accel +1.2pp/q
    """
    parts: list[str] = []

    fy0_30 = a_breakdown.get("fy0_rev_30d")
    fy1_30 = a_breakdown.get("fy1_rev_30d")
    if fy0_30 is not None and fy1_30 is not None:
        sign0 = "+" if fy0_30 >= 0 else ""
        sign1 = "+" if fy1_30 >= 0 else ""
        parts.append(f"FY0 {sign0}{fy0_30:.1f}% / FY1 {sign1}{fy1_30:.1f}% (30d)")
    elif fy0_30 is not None:
        sign0 = "+" if fy0_30 >= 0 else ""
        parts.append(f"FY0 {sign0}{fy0_30:.1f}% (30d)")

    beat_count = b_breakdown.get("beat_count")
    latest = b_breakdown.get("latest_surprise")
    slope = b_breakdown.get("slope")
    if beat_count is not None and latest is not None:
        sign_l = "+" if latest >= 0 else ""
        accel_str = ""
        if slope is not None:
            sign_s = "+" if slope >= 0 else ""
            accel_str = f", accel {sign_s}{slope:.1f}pp/q"
        parts.append(f"beat {beat_count}/4, latest {sign_l}{latest:.1f}%{accel_str}")

    return " | ".join(parts) if parts else "—"


def _ea_wait_hint(a_score: float, b_score: float,
                  a_breakdown: dict, b_breakdown: dict) -> str:
    """Tier B 「等什麼」hint: find the weaker pillar and give context."""
    fy0_30 = a_breakdown.get("fy0_rev_30d")
    latest = b_breakdown.get("latest_surprise")

    # If revision is the weaker engine
    if a_score < b_score or (a_score < TIER_A_REVISION_MIN):
        if fy0_30 is not None:
            sign = "+" if fy0_30 >= 0 else ""
            return f"等 analyst 開始上修（現 FY0 30d {sign}{fy0_30:.1f}%）"
        return "等 analyst 開始上修"

    # If beat is the weaker engine
    beat_count = b_breakdown.get("beat_count", 0)
    if b_score < TIER_A_BEAT_MIN:
        if beat_count is not None and beat_count >= 3 and latest is not None and latest < 0:
            sign = "+" if latest >= 0 else ""
            return f"近季 miss（{sign}{latest:.1f}%），等 reacceleration"
        if latest is not None:
            sign = "+" if latest >= 0 else ""
            return f"等下一季 beat（latest 是 {sign}{latest:.1f}%）"
        return "等下一季財報 beat"

    return "—"


# ── scoring ───────────────────────────────────────────────────────────────────
def score_ticker(s: dict, ed: Optional[dict]) -> Optional[dict]:
    """Return a scored row, or None if vetoed."""
    veto = is_vetoed(s, ed)
    if veto:
        return None

    a, a_breakdown = pillar_revision(ed)
    b, b_breakdown = pillar_beat(ed)
    c, c_breakdown = pillar_floor(s)

    final = (PILLAR_WEIGHTS["revision"] * a
             + PILLAR_WEIGHTS["beat"] * b
             + PILLAR_WEIGHTS["floor"] * c)

    breakdown = {
        "revision": a_breakdown,
        "beat": b_breakdown,
        "floor": c_breakdown,
    }

    tier = None
    if final >= TIER_FINAL_MIN:
        if a >= TIER_A_REVISION_MIN and b >= TIER_A_BEAT_MIN:
            tier = "A"
        else:
            tier = "B"

    rationale = ea_rationale(a_breakdown, b_breakdown) if tier == "A" else None
    wait_hint = _ea_wait_hint(a, b, a_breakdown, b_breakdown) if tier == "B" else None

    return {
        "ticker": s["ticker"],
        "name": s.get("name", ""),
        "sector": s.get("sector", ""),
        "final": round(final, 4),
        "revision": round(a, 4),
        "beat": round(b, 4),
        "floor": round(c, 4),
        "tier": tier,
        "breakdown": breakdown,
        "rationale": rationale,
        "wait_hint": wait_hint,
        # surface raw fields for display
        "moat_grade": s.get("moat_grade"),
        "moat_score": s.get("moat_score"),
        "signal": s.get("signal"),
        "val": s.get("val"),
        "ai_risk": s.get("ai_risk"),
        "fpe_fy2": s.get("fpe_fy2"),
        "pass_count": s.get("pass_count"),
        "quality_score": s.get("quality_score"),
        "eps_revision_pct": s.get("eps_revision_pct"),
        "dd_path": s.get("dd_path"),
        "dca_path": s.get("dca_path"),
        # timing raw for display / tags
        "dist_52w_high_pct": (s.get("timing") or {}).get("dist_52w_high_pct"),
        "rs_score": (s.get("timing") or {}).get("rs_score"),
    }


# ── build pipeline ────────────────────────────────────────────────────────────
def build_pipeline(max_workers: int = 4, top: Optional[int] = None) -> dict:
    print(f"=== Earnings Acceleration build · {_now_taipei_iso()} ===\n")
    if not LATEST_JSON.exists():
        print(f"  ERR: {LATEST_JSON} not found — run scripts/build_dd_screener.py first",
              file=sys.stderr)
        sys.exit(2)

    data = json.loads(LATEST_JSON.read_text(encoding="utf-8"))
    universe = data.get("stocks", []) or []
    schema_ver = data.get("schema_version", "?")
    as_of = data.get("as_of", _today())
    print(f"  Loaded latest.json schema_version={schema_ver} as_of={as_of} "
          f"universe={len(universe)} stocks")

    if top:
        print(f"  (--top {top}: limiting to first {top} tickers)")
        universe = universe[:top]

    # ── Phase 1: fetch all earnings data ─────────────────────────────────────
    print(f"\n  Phase 1 — yfinance fetch ({len(universe)} tickers, {max_workers} workers)...")
    earnings_map = _fetch_all_earnings(universe, max_workers=max_workers)

    eps_trend_ok = sum(1 for ed in earnings_map.values() if ed is not None)
    eps_trend_fail = sum(1 for ed in earnings_map.values() if ed is None)
    hist_4q_ok = sum(
        1 for ed in earnings_map.values()
        if ed is not None and len(ed.get("surprises", [])) >= 4
    )
    print(f"\n  Data coverage:")
    print(f"    eps_trend valid:      {eps_trend_ok}/{len(universe)}")
    print(f"    4q earnings_history:  {hist_4q_ok}/{len(universe)}")
    print(f"    fetch failures:       {eps_trend_fail}/{len(universe)}")

    # ── Phase 2: score ────────────────────────────────────────────────────────
    scored: list[dict] = []
    vetoed: list[tuple[str, str]] = []
    pillar_counts = {"strong_revision": 0, "strong_beat": 0, "solid_floor": 0}
    veto_reasons: dict[str, int] = {}

    for s in universe:
        ticker = s.get("ticker", "?")
        ed = earnings_map.get(ticker)
        veto = is_vetoed(s, ed)
        if veto:
            vetoed.append((ticker, veto))
            key = veto.split(" ")[0] if " " in veto else veto
            veto_reasons[key] = veto_reasons.get(key, 0) + 1
            continue
        row = score_ticker(s, ed)
        if row is not None:
            scored.append(row)
            if row["revision"] >= 0.5:
                pillar_counts["strong_revision"] += 1
            if row["beat"] >= 0.5:
                pillar_counts["strong_beat"] += 1
            if row["floor"] >= 0.5:
                pillar_counts["solid_floor"] += 1

    # Sort by Final desc, then Revision desc as tie-breaker
    scored.sort(key=lambda r: (-r["final"], -r["revision"], r["ticker"]))

    tier_a = [r for r in scored if r["tier"] == "A"]
    tier_b = [r for r in scored if r["tier"] == "B"]

    # Display: Tier A all + Tier B fills to 25 total
    display_a = tier_a[:]
    remaining = max(0, DISPLAY_TOTAL - len(display_a))
    display_b = tier_b[:remaining]

    print(f"\n  Scored: {len(scored)} (vetoed {len(vetoed)})")
    print(f"  Pillar coverage (scored): revision≥0.5: {pillar_counts['strong_revision']} | "
          f"beat≥0.5: {pillar_counts['strong_beat']} | "
          f"floor≥0.5: {pillar_counts['solid_floor']}")
    print(f"  Tier A (Earnings Re-rating):    {len(tier_a)} (display {len(display_a)})")
    print(f"  Tier B (Single-Engine Watch):   {len(tier_b)} (display {len(display_b)})")
    if vetoed:
        veto_sample = vetoed[:10]
        print(f"  Veto sample: {veto_sample}")
    if veto_reasons:
        sorted_reasons = sorted(veto_reasons.items(), key=lambda x: -x[1])
        print(f"  Veto breakdown: {sorted_reasons[:8]}")

    return {
        "schema_version": SCHEMA_VERSION,
        "run_timestamp": _now_taipei_iso(),
        "as_of": as_of,
        "universe_total": len(universe),
        "eligible_total": len(scored),
        "vetoed_count": len(vetoed),
        "eps_trend_ok": eps_trend_ok,
        "hist_4q_ok": hist_4q_ok,
        "fetch_failures": eps_trend_fail,
        "pillar_weights": PILLAR_WEIGHTS,
        "thresholds": {
            "final_min": TIER_FINAL_MIN,
            "tier_a_revision_min": TIER_A_REVISION_MIN,
            "tier_a_beat_min": TIER_A_BEAT_MIN,
            "moat_score_min": MOAT_SCORE_MIN,
            "max_miss_count": MAX_MISS_COUNT,
            "veto_revision_both": VETO_REVISION_BOTH,
        },
        "tier_a": display_a,
        "tier_b": display_b,
        "tier_a_overflow": len(tier_a) - len(display_a),
        "tier_b_overflow": len(tier_b) - len(display_b),
    }


# ── HTML rendering ────────────────────────────────────────────────────────────
def _fmt_pct(v: Optional[float], decimals: int = 1) -> str:
    if v is None:
        return "—"
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.{decimals}f}%"


def _fmt_score(v: float) -> str:
    return f"{v:.2f}"


def _ticker_link(row: dict) -> str:
    dd = row.get("dd_path")
    label = row["ticker"]
    if dd:
        return f'<a href="{dd}">{label}</a>'
    return label


def _row_html_tier_a(row: dict) -> str:
    moat_grade = row.get("moat_grade") or ""
    fpe = row.get("fpe_fy2")
    fpe_str = f"{fpe:.1f}" if fpe is not None else "—"
    dist = row.get("dist_52w_high_pct")
    rs = row.get("rs_score")
    dist_str = f"{dist:.0f}%" if dist is not None else "—"
    rs_str = f"{rs:.0f}" if rs is not None else "—"
    rationale = row.get("rationale") or "—"
    return f"""<tr data-ticker="{row['ticker']}">
  <td class="left">{_ticker_link(row)}</td>
  <td class="score-cell"><strong>{_fmt_score(row['final'])}</strong></td>
  <td class="rev-cell">{_fmt_score(row['revision'])}</td>
  <td class="beat-cell">{_fmt_score(row['beat'])}</td>
  <td>{_fmt_score(row['floor'])}</td>
  <td class="left rationale-cell">{rationale}</td>
  <td class="meta-cell">{moat_grade} · {row.get('signal','')} · PE {fpe_str}x · dist {dist_str} · RS {rs_str}</td>
</tr>"""


def _row_html_tier_b(row: dict) -> str:
    moat_grade = row.get("moat_grade") or ""
    fpe = row.get("fpe_fy2")
    fpe_str = f"{fpe:.1f}" if fpe is not None else "—"
    wait = row.get("wait_hint") or "—"
    return f"""<tr data-ticker="{row['ticker']}">
  <td class="left">{_ticker_link(row)}</td>
  <td class="score-cell"><strong>{_fmt_score(row['final'])}</strong></td>
  <td class="rev-cell">{_fmt_score(row['revision'])}</td>
  <td class="beat-cell beat-low">{_fmt_score(row['beat'])}</td>
  <td>{_fmt_score(row['floor'])}</td>
  <td class="left wait-cell">{wait}</td>
  <td class="meta-cell">{moat_grade} · {row.get('signal','')} · PE {fpe_str}x</td>
</tr>"""


def _section_table(rows: list[dict], renderer, empty_msg: str) -> str:
    if not rows:
        return f'<div class="empty-row">{empty_msg}</div>'
    body = "\n".join(renderer(r) for r in rows)
    return f"""<table>
<thead>
<tr>
  <th class="left">Ticker</th>
  <th>Final</th>
  <th>Revision</th>
  <th>Beat</th>
  <th>Floor</th>
  <th class="left">Rationale / 等什麼</th>
  <th class="left">Tags</th>
</tr>
</thead>
<tbody>
{body}
</tbody>
</table>"""


def _fmt_taipei_stamp(iso_str: Optional[str]) -> str:
    if not iso_str or "T" not in iso_str:
        return iso_str or "—"
    date, time_part = iso_str.split("T", 1)
    return f"{date} {time_part[:5]}"


def render_html(doc: dict, out_path: Path) -> None:
    as_of = doc["as_of"]
    run_ts_display = _fmt_taipei_stamp(doc.get("run_timestamp"))
    universe_total = doc["universe_total"]
    eligible_total = doc["eligible_total"]
    vetoed_count = doc["vetoed_count"]
    tier_a = doc["tier_a"]
    tier_b = doc["tier_b"]
    tier_a_overflow = doc["tier_a_overflow"]
    tier_b_overflow = doc["tier_b_overflow"]
    eps_trend_ok = doc.get("eps_trend_ok", "—")
    hist_4q_ok = doc.get("hist_4q_ok", "—")

    tier_a_html = _section_table(
        tier_a, _row_html_tier_a,
        '尚無 Tier A 標的。目前 universe 中，EPS 上修動能 (A ≥ 0.60) 與財報 beat 記錄 (B ≥ 0.55) 雙重到位的標的不足。'
        '請查看 Tier B 或等待分析師上修 cycle 啟動。'
    )
    tier_b_html = _section_table(
        tier_b, _row_html_tier_b,
        '尚無 Tier B 標的。'
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Earnings Acceleration — EPS 加速 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f5f0fb;color:#1e1040;line-height:1.5}}
.hero{{background:#fff;border-bottom:1px solid #e9d5ff;padding:24px 32px 18px}}
.hero-inner{{max-width:min(1400px,96vw);margin:0 auto}}
.hero-h1{{font-size:22px;font-weight:600;color:#3b0764;margin-bottom:6px}}
.hero-sub{{font-size:12px;color:#7e22ce;line-height:1.6;max-width:920px}}
.hero-stats{{display:flex;gap:14px;margin-top:12px;flex-wrap:wrap}}
.hero-stat{{background:#faf5ff;border:1px solid #e9d5ff;border-radius:6px;padding:7px 11px;font-size:11px;color:#6b21a8}}
.hero-stat strong{{color:#3b0764;font-size:13px;display:block;margin-bottom:1px}}
.section{{max-width:min(1400px,96vw);margin:0 auto;padding:24px 32px}}
.formula-panel{{background:#fff;border:1px solid #e9d5ff;border-radius:10px;padding:14px 18px;margin-bottom:20px}}
.formula-panel h3{{font-size:13px;font-weight:700;color:#3b0764;margin-bottom:8px}}
.formula-panel code{{background:#faf5ff;padding:1px 6px;border-radius:3px;font-size:11.5px;color:#3b0764}}
.formula-row{{font-size:12px;color:#4a044e;line-height:1.85}}
.tier-card{{background:#fff;border:1px solid #e9d5ff;border-radius:10px;padding:16px 18px;margin-bottom:22px}}
.tier-card h2{{font-size:16px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.tier-card.tier-a h2{{color:#7e22ce}}
.tier-card.tier-b h2{{color:#7c3aed}}
.tier-card h2 .badge{{display:inline-block;padding:2px 9px;border-radius:5px;font-size:11px;font-weight:700}}
.tier-card.tier-a h2 .badge{{background:#f3e8ff;color:#7e22ce}}
.tier-card.tier-b h2 .badge{{background:#ede9fe;color:#a78bfa}}
.tier-card .desc{{font-size:12px;color:#6b21a8;margin-bottom:10px;line-height:1.6}}
.tier-card table{{width:100%;border-collapse:collapse;font-size:12px}}
.tier-card th{{background:#faf5ff;color:#6b21a8;font-weight:700;padding:8px 10px;text-align:right;border-bottom:2px solid #e9d5ff;font-size:10px;letter-spacing:.04em;text-transform:uppercase}}
.tier-card th.left{{text-align:left}}
.tier-card td{{padding:8px 10px;text-align:right;border-bottom:1px solid #faf5ff;font-variant-numeric:tabular-nums}}
.tier-card td.left{{text-align:left;color:#1e1040;font-weight:500}}
.tier-card td.left .sub{{font-size:10px;color:#a78bfa;font-weight:400;margin-top:1px}}
.tier-card td a{{color:#7e22ce;text-decoration:none;font-weight:700}}
.tier-card td a:hover{{text-decoration:underline}}
.score-cell{{color:#1e1040}}
.rev-cell{{color:#7e22ce;font-weight:600}}
.beat-cell{{color:#6d28d9;font-weight:600}}
.beat-low{{color:#a78bfa}}
.rationale-cell{{color:#3b0764;font-size:11px}}
.wait-cell{{color:#7c3aed;font-size:11px}}
.meta-cell{{font-size:10.5px;color:#6b21a8;text-align:left !important}}
.empty-row{{padding:14px;text-align:center;color:#a78bfa;font-size:12px;font-style:italic}}
.caveat-panel{{background:#faf5ff;border:1px solid #d8b4fe;border-radius:8px;padding:14px 18px;margin-bottom:20px;font-size:12px;color:#3b0764;line-height:1.65}}
.caveat-panel strong{{color:#7e22ce;display:block;margin-bottom:6px}}
.caveat-panel ul{{margin-left:18px}}
.confluence-bar{{background:#faf5ff;border:1px solid #e9d5ff;border-radius:10px;padding:12px 16px;margin-bottom:18px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.conf-label{{font-size:11px;color:#7e22ce;font-weight:600;margin-right:6px}}
.conf-chip{{padding:5px 12px;border-radius:999px;border:1px solid #d8b4fe;background:#fff;color:#7e22ce;font-size:11.5px;font-weight:600;cursor:pointer;font-family:inherit;transition:all .15s}}
.conf-chip:hover{{border-color:#9333ea;background:#f3e8ff}}
.conf-chip.active{{background:#9333ea;color:#fff;border-color:#9333ea}}
.conf-count{{font-weight:700;margin-left:5px;opacity:0.85;font-size:10.5px}}
.conf-status{{font-size:11px;color:#94a3b8;margin-left:auto;font-style:italic}}
.footer{{padding:30px 32px;font-size:11px;color:#6b21a8;line-height:1.7;max-width:min(1400px,96vw);margin:0 auto;border-top:1px solid #e9d5ff}}
.footer h4{{color:#3b0764;font-size:12px;margin-top:14px;margin-bottom:6px;font-weight:700}}
.footer code{{background:#faf5ff;padding:1px 5px;border-radius:3px;font-size:10px;color:#3b0764}}
</style>
</head>
<body>
{NAV_BLOCK}

<div class="hero">
  <div class="hero-inner">
    <div class="hero-h1">Earnings Acceleration — EPS 加速篩選</div>
    <div class="hero-sub">
      鎖定<b>分析師上修中（EPS revision↑）+ 財報持續 beat</b>的基本面加速標的。
      三支柱複合分數：Revision Momentum（50%）/ Beat Track Record（30%）/ Quality Floor（20%）。
      Tier A 是「雙引擎加速（上修 + beat 並行）」，Tier B 是「單引擎強但另一面尚未到位」。
      與 <a href="/dd-screener/quality-entry.html" style="color:#7e22ce">Quality-Entry</a> /
      <a href="/dd-screener/breakout.html" style="color:#7e22ce">Breakout</a> 可交叉使用——
      EA 篩基本面，timing screener 篩買點，兩個 Tier A 同時出現 = 高 conviction setup。
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>{run_ts_display}</strong>最後更新（台北）</div>
      <div class="hero-stat"><strong>{universe_total}</strong>universe</div>
      <div class="hero-stat"><strong>{eligible_total}</strong>通過 veto</div>
      <div class="hero-stat"><strong>{vetoed_count}</strong>被 veto</div>
      <div class="hero-stat"><strong>{eps_trend_ok}</strong>eps_trend 有效</div>
      <div class="hero-stat"><strong>{hist_4q_ok}</strong>4Q history 有效</div>
      <div class="hero-stat"><strong>{len(tier_a)}</strong>Tier A — Re-rating</div>
      <div class="hero-stat"><strong>{len(tier_b)}</strong>Tier B — Single-Engine</div>
    </div>
  </div>
</div>

<div class="section">

  <div class="formula-panel">
    <h3>方法論</h3>
    <div class="formula-row">
      <b>Final</b> = 0.50·<b>Revision</b> + 0.30·<b>Beat</b> + 0.20·<b>Floor</b>
    </div>
    <div class="formula-row" style="margin-top:6px">
      <b>Revision Momentum（分析師上修）</b>：<code>0.30·fy0_rev_30d + 0.20·fy0_rev_90d + 0.30·fy1_rev_30d + 0.20·fy1_rev_90d</code>
      — Λ 函數：−5%→0、0%→0.4、+2%→0.7、+5%→1.0（cap）。30d &gt; 90d 權重（recency）。
    </div>
    <div class="formula-row">
      <b>Beat Track Record（財報 beat）</b>：<code>0.25·beat_count + 0.30·beat_accel + 0.25·latest_beat + 0.20·consistency</code>
      — 過去 4 季 surprisePercent 驅動；accel = linreg slope。
    </div>
    <div class="formula-row">
      <b>Floor（品質地板）</b>：<code>0.40·moat/10 + 0.30·pass/5 + 0.15·quality/10 + 0.15·eps_rev_safety</code>
    </div>
    <div class="formula-row" style="margin-top:8px;color:#6b21a8">
      <b>Vetoes</b>：<code>ai_risk==🔴</code> · <code>moat_grade∈(C,X)</code> · <code>trap==🔴</code> · <code>moat_score&lt;6</code> ·
      <code>EPS data缺失</code> · <code>miss≥2/4q</code> · <code>FY0+FY1 30d均&lt;−5%</code>
    </div>
    <div class="formula-row" style="color:#6b21a8">
      <b>Tier 切分</b>：Final ≥ {TIER_FINAL_MIN}；A ≥ {TIER_A_REVISION_MIN} AND B ≥ {TIER_A_BEAT_MIN} → Tier A；否則 Tier B
    </div>
  </div>

  <div class="caveat-panel">
    <strong>&#128161; Factor Strategy — 使用前必讀</strong>
    <ul>
      <li><b>Timing-agnostic</b>：EA 不告訴你「現在能不能買」，只告訴你「基本面在加速」。Tier A 標的可能在 ATH 也可能在 −40% 深跌位置。</li>
      <li><b>Lagged signal</b>：EPS 上修 + beat 都是 backward-looking。市場可能已 priced-in fundamentals strength。配合 valuation pillar（PEG / pct_5y）一起看。</li>
      <li><b>Pair with timing screener</b>：最佳用法：EA Tier A 篩出基本面加速，再 cross-reference 是不是 also 在 Quality-Entry / Breakout Tier A → confluence = 高 conviction setup。</li>
      <li><b>跟其他 screener 重疊正常</b>：EA 跟 quality-entry / bottom-out / breakout 的 overlap 是 feature 不是 bug — EA 比 timing screener veto 更寬鬆，同檔可能同時上多個 screener。</li>
    </ul>
  </div>

  <div class="confluence-bar">
    <span class="conf-label">Confluence (× timing screener):</span>
    <button type="button" class="conf-chip active" data-conf="all">All <span class="conf-count">—</span></button>
    <button type="button" class="conf-chip" data-conf="breakout">× Breakout <span class="conf-count">—</span></button>
    <button type="button" class="conf-chip" data-conf="quality-entry">× Quality-Entry <span class="conf-count">—</span></button>
    <button type="button" class="conf-chip" data-conf="bottom-out">× Bottom-Out <span class="conf-count">—</span></button>
    <span class="conf-status">顯示中：<span id="conf-visible-count">—</span></span>
  </div>

  <div class="tier-card tier-a">
    <h2>&#128995; Tier A — Earnings Re-rating <span class="badge">Final ≥ {TIER_FINAL_MIN} · Revision ≥ {TIER_A_REVISION_MIN} · Beat ≥ {TIER_A_BEAT_MIN}</span></h2>
    <div class="desc">雙引擎到位：分析師持續上修（A ≥ {TIER_A_REVISION_MIN}）+ 財報持續 beat（B ≥ {TIER_A_BEAT_MIN}）。Rationale 欄顯示 FY0/FY1 30d revision % + beat 記錄關鍵數字。Tags 欄保留 dist_52w + RS 供 timing cross-reference。{f"（另有 {tier_a_overflow} 檔未顯示）" if tier_a_overflow > 0 else ""}</div>
    {tier_a_html}
  </div>

  <div class="tier-card tier-b">
    <h2>&#9898; Tier B — Single-Engine Watch <span class="badge">Final ≥ {TIER_FINAL_MIN} · A or B short</span></h2>
    <div class="desc">一邊強一邊尚未到位（revision 強但 beat 普通，或反過來）。「等什麼」欄點出弱側的具體等待條件。{f"（另有 {tier_b_overflow} 檔未顯示）" if tier_b_overflow > 0 else ""}</div>
    {tier_b_html}
  </div>

</div>

<div class="footer">
  <h4>數據來源</h4>
  <ul style="margin-left:18px">
    <li><code>docs/dd-screener/latest.json</code> v1.2+（moat_score / quality_score / ai_risk / eps_revision_pct 等 dd-meta propagated 欄位）</li>
    <li>yfinance <code>eps_trend</code>（current / 30daysAgo / 90daysAgo × FY0/FY1）— 每次 build 即時 fetch，內建歷史不需外部 snapshot</li>
    <li>yfinance <code>earnings_history</code>（過去 4 季 surprisePercent）— 每次 build 即時 fetch</li>
    <li>Revision Momentum 學術基礎：Womack (1996) / Stickel (1991) EPS revision alpha factor。Beat drift 基礎：Bernard &amp; Thomas SUE (1989) / Bloomberg ESS。</li>
  </ul>
  <h4>機器可讀</h4>
  <p>JSON sidecar: <a href="/dd-screener/earnings-acceleration.json"><code>/dd-screener/earnings-acceleration.json</code></a> · 每日快照: <code>/dd-screener/earnings-acceleration-snapshots/YYYY-MM-DD.json</code></p>
  <p style="margin-top:16px;color:#a78bfa">Generated by <code>scripts/build_earnings_acceleration.py</code> · schema v{SCHEMA_VERSION}</p>
</div>

<script>
// v1.0.2: Confluence filter — fetch sister screener JSONs, build ticker sets,
// chip-based filter on Tier A + Tier B tables. Lets user surface "EA × Breakout"
// (highest conviction: fundamentals strong + momentum confirmed) etc.
(function(){{
  var SISTER = {{
    'breakout': '/dd-screener/breakout.json',
    'quality-entry': '/dd-screener/quality-entry.json',
    'bottom-out': '/dd-screener/bottom-out.json'
  }};
  var sets = {{ breakout: null, 'quality-entry': null, 'bottom-out': null }};
  var rows = Array.prototype.slice.call(document.querySelectorAll('.tier-card tbody tr[data-ticker]'));
  var chips = document.querySelectorAll('.conf-chip');
  var visibleEl = document.getElementById('conf-visible-count');

  function applyFilter(confKey) {{
    chips.forEach(function(c){{ c.classList.toggle('active', c.dataset.conf === confKey); }});
    var visible = 0;
    rows.forEach(function(tr){{
      var t = tr.dataset.ticker;
      var show = confKey === 'all' || (sets[confKey] && sets[confKey].has(t));
      tr.style.display = show ? '' : 'none';
      if (show) visible++;
    }});
    if (visibleEl) visibleEl.textContent = visible + ' / ' + rows.length;
  }}

  function updateChipCount(key, count) {{
    var chip = document.querySelector('[data-conf="' + key + '"] .conf-count');
    if (chip) chip.textContent = count;
  }}

  // Initial: show all + update "All" count
  updateChipCount('all', rows.length);
  if (visibleEl) visibleEl.textContent = rows.length + ' / ' + rows.length;

  // Fetch sister sets (Tier A only — highest conviction)
  Object.keys(SISTER).forEach(function(key){{
    fetch(SISTER[key]).then(function(r){{ return r.json(); }}).then(function(data){{
      var tier_a = data.tier_a || [];
      sets[key] = new Set(tier_a.map(function(r){{ return r.ticker; }}));
      var count = rows.filter(function(tr){{ return sets[key].has(tr.dataset.ticker); }}).length;
      updateChipCount(key, count);
    }}).catch(function(){{ updateChipCount(key, 'n/a'); }});
  }});

  chips.forEach(function(c){{ c.addEventListener('click', function(){{ applyFilter(c.dataset.conf); }}); }});
}})();
</script>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✓ Wrote {out_path} ({out_path.stat().st_size:,} bytes)")


# ── main ──────────────────────────────────────────────────────────────────────
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Don't write files")
    p.add_argument("--no-snapshot", action="store_true", help="Skip daily snapshot write")
    p.add_argument("--max-workers", type=int, default=4,
                   help="Concurrent yfinance fetchers (default 4)")
    p.add_argument("--top", type=int, default=None,
                   help="Limit to first N tickers (smoke test)")
    args = p.parse_args()

    doc = build_pipeline(max_workers=args.max_workers, top=args.top)

    if args.dry_run:
        print("\n  (dry-run) skipping writes")
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  ✓ Wrote {JSON_OUT} ({JSON_OUT.stat().st_size:,} bytes)")

    render_html(doc, HTML_OUT)

    if not args.no_snapshot:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        snap_path = SNAPSHOT_DIR / f"{_today()}.json"
        snap_path.write_text(
            json.dumps(doc, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  ✓ Wrote snapshot {snap_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
