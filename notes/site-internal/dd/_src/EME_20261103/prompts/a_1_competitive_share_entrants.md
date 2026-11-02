你是 stock-analyst v20 DD 的證據採集子 agent。標的：EME。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - EME EMCOR Group market share gaining OR losing 2026
  - EMCOR Group new entrant OR displace threat Engineering & Construction 2026
  - EME competitor design win 2026
  - EMCOR Group vs Engineering & Construction peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm｜as_of：2026-02-26
<<<
4 Table of Contents Competition Across our operations, we compete with national, regional, and local companies, many of which are small, owner-operated entities that carry on their businesses in a limited geographic area, as well as with certain foreign companies.

The electrical and mechanical construction services industry is highly fragmented and our competition includes thousands of small companies across the United States. In addition, there are a number of larger companies focused on providing electrical and/or mechanical construction services, such as APi Group Corporation, Comfort Systems USA, Inc., Dycom Industries, Inc., Everus Construction Group, Inc., IES Holdings, Inc., MasTec, Inc., MYR Group Inc., Quanta Services, Inc., and Tutor Perini Corporation. A majority of our revenues are derived from projects requiring competitive bids; however, an invitation to bid is often conditioned upon prior experience, technical capability, and financial strength. Competitive factors in the electrical and mechanical construction services business include: (a) the availability of qualified and/or licensed personnel; (b) reputation for integrity and quality; (c) safety record; (d) cost structure and the ability to control project costs; (e) relationships with customers; (f) price; (g) geographic diversity; (h) experience in specialized markets; (i) the ability to obtain surety bonding; (j) adequate working capital or access to bank credit; and (k) the use of technology such as virtual design construction (“VDC”), building information modeling (“BIM”), robotics, and automation.…

While the building services industry is also highly fragmented, with most competitors operating in a specific geographic region, a number of large corporations and original equipment manufacturers are engaged in this field. Within our mechanical services division, we compete with entities such as APi Group Corporation, Comfort Systems USA, Inc., and Service Logic LLC, as well as Carrier Global Corporation and Trane Technologies plc. Within our commercial and government site-based divisions, competition includes companies such as Amentum Services, Inc., IAP Worldwide Services, Inc., Fluor Corporation, Cushman & Wakefield plc, CBRE Group, Inc., Jones Lang LaSalle Incorporated, Sodexo, Inc., Aramark, and ABM Industries Incorporated. In addition, we compete with several regional firms serving all or portions of the markets we target, such as BrightView Holdings, Inc., Kellermeyer Bergensons Services, LLC, and SMS Assist, L.L.C. The key competitive factors in the building services industry include: (a) availability of qualified personnel and managers; (b) service quality and technical expertise; (c) the use of technology tools and data analytics; (d) cost structure and the ability to control project costs; (e) price; and (f) geographic diversity. Due to our financial strength, scope of service offerings, our technical capability and management experience, and our geographic presence, we believe our building services operations are in a strong competitive position.…

The market for providing industrial services includes large national providers, as well as numerous regional companies. In the manufacture of heat exchangers, we compete with both U.S. and foreign manufacturers. Competitors within this industry include JVIC, Universal Plant Services, Inc., Turner Industries Group, LLC, Team, Inc., Specialty Welding and Turnarounds, LLC, Cust-O-Fab, Inc., Dunn Heat Exchangers, Inc., Turn2 Specialty Companies, and Wyatt Field Service Company, LLC, among others. The key competitive factors in the industrial services market consist of: (a) availability of skilled workforce; (b) technical expertise; (c) service, quality, and ability to respond quickly; (d) price; and (e) safety record. Due to our technical capabilities, skilled workforce, and safety record, we believe that we are in a strong competitive position in the industrial services markets that we serve. Although the technical expertise and capital investment that is required in manufacturing heat exchangers may be considered a barrier to entry in this field, there are significantly fewer barriers to entry as it pertains to turnaround projects and services.

Our ability to execute complex projects for our customers, and to perform all of our services with the excellence that makes us an industry leader, depends on our success in attracting and retaining skilled labor in a competitive market. We therefore strive to be and remain an employer of choice for the most talented employees in each of the industries and markets in which we operate. This begins with offering competitive employee compensation and benefits packages, specifically designed to meet the unique needs of each individual in our organization, which include: •Health and Welfare Plans: All full-time employees who do not participate in union plans are offered a range of choices among medical, dental and vision plans, life, accident, dependent and disability insurance, and pre-tax health savings accounts that include employer contributions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm｜as_of：2026-02-26
<<<
Our industry is highly competitive. Our industry is served by numerous small, owner-operated private companies, a few public companies, and several large regional companies. In addition, relatively few barriers exist to prevent entry into most of the industries in which we operate. As a result, any organization that has adequate financial resources, and access to technical expertise, may become a competitor. Competition in our industry depends on numerous factors, including price. Certain of our competitors have lower overhead cost structures and, therefore, are able to provide their services at lower rates than we are currently able to provide. Our project and service work is frequently awarded through a competitive bidding process, which is standard in our industry. We are constantly competing for contracts based on pricing, schedule, and technical expertise. Competition can place downward pressure on our contract prices and profit margins, which may make it difficult to win the project or force us to accept contractual terms and conditions that are less favorable to us, thereby increasing the risk that, among other things, we may not realize profit margins at the same rates we have seen in the past or may become responsible for costs or other liabilities we have not incurred in the past.

We cannot be certain that our competitors will not develop the expertise, experience, and resources necessary to provide services that are superior in quality, and lower in price, to ours. Similarly, we cannot be certain that we will be able to maintain or enhance our competitive position within our industries or maintain a customer base at current levels. We may also face competition from the in-house service organizations of existing or prospective customers, particularly with respect to building services. Many of our customers employ personnel who perform some of the same types of building services that we do. We cannot be certain that our existing or prospective customers will continue to outsource building services in the future. If we are unable to compete effectively, we may experience a loss of customers, reduced profitability, or both, which if significant, could have a material adverse effect on our business, financial condition, and results of operations. Refer also to “Business - Competition” in Item 1 of this Form 10-K.

Our business strategy relies, in part, on acquisitions to sustain our growth, and these transactions present certain risks and uncertainties. As part of our growth strategy, we acquire companies that expand, complement, and/or diversify our businesses. However, there is no guarantee that we will be successful in identifying targets that meet our requirements for acquisition. We may also face increased competition from other potential acquirers, including those who may have greater financial resources available to them or who may be in a position to offer more favorable terms to the target company. This competition may limit our ability to pursue acquisition opportunities. Additionally, circumstances beyond our control, such as elevated interest rates, inflation and potential macroeconomic disruptions, may hinder our ability to pursue and complete acquisitions. Further, realization of the anticipated benefits of an acquisition, such as our acquisition of Miller Electric Company, and avoiding or mitigating the potential risks associated with an acquisition, will depend, among other things, upon our ability to: (a) effectively conduct due diligence to identify and mitigate potential issues at companies we propose to acquire, (b) recognize incompatibilities or other obstacles to the successful integration of the acquired business with our other operations, and (c) gain greater efficiencies and scale that will translate into reduced costs or anticipated synergies in a timely manner.…

The availability and costs to adequately train and maintain a skilled labor force could be impacted by factors we cannot control, including changes in the unemployment rate, prevailing wage rates, benefit costs, potential labor force disruptions, and competition for labor from our competitors in the markets we serve. Labor shortages or increased labor costs, such as those experienced in recent years, could impair our ability to provide services to our customers (or the ability of third-party subcontractors to provide services to us), maintain our business, or grow our revenues. Federal or state regulations, which seek to prohibit non-competition agreements with employees may also impact our ability to retain key employees by reducing barriers to individuals with such agreements leaving to work for our competitors.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
