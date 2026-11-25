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

## 正文佔位

新文章可放的佔位：`{{圖:資本報酬}}`（資料包 `[p:roic]` 段：逐年投入資本報酬率長條圖＋拆解小表，程式用 yfinance 年報自算，口徑同同業表；金融業沒有這段，不算缺）、`{{表:獲利三檔}}`（機器欄位 `earnings_cases` 三檔，程式算「現價是這個獲利的幾倍」，不算任何價位）、`{{表:追蹤條件}}`、`{{表:跟上一份比}}`、`{{表:例行檢查}}`、`{{圖:股價位置}}`。渲染時缺的、殘留的記在 `number_check.json` 的 `placeholders_missing`、`placeholders_leftover`；新文章不再要求 `{{表:歷史倍數}}`、`{{表:獲利乘倍數對照}}`。

這兩個舊佔位的排版程式保留，舊文章有放就照舊排版，沒放不算缺；舊文章若用 `{{表:獲利乘倍數對照}}` 當情境表，也不會被要求補 `{{表:獲利三檔}}`。

## 補「資本報酬」章（舊文章用）

    python3 scripts/dd5/add_roic.py <代號> --date <YYYYMMDD> [--force]

重抓年報把 `[p:roic]` 段補進 run 目錄的資料包，一通 opus（不上網、effort low，每檔約 0.2 美元、半分鐘）只寫「## 資本報酬」一章，插在「護城河與競爭」之後；原文備份 `article.md.pre_roic`。之後用 `dd.py <代號> --date <日期> --reuse` 重排並發布。

## 版面

全文頁由 `render_pretty.py` 產生：先呼叫 `render.render`（數字檢查、佔位、calc.json 照舊），再把正文套進新外殼（頁首結論卡、側邊目錄、同業橫條圖、淺／深色）。render.py 新增的佔位會自動流進新版，不用改 render_pretty。

## 檔案放哪

- run 目錄與花費紀錄：`~/dd5-pilot/runs/<代號>_<日期>/`（留在本機，不進 git）。manifest.json 有每通呼叫的花費。
- 發布位置：`docs/stock-dash/research/<代號>_<日期>.html`，索引在同目錄 `index.json`，每檔只留最新一份。
- 模型呼叫的中立工作目錄：`/private/tmp/dd5_neutral_cwd`。

## 不產出什麼

不給買賣裁決、目標價、機率。下游的席位引擎不讀這份研究，它只是給人看的背景。
