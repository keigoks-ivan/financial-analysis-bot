#!/usr/bin/env python3
"""validate_evidence.py — v16 WP1a 證據包 schema/覆蓋矩陣 gate（0 LLM token）。

檢查（FAIL 擋下一段 / WARN 只提示，輸出格式比照 verify_dd_math.py 的 [pass]/[FAIL]）：
  1. 頂層 key 齊全：ticker/date/archetype_hint/earnings_recency/numbers/coverage/
     events/prior_dd/ledger/canonical_id/transcripts。
  2. coverage 必含該 archetype（common ∪ by_archetype[archetype_hint]）全部軸——
     依 references/coverage-axes.md 展開（end_markets 依 numbers.segments 展開；
     缺 numbers.segments 時退回偵測既有 end_markets__* 軸，見腳本內註解）。任一軸缺席＝FAIL。
  3. 每軸 status ∈ {found, none, not_applicable}；pending（或非法值）＝FAIL。
     - found：≥1 條 findings，每條須有 claim/source/as_of/direction(+|0|-)/affects[]；
       as_of 距 evidence date > 180 天 → WARN；as_of 無法解析為日期 → FAIL。
     - none：queries_run ≥2 條，否則 FAIL。
     - not_applicable：note 非空字串，且該軸 coverage-axes.md 標 na_allowed=true，
       否則 FAIL（不得用「不適用」逃避查證）。
  4. numbers 必含 price_at_dd／price_as_of／earnings_recency（v15.2.4 命名沿用）。
  5. events 必含 QC-19 五組各一個 key（值可為 "none"，缺 key＝FAIL）。

用法：
  python3 scripts/validate_evidence.py .dd_build/AVGO_20260910.evidence.json
  python3 scripts/validate_evidence.py FILE --report   # 逐軸列印狀態，非僅錯誤行
  python3 scripts/validate_evidence.py FILE --strict   # WARN 一併視為 FAIL（exit 1）
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_evidence  # noqa: E402  （沿用 verify_dd_math.py 的「import 同目錄腳本」慣例）

TOP_LEVEL_KEYS = [
    "ticker", "date", "archetype_hint", "earnings_recency", "numbers",
    "coverage", "events", "prior_dd", "ledger", "canonical_id", "transcripts",
]

NUMBERS_REQUIRED = ["price_at_dd", "price_as_of", "earnings_recency"]

# QC-19 五組（順序對齊 coverage-axes.md major_events 軸的 5 條 queries 模板）
EVENTS_KEYS = [
    "ma_merger",
    "lawsuit_class_action",
    "clinical_fda",
    "product_recall_warning",
    "sec_investigation_restatement",
]

FINDING_FIELDS = ["claim", "source", "as_of", "direction", "affects"]
VALID_DIRECTIONS = {"+", "0", "-"}
VALID_STATUS = {"found", "none", "not_applicable"}

DATE_FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]


def parse_date(s):
    if not isinstance(s, str):
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    return None


def required_axes(matrix, evidence):
    archetype = evidence.get("archetype_hint")
    if not archetype:
        return None, "archetype_hint 缺失，無法展開覆蓋矩陣"
    if archetype not in matrix.get("by_archetype", {}):
        known = ", ".join(matrix.get("by_archetype", {}).keys())
        return None, f"archetype_hint={archetype!r} 不在 coverage-axes.md 已知清單（{known}）"

    segments = (evidence.get("numbers") or {}).get("segments")
    if not segments:
        # 退回：從既有 coverage key 偵測 end_markets__* 已展開的 segment slug，
        # 避免「數字包尚未回填 numbers.segments 但覆蓋面已查」被誤判缺軸。
        cov = evidence.get("coverage") or {}
        detected = sorted({k.split("__", 1)[1] for k in cov if k.startswith("end_markets__")})
        segments = detected or None

    axes = dd_evidence.resolve_axes(matrix, archetype, segments)
    ids = {a["id"] for a in axes if not a.get("_template_only")}
    if not segments:
        ids.add("end_markets")  # 無 segments 來源時，允許用單一未展開列
    return ids, None


def check_file(path, matrix, strict=False):
    fails, warns, axis_report = [], [], []
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"JSON 解析失敗：{e}"], [], []

    # ---- 1. 頂層 key 齊全 ----
    for k in TOP_LEVEL_KEYS:
        if k not in evidence:
            fails.append(f"頂層缺 key：{k}")
    if fails:
        return fails, warns, axis_report  # 頂層都不齊，後續檢查沒有意義

    coverage = evidence.get("coverage") or {}
    ev_date = evidence.get("date")

    # ---- 2. 覆蓋矩陣完整性 ----
    req_ids, err = required_axes(matrix, evidence)
    if err:
        fails.append(err)
        req_ids = set()
    missing = sorted(req_ids - set(coverage.keys()))
    for axis_id in missing:
        fails.append(f"coverage 缺軸：{axis_id}")

    # 供 not_applicable 的 na_allowed 查核用：axis_id → na_allowed
    na_allowed_map = {}
    archetype = evidence.get("archetype_hint")
    if archetype in matrix.get("by_archetype", {}):
        for axis in matrix.get("common", []) + matrix["by_archetype"][archetype]:
            if axis.get("per_segment"):
                # per_segment 軸的展開 id 前綴比對
                for cid in coverage:
                    if cid == axis["id"] or cid.startswith(axis["id"] + "__"):
                        na_allowed_map[cid] = axis.get("na_allowed", False)
            else:
                na_allowed_map[axis["id"]] = axis.get("na_allowed", False)

    # ---- 3. 逐軸 status 檢查 ----
    for axis_id in sorted(req_ids & set(coverage.keys())):
        c = coverage.get(axis_id, {})
        status = c.get("status")
        n_findings = len(c.get("findings") or [])
        axis_report.append((axis_id, status, n_findings, (c.get("note") or "")[:40]))

        if status not in VALID_STATUS:
            fails.append(f"[{axis_id}] status={status!r} 非法（pending 或未知值一律 FAIL）")
            continue

        if status == "found":
            findings = c.get("findings") or []
            if not findings:
                fails.append(f"[{axis_id}] status=found 但 findings 為空")
            for i, f in enumerate(findings):
                missing_fields = [k for k in FINDING_FIELDS if not f.get(k)]
                if missing_fields:
                    fails.append(f"[{axis_id}] findings[{i}] 缺欄位：{missing_fields}")
                    continue
                if f["direction"] not in VALID_DIRECTIONS:
                    fails.append(f"[{axis_id}] findings[{i}].direction={f['direction']!r} 須為 +/0/-")
                if not isinstance(f.get("affects"), list) or not f["affects"]:
                    fails.append(f"[{axis_id}] findings[{i}].affects 須為非空陣列")
                d = parse_date(f["as_of"])
                if d is None:
                    fails.append(f"[{axis_id}] findings[{i}].as_of={f['as_of']!r} 無法解析為日期")
                else:
                    ev_d = parse_date(ev_date)
                    if ev_d and (ev_d - d).days > 180:
                        warns.append(f"[{axis_id}] findings[{i}].as_of={f['as_of']} 距報告日 >180 天")

        elif status == "none":
            qr = c.get("queries_run") or []
            if len(qr) < 2:
                fails.append(f"[{axis_id}] status=none 但 queries_run 僅 {len(qr)} 條（須 ≥2）")

        elif status == "not_applicable":
            note = c.get("note") or ""
            if not note.strip():
                fails.append(f"[{axis_id}] status=not_applicable 但 note 為空")
            if not na_allowed_map.get(axis_id, False):
                fails.append(f"[{axis_id}] status=not_applicable 但該軸 na_allowed=false（不得逃避查證）")

    # ---- 4. numbers 必含三欄 ----
    numbers = evidence.get("numbers") or {}
    for k in NUMBERS_REQUIRED:
        if k not in numbers or numbers.get(k) in (None, ""):
            fails.append(f"numbers 缺欄位或為空：{k}")

    # ---- 5. events 必含 QC-19 五組 ----
    events = evidence.get("events") or {}
    for k in EVENTS_KEYS:
        if k not in events:
            fails.append(f"events 缺 QC-19 分組：{k}")

    if strict:
        fails.extend(f"(strict) {w}" for w in warns)
        warns = []

    return fails, warns, axis_report


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    report = "--report" in argv
    strict = "--strict" in argv
    if not args:
        print("用法：validate_evidence.py FILE [--report] [--strict]")
        return 2
    matrix = dd_evidence.load_matrix()
    any_fail = False
    for a in args:
        p = Path(a)
        if not p.exists():
            print(f"✗ {p}: 檔案不存在")
            any_fail = True
            continue
        fails, warns, axis_report = check_file(p, matrix, strict=strict)
        tag = "FAIL" if fails else "pass"
        print(f"[{tag}] {p.name}")
        if report:
            for axis_id, status, n, note in axis_report:
                print(f"    · {axis_id:40s} {status or '?':14s} findings={n} note={note}")
        for f in fails:
            print(f"    ✗ {f}")
        for w in warns:
            print(f"    ⚠ {w}")
        if fails:
            any_fail = True
    print(f"—— 驗證 {len(args)} 檔，{'有 FAIL' if any_fail else '全數通過'}")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
