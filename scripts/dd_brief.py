#!/usr/bin/env python3
"""dd_brief.py — WP4a/WP5c: zero-LLM "quick verdict" (速判) HTML renderer.

Reads a v16/v17 judgment.json (+ scenario_meta.json, evidence.json, optional
gate audit / decision-matrix audit fragment) and mechanically renders a
one-page brief, `scripts/dd_templates/brief.html` filled in with `{{TOKEN}}`
placeholders. No LLM call, no network. Reuses scripts/gen_dd_tables.py's
dd-meta builder and E12 (triggers) table fragment verbatim rather than
re-implementing them.

v17 (2026-09-05, WP5c): the page is now plain-language-first. The judgment
agent writes a `plain` block (see notes/site-internal/dd/_wp_spec_v17_batch3
_20260905.md) straight into judgment.json at judgment time; this script only
reads `judgment.get('plain')` and renders it verbatim. When `plain` (or one
of its sub-fields) is absent, each section falls back to a mechanical
rendering of the underlying structured fields (never raises, never leaves a
"{{" placeholder) and is wrapped in `class="fallback"` so the page visually
flags which prose is judgment-agent-authored vs. machine-assembled.

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


def _truncate(s, n=60):
    s = str(s)
    return s if len(s) <= n else s[:n] + "…"


# ---------------------------------------------------------------------------
# header
# ---------------------------------------------------------------------------

def render_header(j, evidence):
    meta_top = j.get("meta") or {}
    di = j.get("decision_inputs") or {}
    dout = j.get("decision_out") or {}
    thesis = j.get("thesis") or {}
    plain = j.get("plain") or {}

    ticker = meta_top.get("ticker") or ""
    company = meta_top.get("company_name") or ticker
    archetype = di.get("archetype") or j.get("archetype") or ""
    eyebrow = f"DD 速判 · {esc(ticker)} {esc(company)} · {esc(archetype)}"

    verdict_line = plain.get("verdict_line")
    verdict = verdict_line or dout.get("verdict") or "—"
    role = dout.get("role")
    h1 = esc(verdict) + (f' <span class="role">｜{esc(role)}</span>' if role else "")

    verdict_sub = plain.get("verdict_sub")
    if verdict_sub:
        sub, sub_fallback = esc(verdict_sub), False
    else:
        oneliner = j.get("oneliner") or thesis.get("headline") or ""
        sub, sub_fallback = (esc(oneliner), True) if oneliner else ("—", True)

    price = di.get("price_at_dd")

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
        prior_line = "—（首份）"

    meta_box = (
        f'判斷日 <b>{dash(meta_top.get("date"))}</b><br>\n'
        f'    現價 <b>{"$" + esc(num(price, 2)) if price is not None else "—"}</b><br>\n'
        f"    前份 <b>{prior_line}</b>"
    )
    return eyebrow, h1, sub, sub_fallback, meta_box


# ---------------------------------------------------------------------------
# tiles (unchanged from WP4a)
# ---------------------------------------------------------------------------

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
    runway_small = f"內生天花板 {endo}%" if isinstance(endo, (int, float)) else None

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


# ---------------------------------------------------------------------------
# plain-language sections (v17 WP5c)
# ---------------------------------------------------------------------------

_FIVE_ORDER = [
    ("how_it_makes_money", "這家公司靠什麼賺錢"),
    ("why_now", "為什麼現在值得或不值得"),
    ("why_this_size", "為什麼是這個倉位／節奏"),
    ("biggest_fear", "我最怕什麼"),
    ("how_to_act", "怎麼做"),
]


def render_five(j):
    five = ((j.get("plain") or {}).get("five")) or {}
    if not five:
        oneliner = j.get("oneliner") or (j.get("thesis") or {}).get("headline")
        return (f"    <p>{dash(oneliner)}</p>", True)
    parts = [
        f"    <p><b>{label}</b>：{dash(five.get(key))}</p>"
        for key, label in _FIVE_ORDER
    ]
    return "\n".join(parts), False


def render_business(j):
    business = ((j.get("plain") or {}).get("business")) or {}
    moat = j.get("moat") or {}
    fallback = not business
    moat_bits = f"{moat.get('grade') or ''} {moat.get('trend') or ''}".strip()
    moat_fallback = esc(moat_bits) if moat_bits else "—"
    parts = [
        f"    <p><b>賣什麼給誰、怎麼收錢</b>：{dash(business.get('what_to_whom'))}</p>",
        f"    <p><b>客戶為什麼離不開</b>：{dash(business.get('why_customers_stay'))}</p>",
        f"    <p><b>護城河等級、方向與最弱處</b>："
        f"{esc(business['moat_direction']) if business.get('moat_direction') else moat_fallback}</p>",
    ]
    return "\n".join(parts), fallback


def render_bets(j):
    bets = ((j.get("plain") or {}).get("bets")) or []
    if bets:
        items = "\n".join(
            f"    <li><b>{esc(b.get('claim'))}</b>"
            f"<br><span class=\"note\">算錯的門檻：{esc(b.get('wrong_when'))}</span></li>"
            for b in bets[:3]
        )
        return items, False
    H = (j.get("thesis") or {}).get("H") or []
    if not H:
        return "    <li>—</li>", True
    items = "\n".join(
        f"    <li><b>{esc(h.get('text'))}</b>"
        f"<br><span class=\"note\">算錯的門檻：{esc(h.get('threshold'))}</span></li>"
        for h in H[:3]
    )
    return items, True


def render_fears(j):
    fears = ((j.get("plain") or {}).get("fears")) or []
    if fears:
        items = "\n".join(
            f"    <li><span class=\"tag\">{esc(f.get('clock'))}</span>{esc(f.get('text'))}</li>"
            for f in fears[:3]
        )
        return items, False
    R = (j.get("thesis") or {}).get("R") or []
    if not R:
        return "    <li>—</li>", True
    items = "\n".join(
        f"    <li><span class=\"tag\">{esc(r.get('clock'))}</span>{esc(r.get('text'))}"
        f"<br><span class=\"note\">門檻：{esc(r.get('threshold'))}</span></li>"
        for r in R[:3]
    )
    return items, True


def render_market_wrong(j):
    plain = j.get("plain") or {}
    market_wrong = plain.get("market_wrong")
    if market_wrong:
        return f"    <p>{esc(market_wrong)}</p>", False
    fallback = ((j.get("valuation") or {}).get("targets") or {}).get("market_wrong_where")
    return f"    <p>{dash(fallback)}</p>", True


def _growth_cell(v):
    if v is None or v == "":
        return "—"
    try:
        f = float(v)
        return f"{f:g}%"
    except (TypeError, ValueError):
        return esc(_truncate(v, 60))


def _implied_cagr(valuation):
    blob = json.dumps(valuation or {}, ensure_ascii=False)
    m = re.search(r"CAGR[^\d%]{0,10}([\d.]+%(?:[~～\-–][\d.]+%)?)", blob)
    return m.group(1) if m else None


def render_growth_table(j):
    rd = (j.get("moat") or {}).get("roic_durability") or {}
    val = j.get("valuation") or {}
    rows = [
        ("增量投資報酬率（ROIIC）", _growth_cell(rd.get("roiic"))),
        ("再投資率", _growth_cell(rd.get("reinvest_rate"))),
        ("自己賺的錢能撐的成長上限", _growth_cell(rd.get("endo_ceiling"))),
        ("市場隱含成長（CAGR）", dash(_implied_cagr(val))),
    ]
    return "\n".join(
        f'    <tr><td>{esc(label)}</td><td class="num">{value}</td></tr>'
        for label, value in rows
    )


def render_growth_funding(j):
    growth_funding = (j.get("plain") or {}).get("growth_funding")
    if growth_funding:
        return esc(growth_funding), False
    return "—", True


def render_how_to_lose(j):
    how_to_lose = (j.get("plain") or {}).get("how_to_lose")
    if how_to_lose:
        return f"    <p>{esc(how_to_lose)}</p>", False
    return render_premortem(j), True


# ---------------------------------------------------------------------------
# scenario tree + stories
# ---------------------------------------------------------------------------

def render_scenario(j, scenario_meta):
    di = j.get("decision_inputs") or {}
    price = di.get("price_at_dd")
    sm = scenario_meta or {}
    bull_p, bear_p = sm.get("bull_5y_price"), sm.get("bear_5y_price")
    p_bull, p_bear = sm.get("p_bull_pct"), sm.get("p_bear_pct")
    p_base = (100 - p_bull - p_bear) if (p_bull is not None and p_bear is not None) else None
    upside5y = sm.get("upside_5y_pct")
    base_p = (price * (1 + upside5y / 100.0)) if (price is not None and upside5y is not None) else None

    scenario_tree = sm.get("scenario_tree") or {}
    eps_map = scenario_tree.get("eps") or {}
    pe_map = scenario_tree.get("pe") or {}

    def terminal(key):
        arr = eps_map.get(key) or []
        eps_t = arr[-1] if arr else None
        pe_t = pe_map.get(key)
        return eps_t, pe_t

    def vs_now(target):
        if price in (None, 0) or target is None:
            return None
        return (target / price - 1) * 100.0

    def row(label, prob, tprice, key):
        vs = vs_now(tprice)
        vs_cls = "ok" if (vs is not None and vs >= 0) else ("bad" if vs is not None else "")
        eps_t, pe_t = terminal(key)
        return (
            f"    <tr><td>{esc(label)}</td>"
            f"<td class=\"num\">{esc(prob)}{'%' if prob is not None else ''}</td>"
            f"<td class=\"num\">{num(eps_t, 2) if eps_t is not None else '—'}</td>"
            f"<td class=\"num\">{num(pe_t, 0) + 'x' if pe_t is not None else '—'}</td>"
            f"<td class=\"num\">{'$' + num(tprice, 1) if tprice is not None else '—'}</td>"
            f"<td class=\"num {vs_cls}\">{gdt._fmt_signed_pct(vs) if vs is not None else '—'}</td></tr>"
        )

    rows = [
        row("Bull", p_bull, bull_p, "bull"),
        row("Base", p_base, base_p, "base"),
        row("Bear", p_bear, bear_p, "bear"),
    ]
    scenario_rows = "\n".join(rows) if scenario_meta else '    <tr><td colspan="6">—（無 scenario_meta）</td></tr>'

    note_bits = []
    if upside5y is not None:
        note_bits.append(f"Base 5Y 價由 upside_5y {upside5y}% 換算")
    note = "；".join(note_bits) if note_bits else "—"

    eps_base = eps_map.get("base") or []
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


def _terminal_year(scenario_meta):
    tl = ((scenario_meta or {}).get("scenario_tree") or {}).get("terminal_label") or ""
    m = re.search(r"FY(\d{4})", tl)
    return int(m.group(1)) if m else None


def render_stories(j):
    stories = (j.get("plain") or {}).get("stories") or {}
    fallback = not stories
    labels = [("bull", "Bull 怎麼發生"), ("base", "Base 怎麼發生"), ("bear", "Bear 怎麼發生")]
    parts = [
        f'    <div class="story"><b>{label}</b>：{dash(stories.get(key))}</div>'
        for key, label in labels
    ]
    return "\n".join(parts), fallback


# ---------------------------------------------------------------------------
# change-my-mind + prior compare + rulings
# ---------------------------------------------------------------------------

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def render_change_my_mind(j):
    cmm = (j.get("plain") or {}).get("change_my_mind") or []
    if cmm:
        rows = "\n".join(
            "    <tr><td>{w}</td><td>{t}</td><td>{n}</td><td class=\"num\">{d}</td></tr>".format(
                w=esc(c.get("what")), t=esc(c.get("threshold")), n=esc(c.get("then")),
                d=dash(c.get("when")),
            )
            for c in cmm[:3]
        )
        return rows, False
    triggers = j.get("triggers") or []
    if not triggers:
        return '    <tr><td colspan="4">—</td></tr>', True
    rows = "\n".join(
        "    <tr><td>{w}</td><td>{t}</td><td>{n}</td><td class=\"num\">{d}</td></tr>".format(
            w=esc(t.get("text")), t=esc(t.get("threshold")), n=esc(t.get("action")),
            d=dash(t.get("date")),
        )
        for t in triggers[:3]
    )
    return rows, True


def render_next_checkpoint(j):
    triggers = j.get("triggers") or []
    dated = [t for t in triggers if _DATE_RE.match(str(t.get("date") or ""))]
    if not dated:
        return "下一個檢核點：—"
    dated.sort(key=lambda t: t["date"])
    nxt = dated[0]
    return f"下一個檢核點：<b>{esc(nxt.get('date'))} {esc(_truncate(nxt.get('text') or '', 40))}</b>"


_PRIOR_ROWS = [
    ("裁決", "dca_verdict", "dca_verdict"),
    ("股價", "price_at_dd", "price_at_dd"),
    ("5 年期望報酬", "ev5y_pct", "ev5y_pct"),
    ("Base 年化", "irr_base_pct", "irr_base_pct"),
    ("估值燈", "val", "val"),
    ("Bear 機率", "p_bear_pct", "p_bear_pct"),
]


def render_prior_compare(j, evidence, meta):
    prior = (evidence or {}).get("prior_dd") or {}
    prior_meta = prior.get("prior_meta") or {}
    if not prior_meta:
        return '    <tr><td colspan="3">—（首份，無前份可比）</td></tr>'
    rows = []
    for label, cur_key, prior_key in _PRIOR_ROWS:
        cur_v = meta.get(cur_key)
        prior_v = prior_meta.get(prior_key)
        if cur_key == "price_at_dd" and cur_v is not None:
            cur_v = "$" + num(cur_v, 2)
        if prior_key == "price_at_dd" and prior_v is not None:
            prior_v = "$" + num(prior_v, 2)
        rows.append(
            f"    <tr><td>{esc(label)}</td>"
            f'<td class="num">{dash(prior_v)}</td>'
            f'<td class="num">{dash(cur_v)}</td></tr>'
        )
    return "\n".join(rows)


def render_prior_reason(j):
    reason = (j.get("plain") or {}).get("prior_compare_reason")
    if reason:
        return esc(reason), False
    return "—", True


def render_rulings(j):
    contradictions = j.get("contradictions") or []
    debates = [c for c in contradictions if not c.get("prior_field")]
    if not debates:
        return "    <li>—</li>"
    items = []
    for c in debates:
        axis = c.get("axis") or ""
        topic = re.split(r"[:：]", axis, maxsplit=1)[0]
        items.append(
            "    <li><b>{topic}</b>：{a} 對 {b}。<b>裁定</b>：{ruling}</li>".format(
                topic=esc(_truncate(topic, 30)), a=esc(_truncate(c.get("side_a") or "", 120)),
                b=esc(_truncate(c.get("side_b") or "", 120)), ruling=esc(_truncate(c.get("ruling") or "", 160)),
            )
        )
    return "\n".join(items)


# ---------------------------------------------------------------------------
# reused / lightly-adapted mechanical renderers
# ---------------------------------------------------------------------------

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


def _collect_evidence_refs(j):
    """Best-effort index of anything the judgment already claims as an
    evidence_refs / evidence_dismissed pointer, wherever in the tree it
    lives. Forward-compatible with v17 schema addition -- absent data
    renders '—', never fabricated."""
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
                disp = "—（judgment 未列 evidence_refs／evidence_dismissed）"
            out.append(
                "    <tr><td>{axis}</td><td>{claim}</td><td>{src}</td><td>{disp}</td></tr>".format(
                    axis=esc(axis), claim=esc(claim[:200]), src=esc(src_line), disp=esc(disp),
                )
            )
    if not out:
        return '    <tr><td colspan="4">—（evidence 內無 direction=- 的 finding）</td></tr>'
    return "\n".join(out)


def render_decision_audit(j, decision_audit_html):
    if decision_audit_html:
        return decision_audit_html
    frag = gdt.render_audit_html(j)
    if frag:
        return frag
    return "<p>—（judgment 未含 decision_out.audit_rows）</p>"


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


def _audit_counts(text):
    red = re.search(r"🔴\s*[=＝]?\s*(\d+)", text)
    yellow = re.search(r"🟡\s*[=＝]?\s*(\d+)", text)
    return (red.group(1) if red else None, yellow.group(1) if yellow else None)


def render_gate_yellow(audit_path):
    if not audit_path or not Path(audit_path).exists():
        return "<p>—（本次未提供 gate audit）</p>"
    text = Path(audit_path).read_text(encoding="utf-8")
    red, yellow = _audit_counts(text)
    summary = f"<p>跨模型冷讀：判斷級 🔴 {dash(red)}、🟡 {dash(yellow)}</p>"
    if dd_gate is not None and hasattr(dd_gate, "parse_audit"):
        try:
            parsed = dd_gate.parse_audit(str(audit_path))
        except Exception:
            parsed = None
    else:
        parsed = None
    if parsed:
        findings = [f for f in parsed.get("findings", []) if f.get("level") == "🟡"]
        if findings:
            items = "".join(
                f"<li><b>{esc(f.get('axis'))}</b>：{esc(f.get('note'))}"
                f"（{esc(f.get('path'))}）</li>"
                for f in findings
            )
            return summary + f"<ul>{items}</ul>"
        return summary
    return summary + f"<details><summary>gate audit 原文</summary><pre style=\"white-space:pre-wrap\">{esc(text)}</pre></details>"


def _audit_summary_line(audit_path):
    if not audit_path or not Path(audit_path).exists():
        return "—（本次未提供 gate audit）"
    text = Path(audit_path).read_text(encoding="utf-8")
    red, yellow = _audit_counts(text)
    return f"opus 抽查：判斷級 🔴 {dash(red)}、🟡 {dash(yellow)}"


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
# evidence quality (證據品質)
# ---------------------------------------------------------------------------

def render_evidence_quality(j, evidence, audit_path):
    plain_lead = (j.get("plain") or {}).get("evidence_quality")
    lead_html, lead_fallback = (esc(plain_lead), False) if plain_lead else ("—", True)

    if not evidence:
        rows = '    <tr><td colspan="4">—（無 evidence.json）</td></tr>'
        return lead_html, lead_fallback, rows

    coverage = evidence.get("coverage") or {}
    total_axes = len(coverage)
    found = sum(1 for v in coverage.values() if v.get("status") == "found")
    none_n = sum(1 for v in coverage.values() if v.get("status") == "none")
    total_findings = sum(len(v.get("findings") or []) for v in coverage.values())
    neg = sum(
        1 for v in coverage.values() for f in (v.get("findings") or []) if f.get("direction") == "-"
    )
    coverage_cell = f"{found}/{total_axes} 軸有料，{none_n} 軸查無"

    numbers = evidence.get("numbers") or {}
    lqk = numbers.get("latest_quarter_kpis") or {}
    quarter = str(lqk.get("quarter") or "").split("（")[0].strip() or "—"
    numbers_cell = f"{quarter}，共 {total_findings} 條 finding，其中 {neg} 條負向" if quarter != "—" else dash(None)

    transcripts = evidence.get("transcripts") or {}
    selected = (transcripts.get("selected") or {}).get("recent_four_quarters") or []
    if selected:
        m = re.search(r"_(Q\d)_(\d{4})_", selected[-1])
        latest_q = f"{m.group(1)} {m.group(2)}" if m else selected[-1]
        transcripts_cell = f"{latest_q} 法說親讀；前 {max(len(selected) - 1, 0)} 季讀摘要"
    else:
        transcripts_cell = "—"

    audit_cell = _audit_summary_line(audit_path)

    canonical_id = (evidence.get("canonical_id") or {}).get("primary") or {}
    if canonical_id.get("theme"):
        id_cell = f"{canonical_id['theme']}（as-of {canonical_id.get('as_of') or '—'}）"
    else:
        id_cell = "—"

    ledger = evidence.get("ledger") or {}
    cv = ledger.get("current_verdict") or {}
    history = ledger.get("decision_history") or []
    if cv:
        ledger_cell = f"前份 {cv.get('date')} {cv.get('verdict')}；帳本 {len(history)} 筆歷史"
    else:
        ledger_cell = "—"

    rows = (
        f'    <tr><td>覆蓋軸</td><td>{esc(coverage_cell)}</td>'
        f'<td>營運數字</td><td>{esc(numbers_cell)}</td></tr>\n'
        f'    <tr><td>逐字稿</td><td>{esc(transcripts_cell)}</td>'
        f'<td>跨模型冷讀</td><td>{esc(audit_cell)}</td></tr>\n'
        f'    <tr><td>產業報告對帳</td><td>{esc(id_cell)}</td>'
        f'<td>知識帳本</td><td>{esc(ledger_cell)}</td></tr>'
    )
    return lead_html, lead_fallback, rows


# ---------------------------------------------------------------------------
# main assembly
# ---------------------------------------------------------------------------

def _cls(fallback: bool) -> str:
    return " fallback" if fallback else ""


def build_brief_html(j, scenario_meta, evidence, audit_path, decision_audit_html):
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    meta_top = j.get("meta") or {}
    ticker = meta_top.get("ticker") or ""
    date = meta_top.get("date") or ""

    eyebrow, h1, sub, sub_fallback, meta_box = render_header(j, evidence)
    scenario_rows, scenario_note, scenario_eps, scenario_eps_note = render_scenario(j, scenario_meta)
    stories_html, stories_fallback = render_stories(j)
    five_html, five_fallback = render_five(j)
    business_html, business_fallback = render_business(j)
    bets_html, bets_fallback = render_bets(j)
    fears_html, fears_fallback = render_fears(j)
    market_wrong_html, market_wrong_fallback = render_market_wrong(j)
    growth_funding_html, growth_funding_fallback = render_growth_funding(j)
    change_rows, change_fallback = render_change_my_mind(j)
    how_to_lose_html, how_to_lose_fallback = render_how_to_lose(j)
    prior_reason, prior_reason_fallback = render_prior_reason(j)
    evidence_lead, evidence_lead_fallback, evidence_rows = render_evidence_quality(j, evidence, audit_path)

    meta = gdt.build_dd_meta(j, scenario_meta)
    meta["brief"] = True
    dd_meta_script = gdt.render_dd_meta_html(meta)

    tokens = {
        "{{TITLE}}": esc(f"{ticker} 速判 {date}"),
        "{{EYEBROW}}": eyebrow,
        "{{H1}}": h1,
        "{{SUB_CLASS}}": _cls(sub_fallback),
        "{{SUB}}": sub,
        "{{META_BOX}}": meta_box,
        "{{TILES}}": render_tiles(j, scenario_meta),
        "{{FIVE_CLASS}}": _cls(five_fallback),
        "{{FIVE_HTML}}": five_html,
        "{{BUSINESS_CLASS}}": _cls(business_fallback),
        "{{BUSINESS_HTML}}": business_html,
        "{{BETS_CLASS}}": _cls(bets_fallback).strip(),
        "{{BETS_HTML}}": bets_html,
        "{{FEARS_CLASS}}": _cls(fears_fallback).strip(),
        "{{FEARS_HTML}}": fears_html,
        "{{MARKET_WRONG_CLASS}}": _cls(market_wrong_fallback),
        "{{MARKET_WRONG_HTML}}": market_wrong_html,
        "{{GROWTH_TABLE_ROWS}}": render_growth_table(j),
        "{{GROWTH_FUNDING_CLASS}}": _cls(growth_funding_fallback),
        "{{GROWTH_FUNDING_HTML}}": growth_funding_html,
        "{{SCENARIO_ROWS}}": scenario_rows,
        "{{SCENARIO_NOTE}}": esc(scenario_note),
        "{{SCENARIO_EPS}}": scenario_eps,
        "{{SCENARIO_EPS_NOTE}}": esc(scenario_eps_note),
        "{{STORIES_CLASS}}": _cls(stories_fallback).strip(),
        "{{STORIES_HTML}}": stories_html,
        "{{CHANGE_ROWS}}": change_rows,
        "{{NEXT_CHECKPOINT}}": render_next_checkpoint(j),
        "{{PRIOR_TABLE_ROWS}}": render_prior_compare(j, evidence, meta),
        "{{PRIOR_REASON_CLASS}}": ("note" + _cls(prior_reason_fallback)).strip(),
        "{{PRIOR_REASON}}": prior_reason,
        "{{RULINGS_HTML}}": render_rulings(j),
        "{{HOW_TO_LOSE_CLASS}}": _cls(how_to_lose_fallback),
        "{{HOW_TO_LOSE_HTML}}": how_to_lose_html,
        "{{EXEC_ROWS}}": render_exec_rows(j),
        "{{EVIDENCE_LEAD_CLASS}}": _cls(evidence_lead_fallback),
        "{{EVIDENCE_LEAD}}": evidence_lead,
        "{{EVIDENCE_TABLE_ROWS}}": evidence_rows,
        "{{TRIGGERS_TABLE}}": gdt.render_e12_html(j),
        "{{CATALYST_ROWS}}": render_catalysts(j),
        "{{NEGATIVE_EVIDENCE_ROWS}}": render_negative_evidence(j, evidence),
        "{{DECISION_AUDIT}}": render_decision_audit(j, decision_audit_html),
        "{{GATE_YELLOW}}": render_gate_yellow(audit_path),
        "{{REASONING_DETAILS}}": render_reasoning(j),
        "{{FOOTER}}": (
            "頁面由 judgment.json 零 LLM 渲染；dd-meta 欄位與完整版同義，加 brief:true。"
            "白話段落來源：judgment.json 的 plain 欄，由判斷 agent 與判斷同時寫；"
            "標灰（fallback）段落表示這次判斷物未附 plain，改用結構欄位機械組成。"
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
