你是 stock-analyst v20 DD 的證據採集子 agent。標的：EME。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - EMCOR Group product substitute technology threat 2026
  - Engineering & Construction alternative technology disruption 2026 2027
  - EME EMCOR Group technology obsolescence risk
  - Engineering & Construction next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm｜as_of：2026-02-26
<<<
Certain of our businesses, including those within our United States industrial services segment, are exposed to risks associated with the oil and gas industry. These risks, which are not subject to our control, include volatility in the price and production of crude oil, the development of and consumer demand for alternative energy sources, including as a result of a change in consumer preference, or in an effort to reduce greenhouse gas emissions or combat climate change, and legislative and regulatory actions. In addition, macroeconomic conditions, influenced by a variety of events and circumstances, can also affect customer demand for our services within these businesses and lower prices and production volumes, or perceived risk thereof, typically results in the curtailment or deferral of spending by our customers. While higher prices for our customers’ products may increase demand for our services, significant increases in the price or demand for crude oil may also result in the short-term curtailment or deferral of spending by our customers, as facility downtime to perform certain of the services we provide comes at a higher opportunity cost. Volatility within these markets, including the impact of geopolitical instability (such as disruption of shipping lanes or armed conflict or instability in oil-producing nations, including Iran and Venezuela), could negatively impact our financial position, results of operations, and cash flows.

Our business may be adversely affected by significant reductions in government spending, delays or disruptions in the government appropriations process or the failure to fully fund or implement legislation such as the CHIPS and Science Act of 2022 and the Inflation Reduction Act. Some of our businesses derive a portion of their revenues from governmental agencies. As a result, reduced or delayed spending by the federal government and/or state and local governments, potentially including the reduction or elimination of funding for projects or other benefits under relevant legislation, may have a material and adverse impact on our business, financial condition, results of operations, and cash flows. Significant reductions in spending aimed at reducing federal, state, or local budget deficits, the absence of a bipartisan agreement on the federal government's budget or raising the debt ceiling (and any disruption caused by a federal government shutdown as a result thereof), personnel reductions, elimination of government agencies or programs, the closure of government facilities and offices, the freezing or sequestration by the executive branch of congressionally-appropriated funds, or other changes in budget priorities could result in the deferral, delay, disruption, or cancellation of projects or contracts that we might otherwise have sought to perform.…

Volatility in the prices or availability of certain materials, equipment, and commodities used in our businesses and those of our customers, including as a result of inflation, supply chain disruptions, geopolitical instability, and protectionist trade measures, could adversely affect our businesses. We are exposed to market risk of increases in certain commodity prices of materials, such as copper and steel, which are used as components of supplies or materials utilized in our operations. We are also exposed to increases in energy prices, particularly as they relate to gasoline prices for our fleet of approximately 14,400 vehicles. While we believe we can increase our prices to adjust for some price increases in commodities, there can be no assurance that price increases of commodities, if they were to occur, would be recoverable. Further, the timing of our price increases may lag the timing of the underlying increases in commodity or material prices and certain of our contracts do not allow us to adjust our prices. As a result, increases in material or fuel costs could reduce our profitability with respect to projects in progress. Additionally, we rely on third-party vendors and manufacturers to supply much of the materials and equipment necessary for our operations.…

Our business strategy relies, in part, on acquisitions to sustain our growth, and these transactions present certain risks and uncertainties. As part of our growth strategy, we acquire companies that expand, complement, and/or diversify our businesses. However, there is no guarantee that we will be successful in identifying targets that meet our requirements for acquisition. We may also face increased competition from other potential acquirers, including those who may have greater financial resources available to them or who may be in a position to offer more favorable terms to the target company. This competition may limit our ability to pursue acquisition opportunities. Additionally, circumstances beyond our control, such as elevated interest rates, inflation and potential macroeconomic disruptions, may hinder our ability to pursue and complete acquisitions. Further, realization of the anticipated benefits of an acquisition, such as our acquisition of Miller Electric Company, and avoiding or mitigating the potential risks associated with an acquisition, will depend, among other things, upon our ability to: (a) effectively conduct due diligence to identify and mitigate potential issues at companies we propose to acquire, (b) recognize incompatibilities or other obstacles to the successful integration of the acquired business with our other operations, and (c) gain greater efficiencies and scale that will translate into reduced costs or anticipated synergies in a timely manner.…

We are increasingly dependent on sophisticated information technology systems; our business and results of operations are subject to adverse impacts due to the disruption, failure, or breaches of these systems. We and our customers and third-party providers rely on information technology systems, hardware, and software, including third-party “cloud based” systems, to run critical accounting, project management, and financial information systems. We rely upon security measures, systems redundancy, and third-party products and services to attempt to secure our information technology systems and the confidential, proprietary, and sensitive information they contain. However, our information technology systems and data, and that of our customers and third-party providers, are subject to cybersecurity incidents, such as hacking, computer viruses or other malicious or destructive software, ransomware, denial of service attacks, malicious social engineering and other intrusions, encryption, erasure, failure, and damage by individuals (which may include our and our third-party providers’ employees), groups or nation states or state-sponsored threats. Such cybersecurity incidents could result in operational disruption and information misappropriation, such as theft of intellectual property or inappropriate disclosure of customer data or confidential, sensitive, or personal information, or in reputational harm with customers.…

13 Table of Contents The proper functioning of our information technology systems could also be impacted by other causes and circumstances beyond our control, including malware embedded in third-party applications, the decision by software vendors to discontinue further development, integration, or long-term software maintenance support for our information systems, or hardware interruption, damage or disruption as a result of power outages, natural disasters, or computer network failures. Errors or other defects in the design or implementation of hardware or software applications by our employees or third-party providers could also disrupt our networks, information systems or data. System redundancy may be ineffective or inadequate, and the Company’s disaster recovery and business continuity planning may not be sufficient to address all potential cybersecurity incidents or other disruptions. We may also utilize new information technology tools, including AI tools, in certain business functions, and such tools could be subject to malfunction, security vulnerabilities, or algorithmic flaws (including AI generation of false or biased information). Unsettled regulations and case law regarding the ownership of intellectual property generated or used by AI could also expose us to claims of copyright or license infringement or other liability resulting from our use of such tools.…

The availability and costs to adequately train and maintain a skilled labor force could be impacted by factors we cannot control, including changes in the unemployment rate, prevailing wage rates, benefit costs, potential labor force disruptions, and competition for labor from our competitors in the markets we serve. Labor shortages or increased labor costs, such as those experienced in recent years, could impair our ability to provide services to our customers (or the ability of third-party subcontractors to provide services to us), maintain our business, or grow our revenues. Federal or state regulations, which seek to prohibit non-competition agreements with employees may also impact our ability to retain key employees by reducing barriers to individuals with such agreements leaving to work for our competitors.

Terrorist attacks, wars, conflicts, and other catastrophic events could disrupt our operations and services. Acts of terrorism, war, conflicts, and other catastrophic events, and the actions taken by the United States and/or other governments or actors in response to such events, may result in property damage, supply disruption, or economic dislocations throughout the country. Although it is not possible to predict such events or their consequences, these events could increase the volatility of our financial results due to decreased demand and unforeseen costs, with partial or no corresponding compensation from clients.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
