你是 stock-analyst v20 DD 的證據採集子 agent。標的：TER。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - TER Teradyne market share gaining OR losing 2026
  - Teradyne new entrant OR displace threat Semiconductor Equipment & Materials 2026
  - TER competitor design win 2026
  - Teradyne vs Semiconductor Equipment & Materials peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm｜as_of：2026-02-19
<<<
2 Table of Contents Our corporate strategy is to profitably grow revenue and market share through the introduction of differentiated products targeting expanding markets and customer needs. Our capital allocation plan will continue to be balanced between investing in organic and inorganic growth and returning cash to shareholders through share repurchases and dividends.

We are subject to tariffs and restrictions from the dynamically changing global trade environment. While it is difficult to quantify the exact impact, current trade restrictions are limiting our ability to be competitive, particularly in certain markets, where some competitors are not subjected to the same restrictions. We continue to monitor developments in international trade policy, including potential changes to tariffs, further export controls, and other regulatory measures that could affect our supply chain, cost structure, or market access. For information regarding risks associated with import-export control regulations and similar applicable laws and regulations, see Part II - Item 1A “Risk Factors- Risks Related to Legal and Regulatory Compliance.”

Competition We face significant competition throughout the world in each of our reportable segments. Competitors in the Semiconductor Test segment include, among others, Advantest Corporation, SPEA S.p.A., and Cohu, Inc.

Some of our competitors may have greater financial and other resources to pursue engineering, manufacturing, marketing, and distribution of their products. We also face competition from emerging Asian companies and from internal supply at several of our customers. Some of our competitors have introduced or announced new products with certain performance characteristics which may be considered equal or superior to those we currently offer. We expect our competitors to continue to improve the performance of their current products and to introduce new products or new technologies that provide improved cost of ownership and performance characteristics. See also “Item 1A: Risk Factors.”

Competitive Pay and Benefits The primary objective of our compensation program is to provide a compensation and benefits package that will continue to attract, retain, motivate and reward high performing employees who operate in a highly competitive environment. We seek to achieve this objective by linking a meaningful portion of compensation to company and business unit performance. We enable employees worldwide to share in the success of the company through various programs including a stock purchase program, equity compensation and bonus plans. We seek competitiveness and fairness in total compensation with reference to peer comparisons and internal equity.

Employee Development and Training We believe that employee development and training is a key factor in attracting, motivating, improving and retaining a strong, competitive global workforce. We provide continual development to our employees focused on developing their job skills and competencies. Examples include new manager competencies like giving feedback and coaching, and training in software development tools and project management. Our employees worldwide also receive annual performance reviews and are involved in setting goals for their own development and performance. Employees and managers look back on the previous year, review career development plans and create goals for the next year.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/97210/000119312526059002/ter-20251231.htm｜as_of：2026-02-19
<<<
We are subject to intense competition. We face significant competition throughout the world in each of our reportable segments. Some of our competitors have substantial financial and other resources to pursue engineering, manufacturing, marketing and distribution of their products. In addition, we are subject to trade regulations imposed by the United States government, which may not impact some of our competitors. We also face competition from emerging Asian companies and internal development at several of our customers. Some of our competitors have introduced or announced new products with certain performance characteristics that may be considered equal or superior to those we currently offer. We expect our competitors to continue to improve the performance of their current products and to introduce new products or new technologies that provide improved cost of ownership and performance characteristics. In addition, the semiconductor industry has experienced significant consolidation over the past several years. Consolidation among our competitors or customers could lead to a changing competitive landscape, which could negatively impact our competitive position.…

We believe that our technological position depends primarily on the technical competence and creative ability of our engineers. In a rapidly evolving market, such as ours, the development or acquisition of new technologies, commercialization of those technologies into products and market acceptance and customer demand for those products are critical to our success. In the electronics, semiconductor, and robotics industries, products are often replaced by more technologically advanced substitutes and, as demand for older technology falls, the price at which such products can be sold drops. If we cannot advance new technologies to meet our customers’ demands, our revenues and financial condition may be adversely impacted. Successful product development or acquisition, introduction and acceptance depend upon a number of factors, including: •new product selection and ability to predict market requirements and design new products that address those requirements; •ability to meet customer requirements including with respect to safety and cybersecurity; •development of competitive products by competitors; •timely and efficient completion of product design; •timely and efficient implementation of manufacturing and manufacturing processes; •timely remediation of product performance issues, if any, identified during testing; •assembly processes and product performance at customer locations; •differentiation of our products from our competitors' products; •management of customer expectations concerning product capabilities and product life cycles; •transition of customers to new product platforms; •compliance with product…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
