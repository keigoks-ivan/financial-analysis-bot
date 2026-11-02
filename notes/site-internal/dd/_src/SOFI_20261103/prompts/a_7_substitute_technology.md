你是 stock-analyst v20 DD 的證據採集子 agent。標的：SOFI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - SoFi Technologies product substitute technology threat 2026
  - Credit Services alternative technology disruption 2026 2027
  - SOFI SoFi Technologies technology obsolescence risk
  - Credit Services next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm｜as_of：2026-02-17
<<<
Competition to fund prime loans. The prime lending market is highly fragmented and competitive. We face competition from a diverse landscape of consumer lenders, including other banks, credit unions and specialty finance lenders, as well as alternative technology-enabled lenders.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm｜as_of：2026-02-17
<<<
37 SoFi Technologies, Inc. TABLE OF CONTENTS Galileo and Technisys depend on a small number of clients, the loss or disruptions in operations of any of which could have a material adverse effect on their businesses and financial results, and negatively impact our financial results and results of operations.

Galileo and Technisys revenue from clients is highly concentrated and a significant Galileo client recently moved to a competitor. There are inherent risks whenever a large percentage of net revenue is concentrated with a limited number of clients, including fluctuations in revenue, the loss of any one or more of those clients as a result of bankruptcy or insolvency proceedings involving the client, the loss of additional clients to a competitor, harm to that client’s reputation or financial prospects or other reasons, including adverse general economic conditions affecting Galileo and Technisys clients many of which are fintechs and other financial services firms. Any further reduction in the amount of revenue that we derive from these clients, without an offsetting increase in new sales to other clients, has had and could have a material adverse effect on our operating results in the future. A significant change in the liquidity or financial position of our clients could also have a material adverse effect on our liquidity and our future operating results. In addition, disruptions in the operations of certain of Galileo’s key clients have had an adverse impact on Galileo, and any future disruptions in the operations of any key Galileo or Technisys clients could be material and have an adverse impact on our results of operations.

In particular, markets in the U.S. or abroad have been and may in the future be affected by the level and volatility of interest rates, availability and market conditions of financing, recessionary pressures, inflation and hyperinflation, supply chain disruptions, changes in consumer spending, employment levels, labor shortages, changes to fiscal policy, including expansion of U.S. federal deficit spending and resultant debt issuance, federal government shutdowns, developments related to the U.S. federal debt ceiling, changes in legislation, regulations or policy, energy prices, home prices, commercial property values, bankruptcies, a default by a significant market participant or class of counterparties, market volatility, liquidity of the global financial markets, the growth of global trade and commerce, exchange rates, trade policies, the availability and cost of capital and credit, disruption of communication, transportation or energy infrastructure and investor sentiment and confidence. Additionally, global markets have been and may in the future be adversely affected by the current or anticipated impact of climate change, extreme weather events or natural disasters, the emergence or continuation of widespread health emergencies or pandemics, cyberattacks or campaigns, military conflict (e.g., the confrontation in Venezuela, the ongoing conflict in the Middle East and the ongoing war in Ukraine), terrorism or other geopolitical events which may affect our results of operations.…

Occurrences of epidemics or pandemics, depending on their scale, may cause different degrees of disruption to the regional, state and local economies in which we offer our products and services. For example, the COVID-19 pandemic caused changes in consumer and student behavior, as well as economic disruptions. Any future pandemic or public health crisis may result in, among other impacts, worker shortages, supply chain issues, inflationary pressures, and the reinstatement and subsequent lifting of restrictions and health and safety related measures. Any future epidemics or pandemics or other public health crises could adversely affect our business, operations and financial condition, as well as the business, operations and financial conditions of our members, other customers and partners.

Strategic and New Product Risks We have in the past consummated, and from time to time we may evaluate and potentially consummate, acquisitions, which could require significant management attention, disrupt our business and adversely affect our financial results.

TABLE OF CONTENTS unintentional actions could also give rise to significant disruptions to our operations. In addition, the long-term effects of climate change on the global economy and our industry in particular are unclear, however we recognize that there are inherent climate-related risks wherever business is conducted. For example, our offices may be vulnerable to the adverse effects of climate change. We have large offices located in the San Francisco Bay Area, Salt Lake City, Utah, and Jacksonville, Florida, regions that are prone to events such as seismic activity and severe weather, that have experienced and may continue to experience, climate-related events and at an increasing rate. Examples include drought and water scarcity, hurricanes, warmer temperatures, wildfires and air quality impacts and power shut-offs associated with wildfire prevention and hurricanes. The increasing intensity of drought throughout California and Utah and annual periods of wildfire danger, and the increasing intensity of hurricanes in Florida, increase the probability of planned power outages. Although we maintain a disaster response plan and insurance, such events could disrupt our business, the business of our partners or third-party suppliers, and may cause us to experience losses and additional costs to maintain and resume operations.…

Despite the implementation of security measures, our internal computer and information technology systems and infrastructure and those of our third-party service providers and other contractors and consultants upon which our business relies have experienced and are at constant risk of cyber-attacks or cyber intrusions via viruses, worms, break-ins, breakdown, wrongful intrusions, wrongful conduct by insider employees or vendors, malware, ransomware and other malicious software programs, attacks enhanced or facilitated by AI, social engineering (including phishing attacks), business email compromises, hacking, data breaches, denial-of-service attacks or other attacks and similar disruptions from the unauthorized use of or access to computer systems (including from internal and external sources) that attack our products or otherwise exploit any vulnerabilities in our systems or those of our third-party service providers, or attempt to fraudulently induce our members, prospective members, technology platform clients and the customers of our technology platform clients, employees, third-party service providers or others to disclose passwords or other sensitive information or unwittingly provide access to our systems or data. Furthermore, these attempts to disrupt or gain unauthorized access to our and our third-party service providers’ information systems from malicious third parties or insider threats may incorporate widely varying and frequently changing tactics, which may be enhanced or facilitated by AI.…

Disruptions in the operation of our computer systems and third-party data centers and service providers could have an adverse effect on our business.

Our ability to deliver products and services to our members and clients, and otherwise operate our business and comply with applicable laws, depends on the efficient and uninterrupted operation of our computer systems and third-party data centers, as well as third-party service providers. Our computer systems and third-party providers may encounter service interruptions at any time due to system or software failure or errors, employee misconfiguration of resources or misdirected communications, natural disasters, severe weather conditions, health pandemics, terrorist attacks, cyberattacks or other events. For example, in September 2023, the SoFi Invest platform experienced a service interruption that resulted in certain of our members being unable to view certain of their account information and unable to buy and sell securities and other financial products on our platform for a period of time. Any such events, including persistent interruptions or perceptions of such interruptions whether true or not, in our products and services could cause members to believe that our products and services are unreliable, leading them to switch to our competitors or to otherwise avoid our products and services, and otherwise have a negative effect on our business and technology infrastructure (including our computer network systems), which could lead to member dissatisfaction or long-term disruption of our operations.…

Additionally, our reliance on third-party providers may mean that we will not be able to resolve operational problems internally or on a timely basis, as our operations will depend upon such third-party service providers communicating appropriately and responding swiftly to their own service disruptions through industry standard best practices in business continuity and/or disaster recovery. As a last resort, we may rely on our ability to replace a third-party service provider if it experiences difficulties that interrupt operations for a prolonged period of time or if an essential third-party service terminates. If these service arrangements are terminated for any reason without an immediately available substitute arrangement, our operations may be severely interrupted or delayed. If such interruption or delay were to continue for a substantial period of time, our business, prospects, financial condition and results of operations could be adversely affected.

TABLE OF CONTENTS better ones become available. A failure to maintain and/or improve current technology and business processes could cause disruptions in our operations or cause our solution to be less competitive, all of which could have a material adverse effect on our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/parts/axes_7.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
