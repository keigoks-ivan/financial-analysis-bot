#!/usr/bin/env python3
"""gen_dd_tables.py — WP1c: judgment.json -> mechanical DD table/dd-meta HTML.

Reads a v16 judgment.json (schema: scripts/dd_schema/judgment.schema.json,
field derivation: scripts/dd_schema/judgment-to-ddmeta.md) and writes the
mechanical fragments that used to be hand-written by the Stage 2 writer:

  dashboard.html   page-header dashboard (status-bar + hypothesis-box, per
                   .claude/skills/stock-analyst/references/html-output.md
                   "頁首結論儀表板" template)
  e2.html          SS2.B three-assumption table (H1-H3)
  e12.html         <table id="triggers"> monitoring/trigger table (SS13 tail)
  dd-meta.html     <script id="dd-meta" type="application/json"> block
  appA-table.html  Appendix A one-row mechanical grade table
  audit.html       <details class="audit"> block (only if decision_out has
                   audit_rows; omitted otherwise -- no empty-shell rendering)
  e3/e5/e6/e7/e8/e9/e10.html
                   QC-38 商業本質七表（WP1c 修法1）-- <table id="e{N}"> each,
                   sourced from industry.tam_table / moat.{spread_table,
                   competitors,roic_durability.checkpoints} / growth.segments
                   / quality.{dupont,ccc} / governance.{capital_returns,
                   scorecard}; field shapes documented in
                   scripts/dd_schema/judgment-to-ddmeta.md §五之二

Usage:
  python3 scripts/gen_dd_tables.py JUDGMENT.json --out DIR \\
      [--scenario-html E11.html] [--scenario-meta SCENARIO_META.json]

--scenario-meta, when given, overrides judgment.json's own `scenario_ref`
resolution for the six flat scenario dd-meta fields (bull_5y_price /
bear_5y_price / p_bull_pct / p_bear_pct / upside_5y_pct / scenario_tree) plus
irr_base_pct / asym_ratio / ev5y_pct fallback (decision_inputs wins when both
are present). --scenario-html, when given, is copied through verbatim to
DIR/e11.html (dd_scenario.py already owns E11's own arithmetic and HTML
build; this script never recomputes it).
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

E12_ID_TOKEN_RE = re.compile(r"[HR]\d+")


def esc(v) -> str:
    return html_lib.escape("" if v is None else str(v))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_scenario_meta(j: dict, judgment_path: Path, override: Path | None):
    if override is not None:
        if override.exists():
            return load_json(override)
        return None
    ref = j.get("scenario_ref")
    if not ref:
        return None
    ref_path = Path(ref)
    if not ref_path.is_absolute():
        ref_path = judgment_path.parent / ref
    if ref_path.exists():
        return load_json(ref_path)
    return None


# ---------------------------------------------------------------------------
# dd-meta
# ---------------------------------------------------------------------------

def derive_kill_metrics_from_triggers(triggers: list) -> list:
    """Fallback derivation when judgment.json carries no top-level
    kill_metrics[] -- see judgment-to-ddmeta.md 'kill_metrics 兩種居所'.
    Only the 3 dd-meta-required fields (metric/bear_threshold/window) are
    populated; source/last_status are omitted (not fabricated)."""
    out = []
    for t in triggers or []:
        norm_type = re.sub(r"[（(].*?[）)]", "", t.get("type") or "").strip()
        if norm_type not in ("風險", "減碼", "清倉"):
            continue
        out.append({
            "metric": t.get("metric") or "",
            "bear_threshold": t.get("threshold") or "",
            "window": t.get("source_freq") or "",
        })
    return out


def build_dd_meta(j: dict, scenario_meta: dict | None) -> dict:
    meta_top = j.get("meta") or {}
    di = j.get("decision_inputs") or {}
    aa = j.get("appendix_a") or {}
    val = j.get("valuation") or {}
    moat = j.get("moat") or {}
    growth = j.get("growth") or {}
    trap = j.get("trap_analysis") or {}
    gov = j.get("governance") or {}
    dout = j.get("decision_out") or {}
    prem = j.get("premortem") or {}
    industry = j.get("industry") or {}
    eps_meta = j.get("eps_meta") or {}

    meta = {
        "ticker": meta_top.get("ticker"),
        "schema": meta_top.get("schema"),
        "date": meta_top.get("date"),
        "price_at_dd": di.get("price_at_dd"),
        "signal": aa.get("signal"),
        "trap": trap.get("verdict"),
        "trap_label": trap.get("label"),
        "moat": moat.get("grade"),
        "val": aa.get("val"),
        "ma": aa.get("ma"),
        "fpe_fy2": aa.get("fpe_fy2"),
        "pct_5y": aa.get("pct_5y"),
        "peg_fy2": aa.get("peg_fy2"),
        "upside_short_pct": aa.get("upside_short_pct"),
        "upside_mid_pct": aa.get("upside_mid_pct"),
        "stress": aa.get("stress"),
        "moat_score": moat.get("score"),
        "growth_durability": aa.get("growth_durability"),
        "quality_score": aa.get("quality_score"),
        "ai_risk": aa.get("ai_risk"),
        "long_term_confidence": aa.get("long_term_confidence"),
        "verdict": aa.get("verdict"),
        "oneliner": j.get("oneliner"),
        "dca_verdict": dout.get("verdict"),
        "dca_role": dout.get("role"),
        "moat_trend": moat.get("trend"),
        "runway_post_y5": growth.get("runway_post_y5"),
        "ev5y_pct": di.get("ev5y_pct"),
    }

    if di.get("irr_base_pct") is not None:
        meta["irr_base_pct"] = di["irr_base_pct"]
    if di.get("asym_ratio") is not None:
        meta["asym_ratio"] = di["asym_ratio"]

    max_dd = prem.get("max_dd") or {}
    lo, hi = max_dd.get("lo"), max_dd.get("hi")
    if lo is not None and hi is not None:
        meta["max_dd_pct"] = min(lo, hi)
    elif lo is not None:
        meta["max_dd_pct"] = lo

    if scenario_meta:
        for k in ("bull_5y_price", "bear_5y_price", "p_bull_pct", "p_bear_pct",
                  "upside_5y_pct", "scenario_tree"):
            if scenario_meta.get(k) is not None:
                meta[k] = scenario_meta[k]
        for k in ("irr_base_pct", "asym_ratio", "ev5y_pct"):
            if meta.get(k) is None and scenario_meta.get(k) is not None:
                meta[k] = scenario_meta[k]

    if di.get("archetype"):
        meta["archetype"] = di["archetype"]
    rearm = dout.get("rearm_trigger")
    if rearm:
        meta["rearm_trigger"] = rearm

    if j.get("catalysts"):
        meta["catalysts"] = j["catalysts"]
    if eps_meta.get("base_eps_path"):
        meta["base_eps_path"] = eps_meta["base_eps_path"]
    if eps_meta.get("fy_end_month") is not None:
        meta["fy_end_month"] = eps_meta["fy_end_month"]
    if eps_meta.get("eps_basis"):
        meta["eps_basis"] = eps_meta["eps_basis"]

    endo = (moat.get("roic_durability") or {}).get("endo_ceiling")
    if endo is not None:
        meta["endo_growth_ceiling"] = endo
    if gov.get("capalloc_grade"):
        meta["capalloc_grade"] = gov["capalloc_grade"]
    if moat.get("execution") is not None:
        meta["moat_execution"] = moat["execution"]
    if moat.get("pricing") is not None:
        meta["moat_pricing_power"] = moat["pricing"]

    if di.get("cycle_position"):
        meta["cycle_position"] = di["cycle_position"]
    if di.get("cycle_verdict"):
        meta["cycle_verdict"] = di["cycle_verdict"]
    if industry.get("clock_phase"):
        meta["industry_clock_phase"] = industry["clock_phase"]

    km = j.get("kill_metrics") or derive_kill_metrics_from_triggers(j.get("triggers") or [])
    if km:
        meta["kill_metrics"] = km

    # v16 pipeline provenance -- verify_dd_math.py's §C module-existence check
    # reads this to switch from the legacy keyword-count heuristic to a
    # table-id existence check (<table id="e3">…id="e10">) for gen_dd_tables.py
    # output (WP1c 修法1 §11 item 1). Unconditional: this script IS the v16
    # table generator, there is no non-v16 caller.
    meta["pipeline"] = "v16"

    # Drop None values -- dd-meta contract forbids `null` for present keys
    # (validate_dd_meta.py: "must not be null (omit field instead)").
    return {k: v for k, v in meta.items() if v is not None}


def render_dd_meta_html(meta: dict) -> str:
    body = json.dumps(meta, ensure_ascii=False, indent=2)
    return f'<script id="dd-meta" type="application/json">\n{body}\n</script>\n'


# ---------------------------------------------------------------------------
# E2 -- §2.B three-assumption table
# ---------------------------------------------------------------------------

def render_e2_html(j: dict) -> str:
    H = (j.get("thesis") or {}).get("H") or []
    rows = []
    for h in H:
        rows.append(
            "<tr><td>{id}</td><td>{text}</td><td>{y2}</td><td>{y5}</td><td>{y10}</td>"
            "<td>{th}</td><td>{src}</td><td>{drift}</td></tr>".format(
                id=esc(h.get("id")), text=esc(h.get("text")),
                y2=esc(h.get("2y")), y5=esc(h.get("5y")), y10=esc(h.get("10y")),
                th=esc(h.get("threshold")), src=esc(h.get("source")),
                drift=esc(h.get("drift_rule")),
            )
        )
    header = (
        "<tr><th>#</th><th>核心假設</th><th>2Y驗證點</th><th>5Y驗證點</th>"
        "<th>10Y驗證點</th><th>具體數字門檻</th><th>信息來源</th><th>漂移觸發條件</th></tr>"
    )
    return "<table>\n" + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---------------------------------------------------------------------------
# E12 -- §13 tail monitoring/trigger table
# ---------------------------------------------------------------------------

def _type_cell(t: dict) -> str:
    """Verbatim `type_display` wins when present -- the real corpus shows the
    類型 column's parenthetical annotation is writer-controlled prose (H/R
    refs in some reports, a bare enum in others, an ad-hoc label like
    "（上行）" in at least one row of AVGO 2026-09-03), not a mechanical
    function of `maps_to`. Falls back to a best-effort reconstruction
    (canonical type + H/R tokens parsed out of maps_to) only when
    type_display wasn't captured (e.g. hand-authored judgment.json)."""
    if t.get("type_display"):
        return t["type_display"]
    norm_type = re.sub(r"[（(].*?[）)]", "", t.get("type") or "").strip()
    maps_to = t.get("maps_to") or ""
    tokens = E12_ID_TOKEN_RE.findall(maps_to)
    if tokens:
        return f"{norm_type}（{'/'.join(tokens)}）"
    return norm_type


def render_e12_html(j: dict) -> str:
    triggers = j.get("triggers") or []
    rows = []
    for t in triggers:
        rows.append(
            "<tr><td>{n}</td><td>{text}</td><td>{type_}</td><td>{maps_to}</td>"
            "<td>{thresh}</td><td>{action}</td><td>{freq}</td><td>{date}</td></tr>".format(
                n=esc(t.get("n")), text=esc(t.get("text")), type_=esc(_type_cell(t)),
                maps_to=esc(t.get("maps_to")), thresh=esc(t.get("threshold")),
                action=esc(t.get("action")), freq=esc(t.get("source_freq")),
                date=esc(t.get("date")),
            )
        )
    header = (
        "<tr><th>#</th><th>觸發器（白話一句）</th><th>類型</th><th>對應</th>"
        "<th>指標與門檻</th><th>命中後動作</th><th>資料源／頻率</th><th>⏰</th></tr>"
    )
    return '<table id="triggers">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---------------------------------------------------------------------------
# Appendix A -- one-row mechanical grade table
# ---------------------------------------------------------------------------

def render_appA_table_html(j: dict) -> str:
    aa = j.get("appendix_a") or {}
    moat = j.get("moat") or {}
    stress = aa.get("stress") or {}
    header = (
        "<tr><th>訊號</th><th>品質分（護城河/成長/財務）</th><th>估值燈</th><th>MA</th>"
        "<th>陷阱定性</th><th>壓力測試</th><th>長期持有信心</th></tr>"
    )
    row = (
        "<tr><td>{signal}</td><td>{moat_s}/{growth_d}/{quality_s}</td><td>{val}</td>"
        "<td>{ma}</td><td>{trap}</td><td>{sp}/{st}</td><td>{ltc}</td></tr>".format(
            signal=esc(aa.get("signal")), moat_s=esc(moat.get("score")),
            growth_d=esc(aa.get("growth_durability")), quality_s=esc(aa.get("quality_score")),
            val=esc(aa.get("val")), ma=esc(aa.get("ma")),
            trap=esc((j.get("trap_analysis") or {}).get("verdict")),
            sp=esc(stress.get("pass")), st=esc(stress.get("total")),
            ltc=esc(aa.get("long_term_confidence")),
        )
    )
    return "<table>\n" + header + "\n" + row + "\n</table>\n"


# ---------------------------------------------------------------------------
# audit.html -- <details class="audit"> (only when audit_rows non-empty)
# ---------------------------------------------------------------------------

def render_audit_html(j: dict) -> str | None:
    rows = (j.get("decision_out") or {}).get("audit_rows") or []
    if not rows:
        return None
    # 沿用 dd_decision.build_audit_html 的表格渲染（Row／條件／命中／依據／備註），
    # 不再把 audit_rows dict 逐行印成 <p>（2026-09-04 PANW 上站前修正）。
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    from dd_decision import build_audit_html  # noqa: E402
    return build_audit_html(j["decision_out"]) + "\n"


# ---------------------------------------------------------------------------
# E3 -- §3.F 逐段 TAM/SAM + 利潤池合一 (industry.tam_table[])
# ---------------------------------------------------------------------------

def render_e3_html(j: dict) -> str:
    rows_data = (j.get("industry") or {}).get("tam_table") or []
    rows = []
    for r in rows_data:
        rows.append(
            "<tr><td>{seg}</td><td>{now}</td><td>{y5}</td><td>{pen}</td><td>{cagr}</td>"
            "<td>{vcp}</td><td>{pp}</td></tr>".format(
                seg=esc(r.get("segment")), now=esc(r.get("tam_now")), y5=esc(r.get("tam_5y")),
                pen=esc(r.get("penetration_pct")), cagr=esc(r.get("cagr_pct")),
                vcp=esc(r.get("value_chain_position")), pp=esc(r.get("profit_pool_shift")),
            )
        )
    header = (
        "<tr><th>段</th><th>TAM(現)</th><th>TAM(5Y)</th><th>滲透率</th>"
        "<th>段CAGR</th><th>Value Chain位置</th><th>利潤池占比遷移</th></tr>"
    )
    return '<table id="e3">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---------------------------------------------------------------------------
# E5 -- 二維評分 + Moat-to-Numbers 合一 (moat.{execution,pricing,combined,
# grade} 摘要 + moat.spread_table[])
# ---------------------------------------------------------------------------

def render_e5_html(j: dict) -> str:
    moat = j.get("moat") or {}
    summary = (
        '<p class="e5-summary">執行力 {ex} ｜ 定價力 {pr} ｜ 綜合 {comb} ｜ 護城河評級 {grade}</p>'
    ).format(ex=esc(moat.get("execution")), pr=esc(moat.get("pricing")),
              comb=esc(moat.get("combined")), grade=esc(moat.get("grade")))
    rows_data = moat.get("spread_table") or []
    rows = []
    for r in rows_data:
        rows.append(
            "<tr><td>{drv}</td><td>{now}</td><td>{hist}</td><td>{spread}</td><td>{link}</td></tr>".format(
                drv=esc(r.get("driver")), now=esc(r.get("metric_now")),
                hist=esc(r.get("metric_hist_avg")), spread=esc(r.get("spread")),
                link=esc(r.get("moat_linkage")),
            )
        )
    header = "<tr><th>驅動因子</th><th>現值</th><th>歷史均值</th><th>價差</th><th>護城河連結</th></tr>"
    table = '<table id="e5">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"
    return summary + "\n" + table


# ---------------------------------------------------------------------------
# E6 -- §5.F 對手 P&L 對照 (moat.competitors[])
# ---------------------------------------------------------------------------

def render_e6_html(j: dict) -> str:
    rows_data = (j.get("moat") or {}).get("competitors") or []
    rows = []
    for r in rows_data:
        rows.append(
            "<tr><td>{name}</td><td>{rg}</td><td>{gm}</td><td>{om}</td><td>{rd}</td>"
            "<td>{fcf}</td><td>{nc}</td><td>{note}</td></tr>".format(
                name=esc(r.get("name")), rg=esc(r.get("rev_growth")), gm=esc(r.get("gm")),
                om=esc(r.get("om")), rd=esc(r.get("rd_intensity")), fcf=esc(r.get("fcf_margin")),
                nc=esc(r.get("net_cash")), note=esc(r.get("strategy_note")),
            )
        )
    header = (
        "<tr><th>對手</th><th>營收成長</th><th>毛利率</th><th>營業利益率</th>"
        "<th>研發密度</th><th>FCF利潤率</th><th>淨現金</th><th>策略備註</th></tr>"
    )
    return '<table id="e6">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---------------------------------------------------------------------------
# E7 -- §5.R 四檢查點 (moat.roic_durability.checkpoints[] + 摘要列)
# ---------------------------------------------------------------------------

def render_e7_html(j: dict) -> str:
    rd = (j.get("moat") or {}).get("roic_durability") or {}
    rows_data = rd.get("checkpoints") or []
    rows = []
    for r in rows_data:
        rows.append(
            "<tr><td>{n}</td><td>{q}</td><td>{status}</td><td>{ev}</td></tr>".format(
                n=esc(r.get("n")), q=esc(r.get("question")), status=esc(r.get("status")),
                ev=esc(r.get("evidence")),
            )
        )
    header = "<tr><th>#</th><th>檢查點</th><th>狀態</th><th>證據</th></tr>"
    summary = (
        '<tr><td colspan="4">象限：{quad}｜ROIIC：{roiic}｜再投資率：{ri}｜'
        "內生成長天花板：{ceil}（{note}）</td></tr>"
    ).format(quad=esc(rd.get("quadrant")), roiic=esc(rd.get("roiic")),
              ri=esc(rd.get("reinvest_rate")), ceil=esc(rd.get("endo_ceiling")),
              note=esc(rd.get("formula_note")))
    return '<table id="e7">\n' + header + "\n" + "\n".join(rows) + "\n" + summary + "\n</table>\n"


# ---------------------------------------------------------------------------
# E8 -- §6.I 分部前瞻 build (growth.segments[])
# ---------------------------------------------------------------------------

def render_e8_html(j: dict) -> str:
    rows_data = (j.get("growth") or {}).get("segments") or []
    rows = []
    for r in rows_data:
        rows.append(
            "<tr><td>{seg}</td><td>{fy0}</td><td>{fy1}</td><td>{fy2}</td>"
            "<td>{om0}→{om1}→{om2}</td><td>{eps}</td></tr>".format(
                seg=esc(r.get("segment")), fy0=esc(r.get("fy0_rev")), fy1=esc(r.get("fy1e_rev")),
                fy2=esc(r.get("fy2e_rev")), om0=esc(r.get("om_fy0")), om1=esc(r.get("om_fy1e")),
                om2=esc(r.get("om_fy2e")), eps=esc(r.get("eps_contribution_pct")),
            )
        )
    header = (
        "<tr><th>段</th><th>FY0營收</th><th>FY+1E</th><th>FY+2E</th>"
        "<th>OM軌跡(FY0→FY+2E)</th><th>對EPS貢獻%</th></tr>"
    )
    return '<table id="e8">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---------------------------------------------------------------------------
# E9 -- §7.E DuPont + CCC 合一 (quality.dupont[] + quality.ccc[], joined by
# `year`)
# ---------------------------------------------------------------------------

def render_e9_html(j: dict) -> str:
    quality = j.get("quality") or {}
    dupont = {r.get("year"): r for r in (quality.get("dupont") or []) if isinstance(r, dict)}
    ccc = {r.get("year"): r for r in (quality.get("ccc") or []) if isinstance(r, dict)}
    years = sorted({y for y in list(dupont.keys()) + list(ccc.keys()) if y is not None},
                   key=lambda y: str(y))
    rows = []
    for y in years:
        d = dupont.get(y, {})
        c = ccc.get(y, {})
        rows.append(
            "<tr><td>{y}</td><td>{nm}</td><td>{at}</td><td>{lev}</td><td>{roe}</td>"
            "<td>{dso}</td><td>{dio}</td><td>{dpo}</td><td>{ccc}</td></tr>".format(
                y=esc(y), nm=esc(d.get("net_margin")), at=esc(d.get("asset_turnover")),
                lev=esc(d.get("leverage")), roe=esc(d.get("roe")), dso=esc(c.get("dso")),
                dio=esc(c.get("dio")), dpo=esc(c.get("dpo")), ccc=esc(c.get("ccc")),
            )
        )
    header = (
        "<tr><th>年度</th><th>淨利率</th><th>資產週轉</th><th>槓桿</th><th>ROE</th>"
        "<th>DSO</th><th>DIO</th><th>DPO</th><th>CCC</th></tr>"
    )
    return '<table id="e9">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---------------------------------------------------------------------------
# E10 -- §9.D 資本配置 track (governance.capital_returns[] 逐年表 +
# governance.scorecard[] 附列)
# ---------------------------------------------------------------------------

def render_e10_html(j: dict) -> str:
    gov = j.get("governance") or {}
    rows_data = gov.get("capital_returns") or []
    rows = []
    for r in rows_data:
        rows.append(
            "<tr><td>{y}</td><td>{bb}</td><td>{div}</td><td>{capex}</td><td>{rd}</td></tr>".format(
                y=esc(r.get("year")), bb=esc(r.get("buyback")), div=esc(r.get("dividend")),
                capex=esc(r.get("capex")), rd=esc(r.get("rd")),
            )
        )
    header = "<tr><th>年度</th><th>回購</th><th>股利</th><th>資本支出</th><th>研發</th></tr>"
    table = '<table id="e10">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"
    score_rows = gov.get("scorecard") or []
    if score_rows:
        items = "".join(
            "<li>{y}：{action}（{grade}）{rationale}</li>".format(
                y=esc(r.get("year")), action=esc(r.get("action")), grade=esc(r.get("grade")),
                rationale=(("—" + esc(r.get("rationale"))) if r.get("rationale") else ""),
            )
            for r in score_rows
        )
        table += f"<ul class=\"e10-scorecard\">{items}</ul>\n"
    return table


# ---------------------------------------------------------------------------
# dashboard.html -- status-bar + hypothesis-box (best-effort; not a byte-for-
# byte target of the WP1c round-trip test, which only diffs dd-meta / e12)
# ---------------------------------------------------------------------------

def _fmt_signed_pct(x):
    return "" if x is None else f"{x:+.1f}%"


def render_dashboard_html(j: dict, scenario_meta: dict | None) -> str:
    meta_top = j.get("meta") or {}
    di = j.get("decision_inputs") or {}
    dout = j.get("decision_out") or {}
    moat = j.get("moat") or {}
    growth = j.get("growth") or {}
    prem = j.get("premortem") or {}
    gov = j.get("governance") or {}
    thesis = j.get("thesis") or {}
    ticker = meta_top.get("ticker") or ""
    company = meta_top.get("company_name") or ticker
    date = meta_top.get("date") or ""
    price = di.get("price_at_dd")
    max_dd = prem.get("max_dd") or {}
    ev5y = di.get("ev5y_pct")
    irr = di.get("irr_base_pct")
    headline = thesis.get("headline") or j.get("oneliner") or ""

    lines = []
    lines.append(
        f'<div class="topbar">{esc(ticker)} ｜ {esc(company)} ｜ 資料時間 {esc(date)} ｜ '
        f'最新股價 ${esc(price)} ｜ DD Schema {esc(meta_top.get("schema"))}</div>'
    )
    lines.append('<div class="wrap">')
    lines.append(f"<h1>{esc(company)}（{esc(ticker)}）深度研究與統一裁決</h1>")
    lines.append('<div class="status-bar">')
    lines.append(f'<div class="sb-cell"><span class="lab">統一裁決</span><span class="val">{esc(dout.get("verdict"))}</span></div>')
    lines.append(f'<div class="sb-cell"><span class="lab">護城河趨勢</span><span class="val">{esc(moat.get("grade"))} {esc(moat.get("trend"))}</span></div>')
    lines.append(f'<div class="sb-cell"><span class="lab">Y5後跑道</span><span class="val">{esc(growth.get("runway_post_y5"))}</span></div>')
    lines.append(f'<div class="sb-cell"><span class="lab">Max DD</span><span class="val">{esc(max_dd.get("lo"))}%~{esc(max_dd.get("hi"))}%</span></div>')
    lines.append(f'<div class="sb-cell"><span class="lab">5Y EV／IRR</span><span class="val">{_fmt_signed_pct(ev5y)}／Base {_fmt_signed_pct(irr)}/yr</span></div>')
    lines.append("</div>")
    lines.append(f'<p class="thesis">{esc(headline)}</p>')
    lines.append('<div class="hypothesis-box">')
    lines.append("<ul>")
    lines.append(f'<li><strong>統一裁決 <span style="font-size:22px">{esc(dout.get("verdict"))}</span></strong>（§13）｜倉位角色：{esc(dout.get("role"))}</li>')
    lines.append(f'<li><strong>護城河趨勢 {esc(moat.get("grade"))} {esc(moat.get("trend"))}</strong>（§5權威）｜{esc(moat.get("trend_evidence"))}</li>')
    lines.append(f'<li><strong>Y5後跑道 {esc(growth.get("runway_post_y5"))}</strong>（§6.A\'\'）</li>')
    lines.append(f'<li><strong>Max DD {esc(max_dd.get("lo"))}%~{esc(max_dd.get("hi"))}%</strong>（§12c範圍，路徑風險{esc(max_dd.get("path_risk"))}）</li>')
    lines.append(f'<li><strong>5Y機率加權 EV {_fmt_signed_pct(ev5y)}／年化IRR</strong>（§10.5）｜Base案不含息IRR {_fmt_signed_pct(irr)}/yr</li>')
    lines.append(f'<li><strong>長期持有信心：{esc((j.get("appendix_a") or {}).get("long_term_confidence"))}</strong>（附錄A）｜資本配置等級：{esc(gov.get("capalloc_grade"))}</li>')
    lines.append("</ul>")
    lines.append("</div>")
    lines.append(f'<p class="note"><strong>讀法：</strong>本份報告的人面對結論是「統一裁決 {esc(dout.get("verdict"))}」（§13）。倉位組合佔比由 portfolio-manager skill 依組合狀態決定。</p>')
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("judgment", help="judgment.json 路徑")
    ap.add_argument("--out", required=True, help="輸出目錄")
    ap.add_argument("--scenario-html", help="dd_scenario.py --html 產物；若給，逐字複製到 DIR/e11.html")
    ap.add_argument("--scenario-meta", help="dd_scenario.py --meta 產物；覆蓋 judgment.json 的 scenario_ref 解析")
    args = ap.parse_args()

    jpath = Path(args.judgment)
    j = load_json(jpath)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    scenario_meta = resolve_scenario_meta(j, jpath, Path(args.scenario_meta) if args.scenario_meta else None)

    meta = build_dd_meta(j, scenario_meta)
    (out_dir / "dd-meta.html").write_text(render_dd_meta_html(meta), encoding="utf-8")
    (out_dir / "e2.html").write_text(render_e2_html(j), encoding="utf-8")
    (out_dir / "e12.html").write_text(render_e12_html(j), encoding="utf-8")
    (out_dir / "appA-table.html").write_text(render_appA_table_html(j), encoding="utf-8")
    (out_dir / "dashboard.html").write_text(render_dashboard_html(j, scenario_meta), encoding="utf-8")

    # WP1c 修法1（七表由判斷物生成）
    (out_dir / "e3.html").write_text(render_e3_html(j), encoding="utf-8")
    (out_dir / "e5.html").write_text(render_e5_html(j), encoding="utf-8")
    (out_dir / "e6.html").write_text(render_e6_html(j), encoding="utf-8")
    (out_dir / "e7.html").write_text(render_e7_html(j), encoding="utf-8")
    (out_dir / "e8.html").write_text(render_e8_html(j), encoding="utf-8")
    (out_dir / "e9.html").write_text(render_e9_html(j), encoding="utf-8")
    (out_dir / "e10.html").write_text(render_e10_html(j), encoding="utf-8")

    audit_html = render_audit_html(j)
    if audit_html:
        (out_dir / "audit.html").write_text(audit_html, encoding="utf-8")

    if args.scenario_html:
        src = Path(args.scenario_html)
        if src.exists():
            (out_dir / "e11.html").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"寫入 {out_dir}: dd-meta.html, e2.html, e12.html, appA-table.html, dashboard.html, "
          "e3.html, e5.html, e6.html, e7.html, e8.html, e9.html, e10.html"
          + (", audit.html" if audit_html else "（無 audit_rows，略過 audit.html）"))


if __name__ == "__main__":
    main()
