你是 stock-analyst v20 DD 的證據採集子 agent。標的：BSX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - BSX Boston Scientific market share gaining OR losing 2026
  - Boston Scientific new entrant OR displace threat Medical Devices 2026
  - BSX competitor design win 2026
  - Boston Scientific vs Medical Devices peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm｜as_of：2026-02-17
<<<
We expect to continue to invest in our core businesses and pursue opportunities to diversify and further expand our presence in strategic, high-growth adjacencies and new global markets, including growth within the countries we define as emerging markets. Maintaining and expanding our international presence is an important component of our long-term growth strategy. Through our international presence, we seek to increase net sales and market share, leverage our relationships with leading physicians and their clinical research programs, accelerate the time to bring new products to market and gain access to worldwide technological developments that we can implement across our product lines. Our research and development efforts are focused largely on the development of next-generation and novel technology offerings across multiple programs and all divisions. In the past several years, we have completed numerous acquisitions in support of our growth strategy, both strengthening our core businesses and expanding into high growth adjacent markets. We continue to develop digital tools and technologies that enable us to compete more effectively and deliver first class remote physician education, drive deeper patient engagement and increase digitally-enabled sales force productivity.

Markets Competition We encounter significant competition across our business segments, product lines and markets, from global and local competitors. Our primary competitors include large manufacturers with multiple lines of business and competing products, as well as a wide range of medical device companies that sell a single or limited number of competitive products or participate in only a specific market segment. We also encounter competition from the entry of low-cost manufacturers, which may lead to increased pricing pressure. In certain countries, and particularly in China, we face competition from domestic medical device companies that may benefit from their status as local suppliers. We also face competition from non-medical device companies, which may offer alternative therapies for disease states that could also be treated using our products, or from companies offering technologies that could augment or replace procedures using our products.

We believe that our products and solutions compete primarily on their ability to deliver both differentiated clinical and economic outcomes for our customers by enabling physicians to perform diagnostic and therapeutic procedures safely and effectively often in a less-invasive and cost effective manner. We also compete on ease of use, comparative effectiveness, reliability and physician familiarity. In the current environment of managed care, with economically motivated buyers, consolidation among health care providers, increasing prevalence and importance of regional and national tenders, increased competition and declining reimbursement rates, we are also required to compete on the basis of price, value, reliability and efficiency.

We rely on non-disclosure and non-competition agreements with employees, consultants and other parties to protect, in part, trade secrets and other proprietary technology. There has been substantial litigation regarding patent and other intellectual property rights in the medical device industry, particularly in the areas in which we compete. We continue to defend ourselves against claims and legal actions alleging infringement of the patent rights of others. Additionally, we may find it necessary to initiate litigation to enforce our patent rights, to protect our trade secrets or know-how and to determine the scope and validity of the proprietary rights of others. Accordingly, we may seek to settle some or all of our pending litigation, particularly to manage risk over time. Settlement may include cross licensing of the patents that are the subject of the litigation as well as our other intellectual property and may involve monetary payments to or from third parties.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm｜as_of：2026-02-17
<<<
The medical device markets in which we participate are highly competitive. We encounter significant competition across our product lines and in each market in which our products are sold from various medical device companies. Some of our competitors may have greater financial and marketing resources than we do, including as a result of consolidation among companies in our industry. Our primary competitors include large manufacturers with multiple lines of business and competing products, as well as a wide range of medical device companies that sell a single or limited number of competitive products or which participate in only a specific market segment or segments. We also face competition from non-medical device companies, including pharmaceutical companies, biotech companies and providers of various diagnostic solutions, which may offer alternative therapies for disease states also amenable to diagnosis or treatment using our products. New competitors may emerge in the future, potentially including companies introducing new sales or distribution models to our industry or leveraging genomic, robotic, navigation, and/or other automation technologies. Digital technologies, including artificial intelligence (AI) and machine learning capabilities, have and may continue to increase in their applicability and importance to various aspects of our business, operating and competitive environments, research and development (R&D) pipeline and product portfolio.…

In addition, the medical device markets in which we participate are characterized by extensive research and development and rapid technological change. Developments by other companies of products and/or services, processes or technologies, including low-cost alternatives, may make our products or proposed products obsolete or less competitive and may negatively impact our net sales. It is necessary for us to devote continued efforts and financial resources to the development or acquisition of scientifically advanced technologies and products. In addition, we will need to apply our technologies cost-effectively across product lines and markets, obtain patent and other protection for our technologies and products, obtain required regulatory and reimbursement approvals and successfully manufacture and market our products consistent with our quality standards. If we fail to develop or acquire new products or enhance existing products, such failure could have a material adverse effect on our business, financial condition or results of operations. In addition, a delay in the timing of the launch of next-generation products and the overall performance of, and continued physician confidence in, those products may result in declines in our market share and have an adverse impact on our business, financial condition or results of operations.

We may experience declines in market size, average selling prices for our products, medical procedure volumes and/or our share of the markets in which we compete, which could have an adverse effect on our business, financial condition or results of operations.

We continue to experience pressures across many of our businesses due to competitive activity, increased market power of our customers as the health care industry consolidates, national and regional government tenders, economic pressures experienced by our customers, capacity shortages within health care facilities that have and may continue to negatively impact demand for our products, public perception of our products, and the impact of managed care organizations and other third-party payers. Shifts in sites of care including migration of procedures from inpatient to outpatient, ambulatory surgical centers or office-based settings, and associated changes in coverage, reimbursement, payment terms and provider economics, may impact procedure volumes, product mix, and pricing and contracting. These and other factors may adversely impact market sizes, as well as our share of the markets in which we compete, the average selling prices for our products or medical procedure volumes. There can be no assurance that the size of the markets in which we compete will increase, that we will be able to hold or gain market share or compete effectively on the basis of price or that the number of procedures in which our products are used will increase.…

International net sales accounted for 36 percent of our global net sales in 2025. An important part of our strategy is to continue pursuing growth opportunities in net sales and market share outside of the U.S. by expanding global presence, including in Emerging Markets. Our international operations are subject to a number of market, business and financial risks and uncertainties, including those related to our use of channel partners, go-to-market strategies, geopolitical and economic instability, foreign currency exchange and interest rate fluctuations, competitive product offerings, local changes in health care financing and payment systems and health care delivery systems, local product preferences and requirements, including preferences for local manufacturers, trade protection measures, including tariffs and other barriers to market participation, workforce instability, weaker intellectual property protection in certain countries than exists in the U.S. and longer accounts receivable cycles. Such risks and uncertainties may adversely impact our ability to implement our growth strategy in these markets and, as a result, our sales growth, market share and operating profits from our international operations may be adversely affected.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BSX_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
