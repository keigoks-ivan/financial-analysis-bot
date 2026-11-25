#!/usr/bin/env python3
"""dd5 的 opus 呼叫外殼：牆鐘上限、超時改 --effort low 重試一次、再超時就 FAIL。

底層用 scripts/dd2/spawn.py 的 oneshot_stream（subprocess.run(timeout=)，超時會殺子行程）。
不改 scripts/dd2/spawn.py。

可選參數（預設都不開）：
- 環境變數 DD5_MAX_OUTPUT_TOKENS：轉成 CLAUDE_CODE_MAX_OUTPUT_TOKENS 給子行程。
  依據：claude 執行檔（2.1.x）內含這個變數名稱與說明字串
  「Set CLAUDE_CODE_MAX_OUTPUT_TOKENS to pick a different limit」（只讀二進位字串，沒有實際呼叫測過）。
- 環境變數 DD5_MAX_BUDGET_USD：轉成 `--max-budget-usd`（claude --help 有列，只在 --print 模式有效）。
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent), str(HERE.parent / "dd2")):
    if p not in sys.path:
        sys.path.insert(0, p)

import spawn as sp  # noqa: E402

# 估算被殺掉那通的花費：本次試跑實測 opus 暴衝 884～943 秒約 $3.9（約 $0.0043/秒）
EST_USD_PER_SEC = {"opus": 0.0043, "sonnet": 0.0015}


NEUTRAL_CWD = Path("/private/tmp/dd5_neutral_cwd")


class StepTimeout(Exception):
    pass


def _once(prompt_path, model, out_json, cwd, effort, timeout_s):
    extra = ["--include-partial-messages", "--setting-sources", "project"]  # 後者蓋掉 dd2 的 user：不帶入持有人的全域 CLAUDE.md（約 1.2 萬 token、與寫報告無關）  # 串流逐段輸出，被中止時才留得下已產生的內容
    if effort:
        extra += ["--effort", effort]
    if os.environ.get("DD5_MAX_BUDGET_USD"):
        extra += ["--max-budget-usd", os.environ["DD5_MAX_BUDGET_USD"]]
    env_key = "CLAUDE_CODE_MAX_OUTPUT_TOKENS"
    prev = os.environ.get(env_key)
    if os.environ.get("DD5_MAX_OUTPUT_TOKENS"):
        os.environ[env_key] = os.environ["DD5_MAX_OUTPUT_TOKENS"]
    t0 = time.time()
    try:
        # 工作目錄改到家目錄以外的空資料夾：run 目錄在 ~ 底下時，claude 會把 ~/.claude/CLAUDE.md
        # 當成上層專案的 CLAUDE.md 讀進來（--setting-sources project 擋不住），模型就照裡面的
        # 「寫中文先載入 skill」規則吐出上百段假工具呼叫（2026-11-24 五檔試跑 4 檔中招）。
        NEUTRAL_CWD.mkdir(parents=True, exist_ok=True)
        r = sp.oneshot_stream(str(Path(prompt_path).resolve()), model, str(Path(out_json).resolve()), NEUTRAL_CWD,
                              extra_args=extra or None, timeout_s=timeout_s)
        r["effort"] = effort
        n_fake = (r.get("result_text") or "").count("<invoke name=")
        if n_fake >= 3:  # 沒有工具的呼叫卻寫出工具呼叫＝被外來規則帶偏，這份輸出不能用
            r["ok"] = False
            r["fake_tool_calls"] = n_fake
        return r, None
    except subprocess.TimeoutExpired as e:
        secs = time.time() - t0
        try:  # 把被中止前已收到的串流存下來，事後才看得出它在想還是卡住
            part = e.stdout or b""
            if isinstance(part, str):
                part = part.encode("utf-8", "replace")
            Path(str(out_json).replace(".json", "_killed_{0}.jsonl".format(effort or "none"))).write_bytes(part)
        except Exception:
            pass
        return None, {"effort": effort, "timeout_s": timeout_s, "seconds": round(secs, 1),
                      "est_cost_usd": round(secs * EST_USD_PER_SEC.get(model, 0.004), 2)}
    finally:
        if os.environ.get("DD5_MAX_OUTPUT_TOKENS"):
            if prev is None:
                os.environ.pop(env_key, None)
            else:
                os.environ[env_key] = prev


def call(prompt_path, model, out_json, cwd, effort, timeout_s, on_timeout=None):
    """回傳 (結果 dict, 超時紀錄 list)。第一次超時以 effort=low 重試；再超時丟 StepTimeout。
    on_timeout(info) 讓呼叫端把被殺掉那通記進 manifest。"""
    kills = []
    r, k = _once(prompt_path, model, out_json, cwd, effort, timeout_s)
    if r is not None:
        return r, kills
    kills.append(k)
    if on_timeout:
        on_timeout(k)
    if os.environ.get("DD5_NO_RETRY"):
        raise StepTimeout("超過 {0} 秒，DD5_NO_RETRY 已設，不重試".format(timeout_s))
    r, k = _once(prompt_path, model, out_json, cwd, "low", timeout_s)
    if r is not None:
        r["retried_after_timeout"] = True
        return r, kills
    kills.append(k)
    if on_timeout:
        on_timeout(k)
    raise StepTimeout("兩次都超過 {0} 秒（第二次已改 --effort low），該步 FAIL".format(timeout_s))
