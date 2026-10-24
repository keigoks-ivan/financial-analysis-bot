你是 stock-analyst v20 DD 的證據採集子 agent。標的：ROP。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - product substitute technology threat 2026
  - alternative technology disruption 2026 2027
  - ROP technology obsolescence risk
  - next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/882835/000088283526000009/rop-20251231.htm｜as_of：2026-02-24
<<<
Acquisitions involve risks, including difficulties in the integration of the operations, technologies, services, and products of the acquired companies and the diversion of management’s attention from other business concerns. Although our management will endeavor to evaluate the risks inherent in any particular transaction, including but not limited to cybersecurity risks and susceptibility to market disruption from AI or otherwise, there are no assurances that we will properly ascertain all such risks. Acquisitions may involve significant cash expenditures, debt incurrences, equity issuances, and expenses. Difficulties encountered with acquisitions may have a material adverse effect on our business, financial condition, and results of operations.

We rely on information and technology, including third-party cloud computing platforms and other third-party business partners, for many of our business operations which could fail and cause disruption to our business operations.

Our business operations are dependent upon information technology networks and systems to securely transmit, process, and store information and to communicate among our locations around the world and with clients, suppliers, and business partners. A shutdown of, or inability to access, one or more of our facilities, a power outage, or a failure of one or more of our information technology, telecommunications, or other systems could significantly impair our ability to perform such functions on a timely basis. Our compliance, cybersecurity and data privacy programs, cybersecurity technology, and risk management cannot eliminate all system risk. Credential compromise and identity-based attacks represent risks, and while we deploy identity threat protection and multi-factor authentication across our enterprise systems, determined attackers may still gain unauthorized access through sophisticated credential theft, session hijacking, social engineering, or privilege escalation techniques. Cybersecurity incidents including ransomware attacks, insider threats, system disruptions, and configuration errors could result in the misappropriation or corruption of data and assets, or disruptions to our business strategy, results of operations, and financial condition, and may require notification to customers and regulators with associated investigation, remediation, and monitoring obligations.…

We rely on business partners such as third-party data centers and cloud platforms, such as Amazon Web Services, Google Cloud Platform, Microsoft Azure, and Oracle Cloud to host certain enterprise and customer systems. Our software development and business operations rely on open-source components, third-party software libraries, and vendor dependencies that could contain undisclosed vulnerabilities, be subject to supply chain attacks, or become unavailable, potentially affecting our products, hosted services, and internal systems. Our ability to monitor such third parties’ security measures and the full impact of the systemic risk is limited, and concentration with a limited number of providers increases exposure to outages and pricing changes. If any third-party system or cloud platform that we use is unavailable to us for any reason, our customers may experience service interruptions, which could significantly impact our operations, reputation, business, and financial results. Failure of our systems or those of our third-party service providers, may result in interruptions in our service and loss of data or processing capabilities, all of which may cause a loss in customers, refunds of product fees, and/or material harm to our reputation and operating results. While certain of our businesses have experienced temporary disruptions, their impact has been limited and did not have a significant impact on our businesses.

Global cybersecurity threats are rapidly evolving and attacks to identities, networks, platforms, systems, and endpoints can range from uncoordinated individual attempts to sophisticated and targeted measures known as advanced persistent threats, directed at the Company, its businesses, its customers, and/or its third-party service providers, including, but not limited to, cloud providers and providers of network management services. These may include such things as unauthorized access, phishing attacks, denial of service, insider threats, data exfiltration and extortion, introduction of malware or ransomware, and other disruptive problems caused by threat actors. We face emerging risks from AI-powered attacks, including deepfakes used to impersonate executives or customers, AI-assisted social engineering, prompt injection attempts against AI systems, and data poisoning targeting machine learning models. These sophisticated attack techniques may bypass traditional security controls. Additionally, zero-day vulnerabilities, which are previously unknown security flaws with no available patches, pose risks that cannot be fully mitigated through our standard vulnerability management processes, requiring rapid detection and response capabilities to minimize potential damage. While we have experienced and expect to continue to experience these types of cybersecurity threats and incidents, none of them to date have been material to the Company.

10 We seek to deploy measures to protect, detect, respond, and recover from cybersecurity threats and incidents, including identity and access controls, employee training, data protection, vulnerability management, incident response, secure product development, continuous monitoring of our networks, platforms, endpoints, and systems, and maintenance of ransomware resilient backup and recovery capabilities. Our customers are increasingly requiring cybersecurity protections and mandating cybersecurity standards in our products and services, and we may incur additional costs to comply with such demands. Despite these efforts, we can make no assurances that we will be able to mitigate, detect, prevent, timely and adequately respond, or fully recover from the negative effects of cybersecurity incidents, and such cybersecurity incidents, depending on their nature and scope, could potentially result in the misappropriation, destruction, corruption, or unavailability of critical data and confidential or proprietary information (our own or that of third parties) and the disruption of business operations. The potential consequences of a material cybersecurity incident include financial loss, reputational damage, damage to our IT systems, data loss, litigation, theft of intellectual property, regulatory fines, customer attrition, diminution in the value of our investments in research and development (“R&D”), and increased cybersecurity protection and remediation costs, which may not be fully covered by insurance and could adversely affect our competitiveness and results of operations.…

We rely on third-party AI platforms and services, including proprietary and open-source large language models and other AI technologies provided by companies such as OpenAI, Anthropic, Google, and Microsoft. These providers may change their terms of service, increase pricing, discontinue services, experience outages, decline to provide certain indemnities, or make changes to their AI models that adversely affect our products or operations. As AI becomes more central to our offerings, our exposure to pricing changes from these providers increases, and we may not be able to pass such cost increases on to our customers. We have limited control over these third-party AI systems and their updates, and any disruption in access to these services could have a significant impact on our business. The use of AI applications may result in cybersecurity incidents that implicate the personal data of end users of such applications. Any such cybersecurity incidents related to our use of AI applications could adversely affect our reputation and results of operations. AI also presents emerging ethical issues, and if our use of AI becomes controversial, we may experience brand, reputational, or competitive harm, or legal liability.

Our total assets reflect substantial intangible assets, primarily goodwill. At December 31, 2025, goodwill totaled $21,341.2 as compared to $19,881.5 of total stockholders’ equity, and represented approximately 62% of our total assets of $34,577.0. The goodwill results from our acquisitions, representing the excess purchase price over the fair value of the net identifiable assets acquired. We assess at least annually whether there has been an impairment in the value of our goodwill and other indefinite-lived intangible assets. If future operating performance at one or more of our business units were to fall significantly below current or expected levels, if competing or alternative technologies emerge, if discount rates rise, or if business valuations decline, we could incur a non-cash charge to operating income. Any determination requiring the write-off of a significant portion of goodwill or unamortized intangible assets would negatively affect our results of operations, the effect of which could be material.

The availability and prices of raw materials, parts, and components are subject to curtailment or change due to, among other things, suppliers’ allocations to other purchasers, interruptions in production by suppliers, supply chain delays and disruptions, component shortages, changes in exchange rates, and prevailing price levels. In addition, some of our products are provided by sole source suppliers and our SaaS offerings are increasingly reliant on a limited number of third-party cloud computing platforms, and transitioning to alternative suppliers or platforms may require significant time, redesign, and capital investment, or may not be feasible for certain products or services. Any changes in the supply of, or price for, these parts and components, as well as any increases in commodity prices, or the price and availability of, or any decrease in the reliability of, third-party cloud computing platforms could affect our business, financial condition, and results of operations.

15 Any business disruptions due to political instability, armed hostilities, incidents of terrorism, incidents of directed cyberattacks, public health crises, or extreme weather events or other natural disasters could adversely impact our financial performance.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
