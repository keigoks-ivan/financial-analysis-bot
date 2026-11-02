你是 stock-analyst v20 DD 的證據採集子 agent。標的：DASH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - DoorDash product substitute technology threat 2026
  - Internet Retail alternative technology disruption 2026 2027
  - DASH DoorDash technology obsolescence risk
  - Internet Retail next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm｜as_of：2026-02-18
<<<
Our current and future competitors may enjoy competitive advantages such as greater name recognition, longer operating histories, market-specific knowledge, established relationships with local merchants and suppliers, larger existing user bases, more successful marketing capabilities, established geographic footprints and infrastructure, and substantially greater financial, technical, and other resources than we have. For example, with grocery delivery, we compete with established grocery chains that have strong bargaining power, established relationships with suppliers, and their own delivery fleets. Greater financial resources and product development capabilities may allow these competitors to respond more quickly and efficiently to new or emerging technologies and changes in merchant, consumer, and Dasher preferences that may render our platform less attractive or obsolete. If certain merchants choose to partner with our 12 Table of Contents competitors in a specific geographic market, if merchants choose to engage exclusively with our competitors, or if merchants decide to not partner with us at all, we may lack a sufficient variety and supply of merchant options or lack access to the most popular merchants, such that our offering would become less appealing to consumers.…

If merchants on our platform cease operations, temporarily or permanently, or face financial distress or other business disruption, we may not be able to provide consumers with sufficient merchant selection, which may cause us to lose consumers or cause consumers to use our services less frequently. This risk is particularly pronounced with restaurants, as each year a significant percentage of restaurants go out of business, and in markets where we have fewer merchants. Similarly, if we are unsuccessful in attracting and retaining popular merchants, if merchants enter into exclusive arrangements with our competitors, if we fail to negotiate satisfactory terms with merchants, or if we ineffectively manage our relationships with merchants, our business, financial condition, and results of operations could be adversely affected. Our agreements with partner merchants generally remain in effect until terminated by us or partner merchants, and partner merchants may generally terminate such agreements by providing us at least 7 or 30 days' advance notice. Changes to our business and to our relationships with some of our constituencies may also impact our ability to attract and retain other constituencies. For example, the increased growth of our membership products, and how compelling these offerings are to consumers, depends in part on our ability to sign up eligible merchants to our membership products.…

It is critical to our success that merchants, consumers, and Dashers be able to access our platform at all times and we expect to continue to make significant investments to maintain and improve the availability of our platform. Our systems, or those of third parties upon which we rely, may experience service interruptions or degradation or other performance problems because of hardware and software defects or malfunctions, distributed denial-of-service and other cybersecurity attacks, infrastructure changes, human error, natural disasters, power losses, disruptions in telecommunications services, fraud, military or political conflicts, terrorist attacks, or other events. Our systems also may be subject to break-ins, sabotage, theft, and intentional acts of vandalism, including by our own employees. It may become increasingly difficult and expensive to maintain and improve the performance of our systems and the availability of our platform, especially during peak usage times, as our operations grow and the usage of our platform increases. Some of our systems are not fully redundant and our disaster recovery planning may not be sufficient for all eventualities. Our business interruption 14 Table of Contents insurance may not be sufficient to cover all of our losses that may result from interruptions in our service as a result of systems failures and similar events.

Our reliance on third-party vendors, contractors, and SaaS providers creates additional cybersecurity risks. Many of our critical business operations depend on external providers for hosting, cloud services, data analytics, customer support, and other key functions. If these third parties experience a cybersecurity incident, fail to implement adequate security measures, misconfigure their systems, or otherwise do not comply with our security, privacy, or contractual requirements, our systems and data could be exposed to unauthorized access, loss, or misuse, resulting in significant operational disruption, regulatory scrutiny, financial losses, or reputational harm.

20 Table of Contents Although we take measures to enhance monitoring and protection of our systems and data, these and other measures will never fully protect our systems and data, and we cannot guarantee security in the future. Our IT and infrastructure may be vulnerable to viruses, phishing and other forms of social engineering, denial-of-service, credential stuffing, ransomware and other malware, insecure third-party libraries, application or network vulnerabilities, reliance on third-party vendors for patches, misconfigurations in cloud or SaaS environments, ineffective identity and access management practices, inadequate data discovery or deletion practices, employee error or malfeasance, and other sources of disruption or unauthorized access, and, as a result, unauthorized parties may be able to access our systems and data, including personal data and other sensitive and proprietary data, through our systems. Any actual or perceived breach or incident could interrupt our operations, harm our reputation, brand, and competitive position, result in our platform being unavailable, loss or improper access to, or unavailability of, data, fraudulent transfer of funds, regulatory investigations, proceedings, and significant legal, regulatory, and financial exposure.…

The on-demand local commerce category has grown rapidly since we launched our platform in 2013, but it is uncertain to what extent the market for local commerce platforms will continue to grow. The markets for certain services we facilitate, in particular convenience, grocery, advertising, and certain other categories, are in earlier stages of development than our restaurant category, and it is uncertain whether demand for these services will continue to grow and achieve stable, widespread market acceptance. In addition, through both organic and inorganic growth, we have entered geographies where the development of the on-demand local commerce category is in different stages of market acceptance. Our success will depend to a substantial extent on the willingness of people to widely adopt on-demand local commerce platforms. If merchants and consumers do not embrace the transition to on-demand local commerce platforms as we expect, including as a result of concerns regarding safety, affordability, or for other reasons, whether as a result of incidents on our platform or on our competitors’ platforms or otherwise, or instead adopt alternative solutions that may arise, then the market for our platform may not further develop or may develop slower than we expect, either of which could adversely affect our business, financial condition, and results of operations.

Our future success will depend in part on the continued service of our founders, senior management team, key technical employees, and other highly skilled employees, including Tony Xu, our co-founder and Chief Executive Officer, and on our ability to continue to identify, hire, develop, motivate, and retain talented employees. All of our U.S.-based employees, including our senior management team and Mr. Xu, work for us on an at-will basis, and there is no assurance that any such employee will remain with us. Our competitors may be successful in recruiting and hiring members of our management team or other key employees, and it may be difficult for us to find suitable replacements on a timely basis, on competitive terms, or at all. If we are unable to attract and retain the necessary employees, particularly in critical areas 25 Table of Contents of our business, we may not achieve our strategic goals. In addition, there may be changes in our senior management team that may be disruptive to our business. If our senior management team fails to work together effectively and to execute its plans and strategies, our business, financial condition, and results of operations could be adversely affected.

Our business depends on users' access to our platform via a mobile device or personal computer and the Internet. We also have integrations with or otherwise utilize or rely on PayPal, Stripe, Olo, Google Maps, Amazon Web Services ("AWS"), and a variety of other third-party vendors. Our business would be disrupted, and we may have to seek alternative service providers, if the Internet or any of the third-party software or services we utilize, or functional equivalents thereof, were unavailable due to, among other reasons, extended outages or interruptions or because they are no longer available on commercially reasonable terms or prices. Third-party software, applications, products, platforms, and services, and the terms on which they are offered, are constantly evolving, and we may not be able to maintain or modify our platform to ensure its compatibility with third-party offerings. Updates to third-party software that integrates with our offerings could cause our platform to not operate as efficiently as it previously had or at all. In addition, some of our competitors or merchants on our platform may take actions that disrupt the interoperability of our platform with their own products or services, or exert strong business influence on our ability to operate and distribute our platform.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
