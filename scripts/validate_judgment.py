#!/usr/bin/env python3
"""validate_judgment.py — WP1c validator for stock-analyst v16 judgment.json.

Two layers:
  1. Generic JSON-Schema-subset structural check against
     scripts/dd_schema/judgment.schema.json (supports: type / required /
     properties / items / enum / pattern / minItems / minLength / maxLength
     only — NOT a full draft-07 implementation; good enough for this file's
     needs and avoids a jsonschema dependency, per WP1c stdlib-only rule).
  2. Cross-field rules that a plain schema can't express (see design spec
     _v16_design_spec_20260903.md §3.2 + §4 validate_judgment.py row):
       - every thesis.R[].h_ref token resolves to an existing thesis.H[].id
       - every triggers[].maps_to H*/R* token resolves to an existing H/R id
       - triggers[].type is one of the E12 type enum (SKILL.md §13 E12)
       - triggers[].action is non-empty (soft: WARN, not FAIL, if it doesn't
         contain one of the E12 action-enum stems — the three round-trip
         reference DDs (SNOW/DELL/AVGO 2026-09-03) show real action prose
         regularly diverges from the strict verb list, so this is enforced
         as a quality signal, not a hard gate)
       - at least one triggers[] row carries a non-empty `date` (the §14
         review-date row)
       - decision_inputs carries all 22 keys (schema `required` already
         enforces this; value may be null)
       - moat.trend is a single arrow (schema enum already enforces this)
       - scenario_ref, when it resolves to an existing file, is cross-checked
         via dd_scenario.check_meta() (reuses the existing, already-tested
         scenario arithmetic instead of re-deriving it here)
  3. Machine-language / CJK-punctuation leak scan (WP1c 修法3): every string
     leaf is checked against dd_sections.LEAK_PATTERNS and qc.CJK_PUNCT_RE;
     any hit is a FAIL with its JSON path + snippet. Exempt:
     decision_out.audit_rows[] (whole subtree), decision_out.row_hit /
     decision_out.pacing[] (dd_decision.py 機械寫入的矩陣語言，同一豁免理由)
     and the "（QC-\\d+）" citation inside reasoning.* strings only.
  4. Drift-vs-prior attribution check (--evidence, 選配): every drift_watch
     field (evidence.prior_dd.drift_watch, 20 欄) that differs between
     evidence.prior_dd.prior_meta and this judgment's current dd-meta value
     (via gen_dd_tables.build_dd_meta — the single judgment→dd-meta mapping,
     reused not re-derived) must have a corresponding entry in
     judgment.contradictions[] (see _v16_design_spec §5.5 / drift_check_spec.md).
     2026-09-10（A4 規則精簡）：條目可用 `cause`（價格變動／新證據／方法變動）
     歸因多個欄位，`prior_field` 因此接受欄名陣列——規則從「每個變動欄必須有
     獨立條目」放寬成「每個變動欄必須映射到一個原因條目」，逐欄記帳不變。
  5. J1 負向證據可追溯（--evidence 給定才啟用，WP2 2026-09-05）: evidence
     coverage／events 內每條 direction=="-" 的 finding（無 id 時以
     {axis}#{index} 現算）須出現在 judgment 任一 evidence_refs 陣列
     （contradictions[]／moat.threats[]／premortem.blind_spots[]／
     triggers[]／thesis.R[]）或頂層 evidence_dismissed[].ref，否則 FAIL；
     `--j1-warn` 可降為 WARN（校準用）。
  6. J2 判斷層恆等式（WP2）: verify_dd_math.py 檢查 A/B/E 中只需
     judgment.json + 同目錄 scenario_meta.json（由 scenario_ref 推）即可算
     的子集——Max DD 下限 vs Bear 終點跌幅、decision_inputs.irr_base_pct／
     ev5y_pct 對 scenario_meta、情境樹年期、Bull EPS 對 Base 的退化、
     scenario_meta.valuation_dependent 與 decision_inputs 同名欄一致性；
     容差沿用 verify_dd_math.py 原腳本常數，恆常執行（不需 --evidence）。
  7. J3 `--fix`（WP2）: 自動修正 scenario_ref 相對路徑→絕對路徑、字串內半形
     標點轉全形；scenario_meta.valuation_dependent 與 decision_inputs 不一致
     不自動修，仍由 J2 列 FAIL。
  8. J4 plain 完整性（WARN，WP5a 2026-09-05；2026-09-10 A3 收斂）: 頂層選填
     `plain`（白話區塊）只對**dd_brief 真的渲染、且無法從別處機械導出**的子欄
     位列 WARN——`verdict_line`／`verdict_sub`／`market_wrong`／`how_to_lose`／
     `bets`／`fears`／`change_my_mind`／`business.moat_direction` 都有機械
     fallback（decision_out／oneliner／valuation.targets／premortem／thesis.H／
     thesis.R／triggers／moat），缺了頁面自動退回結構欄位並標 `class="fallback"`，
     不再逐欄催稿；三個陣列的「長度必須是 3」配額同時撤除。另檢查 plain 內數字
     ⊆ judgment 其他欄位數字集合為 WARN。`plain` 內字串仍照常走
     leak_and_punct_checks（FAIL）。
  9. 條件式展開區塊完整性（FAIL，WP-E 2026-09-10，修 WP-D 契約接線洞 #2）:
     generic schema_validate 不支援 oneOf，B1–B4 四個條件式展開區塊
     （industry.tam_table／growth.segments／governance.capital_returns／
     valuation.peers）以 object 形態出現時，schema 層放不住「必須是合法未展開
     標記」——`expandable_block_checks()` 另開專用檢查：object 必須
     `expanded is False` 且 `reason` 為去空白後非空字串，否則 FAIL。
  10. 反證唯一來源完整性（FAIL，WP-E 2026-09-10，修契約接線洞 #3）: A1 撤掉
      premortem.failure_story／second_failure 必填後，新格式的反證唯一來源
      （blind_spots[] 依 view 分組）沒有機械契約接住「三視角全空」——
      `premortem_counterevidence_checks()` 對新格式檔（任一 blind_spots 帶
      view 的 object，或缺 failure_story／second_failure）要求三視角
      （論點失敗／論點成功但股東經濟變差／價格已反映太多）各至少一條有非空
      evidence 或 assumption，或該條有非空 not_applicable_reason（合法「不
      適用」出口）。舊格式（有 failure_story 且 blind_spots 為純字串）不受
      影響。
  11. J6 行動門檻變動必須有理由（FAIL，--evidence 給定才啟用，WP-G
      2026-09-11）: `triggers[].type ∈ {"Single Thing", "清倉"}`（判斷規則
      明訂的「唯一居所」型別）前份與本次各剛好一列時，門檻文字（正規化後）
      不同卻在 `contradictions[]` 找不到 `cause∈{新證據,方法變動}`、
      `side_a≠side_b`、且提及該型別字樣的對應條目 → FAIL；非 1:1（0 或
      ≥2 列）比不出來只 WARN，不猜。見 `threshold_drift_checks()`。
  12. trap_analysis.evidence_for／evidence_against 反向引用提醒（WARN，
      WP-G 2026-09-11）: 新格式檔（反證唯一居所＝premortem.blind_spots[]）
      仍手填這兩欄時 WARN，提醒改引用反證紀錄——語意方向是否正確不做機械
      判斷。見 `trap_analysis_redundancy_checks()`。
  13. val_denominator_note 完整性（FAIL，WP-G 2026-09-11）: 新格式檔
      `decision_inputs.val_denominator_disputed` 存在（true 或 false）而
      `val_denominator_note` 缺或空 → FAIL；理由內容是否充分不做語意審。見
      `val_denominator_note_checks()`。

  14. v19 契約（FAIL／WARN，WP-H1 2026-09-11）: 判斷檔帶 `meta.contract`＝
      `"v19"` 時，先用 schema 的 `v19_contract` 區塊驗 judge-owned 形狀，再由
      `dd_project.project()` 投影成舊形狀視圖，**上列 1–13 全部改讀視圖**
      （檢查語義不變，不是新開一套）。v19 專屬檢查（WP-H2-1 2026-09-11 補上
      Codex 點名的兩個漏擋）：
        (a) **事實檔擋門**——`facts_ref` 解析不到／不是合法 JSON／事實檔自身過
            不了 `dd_facts.check` 一律 FAIL（H1 時期只 WARN，fixture 實測「事實
            檔不存在仍 0 FAIL」）；
        (b) `fact_refs[]` 的 id 必須在 `facts.json` 找得到（斷鏈＝FAIL）；
        (c) 由程式投影的 13 個 `decision_inputs` 機械欄不得被判斷者填成非 null；
        (d) **必要項目是否有回答**（`v19_required_items_checks`，取代 schema 的
            `minItems`）——§5.R 四檢查點各要一句判讀或一句不適用理由、同業對照
            要嘛每家一句 `strategy_note` 要嘛寫 `moat.peer_na_reason`，空物件與
            空陣列不算回答；
        (e) **J2 必須真的執行**——`scenario_meta` sidecar 找不到、或 Max DD 恆等
            式因缺輸入而沒算，一律 FAIL（舊形狀維持 WARN）；
        (f) J2 的終端年檢查升 FAIL（終端年＝判斷日起第 5 個完整會計年度，
            `base_eps_path`＝共識三年錨，見 `dd_schema/decision_inputs.md`）。
      **舊形狀（無 `meta.contract`）完全不走這條路**，驗法與輸出逐字不變。

Usage:
  python3 scripts/validate_judgment.py FILE.json [--report] [--evidence EVIDENCE.json]
                                        [--facts FACTS.json] [--j1-warn] [--fix]

Exit 0 = no FAIL-level issues (or --report). Exit 1 otherwise.
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = Path(__file__).resolve().parent / "dd_schema" / "judgment.schema.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import dd_scenario  # noqa: E402
except Exception:  # pragma: no cover - defensive; scenario cross-check just skips
    dd_scenario = None

# WP1c 修法3：判斷層就攔機器語言與半形標點——重用既有詞表/regex，不複製。
import dd_sections  # noqa: E402 — LEAK_PATTERNS（QC-40 詞表，單一權威）
import qc  # noqa: E402 — CJK_PUNCT_RE（半形標點規則，單一權威）
# layer 4（漂移歸因）：current 側 judgment→dd-meta 映射單一權威，import 重用。
import gen_dd_tables  # noqa: E402
# v19（WP-H1）：新契約 → 舊形狀視圖的單一程式轉接；舊形狀 project() 是 identity，
# 故本檔對既有判斷檔的行為完全不變。
import dd_project  # noqa: E402


# ---------------------------------------------------------------------------
# layer 1: generic JSON-Schema subset interpreter
# ---------------------------------------------------------------------------

_TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


def _check_type(value, type_name: str) -> bool:
    if type_name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    py_t = _TYPE_MAP.get(type_name)
    if py_t is None:
        return True  # unknown type keyword — don't block
    if type_name == "boolean":
        return isinstance(value, bool)
    return isinstance(value, py_t)


def schema_validate(instance, schema, path="$") -> list:
    """Return a list of error strings. Empty = valid at this node."""
    errs = []

    if "type" in schema:
        types = schema["type"]
        types = types if isinstance(types, list) else [types]
        if not any(_check_type(instance, t) for t in types):
            errs.append(f"{path}: expected type {types}, got {type(instance).__name__} ({instance!r})")
            return errs  # further checks would be noise once type is wrong

    if "enum" in schema:
        allowed = schema["enum"]
        if instance not in allowed:
            errs.append(f"{path}: value {instance!r} not in enum {allowed!r}")

    if isinstance(instance, str):
        if "pattern" in schema and not re.match(schema["pattern"], instance):
            errs.append(f"{path}: {instance!r} does not match pattern {schema['pattern']!r}")
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errs.append(f"{path}: length {len(instance)} < minLength {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errs.append(f"{path}: length {len(instance)} > maxLength {schema['maxLength']}")

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errs.append(f"{path}: missing required key {req!r}")
        props = schema.get("properties", {})
        for k, v in instance.items():
            if k in props:
                errs.extend(schema_validate(v, props[k], f"{path}.{k}"))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errs.append(f"{path}: {len(instance)} items < minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(instance):
                errs.extend(schema_validate(item, item_schema, f"{path}[{i}]"))

    return errs


# ---------------------------------------------------------------------------
# layer 2: cross-field rules
# ---------------------------------------------------------------------------

E12_TYPE_ENUM = {"假設驗證", "風險", "Single Thing", "估值rearm", "加碼", "減碼", "清倉", "複審日期"}
E12_ACTION_STEMS = ("加碼至", "減碼至", "清倉", "重跑DD", "進場首倉", "維持觀望", "trim回目標倉位", "trim")
_ID_TOKEN_RE = re.compile(r"[HR]\d+")


def _strip_parenthetical(s: str) -> str:
    return re.sub(r"[（(].*?[）)]", "", s or "").strip()


# ---------------------------------------------------------------------------
# scenario_ref 路徑解析（WP-G 2026-09-11 修，Codex 第三輪複審 A 項）：原本
# 相對路徑一律直接接在 judgment 所在目錄後面——v17/v18 run 目錄慣例把
# scenario_ref 寫成相對 repo root 的路徑（如 `.dd_build/runs/TXN_20260910/
# scenario.json`，本身已含 run 目錄名），與 judgment_path.parent 相接會拼出
# 重複目錄、檔案必然不存在，J2／scenario_ref 交叉檢查因此全數「略過」而非
# 真的跑過。改法：絕對路徑直接用；相對路徑先以 repo root 解析，再以 judgment
# 所在目錄解析（相容 `notes/site-internal/dd/_src` 底下少數把 scenario_ref
# 寫成相對 judgment 檔自身位置的既有存查）；兩處都不存在才回傳 None，呼叫端
# 自行印出清楚的略過訊息。單一權威，cross_field_checks／_load_scenario_meta_
# for_j2／apply_fixes 三處共用。
# ---------------------------------------------------------------------------

def _resolve_scenario_ref_path(ref: str, judgment_path: Path) -> Path | None:
    p = Path(ref)
    if p.is_absolute():
        return p if p.exists() else None
    root_candidate = ROOT / p
    if root_candidate.exists():
        return root_candidate
    dir_candidate = judgment_path.parent / p
    if dir_candidate.exists():
        return dir_candidate
    return None


def cross_field_checks(data: dict, judgment_path: Path) -> tuple[list, list]:
    fails, warns = [], []

    thesis = data.get("thesis") or {}
    H = thesis.get("H") or []
    R = thesis.get("R") or []
    h_ids = {h.get("id") for h in H if isinstance(h, dict)}
    r_ids = {r.get("id") for r in R if isinstance(r, dict)}

    # R[].h_ref tokens must resolve to existing H ids
    for r in R:
        if not isinstance(r, dict):
            continue
        h_ref = r.get("h_ref") or ""
        tokens = _ID_TOKEN_RE.findall(h_ref)
        if not tokens:
            warns.append(f"thesis.R[{r.get('id')}].h_ref 找不到任何 H* token（{h_ref!r}）")
            continue
        for tok in tokens:
            if tok.startswith("H") and tok not in h_ids:
                fails.append(f"thesis.R[{r.get('id')}].h_ref 引用不存在的 {tok}（H ids={sorted(h_ids)}）")

    # triggers[]: type enum, maps_to H*/R* resolution, action soft-check, date>=1
    triggers = data.get("triggers") or []
    any_date = False
    for i, t in enumerate(triggers):
        if not isinstance(t, dict):
            continue
        raw_type = t.get("type") or ""
        norm_type = _strip_parenthetical(raw_type)
        if norm_type not in E12_TYPE_ENUM:
            fails.append(f"triggers[{i}].type {raw_type!r}（正規化為 {norm_type!r}）不在 E12 enum {sorted(E12_TYPE_ENUM)}")

        maps_to = t.get("maps_to") or ""
        for tok in _ID_TOKEN_RE.findall(maps_to):
            if tok.startswith("H") and tok not in h_ids:
                fails.append(f"triggers[{i}].maps_to 引用不存在的 {tok}（{maps_to!r}）")
            if tok.startswith("R") and tok not in r_ids:
                fails.append(f"triggers[{i}].maps_to 引用不存在的 {tok}（{maps_to!r}）")

        action = t.get("action") or ""
        if not action.strip():
            fails.append(f"triggers[{i}].action 為空")
        elif not any(stem in action for stem in E12_ACTION_STEMS):
            warns.append(
                f"triggers[{i}].action {action!r} 不含 E12 動作詞幹 {E12_ACTION_STEMS}"
                f"（soft，real-world 觸發器文字常改寫，不擋）"
            )

        date_v = (t.get("date") or "").strip()
        if date_v:
            any_date = True

    if triggers and not any_date:
        fails.append("triggers[] 中沒有任何一列填 date（至少須有 1 列複審日期，§14）")

    # decision_inputs completeness (schema `required` already covers presence;
    # this re-states the rule explicitly per WP1c brief so a schema edit that
    # accidentally drops a key still gets caught with a clear message).
    required_di_keys = [
        "signal", "trap", "val", "ma", "runway_post_y5", "moat_trend", "moat",
        "capalloc_grade", "archetype", "cycle_position", "cycle_verdict",
        "asym_ratio", "irr_base_pct", "ev5y_pct", "price_at_dd",
        "thesis_irreconcilable", "valuation_dependent", "market_wrong_reason_given",
        "week26_return_pct", "momentum_overheated", "cycle_gates_pass",
        "consensus_rev_3m_pct",
    ]
    di = data.get("decision_inputs") or {}
    missing_di = [k for k in required_di_keys if k not in di]
    if missing_di:
        fails.append(f"decision_inputs 缺欄（值可 null 但 key 必須存在）：{missing_di}")

    # moat.trend single-arrow (schema enum already restricts to ↑/→/↓/null;
    # this catches an accidental multi-char string like "↑↑" or "up" that
    # would otherwise slip through if the schema enum were ever loosened).
    trend = (data.get("moat") or {}).get("trend")
    if trend is not None and (not isinstance(trend, str) or len(trend) != 1 or trend not in "↑→↓"):
        fails.append(f"moat.trend 必須是單一箭頭 ↑/→/↓，得到 {trend!r}")

    # scenario_ref cross-check (reuse dd_scenario.check_meta on the referenced
    # scenario-meta artifact; resolved relative to the judgment.json file).
    scenario_ref = data.get("scenario_ref")
    if scenario_ref:
        ref_path = _resolve_scenario_ref_path(scenario_ref, judgment_path)
        if ref_path is None:
            warns.append(
                f"scenario_ref {scenario_ref!r} 找不到（試過絕對路徑／repo root／"
                f"judgment 所在目錄），略過交叉檢查"
            )
        elif dd_scenario is None:
            warns.append("dd_scenario 模組載入失敗，略過 scenario_ref 交叉檢查")
        else:
            try:
                sref = json.loads(ref_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                fails.append(f"scenario_ref {ref_path}: JSON parse error: {e}")
                sref = None
            if sref is not None:
                merged = dict(sref)
                merged.setdefault("price_at_dd", di.get("price_at_dd"))
                s_fails, s_warns = dd_scenario.check_meta(merged)
                fails.extend(f"scenario_ref 交叉檢查：{f}" for f in s_fails)
                warns.extend(f"scenario_ref 交叉檢查：{w}" for w in s_warns)
                # decision_inputs 三欄 vs scenario 產物三欄的容忍對帳
                for di_key, sref_key, tol in (
                    ("asym_ratio", "asym_ratio", 0.06),
                    ("irr_base_pct", "irr_base_pct", 1.0),
                    ("ev5y_pct", "ev5y_pct", 1.0),
                ):
                    di_v = di.get(di_key)
                    sref_v = sref.get(sref_key)
                    if di_v is None or sref_v is None:
                        continue
                    if abs(di_v - sref_v) > tol:
                        fails.append(
                            f"decision_inputs.{di_key}={di_v} 與 scenario_ref.{sref_key}={sref_v} "
                            f"對不上（容忍 {tol}）"
                        )

    return fails, warns


# ---------------------------------------------------------------------------
# 同源欄位 equality 檢查（P2-1，2026-09-07 新增）
#
# scripts/dd_schema/judgment-to-ddmeta.md 宣告多組「＝同源」的 judgment.json
# 欄位 pair（agent 被要求兩處填同一個值；dd-meta 渲染／矩陣讀取只取其中一
# 側，另一側純粹是重複填寫成本，且若兩處填不同值，最終呈現由 renderer 的
# 任意取邊決定，agent 不會被攔下）。這裡只驗證 mapping 文件裡「真正同義」
# 的 pair——`fpe_fy2`／`peg_fy2` 不在此列：複審實測 18 份 2026-09 存查中兩
# 者分別有 10／8 份不同（AVGO 明確區分 FY26/FY27 兩個財年），mapping 文件
# 寫的「appendix_a.fpe_fy2＝valuation.fwd_pe」在財年口徑未定義前不成立，不
# 得比對，見 judgment-to-ddmeta.md 相關兩行附註。兩側都有值（非 null）才
# 比；任一側缺值（schema 允許 null）不視為不一致。
# ---------------------------------------------------------------------------

SAME_SOURCE_PAIRS = [
    ("signal", "decision_inputs.signal", "appendix_a.signal"),
    ("trap", "decision_inputs.trap", "trap_analysis.verdict"),
    ("moat", "decision_inputs.moat", "moat.grade"),
    ("val", "decision_inputs.val", "appendix_a.val"),
    ("ma", "decision_inputs.ma", "appendix_a.ma"),
    ("moat_trend", "decision_inputs.moat_trend", "moat.trend"),
    ("runway_post_y5", "decision_inputs.runway_post_y5", "growth.runway_post_y5"),
    ("capalloc_grade", "decision_inputs.capalloc_grade", "governance.capalloc_grade"),
    ("archetype", "decision_inputs.archetype", "archetype.primary"),
    ("pct_5y", "appendix_a.pct_5y", "valuation.percentile_5y"),
    ("upside_short_pct", "appendix_a.upside_short_pct", "valuation.upside_short_pct"),
    ("upside_mid_pct", "appendix_a.upside_mid_pct", "valuation.upside_mid_pct"),
    ("moat_score", "moat.score", "appendix_a.moat_score"),
]


def _get_path(d, path):
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _same_source_equal(v1, v2) -> bool:
    if (
        isinstance(v1, (int, float)) and isinstance(v2, (int, float))
        and not isinstance(v1, bool) and not isinstance(v2, bool)
    ):
        return abs(v1 - v2) < 1e-9
    return v1 == v2


def same_source_pair_checks(data: dict) -> list:
    fails = []
    for name, path1, path2 in SAME_SOURCE_PAIRS:
        v1, v2 = _get_path(data, path1), _get_path(data, path2)
        if v1 is None or v2 is None:
            continue
        if not _same_source_equal(v1, v2):
            fails.append(
                f"同源欄位不一致（{name}）：{path1}={v1!r} 與 {path2}={v2!r}"
                f"（judgment-to-ddmeta.md 宣告同源，須同值）"
            )
    return fails


# ---------------------------------------------------------------------------
# J2: judgment-layer copy of verify_dd_math.py 檢查 A/B/E 的可算子集（WP2
# 2026-09-05）——只需 judgment.json ＋ 同目錄 scenario_meta.json（由
# scenario_ref 推），不需渲染後 HTML，故不能直接 import verify_dd_math（其
# check_file 讀 dd-meta script tag）。容差沿用該腳本常數，邏輯照抄不改判定。
# ---------------------------------------------------------------------------

J2_MAXDD_TOL = 2.0    # pp，同 verify_dd_math.MAXDD_TOL
J2_EV_TOL = 1.5       # pp，同 verify_dd_math.EV_TOL
J2_IRR_TOL = 1.0      # pp，同 verify_dd_math.IRR_TOL
J2_YEAR_WARN_TOL = 1  # 年，同 verify_dd_math 檢查 B 的終端年寬容度
_FY_YEAR_RE = re.compile(r"FY\s*(\d{4})")


def _extract_fy_year(s) -> int | None:
    if not isinstance(s, str):
        return None
    m = _FY_YEAR_RE.search(s)
    return int(m.group(1)) if m else None


def _load_scenario_meta_for_j2(data: dict, judgment_path: Path):
    """回傳 (scenario_meta_dict_or_None, warn_msg_or_None)。

    WP-G 修（2026-09-11，Codex 第三輪複審 A 項）：J2 檢查用到的欄位
    （bear_5y_price／irr_base_pct／ev5y_pct／scenario_tree 及其巢狀
    valuation_dependent）活在 dd_scenario.py 的輸出 sidecar
    `scenario_meta.json`，不在 `scenario_ref` 指向的 `scenario.json`——後者
    是 dd_scenario.py 的輸入檔，只有 EPS 路徑／終端倍數／機率等原始假設，
    沒有算出來的六個情境欄。舊版直接把 scenario_ref 指向的檔案當 sref
    用，這裡的檢查因此全數靜默 no-op（`sref.get("bear_5y_price")` 等一律
    None）。改法：先用 `_resolve_scenario_ref_path` 確認 scenario_ref 本身
    可解析（給出清楚的略過訊息），再用既有的
    `dd_delta._sibling_scenario_meta`（archive 命名
    `{stem}.scenario_meta.json` 或 in-flight run 目錄同層裸檔名
    `scenario_meta.json`，單一權威不重寫）找同目錄的 sidecar 供 J2 實際
    檢查；sidecar 找不到才略過（scenario_ref 本身存在與否只影響訊息用字，
    不影響 sidecar 尋找——兩者是獨立慣例）。"""
    scenario_ref = data.get("scenario_ref")
    if not scenario_ref:
        return None, "scenario_ref 未填，J2 判斷層恆等式略過"
    ref_path = _resolve_scenario_ref_path(scenario_ref, judgment_path)
    if ref_path is None:
        return None, (
            f"scenario_ref {scenario_ref!r} 找不到（試過絕對路徑／repo root／"
            f"judgment 所在目錄），J2 略過"
        )
    try:
        import dd_delta  # 延遲載入避免循環 import（dd_delta 頂層 import 本檔）
    except Exception as e:  # pragma: no cover - defensive
        return None, f"dd_delta 模組載入失敗（{e}），J2 略過"
    sidecar = dd_delta._sibling_scenario_meta(judgment_path)
    if sidecar is None:
        return None, (
            f"scenario_ref {ref_path} 存在，但找不到 scenario_meta.json sidecar"
            f"（dd_delta._sibling_scenario_meta 兩種慣例皆未命中），J2 略過"
        )
    try:
        return json.loads(sidecar.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"scenario_meta sidecar {sidecar}: JSON parse error: {e}"


def j2_math_checks(data: dict, judgment_path: Path,
                   strict_terminal_year: bool = False,
                   require_executed: bool = False) -> tuple[list, list]:
    """WP2 J2 — 判斷層恆等式：Max DD 下限 vs Bear 終點跌幅、
    decision_inputs.irr_base_pct／ev5y_pct 對 scenario_meta、情境樹年期、
    Bull EPS 對 Base 的退化、scenario_meta.valuation_dependent 與
    decision_inputs 同名欄一致性。恆常執行（不需 --evidence）。

    `require_executed`（WP-H2-1，2026-09-11；Codex 複審點名的第二個漏擋）：
    v19 正式流程下，「scenario_meta 找不到」與「Max DD 恆等式沒有輸入所以沒算」
    都從 WARN 升為 FAIL。原本兩者皆只 WARN——資料缺失時 J2 靜默略過，看起來
    像通過。舊形狀維持 WARN（既有慣例不回頭改）。"""
    fails, warns = [], []
    sref, warn = _load_scenario_meta_for_j2(data, judgment_path)
    if sref is None:
        if warn:
            (fails if require_executed else warns).append(f"J2｜{warn}")
        if require_executed:
            fails.append(
                "J2｜v19 契約要求情境結果完整且 J2 確實執行——scenario_meta 不可解析時"
                "不得放行組頁（先跑 `ddreport.py judge check`，dd_scenario.py 會產出 sidecar）"
            )
        return fails, warns

    di = data.get("decision_inputs") or {}
    price = di.get("price_at_dd")

    # Max DD 下限 ≥ Bear 終點跌幅（verify_dd_math 檢查 A 的 Max DD 恆等式）
    bear_p = sref.get("bear_5y_price")
    mdd = ((data.get("premortem") or {}).get("max_dd") or {}).get("lo")
    if price is not None and bear_p is not None and mdd is not None and price > 0:
        bear_ret = (bear_p / price - 1) * 100
        if abs(mdd) + J2_MAXDD_TOL < abs(bear_ret):
            fails.append(
                f"J2｜Max DD 恆等式違反：premortem.max_dd.lo={mdd} 但 Bear 終點跌幅"
                f"={bear_ret:.1f}%（price_at_dd={price}／scenario_meta.bear_5y_price="
                f"{bear_p}）——路徑最大回撤不可能小於任一情境終點跌幅"
            )
    else:
        msg = "J2｜缺 price_at_dd／bear_5y_price／premortem.max_dd.lo 任一，Max DD 恆等式略過"
        # v19：「沒算」與「算過通過」不可同樣算過關（WP-H2-1）。
        (fails if require_executed else warns).append(msg)

    # decision_inputs.irr_base_pct／ev5y_pct 對 scenario_meta
    for key, tol in (("irr_base_pct", J2_IRR_TOL), ("ev5y_pct", J2_EV_TOL)):
        di_v, sref_v = di.get(key), sref.get(key)
        if di_v is None or sref_v is None:
            continue
        if abs(di_v - sref_v) > tol:
            fails.append(
                f"J2｜decision_inputs.{key}={di_v} 與 scenario_meta.{key}={sref_v} 對不上"
                f"（容忍 {tol}pp）"
            )

    # 情境樹年期：scenario_meta 終端年 vs eps_meta.base_eps_path 終端年。
    # WP-G（2026-09-11）：查過 dd_scenario.py／dd_schema/decision_inputs.md／
    # verify_dd_math.py 三處，皆未定義 base_eps_path 是否必須延伸到情境樹終
    # 端年——base_eps_path 的既有消費端（snapshot_consensus.py／
    # build_variance_tracker.py／build_catalyst_page.py）用途是財報季 EPS
    # 承保比對，只需覆蓋近期財年，不天然要求延伸到 Y5 終端年。語料實測（34
    # 份現行 judgment.json）：30+ 份延伸到終端年，僅 TXN（三份存查皆同）與
    # AVGO 維持三年錨且新舊版一致——非本輪新退化，是既有慣例分歧。契約未
    # 明文前只 WARN 供人工複核，不 FAIL，避免把「未寫死的既有差異」錯判成
    # 本次退步（與報告年+5 差 >1 年的既有寬容同精神，同 verify_dd_math 檢查
    # B）。
    scenario_tree = sref.get("scenario_tree") or {}
    term_year = _extract_fy_year(scenario_tree.get("terminal_label"))
    eps_path = (data.get("eps_meta") or {}).get("base_eps_path") or {}
    eps_years = [y for y in (_extract_fy_year(k) for k in eps_path) if y is not None]
    if term_year and eps_years:
        max_eps_year = max(eps_years)
        if strict_terminal_year:
            # v19 契約（decision_inputs.md「終端年與 base_eps_path」節）：
            # base_eps_path＝共識三年錨，本來就短於終端年，短不算問題；只有
            # 「路徑伸得比終端年還遠」才是口徑不一致。
            if max_eps_year > term_year:
                fails.append(
                    f"J2｜base_eps_path 終端年 FY{max_eps_year} 超過情境樹終端年 "
                    f"FY{term_year}——v19 契約規定 base_eps_path 是共識三年錨，不得伸過終端年"
                )
        elif max_eps_year != term_year:
            warns.append(
                f"J2｜情境樹年期提示：scenario_meta.scenario_tree.terminal_label 宣告 "
                f"FY{term_year}，但 eps_meta.base_eps_path 終端年是 FY{max_eps_year}"
                f"——base_eps_path 年期契約未明文（三年錨或完整路徑皆有既有先例），"
                f"僅供人工複核，不擋"
            )
    dd_date = (data.get("meta") or {}).get("date") or ""
    if term_year and re.match(r"^\d{4}", dd_date):
        dd_year = int(dd_date[:4])
        if abs(term_year - (dd_year + 5)) > J2_YEAR_WARN_TOL:
            msg = (
                f"J2｜終端年 FY{term_year} 與報告年+5（{dd_year + 5}）差 "
                f">{J2_YEAR_WARN_TOL} 年——終端年契約＝判斷日起第 5 個完整會計年度"
                f"（見 dd_schema/decision_inputs.md）"
            )
            # v19 形狀：契約已定死，升 FAIL；舊形狀維持 WARN（既有慣例分歧不回頭改）。
            (fails if strict_terminal_year else warns).append(msg)

    # Bull 前兩年 EPS 與 Base 相同＝情境退化（verify_dd_math 檢查 E 同款）
    bull_path = (scenario_tree.get("eps") or {}).get("bull") or []
    base_path = (scenario_tree.get("eps") or {}).get("base") or []
    if (len(bull_path) >= 2 and len(base_path) >= 2
            and bull_path[0] == base_path[0] and bull_path[1] == base_path[1]):
        fails.append(
            "J2｜Bull 前兩年 EPS 與 Base 相同＝情境退化，Bull 只靠終端倍數分岔；"
            "Bull 路徑須自第 1 年起高於 Base"
        )

    # scenario_meta.valuation_dependent 與 decision_inputs 同名欄一致性
    # （J3 --fix 不自動修此欄，不一致必須人工裁定）。WP-G 修：
    # dd_scenario.build_meta() 把這欄寫在 scenario_tree.valuation_dependent
    # 巢狀底下（不是 sref 頂層），舊版讀 sref.get("valuation_dependent") 一
    # 律 None、此檢查形同沒接線；改讀巢狀路徑，頂層當相容 fallback。
    sref_vd = scenario_tree.get("valuation_dependent")
    if sref_vd is None:
        sref_vd = sref.get("valuation_dependent")
    di_vd = di.get("valuation_dependent")
    if sref_vd is not None and di_vd is not None and bool(sref_vd) != bool(di_vd):
        fails.append(
            f"J2｜scenario_meta.valuation_dependent={sref_vd} 與 "
            f"decision_inputs.valuation_dependent={di_vd} 不一致（J3 --fix 不自動修此欄）"
        )

    return fails, warns


# ---------------------------------------------------------------------------
# J1: negative-evidence traceability (--evidence 給定才啟用，WP2 2026-09-05)
# ---------------------------------------------------------------------------

def _collect_evidence_refs(data: dict) -> set:
    referenced = set()
    for c in (data.get("contradictions") or []):
        if isinstance(c, dict):
            referenced.update(c.get("evidence_refs") or [])
    for t in ((data.get("moat") or {}).get("threats") or []):
        if isinstance(t, dict):
            referenced.update(t.get("evidence_refs") or [])
    for b in ((data.get("premortem") or {}).get("blind_spots") or []):
        if isinstance(b, dict):
            referenced.update(b.get("evidence_refs") or [])
    for tr in (data.get("triggers") or []):
        if isinstance(tr, dict):
            referenced.update(tr.get("evidence_refs") or [])
    for r in ((data.get("thesis") or {}).get("R") or []):
        if isinstance(r, dict):
            referenced.update(r.get("evidence_refs") or [])
    for d in (data.get("evidence_dismissed") or []):
        if isinstance(d, dict) and d.get("ref"):
            referenced.add(d["ref"])
    return referenced


def j1_traceability_checks(data: dict, evidence_path: Path | None, warn_only: bool = False) -> tuple[list, list]:
    """WP2 J1 — 負向證據可追溯：evidence coverage／events 內每條
    direction=="-" 的 finding（無 id 時以 {axis}#{index} 現算）須出現在
    judgment 任一 evidence_refs 陣列或頂層 evidence_dismissed[].ref，否則
    FAIL（逐條列 axis#n｜claim 前 60 字）；--j1-warn 降為 WARN。僅在
    --evidence 給定時啟用。"""
    fails, warns = [], []
    if evidence_path is None:
        return fails, warns
    if not evidence_path.exists():
        warns.append(f"J1｜--evidence {evidence_path} 檔案不存在，J1 略過")
        return fails, warns
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        warns.append(f"J1｜--evidence {evidence_path}: JSON parse error: {e}，J1 略過")
        return fails, warns

    referenced = _collect_evidence_refs(data)
    target = warns if warn_only else fails

    for section in ("coverage", "events"):
        block = evidence.get(section) or {}
        for axis, v in block.items():
            if not isinstance(v, dict):
                continue
            for i, f in enumerate(v.get("findings") or []):
                if not isinstance(f, dict) or f.get("direction") != "-":
                    continue
                ref_id = f.get("id") or f"{axis}#{i}"
                if ref_id not in referenced:
                    claim = (f.get("claim") or "")[:60]
                    target.append(f"J1｜{ref_id}｜{claim}")

    return fails, warns


# ---------------------------------------------------------------------------
# J6: 行動門檻變動必須有理由（--evidence 給定才啟用，WP-G 2026-09-11）
#
# TXN 成對驗證（notes/site-internal/dd/_src/…_v18_paired_test_TXN_20260910.md
# 閘⑧）實測抓到：唯一致命點（Single Thing）從「FY2026 FCF/share <$8」換成
# 「工業＋車用連 2 季 YoY 轉負」、清倉門檻由 $8 上調到 $9，但
# `contradictions[]` 對應條目卻寫「各欄逐欄相同」——既有 layer 4 drift_checks
# 只驗證 prior_field 有沒有提到 rearm_trigger 這個欄名，不驗證條目內文是否
# 誠實描述了差異，所以「field 名字掛著、side_a/side_b 卻抄成一樣」不會被攔。
#
# 只比對 `triggers[].type ∈ {"Single Thing", "清倉"}` 這兩種判斷規則明訂
# 「唯一居所」（§5 thesis Single Thing／§5 唯一清倉級）的型別——前份與本次
# 各剛好一列時才是可靠的 1:1 比對，不是剛好一列（0 或 ≥2）視為比不出來，只
# WARN 不 FAIL（不要猜）。門檻文字（前份用 dd_prior.extract_triggers 產出
# 的「指標與門檻」合併欄，本次用 triggers[].threshold）正規化後不同，卻在
# contradictions[] 找不到 cause∈{新證據,方法變動}、side_a≠side_b、且提及該
# 型別字樣的條目 → FAIL。
# ---------------------------------------------------------------------------

_THRESHOLD_DRIFT_TYPES = ("Single Thing", "清倉")
_THRESHOLD_DRIFT_TOKENS = {
    "Single Thing": ("Single Thing", "唯一致命點", "唯一樞紐"),
    "清倉": ("清倉",),
}


def _unescape_and_norm(s):
    if not isinstance(s, str):
        return None
    return unicodedata.normalize("NFKC", html_lib.unescape(s)).strip()


def _prior_trigger_rows_by_type(prior_triggers: dict, type_label: str) -> list:
    """prior_dd.triggers（dd_prior.extract_triggers 的表格輸出，欄名取自原
    HTML 表頭，含「類型」欄可能帶括注如「Single Thing（H1）」）依去括注後的
    類型比對，回傳等於 type_label 的列。"""
    if not isinstance(prior_triggers, dict) or prior_triggers.get("format") != "table":
        return []
    out = []
    for row in prior_triggers.get("rows") or []:
        if not isinstance(row, dict):
            continue
        raw_type = row.get("類型") or ""
        if _strip_parenthetical(raw_type) == type_label:
            out.append(row)
    return out


def threshold_drift_checks(data: dict, evidence_path: Path | None) -> tuple[list, list]:
    fails, warns = [], []
    if evidence_path is None or not evidence_path.exists():
        return fails, warns
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fails, warns

    prior_dd = evidence.get("prior_dd") or {}
    if prior_dd.get("status") != "ok":
        return fails, warns
    prior_triggers = prior_dd.get("triggers") or {}
    cur_triggers = data.get("triggers") or []
    contradictions = data.get("contradictions") or []

    for type_label in _THRESHOLD_DRIFT_TYPES:
        prior_rows = _prior_trigger_rows_by_type(prior_triggers, type_label)
        cur_rows = [t for t in cur_triggers if isinstance(t, dict) and t.get("type") == type_label]
        if len(prior_rows) != 1 or len(cur_rows) != 1:
            warns.append(
                f"J6｜門檻漂移比對（{type_label}）：前份 {len(prior_rows)} 列／本次 "
                f"{len(cur_rows)} 列，非 1:1 無法機械比對，略過"
            )
            continue
        prior_text = _unescape_and_norm(prior_rows[0].get("指標與門檻"))
        cur_text = _unescape_and_norm(cur_rows[0].get("threshold"))
        if prior_text is None or cur_text is None or prior_text == cur_text:
            continue
        tokens = _THRESHOLD_DRIFT_TOKENS[type_label]
        covered = any(
            isinstance(c, dict)
            and c.get("cause") in ("新證據", "方法變動")
            and _unescape_and_norm(c.get("side_a")) != _unescape_and_norm(c.get("side_b"))
            and any(tok in f"{c.get('axis','')}{c.get('side_a','')}{c.get('side_b','')}" for tok in tokens)
            for c in contradictions
        )
        if not covered:
            fails.append(
                f"J6｜門檻漂移未歸因（{type_label}）：前份「{prior_text}」→本次「{cur_text}」，"
                f"contradictions[] 找不到 cause∈{{新證據,方法變動}}、side_a≠side_b、且提及"
                f"「{type_label}」字樣的對應條目——rearm_trigger／觸發器不得寫「相同」"
            )

    return fails, warns


# ---------------------------------------------------------------------------
# layer 3: machine-language / CJK-punctuation leak scan (WP1c 修法3)
#
# 判斷層就攔——散文/呈現層才攔已經太晚（v16 dry-run §11 item 3 教訓：
# `judgment.triggers[].action` 含「row8a/8b」直接流進 E12 表）。掃所有字串
# 葉節點，命中 dd_sections.LEAK_PATTERNS（QC-40 詞表，import 重用不複製）或
# qc.CJK_PUNCT_RE（半形標點）即 FAIL。
#
# 豁免（見 _v16_design_spec_20260903.md §11 item 3；B 組修法漏洞修正新增
# decision_out.row_hit / decision_out.pacing[]）：
#   - decision_out.audit_rows[] 整個子樹——機器稽核表本就用矩陣語言
#     （row/signal/val/moat_trend/…），渲染在 <details class="audit"> 折疊區。
#   - decision_out.row_hit 與 decision_out.pacing[]——dd_decision.py 機械寫入
#     的矩陣語言（同含「row 8」「QC-49」），比照 audit_rows 豁免；
#     decision_out.rearm_trigger / decision_out.exec_line 仍照常檢查，不豁免。
#   - reasoning.* 字串中的「（QC-\d+）」括注——QC-33 推導允許引用查核代號，
#     只遮蔽這個括注片段，reasoning 內其餘 leak pattern（如欄名外洩）仍抓。
# ---------------------------------------------------------------------------

_LEAK_CHECK_RES = [(p, re.compile(p)) for p in dd_sections.LEAK_PATTERNS]
_QC_ANNOTATION_RE = re.compile(r"[（(]QC-\d+[）)]")
_LEAK_SKIP_SUBTREES = (
    "decision_out.audit_rows",
    "decision_out.row_hit",
    "decision_out.pacing",
)


def _walk_strings(obj, path):
    """Yield (path, string_value) for every string leaf, skipping the paths
    (and their descendants) listed in `_LEAK_SKIP_SUBTREES`."""
    if any(path == p or path.startswith(p + ".") or path.startswith(p + "[")
           for p in _LEAK_SKIP_SUBTREES):
        return
    if isinstance(obj, str):
        if obj:
            yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_strings(v, f"{path}[{i}]")


def leak_and_punct_checks(data: dict) -> list:
    fails = []
    for path, text in _walk_strings(data, ""):
        # decision_out.requires_critic 是 dd_decision.py 機械寫入的觸發標記
        # （值即 "QC-48" 等代號，供 orchestrator 讀），不是讀者面文字——
        # 2026-09-05 WP1d 重放 BE 查出兩支腳本互相打架，此欄整個豁免。
        if path.startswith("decision_out.requires_critic"):
            continue
        # contradictions[].prior_field 依 QC-49 執行細則必須填 dd-meta 欄名（runway_post_y5／
        # archetype 等本身就在洩漏詞表內），該欄整個豁免；axis 以「前份漂移：」開頭時，
        # 冒號後的欄名 token 同樣豁免（HPE 2026-09-05 真跑查出驗證器自相矛盾）。
        # 2026-09-10（WP-E 修 #1）：A4 開放 prior_field 為欄名陣列後，_walk_strings 對
        # 陣列元素產生的路徑是 `prior_field[0]` 這種子路徑，原本的 `$` 收尾只匹配字串
        # 形狀，陣列形狀會漏接、被當成讀者文字誤判外洩——整個子樹（陣列各元素）一併豁免。
        if re.match(r"contradictions\[\d+\]\.prior_field(\[\d+\])?$", path):
            continue
        if re.match(r"contradictions\[\d+\]\.axis$", path) and text.startswith("前份漂移："):
            continue
        scan_text = text
        if path.startswith("reasoning."):
            scan_text = _QC_ANNOTATION_RE.sub(lambda m: " " * len(m.group(0)), scan_text)
        for pat_src, pat in _LEAK_CHECK_RES:
            m = pat.search(scan_text)
            if m:
                ctx = scan_text[max(0, m.start() - 15):m.start() + 25].strip()
                fails.append(
                    f"$.{path}: 機器語言外洩 {m.group(0)!r}（詞表 {pat_src!r}）—「…{ctx}…」"
                )
        for m in qc.CJK_PUNCT_RE.finditer(text):
            ctx = text[max(0, m.start() - 10):m.start() + 15].strip()
            fails.append(f"$.{path}: CJK 接半形標點 {m.group(0)!r}（應用全形，如 ，。：）—「…{ctx}…」")
    return fails


# ---------------------------------------------------------------------------
# WP-E 修 #2（2026-09-10，Codex 複審點 2）：四個 B1-B4 條件式展開區塊
# （industry.tam_table／growth.segments／governance.capital_returns／
# valuation.peers）schema 只放寬成 "type": ["array", "object"]——generic
# schema_validate 不支援 oneOf，object 形態沒有 required/properties 可管，
# 空物件 {}／{"expanded": false}（無 reason）都會被 layer 1 放行。這裡另開
# 一個專用檢查：object 形態必須是合法的「未展開」標記（expanded 明確為
# false，reason 為去空白後非空字串）。不對 reason 做字數或關鍵字品質判斷
# ——理由是否「真的不承重」是判斷問題，留給人工／critic 審讀。
# ---------------------------------------------------------------------------

_EXPANDABLE_BLOCKS = (
    ("industry", "tam_table"),
    ("growth", "segments"),
    ("governance", "capital_returns"),
    ("valuation", "peers"),
)


def expandable_block_checks(data: dict) -> list:
    fails = []
    for top, key in _EXPANDABLE_BLOCKS:
        node = data.get(top)
        if not isinstance(node, dict):
            continue
        value = node.get(key)
        if not isinstance(value, dict):
            continue  # list（正常展開形狀）或缺欄，交給 layer1 required 檢查
        if value.get("expanded") is not False:
            fails.append(
                f"$.{top}.{key}: object 形態必須是未展開標記（expanded 須明確為 false）；要展開請改用陣列（逐列 item／value），"
                f"得到 {value.get('expanded')!r}"
            )
            continue
        reason = value.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            fails.append(f"$.{top}.{key}: 未展開標記缺 reason（省略理由不得為空）")
    return fails


# ---------------------------------------------------------------------------
# WP-E 修 #3（2026-09-10，Codex 複審點 3）：A1 撤掉 premortem.failure_story／
# second_failure 必填後，新格式的反證唯一來源（blind_spots[] 依 view 分組）
# 沒有機械契約接住「三視角全空」——只在 prompt 裡要求。這裡對新格式檔加一個
# 檢查：三個視角（論點失敗／論點成功但股東經濟變差／價格已反映太多）各至少
# 一條有非空 evidence 或 assumption，或該條有非空 not_applicable_reason（合法
# 「此視角不適用」出口，不強逼硬湊三段散文）。舊格式（有 failure_story 且
# blind_spots 為純字串）不受影響，維持原本沒有此檢查的路——用明確的形狀識別
# （_premortem_is_new_format），不誤傷既有存查（BE_20260905 等）。
# ---------------------------------------------------------------------------


_COUNTER_VIEWS = ("論點失敗", "論點成功但股東經濟變差", "價格已反映太多")  # 與 dd_brief._COUNTER_VIEWS 同詞表


def _premortem_is_new_format(premortem: dict) -> bool:
    blind_spots = premortem.get("blind_spots") or []
    has_view_obj = any(isinstance(b, dict) and b.get("view") for b in blind_spots)
    missing_story = not premortem.get("failure_story") and not premortem.get("second_failure")
    return bool(has_view_obj or missing_story)


def premortem_counterevidence_checks(data: dict) -> list:
    premortem = data.get("premortem")
    if not isinstance(premortem, dict) or not _premortem_is_new_format(premortem):
        return []
    blind_spots = premortem.get("blind_spots") or []
    by_view = {v: [] for v in _COUNTER_VIEWS}
    for b in blind_spots:
        if isinstance(b, dict) and b.get("view") in by_view:
            by_view[b["view"]].append(b)
    fails = []
    for view in _COUNTER_VIEWS:
        recs = by_view[view]

        def _nonempty(r, k):
            v = r.get(k)
            return isinstance(v, str) and bool(v.strip())

        ok = any(
            _nonempty(r, "evidence") or _nonempty(r, "assumption") or _nonempty(r, "not_applicable_reason")
            for r in recs
        )
        if not ok:
            fails.append(
                f"$.premortem.blind_spots: 視角「{view}」缺非空 evidence／assumption，"
                f"也無 not_applicable_reason（新格式反證唯一來源不得三視角全空）"
            )
    return fails


# ---------------------------------------------------------------------------
# WP-G 修 #4（2026-09-11，Codex 第三輪複審「反向引用」項）：judgment-rules.md
# §2 問六已明寫 trap_analysis 只交 verdict＋label，判斷依據一律寫在
# premortem.blind_spots[]（反證唯一居所）並在 §5.R／trap_analysis 引用，不在
# trap_analysis.evidence_for／evidence_against 本欄重寫——TXN 成對驗證仍查到
# 新版把這兩欄填成散文，且方向與反證紀錄不同調（消費端若直讀會拿到相反意
# 思）。schema 早已把這兩欄降為選填（見 judgment.schema.json trap_analysis
# 只 required verdict），本檢查只補「新格式檔仍手填時提醒改讀反證紀錄」的
# WARN——語意方向（填的到底支持哪邊）不是能機械判斷的事，交既有 gate 審，
# 這裡只查欄位形狀／是否存在，不新增 LLM 判斷。
# ---------------------------------------------------------------------------

def trap_analysis_redundancy_checks(data: dict) -> list:
    warns = []
    premortem = data.get("premortem")
    if not isinstance(premortem, dict) or not _premortem_is_new_format(premortem):
        return warns
    trap = data.get("trap_analysis") or {}
    for key in ("evidence_for", "evidence_against"):
        v = trap.get(key)
        if isinstance(v, str) and v.strip():
            warns.append(
                f"$.trap_analysis.{key}: 新格式檔（反證唯一居所＝premortem.blind_spots[]）"
                f"不建議填本欄——判斷依據應寫進反證紀錄並在此引用，不重寫一份可能語意反向"
                f"的散文（judgment-rules.md §2 問六）"
            )
    return warns


# ---------------------------------------------------------------------------
# WP-G 修 #5（2026-09-11，Codex 第三輪複審「val_denominator_disputed=false
# 無據」項）：judgment-rules.md 問五分母窗口硬規則只規定 disputed=true 時該
# 便宜論證無效，沒有規定填 false 時要不要交代理由——新版填 false 卻沒有一句
# 可定位的「所選分母為何可用」，消費端讀不到這個判斷是怎麼下的。本檢查只驗
# 「填了 disputed 就必須有非空 note」這個形狀／存在性條件，note 內容是否足
# 以支持 false／true 仍交既有 gate 判斷，不做語意審。僅對新格式檔（判斷層
# schema 已進化到 v18 骨架）生效，沿用 WP-E 的 _premortem_is_new_format 當
# 版本判準，不誤傷舊格式既有存查。
# ---------------------------------------------------------------------------

def val_denominator_note_checks(data: dict) -> list:
    fails = []
    premortem = data.get("premortem")
    if not isinstance(premortem, dict) or not _premortem_is_new_format(premortem):
        return fails
    di = data.get("decision_inputs") or {}
    disputed = di.get("val_denominator_disputed")
    if disputed is None:
        return fails
    note = di.get("val_denominator_note")
    if not isinstance(note, str) or not note.strip():
        fails.append(
            f"$.decision_inputs.val_denominator_note: val_denominator_disputed="
            f"{disputed!r} 已填但 note 缺或空——填 false 或 true 都要一句「所選分母"
            f"（FY2026E／FY2027E／forward）為何可用或為何仍是爭點」"
        )
    return fails


# ---------------------------------------------------------------------------
# layer 4: drift-vs-prior attribution check (--evidence, 選配)
#
# drift_check_spec.md（B 組修法5）：evidence.prior_dd.prior_meta（前份 dd-meta
# 全欄）＋ evidence.prior_dd.drift_watch（固定 20 欄，dd_prior.py 產出，單一
# 權威）逐欄對比 current 側（gen_dd_tables.build_dd_meta 重算，不另建映射）；
# 漂移出的欄位須在 judgment.contradictions[] 找到歸因條目，否則 FAIL。
# ---------------------------------------------------------------------------

_DRIFT_NUMERIC_FIELDS = {
    "ev5y_pct", "irr_base_pct", "max_dd_pct", "bull_5y_price",
    "bear_5y_price", "price_at_dd", "asym_ratio",
}
_DRIFT_PCT_FIELDS = {"p_bull_pct", "p_bear_pct"}
_DRIFT_NUM_TOL = 0.05
_DRIFT_PCT_TOL = 0.5
# token 邊界用負向 lookaround（非 \b）——欄名含底線，\b 在 "_" 兩側不會斷詞，
# 這裡改用「前後不是英數底線字元」才算獨立 token，避免如 "ma" 誤中
# "max_dd_pct" 這種子字串誤判（欄名互為子字串是本檢查唯一已知的假陽性源）。
def _token_re(field: str):
    return re.compile(r"(?<![A-Za-z0-9_])" + re.escape(field) + r"(?![A-Za-z0-9_])", re.I)


def _norm_str_for_drift(v):
    if v is None:
        return None
    return unicodedata.normalize("NFKC", str(v)).strip().lower()


def _field_drifted(field: str, prior_v, cur_v) -> bool:
    if prior_v is None and cur_v is None:
        return False
    if field in _DRIFT_NUMERIC_FIELDS or field in _DRIFT_PCT_FIELDS:
        if prior_v is None or cur_v is None:
            return True  # 一側缺一側有 → 視為漂移
        tol = _DRIFT_PCT_TOL if field in _DRIFT_PCT_FIELDS else _DRIFT_NUM_TOL
        try:
            return abs(float(prior_v) - float(cur_v)) > tol
        except (TypeError, ValueError):
            return prior_v != cur_v
    return _norm_str_for_drift(prior_v) != _norm_str_for_drift(cur_v)


def _prior_fields_of(c: dict) -> set:
    """A4（2026-09-10 規則精簡）：一個 contradictions 條目可用 `cause`（價格變動／新證據／
    方法變動）歸因多個漂移欄，故 `prior_field` 允許欄名陣列；單欄仍可填字串。這裡把兩種
    形狀正規化成集合，讓「每個變動欄必須有獨立條目」放寬成「每個變動欄必須映射到一個
    原因條目」——欄位仍逐欄記帳，只是文字不必逐欄重寫一遍。"""
    pf = (c or {}).get("prior_field")
    if isinstance(pf, str):
        return {pf} if pf else set()
    if isinstance(pf, list):
        return {x for x in pf if isinstance(x, str) and x}
    return set()


def drift_checks(data: dict, judgment_path: Path, evidence_path: Path | None) -> tuple[list, list]:
    fails, warns = [], []

    if evidence_path is None:
        warns.append("未提供 evidence，漂移檢查略過")
        return fails, warns
    if not evidence_path.exists():
        warns.append(f"--evidence {evidence_path} 檔案不存在，漂移檢查略過")
        return fails, warns

    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fails.append(f"--evidence {evidence_path}: JSON parse error: {e}")
        return fails, warns

    prior_dd = evidence.get("prior_dd") or {}
    if prior_dd.get("status") != "ok":
        warns.append(f"evidence.prior_dd.status={prior_dd.get('status')!r}（非 ok，無前份），漂移檢查略過")
        return fails, warns

    prior_meta = prior_dd.get("prior_meta")
    if not prior_meta:
        warns.append("evidence.prior_dd 無 prior_meta，漂移檢查略過")
        return fails, warns

    drift_watch = prior_dd.get("drift_watch") or []
    if not drift_watch:
        warns.append("evidence.prior_dd 無 drift_watch 清單，漂移檢查略過")
        return fails, warns

    # current 側：重用 gen_dd_tables 的唯一 judgment→dd-meta 映射，不另建。
    scenario_meta = gen_dd_tables.resolve_scenario_meta(data, judgment_path, None)
    current_meta = gen_dd_tables.build_dd_meta(data, scenario_meta)

    contradictions = data.get("contradictions") or []

    drifted = []
    for f in drift_watch:
        pv, cv = prior_meta.get(f), current_meta.get(f)
        if _field_drifted(f, pv, cv):
            drifted.append((f, cv, pv))

    for f, cv, pv in drifted:
        tok_re = _token_re(f)
        attributed = False
        for c in contradictions:
            if not isinstance(c, dict):
                continue
            if f in _prior_fields_of(c):
                attributed = True
                break
            axis = c.get("axis") or ""
            if tok_re.search(axis):
                attributed = True
                break
        if not attributed:
            if pv is None:
                # WP7b 2026-09-05：前份 dd-meta 本就沒有這個欄位（缺欄或值為
                # None，例如 rearm_trigger 這種 v16 後才新增的欄）——本次新
                # 出現的值不算「未歸因的漂移」，降為 WARN 提醒可不歸因。
                warns.append(
                    f"漂移未歸因（前份格式無此欄，可不歸因）：{f}（本次={cv!r}／前份={pv!r}）"
                )
            else:
                fails.append(
                    f"漂移未歸因：{f}（本次={cv!r}／前份={pv!r}）— judgment.contradictions[] "
                    f"找不到 prior_field 涵蓋 {f!r}（字串或陣列皆可）或 axis 含 {f!r} token 的條目"
                )

    return fails, warns


# ---------------------------------------------------------------------------
# J4: plain 白話區塊完整性（WARN only，WP5a 2026-09-05）
#
# `plain` 是選填內容欄（見 _wp_spec_v17_batch3_20260905.md「plain 區塊定義」），
# 缺欄／短陣列一律 WARN 不 FAIL——它不是判斷規則。字串本身仍照常過
# leak_and_punct_checks（跑在 data 全樹，plain 已含在內，不需另呼叫）。
# ---------------------------------------------------------------------------

# 2026-09-10（A3）：只留「dd_brief 有渲染且沒有機械 fallback」的子欄位。
# 有 fallback 因而移出清單者（括號內為 dd_brief 的退路）：
#   verdict_line（decision_out.verdict）／verdict_sub（oneliner）／
#   market_wrong（valuation.targets.market_wrong_where）／how_to_lose（premortem）／
#   bets（thesis.H）／fears（thesis.R）／change_my_mind（triggers）／
#   business.moat_direction（moat.grade+trend）。
_PLAIN_FIVE_KEYS = ("how_it_makes_money", "why_now", "why_this_size", "biggest_fear", "how_to_act")
# v18（2026-09-10）：六問白話 `plain.six` 取代 `plain.five` 當首段來源（dd_brief
# 同樣優先讀 six）。有 six 就只查 six 的六欄、不再催 five；舊檔（只有 five）維持
# 原本查 five 的路——兩者都缺才報 five 缺欄，語意仍是「首段沒有白話來源」。
_PLAIN_SIX_KEYS = ("how_it_makes_money", "moat", "growth", "capital", "valuation", "how_wrong")
_PLAIN_BUSINESS_KEYS = ("what_to_whom", "why_customers_stay")
_PLAIN_STORIES_KEYS = ("bull", "base", "bear")
_PLAIN_TOP_SCALAR_KEYS = (
    "growth_funding", "prior_compare_reason", "evidence_quality",
)
_PLAIN_NUM_TOKEN_RE = re.compile(r"\d+(?:\.\d+)?")
_PLAIN_NUM_STRIP_RE = re.compile(r"[,，%＄$]")


def _normalize_numbers(text) -> set:
    """抽出字串內 ≥2 位數字的 token，正規化去千分位／%／$／全半形後回傳集合。"""
    if not isinstance(text, str) or not text:
        return set()
    t = unicodedata.normalize("NFKC", text)
    t = _PLAIN_NUM_STRIP_RE.sub("", t)
    out = set()
    for tok in _PLAIN_NUM_TOKEN_RE.findall(t):
        if len(tok.replace(".", "")) >= 2:
            out.add(tok)
    return out


def _collect_numbers(obj) -> set:
    nums = set()
    if isinstance(obj, str):
        nums |= _normalize_numbers(obj)
    elif isinstance(obj, bool):
        pass
    elif isinstance(obj, (int, float)):
        nums |= _normalize_numbers(str(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            nums |= _collect_numbers(v)
    elif isinstance(obj, list):
        for v in obj:
            nums |= _collect_numbers(v)
    return nums


def j4_plain_checks(data: dict) -> list:
    warns = []
    plain = data.get("plain")
    if not plain or not isinstance(plain, dict):
        warns.append("J4：plain 缺")
        return warns

    def _check(container, key, label):
        v = (container or {}).get(key)
        if not isinstance(v, str) or not v.strip():
            warns.append(f"J4：plain 缺欄或空字串｜{label}")

    for k in _PLAIN_TOP_SCALAR_KEYS:
        _check(plain, k, f"plain.{k}")

    six = plain.get("six") or {}
    if six:
        for k in _PLAIN_SIX_KEYS:
            _check(six, k, f"plain.six.{k}")
    else:
        five = plain.get("five") or {}
        for k in _PLAIN_FIVE_KEYS:
            _check(five, k, f"plain.five.{k}")

    business = plain.get("business") or {}
    for k in _PLAIN_BUSINESS_KEYS:
        _check(business, k, f"plain.business.{k}")

    stories = plain.get("stories") or {}
    for k in _PLAIN_STORIES_KEYS:
        _check(stories, k, f"plain.stories.{k}")

    other = {k: v for k, v in data.items() if k != "plain"}
    other_nums = _collect_numbers(other)
    plain_nums = _collect_numbers(plain)
    extra = plain_nums - other_nums
    if extra:
        warns.append(f"J4：plain 內出現 judgment 其他欄位查無的數字：{sorted(extra)}")

    return warns


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


# J5 白話欄角色一致（2026-09-05 CDNS：Fable 白話寫「當核心持股」，dd_decision 給衛星 9b；
# plain 在矩陣跑之前寫，角色以 decision_out.role 為權威）
_ROLE_TOKENS = ("核心", "衛星", "追蹤")


def j5_plain_role_checks(data: dict) -> tuple:
    fails, warns = [], []
    plain = data.get("plain") or {}
    role = ((data.get("decision_out") or {}).get("role") or "").strip()
    if not plain or role not in _ROLE_TOKENS:
        return fails, warns
    five = plain.get("five") or {}
    texts = {
        "plain.verdict_line": plain.get("verdict_line"),
        "plain.verdict_sub": plain.get("verdict_sub"),
        "plain.five.why_this_size": five.get("why_this_size"),
        "plain.five.how_to_act": five.get("how_to_act"),
    }
    for path, t in texts.items():
        if not isinstance(t, str):
            continue
        for tok in _ROLE_TOKENS:
            if tok == role or tok not in t:
                continue
            # 否定句（不當核心／不是核心／非核心／不列核心）不算矛盾
            neg = re.compile(r"(不當|不是|並非|非|不列為|不做|不當作)" + re.escape(tok))
            strong = any(pat in t for pat in (f"當{tok}", f"{tok}持股", f"{tok}角色", f"{tok}席位", f"列為{tok}")) and not neg.search(t)
            if neg.search(t) and not any(pat in t.replace("不當"+tok, "").replace("不是"+tok, "").replace("非"+tok, "") for pat in (f"當{tok}", f"{tok}持股", f"{tok}角色")):
                continue
            msg = f"J5：{path} 出現「{tok}」但 decision_out.role＝{role}（角色以決策矩陣為準）"
            (fails if strong else warns).append(msg)
    return fails, warns

# WP-H2-1（2026-09-11）：§5.R 四檢查點的正式名稱（references/roic-durability.md
# §1–§4）。改以「四項各有沒有回答」取代 schema 的 `minItems: 4`——四個空物件
# 過得了長度檢查，過不了這裡。
ROIC_CHECKPOINT_NAMES = ("需求基礎值", "決策層級", "價值鏈分配", "社會容忍度")


def _answered(text) -> bool:
    """回答過＝非空字串。空物件、空字串、None 一律不算回答。"""
    return isinstance(text, str) and text.strip() != ""


def v19_required_items_checks(raw: dict, facts: dict | None) -> list:
    """WP-H2-1（Codex 裁定 3 後半）：把「必要項目是否有回答」從長度檢查改成內容
    檢查。**查無或不適用要有理由，空物件不算回答。**

    兩處：
    1. `moat.roic_durability.checkpoints` 的四檢查點——每項要嘛有 `text`
       （判讀句），要嘛有 `not_applicable_reason`；四項缺一即 FAIL。
    2. 同業對照——`facts.peer_comparison` 有列且 `moat.competitor_notes` 每家
       一句 `strategy_note`；沒有可比同業時 `moat.peer_na_reason` 必須寫理由。
    """
    fails = []
    moat = (((raw.get("answers") or {}).get("q2_moat") or {})
            .get("verdict_values") or {}).get("moat") or {}

    cps = (moat.get("roic_durability") or {}).get("checkpoints") or []
    for name in ROIC_CHECKPOINT_NAMES:
        hit = None
        for c in cps:
            if isinstance(c, dict) and name in str(c.get("item") or ""):
                hit = c
                break
        if hit is None:
            fails.append(
                f"v19｜§5.R 四檢查點缺「{name}」——四項各要一個回答（判讀句或不適用理由），"
                f"不是湊滿四列"
            )
        elif not (_answered(hit.get("text")) or _answered(hit.get("not_applicable_reason"))):
            fails.append(
                f"v19｜§5.R 檢查點「{name}」有列但沒有回答（text 與 not_applicable_reason 皆空）"
            )

    peer_rows = ((facts or {}).get("peer_comparison") or {}).get("rows") or []
    subject = ((facts or {}).get("peer_comparison") or {}).get("subject")
    peer_names = [r.get("name") for r in peer_rows
                  if isinstance(r, dict) and r.get("name")
                  and not r.get("is_subject") and r.get("name") != subject]
    notes = [n for n in (moat.get("competitor_notes") or []) if isinstance(n, dict)]
    named = [n for n in notes if _answered(n.get("name")) and _answered(n.get("strategy_note"))]
    if peer_names and not named:
        fails.append(
            "v19｜facts.peer_comparison 有 {0} 家同業數字，但 moat.competitor_notes 沒有任何"
            "一家寫出判讀（每家一句：有沒有本錢打價格戰、策略定位）".format(len(peer_names))
        )
    if not peer_names and not named and not _answered(moat.get("peer_na_reason")):
        fails.append(
            "v19｜沒有同業對照（facts.peer_comparison 無可比同業且 moat.competitor_notes 為空），"
            "但 moat.peer_na_reason 沒寫理由——查無或不適用要說清楚為什麼，不得留空"
        )
    for n in notes:
        if not (_answered(n.get("name")) and _answered(n.get("strategy_note"))):
            fails.append(
                "v19｜moat.competitor_notes 有條目缺 name 或 strategy_note：{0}".format(n)
            )
    return fails


def v19_contract_checks(raw: dict, schema: dict, facts: dict | None,
                        facts_path_found: bool,
                        facts_error: str | None = None) -> tuple[list, list]:
    """v19 專屬檢查（WP-H1 2026-09-11；WP-H2-1 2026-09-11 補擋門）。舊形狀完全
    不跑本函式。

    (1) 用 schema 的 `v19_contract` 區塊驗 judge-owned 形狀；(2) **事實檔必須
    存在、可解析且自身 `dd_facts.py check` 通過**——H1 時期 facts 缺席只 WARN，
    Codex 用 fixture 重現「事實檔不存在仍 0 FAIL」，本輪升為 FAIL；(3)
    `answers[].fact_refs[]` 的每個 id 必須在 facts.json 找得到；(4) 由程式投影
    的 `decision_inputs` 機械欄不得被判斷者填成非 null；(5) 必要項目是否有回答
    （見 `v19_required_items_checks`）。
    """
    fails, warns = [], []
    v19_schema = schema.get("v19_contract")
    if not v19_schema:
        warns.append("v19｜judgment.schema.json 缺 v19_contract 區塊，judge-owned 形狀未驗")
    else:
        fails.extend(f"v19｜{e}" for e in schema_validate(raw, v19_schema, "$"))

    # (2) 事實檔擋門：缺、不可解析、或 facts 自身檢查不過，一律 FAIL。
    if not facts_path_found or facts is None:
        fails.append(
            "v19｜事實檔（facts_ref＝{0!r}）{1}——v19 的判斷只准引 facts.json 的事實 id，"
            "沒有事實檔就沒有可追溯性，不得組頁".format(
                raw.get("facts_ref"),
                "解析失敗：{0}".format(facts_error) if facts_error else "找不到或不可解析")
        )
    else:
        try:
            import dd_facts  # 延遲載入避免循環 import（dd_facts 頂層 import 本檔）
        except Exception as e:  # pragma: no cover - defensive
            warns.append(f"v19｜dd_facts 模組載入失敗（{e}），事實檔自檢略過")
        else:
            f_fails, _f_warns = dd_facts.check(facts)
            fails.extend("v19｜事實檔未通過 dd_facts check：{0}".format(m) for m in f_fails)

    fact_ids = set()
    for q in ((facts or {}).get("questions") or {}).values():
        for f in (q or {}).get("facts") or []:
            if isinstance(f, dict) and f.get("id"):
                fact_ids.add(f["id"])
    for qkey, ans in (raw.get("answers") or {}).items():
        if not isinstance(ans, dict):
            continue
        for ref in ans.get("fact_refs") or []:
            if not facts_path_found:
                continue
            if ref not in fact_ids:
                fails.append(
                    f"v19｜answers.{qkey}.fact_refs 引用了 facts.json 沒有的 id：{ref}"
                )

    fails.extend(v19_required_items_checks(raw, facts))

    raw_di = raw.get("decision_inputs") or {}
    dirty = [k for k in dd_project.PROJECTED_DECISION_INPUT_KEYS
             if raw_di.get(k) is not None]
    if dirty:
        fails.append(
            "v19｜decision_inputs 出現由程式投影的欄且值非 null：{0}"
            "——同一件事不准兩邊都填（歸屬表見 dd_schema/judgment-v19.md）".format(dirty)
        )
    return fails, warns


def validate_file(path: Path, evidence_path: Path | None = None, j1_warn: bool = False,
                  facts_path: Path | None = None):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    raw = json.loads(path.read_text(encoding="utf-8"))

    # v19：先驗 judge-owned 形狀，再投影成舊形狀視圖，後面所有檢查一律讀視圖
    # （檢查語義不變）。舊形狀 raw is data，一個分支都不走。
    v19 = dd_project.is_v19(raw)
    if v19:
        resolved_facts_path = (
            Path(facts_path) if facts_path
            else dd_project.resolve_facts_path(raw, path)
        )
        facts_found = bool(resolved_facts_path and Path(resolved_facts_path).exists())
        facts, facts_error = None, None
        if facts_found:
            try:
                facts = json.loads(Path(resolved_facts_path).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, ValueError) as e:
                facts_error = str(e)
        data = dd_project.project(raw, facts)
        v19_fails, v19_warns = v19_contract_checks(raw, schema, facts, facts_found, facts_error)
    else:
        data = raw
        v19_fails, v19_warns = [], []

    struct_errs = schema_validate(data, schema, "$")
    cross_fails, cross_warns = cross_field_checks(data, path)
    pair_fails = same_source_pair_checks(data)  # 2026-09-07（P2-1）：同源欄位 equality
    leak_fails = leak_and_punct_checks(data)
    expand_fails = expandable_block_checks(data)  # WP-E 修 #2：B1-B4 未展開標記完整性
    premortem_fails = premortem_counterevidence_checks(data)  # WP-E 修 #3：新格式反證三視角
    drift_fails, drift_warns = drift_checks(data, path, evidence_path)
    j2_fails, j2_warns = j2_math_checks(data, path, strict_terminal_year=v19,
                                        require_executed=v19)
    j1_fails, j1_warns = j1_traceability_checks(data, evidence_path, warn_only=j1_warn)
    j4_warns = j4_plain_checks(data)
    j5_fails, j5_warns = j5_plain_role_checks(data)
    j6_fails, j6_warns = threshold_drift_checks(data, evidence_path)  # WP-G 修 #2：行動門檻變動必須有理由
    trap_warns = trap_analysis_redundancy_checks(data)  # WP-G 修 #4：反向引用
    val_note_fails = val_denominator_note_checks(data)  # WP-G 修 #5：分母爭議欄需附一句依據

    fails = (v19_fails + struct_errs + cross_fails + pair_fails + leak_fails + expand_fails
             + premortem_fails + drift_fails + j2_fails + j1_fails + j5_fails + j6_fails
             + val_note_fails)
    warns = (v19_warns + cross_warns + drift_warns + j2_warns + j1_warns + j4_warns
             + j5_warns + j6_warns + trap_warns)
    return fails, warns


# ---------------------------------------------------------------------------
# J3: --fix（WP2 2026-09-05）——可自動修的直接改檔：scenario_ref 相對路徑
# → 絕對路徑；字串內半形標點轉全形（沿用 qc.CJK_PUNCT_RE 偵測，qc.py 無現成
# 轉換函式故轉換表另建，正則本身 import 重用不複製）。
# scenario_meta.valuation_dependent 與 decision_inputs 同名欄不一致「不」在
# 此自動修，維持由 j2_math_checks 列 FAIL。
# ---------------------------------------------------------------------------

_PUNCT_FULLWIDTH = {",": "，", ".": "。", ":": "："}


def _fullwidth_punct(s: str) -> str:
    return qc.CJK_PUNCT_RE.sub(lambda m: m.group(0)[:-1] + _PUNCT_FULLWIDTH[m.group(0)[-1]], s)


def _walk_fix_strings(obj):
    """就地走訪 dict/list，yield (container, key_or_index, string_value)。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                yield obj, k, v
            else:
                yield from _walk_fix_strings(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                yield obj, i, v
            else:
                yield from _walk_fix_strings(v)


def apply_fixes(data: dict, judgment_path: Path) -> list:
    """就地修改 data，回傳套用紀錄字串清單。"""
    applied = []

    scenario_ref = data.get("scenario_ref")
    if scenario_ref and not Path(scenario_ref).is_absolute():
        resolved = _resolve_scenario_ref_path(scenario_ref, judgment_path)
        if resolved is not None:
            abs_path = resolved.resolve()
            data["scenario_ref"] = str(abs_path)
            applied.append(f"scenario_ref 相對路徑 {scenario_ref!r} → {data['scenario_ref']!r}")

    # WP7b 2026-09-05：contradictions[].axis 內的「（QC-\d+）」/「(QC-\d+)」
    # 括注整段刪除（純代號去除，不改語意）並去尾空白——判斷 agent 常把
    # judgment-rules 段名（含 QC 代號）直接抄進讀者面 axis 欄，被 leak scan
    # 擋下；_QC_ANNOTATION_RE 沿用既有詞表（layer 3 leak scan 已定義）。
    n_qc = 0
    for c in (data.get("contradictions") or []):
        if not isinstance(c, dict):
            continue
        axis = c.get("axis")
        if not isinstance(axis, str):
            continue
        fixed_axis = _QC_ANNOTATION_RE.sub("", axis).rstrip()
        if fixed_axis != axis:
            c["axis"] = fixed_axis
            n_qc += 1
    if n_qc:
        applied.append(f"contradictions[].axis 內 QC-\\d+ 代號括注已刪除：{n_qc} 處")

    n_punct = 0
    for container, key, s in list(_walk_fix_strings(data)):
        fixed = _fullwidth_punct(s)
        if fixed != s:
            container[key] = fixed
            n_punct += 1
    if n_punct:
        applied.append(f"半形標點轉全形：{n_punct} 處字串已修")

    return applied


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="judgment.json 路徑")
    ap.add_argument("--report", action="store_true", help="永遠 exit 0，只印報告")
    ap.add_argument("--evidence", help="evidence.json 路徑；給了才啟用漂移檢查（layer 4）與 J1")
    ap.add_argument("--facts", help="facts.json 路徑（v19 專用；不給時讀判斷檔的 facts_ref）")
    ap.add_argument("--j1-warn", action="store_true", help="J1 負向證據可追溯 FAIL 降為 WARN（校準用）")
    ap.add_argument("--fix", action="store_true", help="套用 J3 可自動修正項並寫回檔案，再照常跑驗證報告")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"✗ {path}: 檔案不存在")
        sys.exit(1)

    if args.fix:
        data = json.loads(path.read_text(encoding="utf-8"))
        applied = apply_fixes(data, path)
        if applied:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[J3 --fix] {path.name}：套用 {len(applied)} 項修正")
        for a in applied:
            print(f"  ✓ {a}")
        if not applied:
            print("  無可自動修正項")

    evidence_path = Path(args.evidence) if args.evidence else None
    fails, warns = validate_file(path, evidence_path, j1_warn=args.j1_warn,
                                facts_path=Path(args.facts) if args.facts else None)

    tag = "FAIL" if fails else "PASS"
    print(f"[{tag}] {path.name}（{len(fails)} FAIL／{len(warns)} WARN）")
    for f in fails:
        print(f"  ✗ {f}")
    for w in warns:
        print(f"  ⚠ {w}")
    if not fails and not warns:
        print("  全數通過")

    if fails and not args.report:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
