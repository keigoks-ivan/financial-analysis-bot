# 台股籌碼資料庫（data/tw_chips/）

台股「籌碼」的長期共用資料：加權指數、成交金額、三大法人現貨買賣超、融資融券、期貨與選擇權三大法人未平倉、選擇權 Put/Call Ratio、大額交易人、新台幣匯率。全部是日頻，原始來源是證交所（TWSE）、期交所（TAIFEX）、FRED。網頁 `/tw-chips/` 與回測都讀這裡的資料。

## 目錄結構

| 路徑 | 內容 |
|---|---|
| `{series}.jsonl` | 原始存檔，一天一行，鍵 `d`（YYYY-MM-DD）。**保留來源原單位**，欄位名是短名（下面逐一解釋）。這是唯一的真相來源。 |
| `csv/{series}.csv` | 由 jsonl 扁平化而來，一天一列，第一欄 `date`，欄名是英文全名，供 pandas 直接讀。每次 `build.py` 重新產生，不要手改。 |
| `_state.json` | 抓取進度：`months_done`（已抓完的整月）、`gaps`（某天查無資料的嘗試次數，滿 3 次且超過 5 天就不再重抓）。 |
| `README.md` | 本檔。 |

jsonl 與 csv 一一對應：`taiex`、`turnover`、`inst`、`margin`、`fut_inst`、`opt_inst`、`pcr`、`large`、`usdtwd`。

## 單位約定

- **元**（`*_twd`）：新台幣元，整數。
- **仟元／千元**（`*_thousand_twd`）：證交所融資金額、期交所選擇權契約金額的原單位，1 仟元 = 1,000 元。
- **億元**（`*_yi`）：新台幣億元，1 億 = 1e8 元，四捨五入到小數 2 位。元 → 億元 ÷ 1e8；仟元 → 億元 ÷ 1e5。
- **張**（`*_lots`）：現貨一張 = 1,000 股。融資融券餘額用張。
- **口**（`*_oi`、`*_volume`）：期貨與選擇權契約口數。`*_oi` 是未平倉（open interest）。
- **%**（`*_pct`）：百分比，100 表示 100%。

「淨」一律是**多方減空方**（買方減賣方）。三大法人現貨「買賣超」＝買進金額減賣出金額，正數＝買超。

## 更新方式

- 日常：`python3 scripts/tw_chips/fetch.py`（只抓缺的日子），再 `python3 scripts/tw_chips/build.py`（產生 `docs/tw-chips/data/*.json` 與 `csv/`）。
- GitHub Actions：`.github/workflows/tw-chips-daily.yml`，週一至週五台北 21:47，隔天 08:17 備援。
- 回補：`python3 scripts/tw_chips/fetch.py --backfill`（2016-10 起，可續跑，TWSE 每次請求間隔 ≥ 3 秒，全程約 5 小時）。
- jsonl 是 append-only：同一天內容沒變就不寫，有修正就在檔尾加一行，讀入時以**同日最後一行為準**。回補完成後會整理成依日期排序、每日一行。
- 交易日曆以 `taiex` 為準（加權指數有收盤的日子）。休市日沒有任何序列的資料，也不會被當成缺口。

---

## taiex — 加權指數日 OHLC

- 來源：TWSE `rwd/zh/TAIEX/MI_5MINS_HIST`（月查詢，`date=YYYYMM01`）
- 最早日：2015-10-01 起（多抓一年，讓 240 日均線在 2016-10 就有值；網頁只顯示 2016-10 起）
- 更新：每次執行重抓當月，已結束的整月只抓一次

| jsonl 欄位 | csv 欄名 | 說明 | 單位 |
|---|---|---|---|
| `d` | `date` | 交易日 | YYYY-MM-DD |
| `o` | `open` | 開盤指數 | 點 |
| `h` | `high` | 最高指數 | 點 |
| `l` | `low` | 最低指數 | 點 |
| `c` | `close` | 收盤指數 | 點 |

## turnover — 全市場成交金額與股數

- 來源：TWSE `rwd/zh/afterTrading/FMTQIK`（月查詢）
- 最早日：同 `taiex`
- 範圍：上市（TWSE）整體市場，不含上櫃

| jsonl 欄位 | csv 欄名 | 說明 | 單位 |
|---|---|---|---|
| `d` | `date` | 交易日 | |
| `amt` | `turnover_twd` | 成交金額 | 元 |
| （由 `amt` 換算） | `turnover_yi` | 成交金額 | 億元 |
| `sh` | `volume_shares` | 成交股數 | 股 |

## inst — 現貨三大法人買賣金額

- 來源：TWSE `rwd/zh/fund/BFI82U?type=day&dayDate=YYYYMMDD`（逐日）
- 最早日：2016-10-03
- 口徑：
  - 外資＝「外資及陸資（不含外資自營商）」＋「外資自營商」（2018 年前證交所只給一列「外資及陸資」，已是合計）
  - 自營商＝「自營商（自行買賣）」＋「自營商（避險）」
  - 投信＝本國投資信託基金
- 範圍：上市市場；上櫃的三大法人沒有收

jsonl 每個法人是 `[買進金額, 賣出金額]`，單位元：

| jsonl 欄位 | 說明 |
|---|---|
| `d` | 交易日 |
| `f` | 外資 `[買進, 賣出]` |
| `t` | 投信 `[買進, 賣出]` |
| `dl` | 自營商 `[買進, 賣出]` |

csv 欄名（`foreign`＝外資、`trust`＝投信、`dealer`＝自營商）：`foreign_buy_twd`、`foreign_sell_twd`、`foreign_net_twd`（買減賣，元）、`foreign_net_yi`（億元）；`trust_*`、`dealer_*` 同樣四欄。

## margin — 融資融券餘額（上市）

- 來源：TWSE `rwd/zh/marginTrading/MI_MARGN?date=YYYYMMDD&selectType=MS`（逐日，信用交易統計表）
- 最早日：2016-10-03
- 證交所註明「以**前日餘額**為準」：當天公布的「今日餘額」要等隔日才完整揭露，隔日報表的「前日餘額」才是定稿。所以每一列同時保存今日餘額與前日餘額；csv 另加 `*_final` 欄，用**下一個交易日的前日餘額**定稿，最新一日沒有下一日就沿用今日餘額（`is_final=0`）。
- 已知缺口：官方統計表只有融券**張數**，沒有融券金額；融資金額只有仟元一個口徑。融券金額沒有補。

| jsonl 欄位 | csv 欄名 | 說明 | 單位 |
|---|---|---|---|
| `d` | `date` | 交易日 | |
| `mg` | `margin_balance_lots` | 融資餘額，當日公布的今日餘額 | 張 |
| `mg_p` | `margin_balance_lots_prev_day` | 融資前日餘額（該報表自帶） | 張 |
| `sh` | `short_balance_lots` | 融券餘額，今日餘額 | 張 |
| `sh_p` | `short_balance_lots_prev_day` | 融券前日餘額 | 張 |
| `mga` | `margin_balance_thousand_twd` | 融資餘額金額，今日餘額 | 仟元 |
| `mga_p` | `margin_balance_thousand_twd_prev_day` | 融資前日餘額金額 | 仟元 |
| （換算） | `margin_balance_yi` | 融資餘額金額（今日餘額）| 億元 |
| （換算） | `short_to_margin_ratio_pct` | 券資比＝融券張數 ÷ 融資張數 × 100 | % |
| （定稿） | `margin_balance_yi_final`、`margin_balance_lots_final`、`short_balance_lots_final`、`is_final` | 以隔日前日餘額定稿的數值；`is_final=1` 代表已定稿 | 億元／張／張／0 或 1 |

## fut_inst — 臺股期貨三大法人未平倉

- 來源：
  - 2023-10-18 起：TAIFEX `cht/3/futContractsDateDown`（`commodityId=TXF`，區間 CSV）
  - 2018-06-05 至 2023-10-17：FinMind 資料集 `TaiwanFuturesInstitutionalInvestors`（`data_id=TX`）。這是同一份期交所資料的轉載，2023-10 起與期交所原表逐筆比對一致（2,028 天重疊 0 筆不同）。
- **最早日：2018-06-05**。期交所網站只開放近 3 年；更早的資料 FinMind 與另一份獨立存檔（v7-backtest `vendor_inst_tx.csv`）都從 2018-06-05 才有，之前沒有可取得的來源，留白，不補數字。
- 商品：臺股期貨（TX，大型台指期貨）。不含小型（MTX）、微型（TMF）。
- 近 3 年窗口會隨時間往前滑，期交所之後會刪掉舊日期。這個資料庫已把舊日期存下來，所以不能靠重抓還原，不要刪 jsonl。

| jsonl 欄位 | 說明 | 單位 |
|---|---|---|
| `d` | 交易日 | |
| `f` | 外資及陸資 `[多方未平倉口數, 空方未平倉口數]` | 口 |
| `t` | 投信 `[多方未平倉口數, 空方未平倉口數]` | 口 |
| `dl` | 自營商 `[多方未平倉口數, 空方未平倉口數]` | 口 |

csv 欄名：`foreign_long_oi`、`foreign_short_oi`、`foreign_net_oi`（多減空）；`trust_*`、`dealer_*` 同樣三欄。

## opt_inst — 臺指選擇權三大法人買權、賣權未平倉

- 來源：TAIFEX `cht/3/callsAndPutsDateDown`（`commodityId=TXO`）；2018-06-05 至 2023-10-17 取 FinMind `TaiwanOptionInstitutionalInvestors`（`data_id=TXO`），同上轉載說明。
- **最早日：2018-06-05**（理由同 `fut_inst`）。
- 商品：臺指選擇權（TXO），所有到期月份合計。「買權」＝CALL、「賣權」＝PUT。
- 方向用法：買方口數是該法人買進後尚未平倉的部位，賣方口數是賣出後尚未平倉的部位。買權淨口數為正、賣權淨口數為負，整體偏多；反之偏空。

jsonl 結構：`{"d", "c": {"f": [...], "t": [...], "dl": [...]}, "p": {...}}`，`c`＝買權、`p`＝賣權，每個法人是 4 個數字：

| 位置 | 說明 | 單位 |
|---|---|---|
| `[0]` | 買方未平倉口數 | 口 |
| `[1]` | 賣方未平倉口數 | 口 |
| `[2]` | 買方未平倉契約金額 | 千元 |
| `[3]` | 賣方未平倉契約金額 | 千元 |

csv 欄名規則 `{call|put}_{foreign|trust|dealer}_{尾碼}`，尾碼有六個：`long_oi`、`short_oi`、`long_oi_amount_thousand_twd`、`short_oi_amount_thousand_twd`、`net_oi`（買方減賣方，口）、`net_oi_amount_yi`（買方減賣方金額，億元）。共 36 欄。

## pcr — 臺指選擇權 Put/Call Ratio

- 來源：TAIFEX `cht/3/pcRatioDown`（月查詢，一次最多約一個月）
- 最早日：2016-10-03 起存檔（期交所可查到更早，2008 年起；本庫只存十年）
- 比率在期交所原檔就是百分比。

| jsonl 欄位 | csv 欄名 | 說明 | 單位 |
|---|---|---|---|
| `d` | `date` | 交易日 | |
| `pv` | `put_volume` | 賣權成交量 | 口 |
| `cv` | `call_volume` | 買權成交量 | 口 |
| `vr` | `volume_ratio_pct` | 買賣權成交量比率＝賣權 ÷ 買權 × 100 | % |
| `po` | `put_oi` | 賣權未平倉量 | 口 |
| `co` | `call_oi` | 買權未平倉量 | 口 |
| `or` | `oi_ratio_pct` | 買賣權未平倉量比率＝賣權 ÷ 買權 × 100 | % |

## large — 臺股期貨大額交易人未沖銷部位

- 來源：TAIFEX `cht/3/largeTraderFutDown`（月查詢，檔案含全部期貨契約，只留商品代號 `TX`、到期月份 `999999`＝所有月份合計）
- 最早日：2016-10-03 起存檔（期交所與 v7-backtest 存檔可到 2009-07；本庫只存十年）
- 口數單位：大型臺指約當口數（期交所標示 TX + MTX/4 + TMF/20），小型一口算 1/4、微型一口算 1/20。
- 「全部」＝全部交易人（`交易人類別=0`），「特定法人」＝其中屬於特定法人者（`交易人類別=1`）。前五大、前十大是指未沖銷部位最大的 5 或 10 位交易人，買方與賣方各自排名，所以「買方減賣方」不是同一批人的淨部位。

| jsonl 欄位 | csv 欄名 | 說明 | 單位 |
|---|---|---|---|
| `d` | `date` | 交易日 | |
| `a` | `all_top5_long`、`all_top5_short`、`all_top10_long`、`all_top10_short` | 全部交易人 `[前五大買方, 前五大賣方, 前十大買方, 前十大賣方]` | 口（約當） |
| `s` | `specific_top5_long`、`specific_top5_short`、`specific_top10_long`、`specific_top10_short` | 特定法人，同上順序 | 口（約當） |
| `oi` | `market_oi` | 全市場未沖銷部位數 | 口（約當） |
| （換算） | `all_top5_net`、`all_top10_net`、`specific_top5_net`、`specific_top10_net` | 買方減賣方 | 口（約當） |

## usdtwd — 新台幣兌美元

- 來源：FRED `DEXTAUS`（`fredgraph.csv?id=DEXTAUS`，要用 requests 預設 UA，瀏覽器 UA 會逾時）
- 最早日：2016-10-03 起存檔
- FRED 約晚一週更新，且美國休市日沒有值（FRED 以 `.` 表示缺值，已略過不存）。網頁圖上美國休市日沿用前一營業日，本資料庫不補。

| jsonl 欄位 | csv 欄名 | 說明 | 單位 |
|---|---|---|---|
| `d` | `date` | 日期（美國營業日） | |
| `v` | `usdtwd` | 1 美元兌新台幣 | TWD/USD；數字上升＝新台幣貶值 |

---

## 已知缺口與限制（彙整）

1. 期貨與選擇權三大法人（`fut_inst`、`opt_inst`）最早只到 2018-06-05，之前沒有可取得的來源。
2. 融券只有張數，沒有金額（證交所統計表本身沒有）。
3. 現貨三大法人、融資融券只涵蓋上市（TWSE），不含上櫃（TPEx）。
4. 融資融券最新一日是暫時值（當日餘額），隔日才定稿。
5. 匯率比加權指數晚約一週。
6. `turnover` 是上市市場成交金額；不含上櫃與興櫃。
7. 本庫所有序列的 `d` 都是資料所屬交易日，不是公布日。
8. 資料缺漏日數與各序列涵蓋期間，會寫在網頁頁尾「資料來源與涵蓋期間」表，由 `build.py` 依實際檔案計算。
