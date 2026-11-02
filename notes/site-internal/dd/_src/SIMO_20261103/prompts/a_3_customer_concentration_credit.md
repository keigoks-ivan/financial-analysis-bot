你是 stock-analyst v20 DD 的證據採集子 agent。標的：SIMO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - SIMO Silicon Motion Technology top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Silicon Motion Technology customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-04-30）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm｜as_of：2026-04-30
<<<
We derived a substantial portion of our revenue from sales to a relatively small number of customers. As a result, the loss of any significant customer could materially and adversely affect our financial condition and results of operations. Sales to our five largest customers represented approximately 61%, 66% and 66% of our net revenue in 2023, 2024 and 2025, respectively. Sales to our customers constituting more than 10% of our net revenue represented, in the aggregate, 45%, 57% and 58% of our net revenue in 2023, 2024 and 2025, respectively. Our customers constituting more than 10% of our net revenue were (i) Micron, SK Hynix and AFASTOR in 2023, (ii) Micron, Kioxia, PHISEMI and AFASTOR in 2024 and (iii) PHISEMI, Kioxia, AFASTOR, and Micron in 2025. The identities of our largest customers and their respective contributions to our net revenue may vary from period to period.

We expect that we will continue to depend on a relatively limited number of customers for a substantial portion of our net sales and our ability to maintain good relationships with these customers will be important to the ongoing success of our business. We cannot assure you that revenues generated from these customers, individually or in the aggregate, will reach or exceed historical levels in any future period. Our failure to meet the demands of these customers could lead to cancellation or reduction of businesses from these customers. In addition, any loss, cancellation or reduction of businesses from, significant change in scheduled deliveries to, or decrease in the prices of products sold to any of these customers could significantly reduce our revenues and adversely affect our financial condition and operating results. Moreover, any difficulty in collecting outstanding amounts due from our customers particularly customers who place large orders, would harm our financial performance. In addition, if our relationships with our largest customers are disrupted for any reason, it could have a significant impact on our business.

A substantial portion of our business is conducted outside of the United States and, as a result, we are subject to foreign business, political and economic risks. Most of our ICs are manufactured, assembled and tested by third parties located in China and Taiwan. We generated 91%, 98% and 99% of our revenue in 2023, 2024 and 2025, respectively, from sales to customers outside the United States, and for the year ended December 31, 2025, 79% of our revenue was from sales in three jurisdictions China, Japan and Singapore. Our controller R&D is conducted primarily in Taiwan and our SSD solutions R&D is conducted in both China and Taiwan. Most of our corporate functions are located in Taiwan. These operations are directly influenced by the political and economic conditions of the country in which they are located. We do not expect the portion of our business located outside of the United States to change in the future.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-04-30）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm｜as_of：2026-04-30
<<<
Our Customers We sell our products to NAND flash makers, module makers and OEMs worldwide that service multiple markets including computing, data center, mobile, automotive and industrial markets. Most of our high — performance flash memory storage controllers are supplied to NAND flash manufacturers. We are a leading supplier of SSD controllers used in PCs, mobile phones, data centers, automotive and other client devices and a leading merchant supplier of eMMC and UFS controllers used in smartphones and IoT devices. Sales to our five largest customers represented approximately 61%, 66% and 66% of our net revenue in 2023, 2024 and 2025, respectively. Sales to our customers constituting more than 10% of our net revenue represented, in the aggregate, 45%, 57% and 58% of our net revenue in 2023, 2024 and 2025, respectively. Our customers constituting more than 10% of our net revenue were (i) Micron, SK Hynix and AFASTOR in 2023, (ii) Micron, Kioxia, PHISEMI and AFASTOR in 2024 and (iii) PHISEMI, Kioxia, AFASTOR, and Micron in 2025. The identities of our largest customers and their respective contributions to our net revenue may vary from period to period.

Sales and Marketing We market and sell our products worldwide through a combination of direct sales personnel and independent electronics distributors. Our direct sales personnel are strategically located near our NAND flash manufacturer, leading technology OEM and modular maker customers in Taiwan, Korea, China, the United States, and Japan. Approximately 65% of our sales in 2023, 65% of our sales in 2024, and 53% of our sales in 2025 were attributable to our direct sales force while the remainder was attributable to distributors.
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-04-30）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm｜as_of：2026-04-30
<<<
Net sales Mobile Storage 796,365 99 877,195 99 80,830 10 Others 7,187 1 8,432 1 1,245 17 Net sales 803,552 100 885,627 100 82,075 10 In 2025, our net sales increased by 10% year-over-year to approximately US$885.6 million, primarily due to the continuing new products and new customers ramp and increase in market share with NAND makers, module makers and OEM customers. Our mobile storage revenue increased by 10% year-over-year primarily because of an increase in sales of eMMC and UFS controllers, partially offset by a decline in sales of SSD controllers and SSD solutions. Our SSD controller sales decreased in the range of 0% to 5% year-over-year to account for 45% to 50% of revenue, a lower percentage of net sales than the prior year, eMMC plus UFS controller sales increased in the range of 20% to 25% year-over-year to account for 40% to 45% of revenue, a higher percentage of net sales than the prior year, and SSD solutions sales decreased in the range of 10% to 15% year-over-year to account for 0% to 5% of revenue, a lower percentage of net sales than the prior year.
>>>

[4] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-04-30）｜章節：其他章節（財報附註等）｜url：https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm｜as_of：2026-04-30
<<<
F-9 Table of Contents Concentration of Credit Risk and Significant Customers Financial instruments that potentially subject the Company to a significant concentration of credit risk consist principally of cash equivalents and accounts receivable. Cash and cash equivalents are maintained with high quality financial institutions, the composition and maturities of which are regularly monitored by management. The Company believes that the concentration of credit risk in its accounts receivable is substantially mitigated by the Company’s credit evaluation process, relatively short collection terms and the high level of credit worthiness of its customers. The Company performs ongoing credit evaluations of its customers’ financial conditions and limits the amount of credit extended based upon the payment history and current credit worthiness of the customer. The Company regularly reviews the allowance for bad debt and doubtful accounts or expected losses during the accounts receivable collection process by considering factors, such as historical write-off and recovery experience, credit quality, age of the accounts receivable balances and current economic conditions that may affect a customer’s ability to pay. The Company also takes into account reasonable and supportable forecasts of future conditions when evaluating the adequacy of the allowance for doubtful accounts.

Historically, a relatively small number of customers have accounted for a significant portion of our net sales. Sales to three customers in 2023, four customers in 2024, and four customers in 2025 each accounted for 10% or more of our net revenue, representing 45%, 57% and 58% of our net sales in 2023, 2024 and 2025, respectively. In 2023, the significant customers were SK Hynix, Micron and AFASTOR. In 2024, they were Micron, Kioxia, PHISEMI and AFASTOR. In 2025, they were PHISEMI, Kioxia, AFASTOR and Micron. The Company’s top ten customers in 2023, 2024 and 2025 accounted for approximately 75%, 84% and 82% of net sales, respectively.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
