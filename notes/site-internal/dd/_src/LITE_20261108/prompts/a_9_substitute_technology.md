你是 stock-analyst v20 DD 的證據採集子 agent。標的：LITE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Lumentum Holdings product substitute technology threat 2026
  - Communication Equipment alternative technology disruption 2026 2027
  - LITE Lumentum Holdings technology obsolescence risk
  - Communication Equipment next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm｜as_of：2026-08-17
<<<
Specific concerns we periodically encounter with our sole suppliers or limited number of suppliers include receipt of defective parts or contaminated materials, stoppages or delays of supply, insufficient resources to supply our requirements, substitution of more expensive or less reliable materials, increases in the price of supplies, and an inability to obtain reduced pricing from our suppliers in response to competitive pressures. Furthermore, supply chain disruptions and labor market constraints have created heightened risk that sole suppliers or limited number of suppliers may be unable to meet their obligations to us. Difficulties in obtaining the materials, or services used in the conduct of our business or additional fees or higher prices to do so, have adversely affected our revenue and results of operations, and further challenges or decisions to seek alternate suppliers to secure supply in order to meet demand would increase our costs and reduce our profitability.

The markets in which we operate are dynamic and complex, and our success depends on our ability to deliver both our current product offerings and new products and technologies on time and at acceptable prices to our customers. The markets for our products are characterized by rapid technological change, frequent new product introductions and enhancements, substantial capital investment, changes in customer requirements, continued price pressures and a constantly evolving industry. Historically, these pricing pressures have led to a continued decline of average selling prices in certain areas of our business, and we expect that these historical trends will continue. The development of new, technologically advanced products is a complex and uncertain process requiring high levels of innovation and the accurate prediction of technology and market trends. The introduction of new products also often requires significant investment to ramp up production capacity, the benefit of which may not be realized if we are not successful in the production of such products or if customer demand does not develop as expected. Ramping of production capacity also entails risks of delays which can limit our ability to realize the full benefit of new product introductions.…

15 The market for optical communications products in particular has matured over time and these products have increasingly become subject to commoditization. Both legacy competitors as well as new entrants, predominantly Asia-based competitors, have intensified market competition in recent years leading to pricing pressure. To preserve our revenues and product margin structures, we remain reliant on an integrated customer and market approach that anticipates end customer needs as requirements evolve. We also must continue to develop more advanced, differentiated products that command a premium with customers, while conversely continuing to focus on streamlining product costs for established legacy products. If we fail to continue to develop enhanced or new products that enable us to increase revenues while maintaining consistent margins, or over time are unable to adjust our cost structure to continue to competitively price more mature products, our financial condition and results of operations could be adversely affected.

We are also highly dependent on the ability to ship products to customers and to receive shipments from our suppliers. In the event of a disruption in the worldwide or regional shipping infrastructure, including as a result of geopolitical or armed conflicts, our access to supplies and our ability to deliver products to customers would correspondingly be negatively impacted. As a result of shipping disruptions, we have experienced, among other things, increased costs to ship products and delays in receiving components. Any similar disruptions in the future would likely adversely affect our operating results and financial condition.

Additionally, if operations at these contract manufacturers are adversely impacted, such as by natural disasters, energy shortages or restrictions due to the impact of a widespread health crisis disruptions or any resulting economic impact to their business, this would likely materially impact our financial condition and results of operations. Our ability to control the quality of products produced by contract manufacturers has and may in the future be impaired by pandemics or widespread health epidemics disruptions, and quality issues might not be resolved in a timely manner. Additionally, if our contract manufacturers continue experiencing disruptions or discontinue operations, we may be required to identify and qualify alternative manufacturers, which is expensive and time consuming. If we are required to change or qualify a new contract manufacturer, this would likely cause business disruptions and adversely affect our results of operations and could harm our existing customer relationships.

Restructuring activities could disrupt our business and affect our results of operations.

If we fail to effectively manage our growth or, alternatively, our spending during downturns, our business could be disrupted, which could harm our operating results.

We expect to appropriately scale our business, internal systems and organization, and to continue to improve our operational, financial and management controls, reporting systems and procedures. Growth in sales, combined with the challenges of managing geographically dispersed operations, can place a significant strain on our management systems and resources, and our anticipated growth in future operations could continue to place such a strain. The failure to effectively manage our growth could disrupt our business and harm our operating results, and even if we are able to upgrade our systems and expand our staff, any such expansion will likely be expensive and complex. Our ability to successfully offer our products and implement our business plan in evolving markets requires an effective planning and management process. In economic downturns, we must effectively manage our spending and operations to ensure our competitive position during the downturn, as well as our future opportunities when the economy improves, remains intact. The failure to effectively manage our spending and operations could disrupt our business and harm our operating results.

26 Despite our implementation of security measures, our systems and those of our third-party service providers are vulnerable to damage from these or other types of attacks, errors, acts or omissions. In addition, our systems may be impacted by natural disasters, terrorism or other similar disruptions. Any system failure, disruption, accident or security breach or incident affecting us or our third-party service providers could result in disruptions to our operations and loss or unavailability of, or unauthorized access or damage to, inappropriate access to, or use, disclosure or other processing of confidential information and other information maintained or otherwise processed by us or on our behalf. Any actual or alleged disruption to, or security breach or incident affecting, our systems or those of our third-party partners could cause significant damage to our reputation, lead to theft or misappropriation of our intellectual property and trade secrets, result in claims, investigations, and other proceedings by or before regulators, and claims, demands and litigation, legal obligations or liability, affect our relationships with our customers, require us to bear significant remediation and other costs and ultimately harm our business, financial condition and operating results. In addition, we may be required to incur significant costs to protect against or mitigate damage caused by disruptions or security breaches or incidents.…

We integrate licensed third-party technology into certain of our products. From time-to-time, we may be required to license additional technology from third parties to develop new products or product enhancements. Third-party licenses may not be available or continue to be available to us on commercially reasonable terms. The failure to comply with the terms of any license, including free open-source software, may result in our inability to continue to use such license. Our inability to maintain or re-license any third-party licenses required in our products or our inability to obtain third-party licenses necessary to develop new products and product enhancements, could potentially require us to develop substitute technology or obtain substitute technology of lower quality or performance standards or at a greater cost, any of which could delay or prevent product shipment and harm our business, financial condition, and results of operations.

Our future success depends on our ability to recruit and retain the services of executive, engineering, manufacturing, sales and marketing, and support personnel. The supply of highly qualified individuals, in particular engineers in very specialized technical areas, or salespeople specializing in the service provider, enterprise and commercial laser markets, is limited and competition for such individuals is intense. Competition is particularly intense in certain jurisdictions where we have research and development centers, including Silicon Valley, and for engineering talent generally. Competition is also intense and turnover is high in certain jurisdictions where we or our suppliers have manufacturing facilities. Also, the increase of remote work among employees in our industries has increased employee mobility and turnover, making it difficult for us to retain or hire employees. Further, to attract and retain top talent, we have offered, and we believe we will need to continue to offer, competitive compensation and benefits packages. Job candidates and existing employees often consider the value of the equity awards they receive in connection with their employment. If the perceived value of our equity awards declines, it may adversely affect our ability to attract and retain highly qualified employees.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
