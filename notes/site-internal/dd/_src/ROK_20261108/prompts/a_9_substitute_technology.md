你是 stock-analyst v20 DD 的證據採集子 agent。標的：ROK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Rockwell Automation product substitute technology threat 2026
  - Specialty Industrial Machinery alternative technology disruption 2026 2027
  - ROK Rockwell Automation technology obsolescence risk
  - Specialty Industrial Machinery next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1024478/000102447825000116/rok-20250930.htm｜as_of：2025-11-12
<<<
We are subject to macroeconomic cycles and when recessions occur, we may experience reduced, canceled or delayed orders, payment delays or defaults, supply chain disruptions, or other adverse events as a result of the economic challenges faced by our customers, prospective customers, and suppliers. As our distributor partners and customers work to manage working capital and inventory levels, we may experience volatility in orders.

Changes in trade policies, including the imposition of new tariffs or increases in existing tariffs between the United States, Mexico, Canada, China or other countries, or reactionary measures including retaliatory tariffs, legal challenges, or currency manipulation, could adversely affect our cost structure and profitability. If tariffs on imported materials, components, or finished goods increase, our manufacturing and supply chain costs may rise. Furthermore, changes to trade policies, retaliatory measures, or prolonged uncertainty in trade relationships could result in supply chain disruptions, delayed shipments, or increased operational complexity, adversely affecting our business and financial results. While we take steps to mitigate or avoid these increased costs and disruptions, our ability to do so may be limited by operational and supply chain constraints, especially in the short term. In addition, our ability to recover cost increases and maintain profitability levels through price adjustments may be limited by competitive pressures, customer acceptance, and contractual limitations.

We face the potential harms of natural disasters, including those as a result of climate change, pandemics, acts of war, terrorism, international conflicts, or other disruptions to our operations, the duration and severity of which are highly uncertain and difficult to predict.

Our business depends on the movement of people and goods around the world. Natural disasters (including but not limited to those as a result of climate change), pandemics, acts or threats of war or terrorism, international conflicts, power outages, fires, explosions, equipment failures, sabotage, political instability, and the actions taken by governments could cause damage to or disrupt our business operations, our distribution network, our suppliers or our customers, and could create economic instability. Disruptions to our information technology (IT) infrastructure from system failures, shutdowns, power outages, telecommunication or utility failures, and other events, including disruptions at third-party IT and other service providers, could also interfere with or disrupt our operations. Although it is not possible to predict such events or their consequences, these events could decrease demand for our hardware and software products, solutions, or services, increase our costs, or make it difficult or impossible for us to deliver products, solutions, or services.

Volatility and disruption of the capital and credit markets may result in increased costs to maintain our capital structure.

Any of these uncertainties could adversely affect our profitability and ability to compete. We also maintain several single-source supplier relationships because either alternative sources are not available, or the relationship is advantageous due to performance, quality, support, delivery, capacity, or price considerations. Unavailability of, or delivery delays for, single-source components or products could adversely affect our ability to ship the related products in a timely manner. The effect of unavailability or delivery delays would be more severe if associated with our higher volume and more profitable products. Even where substitute sources of supply are available, qualifying alternative suppliers and establishing reliable supplies could cost more or result in delays and a loss of sales.

6 Table of Contents Product and Services Security Our hardware and software products, services and solutions are used by our customers in applications that may be subject to information theft, tampering, sabotage, or cyber-attacks. Careless or malicious actors could cause a customer’s process to be disrupted or could cause equipment to operate in an improper manner, resulting in harm to people or property. To a significant extent, the security of our customers’ systems depends on how those systems are designed, installed, protected, configured, updated, and monitored, and much of this is typically outside our control. In addition, both software and hardware supply chains can introduce security vulnerabilities into many technologies across the industry. Past global cyber-attacks have also been perpetuated by compromising software updates in widely used software products, posing the risk that vulnerabilities or malicious content could be inserted into our products. In some cases, it is possible that malware attacks could spread throughout the supply chain, moving from one company to the next via authorized network connections. We have designed a Secure Development Lifecycle Program that incorporates appropriate security activities into the necessary development and support practices for our commercial product offerings. The Secure Development Lifecycle Program is audited annually by third-party firms.…

Our success depends in part on our ability to anticipate and offer hardware and software products and services that appeal to the changing needs and preferences of our customers in the various markets we serve. Developing new hardware and software products and service offerings requires high levels of innovation, and the development process is often lengthy and costly. If we are not able to anticipate, identify, develop, and market products that respond to changes in customer preferences and emerging technological and broader industry trends, including the adoption and integration of AI, demand for our products could decline.

We rely on our distribution channel for a substantial portion of our sales. In North America, a large percentage of our sales are through distributors. In certain other countries, the majority of our sales are also through a limited number of distributors. We depend on the capabilities and competencies of our distributors to sell our hardware and software products, solutions, and services and deliver value to our customers. Disruptions to our existing distribution channel or the failure of distributors to maintain and develop the appropriate capabilities to sell our hardware and software products, solutions, and services could adversely affect our sales. A disruption could result from the sale of a distributor to a competitor, financial instability of a distributor, or other events.

We plan to invest over $2 billion over the next five years in manufacturing facilities, digital infrastructure, and talent to support market share growth, operational resilience, and margin expansion. These investments are intended to complement our productivity initiatives and enable long-term global growth. However, there is no assurance that these investments will yield the anticipated benefits. Risks include delays in implementation, cost overruns, supply chain disruptions, and challenges in integrating automation and technologies into our business and manufacturing operations. Additionally, if market conditions change or expected efficiencies do not materialize, the return on these investments may be lower than projected. Furthermore, due to global economic factors or company profitability targets, we may invest at a slower pace than planned, which could impact our ability to achieve desired outcomes. Failure to realize the expected outcomes could negatively impact our operating results and financial condition.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROK_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
