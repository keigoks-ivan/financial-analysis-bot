#!/usr/bin/env bash
# rebase_or_flag.sh 標出衝突後，從最新 main 重跑「本 workflow」一次（帶 retry=1）。
# workflow 必須宣告 workflow_dispatch.inputs.retry，permissions 需 actions: write，
# 呼叫步驟的條件：if: failure() && steps.<commit step id>.outputs.conflict == 'true' && github.event.inputs.retry != '1'
# （上一步 exit 1 後，沒有狀態函式的 if 會被預設 success() 擋掉，所以要寫 failure()）。
# 需要 env GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}。
set -euo pipefail
wf_ref="${GITHUB_WORKFLOW_REF:?GITHUB_WORKFLOW_REF missing}"   # owner/repo/.github/workflows/x.yml@refs/heads/main
wf_file="$(basename "${wf_ref%@*}")"
gh workflow run "$wf_file" --ref main -f retry=1
echo "::notice::Re-triggered ${wf_file} once from the latest main (retry=1). This run ends without pushing."
