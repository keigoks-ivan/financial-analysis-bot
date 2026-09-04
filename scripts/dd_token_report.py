#!/usr/bin/env python3
"""dd_token_report.py — v16.2 分模型計量（0 LLM token）。

讀一個 Claude Code session 目錄下的 `subagents/agent-*.meta.json`＋對應 `.jsonl`，
依每個 sub-agent 的 `model` 欄位（fable／opus／sonnet／其他）分桶加總
cache_read / cache_creation / output tokens，供 ddreport v16.2「分模型計量」段回填
（v16.2 目標：Fable 每份 ≤8M、opus／sonnet 另計）。

用法：
  python3 scripts/dd_token_report.py SESSION_ID
      → 預設在 ~/.claude/projects/{slug}/{SESSION_ID}/subagents/ 找，
        {slug} 由目前工作目錄機械換算（"/" 換成 "-"，等同 Claude Code 專案目錄命名慣例）。
  python3 scripts/dd_token_report.py SESSION_ID --projects-root ~/.claude/projects
  python3 scripts/dd_token_report.py --session-dir /path/to/{SESSION_ID}
  python3 scripts/dd_token_report.py ... --json          # 機器可讀輸出
  python3 scripts/dd_token_report.py ... --filter panw    # 只算 description 含此字串（不分大小寫）的 agent

去重規則：同一 assistant message 在 jsonl 內會因串流重複出現多筆 usage 快照
（cache_read/cache_creation 通常不變、output_tokens 遞增）——本腳本以 `message.id`
為 key，同一 id 只取 output_tokens 最大的一筆，再跨 message id 加總，避免同一輪
被算多次。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MODEL_BUCKETS = ["fable", "opus", "sonnet"]


def default_project_slug(cwd: Path) -> str:
    return str(cwd).replace("/", "-")


def resolve_session_dir(args) -> Path:
    if args.session_dir:
        return Path(args.session_dir).expanduser()
    if not args.session_id:
        raise SystemExit("需要 SESSION_ID 或 --session-dir")
    projects_root = Path(args.projects_root).expanduser() if args.projects_root else Path.home() / ".claude" / "projects"
    slug = default_project_slug(Path.cwd())
    candidate = projects_root / slug / args.session_id
    if candidate.exists():
        return candidate
    # 退回：在 projects_root 下找任一目錄含此 session id 的子資料夾（cwd 換算的 slug 猜錯時的救援）
    hits = list(projects_root.glob(f"*/{args.session_id}"))
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        raise SystemExit(f"session id 在多個專案目錄命中，請用 --session-dir 指定：{hits}")
    raise SystemExit(f"找不到 session 目錄：{candidate}（且 {projects_root} 下無其他命中）")


def dedup_sum(jsonl_path: Path) -> dict:
    """回傳 {"cache_read":n, "cache_creation":n, "output":n, "input":n, "messages":n}。"""
    best_by_id: dict[str, dict] = {}
    try:
        lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return {"cache_read": 0, "cache_creation": 0, "output": 0, "input": 0, "messages": 0, "error": str(e)}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") != "assistant":
            continue
        msg = rec.get("message") or {}
        usage = msg.get("usage") or {}
        if not usage:
            continue
        mid = msg.get("id") or rec.get("uuid")
        out_tok = usage.get("output_tokens", 0) or 0
        prev = best_by_id.get(mid)
        if prev is None or out_tok >= prev.get("output_tokens", 0):
            best_by_id[mid] = usage

    totals = {"cache_read": 0, "cache_creation": 0, "output": 0, "input": 0, "messages": len(best_by_id)}
    for usage in best_by_id.values():
        totals["cache_read"] += usage.get("cache_read_input_tokens", 0) or 0
        totals["cache_creation"] += usage.get("cache_creation_input_tokens", 0) or 0
        totals["output"] += usage.get("output_tokens", 0) or 0
        totals["input"] += usage.get("input_tokens", 0) or 0
    return totals


def bucket_for_model(model: str) -> str:
    m = (model or "").strip().lower()
    for b in MODEL_BUCKETS:
        if b in m:
            return b
    return "other"


def collect(session_dir: Path, name_filter: str | None):
    sub_dir = session_dir / "subagents"
    if not sub_dir.exists():
        raise SystemExit(f"{sub_dir} 不存在（session 內尚無 sub-agent，或路徑不對）")
    rows = []
    for meta_path in sorted(sub_dir.glob("agent-*.meta.json")):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        desc = meta.get("description", "")
        if name_filter and name_filter.lower() not in desc.lower():
            continue
        model = meta.get("model", "?")
        # meta_path = agent-X.meta.json → jsonl = agent-X.jsonl
        jsonl_path = sub_dir / (meta_path.name.replace(".meta.json", ".jsonl"))
        totals = dedup_sum(jsonl_path) if jsonl_path.exists() else {
            "cache_read": 0, "cache_creation": 0, "output": 0, "input": 0, "messages": 0,
            "error": "jsonl 不存在",
        }
        rows.append({
            "agent_file": meta_path.name.replace(".meta.json", ""),
            "description": desc,
            "model": model,
            "bucket": bucket_for_model(model),
            **totals,
        })
    return rows


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("session_id", nargs="?")
    ap.add_argument("--session-dir")
    ap.add_argument("--projects-root")
    ap.add_argument("--filter", help="只算 description 含此字串（不分大小寫）的 agent，如 ticker 名")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    session_dir = resolve_session_dir(args)
    rows = collect(session_dir, args.filter)

    bucket_totals = {b: {"cache_read": 0, "cache_creation": 0, "output": 0, "agents": 0} for b in MODEL_BUCKETS + ["other"]}
    for r in rows:
        bt = bucket_totals[r["bucket"]]
        bt["cache_read"] += r["cache_read"]
        bt["cache_creation"] += r["cache_creation"]
        bt["output"] += r["output"]
        bt["agents"] += 1

    if args.json:
        print(json.dumps({"session_dir": str(session_dir), "rows": rows, "bucket_totals": bucket_totals},
                          ensure_ascii=False, indent=2))
        return 0

    print(f"session_dir={session_dir}")
    print(f"{'agent':22s} {'model':8s} {'description':40s} {'cache_read':>12s} {'cache_create':>13s} {'output':>10s}")
    for r in rows:
        print(f"{r['agent_file']:22s} {r['model']:8s} {r['description'][:40]:40s} "
              f"{r['cache_read']:>12,d} {r['cache_creation']:>13,d} {r['output']:>10,d}"
              + ("  [ERR: " + r["error"] + "]" if r.get("error") else ""))
    print("\n—— 分模型三欄加總（v16.2 分模型計量） ——")
    for b in MODEL_BUCKETS + ["other"]:
        bt = bucket_totals[b]
        if bt["agents"] == 0:
            continue
        print(f"  {b:8s}  agents={bt['agents']:<3d} cache_read={bt['cache_read']:>12,d}  "
              f"cache_creation={bt['cache_creation']:>12,d}  output={bt['output']:>10,d}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
