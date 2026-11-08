你是 stock-analyst v20 DD 的證據採集子 agent。標的：MPWR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Monolithic Power Systems product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - MPWR Monolithic Power Systems technology obsolescence risk
  - Semiconductors next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm｜as_of：2026-02-27
<<<
9 Table of Contents We expect continued competition from existing competitors as well as competition from new entrants into the semiconductor market. We believe that we are competitive in the markets in which we sell because our ICs and solutions are typically smaller in size, are highly integrated with lower energy consumption, and achieve higher performance specifications than most of our competitors. However, there is no assurance that our products will continue to compete favorably or that we will be successful in the face of increasing competition from new products introduced by existing competitors or new companies entering our markets. In addition, there has historically been a high level of consolidation in the semiconductor industry. If these or future acquisitions are successful, competition may intensify, as our competitors add resources with which to compete against us.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm｜as_of：2026-02-27
<<<
Demand for our products is a function of the health of the economies in the U.S., Europe, China and the rest of Asia. We cannot predict the timing, strength or duration of any economic disruptions, such as those resulting from global economic uncertainties, changes to trade laws and policies by the U.S. administration, and current and potential global conflicts, or the rate or magnitude of economic recovery worldwide, in our industry, or in the different markets that we serve. We also may not accurately assess the impact of changing market and economic conditions on our business and operations, resulting in excess or insufficient inventory, increased costs, inability to forecast and adverse effects on our financial condition or operating results. These and other economic factors could have a material adverse effect on demand for our products, and on our financial condition and operating results.

We are subject to U.S. laws and regulations that could limit or restrict the export of some of our products, supplies and services and may restrict our transactions with certain customers, business partners and other individuals, including, in certain cases, dealings with or between us and our employees and subsidiaries. In certain circumstances, export controls and economic sanctions may prohibit the export of certain products, services and technologies, and in other circumstances we may be required to obtain an export license before exporting the controlled item. Compliance with these laws and regulations has not materially limited our operations or our sales, but could in the future, which would materially and adversely affect our business and results of operations. We maintain an export compliance program, but our compliance controls could be circumvented, exposing us to legal liabilities, sanctions and restrictions on our business. We must also comply with export restrictions and laws imposed by other countries affecting trade and investments. Although these restrictions and laws have not materially restricted our operations in the past, they could do so in the future, which would materially and adversely affect our business and results of operations. In addition, U.S.…

We have significant business operations in Taiwan, and many of our manufacturing partners, suppliers and customers are located in Taiwan. Accordingly, our business, financial condition and results of operations may be affected by changes in governmental and economic policies in Taiwan, social instability and diplomatic and social developments in or affecting Taiwan due to its unique international political status. Although Taiwan and China have significant economic and cultural relations, we cannot assure that relations between Taiwan and China will not face political, military or economic challenges or actions in the future. Any deterioration in the relations between Taiwan and China, and other factors affecting military, political or economic conditions in Taiwan or elsewhere in Asia, could disrupt our business operations and materially and adversely affect our results of operations.

Although we provide our suppliers with rolling forecasts of our production requirements, their ability to provide wafers to us is limited by their available capacity, particularly capacity in the geometries we require, at the facilities in which they manufacture wafers for us. This lack of capacity has at times constrained our product sales and revenue growth. In addition, an increased need for capacity to meet internal demands or demands of other customers could cause our suppliers to reduce capacity available to us. Our suppliers may also require us to pay amounts in excess of contracted or anticipated amounts for wafer deliveries or require us to make other concessions in order to acquire the wafer supply necessary to meet our customer requirements. Such concessions can include long‑term capacity reservations, prepayments, take‑or‑pay terms, or tool funding, which may increase working capital needs and reduce flexibility across product cycles. If our suppliers extend lead times, limit supplies or the types of capacity we require, or increase prices due to capacity constraints or other factors, our revenues and our gross margin may materially decline in the future.…

We might not be able to deliver our products on a timely basis if our relationships with our assembly and test subcontractors are disrupted or terminated.

We do not have direct control over product delivery schedules or product quality because all of our products are assembled by third-party subcontractors and a portion of our testing is currently performed by third-party subcontractors. Also, due to the amount of time typically required to qualify assembly and test subcontractors, we could experience delays in the shipment of our products if we were forced to find alternate third parties to assemble or test our products. In addition, current and potential global conflicts and supply chain disruptions may materially impact our assembly or testing suppliers’ ability to operate. Any future product delivery delays or disruptions in our relationships with our subcontractors could have a material adverse effect on our financial condition, results of operations and cash flows.

We may face competition from customers developing products internally. Our customers generally have substantial technological capabilities and financial resources. Some customers have traditionally used, and continue to use, these resources to develop their own products internally. The prospects for our products in these markets are dependent in part upon our customers’ acceptance of our products as an alternative to their internally developed products. Our future sales prospects also are dependent upon acceptance and qualification of third-party sourcing for products as an alternative to in-house development. Customers may continue to increase their use of internally developed components. They may also decide to develop or acquire components, technologies or products that are similar to, or that may be substituted for, our products, or acquire companies that compete with us. If any of these situations were to occur, our business, financial condition and results of operations could be materially and adversely affected.

21 Table of Contents Risks Associated with IT and Cybersecurity Implementation of enhanced enterprise resource planning (“ERP”) or other IT systems could result in significant disruptions to our operations.

Cybersecurity risks, data protection or privacy breaches, cyberattacks, systems integration issues and unauthorized use of AI tools could disrupt our internal operations and/or harm our reputation, and any such disruption or harm could cause a reduction in our expected revenue, increase our expenses, negatively impact our results of operation or otherwise adversely affect our stock price.

Threat actors may be able to penetrate our network security and misappropriate or compromise our confidential and proprietary information, create system disruptions or cause shutdowns, among other things. Further, as AI capabilities improve, threat actors may quickly develop more sophisticated and convincing attacks. Cybersecurity incidents, attacks and threats are increasingly sophisticated, constantly evolving and originate from many sources globally and often cannot be recognized or understood until the target has already been attacked. The costs to us to eliminate or alleviate cyber or other security problems, bugs, viruses, worms, malicious software programs and security vulnerabilities could be significant, and our efforts to address these problems may not be successful and could result in interruptions and delays that may impede our sales, manufacturing, distribution, financial reporting or other critical functions. Despite our efforts to prevent these threats and disruptions to our information technology systems, these systems and those of our third-party providers may be affected by damage or interruption resulting from, among other causes, cybersecurity incidents, attacks, security breaches, power outages, system or operational failures or malware (including ransomware and other programs that operate with malicious intent).

Portions of our IT infrastructure may also experience interruptions, delays or cessations of service or produce errors in connection with systems integration or migration work that takes place from time to time. We may not be successful in implementing new systems and transitioning data, which could cause business disruptions and our remediation efforts may be expensive, time consuming, disruptive and resource-intensive. Such disruptions could adversely impact our ability to fulfill orders in a timely manner and interrupt other processes. Delayed sales or a loss of customers resulting from these disruptions could adversely affect our financial results and reputation.

Compliance with environmental laws and regulations could cause disruptions in our business and operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MPWR_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
