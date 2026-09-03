#!/usr/bin/env python3
"""dd_judgment_from_meta.py — WP1c round-trip tool: reverse-derive a v16
judgment.json from an EXISTING v15 DD report.

Mandated extraction sources (per WP1c brief): dd-meta JSON (primary source
for almost every scalar) + the E12 monitoring/trigger table (§13 tail) + the
§2.B three-assumption table (best effort). Everything else that has no home
in dd-meta is filled with `null` and every required `reasoning.<module>`
entry is the literal string "（回溯反推，無推理段）" -- this tool never
fabricates judgment content that wasn't already machine-readable in the
source report.

As a low-cost bonus (same fetched HTML chunks, cheap regexes), this tool
also best-effort-parses: §2.C R1-R3 risk paragraph, §2.F Single Thing,
§2.A holding-period paragraph, the dashboard `.thesis` headline, §13a
"進場節奏" table row, §13c holding-cap sentence, and the `<details
class="audit">` block. None of these affect the WP1c round-trip target
(dd-meta / E12), which is why they're best-effort rather than mandated.

Also writes a companion `<judgment-stem>.scenario_meta.json` file (shape =
scripts/dd_scenario.py's `--meta` output) copied verbatim from dd-meta's own
`scenario_tree` + the 6 flat scenario fields, and points judgment.json's
`scenario_ref` at it — this is what lets gen_dd_tables.py and
validate_judgment.py's scenario cross-check reproduce those dd-meta fields
losslessly.

Usage:
  python3 scripts/dd_judgment_from_meta.py DD.html --out judgment.json
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_sections  # noqa: E402

REQUIRED_REASONING_MODULES = [
    "archetype", "thesis", "industry", "moat", "growth", "quality",
    "governance", "valuation", "trap_analysis", "premortem",
]
NO_REASONING = "（回溯反推，無推理段）"


# ---------------------------------------------------------------------------
# generic text helpers
# ---------------------------------------------------------------------------

def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    s = html_lib.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_table_rows(table_inner_html: str):
    """List of [cell_text, ...] for every <tr> containing <td> cells (skips
    the <th> header row automatically since it has no <td>)."""
    rows = []
    for row_m in re.finditer(r"<tr>(.*?)</tr>", table_inner_html, re.DOTALL):
        cells = re.findall(r"<td>(.*?)</td>", row_m.group(1), re.DOTALL)
        if cells:
            rows.append([strip_tags(c) for c in cells])
    return rows


def extract_strong_colon_fields(fragment: str) -> dict:
    """`<strong>LABEL</strong>：value...` repeated inline -> {label: value}."""
    pattern = re.compile(r"<strong>([^<]+)</strong>\s*[:：]\s*")
    matches = list(pattern.finditer(fragment))
    out = {}
    for i, m in enumerate(matches):
        label = strip_tags(m.group(1)).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(fragment)
        value = strip_tags(fragment[start:end]).strip()
        out[label] = value
    return out


def _find_by_prefix(fields: dict, prefix: str):
    for k, v in fields.items():
        if k.startswith(prefix):
            return v
    return None


# ---------------------------------------------------------------------------
# §2.B (H1-H3), §2.C (R1-R3), §2.F (Single Thing), §2.A (holding period)
# ---------------------------------------------------------------------------

def build_H(s2_chunk: str):
    m = re.search(r"<h3>B｜三個核心假設.*?</h3>\s*<table>(.*?)</table>", s2_chunk, re.DOTALL)
    H = []
    if m:
        for r in parse_table_rows(m.group(1)):
            if len(r) < 8:
                continue
            id_, text, y2, y5, y10, thresh, src, drift = r[:8]
            H.append({
                "id": id_ or None, "text": text or None, "2y": y2 or None,
                "5y": y5 or None, "10y": y10 or None, "threshold": thresh or None,
                "source": src or None, "drift_rule": drift or None,
            })
    while len(H) < 3:
        i = len(H) + 1
        H.append({"id": f"H{i}", "text": None, "2y": None, "5y": None, "10y": None,
                   "threshold": None, "source": None, "drift_rule": None})
    return H


_R_RE = re.compile(
    r"<strong>R(\d+)</strong>\s*（\s*對應\s*([^，,、]+)[，,、]?\s*([⚡🔥🐢])?[^）]*）\s*[:：]\s*"
    r"(.*?)(?=<strong>R\d+</strong>|</p>)",
    re.DOTALL,
)

_CLOCK_RE = re.compile(r"[⚡🔥🐢]")


def _build_R_from_paragraph(s2_chunk: str):
    R = []
    for m in _R_RE.finditer(s2_chunk):
        desc = strip_tags(m.group(4))
        R.append({
            "id": f"R{m.group(1)}",
            "text": desc or None,
            "h_ref": (m.group(2) or "").strip() or None,
            "clock": m.group(3),
            "threshold": desc or None,
        })
    return R


def _build_R_from_table(s2_chunk: str):
    """Some v15.2 reports render §2.C R1-R3 as a table (5 cols: id / text /
    對應假設 / 時間尺度 / 監測與警戒閾值) instead of the inline <strong>R1</strong>
    paragraph form (e.g. AVGO 2026-09-03) -- both are real, observed shapes."""
    m = re.search(r">C｜三個最可能推翻論點的風險</h3>\s*<table>(.*?)</table>", s2_chunk, re.DOTALL)
    if not m:
        return []
    R = []
    for r in parse_table_rows(m.group(1)):
        if len(r) < 5:
            continue
        id_, text, h_ref, clock_cell, threshold = r[:5]
        clock_m = _CLOCK_RE.search(clock_cell)
        R.append({
            "id": id_ or None, "text": text or None, "h_ref": h_ref or None,
            "clock": clock_m.group(0) if clock_m else None, "threshold": threshold or None,
        })
    return R


def build_R(s2_chunk: str):
    R = _build_R_from_paragraph(s2_chunk) or _build_R_from_table(s2_chunk)
    while len(R) < 3:
        i = len(R) + 1
        R.append({"id": f"R{i}", "text": None, "h_ref": None, "clock": None, "threshold": None})
    return R


def build_single_thing(s2_chunk: str):
    m = re.search(r"<h3>F｜Single Thing</h3>\s*<p>(.*?)</p>", s2_chunk, re.DOTALL)
    if not m:
        return {"description": None, "why_fatal": None, "if_happens": None,
                "how_monitor": None, "probability": None}
    fields = extract_strong_colon_fields(m.group(1))
    return {
        "description": _find_by_prefix(fields, "描述"),
        "why_fatal": _find_by_prefix(fields, "為什麼致命"),
        "if_happens": _find_by_prefix(fields, "如果發生"),
        "how_monitor": _find_by_prefix(fields, "如何監測"),
        "probability": _find_by_prefix(fields, "機率估計"),
    }


def build_holding_period(s2_chunk: str):
    m = re.search(r"<h3>A｜持有期與時間軸宣告</h3>\s*<p>(.*?)</p>", s2_chunk, re.DOTALL)
    if not m:
        return {"horizon": None, "driver": None, "signal_vs_noise": None}
    fields = extract_strong_colon_fields(m.group(1))
    return {
        "horizon": _find_by_prefix(fields, "預設持有期"),
        "driver": _find_by_prefix(fields, "主要驅動理由"),
        "signal_vs_noise": _find_by_prefix(fields, "這個持有期決定"),
    }


# ---------------------------------------------------------------------------
# E12 (§13 <table id="triggers">)
# ---------------------------------------------------------------------------

def _find_table_near_marker(chunk: str, marker: str):
    """The E12 table's `id="triggers"` lands on the <table> tag itself in
    some reports (SNOW) and on a preceding <h3> in others (DELL/AVGO). Handle
    both: if the marker sits inside an already-open <table> (no </table> seen
    between the nearest preceding <table> and the marker), use that table;
    otherwise scan forward for the next <table>."""
    idx = chunk.find(marker)
    if idx == -1:
        return None
    prev_table = chunk.rfind("<table", 0, idx)
    prev_close = chunk.rfind("</table>", 0, idx)
    if prev_table != -1 and (prev_close == -1 or prev_table > prev_close):
        table_start = prev_table
    else:
        table_start = chunk.find("<table", idx)
    if table_start == -1:
        return None
    table_end = chunk.find("</table>", table_start)
    if table_end == -1:
        return None
    inner = chunk[table_start:table_end]
    return re.sub(r"^<table[^>]*>", "", inner, count=1)


def build_triggers(decision_chunk: str):
    inner = _find_table_near_marker(decision_chunk, 'id="triggers"')
    triggers = []
    if inner is None:
        return triggers
    for r in parse_table_rows(inner):
        if len(r) < 8:
            continue
        n, text, type_cell, maps_to, thresh, action, freq, date = r[:8]
        norm_type = re.sub(r"[（(].*?[）)]", "", type_cell).strip()
        try:
            n_val = int(n)
        except ValueError:
            n_val = n
        triggers.append({
            "n": n_val, "text": text or None, "type": norm_type or None,
            "maps_to": maps_to or None, "metric": "", "threshold": thresh or None,
            "action": action or None, "source_freq": freq or None, "date": date or "",
            "type_display": type_cell or None,
        })
    return triggers


# ---------------------------------------------------------------------------
# §13 decision section extras (best effort)
# ---------------------------------------------------------------------------

def build_decision_out(decision_chunk: str, dd_meta: dict):
    audit_rows = []
    row_hit = None
    audit_m = re.search(r'<details class="audit">(.*?)</details>', decision_chunk, re.DOTALL)
    if audit_m:
        inner = audit_m.group(1)
        for p_m in re.finditer(r"<p>(.*?)</p>", inner, re.DOTALL):
            txt = strip_tags(p_m.group(1))
            if txt:
                audit_rows.append(txt)
        rh_m = re.search(r"row ?\d+[a-z]?", inner, re.IGNORECASE)
        if rh_m:
            row_hit = rh_m.group(0)

    holding_cap = None
    hc_m = re.search(r"<strong>建議持有年限[:：]([^<]+)</strong>", decision_chunk)
    if hc_m:
        holding_cap = strip_tags(hc_m.group(1))

    pacing = []
    pc_m = re.search(r"<tr>\s*<td>進場節奏</td>\s*<td>(.*?)</td>\s*</tr>", decision_chunk, re.DOTALL)
    if pc_m:
        val = strip_tags(pc_m.group(1))
        if val:
            pacing = [val]

    return {
        "verdict": dd_meta.get("dca_verdict"),
        "role": dd_meta.get("dca_role"),
        "row_hit": row_hit,
        "pacing": pacing,
        "holding_cap": holding_cap,
        "requires_critic": [],
        "audit_rows": audit_rows,
        "rearm_trigger": dd_meta.get("rearm_trigger"),
        "exec_line": None,
    }


def build_thesis_headline(dashboard_chunk: str):
    m = re.search(r'<p class="thesis">(.*?)</p>', dashboard_chunk, re.DOTALL)
    return strip_tags(m.group(1)) if m else None


def build_company_name(dashboard_chunk: str, ticker: str):
    m = re.search(r"<h1>(.*?)</h1>", dashboard_chunk, re.DOTALL)
    if not m:
        return None
    h1 = strip_tags(m.group(1))
    # "Snowflake Inc.（SNOW）深度研究與統一裁決" -> "Snowflake Inc."
    idx = h1.find(f"（{ticker}）") if ticker else -1
    if idx == -1 and ticker:
        idx = h1.find(f"({ticker})")
    return h1[:idx].strip() if idx != -1 else h1


def build_max_dd(dashboard_chunk: str, dd_meta: dict):
    lo = dd_meta.get("max_dd_pct")
    hi = None
    path_risk = None
    if dashboard_chunk:
        norm = dashboard_chunk.replace("−", "-").replace("－", "-")
        m = re.search(r"Max ?DD[^0-9\-]{0,20}(-?\d+(?:\.\d+)?)%\s*[~～]\s*(-?\d+(?:\.\d+)?)%", norm)
        if m:
            a, b = float(m.group(1)), float(m.group(2))
            lo2, hi = min(a, b), max(a, b)
            if lo is None:
                lo = lo2
        pr_m = re.search(r"路徑風險([🟢🟡🔴])", dashboard_chunk)
        if pr_m:
            path_risk = pr_m.group(1)
    return {"lo": lo, "hi": hi, "path_risk": path_risk, "trigger_time": None}


# ---------------------------------------------------------------------------
# dd-meta -> module builders (dd-meta is the mandated primary source; these
# are 1:1 with scripts/dd_schema/judgment-to-ddmeta.md, read in reverse)
# ---------------------------------------------------------------------------

def build_appendix_a(dd_meta: dict):
    stress = dd_meta.get("stress") or {}
    return {
        "signal": dd_meta.get("signal"), "moat_score": dd_meta.get("moat_score"),
        "growth_durability": dd_meta.get("growth_durability"),
        "quality_score": dd_meta.get("quality_score"), "ai_risk": dd_meta.get("ai_risk"),
        "long_term_confidence": dd_meta.get("long_term_confidence"),
        "val": dd_meta.get("val"), "ma": dd_meta.get("ma"),
        "fpe_fy2": dd_meta.get("fpe_fy2"), "pct_5y": dd_meta.get("pct_5y"),
        "peg_fy2": dd_meta.get("peg_fy2"), "upside_short_pct": dd_meta.get("upside_short_pct"),
        "upside_mid_pct": dd_meta.get("upside_mid_pct"),
        "stress": {"pass": stress.get("pass"), "total": stress.get("total")},
        "verdict": dd_meta.get("verdict"),
    }


def build_moat(dd_meta: dict):
    return {
        "execution": dd_meta.get("moat_execution"), "pricing": dd_meta.get("moat_pricing_power"),
        "combined": None, "grade": dd_meta.get("moat"), "score": dd_meta.get("moat_score"),
        "trend": dd_meta.get("moat_trend"), "trend_evidence": None,
        "spread_table": [], "threats": [],
        "roic_durability": {
            "quadrant": None, "checkpoints": [], "roiic": None, "reinvest_rate": None,
            "endo_ceiling": dd_meta.get("endo_growth_ceiling"), "formula_note": None,
        },
    }


def build_growth(dd_meta: dict):
    return {
        "runway_years": None, "runway_post_y5": dd_meta.get("runway_post_y5"),
        "seven_questions": [], "segments": [], "decay_signals": [], "trap_rating": None,
    }


def build_industry(dd_meta: dict):
    return {
        "clock_phase": dd_meta.get("industry_clock_phase"), "sd_verdict_source": None,
        "bargaining": {"up": None, "down": None, "geo": None},
        "profit_pool_dir": None, "tam_table": [],
    }


def build_valuation(dd_meta: dict):
    return {
        "tier": None, "peers": [], "fwd_pe": dd_meta.get("fpe_fy2"),
        "peg": dd_meta.get("peg_fy2"), "percentile_5y": dd_meta.get("pct_5y"),
        "val_light": dd_meta.get("val"), "val_light_derivation": None, "targets": {},
        "upside_short_pct": dd_meta.get("upside_short_pct"),
        "upside_mid_pct": dd_meta.get("upside_mid_pct"),
    }


def build_trap_analysis(dd_meta: dict):
    return {
        "pattern": None, "evidence_against": None, "evidence_for": None, "bear_case": None,
        "monitor": [], "verdict": dd_meta.get("trap"), "label": dd_meta.get("trap_label"),
    }


def build_governance(dd_meta: dict):
    return {"capalloc_grade": dd_meta.get("capalloc_grade"), "scorecard": [], "sbc": {}}


def build_quality():
    return {"three_year": [], "dupont": [], "ccc": [], "buyback": {}, "lumpiness": {}}


def build_archetype(dd_meta: dict):
    return {"primary": dd_meta.get("archetype"), "secondary": None, "confidence": None, "fingerprint": None}


def build_decision_inputs(dd_meta: dict):
    scenario_tree = dd_meta.get("scenario_tree") or {}
    return {
        "signal": dd_meta.get("signal"), "trap": dd_meta.get("trap"), "val": dd_meta.get("val"),
        "ma": dd_meta.get("ma"), "runway_post_y5": dd_meta.get("runway_post_y5"),
        "moat_trend": dd_meta.get("moat_trend"), "moat": dd_meta.get("moat"),
        "capalloc_grade": dd_meta.get("capalloc_grade"), "archetype": dd_meta.get("archetype"),
        "cycle_position": dd_meta.get("cycle_position"), "cycle_verdict": dd_meta.get("cycle_verdict"),
        "asym_ratio": dd_meta.get("asym_ratio"), "irr_base_pct": dd_meta.get("irr_base_pct"),
        "ev5y_pct": dd_meta.get("ev5y_pct"), "price_at_dd": dd_meta.get("price_at_dd"),
        "thesis_irreconcilable": None,
        "valuation_dependent": scenario_tree.get("valuation_dependent"),
        "market_wrong_reason_given": None, "week26_return_pct": None,
        "momentum_overheated": None, "cycle_gates_pass": None, "consensus_rev_3m_pct": None,
    }


def build_scenario_meta_sidecar(dd_meta: dict):
    keys = ("bull_5y_price", "bear_5y_price", "p_bull_pct", "p_bear_pct",
            "upside_5y_pct", "ev5y_pct", "irr_base_pct", "asym_ratio", "scenario_tree")
    out = {k: dd_meta[k] for k in keys if k in dd_meta}
    return out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_judgment(html_text: str) -> tuple[dict, dict]:
    dd_meta = dd_sections.dd_meta_json(html_text) or {}
    s2_chunk = dd_sections.extract(html_text, ["s2"]) or ""
    decision_chunk = dd_sections.extract(html_text, ["decision"]) or ""
    dashboard_chunk = dd_sections.extract(html_text, ["dashboard"]) or ""

    ticker = dd_meta.get("ticker")
    eps_meta = {
        "base_eps_path": dd_meta.get("base_eps_path") or {},
        "fy_end_month": dd_meta.get("fy_end_month"),
        "eps_basis": dd_meta.get("eps_basis"),
    }

    judgment = {
        "meta": {
            "ticker": ticker, "date": dd_meta.get("date"), "schema": dd_meta.get("schema"),
            "company_name": build_company_name(dashboard_chunk, ticker),
        },
        "oneliner": dd_meta.get("oneliner"),
        "archetype": build_archetype(dd_meta),
        "thesis": {
            "headline": build_thesis_headline(dashboard_chunk),
            "holding_period": build_holding_period(s2_chunk),
            "H": build_H(s2_chunk),
            "R": build_R(s2_chunk),
            "single_thing": build_single_thing(s2_chunk),
        },
        "industry": build_industry(dd_meta),
        "moat": build_moat(dd_meta),
        "growth": build_growth(dd_meta),
        "quality": build_quality(),
        "governance": build_governance(dd_meta),
        "valuation": build_valuation(dd_meta),
        "trap_analysis": build_trap_analysis(dd_meta),
        "appendix_a": build_appendix_a(dd_meta),
        "scenario_ref": None,  # filled in main() once the sidecar path is known
        "eps_meta": eps_meta,
        "catalysts": dd_meta.get("catalysts") or [],
        "decision_inputs": build_decision_inputs(dd_meta),
        "decision_out": build_decision_out(decision_chunk, dd_meta),
        "triggers": build_triggers(decision_chunk),
        "contradictions": [],
        "premortem": {
            "blind_spots": [], "failure_story": None, "second_failure": None,
            "max_dd": build_max_dd(dashboard_chunk, dd_meta),
        },
        "reasoning": {m: NO_REASONING for m in REQUIRED_REASONING_MODULES},
    }
    if dd_meta.get("kill_metrics"):
        judgment["kill_metrics"] = dd_meta["kill_metrics"]

    scenario_meta = build_scenario_meta_sidecar(dd_meta)
    return judgment, scenario_meta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dd_html", help="既有 v15 DD HTML 路徑")
    ap.add_argument("--out", required=True, help="輸出 judgment.json 路徑")
    args = ap.parse_args()

    html_text = Path(args.dd_html).read_text(encoding="utf-8")
    judgment, scenario_meta = build_judgment(html_text)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if scenario_meta:
        sidecar_name = out_path.stem + ".scenario_meta.json"
        sidecar_path = out_path.parent / sidecar_name
        sidecar_path.write_text(
            json.dumps(scenario_meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        judgment["scenario_ref"] = sidecar_name
        print(f"寫入 {sidecar_path}")

    out_path.write_text(json.dumps(judgment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"寫入 {out_path}")


if __name__ == "__main__":
    main()
