你是 stock-analyst v20 DD 的證據採集子 agent。標的：ON。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - ON Semiconductor product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - ON ON Semiconductor technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm｜as_of：2026-02-09
<<<
Trends, Risks and Uncertainties Related to Our Business The manufacturing and other operations required to produce our products are highly dependent on the efficient operation of numerous processes, including processes contingent upon third-party component manufacturers and other service providers, and any disruption in these processes could have a material adverse effect on our business and results of operations.

Our manufacturing network includes multiple owned and third-party facilities, which may each produce one or more components necessary for the assembly of a single product. As a result of this interdependence, an operational disruption at a single facility may have a disproportionate impact on our ability to produce many of our products. In the event of such a disruption, we may be unable to effectively source replacement components on acceptable terms from qualified third parties, in which case our ability to produce many of our products could be materially disrupted or delayed. Conversely, some of our facilities are single source facilities that only produce one of our end-products, and a disruption at any such facility would materially delay or cease production of the related product. In the event of any such operational disruption, we may experience difficulty in beginning production of replacement components or products at new facilities or transferring production to other existing facilities, any of which could result in a loss of future revenues and materially adversely affect our business and results of operations.

Our manufacturing efficiency is contingent upon the operations of these interdependent processes and will continue to be an important factor in our future profitability, and there can be no assurance that we will be able to maintain our manufacturing efficiency, increase our manufacturing efficiency to the same extent as our competitors when facing an increased demand, or be successful in our manufacturing rationalization plans. For example, public health crises may cause disruption to our domestic 17 and international operations. Any associated worker absenteeism, quarantines and restrictions on certain of our employees’ ability to perform their jobs, office and factory closures or restrictions, labor shortages, disruptions to ports and other shipping infrastructure, border closures and/or other travel or health-related restrictions could, depending on the magnitude of such effects on our manufacturing activities (or activities of our suppliers, third-party distributors or sub-contractors), cause disruption and delay to our supply chain, manufacturing and product shipments. Such disruption and delays could materially adversely affect our business, results of operations and financial condition.

In addition, implementation of a business strategy may lead to the disruption of our existing business operations. Similarly, the contingent risks associated with transferring our existing operations to an acquirer, as is the case with several transition services being provided in connection with some of our prior divestitures, could materially impact our financial condition or results of operations and/or could disrupt our existing operations, especially if the acquirer is unable to meet its commitments under any transition services agreements or if the acquirer encounters financial difficulty. Furthermore, any adjustments we make to our manufacturing capacity, whether in response to customer demand or based on business strategy (such as increasing investment in capacity for new products and technology or divesting non-strategic operations), may adversely impact our existing operations or our customer relationships, require additional management time and effort to implement successfully, and, in the case of capacity expansion, lead to higher than anticipated capital expenditures. There are inherent execution risks in expanding or right-sizing production capacity, whether at one of our own factories or at a third-party factory that we utilize, all of which could increase our costs and negatively impact our operating results.

The semiconductor industry is characterized by rapidly evolving technologies, innovation, short product life cycles, evolving regulatory and industry standards and certifications, changing customer needs, wide fluctuations in supply and demand and frequent new product introductions. Products are often replaced by more technologically advanced substitutes and, as demand for older technology falls, the price at which such products can be sold drops. If we cannot advance our process technologies or improve our production efficiencies to a degree sufficient to maintain required margins, we will not be able to make a profit from the sale of older products. In certain limited cases, we may not be able to cease production of older products, either due to contractual obligations or for customer relationship reasons and, as a result, may be required to bear a loss on such products for a sustained period of time. If reductions in our production costs fail to keep pace with reductions in market prices for products we sell, our business and results of operations could be materially adversely affected. If our new product development efforts fail to align with the needs of our customers, our business and results of operations could be materially adversely affected.

If we are unable to compete effectively, our competitive position could be weakened relative to our peers, which would have a material adverse effect on our business and results of operations. Our future success depends on many factors, including the development of new technologies and effective commercialization and customer acceptance of our products, and our ability to increase our position in current markets, expand into adjacent and new markets, and optimize operational performance. Products or technologies developed by competitors may render our products or technologies obsolete or noncompetitive. We also may be unable to market and sell our products if they are not competitive on the basis of price, quality, technical performance, features, system compatibility, ease of use, customized design, innovation, availability, delivery timing and reliability. If we fail to compete effectively on developing strategic relationships with customers and customer sales and technical support, our sales and revenue may be materially adversely affected. Competitive pressures may limit our ability to raise prices, and any inability to maintain revenue or raise prices to offset increases in costs could have a significant adverse effect on our gross margin. Our gross margins may fluctuate across time periods and operating segments and could experience volatility or downward pressure due to a variety of factors.…

A significant portion of our sales are made to customers within the automotive industry and the industrial sector, and the demand for our products depends in part on the market conditions in these end-markets. Sales into the automotive and industrial end-markets represented approximately 51% and 28% of our revenue, respectively, for the year ended December 31, 2025. The automotive industry is cyclical and the industrial sector tends to thrive during a time of economic expansion. As a result, our customers in each end-market are sensitive to changes in general economic conditions, inflationary pressure, changes in interest rates, disruptive innovation and end-market preferences, any of which can adversely affect sales of our products and, correspondingly, our results of operations. Changes in demand in these end-markets (such as fluctuations in demand for EVs), or changes that have the potential to disrupt sales activities to customers in these end-markets, can significantly impact our operating results. Additionally, the quantity and price of our products sold to customers in each end-market could decline despite continued growth in such end-markets. Lower sales to customers in either end-market may have a material adverse effect on our business and results of operations.

We had one customer, a distributor, whose revenue accounted for approximately 11% and 10% of the total revenue for the years ended 2025 and 2024, respectively, across all reportable segments. Although we are not dependent on any single customer, a significant disruption in key customer relationships could adversely affect our business. Further, we could experience fluctuations in our customer base or the mix of revenue by customer or end-market, as markets and strategies evolve.

Trends, Risks and Uncertainties Related to Cybersecurity and Data Privacy Disruptions or breaches of our information technology systems could irreparably damage our reputation and our business, expose us to liability and materially adversely affect our results of operations.

Some of these systems are managed or provided by third-party service providers, including certain cloud platform providers. Failure by these third-party service providers to meet their contractual, regulatory and other obligations to us, or our failure to adequately monitor their performance, could result in our inability to achieve expected efficiencies and result in additional costs to correct errors made by such service providers. Depending on the function involved and despite the availability of contractual remedies against these providers, such errors can also lead to business disruption, systems performance degradation, processing inefficiencies or other systems disruptions, the loss or theft of or damage to intellectual property or sensitive data through security breaches or otherwise, incorrect or adverse effects on financial reporting, litigation, claims, legal or regulatory proceedings, inquiries or investigations, fines or penalties, remediation costs, damage to our reputation or have a negative impact on employee morale, all of which can materially adversely affect our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
