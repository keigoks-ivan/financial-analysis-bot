你是 stock-analyst v20 DD 的證據採集子 agent。標的：UBER。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - UBER Uber Technologies market share gaining OR losing 2026
  - Uber Technologies new entrant OR displace threat Software - Application 2026
  - UBER competitor design win 2026
  - Uber Technologies vs Software - Application peers market share trend 2025 2026


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

•Delivery. Our Delivery offering competes with numerous companies in the meal, grocery and other delivery space in various regions for Drivers, consumers, and merchants, including DoorDash, Instacart, Gopuff, Rappi, Delivery Hero, Just Eat Takeaway, and Amazon. Our Delivery offering also competes with restaurants and other merchants, including those that offer their own delivery and/or take-away, meal kit delivery services, grocery delivery services, and traditional grocers.

Antitrust Competition authorities closely scrutinize us under U.S. and foreign antitrust and competition laws. An increasing number of governments are enforcing competition laws and are doing so with increased scrutiny, including governments in large markets such as the EU, the United States, Brazil, and India, particularly surrounding issues of pricing parity, price-fixing, and abuse of market power. In addition, governmental agencies and regulators may, among other things, prohibit future acquisitions, divestitures, or combinations we plan to make, impose significant fines or penalties, require divestiture of certain of our assets, or impose other restrictions that limit or require us to modify our operations, including limitations on our contractual relationships with platform users or restrictions on our pricing models.

Research and Development Because the industries in which we compete are characterized by rapid technological advances, our ability to compete successfully depends heavily upon our ability to ensure a continual and timely flow of competitive new offerings and technologies. We continue to develop new technologies to enhance existing offerings and services, and to expand the range of our offerings through research and development (“R&D”) and acquisition of third-party businesses and technology.

Our success depends in large part on our ability to attract and retain high-quality management, operations, engineering, and other personnel who are in high demand, are often subject to competing employment offers, and are attractive recruiting targets for our competitors.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm｜as_of：2026-02-13
<<<
•We may fail to offer autonomous vehicle technologies on our platform at competitive scale, fail to offer such technologies or scale on our platform before our competitors, or such technologies may fail to perform as expected, may be inferior to those offered by our competitors, or may be perceived as less safe than those offered by competitors or non-autonomous vehicles.

The mobility, delivery, and logistics industries are highly competitive, with well-established and low-cost alternatives that have been available for decades, low barriers to entry, low switching costs, and well-capitalized competitors in nearly every major geographic region. If we are unable to compete effectively in these industries, our business and financial prospects would be adversely impacted.

Our platform provides offerings in the mobility, delivery, and logistics industries. We compete on a global basis, and the markets in which we compete are highly fragmented. We face significant competition in each of the mobility and delivery industries globally and in the logistics industry in the United States and Canada from existing, well-established, and low-cost alternatives, and in the future we expect to face competition from new market entrants given the low barriers to entry that characterize these industries. In addition, within each of these markets, the cost to switch between products is low. Consumers have a propensity to shift to the lowest-cost or highest-quality provider; Drivers have a propensity to shift to the platform with the highest earnings potential; restaurants and other merchants have a propensity to shift to the delivery platform that offers the lowest service fee for their meals and other goods and provides the highest volume of orders; and Shippers and Carriers have a propensity to shift to the platform with the best price and most convenient service for hauling shipments.

Further, while we work to expand globally and introduce new products and offerings across a range of industries, many of our competitors remain focused on a limited number of products or on a narrow geographic scope, allowing them to develop specialized expertise and employ resources in a more targeted manner than we do. As we and our competitors introduce new products and offerings, and as existing products and offerings evolve, we expect to become subject to additional competition. In addition, our competitors may adopt certain of our product or offering features, or may adopt innovations that Drivers, consumers, merchants, Shippers, and Carriers value more highly than ours, which would render our products or offerings less attractive or reduce our ability to differentiate our products or offerings. Increased competition could result in, among other things, a reduction of the revenue we generate from the use of our platform, the number of platform users, the frequency of use of our platform, and our margins.

We face competition in each of our offerings, including: •Mobility. Our Mobility offering competes with personal vehicle ownership and usage, which accounts for the majority of passenger miles in the markets that we serve, and traditional transportation services, including taxicab companies and taxi-hailing services, livery and other car services. In addition, public transportation can be a superior substitute to our Mobility offering and in many cases, offers a faster and lower-cost travel option in many cities. We also compete with other ridesharing companies, including certain of our minority-owned entities, for Drivers and riders, including Bolt, Didi, Lyft, and Ola. There are also a number of companies developing and introducing autonomous vehicles and technologies 12 that either are competing with us or may compete with us in the future, including Alphabet (Waymo), Amazon (Zoox), and Tesla.

Many of our competitors are well-capitalized and offer discounted services, Driver incentives, consumer discounts and promotions, innovative products and offerings, and alternative pricing models, which may be more attractive to consumers than those that we offer. Further, some of our current or potential competitors have, and may in the future continue to have, greater resources and access to larger Driver, consumer, merchant, Shipper, or Carrier bases in particular geographic markets. In addition, our competitors in certain geographic markets enjoy substantial competitive advantages such as greater brand recognition, longer operating histories, larger marketing budgets, better localized knowledge, and more supportive regulatory regimes. As a result, such competitors may be able to respond more quickly and effectively than us in such markets to new or changing opportunities, technologies, consumer preferences, regulations, or standards, which may render our products or offerings less attractive. In addition, future competitors may share in the effective benefit of any regulatory or governmental approvals and litigation victories we may achieve, without having to incur the costs we have incurred to obtain such benefits.

As a result of certain divestitures, we are contractually restricted from competing with our current or former minority-owned entities with respect to certain aspects of our business, including in Southeast Asia through one year after we dispose of all interests in Grab, and the Middle East, North Africa and Pakistan through two years after we dispose of all interests in Careem Technologies, while our minority-owned entities are not necessarily restricted from competing with us anywhere in the world. In addition, we are contractually restricted from competing with some of our majority-owned entities with respect to certain aspects of our business, including competing against Uber Freight with respect to freight brokerage.

We receive a high degree of negative media coverage around the world, which adversely affects our brand and reputation and fuels distrust of our company. Negative publicity adversely affects our brand and reputation, makes it difficult for us to attract and retain platform users, reduces confidence in and use of our products and offerings, invites continued legislative and regulatory scrutiny, and results in additional litigation and governmental investigations. As a result, our competitors raised additional capital, increased their investments in certain markets, and improved their category positions and market shares, and may continue to do so.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
