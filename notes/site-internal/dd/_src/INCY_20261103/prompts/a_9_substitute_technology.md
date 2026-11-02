你是 stock-analyst v20 DD 的證據採集子 agent。標的：INCY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Incyte product substitute technology threat 2026
  - Biotechnology alternative technology disruption 2026 2027
  - INCY Incyte technology obsolescence risk
  - Biotechnology next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm｜as_of：2026-02-10
<<<
Furthermore, disruptions at the FDA and other regulatory agencies could prevent those agencies from performing normal business functions on which the operation of our business relies, which could negatively impact our business.

The biotechnology and pharmaceutical industries are intensely competitive and subject to rapid and significant technological change. Despite investing significant resources, we may not be successful in discovering, developing, or commercializing additional drug products or our existing drug products in new indications. Discovery and development of drug candidates are expensive, uncertain and time-consuming, and we do not know if our efforts will lead to discovery of any drug candidates that can be successfully developed and marketed. We, or our collaborators or licensees, may decide to discontinue development of any or all of our drug candidates at any time for commercial, scientific or other reasons. Even if a drug candidate receives marketing approval, it may not be able to achieve market acceptance or compete successfully with our competitors’ products and we may never realize a return on the significant amount of time and money invested in the drug candidate, which could adversely affect our operating results and financial condition as well as our business plans. Of the compounds or biologics that we identify as potential drug products or that we in-license from other companies, including potential products for which we are conducting clinical trials, only a few, if any, are likely to lead to successful drug development programs and commercialized drug products.

Conflicts may arise with our collaborators and licensees if they pursue alternative technologies or develop alternative products either on their own or in collaboration with others as a means for developing treatments for the diseases that we have targeted. Competing products and product opportunities may lead our collaborators and licensees to withdraw their support for our drug candidates. Any failure of our collaborators and licensees to perform their obligations under our agreements with them or otherwise to support our drug candidates could negatively impact the development of our drug candidates and lead to our loss of potential revenues from product sales and milestones. Additionally, conflicts have from time to time occurred, and may in the future arise, relating to, among other things, disputes about the achievement and payment of milestone amounts and royalties owed, the ownership of intellectual property that is developed during the course of a collaborative relationship or the operation or interpretation of other provisions in our collaboration and license agreements. These disputes have led and could in the future lead to litigation or arbitration, which could be costly and divert the efforts of our management and scientific staff and could diminish the expected effectiveness of the collaboration.

We will likely not be able to control the amount and timing of resources that our collaborators or licensees devote to our programs or drug candidates. If our collaborators or licensees prove difficult to work with, are less skilled than we originally expected, do not devote adequate resources to the program, are unable to obtain regulatory approval of our drug candidates, pursue alternative technologies or develop alternative products, or do not agree with our approach to development or manufacturing of the drug candidate, the relationship could be unsuccessful. We cannot be sure that potential conflicts will not arise or be alleged among our existing or future collaborations. If a business combination involving a collaborator or licensee and a third-party were to occur, the effect could be to terminate or cause delays in the development of our drug candidate.

As a result of the COVID-19 pandemic we experienced, and as a result of future pandemics we may in the future experience, disruptions with the potential to severely impact our business, results of operations and financial condition. These disruptions can include the following: •the imposition of shelter-in-place orders and work-from-home policies that could affect our research and development activities and access to our laboratory space; •disruptions in our sales and marketing activities; •negative impacts on the demand for our products as a result of a decrease in patient visits to healthcare professionals and the prioritization of hospital resources for a future pandemic; •negative impacts on our clinical trials as a result of delays in site initiation, patient screening, patient enrollment, and monitoring and data collection; •slower response times by the FDA and comparable foreign regulatory agencies for the review and potential approvals of our drug candidate applications; and •negative impacts on the global supply chain which may affect our ability to obtain sufficient materials for our drug products and product candidates.

Our facility in Wilmington, Delaware is our headquarters and is also where we conduct most of our drug discovery, research, development and marketing activities. In addition, natural disasters, the effects of or measures taken to limit the effects of health epidemics such as the COVID-19 pandemic, or actions of activists opposed to aspects of pharmaceutical research may disrupt our experiments or our ability to access or use our facility. The loss of access to or use of our Wilmington, Delaware facility, either on a temporary or permanent basis, would result in an interruption of our business and, consequently, would adversely affect our overall business.

48 Table of Contents Business disruptions and uncertainties could seriously harm our operations, future revenues and financial condition and increase our costs and expenses.

Our operations, and those of our CROs, suppliers, and other contractors and consultants, could be subject to business disruptions as a result of natural disasters, power and other infrastructure failures or shortages, public health pandemics or epidemics, and other natural or man-made disasters, as well as other business uncertainties as a result of international trade policies, including tariff and trade disputes, trade sanctions and import and export licensing requirements. In addition, geopolitical and other events, such as the Russian invasion of Ukraine or the conflicts in the Middle East, could lead to sanctions, embargoes, supply shortages, regional instability, geopolitical shifts, cyberattacks, other retaliatory actions, and adverse effects on macroeconomic conditions, currency exchange rates, and financial markets, which could adversely impact our operations and financial results, as well as those of third parties with whom we conduct business. The occurrence of any of these business disruptions or other uncertainties could seriously harm our operations, future revenues and financial condition and increase our costs and expenses.

51 Table of Contents RISKS RELATING TO INTELLECTUAL PROPERTY AND LEGAL MATTERS If we are subject to arbitration, litigation and infringement claims, they could be costly and disrupt our drug discovery and development efforts.

Our business is increasingly dependent on critical, complex, and interdependent information technology (“IT”) systems, including Internet-based systems, some of which are managed or hosted by third parties, to support business processes as well as internal and external communications. The size and complexity of our IT systems make our IT systems and data vulnerable to risks and damages from a variety of sources, including malicious human acts, breaches of security, cyber-attacks, catastrophe or natural disaster, telecommunications or network failures, loss of power or other natural or man-made events. In addition, despite network security and back-up measures, we and our vendors frequently defend against and respond to data security attacks and incidents, and our servers and our vendors’ servers are potentially susceptible to physical or electronic break-ins, computer viruses, software vulnerabilities, ransomware attacks and similar disruptive problems. If our business continuity and disaster recovery plans and procedures or those of our vendors, including our CROs and contract manufacturers, were disrupted, inadequate or unsuccessful in the event of a problem, we could experience an interruption of all or a portion of our operations, which could result in significant harm to our business, financial results and reputation.…

54 Table of Contents Any such disruption or security breach, as well as any action by us or our employees or contractors that might be inconsistent with the rapidly evolving data privacy and security laws and regulations applicable within the United States and elsewhere where we conduct business, could result in enforcement actions by U.S. states, the U.S. federal government or foreign governments, liability or sanctions under data privacy laws, including healthcare laws such as the Health Insurance Portability and Accountability Act, that protect certain types of sensitive information, regulatory penalties, other legal proceedings such as but not limited to private litigation, the incurrence of significant remediation costs, disruptions to our development programs, business operations and collaborations, diversion of management efforts and damage to our reputation, which could harm our business and operations. Because of the rapidly moving nature of technology and the increasing sophistication of cybersecurity threats, our measures to prevent, respond to and minimize such risks may be unsuccessful.

Disruptions or data security breaches within other healthcare companies could also affect our business, results of operations and financial condition. If systems used by healthcare providers, third-party payors and companies in our distribution network such as PBMs, pharmacies and wholesalers are disrupted by a data security breach, the ability to process claims and fulfill prescriptions could be impacted, which could result in adverse effects on our net product revenues.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
