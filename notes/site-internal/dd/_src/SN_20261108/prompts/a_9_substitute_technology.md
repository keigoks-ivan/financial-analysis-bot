你是 stock-analyst v20 DD 的證據採集子 agent。標的：SN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - SharkNinja product substitute technology threat 2026
  - Furnishings, Fixtures & Appliances alternative technology disruption 2026 2027
  - SN SharkNinja technology obsolescence risk
  - Furnishings, Fixtures & Appliances next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm｜as_of：2026-03-02
<<<
SharkNinja: World-Class Household Appliance Brands Built on Continuous, Disruptive Innovation SharkNinja is a global product design and technology company that creates 5-star rated lifestyle solutions through innovative products for consumers around the world. We seek to leverage our global, agile and cross-functional engineering know-how, product development and manufacturing expertise along with our solutions-driven marketing to increase the efficiency, convenience and enjoyment of consumers’ daily tasks and improve everyday lives. We have built two billion-dollar brands, Shark and Ninja, and have a proven track record of establishing leadership positions by disrupting numerous household product categories, including Cleaning Appliances, Cooking and Beverage Appliances, Food Preparation Appliances and Beauty and Home Environment Appliances. We have successfully gained market share across geographies, taking share from competitors priced both above and below our offerings. We believe our success is centered around our advanced engineering and innovation capabilities coupled with our deep understanding of consumer needs, enabling us to solve consumer problems that others either do not see or are unable to solve.

Our proven track record of bringing disruptive products to market and developing one consumer solution after another has allowed us to enter into multiple product categories, driving significant growth and market share gains. As we continue to innovate, typically our legacy products continue to be sold at more accessible price points, which diversifies our product offering across price points within a category and creates increasing market share positions. We believe our products have broad appeal across income brackets as we aim to deliver industry-leading innovation, design and product quality at compelling value. As a result, we aim to acquire market share from higher and lower priced competitors. We believe our products are aspirational, offering the performance of more expensive competitor products, and attainable, representing a compelling value.

1 Scaled Engineering Powerhouse Focused on Disruptive Innovation and Continuous Optimization SharkNinja aims to continuously innovate products that exceed consumer expectations.

To win in the market, we leverage the diverse expertise of our cross-functional design and engineering teams to capitalize on our deep knowledge of consumer needs. We have a dynamic, in-house global product design team located across the United States, the United Kingdom and China that collaborates seamlessly to integrate unique local market insights into the design and functionality of our products. Our engineering prowess drives our new product innovation, including design, construction, material performance requirements, manufacturing protocols, supplier selection, packaging specifications and quality assurance. Our scaled engineering organization possesses wide-ranging skillsets across mechanical design, mechatronics, electronics engineering, robotics, firmware, app and cloud, deep learning, algorithmic engineering and industrial design. Our team of over 700 cross-functional engineering and design associates is integrated across Shark and Ninja solutions, introducing disruptive technologies within our portfolio to new market segments, in addition to accessing the latest technologies from across the globe. The breadth of our engineering team’s competencies allows us to develop innovative products, while our global collaboration produces a rapid and iterative development cycle.

Delivering Critical Consumer Value Points with Every Product We believe that SharkNinja is differentiated by our ability to innovate while identifying and solving consumer pain points that others either do not see or are unable to solve. SharkNinja strives to deliver on all four of the following critical consumer value points in every innovative product we bring to market: Speed: Deliver first-to-market disruptive innovations Our global consumer insights and product development approach enables us to discover some of the most pressing consumer problems and develop innovative solutions to solve them. Our global product development team collaborates around the world, producing an ongoing cycle of development and increasing our speed of innovation and ultimately our speed to market. Whether it is a first-to-market innovation in an emerging category or our disruption of a mature category with new technologies, we redefine what is possible. Our differentiated pace of innovation enables us to be first-to-market in many product sub-categories. We have rapidly grown our market share and launched new products, often faster than our competitors, creating competitive advantages that are designed to deliver strong and sustainable growth.

Value: Deliver products at accessible prices for incredible value We are obsessed with delivering world-class, innovative products to every consumer in every home in our global markets at great value. With our consumers always in mind, we have built hyper-efficient, global product design and supply chain organizations designed to deliver the perfect product at a compelling price. We believe that, in purchasing our products, our consumers receive the greatest value and a high level of performance for every hard-earned dollar they spend. We accomplish this through our design and manufacturing engineering team and our on-the-ground sourcing organization in Asia, which facilitates a competitive bidding process across numerous manufacturers to secure favorable pricing terms. Furthermore, we are a crucial partner to many of our manufacturers given the scale of our brands. This allows us to enter new categories that are dominated by a few big players, disrupt them through innovation and compelling value and grow the overall market while gaining market share.

Expanding the product assortment and retailer placements of our new categories Within the new categories we enter, we expand our product assortment, further disrupting these markets and growing retailer placements of our new products.

We consistently launch into new categories to bring original consumer-centric innovations to market. Year after year, SharkNinja has accelerated its pace of growth by entering and capturing share in 38 sub-categories, swiftly disrupting and gaining leading market share in many of them. In the past three years alone, we have entered and disrupted the following product sub-categories: outdoor ovens, carbonation, drinkware, wet/dry cleaning floor products, carpet extraction, fans, coolers, frozen drink appliances, skincare, propane grills and fire pits. These new product sub-categories not only increase our household penetration but also expand use occasions, the number of products per home and our brand presence across households.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm｜as_of：2026-03-02
<<<
The pace of technological change continues to accelerate and our ability to react effectively to such change may present significant competitive risks.

The pace of technological change is increasing at an exponential rate. To remain competitive, we must invest in developing tools and processes to improve the speed at which we are able to develop competitive products, including significant investment in the development and advancement of new technologies, such as artificial intelligence, data analytics, robotics, sensor technology, data storage, among others, as well as other technologies in the future that are not foreseen today. Failure to adapt or react effectively to such changes could adversely affect our business, financial condition and results of operations.

From time to time we have been, and expect we will continue to be, subject to claims that we are infringing the patents and other intellectual property of others, and it is possible that third parties will assert infringement, misappropriation, unfair competition or similar claims against us in the future. An adverse finding against us in these or similar patent or other intellectual property litigation or disputes may have a material adverse effect on our business, financial condition and results of operations. Any such claims, with or without merit, could be time consuming and expensive and may require us to incur substantial costs, including the diversion of the resources of management and technical personnel, cause product delays or require us to redesign our products or enter into licensing or other agreements in order to secure continued access to necessary or desirable intellectual property. If we are deemed to be infringing or otherwise violating a third party’s intellectual property and are unable to continue using that intellectual property as we had been, our business and results of operations could be harmed if we are unable to successfully develop non-infringing alternative products or features on a timely basis or license non-infringing alternatives or substitutes, if any exist, on commercially reasonable terms.…

Certain of our packaging materials and products sold through, and/or facilities operated under, each of our business segments are regulated by the CPSC, the Federal Communications Commission, the U.S. Environmental Protection Agency, the Occupational Safety and Health Administration, the U.S. Food and Drug Administration (the “FDA”), the FTC and other federal or state consumer protection and product safety agencies and are subject to the regulations such agencies enforce, as well as by similar state, foreign and multinational agencies and regulations. Failure to comply with such regulatory requirements could result in government-imposed fines, stop sale orders or other penalties, as well as consumer litigation. Our inability to obtain, or the cancellation of, any registration or approval required by such agencies could have an adverse effect on our business, financial condition and results of operations. The severity of the effect could depend, among other things, on factors such as which products were involved, whether another product could be substituted and whether our competitors were similarly affected. We attempt to anticipate regulatory developments and maintain registrations of, and access to, substitute chemicals and other ingredients, but we may not always be able to avoid or minimize these risks.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SN_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
