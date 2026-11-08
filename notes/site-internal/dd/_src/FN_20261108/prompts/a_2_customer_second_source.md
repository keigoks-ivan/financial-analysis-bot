你是 stock-analyst v20 DD 的證據採集子 agent。標的：FN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_second_source] 客戶 second-source 與 in-house
Q: 最大客戶是否正在導入第二供應商，或將此環節自製（in-house）？
  - FN Fabrinet largest customer second-source OR in-house 2026
  - custom chip OR component second source agreement 2026
  - Fabrinet single-source risk customer diversify supplier
  - in-house design OR insourcing Electronic Components 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm｜as_of：2026-08-18
<<<
•Fiber Metallization and Lensing: We use our fiber metallization and fiber lensing capabilities to assist our customers in packaging their products. Many optical component package designs require metallized fiber and some designs also require lensing at the tip of the fiber. We have in-house capabilities that enable us to produce these products at a low cost, with short lead times and high quality.

•Optical Testing: We have the capability to perform parametric and functional tests for a wide variety of optical devices. In many cases, we are also able to help our customers develop their own proprietary software and test fixtures.

We continuously invest in new and optimized processes to accommodate the next generation of optical devices, such as optical packaging, anti-reflective coating and complex printed circuit board technologies. We believe many of these manufacturing processes and technologies will be key to developing and commercializing the next generation of optical devices, which may include multi-function passive optics and photonic integrated circuits (which are devices that incorporate various optical components and modules into a packaged chip), receivers integrated with an optical amplifier, and active optical cabling. We also anticipate our customers will continue to desire our vertically integrated capabilities, designing customized optics and glass to be incorporated into optical components, modules and complete network or laser systems.

Suppliers of Raw Materials Our manufacturing operations use a wide variety of optical, semiconductor, mechanical and electronic components, assemblies and raw materials. We generally purchase materials from suppliers through standard purchase orders, as opposed to long-term supply agreements. We rely on sole-source suppliers for a number of critical materials. Some of these sole-source suppliers are small businesses, which presents risks to us based on their financial health and reliability, which we continually monitor. We have historically experienced supply shortages resulting from various causes, including reduced yields by suppliers, which have prevented us from manufacturing products for our customers in a timely manner. Furthermore, in some cases, our efforts to identify and secure alternative supply chain sources has resulted in our customers or their end customers requiring requalification and validation of components, a process that can often be lengthy and has negatively impacted the timing of our revenue.

We regard our own manufacturing process technologies and customized optics and glass designs as proprietary intellectual property. We own any process engineering technology independently developed in-house by our technical staff. As part of our manufacturing services, to the extent we utilize our own manufacturing process technologies in the manufacture of our customers’ products, we grant our customers a royalty-free license to these process engineering technologies for the purpose of allowing our customers to make their products. Any process engineering or other improvements that we develop in connection with the improvement or optimization of a process for the manufacturing of a customer’s products are immediately assigned to that customer. To protect our proprietary rights, we rely largely upon a combination of trade secrets, non-disclosure agreements and internal security systems. Historically, patents have not played a significant role in the protection of our proprietary rights. Nevertheless, we currently have a relatively small number of solely-owned and jointly-held PRC patents in various customized optic technologies with expiration dates between 2026 and 2040. We believe that both our evolving business practices and industry trends may result in the continued growth of our patent portfolio and its importance to us, particularly as we expand our business.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm｜as_of：2026-08-18
<<<
Consolidation in the markets we serve has resulted in a reduction in the number of potential customers for our services. For example, Nokia Corporation completed its acquisition of Infinera Corporation in February 2025; Lumentum Holdings Inc. completed its acquisition of NeoPhotonics Corporation in August 2022; Coherent Corp. (formerly known as II-VI Incorporated) completed its acquisition of Coherent, Inc. in July 2022; and Cisco Systems, Inc. completed its acquisition of Acacia Communications, Inc. in March 2021. In some cases, consolidation among our customers has led to a reduction in demand for our services as customers have acquired the capacity to manufacture products in-house.

Consolidation among our customers and their customers will continue to adversely affect our business, financial condition and operating results in several ways. Consolidation among our customers and their customers may result in a smaller number of large customers whose size and purchasing power give them increased leverage that may result in, among other things, decreases in our average selling prices. In addition to pricing pressures, this consolidation may also reduce overall demand for our manufacturing services if customers obtain new capacity to manufacture products in-house or discontinue duplicate or competing product lines in order to streamline operations. If demand for our manufacturing services decreases, our business, financial condition and operating results could be harmed.

We purchase some of the critical materials used in certain of our products from a single source or a limited number of suppliers. Supply shortages have in the past, and could in the future, impair the quality, reduce the availability or increase the cost of materials, which could harm our revenues, profitability and customer relations.

We rely on a single source or a limited number of suppliers for critical materials used in a significant number of the products we manufacture. We generally purchase these single or limited source materials through standard purchase orders and do not maintain long-term supply agreements with our suppliers. We generally use a rolling 12-month forecast based on anticipated product orders, customer forecasts, product order history, backlog, and warranty and service demand to determine our materials requirements. Lead times for the parts and components that we order vary significantly and depend on factors such as manufacturing cycle times, manufacturing yields, and the availability of raw materials used to produce the parts or components. Historically, we have experienced supply shortages resulting from various causes, including reduced yields by our suppliers, which prevented us from manufacturing products for our customers in a timely manner. The semiconductor supply chain is complex, and, in recent years, there has been a significant global shortage of semiconductors. Demand for consumer electronics surged during the COVID-19 pandemic, which in turn has increased the demand for semiconductors. At the same time, wafer foundries that support chipmakers have not invested enough in recent years to increase capacities to the levels needed to support the increased demand from all of their customers.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-18）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm｜as_of：2026-08-18
<<<
Revenues, by percentage, from individual customers representing 10% or more of our revenues is set forth in Note 21 of our audited consolidated financial statements. Because we depend upon a small number of customers for a significant percentage of our total revenues, a reduction in orders from, a loss of, or any other adverse actions by, any one of these customers would reduce our revenues and could have a material adverse effect on our business, operating results and share price. Moreover, our customer concentration increases the concentration of our accounts receivable and our exposure to payment default by any of our key customers. Many of our existing and potential customers have substantial debt burdens, have experienced financial distress or have static or declining revenues. Certain customers have gone out of business or have been acquired or announced their withdrawal from segments of the optics market. We generate significant accounts payable and inventory for the services that we provide to our customers, which could expose us to substantial and potentially unrecoverable costs if we do not receive payment from our customers.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/parts/axes_2.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
