# dd5：個股研究（精簡版）

做什麼：對一檔個股產出一頁精簡研究（公司在做什麼、生意往哪走、現價隱含什麼、護城河、追蹤指標），放進個股儀表板的「研究摘要」區塊與全文頁。

## 一鍵指令

在 repo 根目錄執行：

    python3 scripts/dd5/dd.py <代號> [--date YYYYMMDD] [--peers A,B,C] [--reuse] [--dry-run] [--no-push]

- `--date` 預設今天（台北時間）。
- `--peers` 手動指定同業；不給就由模型點名、程式驗代號，驗不過退回程式自動名單。
- `--reuse` run 目錄已有 article.md 時不備資料、不叫模型，只重跑渲染與文字檢查（零花費，補發與測試用）。
- `--dry-run` 只輸出到 `~/dd5-pilot/preview/<代號>/`，做到導覽列注入與 qc，不 commit、不 push。
- `--no-push` 做到 commit 為止，印出內容後把 commit 丟掉。

結束代碼：0 成功；3 文字檢查有 block；4 發布前 qc 或 commit hook 擋下；5 推送失敗。

## 步驟與花費

1. `pack.py` 備資料，零模型費用。
2. `run.py --steps peers,lite,render,lint`：haiku 點名同業約 0.001 美元，opus 寫稿一通約 1 美元；`DD5_RUN_LIMIT` 沒設就設 5（單檔累計上限）。渲染與文字檢查不花錢。
3. 文字檢查有 block 就停，印出被擋的行，不發布。
4. 發布：在暫時 worktree（從 origin/main 開）寫全文頁與 `docs/stock-dash/research/index.json`、注入站上導覽列、跑 `scripts/qc.py`、commit、推到 origin/main；推完若主工作區乾淨就順便 fast-forward。不會碰主工作區的檔案。

## 檔案放哪

- run 目錄與花費紀錄：`~/dd5-pilot/runs/<代號>_<日期>/`（留在本機，不進 git）。manifest.json 有每通呼叫的花費。
- 發布位置：`docs/stock-dash/research/<代號>_<日期>.html`，索引在同目錄 `index.json`，每檔只留最新一份。
- 模型呼叫的中立工作目錄：`/private/tmp/dd5_neutral_cwd`。

## 不產出什麼

不給買賣裁決、目標價、機率。下游的席位引擎不讀這份研究，它只是給人看的背景。
