#!/usr/bin/env python3
"""dd_bundle.py — WP2 判斷層 prompt bundle 組裝器（2026-09-05）。

依母稿 §3.3 順序，把 Stage 0 evidence 包＋逐字稿＋digest＋規則檔組成單一
Markdown，供判斷 agent（judge）或判斷層 critic（gate）一次讀取（無頭執行
時取代人工手貼）。

`judge` 段落順序：①任務頭 → ②schema 速查（機械生成自
judgment.schema.json）→ ③evidence 緊湊版 → ④最新一季逐字稿全文 →
⑤digest → ⑥`references/v16/judgment-rules.md` 全文 → ⑦archetype 條件載入
reference（依 judgment-rules §1 表）。

`gate` 段落順序：①任務頭 → ③evidence 緊湊版 → ④逐字稿全文 → ⑤digest →
judgment.json 全文 → `references/critic-gates.md` 全文。

用法：
  python3 scripts/dd_bundle.py judge --run-dir DIR [--out DIR/bundles/judge.md]
  python3 scripts/dd_bundle.py judge --evidence FILE [--digest FILE]
      [--transcript FILE] [--judgment-rules FILE] --out FILE
  python3 scripts/dd_bundle.py gate --run-dir DIR [--out DIR/bundles/gate.md]
  python3 scripts/dd_bundle.py gate --evidence FILE --judgment FILE
      [--digest FILE] [--transcript FILE] [--critic-gates FILE] --out FILE

印 bundle 位元組數與 chars/3 估 token。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_sections  # noqa: E402 — LEAK_PATTERNS（QC-40 詞表），單一權威不複製
import qc  # noqa: E402 — CJK_PUNCT_RE（半形標點規則），單一權威不複製

SCHEMA_PATH = ROOT / "scripts" / "dd_schema" / "judgment.schema.json"
SKILL_REFS_DIR = ROOT / ".claude" / "skills" / "stock-analyst" / "references"
JUDGMENT_RULES_PATH = SKILL_REFS_DIR / "v16" / "judgment-rules.md"
CRITIC_GATES_PATH = SKILL_REFS_DIR / "critic-gates.md"

# archetype → 條件載入 reference（judgment-rules.md §1 表；ALWAYS_REFS 為該表
# 「任一(寫§5.R前)／任一(Part II前)／填appendix_a四欄前」三列，與 archetype 無關）
ARCHETYPE_REFS = {
    "循環/商品": ["cyclical-lens.md"],
    "EMS/ODM": ["cyclical-lens.md"],
    "金融": ["archetype-gatesets.md"],
    "未獲利高成長": ["archetype-gatesets.md"],
    "轉機/特殊情境": ["archetype-gatesets.md"],
    "受監管公用/穩定內需": ["archetype-gatesets.md"],
}
ALWAYS_REFS = ["roic-durability.md", "judgment-playbook.md", "timing-appendix.md"]


def _load_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _task_header(ticker, date, mode: str) -> str:
    role = "判斷（judge）" if mode == "judge" else "判斷層 critic（gate）"
    goal = (
        "輸出 `judgment.json`（形狀見下方 schema 速查），不得臆測未在證據包內出現的數字或事件；"
        "負向 finding 未處置一律列 `evidence_refs` 或 `evidence_dismissed[]`（見 schema 速查 evidence_refs 用法）。"
        if mode == "judge" else
        "輸出 critic gate 判定（PASS／PASS-with-fixes／FAIL）與逐條 finding，依 `references/critic-gates.md` 全文的 checklist 逐項作答。"
    )
    return (
        f"## ① 任務頭\n\n"
        f"標的：{ticker}　日期：{date}　角色：stock-analyst v16.2 三步制的{role} agent。\n\n"
        f"{goal}"
    )


# 2026-09-06：schema 速查瘦身用型別簡寫表（語意不變，只縮寫 type 字面值）。
_TYPE_ABBR = {
    "string": "str", "object": "obj", "array": "arr",
    "integer": "int", "number": "num", "boolean": "bool", "null": "null",
}


def _schema_cheatsheet() -> str:
    """機械生成 schema 速查。

    2026-09-06：改成縮排巢狀格式（不重複完整路徑，只在陣列/物件邊界縮排一格），
    type/enum/pattern/maxLength/minItems 壓成一行緊湊記法；required 標記從
    「（必填）」全字改成行首 `*`。語意（哪些欄位/型別/enum/pattern/必填與否）
    一個不少，只是省掉逐行重複的路徑前綴與中文標籤字。
    """
    schema = _load_json(SCHEMA_PATH)
    lines = ["## ② Schema 速查（機械生成自 judgment.schema.json，緊湊版）", ""]
    lines.append(
        "格式：縮排＝巢狀層級（不重複完整路徑）；行首 `*`＝必填；"
        "型別簡寫 str/obj/arr/int/num/bool，`a|b`＝可為多型別（含 null）；"
        "`enum[...]`＝允許值；`pat=`＝正則；`≤N`＝maxLength；`≥N`＝minItems；"
        "陣列欄位以 `key[]` 表示，其元素（items）型別接在同一行，物件元素的欄位在下一層縮排列出。"
    )
    lines.append("")

    def type_str(t) -> str:
        if isinstance(t, list):
            return "|".join(_TYPE_ABBR.get(x, x) for x in t)
        return _TYPE_ABBR.get(t, t)

    def scalar_bits(node: dict) -> list:
        bits = []
        if "type" in node and node["type"] != "object" and node["type"] != "array":
            bits.append(type_str(node["type"]))
        if "enum" in node:
            bits.append("enum[" + ",".join(str(x) for x in node["enum"]) + "]")
        if "pattern" in node:
            bits.append(f"pat={node['pattern']}")
        if "maxLength" in node:
            bits.append(f"≤{node['maxLength']}")
        return bits

    def walk(node, key, required_flag, depth):
        if not isinstance(node, dict):
            return
        indent = "  " * depth
        is_array = node.get("type") == "array"
        items = node.get("items") if is_array else None
        display_key = f"{key}[]" if is_array else key
        marker = "*" if required_flag else ""

        bits = []
        if is_array:
            bits.append("arr")
            if "minItems" in node:
                bits.append(f"≥{node['minItems']}")
            if isinstance(items, dict) and items.get("type") not in (None, "object"):
                bits.extend(scalar_bits(items))
        else:
            bits.extend(scalar_bits(node))
        suffix = f": {' '.join(bits)}" if bits else ""
        lines.append(f"{indent}{marker}{display_key}{suffix}")

        target = items if is_array and isinstance(items, dict) else node
        props = target.get("properties") if isinstance(target, dict) else None
        if isinstance(props, dict):
            req = set(target.get("required") or [])
            for k, v in props.items():
                walk(v, k, k in req, depth + 1)

    top_props = schema.get("properties") or {}
    top_req = set(schema.get("required") or [])
    for k, v in top_props.items():
        walk(v, k, k in top_req, 0)

    lines.append("")
    lines.append("### evidence_refs 用法（v17 新增）")
    lines.append(
        "`contradictions[]`／`moat.threats[]`／`premortem.blind_spots[]`（物件形態時）／"
        "`triggers[]`／`thesis.R[]` 可各自加選填 `evidence_refs: [string]`，格式 "
        "`axis_id#index`（對應 evidence coverage/events 該軸 findings 陣列 0-based 索引，"
        "或 finding 自身既有的 `id`）。無法對應到既有證據、但仍要捨棄的負向 finding，"
        "記到頂層 `evidence_dismissed: [{ref, reason}]`。`validate_judgment.py --evidence`"
        "（J1）會檢查每條 `direction==\"-\"` 的 finding 是否被上述任一處引用，未引用＝FAIL。"
    )
    lines.append("")
    lines.append("### 機器語言／半形標點洩漏詞表（單一權威：`dd_sections.LEAK_PATTERNS` ＋ `qc.CJK_PUNCT_RE`）")
    lines.append("、".join(f"`{p}`" for p in dd_sections.LEAK_PATTERNS))
    lines.append(f"- CJK 字元後接半形 `,` `.` `:`（正則 `{qc.CJK_PUNCT_RE.pattern}`）——一律應為全形 ，。：")
    return "\n".join(lines)


# 2026-09-06：JSON 區塊一律緊湊（無縮排、無多餘空白，separators 去掉逗號/冒號後的
# 空格）——只省格式性空白，內容（鍵值）一字不減。所有呼叫點跟著改，不再傳 indent。
_JSON_NOTE = "（以下 JSON 為緊湊格式（省空白），內容完整）"


def _json_block(obj) -> str:
    return "```json\n" + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n```"


def _coverage_table(cov: dict) -> str:
    # 2026-09-06：曾試改緊湊 JSON 陣列，量測反而 +2%（欄位分隔比 ` | ` 還肥）且位置
    # 欄位對判斷 agent 可讀性較差，故維持 markdown 表格原樣。
    lines = ["| id | dir | as_of | claim | source | affects |", "|---|---|---|---|---|---|"]
    for axis, v in (cov or {}).items():
        if not isinstance(v, dict):
            continue
        findings = v.get("findings") or []
        if not findings:
            lines.append(f"| {axis} | - | - | (status={v.get('status')}；無 findings) |  |  |")
            continue
        for i, f in enumerate(findings):
            rid = f.get("id") or f"{axis}#{i}"
            claim = (f.get("claim") or "").replace("|", "\\|").replace("\n", " ")
            source = (f.get("source") or "").replace("|", "\\|").replace("\n", " ")
            affects = ",".join(f.get("affects") or [])
            lines.append(f"| {rid} | {f.get('direction', '')} | {f.get('as_of', '')} | {claim} | {source} | {affects} |")
    return "\n".join(lines)


def _evidence_compact(evidence: dict) -> str:
    lines = ["## ③ Evidence 緊湊版", ""]
    lines.append(
        f"ticker={evidence.get('ticker')}　date={evidence.get('date')}　"
        f"archetype_hint={evidence.get('archetype_hint')}　"
        f"earnings_recency={evidence.get('earnings_recency')}"
    )
    lines.append("")
    lines.append("### numbers（原樣 JSON）")
    lines.append(_JSON_NOTE)
    lines.append(_json_block(evidence.get("numbers") or {}))
    lines.append("")
    lines.append("### coverage（逐軸表格）")
    lines.append(_coverage_table(evidence.get("coverage") or {}))
    lines.append("")
    for key, label in (("events", "events"), ("prior_dd", "prior_dd"),
                        ("ledger", "ledger"), ("canonical_id", "canonical_id")):
        lines.append(f"### {label}（原樣）")
        lines.append(_JSON_NOTE)
        lines.append(_json_block(evidence.get(key) or {}))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _find_transcript_path(ticker: str, filename: str):
    if not ticker or not filename:
        return None
    home = Path.home()
    pattern = f"Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/{ticker}/{filename}"
    matches = list(home.glob(pattern))
    return matches[0] if matches else None


def _transcript_section(evidence: dict, explicit_path) -> str:
    lines = ["## ④ 最新一季逐字稿全文", ""]
    if explicit_path:
        p = Path(explicit_path)
        if p.exists():
            lines.append(f"（來源：{p}）\n")
            lines.append(p.read_text(encoding="utf-8", errors="replace"))
            return "\n".join(lines)
        lines.append(f"[找不到逐字稿：--transcript 指定的 {p} 不存在]")
        return "\n".join(lines)

    ticker = evidence.get("ticker")
    rec = ((evidence.get("transcripts") or {}).get("selected") or {}).get("recent_four_quarters") or []
    if not rec:
        lines.append("[找不到逐字稿：evidence.transcripts.selected.recent_four_quarters 為空或缺席]")
        return "\n".join(lines)
    filename = rec[0]
    found = _find_transcript_path(ticker, filename)
    if found:
        lines.append(f"（來源：{found}）\n")
        lines.append(found.read_text(encoding="utf-8", errors="replace"))
    else:
        lines.append(
            f"[找不到逐字稿：{filename}（已試 "
            f"~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/{ticker}/）]"
        )
    return "\n".join(lines)


def _digest_section(digest_path) -> str:
    """2026-09-06：digest.json 落地檔是 pretty-print（indent=2），改讀入後轉緊湊
    JSON 再嵌入 bundle（省縮排空白，鍵值內容不變）；若不是合法 JSON（理論上不會，
    保留防呆）就原樣塞入，不因壓縮功能而讓 bundle 開天窗。"""
    lines = ["## ⑤ Digest", ""]
    if not digest_path or not Path(digest_path).exists():
        lines.append(f"[找不到 digest：{digest_path}]")
        return "\n".join(lines)
    raw = Path(digest_path).read_text(encoding="utf-8")
    try:
        obj = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        lines.append("```json")
        lines.append(raw)
        lines.append("```")
        return "\n".join(lines)
    lines.append(_JSON_NOTE)
    lines.append(_json_block(obj))
    return "\n".join(lines)


def _judgment_rules_section(path) -> str:
    lines = ["## ⑥ judgment-rules.md 全文", ""]
    p = Path(path)
    if not p.exists():
        lines.append(f"[找不到 {p}]")
        return "\n".join(lines)
    lines.append(p.read_text(encoding="utf-8"))
    return "\n".join(lines)


def _archetype_refs_section(evidence: dict) -> str:
    lines = ["## ⑦ archetype 條件載入 reference（依 judgment-rules.md §1 表）", ""]
    archetype = (evidence or {}).get("archetype_hint")
    refs = list(ALWAYS_REFS) + ARCHETYPE_REFS.get(archetype, [])
    lines.append(f"archetype_hint={archetype!r} → 載入：{refs}")
    lines.append("")
    for name in refs:
        p = SKILL_REFS_DIR / name
        lines.append(f"### {name}")
        if p.exists():
            lines.append(p.read_text(encoding="utf-8"))
        else:
            lines.append(f"[找不到 {p}]")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _write_bundle(parts, out_path: Path):
    bundle = "\n\n---\n\n".join(parts) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(bundle, encoding="utf-8")
    n_bytes = len(bundle.encode("utf-8"))
    print(f"bundle 已寫 {out_path}：{n_bytes} bytes（≈{len(bundle) // 3} tokens）")


def cmd_judge(args) -> int:
    if args.run_dir:
        run_dir = Path(args.run_dir)
        evidence_path = run_dir / "evidence.json"
        digest_path = Path(args.digest) if args.digest else run_dir / "digest.json"
        out_path = Path(args.out) if args.out else run_dir / "bundles" / "judge.md"
    else:
        if not (args.evidence and args.out):
            print("judge：需要 --run-dir，或至少 --evidence 與 --out", file=sys.stderr)
            return 2
        evidence_path = Path(args.evidence)
        digest_path = Path(args.digest) if args.digest else None
        out_path = Path(args.out)

    if not evidence_path.exists():
        print(f"✗ evidence 檔不存在：{evidence_path}", file=sys.stderr)
        return 1
    evidence = _load_json(evidence_path)
    judgment_rules_path = Path(args.judgment_rules) if args.judgment_rules else JUDGMENT_RULES_PATH

    parts = [
        _task_header(evidence.get("ticker"), evidence.get("date"), "judge"),
        _schema_cheatsheet(),
        _evidence_compact(evidence),
        _transcript_section(evidence, args.transcript),
        _digest_section(digest_path),
        _judgment_rules_section(judgment_rules_path),
        _archetype_refs_section(evidence),
    ]
    _write_bundle(parts, out_path)
    return 0


def cmd_gate(args) -> int:
    if args.run_dir:
        run_dir = Path(args.run_dir)
        evidence_path = run_dir / "evidence.json"
        digest_path = Path(args.digest) if args.digest else run_dir / "digest.json"
        judgment_path = Path(args.judgment) if args.judgment else run_dir / "judgment.json"
        out_path = Path(args.out) if args.out else run_dir / "bundles" / "gate.md"
    else:
        if not (args.evidence and args.judgment and args.out):
            print("gate：需要 --run-dir，或至少 --evidence／--judgment／--out", file=sys.stderr)
            return 2
        evidence_path = Path(args.evidence)
        digest_path = Path(args.digest) if args.digest else None
        judgment_path = Path(args.judgment)
        out_path = Path(args.out)

    if not evidence_path.exists():
        print(f"✗ evidence 檔不存在：{evidence_path}", file=sys.stderr)
        return 1
    evidence = _load_json(evidence_path)
    # 2026-09-06：judgment.json 落地檔是 pretty-print，嵌入 gate bundle 前轉緊湊
    # JSON（省縮排空白）；找不到檔／非合法 JSON 時原樣保留既有錯誤訊息或原始文字。
    if judgment_path.exists():
        judgment_raw = judgment_path.read_text(encoding="utf-8")
        try:
            judgment_text = json.dumps(json.loads(judgment_raw), ensure_ascii=False, separators=(",", ":"))
            judgment_note = _JSON_NOTE + "\n\n"
        except (json.JSONDecodeError, ValueError):
            judgment_text = judgment_raw
            judgment_note = ""
    else:
        judgment_text = f"[找不到 judgment：{judgment_path}]"
        judgment_note = ""
    critic_gates_path = Path(args.critic_gates) if args.critic_gates else CRITIC_GATES_PATH
    critic_gates_text = (
        critic_gates_path.read_text(encoding="utf-8") if critic_gates_path.exists()
        else f"[找不到 {critic_gates_path}]"
    )

    parts = [
        _task_header(evidence.get("ticker"), evidence.get("date"), "gate"),
        _evidence_compact(evidence),
        _transcript_section(evidence, args.transcript),
        _digest_section(digest_path),
        "## judgment.json 全文\n\n" + judgment_note + "```json\n" + judgment_text + "\n```",
        "## references/critic-gates.md 全文\n\n" + critic_gates_text,
    ]
    _write_bundle(parts, out_path)
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_judge = sub.add_parser("judge", help="組判斷 agent 的輸入 bundle")
    p_judge.add_argument("--run-dir", help=".dd_build/runs/{T}_{D}/ 目錄（讀 evidence.json／digest.json，寫 bundles/judge.md）")
    p_judge.add_argument("--evidence", help="evidence.json 路徑（無 --run-dir 時必填）")
    p_judge.add_argument("--digest", help="digest.json 路徑")
    p_judge.add_argument("--transcript", help="逐字稿檔路徑；未給則由 evidence.transcripts 自動找")
    p_judge.add_argument("--judgment-rules", help="judgment-rules.md 路徑（預設 references/v16/judgment-rules.md）")
    p_judge.add_argument("--out", help="輸出 bundle 路徑（無 --run-dir 時必填）")
    p_judge.set_defaults(func=cmd_judge)

    p_gate = sub.add_parser("gate", help="組判斷層 critic 的輸入 bundle")
    p_gate.add_argument("--run-dir", help=".dd_build/runs/{T}_{D}/ 目錄（讀 evidence.json／digest.json／judgment.json）")
    p_gate.add_argument("--evidence", help="evidence.json 路徑（無 --run-dir 時必填）")
    p_gate.add_argument("--digest", help="digest.json 路徑")
    p_gate.add_argument("--judgment", help="judgment.json 路徑（無 --run-dir 時必填）")
    p_gate.add_argument("--transcript", help="逐字稿檔路徑；未給則由 evidence.transcripts 自動找")
    p_gate.add_argument("--critic-gates", help="critic-gates.md 路徑（預設 references/critic-gates.md）")
    p_gate.add_argument("--out", help="輸出 bundle 路徑（無 --run-dir 時必填）")
    p_gate.set_defaults(func=cmd_gate)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
