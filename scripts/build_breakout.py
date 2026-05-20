#!/usr/bin/env python3
"""Breakout Screener — 突破動能追擊 + Minervini SEPA / IBD CAN-SLIM gates.

設計 source-of-truth: /Users/ivanchang/.claude/plans/yfinance-eps-zippy-frost.md

Pipeline:
  1. 讀 docs/dd-screener/latest.json (v1.2+, 已含 pct_5y / quality_score / ai_risk / 等)
  2. 每檔套 vetoes (ai_risk 🔴 / moat_grade C/X / trap 🔴 / dist_52w < -7% /
     rs_score < 80 / ma250_slope < 0 / ma50_pct > +35% / eps_revision_pct < -30%)
  3. 算 A (Position / Proximity to 52w High) / B (Momentum Setup) / C (Quality Floor) 三支柱
     Final = 0.40·A + 0.35·B + 0.25·C
  4. Tier 切分：
       Tier A — Active Breakout:    Final ≥ 0.65  AND  B (Setup) ≥ 0.65
       Tier B — Pre-Breakout Setup: Final ≥ 0.65  AND  B < 0.65
  5. 取 Tier A 全部 + Tier B 補到合計 25 檔
  6. 寫 docs/dd-screener/breakout.{html,json} + 每日 snapshot

Usage:
  python3 scripts/build_breakout.py
  python3 scripts/build_breakout.py --dry-run     # 不寫檔
  python3 scripts/build_breakout.py --no-snapshot # 不寫 daily snapshot
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
LATEST_JSON = ROOT / "docs" / "dd-screener" / "latest.json"
OUTPUT_DIR = ROOT / "docs" / "dd-screener"
HTML_OUT = OUTPUT_DIR / "breakout.html"
JSON_OUT = OUTPUT_DIR / "breakout.json"
SNAPSHOT_DIR = OUTPUT_DIR / "breakout-snapshots"

TAIPEI_TZ = timezone(timedelta(hours=8))
SCHEMA_VERSION = "1.0"

# ── scoring constants ─────────────────────────────────────────────────────────
PILLAR_WEIGHTS = {"position": 0.40, "setup": 0.35, "floor": 0.25}

# Tier 門檻
TIER_FINAL_MIN = 0.65
TIER_A_SETUP_MIN = 0.65
DISPLAY_TOTAL = 25  # Tier A 全部 + Tier B 補到合計 25

# Veto: Minervini RS 門檻（SEPA / IBD CAN-SLIM hard gate）
RS_VETO_THRESHOLD = 80.0
# Veto: dist_52w_high — Breakout 必須接近 52w 高
DIST_VETO_THRESHOLD = -7.0
# Veto: EPS 修正下限（分析師大砍 EPS → 不該追突破）
EPS_REV_VETO_THRESHOLD = -30.0
# Veto: 護城河最低分
MOAT_SCORE_MIN = 6
# Veto: vs MA50 overextended 上限
MA50_PCT_VETO_THRESHOLD = 35.0


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


# ── score curves ──────────────────────────────────────────────────────────────
def breakout_proximity_score(dist_52w_high_pct: Optional[float]) -> float:
    """Λ function on dist_52w_high_pct — Breakout sweet spot at 0% (touching ATH).

    Anchor points per plan:
      0%    → 1.0  (touching ATH / just broke out)
      -2%   → 0.95
      -5%   → 0.75
      -7%   → 0.55 (vetoed upstream, safety guard)
      -10%  → 0.30
      -15%  → 0.10 (邊緣)
      <-20% → 0   (vetoed — should use quality-entry / bottom-out)
    """
    if dist_52w_high_pct is None:
        return 0.3  # neutral — missing data
    d = dist_52w_high_pct
    if d >= 0:
        return 1.0  # at or above 52w high (e.g. new ATH)
    if d >= -2:
        # 0 → 1.0; -2 → 0.95
        return 1.0 + d / 2 * 0.05
    if d >= -5:
        # -2 → 0.95; -5 → 0.75
        return 0.95 + (d + 2) / (-3) * 0.20
    if d >= -7:
        # -5 → 0.75; -7 → 0.55
        return 0.75 + (d + 5) / (-2) * 0.20
    if d >= -10:
        # -7 → 0.55; -10 → 0.30
        return 0.55 + (d + 7) / (-3) * 0.25
    if d >= -15:
        # -10 → 0.30; -15 → 0.10
        return 0.30 + (d + 10) / (-5) * 0.20
    if d >= -20:
        # -15 → 0.10; -20 → 0
        return 0.10 + (d + 15) / (-5) * 0.10
    return 0.0  # < -20%: should be quality-entry / bottom-out territory


def rs_momentum_score(rs_score: Optional[float]) -> float:
    """rs_score_norm for Breakout: requires strong momentum (≥ 80 = hard veto).

    Per plan: rs_score / 100, but < 50 gives 0 (vetoed upstream if < 80 anyway).
    Returns value in [0, 1.0].
    """
    if rs_score is None:
        return 0.4  # neutral — missing
    r = rs_score
    if r < 50:
        return 0.0
    if r < 80:
        # 50 → 0; 80 → 0.6 (but rs < 80 is vetoed, so rarely reached)
        return (r - 50) / 30 * 0.6
    if r <= 100:
        # 80 → 0.8; 100 → 1.0
        return 0.8 + (r - 80) / 20 * 0.2
    return 1.0


def ma50_position_score(ma50_pct: Optional[float]) -> float:
    """Λ on ma50_pct for Breakout: sweet spot 0~+20% above MA50.

    Anchor points per plan:
      0~+5%   → 1.0  (textbook sweet — just reclaimed)
      +5~+20% → 0.85 (healthy momentum, current market norm)
      +20~+30% → 0.55
      >+30%   → 0.2  (overextended)
      <-5%    → 0    (below MA50 = no breakout)
      -5~0%   → ramp to 0.5
    """
    if ma50_pct is None:
        return 0.4  # neutral
    v = ma50_pct
    if v < -5:
        return 0.0
    if v < 0:
        # -5 → 0; 0 → 0.5
        return 0.0 + (v + 5) / 5 * 0.5
    if v <= 5:
        # 0 → 0.5; +5 → 1.0
        return 0.5 + v / 5 * 0.5
    if v <= 20:
        # +5 → 1.0; +20 → 0.85
        return 1.0 - (v - 5) / 15 * 0.15
    if v <= 30:
        # +20 → 0.85; +30 → 0.55
        return 0.85 - (v - 20) / 10 * 0.30
    if v <= 35:
        # +30 → 0.55; +35 → 0.2 (vetoed threshold)
        return 0.55 - (v - 30) / 5 * 0.35
    return 0.2  # > +35% vetoed upstream


def ma250_slope_score_breakout(slope_w250_pct: Optional[float]) -> float:
    """slope_w250_pct for Breakout: positive slope required.

    Per plan:
      >= 0 → 1.0 (long-term uptrend confirmed)
      < 0  → 0   (vetoed upstream as well)
    """
    if slope_w250_pct is None:
        return 0.4  # neutral — missing
    return 1.0 if slope_w250_pct >= 0 else 0.0


def drift_4w_score_breakout(drift_4w_pct: Optional[float]) -> float:
    """drift_4w_pct for Breakout: positive drift = momentum confirmation.

    Per plan:
      > 0    → ramp up
      > +10% → cap 1.0
      < 0    → 0.3 (tolerate small neg, but penalized)
    """
    if drift_4w_pct is None:
        return 0.3
    v = drift_4w_pct
    if v < 0:
        return 0.3  # small negative tolerated but low
    if v <= 10:
        # 0 → 0.5; +10 → 1.0 (ramp)
        return 0.5 + v / 10 * 0.5
    return 1.0  # > +10%: capped


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
def pillar_position(s: dict) -> tuple[float, dict]:
    """A = breakout_proximity_score(dist_52w_high_pct)"""
    timing = s.get("timing") or {}
    dist = _safe_float(timing.get("dist_52w_high_pct"))
    score = breakout_proximity_score(dist)
    score = _clip01(score)
    return score, {"dist": dist, "position_score": round(score, 3)}


def pillar_setup(s: dict) -> tuple[float, dict]:
    """B = 0.40·rs_score_norm + 0.30·ma50_position_score
          + 0.20·ma250_slope_score + 0.10·drift_4w_score"""
    ma = s.get("ma") or {}
    timing = s.get("timing") or {}

    rs = _safe_float(timing.get("rs_score"))
    ma50 = _safe_float(timing.get("ma50_pct"))
    slope = _safe_float(ma.get("slope_w250_pct"))
    d4w = _safe_float(ma.get("drift_4w_pct"))

    sr = rs_momentum_score(rs)
    sm = ma50_position_score(ma50)
    ss = ma250_slope_score_breakout(slope)
    sd = drift_4w_score_breakout(d4w)

    score = 0.40 * sr + 0.30 * sm + 0.20 * ss + 0.10 * sd
    score = _clip01(score)
    return score, {
        "rs_score": rs,
        "ma50_pct": ma50,
        "slope_w250": slope,
        "drift_4w": d4w,
        "rs_score_norm": round(sr, 3),
        "ma50_position_score": round(sm, 3),
        "ma250_slope_score": round(ss, 3),
        "drift_4w_score": round(sd, 3),
    }


def pillar_floor(s: dict) -> tuple[float, dict]:
    """C = 0.40·moat/10 + 0.30·pass_count/5 + 0.15·quality_score/10 + 0.15·eps_rev_safety

    REUSED EXACTLY from build_bottom_out.py.
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
def is_vetoed(s: dict) -> Optional[str]:
    """Return veto reason string, or None if eligible."""
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
    # Breakout-specific vetoes
    timing = s.get("timing") or {}
    ma = s.get("ma") or {}
    dist = _safe_float(timing.get("dist_52w_high_pct"))
    if dist is not None and dist < DIST_VETO_THRESHOLD:
        return f"dist {dist:.1f}% (< {DIST_VETO_THRESHOLD}%) — 用 quality-entry/bottom-out"
    rs = _safe_float(timing.get("rs_score"))
    if rs is not None and rs < RS_VETO_THRESHOLD:
        return f"RS {rs:.0f} (< {RS_VETO_THRESHOLD}) — Minervini gate"
    slope = _safe_float(ma.get("slope_w250_pct"))
    if slope is not None and slope < 0:
        return f"MA250 slope {slope:.2f}% < 0 — 長期下降趨勢"
    ma50 = _safe_float(timing.get("ma50_pct"))
    if ma50 is not None and ma50 > MA50_PCT_VETO_THRESHOLD:
        return f"vs MA50 +{ma50:.1f}% (> +{MA50_PCT_VETO_THRESHOLD}%) — overextended"
    eps_rev = _safe_float(s.get("eps_revision_pct"))
    if eps_rev is not None and eps_rev < EPS_REV_VETO_THRESHOLD:
        return f"EPS 修正 {eps_rev:.1f}% (< {EPS_REV_VETO_THRESHOLD}%)"
    return None


# ── rationale strings ─────────────────────────────────────────────────────────
def breakout_rationale(s: dict, a_breakdown: dict, b_breakdown: dict) -> str:
    """Tier A rationale: highlight key breakout signals.

    Example: ATH / RS 95 / MA50 +12% / slope +1.8%
    """
    parts: list[str] = []

    dist = a_breakdown.get("dist")
    if dist is not None:
        if dist >= -1:
            parts.append("ATH")
        else:
            parts.append(f"dist {dist:.0f}%")

    rs = b_breakdown.get("rs_score")
    if rs is not None:
        parts.append(f"RS {rs:.0f}")

    ma50 = b_breakdown.get("ma50_pct")
    if ma50 is not None:
        sign = "+" if ma50 >= 0 else ""
        parts.append(f"MA50 {sign}{ma50:.0f}%")

    slope = b_breakdown.get("slope_w250")
    if slope is not None:
        sign = "+" if slope >= 0 else ""
        parts.append(f"slope {sign}{slope:.1f}%")

    return " / ".join(parts) if parts else "—"


def _setup_wait_hint(b_breakdown: dict) -> str:
    """Tier B 「等什麼」— 找 Setup sub-scores 的最大拖累。

    Logic per plan: check rs_score_norm / ma50_position / ma250_slope / drift_4w
    sub-scores against their weights to find biggest gap.
    """
    # Setup sub-scores with their weights (within pillar B)
    sub_scores = {
        "rs_score_norm":      b_breakdown.get("rs_score_norm", 0.5) * 0.40,
        "ma50_position":      b_breakdown.get("ma50_position_score", 0.5) * 0.30,
        "ma250_slope":        b_breakdown.get("ma250_slope_score", 0.5) * 0.20,
        "drift_4w":           b_breakdown.get("drift_4w_score", 0.5) * 0.10,
    }
    sub_targets = {
        "rs_score_norm": 0.40,
        "ma50_position": 0.30,
        "ma250_slope":   0.20,
        "drift_4w":      0.10,
    }
    gaps = {k: sub_targets[k] - sub_scores[k] for k in sub_targets}
    bottleneck = max(gaps, key=gaps.get)

    # Raw values for contextual hints
    rs = b_breakdown.get("rs_score")
    ma50 = b_breakdown.get("ma50_pct")
    slope = b_breakdown.get("slope_w250")
    drift = b_breakdown.get("drift_4w")

    if bottleneck == "rs_score_norm":
        if rs is not None:
            return f"等 RS 升到 80+（現 {rs:.0f}）"
        return "等 RS 升到 80+"
    if bottleneck == "ma50_position":
        if ma50 is not None:
            sign = "+" if ma50 >= 0 else ""
            return f"等 vs MA50 進入 +5~+20%（現 {sign}{ma50:.0f}%）"
        return "等 vs MA50 進入 +5~+20%"
    if bottleneck == "ma250_slope":
        if slope is not None:
            return f"等 MA250 轉正（現 {slope:.2f}%/w）"
        return "等 MA250 轉正"
    if bottleneck == "drift_4w":
        if drift is not None and drift < 0:
            return f"等 4w drift 轉正（現 {drift:.1f}%）"
        return "等 4w drift 轉正"
    return "—"


# ── scoring ───────────────────────────────────────────────────────────────────
def score_ticker(s: dict) -> Optional[dict]:
    """Return a scored row, or None if vetoed."""
    veto = is_vetoed(s)
    if veto:
        return None

    a, a_breakdown = pillar_position(s)
    b, b_breakdown = pillar_setup(s)
    c, c_breakdown = pillar_floor(s)

    final = (PILLAR_WEIGHTS["position"] * a
             + PILLAR_WEIGHTS["setup"] * b
             + PILLAR_WEIGHTS["floor"] * c)

    breakdown = {
        "position": a_breakdown,
        "setup": b_breakdown,
        "floor": c_breakdown,
    }

    tier = None
    if final >= TIER_FINAL_MIN:
        tier = "A" if b >= TIER_A_SETUP_MIN else "B"

    rationale = breakout_rationale(s, a_breakdown, b_breakdown) if tier == "A" else None
    wait_hint = _setup_wait_hint(b_breakdown) if tier == "B" else None

    return {
        "ticker": s["ticker"],
        "name": s.get("name", ""),
        "sector": s.get("sector", ""),
        "final": round(final, 4),
        "position": round(a, 4),
        "setup": round(b, 4),
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
        "ma50_pct": (s.get("timing") or {}).get("ma50_pct"),
    }


# ── build pipeline ────────────────────────────────────────────────────────────
def build_pipeline() -> dict:
    print(f"=== Breakout build · {_now_taipei_iso()} ===\n")
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
    pillar_counts = {"near_ath": 0, "strong_setup": 0, "solid_floor": 0}
    # Detailed veto breakdown for diagnostics
    veto_reasons: dict[str, int] = {}

    for s in universe:
        veto = is_vetoed(s)
        if veto:
            vetoed.append((s.get("ticker", "?"), veto))
            # Categorize veto reason for diagnostics
            key = veto.split(" ")[0] if " " in veto else veto
            veto_reasons[key] = veto_reasons.get(key, 0) + 1
            continue
        row = score_ticker(s)
        if row is not None:
            scored.append(row)
            if row["position"] >= 0.5:
                pillar_counts["near_ath"] += 1
            if row["setup"] >= 0.5:
                pillar_counts["strong_setup"] += 1
            if row["floor"] >= 0.5:
                pillar_counts["solid_floor"] += 1

    # rank by Final desc, then Setup desc as tie-breaker
    scored.sort(key=lambda r: (-r["final"], -r["setup"], r["ticker"]))

    tier_a = [r for r in scored if r["tier"] == "A"]
    tier_b = [r for r in scored if r["tier"] == "B"]

    # display: Tier A 全部 + Tier B 補到合計 25
    display_a = tier_a[:]
    remaining = max(0, DISPLAY_TOTAL - len(display_a))
    display_b = tier_b[:remaining]

    print(f"  Scored: {len(scored)} (vetoed {len(vetoed)})")
    print(f"  Pillar coverage (scored): position≥0.5: {pillar_counts['near_ath']} | "
          f"setup≥0.5: {pillar_counts['strong_setup']} | "
          f"floor≥0.5: {pillar_counts['solid_floor']}")
    print(f"  Tier A (Active Breakout):    {len(tier_a)} (display {len(display_a)})")
    print(f"  Tier B (Pre-Breakout Setup): {len(tier_b)} (display {len(display_b)})")
    if vetoed:
        veto_sample = vetoed[:10]
        print(f"  Veto sample: {veto_sample}")
    if veto_reasons:
        sorted_reasons = sorted(veto_reasons.items(), key=lambda x: -x[1])
        print(f"  Veto breakdown: {sorted_reasons[:6]}")

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
            "tier_a_setup_min": TIER_A_SETUP_MIN,
            "dist_veto": DIST_VETO_THRESHOLD,
            "rs_veto": RS_VETO_THRESHOLD,
            "eps_rev_veto": EPS_REV_VETO_THRESHOLD,
            "moat_score_min": MOAT_SCORE_MIN,
            "ma50_pct_veto": MA50_PCT_VETO_THRESHOLD,
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
    rs = row.get("rs_score")
    dist_str = f"{dist:.0f}%" if dist is not None else "—"
    rs_str = f"{rs:.0f}" if rs is not None else "—"
    rationale = row.get("rationale") or "—"
    return f"""<tr>
  <td class="left">{_ticker_link(row)}<div class="sub">{row.get('sector','')}</div></td>
  <td class="score-cell"><strong>{_fmt_score(row['final'])}</strong></td>
  <td class="position-cell">{_fmt_score(row['position'])}</td>
  <td class="setup-cell">{_fmt_score(row['setup'])}</td>
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
  <td class="left">{_ticker_link(row)}<div class="sub">{row.get('sector','')}</div></td>
  <td class="score-cell"><strong>{_fmt_score(row['final'])}</strong></td>
  <td class="position-cell">{_fmt_score(row['position'])}</td>
  <td class="setup-cell setup-low">{_fmt_score(row['setup'])}</td>
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
  <th>Position</th>
  <th>Setup</th>
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
        '尚無 Tier A 標的。市場可能偏弱（RS ≥ 80 + dist > -7% 的標的不足），'
        '或大盤進入 correction 期，動能標的暫時退出突破區。請查看 Tier B 或等待市場回暖。'
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
<title>Breakout — 突破動能追擊 | InvestMQuest</title>
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
.tier-card.tier-a h2{{color:#1d4ed8}}
.tier-card.tier-b h2{{color:#475569}}
.tier-card h2 .badge{{display:inline-block;padding:2px 9px;border-radius:5px;font-size:11px;font-weight:700}}
.tier-card.tier-a h2 .badge{{background:#dbeafe;color:#1d4ed8}}
.tier-card.tier-b h2 .badge{{background:#e2e8f0;color:#64748b}}
.tier-card .desc{{font-size:12px;color:#5a7a9a;margin-bottom:10px;line-height:1.6}}
.tier-card table{{width:100%;border-collapse:collapse;font-size:12px}}
.tier-card th{{background:#eff6ff;color:#5a7a9a;font-weight:700;padding:8px 10px;text-align:right;border-bottom:2px solid #dce8f5;font-size:10px;letter-spacing:.04em;text-transform:uppercase}}
.tier-card th.left{{text-align:left}}
.tier-card td{{padding:8px 10px;text-align:right;border-bottom:1px solid #f0f5fb;font-variant-numeric:tabular-nums}}
.tier-card td.left{{text-align:left;color:#0f2a45;font-weight:500}}
.tier-card td.left .sub{{font-size:10px;color:#94a3b8;font-weight:400;margin-top:1px}}
.tier-card td a{{color:#2563eb;text-decoration:none;font-weight:700}}
.tier-card td a:hover{{text-decoration:underline}}
.score-cell{{color:#0f2a45}}
.position-cell{{color:#1d4ed8;font-weight:600}}
.setup-cell{{color:#1e40af;font-weight:600}}
.setup-low{{color:#64748b}}
.rationale-cell{{color:#1e3a5f;font-size:11px}}
.wait-cell{{color:#475569;font-size:11px}}
.meta-cell{{font-size:10.5px;color:#5a7a9a;text-align:left !important}}
.empty-row{{padding:14px;text-align:center;color:#94a3b8;font-size:12px;font-style:italic}}
.caveat-panel{{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:14px 18px;margin-bottom:20px;font-size:12px;color:#1e3a5f;line-height:1.65}}
.caveat-panel strong{{color:#1d4ed8;display:block;margin-bottom:6px}}
.caveat-panel ul{{margin-left:18px}}
.footer{{padding:30px 32px;font-size:11px;color:#5a7a9a;line-height:1.7;max-width:min(1400px,96vw);margin:0 auto;border-top:1px solid #dce8f5}}
.footer h4{{color:#1e3a5f;font-size:12px;margin-top:14px;margin-bottom:6px;font-weight:700}}
.footer code{{background:#f0f5fb;padding:1px 5px;border-radius:3px;font-size:10px;color:#1e3a5f}}
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
          <a href="/dd-screener/alpha-rank.html">Alpha Rank</a>
          <a href="/dd-screener/quality-entry.html">Quality-Entry</a>
          <a href="/dd-screener/bottom-out.html">Bottom-Out</a>
          <a href="/dd-screener/breakout.html" class="active">Breakout</a>
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
    <div class="hero-h1">Breakout — 突破動能追擊</div>
    <div class="hero-sub">
      鎖定<b>接近 52 週高點（dist &gt; −7%）+ RS ≥ 80 + MA250 正斜率</b>的 Minervini-style 突破標的。
      三支柱複合分數：Position（接近 ATH）40% / Momentum Setup 35% / Quality Floor 25%。
      Tier A 是「動能確認中的 Active Breakout」，Tier B 是「體質合格但尚未觸發的 Pre-Breakout Setup」。
      與 <a href="/dd-screener/quality-entry.html" style="color:#2563eb">Quality-Entry</a> /
      <a href="/dd-screener/bottom-out.html" style="color:#ea580c">Bottom-Out</a> 互補不重疊（dist_52w 三段互斥）。
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>{run_ts_display}</strong>最後更新（台北）</div>
      <div class="hero-stat"><strong>{universe_total}</strong>universe</div>
      <div class="hero-stat"><strong>{eligible_total}</strong>通過 veto</div>
      <div class="hero-stat"><strong>{vetoed_count}</strong>被 veto</div>
      <div class="hero-stat"><strong>{len(tier_a)}</strong>Tier A — Active Breakout</div>
      <div class="hero-stat"><strong>{len(tier_b)}</strong>Tier B — Pre-Breakout Setup</div>
    </div>
  </div>
</div>

<div class="section">

  <div class="formula-panel">
    <h3>方法論</h3>
    <div class="formula-row">
      <b>Final</b> = 0.40·<b>Position</b> + 0.35·<b>Setup</b> + 0.25·<b>Floor</b>
    </div>
    <div class="formula-row" style="margin-top:6px">
      <b>Position（接近 ATH）</b>：<code>Λ(dist_52w_high_pct)</code> — ATH 給 1.0，−2% 0.95，−5% 0.75，−7% 0.55（veto 邊界）；&lt;−20% 給 0（用其他 screener）
    </div>
    <div class="formula-row">
      <b>Setup（動能確認）</b>：<code>0.40·rs_score_norm + 0.30·ma50_position_score + 0.20·ma250_slope_score + 0.10·drift_4w_score</code>
    </div>
    <div class="formula-row">
      <b>Floor（品質地板）</b>：<code>0.40·moat/10 + 0.30·pass/5 + 0.15·quality/10 + 0.15·eps_rev_safety</code>
    </div>
    <div class="formula-row" style="margin-top:8px;color:#5a7a9a">
      <b>Vetoes</b>（任一觸發 → 不入榜）：<code>ai_risk==🔴</code> · <code>moat_grade∈(C,X)</code> · <code>trap==🔴</code> · <code>moat_score&lt;6</code> · <code>dist_52w&lt;−7%</code> · <code>rs&lt;80</code> · <code>MA250 slope&lt;0</code> · <code>vs MA50&gt;+35%</code> · <code>eps_revision&lt;−30%</code>
    </div>
    <div class="formula-row" style="color:#5a7a9a">
      <b>Tier 切分</b>：Final ≥ {TIER_FINAL_MIN} 才入榜；Setup ≥ {TIER_A_SETUP_MIN} → Tier A（Active Breakout），否則 Tier B（Pre-Breakout Setup）
    </div>
  </div>

  <div class="caveat-panel">
    <strong>⚡ 動能區 — 使用前必讀</strong>
    <ul>
      <li><b>不是 sure-thing pattern</b>：Breakout 失敗率約 30-50%（Minervini 認知中屬合理）。Tier A 標的不保證繼續漲 — 請配 5-7% stop-loss 進場，讓市場告訴你對不對。</li>
      <li><b>Overextended trap</b>：Tier A 可能包含「爆衝最後一棒」標的。搭最新 IBD market state（見 <a href="/markets.html" style="color:#2563eb">markets.html</a>）一起看；correction 中的 breakout 容易 fail，請在 confirmed uptrend 中操作。</li>
      <li><b>跟 Quality-Entry / Bottom-Out 互補不重疊</b>：dist_52w &gt; −7% → Breakout；−10% ~ −15% → Quality-Entry；&lt; −25% → Bottom-Out。同檔股票不會同時在兩個 screener 的 Tier A。</li>
    </ul>
  </div>

  <div class="tier-card tier-a">
    <h2>&#128309; Tier A — Active Breakout <span class="badge">Final ≥ {TIER_FINAL_MIN} · Setup ≥ {TIER_A_SETUP_MIN}</span></h2>
    <div class="desc">接近 52w 高 + RS ≥ 80 + 動能確認。Rationale 欄顯示 ATH 距離 / RS / vs MA50 / slope 關鍵數字。高動能中高風險 — 配 stop-loss 進場。{f"（另有 {tier_a_overflow} 檔未顯示）" if tier_a_overflow > 0 else ""}</div>
    {tier_a_html}
  </div>

  <div class="tier-card tier-b">
    <h2>&#9898; Tier B — Pre-Breakout Setup <span class="badge">Final ≥ {TIER_FINAL_MIN} · Setup &lt; {TIER_A_SETUP_MIN}</span></h2>
    <div class="desc">體質合格、接近突破位，但動能尚未完全確認（RS 不夠強 / MA 條件未達）。「等什麼」欄點出最大拖累因子 — 條件觸發後再評估進場。{f"（另有 {tier_b_overflow} 檔未顯示）" if tier_b_overflow > 0 else ""}</div>
    {tier_b_html}
  </div>

</div>

<div class="footer">
  <h4>數據來源</h4>
  <ul style="margin-left:18px">
    <li><code>docs/dd-screener/latest.json</code> v1.2+（含 moat_score / quality_score / ai_risk / eps_revision_pct 等 dd-meta propagated 欄位）</li>
    <li>MA snapshot 為 yfinance 週線（每次 build 重抓）；timing 欄位來自 docs/screener/latest.json 每日 cron + yfinance fallback</li>
    <li>RS score = Minervini 相對強度計算（52w 末段加權），dist_52w_high_pct = 與 52 週高點之距離</li>
  </ul>
  <h4>機器可讀</h4>
  <p>JSON sidecar: <a href="/dd-screener/breakout.json"><code>/dd-screener/breakout.json</code></a> · 每日快照: <code>/dd-screener/breakout-snapshots/YYYY-MM-DD.json</code></p>
  <p style="margin-top:16px;color:#94a3b8">Generated by <code>scripts/build_breakout.py</code> · schema v{SCHEMA_VERSION}</p>
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
