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


def agentic(prompt_path, model, out_json, cwd, tools, max_turns, budget_cache_read=None):
    """多輪、帶工具呼叫（查／寫兩通用；帶 `allowed_tools`＋`max_turns`）。

    回傳 dict 同 `oneshot`（含 `thinking_tokens`／`haiku_input_tokens`）。
    """
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
