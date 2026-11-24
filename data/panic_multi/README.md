# 「多類同時」恐慌訊號每日資料

頁面 `/backtest/viable/panic_multi/` 用的輸入與狀態。雲端 workflow `panic-multi-daily`（程式 `scripts/panic_multi/update.py`）每天更新：22:40 UTC 週一至週五、04:17 UTC 週二至週六，以及 RevMom Daily 跑完之後。規則照 v7-backtest `docs/Panic_Call_Prereg.md` 第 41～77 行，上線版不改規則；`scripts/panic_multi/` 的 signals.py、live_core.py、twvix_core.py、breadth_core.py 是 v7-backtest 的逐字副本。

v7-backtest 的 `tools/sync_site_data.py` 每天把整個資料夾複製到 `~/v7-backtest/data/panic_multi/`，並把自算台指 VIX 與鎖跌停比率併回 `data/twvix_proxy/`、`data/tw_limit_breadth/`。

## 檔案

| 檔案 | 內容 | 最早 | 更新方式 |
|---|---|---|---|
| us_inputs.csv | 美股五項收盤，第一欄 date | 見下表 | yfinance 抓最近兩個月，只覆蓋最後 5 列並往後接；五項沒到齊的日子不接 |
| taiex_close.csv | date、close：證交所加權指數收盤（FMTQIK） | 1990-01-04 | 每次重抓本月與上月 |
| twvix_proxy_daily.csv | 自算台指 VIX，欄位與 v7 `data/twvix_proxy/` 相同（vix_settle 是主版本） | 2001-12-24 | 每次用期交所台指選擇權每日行情（dlOptDataDown）重算本月與上月 |
| tw_limit_down_breadth_daily.csv | 鎖跌停家數與比率，欄位與 v7 `data/tw_limit_breadth/` 相同 | 2007-01-02 | 用 Release revmom-data 的上市櫃日線重算最後 20 列；家數沒變的舊列保留原值 |
| final_settle.csv | final_date、expiry、final_settle：台指選擇權最後結算日與結算價 | 2001-12 | 不更新（見已知缺口） |
| state.json | 三個市場今天的狀態：三類各自的值、歷史分位、明天要亮的門檻、能不能觸發、最近事件與隔天規格 | — | 每次覆寫 |
| state_log.csv | 每天每市場一列的狀態紀錄（只增，同日同市場以最後一次為準） | 2026-11-23 | 每次追加 |
| notified.json | 每個市場最近一次寄出通知的訊號日，防同一天重複寄 | — | 有新事件時改 |
| backtest.json | 審查版回測摘要（call 版、期貨版、賣出賣權價差對照版、逐筆） | — | v7 `python3 -m src.panic_call.export_page_data` 產生，不每天變 |

## us_inputs.csv 欄位

| 欄位 | 意思 | Yahoo 代號 | 最早 |
|---|---|---|---|
| gspc | S&P 500 收盤 | ^GSPC | 1927-12-30 |
| ndx | Nasdaq-100 收盤 | ^NDX | 1985-10-01 |
| vix | Cboe VIX 收盤 | ^VIX | 1990-01-02 |
| vxn | Cboe Nasdaq-100 波動率指數收盤 | ^VXN | 2001-01-23 |
| vix3m | Cboe 三個月 VIX 收盤 | ^VIX3M | 2006-07-17 |

單位都是指數點。2026-11-06 以前取自 v7 共用價格庫 `data/price_store`（同樣來自 Yahoo），之後由 CI 從 Yahoo 接上。

## state_log.csv 欄位

date、market（TW／SPX／NDX）、close、vol（波動率指數）、vol_share（歷史上一樣高或更高的比例）、vol_lit、z3（三日標準化報酬）、z3_share、accel（連三天加速下跌是否成立）、accel_lit（乙類是否亮）、ratio（美股 VIX÷VIX3M、台股鎖跌停比率）、ratio_share、ratio_lit、n_lit（亮幾類）、armed_open（上一波已結束、今天可以觸發）、event（今天是新事件）、last_event（最近一次事件的訊號日）。

## 已知缺口

- 台股狀態要等上市櫃全部個股的日線進 Release revmom-data，RevMom Daily 常延到台北隔天清晨才跑完，所以台股最新一天通常晚半天到一天。三項（加權指數、台指 VIX、鎖跌停比率）都到齊的最後一天才算台股狀態。
- final_settle.csv 停在 2026-10 到期月。之後的到期月一律用第三個星期三推算，跟 v7 建檔程式對未結算月份的做法相同；遇休市順延的月份，換月與剩餘天數會差一兩天。
- Yahoo 在 UTC 午夜後回傳的最新一根常是空值，那天會晚一輪才接上。2026-11-03 至 11-06 的 ndx 由 Yahoo 重抓覆蓋，跟共用庫差不到 0.004 點（浮點尾數）。
- 2026-11-24 上線。2026-11-20 S&P 500 的事件發生在上線前，沒有通知。
