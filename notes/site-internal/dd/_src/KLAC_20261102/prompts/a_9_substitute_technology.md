你是 stock-analyst v20 DD 的證據採集子 agent。標的：KLAC。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - KLA product substitute technology threat 2026
  - Semiconductor Equipment & Materials alternative technology disruption 2026 2027
  - KLAC KLA technology obsolescence risk
  - Semiconductor Equipment & Materials next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
5 Table of Contents Although we seek to reduce our dependence on sole and limited source suppliers, in some cases the partial or complete loss of certain of these sources, or disruptions within our suppliers’ often complex supply chains, could disrupt scheduled deliveries to customers, damage customer relationships and have a material adverse effect on our results of operations.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
Industry and Technology Risks •We may not be able to keep pace with trends and technological changes in the industries in which we operate; •We have a highly concentrated customer base; •Prevailing local and global economic conditions, semiconductor industry cyclicality, customer capital spending patterns and AI-related investment trends may negatively affect customer demand and purchasing decisions; and •We are exposed to risks related to the development, adoption, governance and use of AI by us, our competitors, customers, and other third parties.

Commerce may continue to add China-based entities to the U.S. Entity List and impose other end use or end user export restrictions, which could disrupt or prevent our product shipments to China-based entities, and further disrupt our revenue recognition, business operations and our ability to support our customers in China.

These rules and regulations may significantly harm our business unless we are able to obtain required licenses. We will continue to apply for export licenses, when required, in an effort to avoid disruption to our and our customers’ operations, but there can be no assurance that export licenses applied for by either us or our customers, now or in the future, will be granted. To the extent Commerce does issue licenses to us or to our customers, such licenses may have a short duration or require us to satisfy various conditions. If pending and future export license applications are not granted, or additional restrictions are imposed, or if regulators adopt new interpretations of existing regulations, the potential impact on us could be material by disrupting our supply chain and product shipment, impairing our ability to complete product development in a timely manner, or our ability to support existing customers of covered products or supply customers of covered products outside the impacted regions, and requiring us to transition certain operations out of one or more of the identified countries.…

We outsource a number of services to third-party service providers, which decreases our control over the performance of these functions. Disruptions or delays at our third-party service providers could adversely impact our operations.

In the conduct of our business, we and certain of our third-party providers collect, use, transmit and store data on information systems and networks, including systems, software, hardware and networks owned and maintained by KLA and/or by third-party providers (collectively, “IT Systems”). This data includes confidential information, transactional information and IP belonging to us, our customers and our business partners, as well as personal information of individuals (collectively, “Confidential Information”). We also integrate and use certain third-party services and products, including software, in our IT Systems, and such third-party products, services and systems are beyond our control. We face numerous and evolving cybersecurity risks that threaten the confidentiality, integrity and availability of our IT Systems and Confidential Information, including from diverse threat actors, such as state-sponsored organizations, opportunistic hackers and hacktivists, as well as diverse attack vectors, such as computer viruses, bugs, ransomware and other malware, technological errors and known and unknown vulnerabilities in our software and systems and those of third parties, cyber-related security breaches and similar disruptions from unauthorized intrusions, tampering, misuse or criminal acts made directly against our systems or networks, or 16 Table of Contents through our third-party providers or the supply chain, including social engineering, phishing, or other events or developments that we may be unable to anticipate or fail to mitigate, including, but not…

Any impact to the availability, integrity or confidentiality of our IT Systems or Confidential Information can materially adversely impact our business, operations and financial condition directly, or indirectly by impacting third parties in the supply chain, including direct or sub-tier suppliers, in many potential ways: disruptions to operations; misappropriation, corruption or theft of Confidential Information; misappropriation of funds and Company assets; reduced value of our investments in research, development and engineering; litigation (including class action lawsuits) with, or payment of damages to, third parties; reputational damage; costs to comply with regulatory inquiries or actions; data privacy issues; costs to rebuild our IT Systems or restore our Confidential Information; and increased cybersecurity protection and remediation costs. Additionally, cybersecurity and data security and protection laws and regulations are evolving and present increasing compliance challenges, which may increase our costs, affect our competitiveness, cause reputational harm and expose us to substantial fines or other penalties.…

Our global operations are dependent upon certain information systems, including telecommunications, the internet, our corporate intranet, network communications, email and various computer hardware and software applications. System failures or malfunctions, such as difficulties with our customer and supplier relationship management systems, could disrupt our operations and our ability to timely and accurately process and report key components of our financial results. Our ERP system is integral to our ability to accurately and efficiently maintain our books and records, record transactions, provide critical information to our management, and prepare our financial statements. We are currently upgrading our ERP system, with implementation expected to be completed in the first quarter of fiscal year 2027. Implementation of an upgrade to an ERP system requires the investment of significant resources and could lead to data migration issues, administrative and technical problems, and delays. Moreover, once our ERP system is upgraded, it may not operate as we expect it to.…

Disruption of our manufacturing facilities, other operations, suppliers, or customers due to climate change, natural disasters, public health crises, terrorism, acts of war or other catastrophic events could result in order cancellations, delivery delays, supply chain disruption or loss of customers and could seriously harm our business.

We have significant manufacturing operations in the U.S., Singapore, Israel, China and various locations throughout Europe. In addition, our business is international in nature, with our sales, service and administrative personnel and our customers and suppliers located in numerous countries throughout the world. Operations at our manufacturing facilities and our assembly subcontractors and those of our suppliers, as well as our other operations and those of our customers, are subject to disruption for a variety of reasons, including work stoppages, acts of war, terrorism, public health crises, fire, earthquake, volcanic eruptions, drought, storms, extreme temperatures, energy shortages, spikes in energy demand or power blackouts, disruptions in the availability of water necessary for our operations, including in areas of relatively high water stress, flooding or other natural disasters. Certain of these events may become more frequent or intense as a result of climate change, or other environmental or social issues, which may in some instances also contribute to chronic changes such as sea-level rise or changes to meteorological or hydrological patterns that may also disrupt our or our suppliers’ operations or otherwise adversely impact our business.…

We maintain significant operations in Israel. Since the establishment of the State of Israel in 1948, a number of armed conflicts have taken place between Israel and its Arab neighbors, and a state of hostility varying in degree and intensity has led to security and economic challenges for Israel. Persistent hostilities involving Iran and Iran-backed groups, including Hezbollah in Lebanon, the Houthis in Yemen and Hamas in the Gaza Strip, have involved missile strikes against civilian targets in various 19 Table of Contents parts of Israel and attacks on marine vessels traversing the Red Sea. The recent escalation of conflicts in the region has heightened instability, disrupted airspace, and increased freight and insurance costs. Disruptions in shipping routes in the Red Sea could result in delays in shipping our products to customers, which could delay the timing of revenue recognition and create uncertainty related to timeliness of shipments from the region. In addition, some of our employees in Israel are obligated to perform annual reserve duty in the Israel Defense Forces, and may be called to active military duty in emergency circumstances.…

We are increasingly incorporating AI capabilities into the development of technologies and our business operations, and into our products and services. AI technology is complex and rapidly evolving, and may subject us to significant competitive, legal, regulatory and other risks. We cannot predict the pace or trajectory of AI development or the extent to which AI-driven disruption will affect the semiconductor industry, and AI technologies may disrupt the broader semiconductor supply chain and ecosystem in ways that are difficult to predict. The implementation of AI can be costly and there is no guarantee that our use of AI will enhance our technologies, benefit our business operations or produce products and services that are preferred by our customers. Our competitors may be more successful in their AI strategy and develop superior products and services with the aid of AI.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
