#!/usr/bin/env python3
"""scripts/dd2/spawn.py — dd2 LLM 通：包一層 `scripts/dd_headless.spawn`。

見 `scripts/dd2/README.md` §3（本檔契約）。只有兩種呼叫：
- `oneshot`：無工具、`max_turns=1`，供判斷／查詢用單輪呼叫。
- `agentic`：帶 `allowedTools`／`max_turns`，供查／寫兩用多輪呼叫。

不改 `scripts/dd_headless.py`。`thinking_cap` 以環境變數
`MAX_THINKING_TOKENS` 傳給子行程——`dd_headless.spawn` 呼叫
`subprocess.run(...)` 未帶 `env=`，子行程會繼承目前行程的 `os.environ`，
故在呼叫前後「暫時設、finally 還原」是不動 `dd_headless.py` 前提下最乾淨
的做法。是否真的生效（子行程有沒有讀這個變數）**未經驗證**，實測結果見
README §7。

Python 3.9 相容（`from __future__ import annotations`），純標準庫。
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import dd_headless  # noqa: E402

_MAX_THINKING_TOKENS_ENV = "MAX_THINKING_TOKENS"


def _sum_model_usage_field(model_usage, field, name_contains=None):
    """加總 `model_usage`（raw JSON 的 `modelUsage` dict）裡各模型 `field`。

    `name_contains` 給時只加總模型名稱（小寫後）含此子字串者，例如
    `"haiku"` 只挑 `claude-haiku-...` 這類鍵。
    """
    total = 0
    for name, v in (model_usage or {}).items():
        if name_contains and name_contains not in str(name).lower():
            continue
        try:
            total += int((v or {}).get(field, 0) or 0)
        except (TypeError, ValueError):
            pass
    return total


def _augment_with_raw_usage(result, out_json):
    """讀 `out_json` 原始檔，補 `thinking_tokens`／`haiku_input_tokens`。

    讀的是實際寫到磁碟的 raw JSON（而非 `result["by_model"]`），對齊
    README §3「從 out_json 原始檔的 modelUsage.*.thinkingTokens 取」。
    """
    result = dict(result)
    model_usage = {}
    if out_json:
        out_path = Path(out_json)
        if out_path.exists():
            try:
                raw = json.loads(out_path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    model_usage = raw.get("modelUsage") or {}
            except (json.JSONDecodeError, OSError):
                model_usage = {}
    result["thinking_tokens"] = _sum_model_usage_field(model_usage, "thinkingTokens")
    result["haiku_input_tokens"] = _sum_model_usage_field(
        model_usage, "inputTokens", name_contains="haiku"
    )
    return result


def oneshot(prompt_path, model, out_json, cwd, *, thinking_cap=None, budget_cache_read=None):
    """單輪、無工具呼叫（判斷／查詢用；`allowed_tools=None`、`max_turns=1`）。

    回傳 dict 同 `dd_headless.spawn`，另加 `thinking_tokens`／
    `haiku_input_tokens`（見 `_augment_with_raw_usage`）。
    """
    env_key = _MAX_THINKING_TOKENS_ENV
    had_prev = env_key in os.environ
    prev_val = os.environ.get(env_key)
    if thinking_cap is not None:
        os.environ[env_key] = str(thinking_cap)
    try:
        result = dd_headless.spawn(
            prompt_path=prompt_path,
            model=model,
            allowed_tools=None,
            max_turns=1,
            out_json=out_json,
            cwd=cwd,
            budget_cache_read=budget_cache_read,
        )
    finally:
        if thinking_cap is not None:
            if had_prev:
                os.environ[env_key] = prev_val
            else:
                os.environ.pop(env_key, None)
    return _augment_with_raw_usage(result, out_json)


def agentic(prompt_path, model, out_json, cwd, tools, max_turns, budget_cache_read=None, thinking_cap=None):
    """多輪、帶工具呼叫（查／寫兩通用；帶 `allowed_tools`＋`max_turns`）。

    回傳 dict 同 `oneshot`（含 `thinking_tokens`／`haiku_input_tokens`）。
    `thinking_cap`：同 oneshot，以 MAX_THINKING_TOKENS 環境變數暫設（2026-09-16 TXN 散文通實測
    sonnet 思考 95K token、只寫 22KB，故加上限）。
    """
    env_key = _MAX_THINKING_TOKENS_ENV
    had_prev = env_key in os.environ
    prev = os.environ.get(env_key)
    if thinking_cap is not None:
        os.environ[env_key] = str(thinking_cap)
    try:
        result = _agentic_inner(prompt_path, model, out_json, cwd, tools, max_turns, budget_cache_read)
    finally:
        if thinking_cap is not None:
            if had_prev:
                os.environ[env_key] = prev
            else:
                os.environ.pop(env_key, None)
    return result


def _agentic_inner(prompt_path, model, out_json, cwd, tools, max_turns, budget_cache_read):
    result = dd_headless.spawn(
        prompt_path=prompt_path,
        model=model,
        allowed_tools=tools,
        max_turns=max_turns,
        out_json=out_json,
        cwd=cwd,
        budget_cache_read=budget_cache_read,
    )
    return _augment_with_raw_usage(result, out_json)


_FENCE_RE = re.compile(r"```(?:json)?\s*\n(.*?)\n?```", re.S)


def strip_json(text):
    """把 LLM 回覆剝成可 `json.loads` 的字串。回 `(obj, error)`。

    順序：① 若有 ```json fence，先取 fence 內文字；② 直接整段 `json.loads`
    （處理純 JSON、或 fence 內剛好就是乾淨 JSON 的情況）；③ 失敗才找第一個
    `{` 或 `[` 到最後一個對應括號（`{`→`}`、`[`→`]`），剝掉前後說明文字後
    再 parse 一次。全部失敗回 `(None, 錯誤訊息)`。
    """
    if text is None:
        return None, "empty text"

    working = text
    m = _FENCE_RE.search(text)
    if m:
        working = m.group(1)

    stripped = working.strip()
    if not stripped:
        return None, "empty after strip"

    try:
        return json.loads(stripped), None
    except json.JSONDecodeError:
        pass

    start = None
    for i, ch in enumerate(stripped):
        if ch in "{[":
            start = i
            break
    if start is None:
        return None, "no opening bracket found"

    open_ch = stripped[start]
    close_ch = "}" if open_ch == "{" else "]"
    end = stripped.rfind(close_ch)
    if end == -1 or end <= start:
        return None, "no matching closing bracket found"

    snippet = stripped[start:end + 1]
    try:
        return json.loads(snippet), None
    except json.JSONDecodeError as e:
        return None, "json.loads failed: {0}".format(e)

# ---------------------------------------------------------------------------
# 串流版單輪（2026-09-17 MU 案例）：`--output-format json` 只回最後一則 assistant 文字，
# Fable 思考 41K＋JSON 23K 撞到 64K 單則上限被切兩則時，程式只拿到 JSON 尾巴。
# 改 `stream-json --verbose`，把所有 assistant 文字塊接起來；usage 從最後的 result 事件取。
# 指令列旗標與 dd_headless 同一組（slim／--tools ""），不改 dd_headless.py。
# ---------------------------------------------------------------------------

def _stream_cmd(model, max_turns, extra_args=None):
    cmd = [dd_headless._claude_bin() if hasattr(dd_headless, "_claude_bin") else os.environ.get("DD_CLAUDE_BIN", "claude"),
           "-p", "--model", model, "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns)]
    if dd_headless._slim_enabled():
        cmd.extend(dd_headless.SLIM_ARGS)
    if not (extra_args and "--tools" in list(extra_args)):
        cmd.extend(["--tools", ""])
    if extra_args:
        cmd.extend(list(extra_args))
    return cmd


def oneshot_stream(prompt_path, model, out_json, cwd, *, thinking_cap=None, budget_cache_read=None,
                   extra_args=None, timeout_s=3600):
    """無工具單輪，串流收集所有 assistant 文字。回傳 dict 同 oneshot，另加 `stitched_parts`（接了幾則）。"""
    import subprocess, time as _time
    prompt_text = Path(prompt_path).read_text(encoding="utf-8")
    env_key = _MAX_THINKING_TOKENS_ENV
    had_prev = env_key in os.environ
    prev = os.environ.get(env_key)
    if thinking_cap is not None:
        os.environ[env_key] = str(thinking_cap)
    t0 = _time.time()
    try:
        proc = subprocess.run(_stream_cmd(model, 1, extra_args), input=prompt_text, capture_output=True,
                              text=True, cwd=str(cwd) if cwd else None, timeout=timeout_s)
    finally:
        if thinking_cap is not None:
            if had_prev:
                os.environ[env_key] = prev
            else:
                os.environ.pop(env_key, None)
    texts, result_ev, n_assist = [], None, 0
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            content = (ev.get("message") or {}).get("content") or []
            t = "".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
            if t:
                texts.append(t)
                n_assist += 1
        elif ev.get("type") == "result":
            result_ev = ev
    stitched = "".join(texts)
    result_ev = result_ev or {}
    usage = result_ev.get("usage") or {}
    mu = result_ev.get("modelUsage") or {}
    rec = {
        "ok": proc.returncode == 0 and bool(stitched) and result_ev.get("subtype", "success") == "success",
        "result_text": stitched, "stitched_parts": n_assist,
        "num_turns": result_ev.get("num_turns"),
        "output_tokens": usage.get("output_tokens"),
        "cache_read": usage.get("cache_read_input_tokens"),
        "cache_creation": usage.get("cache_creation_input_tokens"),
        "cost_usd": result_ev.get("total_cost_usd"),
        "duration_ms": result_ev.get("duration_ms") or int((_time.time() - t0) * 1000),
        "thinking_tokens": sum((v.get("thinkingTokens") or 0) for v in mu.values() if isinstance(v, dict)),
        "haiku_input_tokens": sum((v.get("inputTokens") or 0) for k, v in mu.items() if "haiku" in k and isinstance(v, dict)),
        "over_budget": bool(budget_cache_read and (usage.get("cache_read_input_tokens") or 0) > budget_cache_read),
        "raw_path": str(out_json), "returncode": proc.returncode,
        "stderr_tail": (proc.stderr or "")[-500:],
    }
    if out_json:
        Path(out_json).parent.mkdir(parents=True, exist_ok=True)
        Path(out_json).write_text(json.dumps({"result_event": result_ev, "stitched_text": stitched,
                                              "stitched_parts": n_assist, "cmd_effort": extra_args},
                                             ensure_ascii=False, indent=1), encoding="utf-8")
    return rec
