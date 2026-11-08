你是 stock-analyst v20 DD 的證據採集子 agent。標的：APP。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - AppLovin product substitute technology threat 2026
  - Advertising Agencies alternative technology disruption 2026 2027
  - APP AppLovin technology obsolescence risk
  - Advertising Agencies next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm｜as_of：2026-02-19
<<<
The advertising and mobile app ecosystems are prone to cyberattacks by third parties seeking unauthorized access to our data or the data of our clients or their end users or to disrupt our ability to provide service. Our advertising solutions, and other offerings involve the collection, storage, transmission, and other processing of a large amount of data, including personal information, and we and our third-party service providers otherwise store and process information, including our confidential and proprietary business information, and personal information and other information relating to our employees, clients or other third parties. We also store and implement measures designed to secure the source code for our advertising solutions as they are created. Any failure to prevent or mitigate security breaches or incidents impacting our advertising solutions, or our systems or other systems used in our business, or improper access to or disclosure of our data, including source code, or user data, including personal information, or information from clients or other third parties, that is stored or otherwise processed in our business could result in the unauthorized loss, modification, disclosure, destruction, or other unauthorized processing of such data, or unavailability of data or of our advertising solutions, or other offerings.…

Malware (including ransomware), viruses, social engineering (predominantly spear phishing attacks or smishing), and general hacking have become more prevalent in the advertising and mobile app ecosystems. Some of these have occurred on our systems and otherwise in our business in the past, and we expect they will continue to occur in the future. We regularly encounter attempts to create false or undesirable client accounts or take other actions for purposes such as spamming or other objectionable ends. Any actual or attempted breaches, incidents, or attacks may cause disruptions or interruptions to our advertising solutions, or other offerings, degrade the user experience, impair, disrupt, or interrupt our systems and networks and other systems and networks used in our business, or adversely affect our reputation, business, financial condition, and results of operations. Our efforts to protect our advertising solutions, and other offerings, our systems and other systems used in our 10 Table of Contents business, and our data, user data, and information from clients, partners, and other third parties, and to disable or otherwise respond to undesirable activities on our offerings, may also be unsuccessful due to software bugs or other technical defects, errors, or malfunctions; employee, contractor, vendor, or partner error or malfeasance, including defects or vulnerabilities in information technology systems or offerings; cyberattacks, including attacks designed to disrupt systems or…

Additionally, our advertising solutions and other offerings operate in conjunction with, and we are in some cases dependent upon, third-party products, services, and components. Our ability to monitor our third-party service providers’ data security is limited, and in any event, attackers may be able to circumvent our third-party service providers’ data security measures. There have been and may continue to be significant attacks on certain third-party providers, and we cannot guarantee that our or our third-party providers’ systems and networks have not been breached or compromised or do not contain defects or bugs that could result in a disruption, breach, or other incident impacting our systems and networks or those of third parties that support us and our advertising solutions. Security vulnerabilities, malicious code, errors, or other bugs or defects in these third-party products, services, and components could cause us to face increased costs, claims, liability, and additional or new obligations, reduced revenue, and harm to our reputation or competitive position. We and our service providers may be unable to anticipate these techniques, react, remediate or otherwise address any security vulnerability, breach or other security incident in a timely manner, or implement adequate preventative measures.

Our future success depends in significant part on the continued service of our key management and engineering personnel, including our co-founder, CEO, and Chairperson, Adam Foroughi. Our ability to compete and grow depends in part on the efforts and talents of these employees and executives, who are important to our vision, strategic direction, culture, products, and technology. We do not have employment agreements, other than offer letters, with Mr. Foroughi or other members of our senior management team, and we do not maintain key-man insurance for members of our senior management team. The loss of Mr. Foroughi or any other member of our senior management team could cause disruption and adversely affect our business, financial condition, or results of operations.

The advertising ecosystem is subject to rapid technological change, and if we do not adapt to, and appropriately allocate our resources among, emerging technologies and business models, our business, financial condition, and results of operations could be adversely affected.

Our business also currently depends in part on the growth and evolution of the internet, especially mobile internet-enabled devices. The number of people using mobile internet-enabled devices has increased rapidly over time, and we expect that this trend will continue. However, the markets in which we operate may not grow in the way we anticipate. We must continually anticipate and adapt to emerging technologies to stay competitive, including the development of AI and its impacts on the advertising ecosystem. As the technological infrastructure for internet access improves and evolves, consumers will be presented with more opportunities to access apps and play games on a variety of devices and platforms and to experience other leisure activities that may compete with mobile apps. Forecasting the financial impact of these emerging technologies and business models is inherently uncertain and volatile. If we decide to support a new technology or business model in the future, it may require partnering with a new platform, technology, or business partner, which may be on terms that are less favorable to us than those for traditional technologies or business models.

To invest in a new technology, enter a new market or expand our offerings, we must invest financial resources and management attention. We may invest significant resources in a new offering, entering a new market or in a strategic acquisition or partnership, which could prove unsuccessful or prevent us from directing these resources towards other opportunities. We may never recover the often-substantial up-front costs of developing and marketing emerging technologies or business models, or recover the opportunity cost of diverting management and financial resources. Further, our competitors may adopt an emerging technology or business model more quickly or effectively than we do, creating products that are technologically superior to ours or attract more users than ours.

Our reputation and ability to attract and retain our clients depends in part on the reliable performance of our advertising solutions. We have in the past experienced, and may in the future experience, interruptions in the availability or performance of our offerings from time to time. Our systems may not be adequately designed or may not operate with the reliability and redundancy necessary to avoid performance delays or outages that could be harmful to our business. If our offerings are unavailable when clients attempt to access them, or if they do not load as quickly as expected, clients may not use our offerings as often in the future, or at all, which could adversely affect our business and results of operations. As we continue to grow, we will need an increasing amount of technical infrastructure, including network capacity and computing power, to continue to satisfy our needs and the needs of our clients. Additionally, we rely on certain third-party providers for our increasing network capacity and computing power needs, and if we fail to properly anticipate our needs or secure sufficient capacity at a reasonable cost, our ability to scale and grow our business, or our profitability, could be negatively impacted.…

We face risks related to our strategic transactions, which may not achieve our strategic objectives, may disrupt our operations or result in unexpected liabilities or expenses.

Additionally, the failure of third-party business partners to provide or maintain adequate services and technologies could result in a disruption to our business operations. While not material to our business to date, we experience from time to time disruptions from third parties with whom we do business, including failure to uphold contractual obligations, violations of our policies and terms of use, and other actions described in this risk. Actions by these third parties may directly or indirectly cause harm to our business, reputation, financial condition and results of operations.

From time to time, we have faced, and we may face in the future, allegations that we have infringed the trademarks, copyrights, patents, and other intellectual property rights of third parties, including from our competitors, non-practicing entities and former employers of our personnel. Intellectual property litigation may be protracted and expensive, and the results are difficult to predict. As a result of any court judgment or settlement, we may be obligated to alter our advertising solutions, in a particular geographic region or worldwide, pay royalties or significant settlement costs, purchase licenses, or develop substitutes.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
