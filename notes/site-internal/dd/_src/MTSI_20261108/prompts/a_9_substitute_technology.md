你是 stock-analyst v20 DD 的證據採集子 agent。標的：MTSI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - MACOM Technology Solutions Holdings product substitute technology threat 2026
  - 半導體 / 光通訊 / RF alternative technology disruption 2026 2027
  - MTSI MACOM Technology Solutions Holdings technology obsolescence risk
  - 半導體 / 光通訊 / RF next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm｜as_of：2025-11-14
<<<
We believe that we compete favorably with respect to these factors. We compete primarily with both our customers’ internal design resources and other suppliers of high-performance analog semiconductor solutions for use in wireless and wireline RF, microwave, millimeter wave and photonic applications, some of whom have greater financial resources and scale than us. We expect competition in our markets to change as new competitors enter these markets, existing competitors merge or form alliances and new technologies emerge. We believe that in the future there will be increased competition from companies utilizing alternative technologies, including high-volume manufacturers using low-cost silicon process technology. Some of our competitors are also our customers, and in certain product categories we compete with semiconductor manufacturers from which we also obtain foundry services.

The principal substrate materials used in the production of our IC products are high purity source materials such as gallium, aluminum, arsenic, nitrite, carbon and silicon. We purchase a wide variety of semiconductors, wafers, packages, metals, printed circuit boards, electromechanical components and other materials from hundreds of suppliers worldwide for use in our operations. These supply relationships are generally conducted on a purchase order basis. The use of external suppliers involves a number of risks, including the possibility of material disruptions in the supply of key raw materials and components, and the lack of control over delivery schedules, capacity, quality and costs.

While we attempt to maintain alternative sources for our principal raw materials to reduce the risk of supply interruptions or price increases, some of the raw materials and components are not readily available from alternate suppliers due to their unique nature, design or the length of time necessary for re-design or qualification. We may utilize single sources of supply for various materials based on availability, performance, efficiency or cost considerations. For example, wafers procured from merchant foundries for a particular process technology are generally sourced through a single foundry on which we rely for all of our wafers in that process. Our reliance on external suppliers puts us at risk of supply chain disruption if a supplier does not have sufficient raw material inventory to meet our manufacturing needs, goes out of business, experiences capacity constraints or temporary facility closures, changes or discontinues the process in which components or wafers are manufactured or declines to continue supplying us for competitive or other reasons, as discussed in more detail in “Item 1A - Risk Factors” herein. Where practical, we attempt to mitigate these risks by qualifying multiple sources of supply, redesigning products for alternative components and purchasing incremental inventory of raw materials and components in order to protect us against supply disruptions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm｜as_of：2025-11-14
<<<
Our business and operations could suffer in the event of a security breach, cybersecurity incident or disruption of our information technology systems.

We rely on our information technology (“IT”) systems and services for the effective operation of our business and for the secure maintenance and storage of confidential data relating to our business. In the ordinary course of our business, we and our third-party service providers collect, maintain and transmit sensitive data on our networks and systems, including Company and third-party intellectual property and proprietary or confidential business information (such as research data and personal information). These systems and services are both internally managed and outsourced, and, in many cases, we rely upon third-party service providers. Any failure of these internal or third-party systems and services to operate effectively could disrupt our operations and have a material adverse effect on our business, financial condition and/or results of operations. Our operations are heavily dependent on the functioning of our IT infrastructure to carry out our business processes and our ability to protect our IT infrastructure against damage from business continuity events that could have a significant disruptive effect.…

13 Any compromise of our information or operational technology systems could result in unauthorized publication, exfiltration or misappropriation of our confidential business or proprietary information or intellectual property; result in the unauthorized release of customer, supplier or employee data; lead to violations of privacy or other laws; extortion; allow competitors to profit from our intellectual property or trade secrets; delay or disrupt our operations; expose us to a risk of investigations and litigation; cause us to incur direct losses if attackers access our bank or investment accounts; undermine investor or market confidence, or damage our reputation. The direct and indirect cost and operational consequences of implementing data protection measures either as a response to specific breaches or as a result of evolving risks could be significant. In addition, our inability to use or access our information or operational systems at critical points in time could adversely affect the timely and efficient operation of our business. Any delayed sales, significant costs or lost customers resulting from a technology failure could adversely affect our business, operations and financial results.

15 In addition, if terrorist activity, armed conflict, civil, economic or military unrest, natural disasters, global pandemics, embargoes or other economic sanctions, enforcement actions against governments, governmental entities or private entities or political instability occurs in the U.S. or other locations, such events may disrupt our manufacturing, assembly, logistics, security and communications, labor issues and transportation and other disruptions, and could also result in reduced demand for our products. We have in the past and, may again in the future, experience difficulties relating to employees traveling in and out of countries facing civil unrest or political instability and with obtaining travel visas for our employees. There can be no assurance that we can mitigate all identified risks with reasonable effort. The occurrence of any of these events, including the conflicts in Ukraine and Israel, could have a material adverse effect on our operating results.

We believe future competition could also come from companies developing new alternative technologies, component suppliers based in countries with lower production costs and IC manufacturers achieving higher levels of integration that exceed the functionality offered by our products. Our customers and suppliers could also develop products that compete with or replace our products. Increased competition has in the past and could in the future lead to lower prices for our products, reduced demand for our products and a corresponding reduction in our ability to recover development, engineering and manufacturing costs.

We purchase numerous raw materials, such as ceramic packages, precious metals, semiconductor wafers and ICs, from a limited number of external suppliers. We also currently use several external manufacturing suppliers for assembly and testing of our products, and in some cases for fully outsourced turnkey manufacturing of our products. We expect to increase our use of outsourced manufacturing in the future as a strategy. Any substantial disruption in the contract manufacturing services that we utilize as a result of a natural disaster, climate change, water shortages, political unrest, military conflicts, geopolitical turmoil, trade tensions, government orders, labor shortages, medical epidemics, economic instability, equipment failure or other cause, could materially harm our business, customer relationships and results of operations. Further, the use of external suppliers involves a number of risks, including the possibility of material disruptions in the supply of key components, the lack of control over delivery schedules, capacity constraints, manufacturing yields, quality and fabrication costs and misappropriation of our intellectual property. If these vendors’ processes vary in reliability or quality, they could negatively affect our products and, therefore, our customer relations and results of operations. We generally purchase raw materials on a purchase order basis, and we do not have significant long-term supply commitments from our vendors.…

We sell products in markets that are characterized by rapid technological changes, evolving industry standards, frequent new product introductions and increasing levels of integration. Our ability to keep pace with these markets at times depends on our ability to obtain technology from third parties on commercially reasonable terms to allow our products to remain competitive. If licenses to such technology are not available on commercially reasonable terms and conditions or at all and we cannot otherwise acquire or integrate such technology, our products or our customers’ products could become unmarketable or obsolete, we could lose market share and our revenue and results of operations could materially decline. In addition, disputes with third-party licensors over required payments, scope of licensed rights and compliance with contractual terms are common in our industry and we have in the past and may in the future be subjected to disputes over the terms of such licenses which could result in substantial unanticipated costs or delays in developing substitute technology to deliver competitive products, damaged customer and vendor relationships, indemnification liabilities and declining revenues and profitability. Such events could have an adverse effect on our financial condition and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
