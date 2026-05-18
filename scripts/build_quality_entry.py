#!/usr/bin/env python3
"""Quality-Entry Screener — 三支柱複合分數 (品質×護城河 / 成長持續性 / 勝率切入點).

設計 source-of-truth: /Users/ivanchang/.claude/plans/https-research-investmquest-com-dd-scree-shiny-dream.md

Pipeline:
  1. 讀 docs/dd-screener/latest.json (v1.2+, 已含 pct_5y / quality_score / ai_risk / 等)
  2. 每檔套 vetoes (ai_risk 🔴 / moat_grade C/X / trap 🔴 / ma System Fail)
  3. 算 A (品質+護城河) / B (成長持續性) / C (進場品質) 三支柱
     Final = 0.40·A + 0.30·B + 0.30·C
  4. Tier 切分：
       Tier A — Buy Zone Now:           Final ≥ 0.65  AND  C ≥ 0.65
       Tier B — Quality Compounder Wait Final ≥ 0.65  AND  C <  0.65
  5. 取 Tier A 全部 + Tier B 補到合計 25 檔
  6. 寫 docs/dd-screener/quality-entry.{html,json} + 每日 snapshot

Usage:
  python3 scripts/build_quality_entry.py
  python3 scripts/build_quality_entry.py --dry-run     # 不寫檔
  python3 scripts/build_quality_entry.py --no-snapshot # 不寫 daily snapshot
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
HTML_OUT = OUTPUT_DIR / "quality-entry.html"
JSON_OUT = OUTPUT_DIR / "quality-entry.json"
SNAPSHOT_DIR = OUTPUT_DIR / "quality-entry-snapshots"

TAIPEI_TZ = timezone(timedelta(hours=8))
SCHEMA_VERSION = "1.0"

# ── scoring constants ─────────────────────────────────────────────────────────
PILLAR_WEIGHTS = {"quality": 0.40, "growth": 0.30, "entry": 0.30}

# Tier 門檻
TIER_FINAL_MIN = 0.65
TIER_A_ENTRY_MIN = 0.65
DISPLAY_TOTAL = 25  # Tier A 全部 + Tier B 補到合計 25

# Val emoji → numeric (與 dd_alpha_ranker 同表)
VAL_NUM = {"🟢": 1.0, "🟡": 0.6, "🟠": 0.3, "🔴": 0.0}

# Moat grade → numeric (純展示用，veto 用 grade 字串本身)
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


# ── derived MA state from latest.json snapshot ────────────────────────────────
def ma_state_label_and_score(ma: dict) -> tuple[str, float]:
    """Approximate pure-MA six-state from ma snapshot fields.

    `ma` snapshot only has `slope_w250_pct` (no per-MA slope), so this is a
    simplified mapping vs DD §2 F. Used purely for the entry-quality score.

    Returns (label_emoji, score 0.0-1.0).
    """
    price = _safe_float(ma.get("price"))
    w52 = _safe_float(ma.get("w52"))
    w104 = _safe_float(ma.get("w104"))
    w250 = _safe_float(ma.get("w250"))
    slope = _safe_float(ma.get("slope_w250_pct"))
    if None in (price, w52, w104, w250) or slope is None:
        return ("—", 0.4)  # neutral 缺資料

    # ❌ System Fail: 跌破 MA250 或 MA250 斜率明顯負
    if price < w250 or slope < -3:
        return ("❌", 0.0)

    slope_strong = slope > 3
    slope_flat = -3 <= slope <= 3

    # 🟢 Best Entry: 在 MA52 之下、MA104 之上、且 MA250 上升 — 回測整理之機
    if price < w52 and price > w104 and slope_strong:
        return ("🟢", 1.0)

    # ✅ Strong Uptrend: 完美排列 + MA250 上升
    if price > w52 and w52 > w104 and w104 > w250 and slope_strong:
        return ("✅", 0.7)

    # 🟡 Caution: 在 MA104 之上但 MA250 斜率平
    if price > w104 and slope_flat:
        return ("🟡", 0.4)

    # 🟠 Avoid Now: 在 MA104 之下、MA250 之上、MA250 仍 +ve
    if price < w104 and price > w250:
        return ("🟠", 0.2)

    # 其他：上升但排列不完美（例如剛站回 MA52）
    return ("🟡", 0.4)


# ── score curves (𝝠 functions) ────────────────────────────────────────────────
def pullback_sweet_spot(dist_52w_high_pct: Optional[float]) -> float:
    """dist_52w_high_pct: 0% = 在高點，負值 = 低於高點。
    Sweet spot 在 -10 ~ -15% （已稍微回檔但 trend 未壞）。"""
    if dist_52w_high_pct is None:
        return 0.3
    d = dist_52w_high_pct
    if d > 0:
        return 0.3  # ATH 或之上：不是回檔機會（也不否決）
    if d >= -5:
        return 0.5 + (0 - d) / 5 * 0.2   # 0% → 0.5；-5% → 0.7
    if d >= -10:
        return 0.7 + (-5 - d) / 5 * 0.3  # -5% → 0.7；-10% → 1.0
    if d >= -15:
        return 1.0
    if d >= -20:
        return 1.0 - (-15 - d) / 5 * 0.3  # -15% → 1.0；-20% → 0.7
    if d >= -25:
        return 0.7 - (-20 - d) / 5 * 0.3  # -20% → 0.7；-25% → 0.4
    if d >= -30:
        return 0.4 - (-25 - d) / 5 * 0.4  # -25% → 0.4；-30% → 0.0
    return 0.0


def trend_intact_bonus(vs_200ma_pct: Optional[float]) -> float:
    """vs_200ma_pct: 正值 = 站上 200MA。Sweet spot +5 ~ +12% (大趨勢未破 + 不過熱)。"""
    if vs_200ma_pct is None:
        return 0.5
    v = vs_200ma_pct
    if v < 0:
        return 0.0  # 跌破 200MA：趨勢破壞
    if v <= 3:
        return 0.6
    if v <= 5:
        return 0.6 + (v - 3) / 2 * 0.4  # 3 → 0.6；5 → 1.0
    if v <= 12:
        return 1.0
    if v <= 15:
        return 1.0 - (v - 12) / 3 * 0.5  # 12 → 1.0；15 → 0.5
    if v <= 25:
        return 0.5
    if v <= 30:
        return 0.5 - (v - 25) / 5 * 0.5  # 25 → 0.5；30 → 0.0
    return 0.0


# ── pillars ───────────────────────────────────────────────────────────────────
def pillar_quality(s: dict) -> tuple[float, dict]:
    """A = 0.45·moat/10 + 0.25·pass/5 + 0.20·quality/10 + 0.10·max(execution,pricing)/10"""
    moat = _safe_float(s.get("moat_score")) or 0  # 1-10
    pass_count = _safe_float(s.get("pass_count")) or 0  # 0-5
    qs = _safe_float(s.get("quality_score"))
    me = _safe_float(s.get("moat_execution"))
    mpp = _safe_float(s.get("moat_pricing_power"))

    moat_norm = moat / 10.0
    pass_norm = pass_count / 5.0
    # quality_score 缺值 → 用 moat_score 當保守 fallback（避免拉低高 moat 標的）
    quality_norm = (qs / 10.0) if qs is not None else moat_norm
    # moat sub-score v12.3+；缺值 → 用 moat_score fallback
    sub_candidates = [v for v in (me, mpp) if v is not None]
    sub_norm = (max(sub_candidates) / 10.0) if sub_candidates else moat_norm

    score = 0.45 * moat_norm + 0.25 * pass_norm + 0.20 * quality_norm + 0.10 * sub_norm
    score = _clip01(score)
    return score, {
        "moat_norm": round(moat_norm, 3),
        "pass_norm": round(pass_norm, 3),
        "quality_norm": round(quality_norm, 3),
        "moat_sub_norm": round(sub_norm, 3),
    }


def pillar_growth(s: dict) -> tuple[float, dict]:
    """B = 0.40·growth_durability/10 + 0.30·clip(eps2y,0,40)/40 + 0.30·clip(ev5y,0,25)/25"""
    gd = _safe_float(s.get("growth_durability"))
    eps2y = _safe_float(s.get("eps2y"))  # %
    ev5y = _safe_float(s.get("ev5y_pct"))  # annualized IRR %
    upside_5y = _safe_float(s.get("upside_5y_pct"))  # total 5Y % return
    moat = _safe_float(s.get("moat_score")) or 5  # fallback proxy

    # growth_durability 缺值 → moat_score (相關但不完全等價，保守降權)
    gd_norm = (gd / 10.0) if gd is not None else (moat / 10.0) * 0.8

    # eps2y 截斷 40% (避免異常值主導)
    eps_norm = _clip01((eps2y or 0) / 40.0)

    # ev5y_pct 為 null 時 fallback 用 upside_5y_pct / 5 (年化)
    if ev5y is not None:
        ev_input = ev5y
    elif upside_5y is not None:
        ev_input = upside_5y / 5.0
    else:
        ev_input = 0.0
    ev_norm = _clip01(ev_input / 25.0)

    score = 0.40 * gd_norm + 0.30 * eps_norm + 0.30 * ev_norm
    score = _clip01(score)
    return score, {
        "growth_durability_norm": round(gd_norm, 3),
        "eps2y_norm": round(eps_norm, 3),
        "ev5y_norm": round(ev_norm, 3),
    }


def pillar_entry(s: dict) -> tuple[float, dict, str]:
    """C = 0.30·(1-pct_5y/100) + 0.25·MA + 0.20·pullback + 0.15·trend + 0.10·val
    Returns (score, breakdown, ma_label)."""
    pct_5y = _safe_float(s.get("pct_5y"))
    ma_snapshot = s.get("ma") or {}
    timing = s.get("timing") or {}
    val_field = s.get("val", "")

    # 5Y P/E 分位（越低越好）
    if pct_5y is not None:
        pct_norm = _clip01(1.0 - pct_5y / 100.0)
    else:
        pct_norm = 0.5

    # MA state
    ma_label, ma_score = ma_state_label_and_score(ma_snapshot)

    # 回檔 sweet spot
    dist = _safe_float(timing.get("dist_52w_high_pct"))
    pullback = pullback_sweet_spot(dist)

    # 趨勢未破
    vs200 = _safe_float(timing.get("vs_200ma_pct"))
    trend = trend_intact_bonus(vs200)

    # 估值燈
    val_score = VAL_NUM.get(val_field, 0.5)

    score = (0.30 * pct_norm + 0.25 * ma_score + 0.20 * pullback
             + 0.15 * trend + 0.10 * val_score)
    score = _clip01(score)
    return score, {
        "pct_5y_norm": round(pct_norm, 3),
        "ma_score": round(ma_score, 3),
        "pullback_score": round(pullback, 3),
        "trend_score": round(trend, 3),
        "val_score": round(val_score, 3),
    }, ma_label


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
    return None


# ── rationale strings ─────────────────────────────────────────────────────────
def entry_rationale(s: dict, breakdown: dict, ma_label: str) -> str:
    """Tier A 進場 rationale — 三段，挑該檔最強的訊號。"""
    parts: list[str] = []
    pct_5y = _safe_float(s.get("pct_5y"))
    if pct_5y is not None:
        parts.append(f"PE {pct_5y:.0f} 分位")
    if ma_label != "—":
        parts.append(f"MA {ma_label}")
    dist = _safe_float((s.get("timing") or {}).get("dist_52w_high_pct"))
    if dist is not None:
        if dist < 0:
            parts.append(f"距 52wH {dist:.0f}%")
        else:
            parts.append(f"距 52wH +{dist:.0f}%")
    val = s.get("val", "")
    if val:
        parts.append(f"估值 {val}")
    return " / ".join(parts[:3]) if parts else "—"


def wait_hint(s: dict, breakdown: dict, ma_label: str) -> str:
    """Tier B 「等什麼」— 點出 entry sub-score 最大拖累。"""
    sub = breakdown["entry"]
    # 找權重後最低貢獻的分項
    weighted = {
        "pct_5y": sub["pct_5y_norm"] * 0.30,
        "ma": sub["ma_score"] * 0.25,
        "pullback": sub["pullback_score"] * 0.20,
        "trend": sub["trend_score"] * 0.15,
        "val": sub["val_score"] * 0.10,
    }
    # 加權目標 vs 加權實際 → 找差距最大的
    targets = {"pct_5y": 0.30, "ma": 0.25, "pullback": 0.20, "trend": 0.15, "val": 0.10}
    gap = {k: targets[k] - weighted[k] for k in targets}
    bottleneck = max(gap, key=gap.get)

    pct_5y = _safe_float(s.get("pct_5y"))
    dist = _safe_float((s.get("timing") or {}).get("dist_52w_high_pct"))
    vs200 = _safe_float((s.get("timing") or {}).get("vs_200ma_pct"))

    if bottleneck == "pct_5y":
        if pct_5y is not None:
            return f"等 PE 分位降至 < 40（現 {pct_5y:.0f}）"
        return "等 PE 分位資料補齊"
    if bottleneck == "ma":
        return f"等 MA 回穩（現 {ma_label}）"
    if bottleneck == "pullback":
        if dist is not None and dist > 0:
            return "等回檔 −10 ~ −15%"
        if dist is not None and dist < -25:
            return "跌幅過深，等 trend 重建"
        return "等回到 sweet spot"
    if bottleneck == "trend":
        if vs200 is not None:
            if vs200 < 0:
                return "等站回 200MA"
            if vs200 > 25:
                return f"漲幅消化（vs 200MA +{vs200:.0f}%）"
        return "等趨勢結構轉好"
    if bottleneck == "val":
        return f"等估值降溫（現 {s.get('val','—')}）"
    return "—"


# ── scoring ───────────────────────────────────────────────────────────────────
def score_ticker(s: dict) -> Optional[dict]:
    """Return a scored row, or None if vetoed."""
    veto = is_vetoed(s)
    if veto:
        return None

    a, a_breakdown = pillar_quality(s)
    b, b_breakdown = pillar_growth(s)
    c, c_breakdown, ma_label = pillar_entry(s)

    final = (PILLAR_WEIGHTS["quality"] * a
             + PILLAR_WEIGHTS["growth"] * b
             + PILLAR_WEIGHTS["entry"] * c)

    breakdown = {
        "quality": a_breakdown,
        "growth": b_breakdown,
        "entry": c_breakdown,
    }

    tier = None
    if final >= TIER_FINAL_MIN:
        tier = "A" if c >= TIER_A_ENTRY_MIN else "B"

    return {
        "ticker": s["ticker"],
        "name": s.get("name", ""),
        "sector": s.get("sector", ""),
        "final": round(final, 4),
        "quality": round(a, 4),
        "growth": round(b, 4),
        "entry": round(c, 4),
        "tier": tier,
        "ma_label_today": ma_label,
        "breakdown": breakdown,
        "rationale": entry_rationale(s, breakdown, ma_label) if tier == "A" else None,
        "wait_hint": wait_hint(s, {"entry": c_breakdown}, ma_label) if tier == "B" else None,
        # surface raw fields for table display
        "moat_grade": s.get("moat_grade"),
        "moat_score": s.get("moat_score"),
        "signal": s.get("signal"),
        "val": s.get("val"),
        "ai_risk": s.get("ai_risk"),
        "pct_5y": s.get("pct_5y"),
        "fpe_fy2": s.get("fpe_fy2"),
        "ev5y_pct": s.get("ev5y_pct"),
        "pass_count": s.get("pass_count"),
        "quality_score": s.get("quality_score"),
        "growth_durability": s.get("growth_durability"),
        "dd_path": s.get("dd_path"),
        "dca_path": s.get("dca_path"),
    }


# ── build pipeline ────────────────────────────────────────────────────────────
def build_pipeline() -> dict:
    print(f"=== Quality-Entry build · {_now_taipei_iso()} ===\n")
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
    for s in universe:
        veto = is_vetoed(s)
        if veto:
            vetoed.append((s.get("ticker", "?"), veto))
            continue
        row = score_ticker(s)
        if row is not None:
            scored.append(row)

    # rank by Final desc, then Entry desc as tie-breaker
    scored.sort(key=lambda r: (-r["final"], -r["entry"], r["ticker"]))

    tier_a = [r for r in scored if r["tier"] == "A"]
    tier_b = [r for r in scored if r["tier"] == "B"]

    # display: Tier A 全部 + Tier B 補到合計 25
    display_a = tier_a[:]
    remaining = max(0, DISPLAY_TOTAL - len(display_a))
    display_b = tier_b[:remaining]

    print(f"  Scored: {len(scored)} (vetoed {len(vetoed)})")
    print(f"  Tier A (Buy Zone Now):           {len(tier_a)} (display {len(display_a)})")
    print(f"  Tier B (Quality Compounder Wait): {len(tier_b)} (display {len(display_b)})")
    if vetoed:
        print(f"  Veto sample: {vetoed[:5]}")

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
            "tier_a_entry_min": TIER_A_ENTRY_MIN,
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
    pct_5y_str = _fmt_pct(row.get("pct_5y"))
    fpe = row.get("fpe_fy2")
    fpe_str = f"{fpe:.1f}" if fpe is not None else "—"
    return f"""<tr>
  <td class="left">{_ticker_link(row)}<div class="sub">{row.get('sector','')}</div></td>
  <td class="score-cell"><strong>{_fmt_score(row['final'])}</strong></td>
  <td>{_fmt_score(row['quality'])}</td>
  <td>{_fmt_score(row['growth'])}</td>
  <td class="entry-cell">{_fmt_score(row['entry'])}</td>
  <td class="left">{row['rationale']}</td>
  <td class="meta-cell">{moat_grade} · {row.get('signal','')} · PE {fpe_str}x</td>
</tr>"""


def _row_html_tier_b(row: dict) -> str:
    moat_grade = row.get("moat_grade") or ""
    pct_5y_str = _fmt_pct(row.get("pct_5y"))
    fpe = row.get("fpe_fy2")
    fpe_str = f"{fpe:.1f}" if fpe is not None else "—"
    return f"""<tr>
  <td class="left">{_ticker_link(row)}<div class="sub">{row.get('sector','')}</div></td>
  <td class="score-cell"><strong>{_fmt_score(row['final'])}</strong></td>
  <td>{_fmt_score(row['quality'])}</td>
  <td>{_fmt_score(row['growth'])}</td>
  <td class="entry-cell entry-low">{_fmt_score(row['entry'])}</td>
  <td class="left">{row['wait_hint']}</td>
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
  <th>Quality</th>
  <th>Growth</th>
  <th>Entry</th>
  <th class="left">Rationale / 等什麼</th>
  <th class="left">Tags</th>
</tr>
</thead>
<tbody>
{body}
</tbody>
</table>"""


def render_html(doc: dict, out_path: Path) -> None:
    as_of = doc["as_of"]
    universe_total = doc["universe_total"]
    eligible_total = doc["eligible_total"]
    vetoed_count = doc["vetoed_count"]
    tier_a = doc["tier_a"]
    tier_b = doc["tier_b"]
    tier_a_overflow = doc["tier_a_overflow"]
    tier_b_overflow = doc["tier_b_overflow"]

    tier_a_html = _section_table(
        tier_a, _row_html_tier_a,
        '尚無 Tier A 標的。可能是市場整體偏熱（Entry 子分過低），或門檻過嚴 — '
        '檢視 Tier B 並等待 entry zone 修正。'
    )
    tier_b_html = _section_table(
        tier_b, _row_html_tier_b,
        '尚無 Tier B 標的。'
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quality-Entry — 品質複利者 + 勝率切入點 | InvestMQuest</title>
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
.tier-card.tier-a h2{{color:#166534}}
.tier-card.tier-b h2{{color:#854d0e}}
.tier-card h2 .badge{{display:inline-block;padding:2px 9px;border-radius:5px;font-size:11px;font-weight:700}}
.tier-card.tier-a h2 .badge{{background:#dcfce7;color:#166534}}
.tier-card.tier-b h2 .badge{{background:#fef3c7;color:#854d0e}}
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
.entry-cell{{color:#166534;font-weight:600}}
.entry-low{{color:#92400e}}
.meta-cell{{font-size:10.5px;color:#5a7a9a;text-align:left !important}}
.empty-row{{padding:14px;text-align:center;color:#94a3b8;font-size:12px;font-style:italic}}
.caveat-panel{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:14px 18px;margin-bottom:20px;font-size:12px;color:#854d0e;line-height:1.65}}
.caveat-panel strong{{color:#78350f;display:block;margin-bottom:6px}}
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
          <a href="/dd-screener/quality-entry.html" class="active">Quality-Entry</a>
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
    <div class="hero-h1">Quality-Entry — 品質複利者 + 勝率切入點</div>
    <div class="hero-sub">
      鎖定<b>有品質、有成長、有護城河、不易被顛覆</b>的標的，
      並從中挑出<b>相對有勝率的切入點（不要求起漲點）</b>。
      三支柱複合分數：品質×護城河 40% / 成長持續性 30% / 進場品質 30%。
      與 <a href="/dd-screener/alpha-rank.html" style="color:#2563eb">Alpha Rank</a>（六法共識）並列：
      Alpha Rank 適合積極追逐六種數學排名共識；Quality-Entry 適合 quality compounder 逢回佈局。
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>{as_of}</strong>快照日期</div>
      <div class="hero-stat"><strong>{universe_total}</strong>universe</div>
      <div class="hero-stat"><strong>{eligible_total}</strong>通過 veto</div>
      <div class="hero-stat"><strong>{vetoed_count}</strong>被 veto</div>
      <div class="hero-stat"><strong>{len(tier_a)}</strong>Tier A — Buy Zone</div>
      <div class="hero-stat"><strong>{len(tier_b)}</strong>Tier B — Wait</div>
    </div>
  </div>
</div>

<div class="section">

  <div class="formula-panel">
    <h3>方法論</h3>
    <div class="formula-row">
      <b>Final</b> = 0.40·<b>Quality</b> + 0.30·<b>Growth</b> + 0.30·<b>Entry</b>
    </div>
    <div class="formula-row" style="margin-top:6px">
      <b>Quality (品質×護城河)</b>：<code>0.45·moat/10 + 0.25·pass/5 + 0.20·quality_score/10 + 0.10·max(execution,pricing)/10</code>
    </div>
    <div class="formula-row">
      <b>Growth (成長持續性)</b>：<code>0.40·durability/10 + 0.30·clip(eps2y,0,40)/40 + 0.30·clip(ev5y,0,25)/25</code>
    </div>
    <div class="formula-row">
      <b>Entry (進場品質)</b>：<code>0.30·(1−pct_5y/100) + 0.25·MA + 0.20·pullback(dist_52wH) + 0.15·trend(vs_200MA) + 0.10·val</code>
    </div>
    <div class="formula-row" style="margin-top:8px;color:#5a7a9a">
      <b>Vetoes</b>（任一觸發 → 不入榜）：<code>ai_risk==🔴</code> · <code>moat_grade∈(C,X)</code> · <code>trap==🔴</code>
    </div>
    <div class="formula-row" style="color:#5a7a9a">
      <b>Tier 切分</b>：Final ≥ {TIER_FINAL_MIN} 才入榜；Entry ≥ {TIER_A_ENTRY_MIN} → Tier A（Buy Zone Now），否則 Tier B（Wait）
    </div>
  </div>

  <div class="caveat-panel">
    <strong>讀法 caveats</strong>
    <ul>
      <li><b>不是起漲點 screener</b>：Entry 子分故意把「距 52w 高點 −10 ~ −15%」算作 sweet spot（不是 0 ~ −5%）。這與 Alpha Rank Angle 2「EV×起漲點」設計相反，刻意對應「不一定要起漲點」的目標。</li>
      <li><b>未做歷史勝率回測</b>：「相對有勝率」claim 來自構造（cheap percentile + 趨勢未破 + 護城河）而非實證 win rate；如要 backtest 證據，需另外開回測 issue。</li>
      <li><b>MA 標籤為近似</b>：本頁 MA 燈號從 latest.json snapshot 推導（缺各 MA 個別斜率），與 DD §2 F 的完整六狀態機可能微差；以個股 DD 的 MA 段為準。</li>
      <li><b>缺資料中性處理</b>：pct_5y / growth_durability / quality_score 缺值時用 fallback（如 moat_score 代理），不直接 0 分以免錯殺老 DD。</li>
      <li><b>跨期不可比</b>：本頁分數僅在「同一份 latest.json snapshot 內」相對排序有意義；不同日期分數絕對值不直接比較。</li>
    </ul>
  </div>

  <div class="tier-card tier-a">
    <h2>🟢 Tier A — Buy Zone Now <span class="badge">Final ≥ {TIER_FINAL_MIN} · Entry ≥ {TIER_A_ENTRY_MIN}</span></h2>
    <div class="desc">三支柱同時及格、且 Entry 子分到位 — 即現在處於「相對有勝率的點位」。Rationale 欄顯示為什麼此檔在 Buy Zone（PE 分位 / MA 狀態 / 距 52w 高點）。{f"（另有 {tier_a_overflow} 檔未顯示）" if tier_a_overflow > 0 else ""}</div>
    {tier_a_html}
  </div>

  <div class="tier-card tier-b">
    <h2>🟡 Tier B — Quality Compounder, Wait <span class="badge">Final ≥ {TIER_FINAL_MIN} · Entry &lt; {TIER_A_ENTRY_MIN}</span></h2>
    <div class="desc">品質+護城河+成長都到位但 Entry 子分還沒到位 — watchlist。「等什麼」欄顯示 entry 子分最大拖累來源（PE 分位 / MA / 回檔 / 趨勢 / 估值燈）。{f"（另有 {tier_b_overflow} 檔未顯示）" if tier_b_overflow > 0 else ""}</div>
    {tier_b_html}
  </div>

</div>

<div class="footer">
  <h4>數據來源</h4>
  <ul style="margin-left:18px">
    <li><code>docs/dd-screener/latest.json</code> v1.2+（含 pct_5y / quality_score / ai_risk / moat sub-scores 等 dd-meta propagated 欄位）</li>
    <li>MA snapshot 為 yfinance 週線（每次 build 重抓）；timing 欄位來自 docs/screener/latest.json 每日 cron + yfinance fallback</li>
  </ul>
  <h4>機器可讀</h4>
  <p>JSON sidecar: <a href="/dd-screener/quality-entry.json"><code>/dd-screener/quality-entry.json</code></a> · 每日快照: <code>/dd-screener/quality-entry-snapshots/YYYY-MM-DD.json</code></p>
  <p style="margin-top:16px;color:#94a3b8">Generated by <code>scripts/build_quality_entry.py</code> · schema v{SCHEMA_VERSION}</p>
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
