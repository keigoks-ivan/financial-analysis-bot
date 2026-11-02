你是 stock-analyst v20 DD 的證據採集子 agent。標的：TER。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - TER Teradyne top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Teradyne customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm｜as_of：2026-02-19
<<<
The market for our test products is concentrated with a limited number of significant customers accounting for a substantial portion of the purchases of test equipment. A few customers drive sizable demand for our offerings both through direct sales and sales to the customer’s supply partners. We expect that sales of our test products will continue to be concentrated with a limited number of major customers for the foreseeable future.

Sales and Distribution In each of the years, 2025, 2024 and 2023, our five largest direct customers in aggregate accounted for 44%, 36%, and 32% of our consolidated revenues, respectively.

Teradyne typically has a specifying customer such as an OEM, IDM, or Fabless company, who chooses platforms and drives demand, and a purchasing customer who actually places the order and receives the equipment. In different cases, the specifying and purchasing customers have more influence in the purchase decision. In 2025, we had two customers who specified greater than 10% of our consolidated revenues and one additional customer who directly purchased more than 10% of our consolidated revenues. The two specifying customers were both customers of our Semiconductor Test and Product Test segments and drove 12% and 10% of consolidated revenues. The additional direct customer, a customer of our Semiconductor Test segment, accounted for 19% of consolidated revenues including certain revenues specified by other customers.

In 2024, we estimate one customer of our Semiconductor Test and Wireless Test segments, specified approximately 13% of our consolidated revenues. In 2023, one customer of our Semiconductor Test segment, accounted for approximately 10% of our consolidated revenues. The loss of, or significant decrease in demand from a significant OEM, IDM, or Fabless customer, or any of our five largest direct customers, could have a material adverse effect on our business, results of operations and financial condition.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm｜as_of：2026-02-19
<<<
The market for our products is concentrated with a limited number of significant global customers accounting for a substantial portion of the purchases of test equipment. In each of the years, 2025, 2024 and 2023, our five largest direct customers in aggregate accounted for 44%, 36% and 32% of consolidated revenues, respectively.

In 2025, we had two customers who specified greater than 10% of our consolidated revenues and one additional customer who directly purchased more than 10% of our consolidated revenues. The two specifying customers drove 12% and 10% of consolidated revenues. The additional direct customer accounted for 19% of consolidated revenues including certain revenues specified by our 10% specifiers.

If we were to lose any of our significant customers, if our products fail to meet changes in customers’ demands or if we suffer a material reduction in our customers’ purchase orders, our revenue could decline and our operating results and financial condition could be materially and adversely affected. We would have no or limited contractual recourse if our significant customers decided to stop buying and using our products with limited advance notice to us.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm｜as_of：2026-02-19
<<<
The market for our test products is concentrated with a limited number of significant customers accounting for a substantial portion of the purchases of test equipment. A few customers drive sizable demand for our offerings both through direct sales and sales to the customer’s supply partners. We expect that sales of our test products will continue to be concentrated with a limited number of major customers for the foreseeable future.

28 Table of Contents In 2025 and 2024, our five largest direct customers in aggregate accounted for 44% and 36% of our consolidated revenues, respectively. See Note V: “Segment, Geographic, and Significant Customer Information” for additional discussion of significant customer concentrations.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：其他章節（財報附註等）｜url：https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm｜as_of：2026-02-19
<<<
Item 7A: Quantitative and Qualitative Disclosures about Market Risks Concentration of Credit Risk Financial instruments which potentially subject us to concentrations of credit risk consist principally of cash equivalents, marketable securities, forward currency contracts and accounts receivable. Our cash equivalents consist primarily of money market funds invested in U.S. Treasuries and government agencies. Our fixed income available-for-sale marketable securities have a minimum rating of AA by one or more of the major credit rating agencies. We place forward currency contracts with high credit-quality financial institutions in order to minimize credit risk exposure. Concentrations of credit risk with respect to accounts receivable are limited due to the large number of geographically dispersed customers. We perform ongoing credit evaluations of our customers’ financial condition and from time to time may require customers to provide a letter of credit from a bank to secure accounts receivable. As of December 31, 2025, two customers primarily of our Semiconductor Test segment accounted for approximately 22% and 20%, respectively, of our accounts receivable balance. As of December 31, 2024, two customers of our Semiconductor Test segment each accounted for 10% of our accounts receivable balance.
>>>

[5] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 8. Financial Statements｜url：https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm｜as_of：2026-02-19
<<<
Concentration of Credit Risk Financial instruments which potentially subject us to concentrations of credit risk consist principally of cash equivalents, marketable securities, forward currency contracts and accounts receivable. Our cash equivalents consist primarily of money market funds invested in U.S. Treasuries and government agencies. Our fixed income available-for-sale marketable securities have a minimum rating of AA by one or more of the major credit rating agencies. Teradyne places forward currency contracts with high credit-quality financial institutions in order to minimize credit risk exposure. Concentrations of credit risk with respect to accounts receivable are limited due to the large number of geographically dispersed customers. Teradyne performs ongoing credit evaluations of our customers’ financial condition and from time to time may require customers to provide a letter of credit from a bank to secure accounts receivable. As of December 31, 2025, two customers of primarily our Semiconductor Test segment accounted for approximately 22% and 20%, respectively, of our accounts receivable balance. As of December 31, 2024, two customers of our Semiconductor Test segment each accounted for 10% of our accounts receivable balance.

Teradyne typically has a specifying customer such as an OEM, IDM, or Fabless company, who chooses platforms and drives demand, and a purchasing customer who actually places the order and receives the equipment. In different cases, the specifying and purchasing customers have more influence in the purchase decision. In 2025, we had two customers who specified greater than 10% of our consolidated revenues and one additional customer who directly purchased more than 10% of our consolidated revenues. The two specifying customers were both customers of our Semiconductor Test and Product Test segments and drove 12% and 10% of consolidated revenues. The additional direct customer, a customer of our Semiconductor Test segment, accounted for 19% of consolidated revenues including certain revenues specified by other customers. In 2024, we estimate one customer of the Semiconductor Test and Wireless Test segments, specified approximately 13% of consolidated revenues. In 2023, one customer of our Semiconductor Test segment accounted for approximately 10% of consolidated revenues.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
