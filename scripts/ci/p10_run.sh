#!/usr/bin/env bash
# P10 價格動能建置的重試包裝（2026-11-03）。
# 用法：bash scripts/ci/p10_run.sh <最多幾次> <每次間隔秒數> <指令…>
# 程式結束碼（見 scripts/p10_price_integrity.py）：
#   0 成功；2 安全機制觸發、track.json 沒寫 → 等一下重跑；3 已寫入但有暫估列太久 → 不重跑。
# 其他非 0 也不重跑。最後的結束碼原樣回傳，呼叫的步驟設 continue-on-error，
# 由 workflow 最後一步依 outcome 把整次執行標成失敗（其他步驟照常提交）。
set -uo pipefail
attempts="$1"; wait_s="$2"; shift 2
rc=0
for i in $(seq 1 "$attempts"); do
  "$@"; rc=$?
  if [ "$rc" -ne 2 ] || [ "$i" -eq "$attempts" ]; then
    break
  fi
  echo "::notice::$* 第 $i 次中止（安全機制），${wait_s} 秒後重跑"
  sleep "$wait_s"
done
exit "$rc"
