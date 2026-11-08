你是 stock-analyst v20 DD 的證據採集子 agent。標的：GRAB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Grab Holdings product substitute technology threat 2026
  - Software - Application alternative technology disruption 2026 2027
  - GRAB Grab Holdings technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
We face intense competition across the segments and markets we serve. We face competition in each of our segments and markets. The segments and markets in which we operate are intensely competitive and are characterized by shifting user preferences, fragmentation, and evolving new services and offerings. We compete both for driver- and merchant-partners and for consumers. Our competitors may operate in single or multiple segments and in a single market or regionally across multiple markets. These competitors may be well-established or new entrants and focused on providing low-cost alternatives or higher quality offerings, or any combination thereof. New competitors may include established players with existing businesses in other segments or markets that expand to compete in our segments or markets. Competitors focused on a limited number of segments or markets may be better able to develop specialized expertise or employ resources in a more targeted manner than we do, and may enjoy lower overhead costs. Our competitors in certain geographic markets may enjoy competitive advantages such as reputational advantages, better brand recognition, longer operating histories, larger marketing budgets, better localized knowledge, and more supportive regulatory regimes and may also offer discounted services, driver- or merchant-partner incentives, consumer incentives, discounts or promotions, innovative products and offerings, or alternative pricing models.…

While our payments and financial services offerings compete with offline options such as cash and credit and debit cards, interbank transfers, traditional banks and other financial institutions, as well as other electronic payment system operators, our competitors in digital payment services also include ShopeePay and Google Pay and single market players such as Dana and GoPay in Indonesia, and Touch ‘n Go and MAE in Malaysia. Some of these competitors in digital payment services also operate e-commerce businesses. This may affect our e-wallet usage (specifically OVO and GrabPay) on these platforms due to preferential treatment that may be afforded to entities related to our competitors. Our competitors in the digital banking space are primarily new digital banks, in addition to incumbent banks in countries where our digital banks operate. In addition, while we have a non-competition agreement with Uber Technologies, Inc. (“Uber”), which was put in place in connection with a transaction with such shareholder and contractually restricts them from competing with us in Southeast Asia, such agreement is subject to limited terms. Uber previously operated in the ride-hailing and food deliveries businesses in Southeast Asia prior to our acquisition of Uber’s business in Southeast Asia in 2018. The non-competition agreement with Uber will expire one year after Uber disposes of all shareholdings in us.…

Because the industries in which we operate are relatively new and disruptive in our market, the relevant laws and regulations, as well as their interpretations, are often unclear and evolving in certain jurisdictions. This dynamic environment means we may be unable to obtain, assess, maintain, or renew all required licenses, permits and approvals necessary to provide our offerings and those we plan to offer. We cannot be sure that our interpretations of the rules and regulations, including our reliance on applicable regulatory exemptions have always been or will be consistent with those of the local regulators. As we expand our businesses, and in particular our financial services business, we may be required to obtain new licenses and will be subject to additional laws and regulations in the markets in which we plan to operate.

14 Table of Contents Segments of our businesses that are currently unregulated could become regulated, or segments of our businesses that are already regulated could be subject to new and changing regulatory requirements, which may adversely impact our business, results of operations, financial results and prospects. Various proposals regarding issues related to our business operations and business model that may impact our business are currently before various national, regional, and local legislative bodies and regulatory entities, or have already been adopted and implemented through new laws, rules or regulations. Compliance with existing or new laws and regulations could expose us to liabilities or cause us to incur significant expenses or otherwise impact our offerings or prospects. For example: •Under regulations governing the transportation business in Vietnam, we may be required to obtain a transport license in each province or city where mobility services are provided through our platform. We are currently engaging with national, provincial and city-level regulators on this requirement, which poses practical constraints for implementation, given that we believe these requirements are not appropriate or suited to a platform business such as ours.…

We also maintain relationships with major credit card providers and banks. Contractual disputes or joint venture issues could result in the restriction or withdrawal of these essential services. While our financial services have historically relied significantly on our deliveries and mobility segments, future growth depends on our ability to continue to grow its use outside our deliveries and mobility segments. As a new entrant in the financial services industry, we face intense competition. See “—Risks Relating to Our Business and Industry—We face intense competition across the segments and markets we serve” for a discussion of competition faced by our financial services business.

While we experience occasional small-scale disruptions affecting specific countries or business lines or temporary platform-wide disruptions, we may also face system failures that cut off or significantly reduce the speed or functionality of our platform. Although we have disaster response procedures, we and our third-party providers may lack a comprehensive business continuity framework in all instances. We are working with consultants to develop such a framework, but there is no assurance it will be implemented cost-effectively or at all, or that it will satisfy the expectations of regulators and stakeholders, including consumers and partners, regarding cybersecurity and technology requirements and business continuity management, which could impact our licensing.

Disruptions in internet infrastructure or a failure of telecommunications network operators could also affect the speed and availability of our platform. Furthermore, our operations rely on virtual private network access in certain jurisdictions and various third-party applications for internal communications and work processes. Disruptions to these services could cause business interruptions. We have no control over the costs of national telecommunications services; increased mobile internet fees could decrease consumer traffic and significantly reduce our revenue. As our platform becomes more complex and user traffic increases, maintaining and improving availability, especially during peak times, may become increasingly difficult. If our platform is unavailable, slow, or faces capacity constraints, users may migrate to competitors, adversely affecting our ecosystem and usage frequency. Failure to effectively address capacity constraints or upgrade our network architecture could significantly disrupt operations, impact user satisfaction, damage our reputation, and subject us to liability, which could materially and adversely affect our financial condition, results of operations and prospects.

As our business grows, competition increases and adoption of AI deepens, we face a higher risk of receiving notices claiming we have infringed upon third-party rights, including risks arising from shared intellectual property within strategic alliances. Any such claims, regardless of merit, could result in expensive litigation, damage to our brand goodwill, or significant liability for damages. Adverse outcomes may require us to stop using certain technologies, content, business methods or branding, or force us to seek licenses that may not be available on commercially reasonable terms, or at all. If licenses are unavailable or alternative technologies, content, business methods or branding business methods cannot be developed, we may be prevented from operating in certain jurisdictions or forced to pay significant royalties, materially harming our ability to compete and our business.

In addition to seasonality, our operating results may fluctuate based on our ability to attract and retain platform users, manage competition, expand into new or existing markets, and effectively maintain and manage growth rates. Other contributing factors include our ability to keep pace with technological changes, shifts in governmental regulations, potential harm to our brand or reputation, and other risks described elsewhere in this annual report. Our fast-paced growth has made, and may in the future make, these fluctuations more pronounced and harder to predict, which could prevent us from accurately forecasting our operating results.

For example, volatile political situations in certain Southeast Asian countries may impact our business. In Myanmar, after the military coup in February 2021, there have been ongoing instability disrupting our business activities in the country, and the situation may deteriorate further. In 2026, several countries in the region will have national, state and/or local elections, including Thailand, Malaysia and Vietnam, which may lead to a more politicized environment leading up to these elections. Any disruptions in our business activities or volatility or uncertainty in the economic, political or regulatory conditions in the markets in which we operate could adversely affect our business, financial condition, results of operations and prospects. Furthermore, heightened global geopolitical uncertainty may have spillover effects in the region. Because the laws in the countries in which we operate may change and their interpretation and enforcement may involve significant uncertainties, we cannot predict the effect of future developments in the legal regimes in these countries.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
