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
     decision_out.audit_rows[] (whole subtree) and the "（QC-\\d+）" citation
     inside reasoning.* strings only.

Usage:
  python3 scripts/validate_judgment.py FILE.json [--report]

Exit 0 = no FAIL-level issues (or --report). Exit 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
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
# layer 3: machine-language / CJK-punctuation leak scan (WP1c 修法3)
#
# 判斷層就攔——散文/呈現層才攔已經太晚（v16 dry-run §11 item 3 教訓：
# `judgment.triggers[].action` 含「row8a/8b」直接流進 E12 表）。掃所有字串
# 葉節點，命中 dd_sections.LEAK_PATTERNS（QC-40 詞表，import 重用不複製）或
# qc.CJK_PUNCT_RE（半形標點）即 FAIL。
#
# 豁免（僅此兩類，見 _v16_design_spec_20260903.md §11 item 3）：
#   - decision_out.audit_rows[] 整個子樹——機器稽核表本就用矩陣語言
#     （row/signal/val/moat_trend/…），渲染在 <details class="audit"> 折疊區。
#   - reasoning.* 字串中的「（QC-\d+）」括注——QC-33 推導允許引用查核代號，
#     只遮蔽這個括注片段，reasoning 內其餘 leak pattern（如欄名外洩）仍抓。
# ---------------------------------------------------------------------------

_LEAK_CHECK_RES = [(p, re.compile(p)) for p in dd_sections.LEAK_PATTERNS]
_QC_ANNOTATION_RE = re.compile(r"[（(]QC-\d+[）)]")
_LEAK_SKIP_SUBTREES = ("decision_out.audit_rows",)


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
# main
# ---------------------------------------------------------------------------

def validate_file(path: Path):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    data = json.loads(path.read_text(encoding="utf-8"))

    struct_errs = schema_validate(data, schema, "$")
    cross_fails, cross_warns = cross_field_checks(data, path)
    leak_fails = leak_and_punct_checks(data)

    fails = struct_errs + cross_fails + leak_fails
    warns = cross_warns
    return fails, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="judgment.json 路徑")
    ap.add_argument("--report", action="store_true", help="永遠 exit 0，只印報告")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"✗ {path}: 檔案不存在")
        sys.exit(1)

    fails, warns = validate_file(path)

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
