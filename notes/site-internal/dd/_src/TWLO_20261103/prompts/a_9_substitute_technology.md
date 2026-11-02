你是 stock-analyst v20 DD 的證據採集子 agent。標的：TWLO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Twilio product substitute technology threat 2026
  - Software - Infrastructure alternative technology disruption 2026 2027
  - TWLO Twilio technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm｜as_of：2026-02-24
<<<
Our research and development organization is predominantly built around small development teams. Our small development teams foster greater agility, which enables us to develop new, innovative products and make rapid changes to our infrastructure that increase resiliency and operational efficiency. Our development teams designed and built much of our customer engagement platform and our core platforms stack. These teams continue to focus on the highest impact product areas for our future, which includes focusing on continued innovation in the face of rapid technological change and changing industry practices. We are continuing to invest in AI-powered capabilities, which we believe have the potential to enhance our offerings’ value to customers, as well as to automate processes and help our business run more efficiently.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm｜as_of：2026-02-24
<<<
Global economic and business activities continue to face widespread macroeconomic uncertainties, including market volatility, changes in international economic and trade relations, supply chain disruptions, changes in the labor market, elevated interest rates and potential increases in inflation, foreign currency exchange rate fluctuations and recession risks, which may continue for an extended period. Additionally, the instability in the political environment in many parts of the world, including in the United States, and changes and uncertainty with respect to trade policies, actual or threatened tariffs, treaties, government regulations, executive orders, directives and enforcement priorities, as well as any ongoing or potential U.S. federal government shutdown, may adversely affect the global economy and/or our business. Given that a majority of our revenue is usage-based and therefore impacted by general consumer sentiment and activity, our business may be more immediately and severely impacted by adverse macroeconomic conditions than those that rely primarily on subscription revenue. Additionally, increased prices resulting from the effects of tariffs and inflation could increase our operating expenses.

Customers may terminate or reduce their use of our products, or we may fail to attract new customers, for any number of reasons, including dissatisfaction with our products or with the value proposition of our products, our inability to meet their needs and expectations, our failure to maintain performance, reliability, security, integrity or availability of our products and infrastructure to the satisfaction of our customers, or customers’ use of competitors’ products. For example, prior instances of disruptions in our networks or systems, or those of our third-party service providers, have impacted our customers’ ability to use products on our platform for up to several hours at a time. Such issues have had, and in the future may have, an adverse impact on customer satisfaction and our ability to retain or attract customers and have caused, and may in the future cause, us to incur certain costs associated with offering credits to our affected customers.

We continue to scale the capacity of, and enhance the capability and reliability of, our technical infrastructure to support increased activity on our platform. Any failure to maintain performance, reliability, security, integrity and availability of our products and infrastructure to the satisfaction of our customers may harm our reputation and our ability to retain existing customers or attract new customers. If we fail to efficiently scale and manage our infrastructure, or if our customers experience service disruptions or outages, our business, financial condition and operating results may be adversely impacted.

Some of our competitors and potential competitors are larger and have greater name recognition, longer operating histories, more established customer relationships, larger budgets, lower operating costs, and significantly greater resources than we do. As a result, our competitors may be able to respond more quickly and effectively than we can to new or changing opportunities, technologies, standards, customer requirements or changing economic conditions. Our competitors may also offer products or services that address one or a limited number of functions at lower prices, with greater depth than our products or in different geographies. Our current and potential competitors have in the past and may in the future develop and market products and services with comparable functionality to our products, and this could lead us to decrease prices in order to remain competitive. In addition, customers may reduce or delay spending on our products or substitute alternative solutions in response to pricing pressures, budget constraints or changing business priorities.

To deliver our products, we rely on network service providers and internet service providers for our network service and connectivity, and disruption or deterioration in the quality of these services or changes in provider fees that we pay in connection with the delivery of communications on our platform could adversely affect our business, results of operations and financial condition.

Our success will depend, in part, on our ability to expand our products and grow our business to meet the needs of current and prospective customers. In some circumstances, we may determine to do so through acquisitions, partnerships or investments in businesses and technologies that are complementary to our business. There can be no assurances that such transactions will result in the anticipated benefits, and it is possible that there could be a loss of our key employees and customers, disruption of ongoing businesses or unexpected issues, higher than expected costs, the diversion of management attention and resources from day-to-day business operations and an overall post-completion process that takes longer than originally anticipated. In addition, the following issues, among others, may need to be addressed in order to realize the anticipated benefits of any acquisitions, partnerships or investments: •combining the acquired businesses’ corporate functions with our corporate functions; •combining acquired businesses with our existing business in a manner that permits us to achieve the synergies anticipated to result from such acquisitions, the failure of which would result in the anticipated benefits of our acquisitions not being realized in the time frame currently anticipated or at all; •maintaining existing agreements with customers, distributors, providers, talent and vendors and avoiding delays in entering into new agreements with prospective customers, distributors, providers, talent…

From time to time, we may also divest or stop investing in certain businesses or products. The sale of a business or product has in the past and may in the future require us to restructure operations and/or terminate employees and could expose us to unanticipated ongoing obligations and liabilities, including as a result of our indemnification obligations. During the pendency of a divestiture, we may be subject to risks related to a decline in the business, loss of employees, customers, or suppliers, and that the transaction may not close, which could have an adverse effect on the business to be divested and on us. Divestitures or winding down businesses or products can also disrupt our customer, supplier and/or employee relationships and divert the time and attention of our management and employees. Additionally, we may experience harm to our financial results, including loss of revenue, and we may not realize the expected benefits and cost savings of these actions and our operating results may be adversely impacted.

We have been targeted by threat actors seeking unauthorized access to our systems or data, or that of our customers or third-party service providers, or to disrupt our operations or ability to provide our services. Our third-party service providers have also been targeted. Our platform and our underlying infrastructure, the information we store and process, and those of our third-party service providers, are subject to evolving threats and have in the past and may in the future be subject to breaches, compromises, disruptions, or other incidents, including as a result of the following: •fraud, social-engineering attacks (such as phishing) and other third-party attempts to induce our employees, customers or partners to disclose sensitive information to gain access to our customers’ data or systems, or our data or our systems; •efforts by hackers or sophisticated groups, such as criminal organizations, state-sponsored organizations or nation-states, to launch coordinated cyberattacks on internally built infrastructure or on third-party cloud-computing platform providers, including malicious code, ransomware, destructive malware, supply chain attacks and distributed denial-of-service attacks; •third-party attempts to abuse our marketing, advertising, messaging or products and functionalities to impersonate persons or organizations and disseminate information that is false, misleading or malicious; •attacks on, malfunctions or unavailability of, or other vulnerabilities in, the underlying networks and services that power the internet or that our products otherwise…

We rely on technology and intellectual property of third parties, the loss of which could limit the functionality of our products and disrupt our business.

General Risks Our business is subject to the risks of pandemics, earthquakes, fire, floods and other natural catastrophic events, and to interruption by man-made problems such as power disruptions, computer viruses, security breaches and incidents, terrorism or war.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TWLO_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
