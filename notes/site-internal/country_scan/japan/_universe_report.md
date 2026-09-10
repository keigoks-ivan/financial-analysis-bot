# 日股國家掃描 · 母體重建報告（2026-09-10）

- **快照日期**：2026-09-10
- **母體檔案**：`_universe.json`（新，939 檔）；先前版本存為 `_universe_v1_476.json`（476 檔，2026-08-14 快照，保留供對照）
- **母體定義**：東京證券交易所主板（Prime／Standard／Growth 皆可入選）普通股，市值 ≥ ¥1,000 億
- **範圍**：東證主板普通股，排除 REIT／信託、優先股、非普通股

## 一、為什麼要重建

先前版本（`_universe_v1_476.json`）的候選清單主體是一份 2022-02 版 TOPIX 500 成分股清單 + 6 檔手動補丁，
`_universe_report.md`（舊版）自陳會系統性漏掉 2023 年後的 IPO／分拆與從 Standard 市場長大的公司，
且頁面曾把它描述為「市值≥¥1,000 億母體」——但實際上是一份「TOPIX 500 骨架＋補丁」，不是對全市場市值的
獨立篩選，兩者口徑不同，舊版報告本身已指出這個名不副實的問題。本輪重建改用即時的 TradingView 全市場
篩選器做候選清單，不再依賴 2022 年的靜態骨架。

## 二、建構方法

### 1. 候選清單來源與篩選條件

以 TradingView 日本股票篩選器（`POST scanner.tradingview.com/japan/scan`）查詢，條件：

- `exchange = TSE`（東京證券交易所主板；Nagoya／Sapporo／Fukuoka 的重複掛牌代碼已透過此條件排除，避免同一家公司被重複計入）
- `subtype = common`（排除優先股）
- `market_cap_basic > ¥1,000 億`

首輪查詢回傳 982 檔（979 檔 common + 3 檔 preferred，已用 subtype 條件濾除）。進一步排除
`industry = "Real Estate Investment Trusts"`（40 檔 J-REIT，TradingView 將其歸類在 `type=stock` 底下，
未被前述 subtype 條件濾除，需額外手動排除）後，**最終候選 939 檔**。

欄位取自 TradingView：`name`／`description`／`sector`／`industry`／`market_cap_basic`／`close`／
`price_earnings_ttm`／`non_gaap_price_to_earnings_per_share_forecast_next_fy`（前瞻本益比，TradingView
的 `price_earnings_forward_fy` 欄位對東證股票 100% 回傳空值，改用此欄位）／`price_book_fq`／
`dividends_yield_current`（`dividend_yield_recent` 欄位同樣對東證股票 100% 回傳空值）／`return_on_equity_fy`／
`total_revenue_yoy_growth_fy`／`net_income_yoy_growth_fy`／`gross_margin_fy`／`operating_margin_fy`／
`total_debt_fy`／`cash_n_short_term_invest_fq`／`total_shares_outstanding_current`／
`price_52_week_high`／`price_52_week_low`。

### 2. yfinance 抽樣驗證與整欄替換

以 `~/.venvs/v7bt/bin/python`（yfinance 1.4.1、pandas 2.3.3<3）對依市值分四分位、各抽 10 檔（共 40 檔）
做交叉比對，計算各欄位中位數絕對百分比偏差：

| 欄位 | 中位數偏差 | 判定 |
|---|---|---|
| market_cap | 1.8% | 保留 TradingView |
| price_to_book | ~0.0% | 保留 TradingView |
| cash | 0.0% | 保留 TradingView |
| shares_outstanding | 0.01% | 保留 TradingView |
| 52週高／低 | 0.0% | 保留 TradingView |
| trailing_pe | 5.86% | **整欄改抓 yfinance** |
| forward_pe | 19.84% | **整欄改抓 yfinance** |
| roe | 7.64% | **整欄改抓 yfinance** |
| dividend_yield | 7.42% | **整欄改抓 yfinance** |
| total_debt | 7.81% | 未使用於頁面計算，未替換（見盲區） |
| revenue_growth／net_income_growth／operating_margin | 30%–150% | 疑為計算基期定義不同（TradingView 用 FY YoY、yfinance 用不同期間），未使用於頁面計算，未替換 |

四個超過 5% 偏差門檻且頁面實際使用的欄位（trailing_pe、forward_pe、roe、dividend_yield），已對全部
939 檔以 `~/.venvs/v7bt/bin/python` 重新抓取 yfinance `get_info()`（批次 20 檔、批間 sleep 2 秒、失敗
重試一次），**939 檔零硬失敗**。3 檔 trailing_pe 原始回傳字串 `"Infinity"`（非數值），已清為 null 處理。

替換後覆蓋率：trailing_pe 96.5%、forward_pe 88.2%、roe 94.4%、dividend_yield 96.5%。

### 3. 與先前 476 檔母體的對應

先前建構的 476 檔母體中，**474 檔（99.6%）在新母體 939 檔中找到**。缺少的 2 檔：

| 代號 | 名稱 | 原因 |
|---|---|---|
| 4919 | Milbon | 現市值約 ¥98.9 億，剛好跌破 ¥1,000 億門檻的邊界案例（市值波動，非資料缺失） |
| 8283 | PALTAC | 已於 2026 年經 MediPal 控股 TOB 完成收購下市（2026-05-12 公告 TOB、2026-07-14 起交割），親子上市解消的真實案例，與治理鏡頭「MediPal 自身正 TOB 收購 PALTAC 消除親子上市」的敘事互相印證，非資料缺失 |

反向查證：兩者皆已用 TradingView 個別查詢確認（4919 現值可查得、8283 完全查無掛牌資料），並用 WebSearch
交叉核對 PALTAC 下市時程，結論一致。

## 三、母體組成（939 檔）

| 項目 | 數字 |
|---|---|
| 候選總數（TSE common，市值＞¥1,000億） | 982 檔 |
| 排除：優先股 | 3 檔 |
| 排除：REIT／信託 | 40 檔 |
| **母體合格檔數** | **939 檔** |
| 母體總市值 | 約 ¥1,284.7 兆 |
| 前十大個股占母體市值 | 22.2%（本頁自算，見 hub Exhibit 相關計算） |
| 母體 P/B&lt;1 比率 | 23.7%（222／936 檔，4 檔無 P/B 資料） |
| 母體 ROE 中位數 | 10.2% |
| 母體前瞻本益比中位數 | 16.6 倍 |
| 母體殖利率中位數（配息股） | 2.54% |

產業分布採 TradingView 自身 20 類粗分類（非 JPX 官方 33 業種——後者本次未能透過自動化工具取得逐檔對應表，
是誠實列出的分類口徑差異）；完整分布與前 12 大分類的 ROE 中位數由 `_build_hub.py` 對 `_universe.json`
現算並嵌入頁面 Exhibit 4，不在此報告重複列出精確數字（避免日後母體更新時本報告與頁面數字不同步）。

## 四、缺值率（939 檔，替換後）

| 欄位 | 缺值率 | 判讀 |
|---|---|---|
| market_cap／sector／industry／close／price_book | 0%–0.4% | 全數或近全數取得 |
| trailing_pe | 3.5% | 多為近期虧損，PE 無意義，屬業務事實 |
| forward_pe | 11.8% | 分析師覆蓋不足，日股中小型股常見 |
| roe | 5.6% | 個別公司財報結構特殊或近期虧損 |
| dividend_yield（含不配息股） | — | 33 檔不配息，未列入殖利率中位數計算分母 |
| cash | 7.7% | 部分金融股資產負債表結構特殊，Yahoo/TradingView 不 populate 此欄，屬業務事實非缺失 |

## 五、盲區自陳

1. **JPX 官方 33 業種分類未取得**：本頁產業分類全部採 TradingView 自身粗分類（20 類），與東證官方
   33 業種分類口徑不同，兩者不可互換引用；若需業種層級精確對照，須另外查證 JPX 官方分類對照表。
2. **total_debt／revenue_growth／net_income_growth／operating_margin／gross_margin 未做 yfinance 整欄替換**：
   雖然抽樣顯示偏差超過 5%，但這些欄位並未用於本頁計分卡或五個論點卡的計算，經評估後判定替換的優先序
   低於頁面實際引用的四個欄位（trailing_pe／forward_pe／roe／dividend_yield），故保留 TradingView 原值，
   列為誠實揭露的方法論取捨，非疏漏。
3. **子頁（七個投資鏡頭）仍使用先前 476 檔母體計算**：compounders／governance／financials／dividends／
   events／ai-chain／domestic 七個子頁是在本輪母體重建之前完成的獨立研究，其量化篩選結果（如「476 檔
   篩出 70 檔候選」「105/476 落在 P/B&lt;1」）皆以先前 476 檔母體為分母，本頁 hub 引用子頁結論時已明寫
   「476 檔母體」字樣以資區分，不與新母體 939 檔的數字混寫成同一口徑。
4. **候選清單本身依賴 TradingView 篩選器的即時性與正確性**：若 TradingView 的 exchange／subtype／
   market_cap_basic 欄位本身有分類錯誤或延遲更新，本頁母體會同樣繼承該誤差；本輪僅能透過 40 檔抽樣與
   yfinance 交叉比對做有限度的品質驗證，無法做到逐檔獨立複核全部 939 檔。
5. **REIT 排除規則的邊界**：僅排除 `industry = "Real Estate Investment Trusts"` 這一個精確字串匹配的
   40 檔，未逐檔人工複核是否有其他信託／基金結構的公司使用不同 industry 標籤逃過此規則；已交叉檢查
   全部 20 類 sector 與逐一 industry 標籤中含「trust」「fund」「reit」關鍵字者，僅此 40 檔命中，
   信心度高但非窮舉式人工複核。
