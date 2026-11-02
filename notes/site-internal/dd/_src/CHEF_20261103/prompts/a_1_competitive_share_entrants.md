你是 stock-analyst v20 DD 的證據採集子 agent。標的：CHEF。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - CHEF The Chefs' Warehouse market share gaining OR losing 2026
  - The Chefs' Warehouse new entrant OR displace threat Food Distribution 2026
  - CHEF competitor design win 2026
  - The Chefs' Warehouse vs Food Distribution peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm｜as_of：2026-02-24
<<<
Competitive Strengths We believe that, during our 40-year history, we have achieved, developed and/or refined the following strengths which provide us with a distinct competitive position in the foodservice distribution industry and also the opportunity to achieve superior margins relative to most large broadline foodservice distributors: Leading Distributor of Specialty Food Products in Many of the Key Culinary Markets. Based on our management’s industry knowledge and experience, we believe we are among the largest distributors of specialty food products, as measured by net sales, in the New York, Washington, D.C., San Francisco and Los Angeles metropolitan markets. We believe these markets, along with a number of other markets we serve, including Las Vegas, Miami, New England, Portland, Columbus, Cincinnati, Chicago, Vancouver, Edmonton, Toronto, Seattle, Sacramento, Texas, Dubai, Abu Dhabi, and Qatar create and set the culinary trends for the rest of the United States, the Middle East, and Canada and provide us with valuable insight into the latest culinary and menu practices.…

Expand our Customer Base Within our Existing Markets. We serve more than 55,000 Core Customer locations, excluding our direct-to-consumer business, in the United States, Middle East, and Canada. We plan to expand our market share in the fragmented specialty food distribution industry by cultivating new customer relationships within our existing markets through the continued penetration of menu-driven independent restaurants, fine dining establishments, country clubs, hotels, caterers, culinary schools, bakeries, patisseries, chocolateries, cruise lines, casinos and specialty food stores. We believe we have the opportunity to continue to gain market share in our existing markets by offering an extensive selection of specialty food products, as well as center-of-the-plate proteins, produce and traditional broadline staple food products through our unique, collaborative and educational sales efforts and efficient, scalable distribution solution.

Competition The foodservice distribution industry is highly competitive. We compete with numerous smaller distributors on a local level, as well as with a limited number of national broadline foodservice distributors. Certain of these distributors have greater financial and other resources than we do. Bidding for contracts or arrangements with customers, particularly larger hotels and caterers, is highly competitive and distributors may market their services to a particular customer over a long period of time before they are invited to bid. We believe that most purchasing decisions in the foodservice distribution industry are based upon the quality and price of the product distributed and the distributor’s ability to completely and accurately fill orders and deliver them in a timely manner.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm｜as_of：2026-02-24
<<<
The foodservice distribution industry is highly fragmented and competitive, with national, multi-regional, regional and local distributors and specialty competitors. Regional and local companies may align themselves with other smaller distributors through group purchasing organizations, with the goal of enhancing their geographic reach, private label offerings, overall purchasing power, cost efficiencies, and ability to meet customer distribution requirements. These distributors may also rely on local presence as a source of competitive advantage, and they may have a lower cost to serve and other competitive advantages due to geographic proximity. Additionally, adjacent competition, such as other cash-and-carry operations, commercial wholesale outlets, warehouse clubs and grocery stores, continue to serve the commercial foodservice market. We also experience competition from online direct food wholesalers and other retailers. We generally do not have exclusive distribution agreements with our customers, and they may switch to other distributors that offer lower prices or differentiated products or customer service. The cost of switching distributors is very low, as are the barriers to entry into the U.S. foodservice distribution industry. Such changes may occur particularly during periods of economic uncertainty or significant inflation.

Our future success will be largely dependent upon our ability to profitably meet our customers’ needs for certain gourmet foods and ingredients, varying drop sizes, high service levels and timely delivery. We compete with numerous smaller distributors on a local level, as well as with a limited number of larger, traditional broadline foodservice distributors. We cannot assure investors that our current or potential competitors will not provide specialty food products and ingredients, produce, center-of-the-plate protein items or services that are comparable or superior to those provided by us at prices that are lower than the prices we charge or adapt more quickly than we do to evolving culinary trends or changing market requirements. Accordingly, we cannot assure investors that we will be able to compete effectively against current and future competitors, and increased competition may result in price reductions, reduced gross margins and loss of market share, any of which could have a material adverse effect on our business, financial condition or results of operations.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1517175/000151717526000005/chef-20251226.htm｜as_of：2026-02-24
<<<
In recent years, our sales to existing and new customers have increased through the continued growth in demand for specialty food and center-of-the-plate products in general; increased market share driven by our large percentage of sophisticated and experienced sales professionals, our high-quality customer service and our extensive breadth and depth of product offerings, including, as a result of our acquisitions; the expansion of our existing distribution centers; our entry into new distribution centers, including the construction of new distribution centers that serve our markets in Las Vegas, Oman, Denver, Portland, San Francisco, United Arab Emirates, Philadelphia and Miami; and the import and sale of our proprietary brands. Through these efforts, we believe that we have been able to expand our customer base, enhance and diversify our product selections, broaden our geographic penetration and increase our market share.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CHEF_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
