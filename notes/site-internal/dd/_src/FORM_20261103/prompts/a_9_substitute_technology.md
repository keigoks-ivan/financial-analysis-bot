你是 stock-analyst v20 DD 的證據採集子 agent。標的：FORM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - FormFactor product substitute technology threat 2026
  - Semiconductor Equipment & Materials alternative technology disruption 2026 2027
  - FORM FormFactor technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
Research, Development and Engineering The semiconductor industry is subject to rapid technological change with a continuous stream of new product introductions and technology enhancements. We believe that our continued commitment to research and development and our timely introduction of new and enhanced products and technologies are integral to maintaining and enhancing our competitive position. We allocate significant resources to these efforts and prioritize those resources to prepare for our customers’ next generation electrical test and measurement challenges. We also increasingly seek to deploy our resources to solve fundamental challenges that are both common to, and provide competitive advantage across, our probe card and system product offerings and roadmaps.

Competition The markets for our products are highly competitive, and we anticipate that these markets will continually evolve and be subject to rapid technological change. Our current and potential competitors are as below: Probe Cards. The probe card market is comprised of many domestic and foreign companies, and has historically been fragmented with many local suppliers servicing individual customers in often differentiated applications. Our primary competitors are Japan Electronic Materials Corporation, Korea Instrument Co., Ltd., Micronics Japan Co., Ltd., MPI Corporation, STAr Technologies, Inc., Max One, Technoprobe S.p.A, TSE Co., Ltd., among others.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
11 Our current or potential competitors may have larger customer bases, more established customer relationships or greater financial, technical, manufacturing, marketing and other resources than we do. As a result, they might be able to respond more quickly to new or emerging technologies and changes in customer requirements, devote greater resources to the development, promotion, sale and support of their products, and reduce prices to increase market share.

We must continue to innovate and to invest in research and development to improve our competitive position and to meet the test and measurement requirements of our customers. Our future growth depends, in significant part, upon our ability to work effectively with and anticipate the future technical and operational needs of our customers and to develop and support new products and product enhancements to meet those needs on a timely and cost-effective basis. This may become more difficult to do as the semiconductor industry innovates to address demand for AI-related products, which may develop more slowly than we anticipate or change rapidly from one period to another for a variety of reasons, including industry-wide shifts in expectations and technological developments. Our customers’ needs are becoming more challenging as the semiconductor industry continues to experience rapid technological change driven by the demand for complex circuits that are shrinking in size, are increasing in speed and functionality, have more complex layouts, and are produced on shorter cycle times and at reduced unit cost.

We obtain some of the components and materials used in our products, such as printed circuit board assemblies, plating materials and ceramic substrates, from a sole source or a limited group of suppliers, and in some cases alternative sources are not currently available. Because we rely on purchase orders rather than long-term contracts with the majority of our suppliers, we cannot guarantee our ability to obtain components and materials in the long term. A sole or limited source supplier could increase prices, which could lead to a decline in our gross profit. Our dependence upon sole or limited source suppliers exposes us to several other risks, including inability to obtain an adequate supply of materials, late deliveries, poor component quality, and business disruptions while we seek to identify and qualify alternative suppliers. This could be exacerbated by certain events outside the control of either the supplier or us, such as global, regional or national health crises, armed conflicts, increased tariffs and trade barriers, regional tensions or other adverse global, regional and national events. The occurrence of any of these risks could adversely impact our business, results of operations and financial condition.

15 We are dependent on the availability of certain key raw materials and natural resources used in our products and various manufacturing processes, and we rely on third parties to supply us with these materials in a cost-effective and timely manner. Our access to raw materials may be adversely affected if our suppliers’ operations were disrupted as a result of limited or delayed access to key raw materials and natural resources, which may result in increased cost for these items.

For example, our manufacturing facilities are located in seismically active areas in California and Oregon. The manufacturing equipment and processes that we use can be severely disrupted by seismic activity. A significant seismic event in an area of our operations could have a materially negative impact on our operations, financial results or financial condition.

A variety of factors, including natural disasters, health crises, climate change, military conflicts and other geopolitical events, may adversely affect national, regional and global economies and financial markets. Recent political changes have created an environment of tension and uncertainty in economic matters, particularly with regard to tariffs and international trade. Any such adverse events may result in global, regional or national economic slowdowns or other economic disruptions or downturns. Such disruption or downturns could curtail or delay spending by businesses and consumers which may ultimately result in reductions in the demand for our products, greater volatility in demand and supply conditions and other adverse impacts. For example, any deterioration in the relations between Taiwan and China, and other factors affecting military, political or economic conditions in Taiwan or elsewhere in Asia, could adversely impact our suppliers, manufacturers and customers with operations located in the region, which could disrupt our business operations, affect demand for our products or increase our costs, negatively impacting our revenues, gross margins, and overall results of operations. Additionally, these events may also increase uncertainty in global credit and financial markets.…

16 We rely on the security and integrity of our electronic data systems, managed both internally and by third parties, for our business requirements, and our business can be damaged by disruptions, security breaches or compromises of these systems.

Our electronic data systems may be subject to defects, failures or disruptions as a result of, among other things, natural disasters, accidents, power disruptions, telecommunications failures, deficiencies in new system designs and implementations, acts of terrorism or war, physical security breaches, computer viruses or other cyber-attacks. Such incidents or other system failures or disruptions could subject us to downtime and delays, compromise or loss of sensitive or proprietary information, destruction or corruption of data, financial losses from remedial actions, breaches of obligations to third parties under privacy laws or contracts, or damage to our reputation or customer relationships. Any of the foregoing could have a material adverse effect on our business, operating results and financial condition.

Failures in our information technology systems, including those incorporating artificial intelligence, or our inability to adapt to technological advancements, could disrupt our operations and harm our business.

Our operations rely significantly on the continuous and secure operation of our information technology systems, networks, and infrastructure, including those of our third-party service providers. These systems are critical for managing our internal operations, processing transactions, communicating with customers and suppliers, and protecting sensitive data. Despite our efforts to maintain the security and integrity of our IT environment, our systems are subject to inherent risks, including natural disasters, power outages, telecommunications failures, malicious cyberattacks (such as ransomware, phishing, and denial-of-service attacks), computer viruses, or human error. Any significant disruption, security breach, or unauthorized access to or disclosure of confidential information could lead to significant financial losses, reputational damage, regulatory penalties, legal liabilities, and operational disruptions, which could materially and adversely affect our business.

If we choose not to protect our proprietary rights or fail in our efforts to protect our proprietary rights, our competitors might gain access to our technology. Unauthorized parties might attempt to copy aspects of our products or to obtain and use information that we regard as proprietary. Others might independently develop similar or competing technologies or methods or design around our patents. In addition, the laws of many foreign countries in which we or our customers do business do not protect our intellectual property rights to the same extent as the laws of the United States. As a result, our proprietary rights could be compromised, our competitors might offer products similar to ours, and we might not be able to compete successfully. We also cannot assure that: •our means of protecting our proprietary rights will be adequate; •patents will be issued from our pending or future applications; •our existing or future patents will be sufficient in scope or strength to provide any meaningful protection or commercial advantage to us; •our patents or other intellectual property will not be invalidated, circumvented or successfully challenged in the United States or foreign countries; or •others will not misappropriate our proprietary technologies or independently develop similar technologies, duplicate our products or design around any of our patents or other intellectual property, or attempt…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
