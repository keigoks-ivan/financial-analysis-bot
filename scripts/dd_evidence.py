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
import sys
from pathlib import Path

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

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
