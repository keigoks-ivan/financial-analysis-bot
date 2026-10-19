# 每日加權預估本益比紀錄（ETF 儀表板）

網站 /etf-dash/ 每檔基金每天算出的加權預估本益比，一檔基金一個 CSV（`{ETF}.csv`）。由 `scripts/etf_dash/pe_daily.py` 在每次 `build_etf_dash.py` 執行時寫入，雲端 etf-dash-daily workflow 寫回 git。本機副本由 v7-backtest `tools/sync_site_data.py` 同步到 `~/v7-backtest/data/etf_pe_daily/`。

## 欄位

| 欄位 | 說明 |
|---|---|
| date | ETF 收盤日（YYYY-MM-DD），不是執行日；同一天重跑覆蓋那一列 |
| pe | 加權預估本益比，倍：成分股「明年度」EPS 預估（Yahoo 分析師估計）對股價的加權調和平均，個股本益比 2–300 倍以外的排除 |
| coverage_pct | 有算進本益比的權重 %（排除沒有 EPS、本益比超出區間、EPS 涵蓋門檻外的成分股） |
| mode | full＝當天重抓持股與 EPS；price＝沿用上次的 EPS，只更新股價 |

## 已知限制

- 自 2026-10-19 起記錄，不回補。
- EPS 一週重抓一次（TOPIX 一個月一次），重抓那天數字會跳；其他天只有股價在動。
- 個股本益比下限 2026-10-19 從 3 倍改為 2 倍（三星、SK 海力士、Charter 的低本益比是真的）。
- 21 檔：SPY、RSP、QQQ、9 檔 SPDR 產業、SMH、SMH_UCITS、TAIEX、0050、TOPIX、EWY、EWM、EWZ、IEV。
- 頁面 Exhibit 3 只有在 dd-screener 推算線畫不出來時（XLE、XLB、TOPIX、EWY、EWM、EWZ、IEV）才畫這條線。
