你是 stock-analyst v20 DD 的證據採集子 agent。標的：GHM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - GHM Graham tariff section 232 2026
  - Graham export control OR entity list Specialty Industrial Machinery 2026
  - GHM Graham China tariff OR trade restriction 2026
  - Specialty Industrial Machinery tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-06-08）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm｜as_of：2026-06-08
<<<
Availability of Raw Materials As discussed more fully in Item 1A “Risk Factors” of this report, inflation has accelerated in the U.S. and globally due in part to global supply chain issues, a rise in energy prices, labor shortages, tariffs, and strong consumer demand. Additionally, international conflicts or other geopolitical events, including the on-going Russia and Ukraine war, the Israel-Hamas and Iran conflicts, the changes in Venezuela, and recent trade-related actions, may further contribute to increased supply chain costs due to shortages in raw materials, increased costs for transportation and energy, disruptions in supply chains, increased tariffs, and heightened inflation. The inflationary environment has increased the cost of our raw materials and labor, which impacts our financial results, especially given that a large percentage of our contracts are fixed-price in nature. To help mitigate this risk, we place orders for raw materials when the purchase orders are received from the customer to lock-in raw material pricing and manufacture a large portion of our international sales in-country which helps isolate us from the impacts of tariffs. Additionally, many of our contracts have terms and conditions that help protect us from inflationary increases.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-06-08）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm｜as_of：2026-06-08
<<<
In addition, the U.S. has previously experienced lapses in federal appropriations, which had, in the past, a short-term effect on our business. Any such future lapse (each, a "Government Shutdown") could negatively affect our ability to ship finished products to customers. We rely on federal government personnel, who are not able to perform their duties during a Government Shutdown, to conduct routine business processes related to the inspection and delivery of our products, process export licenses for us, and perform other services for us that, when disrupted, may prevent us from timely shipping products outside the U.S. If we are unable to timely ship our products outside the U.S., there could be a material adverse impact on our results of operations and business. Moreover, our inability to ship products, or the perception by customers that we might not be able to timely ship our products in the future, may cause such customers to look to foreign competitors to fulfill their demand. If our customers look to foreign competitors to source equipment of the type we manufacture, there could be a material and adverse impact on our results of operations and business.

We are subject to a number of export, import and economic sanction regulations, including the International Traffic in Arms Regulations ("ITAR"), the Export Administration Regulations ("EAR") and U.S. sanction regulations administered by the U.S. Department of Treasury, Office of Foreign Assets ("OFAC"). Foreign governments where we have operations also implement export, import and sanction laws and regulations, some of which may be inconsistent or conflict with ITAR and EAR. Where we face such inconsistencies, it may be impossible for us to comply with all applicable regulations.

If we do not obtain all necessary import and export licenses required by applicable export and import regulations, including ITAR and EAR, or do business with sanctioned countries or individuals, we may be subject to fines, penalties and other regulatory action by governmental authorities, including, among other things, having our export or import privileges suspended. We have compliance policies and procedures in place to ensure compliance with ITAR and EAR, but even if our policies and procedures for exports, imports and sanction regulations comply, but our employees fail or neglect to follow them in all respects, we might incur similar liability.

A significant amount of our revenue includes sales to the Defense industry, which makes us particularly susceptible to investigations, enforcement or other regulatory actions, prosecutions and other legal proceedings, particularly those involving the U.S. government. We are or may become subject to legal proceedings (including criminal, civil and administrative) and across a broad array of matters, including, but not limited to, government contracts, cost accounting, financial accounting and reporting, false statements or claims, sanctions or other trade regulations. These matters can divert resources; result in administrative, civil or criminal fines, penalties or other sanctions (including judgments, convictions, consent or other voluntary decrees or agreements), compensatory, treble or other damages, non-monetary relief, or other liabilities; and otherwise harm our business and our ability to obtain and retain contracts with agencies of the U.S. government. Certain outcomes may lead to our suspension or debarment from government contracts. Suspension or debarment or criminal resolutions in particular could have a material adverse effect on us because of our reliance on government 11 contracts.…

For fiscal 2026, 15% of our revenue was from customers located outside of the U.S. Moreover, through our subsidiaries, we maintain sales and engineering support offices in China and India. We also service our foreign customers through the use of subcontract vendors that are located in those countries. We intend to continue to expand our international operations to the extent that suitable opportunities become available. Our foreign operations and sales could be adversely affected as a result of: •nationalization of private enterprises and assets; •trade policies incentivizing domestic trade over international trade; •political or economic instability in certain countries and regions, such as the ongoing instability throughout the Middle East and/or portions of the former Soviet Union; •the economic impact of global health concerns; •political relationships between the U.S. and certain countries and regions; •differences in foreign laws, including difficulties in protecting intellectual property and uncertainty in enforcement of contract rights; •the possibility that foreign governments may adopt regulations or take other actions that could directly or indirectly harm our business and growth strategy; •credit risks; •currency fluctuations; •tariff and tax increases; •export and import restrictions and restrictive regulations of foreign governments; •shipping products during times of crisis or war; •our failure to comply with U.S.…

The impact of potential changes in customs and trade policies and tariffs imposed by the U.S. and those imposed in response by other countries, including China, as well as rapidly changing trade relations, could materially and adversely affect our business and results of operations.

The U.S. government has made proposals that are intended to address trade imbalances, which include encouraging increased production in the U.S. These proposals could result in increased customs duties and the renegotiation of some U.S. trade agreements. Changes in U.S. and foreign governments’ trade policies have resulted and may continue to result in tariffs on imports into, and exports from, the U.S. In the past, the U.S. imposed tariffs on imports from several countries, including China, Canada, the European Union, India, and Mexico. In response, China, Canada, the European Union, India, and Mexico have proposed or implemented their own tariffs on certain exports from the U.S. into those countries. Tariffs affecting our products and product components, including raw materials we use, particularly electronic components, high-end steel and steel related products, may add significant costs to us and make our products more expensive. Potential future changes in trade policies could result in customers changing their behavior in project procurement, due to uncertainty related to timely execution and/or import and export restrictions. As a result, our products could become less attractive to customers outside the U.S. due to U.S. import tariffs on our raw materials and our profit margins would be negatively impacted.…

Current and future conditions in the economy have an inherent degree of uncertainty and are impacted by political, market, health and social events or conditions. As a result, it is difficult to estimate the level of growth or contraction for the economy as a whole and in the specific markets in which we participate. Current economic uncertainty and market volatility is anticipated to continue as a result of higher inflation, increased tariffs, increased interest rates, supply chain disruptions, fluctuating foreign currency exchange rates and other geopolitical events. An inflationary environment can increase our cost of labor, as well as other operating costs, which may have a material and adverse impact on our financial results, especially given that a large percentage of our contracts are fixed-price in nature. In addition, economic conditions could impact and reduce the number of customers who purchase our products or services as credit becomes more expensive or unavailable. Although interest rates have increased, inflation may continue. Further, protracted uncertainty related to interest rates could have a negative effect on the securities markets generally which may, in turn, have a material and adverse effect on the market price of our common stock.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-06-08）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm｜as_of：2026-06-08
<<<
•Gross profit and margin for fiscal 2026 were $57,750 and 23.5%, respectively. The 170 basis point decline in gross profit margin compared to fiscal 2025 reflects the mix of sales in fiscal 2026, and in particular, a higher level of Defense sales and material receipts, which carry a lower profit margin. The impact of increased tariffs for fiscal 2026 was approximately an incremental $1,000 compared to fiscal 2025. Additionally, fiscal 2025 gross profit benefited $1,298 due to a grant received from the BlueForge Alliance to reimburse us for the cost of our Defense welder training programs in Batavia and related equipment, which did not repeat in fiscal 2026.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
