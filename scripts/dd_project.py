#!/usr/bin/env python3
"""dd_project.py — v19 判斷檔 → 舊形狀判斷視圖的**單一程式轉接**（WP-H1）。

為什麼只有一處：v19 把判斷檔收斂成「六問 answers＋scenario_inputs＋
counter_evidence＋judge-owned decision_inputs」，但既有的檢查與渲染
（`validate_judgment.py` 的 J1／J2／J6／同源／展開區塊／反證三視角、
`gen_dd_tables.py` 的 dd-meta 與七表、`dd_brief.py`、`dd_bundle.py` 的
gate_view、`dd_delta.py` 的 DRIFT_WATCH 對帳）全部依舊欄位取資料。**保留的是
檢查語義，不是原讀檔路徑**——所以新契約在這裡投影一次成舊形狀，所有消費端
經同一個視圖讀，不靠模型再寫一份舊格式。

三條鐵律：

1. **舊形狀零改動**：`meta.contract` 不是 `"v19"` → `project()` 原物件回傳
   （identity），所有消費端行為與改前逐 byte 相同。
2. **程式只做算術與映射，不得補判斷**：缺的判斷值就留空，讓對應檢查 FAIL／
   WARN。評分與燈號（moat 合併分、capalloc_grade、path_risk）只在判斷者給了
   子輸入時才算；moat 等級、估值燈、品質分、signal 一律由判斷者明示，程式不
   從分數或毛利率反推。
3. **同一件事不准兩邊都填**：判斷者填了會被投影覆寫的欄（decision_inputs 的
   13 個機械欄）→ `validate_judgment` 的 v19 檢查報 FAIL，而不是靜默取一邊。

投影規則逐條列在 `scripts/dd_schema/judgment-v19.md`（P-01…P-24），本檔函式
名與該表編號一一對應。

CLI：
  python3 scripts/dd_project.py view JUDGMENT.json [--facts F.json] \\
      [--scenario-meta M.json] [--out VIEW.json]
  python3 scripts/dd_project.py scenario JUDGMENT.json [--out scenario.json]
  python3 scripts/dd_project.py normalize JUDGMENT.json [--write]
  python3 scripts/dd_project.py prose-stub JUDGMENT.json --out PROSE_DIR \\
      [--facts F.json] [--scenario-meta M.json]
"""
from __future__ import annotations

import argparse
import copy
import html as _html
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent

CONTRACT_V19 = "v19"

QUESTION_KEYS = (
    "q1_business", "q2_moat", "q3_growth",
    "q4_capital", "q5_valuation", "q6_how_wrong",
)

# 六問 → 舊 reasoning 子鍵（judgment-rules.md §2 自己的對映：問一 industry／
# 問二 moat／問三 growth／問四 governance／問五 valuation／問六 premortem）。
QUESTION_TO_REASONING = {
    "q1_business": "industry",
    "q2_moat": "moat",
    "q3_growth": "growth",
    "q4_capital": "governance",
    "q5_valuation": "valuation",
    "q6_how_wrong": "premortem",
}

# 六問 → plain.six 子鍵（v18 既有六問白話欄）。
QUESTION_TO_PLAIN_SIX = {
    "q1_business": "how_it_makes_money",
    "q2_moat": "moat",
    "q3_growth": "growth",
    "q4_capital": "capital",
    "q5_valuation": "valuation",
    "q6_how_wrong": "how_wrong",
}

# decision_inputs 由程式投影的欄（判斷者不得填非 null 值）。
PROJECTED_DECISION_INPUT_KEYS = (
    "trap", "val", "moat", "moat_trend", "runway_post_y5", "capalloc_grade",
    "archetype", "price_at_dd", "week26_return_pct", "consensus_rev_3m_pct",
    "asym_ratio", "irr_base_pct", "ev5y_pct",
    "val_denominator_disputed", "val_denominator_note",
)

# decision_inputs 的 judge-owned 欄（v19 required）。
JUDGE_OWNED_DECISION_INPUT_KEYS = (
    "signal", "ma", "cycle_position", "cycle_verdict",
    "thesis_irreconcilable", "valuation_dependent", "market_wrong_reason_given",
    "momentum_overheated", "cycle_gates_pass",
)

# 覆寫層（選填，判斷者或 orchestrator 給）。
OVERLAY_DECISION_INPUT_KEYS = (
    "role_hint", "qc49_inherit_prior", "prior_verdict", "prior_role", "held_now",
)

# 事實欄 → facts.json 的 fact id（P-20）。
FACT_BACKED_DECISION_INPUTS = {
    "price_at_dd": "f_price_at_dd",
    "week26_return_pct": "f_week26_return_pct",
    "consensus_rev_3m_pct": "f_consensus_rev_3m_fy1_pct",
}

CAPALLOC_ITEM_NAMES = ("ma_roiic", "buyback_yield", "sbc_dilution")


def is_v19(judgment) -> bool:
    """唯一判別：`meta.contract` == "v19"。沒有這個標記的一律當舊形狀。"""
    if not isinstance(judgment, dict):
        return False
    return ((judgment.get("meta") or {}).get("contract")) == CONTRACT_V19


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------

def _vv(judgment, qkey, *path):
    """取 answers[qkey].verdict_values 底下的巢狀值；任一層缺就回 None。"""
    node = ((judgment.get("answers") or {}).get(qkey) or {}).get("verdict_values") or {}
    for part in path:
        if not isinstance(node, dict):
            return None
        node = node.get(part)
    return node


def _facts_index(facts) -> dict:
    """facts.json → {fact_id: fact}。facts 為 None 時回空 dict。"""
    idx = {}
    for q in ((facts or {}).get("questions") or {}).values():
        for f in (q or {}).get("facts") or []:
            if isinstance(f, dict) and f.get("id"):
                idx[f["id"]] = f
    return idx


def _fact_value(fact_idx, fid):
    f = fact_idx.get(fid)
    return f.get("value") if isinstance(f, dict) else None


# ---------------------------------------------------------------------------
# P-21 path_risk：既有切點（judgment-rules.md 問六）🟢 0～−30%／🟡 −30～−50%／
# 🔴 <−50%。只把**已判定的** Max DD 範圍轉燈號，不判斷範圍本身。
# ---------------------------------------------------------------------------

def path_risk_from_lo(lo):
    if lo is None:
        return None
    try:
        v = float(lo)
    except (TypeError, ValueError):
        return None
    if v >= -30:
        return "🟢"
    if v >= -50:
        return "🟡"
    return "🔴"


# ---------------------------------------------------------------------------
# P-22 capalloc_grade：既有計分卡（judgment-rules.md 問四）——適用項 ≥2 過＝A、
# 1＝B、0＝C。適用性與逐項輸入由判斷者明示，程式只加總；一項都不適用時留空
# （不猜）。判斷者自己給 grade 就以判斷者為準。
# ---------------------------------------------------------------------------

def capalloc_grade_from_items(capalloc):
    if not isinstance(capalloc, dict):
        return None, None
    explicit = capalloc.get("grade")
    items = capalloc.get("items") or []
    applicable = [i for i in items if isinstance(i, dict) and i.get("applicable") is True]
    if not applicable:
        return explicit, None
    passed = sum(1 for i in applicable if i.get("passed") is True)
    computed = "A" if passed >= 2 else ("B" if passed == 1 else "C")
    return (explicit if explicit else computed), computed


# ---------------------------------------------------------------------------
# P-06 moat 合併分：combined 缺時取 execution／pricing 平均、score 缺時取
# combined（實檔 17 份全部吻合）。**等級不推**：8.5 分在實檔同時對應 A 與 B，
# 映射不成立，grade 只能由判斷者給。
# ---------------------------------------------------------------------------

def _fill_moat_scores(moat: dict) -> dict:
    if not isinstance(moat, dict):
        return moat
    out = dict(moat)
    ex, pr = out.get("execution"), out.get("pricing")
    if out.get("combined") is None and isinstance(ex, (int, float)) and isinstance(pr, (int, float)):
        out["combined"] = round((ex + pr) / 2.0, 2)
    if out.get("score") is None and out.get("combined") is not None:
        out["score"] = out["combined"]
    return out


# ---------------------------------------------------------------------------
# P-24 catalysts 缺席時的機械投影：帶日期的 triggers 逐列轉成行事曆條目。
# 影響度（高／中／低）是判斷，程式不填——留 None，讓渲染顯示「—」。
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# P-26 同業對照表（WP-H2-1，2026-09-11；Codex 裁定 3「部分搬移」）
#
# 同業的數字、期間、口徑、來源住 `facts.peer_comparison`，判斷者只寫每家的
# `strategy_note`（對手有沒有本錢打價格戰、策略定位）。這裡把兩邊合起來還原成
# 舊形狀的兩張表：`moat.spread_table`（度量為列）與 `moat.competitors`（對手為
# 列）。**一個數字都不新增、不換算**：facts 沒有的度量就留 None，由渲染顯示空格。
# ---------------------------------------------------------------------------

# facts 的度量 key → 舊形狀 competitors 欄名（E6 表頭順序）。
_PEER_KEY_TO_COMPETITOR_FIELD = {
    "rev_growth_pct": "rev_growth",
    "gross_margin_pct": "gm",
    "operating_margin_pct": "om",
    "rd_intensity_pct": "rd_intensity",
    "fcf_margin_pct": "fcf_margin",
    "net_cash": "net_cash",
}


def _peer_rows(facts):
    pc = (facts or {}).get("peer_comparison") or {}
    metrics = [m for m in (pc.get("metrics") or []) if isinstance(m, dict) and m.get("key")]
    rows = [r for r in (pc.get("rows") or []) if isinstance(r, dict) and r.get("name")]
    return pc, metrics, rows


def spread_table_from_facts(facts, notes=None) -> list:
    """度量為列：`{"metric": 中文表頭, "period": …, "unit": …, <公司名>: 值, "note": …}`。

    `notes`＝判斷者的 `moat.spread_notes`（{度量 key: 一句判讀}），沒給就退回
    facts 的 metric 事實層註記；兩者皆無就不放 note 欄。"""
    _pc, metrics, rows = _peer_rows(facts)
    out = []
    for m in metrics:
        key = m["key"]
        row = {"metric": m.get("label") or key}
        periods = set()
        for r in rows:
            val = (r.get("values") or {}).get(key)
            row[r["name"]] = val
            if val is not None and r.get("period"):
                periods.add(r["period"])
        if len(periods) == 1:
            row["period"] = periods.pop()
        if m.get("unit"):
            row["unit"] = m["unit"]
        note = (notes or {}).get(key) or m.get("note")
        if note:
            row["note"] = note
        out.append(row)
    return out


def competitors_from_facts(facts, competitor_notes=None) -> list:
    """對手為列（不含本檔自己）。數字來自 facts，`strategy_note` 來自判斷者。

    對名：先精確比對，再比對「facts 名是判斷者寫法的前綴」（判斷者常寫
    `EME（EMCOR）`，facts 只有 `EME`）。對不上就留空 note，由
    `validate_judgment` 的必要項目檢查報缺，不靜默補字。"""
    pc, metrics, rows = _peer_rows(facts)
    subject = pc.get("subject")
    notes = {}
    for n in competitor_notes or []:
        if isinstance(n, dict) and n.get("name"):
            notes[n["name"]] = n
    out = []
    for r in rows:
        name = r["name"]
        if r.get("is_subject") or (subject and name == subject):
            continue
        entry = {"name": name}
        for m in metrics:
            field = _PEER_KEY_TO_COMPETITOR_FIELD.get(m["key"])
            if field:
                entry[field] = (r.get("values") or {}).get(m["key"])
        hit = notes.get(name)
        if hit is None:
            for jname, n in notes.items():
                if jname.startswith(name) or name.startswith(jname):
                    hit = n
                    break
        if hit:
            if hit.get("name"):
                entry["name"] = hit["name"]
            if hit.get("strategy_note"):
                entry["strategy_note"] = hit["strategy_note"]
        if r.get("period"):
            entry["period"] = r["period"]
        out.append(entry)
    return out


_TRIGGER_TO_CATALYST_TYPE = {
    "複審日期": "other", "假設驗證": "guidance", "風險": "other",
    "Single Thing": "other", "估值rearm": "other",
    "加碼": "other", "減碼": "other", "清倉": "other",
}


def catalysts_from_triggers(triggers) -> list:
    out = []
    for t in triggers or []:
        if not isinstance(t, dict):
            continue
        date = (t.get("date") or "").strip()
        if not date:
            continue
        out.append({
            "date": date,
            "type": _TRIGGER_TO_CATALYST_TYPE.get(
                re.sub(r"[（(].*?[）)]", "", t.get("type") or "").strip(), "other"),
            "event": t.get("text"),
            "impact": None,
            "watch": t.get("metric") or t.get("threshold"),
        })
    return out


# ---------------------------------------------------------------------------
# 主投影
# ---------------------------------------------------------------------------

def project(judgment: dict, facts: dict | None = None,
            scenario_meta: dict | None = None) -> dict:
    """v19 判斷檔 → 舊形狀視圖。非 v19 一律原物件回傳（identity）。

    `facts` 只用來投影三個純事實欄（price_at_dd／week26_return_pct／
    consensus_rev_3m_pct）；沒給 facts 時退回判斷檔自己帶的值（若有），再沒有
    就留 None，由既有檢查報缺。`scenario_meta` 目前不參與投影（EV／IRR／AR 由
    `dd_metric_resolver` 在各消費端統一解析），保留參數位是為了呼叫端一致。
    """
    if not is_v19(judgment):
        return judgment

    j = judgment
    fact_idx = _facts_index(facts)
    view: dict = {}

    # P-02／P-03 原樣搬（meta 保留 contract 標記，dd-meta 只取 ticker/date/schema）
    view["meta"] = copy.deepcopy(j.get("meta") or {})
    for key in ("oneliner", "thesis", "appendix_a", "eps_meta", "scenario_ref"):
        if key in j:
            view[key] = copy.deepcopy(j[key])

    # P-04 archetype ← 問一
    view["archetype"] = copy.deepcopy(_vv(j, "q1_business", "archetype") or {})
    # P-05 industry ← 問一
    view["industry"] = copy.deepcopy(_vv(j, "q1_business", "industry") or {})

    # P-06 moat ← 問二（含 roic_durability）
    view["moat"] = _fill_moat_scores(copy.deepcopy(_vv(j, "q2_moat", "moat") or {}))
    # 機制句是 v19 新欄，舊形狀沒有對應欄位；併進 trend_evidence 會竄改原文，
    # 故原樣保留在 moat.mechanism（舊 schema 不禁止額外欄位，渲染不讀）。
    # P-26 同業兩張表 ← facts.peer_comparison ＋ 判斷者的 strategy_note／
    # spread_notes。facts 沒有同業資料時兩張表都不生（`moat.peer_na_reason`
    # 由 validate 要求判斷者說明），不放空表假裝有比過。
    spread_notes = view["moat"].pop("spread_notes", None)
    competitor_notes = view["moat"].pop("competitor_notes", None)
    if (facts or {}).get("peer_comparison"):
        view["moat"]["spread_table"] = spread_table_from_facts(facts, spread_notes)
        view["moat"]["competitors"] = competitors_from_facts(facts, competitor_notes)

    # P-07 growth ← 問三
    # driver_mix／endo_ceiling_basis 是 v19 新欄，舊 schema 不禁額外欄位，原樣
    # 保留讓散文引用（渲染不讀，dd-meta 只取白名單欄）。
    growth = copy.deepcopy(_vv(j, "q3_growth", "growth") or {})
    view["growth"] = growth

    # P-08／P-09 quality／governance ← 問四
    view["quality"] = copy.deepcopy(_vv(j, "q4_capital", "quality") or {})
    governance = copy.deepcopy(_vv(j, "q4_capital", "governance") or {})
    capalloc = _vv(j, "q4_capital", "capalloc")
    grade, _computed = capalloc_grade_from_items(capalloc)
    governance["capalloc_grade"] = grade
    if isinstance(capalloc, dict) and capalloc.get("items"):
        governance.setdefault("scorecard", [])
        if not governance["scorecard"]:
            governance["scorecard"] = [
                {
                    "year": "—",
                    "action": i.get("name"),
                    "rationale": i.get("input"),
                    "grade": ("過" if i.get("passed") else ("不過" if i.get("applicable") else "N/A")),
                }
                for i in capalloc["items"] if isinstance(i, dict)
            ]
    view["governance"] = governance

    # P-10 valuation ← 問五（分母爭議兩欄搬去 decision_inputs，不留兩份）
    valuation = copy.deepcopy(_vv(j, "q5_valuation", "valuation") or {})
    denom_disputed = valuation.pop("denominator_disputed", None)
    denom_note = valuation.pop("denominator_note", None)
    view["valuation"] = valuation

    # P-11 trap_analysis ← 問六
    trap = copy.deepcopy(_vv(j, "q6_how_wrong", "trap") or {})
    view["trap_analysis"] = {"verdict": trap.get("verdict"), "label": trap.get("label")}

    # P-12 premortem ← counter_evidence.blind_spots ＋ scenario_inputs.max_dd
    ce = j.get("counter_evidence") or {}
    scenario_inputs = j.get("scenario_inputs") or {}
    max_dd_src = copy.deepcopy(scenario_inputs.get("max_dd") or {})
    max_dd = {
        "lo": max_dd_src.get("lo"),
        "hi": max_dd_src.get("hi"),
        "path_risk": max_dd_src.get("path_risk") or path_risk_from_lo(max_dd_src.get("lo")),
    }
    if max_dd_src.get("trigger_time") is not None:
        max_dd["trigger_time"] = max_dd_src.get("trigger_time")
    view["premortem"] = {
        "blind_spots": copy.deepcopy(ce.get("blind_spots") or []),
        "max_dd": max_dd,
    }

    # P-13～P-16 反證唯一居所的其餘四塊
    view["contradictions"] = copy.deepcopy(ce.get("contradictions") or [])
    view["triggers"] = copy.deepcopy(ce.get("triggers") or [])
    if ce.get("kill_metrics"):
        view["kill_metrics"] = copy.deepcopy(ce["kill_metrics"])
    if ce.get("evidence_dismissed") is not None:
        view["evidence_dismissed"] = copy.deepcopy(ce["evidence_dismissed"])

    # P-17 decision_out ＝ 程式寫入的矩陣欄 ＋ 行動條件（rearm／exec_line）
    dout = copy.deepcopy(j.get("decision_out") or {})
    actions = ce.get("action_conditions") or {}
    if actions.get("rearm_trigger") is not None:
        dout["rearm_trigger"] = actions.get("rearm_trigger")
    if actions.get("exec_line") is not None:
        dout["exec_line"] = actions.get("exec_line")
    if dout.get("holding_cap") in (None, "") and actions.get("holding_cap"):
        dout["holding_cap"] = actions.get("holding_cap")
    view["decision_out"] = dout

    # P-18 reasoning ← 六問的短理由
    reasoning = {}
    for qkey, rkey in QUESTION_TO_REASONING.items():
        text = ((j.get("answers") or {}).get(qkey) or {}).get("reasoning")
        if text:
            reasoning[rkey] = text
    view["reasoning"] = reasoning

    # P-19 plain.six ← 六問的結論句（判斷句只寫一次，白話段落直接引用）
    six = {}
    for qkey, pkey in QUESTION_TO_PLAIN_SIX.items():
        text = ((j.get("answers") or {}).get(qkey) or {}).get("verdict")
        if text:
            six[pkey] = text
    plain = copy.deepcopy(j.get("plain") or {})
    if six:
        plain["six"] = six
    if plain:
        view["plain"] = plain

    # P-20 decision_inputs：judge-owned 原樣 ＋ 機械欄投影
    raw_di = j.get("decision_inputs") or {}
    di = {}
    for k in JUDGE_OWNED_DECISION_INPUT_KEYS:
        if k in raw_di:
            di[k] = raw_di[k]
    for k in OVERLAY_DECISION_INPUT_KEYS:
        if k in raw_di:
            di[k] = raw_di[k]
    di["trap"] = trap.get("verdict")
    di["val"] = valuation.get("val_light")
    di["moat"] = view["moat"].get("grade")
    di["moat_trend"] = view["moat"].get("trend")
    di["runway_post_y5"] = growth.get("runway_post_y5")
    di["capalloc_grade"] = grade
    di["archetype"] = (view["archetype"] or {}).get("primary")
    for key, fid in FACT_BACKED_DECISION_INPUTS.items():
        value = _fact_value(fact_idx, fid)
        di[key] = value if value is not None else raw_di.get(key)
    # 三個衍生欄一律 null，由 scenario 權威重算（contract 既有規定）
    for k in ("asym_ratio", "irr_base_pct", "ev5y_pct"):
        di[k] = None
    if denom_disputed is not None:
        di["val_denominator_disputed"] = denom_disputed
    if denom_note is not None:
        di["val_denominator_note"] = denom_note
    view["decision_inputs"] = di

    # P-23 catalysts：有就用判斷者給的（獨立居所），缺席才從帶日期的 triggers 投影
    if j.get("catalysts") is not None:
        view["catalysts"] = copy.deepcopy(j["catalysts"])
    else:
        view["catalysts"] = catalysts_from_triggers(view["triggers"])

    # 供消費端辨識這是投影視圖（不進 dd-meta——build_dd_meta 只取白名單欄）
    view["_projected_from"] = CONTRACT_V19
    return view


# ---------------------------------------------------------------------------
# 載入輔助：消費端一行接線
# ---------------------------------------------------------------------------

def resolve_facts_path(judgment: dict, judgment_path) -> Path | None:
    """`facts_ref` 解析順序：絕對路徑 → repo root → 判斷檔所在目錄。找不到回
    None（呼叫端自行降級，不硬性擋——事實欄會退回判斷檔自帶值）。"""
    ref = (judgment or {}).get("facts_ref")
    if not ref:
        return None
    p = Path(ref)
    if p.is_absolute():
        return p if p.exists() else None
    for cand in (ROOT / p, Path(judgment_path).parent / p):
        if cand.exists():
            return cand
    return None


def load_facts(judgment: dict, judgment_path, facts_path=None):
    path = Path(facts_path) if facts_path else resolve_facts_path(judgment, judgment_path)
    if path is None or not Path(path).exists():
        return None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def view_for(judgment: dict, judgment_path, facts_path=None, scenario_meta=None) -> dict:
    """消費端統一入口：舊形狀原樣回傳，v19 自動找 facts 後投影。"""
    if not is_v19(judgment):
        return judgment
    facts = load_facts(judgment, judgment_path, facts_path)
    return project(judgment, facts, scenario_meta)


def load_view(judgment_path, facts_path=None, scenario_meta=None) -> tuple:
    """回傳 (raw, view)。"""
    raw = json.loads(Path(judgment_path).read_text(encoding="utf-8"))
    return raw, view_for(raw, judgment_path, facts_path, scenario_meta)


# ---------------------------------------------------------------------------
# prose-stub：完整版散文段的機械骨架（H2 的散文 agent 會覆寫）
#
# 只把投影視圖已有的內容排進 `<section id="sX">`：六問各一段（結論句＋短理由
# ＋引用的事實 id），反證三視角、矛盾裁定、觸發器條列。**不生新句子、不加形容
# 詞**——這是佔位骨架，讓 `render_dd.py --assemble` 對 v19 run 能組出完整版頁
# 面，散文品質（外資報告風格、條列白話）是 H2 散文 prompt 的工作。
# ---------------------------------------------------------------------------

def _esc(v) -> str:
    return _html.escape("" if v is None else str(v))


_STUB_SECTIONS = [
    ("s1", "1．結論"),
    ("s2", "2．論點"),
    ("s3", "3．產業"),
    ("s4", "4．商業模式"),
    ("s5", "5．護城河"),
    ("s6", "6．成長"),
    ("s7", "7．財務品質"),
    ("s8", "8．最新財報"),
    ("s9", "9．資本配置與治理"),
    ("s10", "10．估值與情境"),
    ("s11", "11．矛盾與裁定"),
    ("s12", "12．可能看錯在哪"),
    ("decision", "13．統一裁決"),
]

# 段落 → 取哪一問的答案（沒有對應問題的段落只放機械內容）。
_STUB_SECTION_QUESTION = {
    "s3": "q1_business",
    "s4": "q1_business",
    "s5": "q2_moat",
    "s6": "q3_growth",
    "s9": "q4_capital",
    "s10": "q5_valuation",
    "s12": "q6_how_wrong",
}


def _answer_block(raw: dict, qkey: str) -> str:
    ans = ((raw.get("answers") or {}).get(qkey) or {})
    parts = []
    if ans.get("verdict"):
        parts.append(f"<p><b>{_esc(ans['verdict'])}</b></p>")
    if ans.get("reasoning"):
        parts.append(f"<p>{_esc(ans['reasoning'])}</p>")
    refs = ans.get("fact_refs") or []
    if refs:
        parts.append("<p class=\"note\">引用事實：{0}</p>".format(
            _esc("、".join(str(r) for r in refs))))
    return "\n".join(parts) if parts else "<p>—</p>"


def prose_stub(raw: dict, view: dict) -> dict:
    """回傳 {sid: html}；`revlog`／`s14`／`appA` 由 gen_dd_tables 機械生成，不在此。"""
    out = {}
    for sid, heading in _STUB_SECTIONS:
        body = []
        qkey = _STUB_SECTION_QUESTION.get(sid)
        if qkey:
            body.append(_answer_block(raw, qkey))
        if sid == "s1":
            body.append(f"<p>{_esc(view.get('oneliner'))}</p>")
        if sid == "s2":
            for h in ((view.get("thesis") or {}).get("H") or []):
                body.append("<p><b>{0}</b>：{1}（門檻：{2}）</p>".format(
                    _esc(h.get("id")), _esc(h.get("text")), _esc(h.get("threshold"))))
        if sid == "s11":
            items = []
            for c in view.get("contradictions") or []:
                if not isinstance(c, dict) or c.get("prior_field"):
                    continue
                items.append("<li>{0}：{1}</li>".format(
                    _esc(c.get("axis")), _esc(c.get("ruling"))))
            body.append("<ul>{0}</ul>".format("".join(items)) if items else "<p>—</p>")
        if sid == "s12":
            items = []
            for b in ((view.get("premortem") or {}).get("blind_spots") or []):
                if not isinstance(b, dict):
                    continue
                items.append("<li><b>{0}</b>：{1}</li>".format(
                    _esc(b.get("view")),
                    _esc(b.get("evidence") or b.get("assumption") or b.get("not_applicable_reason"))))
            body.append("<ul>{0}</ul>".format("".join(items)) if items else "<p>—</p>")
        if sid == "decision":
            dout = view.get("decision_out") or {}
            body.append("<p><b>{0}</b>｜{1}</p>".format(_esc(dout.get("verdict")), _esc(dout.get("role"))))
            if dout.get("exec_line"):
                body.append(f"<p>{_esc(dout['exec_line'])}</p>")
            body.append("<!-- AUDIT -->")
            body.append("<!-- E12 -->")
        markers = {
            "s2": "<!-- E2 -->", "s3": "<!-- E3 -->", "s6": "<!-- E8 -->",
            "s7": "<!-- E9 -->", "s10": "<!-- E11 -->",
        }
        if sid in markers:
            body.append(markers[sid])
        if sid == "s5":
            body.extend(["<!-- E5 -->", "<!-- E6 -->", "<!-- E7 -->"])
        if sid == "s9":
            body.append("<!-- E10 -->")
        out[sid] = '<section id="{0}">\n<h2>{1}</h2>\n{2}\n</section>\n'.format(
            sid, _esc(heading), "\n".join(body) or "<p>—</p>")
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# scenario.json 產生器（P-25）：v19 的情境假設只寫在 `scenario_inputs` 一處，
# `dd_scenario.py` 的輸入檔由這裡機械產出——判斷者不必把同一組 EPS 路徑、倍數
# 與機率再抄一次到 scenario.json。價格取 facts 的 f_price_at_dd，共識三年取
# eps_meta.base_eps_path，其餘欄位原樣搬。**不補判斷**：judge 沒給的欄
# （basis／endo_ceiling_exceeded／peer_max_fpe）就不寫，由 dd_scenario.py 自己
# 的檢查去報。
# ---------------------------------------------------------------------------

_FY_KEY_RE = re.compile(r"FY\s*(\d{4})")


def scenario_input_from_v19(raw: dict, facts: dict | None) -> dict:
    si = raw.get("scenario_inputs") or {}
    meta = raw.get("meta") or {}
    fact_idx = _facts_index(facts)
    eps_path = (raw.get("eps_meta") or {}).get("base_eps_path") or {}
    fy_years = sorted(
        (int(m.group(1)), k) for k, m in
        ((k, _FY_KEY_RE.search(k)) for k in eps_path if isinstance(k, str)) if m
    )
    forward = [k for _y, k in fy_years if not k.endswith("A")]
    consensus = {}
    for i, key in enumerate(forward[:3], start=1):
        value = eps_path.get(key)
        if isinstance(value, (int, float)):
            consensus[f"fy{i}"] = value

    out = {
        "ticker": meta.get("ticker"),
        "date": meta.get("date"),
        "price": _fact_value(fact_idx, "f_price_at_dd"),
        "start": si.get("start") or {},
        "yield_pct": si.get("yield_pct") or {},
        "terminal_label": si.get("terminal_label"),
        "scenarios": {},
    }
    if consensus:
        out["consensus"] = consensus
    basis = si.get("basis") or {}
    for key in ("bull", "base", "bear"):
        node = {
            "eps_path": (si.get("eps") or {}).get(key),
            "terminal_pe": (si.get("pe") or {}).get(key),
            "p": (si.get("p") or {}).get(key),
        }
        if basis.get(key):
            node["basis"] = basis[key]
        out["scenarios"][key] = node
    if si.get("second_stage"):
        out["second_stage"] = si["second_stage"]
    if si.get("endo_ceiling_exceeded") is not None:
        out["endo_ceiling_exceeded"] = si["endo_ceiling_exceeded"]
    peer_max = si.get("peer_max_fpe")
    if peer_max is None:
        peer_max = _fact_value(fact_idx, "f_q5_peer_max_fpe")
    if peer_max is not None:
        out["peer_max_fpe"] = peer_max
    return out


# ---------------------------------------------------------------------------
# normalize：格式正規化（WP-H2-1，2026-09-11；界線擴充於 WP-H2-5，2026-09-11）
#
# 判斷段改成一回合交卷後，剩下的失敗多半是**形狀**而不是判斷（把該包陣列的東
# 西寫成單一物件、沿用 v18 的欄名、路徑寫成相對）。這些由程式修，不要為此再燒
# 一輪模型。
#
# **界線（Codex WP-H2-1 開工前提第 2 條 + WP-H2-5 第一次真跑擴充）**：只准修
# 六類——
#   ①路徑（facts_ref／scenario_ref 相對 → 絕對）
#   ②確定的欄名映射（下表；一對一、無歧義才列）
#   ③單物件包陣列（依 schema 的 v19_contract 宣告，該是陣列卻給了單一物件）
#   ④數字鍵 dict → 陣列（鍵為連續字串「0」「1」…「N-1」的物件，依 schema 宣告
#     的陣列路徑轉正；同時涵蓋「頂層重複欄（v18 習慣殘留）與 counter_evidence
#     正式欄同時存在」的去重——頂層版本回填正式版本缺的鍵（不覆寫既有值）後
#     捨棄，兩邊都填的是同一份判斷值搬錯地方，不是新內容）
#   ⑤確定的 enum 別名對照（下表；只認得出的別名才轉，轉不出或非別名嘗試一律
#     不動、留給 validate 照實報 FAIL——不是「猜一個給它」）
#   ⑥檢查點鍵名改名（`moat.roic_durability.checkpoints[]` 的
#     name/answer/label/light → item/text/level，屬②的巢狀特例，因位置夠深
#     獨立列出）
# **一律不補**：理由、評級、false、門檻、機率，以及任何缺值。修不掉就讓
# validate FAIL，交 patch map（上限 1 輪）或交指揮者，不得用預設值發布。
# ---------------------------------------------------------------------------

SCHEMA_PATH = SCRIPT_DIR / "dd_schema" / "judgment.schema.json"

# ②欄名映射：{父節點路徑: {舊名: 新名}}；父路徑 "" ＝頂層。只列一對一、語意
# 完全相同的改名，任何需要判斷「這兩個是不是同一件事」的都不列。
_RENAME_MAP = {
    "": {
        "scenario": "scenario_inputs",          # v18 另一個檔的名字
        "scenario_input": "scenario_inputs",
        "counterevidence": "counter_evidence",
        "facts_path": "facts_ref",
    },
    "answers": {
        "q1": "q1_business", "q2": "q2_moat", "q3": "q3_growth",
        "q4": "q4_capital", "q5": "q5_valuation", "q6": "q6_how_wrong",
    },
}
# 每個 answers.qX 底下的同款改名（判斷者常沿用 v18 的欄名）。
_ANSWER_RENAME = {"facts": "fact_refs", "refs": "fact_refs", "values": "verdict_values"}
# v18 住頂層、v19 收進 counter_evidence 的四塊（純搬家，內容不動）。
_INTO_COUNTER_EVIDENCE = ("contradictions", "triggers", "kill_metrics", "evidence_dismissed")
# ⑥ §5.R 四檢查點鍵名（validate_judgment.v19_required_items_checks 認
# item/text/not_applicable_reason；level 供渲染燈號）——判斷者常沿用別名。
_CHECKPOINT_RENAME = {"name": "item", "answer": "text", "label": "level", "light": "level"}

# ⑤ triggers[].type：括號註解（如「假設驗證(H1-H3)」）是常見誤寫，H/R 編號本
# 該寫在 maps_to。只在「去括號後」剛好命中 enum 才轉；命中不了就不動、留 FAIL
# （不是每個括號都安全去掉）。
_TRIGGER_TYPE_ENUM = (
    "假設驗證", "風險", "Single Thing", "估值rearm",
    "加碼", "減碼", "清倉", "複審日期",
)
_TRIGGER_TYPE_PAREN_RE = re.compile(r"[（(][^（）()]*[）)]?\s*$")


def _v19_array_paths(schema_node, prefix="", out=None):
    """走 v19_contract schema，蒐集所有宣告為 array 的欄位路徑（`a.b.c`，陣列
    元素以 `[]` 略過不展開）。用來判斷「該是陣列卻給了單一物件／數字鍵物件」。"""
    out = [] if out is None else out
    if not isinstance(schema_node, dict):
        return out
    props = schema_node.get("properties")
    if isinstance(props, dict):
        for k, v in props.items():
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict) and v.get("type") == "array":
                out.append(path)
                items = v.get("items")
                if isinstance(items, dict):
                    _v19_array_paths(items, path, out)
            else:
                _v19_array_paths(v, path, out)
    return out


def _coerce_numeric_dict(d):
    """④ dict 鍵為連續數字字串「0」「1」…「N-1」→依鍵排序的 list；不是這個
    形狀（缺號、不連續、有非數字鍵、空物件）一律回傳 None，交給後續檢查照實
    報 FAIL——不強猜順序。"""
    if not isinstance(d, dict) or not d:
        return None
    keys = list(d.keys())
    if not all(isinstance(kk, str) and kk.isdigit() for kk in keys):
        return None
    n = len(keys)
    if sorted(keys, key=int) != [str(i) for i in range(n)]:
        return None
    return [d[str(i)] for i in range(n)]


def _wrap_singletons(node, prefix, array_paths, changes):
    if not isinstance(node, dict):
        return
    for k in list(node.keys()):
        path = f"{prefix}.{k}" if prefix else k
        v = node[k]
        if path in array_paths and isinstance(v, dict):
            coerced = _coerce_numeric_dict(v)
            if coerced is not None:
                node[k] = coerced
                changes.append(f"數字鍵轉陣列：{path}")
                v = node[k]
            else:
                node[k] = [v]
                changes.append(f"單物件包陣列：{path}")
                v = node[k]
        if isinstance(v, dict):
            _wrap_singletons(v, path, array_paths, changes)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    _wrap_singletons(item, path, array_paths, changes)


def _rename_keys(node, table, changes, label):
    if not isinstance(node, dict):
        return
    for old, new in table.items():
        if old in node and new not in node:
            node[new] = node.pop(old)
            changes.append(f"欄名映射：{label}{old} → {new}")


def _normalize_checkpoints(out, changes):
    """⑥ moat.roic_durability.checkpoints[] 的鍵名改名（純搬家，值不動）。"""
    try:
        cps = out["answers"]["q2_moat"]["verdict_values"]["moat"]["roic_durability"]["checkpoints"]
    except (KeyError, TypeError):
        return
    if not isinstance(cps, list):
        return
    for i, c in enumerate(cps):
        if isinstance(c, dict):
            _rename_keys(
                c, _CHECKPOINT_RENAME, changes,
                f"answers.q2_moat.verdict_values.moat.roic_durability.checkpoints[{i}].",
            )


def _normalize_trigger_types(out, changes):
    """⑤ counter_evidence.triggers[].type 的括號註解去除（H1-H3/R1-R3 屬於
    maps_to，不屬於 type）。"""
    try:
        triggers = out["counter_evidence"]["triggers"]
    except (KeyError, TypeError):
        return
    if not isinstance(triggers, list):
        return
    for i, t in enumerate(triggers):
        if not isinstance(t, dict):
            continue
        v = t.get("type")
        if not isinstance(v, str) or v in _TRIGGER_TYPE_ENUM:
            continue
        stripped = _TRIGGER_TYPE_PAREN_RE.sub("", v).strip()
        if stripped in _TRIGGER_TYPE_ENUM:
            t["type"] = stripped
            changes.append(f"enum別名：counter_evidence.triggers[{i}].type {v!r} → {stripped!r}")




def normalize(raw: dict, judgment_path=None) -> tuple:
    """回傳 (normalized_dict, changes)。非 v19 一律原物件回傳、零變更。"""
    if not is_v19(raw):
        return raw, []
    out = copy.deepcopy(raw)
    changes = []

    # ② 欄名映射
    _rename_keys(out, _RENAME_MAP[""], changes, "")
    answers = out.get("answers")
    if isinstance(answers, dict):
        _rename_keys(answers, _RENAME_MAP["answers"], changes, "answers.")
        for qk, ans in answers.items():
            _rename_keys(ans, _ANSWER_RENAME, changes, f"answers.{qk}.")

    # ⑥ §5.R 四檢查點鍵名
    _normalize_checkpoints(out, changes)

    # ②＋④ 頂層四塊搬進 counter_evidence；兩邊都有時（v18 習慣殘留＋v19 正式
    # 欄並存）先把頂層版本的數字鍵轉陣列，再回填正式版本缺的鍵（不覆寫既有
    # 值），無可回填內容就單純丟棄頂層重複版本。
    ce = out.setdefault("counter_evidence", {}) if any(
        k in out for k in _INTO_COUNTER_EVIDENCE) else out.get("counter_evidence")
    if isinstance(ce, dict):
        for k in _INTO_COUNTER_EVIDENCE:
            if k not in out:
                continue
            root_val = out.pop(k)
            coerced = _coerce_numeric_dict(root_val)
            if coerced is not None:
                changes.append(f"數字鍵轉陣列：頂層 {k}（{len(coerced)} 項）")
                root_val = coerced
            if k not in ce:
                ce[k] = root_val
                changes.append(f"欄名映射：{k} → counter_evidence.{k}")
                continue
            existing = ce.get(k)
            filled = 0
            if isinstance(existing, list) and isinstance(root_val, list):
                for i, item in enumerate(root_val):
                    if i >= len(existing):
                        break
                    tgt = existing[i]
                    if isinstance(tgt, dict) and isinstance(item, dict):
                        for fk, fv in item.items():
                            cur = tgt.get(fk)
                            if (cur is None or cur == "") and fv not in (None, ""):
                                tgt[fk] = fv
                                filled += 1
            if filled:
                changes.append(
                    f"去重回填：頂層重複 {k}（與 counter_evidence.{k} 同時存在）"
                    f"回填 {filled} 個欄位後移除頂層版本"
                )
            else:
                changes.append(f"移除頂層重複欄位：{k}（counter_evidence 已有版本，頂層版本無可回填內容）")

    # ③＋④ 單物件包陣列／數字鍵轉陣列（依 schema 宣告，不自己列清單）
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        array_paths = set(_v19_array_paths(schema.get("v19_contract") or {}))
    except (OSError, json.JSONDecodeError, ValueError):
        array_paths = set()
    if array_paths:
        _wrap_singletons(out, "", array_paths, changes)

    # 2026-09-11：僅清除觸發器 type 的括號註解，不改事件分類。
    _normalize_trigger_types(out, changes)
    # 2026-09-11：分類由判斷者填合法 enum，格式整理不得猜分類或改成 other。

    # ① 路徑：相對 → 絕對（找不到檔就不動，讓 validate 照實報缺）
    base = Path(judgment_path).parent if judgment_path else None
    for key in ("facts_ref", "scenario_ref"):
        ref = out.get(key)
        if not isinstance(ref, str) or not ref or Path(ref).is_absolute():
            continue
        for cand in ([ROOT / ref] + ([base / ref] if base else [])):
            if cand.exists():
                out[key] = str(cand.resolve())
                changes.append(f"路徑：{key} → 絕對路徑")
                break

    if changes:
        out.setdefault("normalize_log", []).extend(changes)
    return out, changes


def cmd_normalize(args) -> int:
    path = Path(args.judgment)
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not is_v19(raw):
        print("[skip] 非 v19 形狀，正規化不適用", file=sys.stderr)
        return 0
    out, changes = normalize(raw, path)
    for c in changes:
        print(f"  · {c}")
    print("正規化 {0} 項{1}".format(len(changes), "（未寫檔，加 --write 才落地）" if not args.write else ""))
    if args.write and changes:
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


def cmd_scenario(args) -> int:
    raw = json.loads(Path(args.judgment).read_text(encoding="utf-8"))
    if not is_v19(raw):
        print("scenario 只對 v19 判斷檔有意義（舊形狀的 scenario.json 是獨立輸入檔）",
              file=sys.stderr)
        return 2
    facts = load_facts(raw, args.judgment, args.facts)
    payload = scenario_input_from_v19(raw, facts)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"寫入 {args.out}")
    else:
        sys.stdout.write(text)
    return 0


def cmd_view(args) -> int:
    raw, view = load_view(args.judgment, args.facts,
                          json.loads(Path(args.scenario_meta).read_text(encoding="utf-8"))
                          if args.scenario_meta else None)
    if not is_v19(raw):
        print("[skip] 非 v19 形狀（meta.contract 未標 v19），視圖＝原檔", file=sys.stderr)
    text = json.dumps(view, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"寫入 {args.out}（{len(text.encode('utf-8'))} bytes）")
    else:
        sys.stdout.write(text)
    return 0


def cmd_prose_stub(args) -> int:
    raw, view = load_view(args.judgment, args.facts, None)
    if not is_v19(raw):
        print("prose-stub 只對 v19 判斷檔有意義（舊形狀的散文由散文 agent 寫）", file=sys.stderr)
        return 2
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for sid, html_text in prose_stub(raw, view).items():
        (out_dir / f"{sid}.html").write_text(html_text, encoding="utf-8")
        written.append(sid)
    print("寫入 {0}：{1}（revlog／s14／appA 由 gen_dd_tables.py 機械生成）".format(
        out_dir, "、".join(written)))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_view = sub.add_parser("view", help="輸出舊形狀判斷視圖")
    p_view.add_argument("judgment")
    p_view.add_argument("--facts", help="facts.json 路徑（預設讀 judgment.facts_ref）")
    p_view.add_argument("--scenario-meta", help="scenario_meta.json 路徑（目前不參與投影）")
    p_view.add_argument("--out", help="輸出路徑；不給就印到 stdout")
    p_view.set_defaults(func=cmd_view)

    p_sc = sub.add_parser("scenario", help="由 scenario_inputs 產 dd_scenario.py 的輸入檔（v19 專用）")
    p_sc.add_argument("judgment")
    p_sc.add_argument("--facts")
    p_sc.add_argument("--out", help="輸出 scenario.json 路徑；不給就印到 stdout")
    p_sc.set_defaults(func=cmd_scenario)

    p_nm = sub.add_parser("normalize", help="格式正規化（只修路徑／欄名映射／單物件包陣列，不補判斷值）")
    p_nm.add_argument("judgment")
    p_nm.add_argument("--write", action="store_true", help="就地寫回；不給只印會改什麼")
    p_nm.set_defaults(func=cmd_normalize)

    p_stub = sub.add_parser("prose-stub", help="產完整版散文段的機械骨架（v19 專用）")
    p_stub.add_argument("judgment")
    p_stub.add_argument("--facts")
    p_stub.add_argument("--out", required=True, help="prose/ 目錄")
    p_stub.set_defaults(func=cmd_prose_stub)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
