# data/active_etf 折溢價資料說明

折溢價頁面（/active-etf/）用的兩份底稿，由 `scripts/active_etf/premium.py` 每日更新。輸出 `docs/active-etf/data/premium.json`。

## close_twse.jsonl：證交所每日收盤價

- 一個交易日一行：`{"date": "YYYY-MM-DD", "close": {代號: 收盤價}}`，依日期排序。
- 單位：新台幣元，每單位 ETF 的收盤價。代號涵蓋 22 檔主動式 ETF 加 0050。
- 來源：`https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=YYYYMMDD&type=0099P`，取標題為「每日收盤行情(ETF)」的表，欄位「收盤價」。
- 只抓「已有淨值、尚未快取」的日期。休市日回傳空表，不寫入。
- 最早日：2026-01-28（最早一筆投信淨值，00995A）。
- 已知缺口：證交所當日行情未公布前執行會缺當日，下次執行自動補。

## nav_twse.jsonl：證交所公告的每單位淨值

- 一個淨值日一行：`{"nav_date", "snapshot_date", "snapshot_time", "nav": {代號: 淨值}, "units": {代號: 流通單位數}}`。
- 單位：淨值為新台幣元每單位；`units` 為單位數（股）。
- 來源：`https://mis.twse.com.tw/stock/data/all_etf.txt`，欄位 h 為前一營業日每單位淨值，欄位 c 為流通單位數。
- 最早日：2026-10-28（2026-10-29 首次執行抓到的前一日淨值），之後每次執行累積一行，不回補。
- 淨值日期判斷：h 不一定是快照日的前一營業日，收盤後可能已換成當日淨值。程式把 h 四捨五入到小數 2 位，和投信 PCF 淨值比對，取「快照日」與「快照日前一交易日」兩個候選中相符檔數較多者，且至少 10 檔相符、不能並列。條件不符就不寫入，並印出警告。
- 已知缺口：
  - MIS 主機是否能從 GitHub Actions 連線尚未驗證，連不上時只記錄，折溢價改用投信 PCF 淨值。
  - 日期判斷依賴 PCF 淨值，PCF 缺當日資料時可能無法判斷而跳過該次。

## 淨值取用順序與例外

1. 該日有證交所公告淨值就用它。
2. 否則用投信 PCF 淨值（`holdings/{代號}.jsonl` 的 `nav.nav_per_unit`，同一 as_of 取最後一行）。

例外：

- **00401A**：投信 PCF 淨值日期標錯。2026-10-28 PCF 為 13.42，證交所公告為 13.75，用 PCF 會算出 −4.47% 與 +1.6% 的假折溢價。程式一律不用它的 PCF 淨值，歷史只從 `nav_twse.jsonl` 累積。
- **00996A**：投信 PCF 自 2026-09-24 起 GitHub 抓不到，之後只靠證交所公告淨值。

折溢價絕對值超過 5% 的日子視為日期對不齊，不進序列與統計，列在 `premium.json` 的 `suspect`。
