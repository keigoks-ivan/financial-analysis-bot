# 美股籌碼資料庫（data/us_chips/）

美股「籌碼」的長期共用資料：S&P 500、Nasdaq-100、費城半導體三個指數日線，期貨大戶部位（CFTC），SPY／QQQ／SMH／SOXX 四檔 ETF 的放空餘額與每日放空量（FINRA）、分帳戶選擇權成交量（OCC）、流通份額（發行商），槓桿 ETF 份額與淨值（ProShares），VIX、VXN、SKEW，全市場 put／call 比（Cboe），成分股內部人買賣（SEC）。網頁 `/us-chips/` 讀這裡建出的 `docs/us-chips/data/*.json`。

不在本資料夾、由網頁直接讀其他頁已有檔案的兩塊（不另外抓、不複製）：

- ETF 申購贖回週序列：`docs/etf-dash/data/{SPY,QQQ,SMH,SOXX}.json` 的 `chart.flows_weekly`，正本是 `data/crowding_monitor/etf_flows_weekly.csv` 與 `data/etf_dash/flows/`。
- 全市場融資餘額：`docs/fear-greed/data/raw/finra_margin.csv`（FINRA margin statistics，月資料，恐懼貪婪頁每週更新；v7-backtest 副本在 `data/fear_greed/raw/`）。
- 槓桿 ETF TQQQ、SQQQ、SOXL、SOXS 的週淨申購：`data/crowding_monitor/leveraged_etf_flows_weekly.csv`（build.py 只讀，不改）。

## 目錄結構

| 路徑 | 內容 |
|---|---|
| `{series}.jsonl` | 原始存檔，一天（或一期）一行，鍵 `d`（YYYY-MM-DD）。欄位名是短名（下面逐一解釋）。append-only：同日內容沒變不寫，有修正就在檔尾加一行，讀入以同鍵最後一行為準。 |
| `insider/{YYYYqN}.jsonl` | 內部人買賣，每個 SEC 季度資料集一個檔，每列＝一個代號一個月。 |
| `csv/{series}.csv` | 由 jsonl 扁平化而來，第一欄 `date`，欄名是英文全名，pandas 直接能讀。每次 `build.py` 重新產生，不要手改。 |
| `constituents.json` | 內部人彙總用的成分股名單（etf-dash 當時的持股，代號只留英數字）。 |
| `_state.json` | 抓取進度：`no_data`（平日但來源沒檔，多半是休市）、`insider_done`（已處理完的內部人季度）。 |

## 更新方式

- 日常：`python3 scripts/us_chips/fetch.py`（只抓缺的），再 `python3 scripts/us_chips/build.py`。
- GitHub Actions：`.github/workflows/us-chips-daily.yml`，台北週二至週六 08:41。
- 回補：`fetch.py --backfill`（svol 自 2018-08-01、pcr 自 2019-10-07、occ 自 2024-10-23），可用 `--only svol,occ` 指定來源。
- 本機有 SEC 原始 zip 時，`US_CHIPS_INSIDER_RAW=~/v7-backtest/data/insider/raw` 可省下載。
- 單一來源失敗不影響其他來源，log 會寫 `FAIL <來源>`。

---

## idx — 三個指數日收盤

- 欄位：`spx`＝S&P 500、`ndx`＝Nasdaq-100、`sox`＝費城半導體指數，指數點數收盤。
- 來源：Yahoo Finance（`^GSPC`、`^NDX`、`^SOX`），不還原（指數沒有股息調整）。
- 最早日：`spx`、`ndx` 1990-01-02，`sox` 1994-05-04。更新：每日。
- 注意：Yahoo 在 UTC 午夜後最新一根可能是 NaN，抓取時丟掉，隔天補。

## cot_spx、cot_ndx — CFTC 金融期貨持倉（週）

- 來源：CFTC Public Reporting `https://publicreporting.cftc.gov/resource/gpe5-46if.json`（Traders in Financial Futures，Futures Only）。`cot_spx` 是 `S&P 500 Consolidated`（代碼 `13874+`），`cot_ndx` 是 `NASDAQ-100 Consolidated`（代碼 `20974+`）。
- 日期 `d`＝調查日（週二），週五公布。最早日 2010-06-15，更新：每週。
- 單位：口數（合約數）。Consolidated 是 CFTC 的合併口徑，比只算迷你契約（E-mini）略大（2026-10-27 約大 1% 到 5%，下面列數字）。對照：2026-10-27 的 S&P 500 避險基金多單，合併口徑 102,967 口，迷你契約（`13874A`，fab `data/market_sources/series/cftc_spx_lev_*.json` 用的那條）102,079 口；未平倉量合併 1,978,590 口、迷你 1,955,711 口。Nasdaq-100 未平倉量合併 281,669 口、迷你（`209742`）268,508 口。
- **單位斷點**：CFTC 在 2023-05-02 把這兩個 Consolidated 的契約單位從 $250（S&P 500）、$100（Nasdaq-100）改成 $50、$20（API 的 `contract_units` 欄），同一批部位的口數變成 5 倍（2023-04-25 未平倉 453,159 口，2023-05-02 變 2,304,633 口）。jsonl 與 csv 存原值並附 `cu` 欄（契約乘數）；`build.py` 把舊單位的口數乘以（舊乘數÷最新乘數）＝5，統一成最新單位後才畫圖，轉換後兩週的未平倉為 2,265,795 與 2,304,633 口，接得上。用 csv 做研究時要自己處理這個斷點。
- 欄位：`cu` 契約乘數（美元／指數點）；`oi` 未平倉量；`dl_l／dl_s／dl_sp` 交易商（Dealer）多／空／跨月價差；`am_*` 資產管理人（Asset Manager）；`lv_*` 避險基金（Leveraged Funds）；`ot_*` 其他申報者（Other Reportables）；`nr_l／nr_s` 散戶（Nonreportable，未達申報門檻）。淨部位＝多減空，不含 spreading。
- 已知缺口：無。

## si_SPY、si_QQQ、si_SMH、si_SOXX — FINRA 放空餘額（每月兩次）

- 來源：`POST https://api.finra.org/data/group/otcMarket/name/consolidatedShortInterest`，body 用 `compareFilters` 篩 `symbolCode`，不要帶 `sortFields`（會 400）。
- 日期 `d`＝結算日（約 15 日與月底），公布晚約 7 個營業日。最早日 2017-12-29，每檔 212 筆（到 2026-10-15）。
- 欄位：`short` 放空股數（`currentShortPositionQuantity`）、`prev` 上期放空股數、`adv` 日均成交量（股）、`dtc` 回補天數（`daysToCoverQuantity`，FINRA 公布值；最小 1）。
- 已知缺口：無；FINRA 偶有 `revisionFlag` 修正，抓取時以最新值覆蓋（檔尾加一行）。

## shares_SPY、shares_QQQ、shares_SMH、shares_SOXX — ETF 流通份額（逐日）

- 來源：發行商官方歷史檔，抓法沿用 `scripts/etf_dash/flows.py`：SPY＝SSGA navhist xlsx、QQQ＝Invesco、SMH＝VanEck、SOXX＝iShares。etf-dash 自己只留近 200 天，這裡存全歷史，用來算放空股數占流通份額。
- 欄位：`sh` 流通份額（股）、`nav` 每股淨值（美元）。
- 最早日：SPY 2006-05-31、SMH 2011-12-20、SOXX 2001-07-10；QQQ 需要 Invesco 的 API，部分網路環境會被擋（406），本機抓不到時 build.py 退回 etf-dash 近 200 天的份額（只有 2026-04 起），雲端 CI 抓得到時會自動補成全歷史。

## svol_SPY、svol_QQQ、svol_SMH、svol_SOXX — FINRA 每日放空量

- 來源：`https://cdn.finra.org/equity/regsho/daily/CNMSshvolYYYYMMDD.txt`（Reg SHO 每日放空量，交易所與場外合併）。最早日 2018-08-01（更早的檔案 403），每檔 2,075 筆。更新：每日，美東約 18:00 公布。
- 欄位：`sv` 放空成交股數（`ShortVolume`）、`sxv` 豁免放空股數（`ShortExemptVolume`）、`tv` 總成交股數（`TotalVolume`）。檔內數字有小數，是 FINRA 合併後的原值。
- 每日放空量比率＝`sv ÷ tv`。這個比率包含造市商為了提供流動性與避險做的放空，不等於看空比例。
- 已知缺口：休市日沒有檔（79 個平日，記在 `_state.json` 的 `no_data.svol`）。

## occ_SPY、occ_QQQ、occ_SMH、occ_SOXX — OCC 分帳戶選擇權成交量

- 來源：`https://marketdata.theocc.com/volume-query?reportDate=YYYYMMDD&format=csv&volumeQueryType=O&symbolType=U&symbol=<ETF>&reportType=D&accountType=ALL&productKind=ALL&porc=BOTH`。
- 欄位：`c_c／c_p` 客戶（actype C）買權／賣權成交量、`f_c／f_p` 券商自營（F）、`m_c／m_p` 造市商（M），單位合約數。同一標的的所有交易所（CBOE、AMEX、ISE 等）與所有週別合約（`SPY`、`2SPY`、`4SPY` 等代號）加總。
- 最早日：OCC 只提供近約 2 年，2026-11-03 實測 2024-10-22 以前回空表、2024-10-30 有資料，實際第一筆 2024-10-30（回補從 2024-10-23 起試）；之後每天累積，**不會再往前補**。
- 請求間隔約 1 秒。

## vix、vxn、skew — Cboe 指數日線

- 來源：`https://cdn.cboe.com/api/global/us_indices/daily_prices/{VIX,VXN,SKEW}_History.csv`（要跟隨轉址）。欄位 `v`＝收盤（SKEW 為指數值）。
- 最早日：VIX、SKEW 1990-01-02，VXN 2009-09-14。更新：每日，每次整檔重抓。
- 費半沒有對應的波動率指數。

## pcr — Cboe 全市場選擇權 put／call 比

- 2006-11-01 至 2019-10-04：舊歷史 CSV（`https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/{totalpc,indexpc,equitypc}.csv`），標 `src=csv`，只有總計、指數、股票三項，沒有 ETF 產品分項。
- 2019-10-07 起：每日統計檔 `https://cdn.cboe.com/data/us/options/market_statistics/daily/YYYY-MM-DD_daily_options`（JSON，`ratios` 與 `SUM OF ALL PRODUCTS`），標 `src=json`，多了 ETF 產品（`etp`）。這個端點最早到 2019-10-07（2019-10-04 以前回 403），剛好接在舊 CSV 之後。
- 欄位：`total／index／etp／equity` put÷call 成交量比；`calls／puts` 全產品 call／put 成交量（合約數）。
- 已知缺口：兩段在 2019-10-04 與 2019-10-07 之間直接相接（中間沒有交易日），對照 S&P 500 交易日曆無缺漏日。`2025-01-09`（國殤日休市）Cboe 仍發了一份空殼檔，build.py 以成交量過低排除。

## lev_UPRO、lev_SPXU、lev_SSO、lev_SDS — ProShares 槓桿 ETF 份額與淨值

- 來源：`https://accounts.profunds.com/etfdata/ByFund/<代號>-historical_nav.csv`（官方全歷史）。欄位 `sh` 流通份額、`nav` 淨值（檔內份額與淨值同日一致，份額乘淨值就是規模）。
- 最早日：UPRO、SPXU 2009-06-23，SSO 2006-06-19，SDS 2006-07-11。
- 週淨申購（`csv/lev_weekly.csv`）＝逐日（份額變化 × 當日淨值）併成週（週一為週標籤），百萬美元，2016-11-07 起，口徑同 `scripts/crowding/build_dash.py`。
- Direxion 的 SPXL、SPXS 沒有公開歷史份額，不收。

## insider/ — 成分股內部人買賣（月）

- 來源：SEC Form 3/4/5 季度資料集（`https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/<YYYY>q<N>_form345.zip`；2026q2 起改放 `.../files/datastandardsinnovation/data/insider-transactions-data-sets/`）。原始 zip 在 v7-backtest `data/insider/raw/`（2009q1 起）。
- 做法：只取 Form 4（不含 4/A 更正）的公開市場買進（交易代碼 P）與賣出（S）；依交易日所在月份與公司代號彙總。每列：`t` 代號（只留英數字）、`m` 月、`nb`／`ns` 該月買進／賣出的不同申報人數、`buy`／`sell` 成交金額（股數 × 單價，美元；缺單價的列不計金額；單價高於 5,000 美元或單筆超過 50 億美元視為申報手誤不計金額，同公司同日同股數同單價同方向的重複列只算一筆）。
- 成分股：etf-dash 今天的持股名單（SPY、QQQ、SOXX 與 SMH，四檔的聯集 `constituents.json`）。**用的是今天的成分股，過去被剔除的公司不在內**；用代號比對，改過代號的公司可能對不上。
- 頁面上每個分頁把名單內的代號相加：人數是「公司別的申報人數相加」，同一人在兩家公司買賣會算兩次。
- 時間落差：SEC 每季資料集在季底後一到三個月才發布，最新資料到上一個季底。同一個月的交易會出現在多個季度檔（晚申報的），build.py 把各季相加，所以每個季度只要處理一次。
- 範圍：2009-01 起（2009q1 起的 zip）；交易日期晚於該季季末的列視為申報打錯，不收。
