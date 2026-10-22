你是 stock-analyst v20 DD 的證據採集子 agent。標的：MSCI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MSCI MSCI market share gaining OR losing 2026
  - MSCI new entrant OR displace threat Financial Data & Stock Exchanges 2026
  - MSCI competitor design win 2026
  - MSCI vs Financial Data & Stock Exchanges peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-06）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm｜as_of：2026-02-06
<<<
Competition Index. Many industry participants compete with us by offering one or more indexes in similar categories. Such indexes vary widely in scope, including by geographic region, business sector and weighting methodology, and may be used by clients in a variety of ways in many different markets around the world. Among our Index competitors are S&P Dow Jones Indices LLC (a joint venture of S&P Global Inc. and CME Group Inc.); FTSE Russell, a subsidiary of the London Stock Exchange Group plc; Nasdaq Inc; Bloomberg Finance L.P. (“Bloomberg”); and Solactive AG.

Analytics. Our Analytics offerings compete with those from a range of competitors, including Axioma (part of SimCorp), BlackRock Solutions, Bloomberg, and FactSet Research Systems Inc. Additionally, some of the larger broker-dealers have developed proprietary analytics tools for their clients. Similarly, some of the large global investment organizations, such as custodians, have developed internal risk management and performance analytics tools that they offer to their clients.

All Other – Private Assets. We have a variety of competitors for our offerings that provide data, market intelligence, indexes, and performance and risk attribution services relating to private assets. Our private assets data and analytics products also compete with a variety of products and tools that provide transaction-, fund- and asset-level data for private assets and across asset classes.

Our goal is to provide competitive compensation in the markets where we compete for talent and to link pay to performance. All employees are eligible for annual cash bonuses based on performance and, for managing directors, how effectively they demonstrate leadership behaviors consistent with our values and culture.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-06）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm｜as_of：2026-02-06
<<<
We have complex relationships with various parties, including clients, shareholders, distributors of our content and competitors, which may present potential conflicts of interest that could adversely affect our business. Certain of our clients are also significant shareholders, competitors or distributors of our content, including some of our largest clients, such as BlackRock. This dynamic may introduce competitive pressures that could cause these clients to terminate all or a portion of the relationship and result in a loss of business or reduced revenue or influence our strategic decisions, such as whether to prioritize the client relationship over the development or enhancement of products that directly compete with those clients’ offerings.

Competitors and new market entrants may use AI to develop products that compete with our offerings at lower price points, with faster time-to-market or with additional or better capabilities, which could impair our ability to compete effectively and put pressure on our revenues and subscriptions. Additionally, AI-enabled tools may allow clients, including asset managers, asset owners, banks, hedge funds and others, to develop in-house capabilities to replace our products such as custom indexes, risk analytics, and sustainability and climate data. Large-scale data scraping and generative AI models trained on publicly available information could also diminish the perceived uniqueness and commercial value of our proprietary content. Further, third-party AI tools and model providers may change their model behavior, pricing or terms, which could adversely affect our offerings, increase our costs or disrupt our operations.

Competition and financial and budgetary pressures affecting clients may cause price reductions or loss of market share, which may materially adversely affect our business, financial condition or results of operations.

Competition exists across all markets for our products and services. Our competitors range from large companies with substantial resources to small, single-product businesses that are highly specialized. Larger competitors may have access to more resources and may be able to achieve greater economies of scale, and specialized competitors may have unique expertise and dedicated resources and capabilities to compete with respect to a particular product or service. Some competitors may offer price incentives or different pricing structures that are more attractive to clients. The competitive landscape may also experience consolidation, which results in a narrower pool of competitors that are better capitalized or that are able to gain a competitive advantage through synergies.

There is no guarantee that any intellectual property rights that we may obtain will protect our competitive advantages, nor is there any assurance that our competitors will not infringe upon our rights, including through the use of AI models. Furthermore, our competitors may independently develop and protect products and services that are the same or similar to ours. We may be unable to detect the unauthorized use or disclosure of our intellectual property or confidential information, particularly where such use occurs through AI technologies, or to take the necessary steps to enforce our rights. In addition, our products and services, or third-party products that we provide to our clients, could infringe upon the intellectual property rights of others.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
