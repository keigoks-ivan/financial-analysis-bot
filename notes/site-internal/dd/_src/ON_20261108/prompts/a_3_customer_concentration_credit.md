你是 stock-analyst v20 DD 的證據採集子 agent。標的：ON。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - ON ON Semiconductor top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - ON Semiconductor customer concentration risk disclosure
  - bankruptcy OR downgrade OR guidance cut 2026
  (na_allowed=true)


## 規則（嚴格遵守，違反視為無效輸出）
1. **只回 sourced claim**：每條 finding 必須有可查證的 source（URL 或明確可搜尋到的來源名＋標題）與 as_of（該資訊的發布/生效日期，非你查詢的日期）。
2. **查不到就 status="none"**，並列出你實際下過的 queries_run（至少 1 條，需與你實際搜尋詞一致，不得事後編造）。軸清單裡的 `queries` 是起點不是配額，同一次搜尋的來源可同時支撐多個軸。**不得因為查無所獲就用訓練知識/常識填 claim。**
3. **三種狀態不得混用**：found＝有 sourced claim；none＝軸適用於本標的業態、但搜尋查無來源；not_applicable＝該軸對本標的業態根本不成立（例：銀行沒有「最大客戶導入第二供應商」、零售商的客戶是終端消費者）。**軸對此業態不適用時回 not_applicable 並在 note 寫理由，不要回 none。**只有軸物件標 na_allowed=true 才可回 not_applicable，沒標的軸只能 found 或 none；拿不準是否適用就當適用、照常搜尋，不要用 not_applicable 省搜尋。
4. **不臆測、不外推**：claim 只寫你實際找到的事實，不要自己推論「這意味著」，那是判斷層的工作。
5. direction 欄：這條 finding 對本標的是正面(+)／中性(0)／負面(-)，僅標事實方向，不要寫成裁決語。
6. affects 欄：這條 finding 影響哪些判斷面（可填 moat_trend／thesis.H／thesis.R／decision_inputs.bear／valuation／triggers 等，可複選）。
7. **現價一律引 `numbers.price_at_dd`／`price_as_of`，不得自行寫「現價」數字**：市值、距 52 週高低點 %、目標價 vs 現價，一律引用該欄，不從聚合站另抓現價字面數字。
8. **原始證據與解讀分開存**：每條 finding 另填三欄——`url`（實際讀到的網址，沒有就填 null）、`excerpt`（從該來源**逐字複製**、支撐 claim 的原文，≤300 字，不得改寫或翻譯）、`excerpt_from`（`snippet`＝搜尋摘要／`page`＝WebFetch 讀到的頁面）。`claim` 是你對原文的精簡轉述；`excerpt` 是證據本身。找不到可逐字複製的原文就填 null，不要自己寫一句當原文。

## 程式已抓好的一手文件摘錄（本軸）
以下為程式抓取的一手文件摘錄，可直接逐字引用（附 url 與 as_of）：
- 引用時 finding 的 `url`、`as_of` 照該則標示填；`source` 寫「來源＋文件」；`excerpt` 從「<<<」「>>>」之間**逐字複製**（≤300 字，取最能支撐 claim 的連續一段，不改寫、不翻譯）；`excerpt_from` 填 `"page"`。
- 一手清單顯示沒有某類事件時（例如「標題含關鍵字者 0 則」），可據此寫一條「經查一手紀錄無此類事件」的 finding（status=found、direction=`"0"`），excerpt 用清單本身那一句統計；不要因為沒找到事件就標 none。
- 這些摘錄不算你的搜尋：`queries_run` 只記你自己實際下過的搜尋；摘錄仍可另外搜尋補充，但不必為了湊證據重搜摘錄已涵蓋的內容。
- 摘錄與本軸問題無關或不足以回答時，照常搜尋；仍查不到才記 none。

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm｜as_of：2026-02-09
<<<
Distributors Sales to distributors accounted for approximately 54%, 53% and 52% of our revenue in 2025, 2024 and 2023, respectively. We had one distributor whose revenue accounted for approximately 11% and 10% of the total revenue for the years ended December 31, 2025 and 2024, respectively. There were no distributors whose revenue accounted for more than 10% of total revenue for the year ended December 31, 2023. Our distributors provide fulfillment services and resell our products to OEMs, contract manufacturers, and other end-customers. Sales to distributors are typically made pursuant to agreements that provide return rights and stock rotation provisions permitting limited levels of product returns.

Direct Customers Sales to direct customers accounted for approximately 46%, 47% and 48% of our revenue in 2025, 2024 and 2023, respectively. Large multi-national companies and selected regional OEMs, which are significant in specific markets, form our core direct customers. Generally, these customers do not have the right to return our products following a sale other than pursuant to our warranty.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm｜as_of：2026-02-09
<<<
A significant portion of our sales are made to customers within the automotive industry and the industrial sector, and the demand for our products depends in part on the market conditions in these end-markets. Sales into the automotive and industrial end-markets represented approximately 51% and 28% of our revenue, respectively, for the year ended December 31, 2025. The automotive industry is cyclical and the industrial sector tends to thrive during a time of economic expansion. As a result, our customers in each end-market are sensitive to changes in general economic conditions, inflationary pressure, changes in interest rates, disruptive innovation and end-market preferences, any of which can adversely affect sales of our products and, correspondingly, our results of operations. Changes in demand in these end-markets (such as fluctuations in demand for EVs), or changes that have the potential to disrupt sales activities to customers in these end-markets, can significantly impact our operating results. Additionally, the quantity and price of our products sold to customers in each end-market could decline despite continued growth in such end-markets. Lower sales to customers in either end-market may have a material adverse effect on our business and results of operations.

We had one customer, a distributor, whose revenue accounted for approximately 11% and 10% of the total revenue for the years ended 2025 and 2024, respectively, across all reportable segments. Although we are not dependent on any single customer, a significant disruption in key customer relationships could adversely affect our business. Further, we could experience fluctuations in our customer base or the mix of revenue by customer or end-market, as markets and strategies evolve.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm｜as_of：2026-02-09
<<<
Total $ 1,983.9 33.1 % $ 3,216.1 45.4 % $ (1,232.2) (1)Gross profit margin as a percent of respective segment revenue balances Revenue Revenue was $5,995.4 million and $7,082.3 million for 2025 and 2024, respectively. The decrease from 2024 to 2025 of $1,086.9 million, or 15.3%, was attributable primarily to lower sales volumes across all reportable segments, which are further explained below. We had one customer, a distributor, whose revenue accounted for approximately 11% and 10% of the total revenue for the years ended December 31, 2025 and 2024, respectively, with sales across all reportable segments.

Revenue Revenue was $7,082.3 million and $8,253.0 million for 2024 and 2023, respectively. The decrease from 2023 to 2024 of $1,170.7 million, or 14.2%, was attributable primarily to lower sales volumes across all segments, which are further explained below. We had one customer, a distributor, whose revenue accounted for approximately 10% of our total revenue for the year ended December 31, 2024, with sales across all reportable segments. There was no customer whose revenue exceeded 10% of total revenue for the year ended December 31, 2023.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：其他章節（財報附註等）｜url：https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm｜as_of：2026-02-09
<<<
Revenue and gross profit for the Company’s operating and reportable segments were as follows (in millions): PSG AMG ISG Total Year ended December 31, 2025: Revenue from external customers $ 2,805.1 $ 2,261.9 $ 928.4 $ 5,995.4 Cost of revenue 2,117.6 1,105.4 788.5 4,011.5 Segment gross profit $ 687.5 $ 1,156.5 $ 139.9 $ 1,983.9 Year ended December 31, 2024: Revenue from external customers $ 3,348.2 $ 2,609.1 $ 1,125.0 $ 7,082.3 Cost of revenue 1,963.8 1,302.8 599.6 3,866.2 Segment gross profit $ 1,384.4 $ 1,306.3 $ 525.4 $ 3,216.1 Year ended December 31, 2023: Revenue from external customers $ 3,880.4 $ 3,057.1 $ 1,315.5 $ 8,253.0 Cost of revenue 2,058.5 1,635.8 675.2 4,369.5 Segment gross profit $ 1,821.9 $ 1,421.3 $ 640.3 $ 3,883.5 The Company had one customer, a distributor, whose revenue accounted for approximately 11% and 10% of total revenue for the years ended December 31, 2025 and 2024, respectively, with sales across all reportable segments. No customer exceeded 10% of the total revenue for the year ended December 31, 2023. One customer, a distributor, accounted for approximately 10% and 13% of the Company's accounts receivable balance as of December 31, 2025 and 2024, respectively.
>>>


## 回傳格式（嚴格 JSON 契約，不得夾雜其他文字；一次 Write）
```json
{
  "coverage": {
    "<axis_id>": {
      "status": "found|none|not_applicable",
      "queries_run": ["...", "..."],
      "findings": [
        {"claim": "...", "source": "...", "url": "https://...", "excerpt": "逐字原文…", "excerpt_from": "snippet|page", "as_of": "YYYY-MM-DD", "direction": "+|0|-", "affects": ["moat_trend"]}
      ],
      "note": "",
      "clues": [
        {"claim": "...", "source": "...", "url": "https://...", "as_of": "YYYY-MM-DD", "direction": "+|0|-", "affects": ["moat_trend"], "match_terms": ["預期原文逐字出現的字串", "..."]}
      ]
    }
  }
}
```

`clues` 選填、每軸一個陣列，沒有就整個欄位省略。只在你**找到有網址的線索、但沒讀到頁面而拿不到可逐字複製的原文**時放；程式會打開該網址，在全文裡找 `match_terms` 同時出現的一段原文，找到就升級成帶原文的 finding；找不到（或頁面打不開）就照 `excerpt_from: "snippet"`、`excerpt: null` 的 finding 保留，並標為未核原文。
- 只有 clues、findings 是空的時，`status` 填 `none`（程式核實到原文後會自動改成 `found`）。
- `url` 必須是你在搜尋結果裡實際看到的網址；不得編造、不得猜網址、不得填網站首頁。沒有網址的線索不要放（寫進 note）。已經寫在 findings 的網址不要重複放。
- `match_terms` 放 2～5 個預期原文會逐字出現的字串：金額、比例、專有名詞、引號裡的關鍵詞。照原文可能的寫法填，不要改寫或翻譯；不要放公司名、代號、年份或「營收」「公司」這類到處都有的詞。
- 其餘欄位（`claim`、`source`、`as_of`、`direction`、`affects`）規則同 findings；`as_of` 填你推估的文章發布日，程式讀到頁面發布日會以頁面為準。

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
