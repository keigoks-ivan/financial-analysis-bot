你是 stock-analyst v20 DD 的證據採集子 agent。標的：PH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - PH Parker-Hannifin tariff section 232 2026
  - Parker-Hannifin export control OR entity list Specialty Industrial Machinery 2026
  - PH Parker-Hannifin China tariff OR trade restriction 2026
  - Specialty Industrial Machinery tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-21）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm｜as_of：2026-08-21
<<<
Our business is sensitive to global macro-economic conditions. Macroeconomic downturns may have an adverse effect on our business, results of operations and financial condition, as well as our distributors, customers and suppliers, and on activity in many of the industries and markets we serve. Among the economic factors which may have such an effect are manufacturing and other end-market activity, currency exchange rates, air travel trends, difficulties entering new markets, tariffs and governmental trade and monetary policies, changes in government spending priorities (including defense and infrastructure spending), global pandemics, and general economic conditions such as inflation, deflation, interest rates and credit availability. These factors may, among other things, negatively impact our level of purchases, capital expenditures, and creditworthiness, as well as our distributors, customers and suppliers, and, therefore, the Company’s revenues, operating profits, margins, and order rates.

Our net sales attributable to selling locations outside of the United States were approximately 36% in each of 2026, 2025 and 2024. In addition, many of our customers, manufacturing operations and suppliers are located outside the United States. The Company expects net sales from non-U.S. markets to continue to represent a significant portion of its total net sales. Furthermore, completed and pending acquisitions may increase our international exposure and the complexity of managing operations across multiple jurisdictions. Our non-U.S. operations are subject to risks in addition to those facing our domestic operations, including: •fluctuations in currency exchange rates and/or changes in monetary policy; •limitations on ownership and on repatriation of earnings; •transportation delays and other supply chain disruptions; •political, social and economic instability and disruptions, including armed conflicts; •the imposition of duties and tariffs and other trade barriers; •government import and export controls, embargoes, sanctions or trade restrictions, including possible restrictions on trade and/or obstacles to conducting business in China; •labor unrest and current and changing regulatory environments; •difficulties in implementing restructuring actions on a timely basis; •difficulties in staffing and managing multi-national operations; •limitations on our ability to enforce legal rights and remedies; •public health crises, including pandemics; •the potential for nationalization of enterprises; and •potentially adverse tax consequences.

For example, the global nature of our business and our operations exposes us to political, economic, and other conditions in foreign countries and regions, such as the uncertainty about the future relationship between the U.S. and China, including with respect to trade policies, treaties, government regulations and tariffs, and the potential 9 Table of Contents renegotiation of the United States-Mexico-Canada Agreement. Any increased trade barriers or restrictions on global trade, including trade with China or among North American trading partners, could adversely impact our business, results of operations or financial condition.

Our supply of raw materials could be interrupted for a variety of reasons, including availability and pricing. Furthermore, changes to United States and other countries' tariff and import/export regulations have in the past and may in the future have a negative impact on the availability and pricing of raw materials. Prices for raw materials necessary for production have fluctuated significantly in the past and significant increases could adversely affect our results of operations and profit margins. Our efforts to manage these fluctuations by, among other things, passing along price increases to our customers, may be subject to a time delay between raw material prices increasing and our ability to increase the price of our products, or we may be unable to increase the prices of our products due to pricing pressure, contract terms (including fixed-price contracts) or other factors. Any such inability to manage fluctuations could adversely impact our results of operations and cash flows.

U.S. Government contractors are subject to extensive legal and regulatory requirements, including the International Traffic in Arms Regulations (“ITAR”), the Export Administration Regulations, the U.S. Foreign Corrupt Practices Act and evolving cybersecurity requirements such as the Cybersecurity Maturity Model Certification framework. From time to time, agencies of the U.S. Government investigate whether we have been and are operating in accordance with these and/or applicable contractual requirements. Changes in export control lists or the scope of ITAR-controlled items may require us to modify our operations, obtain additional licenses or restrict certain business activities. If the Company were charged with wrongdoing as a result of any such investigation, or failed to achieve or maintain required cybersecurity certifications, it could be suspended or debarred from bidding on or receiving awards of new government contracts, subject to fines or penalties associated with contract non-compliance or resulting from such investigations or lose its export privileges, which could have a material adverse effect on our results of operations and financial condition.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-21）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm｜as_of：2026-08-21
<<<
21 Table of Contents Over the long term, the extent to which our business and results of operations will be impacted by global economic and political uncertainty and geopolitical risks depends on future developments that remain uncertain. In particular, the tariff environment continues to be dynamic. In February 2026, the U.S. Supreme Court ruled that tariffs imposed under the International Emergency Economic Powers Act ("IEEPA") on goods imported into the U.S. were unauthorized. During the fourth quarter of fiscal 2026, the Company recognized a reduction to cost of sales of $84 million related to IEEPA tariff refunds received from the U.S. government. We have applied for additional refunds under the same program, though for lesser amounts. No receivable has been recorded for these additional refunds as the amount and timing remain uncertain. We will continue to monitor the global environment and manage our business with the goal to minimize unfavorable impacts on operations and financial results.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
