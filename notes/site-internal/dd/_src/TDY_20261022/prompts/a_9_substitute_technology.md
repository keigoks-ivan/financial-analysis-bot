你是 stock-analyst v20 DD 的證據採集子 agent。標的：TDY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Teledyne Technologies product substitute technology threat 2026
  - Scientific & Technical Instruments alternative technology disruption 2026 2027
  - TDY Teledyne Technologies technology obsolescence risk
  - Scientific & Technical Instruments next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm｜as_of：2026-02-20
<<<
Global conflicts could lead to disruption, instability and volatility in global markets and industries that could negatively impact our operations.

A military conflict between China and Taiwan would likely have a material adverse impact on our ability to sell products to customers in these areas and on our supply chain. Ongoing instability in the Middle East and the conflict between Russia and Ukraine could result in supply chain and other business disruptions.

Risks related to climate change Climate change may disrupt or adversely impact our business. Climate change may have an increasingly adverse impact on our business and those of our customers, partners and suppliers. As discussed under the risk factor below headed “Natural and man-made disasters could adversely affect our business, results of operations and financial condition,” some of our manufacturing facilities are located in regions that may be impacted by severe weather events, like hurricanes or ice storms, or in areas prone to wildfires, droughts and rising sea levels, the frequency and severity of which may increase as a result of climate change. These events could result in potential damage to our physical assets and may result in disruptions in manufacturing activities and impair the ability of our employees to work effectively. The effects of climate change also may impact our decisions to construct new facilities or maintain existing facilities in the areas most prone to physical risks, which could similarly increase our operating and material costs. We could also face indirect financial risks passed through the supply chain that could result in higher prices for our products and the resources needed to produce them.

Our Teledyne Battery Products unit makes lead acid batteries in California and is subject to a variety of environmental regulations and inspections, which have increased over time. Also, some of our sites conduct electroplating, metal finishing and other operations that utilize hazardous materials that are subject to similar regulations. Regulatory changes or failure by a business to meet applicable requirements could disrupt that business or force a closure or relocation of the business.

Several of our facilities, as a result of their locations, could be subject to a catastrophic loss caused by earthquakes, hurricanes, tornados, floods, ice storms, rising sea levels, droughts or other natural disasters. Many of our production facilities and our headquarters are located in California and thus are in areas with above average seismic activity and may also be at risk of damage due to wildfire or mudslides. Local utilities may impose blackouts during high fire risk weather conditions, which could result in disruptions to our businesses located in California, including our headquarters.

In the event of a major earthquake, tornado, hurricane or catastrophic event such as fire, power loss, telecommunications failure, vandalism, cyber-attack, war, terrorist attack or health epidemic (including COVID), we may be unable to continue our operations and may endure system interruptions, reputational harm, delays in our application development, lengthy interruptions in our production, breaches of data security and loss of critical data, all of which could harm our business, results of operations and financial condition and have a material adverse impact on us. Starting in December 2022, a series of direct-action protests by political extremists on several of our facilities in the UK have resulted in trespass and vandalism and in some cases caused damage to our facilities and interrupted some productions lines for a period of time. Teledyne FLIR’s components operation is a single source supplier of certain sensors used throughout the FLIR business, and a disruption in business due to a disaster could have a material adverse impact on the businesses of Teledyne FLIR. Teledyne’s facilities in Quebec, Canada have been impacted by loss of electrical power caused by severe ice storms. In addition, we have manufacturing facilities in the southeastern United States and Texas that have been threatened or struck by major hurricanes.…

Disasters also have an indirect adverse impact on our business. For example, in 2018, a fire at a Netherlands-based facility of a key supplier of printed circuit boards resulted in delivery disruptions to the electronics industry, including to businesses in our Digital Imaging segment.

Our business and operations could suffer in the event of cybersecurity breaches. Attempts by malicious actors to gain unauthorized access to our information technology systems have become more sophisticated and are sometimes successful. These attempts, which might be related to industrial or foreign government espionage, crime, activism, or other motivations, include covertly introducing malware into our computers and computer networks, performing reconnaissance, impersonating authorized users, extortion, fraud, and stealing, corrupting or restricting our access to data, among other activities. We have in the past experienced cyber-attacks including some loss of confidentiality and some loss of availability and integrity, although these attacks have not had material impact on our business. Our customers and suppliers have also experienced successful cyber-attacks, which in some cases resulted in payments by or to us being 16 Table of Contents unlawfully diverted. The theft, corruption, unauthorized use or publication of our intellectual property or confidential business information due to a cyber-attack could harm our competitive position, damage our reputation, reduce the value of our investment in R&D and other strategic initiatives or otherwise adversely affect our business. We are subject to U.S.…

We currently incorporate machine learning and AI capabilities into certain of our products and solutions and may seek to expand the use of AI in our offerings in the future. As with many innovations, AI presents risks, challenges, and unintended consequences that could affect our business. AI algorithms and training methodologies may be flawed. These deficiencies and other failures of AI systems could subject us to competitive harm, regulatory action, legal liability, and brand or reputational harm. Further, incorporating AI could give rise to litigation risk and risk of non-compliance and unknown cost of compliance, as AI is an emerging technology for which the legal and regulatory landscape is not fully developed (including potential liability for breaching intellectual property or privacy rights or laws). While new AI initiatives, laws, and regulations are emerging and evolving, what they ultimately will look like remains uncertain, and our obligation to comply with them could entail significant costs, negatively affect our business, or entirely limit our ability to incorporate certain AI capabilities into our offerings.

Our competitors may be faster or more successful than we are in incorporating AI and other disruptive technology into their offerings, which would impair our ability to compete successfully.

Some items we purchase for the manufacture of our products are purchased from limited or single sources of supply due to technical capability, price and other factors. Furthermore, sole source supply is more common among our businesses that are heavily involved in R&D because there can be few suppliers in the world capable of producing the products or providing the services with the right highly specialized technology. In the case of our Defense Electronics businesses, once a part has been designed in, our customers often require lengthy and expensive qualification testing, potentially at the system level before a new supplier can be used on production hardware. Additionally, overall volumes are often small when compared to commercial markets. Both factors limit the ability to rapidly address supply chain issues when they occur. We have also outsourced from time to time the manufacturing of certain parts, components, subsystems and even finished products to single or limited sources, including international sources. Disruption of these sources or supplier-imposed rationing of scarce components could cause delays or reductions in shipments of our products or increases in our costs, which could have an adverse effect on our financial condition or operations. International sources pose additional risks, some of which are similar to those described above regarding international sales.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TDY_20261022/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
