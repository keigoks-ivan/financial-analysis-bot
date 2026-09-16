#!/usr/bin/env python3
"""2026-09-11：Codex CLI 的直接回傳轉接，僅供已收齊證據的研究／審核。

官方契約：https://learn.chatgpt.com/docs/non-interactive-mode
本機 codex exec --help 已核對參數。離線測試不啟動模型；不切換 API 或登入方式。
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import uuid

MODELS = ("gpt-5.6-sol", "gpt-5.6-terra", "gpt-6-astra")


def spawn(prompt_path, model, out_json, budget_cache_read=None):
    if model not in MODELS:
        raise ValueError("未驗證的研究模型：" + str(model))
    call_id = uuid.uuid4().hex
    requested = Path(out_json)
    raw_path = requested.with_name(requested.stem + "_" + call_id + ".json")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    prompt = Path(prompt_path).read_text(encoding="utf-8")
    prompt = ("本次只依提供材料作答，禁止任何工具、搜尋、檔案讀寫或委派。"
              "僅回傳要求的完整結果，程式負責存檔與驗證。\n\n" + prompt)
    started = time.monotonic()
    # 2026-09-11：獨立空目錄與獨立 session，避免審核沿用作者對話或 repo 指令。
    with tempfile.TemporaryDirectory(prefix="dd-codex-") as work:
        output = Path(work) / "result.txt"
        cmd = [os.environ.get("DD_CODEX_BIN", "codex"), "exec", "--ignore-user-config",
               "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
               "--model", model, "-c", 'model_reasoning_effort="high"',
               "--json", "--output-last-message", str(output), "-"]
        try:
            proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=work)
            stdout, stderr, returncode = proc.stdout or "", proc.stderr or "", proc.returncode
        except OSError as exc:
            stdout, stderr, returncode = "", str(exc), -1
        result = output.read_text(encoding="utf-8") if output.exists() else ""
    events, errors = [], []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError("event 必須是 object")
            events.append(event)
        except ValueError as exc:
            errors.append("無法解析 CLI event：" + str(exc))
    completed = [e for e in events if e.get("type") == "turn.completed"]
    if len(completed) != 1:
        errors.append("必須有一次完整 turn.completed")
    for event in events:
        if event.get("type") in ("error", "turn.failed"):
            errors.append(str(event))
        item = event.get("item") or {}
        if item and item.get("type") not in ("agent_message", "reasoning"):
            errors.append("純研究回傳不可呼叫工具：" + str(item.get("type")))
    usage = completed[-1].get("usage") or {} if completed else {}
    counts = {key: usage.get(key) for key in ("input_tokens", "cached_input_tokens", "output_tokens")}
    if not all(isinstance(x, int) and not isinstance(x, bool) and x >= 0 for x in counts.values()):
        errors.append("缺少有效用量，不能把未知用量記為零")
    total, cached, output_tokens = (counts[k] for k in ("input_tokens", "cached_input_tokens", "output_tokens"))
    if isinstance(total, int) and isinstance(cached, int) and cached > total:
        errors.append("cached_input_tokens 不得大於 input_tokens")
    fresh = total - cached if isinstance(total, int) and isinstance(cached, int) else None
    raw_path.write_text(json.dumps({"call_id": call_id, "model": model, "events": events,
        "stdout": stdout, "stderr": stderr, "returncode": returncode,
        "result": result, "errors": errors}, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": returncode == 0 and bool(result.strip()) and not errors,
            "provider": "codex_cli", "call_id": call_id, "raw_path": str(raw_path),
            "result_text": result, "num_turns": len(completed), "input_tokens": fresh,
            "cache_read": cached, "cache_creation": None, "output_tokens": output_tokens,
            "thinking_tokens": usage.get("reasoning_output_tokens"),
            "cost_usd": None, "cost_available": False,
            "usage_note": "cached input 已包含於 input；思考已包含於 output；CLI 不提供美元費用。",
            "by_model": {model: {"inputTokens": fresh, "cacheReadInputTokens": cached,
                         "outputTokens": output_tokens, "costUSD": None}},
            "duration_ms": round((time.monotonic() - started) * 1000),
            "over_budget": bool(budget_cache_read is not None and cached is not None and cached > budget_cache_read),
            "quota_exhausted": any(term in (stdout + stderr).lower() for term in
                                   ("usage limit", "quota exceeded", "rate limit")),
            "errors": errors}
