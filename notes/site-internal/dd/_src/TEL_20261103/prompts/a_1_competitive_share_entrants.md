你是 stock-analyst v20 DD 的證據採集子 agent。標的：TEL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - TEL TE Connectivity market share gaining OR losing 2026
  - TE Connectivity new entrant OR displace threat Electronic Components / Connectors 2026
  - TEL competitor design win 2026
  - TE Connectivity vs Electronic Components / Connectors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1385157/000110465925109150/tel-20250926x10k.htm｜as_of：2025-11-10
<<<
The Transportation Solutions segment’s major competitors include Yazaki, Aptiv, Sumitomo, Sensata, Honeywell, Molex, and Amphenol.

Competition The industries in which we operate are highly competitive, and we compete with thousands of companies that range from large multinational corporations to local manufacturers. Competition is generally based on breadth of product offering, product innovation, price, quality, delivery, and service. We have experienced, and expect to continue to experience, downward pressure on prices. However, as a result of increased costs and tariffs, certain of our businesses implemented price increases in recent years.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1385157/000110465925109150/tel-20250926x10k.htm｜as_of：2025-11-10
<<<
Approximately 41% of our net sales for fiscal 2025 were to customers in the automotive end market. The automotive industry is dominated by large manufacturers that can exert significant price pressure on their suppliers. Additionally, the automotive industry has historically experienced significant downturns during periods of deteriorating global or regional economic or credit conditions. As a supplier of automotive electronics products, our sales of these products and our profitability have been and could continue to be negatively affected by significant declines in global or regional economic or credit conditions and changes in the operations, products, business models, part-sourcing requirements, financial condition, and market share of automotive manufacturers, as well as potential consolidations among automotive manufacturers. Further, work stoppages or slowdowns experienced by our customers in the automotive industry, or changes in consumer preferences, could result in slowdowns or closures of assembly plants where our products are included in assembled vehicles.

We encounter competition in substantially all areas of the electronic components industry, which has and could in the future negatively impact our prices, margins, and market share.

We operate in highly competitive markets for electronic components and expect that both direct and indirect competition will increase in the future. Our overall competitive position depends on various factors including the price, 11 Table of Contents quality, and performance of our products; the level of customer service; the development of new technology; our ability to participate in emerging markets; and customers’ expectations relating to socially responsible operations. The competition we experience across product lines from other companies ranges in size from large, diversified manufacturers to small, highly specialized manufacturers. The electronic components industry has become increasingly concentrated and globalized in recent years, and our major competitors have significant financial resources and technological capabilities. A number of these competitors compete with us primarily on price and in some instances may have the benefit of lower production costs for certain products. We cannot provide assurance that additional competitors will not enter our markets or that we will be able to compete successfully against existing or new competitors. Increased competition has and may in the future result in price reductions, reduced margins, or loss of market share, any of which could materially and adversely affect our results of operations, financial position, and cash flows.

In order to remain competitive, we will need to stay abreast of such technologies, require our employees to continue to learn and adapt to new technologies, be able to integrate them into our current and future business models, products, services, and processes, and also guard against existing and new competitors disrupting their business using such technologies. Our strategy, value creation model, operating model, and innovation ecosystem have important technological elements and certain of our products and offerings are based on technological advances, including AI, machine learning, advanced analytics, and the Internet of Things. Meeting evolving industry requirements, including the increasing use of AI and machine learning technologies (including the need to run complex AI-based applications on devices), and introducing new products to the market in a timely manner and at prices that are acceptable to our customers are important factors in determining our competitiveness and success. Further, increasing use of AI may expose us to social and ethical issues, which may result in reputational harm and liability. In addition, we will need to compete for talent in a competitive market that is familiar with such technologies including upskilling our workforce.…

Our operations are subject to applicable antitrust and competition laws in the jurisdictions in which we conduct our business, in particular the U.S. and the EU. These laws prohibit, among other things, anticompetitive agreements and practices. If any of our commercial agreements and practices with respect to the electronic components or other markets are found to violate or infringe such laws, we may be subject to civil and other penalties. We may also be subject to third-party claims for damages. Further, agreements that infringe these antitrust and competition laws may be void and unenforceable, in whole or in part, or require modification to be lawful and enforceable. If we are unable to enforce our commercial agreements, whether at all or in material part, our results of operations, financial position, and cash flows could be adversely affected.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TEL_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
