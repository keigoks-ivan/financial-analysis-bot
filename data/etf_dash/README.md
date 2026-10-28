# ETF 儀表板資料（/etf-dash/）

網站 https://research.investmquest.com/etf-dash/ 用到的全部資料。由 `scripts/etf_dash/build_etf_dash.py` 產生，雲端 etf-dash-daily workflow 每天寫回 git。整個資料夾連同頁面 JSON（`docs/etf-dash/data/`）每天同步一份到 `~/v7-backtest/data/etf_dash/`（v7-backtest `tools/sync_site_data.py`），回測要用就到那邊拿。

## 內容

| 路徑 | 內容 | 格式 |
|---|---|---|
| `prices.jsonl` | 算報酬貢獻用的成分股收盤工作檔，一行一天：`{"date", "closes": {代號: 收盤}}`，約 1,400 個代號，只留最近約 100 個曆日 | JSONL；**不要當價格來源**，見下方限制 |
| `pe_daily/{ETF}.csv` | 每檔基金每天的加權預估本益比（date,pe,coverage_pct,mode），2026-10-19 起 | CSV，見該資料夾 README |
| `long_pe/*.csv` | 長期本益比：美股 7 條預估（週）、台股大盤與東證（月） | CSV，見該資料夾 README |
| `snapshots/{ETF}/{日期}.json` | 每天一份成分股快照：權重、明年度 EPS（原幣與美元）、ETF 收盤 | JSON |
| `holdings_cache/{ETF}.json` | 最近一次抓到的持股（代號、名稱、權重 %），只留最新一份 | JSON |
| `eps_cache/{ETF}.json` | 最近一次 FULL 模式抓的成分股 EPS 預估（Yahoo eps_trend）、股價、市值、排除原因，只留最新一份 | JSON |
| `anchor_history/{ETF}.jsonl` | 每次 FULL 記一行：成分股加權明年度 EPS 在 90／60／30／7 天前與今天的指數（今天＝100） | JSONL |
| `dd_eps_history.jsonl` | dd-screener 名單每天的明年度與後年度 EPS 預估，一行一天，2026-05-15 起；欄位順序見 `scripts/etf_dash/dd_eps_history.py` 的 FIELDS | JSONL |
| `flows/{ETF}.jsonl` | 每天的流通單位數與淨值，用來推算資金流 | JSONL |
| `tw_industry_map.json` | 台股公司代號對產業別（證交所） | JSON |
| `picks.json` | 本站挑選的事前登記清單（picks-registry-v2）：每筆登記的挑選、文字、登記日數字、查核點。第一筆 2026-10-28（SMH 攻、XLV 守，基準 SPY，結算 2027-10-28）手寫；之後每季 1 日由雲端排程 picks-monthly 用 `scripts/etf_dash/picks_register.py` 新增，既有登記不改 | JSON |
| `picks_reviews.json` | 每月 1 日雲端排程寫的月評（picks-reviews-v1），依登記 id 歸屬；`picks_candidates.json` 是季度重挑用的候選數據（`picks_candidates.py`），`picks_status.json` 是排程成功／失敗紀錄 | JSON |
| `picks_prices.json` | 挑選追蹤用的三檔（SMH、XLV、SPY）登記日起的未還原收盤與除息日配息，`scripts/etf_dash/picks_track.py` 每天抓並覆蓋；抓不到時當退路。輸出在 `docs/etf-dash/data/picks_track.json` | JSON |

## 已知限制

- `prices.jsonl` 的日期是台北執行日，不是交易日：美股收盤會差一天（標 10-16 的是美股 10-15 收盤），週末也有列；基金本身（SPY 等）2026-09-25 之後沒有記錄。價格只調拆股、不含股息。要歷史價格請用 v7-backtest 價格目錄裡的正本。
- 倫敦掛牌股票的價格已從便士換成英鎊。
- `holdings_cache`、`eps_cache` 每次覆蓋，網站上看不到舊版本；回測庫的副本也只保留最新一份。要歷史持股與 EPS 用 `snapshots/`。
- EPS 一週重抓一次（TOPIX 一個月一次），其他天沿用。
