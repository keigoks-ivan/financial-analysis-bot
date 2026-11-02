你是 stock-analyst v20 DD 的證據採集子 agent。標的：AMKR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - AMKR Amkor Technology market share gaining OR losing 2026
  - Amkor Technology new entrant OR displace threat Semiconductor Equipment & Materials 2026
  - AMKR competitor design win 2026
  - Amkor Technology vs Semiconductor Equipment & Materials peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
GOVERNMENTAL REGULATIONS As a public company with global operations, we are subject to various federal, state, local and foreign laws, and our products and services are governed by a number of rules and regulations. These regulations, which differ among jurisdictions, include financial and other external reporting disclosure rules, accounting standards and environmental, corporate governance, intellectual property, tax, trade, antitrust, employment, immigration and travel, privacy and anti-corruption laws. Costs and accruals incurred to comply with these governmental regulations are presently not material to our capital expenditures, results of operations and competitive position. Although there is no assurance that existing or future government laws applicable to our operations, services or products will not have a material adverse effect on our capital expenditures, results of operations and competitive position, we do not currently anticipate material expenditures for compliance with government regulations.

12 Table of Contents COMPETITION The outsourced semiconductor packaging and test market is highly competitive, and geopolitical trade tensions have increased competition from Chinese firms supporting a China-for-China supply chain. We face competition from established packaging and test service providers primarily located in Asia, including ASE Technology, JCET Group and Powertech Technology.

Additionally, we compete with contract foundries and electronic manufacturing service providers or contract electronics manufacturers, which offer certain types of advanced packaging. Our IDM customers also evaluate our services and scale against their own in-house capabilities.

The key competitive factors in the outsourced semiconductor packaging and test services market are: •Advanced packaging technology •Geographic location of services •Manufacturing scale and expertise •Customer co-development and innovation •Investment in new technology and capacity •Quality and reliability •Price •Cycle time We believe we are competitive in these areas.

HUMAN CAPITAL RESOURCES Amkor believes that its future success is highly dependent upon our continued ability to attract, retain and motivate qualified employees. As part of our effort to attract and motivate employees, Amkor is committed to providing competitive and comprehensive benefits that are designed to enable our employees and their families to live healthier and more secure lives. Additionally, Amkor has implemented various retention programs to incentivize and retain high-performing employees. We regularly evaluate such retention programs and our compensation practices generally to ensure they remain competitive and are aligned with local market practices. We look to promote our management-level employees from within Amkor, and we believe that we have been successful in this effort. Factory locations also maintain training and development programs that enable the continued learning and growth of our employees, and senior management regularly meets to share and implement best practices among our various facilities.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
We compete against established competitors in the packaging and test business as well as internal capabilities of IDMs and face competition from foundries and contract manufacturers.

The outsourced semiconductor packaging and test services market is very competitive. We face substantial competition from established and emerging packaging and test service providers primarily located in Asia, including companies with significantly greater processing capacity, financial resources, local presence, research and development operations, marketing, technology and other capabilities. In addition, we may compete with electronics manufacturing service providers or contract electronics manufacturers that also provide advanced integrated device solutions. We also may face increased competition from domestic companies located in China, where there are government-supported efforts to promote and subsidize the development and growth of the local semiconductor industry. We may be at a disadvantage in attempting to compete with entities associated with such government-supported initiatives based on their lower cost of capital, access to government resources and incentives, preferential sourcing practices, stronger local relationships or otherwise. Our competitors may also have established relationships, or enter into new strategic relationships, with one or more of the large semiconductor companies that are our current or potential customers or key suppliers to these customers. Consolidation among our competitors could also strengthen their competitive position.

We also face competition from contract manufacturers and electronic manufacturing service providers, many of which are larger than us, have lower cost structures, and may be willing or able to sell their services at lower margins. These competitors have increased and could increase pricing and competitive pressures.

We cannot assure you that we will be able to compete successfully in the future against our existing or potential competitors, that our customers will not rely on internal sources, foundries or contract manufacturers for packaging and test services or that our business, liquidity, results of operations, financial condition or cash flows will not be materially and adversely affected by such increased competition.

We have derived and expect to continue to derive a large portion of our revenues from a small group of customers during any particular period due in part to the concentration of market share in the semiconductor industry. Our ten largest customers accounted for, in the aggregate, 72% of our net sales for the year ended December 31, 2025. In addition, we have significant customer concentration within our end markets. The loss of a significant customer, a business combination among our customers, a reduction in orders or decrease in price from a significant customer or disruption in any of our significant commercial arrangements may result in a decline in our sales and profitability and could have a material adverse effect on our business, liquidity, results of operations, financial condition and cash flows.

Many of these factors and risks are present and may be heightened within our business operations in China. For example, changes in U.S.-China relations, the political environment or international trade policies could result in further revisions to laws or regulations or their interpretation and enforcement, increased taxation, trade sanctions, the imposition of import or export duties and tariffs, restrictions on imports or exports, currency revaluations or retaliatory actions, which have had and may continue to have an adverse effect on our business plans and operating results. Additionally, the BIS Regulations place limitations on the ability of companies to export certain advanced computing semiconductor chips, as well as chipmaking equipment, by requiring companies to obtain licenses to export such products and equipment into China or other designated countries. These expanded export restrictions limit our ability to sell to certain Chinese companies and to third parties that do business with those companies. Certain of the Company’s competitors may be exempt from the BIS Regulations by virtue of being non-U.S. manufacturers.…

Our success depends to a significant extent upon the continued service of our key senior management, sales and technical personnel, any of whom may be difficult to replace. Competition for qualified employees is intensifying, accelerated by increasing competition in the semiconductor industry for talent to meet strong demand, and our business could be materially and adversely affected by the loss of the services of any of our existing key personnel, including senior management and technical talent, as a result of competition or for any other reason. Labor shortages could also result in higher wages that would increase our labor costs, which could reduce our profits. Although we have entered into agreements with our Chief Executive Officer and certain other executives that would prevent them from working for, or impose financial penalties for doing business with, our competitors in the event that those executives cease working for us, we cannot assure you that we will be successful in our efforts to retain or replace key employees or in hiring and properly training sufficient numbers of qualified personnel and in effectively managing our growth. Our inability to attract, retain, motivate and train qualified new personnel could have a material adverse effect on our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
