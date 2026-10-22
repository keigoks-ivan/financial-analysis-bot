你是 stock-analyst v20 DD 的證據採集子 agent。標的：ISRG。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Intuitive Surgical product substitute technology threat 2026
  - Medical Instruments & Supplies alternative technology disruption 2026 2027
  - ISRG Intuitive Surgical technology obsolescence risk
  - Medical Instruments & Supplies next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm｜as_of：2026-02-03
<<<
Patient Value. We believe that the value of a medical procedure to a patient can be defined: Patient Value = Procedure Efficacy / Invasiveness. We define procedure efficacy as a measure of the success of the procedure in helping resolve the underlying disease, and invasiveness as a measure of patient pain and disruption of regular activities.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm｜as_of：2026-02-03
<<<
We have increased, and will continue to increase, our operations in China. There is inherent risk, based on the complex and changing dynamic between China and the U.S., that political, diplomatic, military, or other events could result in business disruptions, including, but not limited to, increased policy or regulatory enforcement against companies, tariffs, trade embargoes, or export restrictions. Tariffs increase the cost of our products and the components and raw materials that go into making them. These increased costs adversely impact the gross margin that we earn on our products. Tariffs can also make our products more expensive for customers, which could make our products less competitive when compared to those products offered by domestic companies and reduce consumer demand. Countries may also adopt other measures, such as controls on imports or exports of goods, technology, or data, which could adversely impact our operations and supply chain and limit our ability to offer our products and services as designed. These measures can require us to take various actions, including changing suppliers and restructuring business relationships. Changing our operations in accordance with new or changed trade restrictions can be expensive, time-consuming, disruptive to our operations and distracting to management.…

The manufacture of our products requires the timely delivery of a sufficient amount of quality components and materials and is highly exacting and complex, due in part to complex trade and strict regulatory requirements. Some of the components necessary for the assembly of our products are currently provided to us by sole-sourced suppliers or single-sourced suppliers due to, among other things, quality considerations, unique intellectual property considerations, or constraints associated with regulatory requirements. We generally purchase components through purchase orders rather than long-term supply agreements 30 Table of Contents and generally do not maintain large volumes of components within our inventory. While alternative suppliers exist and could be identified for single-sourced components, the disruption or termination of the supply of components, or inflationary pressure in our supply chain, could cause a significant increase in the costs of these components, which could affect our operating results. Certain of our sole-sourced suppliers or single-sourced suppliers could be adversely affected by the macroeconomic conditions. A disruption or termination in the supply of components could also result in our inability to meet demand for our products, which could harm our ability to generate revenues, lead to customer dissatisfaction, and damage our reputation and our brand.…

Our information technology systems are critical to the success of our products, help us operate effectively and efficiently, interface with customers, maintain our supply chain and manufacturing operations, maintain financial accuracy and efficiency, and help us produce our Annual Report on Form 10-K and other filings with the Securities and Exchange Commission. If we do not allocate and effectively manage the resources necessary to build and sustain the proper information technology infrastructure, we could be subject to transaction errors, processing inefficiencies, loss of existing customers, difficulties in attracting new customers, business operation disruptions, diversion of the attention of management and key information technology resources, security breaches, or the unauthorized access to, loss of, or damage to intellectual property, confidential information, or personal information. Our information technology systems, and those of our third-party service providers, strategic partners, and other contractors or consultants, are vulnerable to attack, damage, or interruption from a variety of sources. These sources include computer viruses and malware (e.g., ransomware), malicious code, hacking, cyberattacks, phishing attacks and other social engineering schemes, employee theft or misuse, human error, fraud, natural disasters, terrorism, war, telecommunication and electrical failures, denial or degradation of service attacks, sophisticated nation-state and nation-state-supported actors, or unauthorized access or use by persons inside our organization, or persons with access to systems inside our organization.…

Our business requires us to use and store confidential information, including customer, employee, and business partner personal information, as well as other proprietary information and business data. We have implemented various controls, systems, and processes intended to secure our information technology systems and the information on it. We also have programs in place to detect, contain, and respond to data security incidents, and we make ongoing improvements to our information-sharing products designed to minimize vulnerabilities. However, we cannot guarantee that these measures will be effective or that attempted security breaches or disruptions would not be successful or damaging to our information technology systems and information. These security measures may be compromised as a result of security breaches by unauthorized persons, employee error, malfeasance, faulty password management, or other irregularity and result in persons obtaining unauthorized access to our data or accounts. Third parties may attempt to fraudulently induce employees or customers into disclosing usernames, passwords, or other sensitive information or otherwise attempt to hack into our information technology systems to obtain personal data relating to patients or employees, our confidential or proprietary information, or confidential information we hold on behalf of third parties. In addition, with the prolific use of AI technologies, there is an increased risk of unauthorized or accidental disclosure.…

Disruptions caused by ongoing or future global conflicts, including those resulting from conflicts affecting or in close proximity to countries and regions in the Middle East, may result in extended lead times, delays in supplier deliveries, and increasing freight costs. The risk of supply disruptions may further result in delays in the delivery of our products.

The length, impact, and outcome of ongoing military conflicts is highly unpredictable and could lead to significant market and other disruptions, including significant volatility in commodity prices and supply of energy resources, instability in financial markets, supply chain interruptions, political and social instability, trade disputes or trade barriers, changes in consumer or purchaser preferences, an increase in global shipping expenses, greater volatility in foreign exchange and interest rates, an increase in cyberattacks and espionage, and other unforeseen business disruptions. The extent and duration of the military action, sanctions, other consequences, such as restrictions on transactions or banning the export of energy products, including natural gas, and the resulting market disruptions could be significant and could potentially have substantial impact on the global economy and our business for an unknown period of time. Impacts to our business may include, but are not limited to, a reduction in procedures performed, reduced demand for our products, limitations on hospitals’ ability to spend on capital equipment and in healthcare spending in general, and supply disruption. Any such disruption may also magnify the impact of other risks described in this “Risk Factors” section.

For example, the COVID-19 pandemic, which first emerged in late 2019, adversely impacted our operations, supply chains, and expenses. These impacts resulted from a number of impacts and measures, including, but not limited to, healthcare customers diverting resources and priorities towards disease treatment, hospital staffing shortages and supply chain disruptions that impaired their ability to provide patient care, and precautionary measures implemented by governments, businesses, and ourselves. Due to these factors, we experienced significant and unpredictable reductions in the demand for our products as customers delayed or canceled planned procedures and capital expenditures. Furthermore, the COVID-19 pandemic also caused widespread business disruptions, including travel restrictions, reduced access to our customers, and temporary closures of our facilities and those of our suppliers. For instance, California, where many of our operations and manufacturing facilities are located, implemented risk-reduction orders that limited our employees’ ability to produce and move products through the supply chain. Such disruptions negatively impacted our business, financial condition, and results of operations. Similar effects may occur in the event of a resurgence of COVID-19 or the emergence of another public health crisis.

CLIMATE CHANGE, NATURAL DISASTERS, OR OTHER EVENTS BEYOND OUR CONTROL COULD DISRUPT OUR BUSINESS, FINANCIAL CONDITION, OR RESULTS OF OPERATIONS.

Natural disasters, terrorist activities, and other events beyond our control including, but not limited to, internet security threats and violence motivated by political or social causes, could adversely affect our business, financial condition, or results of operations. Moreover, global climate change could result in certain types of natural disasters occurring more frequently or with more intense effects. The impacts of climate change may include physical risks (such as frequency and severity of extreme weather conditions), social and human effects (such as population dislocations or harm to health and well-being), compliance costs, transition risks, shifts in market trends, and other adverse effects. Such impacts may disrupt parties in our supply chain, our customers, and our operations. For example, the March 2011 earthquake and tsunami in Japan, and their aftermath, created economic uncertainty and disrupted economic activities in Japan, including a reduction in hospital spending. More recently in September and October 2024, Hurricane Helene and Hurricane Milton caused economic uncertainty and business disruptions in the Southeast region of the U.S.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
