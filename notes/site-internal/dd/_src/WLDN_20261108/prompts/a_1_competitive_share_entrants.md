你是 stock-analyst v20 DD 的證據採集子 agent。標的：WLDN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - WLDN Willdan Group market share gaining OR losing 2026
  - Willdan Group new entrant OR displace threat Engineering & Construction 2026
  - WLDN competitor design win 2026
  - Willdan Group vs Engineering & Construction peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm｜as_of：2026-02-27
<<<
​ Competition The markets for energy efficiency and sustainability, engineering, construction management, economic and financial consulting, design planning and national preparedness services are competitive and highly fragmented. Our competition varies by type of client, type of service and geography. The range of competitors for any one project can vary depending upon technical specialties, the relative value of the project, geographic location, financial terms, risks associated with the work, and any client-imposed restrictions. We often compete with many other technical service firms ranging from small local firms to large international firms. Contract awards are based primarily on qualifications, relevant experience, staffing capabilities, geographic presence, financial stability, customer service, and price. We face strong competition primarily from other regional, national, and international providers of energy efficiency and sustainability consulting services, local electrical and mechanical contractors and engineering firms, lighting and lighting fixture manufacturers and distributors. In addition to our existing competitors, new competitors such as large national or international engineering and/or construction companies could enter our markets.

Unlike some of our competitors, we focus our services on utilities, commercial and industrial markets, and public sector clients and generally exclude most residential services. Utility and public sector clients generally choose among competing firms by weighing the quality, experience, innovation and timeliness of the firm’s services. When selecting consultants for engineering projects, many utilities and government agencies are required to, and others choose to, employ Qualifications Based Selection (“QBS”). QBS requires the selection of the most technically qualified firms for a project, while the financial and legal terms of the engagement are generally secondary.

Our competition varies geographically. Although we provide services in several states, we may be stronger in certain service lines in some geographical areas than in other regions. Similarly, some of our larger competitors are stronger in some service lines in certain localities but are not as competitive in others. Our smaller competitors generally are limited both geographically as well as by the depth and breadth of services they are able to provide.

We consider our principal competitive advantages to be our reputation for dependability, technical knowledge and industry expertise of employees, quality of services and solutions, and the scope and scale of our service offerings. We believe that no single competitor has sufficient market share to influence the markets in which we operate.

Our Workforce As of January 2, 2026, we employed a total of 1,814 employees, excluding contractors. Our employees include, among others, licensed electrical, mechanical, structural, geotechnical and civil engineers; land surveyors; certified building officials; certified inspectors and plans examiners; licensed architects and landscape architects; certified planners; energy sales and audit specialists; installation technicians; program managers; policy advisors, economists, and information technology specialists. We believe that we attract and retain highly skilled personnel with significant industry experience and strong client relationships by offering them challenging assignments in a dynamic work environment that recognizes, supports, and encourages diverse backgrounds and inter-cultural cooperation combined with compensation and employee benefit programs that are competitive with those offered by our competitors. See Part I, Item 1A, "Risk Factors" included in this Annual Report on Form 10-K for a discussion of the risks related to the loss of key personnel or our inability to attract and retain qualified personnel.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm｜as_of：2026-02-27
<<<
We derive significant revenue and profit from contracts that are awarded through a competitive bidding process. Competitive bidding imposes substantial costs and presents a number of risks, including the substantial cost and managerial time and effort that we spend to prepare bids and proposals; the need to estimate accurately the resources and costs that will be required to service any contracts we are awarded, sometimes in advance of the final determination of their full scope; the expense and delay that may arise if our competitors protest or challenge awards made to us pursuant to competitive bidding, as discussed below; and the opportunity cost of not bidding on and winning other contracts we may have otherwise pursued.

To the extent we engage in competitive bidding and are unable to win particular contracts, we not only incur substantial costs in the bidding process that negatively affect our operating results, but we may lose the opportunity to operate in the market for the services provided under those contracts for a number of years. Even if we win a particular contract through competitive bidding, our profit margins may be depressed or we may even suffer losses as a result of the costs incurred through the bidding process and the need to lower our prices to overcome competition.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
