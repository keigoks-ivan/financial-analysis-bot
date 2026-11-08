你是 stock-analyst v20 DD 的證據採集子 agent。標的：ANET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - ANET Arista Networks top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Arista Networks customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
Our Customers Our customers include large cloud customers or Cloud and AI Titans, other internet and service providers, including specialty and AI Neoclouds, and a wide breadth of enterprise customers, including financial services organizations and government agencies. We continue to diversify the types of enterprise customers we serve and have expanded our presence across a wide spectrum of industries, including media and entertainment, healthcare, oil and gas, education, manufacturing and industrial sectors, among others. Two of our customers accounted for more than 10% of our sales for the year ended December 31, 2025. Sales to these two customers represented 26% and 16% of our total revenue for the year ended December 31, 2025, respectively.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
Large purchases by a relatively limited number of customers have accounted for a significant portion of our revenue. For example, sales to one end customer represented 16%, 15%, and 21% of our total revenue, and sales to the other end customer represented 26%, 20%, and 18% of our total revenue for the years ended December 31, 2025, 2024, and 2023, respectively. We have experienced unpredictability in the timing of orders from our large customers primarily due to the overall complexity of these large orders and changes in demand specific to these customers, including reductions in or changes in the mix of capital expenditures by these customers and the impact of cost reduction and other efficiency efforts by these customers. In addition, the variability in customer concentration is linked to the timing of new product deployments, and spending cycles with these customers, as well as the time it takes these customers to evaluate, test, qualify and accept our products and services, and we expect continued variability in our customer concentration and timing of sales on a quarterly and annual basis.…

Our business is reliant on demand for network infrastructure, which rises and falls in cycles. Moreover, business cycles vary somewhat in different geographical regions and by customer type. Our customers’ demand is driven by, among other factors, the development of new network infrastructure and the refreshment of existing network infrastructure. Cyclical changes in our customers’ demand for our products and services, particularly changes in the demand of our largest customers, could result in fluctuations in our revenue, revenue growth and results of operations. We believe that this cyclicality results from a number of factors, including the specific procurement, budgeting and deployment cycles of our customers as well as the impact of general economic conditions on business operations and investment. The effects of supply chain disruptions and our rapid growth may have reduced the impact of cyclical factors that might otherwise have influenced our business and broader industry performance. If our growth rates slow, cyclical variations in our operations may become more pronounced over time and may materially affect our business, financial condition, results of operations and prospects.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
Historically, a limited number of customers have accounted for a significant portion of our revenue. Two of our customers accounted for more than 10% of our total revenue in each of the last three years. Sales to one end customer represented 16%, 15%, and 21% of our total revenue, and sales to the other end customer represented 26%, 20%, and 18% of our total revenue for the years ended December 31, 2025, 2024, and 2023, respectively. We have experienced unpredictability in the timing of orders from our high-volume customers, primarily due to the inherent complexity of large-scale orders and fluctuations in their specific demand. This includes reductions or shifts in their capital expenditure budgets, as well as the impact of their internal cost-reduction and efficiency initiatives. Furthermore, variability in customer concentration is driven by the timing of new product deployments, customer spending cycles, and the extensive periods required for evaluation, testing, and qualification. We expect this variability in concentration and sales timing to continue on both a quarterly and annual basis.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 8. Financial Statements｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
We market and sell our products through both our direct sales force and our channel partners, including distributors, value-added resellers, system integrators and OEM partners, and in conjunction with various technology partners. Significant customers are those that represent more than 10% of our total revenue during the period. There were two end customers who represented more than 10% of our total revenue for the years ended 2025, 2024 and 2023. Sales to one end customer represented 16%, 15% and 21% of our total revenue, and sales to the other end customer represented 26%, 20% and 18% of our total revenue for the years ended December 31, 2025, 2024 and 2023, respectively. As of December 31, 2025, and 2024, our top two resellers accounted for 52% and 50% of total accounts receivable, respectively.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
