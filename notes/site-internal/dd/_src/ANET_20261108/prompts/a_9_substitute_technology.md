你是 stock-analyst v20 DD 的證據採集子 agent。標的：ANET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Arista Networks product substitute technology threat 2026
  - Computer Hardware alternative technology disruption 2026 2027
  - ANET Arista Networks technology obsolescence risk
  - Computer Hardware next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
We also face competition from other companies and new market entrants, current technology partners, and customers who may acquire or develop network switches and cloud service solutions for internal use and/or broaden their product portfolios to market and sell to customers. Some of these entities are developing white box networking products based on open-source network operating systems that may be provided for free using off-the-shelf or commoditized hardware technology 8 Table of Contents (“white box” hardware). Others may adopt a disaggregated approach to the procurement of hardware and leverage their own proprietary software. The arrival of new market entrants and the rapid adoption of alternative technologies may create downward pricing pressure. Such shifts could result in lost sales and materially harm our operating results and financial condition.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
In addition, business disruptions and supply chain and manufacturing disruptions may result in customers delaying or canceling or reprioritizing capital expenditures on information technology and network infrastructure, which may affect the overall demand for our products. We also believe that our customers continue to assess the impact of macroeconomic factors on their business and future investment plans, resulting in business uncertainty. Continuing or worsening economic instability or the deterioration of the financial performance, condition or prospects of our customers could result in a cancellation of, or 16 defaults in the payments for, such orders or otherwise adversely affect spending for IT, network infrastructure, systems and tools, and limit our ability to forecast future demand for our products, which could reduce expected revenue or result in a write-down of excess or obsolete inventory.

We have entered into significant purchase commitments and are susceptible to supply shortages, extended lead times or supply changes, which could disrupt or delay our scheduled product deliveries to our customers and may result in the loss of sales and customers.

We have made substantial investments to develop new products and services, make enhancements to existing products, and expand our product offerings through our acquisitions and internal research and development efforts. If we are unable to anticipate technological changes in our industry by introducing new, enhanced or expanded products and services in a timely and cost-effective manner or if we fail to introduce products and services that meet market demand or gain market share, we may lose our competitive position, our products may become obsolete, and our business, financial condition or results of operations could be adversely affected. For example, with our most recently introduced 800 GbE, AI focused Ethernet products and AI-Driven Campus and Branch Networking Offerings, our ability to maintain our competitive position with our customers will depend on our ability to deliver these new products in a timely manner, our customers' acceptance of these products and the growth of the markets that these products serve. In addition, the evaluation, testing and qualification of our new products by our customers may be lengthy and may require increased customer trials and contracts with acceptance clauses, which delay revenue recognition and may negatively impact our revenue.

Managing our manufacturing capacity and extended supply chain is complex, and our inventory management systems and related supply-chain visibility tools may not enable us to effectively manage the supply of our products and product components. Our ability to manage our supply chain has also and could continue to be adversely affected by other factors including geopolitical conditions such as international trade tensions between the U.S. and China, Canada, Mexico and other countries where we manufacture our products including Malaysia and Vietnam, the Russia-Ukraine conflict and related economic sanctions against Russia, and political tensions between China and Taiwan. Global geopolitical and macroeconomic uncertainties have resulted in prolonged manufacturing and supply chain disruptions, including temporary closures of certain manufacturing and supplier facilities particularly within China and controls on certain supplies including China's restrictions on the use of certain U.S. products and its export controls on metals used in semiconductor manufacturing such as gallium and germanium which, in turn, have caused and may continue to cause shortages of, and extended lead times for, components used to manufacture our products, increases in the prices for such components, a reduction, unpredictability or interruption of supply, prioritization of component shipments to other vendors and decommitments of orders.…

In the event that we are found to infringe, misappropriate or violate any third-party intellectual property rights, we could be enjoined, or subject to other remedial orders that would prohibit us, from making, licensing, using or importing into the U.S. or elsewhere such products or services. In order to resume such activities with respect to any affected products or services, we (or our component suppliers) would be required to develop technical redesigns that no longer infringe, misappropriate or violate the third-party intellectual property right. In any efforts to develop technical redesigns for these products or services, we (or our component suppliers) may be unable to do so in a manner that does not continue to infringe the third-party intellectual property right or that is acceptable to our customers. These redesign efforts could be extremely costly and time consuming as well as disruptive to our other development activities and distracting to management. Moreover, such redesigns could require us to obtain approvals from the court or administrative body to resume the activities with respect to these affected solutions. We may not be successful in our efforts to obtain such approvals in a timely manner, or at all.…

Many of our products and services include software or other intellectual property licensed from third parties, and we otherwise use software and other intellectual property licensed from third parties in our business. This exposes us to risks over which we may have little or no control. For example, a licensor may have difficulties keeping up with technological changes or may stop supporting the software or other intellectual property that it licenses to us. Also, it will be necessary in the future to renew licenses, expand the scope of existing licenses or seek new licenses, relating to various aspects of these products and services or otherwise relating to our business, which may result in increased license fees. These licenses may not be available on acceptable terms, if at all. In addition, a third-party may assert that we or our customers are in breach of the terms of a license, which could, among other things, give such third-party the right to terminate a license or seek damages from us, or both.…

If we experience a cybersecurity incident, or if any of the above events occur, or are perceived to have occurred, we could be subject to significant claims for liability from our customers and others and regulatory investigations and actions from governmental agencies, and we could be required to expend significant capital and other resources to remediate and otherwise address any incident, including to notify individuals, entities, or regulatory bodies. In addition, our ability to protect our intellectual property rights could be compromised and our reputation and competitive position could be significantly harmed. The regulatory and contractual actions, proceedings, litigation, investigations, fines, penalties and liabilities relating to any actual or perceived incidents can be significant in terms of fines and reputational impact and necessitate changes to our business operations that may be disruptive to us. We could incur significant costs to upgrade our systems and measures in an effort to prevent network and system disruptions and other cybersecurity incidents. Even the perception of inadequate security may damage our reputation and negatively impact our ability to win new customers and retain existing customers. Consequently, our financial performance and results of operations could be adversely affected by any of the foregoing types of incidents or perceived incidents.

45 Our corporate headquarters and the operations of our key manufacturing vendors, logistics providers and partners, as well as many of our customers, are located in areas, such as the San Francisco Bay Area, Japan and Taiwan, that are exposed to risks of natural disasters and threats, such as fires, earthquakes, tsunamis, extreme precipitation or winds, high heat or outbreaks of disease, and systemic failures, or other catastrophic events, such as widespread power outages or transportation network malfunctions. In addition, climate change may result in greater frequency and severity of such natural disasters and systemic failures. A significant natural disaster, epidemic or pandemic, systemic failure, flood or other similar event, could have a material adverse effect on our or their business, which could in turn materially affect our financial condition, results of operations and prospects. These events could result in manufacturing and supply chain disruptions, shipment delays, order cancellations, and sales delays which could result in missed financial targets. Any such disruption of our suppliers, our contract manufacturers or our service providers would likely impact our supply chain, sales and operating results. These events could also have a material adverse effect on the demand for our products, which could in turn materially affect our financial condition, results of operations and prospects.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
