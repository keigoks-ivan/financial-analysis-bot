#!/usr/bin/env python3
"""dd_headless.py — v17 WP1c 無頭執行器。

把「呼叫一次 `claude -p` 子 agent」與「平行呼叫多個」包成兩個函式
（`spawn` / `spawn_many`）＋一支 CLI，給 `ddreport.py`（WP1a／WP1d）
串批次用。Python 3.9 相容（`from __future__ import annotations`，不用
3.10+ 執行期語法）。

實作選擇（規格允許擇一，此檔選 stdin）
--------------------------------------
prompt 內容透過「子行程 stdin」傳入 `claude -p`（不是拼進 argv 的
positional 參數）。理由：prompts/ 底下的批次檔可能相當大（覆蓋面掃描
+ 逐字稿摘要等），走 argv 有 shell/OS ARG_MAX 風險；stdin 沒有這個
上限，且已用 `echo "只回 OK" | claude -p --model sonnet --max-turns 1
--output-format json` 實測可行（見下方實測記錄）。呼叫的子行程本身
仍是 `[claude, -p, --model, M, --output-format, json, --max-turns, N,
--allowedTools, t1, t2, ...]`（+ `extra_args`），prompt 用
`subprocess.run(..., input=prompt_text)` 餵進去，不經過 shell。

binary 覆寫：環境變數 `DD_CLAUDE_BIN`（預設 `claude`）——測試用假
binary 指這裡。

已知回傳 JSON 形狀（2026-09-05 實測樣本，供假 binary／測試 fixture
比對）：
    {"type":"result","is_error":false,"num_turns":3,"duration_ms":11692,
     "total_cost_usd":0.0915,
     "result":"Bloom Energy 2026 年 Q2 營收 10.65 億美元 …",
     "usage":{"input_tokens":6,"cache_creation_input_tokens":12597,
               "cache_read_input_tokens":77719,"output_tokens":297},
     "modelUsage":{
       "claude-haiku-4-5-20251001":{"inputTokens":10371,"outputTokens":446,
         "cacheReadInputTokens":0,"cacheCreationInputTokens":0,
         "webSearchRequests":1,"costUSD":0.0226},
       "claude-sonnet-5":{"inputTokens":6,"outputTokens":297,
         "cacheReadInputTokens":77719,"cacheCreationInputTokens":12597,
         "webSearchRequests":0,"costUSD":0.0689}}}

兩個實測（2026-09-05，本機 `claude` 2.1.258；每次 `--max-turns 1`、
prompt 固定「只回 OK」、model sonnet）
--------------------------------------------------------------------
(i) 預設（載入 user+project+local，含本 repo 龐大的專案 CLAUDE.md）
    vs `--setting-sources user`（只載 user 設定，略過專案 CLAUDE.md）
    ——實測兩次，經 `scripts/dd_headless.py` CLI 本身跑出：
      - 預設：`cache_read_input_tokens = 18534`，
        `cache_creation_input_tokens = 42610`。
      - `--setting-sources user`：`cache_read_input_tokens = 18534`
        （**與預設相同，未觀察到差異**），
        `cache_creation_input_tokens = 13841`（明顯較小）。
    據實記錄：spec 原假設「`--setting-sources user` 會壓低
    `cache_read_input_tokens`（基準約 78K）」在本機兩次真實呼叫中
    **未成立**——兩次 cache_read 完全相同（18534，應是命中某個與
    CLAUDE.md 無關、本機環境已預熱的共用前綴快取）。真正隨
    `--setting-sources user` 顯著縮小的是 `cache_creation_input_tokens`
    （42610→13841），方向與「略過專案 CLAUDE.md」一致，但體現在
    *寫入*而非*讀取*這個欄位上；若要驗證讀取端的差異需要一個乾淨、
    從未跑過這個 prefix 的冷啟動環境，本輪未做（受 3 次真實呼叫
    額度限制）。回報時的「cache_read 數字」據此如實列出上述兩個
    18534，並註明差異其實落在 cache_creation。
(ii) `--model fable`：`claude -p --help` 的 `--model` 說明原文為
    "Provide an alias for the latest model (e.g. 'fable', 'opus', or
    'sonnet') or a model's full name"——CLI 文件本身已把 'fable' 列為
    合法別名，故未再耗用第三次真實呼叫額度去驗證；旗標層級判定：
    **接受**。若要看 `modelUsage` 實際回傳的規範化模型名稱（例如是否
    正規化成某個 `claude-fable-5-...` 字串），需另一次真實呼叫，此
    輪未做（3 次真實呼叫額度：上面 (i) 兩次＋CLI 驗收 1 次，已滿）。
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_CLAUDE_BIN = "claude"


def _claude_bin() -> str:
    return os.environ.get("DD_CLAUDE_BIN", DEFAULT_CLAUDE_BIN)


def _sum_model_usage_field(model_usage, field):
    total = 0
    for v in (model_usage or {}).values():
        try:
            total += int(v.get(field, 0) or 0)
        except (TypeError, ValueError):
            pass
    return total


def spawn(
    prompt_path,
    model,
    allowed_tools=None,
    max_turns=10,
    budget_cache_read=None,
    out_json=None,
    cwd=None,
    extra_args=None,
):
    """呼叫一次 `claude -p`，回傳整理後的量測 dict。

    Args:
        prompt_path: prompt 檔路徑（內容以 stdin 餵給子行程）。
        model: `--model` 值（如 "sonnet"、"opus"、"fable"）。
        allowed_tools: 傳給 `--allowedTools` 的工具名稱清單，None/空
            則不帶這個旗標。
        max_turns: `--max-turns` 值。
        budget_cache_read: cache_read token 預算；超過則
            `over_budget=True`。None 表示不設預算（恆 False）。
        out_json: 原始回傳 JSON 要寫到哪個檔。
        cwd: 子行程工作目錄，None 用目前目錄。
        extra_args: 附加在指令尾端的原始 CLI 參數（例如
            `["--setting-sources", "user"]`）。

    Returns:
        dict：`ok`／`num_turns`／`cache_read`／`cache_creation`／
        `output_tokens`／`by_model`／`over_budget`／`cost_usd`／
        `duration_ms`／`result_text`／`raw_path`。
    """
    prompt_path = Path(prompt_path)
    prompt_text = prompt_path.read_text(encoding="utf-8")

    cmd = [
        _claude_bin(),
        "-p",
        "--model",
        str(model),
        "--output-format",
        "json",
        "--max-turns",
        str(max_turns),
    ]
    if allowed_tools:
        cmd.append("--allowedTools")
        cmd.extend(list(allowed_tools))
    if extra_args:
        cmd.extend(list(extra_args))

    proc = subprocess.run(
        cmd,
        input=prompt_text,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
    )

    stdout = (proc.stdout or "").strip()
    try:
        raw = json.loads(stdout) if stdout else {}
        if not isinstance(raw, dict):
            raise ValueError("top-level JSON is not an object")
        parse_error = False
    except (json.JSONDecodeError, ValueError):
        raw = {
            "type": "result",
            "is_error": True,
            "result": stdout or (proc.stderr or "").strip(),
        }
        parse_error = True

    if out_json:
        out_path = Path(out_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        raw_path = str(out_path)
    else:
        raw_path = None

    model_usage = raw.get("modelUsage") or {}
    if model_usage:
        cache_read = _sum_model_usage_field(model_usage, "cacheReadInputTokens")
        cache_creation = _sum_model_usage_field(model_usage, "cacheCreationInputTokens")
        output_tokens = _sum_model_usage_field(model_usage, "outputTokens")
    else:
        usage = raw.get("usage") or {}
        cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
        cache_creation = int(usage.get("cache_creation_input_tokens", 0) or 0)
        output_tokens = int(usage.get("output_tokens", 0) or 0)

    is_error = bool(raw.get("is_error", False)) or parse_error or (proc.returncode != 0)
    # 訂閱額度耗盡（2026-09-05 批次實測：result＝"You've hit your session limit · resets 8:50pm"）：
    # 不是 agent 失敗，標 quota_exhausted 讓上層明確停下、等重置再 resume。
    _rtxt = str(raw.get("result") or "")
    quota_exhausted = ("hit your session limit" in _rtxt) or ("usage limit" in _rtxt.lower() and "reset" in _rtxt.lower())
    if quota_exhausted:
        is_error = True
        print("[quota] 訂閱額度耗盡：" + _rtxt[:120], file=sys.stderr)
    # 母稿 §4.1：budget 是目標值，熔斷線＝目標 2×；超過目標只記 over_target（回報用），
    # 超過 2× 才 over_budget 停流程（WDAY 2026-09-05：一篇摘要 0.77M 對 0.7M 目標就停，屬誤停）。
    over_target = (budget_cache_read is not None) and (cache_read > budget_cache_read)
    over_budget = (budget_cache_read is not None) and (cache_read > 2 * budget_cache_read)

    return {
        "ok": not is_error,
        "num_turns": raw.get("num_turns"),
        "cache_read": cache_read,
        "cache_creation": cache_creation,
        "output_tokens": output_tokens,
        "by_model": model_usage,
        "over_budget": over_budget,
        "over_target": over_target,
        "quota_exhausted": quota_exhausted,
        "cost_usd": raw.get("total_cost_usd"),
        "duration_ms": raw.get("duration_ms"),
        "result_text": raw.get("result"),
        "raw_path": raw_path,
    }


def spawn_many(specs, max_parallel=4):
    """平行執行多個 `spawn` 呼叫，回傳結果 list（順序 = specs 順序）。

    spec 形狀＝WP1a `spawn_list.json` 元素＋`run_dir`：
        {id, model, prompt, out, tools, max_turns, budget_cache_read,
         run_dir}
    `prompt`／`out` 若非絕對路徑，視為相對 `run_dir` 解析。
    """
    n = len(specs)
    results: List[Optional[Dict[str, Any]]] = [None] * n

    def _run(idx, spec):
        run_dir = spec.get("run_dir")
        prompt_path = spec["prompt"]
        out_json = spec.get("out")
        if run_dir:
            if not os.path.isabs(prompt_path):
                prompt_path = os.path.join(run_dir, prompt_path)
            if out_json and not os.path.isabs(out_json):
                out_json = os.path.join(run_dir, out_json)
        r = spawn(
            prompt_path=prompt_path,
            model=spec.get("model", "sonnet"),
            allowed_tools=spec.get("tools"),
            max_turns=spec.get("max_turns", 10),
            budget_cache_read=spec.get("budget_cache_read"),
            out_json=out_json,
            cwd=run_dir,
            extra_args=spec.get("extra_args"),
        )
        r = dict(r)
        r["id"] = spec.get("id")
        return idx, r

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel) as ex:
        futures = [ex.submit(_run, i, spec) for i, spec in enumerate(specs)]
        for fut in concurrent.futures.as_completed(futures):
            idx, r = fut.result()
            results[idx] = r

    return results


def _build_arg_parser():
    p = argparse.ArgumentParser(prog="dd_headless.py")
    p.add_argument("--prompt", required=True, help="prompt 檔路徑")
    p.add_argument("--model", default="sonnet")
    p.add_argument("--tools", nargs="*", default=None, help="傳給 --allowedTools 的工具名稱")
    p.add_argument("--max-turns", type=int, default=10)
    p.add_argument("--budget", dest="budget_cache_read", type=int, default=None)
    p.add_argument("--out", required=True, help="原始回傳 JSON 輸出路徑")
    p.add_argument("--setting-sources", default=None, help="轉傳給 claude 的 --setting-sources")
    p.add_argument("--cwd", default=None)
    return p


def main(argv=None):
    args = _build_arg_parser().parse_args(argv)

    extra_args = []
    if args.setting_sources:
        extra_args.extend(["--setting-sources", args.setting_sources])

    result = spawn(
        prompt_path=args.prompt,
        model=args.model,
        allowed_tools=args.tools,
        max_turns=args.max_turns,
        budget_cache_read=args.budget_cache_read,
        out_json=args.out,
        cwd=args.cwd,
        extra_args=extra_args,
    )

    print(
        "{model}／{turns}／{cache_read}／{output}／{over_budget}".format(
            model=args.model,
            turns=result["num_turns"],
            cache_read=result["cache_read"],
            output=result["output_tokens"],
            over_budget=result["over_budget"],
        )
    )
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
