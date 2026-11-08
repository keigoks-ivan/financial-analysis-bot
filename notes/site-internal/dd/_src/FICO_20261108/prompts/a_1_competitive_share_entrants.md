你是 stock-analyst v20 DD 的證據採集子 agent。標的：FICO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - FICO Fair Isaac market share gaining OR losing 2026
  - Fair Isaac new entrant OR displace threat Software - Application 2026
  - FICO competitor design win 2026
  - Fair Isaac vs Software - Application peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-06）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm｜as_of：2026-11-06
<<<
•Decision Analysis and Augmentation We are focused on advancing human-machine collaboration for complex problem solving across a variety of scenarios and with multiple tools. This includes research and development of a highly advanced suite of mathematical optimization solvers addressing both linear and non-linear problem types. These solvers enable customers to balance competing objectives, such as market share growth against profit maximization, to calculate mathematically optimal decisions and automate their execution. We have seen broader adoption of these solvers within the operations research and academic communities. In addition, our simulation tools and methods enable customers to construct a digital twin of their organization, allowing them to test and iterate on new business strategies and evaluate expected outcomes, without introducing risky changes into their production environments.

COMPETITION The market for our solutions is intensely competitive and is constantly changing. Our competitors vary both in size and in the scope of the products and services they offer. We encounter competition from several sources, including: •in-house data science and systems developers; •developers and providers of large language models, machine learning, and AI systems; •fraud solutions providers; •scoring model builders; •providers of credit reports and credit scores, including consumer reporting agencies; •software companies supplying machine learning modeling, rules, or AI development tools; •entity resolution and social network analysis solutions providers; •providers of customer engagement and risk management solutions; •providers of account workflow management software; •business process management and intelligent decisioning platform providers; •enterprise resource planning and customer relationship management solutions providers; •business intelligence solutions providers; •providers of automated application processing services; and •third-party professional services and consulting organizations.

We believe the principal competitive factors affecting our markets include technical performance; access to unique proprietary AI and predictive models and data; product attributes like adaptability, scalability, interoperability, functionality, and ease-of-use; on-premises and SaaS product availability; product price; customer service and support; the effectiveness of sales and marketing efforts; partner channel effectiveness; existing market penetration; and reputation. Although we believe our products and services compete favorably with respect to these factors, we may not be able to maintain our competitive position against current and future competitors.

Scores In our Scores segment, we compete with both outside suppliers and in-house analytics. Primary competitors among outside suppliers of scoring models are the three major consumer reporting agencies in the U.S. and Canada — which are also our partners in offering our scoring solutions — and VantageScore (a joint venture entity established by the three major U.S. consumer reporting agencies), which is selling a credit scoring product competitive with our products and which has experienced increased regulatory acceptance in the U.S. mortgage market. Additional competitors include consumer reporting agencies outside the U.S. like CRIF, which operates in the European Union, and other data providers like LexisNexis, some of which also are our partners.

For our offerings that deliver credit scores, credit reports, and consumer credit education solutions directly to consumers, we compete with other direct to consumer credit and identity services such as Credit Karma, Credit Sesame, Experian, and TransUnion — most of which are also our partners.

9 Table of Contents Software The competition in our Software segment varies by capability and use case. In the intelligent decisioning platform market, we compete primarily with IBM, SAS and Pegasystems. For solutions that address a specific use case, we compete with a number of individual solution vendors and startups in areas such as fraud solutions, loan origination, optimization, and customer communications. We also continue to see customers attempting do-it-yourself solutions, which trend is expected to increase given the advancement of large language model-based coding and development tools.

15 Table of Contents We offer competitive health and welfare benefit plans with significant company subsidies to offset premiums, retirement plans with a competitive company match to encourage participation and flexible paid-time-off programs including vacation, sick time and disability time. We have paid Maternity and Parental Leave benefits totaling up to 12 weeks, and we have adopted a Well-Being Program designed to provide broad-based physical and mental health education and personal health coaching, as well as quarterly cash Wellness Awards designed to help employees fund wellness-related purchases which they find most valuable. In addition, we have a global Family Building Benefit program, which provides infertility, cryopreservation, surrogacy and adoption support services. In India, we have a Childcare Reimbursement program to assist parents of young children.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-06）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm｜as_of：2026-11-06
<<<
We are subject to significant competition in the markets in which we operate, and our products and pricing strategies, and those of our competitors, could decrease our product sales and market share.

Demand for our products and services may be sensitive to changes in our products and pricing, and our product and pricing strategies may not be accepted by the market. If our customers fail to accept our product and pricing strategies, our revenues, results of operations, and business may suffer. The market for our solutions is intensely competitive and is constantly changing, and we expect competition to persist and intensify. Our regional and global competitors vary in size and in the scope of the products and services they offer, and include: •in-house data science and systems developers; •developers and providers of large language models, machine learning, and AI systems; •fraud solutions providers; •scoring model builders; •providers of credit reports and credit scores, including consumer reporting agencies; •software companies supplying machine learning modeling, rules, or AI development tools; •entity resolution and social network analysis solutions providers; •providers of customer engagement and risk management solutions; •providers of account workflow management software; •business process management and intelligent decisioning platform providers; 18 Table of Contents •enterprise resource planning and customer relationship management solutions providers; •business intelligence solutions providers; •providers of automated application processing services; and •third-party professional services and consulting organizations.

We expect competition from both established and emerging companies to continue to increase. This competition may include our customers developing their own scoring models or other products, including through the use of AI-based offerings, which could eliminate or reduce their purchases of our products and services. For example, our Scores segment faces competition from other credit score models, including VantageScore, which has experienced increased regulatory acceptance in the U.S. mortgage market. VantageScore is a product of a joint venture of TransUnion, Equifax, and Experian, the three major consumer reporting agencies from which we have historically derived a substantial portion of our revenues. We also face competition from other technologies, particularly with respect to AI-based offerings. For example, certain of our fraud solutions products compete against other methods of preventing payment card fraud, and our analytics and decisioning products increasingly compete against products from large language model developers.

Many of our existing and potential competitors have greater financial, technical, marketing, professional services and other resources than we do, and industry consolidation is creating even larger competitors in many of our markets. As a result, our competitors may be able to respond more quickly to new or emerging technologies and changes in customer requirements. They may also be able to devote greater resources than we can to develop, promote, and sell their products. Many of these competitors have long-standing or broad customer relationships, including with many of our current and prospective customers. In addition, new competitors or alliances among competitors may emerge and rapidly gain significant market share. If we are unable to respond as quickly or effectively to changes in customer requirements as our competition, our ability to expand our business and sell our products could be adversely affected.

Our competitors may offer existing or new products that compete with our products at lower prices, either on a standalone basis or as part of integrated product suites. As a result, our customers may purchase competing products instead of ours, which could decrease our sales and market share. Competitive pricing pressure may also require us to reduce our prices in a manner that negatively impacts our margins and could also harm our ability to obtain new long-term contracts and renewals of existing long-term contracts on favorable terms.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FICO_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
