#!/usr/bin/env bash
# CI push 迴圈用：取代 `git pull --rebase ... || { echo "Rebase failed"; exit 1; }`。
#
# 成功 rebase → exit 0，呼叫端照原本的迴圈再 push。
# 內容衝突（產生檔被另一個 run／session 同時重建，例如 docs/dd-screener/latest.json）→
#   不試著自動解 diff：abort 保留乾淨狀態、寫 conflict=true 到 $GITHUB_OUTPUT、exit 1。
#   同一 job 的下一步（scripts/ci/retrigger_once.sh）會從最新 main 重跑整條 workflow 一次。
#   IS_RETRY=1（已經是重跑的 run）再撞 → ::error:: 結束，不再重觸發（防無限迴圈）。
# 由來：2026-09-24 晨間排程 run 35962194424 跑完 298 檔，因 latest.json 衝突整批丟失。
#
# 用法（在 commit step 的 run 裡）：bash scripts/ci/rebase_or_flag.sh || exit 1
# 該 step 需 `id:`，env 需 `IS_RETRY: ${{ github.event.inputs.retry || '0' }}`。
set -u
if git pull --rebase --autostash origin main; then
  exit 0
fi
git rebase --abort >/dev/null 2>&1 || true
[ -n "${GITHUB_OUTPUT:-}" ] && echo "conflict=true" >> "$GITHUB_OUTPUT"
if [ "${IS_RETRY:-0}" = "1" ]; then
  echo "::error::Rebase conflict again on the retry run (retry=1). Not re-triggering to avoid a loop; this run's data was NOT pushed. Needs a human look or a manual workflow_dispatch."
else
  echo "::warning::Rebase conflict with a concurrent push to origin/main (a generated file was rebuilt elsewhere at the same time). This run's commit was not pushed; the next step re-runs this workflow once from the latest main (retry=1)."
fi
exit 1
