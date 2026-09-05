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
  8. J4 plain 完整性（WARN，WP5a 2026-09-05）: 頂層選填 `plain`（白話區塊，
     契約見 `_wp_spec_v17_batch3_20260905.md`）缺、或任一子欄缺／空字串、或
     `bets`／`fears`／`change_my_mind` 三個陣列長度 ≠3 → WARN 逐項列出（不
     FAIL；`plain` 是內容欄不是判斷規則）。另檢查 plain 內數字 ⊆ judgment
     其他欄位數字集合（正規化去千分位／%／$／全半形，只比對 ≥2 位數字的
     token）為 WARN。`plain` 內字串仍照常走 leak_and_punct_checks（FAIL）。

Usage:
  python3 scripts/validate_judgment.py FILE.json [--report] [--evidence EVIDENCE.json]
                                        [--j1-warn] [--fix]

Exit 0 = no FAIL-level issues (or --report). Exit 1 otherwise.
"""
from __future__ import annotations

import argparse
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
        ref_path = Path(scenario_ref)
        if not ref_path.is_absolute():
            ref_path = judgment_path.parent / scenario_ref
        if not ref_path.exists():
            warns.append(f"scenario_ref {scenario_ref!r} 指向的檔案不存在（{ref_path}），略過交叉檢查")
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
    """回傳 (scenario_meta_dict_or_None, warn_msg_or_None)。獨立於
    cross_field_checks 既有的 scenario_ref 解析（不動既有函式），解析規則
    相同：相對路徑以 judgment 所在目錄為準。"""
    scenario_ref = data.get("scenario_ref")
    if not scenario_ref:
        return None, "scenario_ref 未填，J2 判斷層恆等式略過"
    ref_path = Path(scenario_ref)
    if not ref_path.is_absolute():
        ref_path = judgment_path.parent / scenario_ref
    if not ref_path.exists():
        return None, f"scenario_ref {scenario_ref!r} 指向的檔案不存在（{ref_path}），J2 略過"
    try:
        return json.loads(ref_path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"scenario_ref {ref_path}: JSON parse error: {e}"


def j2_math_checks(data: dict, judgment_path: Path) -> tuple[list, list]:
    """WP2 J2 — 判斷層恆等式：Max DD 下限 vs Bear 終點跌幅、
    decision_inputs.irr_base_pct／ev5y_pct 對 scenario_meta、情境樹年期、
    Bull EPS 對 Base 的退化、scenario_meta.valuation_dependent 與
    decision_inputs 同名欄一致性。恆常執行（不需 --evidence）。"""
    fails, warns = [], []
    sref, warn = _load_scenario_meta_for_j2(data, judgment_path)
    if sref is None:
        if warn:
            warns.append(f"J2｜{warn}")
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
        warns.append("J2｜缺 price_at_dd／bear_5y_price／premortem.max_dd.lo 任一，Max DD 恆等式略過")

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

    # 情境樹年期：scenario_meta 終端年 vs eps_meta.base_eps_path 終端年；
    # 與報告年+5 差 >1 年只 WARN（容忍財年錯位，同 verify_dd_math 檢查 B）
    scenario_tree = sref.get("scenario_tree") or {}
    term_year = _extract_fy_year(scenario_tree.get("terminal_label"))
    eps_path = (data.get("eps_meta") or {}).get("base_eps_path") or {}
    eps_years = [y for y in (_extract_fy_year(k) for k in eps_path) if y is not None]
    if term_year and eps_years:
        max_eps_year = max(eps_years)
        if max_eps_year != term_year:
            fails.append(
                f"J2｜情境樹年期錯配：scenario_meta.scenario_tree.terminal_label 宣告 "
                f"FY{term_year}，但 eps_meta.base_eps_path 終端年是 FY{max_eps_year}"
            )
    dd_date = (data.get("meta") or {}).get("date") or ""
    if term_year and re.match(r"^\d{4}", dd_date):
        dd_year = int(dd_date[:4])
        if abs(term_year - (dd_year + 5)) > J2_YEAR_WARN_TOL:
            warns.append(
                f"J2｜終端年 FY{term_year} 與報告年+5（{dd_year + 5}）差 "
                f">{J2_YEAR_WARN_TOL} 年——確認主時距宣告與財年口徑"
            )

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
    # （J3 --fix 不自動修此欄，不一致必須人工裁定）
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
            if c.get("prior_field") == f:
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
                    f"找不到 prior_field={f!r} 或 axis 含 {f!r} token 的條目"
                )

    return fails, warns


# ---------------------------------------------------------------------------
# J4: plain 白話區塊完整性（WARN only，WP5a 2026-09-05）
#
# `plain` 是選填內容欄（見 _wp_spec_v17_batch3_20260905.md「plain 區塊定義」），
# 缺欄／短陣列一律 WARN 不 FAIL——它不是判斷規則。字串本身仍照常過
# leak_and_punct_checks（跑在 data 全樹，plain 已含在內，不需另呼叫）。
# ---------------------------------------------------------------------------

_PLAIN_FIVE_KEYS = ("how_it_makes_money", "why_now", "why_this_size", "biggest_fear", "how_to_act")
_PLAIN_BUSINESS_KEYS = ("what_to_whom", "why_customers_stay", "moat_direction")
_PLAIN_STORIES_KEYS = ("bull", "base", "bear")
_PLAIN_TOP_SCALAR_KEYS = (
    "verdict_line", "verdict_sub", "market_wrong", "growth_funding",
    "prior_compare_reason", "how_to_lose", "evidence_quality",
)
_PLAIN_ARRAY_KEYS = ("bets", "fears", "change_my_mind")
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

    five = plain.get("five") or {}
    for k in _PLAIN_FIVE_KEYS:
        _check(five, k, f"plain.five.{k}")

    business = plain.get("business") or {}
    for k in _PLAIN_BUSINESS_KEYS:
        _check(business, k, f"plain.business.{k}")

    stories = plain.get("stories") or {}
    for k in _PLAIN_STORIES_KEYS:
        _check(stories, k, f"plain.stories.{k}")

    for k in _PLAIN_ARRAY_KEYS:
        arr = plain.get(k)
        n = len(arr) if isinstance(arr, list) else 0
        if n != 3:
            warns.append(f"J4：plain.{k} 長度應為 3，實際 {n}")

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

def validate_file(path: Path, evidence_path: Path | None = None, j1_warn: bool = False):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    data = json.loads(path.read_text(encoding="utf-8"))

    struct_errs = schema_validate(data, schema, "$")
    cross_fails, cross_warns = cross_field_checks(data, path)
    leak_fails = leak_and_punct_checks(data)
    drift_fails, drift_warns = drift_checks(data, path, evidence_path)
    j2_fails, j2_warns = j2_math_checks(data, path)
    j1_fails, j1_warns = j1_traceability_checks(data, evidence_path, warn_only=j1_warn)
    j4_warns = j4_plain_checks(data)

    fails = struct_errs + cross_fails + leak_fails + drift_fails + j2_fails + j1_fails
    warns = cross_warns + drift_warns + j2_warns + j1_warns + j4_warns
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
        abs_path = (judgment_path.parent / scenario_ref).resolve()
        if abs_path.exists():
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
    fails, warns = validate_file(path, evidence_path, j1_warn=args.j1_warn)

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
