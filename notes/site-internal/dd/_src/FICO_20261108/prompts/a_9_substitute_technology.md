你是 stock-analyst v20 DD 的證據採集子 agent。標的：FICO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Fair Isaac product substitute technology threat 2026
  - Software - Application alternative technology disruption 2026 2027
  - FICO Fair Isaac technology obsolescence risk
  - Software - Application next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-06）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm｜as_of：2026-11-06
<<<
Many of our existing and potential competitors have greater financial, technical, marketing, professional services and other resources than we do, and industry consolidation is creating even larger competitors in many of our markets. As a result, our competitors may be able to respond more quickly to new or emerging technologies and changes in customer requirements. They may also be able to devote greater resources than we can to develop, promote, and sell their products. Many of these competitors have long-standing or broad customer relationships, including with many of our current and prospective customers. In addition, new competitors or alliances among competitors may emerge and rapidly gain significant market share. If we are unable to respond as quickly or effectively to changes in customer requirements as our competition, our ability to expand our business and sell our products could be adversely affected.

We expect that revenues derived from our scoring solutions, fraud solutions, customer communication services, customer management solutions, and decision management software, and their corresponding capabilities when enabled on FICO Platform, will continue to account for a substantial portion of our total revenues for the foreseeable future. Our revenues may decline if the market does not continue to accept these products and services. Factors that might affect the market acceptance of these products and services include the following: •changes in the business analytics industry; •changes in technology, including increased use of artificial intelligence (“AI”) and market disruption caused by AI-based offerings; •our inability to obtain or use key data for our products; •saturation or contraction of market demand; •loss of key customers; •industry consolidation; •failure to successfully adopt cloud-based or AI technologies; •our inability to obtain regulatory approvals for our products and services, including credit score models; •the availability, acceptance and increased use of competing credit score models; •the increasing availability of free or relatively inexpensive consumer credit, credit score, and other information from public or commercial sources, including those that use AI technologies; •failure to execute our selling approach; •failure to establish additional or expanded distribution channels, including through third-party partners and distributors, for our products and services; and •inability to successfully sell our products in new vertical markets.

In addition, the U.S. and other key international economies periodically experience economic downturns and periods of heightened uncertainty, which may result in reduced demand for goods and services, increased volatility of interest rates, fluctuating rates of inflation, geopolitical tensions, restricted credit, poor liquidity, reduced corporate profitability, volatility in credit, trade policies and tariffs, equity and foreign exchange markets, bankruptcies, and overall uncertainty with respect to the economy. The potential for economic disruption presents considerable risks to our business, including potential bankruptcies or credit deterioration of financial institutions with which we have substantial relationships. Economic disruption could adversely affect demand for our products and services, resulting in a decline in the sales of new products to our customers and a reduction in transaction volumes from existing customers. In addition, the volume of our Scores sales depends heavily on macroeconomic conditions in the markets in which our customers operate. For example, the volume of transactions in the U.S. mortgage and credit card markets, which account for a significant portion of the revenues in our Scores segment, may be adversely affected by economic conditions.

During fiscal 2026, 92% of our revenues were derived from sales of products and services to the banking industry. Periods of global economic uncertainty historically have produced substantial stress, volatility, illiquidity, and disruption of global credit and other financial markets, including the bankruptcy, acquisition, or government assistance related to certain major domestic and international financial institutions. The potential for future stress and disruptions, including in connection with geopolitical tensions, military conflicts, trade policies and tariffs, inflationary pressures, and interest rate volatility, presents considerable risks to our businesses and operations. These risks include potential bankruptcies or credit deterioration of financial institutions, many of which are our customers. Such disruption would result in a decline in the revenue we receive from financial and other institutions. In addition, if consumer demand for financial services and products and the number of credit applications decrease, including due to interest rate changes or other factors, the demand for our products and services could also be materially reduced. These types of disruptions could lead to a decline in the volumes of products and services we provide our customers and could negatively impact our revenue and results of operations.

While we expand our sales into international markets, the risks are greater as some of these markets have experienced and may in the future experience substantial disruption and we are less well-known in them.

In our markets, technology changes rapidly, and there are continuous improvements in computer hardware, network operating systems, programming tools, database technologies, cloud-based technologies, AI-based offerings, and the use of the Internet. For example, AI technologies, including generative and agentic AI, and their use are currently undergoing rapid change. If we fail to enhance our current products and develop new products in response to changes in technology or industry standards, or if we fail to bring product enhancements or new product developments to market quickly enough, our products could rapidly become less competitive or obsolete. Our future success will depend, in part, upon our ability to: •innovate by internally developing new and competitive technologies; •use leading third-party technologies effectively; 22 Table of Contents •continue to develop our technical expertise; •anticipate and effectively respond to changing customer needs; •initiate new product introductions in a way that minimizes the impact of customers delaying purchases of existing products in anticipation of new product releases; and •influence and respond to emerging industry standards and other technological changes, including relating to AI.

Our acquisition activities may disrupt our ongoing business and may involve increased expenses, and we may not realize the financial and strategic goals contemplated at the time of a transaction.

25 Table of Contents Our ability to provide reliable products and services to our customers depends on the efficient and uninterrupted operation of our data centers, information technology, and communication systems, as well as those of our external service providers. Any disruption of or interference with our use of data centers, information technology, or communication systems of our external service providers could adversely affect our operations and our business. As our Software segment’s business continues to grow, our dependence on the continuing operation and availability of these systems increases. Our systems and data centers, and those of our external service providers, could be exposed to damage or interruption. These interruptions can include software or hardware malfunctions, communication failures, critical infrastructure failure, outages or other failures of third-party environments or service providers, or be due to defective updates, fires, floods, earthquakes, other extreme weather events or natural disasters, pandemics, war, terrorist acts or civil unrest, power losses, equipment failures, supply chain disruptions, computer viruses, denial-of-service or other cybersecurity attacks, employee or insider malfeasance, human error, and other events beyond our control. Any steps that we or our external service providers have taken to prevent or reduce disruption may not be sufficient to prevent an interruption of services and disaster recovery planning may not account for all eventualities.

If we are subject to infringement claims, it could harm our business. Products in the industry segments in which we compete, including software products, are often subject to claims of patent and other intellectual property infringement, and such claims could increase as the number of products and competitors in our industry segments grow. We may need to defend claims that our products infringe intellectual property rights, and as a result we may: •incur significant defense costs or substantial damages; •be required to cease the use or sale of infringing products; •expend significant resources to develop or license a substitute non-infringing technology; •discontinue the use of some technology; or 29 Table of Contents •be required to obtain a license under the intellectual property rights of the third-party claiming infringement, which license may not be available or might require substantial royalties or license fees that would reduce our margins.

30 Table of Contents Economic uncertainty has and could continue to negatively affect the businesses and purchasing decisions of companies in the industries we serve. Such disruptions present considerable risks to our businesses and operations. As global economic conditions experience stress and negative volatility, including any stress or negative volatility related to the imposition of, or threatened imposition of, tariffs and retaliatory tariffs, economic sanctions, and increased trade tensions or if there is an escalation in regional or global conflicts, or terrorism, we may experience reductions in the number of available customers and in capital expenditures by our remaining customers, longer sales cycles, deferral or delay of purchase commitments for our products, and increased price competition. These factors may adversely affect our business, results of operations, and liquidity.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FICO_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
