你是 stock-analyst v20 DD 的證據採集子 agent。標的：BWA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - BorgWarner product substitute technology threat 2026
  - Auto Tier 1 / Propulsion + eProducts alternative technology disruption 2026 2027
  - BWA BorgWarner technology obsolescence risk
  - Auto Tier 1 / Propulsion + eProducts next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm｜as_of：2026-02-11
<<<
17 Table of Contents We have recorded goodwill and indefinite-lived intangible assets related to acquisitions. We periodically assess these assets to determine if they are impaired. Significant negative industry or macroeconomic trends, disruptions to our business, inability to effectively integrate acquired businesses, unexpected significant changes or planned changes in use of the assets, dispositions and market capitalization declines may impair these assets.

The combination of independent businesses is a complex, costly and time-consuming process that requires significant management attention and resources. It is possible that the integration process could result in the loss of key employees, the disruption of our operations, the inability to maintain or increase our competitive presence, inconsistencies in standards, controls, procedures and policies, difficulties in achieving anticipated cost savings, synergies, business opportunities and growth prospects from the acquisition, the diversion of management’s attention to integration matters and/or difficulties in the assimilation of employees and corporate cultures. Any or all of these factors could adversely affect our ability to maintain relationships with customers and employees or to achieve the anticipated benefits of the acquisition and could have an adverse effect on the combined company. In addition, many of these factors are outside of our control, and any one of these factors could result in increased costs, decreases in the amount of expected revenues, unanticipated risks and liabilities associated with the acquired business, and additional diversion of management’s time and energy, which could materially adversely impact our business, financial condition and results of operations. In addition, if the expected benefits of an acquisition do not meet the expectations of investors or securities analysts, the market price of our common stock may decline.

We have taken, are taking, and may in the future take restructuring actions to realign and resize our production capacity and cost structure to meet current and projected operational and market requirements. Implementation of any restructuring action may be costly and disruptive to our business, and we may not be able to realize the cost savings, operational improvements and estimated workforce reductions that we anticipate within the projected timing or at all. We are also subject to the risks of labor unrest, negative publicity and business disruption in connection with our restructuring actions. Additionally, as a result of restructuring initiatives, we may experience a loss of continuity, loss of accumulated knowledge and/or inefficiency, loss of key employees and/or other retention issues during transitional periods. Restructuring can require a significant amount of time and focus, which may divert attention from operating and growing our business. Moreover, we base projections of any cost savings or other benefits associated with our restructuring actions on current business operations and market dynamics, and various factors, including but not limited to our evolving business models, future investment decisions, market environment and technology landscape, could significantly impact the success of these actions. Refer to Note 4, “Restructuring,” to the Consolidated Financial Statements for more information.

In 2025, the U.S. announced significant tariffs on imports from a broad range of countries, including the European Union, Canada, Mexico and China. These tariffs have increased the cost of raw materials and components we purchase, and to the extent the tariffs announced to date or announced in the future become or remain effective and are maintained, these tariffs would likely further increase the cost of raw materials and components we purchase. The imposition of tariffs by the U.S. has resulted in retaliatory tariffs from other countries, including China, which has increased and would continue to increase the cost 21 Table of Contents of products we sell. Additionally, ongoing changes in U.S. and foreign government trade policies, including potential modifications to existing trade agreements and further restrictions on free trade, could introduce additional uncertainty with respect to trade policies and government regulations affecting international trade. Tariffs or retaliatory tariffs announced to date or announced in the future, current trade tensions, any escalation of trade tensions, additional tariffs, retaliatory measures by foreign governments, shifts in U.S.…

22 Table of Contents To improve efficiency and reduce costs, we have regionally centralized the information systems that support our business processes such as invoicing, payroll, and general management operations. If the centralized systems are disrupted or disabled, key business processes could be interrupted, which could adversely affect our business.

A failure of or disruption in our information technology infrastructure, including a disruption related to cybersecurity, could adversely impact our business and operations.

We rely on the capacity, reliability and security of our IT systems and infrastructure to operate our business. IT systems are vulnerable to disruptions, including those resulting from natural disasters, cyber-attacks or failures in third-party provided services. Disruptions and attacks on our IT systems pose a risk to our business operations and our ability to protect our systems, networks and communications, and the confidentiality and availability of third-party and internal data, including our employees. Some cyber-attacks depend on human error or manipulation, including phishing attacks, social engineering schemes or ransomware to gain access to systems or carry out disbursement of funds or other frauds, which raise the risks from such events and the costs associated with protecting against such attacks. Although we have implemented security policies, processes, and layers of defense designed to help identify and protect against intentional and unintentional misappropriation or corruption of our systems and information and disruptions of our operations (and, to date, we are not aware that we have experienced a cybersecurity incident that has materially affected our business strategy, results of operations, or financial condition), we have been, and likely will continue to be, subjected to such attacks or disruptions which could be material.…

Work stoppages, production shutdowns and similar events could significantly disrupt our business.

Because the automotive industry relies heavily on just-in-time delivery of components during the assembly and manufacture of vehicles, a work stoppage or production shutdown at one or more of our manufacturing and assembly facilities could have adverse effects on our business. Similarly, if one or more of our customers were to experience a work stoppage or production shutdown, that customer would likely halt or limit purchases of our products, which could result in the shutdown of the related manufacturing facilities. A significant disruption in the supply of a key component due to supply constraints or due to a work stoppage or production shutdown at one of our suppliers or any other supplier could have the same consequences and, accordingly, have an adverse effect on our financial results.

Climate change is receiving increasing attention worldwide, which has led to significant legislative and regulatory efforts to limit greenhouse gas emissions. Our manufacturing plants use energy, including electricity and natural gas, and certain of our plants emit amounts of greenhouse gas that may be affected by these legislative and regulatory efforts. Greenhouse gas regulation could increase the price of the electricity we purchase, increase costs for use of natural gas, potentially restrict access to or the use of natural gas, require us to purchase allowances to offset our own emissions or result in an overall increase in costs of raw materials, any one of which could increase our costs, reduce competitiveness in a global economy or otherwise negatively affect our financial condition, results of operations and reputation. Many of our suppliers face similar circumstances. Supply disruptions would raise market rates and jeopardize the continuity of production and could have an adverse effect on our financial results.

Climate changes could also disrupt our operations by impacting the availability and cost of materials within our supply chain and could also increase insurance and other operating costs. In addition, extreme weather events may damage a facility or surrounding infrastructure, making the facility unusable for a time. These factors may impact our decisions to construct new facilities.

We provide product warranties to our customers for some of our products. Under these product warranties, we may be required to bear costs and expenses for the repair or replacement of these products. As suppliers become more integrally involved in the vehicle design process and assume more of the vehicle assembly functions, auto manufacturers are increasingly looking to their suppliers for contribution when faced with recalls and product warranty claims. A recall claim brought against us, or a product warranty claim brought against us, could adversely impact our results of operations. In addition, a recall claim could require us to review our entire product portfolio to assess whether similar issues are present in other product lines, which could result in significant disruption to our business and could have an adverse impact on our results of operations. We cannot assure that costs and expenses associated with these product warranties will not be material or that those costs will not exceed our available insurance, or any amounts accrued for such product warranties in our financial statements.

29 Table of Contents Suppliers’ economic distress could result in supply interruptions and, in turn, disrupt our operations and adversely affect our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
