你是 stock-analyst v20 DD 的證據採集子 agent。標的：TER。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Teradyne product substitute technology threat 2026
  - Semiconductor Equipment & Materials alternative technology disruption 2026 2027
  - TER Teradyne technology obsolescence risk
  - Semiconductor Equipment & Materials next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm｜as_of：2026-02-19
<<<
Capital equipment providers in the electronics, semiconductor industries and robotics, such as Teradyne, have, in the past, been negatively impacted by both sudden slowdowns in the global economies and recurring cyclicality within those industries. These cycles, which can be driven by broad changes to Semiconductor buying patterns, or to specific markets within the Semiconductor industry, have resulted in periods of over-supply; a trend we believe will continue to occur. Our business and results of operations depend, in significant part, upon capital expenditures of manufacturers of semiconductors, electronics, and other industrial products, which in turn depend upon the current and anticipated market demand for those products. Disruption or deterioration in global or industry-specific economic conditions may reduce customer purchases of our products, thereby reducing our revenues and earnings. In addition, such adverse changes in economic conditions, and resulting slowdowns in the market for our products, may, among other things, result in increased price competition for our products, increased risk of excess and obsolete inventories, increased risk in the collectability of our accounts receivable from our customers, potential reserves for credit losses and write-offs of accounts receivable, increased risk of restructuring charges, and higher operating costs as a percentage of revenues, which, in each case and together, adversely affect our operating results.…

We believe that our technological position depends primarily on the technical competence and creative ability of our engineers. In a rapidly evolving market, such as ours, the development or acquisition of new technologies, commercialization of those technologies into products and market acceptance and customer demand for those products are critical to our success. In the electronics, semiconductor, and robotics industries, products are often replaced by more technologically advanced substitutes and, as demand for older technology falls, the price at which such products can be sold drops. If we cannot advance new technologies to meet our customers’ demands, our revenues and financial condition may be adversely impacted. Successful product development or acquisition, introduction and acceptance depend upon a number of factors, including: •new product selection and ability to predict market requirements and design new products that address those requirements; •ability to meet customer requirements including with respect to safety and cybersecurity; •development of competitive products by competitors; •timely and efficient completion of product design; •timely and efficient implementation of manufacturing and manufacturing processes; •timely remediation of product performance issues, if any, identified during testing; •assembly processes and product performance at customer locations; •differentiation of our products from our competitors' products; •management of customer expectations concerning product capabilities and product life cycles; •transition of customers to new product platforms; •compliance with product…

A significant portion of our consolidated revenues is derived from customers outside the United States. Our international sales and operations are subject to significant risks and difficulties, including: •unexpected changes in legal and regulatory requirements affecting international markets; •cost increases due to inflation; •expense and complexity of complying with U.S. and foreign import and export regulations; •changes in tariffs and foreign currency exchange rates; •social, political and economic instability, acts of terrorism and international conflicts; •restrictions on the transfer of funds; •disruption caused by health pandemics; •difficulties in protecting intellectual property; •difficulties in accounts receivable collection; •cultural differences in the conduct of business; •difficulties in staffing and managing international operations; •compliance with anti-corruption laws, cybersecurity, data privacy regulations, customs and trade regulations; •compliance with international tax laws and regulations.

In addition, an increasing portion of our products and the products we purchase from our suppliers are sourced or manufactured in foreign locations, including Malaysia and Denmark, and a large portion of the devices our products test are fabricated and tested by foundries and subcontractors in Taiwan, China, Korea and other parts of Asia. As a result, we are subject to a number of economic and other risks, particularly during times of political, health or financial instability in these regions. Disruption of manufacturing or supply sources in these international locations could materially adversely impact our ability to fill customer orders and potentially result in lost business.

Risks Related to Operations Our operating results are likely to fluctuate significantly. Our operating results are affected by a wide variety of factors that could materially adversely affect revenues or profitability. The following factors could impact future operations: •macroeconomic conditions, a worldwide economic slowdown or disruption in the global financial or industrial markets; •legal, tax, accounting or regulatory changes (including changes in import/export regulations and tariffs, such as regulations imposed by the U.S. government restricting exports to China) or changes in the interpretation or enforcement of existing requirements; •cost increases from inflation on materials, employee wages, third party labor, and contract manufacturing; •competitive pressures on selling prices; •foreign currency exchange rate fluctuations; •our ability to introduce, and the market acceptance of, new products; •changes in product revenues mix resulting from changes in customer demand; •customer demand considerations, including the size and timing of customer orders, customers’ decisions to accelerate, decelerate or delay shipments, customers’ decisions on how to manage their inventory, customers’ rate of replacement of our consumable products or their decisions to delay expansion projects; •the level of orders received which can be shipped in a quarter because of the tendency of customers to wait until late in a quarter to commit to purchase due to capital expenditure approvals and constraints occurring at the end of a quarter, or…

If we experience a problem with our supply of products from Flex, Plexus, SAM Meerkat, or our other contract manufacturers, it may take us significant time to either manufacture the product or find an alternate contract manufacturer, which could result in substantial expense and disruption to our business. We have, however, significantly invested in our internal manufacturing for FLEX products in our Cebu site.

Our business is international in nature, with our sales, service and administrative personnel and our customers and suppliers located in numerous countries throughout the world. Our operations, and those of our customers and suppliers, are subject to disruption for a variety of reasons, including work stoppages, acts of war and geopolitical conflict, terrorism, health epidemics, fires, earthquakes, hurricanes, typhoons, volcanic eruptions, energy shortages, telecommunication failures, tsunamis, flooding or other natural disasters, including as a result of global climate change. Any disruptions from these events could require substantial expenditures and recovery time to fully resume operations and could also have a material adverse effect on our operations and financial results to the extent that losses are uninsured or exceed insurance recoveries, and to the extent that such disruptions adversely impact our relationships with our customers. Additionally, any such disruption could materially increase our costs and expenses as well as cause delays in, among other things, shipments of products to our customers, our ability to perform services requested by our customers, or the installation and acceptance of our products at customer sites. Any of these conditions could have a material adverse effect on our business, financial condition or results of operations.

We rely on various information technology networks and systems to process, transmit and store electronic information, including proprietary and confidential data, and to carry out and support a variety of business activities, including manufacturing, research and development, supply chain management, sales and accounting. We have experienced several attempted cyber-attacks of our network. None of the attempted attacks have caused a disruption to our operations or had a material adverse effect on our business or financial results. As a result of the attempts, we have taken further preventive security measures to protect our systems. Despite the preventive security measures we have implemented, we may continue to be vulnerable to attempts by third parties to gain 17 Table of Contents unauthorized access to our networks or sabotage our systems. These attempts, which might be related to criminal hackers, industrial espionage or state-sponsored intrusions, include trying to covertly introduce malware to our computers, networks and systems and impersonating authorized users. Additionally, evolving geopolitical tensions or conflicts have created a heightened risk of cybersecurity attacks. In addition, third party suppliers and service providers that we rely on to manage our networks and systems and who process and store our proprietary and confidential data, including the data of our customers and suppliers, may also be subject to similar attacks.…

We may be subject to security breaches of certain of our products caused by viruses, illegal break-ins or hacking, sabotage, or acts of vandalism by third parties or our employees or contractors. A breach of our product security systems could have a material adverse effect on our business or financial results, disrupt our business, result in the disclosure or misuse of proprietary or confidential information, damage our reputation, cause losses, and increase our costs. We expect to continue to devote significant resources to the security of our products.

Our business operations and supply chain are global and may be disrupted by the implementation of tariffs. In recent years, the United States has imposed significant tariffs on goods from some of our trading partners, and more significant tariffs continue to be threatened in light of rapidly evolving geopolitical tensions.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
