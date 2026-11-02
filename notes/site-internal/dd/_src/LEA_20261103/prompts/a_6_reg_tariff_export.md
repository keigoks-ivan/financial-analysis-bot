你是 stock-analyst v20 DD 的證據採集子 agent。標的：LEA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - LEA Lear tariff section 232 2026
  - Lear export control OR entity list Auto Parts 2026
  - LEA Lear China tariff OR trade restriction 2026
  - Auto Parts tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
Due to the interconnectedness of the global economy, policy changes in one area of the world can have an immediate and material impact on markets around the world. Since his inauguration in January 2025, U.S. President Donald J. Trump has announced various tariffs that impact industries around the world, including the automotive industry. As of the date of this Report, many of the tariffs announced, implemented or threatened by the current U.S. administration apply to (a) the countries in which we do business or from which we purchase, either directly or indirectly, materials or components, including China, Mexico and Canada, and (b) the materials or components that we purchase, either directly or indirectly, or produce, including steel, aluminum and automobile parts, among others, and therefore could adversely impact our business by increasing our operating costs, requiring us to incur significant costs to transition to alternative suppliers if our mitigation efforts are unsuccessful, or negatively impacting our customers' production. In addition to tariffs, the U.S. and foreign governments have implemented sanctions, export controls and other trade restrictions that impact industries around the world, including the automotive industry.

For a description of risks related to macroeconomic events and tariffs, sanctions, export controls and other trade restrictions, see Item 1A, "Risk Factors," included in this Report.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
•International trade policies, such as tariffs, sanctions, export controls and other trade restrictions, could adversely affect our financial performance.

Since his inauguration in January 2025, U.S. President Donald J. Trump has announced various tariffs that impact industries around the world, including the automotive industry. As of the date of this Report, many of the tariffs announced, implemented or threatened by the current U.S. administration apply to (a) the countries in which we do business or from which we purchase, either directly or indirectly, materials or components, including China, Mexico and Canada, and (b) the materials or components that we purchase, either directly or indirectly, or produce, including steel, aluminum and automobile parts, among others, and therefore could adversely impact our business by increasing our operating costs, requiring us to incur significant costs to transition to alternative suppliers if our mitigation efforts are unsuccessful, or negatively impacting our customers' production. In addition to tariffs, the U.S. and foreign governments have implemented sanctions, export controls and other trade restrictions that impact industries around the world, including the automotive industry.

The policies relating to these tariffs continue to evolve, including with respect to the type of tariff or export control, the tariff rates, the countries, components and materials to which such tariffs apply, and the existence and applicability of any exemptions. The actual impacts of tariffs and other trade restrictions on our business, financial condition and results of operations continue to be subject to a number of factors that are not yet known or are subject to change, including the effect such tariffs and restrictions may have on consumer demand and global automotive production volumes, the duration of such tariffs and restrictions, future changes in the amounts and scope of tariffs, the potential withdrawal of such tariffs and restrictions in whole or in part, the scope and effective date of any exemptions to such tariffs or restrictions, any modification to existing exemptions to such tariffs or restrictions, countermeasures that target countries may take in 22 Table of Contents response to such tariffs and restrictions, the impact such tariffs and restrictions may have on our customers and our supply chain, and whether and to what extent such tariffs are impacted by judicial review.…

Further, the U.S. and other governments could impose additional sanctions, export controls or other trade restrictions that could restrict us from doing business directly or indirectly in or with certain countries or parties, which could include affiliates (e.g., China has imposed tariffs and taken other retaliatory actions). The current trade environment could impact the status of other trade agreements between the United States and countries other than Canada and Mexico, including, without limitation, the Dominican Republic-Central America-United States Free Trade Agreement. Any of the above factors could impact our supply chain, as well as our operations, and adversely affect our financial condition and operating results.

We have substantial international operations, with manufacturing and distribution facilities in many foreign countries, including Mexico and countries in Africa, Asia, Central and South America, and Europe. Some of the markets in which we do business may have volatile economic and/or political environments. This may expose us to heightened risks as a result of economic, geopolitical or other events, including: –exposure to local economic conditions; –political, economic and civil instability and uncertainty (including acts of terrorism, civil unrest, drug cartel-related and other forms of violence); –international disputes, including war, military conflict, security or law enforcement operations, and geopolitical unrest, including due to threatened uses of force; –labor scarcity, labor unrest and governmental regulations impacting labor supply; –expropriation, governmental takeover and nationalization; –currency exchange rate fluctuations, discrepancies in commodity pricing between different exchanges, currency controls and the ability to economically hedge currencies; –withholding and other taxes on remittances and other payments by subsidiaries; –investment restrictions or requirements; –repatriation restrictions or requirements; –trade wars, tariffs, sanctions, export controls or other trade restrictions; –concerns about human rights, working conditions and other labor rights and conditions and the environmental impact in foreign countries where our products are produced and raw materials and/or components are sourced, as well as changing labor, environmental and other laws in these countries; –pandemic illness and limited access to vaccines; –…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
38 Table of Contents Due to the interconnectedness of the global economy, policy changes in one area of the world can have an immediate and material impact on markets around the world. Since his inauguration in January 2025, U.S. President Donald J. Trump has announced various tariffs that impact industries around the world, including the automotive industry. As of the date of this Report, many of the tariffs announced, implemented or threatened by the current U.S. administration apply to (a) the countries in which we do business or from which we purchase, either directly or indirectly, materials or components, including China, Mexico and Canada, and (b) the materials or components that we purchase, either directly or indirectly, or produce, including steel, aluminum and automobile parts, among others, and therefore could adversely impact our business by increasing our operating costs, requiring us to incur significant costs to transition to alternative suppliers if our mitigation efforts are unsuccessful, or negatively impacting our customers' production. In addition to tariffs, the U.S. and foreign governments have implemented sanctions, export controls and other trade restrictions that impact industries around the world, including the automotive industry.

Although U.S. tariffs did not have a material impact on our operating performance in 2025, the policies relating to these tariffs continue to evolve, including with respect to the type of tariff or export control, the tariff rates, the countries, components and materials to which such tariffs apply, and the existence and applicability of any exemptions. The actual impacts of tariffs and other trade restrictions on our business, financial condition and results of operations continue to be subject to a number of factors that are not yet known or are subject to change, including the effect such tariffs and restrictions may have on consumer demand and global automotive production volumes, the duration of such tariffs and restrictions, future changes in the amounts and scope of tariffs, the potential withdrawal of such tariffs and restrictions in whole or in part, the scope and effective date of any exemptions to such tariffs or restrictions, any modification to existing exemptions to such tariffs or restrictions, countermeasures that target countries may take in response to such tariffs and restrictions, the impact such tariffs and restrictions may have on our customers and our supply chain, and whether and to what extent such tariffs are impacted by judicial review.…

Further, the U.S. and other governments could impose additional sanctions, export controls or other trade restrictions that could restrict us from doing business directly or indirectly in or with certain countries or parties, which could include affiliates (e.g., China has imposed tariffs and taken other retaliatory actions). The current trade environment could impact the status of other trade agreements between the United States and countries other than Canada and Mexico, including, without limitation, the Dominican Republic-Central America-United States Free Trade Agreement. Any of the above factors could impact our supply chain, as well as our operations, and adversely affect our financial condition and operating results.

For a description of risks related to macroeconomic events and tariffs, sanctions, export controls and other trade restrictions, see Part I — Item 1A, "Risk Factors," included in this Report.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
