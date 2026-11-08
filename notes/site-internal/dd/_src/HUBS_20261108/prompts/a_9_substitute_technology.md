你是 stock-analyst v20 DD 的證據採集子 agent。標的：HUBS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - HubSpot product substitute technology threat 2026
  - Software - Application alternative technology disruption 2026 2027
  - HUBS HubSpot technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm｜as_of：2026-02-11
<<<
We face intense competition from other software companies in the market we operate that provide interactive marketing services. Competition could significantly impede our ability to sell subscriptions to our customer platform on terms favorable to us. Our current and potential competitors may develop and market new technologies including as a result of new or better use of evolving AI technologies, whether through greater investments in AI development, access to higher quality training datasets, or more advanced AI models, that render our existing or future products less competitive, or obsolete. We may also face greater competition from non-specialist solutions relying on generic large language models (“LLMs”), generative AI and general-purpose agents to address a broad range of business needs. As we attempt to sell our products and solutions to new and existing customers, we must convince them that our products and solutions are superior to other solutions available to their organizations, including generic LLMs, software created using natural language prompts and generative AI (referred to as vibe coding) and other emerging technologies. In addition, if these competitors develop products with similar or superior functionality to our platform, we may need to decrease the prices or accept less favorable terms for our platform subscriptions in order to remain competitive.…

Our future success depends on our ability to adapt and innovate our customer platform. To attract new customers and increase revenue from existing customers, we need to continue to enhance and improve our offerings to meet customer needs at prices that our customers are willing to pay. Such efforts will require adding new functionality and responding to technological advancements, including AI and machine learning, which will increase our research and development costs. Further, any third-party AI technologies leveraged in our products and services may not be available on commercially reasonable terms or at all and any loss of rights to use such technologies may significantly increase our expenses or otherwise disrupt or delay the provisioning of our products and services to customers. If we are unable to develop, license or acquire new applications that address our customers’ needs, or to enhance and improve our platform in a timely manner, we may not be able to maintain or increase market acceptance of our platform. Our ability to grow is also subject to the risk of future disruptive technologies. Access and use of our customer platform is provided via the cloud, which, itself, was disruptive to the previous enterprise software model.…

The Company’s inability, for technological, legal or other reasons, some of which may be beyond the Company’s control, to enhance, develop, introduce and monetize products and services in a timely manner, or at all, in response to changing market conditions or customer requirements could have a material adverse effect on the Company’s business, results of operations and financial condition or could result in its products and services not achieving market acceptance or becoming obsolete. In addition, if the Company fails to deliver a compelling customer experience or accurately predict emerging technological trends and the changing needs of customers and end users, or if the features of its new products and services do not meet the demands of its customers or are not sufficiently differentiated from those of its competitors, the Company’s business, results of operations and financial condition could be materially harmed.

Our customer platform and its underlying infrastructure are inherently complex and may contain material defects or errors. We release modifications, updates, bug fixes and other changes to our software several times per day, without traditional human-performed quality control reviews for each release. While we seek to implement secure development practices, we cannot eliminate the risk that our applications may have vulnerabilities. From time to time, we find defects in our software and may discover in the future additional defects, outages, delays or cessations of service, performance and quality problems or may produce errors in connection with systems integrations, migration work or other causes, which could result in business disruptions and the process of remediating them could be more expensive, time-consuming, disruptive and resource intensive than planned. Such disruptions could adversely impact our internal operations and interrupt other processes. Delayed sales, lower margins or lost customers resulting from these disruptions could reduce our revenue, increase our expenses, damage our reputation and adversely affect our cash flows and stock price.

We rely on data provided by third parties, the loss of which could limit the functionality of our platform and disrupt our business.

Cyber-attacks, denial-of-service attacks, ransomware attacks, supply chain attacks, business email compromises, computer malware, viruses, wrongful intrusions, data breaches social engineering (including phishing), and other compromises are prevalent in our industry, the industries of certain of our service providers and our customers' industries. Like other companies in our industry, we and our third party vendors have in the past experienced threats and security incidents related to our data and systems, and we may in the future experience other threats, compromises, breaches, or incidents. Attempts to disrupt or gain unauthorized access to our and our third-party vendors’ information systems from malicious third parties or insider threats may incorporate widely varying and frequently changing tactics, which may be enhanced or facilitated by AI. Our internal computer systems and those of our current and any future strategic collaborators, vendors, and other contractors or consultants are vulnerable to damage from cyber-attacks, attacks enhanced or facilitated by AI, computer viruses, unauthorized access, natural disasters, cybersecurity threats, terrorism, geopolitical conflict, war and telecommunication and electrical failures.…

Recent cybersecurity incidents and compromises affecting large institutions, including an incident that affected us in 2024, suggest that the risk of such events is significant, even if privacy protection and security measures are implemented and enforced. A cyber-attack, incident, or compromise could result in a material disruption of our development programs and our business operations, whether due to a loss of our trade secrets or other proprietary information or other disruptions. These cyber-attacks could be carried out by threat actors of all types (including but not limited to nation states, organized crime, other criminal enterprises, individual actors, malicious insiders, and/or advanced persistent threat groups). In addition, we may experience intrusions on our physical premises by any of these threat actors. To the extent that any compromise, disruption or security breach were to result in a loss of, or damage to, our data or applications, or inappropriate disclosure of confidential or proprietary information, we could incur liability, incur significant costs associated with remediation and the implementation of additional security measures, including costs to deploy additional personnel and protection technologies, train employees, and engage third-party experts and consultants, and our competitive position could be harmed.…

We rely on our network infrastructure and enterprise applications, internal technology systems and website for our development, marketing, operations, support, hosted services and sales activities. In addition, some of our businesses rely on third-party hosted services, and we do not control the operation of third-party data center facilities serving our customers from around the world, which increases our vulnerability. A disruption, infiltration or failure of these systems or third-party hosted services in the event of a major earthquake, fire, flood, tsunami or other weather event, power loss, telecommunications failure, software or hardware malfunctions, pandemics, cyber-attack, war, terrorist attack or other catastrophic event that we do not adequately address, could cause system interruptions, reputational harm, loss of intellectual property, delays in our product development, lengthy interruptions in our services, breaches of data security and loss of critical data. Any of these events could prevent us from fulfilling our customer demands or could negatively impact a country or region in which we sell our products, which could in turn decrease that country’s or region’s demand for our products.…

While we seek to partner with organizations that mitigate their business risks associated with climate change, we recognize that there are inherent risks wherever business is conducted, including risks relating to the physical impact of climate change and to transitioning to a lower carbon economy. Any of our primary locations may be vulnerable to the adverse effects of climate change. For example, our offices globally may experience climate-related events at an increasing frequency, including drought, water scarcity, heat waves, cold waves, wildfires and resultant air quality impacts and power shutoffs associated with wildfire prevention. While this danger has a low-assessed risk of disrupting normal business operations, it has the potential to disrupt employees’ abilities to commute to work or to work from home and stay connected effectively. Furthermore, it is more difficult to mitigate the impact of these events on our employees to the extent they work from home. Climate-related events, including the increasing frequency of extreme weather events and their impact on the U.S.’s, Europe’s and other major region’s critical infrastructure, have the potential to disrupt our business, our third-party suppliers and/or the business of our customers, and may cause us to experience higher attrition of our employees, losses and additional costs to maintain or resume operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
