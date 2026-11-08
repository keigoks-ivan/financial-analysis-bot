你是 stock-analyst v20 DD 的證據採集子 agent。標的：RL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Ralph Lauren product substitute technology threat 2026
  - Apparel Manufacturing alternative technology disruption 2026 2027
  - RL Ralph Lauren technology obsolescence risk
  - Apparel Manufacturing next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-21）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm｜as_of：2026-05-21
<<<
•attract consumer traffic to stores, shop-within-shops, and digital commerce sites; •source sustainable and traceable raw materials at cost-effective prices; •anticipate and maintain proper inventory levels; •ensure product availability and optimize supply chain and distribution efficiencies; •maintain and grow market share; •recruit and retain talent to operate our retail stores, distribution centers, and various corporate functions; •protect our intellectual property; and •withstand prolonged periods of adverse economic conditions or business disruptions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-21）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm｜as_of：2026-05-21
<<<
Although we believe that our existing cash and investments, cash provided by operations, and available borrowing capacity under our credit facilities and commercial paper borrowing program will provide us with sufficient liquidity, the impact of adverse economic conditions (such as ongoing inflationary pressures and high interest rates) on our major customers, suppliers, vendors, and lenders and their ability to access global capital markets cannot be predicted. The inability of third parties to manufacture and/or ship our products due to insufficient liquidity or otherwise could impair our ability to meet the delivery date requirements of our customers. A disruption in the ability of our significant customers to access liquidity could cause serious disruptions or an overall deterioration of their businesses which could lead to a significant reduction in their future orders of our products and the inability or failure on their part to meet their payment obligations to us, any of which could have a material adverse effect on our business.

Widespread public health emergencies and infectious disease outbreaks (including pandemics, epidemics, resurgences of endemic diseases, and the emergence of new or more transmissible variants or pathogens), whether occurring domestically or internationally, have had, and could again in the future, have a material adverse effect on our business, results of operations, and financial condition. Such events may result in, among other things, government mandates or recommendations (including quarantines, travel restrictions, or other public safety measures), changes in consumer behavior and demand, and operational disruptions. Potential impacts to our business include, but are not limited to: (i) global supply chain disruptions due to factory closures, labor shortages, scarcity of raw materials, shipping and sourcing limitations, and any related cost increases; (ii)

We do not own or operate any manufacturing facilities and depend exclusively on independent third parties for the manufacture of our products. Our products are manufactured to our specifications through arrangements with approximately 300 foreign manufacturers in various countries. In Fiscal 2026, the vast majority of our products (by dollar value) were produced outside of the U.S., primarily in Asia, Europe, and Latin America, with approximately 21% of our products sourced from Vietnam, 16% from Cambodia, and 11% from India. Risks inherent in importing our products include (i) the imposition of additional tariffs, duties, taxes, and other charges on imports or exports, such as those announced by the U.S. as discussed below; (ii) changes in diplomatic and trade relationships, including sanctions, trade restrictions, and other retaliatory measures; (iii) the imposition of additional regulations, quotas, trade sanctions, or safeguards or sourcing and reporting requirements that could increase compliance costs or lead to the detention, exclusion, or seizure of goods and imposition of monetary penalties and fines; (iv) adverse changes in local economic conditions, such as prolonged periods of economic weakness, high inflation and/or interest rates, or other factors described herein; (v) changes in social or political conditions, including those resulting from military conflicts, terrorist acts, or other hostilities, that could result in the disruption of trade from the countries in which…

In addition, we rely on a number of owned, leased, and independently-operated distribution facilities around the world to warehouse and ship products to our customers and perform other related logistic services. Our ability to meet the needs of our customers depends on the proper operation of these distribution centers. Our distribution centers generally utilize computer-controlled and automated equipment, which are subject to various risks, including software viruses, security breaches, power interruptions, or other system failures. If any of our distribution centers were to close or become inoperable or inaccessible for any reason, including, but not limited to, natural disasters, severe weather, labor shortages, fires, and system failures, pandemic diseases, or if we fail to successfully consolidate existing facilities or transition to new facilities, we could experience a substantial loss of inventory, disruption of deliveries to our customers and our stores, increased costs, and longer lead times associated with the distribution of products during the period that would be required to reopen or replace the facility. Any such disruptions could have a material adverse effect on our business.

We rely on our operating cash flows to repay our outstanding borrowings, as well as to fund any working capital needs, capital expenditures, dividend payments, share repurchases, and other general corporate purposes. Prolonged periods of adverse economic conditions or business disruptions in any of our key regions, or a combination thereof, could impede our ability to pay our obligations as they become due or return value to our shareholders, as well as delay previously planned expenditures related to our operations. Credit rating agencies also periodically review our capital structure and our ability to generate earnings. A prolonged period of deteriorated financial performance or our inability to comply with debt covenants (as discussed below) could make future financing more difficult to secure and/or expensive. Further, factors beyond our control, such as adverse economic conditions, could disrupt capital markets and limit the availability or willingness of financial institutions to extend capital to us in the future.

Our operations, including retail, distribution, warehousing, and corporate operations, are susceptible to man-made or natural disasters, including severe weather, geological events, pandemic diseases, and other catastrophic events, such as terrorist attacks and military conflicts, any of which could disrupt our operations. In addition, the operations of our customers and suppliers could experience similar disruptions. The occurrence of natural disasters or other catastrophic events may result in sudden disruptions in the business operations of the local and regional economies affected, as well as the global economy as a whole, including, but not limited to, shortages and/or rising costs of raw materials or energy, public health issues, system failures, and reduced retail traffic. The occurrence of such events could also adversely affect financial markets and the availability of capital. In addition, our business can be affected by unseasonable weather conditions, such as extended periods of unseasonably warm temperatures in the winter or unseasonably cold temperatures in the summer. There is growing concern that climate change may increase both the frequency and severity of extreme weather conditions and natural disasters. Any of these events could result in decreased demand for our products and disruptions in our sales channels and manufacturing and distribution networks, which could have a material adverse effect on our business.

34 We are continually improving and upgrading our computer systems, software, and related processes. As described in Item 1 — "Business — Recent Developments," our Next Generation Transformation project, which began during Fiscal 2024, entails upgrading and enhancing our technology infrastructure, including AI and machine learning capabilities, to better enable us to implement process changes to improve productivity and operational efficiencies on a global scale. A system project of this scope requires a significant investment in human and financial resources and involves many risks and uncertainties, including failure to operate as designed, failure to properly integrate with other systems, potential loss of data or information, cost overruns, and implementation delays. Any disruptions, delays, or deficiencies in the design, implementation, or transition of such systems could also result in disruptions to our business operations, including the sourcing, sale, and shipment of our product, delays in the collection of cash from our customers, diversion of management attention, and/or adversely affect our ability to accurately report our financial results in a timely manner or otherwise maintain compliance with internal controls. There is also no guarantee that we will realize the anticipated global synergies and benefits related to this project. Any material disruptions in our information technology systems could have a material adverse effect on our business.

Our business is susceptible to risks associated with climate change, including potential disruptions to our retail stores, distribution centers, and corporate facilities or those facilities of our wholesale customers, licensees, logistics partners, and suppliers. Increased frequency and/or severity of extreme weather events due to climate change could adversely impact global supply chains, including the availability, quality, and cost of raw materials (such as cotton, a key raw material used in the production of our products that is highly susceptible to severe weather conditions), the ability of our manufacturers to fulfill our orders timely and to our specifications, and shipping disruptions and/or higher freight costs. An increase in extreme weather conditions could also result in more frequent damage and/or closures of our stores, distribution centers, and corporate facilities, adversely impact retail traffic, consumer's disposable income levels or spending habits on discretionary items, or otherwise disrupt business operations in the communities in which we operate, any of which could result in lost sales or higher costs.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
