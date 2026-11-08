你是 stock-analyst v20 DD 的證據採集子 agent。標的：MP。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - MP MP Materials tariff section 232 2026
  - MP Materials export control OR entity list Rare Earth Mining + Magnet Manufacturing 2026
  - MP MP Materials China tariff OR trade restriction 2026
  - Rare Earth Mining + Magnet Manufacturing tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm｜as_of：2026-02-26
<<<
Because our revenue is, and will be for the foreseeable future, from the sale of rare earth products, changes in demand for, and the market price of (including taxes and other tariffs and fees imposed upon) REE and magnet materials could significantly affect our profitability. The Company’s arrangements with the DoW are intended to significantly mitigate the risks of commodity price fluctuations associated with NdPr on our results of operations. In particular, the Company entered into the Price Protection Agreement, which provides a price floor of $110 per kilogram (“kg”) for NdPr products stockpiled, sold to internal affiliates, or sold to third parties. If market prices fall below this threshold, the Company will receive a quarterly payment from the DoW to offset the shortfall. Conversely, once the 10X Facility reaches full production capacity, if the price of NdPr exceeds the threshold, the Company will remit a portion of the upside to the DoW, equal to 30% of the NdPr sales price in excess of $110 per kg. This arrangement allows the Company to sell NdPr at a more stable price, with limited exposure to price declines while retaining upside exposure. This moderates the Company’s exposure to the fluctuations in the NdPr commodity market which the Company has experienced in recent years.

However, while this DoW commitment provides a meaningful measure of certainty with respect to our medium- and longer-term NdPr-related cash flows, our business and financial results remain susceptible to the fluctuations in the demand for, and the realized prices of, REE and magnet materials, which may fluctuate and are affected by numerous factors beyond our control such as interest rates, exchange rates, taxes, inflation or deflation, changes in tariffs or trade restrictions, fluctuation in the relative value of the U.S. dollar against foreign currencies on the world market, shipping and other transportation and logistics costs, global and regional supply and demand for rare earth minerals and products, potential industry trends, such as competitor consolidation or other integration methodologies, and the political and economic conditions of countries that produce and procure REE and magnet materials. A change in the U.S. federal administration introduces uncertainty as to shifts in policies, tariffs, taxes, regulations, and priorities, all of which may have a detrimental impact on demand. Furthermore, supply side factors have a significant influence on price volatility for REE and magnet materials. Supply of REE and magnet materials is dominated by Chinese producers.…

We operate globally and sell our products in countries throughout the world. Significant political, trade, or regulatory developments in the jurisdictions in which we sell our products, including changes in tariff policies by the U.S. administration, export controls, or other trade restrictions, are difficult to predict and may have a material adverse effect on us. Similarly, changes in U.S. federal policy that affect the geopolitical landscape could give rise to circumstances outside our control that could have negative impacts on our business operations. For example, the current U.S. administration has increased tariffs on goods imported into the U.S., particularly from China, Canada, and Mexico. Historically, tariffs have led to increased trade and political tensions, between not only the U.S. and China, but also between the U.S. and other countries in the international community. In response to tariffs, other countries have implemented retaliatory tariffs on U.S. goods. Political tensions as a result of trade policies or other geopolitical dynamics could reduce trade volume, investment, technological exchange, and other economic activities between major international economies, resulting in a material adverse effect on global economic conditions and the stability of global financial markets.…

We are subject to numerous and detailed federal, state and local environmental laws, certifications, regulations, permits, and other legal requirements applicable to the mining and mineral processing industry, including, without limitation, those pertaining to employee health and safety, air emissions, water usage, wastewater and stormwater discharges, air quality standards, GHG emissions, waste management, plant and wildlife protection, handling and disposal of hazardous and radioactive substances and waste, remediation of soil and groundwater contamination, land use, reclamation and restoration of properties, the discharge of materials into the environment, procurement of certain materials used in our operations, and groundwater quality and availability. These requirements may result in significant costs, liabilities and obligations, impose conditions that are difficult to achieve or otherwise delay, limit or prohibit current or planned operations and future growth. Consequently, the modernization and expansion of Mountain Pass and the development of the Independence Facility and the 10X Facility may be delayed, limited or prevented and current operations may be curtailed. Failure to comply with these laws, regulations and permits, including as they evolve, may result in the assessment of administrative, civil and criminal penalties, the issuance of injunctions to limit or cease operations, fines, or the suspension or revocation of permits and other sanctions.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm｜as_of：2026-02-26
<<<
Throughout 2025, China imposed and expanded export controls and restrictions on certain rare earths and related materials, requiring companies to secure special export licenses and obtain Chinese government approval for exports of products containing even small amounts of Chinese-origin rare earths, among other restrictions. While in November 2025 the U.S. reached a trade and economic deal in which China agreed to suspend implementation of the expanded export controls and to suspend retaliatory tariffs and non-tariff measures imposed since March 2025, these developments have led and continue to lead to several market trends, which may or may not be permanent, including volatility and disruptions in global supply chains, shortages of rare earth elements, potential price volatility, and an increased demand for alternative supply chains outside of China, all of which, if sustained, may have a material impact on the demand for our products.

Revenue Rare earth concentrate revenue consists of sales of traditional and roasted rare earth concentrate. For the majority of our sales of rare earth concentrate, the sales price is based on a preliminary market price (net of taxes, tariffs, and certain other agreed charges) per MT, with an adjustment for the ultimate market price of the product realized upon final sale, including the impact of changes in exchange rates.

While the DoW Transactions, together with our supply agreements with Apple and GM, provide a measure of certainty with respect to both near- and longer-term demand for our products and related revenues, there are still significant factors that could negatively impact our liquidity, particularly in the longer-term, many of which remain largely uncertain and dependent on future developments that cannot be accurately predicted at this time, such as: our ability to accelerate our downstream operations and expansion, achieve our business milestones, and perform the obligations under our customer supply agreements, our ability and that of the U.S. Government to perform our respective obligations under the DoW Transaction Agreements, as well as further changes in trade policies in the United States, China or other countries, including the implementation of new tariffs, increases in or reductions of existing tariffs, or the taking of other actions.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
