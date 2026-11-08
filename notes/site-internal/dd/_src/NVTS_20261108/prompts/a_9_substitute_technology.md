你是 stock-analyst v20 DD 的證據採集子 agent。標的：NVTS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Navitas Semiconductor product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - NVTS Navitas Semiconductor technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm｜as_of：2026-02-27
<<<
•If we fail to accurately anticipate and respond to rapid technological change in the industries in which we operate or adopt to emerging industry standards, our ability to attract and retain end customers could be impaired and our competitive position could be harmed.

•Our ability to accurately predict future revenues and profits is inherently subject to significant uncertainties, particularly as our products are designed to disrupt existing markets and create new or emerging markets.

Risks Related to Owning Our Common Stock •Our business and operations could be impacted by stockholder activism, which could negatively affect our business and cause disruptions.

16 TABLE OF CONTENTS Furthermore, as we reduce our focus on the mobile and consumer markets, we may lose existing customer relationships and brand visibility in those sectors. Mobile and consumer revenue may decline faster than we can establish revenue growth in high power markets. The markets for AI data centers, energy and grid infrastructure, performance computing and industrial electrification are also subject to cycles of over-investment, component oversupply, and technological disruption, which can lead to sharp fluctuations in demand and variability in results. If our transition does not yield expected revenue growth or margin improvement, or if emerging competitors capture key design opportunities, our business, financial performance, and long-term growth prospects could be materially and adversely affected.

If we fail to accurately anticipate and respond to rapid technological change in the industries in which we operate or adapt to emerging industry standards, our ability to attract and retain end customers could be impaired and our competitive position could be harmed.

We operate in industries characterized by rapidly changing technologies as well as technological obsolescence. This is especially true as we prioritize high-power markets. The introduction of new products by our competitors, the delay or cancellation of any of our end customers’ product offerings for which our solutions are designed, the market acceptance of products based on new or alternative technologies, or the emergence of new industry standards could render our existing or future products uncompetitive, obsolete, and otherwise unmarketable. Our failure to anticipate or timely develop new or enhanced products or technologies in response to changing or emerging market demand, whether due to technological shifts or otherwise, could result in the loss of end customers and decreased revenue and have an adverse effect on our business, financial condition, and results of operations.

We have historically relied on a single third-party manufacturer (wafer foundry) to fabricate our GaN products, and on a separate, single wafer foundry to fabricate our SiC products. We also purchase a number of key materials and components used in the manufacture of our products from single or limited sources. As a result, any disruption in the supply to or from these third parties (including ceasing or suspending operations entirely), may require us to transfer manufacturing processes to a new location or facility and we may not be able to do so in a timely manner. Our success is dependent upon our ability to successfully partner with our suppliers and our ability to produce wafers with competitive performance attributes and prices, including smaller process geometries. As we attract new customers in high power markets, those customers’ quality and capacity requirements may force us to work with new or additional suppliers and there is no guarantee that we will successfully transition or onboard such new suppliers without excess delay, cost or disruption. Qualifying alternative manufacturing partners or relocating production involves significant time, cost, and technical risk and may not be feasible in the short term. Similarly, many of our suppliers serve multiple customers and in the event of a supply constraint, those other customers may receive preferential priority or allocation.…

For example, historically, we have relied on TSMC as our sole supplier of GaN wafers, a key component in our product offerings. On July 1, 2025, TSMC announced its intention to cease GaN production in July 2027. We have taken proactive steps to mitigate this risk, including committing to purchase buffer inventory from TSMC, expanding our collaboration 20 TABLE OF CONTENTS with Powerchip Semiconductor Manufacturing Corporation and in November 2025, we announced a long-term strategic partnership with GlobalFoundries to develop and deliver advanced GaN solutions for critical applications in high power markets, including AI datacenters, energy and grid infrastructure, performance computing and industrial electrification. Despite these mitigation steps, there is no assurance that we will be able to successfully source sufficient quality or volume of GaN wafers at a cost or on a timeline that meets our requirements. We may not be able to purchase a sufficient quantity of buffer inventory from TSMC, or we may incur substantial costs in doing so and end with excess inventory that must be scrapped. Any delays or disruptions in qualifying or ramping production with Powerchip or GlobalFoundries, or other alternative suppliers, could negatively impact our ability to fulfill customer orders, lead to increased costs, or cause a loss of revenue and market share.…

Supply disruptions may also occur due to shortages in critical materials or components. We have encountered shortages and delays in obtaining components and materials and may encounter additional shortages and delays in the future. Because our products are complex, it is frequently difficult or impossible to substitute one type of material with another. Further, a failure by suppliers to deliver requirements could result in disruptions to our third party manufacturing operations. Our business, financial condition and results of operations could be harmed if we are unable to obtain adequate supplies of materials in a timely manner or if there are significant increases in the costs of materials.

•government restrictions on the export of certain semiconductor products, technologies, or manufacturing processes due to national security concerns, or the imposition of sanctions or licensing requirements on the sale of our semiconductor products to customers located abroad; •actual or threatened military conflicts in countries or regions where we do not do business or have manufacturing partners, such as the military conflict between Russia and Ukraine, unrest in the Middle East and recent events in Venezuela, may increase the likelihood of supply interruptions or disruptions in countries or regions where we do business or in which our manufacturing partners have facilities. Such interruptions or disruptions may make it harder for us to find favorable pricing and reliable sources for materials and services we need to make our products, putting upward pressure on our costs; •unexpected changes in, or impositions of, legislative or regulatory requirements, including changes in tax laws; •restrictions on cross-border investment, including enhanced oversight by the Committee on Foreign Investment in the United States (“CFIUS”) or the foreign equivalent thereof, and substantial restrictions on investment from China as well as recently introduced restrictions on investments by U.S.…

•differing definitions of “country of origin” resulting in stacked or inconsistent treatment under multi-jurisdiction tariff or import regimes or increased costs and supply chain adjustments for semiconductor companies due to recent U.S. tariffs on Chinese imports; •disruptions of capital and trading markets and currency fluctuations; and •global pandemics, natural disasters, political instability, labor disruptions and other geopolitical and macroeconomic factors that can disrupt global supply chains or impact global economic activity..

In the United States, certain investments that involve the acquisition of, or investment in, a U.S. business by an investor subject to foreign control (a “foreign person”) may be subject to review and approval by CFIUS. Whether CFIUS has jurisdiction to review an acquisition or investment transaction depends on, among other factors, the nature and structure of the transaction, including the level of beneficial ownership interest and the nature of any information or governance rights involved, and the nature of the technology possessed by the U.S. business. For example, investments that result in “control” of a U.S. business, which may include governance rights falling well short of majority control, by a foreign person are always subject to CFIUS jurisdiction. CFIUS’s jurisdiction also extends to investments that do not result in control of a U.S. business by a foreign person, if they afford foreign investors with information or governance rights in a U.S. business that has a nexus to, among other things, “critical technologies.” Transactions involving companies that develop, produce, or test critical technologies may be subject to mandatory filing requirements. In addition, U.S. regulatory initiatives over the past several years have classified certain semiconductor technologies as “critical to national security,” including compound semiconductors and wide bandgap semiconductors. Both GaN and SiC are compound semiconductors and wide bandgap semiconductors.…

In addition, U.S. laws and regulations and sanctions, or threat of sanctions, that could limit and restrict the export of some of our products and services to end customers, may also encourage end customers to develop their own solutions to replace 26 TABLE OF CONTENTS our products, or seek to obtain a greater supply of similar or substitute products from competitors that are not subject to these restrictions, which could materially and adversely affect our business, financial condition and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVTS_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
