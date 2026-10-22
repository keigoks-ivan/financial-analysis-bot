你是 stock-analyst v20 DD 的證據採集子 agent。標的：GM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - General Motors product substitute technology threat 2026
  - Auto Manufacturers alternative technology disruption 2026 2027
  - GM General Motors technology obsolescence risk
  - Auto Manufacturers next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
In some instances, we purchase systems, components, parts, and supplies from a single source, which may increase risk to supply disruptions. The inability or unwillingness of these sources to provide us with parts and supplies could have a material adverse effect on our production. Combined purchases from our two largest suppliers overall were approximately 12% of our total purchases in the year ended December 31, 2025, and approximately 11% of our total purchases in each of the years ended December 31, 2024 and 2023. Refer to Item 1A. Risk Factors for further discussion of these risks.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
Item 1A. Risk Factors We have listed below the most material risk factors applicable to us. These risk factors are not necessarily in the order of importance or probability of occurrence: Risks related to our competition and strategy If we do not deliver new products, services, technologies, and customer experiences in response to increased competition and changing consumer needs and preferences, our business could suffer. We believe that the automotive industry will continue to experience significant change in the coming years, particularly as traditional automotive original equipment manufacturers (OEMs) shift resources and strategies in response to changes in the regulatory landscape and evolving consumer preferences. In addition to our traditional competitors, we must also be responsive to the entrance of start-ups and other non-traditional competitors in the automotive industry, such as software and ridesharing services supported by large technology companies. These new competitors, as well as established industry participants, are disrupting the historic business model of our industry through the introduction of new technologies, products, services, direct-to-consumer sales channels, methods of transportation, and vehicle ownership.…

Our ability to attract and retain talented and highly skilled employees is critical to our success and competitiveness. Attracting and retaining employees who are highly skilled in their areas is critical to thriving in an increasingly competitive landscape. In particular, our vehicles and connected services increasingly rely on software and hardware that is highly technical and complex, and our success in this area is dependent upon our ability to retain and recruit the best talent. The market for highly skilled workers and leaders in our industry is extremely competitive. In addition to compensation considerations, current and potential employees are increasingly placing a premium on culture and other various intangibles, such as working for companies with a clear purpose and strong brand reputation, flexible work arrangements, and other considerations. Failure to attract, hire, develop, motivate, and retain highly qualified employees could disrupt our operations and adversely affect our strategic plans.

Any significant disruption at one of our manufacturing facilities could disrupt our production schedule. We assemble vehicles at various facilities around the world. Our facilities are typically designed to produce particular models for particular geographic markets. No single facility is designed to manufacture our full range of vehicles. In some cases, certain facilities produce products, systems, components, and parts that disproportionately contribute a greater degree to our profitability than others and create significant interdependencies among manufacturing facilities around the world. When these or other facilities become unavailable, either temporarily or permanently and for any number of reasons, including labor disruptions or shortages, supply chain disruptions, the occurrence of a public health crisis, or catastrophic weather events, whether or not as a result of climate change, the inability to manufacture at the affected facility has resulted, and may in the future result, in harm to our reputation, increased costs, lower revenues, and the loss of customers. We may not be able to easily shift production to other facilities or to make up for lost production. Any new facility needed to replace an inoperable manufacturing facility would need to comply with the necessary regulatory requirements and applicable labor agreements, need to satisfy our specialized manufacturing requirements, and require specialized equipment.

Disruption in our suppliers’ operations have disrupted, and could in the future disrupt, our production schedule. Our automotive operations are dependent upon the continued ability of our suppliers to deliver the systems, components, raw materials, and parts that we need to manufacture our products. Other than with respect to certain of our offtake agreements with battery raw material suppliers, our use of “just-in-time” manufacturing processes typically allows us to maintain minimal inventory. As a result, our ability to maintain production is dependent upon our suppliers delivering sufficient quantities of systems, components, raw materials, and parts on time to meet our production schedules and specifications. In some instances, we purchase systems, components, raw materials, and parts that are ultimately derived from a single source and may be at an increased risk for supply disruptions. Any number of factors, including labor disruptions, catastrophic weather events, the occurrence of a public health crisis, contractual or other disputes, unfavorable economic or industry conditions, geopolitical conflicts, restrictions on transactions involving certain territories, entities or individuals, delivery delays or other performance problems or financial difficulties or solvency problems, could disrupt our suppliers’ operations and lead to uncertainty in our supply chain or cause supply disruptions for us, which could, in turn, disrupt our operations, including the production of certain higher margin vehicles.…

Pandemics, epidemics, disease outbreaks, and other public health crises have disrupted our business and operations, and future public health crises could materially adversely impact our business, financial condition, liquidity, and results of operations. Pandemics, epidemics, or disease outbreaks in the U.S. or globally, such as the COVID-19 pandemic, have previously disrupted, and may in the future disrupt, our business, which could materially affect our results of operations, financial condition, liquidity, and future expectations. Any such events may adversely impact our global supply chain and global manufacturing operations and cause us to suspend our operations in the affected markets. In particular, we could experience, among other things: (1) continued or additional global supply disruptions; (2) labor disruptions or shortages; (3) an inability to manufacture; (4) an inability to sell to our customers; (5) a decline in showroom traffic and customer demand; (6) customer defaults on automobile loans and leases; (7) lower than expected pricing on vehicles sold at auction; and (8) an impaired ability to access credit and the capital markets. Any new public health crisis could have a material impact on our business, financial condition, and results of operations going forward.

Security breaches, cyberattacks, and other disruptions to information technology systems and networked products, including connected vehicles, owned or maintained by us, GM Financial, service providers, such as data processors, or third parties, such as vendors or suppliers, could materially compromise our operations and/or sensitive customer data and proprietary information. We rely upon information technology systems and manufacture networked and connected products, some of which are managed by third parties, to collect, process, transmit, use, protect, and store electronic information and to manage or support a variety of our business processes, activities, and products. Additionally, we and GM Financial collect, process, transmit, use, protect, and store confidential data, including intellectual property and proprietary business information (including that of our dealers and suppliers), as well as personally identifiable information of our respective customers and employees, in data centers and on information technology networks (including networks that are controlled or maintained by third parties). The secure operation of these systems and products, and the processing and maintenance of the information processed by these systems and products, is critical to our business operations and strategy. Further, customers using our systems rely on the security of our infrastructure, including hardware and other elements provided by third parties, to ensure the reliability of our products and the protection of their data.…

Despite our and our third-party providers' security measures and business continuity plans, our information technology systems and networked and connected products are vulnerable to intrusions, damage, disruptions, or shutdowns caused by attacks by hackers, computer viruses or worms, malware (including “ransomware”), phishing attacks, spyware, denial of service attacks, and/or breaches due to errors, negligence or malfeasance by employees, contractors, vendors, and others who have access to these systems and products. We and our third-party providers regularly experience cyberattacks and security incidents, such as phishing attacks, and we expect cyberattacks and incidents to continue in varying degrees, including due to the rapid evolution and adoption of AI. While to date no incidents have had a material impact on our operations or financial results, we cannot guarantee that material incidents will not occur in the future. Cybersecurity threat actors are increasingly sophisticated and are targeting employees, contractors, service providers, and third parties through various techniques, including but not limited to, social engineering. Techniques used in cyberattacks to obtain unauthorized access to, disable, or sabotage information technology systems are increasingly diverse and sophisticated, including as a result of emerging technologies, such as AI and machine learning.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
