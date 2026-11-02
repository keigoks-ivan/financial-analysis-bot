你是 stock-analyst v20 DD 的證據採集子 agent。標的：CLS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - CLS Celestica top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Celestica customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
In recent years, we have experienced an increasing shift in the mix of our programs towards cloud-based and other service providers, primarily hyperscalers, which are cyclically different from our traditional OEM customers, and currently experiencing a period of significant increases in product deployments to support their build-out of data center infrastructure, including to support AI applications. This demand growth has required our business to place a greater focus on various operational factors, including the management of our manufacturing capacity, human capital dedicated to these programs, 5 supply chain, capital investments, and working capital requirements. Related to this trend, our CCS segment, including our HPS business, continues to grow. Our CCS segment revenue for 2025 increased 42% to $9.19 billion compared to $6.49 billion in 2024. HPS revenue for 2025 increased 81% compared to 2024. In 2025, HPS revenue accounted for 41% of our total revenue (2024 — 29%; 2023 — 21%).

Customer Concentration and Relationship Management We target industry-leading customers in each of our segments. Our CCS segment customers include Amazon Fulfillment Services, Inc., Meta Platforms, Inc., Google Inc., Ciena Corporation, Dell Technologies, Hewlett-Packard Enterprise, and IBM Corporation, Inc. Our ATS segment customers include Applied Materials, Inc., LAM Research and Honeywell Inc. We are focused on strengthening our relationships with strategic customers through the delivery of new and expanding end-to-end solutions.

We depend on a small number of customers for a substantial portion of our revenue. In the aggregate, our top 10 customers represented 79% of total revenue for 2025, 73% for 2024 and 64% for 2023. In 2025, three customers (all in our CCS segment) individually represented 10% or more of total revenue (32%, 14% and 12%). In 2024, two customers (each in our CCS segment) individually represented 10% or more of total revenue (28% and 11%). In 2023, one customer (in our CCS segment) individually represented 10% or more of total revenue (22%). Significant reductions in, or the loss of, revenue from these or any of our major customers may have a material adverse effect on us. See Item 1A, Risk Factors — "We are dependent on a limited number of customers and end markets and are sensitive to their investment cycles and operating conditions. Revenue decline or loss of any major customer could have a material adverse effect on our operating results, financial position and cash flows."
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
We depend (and expect to continue to depend) upon a small number of customers for a substantial portion of our revenue. In the aggregate, our top 10 customers represented 79% of total revenue for 2025, 73% for 2024 and 64% for 2023. In 2025, three customers in our CCS segment individually represented 10% or more of total revenue (32%, 14% and 12%). CCS segment revenue represented 74% of our consolidated revenue in 2025 (2024 — 67%; 2023 — 58%).

A decline in revenue from, or the loss of, any significant customer could have a material adverse effect on our operating results, financial position and cash flows, and may increase the variability of our operating results from period to period. We cannot assure: (i) the replacement of completed, delayed, cancelled or reduced orders with new business; (ii) that our current customers will continue to utilize our services consistent with historical volumes or at all; and/or (iii) that our customers will renew their long-term manufacturing or services contracts with us on acceptable terms or at all. There can also be no assurance that our efforts to secure new customers and programs will succeed in reducing our customer concentration. Failure to secure business from existing or new customers in any of our end markets would adversely impact our operating results. See "Our revenue and operating results may vary significantly from period to period."
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
Recent Developments Segment Environment: CCS Segment CCS segment revenue for 2025 increased 42% to $9.19 billion compared to $6.49 billion in 2024. Revenue in our Enterprise end market decreased by 19% in 2025 compared to 2024, driven by a technology transition in an AI/machine learning (ML) compute program with one of our hyperscaler customers. Revenue in our Communications end market increased by 81% in 2025 compared to 2024, driven by data center networking demand, including the ramping of our switch programs. HPS revenue for 2025 accounted for 41% of our total revenue and increased 81% compared to 2024, driven by accelerating volumes in our ramping networking switch programs with hyperscaler customers.

CCS segment revenue for 2025 increased $2,698.0 million (42%) compared to 2024. Communications end market revenue for 2025 increased $3,179.7 million (81%) compared to 2024, driven by data center networking demand, including the ramping of our switch programs. HPS revenue for 2025 increased 81% (to $5.0 billion) compared to 2024, and accounted for 41% of our total 2025 revenue (compared to 29% of our total 2024 revenue), driven by accelerating volumes in our ramping networking switch programs with hyperscaler customers. Enterprise end market revenue for 2025 decreased $481.7 million (19%) compared to 2024, driven by the technology transition in an AI/ML compute program with one of our hyperscaler customers.

CCS segment revenue for 2024 increased $1,849.3 million (40%) compared to 2023. Communications end market revenue for 2024 increased $1,271.1 million (48%) compared to 2023 driven by increased demand for HPS networking products from hyperscaler customers. HPS revenue for 2024 increased 63% (to $2.8 billion) compared to 2023, and accounted for 29% of our total 2024 revenue (compared to 21% of our total 2023 revenue), driven by strong demand for networking products from hyperscaler customers. Enterprise end market revenue for 2024 increased $578.2 million (29%) compared to 2023, driven primarily by stronger demand in our storage business and stronger demand for compute products from our hyperscaler customers.

We depend on a small number of customers for a substantial portion of our revenue. In the aggregate, our top 10 customers represented 79% of total revenue for 2025, 73% for 2024 and 64% for 2023. Three customers (all in our CCS segment) individually represented 10% or more of total revenue in 2025 (32%, 14%, and 12%). Two customers (both in our CCS segment) individually represented 10% or more of total revenue in 2024 (28% and 11%). One customer (in our CCS segment) individually represented 10% or more of total revenue in 2023 (22%).
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：其他章節（財報附註等）｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
18 % 22 % Malaysia 14 % 12 % Mexico * 10 % * Less than 10%. Customers: In 2025, three customers (all in our CCS segment) individually represented 10% or more of total revenue (32%, 14% and 12%). In 2024, two customers (both in our CCS segment) individually represented 10% or more of total revenue (28% and 11%). In 2023, one customer (in our CCS segment) individually represented 10% or more of total revenue (22%).
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
