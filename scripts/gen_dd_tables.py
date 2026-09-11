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
from dd_metric_resolver import resolve_max_dd_pct, resolve_scenario_metrics  # noqa: E402
# v19（WP-H1 2026-09-11）：判斷檔若帶 meta.contract="v19"，本檔的 dd-meta 與七表
# 一律讀 dd_project 投影出的舊形狀視圖；舊形狀 view_for() 是 identity，既有輸出
# 逐 byte 不變。
import dd_project  # noqa: E402

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
        meta = load_json(ref_path)
        # v17 per-run 目錄：scenario_ref 指向 dd_scenario.py 的輸入檔 scenario.json，
        # 六個結果欄在同目錄的 scenario_meta.json（或 {stem}.scenario_meta.json）——
        # 輸入檔缺 bull_5y_price 時改讀 meta 檔（AVGO 2026-09-05 真跑查出：漂移檢查誤判本次=None）。
        if isinstance(meta, dict) and meta.get("bull_5y_price") is None:
            for cand in (ref_path.parent / "scenario_meta.json",
                         ref_path.with_name(ref_path.name.replace(".scenario.json", ".scenario_meta.json"))):
                if cand != ref_path and cand.exists():
                    alt = load_json(cand)
                    if isinstance(alt, dict) and alt.get("bull_5y_price") is not None:
                        return alt
        return meta
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

    # v18（2026-09-10）：appendix_a 與權威欄同源的投影欄（signal／val／ma／
    # verdict／pct_5y／兩個 upside／moat_score）改為「有就用、沒有就從權威欄投
    # 影」——schema 已把這些 appendix_a 子欄降為選填（judgment-to-ddmeta.md 宣
    # 告的同源 pair 就是權威來源），舊檔兩側都有值時取值不變（同源檢查保證同
    # 值），故舊檔渲染結果完全不動。fpe_fy2／peg_fy2 不在此列：口徑待定義，
    # 沒有可投影的權威側（見 judgment-to-ddmeta.md 2026-09-07 附註）。
    def _aa(key, fallback):
        v = aa.get(key)
        return fallback if v is None else v

    meta = {
        "ticker": meta_top.get("ticker"),
        "schema": meta_top.get("schema"),
        "date": meta_top.get("date"),
        "price_at_dd": di.get("price_at_dd"),
        "signal": _aa("signal", di.get("signal")),
        "trap": trap.get("verdict"),
        "trap_label": trap.get("label"),
        "moat": moat.get("grade"),
        "val": _aa("val", di.get("val")),
        "ma": _aa("ma", di.get("ma")),
        "fpe_fy2": aa.get("fpe_fy2"),
        "pct_5y": _aa("pct_5y", val.get("percentile_5y")),
        "peg_fy2": aa.get("peg_fy2"),
        "upside_short_pct": _aa("upside_short_pct", val.get("upside_short_pct")),
        "upside_mid_pct": _aa("upside_mid_pct", val.get("upside_mid_pct")),
        "stress": aa.get("stress"),
        "moat_score": moat.get("score"),
        "growth_durability": aa.get("growth_durability"),
        "quality_score": aa.get("quality_score"),
        "ai_risk": aa.get("ai_risk"),
        "long_term_confidence": aa.get("long_term_confidence"),
        "verdict": _aa("verdict", _aa("signal", di.get("signal"))),
        "oneliner": j.get("oneliner"),
        "dca_verdict": dout.get("verdict"),
        "dca_role": dout.get("role"),
        "moat_trend": moat.get("trend"),
        "runway_post_y5": growth.get("runway_post_y5"),
    }

    # 2026-09-07：四個呈現入口共用同一 resolver；scenario 有值時是權威，
    # judgment 的歷史非 null 值只參與既有容差警告。
    meta.update(resolve_scenario_metrics(j, scenario_meta, source="gen_dd_tables"))
    meta["max_dd_pct"] = resolve_max_dd_pct(j)

    if scenario_meta:
        for k in ("bull_5y_price", "bear_5y_price", "p_bull_pct", "p_bear_pct",
                  "upside_5y_pct", "scenario_tree"):
            if scenario_meta.get(k) is not None:
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

# v18（2026-09-10）：appendix_a 的 signal／val／ma 已降為選填（與
# decision_inputs 同源，judgment-to-ddmeta.md 宣告）。呈現層跟 build_dd_meta
# 一樣「有就用、沒有才回退權威欄」，否則完整版附錄 A 會在新形狀下渲染成空格。
def _aa_or_di(j: dict, key: str):
    v = (j.get("appendix_a") or {}).get(key)
    if v is None:
        v = (j.get("decision_inputs") or {}).get(key)
    return v


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
            signal=esc(_aa_or_di(j, "signal")), moat_s=esc(moat.get("score")),
            growth_d=esc(aa.get("growth_durability")), quality_s=esc(aa.get("quality_score")),
            val=esc(_aa_or_di(j, "val")), ma=esc(_aa_or_di(j, "ma")),
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

def _unexpanded_table(table_id: str, block, header: str):
    """2026-09-10（B1–B4）：條件式展開區塊被標成 {"expanded": false, "reason": …}
    時，整張表改渲染成一行「未展開：理由」——欄數對齊原表頭，讀者看得到為什麼
    沒展開，不是靜靜消失。非未展開形狀回 None，呼叫端照原路走。"""
    if not (isinstance(block, dict) and block.get("expanded") is False):
        return None
    # v19（WP-H2-2）：七表表頭部分欄位改標 class="num"（<th class="num">…），
    # 原本的 exact-match "<th>" 計數會漏算這些欄，colspan 算少（已實測 E10
    # 未展開分支 5 欄算成 1 欄）——改用 "<th" 前綴計數，兩種寫法都算得到。
    ncol = header.count("<th")
    reason = esc(block.get("reason") or "（未附理由）")
    return ('<table id="{tid}">\n'.format(tid=table_id) + header + "\n"
            + '<tr><td colspan="{n}">未展開：{r}</td></tr>\n</table>\n'.format(n=ncol, r=reason))


# ---------------------------------------------------------------------------
# WP-G 修 #6b（2026-09-11，Codex 第三輪複審「B．陣列形狀修補仍未與表格渲染
# 契約對齊」項）：judgment-rules.md §0.5(二) 給的條件式展開陣列示例是
# `[{"item": "…", "value": "…"}]`，但 E3/E8/E10 各自要的是自己的專屬逐列形狀
# （E3 segment/tam_now/…、E8 segment/fy0_rev/…、E10 year/buyback/…）——判斷
# agent 照字面套用示例形狀時（TXN 2026-09-10 實例：governance.capital_returns
# 填成 7 筆 {item,value}），原本的專屬欄位 renderer 全部讀不到值，渲染出全空
# 表格而非「未展開」訊息，讀者看不出哪裡壞了。這裡加一個輕量偵測＋通用兩欄
# 渲染：第一列有 item/value 鍵、卻沒有該表自己的第一個專屬鍵，判定為退化成
# 示例形狀，改渲染兩欄「項目／內容」表，不強行對應五到七個專屬欄位。
# ---------------------------------------------------------------------------

def _is_item_value_shape(rows_data: list, primary_key: str) -> bool:
    if not rows_data:
        return False
    first = rows_data[0]
    return (
        isinstance(first, dict)
        and "item" in first and "value" in first
        and primary_key not in first
    )


def _render_item_value_table(table_id: str, rows_data: list) -> str:
    rows = [
        "<tr><td>{item}</td><td>{value}</td></tr>".format(
            item=esc(r.get("item")), value=esc(r.get("value"))
        )
        for r in rows_data if isinstance(r, dict)
    ]
    header = "<tr><th>項目</th><th>內容</th></tr>"
    return '<table id="{tid}">\n'.format(tid=table_id) + header + "\n" + "\n".join(rows) + "\n</table>\n"


def render_e3_html(j: dict) -> str:
    block = (j.get("industry") or {}).get("tam_table")
    rows_data = block if isinstance(block, list) else []
    rows = []
    for r in rows_data:
        rows.append(
            '<tr><td>{seg}</td><td class="num">{now}</td><td class="num">{y5}</td>'
            '<td class="num">{pen}</td><td class="num">{cagr}</td>'
            "<td>{vcp}</td><td>{pp}</td></tr>".format(
                seg=esc(r.get("segment")), now=esc(r.get("tam_now")), y5=esc(r.get("tam_5y")),
                pen=esc(r.get("penetration_pct")), cagr=esc(r.get("cagr_pct")),
                vcp=esc(r.get("value_chain_position")), pp=esc(r.get("profit_pool_shift")),
            )
        )
    # v19（WP-H2-2，2026-09-11）：七表數值欄改標 class="num"（新版面 CSS 靠
    # class 而非欄序套右對齊／等寬數字樣式），第一欄的名稱/標籤欄不加——沿用
    # dd_templates/v19.css 的 td.num 慣例。舊版面 dd_template/dd.css 沒有
    # `.num` 選擇器，這個 class 屬性對舊版面是無作用的多餘屬性（純新增，不影
    # 響既有視覺），故舊版面重跑只多這個屬性、其餘 bytes 不變。
    header = (
        '<tr><th>段</th><th class="num">TAM(現)</th><th class="num">TAM(5Y)</th>'
        '<th class="num">滲透率</th><th class="num">段CAGR</th>'
        "<th>Value Chain位置</th><th>利潤池占比遷移</th></tr>"
    )
    skipped = _unexpanded_table("e3", block, header)
    if skipped:
        return skipped
    if _is_item_value_shape(rows_data, "segment"):
        return _render_item_value_table("e3", rows_data)
    return '<table id="e3">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---------------------------------------------------------------------------
# E5 -- 二維評分 + Moat-to-Numbers 合一 (moat.{execution,pricing,combined,
# grade} 摘要 + moat.spread_table[])
# ---------------------------------------------------------------------------

# 舊窄形狀（v15/v18 判斷檔手填）的欄名指紋：一列一個驅動因子。
_E5_NARROW_KEYS = ("driver", "metric_now", "metric_hist_avg", "spread", "moat_linkage")


def _e5_narrow_rows(rows_data) -> str:
    rows = []
    for r in rows_data:
        rows.append(
            '<tr><td>{drv}</td><td class="num">{now}</td><td class="num">{hist}</td>'
            '<td class="num">{spread}</td><td>{link}</td></tr>'.format(
                drv=esc(r.get("driver")), now=esc(r.get("metric_now")),
                hist=esc(r.get("metric_hist_avg")), spread=esc(r.get("spread")),
                link=esc(r.get("moat_linkage")),
            )
        )
    header = ('<tr><th>驅動因子</th><th class="num">現值</th><th class="num">歷史均值</th>'
              '<th class="num">價差</th><th>護城河連結</th></tr>')
    return '<table id="e5">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


def _e5_matrix_from_facts(facts):
    """`facts.peer_comparison` → 同業矩陣（度量為列、公司為欄）。

    優先讀事實表而不是 `dd_project` 的 P-26 投影：事實表帶得到期間與單位，投影
    為了還原舊形狀會把它們攤平掉。回 `(欄名清單, 列 dict 清單)`；facts 沒有同業
    區塊回 None。"""
    pc = (facts or {}).get("peer_comparison") or {}
    metrics = [m for m in (pc.get("metrics") or []) if isinstance(m, dict) and m.get("key")]
    peers = [r for r in (pc.get("rows") or []) if isinstance(r, dict) and r.get("name")]
    if not metrics or not peers:
        return None
    cols = [r["name"] for r in peers]
    rows = []
    for m in metrics:
        label = m.get("label") or m["key"]
        if m.get("unit"):
            label = "{0}（{1}）".format(label, m["unit"])
        row = {"metric": label}
        periods = []
        for r in peers:
            val = (r.get("values") or {}).get(m["key"])
            row[r["name"]] = val
            if val is not None and r.get("period") and r["period"] not in periods:
                periods.append(r["period"])
        note = m.get("note") or ""
        if not note and len(periods) == 1:
            note = periods[0]
        row["note"] = note
        rows.append(row)
    return cols, rows


def _e5_matrix_from_rows(rows_data):
    """寬形狀 `moat.spread_table`（v19＝P-26 投影，或判斷者手填的寬表）→
    `(欄名清單, 列)`。欄＝除 metric／note／period／unit 以外的鍵，依首次出現序。"""
    cols = []
    for r in rows_data:
        if not isinstance(r, dict):
            continue
        for k in r:
            if k not in ("metric", "note", "period", "unit") and k not in cols:
                cols.append(k)
    if not cols:
        return None
    rows = []
    for r in rows_data:
        if not isinstance(r, dict):
            continue
        label = r.get("metric")
        if r.get("unit"):
            label = "{0}（{1}）".format(label, r["unit"])
        row = {"metric": label}
        for c in cols:
            row[c] = r.get(c)
        row["note"] = r.get("note") or r.get("period") or ""
        rows.append(row)
    return cols, rows


def _e5_matrix_html(cols, rows) -> str:
    header = ('<tr><th>指標</th>'
              + "".join('<th class="num">{0}</th>'.format(esc(c)) for c in cols)
              + "<th>備註</th></tr>")
    body = []
    for r in rows:
        cells = "".join(
            '<td class="num">{0}</td>'.format(esc(r[c]) if r.get(c) is not None else "—")
            for c in cols)
        body.append("<tr><td>{0}</td>{1}<td>{2}</td></tr>".format(
            esc(r.get("metric")), cells, esc(r.get("note")) or "—"))
    return '<table id="e5">\n' + header + "\n" + "\n".join(body) + "\n</table>\n"


def render_e5_html(j: dict, facts=None) -> str:
    """E5 護城河／同業對照表。

    2026-09-11（WP-H2-3）：改讀**同業矩陣形狀**（metric／各同業值／note），舊窄
    形狀（driver／metric_now／metric_hist_avg／spread／moat_linkage）原樣 fallback
    ——36 份舊格式判斷檔的輸出因此逐位元組不變。資料來源優先序：①`facts
    .peer_comparison`（期間與單位最完整）②`moat.spread_table`（v19 是 `dd_project`
    的 P-26 投影，舊形狀是判斷者手填）。

    H2-2 的 `render_v19_spread_html()` 平行函式由本函式接手（已撤），v19 版面的
    §5 標記直接指 `e5.html`——同一張表兩支 renderer 是漂移的溫床。"""
    moat = j.get("moat") or {}
    summary = (
        '<p class="e5-summary">執行力 {ex} ｜ 定價力 {pr} ｜ 綜合 {comb} ｜ 護城河評級 {grade}</p>'
    ).format(ex=esc(moat.get("execution")), pr=esc(moat.get("pricing")),
              comb=esc(moat.get("combined")), grade=esc(moat.get("grade")))
    rows_data = moat.get("spread_table") or []
    narrow = any(isinstance(r, dict) and any(k in r for k in _E5_NARROW_KEYS)
                 for r in rows_data)
    if narrow:
        return summary + "\n" + _e5_narrow_rows(rows_data)
    matrix = _e5_matrix_from_facts(facts) or _e5_matrix_from_rows(rows_data)
    table = _e5_matrix_html(*matrix) if matrix else _e5_narrow_rows(rows_data)
    return summary + "\n" + table


# ---------------------------------------------------------------------------
# E6 -- §5.F 對手 P&L 對照 (moat.competitors[])
# ---------------------------------------------------------------------------

def render_e6_html(j: dict) -> str:
    rows_data = (j.get("moat") or {}).get("competitors") or []
    rows = []
    for r in rows_data:
        rows.append(
            '<tr><td>{name}</td><td class="num">{rg}</td><td class="num">{gm}</td>'
            '<td class="num">{om}</td><td class="num">{rd}</td>'
            '<td class="num">{fcf}</td><td class="num">{nc}</td><td>{note}</td></tr>'.format(
                name=esc(r.get("name")), rg=esc(r.get("rev_growth")), gm=esc(r.get("gm")),
                om=esc(r.get("om")), rd=esc(r.get("rd_intensity")), fcf=esc(r.get("fcf_margin")),
                nc=esc(r.get("net_cash")), note=esc(r.get("strategy_note")),
            )
        )
    header = (
        '<tr><th>對手</th><th class="num">營收成長</th><th class="num">毛利率</th>'
        '<th class="num">營業利益率</th><th class="num">研發密度</th>'
        '<th class="num">FCF利潤率</th><th class="num">淨現金</th><th>策略備註</th></tr>'
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
            '<tr><td class="num">{n}</td><td>{q}</td><td>{status}</td><td>{ev}</td></tr>'.format(
                n=esc(r.get("n")), q=esc(r.get("question")), status=esc(r.get("status")),
                ev=esc(r.get("evidence")),
            )
        )
    header = '<tr><th class="num">#</th><th>檢查點</th><th>狀態</th><th>證據</th></tr>'
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
    block = (j.get("growth") or {}).get("segments")
    rows_data = block if isinstance(block, list) else []
    rows = []
    for r in rows_data:
        rows.append(
            '<tr><td>{seg}</td><td class="num">{fy0}</td><td class="num">{fy1}</td>'
            '<td class="num">{fy2}</td>'
            '<td>{om0}→{om1}→{om2}</td><td class="num">{eps}</td></tr>'.format(
                seg=esc(r.get("segment")), fy0=esc(r.get("fy0_rev")), fy1=esc(r.get("fy1e_rev")),
                fy2=esc(r.get("fy2e_rev")), om0=esc(r.get("om_fy0")), om1=esc(r.get("om_fy1e")),
                om2=esc(r.get("om_fy2e")), eps=esc(r.get("eps_contribution_pct")),
            )
        )
    header = (
        '<tr><th>段</th><th class="num">FY0營收</th><th class="num">FY+1E</th>'
        '<th class="num">FY+2E</th>'
        '<th>OM軌跡(FY0→FY+2E)</th><th class="num">對EPS貢獻%</th></tr>'
    )
    skipped = _unexpanded_table("e8", block, header)
    if skipped:
        return skipped
    if _is_item_value_shape(rows_data, "segment"):
        return _render_item_value_table("e8", rows_data)
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
            '<tr><td>{y}</td><td class="num">{nm}</td><td class="num">{at}</td>'
            '<td class="num">{lev}</td><td class="num">{roe}</td>'
            '<td class="num">{dso}</td><td class="num">{dio}</td><td class="num">{dpo}</td>'
            '<td class="num">{ccc}</td></tr>'.format(
                y=esc(y), nm=esc(d.get("net_margin")), at=esc(d.get("asset_turnover")),
                lev=esc(d.get("leverage")), roe=esc(d.get("roe")), dso=esc(c.get("dso")),
                dio=esc(c.get("dio")), dpo=esc(c.get("dpo")), ccc=esc(c.get("ccc")),
            )
        )
    header = (
        '<tr><th>年度</th><th class="num">淨利率</th><th class="num">資產週轉</th>'
        '<th class="num">槓桿</th><th class="num">ROE</th>'
        '<th class="num">DSO</th><th class="num">DIO</th><th class="num">DPO</th>'
        '<th class="num">CCC</th></tr>'
    )
    return '<table id="e9">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---------------------------------------------------------------------------
# E10 -- §9.D 資本配置 track (governance.capital_returns[] 逐年表 +
# governance.scorecard[] 附列)
# ---------------------------------------------------------------------------

def render_e10_html(j: dict) -> str:
    gov = j.get("governance") or {}
    block = gov.get("capital_returns")
    rows_data = block if isinstance(block, list) else []
    rows = []
    for r in rows_data:
        rows.append(
            '<tr><td>{y}</td><td class="num">{bb}</td><td class="num">{div}</td>'
            '<td class="num">{capex}</td><td class="num">{rd}</td></tr>'.format(
                y=esc(r.get("year")), bb=esc(r.get("buyback")), div=esc(r.get("dividend")),
                capex=esc(r.get("capex")), rd=esc(r.get("rd")),
            )
        )
    header = ('<tr><th>年度</th><th class="num">回購</th><th class="num">股利</th>'
              '<th class="num">資本支出</th><th class="num">研發</th></tr>')
    skipped = _unexpanded_table("e10", block, header)
    if skipped:
        table = skipped
    elif _is_item_value_shape(rows_data, "year"):
        table = _render_item_value_table("e10", rows_data)
    else:
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
    # 2026-09-07：完整版頁首不得繞過 scenario 衍生欄的共用權威解析。
    scenario_metrics = resolve_scenario_metrics(j, scenario_meta, source="dashboard")
    ev5y = scenario_metrics.get("ev5y_pct")
    irr = scenario_metrics.get("irr_base_pct")
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
# v17 WP4b C-1（2026-09-06）：revlog / s14（複審表）/ appA 敘述 三個機械段
# ——全部是 judgment（+ evidence.prior_dd）欄位的復述，散文 agent 不再撰寫，
# 省一輪散文輸出與一輪 validate_prose 覆蓋檢查。刻意只用「原樣或逐字複製」
# 的欄位值，不做任何算術（如價格漲跌幅），避免 validate_prose.py 把衍生出
# 的新數字判定為「判斷物沒有」而 FAIL——見
# notes/site-internal/dd/_dd_pipeline_redesign_spec_20260905.md §8 C-1。
# ---------------------------------------------------------------------------

_VAL_DESC = {
    "🔴": "落在最嚴一檔",
    "🟠": "落在偏貴區間",
    "🟡": "落在觀察區間",
    "🟢": "落在便宜區間",
}
_ROLE_OTHER = {"核心": "衛星", "衛星": "核心", "追蹤": "核心", "不持有": "核心"}
_TRAP_EMOJI_RE = re.compile(r"^[🟢🟡🔴]\s*")


def _val_desc(val) -> str:
    if not val:
        return "未標示"
    return _VAL_DESC.get(val, "訊號{0}".format(val))


def _ma_desc(ma) -> str:
    return "符合多頭排列" if ma == "✅" else "未通過週線結構檢核"


def render_appA_section_html(j: dict) -> str:
    """appA 完整 `<details>` 外層（intro 段固定文案 + `<!-- APPA_TABLE -->`
    標記 + 機械收尾段），取代散文 agent 手寫此段——收尾段句型固定為 BE
    2026-09-05 那份（四份樣本中最單純機械的寫法），內容依 judgment 逐檔
    代換。"""
    aa = j.get("appendix_a") or {}
    moat = j.get("moat") or {}
    trap = j.get("trap_analysis") or {}
    gov = j.get("governance") or {}
    dout = j.get("decision_out") or {}
    stress = aa.get("stress") or {}
    role = dout.get("role") or "衛星"
    other_role = _ROLE_OTHER.get(role, "核心")
    pass_n, total_n = stress.get("pass"), stress.get("total")
    if pass_n is not None and total_n is not None and pass_n == total_n:
        stress_desc = "兩項壓力測試皆通過"
    else:
        stress_desc = "{0}/{1} 項壓力測試通過".format(esc(pass_n), esc(total_n))
    trap_label = _TRAP_EMOJI_RE.sub("", trap.get("label") or "")
    intro = (
        "本表把品質、護城河、成長三項分數與估值分色、週線結構、陷阱定性、壓力測試結果"
        "收攏成單一機械輸出的評級卡，供跨檔比較與下游列表讀取——正文統一裁決以第 13 節"
        "為準，本表只作評級留存用。"
    )
    closing = (
        "本檔綜合訊號為 {signal}（護城河 {moat_score}、成長耐久度 {growth_d}、財務品質 "
        "{quality_s}），估值分色{val_desc}、週線結構{ma_desc}、陷阱定性為{trap_label}、"
        "{stress_desc}，長期持有信心因資本配置等級 {capalloc} 定在「{ltc}」——這是本檔"
        "角色被限定在{role}而非{other_role}的機械依據。"
    ).format(
        signal=esc(_aa_or_di(j, "signal")), moat_score=esc(moat.get("score")),
        growth_d=esc(aa.get("growth_durability")), quality_s=esc(aa.get("quality_score")),
        val_desc=_val_desc(_aa_or_di(j, "val")), ma_desc=_ma_desc(_aa_or_di(j, "ma")),
        trap_label=esc(trap_label) or "—", stress_desc=stress_desc,
        capalloc=esc(gov.get("capalloc_grade")), ltc=esc(aa.get("long_term_confidence")),
        role=esc(role), other_role=other_role,
    )
    return (
        '<details id="appA">\n'
        "<summary>附錄 A．基本面評級（機械推導）</summary>\n"
        "<p>{intro}</p>\n"
        "<!-- APPA_TABLE -->\n"
        "<p>{closing}</p>\n"
        "</details>\n"
    ).format(intro=intro, closing=closing)


def render_e12_note_html(j: dict) -> str:
    """C-1「E12 觸發器說明段」：decision 段仍由散文 agent 撰寫，唯獨這一句
    機械附加在 `<!-- E12 -->` 標記之後（由 `ddreport.py prose split` 接線，
    不動 `render_e12_html` 本身——`dd_brief.py` 快速版也呼叫
    `render_e12_html`，改它會連帶動到快速版語意，故另立此函式）。"""
    triggers = j.get("triggers") or []
    dout = j.get("decision_out") or {}
    rearm = dout.get("rearm_trigger")
    n = len(triggers)
    # validate_prose 只無條件容忍 |value|<=12 的小整數；觸發器件數超過 12 時
    # 不保證這個數字能在 judgment.json 別處找到對帳，故只在 <=12 時才印出，
    # 避免這句機械附加句自己觸發覆蓋檢查 FAIL。
    text = (
        "完整的假設驗證、風險與觸發器門檻共 {0} 項見上表。".format(n)
        if (n and n <= 12) else "完整的假設驗證、風險與觸發器門檻見上表。"
    )
    if rearm:
        text += "重啟條件：{0}。".format(esc(rearm))
    return "<p>{0}</p>\n".format(text)


def _revlog_note_bits(val, asym, ev5y) -> str:
    bits = []
    if val:
        bits.append("估值分色 {0}".format(val))
    if asym is not None:
        bits.append("不對稱比率 {0}".format(asym))
    if ev5y is not None:
        try:
            v = float(ev5y)
            bits.append("5 年機率加權報酬 {0}{1:.1f}%".format("+" if v > 0 else ("−" if v < 0 else ""), abs(v)))
        except (TypeError, ValueError):
            bits.append("5 年機率加權報酬 {0}".format(ev5y))
    return "、".join(bits)


def _revlog_row(date, price, verdict, role, note) -> str:
    return (
        "<tr><td>{date}</td><td>${price}</td><td>{verdict}</td><td>{role}</td><td>{note}</td></tr>"
    ).format(date=esc(date), price=esc(price), verdict=esc(verdict), role=esc(role), note=esc(note))


def render_revlog_html(j: dict, prior: dict | None = None,
                       scenario_meta: dict | None = None) -> str:
    """revlog 完整 `<section>`——沿用 BE 2026-09-05 的最簡表格寫法（日期／
    股價／裁決／角色／備註）。`prior` 為 evidence.json 的 `prior_dd` 子物件
    （`{"status":"ok","prior_meta":{...}}` 或 `{"status":"unavailable"}`）；
    刻意不算價格漲跌幅這類衍生數字（見上方模組註解），只逐字複製既有欄位。"""
    meta = j.get("meta") or {}
    di = j.get("decision_inputs") or {}
    dout = j.get("decision_out") or {}
    aa = j.get("appendix_a") or {}
    rows = []
    prior_meta = (prior or {}).get("prior_meta") if isinstance(prior, dict) else None
    if isinstance(prior, dict) and prior.get("status") == "ok" and prior_meta:
        rows.append(_revlog_row(
            prior_meta.get("date"), prior_meta.get("price_at_dd"),
            prior_meta.get("dca_verdict") or prior_meta.get("verdict"),
            prior_meta.get("dca_role"),
            _revlog_note_bits(prior_meta.get("val"), prior_meta.get("asym_ratio"), prior_meta.get("ev5y_pct")),
        ))
    # 2026-09-07：當期 revlog 與 dashboard／dd-meta／brief 使用同一組值。
    scenario_metrics = resolve_scenario_metrics(j, scenario_meta, source="revlog")
    rows.append(_revlog_row(
        meta.get("date"), di.get("price_at_dd"), dout.get("verdict"), dout.get("role"),
        _revlog_note_bits(
            aa.get("val") or di.get("val"),
            scenario_metrics.get("asym_ratio"), scenario_metrics.get("ev5y_pct"),
        ),
    ))
    header = "<tr><th>日期</th><th>股價</th><th>裁決</th><th>角色</th><th>備註</th></tr>"
    return (
        '<section id="revlog">\n<h2>版本紀錄</h2>\n<table>\n{header}\n{rows}\n</table>\n</section>\n'
    ).format(header=header, rows="\n".join(rows))


def render_s14_html(j: dict) -> str:
    """s14（複審表）：把 catalysts[] 逐字轉成一張表（日期/事件/類型/影響/
    觀察重點），取代散文 agent 手寫的保質期敘事——事件與觀察重點文字本身
    就是 judgment.catalysts[] 的原樣子字串，逐字複製不生新數字。"""
    cats = sorted(j.get("catalysts") or [], key=lambda c: c.get("date") or "9999-99-99")
    prem = j.get("premortem") or {}
    max_dd = prem.get("max_dd") or {}
    lead_bits = []
    if cats:
        nxt = cats[0]
        lead_bits.append("下一個排定複審點：{0}　{1}".format(esc(nxt.get("date")), esc(nxt.get("event"))))
    if max_dd.get("lo") is not None or max_dd.get("hi") is not None:
        lead_bits.append("最大回撤路徑落在 {0}%~{1}%".format(esc(max_dd.get("lo")), esc(max_dd.get("hi"))))
    parts = ['<section id="s14">', "<h2>14．保質期與複審</h2>"]
    if lead_bits:
        parts.append("<p>{0}。任一項提前發生即應重新評估，不需要等到下一個排定複審日。</p>".format("；".join(lead_bits)))
    if cats:
        rows = [
            "<tr><td>{date}</td><td>{event}</td><td>{type_}</td><td>{impact}</td><td>{watch}</td></tr>".format(
                date=esc(c.get("date")), event=esc(c.get("event")), type_=esc(c.get("type")),
                impact=esc(c.get("impact")), watch=esc(c.get("watch")),
            )
            for c in cats
        ]
        header = "<tr><th>日期</th><th>事件</th><th>類型</th><th>影響</th><th>觀察重點</th></tr>"
        parts.append("<table>\n{0}\n{1}\n</table>".format(header, "\n".join(rows)))
    parts.append("</section>")
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# v19（WP-H2-2，2026-09-11）：新版面頁首（meta 行/h1/摘要/五張卡/24 格篩選器
# 資料列/改變主意三條）與 s7/s8/s10/decision 的免費資料折疊區、v19 專用附錄
# A/B/C 與 revlog 片段。規格：notes/site-internal/dd/_v19_layout_spec_20260911.md。
#
# 零 LLM：只讀 build_dd_meta() 已投影好的 dd-meta 欄位（`meta`）、投影視圖
# （`j` = dd_project.view_for() 的輸出）、facts.json、scenario_meta.json——
# 不新增判斷、不外推判斷檔沒有的新數字。唯一允許的算術是「已 sourced 的兩個
# 數字相乘/相減」（例：一年/兩年合理價＝price_at_dd×(1+upside_pct/100)），
# 一律標「由 X% 推算」。只在 `dd_project.is_v19(raw)` 為真時由 main() 呼叫；
# 舊形狀報告完全不受影響（見下方 main() 的 if 分支）。
#
# 這些函式輸出的 HTML 片段（v19-*.html）由 render_dd.py 的
# `assemble_from_parts_v19()` 讀取並注入 v19.html 模板；canonical id
# （s1..s14/decision/appA/appB/appC/revlog）與舊版面共用，dd_sections.py 既有
# 的 bytes/leaks 掃描機制不需改動即可涵蓋。
# ---------------------------------------------------------------------------

_DOT_HEX_V19 = {
    "🟢": "#16A34A", "🟡": "#D97706", "🟠": "#EA580C", "🔴": "#DC2626", "⚪": "#94A3B8",
}
_DOT_COLOR_NAME_V19 = {"🟢": "綠", "🟡": "黃", "🟠": "橙", "🔴": "紅", "⚪": "灰"}
_RISK_LEVEL_LABEL_V19 = {"🟢": "低", "🟡": "中", "🟠": "中高", "🔴": "高"}
_RUNWAY_LABEL_V19 = {"🟢": "結構性", "🟡": "待驗證", "🟠": "轉弱", "🔴": "消退中"}
_MOAT_TREND_LABEL_V19 = {"↑": "上升", "→": "持平", "↓": "下降"}
_CLOCK_PHASE_LABEL_V19 = {"I": "第一階段", "II": "第二階段", "III": "第三階段", "IV": "第四階段"}
_SIGNAL_PLAIN_V19 = {"進場": "進場時機", "觀望": "時機不到", "迴避": "避開"}
_EXEC_SHORT_V19 = {"進場": "現價分批", "觀望": "等重啟門檻", "迴避": "不參與"}
_IRR_NOTE_V19 = {"進場": "過門檻，不用等回檔", "觀望": "不到門檻，等價格", "迴避": "不到門檻"}
_DIRECTION_DOT_V19 = {"+": "🟢", "-": "🔴", "0": "⚪"}
_DIRECTION_LABEL_V19 = {"+": "正", "-": "負", "0": "中"}
_FY_KEY_RE_V19 = re.compile(r"FY\s*(\d{4})")


def _dot(emoji: str, fallback: str = "#94A3B8") -> str:
    hexv = _DOT_HEX_V19.get(emoji, fallback) if emoji else fallback
    return f'<span class="dot" style="background:{hexv}"></span>'


def _strip_paren(text) -> str:
    if not text:
        return ""
    return re.split(r"[（(]", str(text), 1)[0].strip()


def _v19_pct(v, nd: int = 1) -> str:
    if v is None:
        return "—"
    try:
        f = float(v)
    except (TypeError, ValueError):
        return esc(v)
    sign = "+" if f > 0 else ("−" if f < 0 else "")
    return f"{sign}{abs(f):.{nd}f}%"


def _v19_usd(v) -> str:
    if v is None:
        return "—"
    try:
        return "${0:,.0f}".format(float(v))
    except (TypeError, ValueError):
        return esc(v)


def _v19_usd2(v) -> str:
    """同 `_v19_usd` 但保留 2 位小數——僅用於「現價」本身（判斷日收盤價，
    dd-meta.price_at_dd 原樣數字），推算出的目標價一律用整數。"""
    if v is None:
        return "—"
    try:
        return "${0:,.2f}".format(float(v))
    except (TypeError, ValueError):
        return esc(v)


def _v19_derive_target(price_at_dd, pct):
    """price_at_dd × (1+pct/100)——兩個已 sourced 的 dd-meta 數字的算術，不是
    新判斷；呼叫端必須在旁標「由 X% 推算」。"""
    if price_at_dd is None or pct is None:
        return None
    try:
        return round(float(price_at_dd) * (1 + float(pct) / 100.0))
    except (TypeError, ValueError):
        return None


def _pct5y_tier_label(pct) -> str:
    if pct is None:
        return ""
    try:
        v = float(pct)
    except (TypeError, ValueError):
        return ""
    if v >= 85:
        return "貴"
    if v >= 50:
        return "合理偏貴"
    if v >= 15:
        return "合理"
    return "便宜"


def _fy2_label(meta: dict) -> str:
    """由 eps_meta.base_eps_path（dd-meta 已投影為 base_eps_path）的財年鍵反推
    第二個前瞻財年標籤（跳過含 A 後綴的已實現年）；沒有可用鍵時回退通用
    「FY2」，不臆造年份。"""
    path = meta.get("base_eps_path") or {}
    years = sorted(
        (int(m.group(1)), k) for k, m in
        ((k, _FY_KEY_RE_V19.search(k)) for k in path if isinstance(k, str)) if m
    )
    forward = [k for _y, k in years if not k.endswith("A")]
    return forward[1] if len(forward) >= 2 else "FY2"


def _fact_by_id(facts: dict | None, fid: str):
    for q in ((facts or {}).get("questions") or {}).values():
        for f in (q or {}).get("facts") or []:
            if isinstance(f, dict) and f.get("id") == fid:
                return f
    return None


def _price_as_of(facts: dict | None) -> str:
    f = _fact_by_id(facts, "f_price_at_dd")
    if not f:
        return ""
    period = f.get("period") or ""
    return period.split("（")[0].strip() if period else ""


# ---- 頁首：meta 行／h1／摘要 --------------------------------------------

def _split_bullets(text: str, max_items: int = 3) -> list:
    """持有人 2026-09-11 拍板：能條列就條列，文字不得擠成一段——頁首摘要段
    改 2-3 條條列，不用段落。oneliner 是判斷檔既有單一字串，機械層沒有 LLM
    可重寫，只能用既有的分句標點（；/;／。！？）當斷點原樣切開，不新增、不
    改寫任何字；切不出多段就回傳單一條（不硬湊）。超過 max_items 時，多出
    的片段用「，」併入最後一條（不是用「；」再串——那正是這條規則要拆掉的
    寫法），避免內容遺失又不違反規則字面。"""
    if not text:
        return []
    parts = [p.strip() for p in re.split(r"[；;]", text) if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in re.split(r"(?<=[。！？])", text) if p.strip()]
    if len(parts) > max_items:
        parts = parts[:max_items - 1] + ["，".join(parts[max_items - 1:])]
    return parts or [text]


def render_v19_header_top_html(j: dict, meta: dict, facts: dict | None) -> str:
    meta_top = j.get("meta") or {}
    ticker = meta_top.get("ticker") or meta.get("ticker") or ""
    company = meta_top.get("company_name") or ticker
    date = meta.get("date") or meta_top.get("date") or ""
    price = meta.get("price_at_dd")
    price_as_of = _price_as_of(facts)
    headline = (j.get("thesis") or {}).get("headline") or meta.get("oneliner") or j.get("oneliner") or ""
    summary = meta.get("oneliner") or j.get("oneliner") or ""
    date_price = f"{esc(date)}　・　收盤 {_v19_usd2(price)}"
    if price_as_of:
        date_price += f"（{esc(price_as_of)}）"
    meta_line = f"個股深度研究　・　{esc(ticker)}　{esc(company)}"
    summary_items = _split_bullets(summary, max_items=3)
    summary_html = (
        '<ul class="pts" style="margin:0;font-size:16px;color:#334155">'
        + "".join(f"<li>{esc(it)}</li>" for it in summary_items) + "</ul>"
    )
    return (
        '<div style="display:flex;flex-direction:row;justify-content:space-between;'
        'align-items:baseline;gap:16px;font-size:13px;color:#64748B">'
        f'<div>{meta_line}</div><div>{date_price}</div></div>\n'
        '<h1 style="font-size:30px;line-height:1.35;margin:0;font-weight:700;'
        f'letter-spacing:0.005em">{esc(headline)}</h1>\n'
        f'{summary_html}'
    )


# ---- 頁首：五張卡 ----------------------------------------------------------

def _v19_card(label: str, value_html: str, sub_html: str, dark: bool = False) -> str:
    bg = "#1E3A5F" if dark else "#FFFFFF"
    color = "#FFFFFF" if dark else "#1E3A5F"
    border = "" if dark else "border:1px solid #E2E8F0;"
    lab_color = "rgba(255,255,255,.75)" if dark else "#64748B"
    sub_color = "rgba(255,255,255,.85)" if dark else "#64748B"
    val_size = "26" if dark else "24"
    val_extra = "line-height:1.1" if dark else "font-variant-numeric:tabular-nums"
    return (
        f'<div style="background:{bg};color:{color};{border}border-radius:6px;'
        f'padding:16px 18px;display:flex;flex-direction:column;gap:4px">'
        f'<div style="font-size:12px;color:{lab_color}">{esc(label)}</div>'
        f'<div style="font-size:{val_size}px;font-weight:700;{val_extra}">{value_html}</div>'
        f'<div style="font-size:12.5px;color:{sub_color}">{sub_html}</div>'
        f'</div>'
    )


def render_v19_cards_html(meta: dict, j: dict) -> str:
    dout = j.get("decision_out") or {}
    verdict = meta.get("dca_verdict") or dout.get("verdict") or "—"
    role = meta.get("dca_role") or dout.get("role") or "—"
    exec_short = _EXEC_SHORT_V19.get(verdict, _strip_paren(dout.get("exec_line")) or "—")

    p_bull, p_bear = meta.get("p_bull_pct"), meta.get("p_bear_pct")
    p_base = None
    if isinstance(p_bull, (int, float)) and isinstance(p_bear, (int, float)):
        p_base = round(100 - p_bull - p_bear)
    ev5y, irr = meta.get("ev5y_pct"), meta.get("irr_base_pct")
    irr_note = _IRR_NOTE_V19.get(verdict, "")

    max_dd = (j.get("premortem") or {}).get("max_dd") or {}
    lo, hi = max_dd.get("lo"), max_dd.get("hi")
    path_risk = max_dd.get("path_risk") or ""
    # 顯示順序＝淺至深（hi 在前、lo 在後），對照樣稿「−30～−56%」讀法；
    # path_risk_from_lo 的燈號計算仍以 lo（較深的那端）為準，不受顯示順序影響。
    if hi is not None and lo is not None:
        maxdd_val = _v19_pct(hi, 0) + "～" + _v19_pct(lo, 0)
    elif lo is not None:
        maxdd_val = _v19_pct(lo, 0)
    elif hi is not None:
        maxdd_val = _v19_pct(hi, 0)
    else:
        maxdd_val = "—"

    fpe = meta.get("fpe_fy2")
    pct5y = meta.get("pct_5y")
    val = meta.get("val")
    tier = _pct5y_tier_label(pct5y)
    fpe_val = f"{fpe:.1f}x" if isinstance(fpe, (int, float)) else "—"

    cards = [
        _v19_card("裁決", esc(verdict),
                  f"角色：{esc(role)}　·　{esc(exec_short)}", dark=True),
        _v19_card("五年機率加權報酬", _v19_pct(ev5y),
                   f"牛 {esc(p_bull)}%／基 {esc(p_base) if p_base is not None else '—'}%／熊 {esc(p_bear)}%"),
        _v19_card("基本情境年化", _v19_pct(irr), esc(irr_note)),
        _v19_card("最大回撤範圍", maxdd_val,
                   _dot(path_risk) + f"路徑風險{esc(_RISK_LEVEL_LABEL_V19.get(path_risk, '—'))}"),
        _v19_card(f"本益比（{esc(_fy2_label(meta))}）", fpe_val,
                   (_dot(val) + f"五年分位 {esc(pct5y)}%，{esc(tier)}") if pct5y is not None else _dot(val) + "估值燈"),
    ]
    return '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px">' \
        + "".join(cards) + "</div>"


# ---- 頁首：24 格篩選器資料列 ----------------------------------------------

def _v19_cell(label: str, value_html: str) -> str:
    return f'<div><div class="k">{esc(label)}</div><div class="v">{value_html}</div></div>'


def render_v19_grid_html(meta: dict, j: dict) -> str:
    price = meta.get("price_at_dd")

    def num(v, nd=1, suffix="x"):
        if not isinstance(v, (int, float)):
            return "—"
        return f"{v:.{nd}f}{suffix}"

    trap_label = _strip_paren(meta.get("trap_label")) or "—"
    runway = meta.get("runway_post_y5")
    moat_trend_label = _MOAT_TREND_LABEL_V19.get(meta.get("moat_trend"), "—")
    archetype_secondary = _strip_paren(((j.get("archetype") or {}).get("secondary")))
    clock_label = _CLOCK_PHASE_LABEL_V19.get(meta.get("industry_clock_phase"), meta.get("industry_clock_phase") or "—")

    up_1y, up_2y, up_5y = meta.get("upside_short_pct"), meta.get("upside_mid_pct"), meta.get("upside_5y_pct")
    tgt_1y = _v19_derive_target(price, up_1y)
    tgt_2y = _v19_derive_target(price, up_2y)
    tgt_5y = _v19_derive_target(price, up_5y)

    verdict = meta.get("dca_verdict") or (j.get("decision_out") or {}).get("verdict")
    rearm_label = "加碼窗口" if verdict == "進場" else "重啟門檻"

    row1 = [
        _v19_cell("基本面評級", esc(meta.get("verdict")) or "—"),
        _v19_cell("訊號", f'{esc(meta.get("signal"))}　<span class="vs">{esc(_SIGNAL_PLAIN_V19.get(verdict, "—"))}</span>'),
        _v19_cell("估值燈", _dot(meta.get("val")) + esc(_DOT_COLOR_NAME_V19.get(meta.get("val"), "—"))),
        _v19_cell("均線", _dot("🟢" if meta.get("ma") == "✅" else "🔴") + ("強勢" if meta.get("ma") == "✅" else ("弱勢" if meta.get("ma") == "❌" else "—"))),
        _v19_cell("陷阱", _dot(meta.get("trap")) + esc(trap_label)),
        _v19_cell("五年後跑道", _dot(runway) + esc(_RUNWAY_LABEL_V19.get(runway, "—"))),
    ]
    row2 = [
        _v19_cell("護城河", f'{esc(meta.get("moat"))}　{esc(moat_trend_label)}　'
                   f'<span class="vs">執行 {esc(meta.get("moat_execution"))}・定價 {esc(meta.get("moat_pricing_power"))}</span>'),
        _v19_cell("品質分", esc(meta.get("quality_score")) or "—"),
        _v19_cell("成長持久", esc(meta.get("growth_durability")) or "—"),
        _v19_cell("資本配置", esc(meta.get("capalloc_grade")) or "—"),
        _v19_cell("原型", esc(meta.get("archetype")) + (f'　<span class="vs">{esc(archetype_secondary)}</span>' if archetype_secondary else "") if meta.get("archetype") else "—"),
        _v19_cell("產業時鐘", esc(clock_label) + (f'　<span class="vs">{esc(meta.get("cycle_position"))}</span>' if meta.get("cycle_position") else "")),
    ]
    row3 = [
        _v19_cell(f"本益比（{esc(_fy2_label(meta))}）", num(meta.get("fpe_fy2"))),
        _v19_cell("PEG（FY2）", num(meta.get("peg_fy2"), nd=2, suffix="")),
        _v19_cell("五年分位", (esc(meta.get("pct_5y")) + "%　<span class=\"vs\">見 §10 估值口徑</span>") if meta.get("pct_5y") is not None else "—"),
        _v19_cell("一年合理價", f'{_v19_usd(tgt_1y)}　<span class="vs">由 {_v19_pct(up_1y, 1)} 推算</span>' if tgt_1y is not None else "—"),
        _v19_cell("兩年合理價", f'{_v19_usd(tgt_2y)}　<span class="vs">由 {_v19_pct(up_2y, 1)} 推算</span>' if tgt_2y is not None else "—"),
        _v19_cell("五年基本情境", f'{_v19_usd(tgt_5y)}　<span class="vs">由 {_v19_pct(up_5y, 1)} 推算</span>' if tgt_5y is not None else "—"),
    ]
    row4 = [
        _v19_cell("牛市五年價", f'{_v19_usd(meta.get("bull_5y_price"))}　<span class="vs">{esc(meta.get("p_bull_pct"))}%</span>' if meta.get("bull_5y_price") is not None else "—"),
        _v19_cell("熊市五年價", f'{_v19_usd(meta.get("bear_5y_price"))}　<span class="vs">{esc(meta.get("p_bear_pct"))}%</span>' if meta.get("bear_5y_price") is not None else "—"),
        _v19_cell("不對稱比", esc(meta.get("asym_ratio")) if meta.get("asym_ratio") is not None else "—"),
        _v19_cell("內生成長上限", (esc(meta.get("endo_growth_ceiling")) + "%") if meta.get("endo_growth_ceiling") is not None else "—"),
        _v19_cell("AI 風險", (_dot(meta.get("ai_risk")) + esc(_RISK_LEVEL_LABEL_V19.get(meta.get("ai_risk"), "—"))) if meta.get("ai_risk") else "—"),
        _v19_cell(rearm_label, esc(meta.get("rearm_trigger")) or "—"),
    ]
    grid = "".join(row1 + row2 + row3 + row4)
    return (
        '<div style="display:grid;grid-template-columns:repeat(6,minmax(0,1fr));'
        'gap:8px 14px;font-size:12.5px;line-height:1.45">' + grid + "</div>"
    )


# ---- 頁首：什麼會讓我改變主意（三條，取自 triggers[]） --------------------

_CHANGEMIND_PRIORITY_V19 = ["估值rearm", "加碼", "Single Thing", "清倉", "減碼", "風險"]


def _norm_trigger_type(t: dict) -> str:
    return re.sub(r"[（(].*?[）)]", "", t.get("type") or "").strip()


def render_v19_changemind_html(j: dict) -> str:
    triggers = j.get("triggers") or []
    by_type: dict = {}
    for t in triggers:
        by_type.setdefault(_norm_trigger_type(t), []).append(t)
    picked = []
    for typ in _CHANGEMIND_PRIORITY_V19:
        cands = by_type.get(typ) or []
        if cands:
            picked.append(cands[0])
        if len(picked) >= 3:
            break
    if len(picked) < 3:
        for t in triggers:
            if t not in picked:
                picked.append(t)
            if len(picked) >= 3:
                break
    items = []
    for t in picked[:3]:
        threshold = t.get("threshold") or ""
        metric = t.get("metric") or ""
        strong_bits = threshold or metric
        detail = f"（{metric}）" if threshold and metric else ""
        action = t.get("action") or ""
        items.append(f"<li><strong>{esc(strong_bits)}</strong>{esc(detail)}：{esc(action)}。</li>")
    if not items:
        items = ["<li>—</li>"]
    return (
        '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:6px;'
        'padding:18px 22px;display:flex;flex-direction:column;gap:8px">'
        '<div style="font-size:13px;color:#64748B;letter-spacing:0.06em">什麼會讓我改變主意</div>'
        '<ul class="pts" style="font-size:15px">' + "".join(items) + "</ul></div>"
    )


def render_v19_dashboard_html(j: dict, meta: dict, facts: dict | None) -> str:
    """v19 版面頁首整塊：meta 行/h1/摘要/五張卡/24 格篩選器資料列/改變主意。"""
    top = render_v19_header_top_html(j, meta, facts)
    cards = render_v19_cards_html(meta, j)
    grid = render_v19_grid_html(meta, j)
    changemind = render_v19_changemind_html(j)
    return (
        '<header style="display:flex;flex-direction:column;gap:20px">\n'
        + top + "\n" + cards + "\n"
        + '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:6px;'
          'padding:14px 18px;display:flex;flex-direction:column;gap:10px">'
          '<div style="display:flex;flex-direction:row;justify-content:space-between;'
          'align-items:baseline"><div style="font-size:12px;color:#64748B;'
          'letter-spacing:0.06em">篩選器資料</div><div style="font-size:11.5px;color:#94A3B8">'
          '與 /dd-screener/ 同源，機器讀 dd-meta，人讀這一列</div></div>'
        + grid + "</div>\n"
        + changemind + "\n</header>\n"
    )


# ---- 免費資料區：§7 三到四年財務表 + ROE 拆解 -----------------------------

def render_v19_financials_html(j: dict) -> str | None:
    """quality.three_year[] 欄位隨列變動（毛利率/營益率用 Q2_2025/Q2_2026，
    trailing P/E 用 FY2022/FY2025）；動態收集出現過的欄位當表頭，缺格印「—」，
    不補算。"""
    rows_data = (j.get("quality") or {}).get("three_year") or []
    if not rows_data:
        return None
    cols: list = []
    for r in rows_data:
        if not isinstance(r, dict):
            continue
        for k in r:
            if k != "metric" and k not in cols:
                cols.append(k)
    header = "<tr><th>指標</th>" + "".join(f'<th class="num">{esc(c)}</th>' for c in cols) + "</tr>"
    rows = []
    for r in rows_data:
        if not isinstance(r, dict):
            continue
        cells = "".join(f'<td class="num">{esc(r[c]) if c in r else "—"}</td>' for c in cols)
        rows.append(f"<tr><td>{esc(r.get('metric'))}</td>{cells}</tr>")
    return '<table id="e9b">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


def render_v19_roe_html(j: dict) -> str | None:
    quality = j.get("quality") or {}
    rows_data = list(quality.get("dupont") or []) + list(quality.get("ccc") or [])
    if not rows_data:
        return None
    return _render_item_value_table("roe", rows_data)


# ---- 免費資料區：§8 法說原話（facts 逐句 quote 欄） ------------------------

def render_v19_quotes_html(facts: dict | None) -> str | None:
    if not facts:
        return None
    items = []
    for q in (facts.get("questions") or {}).values():
        for f in (q or {}).get("facts") or []:
            if not (isinstance(f, dict) and f.get("quote")):
                continue
            src = f.get("source") or {}
            as_of = src.get("as_of") or f.get("period") or ""
            items.append(
                f'<li>「{esc(f["quote"])}」<span class="mach">（{esc(f.get("label"))}，{esc(as_of)}）</span></li>'
            )
    if not items:
        return None
    return '<ul class="pts" id="quotes">' + "".join(items) + "</ul>\n"


# ---- 免費資料區：§10 情境樹逐項（scenario_meta.scenario_tree） -----------

def render_v19_scenario_tree_html(scenario_meta: dict | None) -> str | None:
    tree = (scenario_meta or {}).get("scenario_tree")
    if not isinstance(tree, dict):
        return None
    eps, pe, p = tree.get("eps") or {}, tree.get("pe") or {}, tree.get("p") or {}
    start = tree.get("start") or {}
    n_years = max((len(v) for v in eps.values() if isinstance(v, list)), default=0)
    header = ("<tr><th>情境</th><th class=\"num\">機率</th>"
              + "".join(f'<th class="num">年{i + 1}</th>' for i in range(n_years))
              + "<th class=\"num\">終端倍數</th></tr>")
    label_map = {"bull": "牛", "base": "基本", "bear": "熊"}
    rows = []
    for key in ("bull", "base", "bear"):
        path = eps.get(key) or []
        cells = "".join(f'<td class="num">{esc(v)}</td>' for v in path)
        pad = "".join('<td class="num">—</td>' for _ in range(n_years - len(path)))
        rows.append(
            f'<tr><td>{label_map.get(key, key)}</td><td class="num">{esc(p.get(key))}%</td>'
            f'{cells}{pad}<td class="num">{esc(pe.get(key))}x</td></tr>'
        )
    note = ""
    if start:
        note = (f'<p class="mach">起點：EPS {esc(start.get("eps"))}、'
                f'本益比 {esc(start.get("pe"))}x（{esc(start.get("basis"))}）</p>')
    return '<table id="stree">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n" + note


# ---- 免費資料區：§10 同業對照（facts 的 f_peer_* 三項利潤率） -------------

_PEER_FACT_RE = re.compile(r"^f_peer_([a-z0-9]+)_(gross_margin_pct|operating_margin_pct|fcf_margin_pct)$")
_PEER_METRIC_LABEL = {
    "gross_margin_pct": "毛利率", "operating_margin_pct": "營業利益率", "fcf_margin_pct": "FCF 利潤率",
}


def render_v19_peers_html(facts: dict | None) -> str | None:
    """facts 有同業區塊（f_peer_<ticker>_<metric>）才輸出；管線端尚未搬完時
    這裡回 None，呼叫端 fallback 到既有 E6（moat.competitors，判斷視圖）。"""
    if not facts:
        return None
    by_ticker: dict = {}
    for q in (facts.get("questions") or {}).values():
        for f in (q or {}).get("facts") or []:
            if not isinstance(f, dict):
                continue
            m = _PEER_FACT_RE.match(f.get("id") or "")
            if not m:
                continue
            tk, metric = m.group(1).upper(), m.group(2)
            by_ticker.setdefault(tk, {})[metric] = f.get("value")
    if not by_ticker:
        return None
    metrics = ["gross_margin_pct", "operating_margin_pct", "fcf_margin_pct"]
    header = "<tr><th>公司</th>" + "".join(f'<th class="num">{_PEER_METRIC_LABEL[m]}</th>' for m in metrics) + "</tr>"
    rows = [
        "<tr><td>{tk}</td>{cells}</tr>".format(
            tk=esc(tk),
            cells="".join(f'<td class="num">{esc(by_ticker[tk].get(m, "—"))}</td>' for m in metrics),
        )
        for tk in sorted(by_ticker)
    ]
    return '<table id="peers">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---- 免費資料區：§5 護城河——v19 答案表的實際形狀與舊 E7/E8 renderer 預期的
# 欄位名不同（E7 期待 n/question/status/evidence，v19 的 checkpoints 是
# item/level/text；E8 期待 fy0_rev/fy1e_rev/fy2e_rev，v19 的 segments 是
# share/driver/note）——沿用舊 renderer 會整表空白（已實測 e7/e8.html 對 FIX
# fixture 全空），故 v19 另立兩個對應實際形狀的 renderer，取代 E7/E8 在 v19
# 版面的注入（E6 對手對照欄位名不變，繼續沿用）。
#
# 2026-09-11（WP-H2-3）：原本這裡還有第三支 `render_v19_spread_html()`——已撤。
# `render_e5_html()` 現在自己認得同業矩陣形狀（並優先讀 `facts.peer_comparison`），
# v19 版面的 §5 標記直接指 `e5.html`；同一張表留兩支 renderer 是漂移的溫床。
# ---------------------------------------------------------------------------

def render_v19_threats_html(j: dict) -> str | None:
    rows_data = (j.get("moat") or {}).get("threats") or []
    if not rows_data:
        return None
    items = [
        '<li>{dot}{text}<span class="mach">（機率：{p}）</span></li>'.format(
            dot=_dot(r.get("level")), text=esc(r.get("text")), p=esc(r.get("p")),
        )
        for r in rows_data if isinstance(r, dict)
    ]
    if not items:
        return None
    return '<ul class="pts" id="threats">' + "".join(items) + "</ul>\n"


def render_v19_roic_checkpoints_html(j: dict) -> str | None:
    rd = (j.get("moat") or {}).get("roic_durability") or {}
    rows_data = rd.get("checkpoints") or []
    if not rows_data:
        return None
    header = "<tr><th>持續期檢查點</th><th>判定</th><th>依據</th></tr>"
    rows = [
        "<tr><td>{item}</td><td>{dot}</td><td>{text}</td></tr>".format(
            item=esc(r.get("item")), dot=_dot(r.get("level")), text=esc(r.get("text")),
        )
        for r in rows_data if isinstance(r, dict)
    ]
    summary = ""
    if rd.get("quadrant") or rd.get("endo_ceiling") is not None:
        summary = (
            '<p class="mach">象限：{q}｜ROIIC：{roiic}｜再投資率：{ri}｜'
            "內生成長天花板：{c}（{note}）</p>"
        ).format(q=esc(rd.get("quadrant")), roiic=esc(rd.get("roiic")),
                  ri=esc(rd.get("reinvest_rate")), c=esc(rd.get("endo_ceiling")),
                  note=esc(rd.get("formula_note")))
    return '<table id="roic">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n" + summary


# ---- 免費資料區：§6 成長——分部前瞻（growth.segments，share/driver/note 形狀）

def render_v19_segments_html(j: dict) -> str | None:
    rows_data = (j.get("growth") or {}).get("segments") or []
    if not rows_data:
        return None
    header = '<tr><th>分部</th><th class="num">占比</th><th>驅動</th><th>備註</th></tr>'
    rows = [
        '<tr><td>{seg}</td><td class="num">{share}</td><td>{drv}</td><td>{note}</td></tr>'.format(
            seg=esc(r.get("segment")), share=esc(r.get("share")) or "—",
            drv=esc(r.get("driver")), note=esc(r.get("note")) or "—",
        )
        for r in rows_data if isinstance(r, dict)
    ]
    return '<table id="segs">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---- 免費資料區：decision 折疊——致命指標全表／催化劑全表 ------------------

def render_v19_kill_html(j: dict) -> str | None:
    rows_data = j.get("kill_metrics") or []
    if not rows_data:
        return None
    header = "<tr><th>致命指標</th><th>熊市門檻</th><th>頻率</th><th>來源</th><th>狀態</th></tr>"
    rows = [
        "<tr><td>{m}</td><td>{th}</td><td>{w}</td><td>{s}</td><td>{st}</td></tr>".format(
            m=esc(r.get("metric")), th=esc(r.get("bear_threshold")), w=esc(r.get("window")),
            s=esc(r.get("source")), st=esc(r.get("last_status")),
        )
        for r in rows_data
    ]
    return '<table id="kill">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


def render_v19_catalysts_html(j: dict) -> str | None:
    cats = sorted(j.get("catalysts") or [], key=lambda c: c.get("date") or "9999-99")
    if not cats:
        return None
    header = "<tr><th>日期</th><th>事件</th><th>類型</th><th>影響</th><th>觀察重點</th></tr>"
    rows = [
        "<tr><td>{d}</td><td>{e}</td><td>{t}</td><td>{i}</td><td>{w}</td></tr>".format(
            d=esc(c.get("date")), e=esc(c.get("event")), t=esc(c.get("type")),
            i=esc(c.get("impact")) or "—", w=esc(c.get("watch")),
        )
        for c in cats
    ]
    return '<table id="catalysts">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"


# ---- v19 專用附錄 A（擇時）------------------------------------------------

def render_v19_appA_html(j: dict, meta: dict, facts: dict | None) -> str:
    """位置（回撤/突破）與階段（選股看板代碼）不在 judgment/facts 證據包內，
    不臆造——只印均線、產業循環位置（decision_inputs.cycle_position，注意這
    是景氣循環位置，不是股價技術位置）與距 52 週高點（facts，若有）。"""
    ma = meta.get("ma")
    ma_label = "強勢" if ma == "✅" else ("弱勢" if ma == "❌" else "—")
    cycle_pos = meta.get("cycle_position") or "—"
    f = _fact_by_id(facts, "f_q6_distance_from_52w_high")
    dist52 = f.get("value") if f else None
    parts = [f"均線：{esc(ma_label)}", f"產業循環位置：{esc(cycle_pos)}"]
    if dist52 is not None:
        parts.append(f"距 52 週高點 {_v19_pct(dist52, 1)}")
    line = "　・　".join(parts) + "。股價技術位置／階段（選股看板代碼）本輪證據包未提供，不填。擇時只是燈號，不進裁決。"
    return (
        '<details id="appA">\n<summary>附錄 A　擇時</summary>\n'
        f'<div class="mach" style="margin-top:6px">{line}</div>\n</details>\n'
    )


# ---- v19 專用附錄 B（證據清單，facts.findings_digest，缺就不寫此段） ------

def render_v19_appB_html(facts: dict | None) -> str | None:
    items = (facts or {}).get("findings_digest") or []
    if not items:
        return None
    header = '<tr><th style="width:8%">方向</th><th>發現</th><th>來源</th><th>日期</th></tr>'
    rows = []
    for it in items:
        if not isinstance(it, dict):
            continue
        direction = it.get("direction")
        rows.append(
            "<tr><td>{dot}{lab}</td><td>{claim}</td><td>{src}</td><td>{date}</td></tr>".format(
                dot=_dot(_DIRECTION_DOT_V19.get(direction, "⚪")),
                lab=esc(_DIRECTION_LABEL_V19.get(direction, "—")),
                claim=esc(it.get("claim")), src=esc(it.get("source")), date=esc(it.get("as_of")),
            )
        )
    return (
        '<details id="appB">\n<summary>附錄 B　證據清單</summary>\n'
        '<table style="margin-top:8px">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n</details>\n"
    )


# ---- v19 專用附錄 C（跟上一份比，contradictions[].prior_field，缺就不寫） -

def render_v19_appC_html(j: dict) -> str | None:
    items = [c for c in (j.get("contradictions") or []) if isinstance(c, dict) and c.get("prior_field")]
    if not items:
        return None
    header = "<tr><th>欄位</th><th>上一份</th><th>本份</th><th>原因</th></tr>"
    rows = [
        "<tr><td>{axis}</td><td>{a}</td><td>{b}</td><td>{r}</td></tr>".format(
            axis=esc(c.get("axis")), a=esc(c.get("side_a")), b=esc(c.get("side_b")), r=esc(c.get("ruling")),
        )
        for c in items
    ]
    note = ""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import dd_prior  # noqa: E402 — 只讀既有 DRIFT_WATCH 清單，不改該檔
        note = '<p class="mach">對帳欄位清單（DRIFT_WATCH，共 {0} 欄）：{1}</p>'.format(
            len(dd_prior.DRIFT_WATCH), esc("、".join(dd_prior.DRIFT_WATCH))
        )
    except Exception:
        pass
    return (
        '<details id="appC">\n<summary>附錄 C　跟上一份比</summary>\n'
        '<table style="margin-top:8px">\n' + header + "\n" + "\n".join(rows) + "\n</table>\n"
        + note + "</details>\n"
    )


def write_mechanical_prose(j: dict, prior: dict | None, out_dir: Path,
                           scenario_meta: dict | None = None) -> list:
    """把 revlog／s14／appA 三個機械段寫進 `out_dir/{sid}.html`（`out_dir`
    即 run 目錄的 `prose/`）。散文 agent 不寫這三段，見 render-rules.md 之外
    另行約定的 v17 prose bundle §⑦。回傳已寫入的 sid 清單。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "revlog.html").write_text(
        render_revlog_html(j, prior, scenario_meta), encoding="utf-8")
    (out_dir / "s14.html").write_text(render_s14_html(j), encoding="utf-8")
    (out_dir / "appA.html").write_text(render_appA_section_html(j), encoding="utf-8")
    return ["revlog", "s14", "appA"]


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
    raw = load_json(jpath)
    j = dd_project.view_for(raw, jpath)  # 舊形狀＝原物件；v19＝投影視圖
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
    # 2026-09-11（WP-H2-3）：E5 對 v19 改讀同業矩陣，優先取 facts.peer_comparison；
    # 舊形狀判斷檔 load_facts 回 None，走既有窄表路徑，輸出逐位元組不變。
    e5_facts = dd_project.load_facts(raw, jpath) if dd_project.is_v19(raw) else None
    (out_dir / "e5.html").write_text(render_e5_html(j, e5_facts), encoding="utf-8")
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

    v19_written = []
    if dd_project.is_v19(raw):
        # v19（WP-H2-2）：新版面頁首與免費資料區片段，只對 meta.contract=="v19"
        # 的判斷檔生成——舊形狀報告的輸出檔案集合完全不變（見上方既有五行）。
        facts = dd_project.load_facts(raw, jpath)
        (out_dir / "v19-dashboard.html").write_text(
            render_v19_dashboard_html(j, meta, facts), encoding="utf-8")
        v19_written.append("v19-dashboard.html")
        for name, html_text in (
            ("v19-threats.html", render_v19_threats_html(j)),
            ("v19-roic.html", render_v19_roic_checkpoints_html(j)),
            ("v19-segs.html", render_v19_segments_html(j)),
            ("v19-e9b.html", render_v19_financials_html(j)),
            ("v19-roe.html", render_v19_roe_html(j)),
            ("v19-quotes.html", render_v19_quotes_html(facts)),
            ("v19-stree.html", render_v19_scenario_tree_html(scenario_meta)),
            ("v19-peers.html", render_v19_peers_html(facts)),
            ("v19-kill.html", render_v19_kill_html(j)),
            ("v19-catalysts.html", render_v19_catalysts_html(j)),
            ("v19-appB.html", render_v19_appB_html(facts)),
            ("v19-appC.html", render_v19_appC_html(j)),
        ):
            if html_text:
                (out_dir / name).write_text(html_text, encoding="utf-8")
                v19_written.append(name)
        (out_dir / "v19-appA.html").write_text(
            render_v19_appA_html(j, meta, facts), encoding="utf-8")
        v19_written.append("v19-appA.html")
        (out_dir / "v19-revlog.html").write_text(
            render_revlog_html(j, None, scenario_meta), encoding="utf-8")
        v19_written.append("v19-revlog.html")
        (out_dir / "v19-s14.html").write_text(render_s14_html(j), encoding="utf-8")
        v19_written.append("v19-s14.html")

    print(f"寫入 {out_dir}: dd-meta.html, e2.html, e12.html, appA-table.html, dashboard.html, "
          "e3.html, e5.html, e6.html, e7.html, e8.html, e9.html, e10.html"
          + (", audit.html" if audit_html else "（無 audit_rows，略過 audit.html）")
          + (", " + ", ".join(v19_written) if v19_written else ""))


if __name__ == "__main__":
    main()
