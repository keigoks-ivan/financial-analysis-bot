你是 stock-analyst v20 DD 的證據採集子 agent。標的：CVNA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Carvana Co. product substitute technology threat 2026
  - Auto & Truck Dealerships alternative technology disruption 2026 2027
  - CVNA Carvana Co. technology obsolescence risk
  - Auto & Truck Dealerships next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm｜as_of：2026-02-18
<<<
Our Company Carvana is the leading e-commerce platform for buying and selling used cars. We are transforming the used car buying and selling experience by giving consumers what they want - a wide selection, great value and quality, transparent pricing, and a simple, no pressure transaction. Our differentiated business model combines a comprehensive online sales experience with a vertically integrated supply chain, designed to sell high-quality vehicles to our customers transparently and efficiently at a low price. The automotive retail industry is large – with approximately 37 million used auto retail transactions in the United States (“U.S.”) in 2024 according to Cox Automotive – and highly fragmented – with the top 10 used auto retailers in the U.S. accounting for less than 10% of the market share in 2024. These dynamics create an exceptional opportunity for disruption that our custom-built business model can capitalize on to remain well-positioned for long term growth. Over the years, we have leveraged our growing logistics network, which spans 316 metropolitan statistical areas, and our in-house distribution network, servicing over 80% of the U.S. population as of December 31, 2025, to sell 2.8 million retail vehicles, generating $84.1 billion in total revenue since inception in 2012 through December 31, 2025.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm｜as_of：2026-02-18
<<<
Adverse conditions affecting one or more automotive manufacturers could also impact the supply of vehicles and our inventory, change consumer car purchasing behaviors, and have a material adverse effect on our sales and results of operations. Manufacturer recalls and the increased regulatory scrutiny surrounding selling used vehicles with open safety recalls could adversely affect used vehicle sales or valuations, cause us to temporarily remove vehicles from inventory, cause us to sell affected vehicles at a loss, cause us to incur increased costs, and expose us to litigation and adverse publicity related to the sale of recalled vehicles. Further adverse conditions, including labor disruptions at manufacturer facilities, may affect the market for new vehicles, thereby affecting the supply and market for used vehicles.

We rely on a combination of internal and external logistics to transport vehicles to and from wholesale auctions, IRCs, hubs, vending machines, and our customers. As a result, we are exposed to risks associated with the transportation industry such as weather, traffic patterns, gasoline prices, recalls affecting our vehicle fleet, local and federal regulations, vehicular crashes, insufficient internal capacity, rising prices of transportation vendors, taxes, license and registration fees, insurance premiums, self-insurance levels, difficulty in recruiting and retaining qualified drivers, disruption of our technology systems, equipment supply, equipment quality, and increasing equipment and operational costs. Our failure to successfully manage our logistics and fulfillment process could cause a disruption in our inventory supply chain and distribution, which may adversely affect our operating results and financial condition. Capacity constraints, labor shortages, and regulatory changes affecting hours-of-service and emissions may increase cost-to-deliver and extend cycle times.

16 Our use of artificial intelligence may not perform as expected and could expose us to technological, operational, legal, and reputational risks that could adversely affect our business, financial condition, and results of operations We increasingly develop and deploy AI technology through third party generative AI platforms and internal software, in connection with our proprietary systems and customer experiences, including automated, self-service workflows, AI-enabled customer support tools, internal work efficiencies, and enhancement of our recruiting and hiring processes. These initiatives are complex, rapidly evolving, and inherently uncertain. There is no assurance that our AI capabilities will function as intended, deliver anticipated benefits, or scale cost-effectively. The performance, quality, and impact of AI models depend on numerous factors, including the availability and integrity of training data, model design, computational resources, integration with our operations and technology stack, and ongoing monitoring and governance. If our AI systems or those third party platforms we utilize underperform, produce inaccurate, incomplete, or biased outputs, hallucinate or fail under edge cases, degrade customer experiences, inadvertently disclose or misuse intellectual property, or otherwise fail to meet expectations, we could experience decreased conversion, operational disruptions, increased costs, reduced margins, customer dissatisfaction, negative publicity, or harm to our brand and competitive position. Increased use of AI may additionally result in cybersecurity, data privacy, and labor and employment risks.

If our cybersecurity measures are breached or there is a disruption in our technology systems, our business, brand, operating results, and financial condition could be harmed.

If an actual or perceived breach of our security occurs or there is a disruption in our technology systems, we could lose competitively sensitive business information, intellectual property or experience compromise of our information processes or internal controls. In addition, the public perception of the effectiveness of our security measures or services could be harmed, and we could lose employees, customers, and business partners. In the event of a security breach, we could suffer financial exposure in connection with demands from perpetrators, penalties and fines, remediation efforts, investigations and legal proceedings, and changes in our security and system protection measures. In the event of an error, defects, disruptions, or other performance or reliability problems with our network operations, our customers’ physical or electronic access to our inventory, or purchase, financing, and fulfillment process, and our access to data that drives our inventory purchase operations could be interrupted as well as cause delays and additional expense in arranging access to new facilities and services, any of which could harm our reputation, business, operating results, and financial condition.

19 We have acquired, and may continue to acquire, other companies or technologies, which could divert our management’s attention, result in additional dilution to our stockholders and otherwise disrupt our operations and harm our operating results.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
