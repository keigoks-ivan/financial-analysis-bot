#!/usr/bin/env python3
"""dd_gate.py — v17 WP3：閘（gate）稽核輸出解析與修補 prompt 產生（0 LLM token）。

子命令：
  parse AUDIT.md [--json]
      解析 gate agent 產出的 `_audit_*.md`（或 v17 表格模板），輸出
      {"red": N, "yellow": M, "findings":[{axis, level, path, note, fix}]}。
      支援兩種形狀：
        (a) 既有散文／半表格式 audit（如 `_audit_BE_20260905.md`、
            `_audit_CIEN_20260905.md`）
        (b) v17 模板：`## AUDIT: 判斷級🔴 = N` + `| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |`
      `red` 一律以首行「判斷級🔴 = N」為準；與表內／文內計數不符時印警告（stderr）但不改。

  patch-prompt --audit AUDIT.md --judgment J.json --evidence E.json --out PROMPT.md
      只取 🔴 條目，從 judgment 抽出被點名子樹、從 evidence 抽出被點名 finding，
      渲染 `scripts/dd_prompts/judge_patch.md.tmpl`（不存在則用內建最小模板）到
      --out。

  decide PARSED.json
      印 BLOCK（red>0）或 PASS，exit code 對應（1／0）。

用法：
  python3 scripts/dd_gate.py parse notes/site-internal/dd/_audit_BE_20260905.md --json
  python3 scripts/dd_gate.py patch-prompt --audit AUDIT.md --judgment J.json \
      --evidence E.json --out /tmp/patch.md
  python3 scripts/dd_gate.py decide /tmp/parsed.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RED = "🔴"
YELLOW = "🟡"
GREEN = "🟢"
LEVELS = (RED, YELLOW, GREEN)

DEFAULT_TMPL = ROOT / "scripts" / "dd_prompts" / "judge_patch.md.tmpl"

# 路徑樣式 token：至少含一個「.欄位」或「[數字]」，供從散文/表格欄位中抽出候選路徑。
PATH_TOKEN_RE = re.compile(
    r"[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*|\[\d+\])+"
)

# evidence finding 參照：axis.findings[idx] 或 axis#idx（0-based，皆指向
# evidence.coverage[axis].findings[idx]）。
EVIDENCE_REF_RE = re.compile(
    r"([a-zA-Z_][a-zA-Z0-9_]*)(?:\.findings\[(\d+)\]|#(\d+))"
)


# ---------------------------------------------------------------------------
# parse
# ---------------------------------------------------------------------------

def _first_line_red(text: str):
    m = re.search(r"判斷級\s*🔴\s*[=＝]\s*(\d+)", text)
    return int(m.group(1)) if m else None


def _is_table_line(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and s.count("|") >= 2


def _split_row(line: str):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _is_sep_row(cells) -> bool:
    nonempty = [c.strip() for c in cells if c.strip() != ""]
    if not nonempty:
        return True
    return all(re.fullmatch(r":?-+:?", c) for c in nonempty)


def _extract_level(cell: str):
    for lv in LEVELS:
        if lv in cell:
            return lv
    return None


def _extract_paths(text: str):
    seen = []
    for m in PATH_TOKEN_RE.finditer(text):
        tok = m.group(0)
        if tok not in seen:
            seen.append(tok)
    return seen


def _find_tables(lines):
    """把連續的 table-line 區塊切出來，回傳 list[list[str]]。"""
    tables = []
    cur = []
    for line in lines:
        if _is_table_line(line):
            cur.append(line)
        else:
            if len(cur) >= 2:
                tables.append(cur)
            cur = []
    if len(cur) >= 2:
        tables.append(cur)
    return tables


def _parse_table(table_lines):
    rows = [_split_row(l) for l in table_lines]
    header = rows[0]
    idx = {}
    for i, h in enumerate(header):
        hs = h.strip()
        if hs in ("#", "編號", "項", "項次"):
            idx.setdefault("num", i)
        elif "軸" in hs:
            idx.setdefault("axis", i)
        elif "燈" in hs:
            idx.setdefault("level", i)
        elif "依據" in hs:
            idx.setdefault("note", i)
        elif "指向" in hs:
            idx.setdefault("path", i)
        elif "建議" in hs:
            idx.setdefault("fix", i)

    def cell(row, key):
        i = idx.get(key)
        if i is None or i >= len(row):
            return ""
        return row[i]

    findings = []
    for row in rows[1:]:
        if _is_sep_row(row):
            continue
        if not any(c.strip() for c in row):
            continue
        num = cell(row, "num")
        axis_txt = cell(row, "axis")
        axis = (num + " " + axis_txt).strip()
        level = _extract_level(cell(row, "level")) or ""
        note = cell(row, "note")
        path = cell(row, "path").replace("`", "")
        fix = cell(row, "fix")
        excluded = ("不計" in axis) or ("不計" in note)
        findings.append(
            {
                "axis": axis,
                "level": level,
                "note": note,
                "path": path,
                "fix": fix,
                "_excluded": excluded,
            }
        )
    return findings


_PROSE_RE = re.compile(
    r"^([①-⑳])\s*([^\n🟢🟡🔴]*?)(🟢|🟡|🔴)\s*[:：]\s*(.*)$",
    re.MULTILINE,
)


def _parse_prose(text: str):
    findings = []
    for m in _PROSE_RE.finditer(text):
        num, label, level, rest = m.groups()
        axis = f"{num} {label}".strip()
        rest = rest.strip()
        excluded = ("不計" in label) or ("不計" in rest)
        findings.append(
            {
                "axis": axis,
                "level": level,
                "note": rest,
                "path": "、".join(_extract_paths(rest)),
                "fix": "",
                "_excluded": excluded,
            }
        )
    return findings


def parse_audit(audit_path: str) -> dict:
    text = Path(audit_path).read_text(encoding="utf-8")
    lines = text.splitlines()

    tables = _find_tables(lines)
    chosen = None
    for t in tables:
        header = _split_row(t[0])
        if any("軸" in h for h in header) and any("燈" in h for h in header):
            if chosen is None or len(t) > len(chosen):
                chosen = t

    if chosen:
        findings = _parse_table(chosen)
    else:
        findings = _parse_prose(text)

    counted = [f for f in findings if not f["_excluded"]]
    red_computed = sum(1 for f in counted if f["level"] == RED)
    yellow = sum(1 for f in counted if f["level"] == YELLOW)

    first_line_red = _first_line_red(text)
    if first_line_red is not None:
        red = first_line_red
        if red != red_computed:
            print(
                f"WARNING: 首行「判斷級🔴 = {red}」與表內／文內計數 {red_computed} 不符"
                "（以首行數字為準，不改動）",
                file=sys.stderr,
            )
    else:
        red = red_computed
        print("WARNING: 找不到首行「判斷級🔴 = N」，改用逐條計數當 red", file=sys.stderr)

    for f in findings:
        f.pop("_excluded", None)

    return {"red": red, "yellow": yellow, "findings": findings}


def cmd_parse(args):
    result = parse_audit(args.audit)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"red={result['red']} yellow={result['yellow']}")
        for f in result["findings"]:
            note = f["note"][:60].replace("\n", " ")
            print(f"  {f['level'] or '?'} {f['axis']}｜{note}｜path={f['path']}")
    return 0


# ---------------------------------------------------------------------------
# patch-prompt
# ---------------------------------------------------------------------------

def _load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


_FULL_PATH_RE = re.compile(
    r"[a-zA-Z_][a-zA-Z0-9_]*(?:\[\d+\]|\.[a-zA-Z_][a-zA-Z0-9_]*)*"
)
_PATH_TOKENIZE_RE = re.compile(r"\.|([a-zA-Z_][a-zA-Z0-9_]*)|\[(\d+)\]")


def _tokenize_path(path: str):
    """把 `a.b[2].c` 拆成有序 step 序列：[('key','a'),('key','b'),('idx',2),('key','c')]。"""
    steps = []
    for m in _PATH_TOKENIZE_RE.finditer(path):
        if m.group(1) is not None:
            steps.append(("key", m.group(1)))
        elif m.group(2) is not None:
            steps.append(("idx", int(m.group(2))))
    return steps


def _render_steps(steps) -> str:
    out = ""
    for i, (kind, val) in enumerate(steps):
        if kind == "key":
            out += ("." if i > 0 else "") + val
        else:
            out += f"[{val}]"
    return out


def resolve_path(obj, path: str):
    """解析簡單路徑 a.b[2].c；逐步驟解析，某一步驟解不到（key 不存在／index 超界）就
    退回上一個能解的步驟，回傳 (value, resolved_path)；完全解不到回傳 (None, None)。"""
    if not path or not _FULL_PATH_RE.fullmatch(path):
        return None, None
    steps = _tokenize_path(path)
    for k in range(len(steps), 0, -1):
        cur = obj
        ok = True
        for kind, val in steps[:k]:
            if kind == "key":
                if not isinstance(cur, dict) or val not in cur:
                    ok = False
                    break
                cur = cur[val]
            else:
                if not isinstance(cur, list) or val >= len(cur):
                    ok = False
                    break
                cur = cur[val]
        if ok:
            return cur, _render_steps(steps[:k])
    return None, None


FALLBACK_KEYS = ("contradictions", "decision_inputs", "premortem")


def _dump(obj, limit=4000) -> str:
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    if len(text) > limit:
        text = text[:limit] + "\n... (截斷，原長 %d 字元)" % len(text)
    return text


def _resolve_judgment_subtrees(judgment: dict, path_field: str):
    """回傳 [(resolved_path, value), ...]；path_field 抽不到任何路徑時回退三塊。"""
    tokens = _extract_paths(path_field) if path_field else []
    out = []
    seen = set()
    for tok in tokens:
        value, resolved = resolve_path(judgment, tok)
        if resolved is not None and resolved not in seen:
            out.append((resolved, value))
            seen.add(resolved)
    if not out:
        for key in FALLBACK_KEYS:
            if key in judgment and key not in seen:
                out.append((key, judgment[key]))
                seen.add(key)
    return out


def _shares_ngram(a: str, b: str, n: int = 6) -> bool:
    if len(a) < n:
        return a and a in b
    for i in range(len(a) - n + 1):
        if a[i : i + n] in b:
            return True
    return False


def _resolve_evidence_findings(evidence: dict, combined_text: str):
    """回傳 [(ref, finding_dict), ...]。優先 axis.findings[idx] / axis#idx 精準比對，
    找不到時退回關鍵詞比對（axis_id 出現在文字中 → 掃該軸 findings 找 claim 有詞面重疊者）。
    """
    coverage = evidence.get("coverage", {})
    out = []
    seen = set()

    for m in EVIDENCE_REF_RE.finditer(combined_text or ""):
        axis = m.group(1)
        idx_s = m.group(2) or m.group(3)
        if axis not in coverage or idx_s is None:
            continue
        idx = int(idx_s)
        findings = coverage[axis].get("findings", [])
        if 0 <= idx < len(findings):
            ref = f"{axis}#{idx}"
            if ref not in seen:
                out.append((ref, findings[idx]))
                seen.add(ref)

    if not out:
        for axis, axis_obj in coverage.items():
            if axis in (combined_text or ""):
                for i, f in enumerate(axis_obj.get("findings", [])):
                    claim = f.get("claim", "")
                    if claim and _shares_ngram(claim, combined_text):
                        ref = f"{axis}#{i}"
                        if ref not in seen:
                            out.append((ref, f))
                            seen.add(ref)

    return out


def _built_in_template() -> str:
    return (
        "你是 stock-analyst v17 判斷 agent，回來做一輪定點修補。標的 {ticker}（{date}）。\n"
        "判斷物已由跨模型閘（gate）冷讀過，下面是它點名的判斷級發現。你的任務只有一件："
        "**針對被點名的欄位做最小修正**，不重寫判斷。\n\n"
        "## 讀\n\n`{judgment_path}`\n\n"
        "## 閘的發現（gate findings）\n\n{findings_block}\n\n"
        "## 修補紀律\n\n"
        "1. 只准改被點名的欄位；沒被點名的欄位一字不動。\n"
        "2. 裁決方向不由你主動翻；`judge check` 重算若自己翻面，照實接受並在回報點名。\n"
        "3. 可以不採納，但須在頂層 `evidence_dismissed[]` 補一條 "
        "{{\"ref\": \"...\", \"reason\": \"...\"}}；每一條 🔴 都必須有處置。\n"
        "4. 不得編造數字。\n"
        "5. 禁 WebSearch／WebFetch。\n\n"
        "## 寫（一次 Write 整檔）\n\n"
        "改完後把完整的 judgment.json 一次 Write 回 `{judgment_path}`，接著跑：\n\n"
        "```\npython3 scripts/ddreport.py judge check {ticker} {date}\n```\n\n"
        "FAIL → 只准改 FAIL 訊息點名的欄位，重跑同一條 `judge check`，≤1 輪。\n\n"
        "輪次上限 {max_turns} 輪。\n"
    )


def _build_findings_block(red_findings, judgment: dict, evidence: dict) -> str:
    blocks = []
    for n, f in enumerate(red_findings, 1):
        axis = f["axis"] or f"發現 {n}"
        note = f["note"] or "（無依據文字）"
        fix = f["fix"] or "（無明列建議改法，請依「依據」自行判斷修法）"
        path_field = f["path"] or ""

        subtree_parts = []
        for resolved, value in _resolve_judgment_subtrees(judgment, path_field):
            subtree_parts.append(f"`{resolved}`：\n```json\n{_dump(value)}\n```")
        subtree_text = "\n\n".join(subtree_parts) if subtree_parts else "（無法解析出對應子樹，指向欄位：%s）" % (path_field or "無")

        combined_text = f"{path_field}\n{note}"
        finding_parts = []
        for ref, ev_finding in _resolve_evidence_findings(evidence, combined_text):
            finding_parts.append(f"`{ref}`：\n```json\n{_dump(ev_finding)}\n```")
        finding_text = "\n\n".join(finding_parts) if finding_parts else "（未定位到對應 evidence finding）"

        block = (
            f"### 發現 {n}：{axis} 🔴\n"
            f"- **依據**：{note}\n"
            f"- **建議改法**：{fix}\n"
            f"- **指向欄位**：{path_field or '（未標）'}\n\n"
            f"**受影響子樹原文**：\n\n{subtree_text}\n\n"
            f"**相關 evidence finding 原文**：\n\n{finding_text}\n"
        )
        blocks.append(block)
    return "\n---\n\n".join(blocks) if blocks else "（本輪無 🔴 發現，僅供參考）"


def _compact_date(raw: str) -> str:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw or ""):
        return raw.replace("-", "")
    return raw or ""


def cmd_patch_prompt(args):
    parsed = parse_audit(args.audit)
    red_findings = [f for f in parsed["findings"] if f["level"] == RED]

    judgment = _load_json(args.judgment)
    evidence = _load_json(args.evidence)

    meta = judgment.get("meta", {}) if isinstance(judgment, dict) else {}
    ticker = args.ticker or meta.get("ticker") or ""
    date = args.date or _compact_date(meta.get("date", "")) or ""

    findings_block = _build_findings_block(red_findings, judgment, evidence)

    tmpl_path = Path(args.template) if args.template else DEFAULT_TMPL
    if tmpl_path.exists():
        tmpl_text = tmpl_path.read_text(encoding="utf-8")
    else:
        tmpl_text = _built_in_template()

    rendered = tmpl_text.format_map(
        {
            "ticker": ticker,
            "date": date,
            "run_dir": args.run_dir or "",
            "bundle_path": args.bundle_path or "",
            "judgment_path": args.judgment,
            "scenario_path": args.scenario_path or "",
            "audit_path": args.audit,
            "max_turns": args.max_turns,
            "findings_block": findings_block,
        }
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"WROTE {out_path}（🔴 {len(red_findings)} 條）")
    return 0


# ---------------------------------------------------------------------------
# decide
# ---------------------------------------------------------------------------

def cmd_decide(args):
    data = _load_json(args.parsed)
    red = int(data.get("red", 0) or 0)
    if red > 0:
        print("BLOCK")
        return 1
    print("PASS")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("parse", help="解析 gate audit md")
    pp.add_argument("audit")
    pp.add_argument("--json", action="store_true")
    pp.set_defaults(func=cmd_parse)

    pt = sub.add_parser("patch-prompt", help="產生修補 prompt")
    pt.add_argument("--audit", required=True)
    pt.add_argument("--judgment", required=True)
    pt.add_argument("--evidence", required=True)
    pt.add_argument("--out", required=True)
    pt.add_argument("--template", default=None, help="覆寫模板路徑（預設 scripts/dd_prompts/judge_patch.md.tmpl）")
    pt.add_argument("--ticker", default=None)
    pt.add_argument("--date", default=None, help="YYYYMMDD；未給則從 judgment.meta.date 推")
    pt.add_argument("--run-dir", default=None)
    pt.add_argument("--bundle-path", default=None)
    pt.add_argument("--scenario-path", default=None)
    pt.add_argument("--max-turns", type=int, default=6)
    pt.set_defaults(func=cmd_patch_prompt)

    pd = sub.add_parser("decide", help="印 BLOCK/PASS")
    pd.add_argument("parsed")
    pd.set_defaults(func=cmd_decide)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
