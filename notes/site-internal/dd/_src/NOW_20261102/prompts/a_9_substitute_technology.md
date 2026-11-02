你是 stock-analyst v20 DD 的證據採集子 agent。標的：NOW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - ServiceNow product substitute technology threat 2026
  - Software - Application alternative technology disruption 2026 2027
  - NOW ServiceNow technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm｜as_of：2026-01-29
<<<
Several factors contribute to our competitive positioning in this environment. Our two decades partnering with enterprise customers provide us with a deep understanding of how work actually flows across organizations—across departments, systems and organizational silos. We have developed expertise in the operational processes specific to different industries, functional areas and user roles, knowledge that cannot be readily replicated and that proves essential when designing solutions that must integrate with existing workflows rather than replace them. This institutional knowledge enables us to build cross-functional workflows that reflect the practical realities of how enterprises operate, rather than idealized process models. Building on this foundation, our platform’s architecture, developed over years of iteration with customer feedback, allows organizations to deploy AI-enhanced workflows without replacing their existing technology infrastructure or disrupting established processes. We bridge the gap between AI's analytical capabilities and the execution layer where business processes operate, providing the connective tissue that turns insights into outcomes. Equally important, our experience operating a software-as-a-service platform at scale gives us operational expertise in maintaining reliability, security, and performance standards that enterprise customers require, particularly as they entrust increasingly critical functions to AI-enabled systems.

Part I IT Operations Management IT Operations Management, or ITOM, identifies, monitors and manages a customer’s physical and cloud-based IT infrastructure. It can simultaneously identify issues from a customer’s IT infrastructure (e.g., physical servers) and digital components (e.g., email), which helps organizations better manage potential disruptions to business services. ITOM also maintains a single record of all IT configurable items, providing organizations better control over on-premises or cloud-based infrastructures while orchestrating key processes and tasks.

We also use our own products to collect real-time feedback on new and existing features – as part of what we call our “Now on Now” program – which informs product refinement and helps improve the customer experience. By incorporating insights from the Now on Now program and evaluating emerging technologies, we aim to anticipate customer needs and introduce new solutions-oriented features and services to the market quickly.

For additional information about competition, see “Risk Factors—A failure to innovate and adapt how we offer our products in response to rapidly evolving technological changes and in the midst of an intensely competitive market may harm our competitive position and business prospects.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm｜as_of：2026-01-29
<<<
Risk Factors Summary This summary provides an overview of the risks we face and should not be considered a substitute for the more fulsome risk factors discussed immediately following this summary.

•A failure to innovate and adapt how we offer our products in response to rapidly evolving technological changes and in the midst of an intensely competitive market may harm our competitive position and business prospects.

•Disruptions or defects in our services could damage our customers’ businesses, subject us to substantial liability and harm our business.

A failure to innovate and adapt how we offer our products in response to rapidly evolving technological changes and in the midst of an intensely competitive market may harm our competitive position and business prospects.

We compete in markets that evolve rapidly. The pace of innovation will continue to accelerate as customers recognize the advantages of acquiring leading digital technologies and adopting AI native solutions and modern cloud-based infrastructure. Cutting-edge capabilities such as AI, machine learning, hyper automation, low-code/no-code application development, system observability and predictive insights become increasingly relevant to the customer’s evolving needs. With this rapid evolution, we are increasingly competing with alternative solutions and approaches to solve customer needs, and we expect additional competition as we shift our products and services to compete with providers in new and adjacent markets.

Part I assumed by such third-party distributor or reseller. If a contract is terminated for convenience, we may only be able to collect fees for products or services delivered prior to termination and settlement expenses. If a contract is terminated due to a default, we may be liable for excess costs incurred by the customer for procuring alternative products or services. In addition, we could be precluded from doing further business with governmental entities. Further, we are required to comply with a variety of complex laws, regulations and contractual provisions relating to the formation, administration or performance of government contracts that give public sector customers substantial rights and remedies, many of which are not typically found in commercial contracts. These laws, regulations and contractual provisions may encompass rights with respect to price protection, refund and setoff, the provision of services in languages other than English, the accuracy of information provided to the government, contractor compliance with supplier diversity policies, constraints on certain business and sales practices, and other obligations that are particular to government contracts. These obligations may apply to us and/or our third-party resellers or distributors whose practices we may not control. Such parties’ non-compliance could create legal, contractual and customer satisfaction issues.

Disruptions or defects in our services could damage our customers’ businesses, subject us to substantial liability and harm our business.

Our business depends on our platform to be available without disruption. From time to time, we have experienced and expect to continue to experience defects, disruptions, data loss, outages and other performance and quality problems with our platform. New defects may be detected in the future and may arise from our increasing use of public cloud service providers. For example, we provide regular updates to our services, which can contain undetected defects. Defects may also be introduced by our use of third-party software, including open-source software. Disruptions, data loss and service degradation may result from errors we make in developing, delivering, configuring or hosting our services, or designing, installing, expanding or maintaining our cloud infrastructure. They may also arise from incidents outside of our control, including third-party incidents, denial of service or ransomware attacks, as well as from our efforts to address vulnerabilities and security incidents. Although we currently serve our customers primarily using equipment managed by us and co-located in third-party data centers operated by several different providers worldwide, we expect to increasingly serve our customers using data center facilities operated by public cloud service providers. As our reliance on public cloud service providers increases, we face heightened risks of outages or performance degradation beyond our direct control.…

We also have a large ecosystem of vendors and service providers that we use for our products, and a data compromise, supply chain issue or other incident involving a critical service provider could impact our ability to provide our services and reduce our productivity. Our customers use our services to manage important aspects of their businesses, and our reputation and business will be adversely affected if our customers and potential customers believe our services are unreliable. Disruptions or defects in our services may reduce our revenues, cause us to issue credits or pay penalties, subject us to claims and litigation, cause our customers to delay payment or terminate or decline to renew their subscriptions, and adversely affect our ability to attract new customers. Similarly, customers may have unique requirements for system resiliency and performance depending on their business models and customers in highly regulated markets may have more demanding requirements that we may not be able to, or may not choose to, meet. The occurrence of payment delays, service credit, warranty or termination for material breach or other claims against us could result in an increase in our bad debt expense, longer aggregate collection cycles, service level credit accruals and other expenses and a heightened risk of litigation.…

Natural disasters or other catastrophic events may damage or disrupt our operations, international commerce and the global economy, and thus could have a negative effect on our business. Our business operations are subject to interruption by natural disasters, flooding, fire, extreme heat, power shortages, pandemics, terrorism, political 2025 Annual Report 35 Table of Contents

We operate globally and as a result, our business, revenues and profitability are impacted by global macroeconomic and political conditions. The success of our activities is affected by general economic and market conditions, including, among others, inflation, interest rates, tax rates, foreign exchange rates, economic downturns, recession, economic uncertainty, political instability, warfare, changes in laws, trade barriers, supply chain disruptions and economic and trade sanctions. The U.S. capital markets experienced and continue to experience extreme volatility and disruption. Such volatility could adversely affect our business, financial condition, results of operations and cash flows and future market disruptions could negatively impact us. These unfavorable economic conditions could increase our operating costs and, because our typical contracts with customers lock in our price for a few years, our profitability could be negatively affected. Geopolitical destabilization and warfare have impacted and may continue to impact global currency exchange rates, commodity prices, energy markets, trade and movement of resources, which may adversely affect the buying power of our customers and our access to and cost of resources from our suppliers and ability to operate or grow our business. In addition, from time to time, the U.S. and other key international economies have been impacted and may continue to be impacted by geopolitical and economic instability.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
