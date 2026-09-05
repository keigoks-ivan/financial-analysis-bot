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


def _schema_cheatsheet() -> str:
    schema = _load_json(SCHEMA_PATH)
    lines = ["## ② Schema 速查（機械生成自 judgment.schema.json）", ""]

    def walk(node, path, required_flag):
        if not isinstance(node, dict):
            return
        bits = []
        if "type" in node:
            bits.append(f"type={node['type']}")
        if "enum" in node:
            bits.append(f"enum={node['enum']}")
        if "pattern" in node:
            bits.append(f"pattern={node['pattern']!r}")
        if "maxLength" in node:
            bits.append(f"maxLength={node['maxLength']}")
        if "minItems" in node:
            bits.append(f"minItems={node['minItems']}")
        if path != "$":
            marker = "必填" if required_flag else "選填"
            suffix = f"：{'; '.join(bits)}" if bits else ""
            lines.append(f"- `{path}`（{marker}）{suffix}")
        props = node.get("properties")
        if isinstance(props, dict):
            req = set(node.get("required") or [])
            for k, v in props.items():
                child = f"{path}.{k}" if path != "$" else f"$.{k}"
                walk(v, child, k in req)
        items = node.get("items")
        if items:
            walk(items, f"{path}[]", True)

    walk(schema, "$", True)

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
    for p in dd_sections.LEAK_PATTERNS:
        lines.append(f"- `{p}`")
    lines.append(f"- CJK 字元後接半形 `,` `.` `:`（正則 `{qc.CJK_PUNCT_RE.pattern}`）——一律應為全形 ，。：")
    return "\n".join(lines)


def _json_block(obj, indent=None) -> str:
    return "```json\n" + json.dumps(obj, ensure_ascii=False, indent=indent) + "\n```"


def _coverage_table(cov: dict) -> str:
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
    lines.append("### numbers（原樣 JSON，不縮排）")
    lines.append(_json_block(evidence.get("numbers") or {}))
    lines.append("")
    lines.append("### coverage（逐軸表格）")
    lines.append(_coverage_table(evidence.get("coverage") or {}))
    lines.append("")
    for key, label in (("events", "events"), ("prior_dd", "prior_dd"),
                        ("ledger", "ledger"), ("canonical_id", "canonical_id")):
        lines.append(f"### {label}（原樣）")
        lines.append(_json_block(evidence.get(key) or {}, indent=1))
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
    lines = ["## ⑤ Digest", ""]
    if not digest_path or not Path(digest_path).exists():
        lines.append(f"[找不到 digest：{digest_path}]")
        return "\n".join(lines)
    lines.append("```json")
    lines.append(Path(digest_path).read_text(encoding="utf-8"))
    lines.append("```")
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
    judgment_text = (
        judgment_path.read_text(encoding="utf-8") if judgment_path.exists()
        else f"[找不到 judgment：{judgment_path}]"
    )
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
        "## judgment.json 全文\n\n```json\n" + judgment_text + "\n```",
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
