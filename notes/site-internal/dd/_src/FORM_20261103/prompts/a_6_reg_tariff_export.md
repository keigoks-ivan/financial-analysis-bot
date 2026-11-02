你是 stock-analyst v20 DD 的證據採集子 agent。標的：FORM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - FORM FormFactor tariff section 232 2026
  - FormFactor export control OR entity list Semiconductor Equipment & Materials 2026
  - FORM FormFactor China tariff OR trade restriction 2026
  - Semiconductor Equipment & Materials tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
Import and Export Control We manufacture, market and sell our products both inside and outside the U.S. Certain products are subject to export control regulations. Failure to comply with these laws could result in sanctions by the U.S. or other governments, including substantial monetary penalties, denial of import, export or other privileges, and debarment from government contracts. For example, 8 approximately 7% of our fiscal 2025 revenue and 14% of our fiscal 2024 revenue was derived from sales to customers in China, which was one of the regions subject to the expanded export license requirements imposed by the United States government.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
The semiconductor industry has historically been cyclical and is characterized by wide fluctuations in product supply and demand. From time to time, this industry has experienced significant downturns, often in connection with, or in anticipation of, maturing product and technology cycles, excess inventories, and declines in general economic conditions. The global economic and semiconductor downturns have caused and may in the future cause our operating results to decline dramatically from one period to the next. Global economic stability can be negatively affected by a variety of factors and interrelationships, including the impacts of epidemics and pandemics, military conflicts or regional tensions, climate change, trade tensions, barriers and conflicts (such as U.S.-China trade restrictions) and other factors acting alone or in combination. Some of these factors can also have a more direct adverse impact upon our operations to varying degrees. Our business depends heavily upon the development 13 and manufacture of new semiconductors, the rate at which semiconductor manufacturers make transitions to smaller nanometer technology nodes and implement tooling cycles, the volume of production by semiconductor manufacturers, and the overall financial strength of our customers, which, in turn, depend upon the current and anticipated market demand for semiconductors and products that use semiconductors, such as servers, artificial intelligence, personal computers, automobiles and cell phones.…

We obtain some of the components and materials used in our products, such as printed circuit board assemblies, plating materials and ceramic substrates, from a sole source or a limited group of suppliers, and in some cases alternative sources are not currently available. Because we rely on purchase orders rather than long-term contracts with the majority of our suppliers, we cannot guarantee our ability to obtain components and materials in the long term. A sole or limited source supplier could increase prices, which could lead to a decline in our gross profit. Our dependence upon sole or limited source suppliers exposes us to several other risks, including inability to obtain an adequate supply of materials, late deliveries, poor component quality, and business disruptions while we seek to identify and qualify alternative suppliers. This could be exacerbated by certain events outside the control of either the supplier or us, such as global, regional or national health crises, armed conflicts, increased tariffs and trade barriers, regional tensions or other adverse global, regional and national events. The occurrence of any of these risks could adversely impact our business, results of operations and financial condition.

A variety of factors, including natural disasters, health crises, climate change, military conflicts and other geopolitical events, may adversely affect national, regional and global economies and financial markets. Recent political changes have created an environment of tension and uncertainty in economic matters, particularly with regard to tariffs and international trade. Any such adverse events may result in global, regional or national economic slowdowns or other economic disruptions or downturns. Such disruption or downturns could curtail or delay spending by businesses and consumers which may ultimately result in reductions in the demand for our products, greater volatility in demand and supply conditions and other adverse impacts. For example, any deterioration in the relations between Taiwan and China, and other factors affecting military, political or economic conditions in Taiwan or elsewhere in Asia, could adversely impact our suppliers, manufacturers and customers with operations located in the region, which could disrupt our business operations, affect demand for our products or increase our costs, negatively impacting our revenues, gross margins, and overall results of operations. Additionally, these events may also increase uncertainty in global credit and financial markets.…

Our operations, including data processing and transfer activities, are subject to the evolving geopolitical landscape and the increasingly stringent regulatory environment in jurisdictions where we operate or from which we process data. Specifically, escalating trade tensions and policy divergence between the U.S. and China, including restrictions on technology transfers, cross-border data transfers, export controls, and investment limitations, could impact our ability to conduct business, access critical technologies, or operate effectively in the Chinese market. The sale of our products as a percentage of our revenues to customers inside of China represented 7%, 14%, and 14% of total revenue for fiscal 2025, 2024 and 2023, respectively.

18 Any of these factors could harm our existing international operations, impair our ability to continue expanding into international markets or materially adversely affect our operating results. Political developments in the United States and elsewhere may increase the risks and uncertainties associated with conducting international business, including the possibilities of greater tariffs and other trade barriers in the regions where we conduct business. In fiscal years 2025, 2024 and 2023, we observed a continuing trend of increasing risks and challenges in the conduct of our international business activities, including expanded tariffs and other trade barriers affecting the United States and China, and trade tensions and conflicts (including proposed tariffs) between the United States and other countries. Additionally, we are required to comply with foreign import and export requirements, customs and value added tax standards that can be unclear or complex. Our failure to meet these requirements and standards could negatively impact our business operations.

Sales of our products to customers outside of the United States represent a significant part of our past and anticipated revenues. In recent months, markets have reacted adversely to geopolitical tensions, volatility and uncertainty in international trade policies, substantially stemming from the U.S. government’s implementation of rapidly evolving changes to trade policies, including new and expanded tariffs and changes in U.S. participation in multilateral trade agreements resulting in reciprocal tariffs and other trade restrictions imposed and modified, and selective tariff exemptions being granted, often suddenly and with little notice, impacting a broad range of raw materials and trade globally.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
Gross profit and gross margin by segment were as follows (dollars in thousands): Fiscal 2025 Probe Cards Systems Corporate and Other Total Gross profit $ 258,500 $ 61,553 $ (11,202) $ 308,851 Gross margin 40.5 % 41.8 % 39.3 % Fiscal 2024 Probe Cards Systems Corporate and Other Total Gross profit $ 259,007 $ 59,511 $ (10,595) $ 307,923 Gross margin 41.4 % 43.2 % 40.3 % Fiscal 2023 Probe Cards Systems Corporate and Other Total Gross profit $ 185,392 $ 84,735 $ (11,547) $ 258,580 Gross margin 37.2 % 51.3 % 39.0 % Probe Cards—Gross profit and gross margin in the Probe Cards segment decreased in fiscal 2025 compared to fiscal 2024, despite the record revenue levels primarily due to higher manufacturing costs, which included increased costs for tariffs, partially offset by a favorable product mix and favorable factory utilization with the increased volumes. For fiscal 2025 compared to fiscal 2024, DRAM revenue was up from 36.3% of Probe Card sales to 38.8% of Probe Card sales, and Foundry & Logic revenue was down from 60.9% of Probe Card sales to 58.0% of Probe Card sales. In general, our DRAM products have lower margins than our Foundry & Logic products, although there is a significant intra-market variance depending on customer and device.

Overall—Gross profit and gross margin fluctuate with revenue levels, product mix, selling prices, factory loading and material costs. For fiscal 2025 compared to fiscal 2024, gross profit increased and gross margins decreased as a result of greater revenues and a favorable product mix, that was offset by higher manufacturing costs, which included a 1.4% gross margin impact from increased costs for tariffs. Despite the impact of tariffs, third and fourth quarters of fiscal 2025 have shown meaningful improvement in gross margins compared to the first half of fiscal 2025 and second half of fiscal 2024.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
