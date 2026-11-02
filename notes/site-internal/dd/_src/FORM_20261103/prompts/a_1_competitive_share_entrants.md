你是 stock-analyst v20 DD 的證據採集子 agent。標的：FORM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - FORM FormFactor market share gaining OR losing 2026
  - FormFactor new entrant OR displace threat Semiconductor Equipment & Materials 2026
  - FORM competitor design win 2026
  - FormFactor vs Semiconductor Equipment & Materials peers market share trend 2025 2026


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

We believe that the primary competitive factors in the production probe card market depend upon the type of integrated circuit being tested. These factors include customer service, knowledge of measurement techniques, custom design success, delivery time, price, probe card lifetime, chip damage prevention, probe tip touch-down accuracy, electrical signal speed and current carrying capability, number of chips contacted in parallel, number of probe tips and their layout and pitch, signal integrity, and the frequency and effectiveness of any required cleaning. As a result of our relative strengths in these areas, we believe that we compete favorably in the advanced probe card market, and in probe cards for parallel testing of chips with densely-packed bond pads, bumps or pillars, and in high signal integrity testing of wireless radio frequency devices that operate up to millimeter-wave frequencies, a capability needed for components used in 5G applications. We believe that this high-frequency capability also enables us to compete favorably in HBM testing, which is a stack of eight, twelve, or even sixteen individual DRAM die assembled with advanced packaging processes like through-silicon-vias and thermo-compression bonding.

Analytical Probes. Our primary competitors in the analytical probe market are GGB Industries Inc. and MPI Corporation. We believe that the primary competitive factors in this market are breadth of probe types, probe frequency and electrical signal integrity, contact integrity and the related cleaning required, knowledge of measurement techniques, calibration support, delivery time and price. We believe that we compete favorably with respect to these factors.

Probe Stations. Our primary competitors in the probe station market are MPI Corporation, Shenzhen Senmeixieer Technology Co., Ltd (“Semishare”), STAr Technologies, Inc., Tokyo Electron Limited (“TEL”), and Wentworth Laboratories, Inc. We believe that the primary competitive factors in the probe station market are measurement accuracy and versatility at temperature, including cryogenic temperatures, measurement speed, automation features, knowledge of measurement techniques, completeness of the measurement solutions, delivery time and price. We believe that we compete favorably with respect to these factors.

Thermal Subsystems. In the market for thermal subsystems, we compete principally against AEM Singapore Pte., ERS Electronic GmbH, and Temptronic Corporation. In addition, many of our probe station competitors develop and produce their own thermal subsystems for use in their products. We believe the primary competitive factors in this market are thermal performance, reliability, flexibility and completeness of product offerings. We believe that we compete favorably with respect to these factors.

Cryogenic Systems. In the market for cryogenic systems, we compete principally against Bluefors Oy, Lake Shore Cryotronics, Inc, Maybell Quantum Industries Inc., Montana Instruments, and Quantum Design. We believe the primary competitive factors in this market are cryogenic performance, reliability, throughput and application expertise. We believe we compete favorably with respect to these factors.

Some of our competitors are also suppliers of other types of test and measurement equipment or other semiconductor equipment and may have greater financial and other resources than we do. Our competitors may enhance their current products and may introduce new products that will be competitive with ours. New alternatives to our products may also be introduced, by our current competitors or others, which may reduce the value of one or more of our products.

Semiconductor manufacturers may implement chip designs that include capabilities or use other methodologies that increase test throughput and reduce test content. This may reduce or eliminate some or all of our current products’ advantages. Semiconductor manufacturers may also increase their use of test strategies that include low performance semiconductor testers, 9 less complex probe cards, or test procedures that do not involve our products. Our ability to compete favorably may also be adversely affected by the long-standing relationships between our competitors and certain semiconductor manufacturers.

No assurance can be given that patents will not be challenged, invalidated or circumvented, or that the rights granted thereunder will provide us with a sustained competitive advantage. In addition, there can be no assurance that we will be able to protect our technology, or that competitors will not be able to independently develop similar or functionally competitive technologies, design around our patents, or attempt to manufacture and sell infringing products in countries that do not strongly enforce intellectual property rights.

Our compensation programs help attract and retain key talent and are designed for our employees to share in our company’s success. These programs focus on compensation that we believe is market-competitive, reflects company performance, and aligns with drivers of stockholder value with differentiation based on performance, role, geographic location, and tenure. We use information from outside compensation and benefits consulting firms to evaluate the competitiveness of the rewards we offer to employees, and to evaluate the structure of our compensation and benefit programs, as a benchmark against our peers within the industry.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
We have experienced increased competition in the markets in which we operate, and we expect competition to intensify in the future. Increased competition has resulted in, and in the future may result in, price reductions, reduced gross margins or loss of market share.

11 Our current or potential competitors may have larger customer bases, more established customer relationships or greater financial, technical, manufacturing, marketing and other resources than we do. As a result, they might be able to respond more quickly to new or emerging technologies and changes in customer requirements, devote greater resources to the development, promotion, sale and support of their products, and reduce prices to increase market share.

Not only do we need the technical expertise to implement the changes necessary to keep our technologies current, but we must also rely heavily on the judgment of our management to anticipate future market trends. If we are unable to timely predict industry changes or industry trends, or if we are unable to modify our products or design, manufacture and deliver new products on a timely basis, or if a third party with which we engage does not timely deliver a component or service for one of our product modifications or new products, we might lose customers or market share. In addition, we might not be able to recover our research and development expenditures, which could harm our operating results.

A relatively small number of customers account for a significant portion of our revenues. One customer represented 22.9% of total revenues in fiscal 2025, two customers represented a combined 33.5% of total revenues in fiscal 2024 and one customer represented 17.1% of total revenues in fiscal 2023. We anticipate that sales of our products to a relatively small number of customers will continue to account for a significant portion of our revenues, which can drive material fluctuations in sales volume, gross margins due to changes in mix, and leverage on fixed costs. Consolidation in the semiconductor industry may increase this concentration. In the future, the loss of any of these customers, or cancellation, reduction or deferral of even a small number of purchases of our products by these customers, could significantly reduce our revenues. A decline in our 12 customers' market share and commercial success, including their ability to compete favorably within their respective end markets, could significantly impact demand for our products and reduce our revenues. Cancellations, reductions, deferrals or non-payment of invoices could result from downturns in the semiconductor industry, manufacturing delays, quality or reliability issues with our products, or from interruptions to our customers’ operations due to fire, natural disasters or other events, or other issues with the financial stability of our customers.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
