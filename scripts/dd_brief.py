#!/usr/bin/env python3
"""dd_brief.py — WP4a: zero-LLM "quick verdict" (速判) HTML renderer.

Reads a v16 judgment.json (+ scenario_meta.json, evidence.json, optional
gate audit / decision-matrix audit fragment) and mechanically renders a
one-page brief, `scripts/dd_templates/brief.html` filled in with `{{TOKEN}}`
placeholders. No LLM call, no network. Reuses scripts/gen_dd_tables.py's
dd-meta builder and E2 (H1-H3)/E12 (triggers) table fragments verbatim
rather than re-implementing them.

Usage:
  python3 scripts/dd_brief.py --run-dir DIR --out FILE
  python3 scripts/dd_brief.py --judgment J.json --scenario-meta M.json \\
      [--evidence E.json] [--audit gate_audit.md] \\
      [--decision-audit tables/audit.html] --out FILE

--run-dir DIR resolves to DIR/judgment.json, DIR/scenario_meta.json,
DIR/evidence.json, DIR/gate_audit.md, DIR/tables/audit.html — any that don't
exist are simply treated as absent (rendered as "—", never fatal).
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import gen_dd_tables as gdt  # noqa: E402

TEMPLATE_PATH = SCRIPT_DIR / "dd_templates" / "brief.html"

try:
    import dd_gate  # noqa: E402  -- WP3, may not exist yet
except Exception:
    dd_gate = None


def esc(v) -> str:
    return html_lib.escape("" if v is None else str(v))


def load_json(path):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def dash(v):
    """Render a value, or the contract's '—' placeholder when absent."""
    if v is None or v == "":
        return "—"
    return esc(v)


def fmt_ymd(s):
    if not s:
        return None
    s = str(s)
    m = re.match(r"^(\d{4})(\d{2})(\d{2})$", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return s


def verdict_category(v):
    if not v:
        return None
    for cat in ("進場", "觀望", "迴避"):
        if v.startswith(cat):
            return cat
    return v


def num(x, digits=1):
    if x is None:
        return None
    try:
        return f"{float(x):.{digits}f}"
    except (TypeError, ValueError):
        return str(x)


# ---------------------------------------------------------------------------
# section renderers
# ---------------------------------------------------------------------------

def render_header(j, evidence):
    meta_top = j.get("meta") or {}
    di = j.get("decision_inputs") or {}
    dout = j.get("decision_out") or {}
    thesis = j.get("thesis") or {}

    ticker = meta_top.get("ticker") or ""
    company = meta_top.get("company_name") or ticker
    archetype = di.get("archetype") or j.get("archetype") or ""
    eyebrow = f"DD 速判 · {esc(ticker)} {esc(company)} · {esc(archetype)}"

    verdict = dout.get("verdict") or "—"
    role = dout.get("role")
    h1 = esc(verdict) + (f' <span class="role">｜{esc(role)}</span>' if role else "")

    oneliner = esc(j.get("oneliner") or thesis.get("headline") or "")

    price = di.get("price_at_dd")
    row_hit = dout.get("row_hit")

    prior = (evidence or {}).get("prior_dd") or {}
    prior_meta = prior.get("prior_meta") or {}
    prior_verdict = prior.get("dca_verdict") or prior_meta.get("verdict")
    if prior_verdict:
        same = verdict_category(prior_verdict) == verdict_category(verdict)
        label = "同向" if same else "翻面"
        prior_line = (
            f"{esc(fmt_ymd(prior.get('date')))} {esc(prior_verdict)}"
            f"{'｜' + esc(prior.get('dca_role')) if prior.get('dca_role') else ''}"
            f"（{label}）"
        )
    else:
        prior_line = "—"

    meta_box = (
        f'判斷日 <b>{dash(meta_top.get("date"))}</b><br>\n'
        f'    現價 <b>{"$" + esc(num(price, 2)) if price is not None else "—"}</b><br>\n'
        f'    決策矩陣 <b>{"Row " + esc(row_hit) if row_hit else "—"}</b><br>\n'
        f"    前份 <b>{prior_line}</b>"
    )
    return eyebrow, h1, oneliner, meta_box


def _tile(label, value, small=None):
    small_html = f"<small> {esc(small)}</small>" if small else ""
    return f'    <div class="tile"><div class="k">{esc(label)}</div><div class="v">{esc(value) if value is not None else "—"}{small_html}</div></div>'


def render_tiles(j, scenario_meta):
    di = j.get("decision_inputs") or {}
    sm = scenario_meta or {}
    moat = j.get("moat") or {}
    growth = j.get("growth") or {}
    prem = j.get("premortem") or {}
    trap = j.get("trap_analysis") or {}
    val = j.get("valuation") or {}

    ev5y = di.get("ev5y_pct", sm.get("ev5y_pct"))
    irr = di.get("irr_base_pct", sm.get("irr_base_pct"))
    ar = di.get("asym_ratio", sm.get("asym_ratio"))

    max_dd = prem.get("max_dd") or {}
    lo, hi = max_dd.get("lo"), max_dd.get("hi")
    if lo is not None and hi is not None:
        dd_main = min(lo, hi)
        dd_small = f"({esc(lo)}～{esc(hi)})"
    elif lo is not None:
        dd_main, dd_small = lo, None
    else:
        dd_main, dd_small = None, None

    moat_val = f"{esc(moat.get('grade'))} {esc(moat.get('trend'))}".strip() or None
    moat_small = moat.get("score")

    val_light = di.get("val", (j.get("appendix_a") or {}).get("val"))
    val_bits = []
    if val.get("percentile_5y") is not None:
        val_bits.append(f"分位 {val.get('percentile_5y')}%")
    if val.get("peg") is not None:
        val_bits.append(f"PEG {val.get('peg')}")
    val_small = " · ".join(val_bits) if val_bits else None

    trap_verdict = trap.get("verdict")
    trap_label = trap.get("label") or ""
    trap_small = trap_label
    if trap_verdict and trap_label.startswith(str(trap_verdict)):
        trap_small = trap_label[len(str(trap_verdict)):].strip() or trap_label

    endo = (moat.get("roic_durability") or {}).get("endo_ceiling")
    runway_small = f"內生天花板 {endo}%" if endo is not None else None

    rows = [
        _tile("5Y 期望值 EV", (gdt._fmt_signed_pct(ev5y) if ev5y is not None else None)),
        _tile("Base IRR", (num(irr) if irr is not None else None), "%/yr" if irr is not None else None),
        _tile("不對稱比 AR", (num(ar) if ar is not None else None)),
        _tile("Max DD", (f"{dd_main}%" if dd_main is not None else None), dd_small),
        _tile("護城河", moat_val, moat_small),
        _tile("估值燈", val_light, val_small),
        _tile("陷阱定性", trap_verdict, trap_small),
        _tile("Y5 後跑道", growth.get("runway_post_y5"), runway_small),
    ]
    return "\n".join(rows)


def render_r_list(j):
    R = (j.get("thesis") or {}).get("R") or []
    if not R:
        return "    <li>—</li>"
    out = []
    for r in R:
        tag = f"{r.get('id') or ''} {r.get('clock') or ''}".strip()
        out.append(
            f"    <li><span class=\"hr\">{esc(tag)}</span>{esc(r.get('text'))}"
            f"<br><b>門檻</b>：{esc(r.get('threshold'))}</li>"
        )
    return "\n".join(out)


def render_single_thing(j):
    st = (j.get("thesis") or {}).get("single_thing")
    if not st:
        return "<p>—</p>"
    if isinstance(st, str):
        return f"<p>{esc(st)}</p>"
    parts = []
    if st.get("description"):
        parts.append(f"<p><b>{esc(st['description'])}</b></p>")
    if st.get("why_fatal"):
        parts.append(f"<p>為何致命：{esc(st['why_fatal'])}</p>")
    if st.get("if_happens"):
        parts.append(f"<p>發生後：{esc(st['if_happens'])}</p>")
    if st.get("how_monitor"):
        parts.append(f"<p>怎麼監測：{esc(st['how_monitor'])}</p>")
    if st.get("probability"):
        parts.append(f"<p>機率：{esc(st['probability'])}</p>")
    return "\n  ".join(parts) if parts else "<p>—</p>"


def _terminal_year(scenario_meta):
    tl = ((scenario_meta or {}).get("scenario_tree") or {}).get("terminal_label") or ""
    m = re.search(r"FY(\d{4})", tl)
    return int(m.group(1)) if m else None


def render_scenario(j, scenario_meta):
    di = j.get("decision_inputs") or {}
    price = di.get("price_at_dd")
    sm = scenario_meta or {}
    bull_p, bear_p = sm.get("bull_5y_price"), sm.get("bear_5y_price")
    p_bull, p_bear = sm.get("p_bull_pct"), sm.get("p_bear_pct")
    p_base = (100 - p_bull - p_bear) if (p_bull is not None and p_bear is not None) else None
    upside5y = sm.get("upside_5y_pct")
    base_p = (price * (1 + upside5y / 100.0)) if (price is not None and upside5y is not None) else None

    def vs_now(target):
        if price in (None, 0) or target is None:
            return None
        return (target / price - 1) * 100.0

    def row(label, prob, tprice, cls_extra=""):
        vs = vs_now(tprice)
        vs_cls = "ok" if (vs is not None and vs >= 0) else ("bad" if vs is not None else "")
        return (
            f"    <tr><td>{esc(label)}</td>"
            f"<td class=\"num\">{esc(prob)}{'%' if prob is not None else ''}</td>"
            f"<td class=\"num\">{'$' + num(tprice, 1) if tprice is not None else '—'}</td>"
            f"<td class=\"num {vs_cls}\">{gdt._fmt_signed_pct(vs) if vs is not None else '—'}</td></tr>"
        )

    rows = [
        row("Bull", p_bull, bull_p),
        row("Base", p_base, base_p),
        row("Bear", p_bear, bear_p),
    ]
    scenario_rows = "\n".join(rows) if scenario_meta else "    <tr><td colspan=\"4\">—（無 scenario_meta）</td></tr>"

    note_bits = []
    if upside5y is not None:
        note_bits.append(f"Base 5Y 價由 upside_5y {upside5y}% 換算")
    note = "；".join(note_bits) if note_bits else "—"

    eps_base = (((sm.get("scenario_tree") or {}).get("eps") or {}).get("base")) or []
    if eps_base:
        end_year = _terminal_year(scenario_meta)
        if end_year:
            start_year = end_year - len(eps_base) + 1
            labels = [f"FY{str(y)[-2:]}" for y in range(start_year, end_year + 1)]
        else:
            labels = [f"Y{i + 1}" for i in range(len(eps_base))]
        eps_html = "\n".join(
            f"    <div><span>{esc(lab)}</span>{esc(num(v, 2))}</div>"
            for lab, v in zip(labels, eps_base)
        )
        try:
            cum = (eps_base[-1] / eps_base[0] - 1) * 100.0 if eps_base[0] else None
        except (TypeError, ZeroDivisionError):
            cum = None
        eps_note = "Base EPS 路徑" + (f"，累積 {gdt._fmt_signed_pct(cum)}" if cum is not None else "")
    else:
        eps_html = "    <div>—</div>"
        eps_note = "—（無 EPS 路徑資料）"

    return scenario_rows, note, eps_html, eps_note


def render_val_kv(j):
    aa = j.get("appendix_a") or {}
    val = j.get("valuation") or {}
    industry = j.get("industry") or {}
    gov = j.get("governance") or {}
    growth = j.get("growth") or {}

    rows = [
        ("Fwd PE FY2", f"{val.get('fwd_pe')}x" if val.get("fwd_pe") is not None else None),
        ("PEG FY2", val.get("peg")),
        ("5Y 分位", f"{val.get('percentile_5y')}%" if val.get("percentile_5y") is not None else None),
        ("品質分", f"{aa.get('quality_score')}／capalloc {gov.get('capalloc_grade')}" if aa.get("quality_score") is not None else None),
        ("成長持續期", f"{aa.get('growth_durability')}／長期信心 {aa.get('long_term_confidence')}" if aa.get("growth_durability") is not None else None),
        ("產業時鐘", industry.get("clock_phase")),
        ("賣方共識", (val.get("targets") or {}).get("consensus_pt")),
        ("Y5 後跑道", growth.get("runway_post_y5")),
    ]
    out = []
    for label, v in rows:
        out.append(f"    <dt>{esc(label)}</dt><dd>{dash(v)}</dd>")
    return "\n".join(out)


def render_decision_audit(j, decision_audit_html):
    if decision_audit_html:
        return decision_audit_html
    frag = gdt.render_audit_html(j)
    if frag:
        return frag
    return "<p>—（judgment 未含 decision_out.audit_rows）</p>"


def render_contradictions(j):
    rows = j.get("contradictions") or []
    if not rows:
        return '    <tr><td colspan="5">—</td></tr>'
    out = []
    for c in rows:
        out.append(
            "    <tr><td>{axis}</td><td>{a}</td><td>{b}</td><td>{ruling}</td><td>{settle}</td></tr>".format(
                axis=esc(c.get("axis")), a=esc(c.get("side_a")), b=esc(c.get("side_b")),
                ruling=esc(c.get("ruling")), settle=esc(c.get("settle_metric")),
            )
        )
    return "\n".join(out)


def render_premortem(j):
    prem = j.get("premortem") or {}
    max_dd = prem.get("max_dd") or {}
    parts = []
    if prem.get("failure_story"):
        parts.append(f"<p><b>失敗故事</b>：{esc(prem['failure_story'])}</p>")
    if prem.get("second_failure"):
        parts.append(f"<p><b>第二敗局</b>：{esc(prem['second_failure'])}</p>")
    blind_spots = prem.get("blind_spots") or []
    if blind_spots:
        items = "".join(f"<li>{esc(b)}</li>" for b in blind_spots)
        parts.append(f"<p><b>盲點</b></p><ul>{items}</ul>")
    if max_dd:
        lo, hi = max_dd.get("lo"), max_dd.get("hi")
        parts.append(
            "<p><b>Max DD</b> {lo}%～{hi}%（路徑風險 {pr}）：{tt}</p>".format(
                lo=esc(lo), hi=esc(hi), pr=esc(max_dd.get("path_risk")),
                tt=esc(max_dd.get("trigger_time")),
            )
        )
    return "\n  ".join(parts) if parts else "<p>—</p>"


def render_catalysts(j):
    cats = j.get("catalysts") or []
    if not cats:
        return '    <tr><td colspan="4">—</td></tr>'
    out = []
    for c in cats:
        out.append(
            "    <tr><td class=\"num\">{d}</td><td>{e}</td><td>{w}</td><td>{i}</td></tr>".format(
                d=esc(c.get("date")), e=esc(c.get("event")), w=esc(c.get("watch")),
                i=esc(c.get("impact")),
            )
        )
    return "\n".join(out)


def render_exec_rows(j):
    dout = j.get("decision_out") or {}
    pacing = dout.get("pacing")
    pacing_txt = "；".join(pacing) if isinstance(pacing, list) else pacing
    rows = [
        ("執行摘要", dout.get("exec_line")),
        ("反轉／加碼觸發", dout.get("rearm_trigger")),
        ("配速", pacing_txt),
        ("持有上限", dout.get("holding_cap")),
    ]
    out = []
    for label, v in rows:
        out.append(f"    <tr><td><b>{esc(label)}</b></td><td>{dash(v)}</td></tr>")
    return "\n".join(out)


def _collect_evidence_refs(j):
    """Best-effort index of anything the judgment already claims as an
    evidence_refs / evidence_dismissed pointer, wherever in the tree it
    lives. Current v16 fixtures (2026-09-05) carry neither field yet -- this
    walk is forward-compatible, not fabricated: absent data renders '—'."""
    refs = set()
    dismissed = {}

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "evidence_refs" and isinstance(v, list):
                    for r in v:
                        refs.add(str(r))
                elif k == "evidence_dismissed" and isinstance(v, list):
                    for d in v:
                        if isinstance(d, dict) and d.get("ref"):
                            dismissed[str(d["ref"])] = d.get("reason")
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(j)
    return refs, dismissed


def render_negative_evidence(j, evidence):
    if not evidence:
        return '    <tr><td colspan="4">—（無 evidence.json）</td></tr>'
    coverage = evidence.get("coverage") or {}
    refs, dismissed = _collect_evidence_refs(j)
    out = []
    for axis, axv in coverage.items():
        for f in (axv.get("findings") or []):
            if f.get("direction") != "-":
                continue
            claim = f.get("claim") or ""
            src_line = f"{f.get('source') or ''}（{f.get('as_of') or '—'}）"
            key = claim
            if key in dismissed:
                disp = f"不採納：{dismissed[key]}"
            elif key in refs or axis in refs:
                disp = "已採納"
            else:
                disp = "—（judgment 未列 evidence_refs／evidence_dismissed，此版 schema 未附）"
            out.append(
                "    <tr><td>{axis}</td><td>{claim}</td><td>{src}</td><td>{disp}</td></tr>".format(
                    axis=esc(axis), claim=esc(claim[:200]), src=esc(src_line), disp=esc(disp),
                )
            )
    if not out:
        return '    <tr><td colspan="4">—（evidence 內無 direction=- 的 finding）</td></tr>'
    return "\n".join(out)


def _fallback_parse_audit(text):
    """Minimal fallback when scripts/dd_gate.py isn't available yet (WP3
    ships in parallel). Only needs the yellow-row list for this section."""
    m = re.search(r"判斷級🔴\s*=\s*(\d+)", text)
    red = int(m.group(1)) if m else 0
    yellow_rows = []
    for line in text.splitlines():
        if line.strip().startswith("|") and "🟡" in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            yellow_rows.append(cells)
    return {"red": red, "yellow_rows": yellow_rows}


def render_gate_yellow(audit_path):
    if not audit_path or not Path(audit_path).exists():
        return "<p>—（本次未提供 gate audit）</p>"
    text = Path(audit_path).read_text(encoding="utf-8")
    if dd_gate is not None and hasattr(dd_gate, "parse_audit"):
        try:
            parsed = dd_gate.parse_audit(str(audit_path))
        except Exception:
            parsed = None
    else:
        parsed = None
    if parsed:
        findings = [f for f in parsed.get("findings", []) if f.get("level") == "🟡"]
        if not findings:
            return "<p>🟡 = 0</p>"
        items = "".join(
            f"<li><b>{esc(f.get('axis'))}</b>：{esc(f.get('note'))}"
            f"（{esc(f.get('path'))}）</li>"
            for f in findings
        )
        return f"<ul>{items}</ul>"
    parsed_fb = _fallback_parse_audit(text)
    if not parsed_fb["yellow_rows"]:
        return "<p>（未解析出 🟡 表格列，見 gate audit 原文）</p>"
    items = "".join("<li>" + " ／ ".join(esc(c) for c in row) + "</li>" for row in parsed_fb["yellow_rows"])
    return f"<ul>{items}</ul>"


def render_reasoning(j):
    reasoning = j.get("reasoning") or {}
    if not reasoning:
        return "  <p>—</p>"
    out = []
    for k, v in reasoning.items():
        out.append(
            f'  <details class="reasoning"><summary>{esc(k)}</summary><p>{esc(v)}</p></details>'
        )
    return "\n".join(out)


# ---------------------------------------------------------------------------
# main assembly
# ---------------------------------------------------------------------------

def build_brief_html(j, scenario_meta, evidence, audit_path, decision_audit_html):
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    meta_top = j.get("meta") or {}
    ticker = meta_top.get("ticker") or ""
    date = meta_top.get("date") or ""

    eyebrow, h1, oneliner, meta_box = render_header(j, evidence)
    scenario_rows, scenario_note, scenario_eps, scenario_eps_note = render_scenario(j, scenario_meta)

    meta = gdt.build_dd_meta(j, scenario_meta)
    meta["brief"] = True
    dd_meta_script = gdt.render_dd_meta_html(meta)

    tokens = {
        "{{TITLE}}": esc(f"{ticker} 速判 {date}"),
        "{{EYEBROW}}": eyebrow,
        "{{H1}}": h1,
        "{{ONELINER}}": oneliner,
        "{{META_BOX}}": meta_box,
        "{{TILES}}": render_tiles(j, scenario_meta),
        "{{H_TABLE}}": gdt.render_e2_html(j),
        "{{R_LIST}}": render_r_list(j),
        "{{SINGLE_THING}}": render_single_thing(j),
        "{{SCENARIO_ROWS}}": scenario_rows,
        "{{SCENARIO_NOTE}}": esc(scenario_note),
        "{{SCENARIO_EPS}}": scenario_eps,
        "{{SCENARIO_EPS_NOTE}}": esc(scenario_eps_note),
        "{{VAL_KV}}": render_val_kv(j),
        "{{DECISION_AUDIT}}": render_decision_audit(j, decision_audit_html),
        "{{CONTRADICTIONS_ROWS}}": render_contradictions(j),
        "{{PREMORTEM}}": render_premortem(j),
        "{{TRIGGERS_TABLE}}": gdt.render_e12_html(j),
        "{{EXEC_ROWS}}": render_exec_rows(j),
        "{{CATALYST_ROWS}}": render_catalysts(j),
        "{{NEGATIVE_EVIDENCE_ROWS}}": render_negative_evidence(j, evidence),
        "{{GATE_YELLOW}}": render_gate_yellow(audit_path),
        "{{REASONING_DETAILS}}": render_reasoning(j),
        "{{FOOTER}}": (
            "頁面由 judgment.json 零 LLM 渲染；dd-meta 欄位與完整版同義，加 brief:true。"
            "完整散文版可隨時從同一份判斷物補跑。"
        ),
        "{{DD_META_SCRIPT}}": dd_meta_script,
    }
    out = template
    for token, value in tokens.items():
        out = out.replace(token, value)
    return out


def resolve_paths(args):
    if args.run_dir:
        d = Path(args.run_dir)
        judgment = d / "judgment.json"
        scenario_meta = d / "scenario_meta.json"
        evidence = d / "evidence.json"
        audit = d / "gate_audit.md"
        decision_audit = d / "tables" / "audit.html"
    else:
        judgment = Path(args.judgment) if args.judgment else None
        scenario_meta = Path(args.scenario_meta) if args.scenario_meta else None
        evidence = Path(args.evidence) if args.evidence else None
        audit = Path(args.audit) if args.audit else None
        decision_audit = Path(args.decision_audit) if args.decision_audit else None
    return judgment, scenario_meta, evidence, audit, decision_audit


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", help="per-run directory holding judgment.json etc.")
    ap.add_argument("--judgment", help="judgment.json path (ignored if --run-dir given)")
    ap.add_argument("--scenario-meta", help="scenario_meta.json path")
    ap.add_argument("--evidence", help="evidence.json path")
    ap.add_argument("--audit", help="gate_audit.md path (cross-model gate output)")
    ap.add_argument("--decision-audit", help="pre-rendered decision-matrix audit HTML fragment (tables/audit.html)")
    ap.add_argument("--out", required=True, help="output HTML path")
    args = ap.parse_args()

    judgment_path, scenario_meta_path, evidence_path, audit_path, decision_audit_path = resolve_paths(args)

    if not judgment_path or not judgment_path.exists():
        print(f"ERROR: judgment file not found: {judgment_path}", file=sys.stderr)
        sys.exit(1)

    j = load_json(judgment_path)
    scenario_meta = load_json(scenario_meta_path)
    evidence = load_json(evidence_path)
    decision_audit_html = None
    if decision_audit_path and decision_audit_path.exists():
        decision_audit_html = decision_audit_path.read_text(encoding="utf-8")

    html_out = build_brief_html(j, scenario_meta, evidence, audit_path, decision_audit_html)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
