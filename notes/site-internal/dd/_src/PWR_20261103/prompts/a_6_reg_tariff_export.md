你是 stock-analyst v20 DD 的證據採集子 agent。標的：PWR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - PWR Quanta Services tariff section 232 2026
  - Quanta Services export control OR entity list Engineering & Construction 2026
  - PWR Quanta Services China tariff OR trade restriction 2026
  - Engineering & Construction tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm｜as_of：2026-02-19
<<<
The overall regulatory environment also creates both challenges and opportunities for our business. In recent years, certain of our projects and certain customer spending in our industries have been negatively impacted by regulatory and permitting delays, as well as private legal challenges related to regulatory requirements, particularly with respect to large transmission and pipeline projects. Any tariffs, duties, taxes, assessments, or other limitations on the availability or sourcing of materials or components for our customers’ projects can also increase costs for customers and create variability of project timing. For example, regulatory, legislative or executive action with respect to regional and global trade relationships have impacted, and may impact in the future, the supply chain for certain components required for our customers’ projects (e.g., solar panels). For further information regarding the effects of regulation on our business, see Risks Related to Operating Our Business and Risks Related Regulation and Compliance in Item 1A. Risk Factors in Part I of this Annual Report.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm｜as_of：2026-02-19
<<<
Certain industries in which we operate can be cyclical and our business is subject to seasonality and other factors that can result in significantly different operating results from quarter to quarter, and therefore our results in any particular quarter may 16 not be indicative of future results. Our quarterly results have been and may in the future be materially and/or adversely affected by, among other things: •the timing and volume of work we perform and our performance with respect to ongoing projects and services, including as a result of fluctuations in the amount of work customers assign to us under our agreements (e.g., MSAs), delays and reductions in scope of projects, and project and agreement terminations, expirations or cancellations; •increases in project costs that result from, among other things, natural disasters and emergencies, adverse weather conditions or events, legal challenges, permitting, regulatory or environmental processes, tariffs, or inaccurate project cost estimates; •variations in the size, scope, costs and operating income margins of ongoing projects, as well as the mix of our customers, contracts and business; •fluctuations in economic, political, financial, industry and market conditions on a regional, national or global basis, including as a result of, among other things, inflationary pressure that impacts our costs associated with labor, equipment and materials; increased interest rates; default or threat of default by…

Our overall business, financial condition, results of operations and cash flows can be negatively impacted by our activities and operations outside the continental United States, including our international operations and operations in U.S. territories. Although these operations are presently conducted primarily in Canada and Australia, we also perform work in other foreign countries and U.S. territories. For the year ended December 31, 2025, we derived $2.00 billion, or 7.0%, of our consolidated revenues from foreign operations, the substantial majority of which was related to Canada and Australia. Changes in economic conditions, including those resulting from wars and other geopolitical conflicts, civil unrest, public health crises, pandemics, acts of terrorism, or volatility in global markets, may adversely affect demand for our services and our customers’ ability to pay for our services. In addition, at times we are paid for work outside the United States in currencies other than the U.S. dollar. Such payments are subject to fluctuating foreign currency exchange rates and may exceed our local currency needs, and, in certain instances, those amounts may be subject to temporary blocking, taxes or tariffs, and we may experience difficulties if we attempt to convert such amounts to U.S. dollars.…

We rely on suppliers to obtain necessary materials and subcontractors to perform portions of our services, and our customers rely on suppliers for materials necessary for the construction, upgrade and repair and maintenance of their infrastructure. We also rely on equipment manufacturers to timely provide us with the equipment required to conduct our operations, including a significant number of specialty vehicles. Limitations on the availability of suppliers, subcontractors or equipment manufacturers could negatively impact our or our customers’ operations, particularly in the event we rely on a single or small number of providers. The risk of a lack of available suppliers, subcontractors or equipment manufacturers can be heightened as a result of market, regulatory or economic conditions. For example, customers in certain U.S. states and Canada, in order to receive certain funding or for other reasons, may expect or compel us to engage a specified percentage of services from suppliers or subcontractors that meet diversity-ownership requirements, which can further limit our pool of available suppliers and subcontractors and limit our ability to secure contracts, maintain our services or grow in those areas. Availability of suppliers and manufacturers may also be limited by U.S.…

Pursuant to certain contracts, including fixed price and EPC contracts where we have assumed responsibility for procuring materials for a project, we may be exposed to availability issues and price increases for materials that are utilized in connection with our operations, including, among other things, copper, steel, aluminum, specialized project components (e.g., transformers, solar panels, breakers, turbines, batteries) and raw materials utilized for certain of our product solutions. In addition, the timing of our customers’ ongoing projects, as well as their capital budgets and decision-making with respect to the timing of the future projects, can be negatively impacted by a lack of availability or an increase in prices of these materials. Prices and availability could be materially impacted by, among other things, supply chain and other logistical challenges (including inability of manufacturers to timely meet demand), global trade relationships (e.g., tariffs, duties, taxes, assessments, sourcing restrictions) and other general market and geopolitical conditions (e.g., inflation, market volatility, increased interest rates and geopolitical conflicts).…

For example, in the past, sourcing restrictions on critical components for our customers’ projects have resulted in supply chain and logistical challenges, which negatively impacted certain of our services. We may be impacted in the future by sourcing restrictions, including, but not limited to, taxes, tariffs and duties, which may negatively impact project timing within certain of our markets in the future. Furthermore, with respect to our contracts under which we are responsible for procuring all or a portion of the materials needed for projects, including our EPC contracts, we are often required to comply with complex sourcing and transportation regulations, which can involve cross-border movement of such materials. Changes to, or our failure to comply with, these regulatory requirements can result in project delays and additional project costs, which may be substantial and not recoverable from third parties, and in some cases, we may be required to compensate the customer for such delays, including in circumstances where we have guaranteed project completion or performance by a scheduled date and incur liquidated damages if we do not meet such schedule. Additionally, our failure to comply with these regulatory requirements could result in criminal or civil fines, penalties, forfeitures or other sanctions.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm｜as_of：2026-02-19
<<<
Demand for services. Some of our services are provided under contracts, including MSAs and similar agreements, pursuant to which our customers are not committed to specific volumes of our services. Therefore our volume of business can be positively or negatively affected by fluctuations in the amount of work our customers assign us in a given period, which may vary by geographic region. Examples of items that may cause demand for our services to fluctuate materially from quarter to quarter include: the financial condition of our customers, their capital spending and their access to and cost of capital; acceleration of any projects or programs by customers (e.g., modernization or hardening programs); economic and political conditions on a regional, national or global scale, including availability of renewable energy tax credits; interest rates; governmental regulations affecting the sourcing and costs of materials and equipment; other changes in U.S. and global trade relationships (e.g., tariffs, taxes); and project deferrals and cancellations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
