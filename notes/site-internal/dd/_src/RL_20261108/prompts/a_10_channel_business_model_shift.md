你是 stock-analyst v20 DD 的證據採集子 agent。標的：RL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Ralph Lauren distribution channel disruption OR shift 2026
  - RL Ralph Lauren business model transition subscription OR platform 2026
  - Apparel Manufacturing channel disintermediation D2C 2026
  - Ralph Lauren go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-21）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm｜as_of：2026-05-21
<<<
Item 1. Business. General Founded in 1967 by Mr. Ralph Lauren, we are a global leader in the design, marketing, and distribution of luxury lifestyle products, including apparel, handbags, footwear & accessories, fragrances, home, and hospitality. For nearly 60 years, Ralph Lauren has sought to inspire the dream of a better life through authenticity and timeless style. Our long-standing reputation and distinctive image have been developed across a wide range of products, brands, distribution channels, and international markets. We believe that our global reach, breadth of lifestyle product offerings, and multi-channel distribution network are unique among luxury and apparel companies.

We diversify our business by geography (North America, Europe, and Asia, among other regions) and channel of distribution (retail, wholesale, and licensing). This allows us to maintain a dynamic balance as our operating results do not depend solely on the performance of any single geographic area or channel of distribution. We sell directly to consumers through our integrated retail channel, which includes our retail stores, concession-based shop-within-shops, and digital commerce operations around the world. Our wholesale sales are made principally to major department stores, specialty stores, and third-party digital partners around the world, as well as to certain third-party-owned stores to which we have licensed the right to operate in defined geographic territories using our trademarks. In addition, we license to third parties for specified periods and geographies the right to access our various trademarks in connection with the licensees' manufacture and sale of designated products, such as certain apparel categories, eyewear, fragrances, and home furnishings.

Our global reach is extensive, as we sell directly to customers throughout the world via our 594 retail stores and 644 concession-based shop-within-shops, as well as through our own digital commerce sites and those of various third-party digital partners. Merchandise is also available through our wholesale distribution channels at approximately 9,500 doors worldwide, the majority in specialty stores, as well as through the digital commerce sites of many of our wholesale customers. In addition to our directly-operated stores and shops, our international licensing partners operate 135 stores.

Objectives and Opportunities Our purpose is to inspire the dream of a better life through authenticity and timeless style. We believe that our size and the global scope of our operations provide us with design, sourcing, and distribution synergies across our business. Our core strengths include a portfolio of luxury lifestyle products spanning across five categories: Apparel, Handbags, footwear & accessories, Fragrances, Home, and Hospitality; a well-diversified global multi-channel distribution network; an investment philosophy supported by a strong balance sheet; and an experienced management team. Despite the various risks and uncertainties associated with the current global economic environment, as discussed further in Item 7 — "Management's Discussion and Analysis of Financial Condition and Results of Operations — Global Economic Conditions and Industry Trends," we believe our core strengths will allow us to effectively execute our long-term growth strategy.

Our lifestyle brand image is reinforced by our distribution through our stores and concession-based shop-within-shops, our wholesale channels of distribution, our global digital commerce sites, and our Ralph Lauren restaurants and cafés. We sell our products under the following key brand platforms: 1.Ralph Lauren Luxury — Our Luxury group includes: Ralph Lauren Collection and Ralph Lauren Purple Label. Ralph Lauren Collection embodies the highest expression of chic, feminine glamour. Each piece is inspired by a vision of timeless luxury and modern elegance and is crafted with unparalleled passion and artistry. For men, Ralph Lauren Purple Label is the ultimate expression of luxury for the modern gentleman. Refined suitings are hand-tailored, including custom made-to-measure suits crafted in the time-honored traditions of Savile Row. Purple Label's sophisticated sportswear is designed with a meticulous attention to detail, capturing the elegance and ease of Ralph Lauren's signature, timeless style. Ralph Lauren Collection and Ralph Lauren Purple Label are made predominantly in Italy with the utmost attention to detail and quality and are available in select Ralph Lauren stores around the world, an exclusive selection of the finest specialty stores, and online at our Ralph Lauren digital commerce sites, including RalphLauren.com.

Our Retail Business Our retail business sells directly to customers throughout the world via our 594 retail stores and 644 concession-based shop-within-shops, totaling approximately 4.1 million and 0.7 million square feet, respectively, as well as through our own digital commerce sites and those of various third-party digital partners. We operate our business using a global omni-channel retailing strategy that seeks to deliver an integrated shopping experience with a consistent message of our brands and products to our customers, regardless of whether they are shopping for our products in physical stores or online. We also continue to scale and expand our Online to Offline capabilities to enhance the consumer experience, which include Online Appointment Bookings, Digital Clienteling, Endless Aisle, Buy Online-Ship from Store, Buy Online-Pick Up in Store, Same-Day Delivery, and Mobile Point of Sale and contactless payments, among other capabilities.

The following table presents the number of outlet stores by segment as of March 28, 2026: Outlet Stores North America 166 Europe 54 Asia 87 Total 307 Our outlet stores range in size from approximately 1,100 to 28,300 square feet. Outlet stores obtain products from our suppliers, our product licensing partners, and our other retail stores and digital commerce operations, and also serve as a secondary distribution channel for our excess and out-of-season products.

The primary product offerings sold through our wholesale channels of distribution include apparel, handbags, footwear & accessories, and home product assortments. Our luxury brands, including Ralph Lauren Collection and Ralph Lauren Purple Label, are distributed worldwide through a limited number of premier fashion retailers. In North America, our wholesale business is comprised primarily of sales to department stores, and to a lesser extent, specialty stores. In Europe, our wholesale business is comprised primarily of a varying mix of sales to both department stores and specialty stores, depending on the country, as well as to various third-party digital partners. In Asia, our wholesale business is comprised primarily of sales to department stores and various third-party digital partners. We also distribute our wholesale products to certain licensed stores operated by our partners in Asia, Europe, Latin America, and emerging markets.

We sell most of our excess and out-of-season products through secondary distribution channels worldwide, including our retail outlet stores.

Wholesale Distribution Channels The following table presents by segment the approximate number of our primary full-price wholesale doors of distribution as of March 28, 2026: Doors North America 3,050 Europe 5,700 Asia 750 Total 9,500 In addition to our conventional wholesale doors, our products are increasingly being sold through the websites of many of our traditional wholesale customers, as well as those of our third-party digital partners. As of March 28, 2026, our wholesale business served approximately 110 third-party digital partners, primarily in Europe.

•attract consumer traffic to stores, shop-within-shops, and digital commerce sites; •source sustainable and traceable raw materials at cost-effective prices; •anticipate and maintain proper inventory levels; •ensure product availability and optimize supply chain and distribution efficiencies; •maintain and grow market share; •recruit and retain talent to operate our retail stores, distribution centers, and various corporate functions; •protect our intellectual property; and •withstand prolonged periods of adverse economic conditions or business disruptions.

16 Distribution To facilitate global distribution, our products are shipped from manufacturers to a network of distribution centers around the world for inspection, sorting, packing, and delivery to our retail locations and digital commerce and wholesale customers. This network includes the following primary distribution facilities: Facility Location Geographic Region Serviced Facility Ownership N. Pendleton Street, High Point, North Carolina U.S. Owned NC Highway 66, High Point, North Carolina U.S. Leased Toronto, Ontario Canada Third-party Parma, Italy Europe and Latin America Third-party Yokohama, Japan Japan Third-party Bugok, South Korea South Korea Leased Tuen Mun, Hong Kong China and Southeast Asia(a)

Our retail operation systems, including point-of-sale registers and merchandising, planning, and inventory management systems, support operational processes within our store network and link with our digital commerce processes to support omni-channel capabilities.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-21）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm｜as_of：2026-05-21
<<<
We diversify our business by geography (North America, Europe, and Asia, among other regions) and channel of distribution (retail, wholesale, and licensing). This allows us to maintain a dynamic balance as our operating results do not depend solely on the performance of any single geographic area or channel of distribution. We sell directly to consumers through our integrated retail channel, which includes our retail stores, concession-based shop-within-shops, and digital commerce operations around the world. Our wholesale sales are made principally to major department stores, specialty stores, and third-party digital partners around the world, as well as to certain third-party-owned stores to which we have licensed the right to operate in defined geographic territories using our trademarks. In addition, we license to third parties for specified 44 periods and geographies the right to access our various trademarks in connection with the licensees' manufacture and sale of designated products, such as certain apparel categories, eyewear, fragrances, and home furnishings.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
