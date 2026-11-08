你是 stock-analyst v20 DD 的證據採集子 agent。標的：NET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Cloudflare product substitute technology threat 2026
  - Software - Infrastructure alternative technology disruption 2026 2027
  - NET Cloudflare technology obsolescence risk
  - Software - Infrastructure next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
20 Table of contents Downturns in economic conditions and recessions — including potential stagflation, inflation, rising interest rates, reductions in business confidence and activity, the curtailment of government or corporate spending, volatile financial markets, the actual or perceived failure or financial difficulties of financial institutions, supply chain disruptions or increased equipment costs due to current or potential future tariffs, and reduced demand for products and services across a variety of industries — have in the past and may in the future affect our business and our current and prospective customers and their industries adversely. For example, during an economic downturn, our current and prospective customers may suffer from reduced operating budgets. Some of our paying customers may view a subscription to our products as a discretionary purchase and may reduce their discretionary spending on our products or reduce or cut their budget to otherwise expand their subscriptions to our products. Moreover, our competitors may respond to market conditions by lowering prices and attempting to lure away our customers.

We rely on third-party software for certain essential financial and operational services, and a failure or disruption in these services could materially and adversely affect our ability to manage our business effectively.

We rely on third-party software to provide many essential financial and operational services to support our business. Some of these vendors are less established and have shorter operating histories than traditional software vendors. Moreover, these vendors provide their services to us via a cloud-based model instead of software that is installed on our premises. As a result, we depend upon these vendors to provide us with services that are always available and are free of errors or defects that could cause disruptions in our business processes. Any failure by these vendors to do so, or any disruption in our ability to access the Internet, would materially and adversely affect our ability to manage our operations.

In addition, we may not be able to find suitable acquisition candidates and we may not be able to complete acquisitions on favorable terms, if at all. If we identify companies that we would like to buy, we may also face antitrust, competition, and other regulatory scrutiny that may limit our ability to complete such acquisitions. If we do complete acquisitions, we may not ultimately strengthen our competitive position or achieve our goals, and any acquisitions we complete could be viewed negatively by customers, developers, or investors. In addition, we may not be able to integrate acquired businesses successfully or effectively manage the combined company following an acquisition. If we fail to successfully integrate our acquisitions, or integrate and retain the people, technologies, business partners, or customers associated with those acquisitions, into our company, the results of operations of the combined company could be adversely affected. Any integration process in connection with an acquisition will require significant time and resources, require significant attention from management, and disrupt the ordinary functioning of our business, and we may not be able to manage the process successfully, which could adversely affect our business, results of operations, and financial condition.…

The industry in which we compete is characterized by rapid technological change, including frequent introductions of new products and services, evolving industry standards, changing regulations, and the development of novel cyber attacks by hostile parties, as well as changing customer needs, requirements, and preferences. Our need for continuous innovation is driven not only by competitive forces within our industry but also by our need to out-innovate the highly motivated third parties seeking to breach or compromise our network and those of our customers for economic, political, military, or other purposes.

There can be no assurance that any security measures that we or our third-party service providers have implemented or that are included in the equipment and related third-party software that we use to operate our global network will be effective against current or future security threats. We also cannot guarantee that our systems and networks or those of our third-party service providers or the equipment and related third-party software that we use to operate our global network have not been breached or otherwise compromised, or that they and any software in our or their supply chains do not contain bugs, vulnerabilities, or compromised code that could result in a breach of or disruption to our systems and networks or the systems and networks of third parties that support us and our services. Unauthorized access to, other security breaches of, or security incidents affecting, systems, networks, equipment, and data used in our business, including those of our vendors, contractors, or those with which we have strategic relationships, even if not resulting in an actual or perceived introduction of ransomware, malware, or other malicious code or other actual or perceived breach of our customers’ networks, systems, or data, could result in the loss, compromise, corruption or other unavailability of data, disruptions to our and our customers' products, systems, networks, and operations, loss…

As we have expanded our global network, for efficiency reasons we have increased the amount of automation that is used to update and maintain our network. While we believe this increased automation generally makes our network more reliable and robust, if portions of this automation were to fail then the impact could apply to all or substantially all of our co-location facilities, instead of the more localized impact if we were not using automation. In addition, the components of our global network are interrelated, such that disruptions or outages affecting one or more of our network co-location facilities may increase the strain on other components of our network. Concurrent disruptions or outages at one or more of our network co-location facilities may lead to a cascading effect in which heightened strain on our network causes further disruptions or outages, particularly within the regions where the disruptions and outages occur. In addition, the failure of any of our core co-location facilities for any significant period of time, particularly our U.S. core co-location facility, could place a significant strain upon the ongoing operation of our business, as we have only limited redundant functionality for these facilities.…

Any interruption or delay in our customers’ or partners’ access to our network and products will negatively impact our customers. Our customers depend on the continuous availability of our network for the delivery and use of our products, and our products are designed to operate without interruption, including up to 100% uptime guarantee for our Business and Enterprise plans. If all or a portion of our network were to fail, our customers and partners could lose access to their internal network and/or the Internet as a whole until such disruption is resolved or they deploy disaster recovery options that allow them to bypass our network. The adverse effects of any network interruptions on our reputation and financial condition may be heightened due to the nature of our business and our customers’ expectation of continuous and uninterrupted Internet access and low tolerance for interruptions of any duration. In addition, because some of our customers’ most critical applications are protected by our products and network and these customers may not be using other providers for similar services, the adverse effect of network disruptions to these customers could be particularly severe.…

If our supply of certain components is disrupted or delayed or becomes more expensive, there can be no assurance that additional supplies or components can serve as adequate replacements or that supplies will be available on terms that are favorable to us, if at all. Any disruption or delay or additional costs in the supply of our hardware components may delay the opening of new co-location facilities, limit capacity expansion or replacement of defective or obsolete equipment, cause other constraints on our operations that could damage our customer relationships, or otherwise adversely impact our business, financial condition, or results of operations.

If our commercial relationship with JD Cloud is terminated, identifying an alternative solution in China could be difficult, time-consuming, and expensive. Even if an alternative solution is identified, we cannot be certain that the economic terms or performance of any such alternative arrangement will be comparable to our existing relationship with JD Cloud, which could materially negatively impact our financial results and customer satisfaction with such alternative arrangement. A lack of network presence in China would represent a significant loss of utility to many of our customers and could materially harm our business, financial condition, or results of operations.

If we are unable to license necessary technology from third parties now or in the future, we may be forced to acquire or develop alternative technology, which we may be unable to do in a commercially feasible manner or at all, and we may be required to use alternative technology of lower quality or performance. This could limit and delay our ability to offer new or competitive products and increase our costs of production. As a result, our business and results of operations could be significantly harmed.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
