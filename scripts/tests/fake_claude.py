#!/usr/bin/env python3
"""假 `claude` binary，供 test_dd_headless.py 經 `DD_CLAUDE_BIN` 指到這裡。

行為：
- 讀 stdin（dd_headless.spawn 把 prompt 內容從 stdin 餵進來）。
- 若 stdin 內容第一行是 `SLEEP:<seconds>`，先 sleep 該秒數再回應——用來
  在 spawn_many 的平行測試裡刻意製造「後送出的先完成」，驗證回傳順序
  仍照 specs 原始順序而非完成順序。
- 若環境變數 `FAKE_CLAUDE_RESPONSE` 有設，直接把該路徑檔案內容原樣印到
  stdout（用來餵固定 fixture，如已知回傳形狀樣本／is_error 樣本）。
- 否則印一個預設的成功回應，`result` 欄位回填收到的 stdin 全文，方便
  測試比對「這個結果是哪一個 spec 送出去的」。
- 若有設 `FAKE_CLAUDE_LOG`，把這次呼叫的 argv 與 stdin 追加寫入該檔
  （每行一個 JSON），供需要時檢查實際傳給 claude 的參數。
"""
from __future__ import annotations

import json
import os
import sys
import time


def main():
    data = sys.stdin.read()

    if data.startswith("SLEEP:"):
        first_line = data.splitlines()[0] if data.splitlines() else data
        try:
            sleep_s = float(first_line.split(":", 1)[1].strip())
        except (IndexError, ValueError):
            sleep_s = 0.0
        if sleep_s > 0:
            time.sleep(sleep_s)

    log_path = os.environ.get("FAKE_CLAUDE_LOG")
    if log_path:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"argv": sys.argv[1:], "stdin": data}, ensure_ascii=False) + "\n")

    resp_path = os.environ.get("FAKE_CLAUDE_RESPONSE")
    if resp_path:
        with open(resp_path, "r", encoding="utf-8") as fh:
            sys.stdout.write(fh.read())
    else:
        payload = {
            "type": "result",
            "is_error": False,
            "num_turns": 1,
            "duration_ms": 100,
            "total_cost_usd": 0.001,
            "result": data,
            "usage": {
                "input_tokens": 1,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "output_tokens": 1,
            },
            "modelUsage": {
                "claude-sonnet-5": {
                    "inputTokens": 1,
                    "outputTokens": 1,
                    "cacheReadInputTokens": 0,
                    "cacheCreationInputTokens": 0,
                    "webSearchRequests": 0,
                    "costUSD": 0.001,
                }
            },
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
