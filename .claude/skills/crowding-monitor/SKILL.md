---
name: crowding-monitor
description: 維護「跨資產擁擠交易監測」儀表頁（docs/crowding/index.html，上站 /crowding/）。v2.0（2026-11-01）起不再出月刊：頁面是一頁持續更新的儀表（BofA 基金經理人調查最擁擠交易與現金水位、CFTC 15 市場投機部位、AAII 散戶、NAAIM 顧問曝險、S&P 500 與 11 個產業 ETF 加 SMH 的資金流），歷史序列與現在的分位由 CI 每週日自動更新。skill 的工作只有兩件：每月中旬 BofA 調查出來後補一列 CSV；數字換區間時寫一則幾句話的判讀。觸發：「跑擁擠交易監測」「crowding monitor」「更新擁擠交易」「補 FMS」「寫擁擠判讀」「positioning monitor」。
version: v2.0
date: 2026-11-01
changelog:
  - v2.0 (2026-11-01)：持有人不滿意月刊式呈現（兩萬字、15 張 Exhibit、英文術語、只出過一期），改成一頁持續更新的儀表＋短判讀。創刊號 CROWDING_20260705.html 保留為檔案，不再出期刊。資料層新增 AAII／NAAIM／BofA FMS 月序列／ETF 資金流累積檔。
  - v1.0 (2026-07-05)：月刊格式（已退役）。
---

# crowding-monitor v2.0 — 擁擠交易儀表的維護

## 定位
`/crowding/` 回答「現在誰站在同一邊，那一邊有多滿」。描述器，不是擇時訊號：擁擠衡量下方緩衝有多薄、反轉時同向的人有多少，不預測轉折時點。頁面不給買賣指令。

## 兩層結構（誰管什麼）

| 層 | 檔案 | 誰更新 | 頻率 |
|---|---|---|---|
| 儀表資料 | `docs/crowding/data/dash.json` | `scripts/crowding/build_dash.py`（CI `intel-2-daily.yml` 週日步驟） | 每週日 |
| AAII、NAAIM | `data/crowding_monitor/aaii_weekly.csv`、`naaim_weekly.csv` | `scripts/crowding/fetch_sentiment.py`（同一 CI 步驟，抓官方 Excel） | 每週日 |
| CFTC COT | `data/cot_history.json` | `scripts/build_crowding.py`（原有 pipeline，也產 `latest.json` 給 detective） | 每週日 |
| ETF 資金流 | `data/crowding_monitor/etf_flows_daily.csv`（累積檔） | `build_dash.py` 從 `data/etf_dash/flows/*.jsonl` 累積（etf-dash 只留 200 天） | 每週日 |
| 槓桿 ETF 多空流量 | `data/crowding_monitor/leveraged_etf_flows_weekly.csv`（2016-11 起週，TradingView 匯出一次）＋`leveraged_etf_daily.csv`（發行商每日快照） | `scripts/crowding/fetch_leveraged.py` 抓每日；`build_dash.py` 把每日併成新週寫回週檔 | 每日抓、每週日併 |
| BofA 基金經理人調查 | `docs/crowding/data/bofa_fms_monthly.csv` | **本 skill，人工** | 每月中旬 |
| 判讀 | `docs/crowding/data/readings.json` | **本 skill，人工** | 數字換區間時 |
| 頁面 | `docs/crowding/index.html` | 靜態；本體與圖表程式改了要整頁重組 | 很少 |

正本副本：AAII／NAAIM／ETF 累積檔正本在本 repo（CI 寫），`~/v7-backtest/data/crowding_monitor/` 是副本；BofA 月序列正本在本 repo `docs/crowding/data/`，v7 同名資料夾放副本。

## 每月工作：補 BofA 調查
2026-11-01 起由雲端 `idea-watch` 每天 05:15 自動做（12 日以後、CSV 缺本月那列時搜尋並補列，見 `.claude/skills/idea-watch/SKILL.md` 步驟 3）。以下是它照的格式，也是自動補失敗時人工補的步驟。
1. BofA Global Fund Manager Survey 每月第二或第三個星期二發布。用 WebSearch 搜 `"most crowded trade" "fund manager survey" <月份> <年>`，Reuters、Bloomberg、CNBC、ZeroHedge、Investing.com 與 Hartnett 相關的 X 貼文都會轉。
2. 在 `docs/crowding/data/bofa_fms_monthly.csv` 末尾加一列。欄位：`survey_month,publish_date,top_trade,top_pct,second_trade,second_pct,third_trade,third_pct,cash_pct,source,tier,note`。`top_trade` 用 BofA 原文英文（例如 `Long global semiconductors`）；`tier` 一手＝報告原文或原圖轉述、二手＝媒體文字；找不到的欄位留空，不猜；兩個來源數字不同時 `note` 寫明。數字不用千分位，文字含逗號用雙引號。
3. 跑 `python3 scripts/crowding/build_dash.py`，確認輸出列的 FMS 覆蓋多了一個月。
4. 把 CSV 複製一份到 `~/v7-backtest/data/crowding_monitor/`。

## 數字換區間時：寫判讀
`docs/crowding/data/readings.json` 是陣列，最新在最前：`{"date":"YYYY-MM-DD","title":"一句話","body":["段落","段落"]}`。寫之前先載入 `~/.claude/skills/zh-analyst-prose/SKILL.md`。
- 只在狀態列的「極端」出現或消失、第一名交易換人、現金穿過 4% 或 5%、AAII 穿過 ±1σ 時寫；平常不寫。
- 三到五句：變了什麼、五個來源同向還是分歧、對本站指數部位的意思只能是「規則照舊」或「看某個查核點」，不寫買賣指令。
- 每句錨定頁面上的數字與日期。
- 舊判讀不刪，頁面自動折疊。

## 改頁面本體
本體與圖表程式在組裝時寫入 `docs/crowding/index.html`（樣板頁首、樣式、選單取自 `docs/ideas/anthropic-ipo.html` 1～176 行）。改文字直接改 HTML 即可；改圖表邏輯改 `<script>` 段。改完 `python3 scripts/qc.py docs/crowding/index.html`，本機 `python3 -m http.server 8765 --bind 127.0.0.1`（cwd docs/）開 `http://127.0.0.1:8765/crowding/` 看圖有沒有畫、主控台有沒有錯。

## 硬規則
- 中文全形標點；描述器定位，禁買賣指令句。
- 每個數字帶日期與來源；找不到就留空，不捏造。
- 不改 `scripts/build_crowding.py` 的 COT 與主題分數部分（detective 在讀 `latest.json`）。
- git：只 add 自己動的檔（CSV、readings.json、index.html），不 `git add -A`；commit 前跑 `scripts/qc.py`。
