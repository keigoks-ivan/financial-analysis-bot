你是 stock-analyst v20 DD 的證據採集子 agent。標的：TEL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - TE Connectivity product substitute technology threat 2026
  - Electronic Components / Connectors alternative technology disruption 2026 2027
  - TEL TE Connectivity technology obsolescence risk
  - Electronic Components / Connectors next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1385157/000110465925109150/tel-20250926x10k.htm｜as_of：2025-11-10
<<<
Raw Materials We use a wide variety of raw materials in the manufacture of our products. The principal raw materials that we use include plastic resins for molding; precious metals such as gold, silver, and palladium for plating; and other metals such as copper, aluminum, brass, and steel for manufacturing cable, contacts, and other parts that are used for cable and component bodies and inserts. Many of these raw materials are produced in a limited number of countries around the world or are only available from a limited number of suppliers. The prices of these materials are driven by global supply and demand. In recent years, raw material prices and availability have been affected by worldwide economic conditions, including supply chain disruptions, trade wars, and inflationary cost pressures.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1385157/000110465925109150/tel-20250926x10k.htm｜as_of：2025-11-10
<<<
Our business and operating results have been and will continue to be affected by economic conditions regionally or globally, including new or increased tariffs and other barriers to trade, including escalation of trade and tariff tensions between the United States (“U.S.”), China, the EU, and other countries, changes to fiscal and monetary policy, inflation, slower growth or recession, higher interest rates, labor disruptions, the cost and availability of consumer and business credit, end demand from consumer and industrial markets, significant bank failures, government shutdowns, and concerns as to sovereign debt levels including credit rating downgrades and defaults on sovereign debt. Any of these economic factors could cause our customers to experience deterioration of their businesses, cash flow, financial condition, and ability to obtain financing. As a result, existing or potential customers may delay or cancel plans to purchase our products and may not be able to fulfill their obligations to us in a timely fashion or in full. Further, our vendors may experience similar problems, which may impact their ability to fulfill our orders or meet agreed service and quality levels. If regional or global economic conditions deteriorate, our results of operations, financial position, and cash flows could be materially adversely affected.…

Our operations and those of our suppliers and customers, and the supply chains that support their operations, have been and may be in the future vulnerable to interruption by natural disasters such as hurricanes, earthquakes, tsunamis, typhoons, tornados, or floods, which may be exacerbated by the effects of climate change; other disasters such as fires, explosions, acts of terrorism, or war, including the continuing military conflicts in certain parts of the world; disease or other adverse health developments; or failures of management information or other systems due to internal or external causes. These events could cause some of our operations to suffer from supply chain disruptions and potential delays in fulfilling customer orders or order cancellations altogether, lost business and sales, changing costs or availability of insurance, and/or property damage or harm to our people, each and all of which could have an adverse effect on our business operations, financial condition, and results of operations. In addition, such interruptions could result in a widespread crisis that could adversely affect the economies and financial markets of many countries, resulting in an economic downturn that could affect demand for our end customers’ products.…

Disruption in credit markets and volatility in equity markets may affect our ability to access sufficient funding.

The global equity markets have been volatile and at times credit markets have been disrupted, which has reduced the availability of investment capital and credit. Downgrades of sovereign debt credit ratings have similarly affected the availability and cost of capital. As a result, we may be unable to access adequate funding to operate and grow our business. Our inability to access adequate funding or to generate sufficient cash from operations may require us to reconsider certain projects and capital expenditures. The extent of any impact will depend on several factors, including our operating cash flows, the duration of tight credit conditions and volatile equity markets, our credit ratings and credit capacity, the cost of financing, and other general economic and business conditions.

Substantially all markets in which we operate are impacted by technological change or change in consumer tastes and preferences, which are rapid in certain end markets. Our operating results depend substantially upon our ability to continually design, develop, introduce, and sell new and innovative products; to modify existing products; and to customize products to meet customer requirements driven by such change. There are numerous risks inherent in these processes, including the risk that we will be unable to anticipate the direction of technological change or that we will be unable to develop and market profitable new products and applications in time to satisfy customer demands.

The pace of technological change continues to accelerate and our ability to react effectively to such change may present significant competitive risks.

The pace of technological change is increasing at an exponential rate. The continued creation, development, and advancement of new technologies such as AI, blockchain, quantum computing, data analytics, 3-D printing, robotics, sensor technology, data storage, neural networks, and augmented reality, as well as other technologies in the future that are not foreseeable today, continue to transform our processes, products, and services.

In order to remain competitive, we will need to stay abreast of such technologies, require our employees to continue to learn and adapt to new technologies, be able to integrate them into our current and future business models, products, services, and processes, and also guard against existing and new competitors disrupting their business using such technologies. Our strategy, value creation model, operating model, and innovation ecosystem have important technological elements and certain of our products and offerings are based on technological advances, including AI, machine learning, advanced analytics, and the Internet of Things. Meeting evolving industry requirements, including the increasing use of AI and machine learning technologies (including the need to run complex AI-based applications on devices), and introducing new products to the market in a timely manner and at prices that are acceptable to our customers are important factors in determining our competitiveness and success. Further, increasing use of AI may expose us to social and ethical issues, which may result in reputational harm and liability. In addition, we will need to compete for talent in a competitive market that is familiar with such technologies including upskilling our workforce.…

We are a large buyer of resins, chemicals, additives, and metals, including copper, gold, silver, palladium, aluminum, brass, steel, and zinc. Many of these raw materials are produced in a limited number of countries around the world or are only available from a limited number of suppliers. The prices of many of these raw materials continue to fluctuate, and in many cases increase, and fluctuations may persist in the future. In addition, feedstock for resins and resins themselves, as well as certain other commodities, are increasingly subject to varied and unrelated force majeure events worldwide further impacting price and availability. In recent years, raw material prices and availability have been affected by worldwide economic conditions, including supply chain disruptions, inflationary cost pressures, and tariff and trade policies. If we have difficulty obtaining raw materials, the quality of available raw materials deteriorates, or there are significant price increases for these raw materials, it could have a substantial impact on the price we pay for raw materials. To the extent we cannot compensate for cost increases through productivity improvements or price increases to our customers, our margins may decline, materially affecting our results of operations, financial position, and cash flows. In addition, we use financial instruments to hedge the volatility of certain commodities prices.…

Cybersecurity incidents and other disruptions affecting our information technology infrastructure or violations of data privacy laws have and could interfere with our operations, compromise confidential information, and expose us to liability which could materially adversely impact our business and reputation.

Our information technology networks and infrastructure, and the technology networks and infrastructure of our third-party suppliers and business partners, are vulnerable to damage, disruptions or shutdowns due to attack by malicious actors with significant financial and technological resources, breaches, employee error or malfeasance, power outages, malware (such as computer viruses and ransomware), social engineering (i.e., phishing attacks), theft of system credentials, other increasingly sophisticated attacks, telecommunication or utility failures, systems failures, natural disasters, or other catastrophic events, which may require us to notify regulators, customers, or employees, and enlist identity theft protection in the event of a privacy breach. We continue to monitor and develop our systems to protect the integrity and functionality of our information technology infrastructure and access to and the security of our intellectual property and our employees’, customers’, and suppliers’ data. Cybersecurity breaches and other disruptions to our information technology infrastructure or the information technology infrastructure of our third-party suppliers and business partners, or violations of applicable laws, could result in legal claims or proceedings, liability or penalties, disruption in operations, and damage to our reputation, which could materially adversely affect our business.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TEL_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
