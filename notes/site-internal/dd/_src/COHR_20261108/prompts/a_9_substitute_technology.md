你是 stock-analyst v20 DD 的證據採集子 agent。標的：COHR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Coherent product substitute technology threat 2026
  - Scientific & Technical Instruments alternative technology disruption 2026 2027
  - COHR Coherent technology obsolescence risk
  - Scientific & Technical Instruments next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm｜as_of：2026-08-14
<<<
Our markets are characterized by extensive research and development, rapid technological change, frequent new product introductions, changes in customer requirements and evolving industry standards. The nature of these markets requires significant research and development expenses to participate, with substantial resources invested in advance of material sales of our products to our customers. To compete effectively, we must continually address the challenges of dynamic and accelerating market trends and competitive developments. Otherwise, our product offerings may become less competitive given the frequent introduction of alternative or more cost-effective technologies. Because this industry is subject to rapid change, it is difficult to predict its potential size or future growth rate. We cannot ensure that our expenditures for research and development will result 16 Table of Contents in the launch of new products or, if such products are introduced, that those products will achieve sufficient market acceptance or generate sales to offset the costs of development. Our failure to address rapid technological changes in our markets, or the failure of either our customers’ or our products to gain market acceptance, or the failure of the markets in which we participate to grow could adversely affect our business and results of operations.

We provide components to contract manufacturers to produce finished or intermediary goods, and for some products a particular internal or external manufacturing site may be the sole qualified source. Our reliance on contract manufacturers exposes us to risks including reduced control over delivery schedules and planning, limited visibility into or availability of manufacturing capability and capacity, reliance on third-party quality assurance procedures, cybersecurity incidents or data security breaches affecting contract manufacturers, and the risk that disruptions at those manufacturers could require us to identify and qualify alternatives, which may be expensive and time-consuming and could result in supply interruptions and harm to customer relationships.

18 Table of Contents We may encounter increased competition, and we may fail to accurately estimate our competitors’ or our customers’ willingness and capability to backward integrate into our competencies and thereby displace us.

We may encounter substantial competition from other companies in the same market, including established companies with significant resources. Some of our competitors may have financial, technical, marketing, or other capabilities that are more extensive than ours. They may be able to respond more quickly than we can to new or emerging technologies and other competitive pressures. We may not be able to compete successfully against our present or future competitors. Our failure to compete effectively could have a material adverse effect on our business, results of operations, or financial condition.

We have a broad portfolio of products to address our customers’ needs, which span multiple market segments and are subject to rapid technological changes. We invest our capital in areas that we believe best align with our business strategy and optimize future returns. Investments in capital expenditures may not generate expected returns or cash flows. Significant judgment is required to determine which capital investments will result in optimal returns, and we could invest in projects that are ultimately 19 Table of Contents less profitable than those projects we do not select. Our strategic decision-making process involves careful evaluation and prioritization of investments to ensure alignment with our long-term goals. Additionally, we may choose to exit business segments that do not provide us with optimal returns. As we streamline our product portfolio, we may face execution risks that could impact our ability to support demand and maintain share in certain markets. Further, as we continue to make strategic investments to support customer demand, any delays in completion and ramping of expanded production facilities, or failure to optimize our investment choices, could significantly impact our ability to realize expected returns on our capital expenditures.

We are exposed to a variety of market risks, including the effects of increases in commodity prices and diminished availability of rare earth minerals and noble gases. Our businesses purchase, produce, and sell raw materials based upon quoted market prices from minor metal exchanges. Trade disputes, geopolitical tensions, economic circumstances, or political conditions may limit our ability to obtain certain materials. Although rare earth and other materials are generally available from multiple suppliers, China is the predominant producer of certain of these materials. In 2024, China imposed export restrictions on certain rare earth minerals such as yttrium and germanium, which disrupted and may continue to disrupt global supply chains, driving up costs. The negative impact from increases in commodity prices and diminished availability of rare earth minerals and noble gases might not be recovered through our product sales, which could have a material adverse effect on our results of operations and financial condition.

Our manufacturing processes and those of our contract manufacturers rely on many materials, including precious and rare earth metals, indium phosphide (“InP”) and certain lasers and laser components that may be difficult to source, may only be available from a single or limited number of suppliers. We have historically not had long-term contracts with our materials suppliers and a significant amount of our purchases are on a purchase order basis. Suppliers have previously, and may in the future, extend lead times, limit suppliers and place products on allocation, increase prices, or prioritize supplies for other customers, any of which could disrupt supply or increase demand in the industry and negatively impact our results of operations and our ability to fully meet our customers’ demand.

Cybersecurity attacks and incidents and other vulnerabilities could subject us to costly damages, claims and expenses, harm to our reputation or competitive position, or disrupt our operations and business.

Natural disasters or other global or regional catastrophic events could disrupt our operations, give rise to substantial environmental hazards, and adversely affect our results.

We and our subcontractors manufacture products using highly complex processes that require technologically advanced equipment and continuous modification to improve yields and performance. Difficulties in the manufacturing process or the effects from a shift in product mix can reduce yields or disrupt production and may increase our manufacturing costs. We and our subcontractors maintain operations and continuously implement new product and process technologies at manufacturing facilities, which are widely dispersed in multiple locations in several countries including the United States, Germany, Malaysia, and China. As a result of the interdependence within our network of manufacturing facilities, an operational disruption at one of our or a subcontractor’s facilities may have a disproportionate impact on our ability to produce many of our products.

From time to time, there have been disruptions in our manufacturing operations as a result of power outages, improperly functioning equipment, disruptions in supply of raw materials or components, or equipment failures. We have manufacturing and other operations in locations subject to natural occurrences and possible climate changes, such as severe and variable weather and geological events resulting in increased costs, or disruptions to our manufacturing operations or those of our suppliers or customers. In addition, climate change may pose physical risks to our manufacturing facilities or our suppliers’ facilities, including increased extreme weather events that could result in supply delays or disruptions. Other events, including political or public health crises, such as an outbreak of contagious diseases, may also affect our production capabilities or that of our suppliers, including as a result of quarantines, closures of production facilities, lack of supplies, or delays caused by restrictions on travel or shipping. Events of the types noted above have occurred from time to time and, because these risks are a characteristic of our business, they may occur in the future. As a result, in addition to disruptions to operations, our insurance premiums may increase or we may not be able to fully recover any sustained losses through insurance.

We from time to time borrow under our existing credit facility or use proceeds from sales of our securities to fund portions of our operations, including working capital investments and financing of our acquisition strategies. In the past, market disruptions experienced in the United States and abroad have materially impacted liquidity in the credit and debt markets, making financing terms for borrowers less attractive and, in certain cases, have resulted in the unavailability of certain types of financing. Uncertainty in the financial markets may negatively impact our ability to access additional financing or to refinance our existing 29 Table of Contents debt arrangements on favorable terms or at all, which could negatively affect our ability to fund current and future expansion as well as future acquisitions and development. These disruptions may include turmoil in the financial services industry, volatility in the markets where our outstanding securities trade, and changes in general economic conditions in the areas where we do business. If we are unable to access funds at competitive rates, or if our short-term or long-term borrowing costs increase, our ability to finance our operations, meet our short-term obligations, and implement our operating strategies could be adversely affected.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
