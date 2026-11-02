你是 stock-analyst v20 DD 的證據採集子 agent。標的：PYPL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - PayPal Holdings product substitute technology threat 2026
  - Credit Services alternative technology disruption 2026 2027
  - PYPL PayPal Holdings technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm｜as_of：2026-02-03
<<<
COMPETITION The global payments industry is highly competitive, dynamic, innovative, and subject to regulatory scrutiny and oversight. Many of the areas in which we compete evolve rapidly with innovative and disruptive technologies, shifting preferences, needs, and price sensitivity of consumers and merchants, and frequent introductions of new products and services. Competition also may intensify as new competitors emerge, businesses combine or enter into new partnerships, and established companies in other segments expand to become competitive with various aspects of our business.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm｜as_of：2026-02-03
<<<
Our systems and operations and those of our service providers and partners have experienced from time to time, and may experience in the future, business interruptions or degradation of service because of distributed denial-of-service and other cyberattacks, insider threats, hardware and software defects or malfunctions, human error, earthquakes, hurricanes, floods, fires, and other natural disasters, public health crises (including pandemics), power losses, disruptions in telecommunications services, fraud, military or political conflicts, terrorist attacks, computer viruses or other malware, or other events. The frequency and intensity of weather events related to climate change are increasing, which could increase the likelihood and severity of such disasters as well as related damage and business interruption. Our corporate headquarters are located in the San Francisco Bay Area, a seismically active region in California. A catastrophic event that results in a disruption to or failure of our systems or operations could result in significant losses and require substantial recovery time and significant expenditures to resume or maintain operations. Some of our systems, including those of companies that we have acquired, are not fully redundant and any failure of these systems, including due to a catastrophic event, may lead to operational outages or delays.…

We have experienced, and expect to continue to experience, system failures, cyberattacks, unplanned outages, and other events or conditions that have or may interrupt the availability, or reduce or adversely affect the speed or functionality, of our products and services. While we continue to undertake system upgrades and re-platforming efforts designed to improve the availability, reliability, resiliency, and speed of our platform, these efforts are costly and time-consuming, involve significant technical complexity and risk, may divert our resources from new features and products, and may ultimately not be effective. A prolonged interruption of, or reduction in, the availability, speed, or functionality of our products and services could materially harm our business and financial condition. For example, in August 2025, PayPal experienced a temporary service disruption triggered by a coding error in a system update, which primarily impacted a limited number of customers and partners in Germany. In connection with this disruption, we experienced some fraudulent transaction activity for a limited time period. We have incurred transaction losses and other expenses as a result, including claims under our protection programs, and this or other disruptions may subject us to increased regulatory scrutiny, fines, penalties and litigation. Frequent or persistent interruptions in or disruptions to our services could permanently harm our relationship with our customers and partners and our reputation.…

We rely on facilities, components, applications, software, and services supplied by third parties, including data center facilities and cloud data storage and processing services. From time to time, we have experienced interruptions in the provision of such facilities and services provided by these third parties. If these third parties experience operational interference or disruptions (including a cybersecurity incident), fail to perform their obligations, or breach their agreements with us, our operations could be disrupted or negatively affected, which could result in customer dissatisfaction, regulatory scrutiny, and damage to our reputation and brands, and materially and adversely affect our business. While we maintain business interruption insurance, our coverage may be insufficient to cover all our losses caused by interruptions in our service due to systems failures and similar events.

Rapid, significant, and disruptive technological changes impact the industries in which we operate, including payment technologies (including real-time payments, payment card tokenization, virtual currencies, distributed ledger and blockchain technologies, and proximity payment technology such as Near Field Communication and other contactless payments); web browser technologies that enable users to easily store their payment card information for use on any retail or e-commerce FY 2025 FORM 10-K 15 Table of Contents website; AI; developments in technologies supporting our regulatory and compliance obligations; and in-store, digital, agentic and social commerce.

We expect that new technologies applicable to the industries in which we operate, including the development, adoption, and use of generative AI technologies and autonomous AI agents, will continue to emerge and may be superior to, or render obsolete, the technologies we currently use in our products and services. We cannot predict the effects of technological changes on our business, which technological developments or innovations will become widely adopted, and how those technologies may be regulated. Developing and incorporating new technologies into new and existing products and services may require significant investment, take considerable time, and may not ultimately be successful. For example, AI algorithms that we use may be flawed or may be based on datasets that are biased or insufficient. In addition, any latency, disruption, or failure in our AI systems or infrastructure could result in delays or errors in our offerings. There also may be real or perceived social harm, unfairness, or other outcomes that undermine public confidence in the use of our products or of AI. In addition, third parties may deploy AI technologies in a manner that reduces customer demand for our products and services.

We have selected custodian partners and the PYUSD Issuer, and may in the future select additional custodian partners and stablecoin issuing entities subject to regulatory oversight, capital requirements, maintenance of audit and compliance industry certifications, and cybersecurity procedures and policies. Any operational disruptions at any such custodian or issuer, or such custodians’ or issuer’s failure to safeguard cryptocurrency holdings (or reserve assets), could result in losses of customer assets, expose us to customer claims, reduce consumer confidence, harm our reputation, and materially impact our cryptocurrency product offerings and our operating results.

The global payments industry is highly competitive, dynamic, and innovative, and subject to regulatory scrutiny and oversight. Many of the areas in which we compete evolve rapidly with innovative and disruptive technologies, shifting preferences, needs, and price sensitivity of consumers and merchants, and frequent introductions of new products and services. Competition also may intensify as new competitors emerge, businesses combine or enter into new partnerships, and established companies in other segments expand to become competitive with various aspects of our business.

We compete with a wide range of businesses in every aspect of our business. Some of our current and potential competitors are or may be larger than we are, have larger customer bases, greater brand recognition, longer operating histories, a dominant or more secure position, broader geographic scope, volume, scale, resources, and market share than we do, or offer products and services that we do not offer. Other competitors are or may be smaller or younger companies that may be more agile in responding to regulatory and technological changes and customer preferences. Our competitors may devote greater resources to the development, promotion, and sale of products and services, and/or offer lower prices or more effectively offer their own innovative programs, products, and services. We regularly partner with other businesses, and the ability to continue developing these partnerships is important to our business. Competition for relationships with these partners is intense, and there can be no assurance that we will be able to continue to establish, grow, or maintain partner relationships.…

We expect to continue to consider and evaluate a wide array of potential strategic transactions as part of our overall business strategy, including business combinations, acquisitions, and dispositions of certain businesses, technologies, services, products, and other assets; strategic investments; and commercial and strategic partnerships (collectively, “strategic transactions”). At any given time, we may be engaged in discussions or negotiations with respect to one or more strategic transactions, any of which could, individually or in the aggregate, be material to our financial condition and results of operations. There can be no assurance that we will be successful in identifying, negotiating, consummating, or integrating suitable transaction opportunities. Strategic transactions may involve additional significant challenges, uncertainties, and risks, including challenges of obtaining regulatory or other approvals, integrating new employees, products, systems, technologies, operations, and business cultures; challenges associated with operating acquired businesses in markets or business areas in which we may have limited or no FY 2025 FORM 10-K 24 Table of Contents experience; disruption of our ongoing operations and diversion of our management’s attention; inadequate data security, cybersecurity, or operational and IT resilience; failure to identify or accurately assess commitments, liabilities, deficiencies and other risks associated with acquired businesses or assets; potential exposure to new or incremental risks associated with acquired businesses and entities, strategic investments or other strategic transactions, including potential…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
