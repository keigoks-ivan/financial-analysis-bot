你是 stock-analyst v20 DD 的證據採集子 agent。標的：GM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - GM General Motors market share gaining OR losing 2026
  - General Motors new entrant OR displace threat Auto Manufacturers 2026
  - GM competitor design win 2026
  - General Motors vs Auto Manufacturers peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
GM has made significant investments to build a broad portfolio of electric vehicles (EVs) including establishing manufacturing and supply chain capacity for EVs, batteries, and components, in North America. Our EV portfolio has achieved significant market growth with strong positioning in the U.S. market. Our New Energy Vehicles (NEVs) in China have contributed to the turnaround in sales and business performance in China. EVs like the Chevrolet Equinox EV, Cadillac LYRIQ, Cadillac ESCALADE IQ, and the GMC Sierra EV have brought new customers to our brands and helped increase our EV market share.

Competitive Position and Vehicle Sales The principal factors that determine consumer vehicle preferences in the markets in which we operate include overall vehicle design, price, quality, available options, safety, reliability, fuel economy or range, and functionality. Market leadership in individual countries in which we compete varies widely.

We present both wholesale and total vehicle sales data to assist in the analysis of our revenue and market share. Wholesale vehicle sales data consists of sales to GM's dealers and distributors, as well as sales to the U.S. Government, and excludes vehicles sold by our joint ventures. Wholesale vehicle sales data correlates to our revenue recognized from the sale of vehicles, which is the largest component of Automotive net sales and revenue. In the year ended December 31, 2025, 27.5% of our wholesale vehicle sales volume was generated outside the U.S. The following table summarizes wholesale vehicle sales by our Automotive operations (vehicles in thousands): Years Ended December 31, 2025 2024 2023 GMNA 3,296 86.8 % 3,464 86.4 % 3,147 83.5 % GMI 503 13.2 % 547 13.6 % 621 16.5 % Total 3,799 100.0 % 4,010 100.0 % 3,768 100.0 % Total vehicle sales data represents: (1) retail sales (i.e., sales to consumers who purchase new vehicles from dealers or distributors); (2) fleet sales (i.e., sales to large and small businesses, governments, and daily rental car companies); and (3) certain vehicles used by dealers in their business, including but not limited to courtesy transportation vehicles previously used by dealers that were sold to the end consumer.…

(b)Cuba, Iran, North Korea, and Sudan have been subject to broad economic sanctions. Accordingly, these countries are excluded from industry sales data and corresponding calculation of market share.

3 Table of Contents GENERAL MOTORS COMPANY AND SUBSIDIARIES As discussed above, total vehicle sales and market share data provided in the table above includes fleet vehicles. We sell vehicles directly or through our dealer network to fleet customers, including daily rental car companies, commercial fleet customers, leasing companies, and governments. Certain fleet transactions, particularly sales to daily rental car companies, are generally less profitable than retail sales to end customers. The following table summarizes estimated fleet sales and those sales as a percentage of total vehicle sales (vehicles in thousands): Years Ended December 31, 2025 2024 2023 GMNA 667 615 679 GMI 427 401 506 Total fleet sales 1,094 1,016 1,185 Fleet sales as a percentage of total vehicle sales 17.7 % 16.9 % 19.2 % Product Pricing Several methods are used to promote our products, including the use of dealer, retail, and fleet incentives, such as customer rebates and finance rate support. The level of incentives is dependent upon the level of competition in the markets in which we operate and the level of demand for our products.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
Item 1A. Risk Factors We have listed below the most material risk factors applicable to us. These risk factors are not necessarily in the order of importance or probability of occurrence: Risks related to our competition and strategy If we do not deliver new products, services, technologies, and customer experiences in response to increased competition and changing consumer needs and preferences, our business could suffer. We believe that the automotive industry will continue to experience significant change in the coming years, particularly as traditional automotive original equipment manufacturers (OEMs) shift resources and strategies in response to changes in the regulatory landscape and evolving consumer preferences. In addition to our traditional competitors, we must also be responsive to the entrance of start-ups and other non-traditional competitors in the automotive industry, such as software and ridesharing services supported by large technology companies. These new competitors, as well as established industry participants, are disrupting the historic business model of our industry through the introduction of new technologies, products, services, direct-to-consumer sales channels, methods of transportation, and vehicle ownership.…

We operate in a highly competitive industry that has historically had excess manufacturing capacity, and attempts by our competitors to sell more vehicles could have a significant negative effect on our vehicle pricing, market share, and results of operations. The global automotive industry is highly competitive in terms of the quality, innovation, new technologies, pricing, fuel economy, reliability, safety, customer service, and financial services offered. Additionally, despite the fact that OEMs have experienced supply constraints in recent years due to the COVID-19 pandemic and certain supply chain and logistics challenges, overall manufacturing capacity in the automotive industry has historically far exceeded demand. Supply chain and 13 Table of Contents GENERAL MOTORS COMPANY AND SUBSIDIARIES logistics challenges may occur as a result of geopolitical and/or policy actions. Our ICE and electric vehicles also require a more resilient, scalable, and sustainable North American-focused supply chain, which includes advancing our strategic sourcing initiatives to secure supply through investments in raw materials suppliers and the execution of strategic, multi-year supply agreements with suppliers throughout the value chain. These agreements may require us to hold higher-than-normal levels of raw materials inventory and to make long-term commitments to purchase raw materials. Expected demand for these raw materials currently exceeds the North American capacity of the existing supply chain.…

Manufacturers in countries that have lower production costs, such as China and India, have become competitors in key emerging markets and have begun offering their products in established markets, as well as low-cost alternatives to established entry-level automobiles. These actions have had, and are expected to continue to have, a significant negative effect on our vehicle pricing, market share, and results of operations in these markets. In addition, foreign governments may decide to implement tax and other policies that favor their domestic manufacturers at the expense of international manufacturers, including GM and its joint venture partners. Introduction or modification of import tariffs or tariff-related measures may lead to further challenges for GM and our global business.

In addition, our success in China depends upon our ability to adequately address unique market and consumer preferences driven by advancements related to EVs, infotainment, software-enabled connected services, and other new technologies while achieving affordability. Our ability to fully deploy our technologies in China may be impacted by evolving laws and regulations in the U.S. and China and the unique regulatory landscape in China. Increased competition, continued U.S.-China trade tensions, weakening economic conditions in China or China's level of integration with key components of our global supply chain, among other factors, may result in cost increases, price reductions, reduced sales, profitability, and margins, and challenges to gaining or holding market share.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
GMI Industry sales in China were 26.4 million units in the year ended December 31, 2025, remaining flat compared to the corresponding period in 2024. Our total vehicle sales in China were 1.9 million units resulting in a market share of 7.1% in the year ended December 31, 2025, representing an increase of 0.1 percentage points compared to the corresponding period in 2024. Our Automotive China JVs generated an equity loss of $0.3 billion in the year ended December 31, 2025, which includes charges of $0.6 billion related to the previously announced restructuring of SGM. We continue to focus on enhancing the 28 Table of Contents GENERAL MOTORS COMPANY AND SUBSIDIARIES competitiveness of our products in the Chinese market and executing restructuring plans. Additional restructuring charges may be incurred going forward.

31 Table of Contents GENERAL MOTORS COMPANY AND SUBSIDIARIES GMNA EBIT-Adjusted The most significant factors that influence profitability are industry volume and market share. While not as significant as industry volume and market share, another factor affecting profitability is the relative mix of vehicles sold. Trucks, crossovers, and cars sold currently have a variable profit of approximately 160%, 40%, and 60% of our GMNA portfolio on a weighted-average basis.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
