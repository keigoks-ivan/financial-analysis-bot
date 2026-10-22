你是 stock-analyst v20 DD 的證據採集子 agent。標的：VICR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - VICR Vicor tariff section 232 2026
  - Vicor export control OR entity list 半導體 — 電源管理 / AI 加速器電源 2026
  - VICR Vicor China tariff OR trade restriction 2026
  - 半導體 — 電源管理 / AI 加速器電源 tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm｜as_of：2026-03-02
<<<
Over the course of recent years the supply picture for the semiconductor industry generally improved and we have reduced quoted lead time to 22 – 28 weeks, depending on product family. In the second half of 2025, we added a 10% tariff surcharge on our products to cover the estimated cost of tariffs introduced during the year.

For 2025, exports to China and Hong Kong were approximately $48,347,000, representing approximately 11.9% of total net revenues and an approximately 7.0% increase compared to the 2024 total net revenues of approximately $45,199,000. Current exports to China and Hong Kong are heavily oriented toward Brick Products for industrial and rail applications, as well as certain aerospace and defense electronics applications permitted under U.S. export control regulations (our products are designated EAR99 commodities under the Export Administration Regulations of the U.S. Department of Commerce and are not subject to export licenses).

To date, we have not experienced material delays or reduced raw material availability as a result of trade disputes between the U.S. and China, including the imposition in 2018 of import tariffs under the provisions of Section 301 of the Trade Act of 1974 (19 U.S.C. § 2411) (“Section 301 Tariffs”) on certain Chinese goods imported into the United States. For the year ended December 31, 2025, costs associated with tariffs totaled approximately $7,375,000, an increase of 76.1% compared to $4,189,000 in costs incurred for the year ended December 31, 2024. For the year ended December 31, 2023, costs associated with tariffs totaled approximately $7,985,000. We continue to assess the impact of these costs and are actively evaluating alternative sources of raw materials. We also have filed “duty drawback” applications with U.S. Customs and Border Protection for the recovery of tariffs paid on raw materials used to produce products we subsequently exported. We recovered $907,000, $1,669,000 and $6,954,000 for the years ended December 31, 2025, 2024 and 2023, respectively, however, we are not able to estimate the amount or timing of any additional recoveries, and there can be no assurance that there will be any additional recoveries. To mitigate the impact of tariffs, we implemented a 10% tariff surcharge on our products in July 2025.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm｜as_of：2026-03-02
<<<
•the timing of new product introductions or other competitive actions (e.g., product price reductions) by our competitors; •the ability to hire, retain, and motivate qualified employees to meet the demands of our customers; •intellectual property disputes including disputes relating to the licensing of our intellectual property; •our ability to license our intellectual property; •litigation-related costs, which may be significant; •adverse economic conditions in the U.S. and those foreign countries in which we operate, as well as our ability to respond to unanticipated developments, such as the imposition of tariffs or trade restrictions; •adverse budgetary conditions within the U.S. government, particularly the Department of Defense, which continue to influence spending on current and anticipated programs into which we sell or anticipate to sell our products; •costs related to compliance with increasing worldwide governance, quality, environmental, and other regulations; •costs and consequences of disruption by third-parties of our global computer network and related resources; and •the effects of events outside of our control, including public health emergencies, natural disasters, terrorist activities, political risks, international conflicts, information security breaches, communication interruptions, and other force majeure.

To date, we have not experienced material delays or reduced raw material availability as a result of trade disputes between the U.S. and China, including the imposition in 2018 of import tariffs under the provisions of Section 301 of the Trade Act of 1974 (19 U.S.C. § 2411) (“Section 301 Tariffs”) on certain Chinese goods imported into the United States. However, the costs of Section 301 Tariffs have had a material impact on our profitability. For the year ended December 31, 2025, Section 301 Tariffs totaled approximately $7,375,000, an increase of 76.1% compared to $4,189,000 incurred for 2024. For the year ended December 31, 2023, costs associated with tariffs totaled approximately $7,985,000. For 2025, 2024 and 2023, Section 301 Tariffs totaled approximately 1.8%, 1.2% and 2.0%, respectively, of total annual net revenues, representing a reduction in our gross profit margin as a percentage of total annual net revenues.

We have filed “duty drawback” applications with U.S. Customs and Border Protection for the recovery of Section 301 Tariffs paid on raw materials and components used to produce products we subsequently exported. We recovered $907,000 for the year ended December 31, 2025, however, we are not able to estimate the amount or timing of any additional recoveries, and there can be no assurance that there will be any additional recoveries.

Uncertain macroeconomic conditions, extended trade disputes, an evolving and unpredictable tariff environment, export controls, and the relative strength of the U.S. Dollar may reduce end-demand for our customers’ products and, in turn, their purchases of our products, thereby reducing our revenues and earnings. In addition, such adverse conditions may, among other things, result in increased price competition for our products, notably in Brick Product categories, increased risk of excess and obsolete inventories, increased risk in the collectability of our accounts receivable from our customers, increased risk in potential reserves for doubtful accounts and write-offs of accounts receivable, and higher operating costs as a percentage of revenues. We cannot predict the extent and/or impact of the current trade and tariff disputes between the United States and other countries, which adds to the uncertainty and risks associated with our business.

Government actions, including trade protection and national security policies of U.S. and foreign government bodies, such as tariffs, import or export regulations, including deemed export restrictions, trade and economic sanctions, decrees, quotas or other trade barriers and restrictions could affect our ability or the ability of our customers and end users to sell products in certain countries and thereby have a material adverse effect on our business, revenue and results of operations. In recent years, the U.S. government has continued to expand the number of foreign entities on the Entity List (a restricted party list that imposes additional licensing requirements on shipments to listed parties). These export controls are, in part, intended to restrict the ability of the People’s Republic of China to obtain advanced computing chips, develop and maintain supercomputers, and manufacture advanced semiconductors. The implementation, interpretation and impact on our business of these rules and other regulatory actions taken by the U.S. government is uncertain and evolving, and these rules, other regulatory actions or changes, and other actions taken by the governments of either the U.S. or China, or both, that have occurred and may continue to occur in the future could materially and adversely affect our business, revenue and results of operations.

While we have policies and procedures in place to ensure compliance with sanctions and trade restrictions and other applicable laws, our employees, contractors, partners, and agents may take actions in violation of such policies and applicable law, for which we may be ultimately held responsible. Intentional and unintentional violations of these laws can result in fines and penalties; criminal sanctions against us, our officers, or our employees; prohibitions on the conduct of our business; and damage to our reputation, any of which could have a material and adverse impact on our business, operating results and financial condition.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm｜as_of：2026-03-02
<<<
•Gross margin for the year ended December 31, 2025 increased $75,431,000, or 41.0%, to $259,429,000 from $183,998,000 for the year ended December 31, 2024. Gross margin, as a percentage of total net revenues and patent litigation settlement, increased to 57.3% for the year ended December 31, 2025, as compared to 51.2% for the year ended December 31, 2024. The increase in gross margin dollars and gross margin percentage was primarily attributable to the $45,000,000 patent litigation settlement payment received by the Company in the second quarter of 2025 and the favorable impact from higher sales volume and improved sales mix on that revenue, including royalty revenue, when compared to 2024, offset by the unfavorable impact of production inefficiencies including an increase in freight-in and tariff spending of $3,949,000 (net of approximately $907,000 in duty drawback recovery in 2025 and $1,669,000 in duty drawback recovery in 2024 of previously paid tariffs).

Gross margin for the year ended December 31, 2025 increased $75,431,000, or 41.0%, to $259,429,000 from $183,998,000 for the year ended December 31, 2024. Gross margin, as a percentage of total net revenues and patent litigation settlement, increased to 57.3% for the year ended December 31, 2025, as compared to 51.2% for the year ended December 31, 2024. The increase in gross margin dollars and gross margin percentage was primarily attributable to the $45,000,000 patent litigation settlement payment received by the Company in the second quarter of 2025 and the favorable impact from higher sales volume and improved sales mix on that revenue, including royalty revenue, when compared to 2024, offset by the unfavorable impact of production inefficiencies including an increase in freight-in and tariff spending of $3,949,000 (net of approximately $907,000 in duty drawback recovery in 2025 and $1,669,000 in duty drawback recovery in 2024 of previously paid tariffs).
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
