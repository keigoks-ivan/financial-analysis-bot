你是 stock-analyst v20 DD 的證據採集子 agent。標的：FN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Fabrinet product substitute technology threat 2026
  - Electronic Components alternative technology disruption 2026 2027
  - FN Fabrinet technology obsolescence risk
  - Electronic Components next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm｜as_of：2026-08-18
<<<
11 Table of Contents Our overall competitive position depends upon a number of factors, including: •our manufacturing technologies and capacity; •the quality of our manufacturing processes and products; •our supply chain tools and data management systems; •our ability to safeguard and protect our customers’ intellectual property; •our engineering and prototyping capabilities; •our ability to strengthen and broaden our engineering services and know-how to participate in the growth of emerging technologies; •our ability to deliver on-time; •our ability to deliver continuous cost improvements; and •our responsiveness and flexibility.

Trade Regulations We and our suppliers and service providers could be affected by tariffs, embargoes, or other trade restrictions, as well as laws and regulations enacted in response to concerns regarding climate change, conflict minerals, responsible sourcing practices, public health crises, contagious disease outbreaks, or other matters, which could limit the supply of our materials and increase their cost. In addition, compliance with trade regulations may result in disruptions in logistics, which could delay our receipt of materials. We have experienced increased lead times and expedite fees for the supply of materials. The disruption of our supply of parts and materials, including where such disruption results in the extension of our lead times, could have a material adverse effect on our business, results of operations, or financial condition. Similarly, if our customers experience disruptions to their supplies or materials, or the extension of their lead times, they may reduce, cancel, or alter the timing of their purchases with us, which could have a material adverse effect on our business, financial condition and operating results.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm｜as_of：2026-08-18
<<<
Our quarterly revenues, gross profit margins, and operating results have fluctuated significantly and may continue to fluctuate significantly in the future. For example, any of the risks described in this “Risk Factors” section and, in particular, the following factors, could cause our revenues, gross profit margins, and operating results to fluctuate from quarter to quarter: •any reduction in customer demand or our ability to fulfill customer orders as a result of disruptions in our supply chain; •our ability to acquire new customers and retain our existing customers; •the cyclicality of the optical communications, automotive, industrial lasers, medical, and sensors markets; •competition; •our ability to achieve favorable pricing for our services; •the effect of fluctuations in foreign currency exchange rates; •our ability to manage our headcount and other costs; and •changes in the relative mix in our revenues.

We rely on a single source or a limited number of suppliers for critical materials used in a significant number of the products we manufacture. We generally purchase these single or limited source materials through standard purchase orders and do not maintain long-term supply agreements with our suppliers. We generally use a rolling 12-month forecast based on anticipated product orders, customer forecasts, product order history, backlog, and warranty and service demand to determine our materials requirements. Lead times for the parts and components that we order vary significantly and depend on factors such as manufacturing cycle times, manufacturing yields, and the availability of raw materials used to produce the parts or components. Historically, we have experienced supply shortages resulting from various causes, including reduced yields by our suppliers, which prevented us from manufacturing products for our customers in a timely manner. The semiconductor supply chain is complex, and, in recent years, there has been a significant global shortage of semiconductors. Demand for consumer electronics surged during the COVID-19 pandemic, which in turn has increased the demand for semiconductors. At the same time, wafer foundries that support chipmakers have not invested enough in recent years to increase capacities to the levels needed to support the increased demand from all of their customers.…

Our revenues, profitability and customer relations will be harmed by continued fluctuations in the availability of materials, a stoppage or delay of supply, a substitution of more expensive or less reliable parts, the receipt of defective parts or contaminated materials, an increase in the price of supplies, or an inability to obtain reductions in price from our suppliers in response to competitive pressures. We continue to undertake programs to strengthen our supply chain. Nevertheless, we are experiencing, and expect for the foreseeable future to experience, strain on our supply chain, as well as periodic supplier problems. These supply chain issues have impacted, and will continue to impact, our ability to generate revenue. In addition, we have incurred, and expect for the foreseeable future to incur, increased costs related to our efforts to address these problems.

We most recently expanded our manufacturing capacity by acquiring an 8-acre campus in Navanakorn, Thailand in May 2026, and we began construction of a new manufacturing building of approximately 2.0 million square feet at our Chonburi campus in February 2025. We may continue to devote significant resources to the expansion of our manufacturing capacity, and any such expansion will be expensive, will require management’s time and may disrupt our operations. In the event we are unsuccessful in our attempts to expand our manufacturing capacity, our business, financial condition and operating results could be harmed.

Our business may be adversely affected by evolving global trade policies, including tariffs and other trade restrictions. We are subject to risks associated with changes in international trade policies, regulations, and relationships. In recent years, multiple countries, including the United States, the PRC, and members of the European Union, among others have enacted tariffs, export controls, quotas, and other forms of trade restrictions on a variety of goods and services. These measures have led to increased costs, supply chain disruptions, and reduced demand across several industries. Although certain tariffs have been reduced or delayed, the potential for future escalation or the imposition of new trade restrictions remains. Ongoing or future trade disputes may impact the availability and cost of materials used in our manufacturing processes. In some cases, suppliers may struggle to meet increased demand resulting from accelerated purchasing ahead of anticipated policy changes, further exacerbating supply chain instability. Additionally, retaliatory actions or changes in trade policies by foreign governments may reduce the demand for our customers’ products in impacted regions, which could lead to reduced orders and revenue for us. If we are unable to mitigate the effects of increased costs or pass them on to our customers, our gross margins, financial condition, and results of operations could be materially and adversely affected.

In addition, increased international political instability, the threat or occurrence of terrorist attacks, conflicts in the Middle East, Asia and Europe (including the U.S.-Iran war, the Israel-Hamas war, and the Russia-Ukraine war), strained international relations arising from these conflicts and the related decline in consumer confidence and economic weakness, may hinder our ability to do business. Any escalation in these events or similar future events may disrupt our operations and the operations of our customers and suppliers and may affect the availability of materials needed for our manufacturing services. Such events may also disrupt the transportation of materials to our manufacturing facilities and finished products to our customers. These events have had, and may continue to have, an adverse impact on the U.S. and world economy in general, and customer confidence and spending in particular, which in turn could adversely affect our total revenues and operating results. The impact of these events on the volatility of the U.S. and world financial markets also could increase the volatility of the market price of our ordinary shares and may limit the capital resources available to us, our customers and our suppliers.

Despite our implementation of security measures, our systems are vulnerable to damage caused by computer viruses, natural disasters, unauthorized access and other similar disruptions. Any system failure, accident or security breach could result in disruptions to our operations. To the extent that any disruption, cyber-attack or other security breach results in a loss or damage to our data or inappropriate disclosure of confidential information, our business could be harmed. In addition, we may be required to incur significant costs to protect against damage caused by these disruptions or security breaches in the future.

If an activist investor takes an ownership position in our ordinary shares, responding to actions by such activist shareholder could be costly and time-consuming, disrupt our operations and divert the attention of management and our employees. Additionally, perceived uncertainties as to our future direction as a result of shareholder activism or changes to the composition of our board of directors may lead to the perception of a change in the direction of our business or other instability, which may be exploited by our competitors, cause concern to our current or potential customers, and make it more difficult to attract and retain qualified personnel. If customers choose to delay, defer or reduce transactions with us or do business with our competitors instead of us because of any such issues, then our business, financial condition and operating results would be adversely affected. In addition, our share price could experience periods of increased volatility as a result of shareholder activism.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
