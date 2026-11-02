你是 stock-analyst v20 DD 的證據採集子 agent。標的：HLT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Hilton Worldwide Holdings product substitute technology threat 2026
  - Lodging alternative technology disruption 2026 2027
  - HLT Hilton Worldwide Holdings technology obsolescence risk
  - Lodging next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm｜as_of：2026-02-11
<<<
Career Opportunities, Development and Training We take a broad, long-term and business-aligned approach to develop a dedicated and collaborative workforce to better serve our guests. Our Pathway Programs help foster economic mobility in the communities in which we operate and create a more robust talent pipeline for our business drawing from untapped talent pipelines including veterans, which consists of individuals who have served in the military and the caregivers and spouses of those who have served in the military, as well as people with disabilities, youth and displaced persons.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm｜as_of：2026-02-11
<<<
Macroeconomic conditions, geopolitical activity, public health concerns and other factors beyond our control can reduce demand for hospitality products and services, including demand for rooms at our hotels. These factors include, but are not limited to: •changes in general economic conditions, including inflation, interest rates, supply chain disruptions, low consumer confidence, tariffs, increases in unemployment levels and depressed real estate prices resulting from the severity and duration of any downturn in the U.S. or global economy and financial markets; •conditions that negatively shape public perception of travel or result in temporary closures or other disruption at our hotel properties, including travel-related accidents, outbreaks of pandemic or contagious diseases, such as COVID-19; •geopolitical activity, political and social unrest and governmental action and uncertainty resulting from U.S. and global political and social trends and policies, including potential barriers to travel, trade and immigration; •wars, geopolitical conflict, political instability or civil unrest, terrorist activities or threats and resulting heightened travel security measures, any of which may foreclose travel to certain locales or decrease the appeal of travel among the general population; •the impact of U.S.…

The hospitality industry demands the use of sophisticated technology and systems for property management, brand assurance and compliance, procurement, finance, human resources, reservation systems, distribution of hotel resources to current and future customers and guest amenities and the operation of the Hilton Honors guest loyalty program. These technologies may require maintenance or refinements and upgrades, and third parties may cease support of systems that are currently in use. The development and maintenance of these technologies has required and may further require significant investment by us. As various systems and technologies become outdated or new technology is required, we may not be able to replace or introduce them as quickly as needed or in a cost-effective and timely manner. If we fail to keep pace with rapidly evolving technological developments in AI, our competitive position and business results may suffer. Our competitors or other third parties may incorporate AI into their operations more quickly or successfully than us, or develop superior offerings with the aid of AI, which could impair our ability to compete effectively and adversely affect our results of operations. In some cases, hotel owners may refuse to upgrade systems or deploy new technology to replace aging or end-of-life software and/or hardware.…

We depend heavily upon our information technology systems in the conduct of our business. We develop, own and license or otherwise contract for sophisticated technology systems and services for property management, brand assurance and compliance, procurement, finance, human resources, reservation systems, distribution of hotel resources to current and future customers and guest amenities and the operation of the Hilton Honors guest loyalty program. Such systems are subject to, among other things, damage or interruption from power outages, computer and telecommunications failures, computer viruses, third-party criminal activity including "ransomware" or other malware and natural and man-made disasters. We have a cold disaster recovery site in a separate location and cloud backup processes to provide continuous resilience of our core reservation, property management, distribution and financial systems, but certain of our data center operations are currently located in a single facility or with a single cloud-based provider. Although we continue to renovate and migrate portions of our operations to cloud-based providers while simultaneously building and operating new applications and services with those cloud-based providers, any loss or damage to our primary physical or cloud-based facilities could result in operational disruption and data loss as we transfer production operations to our disaster recovery site or cloud providers.…

We rely on third parties for the performance of a significant portion of our information technology functions worldwide. In particular, our loyalty platform, property management, reservation and distribution systems rely on data communications networks and systems operated by unaffiliated third parties and cloud providers. The success of our business depends in part on maintaining our relationships with these third parties and their continuing ability to perform these functions and services in a timely and satisfactory manner. If we experience a loss or disruption in the provision of any of these functions or services, or they are not performed in a satisfactory manner, we may have difficulty in finding alternate providers on terms favorable to us, in a timely manner or at all, and our business could be adversely affected.

We rely on certain vendors for traditional software and cloud/software-as-a-service operations to maintain and periodically upgrade many of these systems and applications so that they can continue to support our business. The software programs supporting many of our systems were licensed to us by independent software developers. The inability of these developers or us to continue to maintain and upgrade these information systems and software programs has impacted, and in the future could, disrupt or reduce, the efficiency of our operations if we were unable to convert to alternate systems in an efficient and timely manner. For example, in July 2024 a software update by CrowdStrike Holdings, Inc., a cybersecurity technology company, caused a global information technology outage. Although the outage did not have a material impact to our business, we were temporarily impacted by the outage, and similar software outages in the future could harm our operations and be material to us.

Cyber-attacks could have a disruptive effect on our business. From time to time we and our third-party service providers experience cyber-attacks, attempted and actual breaches of our or their information technology systems and networks or similar events, which could result in a loss of sensitive business or customer information, systems interruption or the disruption of our operations. The techniques that are used to obtain unauthorized access, disable or degrade service or sabotage systems change frequently and may be difficult to detect for long periods of time, and despite our deployment of cyber-attack prevention and detection techniques, we are accordingly unable to anticipate and prevent all data security incidents. We have in the past been subject to cyber-attacks and expect that we will be subject to additional cyber-attacks in the future and may experience data breaches, especially as the pace, scale and sophistication of cyber-attacks continue to increase across all industry sectors, including hospitality.

Even if we are fully compliant with legal standards and contractual or other requirements, we still may not be able to prevent security breaches involving sensitive data. The sophistication of efforts by hackers to gain unauthorized access to information systems has continued to increase in recent years and may continue to do so at an accelerating pace as criminals increasingly leverage generative and agentic AI-based technologies and services. Breaches, thefts, losses or fraudulent uses of customer, employee or company data could cause consumers to lose confidence in the security of our websites, mobile applications, point of sale systems and other information technology systems and, as a result of this loss in confidence, choose not to purchase from us. Such security breaches also could expose us to risks of data loss, business disruption, litigation, fines, regulatory charges and other costs or liabilities, any of which could adversely affect our business.

Our reservation system is an important component of our business operations and a disruption to its functioning could have an adverse effect on our performance and results.

A significant number of our employees and employees of our hotel owners are covered by collective bargaining agreements and similar agreements, including approximately 25 percent of people employed or managed by us globally and approximately 45 percent of people working in the U.S. as of December 31, 2025. If relationships with our employees or employees of our hotel owners or the unions that represent them become adverse, the properties we manage, franchise or lease have in the past and could in the future experience labor disruptions such as strikes, lockouts, boycotts and public demonstrations. A number of our collective bargaining agreements are in the process of being renegotiated, and, if more employees become unionized, we may be required to negotiate additional collective bargaining agreements in the future. Labor disputes, which may be more likely when collective bargaining agreements are being negotiated, could harm our relationship with our employees or employees of our hotel owners, result in increased regulatory inquiries and enforcement by governmental authorities and deter guests. Further, adverse publicity related to a labor dispute could harm our reputation and 24 reduce customer demand for our services.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HLT_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
