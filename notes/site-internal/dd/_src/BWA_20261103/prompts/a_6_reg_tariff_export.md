你是 stock-analyst v20 DD 的證據採集子 agent。標的：BWA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - BWA BorgWarner tariff section 232 2026
  - BorgWarner export control OR entity list Auto Tier 1 / Propulsion + eProducts 2026
  - BWA BorgWarner China tariff OR trade restriction 2026
  - Auto Tier 1 / Propulsion + eProducts tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm｜as_of：2026-02-11
<<<
The Company uses a variety of tactics in an attempt to limit the impact of supply shortages, tariffs, export bans and inflationary pressures. The Company’s global procurement organization works to accelerate cost reductions, purchase from lower cost regions, optimize the supply base, mitigate risk and collaborate on its buying activities. In addition, the Company uses long-term contracts, cost sharing arrangements, design changes, dual sourcing, customer buy programs and limited financial instruments to help control costs. The Company intends to use similar measures in 2026 and beyond. Refer to Note 17, “Financial Instruments,” to the Consolidated Financial Statements in Item 8 of this report for information related to the Company’s hedging activities.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm｜as_of：2026-02-11
<<<
Changes in administrative policy on the part of the U.S. or other countries, including the imposition of or increases in tariffs, changes to existing trade agreements and any resulting changes in international trade relations, may have an adverse effect on us.

In 2025, the U.S. announced significant tariffs on imports from a broad range of countries, including the European Union, Canada, Mexico and China. These tariffs have increased the cost of raw materials and components we purchase, and to the extent the tariffs announced to date or announced in the future become or remain effective and are maintained, these tariffs would likely further increase the cost of raw materials and components we purchase. The imposition of tariffs by the U.S. has resulted in retaliatory tariffs from other countries, including China, which has increased and would continue to increase the cost 21 Table of Contents of products we sell. Additionally, ongoing changes in U.S. and foreign government trade policies, including potential modifications to existing trade agreements and further restrictions on free trade, could introduce additional uncertainty with respect to trade policies and government regulations affecting international trade. Tariffs or retaliatory tariffs announced to date or announced in the future, current trade tensions, any escalation of trade tensions, additional tariffs, retaliatory measures by foreign governments, shifts in U.S.…

In addition to potential increases in customs duties and tariffs in the U.S. and other countries, the United States-Mexico-Canada Agreement ("USMCA") is subject to renewal in 2026. There can be no assurance that the USMCA will be renewed or, if renewed, any newly negotiated terms in the USMCA will not adversely affect our business. Also, China presents unique risks to U.S. automotive manufacturers due to the strain in U.S.-China relations and the level of integration with key components in our global supply chain. It remains unclear what additional actions the current U.S. administration may take with respect to trade issues involving China and other countries.

26 Table of Contents Changes that could impact the legal environment include new legislation, new regulations, new policies, investigations and legal proceedings, and new interpretations of existing legal rules and regulations, in particular, changes in import and export control laws or exchange control laws, additional restrictions on doing business in countries subject to sanctions, additional limitations on greenhouse gas emissions or other matters related to climate change and other changes in laws in countries where we operate or intend to operate.

Rapidly changing industry conditions such as volatile production volumes, including volatility in electric vehicle adoption across different regions; our need to seek price reductions from our suppliers as a result of the substantial pressure we face from OEMs to reduce the prices of our products; credit tightness; changes in foreign currency exchange rates; raw material, commodity, tariffs, transportation, and energy price escalation; drastic changes in consumer preferences; and other factors could adversely affect our supply chain, and sometimes with little advance notice. These conditions could also result in increased commercial disputes and supply interruption risks. In certain instances, it would be difficult and expensive for us to change suppliers that are critical to our business. On occasion, we must provide financial support to distressed suppliers or take other measures to protect our supply lines. We cannot predict with certainty the potential adverse effects these costs might have on our business and results of operations.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm｜as_of：2026-02-11
<<<
Key Trends and Economic Factors Economic Conditions. The Company’s financial performance depends on conditions in the global automotive industry. Automotive and truck production and sales are cyclical and sensitive to general economic conditions and other factors, including interest rates, consumer credit and consumer spending and preferences. Government policies, such as the imposition of, termination of or other changes in tariffs (including retaliatory tariffs), or the commencement or termination of consumer tax incentives, such as EV tax credits and programs to invest in infrastructure, including EV charging stations, may affect consumer preferences. Economic declines or impacts of tariffs that result in a material reduction in automotive or truck production would have an adverse effect on the Company’s sales. The weighted average market production, as estimated by the Company for the year ended December 31, 2025, was approximately flat from the year ended December 31, 2024. Weighted average market production reflects light and commercial vehicle production as reported by S&P Global, weighted for the Company’s geographic exposure, as estimated by the Company.

Commodities and Other Inflationary Impacts. During 2025, prices for commodities showed a lower level of volatility in comparison to what the Company had experienced from the beginning of 2021. The Company expects commodities and other costs to be relatively flat in 2026. However, the Company has experienced impacts from commodity pricing, inflation and tariffs over the last several years. Volatility in these areas and other factors could cause actual costs to be materially higher than expected in 2026.

•Customer recoveries relating to tariffs increased sales by approximately $80 million.

•Tariff expense resulted in a year-over-year increase in cost of sales of approximately $108 million.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
