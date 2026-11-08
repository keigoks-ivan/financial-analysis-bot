你是 stock-analyst v20 DD 的證據採集子 agent。標的：UBER。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Uber Technologies product substitute technology threat 2026
  - Software - Application alternative technology disruption 2026 2027
  - UBER Uber Technologies technology obsolescence risk
  - Software - Application next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm｜as_of：2026-02-13
<<<
Competitive Environment We compete on a global basis in highly fragmented markets. We face significant competition in each of the mobility and delivery industries globally and in the logistics industry in the North America from existing, well-established, and low-cost alternatives, and in the future we expect to face competition from new market entrants given the low barriers to entry that characterize these industries. As we and our competitors introduce new products and offerings, and as existing products evolve, we expect to become subject to additional competition. While we work to expand globally and introduce new products and offerings across a range of industries, many of our competitors remain focused on a limited number of products or on a narrow geographic scope, allowing them to develop specialized expertise and employ resources in a more targeted manner than we do. The competition we face in each of our offerings includes: 5 •Mobility. Our Mobility offering competes with personal vehicle ownership and usage, which accounts for the majority of passenger miles in the markets that we serve, and traditional transportation services, including taxicab companies and taxi-hailing services, livery and other car services. In addition, public transportation can be a superior substitute to our Mobility offering and in many cases, offers a faster and lower-cost travel option in many cities.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm｜as_of：2026-02-13
<<<
We face competition in each of our offerings, including: •Mobility. Our Mobility offering competes with personal vehicle ownership and usage, which accounts for the majority of passenger miles in the markets that we serve, and traditional transportation services, including taxicab companies and taxi-hailing services, livery and other car services. In addition, public transportation can be a superior substitute to our Mobility offering and in many cases, offers a faster and lower-cost travel option in many cities. We also compete with other ridesharing companies, including certain of our minority-owned entities, for Drivers and riders, including Bolt, Didi, Lyft, and Ola. There are also a number of companies developing and introducing autonomous vehicles and technologies 12 that either are competing with us or may compete with us in the future, including Alphabet (Waymo), Amazon (Zoox), and Tesla.

Our failure to upgrade our technology or network infrastructure effectively to support our growth could result in unanticipated system disruptions, slow response times, or poor experiences for Drivers, consumers, merchants, Shippers, and Carriers. To manage the growth of our operations and personnel and improve the technology that supports our business operations, as well as our financial and management systems, disclosure controls and procedures, and internal controls over financial reporting, we will be required to commit substantial financial, operational, and technical resources. In particular, we will need to improve our transaction processing and reporting, operational, and financial systems, procedures, and controls. For example, due to our significant growth, especially with respect to emerging offerings, we face challenges in timely and appropriately designing controls in response to evolving risks of material misstatement. These improvements are and will be particularly challenging when we acquire new businesses with different systems. Our current and planned personnel, systems, procedures, and controls may not be adequate to support our future operations.…

We may not successfully accomplish any of these objectives. A softening of Driver, consumer, merchant, Shipper, or Carrier demand, whether caused by changes in the preferences of such parties, failure to maintain our brand, changes in the U.S. or global economies, pandemics, licensing fees in various jurisdictions, competition, or other factors, may result in decreased revenue or growth and our financial results and future prospects would be adversely impacted. For example, shifts in consumer behavior, including the use of new or emerging technologies, such as AI-enabled platforms and digital assistants, may disintermediate our relationship with consumers by controlling how our products are accessed, presented or selected, which could redirect demand to competitors and adversely affect our demand and growth. In addition, we expect to continue to incur significant expenses, and if we cannot increase our revenue at a faster rate than the increase in our expenses, we will not achieve or maintain profitability.

We have experienced, and may again experience security or privacy breaches or other unauthorized or improper access to, use of, disclosure of, alteration of or destruction of our proprietary or confidential data, employee data, or platform user data, which could cause loss of revenue, harm to our brand, business disruption, and significant liabilities.

Security breaches could also expose us to liability under various laws and regulations across jurisdictions and increase the risk of litigation and governmental investigation. We have been subject to security and privacy incidents in the past and may be again in the future. For example, in September 2022, we experienced a cybersecurity incident where an attacker accessed certain internal corporate systems, tools and data. In October and November of 2016, outside actors downloaded the personal data of approximately 57 million Drivers and consumers worldwide (the “2016 Breach”). The accessed data included the names, email addresses, mobile phone numbers, and drivers’ license numbers of approximately 600,000 Drivers, among other information. For further information on this incident, see the risk factor titled “—We face risks related to our collection, use, transfer, disclosure, and other processing of data, which could result in investigations, inquiries, litigation, fines, legislative, and regulatory action, and negative press about our privacy and data protection practices,” below. As we expand our operations, we may also assume liabilities for breaches experienced by the companies we acquire. For example, in April 2018, Careem publicly disclosed and notified relevant regulatory authorities that it had been subject to a data security incident that allowed access to certain personal information of riders and drivers on its platform, as of January 14, 2018.…

In addition, any businesses we acquire may not perform as well as we expect. Failure to manage and successfully integrate acquired businesses and technologies, including managing internal controls and any privacy, data security or AI risks associated with such acquisitions, may harm our operating results and expansion prospects. For example, Careem has historically shared certain user data with certain government authorities, which conflicts with our global policies regarding data use, sharing, and ownership. We have maintained our data use, sharing, and ownership practices for both our business and Careem’s business, and doing so may cause our relationships with government authorities in certain jurisdictions to suffer, and may result in such government authorities assessing fines or penalties against us. The process of integrating an acquired company, business, or technology or acquired personnel into our company is subject to various risks and challenges, including: •diverting management time and focus from operating our business to acquisition integration; •disrupting our ongoing business operations; •platform user acceptance of the acquired company’s offerings; •implementing or remediating the controls, procedures, and policies of the acquired company; 32 •integrating the acquired business onto our systems and ensuring the acquired business meets our financial reporting requirements and timelines; •retaining and integrating acquired employees, including aligning incentives between acquired employees and existing employees, managing cultural differences between acquired businesses and…

The nature of our business exposes us to claims, including civil lawsuits in the United States such as those related to the 2016 Breach. These and any past or future privacy or security incidents could result in violation of applicable U.S. and international privacy, data protection, and other laws. Such violations subject us to individual or consumer class action litigation as well as governmental investigations and proceedings by federal, state, and local regulatory entities in the United States and internationally, resulting in exposure to material civil or criminal liability. Our data security and privacy practices have been the subject of inquiries from government agencies and regulators, not all of which are finally resolved. In April 2018, we entered into an FTC consent decree pursuant to which we agreed, among other things, to implement a comprehensive privacy program, undergo biennial third-party assessments, and not misrepresent how we protect consumer information through 2038. In October 2018, the FTC approved the final settlement, which exposes us to penalties for, amongst other activities, future failure to report security incidents. In November and December 2018, UK, Dutch and French supervisory authorities imposed fines totaling approximately $1.6 million. We have also entered into settlement agreements with numerous state enforcement agencies.…

We may be required or may opt to seek a license for the right to use intellectual property held by others, which may not be available on commercially reasonable terms, or at all. Even if a license is available, we may be required to pay significant royalties or license fees, which may increase our operating expenses. We may also be required to develop alternative non-infringing technology, content, branding, or business methods, which could require significant effort and expense and make us less competitive. If we cannot license or develop alternative technology, content, branding, or business methods for any allegedly infringing aspect of our business, 41 we may be unable to compete effectively or we may be prevented from operating our business in certain jurisdictions. Any of these results could harm our operating results.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
