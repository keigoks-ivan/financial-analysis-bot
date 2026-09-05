#!/usr/bin/env python3
"""dd_evidence.py — v16 WP1a Stage 0 證據包骨架與覆蓋矩陣派工工具（0 LLM token）。

子命令：
  axes    --archetype X [--segments a,b,c] [--ticker T --company C --industry I --customers X] [--json]
          印出該 archetype 應查的軸清單（含 per_segment 展開＋佔位符替換），供 orchestrator fan-out 派工。
  init    TICKER DATE --archetype X [--segments a,b,c]
          寫 .dd_build/{TICKER}_{DATE}.evidence.json 骨架（coverage 依 archetype 展開，全部 status=pending）。
  merge   FILE PART.json
          把子 agent 回傳的片段深合併進 evidence.json（原子寫入 tmp+rename）；
          coverage.<axis> 重複 merge 以後者為準，但 queries_run 取聯集。
  status  FILE
          列出每軸 status 與 findings 數，統計 pending 幾軸。
  finalize --run-dir DIR | --parts DIR --out FILE
          v17 WP1b：依固定順序合併 Stage 0 子 agent 交回的 parts/*.json（prior →
          numbers_extra → numbers_collect|numbers_agent|numbers_flat →
          axes_*|batch* → events → transcripts → digest_path），merge 前逐 part
          跑 validate_evidence.check_axis，FAIL 的 part 不合併、列入需重派清單；
          合併後給每條 coverage finding 補 id（{axis_id}#{index}，已有不覆寫），
          最後跑 validate_evidence.py --strict 當總 gate。

軸清單唯一權威：references/coverage-axes.md 內的單一 ```json fenced block。
用法：
  python3 scripts/dd_evidence.py axes --archetype "循環/商品" --json
  python3 scripts/dd_evidence.py init AVGO 20260910 --archetype "品質複利成長" --segments "半導體,軟體"
  python3 scripts/dd_evidence.py merge .dd_build/AVGO_20260910.evidence.json .dd_build/evidence_parts/reg_tariff_export.json
  python3 scripts/dd_evidence.py status .dd_build/AVGO_20260910.evidence.json
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
AXES_MD = ROOT / ".claude" / "skills" / "stock-analyst" / "references" / "coverage-axes.md"
BUILD_DIR = ROOT / ".dd_build"

# 錨定在獨立一行的 ```json ... ``` 圍欄（^/$ + MULTILINE），避免 prose 中引用本正則字串本身
# 的行內反引號範例（如「` ```json `」這種說明文字）被誤判成 fenced block 起點。
JSON_BLOCK_RE = re.compile(r"^```json\s*$\n(.*?)\n^```\s*$", re.M | re.S)

PLACEHOLDER_KEYS = ["TICKER", "COMPANY", "INDUSTRY", "CUSTOMERS", "SEGMENT"]


def load_matrix(path=AXES_MD):
    text = path.read_text(encoding="utf-8")
    m = JSON_BLOCK_RE.search(text)
    if not m:
        raise SystemExit(f"找不到 ```json fenced block：{path}")
    return json.loads(m.group(1))


def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9一-鿿]+", "_", s)
    return s.strip("_") or "seg"


def fill(text, values):
    for k, v in values.items():
        if v:
            text = text.replace("{" + k + "}", v)
    return text


def resolve_axes(matrix, archetype, segments=None, values=None):
    """回傳展開後的軸清單（per_segment 展開、佔位符已替換若 values 提供）。"""
    values = values or {}
    common = matrix.get("common", [])
    extra = matrix.get("by_archetype", {}).get(archetype)
    if extra is None:
        known = ", ".join(matrix.get("by_archetype", {}).keys())
        raise SystemExit(f"未知 archetype：{archetype!r}（已知：{known}）")
    resolved = []
    for axis in common + extra:
        if axis.get("per_segment"):
            segs = segments or []
            if not segs:
                # 無 segments 輸入時保留單一模板列（id 不展開），供人工檢視
                a = dict(axis)
                a["id"] = axis["id"]
                a["_template_only"] = True
                resolved.append(_apply_placeholders(a, values))
                continue
            for seg in segs:
                a = dict(axis)
                a["id"] = f"{axis['id']}__{slugify(seg)}"
                a["name"] = f"{axis['name']}（{seg}）"
                seg_values = dict(values)
                seg_values["SEGMENT"] = seg
                resolved.append(_apply_placeholders(a, seg_values))
        else:
            resolved.append(_apply_placeholders(dict(axis), values))
    return resolved


def _apply_placeholders(axis, values):
    if values:
        axis["question"] = fill(axis.get("question", ""), values)
        axis["queries"] = [fill(q, values) for q in axis.get("queries", [])]
    return axis


def cmd_axes(args):
    matrix = load_matrix()
    values = {
        "TICKER": args.ticker or "",
        "COMPANY": args.company or "",
        "INDUSTRY": args.industry or "",
        "CUSTOMERS": args.customers or "",
    }
    segments = [s.strip() for s in args.segments.split(",") if s.strip()] if args.segments else None
    axes = resolve_axes(matrix, args.archetype, segments, values)
    if args.json:
        print(json.dumps(axes, ensure_ascii=False, indent=2))
        return 0
    print(f"archetype={args.archetype!r}　軸數={len(axes)}")
    for a in axes:
        print(f"\n[{a['id']}] {a['name']}")
        print(f"  Q: {a['question']}")
        for q in a["queries"]:
            print(f"    - {q}")
        if a.get("na_allowed"):
            print("  (na_allowed=true)")
    return 0


def cmd_init(args):
    matrix = load_matrix()
    segments = [s.strip() for s in args.segments.split(",") if s.strip()] if args.segments else None
    axes = resolve_axes(matrix, args.archetype, segments)
    coverage = {
        a["id"]: {"status": "pending", "findings": [], "queries_run": [], "note": ""}
        for a in axes
    }
    evidence = {
        "ticker": args.ticker,
        "date": args.date,
        "archetype_hint": args.archetype,
        "earnings_recency": None,
        "numbers": {},
        "coverage": coverage,
        "events": {},
        "prior_dd": {},
        "ledger": {},
        "canonical_id": {},
        "transcripts": {},
    }
    BUILD_DIR.mkdir(exist_ok=True)
    out = BUILD_DIR / f"{args.ticker}_{args.date}.evidence.json"
    _atomic_write(out, evidence)
    print(f"寫入 {out}（{len(coverage)} 軸，全部 pending）")
    return 0


def _atomic_write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _deep_merge(base, part):
    """遞迴合併 part 進 base（原地修改 base 並回傳）。
    coverage.<axis>.queries_run 取聯集；其餘 list/scalar 由 part 覆蓋。"""
    for k, v in part.items():
        if k == "queries_run" and isinstance(v, list) and isinstance(base.get(k), list):
            merged = list(base[k])
            for item in v:
                if item not in merged:
                    merged.append(item)
            base[k] = merged
        elif isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def cmd_merge(args):
    file_path = Path(args.file)
    part_path = Path(args.part)
    if not file_path.exists():
        raise SystemExit(f"evidence.json 不存在：{file_path}")
    if not part_path.exists():
        raise SystemExit(f"片段檔不存在：{part_path}")
    evidence = json.loads(file_path.read_text(encoding="utf-8"))
    part = json.loads(part_path.read_text(encoding="utf-8"))
    _deep_merge(evidence, part)
    _atomic_write(file_path, evidence)
    touched = ", ".join(sorted(part.keys()))
    print(f"已合併 {part_path.name} → {file_path.name}（頂層 key：{touched}）")
    return 0


def cmd_status(args):
    file_path = Path(args.file)
    evidence = json.loads(file_path.read_text(encoding="utf-8"))
    coverage = evidence.get("coverage", {})
    pending = 0
    for axis_id, c in coverage.items():
        status = c.get("status", "?")
        n = len(c.get("findings", []))
        note = (c.get("note") or "")[:40]
        if status == "pending":
            pending += 1
        print(f"[{status:14s}] {axis_id:40s} findings={n} note={note}")
    print(f"—— {len(coverage)} 軸，pending {pending} 軸")
    return 0


# v17 WP1b：finalize 的固定合併順序（正規檔名先於 glob 分類；_all_axes.json／
# batch{n}.axes.json 這類軸清單元資料檔不在任何分類裡，永不合併）。
_AXIS_PART_RE = re.compile(r"^(axes_\d+|batch\d+)\.json$")
_METADATA_ONLY_RE = re.compile(r"(^_all_axes\.json$|\.axes\.json$)")


def _axis_part_sort_key(path):
    m = re.search(r"(\d+)", path.stem)
    return (0 if path.name.startswith("axes_") else 1, int(m.group(1)) if m else 0)


def _select_parts(parts_dir):
    """依 v17 WP1b 固定順序回傳待 merge 的 part 檔路徑清單：
    prior → numbers_extra → numbers_collect|numbers_agent|numbers_flat →
    axes_*|batch*（coverage part，依編號排序） → events → transcripts →
    digest_path → 其餘未分類的 *.json（排除軸清單元資料檔，見 _METADATA_ONLY_RE）。"""
    order = []
    seen = set()

    def pick(*names):
        for name in names:
            p = parts_dir / name
            if p.exists():
                order.append(p)
                seen.add(p)

    pick("prior.json")
    pick("numbers_extra.json")
    pick("numbers_collect.json", "numbers_agent.json", "numbers_flat.json")

    axis_parts = sorted(
        (p for p in parts_dir.glob("*.json") if _AXIS_PART_RE.match(p.name)),
        key=_axis_part_sort_key,
    )
    for p in axis_parts:
        order.append(p)
        seen.add(p)

    pick("events.json")
    pick("transcripts.json")
    pick("digest_path.json")

    # 其餘未分類檔：排除軸清單元資料檔（_all_axes.json／batch{n}.axes.json 等），
    # 其餘按檔名排序附加在最後，仍走「有 coverage/events 就查證、否則直接合併」邏輯。
    leftovers = sorted(
        p for p in parts_dir.glob("*.json")
        if p not in seen and not _METADATA_ONLY_RE.search(p.name)
    )
    order.extend(leftovers)
    return order


def _add_finding_ids(coverage):
    """幫每條 coverage finding 補 id＝{axis_id}#{index}（index 為該軸 findings 順序，
    從 0 起算；已有 id 不覆寫）。"""
    for axis_id, c in (coverage or {}).items():
        findings = (c or {}).get("findings") or []
        for i, f in enumerate(findings):
            if isinstance(f, dict) and "id" not in f:
                f["id"] = f"{axis_id}#{i}"


def _empty_evidence_skeleton():
    """finalize 找不到既有 evidence.json 骨架時的起點（頂層 key 齊全、值皆空，
    形狀比照 cmd_init 的輸出），避免純 --parts 模式下純粹因「key 不存在」洗出一堆
    與覆蓋面/合併本身無關的頂層缺 key 訊息。"""
    return {
        "ticker": None, "date": None, "archetype_hint": None, "earnings_recency": None,
        "numbers": {}, "coverage": {}, "events": {}, "prior_dd": {}, "ledger": {},
        "canonical_id": {}, "transcripts": {},
    }


def cmd_finalize(args):
    # 延遲 import：validate_evidence.py 頂層會 `import dd_evidence`，若這裡放在檔頭
    # import 會形成雙向循環；放進函式內、等 dd_evidence 模組自己完全載入完才觸發，
    # 兩邊都能安全解析（沿用 validate_evidence.py 既有「import 同目錄腳本」慣例）。
    import validate_evidence

    if args.run_dir:
        run_dir = Path(args.run_dir)
        parts_dir = run_dir / "parts"
        out_path = Path(args.out) if args.out else run_dir / "evidence.json"
        base_path = run_dir / "evidence.json"
        base = json.loads(base_path.read_text(encoding="utf-8")) if base_path.exists() else _empty_evidence_skeleton()
    else:
        if not args.parts or not args.out:
            raise SystemExit("finalize 需要 --run-dir DIR，或 --parts DIR --out FILE")
        parts_dir = Path(args.parts)
        out_path = Path(args.out)
        base = _empty_evidence_skeleton()
        # 純 --parts 模式常沒有 run-dir 骨架（如對歷史 fixture 重放），嘗試從
        # parts 上層目錄名稱 {TICKER}_{DATE} 補 ticker/date，減少頂層缺 key 的雜訊。
        m = re.match(r"^([A-Za-z0-9.]+)_(\d{8})$", parts_dir.parent.name)
        if m:
            if base.get("ticker") is None:
                base["ticker"] = m.group(1)
            if base.get("date") is None:
                base["date"] = m.group(2)

    if not parts_dir.exists():
        raise SystemExit(f"parts 目錄不存在：{parts_dir}")

    matrix = load_matrix()
    merged, failed = [], []

    for part_path in _select_parts(parts_dir):
        try:
            part = json.loads(part_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            failed.append((part_path.name, [f"JSON 解析失敗：{e}"]))
            continue
        if not isinstance(part, dict):
            failed.append((part_path.name, ["非 JSON object，略過（疑似軸清單元資料檔）"]))
            continue

        part_fails = []
        for key in ("coverage", "events"):
            for axis_id, axis_obj in (part.get(key) or {}).items():
                f, _w = validate_evidence.check_axis(axis_id, axis_obj, matrix)
                part_fails.extend(f)

        if part_fails:
            failed.append((part_path.name, part_fails))
            continue

        _deep_merge(base, part)
        merged.append(part_path.name)

    _add_finding_ids(base.get("coverage") or {})
    _atomic_write(out_path, base)

    print(f"finalize：合併 {len(merged)} 個 part → {out_path}")
    for name in merged:
        print(f"  + {name}")
    if failed:
        print(f"需重派（{len(failed)} 個 part 未合併）：")
        for name, fails in failed:
            print(f"  ✗ {name}")
            for f in fails:
                print(f"      {f}")

    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "validate_evidence.py"),
         str(out_path), "--strict", "--report"],
        capture_output=True, text=True,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    ok = result.returncode == 0 and not failed
    print(f"—— finalize {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv):
    p = argparse.ArgumentParser(prog="dd_evidence.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    ax = sub.add_parser("axes")
    ax.add_argument("--archetype", required=True)
    ax.add_argument("--segments")
    ax.add_argument("--ticker")
    ax.add_argument("--company")
    ax.add_argument("--industry")
    ax.add_argument("--customers")
    ax.add_argument("--json", action="store_true")
    ax.set_defaults(func=cmd_axes)

    init = sub.add_parser("init")
    init.add_argument("ticker")
    init.add_argument("date")
    init.add_argument("--archetype", required=True)
    init.add_argument("--segments")
    init.set_defaults(func=cmd_init)

    mg = sub.add_parser("merge")
    mg.add_argument("file")
    mg.add_argument("part")
    mg.set_defaults(func=cmd_merge)

    st = sub.add_parser("status")
    st.add_argument("file")
    st.set_defaults(func=cmd_status)

    fin = sub.add_parser("finalize")
    fin.add_argument("--run-dir")
    fin.add_argument("--parts")
    fin.add_argument("--out")
    fin.set_defaults(func=cmd_finalize)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
