你是 stock-analyst v20 DD 的證據採集子 agent。標的：HUBB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Hubbell product substitute technology threat 2026
  - Electrical Equipment & Parts alternative technology disruption 2026 2027
  - HUBB Hubbell technology obsolescence risk
  - Electrical Equipment & Parts next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm｜as_of：2026-02-12
<<<
Raw Materials Raw materials used in the manufacture of Hubbell products primarily include steel, aluminum, brass, copper, bronze, zinc, nickel, plastics, elastomers and petrochemicals. Hubbell also purchases certain electrical and electronic components, including solenoids, printed circuit boards, integrated circuit chips and cord sets, from a number of suppliers. Hubbell is not materially dependent upon any one supplier for raw materials used in the manufacture of its products and equipment however the cost and supply of these materials may be affected by disruptions in availability of raw materials, components or sourced finished goods. See also Item 7A. Quantitative and Qualitative Disclosures about Market Risk.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/48898/000162828026007500/hubb-20251231.htm｜as_of：2026-02-12
<<<
We manufacture and source products and materials from various countries throughout the world. A disruption in the availability, price or quality of these products or materials could adversely affect our operating results.

As of December 31, 2025, the net carrying value of our goodwill and other intangible assets totaled approximately $4,455 million. As required by generally accepted accounting principles, we periodically assess these assets to determine if they are impaired. Impairment of intangible assets may be triggered by developments both within and outside the Company’s control. Deteriorating economic conditions, technological changes, disruptions to our business, inability to effectively integrate acquired businesses, unexpected significant changes or planned changes in use of the assets, intensified competition, divestitures, market capitalization declines and other factors may impair our goodwill and other intangible assets. Any charges relating to such impairments could adversely affect our results of operations in the periods an impairment is recognized.

Achieving our long-term profitability goals depends significantly on our ability to control or reduce our operating costs. Because many of our costs are affected by factors completely, or substantially outside our control, we generally must seek to control or reduce costs through productivity initiatives. If we are not able to identify and implement initiatives that control or reduce costs and increase operating efficiency, or if the cost savings initiatives we have implemented to date do not generate expected cost savings, our financial results could be adversely affected. Our efforts to control or reduce costs may include restructuring activities involving workforce reductions, facility consolidations and other cost reduction initiatives. If we do not successfully manage our current restructuring activities, or any other restructuring activities that we may undertake in the future, expected efficiencies and benefits may be delayed or not realized, and our operations and business could be disrupted, which could have an adverse effect on our results of operations, financial condition and cash flows.

We are subject to risks surrounding our information technology systems and industrial controls systems failures, and the use of emerging technologies, including artificial intelligence, as well as, network disruptions, breaches in data security and compliance with data privacy laws or regulations.

We are highly dependent on various software and information technology systems to record and process operational, human resources and financial transactions. The proper functioning of Hubbell’s information technology systems is critical to the successful operation of our business. Our information technology systems are susceptible to cyber threats, malware, phishing attacks, break-ins and similar events, breaches of physical security or tampering and manipulation of these systems by employees or unauthorized third parties. Information security risks also exist with respect to the use of portable electronic devices, such as smartphones and laptops, which are particularly vulnerable to loss and theft. Hubbell may also be subject to disruptions of any of our systems and our vendor’s systems arising from events that are wholly or partially beyond our control, such as natural disasters, acts of terrorism, cyber-attacks, computer viruses, and electrical/telecommunications outages or failures. All of these risks are also applicable where Hubbell relies on outside vendors to provide services, which may operate in an online, or “cloud,” environment. A failure of our information technology systems could adversely affect our ability to process orders, maintain proper levels of inventory, collect accounts receivable and pay expenses; all of which could have an adverse effect on our results of operations, financial condition and cash flows.…

Hubbell is also subject to an increasing number of evolving data privacy and security laws and regulations that impose requirements on the Company and our technology prior to certain use or transfer, storing, processing, disclosure, and protection of data and prior to sale or use of certain technologies. Failure to comply with such laws and regulations could result in the imposition of fines, penalties and other costs. For example, the European Union’s General Data Protection Regulation, the European Union’s pending ePrivacy Regulation and the implementation of the ePrivacy Directive by the various European Union member states, and California’s Consumer Privacy Act of 2018 and Connected Device Privacy Act of 2018, as well as data privacy statutes implemented by other states, could all disrupt our ability to sell products and solutions or use and transfer data because such activities may not be in compliance with applicable law in certain jurisdictions.

We utilize materials (such as steel, aluminum and copper), components and finished goods that are sourced from or manufactured in foreign countries, including Canada, China, Mexico and countries in Europe. Import tariffs and potential additional import tariffs have resulted or may result in increased prices for these imported goods and materials and, in some cases, may result or have resulted in price increases for domestically sourced goods and materials. Changes in U.S. trade policy have resulted in trade policy responses from other countries (and may result in additional ones in the future), including the adoption of reciprocal trade policies that could make it more difficult or costly for us to export our products or import goods and materials from those countries. These measures could also result in increased costs for goods imported into the U.S. or may lead to disruptions in the supply of goods and materials that could cause us to adjust our worldwide supply chain. This could require us to increase prices to our customers which may reduce demand, or, if we are unable to increase prices, result in lowering our margin on products sold.

We must comply with various laws and regulations relating to the import and export of products, services and technology from the U.S. and other countries having jurisdiction over our operations, which may affect our transactions with certain customers, business partners and other persons. In certain circumstances, export control and economic sanctions regulations may prohibit the export of certain products, services and technologies and in other circumstances, we may be required to obtain an export license before exporting a controlled item. The length of time required by the licensing processes can vary, potentially delaying the shipment of products or performance of services and the recognition of the corresponding revenue. In addition, failure to comply with any of these regulations could result in civil and criminal, monetary and non-monetary penalties, disruptions to our business, limitations on our ability to import and export products and services and damage to our reputation. Moreover, any changes in export control or sanctions regulations may further restrict the export of our products or services, and the possibility of such changes requires constant monitoring to ensure we remain compliant. Any restrictions on the export of our products or product lines could have a material adverse effect on our competitive position, results of operations, cash flows or financial condition.

We face the potential harms of natural disasters, terrorism, acts of war, international conflicts or other disruptions to our operations.

Natural disasters, the economic uncertainty resulting from the spread of global pandemics, acts or threats of war or terrorism, international conflicts, and the actions taken by the United States and other governments in response to such events have in the past, and could in the future cause damage to or disrupt our business operations, our suppliers or our customers, and could create political or economic instability, any of which could have an adverse effect on our business. For example, increases in energy demand and supply disruptions caused by the conflict in Ukraine have resulted in significantly higher energy prices, particularly in Europe. Additionally, the conflict in the Middle East has added to the volatility in energy costs. Persistent high energy prices and the potential for further supply disruptions, may have an adverse impact on our business. Although it is not possible to predict such events or their consequences, these events could decrease demand for our products, make it difficult or impossible for us to deliver products, or disrupt our supply chain.

Global economic uncertainty could adversely affect us. During periods of prolonged slow growth, or a downturn in conditions in the worldwide or domestic economies, we could experience reduced orders, payment delays, supply chain disruptions or other factors caused by economic challenges faced by our customers, prospective customers and suppliers. Depending upon their severity and duration, these conditions could have an adverse impact on our results of operations, financial condition and cash flows.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
