你是 stock-analyst v20 DD 的證據採集子 agent。標的：COHR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - COHR Coherent market share gaining OR losing 2026
  - Coherent new entrant OR displace threat Scientific & Technical Instruments 2026
  - COHR competitor design win 2026
  - Coherent vs Scientific & Technical Instruments peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-14）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm｜as_of：2026-08-14
<<<
Competition Coherent is a global leader in many of its product families. We compete, in part, on our core competencies from materials to systems, our differentiated products and services, and the sustainability of our competitive advantages. We also compete by using our intellectual property, ability to scale, product quality, on-time delivery, and technical support. We believe that our vertical integration, manufacturing facilities and equipment, experienced technical and manufacturing employees, and worldwide marketing and distribution channels provide us with competitive advantages. In addition to competitors who manufacture products similar to those we produce, there are other technologies and products available that may compete with our technologies and products.

Trade Secrets, Patents, and Trademarks Our use of trade secrets, proprietary know-how, trademarks, copyrights, patents, contractual confidentiality, and IP ownership provisions helps us develop and maintain our competitive position with respect to our products and manufacturing processes. We aggressively pursue process and product patents in certain areas of our businesses and in certain jurisdictions across the globe. We have entered into selective IP licensing agreements. We have confidentiality and noncompetition agreements with certain personnel. We require our U.S. employees to sign a confidentiality and noncompetition agreement upon commencement of their employment with us. As of June 30, 2026, we had a total of approximately 3,160 issued patents and 1,280 patent applications pending globally.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm｜as_of：2026-08-14
<<<
We continue to make investments in programs with the goal of gaining a greater share of end markets, including the key components for fast growth markets. We cannot guarantee that our investments in capital and capabilities will be sufficient. The potential end markets, as well as our ability to gain market share in such markets, may not materialize on the timeline anticipated or at all. We cannot be sure of the end market price, specification, or yield for products incorporating our technologies. Our technologies could fail to fulfill, partially or completely, our target customers’ specifications. We cannot guarantee the end market customers’ acceptance of our technologies. Further, we may be unable to fulfill the terms of our contracts with our target customers, which could result in penalties of a material nature, including damages, loss of market share, and loss of reputation.

Our markets are characterized by extensive research and development, rapid technological change, frequent new product introductions, changes in customer requirements and evolving industry standards. The nature of these markets requires significant research and development expenses to participate, with substantial resources invested in advance of material sales of our products to our customers. To compete effectively, we must continually address the challenges of dynamic and accelerating market trends and competitive developments. Otherwise, our product offerings may become less competitive given the frequent introduction of alternative or more cost-effective technologies. Because this industry is subject to rapid change, it is difficult to predict its potential size or future growth rate. We cannot ensure that our expenditures for research and development will result 16 Table of Contents in the launch of new products or, if such products are introduced, that those products will achieve sufficient market acceptance or generate sales to offset the costs of development. Our failure to address rapid technological changes in our markets, or the failure of either our customers’ or our products to gain market acceptance, or the failure of the markets in which we participate to grow could adversely affect our business and results of operations.

Large end-user service providers and product companies comprise a significant portion of our customer base. These large customers generally have greater purchasing power than smaller customers and, accordingly, often negotiate more favorable terms from suppliers, including us. As we seek to expand our sales to existing and new large customers, we may be required to agree to terms and conditions that are more favorable to these customers and that may affect the timing of our ability to recognize revenue, increase our costs, and have an adverse effect on our business, results of operations and financial condition. Furthermore, large customers have increased buying power and ability to negotiate onerous terms into our contracts with them, including pricing, warranties, indemnification and production capability terms. If we are unable to satisfy the terms of these contracts, it could result in liabilities of a material nature, including litigation, damages, additional costs, loss of market share, and loss of reputation. Additionally, the terms these large customers require, such as most-favored customer or exclusivity provisions, may impact our ability to do business with other customers and generate revenues from such customers.

18 Table of Contents We may encounter increased competition, and we may fail to accurately estimate our competitors’ or our customers’ willingness and capability to backward integrate into our competencies and thereby displace us.

We may encounter substantial competition from other companies in the same market, including established companies with significant resources. Some of our competitors may have financial, technical, marketing, or other capabilities that are more extensive than ours. They may be able to respond more quickly than we can to new or emerging technologies and other competitive pressures. We may not be able to compete successfully against our present or future competitors. Our failure to compete effectively could have a material adverse effect on our business, results of operations, or financial condition.

We are increasingly incorporating AI capabilities into the development of technologies and our business operations, and into our products and services. AI technology is complex and rapidly evolving, and may expose us to significant competitive, legal, regulatory, and other risks. The implementation of AI can be costly and there is no guarantee that our use of AI will enhance our technologies, benefit our business operations, or produce products and services that are preferred by our customers. AI will likely increase or change the competitive environment in our markets. Our competitors may be more successful in their AI strategy or they may have access to greater AI resources or technology and develop superior products and services.

We have completed acquisitions and divestitures in the past, and expect to expand and diversify our operations with additional acquisitions, but we may be unable to identify or complete prospective acquisitions for many reasons, including increasing competition from other potential acquirers, the effects of consolidation in our industries, and potentially high valuations of acquisition candidates. In addition, applicable competition laws and other regulations may limit our ability to acquire targets, integrate businesses, or force us to divest an acquired business line. If we are unable to identify suitable targets or complete acquisitions, our growth prospects may suffer, and we may not be able to realize sufficient scale and technological advantages to compete effectively in all markets.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
