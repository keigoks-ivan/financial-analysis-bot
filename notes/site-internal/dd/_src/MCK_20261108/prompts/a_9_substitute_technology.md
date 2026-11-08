你是 stock-analyst v20 DD 的證據採集子 agent。標的：MCK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - McKesson product substitute technology threat 2026
  - Pharmaceutical Distribution + Specialty Solutions alternative technology disruption 2026 2027
  - MCK McKesson technology obsolescence risk
  - Pharmaceutical Distribution + Specialty Solutions next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
Additionally, we compete with other service providers and healthcare manufacturers, as well as potential customers who may choose to build internal supply management capabilities rather than rely on external partners like us. We believe that our scale and the breadth of our product and service portfolio are key competitive advantages. In all areas, primary competitive factors include price, quality of service, product assortment, innovation, adoption of emerging technologies, and, in some cases, customer convenience.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
Item 1A Index McKESSON CORPORATION Litigation and Regulatory Risks We experience costly and disruptive legal disputes.

We are routinely named as a defendant in litigation or regulatory proceedings and other legal disputes, which may include asserted class action litigation, such as those described in Financial Note 17, “Commitments and Contingent Liabilities,” to the consolidated financial statements included in this Annual Report. Regulatory proceedings involve allegations such as false claims, healthcare fraud and abuse, and violations of competition laws. Civil litigation proceedings involve commercial, employment, environmental, intellectual property, tort, and other claims. Despite valid defenses that we assert, legal disputes are often costly, time-consuming, distracting to management, and disruptive to normal business operations. The uncertainty and expense associated with unresolved legal disputes might harm our business and reputation even if the matter ultimately is favorably resolved. The outcome of legal disputes is difficult to predict, and outcomes may occur that we believe are not justified by the evidence or existing law. Outcomes include monetary damages, penalties and fines, and injunctive or other relief that requires us to change our business operations, practices, or arrangements and incur significant expense. Accordingly, legal disputes might have a materially adverse impact on our reputation, our business operations, and our financial position or results of operations.

We, our external service providers, vendors, and other third parties with which we do business, use technology and systems to perform our business operations, such as the secure electronic transmission, processing, storage, and hosting of sensitive information, including protected health information and other types of personal information, confidential financial information, proprietary information, and other sensitive information relating to our customers, company, and workforce. Despite our physical, technical, and administrative security measures as well as third party risk management processes as discussed in “Cybersecurity” in Item 1C of Part I below, technology systems and operations of the Company and third parties, including our external service providers and vendors, with which we do business, have experienced cybersecurity incidents and are subject to future cyberattacks and cybersecurity incidents. Companies in the healthcare industry are increasingly targeted for cyberattacks. Cybersecurity incidents include unauthorized occurrences on or conducted through our or our third parties’ information systems, such as tampering, malware insertion, ransomware attacks, or other system integrity events.…

We experience significant problems with information systems or networks. We rely on sophisticated information systems and networks to perform our business operations, such as to obtain, rapidly process, analyze, and manage data that facilitate the purchase and distribution of thousands of inventory items from distribution centers. We provide remote services that involve hosting customer data and operating software on our own or third-party systems. Our customers rely on their ability to access and use these systems, and their data, as needed, and our ability to compete effectively is increasingly dependent on access to, and interpretation of, data. Data quality impacts customer ordering, order fulfillment and higher order processing. If we fail to effectively implement and maintain data governance structures across our businesses, to effectively interpret and utilize such data, or protect the integrity of such data, including systems powered by or incorporating AI and machine learning, our operations could be impacted, and we may be at a competitive disadvantage. Our networks and hosting systems are also vulnerable to interruption or damage from sources beyond our control.…

We distribute pharmaceutical, medical, and other FDA-regulated products manufactured by third parties and by our private label businesses, including medications that may be temperature sensitive or have limited shelf lives. Our systems and procedures are designed to maintain the safety and efficacy of the products throughout the sourcing and distribution process. Issues affecting product safety or efficacy can arise from manufacturing, storing, distributing, dispensing, or using products, and can result in adverse consequences such as safety alerts, seizures, bans, recalls, withdrawals or other market action, suspensions, and other regulatory actions and sanctions, civil lawsuits, increased costs, disruptions, delays, and reputational damage. Any of these types of issues or results might have a materially adverse impact on our reputation, our business operations, and our financial position or results of operations.

We might not realize expected benefits from business process initiatives. From time to time, we implement restructuring, cost reduction, or other business process initiatives that result in significant charges and expenses. These initiatives might fail to achieve our desired objectives or have unintended consequences such as distraction of our management and employees, business disruption, attrition beyond any planned reduction in workforce, inability to attract or retain key personnel and reduced employee productivity. Any of these risks might have a materially adverse impact on our business operations and our financial position or results of operations.

We are adversely impacted by competition and industry consolidation. Our businesses face a highly competitive global environment with strong competition from international, national, regional, and local full-line, short-line, and specialty distributors, service merchandisers, self-warehousing chain drug stores, manufacturers engaged in direct distribution, third-party logistics companies, and large payer organizations. In addition, our businesses face competition from various other service providers and from pharmaceutical and other healthcare manufacturers as well as other potential customers, which may from time to time decide to develop, for their own internal needs, supply management capabilities that might otherwise be provided by our businesses. We also may face competition from companies that move faster to adopt emerging technologies. Due to consolidation, a few large suppliers control a significant share of the pharmaceuticals market. This concentration reduces our ability to negotiate favorable terms with suppliers and causes us to depend on a smaller number of suppliers. Many of our customers, including healthcare organizations, have consolidated or joined group purchasing organizations and have greater power to negotiate favorable prices. Consolidation by our customers, suppliers, and competitors might reduce the number of market participants and give the remaining enterprises greater bargaining power, which might lead to erosion in our profit margin. Consolidation might increase counterparty credit risk because credit purchases increase for fewer market participants.…

We rely on third parties for the supply of pharmaceutical and other products, and our operations are subject to our suppliers’ continued ability to supply the products that we require. From time to time, we experience difficulties and delays in sourcing and selling products due to a variety of causes that result in suppliers’ failure to satisfy production demand. Among these causes are suppliers’ challenges in complying with legal requirements (including product and production quality standards), access to raw materials, inputs, and finished goods, manufacturing shutdowns, and operational and systems difficulties. Supply disruptions also arise from other factors beyond our control, such as product rationalization; government actions or policies (including trade sanctions, tariffs and other trade restrictions, as well as the requisition, diversion, or allocation of inventory); shifts in customer or societal demand for products; labor disputes or shortages; ethical sourcing issues; supplier financial distress; natural disasters and weather-related events; civil unrest; military conflicts; and epidemics or pandemics. In these types of situations, our alternative sourcing efforts are not always fully successful. We might experience extended delays or incur higher sourcing costs or suffer harm to our customer relationships and reputation. Furthermore, changes in the healthcare industry’s or our suppliers’ pricing, selling, inventory, distribution, or supply policies or practices could significantly reduce our revenues and net income.…

From time to time we are adversely affected by conditions and events outside of our control, including: widespread public health issues such as epidemic or pandemic infectious diseases; natural disasters and other catastrophic events such as earthquakes, floods, or severe weather; and geopolitical factors such as terrorism, military conflicts, civil unrest, political circumstances (including changes in international relations), changes or uncertainty in government policies (including with respect to U.S. or international trade), actual or announced tariffs or other trade restrictions, government shutdowns, or changes in laws or their interpretation. These conditions and events can disrupt operations for us, our suppliers, our vendors, and our customers, as well as impair product manufacturing, supply, and transport availability and cost in unpredictable ways that depend on highly uncertain future developments. They might affect consumer confidence levels and spending or the availability of certain goods, commodities, raw materials, and other inputs. In response to these types of conditions and events, we might seek alternate sources for product supply, incur additional sourcing or distribution costs, suspend operations, implement extraordinary procedures, or suffer consequences that are unexpected and difficult to mitigate. For example, the trade environment remains highly dynamic and uncertain, and trade policies may be interrelated with other government initiatives.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
