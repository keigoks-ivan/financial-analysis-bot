你是 stock-analyst v20 DD 的證據採集子 agent。標的：DASH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - DASH DoorDash market share gaining OR losing 2026
  - DoorDash new entrant OR displace threat Internet Retail 2026
  - DASH competitor design win 2026
  - DoorDash vs Internet Retail peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm｜as_of：2026-02-18
<<<
6 Table of Contents COMPETITION The markets in which we operate are intensely competitive and characterized by shifting user preferences, fragmentation, and frequent introductions of new services and offerings. We compete for our constituencies on the following criteria: •Merchants. We compete for merchants based on our ability to generate consumer demand and the quality of our business enablement and demand fulfillment services.

In particular, local food delivery logistics, the largest category of our business today, is fragmented and intensely competitive. Globally, we compete with other local on-demand delivery companies, including Amazon, Uber Eats, Prosus, Delivery Hero, and other local incumbents. We also compete with merchants that have their own online ordering platforms, online ordering systems, merchants that own and operate their own delivery fleets, grocers and grocery delivery services, convenience stores and convenience store delivery services, and companies that provide merchant delivery services. In addition, we compete with traditional offline ordering channels, such as take-out offerings, telephone, and paper menus that merchants distribute to consumers. As we continue to expand into additional verticals, we may compete or come in closer competition with additional businesses with substantial resources, users, and brand power.

For additional information about the risks to our business related to competition, see the section titled “Risk Factors—Risks Related to Our Business and Operations—We face intense competition and if we are unable to compete effectively, our business, financial condition, and results of operations could be adversely affected.”

We believe access and choice are empowering. Our goal with dashing is to provide as many people as we can with an opportunity to earn incrementally in a way that fits their lives. Since the vast majority of Dashers are independent contractors, we must compete for their time and effort with every task. We compete against other earnings opportunities, other sources of capital like loans or credit cards, as well as alternative uses of time like doing errands or leisure. Because of this competition, we must make dashing attractive, worthwhile, and incremental to other choices available. Specifically, we strive to make dashing positive based on: •Accessibility: We believe the barriers to entry in dashing are very low. Where permitted by applicable law, prospective Dashers must pass a background check and, in most geographies, have access to a bike, scooter, or car. People who qualify to become Dashers are often eligible to begin generating income within a day of signing up.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm｜as_of：2026-02-18
<<<
The markets in which we operate are intensely competitive and characterized by shifting user preferences, fragmentation, and frequent introductions of new services and offerings. In particular, local food delivery logistics, the largest category of our business today, is fragmented and intensely competitive. Globally, we compete with other local on-demand delivery companies, such as Amazon, Uber Eats, Prosus, Delivery Hero, and other local incumbents. We also compete with merchants that have their own online ordering platforms, online ordering systems, merchants that own and operate their own delivery fleets, grocers and grocery delivery services, convenience stores and convenience store delivery services, and companies that provide merchant delivery services. In addition, we compete with traditional offline ordering channels, such as in-store dining, take-out offerings, telephone, and paper menus that merchants distribute to consumers. As we continue to expand to additional verticals, we may compete or come in closer competition with additional businesses with substantial resources, users, and brand power, including large e-commerce companies, large retailers, large grocery store chains and other large delivery service providers.

Our current and future competitors may enjoy competitive advantages such as greater name recognition, longer operating histories, market-specific knowledge, established relationships with local merchants and suppliers, larger existing user bases, more successful marketing capabilities, established geographic footprints and infrastructure, and substantially greater financial, technical, and other resources than we have. For example, with grocery delivery, we compete with established grocery chains that have strong bargaining power, established relationships with suppliers, and their own delivery fleets. Greater financial resources and product development capabilities may allow these competitors to respond more quickly and efficiently to new or emerging technologies and changes in merchant, consumer, and Dasher preferences that may render our platform less attractive or obsolete. If certain merchants choose to partner with our 12 Table of Contents competitors in a specific geographic market, if merchants choose to engage exclusively with our competitors, or if merchants decide to not partner with us at all, we may lack a sufficient variety and supply of merchant options or lack access to the most popular merchants, such that our offering would become less appealing to consumers.…

Many of our competitors are well capitalized and may offer discounted services, lower merchant commission rates and consumer fees, greater incentives for merchants joining their platforms and independent contractors who provide delivery services, consumer discounts and promotions, innovative platforms and offerings, and alternative pay models, any of which may be more attractive than those that we offer. Such competitive pressures have led us, and may lead us in the future, to change our commission rates and fees or change our incentives, discounts, and promotions to remain competitive. Such efforts have negatively affected, and will likely continue to negatively affect, our financial performance, and there is no guarantee that such efforts will be successful. Local on-demand delivery services for food and the other areas in which we compete are nascent, and we cannot guarantee that they will stabilize at a competitive equilibrium that will allow us to maintain or increase profitability. Further, merchants could determine that it is in their best interests to develop their own platforms to offer online pickup and delivery rather than use our platform.

It is relatively easy to switch between offerings in our industry. Consumers have a propensity to shift based on cost, quality, and selection and could use more than one local commerce platform; independent contractors who provide delivery services could use multiple platforms concurrently as they attempt to maximize earnings; and merchants could prefer to use the local commerce platform that offers the lowest commission rates and adopt more than one platform to maximize their volume of orders. As we and our competitors introduce new offerings and as existing offerings evolve, we expect to become subject to additional competition. Our competitors may adopt certain of our platform features or may adopt innovations that merchants, consumers, or Dashers value more highly than ours, which would make our platform less attractive and more difficult to differentiate.

Certain of our competitors offer, or may in the future offer, lower-priced or a broader range of offerings. Similarly, certain competitors may use marketing strategies that enable them to attract and retain new merchants, consumers, and Dashers at a lower cost than us. There is no assurance that we will not be forced, through competition, regulation, or otherwise, to reduce the price of delivery for consumers, increase the incentives we pay to Dashers that utilize our platform, further reduce the fees and commissions we charge merchants, or increase our marketing and other expenses to attract and retain merchants, consumers, and Dashers in response to competitive pressures. We have launched, and may in the future launch, new pricing strategies and initiatives, including Dasher or consumer loyalty programs, or modify existing pricing methodologies, the way in which fees, taxes, or similar items are presented on our platform, or our policies with respect to refunds and credits, any of which may not ultimately be successful in attracting and retaining merchants, 17 Table of Contents consumers, or Dashers and which may result in lower commissions or fees, which could adversely affect our business, financial condition, and results of operations.…

Further, if competitors introduce new features, offerings, or technologies, or if new industry standards and practices or consumer trends emerge, our existing technology, services, websites, and mobile applications may become less popular or obsolete. For example, companies operating in different industries are developing and have begun implementing autonomous technologies, and we believe that they may use these technologies to compete with us in the delivery or logistics industries. Our competitors may develop and commercialize autonomous and drone delivery technologies at scale before we or our partners do. In the event that our competitors bring autonomous or drone delivery to market or scale those technologies before we do, or their technology is, or is perceived to be, superior to our or our partners’ technology, they may be able to leverage such technology to compete more effectively with us, which could adversely affect our business, financial condition, and results of operations. Our future success could depend in large part on our ability to invest in, develop, and respond to technological advances and emerging industry standards and practices in a cost-effective and timely manner. Our implementation of autonomous technologies may take longer than initially anticipated and may require more upfront capital investment that may not generate return on investment.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
