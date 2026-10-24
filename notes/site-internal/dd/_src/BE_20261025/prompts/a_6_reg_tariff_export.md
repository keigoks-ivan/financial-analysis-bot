你是 stock-analyst v20 DD 的證據採集子 agent。標的：BE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - BE tariff section 232 2026
  - export control OR entity list 2026
  - BE China tariff OR trade restriction 2026
  - tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
20 Table of Contents Index to Financial Statements •Deployment of our fuel cell products can be affected by interconnection requirements, export tariff arrangements and utility tariff requirements that are each subject to change.

•Trade tariffs could have a material adverse effect on our business. •A failure to properly comply with foreign trade zone laws and regulations could increase the cost of duties and tariffs.

Deployment of our fuel cell products can be affected by interconnection requirements, export tariff arrangements and utility tariff requirements that are each subject to change.

Fuel cell net metering can be affected by local utility tariffs and fees, changes to interconnection agreement terms and fuel cell net metering requirements, and some jurisdictions do not allow the export of excess electricity. At times in the past, such changes have had the effect of significantly reducing or eliminating the benefits of such programs. Changes in the availability of, or benefits offered by, utility tariffs, the applicable net metering requirements or interconnection agreements could adversely affect the demand for our Energy Server systems. For example, in California, the fuel cell net metering tariff expressly addressing fuel cells and providing certain incentives and export capability (referred to as the “Fuel Cell Net Energy Metering” (“FC NEM”)) expired at the end of 2023 and is no longer available to new customers. Existing customers can remain on the tariff if they comply with greenhouse gas emission standards that are intended to ensure they operate at a rate that is the same or better than the grid resources they are displacing. If at some point fuel cell resources cease to operate at a rate that is the same or better than the grid resources they are displacing, this may result in increased cost.…

Trade tariffs could have a material adverse effect on our business. Our business is dependent on the availability of raw materials and components for our products. Prior tariffs imposed on steel and aluminum imports increased the cost of raw materials for our products and decreased the available supply, and, accordingly, we expect the 50% tariffs imposed on U.S. imports of steel, aluminum, copper, and subsequent derivative products to adversely impact our costs. Additional new trade tariffs or other trade protection measures that are being considered or threatened by the current U.S. federal administration and possible reciprocating tariffs from other countries in which we operate or do business in response to any such U.S. tariffs or other trade protection measures could have a material adverse effect on our business, results of operations and financial condition, particularly if the countries where we source a significant amount of our components or where we sell or seek to sell our solutions are impacted.

We have established foreign trade zones in California and Delaware, through qualification with U.S. Customs and Border Protection, which allow for “zone to zone” transfers between our facilities located in those states. The foreign trade zone allows the deferment of certain U.S. duties or tariffs until the goods enter U.S. commerce, as well as the opportunity for duty and tariff avoidance on goods directly exported from the foreign trade zones which do not enter U.S. commerce. Other savings from compliance with applicable rules and regulations include reductions in processing fees through the program. If we are unable to maintain the qualifications of our foreign trade zones, or if foreign trade zones are limited or unavailable to us in the future, we would be liable to pay outstanding duties and tariffs owed on goods located within such zones, which could have an adverse effect on our business, cash flows, and results of operations.

For example, many of our installations in California interconnect with investor-owned utilities on FC NEM tariffs. FC NEM tariffs were available for new California installations until December 31, 2023. To remain eligible for those FC NEM tariffs, installations currently on those tariffs will be required to meet greenhouse gas emissions standards that are intended to support operations at a rate that is the same or better than the grid resources they are displacing. Other generally applicable tariffs are available for customers deploying fuel cells, and do not impose greenhouse gas standards. If, and when, installations cannot meet any applicable greenhouse gas standards, there are alternative tariffs available for our customers. If the cost to remain on the FC NEM tariffs increase significantly or suitable alternatives are not available, it may negatively impact our existing customer base and future demand for our products. Additionally, the uncertainty regarding requirements for service under any of these tariffs could negatively impact the perceived value of, or risks associated with, our products, which could also negatively impact demand.

The markets for our products are heavily influenced by laws, regulations and policies, including customers’ voluntary procurement standards, as well as by tariffs, internal policies and practices of electric utility providers. These regulations, tariffs, standards, and policies often relate to electricity pricing and technical interconnection of electricity generation. These regulations, tariffs, standards, and policies are often modified and could continue to change, which could result in a significant reduction in demand for our products. For example, utility companies commonly charge fees to industrial customers for disconnecting from the electric grid. These fees could change, thereby increasing the cost to our customers of using our products and making them less economically attractive.

Although we generally are not regulated as a utility, statutes, regulations, tariffs and market rules often relate to electricity and natural gas pricing, net metering, incentives, taxation, and the rules surrounding the interconnection of electricity 35 Table of Contents Index to Financial Statements generation for specific technologies. In the U.S., governments and market operators frequently modify these statutes, regulations, tariffs and market rules. Governments, often acting through state utility or public service commissions, as well as market operators subject to FERC regulation, change, adopt or approve different utility requirements and rates for commercial and industrial customers on a regular basis. Rules adopted by FERC and state public utility commissions may also create new requirements that affect commercial and industrial customers, including the potential direct assignment of energy and transmission-system upgrade costs to new data center customers as a class. Changes, or in some cases a lack of change, in any of the laws, regulations, tariffs ordinances, or other rules that apply to our installations and new technology could make it more costly for us or our customers to install and operate our products and could negatively affect our ability to deliver cost savings to customers.

Geopolitical and security issues, such as changes in U.S. government and other nations’ administration and their associated shifts in policy and priorities, armed conflict and civil or military unrest, political instability, terrorist activity and public health emergencies, could adversely affect our business, financial condition and operating results. For example: •Trade tensions have risen between the U.S. and China. China as a country supplies multiple components including rare earth metals and compounds used in electronic and electromechanical components that are part of our tier 2 and tier 3 sub-assembly suppliers. The continued escalation of trade tensions between China and the U.S. could impact our ability to source these rare earth metals and components; •Tensions between mainland China and Taiwan have increased significantly in recent years, presenting an elevated risk of hostilities. Our products contain components which are supplied principally from Taiwan. As such, any disruption impacting Taiwan could adversely impact our ability to obtain these components and supply our customers with products. In addition, such events could adversely affect the potential strength of the Taiwan market for our Energy Server product; •The current administration has implemented new and revised tariffs on all U.S. trade partners as well as sanctions, and is in the process of negotiating trade deals.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
Supply Chain Constraints and Trade Tariff Uncertainties We continue to see effects from global supply chain tightness due to factors such as trade tensions between the U.S. and China, tariffs the current administration has also implemented on all trade partners, war and armed conflicts in Ukraine and the Middle East, and strain in relationships between the U.S. and Europe as a result of issues such as defense. While we have not experienced any significant component shortages to date, such factors, as well as challenges we face as a result of our need to expand our capacity due to the growth of our business, have placed pressure on our supply chain. Measures we are taking to mitigate these supply chain issues include expanding our supply chain base and reducing where feasible significant dependencies on any singular supply chain vendor. However, these measures may not be successful and dynamics could worsen as a result of continued geopolitical instability or escalation of current military conflicts or trade tensions. Also, additional internal factors such as continual evolution to improve our products which may require changes in the components utilized and pressure to reduce costs of components in efforts to improve margins further complicate the mitigation measures.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
