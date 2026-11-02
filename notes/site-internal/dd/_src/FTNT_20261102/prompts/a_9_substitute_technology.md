你是 stock-analyst v20 DD 的證據採集子 agent。標的：FTNT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Fortinet product substitute technology threat 2026
  - Software - Infrastructure alternative technology disruption 2026 2027
  - FTNT Fortinet technology obsolescence risk
  - Software - Infrastructure next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm｜as_of：2026-02-25
<<<
Conditions in our markets could change rapidly and significantly as a result of technological advancements, market consolidation or de-consolidation, supply chain constraints, price list or discount changes or inflation. The development and market acceptance of alternative technologies could decrease the demand for our products or render them obsolete. Our competitors may introduce products that are less costly, provide superior performance, are better marketed, or achieve greater market acceptance than our products. Additionally, our larger competitors often have broader product lines and are better positioned to withstand a significant reduction in capital spending by end-customers, and will therefore not be as susceptible to downturns in a particular market. The above competitive pressures are likely to continue to impact our business. We may not be able to compete successfully in the future, and competition may harm our business.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm｜as_of：2026-02-25
<<<
We market and sell our products throughout the world and have established sales offices in many parts of the world. Our international sales have represented a majority of our total revenue in recent periods. Therefore, we are subject to risks associated with having worldwide operations. We are also subject to a number of risks typically associated with international sales and operations, including: •disruption in the supply chain or in manufacturing or shipping, or decreases in demand by channel partners or end-customers, including any such disruption or decreases caused by factors outside of our control such as international trade disputes or tariffs, labor or supply chain disruptions, inflation and other cost increases, international conflicts, terrorism, wars, such as the war in Ukraine, tensions between China and Taiwan, conflicts in the Middle East, critical infrastructure attacks, natural disasters, health emergencies, epidemics and pandemics, power outages and civil unrest; •fluctuations in foreign currency exchange rates or a weakening of the U.S. dollar, as a significant portion of our expenses are incurred and paid in currencies other than the U.S.…

Our products are also susceptible to errors, defects, logic flaws, vulnerabilities and inserted vulnerabilities that may arise in, or be included in our products in, different stages of our supply chain, manufacturing and shipment processes, and a threat actor’s exploitation of these weaknesses may be difficult to anticipate, prevent, and detect. If we are unable to maintain an effective supply chain security risk management and products security program or we inadvertently release a product or an update to a product with a defect in it, then the security and integrity of our products and the updates to those products that our customers receive could be exploited by third parties or insiders, or our solutions or updates thereto could cause an unintended disruption to our customers’ operations. Different customers deploy and use our products in different ways, and certain deployments and usages may subject our products to adverse conditions that may negatively impact the effectiveness and useful lifetime of our products. Further, customers may choose not to apply patches in a timely manner for business or operational reasons, or may neglect to upgrade at all and may run unpatched or unsupported devices against our guidance and industry best 26 Table of Contents practice.…

We cannot ensure that our products will prevent all adverse security events or not cause disruptions to our customers’ operations. Because the techniques used by malicious adversaries to access or sabotage networks change frequently and generally are not recognized until launched against a target, we may be unable to anticipate these techniques. In addition, defects or errors in our FortiGuard and other security subscriptions or FortiCare updates or our Fortinet appliances and operating systems could result in a failure of our FortiGuard and other security subscription services to effectively or correctly update end-customers’ Fortinet appliances and cloud-based products and thereby leave customers vulnerable to attacks or to disruptions in operations. Furthermore, our solutions may also fail to detect or prevent viruses, worms, ransomware attacks or similar threats due to a number of reasons such as the evolving nature of such threats and the continual emergence of new threats that we may fail to anticipate or add to our FortiGuard databases in time to protect our end-customers’ networks.

Managing our inventory is complex, especially in times of supply chain disruption. Our channel partners may increase orders during periods of product shortages, cancel orders or not place orders commensurate with our expectations if their inventory is too high, return products or take advantage of price protection (if any is available to the particular partner) or delay orders in anticipation of new products, and accurately forecasting inventory requirements and demand can be challenging. Our channel partners also may adjust their orders in response to the supply of our products and the products of our competitors that are available to them and in response to seasonal fluctuations in end-customer demand. If we cannot manufacture and ship our products due to, for example, global chip shortages, excessive demand on contract manufacturers capacity, natural disasters and health emergencies such as earthquakes, fires, power outages, typhoons, floods, health pandemics and epidemics or manmade events such as civil unrest, labor disruption, tariffs, cyber events, international trade disputes, international conflicts, terrorism, wars or other foreign conflicts, such as the war in Ukraine, tensions between China and Taiwan or conflicts in the Middle East, and critical infrastructure attacks, our business and financial results could be materially and adversely impacted.…

We outsource the manufacturing of our security appliance products to contract manufacturing partners and original design manufacturing partners, including manufacturers with facilities located in Taiwan and other countries outside the United States such as Accton, IBASE, Micro-Star, Senao and Wistron. Our reliance on our third-party manufacturers reduces our control over the manufacturing process, exposing us to risks, including reduced control over quality assurance, costs, supply and timing and possible tariffs. Any manufacturing disruption related to our third-party manufacturers or their component suppliers for any reason, including global chip shortages, natural disasters and health emergencies such as earthquakes, fires, power outages, typhoons, floods, health pandemics and epidemics and manmade events such as civil unrest, labor disruption, cyber events, international trade disputes, tariffs, international conflicts, terrorism, wars or other foreign conflicts, such as the war in Ukraine, tensions between China and Taiwan or conflicts in the Middle East, and critical infrastructure attacks, could impair our ability to fulfill orders. If we are unable to manage our relationships with these third-party manufacturers effectively, or if these third-party manufacturers experience delays, increased manufacturing lead-times, disruptions, capacity constraints or quality control problems in their manufacturing operations, or fail to meet our future requirements for timely delivery, our ability to ship products to our customers could be impaired and our business would be seriously harmed.…

The EU RoHS Directive and the similar laws of other jurisdictions ban or restrict the presence of certain hazardous substances such as lead, mercury, cadmium, hexavalent chromium and certain fire-retardant plastic additives in electrical equipment, including our products. We have incurred costs to comply with these laws, including research and development costs and costs associated with assuring the supply of compliant components. We expect to continue to incur costs related to environmental laws and regulations in the future. With respect to the EU RoHS, we and our competitors rely on exemptions for lead and other substances in network infrastructure equipment. It is possible one or more of these use exemptions will be revoked in the future. Additionally, although some of the EU RoHS exemptions have been extended, it is possible that some of these exemptions may expire in the future without being extended. If this exemption is revoked or expires without extension, if there are other changes to these laws (or their interpretation) or if new similar laws are passed in other jurisdictions, we may be required to re-engineer our products to use components compatible with these regulations. This re-engineering and component substitution could result in additional costs to us and/or disrupt our operations or logistics.

A significant natural disaster, such as an earthquake, drought, fire, power outage, typhoon, flood, viral outbreak or other catastrophic event, could have a material adverse impact on our business, operating results and financial condition. Our corporate headquarters are located in the San Francisco Bay Area, a region known for seismic activity, and our research and development and data center in Burnaby, Canada, from which we deliver to customers our FortiGuard and other security subscription updates, is subject to the risk of flooding and is also in a region known for seismic activity. Any earthquake in the Bay Area or Burnaby, or flooding in Burnaby, could materially negatively impact our ability to provide products and services, such as FortiCare support and FortiGuard subscription services and could otherwise materially negatively impact our business. In addition, natural disasters could affect our manufacturing vendors, suppliers or logistics providers’ ability to perform services, such as obtaining product components and manufacturing products, or performing or assisting with shipments, on a timely basis, as well as our customers’ ability to order from us and our employees’ ability to perform their duties.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTNT_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
