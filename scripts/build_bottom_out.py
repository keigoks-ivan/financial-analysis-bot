#!/usr/bin/env python3
"""Bottom-Out Screener — 深回檔 + 觸底反彈訊號 + 不是落下的刀 (Drawdown / Reversal / Floor).

設計 source-of-truth: /Users/ivanchang/.claude/plans/yfinance-eps-zippy-frost.md

Pipeline:
  1. 讀 docs/dd-screener/latest.json (v1.2+, 已含 pct_5y / quality_score / ai_risk / 等)
  2. 每檔套 vetoes (ai_risk 🔴 / moat_grade C/X / trap 🔴 / dist_52w > -15 /
     eps_revision_pct < -30 / moat_score < 6)
  3. 算 A (Drawdown depth) / B (Reversal signal) / C (Not-broken floor) 三支柱
     Final = 0.40·A + 0.35·B + 0.25·C
  4. Tier 切分：
       Tier A — Reversal Confirmed:  Final ≥ 0.65  AND  B (Reversal) ≥ 0.60
       Tier B — Deep Value Watch:    Final ≥ 0.65  AND  B < 0.60
  5. 取 Tier A 全部 + Tier B 補到合計 25 檔
  6. 寫 docs/dd-screener/bottom-out.{html,json} + 每日 snapshot

Usage:
  python3 scripts/build_bottom_out.py
  python3 scripts/build_bottom_out.py --dry-run     # 不寫檔
  python3 scripts/build_bottom_out.py --no-snapshot # 不寫 daily snapshot
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# Shared Excel-coverage helpers (v1.x: Excel-only growth signal)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dd_screener_quality import has_excel_cagr, cagr_growth_score  # noqa: E402
from site_nav import DD_SCREENER_SUBNAV, build_subnav, full_nav_block  # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
LATEST_JSON = ROOT / "docs" / "dd-screener" / "latest.json"
OUTPUT_DIR = ROOT / "docs" / "dd-screener"
HTML_OUT = OUTPUT_DIR / "bottom-out.html"
JSON_OUT = OUTPUT_DIR / "bottom-out.json"
SNAPSHOT_DIR = OUTPUT_DIR / "bottom-out-snapshots"

# Canonical site header + dd-screener sub-nav (single source: scripts/site_nav.py)
NAV_BLOCK = full_nav_block(
    "pick", "dds", build_subnav(DD_SCREENER_SUBNAV, "/dd-screener/bottom-out.html")
)

TAIPEI_TZ = timezone(timedelta(hours=8))
SCHEMA_VERSION = "1.0"

# ── scoring constants ─────────────────────────────────────────────────────────
PILLAR_WEIGHTS = {"drawdown": 0.40, "reversal": 0.35, "floor": 0.25}

# Tier 門檻
TIER_FINAL_MIN = 0.65
TIER_A_REVERSAL_MIN = 0.60
DISPLAY_TOTAL = 25  # Tier A 全部 + Tier B 補到合計 25

# Veto: 跌幅門檻（不夠深 → quality-entry 去處理）
DIST_VETO_THRESHOLD = -15.0
# Veto: EPS 修正下限（分析師大幅砍 → falling knife）
EPS_REV_VETO_THRESHOLD = -30.0
# Veto: 護城河最低分（避免弱護城河體質的「反彈陷阱」）
MOAT_SCORE_MIN = 6

# Val emoji → numeric
VAL_NUM = {"🟢": 1.0, "🟡": 0.6, "🟠": 0.3, "🔴": 0.0}

# Moat grade → numeric (純展示用)
MOAT_GRADE_NUM = {"S": 5, "A": 4, "B": 3, "C": 2, "X": 1}


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


# ── score curves (Λ functions) ────────────────────────────────────────────────
def drawdown_sweet_spot(dist_52w_high_pct: Optional[float]) -> float:
    """Λ function on dist_52w_high_pct (negative = below 52w high).

    Sweet spot: -30% to -40% (score 1.0).
    Too shallow (> -15%): vetoed upstream, so returns 0 here as safety.
    Too deep (< -70%): capitulation / broken thesis territory, score 0.1.

    Anchor points per plan:
      > -15%   → 0   (vetoed upstream)
      -20%     → 0.4
      -25%     → 0.7
      -30% to -40% → 1.0
      -50%     → 0.7
      -60%     → 0.4
      < -70%   → 0.1
    """
    if dist_52w_high_pct is None:
        return 0.3  # neutral — missing data
    d = dist_52w_high_pct
    if d > -15:
        return 0.0  # vetoed, but safety guard
    if d >= -20:
        # -15 → 0; -20 → 0.4 (linear interpolation)
        return 0.0 + (-d - 15) / 5 * 0.4
    if d >= -25:
        # -20 → 0.4; -25 → 0.7
        return 0.4 + (-d - 20) / 5 * 0.3
    if d >= -30:
        # -25 → 0.7; -30 → 1.0
        return 0.7 + (-d - 25) / 5 * 0.3
    if d >= -40:
        # -30 → 1.0; -40 → 1.0 (plateau)
        return 1.0
    if d >= -50:
        # -40 → 1.0; -50 → 0.7
        return 1.0 - (-d - 40) / 10 * 0.3
    if d >= -60:
        # -50 → 0.7; -60 → 0.4
        return 0.7 - (-d - 50) / 10 * 0.3
    if d >= -70:
        # -60 → 0.4; -70 → 0.1
        return 0.4 - (-d - 60) / 10 * 0.3
    return 0.1  # < -70%: capitulation


def drift_4w_score(drift_4w_pct: Optional[float]) -> float:
    """Λ on drift_4w_pct. Peaks at +5 to +15% (early recovery, not overheated).

    Anchor points per plan:
      < -5%     → 0
      0%        → 0.3
      +5% to +15% → 1.0 (peak)
      +25%      → 0.5
      > +30%    → 0.2 (already bounced hard)
    """
    if drift_4w_pct is None:
        return 0.3
    v = drift_4w_pct
    if v < -5:
        return 0.0
    if v < 0:
        # -5 → 0; 0 → 0.3
        return 0.0 + (v + 5) / 5 * 0.3
    if v <= 5:
        # 0 → 0.3; +5 → 1.0
        return 0.3 + v / 5 * 0.7
    if v <= 15:
        return 1.0  # plateau peak
    if v <= 25:
        # +15 → 1.0; +25 → 0.5
        return 1.0 - (v - 15) / 10 * 0.5
    if v <= 30:
        # +25 → 0.5; +30 → 0.2
        return 0.5 - (v - 25) / 5 * 0.3
    return 0.2  # > +30%: already bounced hard


def ma_slope_score(slope_w250_pct: Optional[float]) -> float:
    """slope_w250_pct — flattening / turning positive = bullish reversal signal.

    Anchor points per plan:
      < -3      → 0   (still steeply declining)
      -3 to 0   → 0.5 (flattening = early reversal)
      0 to +3   → 0.8 (just turned positive = good)
      > +3      → 0.6 (already recovering — less pure reversal signal)
    """
    if slope_w250_pct is None:
        return 0.4
    s = slope_w250_pct
    if s < -3:
        return 0.0
    if s <= 0:
        # -3 → 0; 0 → 0.5
        return 0.0 + (s + 3) / 3 * 0.5
    if s <= 3:
        # 0 → 0.5; +3 → 0.8
        return 0.5 + s / 3 * 0.3
    # > +3
    return 0.6


def price_vs_ma50_score(ma50_pct: Optional[float]) -> float:
    """ma50_pct: % above/below MA50 (positive = above MA50).

    Sweet spot: 0 to +5% (just reclaimed MA50 = best signal).

    Anchor points per plan:
      < -10     → 0
      -10 to -5 → ramp to 0.4
      -5 to 0   → 0.8  (just below MA50, about to reclaim)
      0 to +5   → 1.0  (just reclaimed = best)
      +5 to +10 → 0.6
      +10 to +15 → 0.4
      > +15     → 0.2
    """
    if ma50_pct is None:
        return 0.4
    v = ma50_pct
    if v < -10:
        return 0.0
    if v < -5:
        # -10 → 0; -5 → 0.4
        return 0.0 + (v + 10) / 5 * 0.4
    if v < 0:
        # -5 → 0.4; 0 → 0.8
        return 0.4 + (v + 5) / 5 * 0.4
    if v <= 5:
        # 0 → 0.8; +5 → 1.0
        return 0.8 + v / 5 * 0.2
    if v <= 10:
        # +5 → 1.0; +10 → 0.6
        return 1.0 - (v - 5) / 5 * 0.4
    if v <= 15:
        # +10 → 0.6; +15 → 0.4
        return 0.6 - (v - 10) / 5 * 0.2
    return 0.2


def rs_recovery_score(rs_score: Optional[float]) -> float:
    """rs_score (0-100): moderate strength = bottoming; too strong = already recovered.

    Anchor points per plan:
      < 30      → 0.3
      30-50     → 0.6
      50-70     → 0.8
      > 70      → 0.4 (too strong = no longer bottoming)
    """
    if rs_score is None:
        return 0.4
    r = rs_score
    if r < 30:
        return 0.3
    if r < 50:
        # 30 → 0.3; 50 → 0.6 (linear)
        return 0.3 + (r - 30) / 20 * 0.3
    if r <= 70:
        # 50 → 0.6; 70 → 0.8
        return 0.6 + (r - 50) / 20 * 0.2
    # > 70: too strong
    return 0.4


def eps_rev_safety_score(eps_revision_pct: Optional[float]) -> float:
    """eps_revision_pct: EPS revision % (negative = analysts cutting).

    >= -10%   → 1.0
    -10 to -20% → 0.5
    -20 to -30% → 0.2
    < -30%    → vetoed upstream (0 here as safety)
    """
    if eps_revision_pct is None:
        return 0.7  # missing = neutral-positive (not being cut)
    e = eps_revision_pct
    if e >= -10:
        return 1.0
    if e >= -20:
        # -10 → 1.0; -20 → 0.5
        return 1.0 - (e + 10) / (-10) * 0.5
    if e >= -30:
        # -20 → 0.5; -30 → 0.2
        return 0.5 - (e + 20) / (-10) * 0.3
    return 0.0  # vetoed upstream


# ── pillars ───────────────────────────────────────────────────────────────────
def pillar_drawdown(s: dict) -> tuple[float, dict]:
    """A = drawdown_sweet_spot(dist_52w_high_pct)"""
    timing = s.get("timing") or {}
    dist = _safe_float(timing.get("dist_52w_high_pct"))
    score = drawdown_sweet_spot(dist)
    score = _clip01(score)
    return score, {"dist": dist, "drawdown_score": round(score, 3)}


def pillar_reversal(s: dict) -> tuple[float, dict]:
    """B = 0.35·drift_4w_score + 0.30·ma_slope_score
          + 0.20·price_vs_ma50_score + 0.15·rs_recovery_score"""
    ma = s.get("ma") or {}
    timing = s.get("timing") or {}

    d4w = _safe_float(ma.get("drift_4w_pct"))
    slope = _safe_float(ma.get("slope_w250_pct"))
    ma50 = _safe_float(timing.get("ma50_pct"))
    rs = _safe_float(timing.get("rs_score"))

    sd = drift_4w_score(d4w)
    ss = ma_slope_score(slope)
    sm = price_vs_ma50_score(ma50)
    sr = rs_recovery_score(rs)

    score = 0.35 * sd + 0.30 * ss + 0.20 * sm + 0.15 * sr
    score = _clip01(score)
    return score, {
        "drift_4w": d4w,
        "slope_w250": slope,
        "ma50_pct": ma50,
        "rs_score": rs,
        "drift_4w_score": round(sd, 3),
        "ma_slope_score": round(ss, 3),
        "price_vs_ma50_score": round(sm, 3),
        "rs_recovery_score": round(sr, 3),
    }


def pillar_floor(s: dict) -> tuple[float, dict]:
    """C = 0.40·moat/10 + 0.30·pass_count/5 + 0.15·quality_score/10 + 0.15·cagr_growth_score

    v1.x: 0.15 slot 從 eps_rev_safety (yfinance eps_revision_pct 30/90 天動能)
    換成 Excel forward CAGR (eps_fy1_fy3_cagr_pct, FY+1→FY+3 pure forward)。
    eps_revision_pct < -30% veto 保留作為論點破裂 thesis-break 早期警示。
    """
    moat = _safe_float(s.get("moat_score")) or 0
    pass_count = _safe_float(s.get("pass_count")) or 0
    qs = _safe_float(s.get("quality_score"))
    cagr = _safe_float(s.get("eps_fy1_fy3_cagr_pct"))

    moat_norm = moat / 10.0
    pass_norm = pass_count / 5.0
    quality_norm = (qs / 10.0) if qs is not None else moat_norm
    cagr_score = cagr_growth_score(cagr)

    score = 0.40 * moat_norm + 0.30 * pass_norm + 0.15 * quality_norm + 0.15 * cagr_score
    score = _clip01(score)
    return score, {
        "moat_norm": round(moat_norm, 3),
        "pass_norm": round(pass_norm, 3),
        "quality_norm": round(quality_norm, 3),
        "cagr_growth_score": round(cagr_score, 3),
        "cagr_fy1_fy3_pct": cagr,
    }


# ── vetoes ────────────────────────────────────────────────────────────────────
def is_vetoed(s: dict) -> Optional[str]:
    """Return veto reason string, or None if eligible."""
    if not has_excel_cagr(s):
        return "Excel EPS 覆蓋外"
    ai_risk = s.get("ai_risk")
    if ai_risk == "🔴":
        return "AI disrupt 🔴"
    moat_grade = s.get("moat_grade", "")
    if moat_grade in ("C", "X"):
        return f"護城河 {moat_grade}"
    trap = s.get("trap", "")
    if trap == "🔴":
        return "Trap 🔴"
    # Bottom-out specific vetoes
    timing = s.get("timing") or {}
    dist = _safe_float(timing.get("dist_52w_high_pct"))
    if dist is not None and dist > DIST_VETO_THRESHOLD:
        return f"跌幅不足 {dist:.1f}% (>{DIST_VETO_THRESHOLD}%)"
    eps_rev = _safe_float(s.get("eps_revision_pct"))
    if eps_rev is not None and eps_rev < EPS_REV_VETO_THRESHOLD:
        return f"EPS 修正 {eps_rev:.1f}% (<{EPS_REV_VETO_THRESHOLD}%)"
    moat_score = _safe_float(s.get("moat_score"))
    if moat_score is not None and moat_score < MOAT_SCORE_MIN:
        return f"護城河分 {moat_score:.0f} (<{MOAT_SCORE_MIN})"
    return None


# ── rationale strings ─────────────────────────────────────────────────────────
def bottom_rationale(s: dict, a_breakdown: dict, b_breakdown: dict) -> str:
    """Tier A rationale: dist / 4w drift / slope — 三段關鍵逆向訊號。

    Example: dist −34% / 4w +8% / slope +0.5%
    """
    parts: list[str] = []

    dist = a_breakdown.get("dist")
    if dist is not None:
        parts.append(f"dist {dist:.0f}%")

    drift_4w = b_breakdown.get("drift_4w")
    if drift_4w is not None:
        sign = "+" if drift_4w >= 0 else ""
        parts.append(f"4w {sign}{drift_4w:.0f}%")

    slope = b_breakdown.get("slope_w250")
    if slope is not None:
        sign = "+" if slope >= 0 else ""
        parts.append(f"slope {sign}{slope:.1f}%")

    return " / ".join(parts) if parts else "—"


def _reversal_wait_hint(b_breakdown: dict, floor_breakdown: dict) -> str:
    """Tier B 「等什麼」— 找 Reversal 和 Floor sub-score 的最大拖累。

    Logic: check drift_4w / ma_slope / price_vs_ma50 / cagr_growth_score
    sub-scores against their target weights to find biggest gap.
    """
    # Reversal sub-scores with their weights (within pillar B)
    reversal_weighted = {
        "drift_4w": b_breakdown.get("drift_4w_score", 0.5) * 0.35,
        "ma_slope": b_breakdown.get("ma_slope_score", 0.5) * 0.30,
        "price_vs_ma50": b_breakdown.get("price_vs_ma50_score", 0.5) * 0.20,
    }
    reversal_targets = {"drift_4w": 0.35, "ma_slope": 0.30, "price_vs_ma50": 0.20}
    reversal_gap = {k: reversal_targets[k] - reversal_weighted[k] for k in reversal_targets}

    # Floor: cagr_growth_score gap (check if forward growth is notably weak)
    cagr_safe = floor_breakdown.get("cagr_growth_score", 0.7)
    cagr_gap = 0.15 - cagr_safe * 0.15

    # Find the single biggest gap across reversal subs + cagr
    all_gaps = {**reversal_gap, "cagr": cagr_gap}
    bottleneck = max(all_gaps, key=all_gaps.get)

    # Build actionable hint
    drift = b_breakdown.get("drift_4w")
    slope = b_breakdown.get("slope_w250")
    ma50 = b_breakdown.get("ma50_pct")
    cagr_pct = floor_breakdown.get("cagr_fy1_fy3_pct")

    if bottleneck == "drift_4w":
        if drift is not None and drift < 0:
            return f"等 4w drift 轉正（現 {drift:.1f}%）"
        return "等 4w drift 轉正"
    if bottleneck == "ma_slope":
        if slope is not None:
            return f"等 MA250 趨平（現 {slope:.1f}%/w）"
        return "等 MA250 趨平"
    if bottleneck == "price_vs_ma50":
        if ma50 is not None and ma50 < 0:
            return f"等站回 MA50（現 {ma50:.1f}%）"
        return "等站回 MA50"
    if bottleneck == "cagr":
        if cagr_pct is not None:
            return f"等前瞻 CAGR 加速（現 {cagr_pct:.1f}%）"
        return "等前瞻 CAGR 加速"
    return "—"


# ── scoring ───────────────────────────────────────────────────────────────────
def score_ticker(s: dict) -> Optional[dict]:
    """Return a scored row, or None if vetoed."""
    veto = is_vetoed(s)
    if veto:
        return None

    a, a_breakdown = pillar_drawdown(s)
    b, b_breakdown = pillar_reversal(s)
    c, c_breakdown = pillar_floor(s)

    final = (PILLAR_WEIGHTS["drawdown"] * a
             + PILLAR_WEIGHTS["reversal"] * b
             + PILLAR_WEIGHTS["floor"] * c)

    breakdown = {
        "drawdown": a_breakdown,
        "reversal": b_breakdown,
        "floor": c_breakdown,
    }

    tier = None
    if final >= TIER_FINAL_MIN:
        tier = "A" if b >= TIER_A_REVERSAL_MIN else "B"

    rationale = bottom_rationale(s, a_breakdown, b_breakdown) if tier == "A" else None
    wait_hint = _reversal_wait_hint(b_breakdown, c_breakdown) if tier == "B" else None

    return {
        "ticker": s["ticker"],
        "name": s.get("name", ""),
        "sector": s.get("sector", ""),
        "final": round(final, 4),
        "drawdown": round(a, 4),
        "reversal": round(b, 4),
        "floor": round(c, 4),
        "tier": tier,
        "breakdown": breakdown,
        "rationale": rationale,
        "wait_hint": wait_hint,
        # surface raw fields for table display
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
        # timing raw for display
        "dist_52w_high_pct": (s.get("timing") or {}).get("dist_52w_high_pct"),
        "drift_4w_pct": (s.get("ma") or {}).get("drift_4w_pct"),
        "slope_w250_pct": (s.get("ma") or {}).get("slope_w250_pct"),
        "rs_score": (s.get("timing") or {}).get("rs_score"),
    }


# ── build pipeline ────────────────────────────────────────────────────────────
def build_pipeline() -> dict:
    print(f"=== Bottom-Out build · {_now_taipei_iso()} ===\n")
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

    scored: list[dict] = []
    vetoed: list[tuple[str, str]] = []
    pillar_counts = {"deep_enough": 0, "reversal_signal": 0, "strong_floor": 0}

    for s in universe:
        veto = is_vetoed(s)
        if veto:
            vetoed.append((s.get("ticker", "?"), veto))
            continue
        row = score_ticker(s)
        if row is not None:
            scored.append(row)
            if row["drawdown"] >= 0.5:
                pillar_counts["deep_enough"] += 1
            if row["reversal"] >= 0.5:
                pillar_counts["reversal_signal"] += 1
            if row["floor"] >= 0.5:
                pillar_counts["strong_floor"] += 1

    # rank by Final desc, then Reversal desc as tie-breaker
    scored.sort(key=lambda r: (-r["final"], -r["reversal"], r["ticker"]))

    tier_a = [r for r in scored if r["tier"] == "A"]
    tier_b = [r for r in scored if r["tier"] == "B"]

    # display: Tier A 全部 + Tier B 補到合計 25
    display_a = tier_a[:]
    remaining = max(0, DISPLAY_TOTAL - len(display_a))
    display_b = tier_b[:remaining]

    print(f"  Scored: {len(scored)} (vetoed {len(vetoed)})")
    print(f"  Pillar coverage (scored): drawdown≥0.5: {pillar_counts['deep_enough']} | "
          f"reversal≥0.5: {pillar_counts['reversal_signal']} | "
          f"floor≥0.5: {pillar_counts['strong_floor']}")
    print(f"  Tier A (Reversal Confirmed): {len(tier_a)} (display {len(display_a)})")
    print(f"  Tier B (Deep Value Watch):   {len(tier_b)} (display {len(display_b)})")
    if vetoed:
        veto_sample = vetoed[:8]
        print(f"  Veto sample: {veto_sample}")

    return {
        "schema_version": SCHEMA_VERSION,
        "run_timestamp": _now_taipei_iso(),
        "as_of": as_of,
        "universe_total": len(universe),
        "eligible_total": len(scored),
        "vetoed_count": len(vetoed),
        "pillar_weights": PILLAR_WEIGHTS,
        "thresholds": {
            "final_min": TIER_FINAL_MIN,
            "tier_a_reversal_min": TIER_A_REVERSAL_MIN,
            "dist_veto": DIST_VETO_THRESHOLD,
            "eps_rev_veto": EPS_REV_VETO_THRESHOLD,
            "moat_score_min": MOAT_SCORE_MIN,
        },
        "tier_a": display_a,
        "tier_b": display_b,
        "tier_a_overflow": len(tier_a) - len(display_a),
        "tier_b_overflow": len(tier_b) - len(display_b),
    }


# ── HTML rendering ────────────────────────────────────────────────────────────
def _fmt_pct(v: Optional[float], decimals: int = 0) -> str:
    if v is None:
        return "—"
    return f"{v:.{decimals}f}"


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
    drift = row.get("drift_4w_pct")
    dist_str = f"{dist:.0f}%" if dist is not None else "—"
    drift_str = (f"+{drift:.0f}%" if drift is not None and drift >= 0
                 else f"{drift:.0f}%" if drift is not None else "—")
    rationale = row.get("rationale") or "—"
    return f"""<tr>
  <td class="left">{_ticker_link(row)}</td>
  <td class="score-cell"><strong>{_fmt_score(row['final'])}</strong></td>
  <td class="drawdown-cell">{_fmt_score(row['drawdown'])}</td>
  <td class="reversal-cell">{_fmt_score(row['reversal'])}</td>
  <td>{_fmt_score(row['floor'])}</td>
  <td class="left rationale-cell">{rationale}</td>
  <td class="meta-cell">{moat_grade} · {row.get('signal','')} · PE {fpe_str}x</td>
</tr>"""


def _row_html_tier_b(row: dict) -> str:
    moat_grade = row.get("moat_grade") or ""
    fpe = row.get("fpe_fy2")
    fpe_str = f"{fpe:.1f}" if fpe is not None else "—"
    wait = row.get("wait_hint") or "—"
    return f"""<tr>
  <td class="left">{_ticker_link(row)}</td>
  <td class="score-cell"><strong>{_fmt_score(row['final'])}</strong></td>
  <td class="drawdown-cell">{_fmt_score(row['drawdown'])}</td>
  <td class="reversal-cell reversal-low">{_fmt_score(row['reversal'])}</td>
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
  <th>Drawdown</th>
  <th>Reversal</th>
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
    """Convert "2026-05-18T11:49:02+08:00" → "2026-05-18 11:49" for display."""
    if not iso_str or "T" not in iso_str:
        return iso_str or "—"
    date, time = iso_str.split("T", 1)
    return f"{date} {time[:5]}"


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

    tier_a_html = _section_table(
        tier_a, _row_html_tier_a,
        '尚無 Tier A 標的。市場可能整體偏熱（無深跌）或觸底反彈訊號尚未出現。'
        '請查看 Tier B 或等待更明確的 reversal 訊號。'
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
<title>Bottom-Out — 深回檔逆向訊號 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f0f5fb;color:#1e3a5f;line-height:1.5}}
.hero{{background:#fff;border-bottom:1px solid #dce8f5;padding:24px 32px 18px}}
.hero-inner{{max-width:min(1400px,96vw);margin:0 auto}}
.hero-h1{{font-size:22px;font-weight:600;color:#0f2a45;margin-bottom:6px}}
.hero-sub{{font-size:12px;color:#5a7a9a;line-height:1.6;max-width:920px}}
.hero-stats{{display:flex;gap:14px;margin-top:12px;flex-wrap:wrap}}
.hero-stat{{background:#f0f5fb;border:1px solid #dce8f5;border-radius:6px;padding:7px 11px;font-size:11px;color:#5a7a9a}}
.hero-stat strong{{color:#1e3a5f;font-size:13px;display:block;margin-bottom:1px}}
.section{{max-width:min(1400px,96vw);margin:0 auto;padding:24px 32px}}
.formula-panel{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:14px 18px;margin-bottom:20px}}
.formula-panel h3{{font-size:13px;font-weight:700;color:#0f2a45;margin-bottom:8px}}
.formula-panel code{{background:#f0f5fb;padding:1px 6px;border-radius:3px;font-size:11.5px;color:#1e3a5f}}
.formula-row{{font-size:12px;color:#334e68;line-height:1.85}}
.tier-card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:16px 18px;margin-bottom:22px}}
.tier-card h2{{font-size:16px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.tier-card.tier-a h2{{color:#c2410c}}
.tier-card.tier-b h2{{color:#475569}}
.tier-card h2 .badge{{display:inline-block;padding:2px 9px;border-radius:5px;font-size:11px;font-weight:700}}
.tier-card.tier-a h2 .badge{{background:#fed7aa;color:#c2410c}}
.tier-card.tier-b h2 .badge{{background:#e2e8f0;color:#475569}}
.tier-card .desc{{font-size:12px;color:#5a7a9a;margin-bottom:10px;line-height:1.6}}
.tier-card table{{width:100%;border-collapse:collapse;font-size:12px}}
.tier-card th{{background:#f0f6ff;color:#5a7a9a;font-weight:700;padding:8px 10px;text-align:right;border-bottom:2px solid #dce8f5;font-size:10px;letter-spacing:.04em;text-transform:uppercase}}
.tier-card th.left{{text-align:left}}
.tier-card td{{padding:8px 10px;text-align:right;border-bottom:1px solid #f0f5fb;font-variant-numeric:tabular-nums}}
.tier-card td.left{{text-align:left;color:#0f2a45;font-weight:500}}
.tier-card td.left .sub{{font-size:10px;color:#94a3b8;font-weight:400;margin-top:1px}}
.tier-card td a{{color:#2563eb;text-decoration:none;font-weight:700}}
.tier-card td a:hover{{text-decoration:underline}}
.score-cell{{color:#0f2a45}}
.drawdown-cell{{color:#c2410c;font-weight:600}}
.reversal-cell{{color:#9a3412;font-weight:600}}
.reversal-low{{color:#64748b}}
.rationale-cell{{color:#7c2d12;font-size:11px}}
.wait-cell{{color:#475569;font-size:11px}}
.meta-cell{{font-size:10.5px;color:#5a7a9a;text-align:left !important}}
.empty-row{{padding:14px;text-align:center;color:#94a3b8;font-size:12px;font-style:italic}}
.caveat-panel{{background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:14px 18px;margin-bottom:20px;font-size:12px;color:#9a3412;line-height:1.65}}
.caveat-panel strong{{color:#7c2d12;display:block;margin-bottom:6px}}
.caveat-panel ul{{margin-left:18px}}
.footer{{padding:30px 32px;font-size:11px;color:#5a7a9a;line-height:1.7;max-width:min(1400px,96vw);margin:0 auto;border-top:1px solid #dce8f5}}
.footer h4{{color:#1e3a5f;font-size:12px;margin-top:14px;margin-bottom:6px;font-weight:700}}
.footer code{{background:#f0f5fb;padding:1px 5px;border-radius:3px;font-size:10px;color:#1e3a5f}}
</style>
</head>
<body>
{NAV_BLOCK}

<div class="hero">
  <div class="hero-inner">
    <div class="hero-h1">Bottom-Out — 深回檔逆向訊號</div>
    <div class="hero-sub">
      鎖定<b>跌幅夠深（-25% ~ -45%）+ 出現觸底反彈訊號 + 尚有護城河地板</b>的標的。
      三支柱複合分數：Drawdown深度 40% / Reversal訊號 35% / Not-broken Floor 25%。
      屬<b>高風險逆向區</b>：Tier A 是「reversal 訊號已出現」的逆向機會，Tier B 是「跌夠深但尚未反轉」的 watchlist。
      與 <a href="/dd-screener/quality-entry.html" style="color:#2563eb">Quality-Entry</a> 互補不重疊（兩者 dist_52w 門檻互斥）。
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>{run_ts_display}</strong>最後更新（台北）</div>
      <div class="hero-stat"><strong>{universe_total}</strong>universe</div>
      <div class="hero-stat"><strong>{eligible_total}</strong>通過 veto</div>
      <div class="hero-stat"><strong>{vetoed_count}</strong>被 veto</div>
      <div class="hero-stat"><strong>{len(tier_a)}</strong>Tier A — Reversal Confirmed</div>
      <div class="hero-stat"><strong>{len(tier_b)}</strong>Tier B — Deep Value Watch</div>
    </div>
  </div>
</div>

<div class="section">

  <div class="formula-panel">
    <h3>方法論</h3>
    <div class="formula-row">
      <b>Final</b> = 0.40·<b>Drawdown</b> + 0.35·<b>Reversal</b> + 0.25·<b>Floor</b>
    </div>
    <div class="formula-row" style="margin-top:6px">
      <b>Drawdown (深度)</b>：<code>Λ(dist_52w_high_pct)</code> — 甜蜜點 −30% ~ −40%（1.0），兩側遞減；&lt;−70% 給 0.1（可能是 broken thesis）
    </div>
    <div class="formula-row">
      <b>Reversal (觸底訊號)</b>：<code>0.35·drift_4w_score + 0.30·ma_slope_score + 0.20·price_vs_ma50_score + 0.15·rs_recovery_score</code>
    </div>
    <div class="formula-row">
      <b>Floor (護城河地板)</b>：<code>0.40·moat/10 + 0.30·pass/5 + 0.15·quality/10 + 0.15·cagr_growth_score</code>
    </div>
    <div class="formula-row" style="margin-top:8px;color:#5a7a9a">
      <b>Vetoes</b>（任一觸發 → 不入榜）：<code>ai_risk==🔴</code> · <code>moat_grade∈(C,X)</code> · <code>trap==🔴</code> · <code>dist_52w&gt;−15%</code> · <code>eps_revision&lt;−30%</code> · <code>moat_score&lt;6</code>
    </div>
    <div class="formula-row" style="color:#5a7a9a">
      <b>Tier 切分</b>：Final ≥ {TIER_FINAL_MIN} 才入榜；Reversal ≥ {TIER_A_REVERSAL_MIN} → Tier A（Reversal Confirmed），否則 Tier B（Deep Value Watch）
    </div>
  </div>

  <div class="caveat-panel">
    <strong>⚠ 高風險逆向區 — 使用前必讀</strong>
    <ul>
      <li><b>不是價值陷阱 screener</b>：通過 Floor pillar 不保證 thesis 還活著 — 務必先看個股 DD 確認護城河是否仍成立，再判斷是逆向機會還是接落刀。</li>
      <li><b>不是動量 screener</b>：Tier A 代表「reversal 早期訊號」，不代表起漲點已確認或趨勢已反轉 — 可能還有再跌一段的空間。</li>
      <li><b>跟 Quality-Entry 互補不重複</b>：dist_52w_high_pct &gt; −15% 的標的被 veto 出 Bottom-Out，dist &lt; −15% 的標的在 Quality-Entry 的 pullback 子分接近 0；兩個 screener 結果設計上不重疊。</li>
    </ul>
  </div>

  <div class="tier-card tier-a">
    <h2>🟠 Tier A — Reversal Confirmed <span class="badge">Final ≥ {TIER_FINAL_MIN} · Reversal ≥ {TIER_A_REVERSAL_MIN}</span></h2>
    <div class="desc">深回檔 + 觸底反彈訊號已出現（4w drift 轉正 / MA250 趨平 / 站回 MA50）。Rationale 欄顯示關鍵逆向訊號（dist / 4w / slope）。高風險區：先看 DD 確認 thesis 未崩。{f"（另有 {tier_a_overflow} 檔未顯示）" if tier_a_overflow > 0 else ""}</div>
    {tier_a_html}
  </div>

  <div class="tier-card tier-b">
    <h2>⬜ Tier B — Deep Value Watch <span class="badge">Final ≥ {TIER_FINAL_MIN} · Reversal &lt; {TIER_A_REVERSAL_MIN}</span></h2>
    <div class="desc">跌幅夠深、護城河地板在，但 reversal 訊號尚未出現。「等什麼」欄點出最大拖累訊號 — 觸發後再評估進場。{f"（另有 {tier_b_overflow} 檔未顯示）" if tier_b_overflow > 0 else ""}</div>
    {tier_b_html}
  </div>

</div>

<div class="footer">
  <h4>數據來源</h4>
  <ul style="margin-left:18px">
    <li><code>docs/dd-screener/latest.json</code> v1.2+（含 moat_score / quality_score / ai_risk / eps_revision_pct 等 dd-meta propagated 欄位）</li>
    <li>MA snapshot 為 yfinance 週線（每次 build 重抓）；timing 欄位來自 docs/screener/latest.json 每日 cron + yfinance fallback</li>
  </ul>
  <h4>機器可讀</h4>
  <p>JSON sidecar: <a href="/dd-screener/bottom-out.json"><code>/dd-screener/bottom-out.json</code></a> · 每日快照: <code>/dd-screener/bottom-out-snapshots/YYYY-MM-DD.json</code></p>
  <p style="margin-top:16px;color:#94a3b8">Generated by <code>scripts/build_bottom_out.py</code> · schema v{SCHEMA_VERSION}</p>
</div>
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
    args = p.parse_args()

    doc = build_pipeline()

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
