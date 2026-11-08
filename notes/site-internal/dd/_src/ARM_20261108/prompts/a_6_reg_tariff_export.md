你是 stock-analyst v20 DD 的證據採集子 agent。標的：ARM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - ARM Arm Holdings tariff section 232 2026
  - Arm Holdings export control OR entity list Semiconductors 2026
  - ARM Arm Holdings China tariff OR trade restriction 2026
  - Semiconductors tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
The U.S. and U.K. have trade and national security policies regarding exports to the PRC and certain countries that the U.S. Government suspects are supplying the PRC of technology with potential advanced compute, AI, advanced node semiconductor applications, or military uses that would require us to obtain export licenses for certain processors, which can be difficult to obtain. For example, our Neoverse V series processors meet or exceed performance thresholds under U.S. and U.K. export control regimes and thereby trigger U.S. and U.K. export license requirements prior to export and delivery to customers in the PRC. Given that national security concerns are higher for AI data centers, high-performance computing (“HPC”) and advanced compute technologies destined for the PRC and certain countries suspected of supplying the PRC and government response timelines are not defined, it can be challenging and unpredictable to obtain such export licenses. Combined with customer need for certainty, we have been able to address customer demand by licensing other central processing unit (“CPU”) cores that do not exceed the HPC performance or advanced compute export control thresholds but yet still present a compelling solution.…

Economic conditions could continue to deteriorate in the future, including as a result of fluctuating inflation and interest rates, a sustained global semiconductor shortage, supply chain disruptions and any disruptions of international trade relationships, such as tariffs, export licenses or other government trade restrictions or new or continued conflicts. In particular, the semiconductor and electronics industries could fail to grow and sustained or increasing inflation could increase our operating expenses, increase costs for our customers and reduce demand for our products or our customers’ products. In addition, adverse economic conditions affect demand for devices that our products help create, such as smartphones, automobiles and servers. Longer-term reduced demand for these or other devices could result in reduced demand for our products and significant decreases in our licensing fees and royalty revenues over time. In addition, if our customers, distributors or other companies in the value-chain build elevated inventory levels, we could experience a decrease in short-term and/or long-term demand for our products. If any of these events or disruptions were to occur, the demand for our products could be materially adversely affected along with our business, results of operations, financial condition and prospects.

Our business and operating results are also vulnerable to interruption by other events outside of our control, such as earthquakes, fire, extreme weather events, power loss, telecommunications failures, epidemics, pandemics or other public health crises, political instability, geopolitical turmoil, such as the war in Ukraine and conflicts in the Middle East, including Iran, and any sanctions, export controls or restrictions on doing business with Russia and Belarus, or with other countries (including the PRC), as well as any resulting disruption, instability or volatility in the global markets and industries resulting from such conflict, pandemics, military conflict and uncertainties arising out of terrorist attacks, including a global economic slowdown, the economic consequences of the recent resurgence and escalation of trade conflicts between the U.S. and the PRC as well as other major U.S. trade partners, the potential for deteriorating relations between the PRC and Taiwan and the associated disruptions to, or effects on, the semiconductor industry, military action or terrorist activities and associated political instability. Economic or political instability may undermine consumer confidence and/or cause current or potential customers, including the end customers of our customers or potential customers, to reduce 22 or delay their technology purchases and investments.…

We are subject to governmental export and import requirements that could subject us to liability or restrict our ability to license our products. If the U.S. Department of Commerce were to further broaden U.S. export restrictions on advanced semiconductors or foreign-origin items, these expanded restrictions would subject more of our products to U.S. export controls and could impose export restrictions on the licensing and delivery of impacted items to certain customers and trading partners. Furthermore, if the U.S. Government implemented expanded economic sanctions on specific countries or regions, that could impact our portfolio. For instance, over the last couple of years and in response to changing geopolitical events, the U.S. has introduced significant changes to export controls and sanctions with respect to advanced AI semiconductors, as well as “countries of concern” (e.g., Russia and the PRC), and, while unpredictable, we anticipate additional changes to such regulations in the future.

During 2025, the U.S. Government published export control rules and guidance on advanced compute chips and services, large compute clusters, closed-weight AI models, Gate All-Around Field-Effect Transistor (“GAAFET”) and High Bandwidth Memory (“HBM”) technologies, and semiconductor manufacturing equipment, as well as controls on transactions involving items for supercomputer and semiconductor manufacturing end-uses. The rulemakings in 2025 also results in new additions to the U.S. Entity List and modifications to the scope of items subject to license requirements for certain entities on the U.S. Entity List. As a result, our ability to license our products to designated countries or entities could be reduced, and our commercial relationships could be further harmed by limiting the ability of certain of our customers and partners from shipping chips and end products incorporating certain of our products. For instance, given U.S. and U.K. trade and national security policies regarding exports of technology with potential advanced compute or military uses, it is unlikely that we would be able to obtain a U.S. or U.K. export license for certain high performance compute cores in the Neoverse series processor family. This and any similar limitations could also reduce our revenues and cause significant uncertainty in our products roadmap, which could have an adverse effect on our business, results of operations, financial condition and prospects.

36 Also in 2025, the U.S. administration announced increased tariffs applicable to U.S. imports from all countries with some countries subject to a flat 10% tariff and others subject to higher individualized tariffs, known as reciprocal tariffs. Since the initial announcement of tariffs, a pause on certain tariffs for most countries, including China went into effect for 90 days, and exemptions were announced for certain strategic sectors, including semiconductors and electronics. On February 20, 2026, the U.S. Supreme Court issued a ruling striking down certain tariffs previously imposed under the International Emergency Economic Powers Act (“IEEPA”). Following the Supreme Court’s decision, the U.S. administration announced its intention to invoke other laws to collect tariffs and announced new tariffs on imports from all countries, in addition to any existing non-IEEPA tariffs. Although temporary relief has been provided from certain newly imposed tariffs and new trade agreements may be negotiated with existing trade partners, the economic uncertainty surrounding these actions, or the prospect that these or similar actions will be taken, could result in adverse consequences to us, including, among others, causing new or existing customers to decrease their level of business with us or causing our customers to increase the prices of their products to offset increased costs resulting from global trade conditions, which could make them less competitive.…

Further, BIS initiated a Section 232 investigation in 2025 into the effects of U.S. national security of imports of, among other things, semiconductors and semiconductor manufacturing equipment. The investigation resulted in an announcement of tariffs, effective January 15, 2026, applicable to NVIDIA H200 and AMD MI325X chips and systems incorporating such chips.

In addition, in 2026, the U.S. government launched a "Section 301" investigation into semiconductors and significantly expanded Section 232 tariffs on steel, aluminum, and copper to apply to the value of the full product not just the value of the metal contained within the full product.

Our business is subject to regulation by various governmental agencies, including, but not limited to, such agencies in the U.K., the European Union, the U.S. and the PRC. These laws and regulations affect our activities in areas including, but not limited to, labor, telecommunications, IP ownership and infringement, tax, economic sanctions, import and export control requirements and sanctions, anti-corruption, national security and foreign investment, foreign exchange controls and cash repatriation restrictions, privacy and data protection (such as the European Union General Data Protection Regulation (“GDPR”), the U.K. General Data Protection Regulation (“U.K. GDPR”), and the California Consumer Privacy Act as amended by the California Privacy Rights Act (collectively, “CCPA”)), security and cybersecurity, and anti-competition, environmental, health and safety, financial reporting and the certification requirements associated with public sector contracts. These laws, regulations and orders are complex, may change frequently and with limited notice, and many have become more stringent and have intensified over time, especially in light of continuing tensions between the U.S. and the PRC and sanctions on Russia and individual Russians as a result of the ongoing war in Ukraine.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
Developments in Export Control Regulations The Bureau of Industry and Security of the U.S. Department of Commerce (“BIS”), significantly extended the reach of U.S. export controls on the semiconductor industry, in particular advanced computing chips and services, in a series of rules and guidance published over the past year.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
