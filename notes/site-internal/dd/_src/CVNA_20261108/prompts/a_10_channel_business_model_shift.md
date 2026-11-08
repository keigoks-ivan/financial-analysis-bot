你是 stock-analyst v20 DD 的證據採集子 agent。標的：CVNA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Carvana Co. distribution channel disruption OR shift 2026
  - CVNA Carvana Co. business model transition subscription OR platform 2026
  - Auto & Truck Dealerships channel disintermediation D2C 2026
  - Carvana Co. go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm｜as_of：2026-02-18
<<<
Our Company Carvana is the leading e-commerce platform for buying and selling used cars. We are transforming the used car buying and selling experience by giving consumers what they want - a wide selection, great value and quality, transparent pricing, and a simple, no pressure transaction. Our differentiated business model combines a comprehensive online sales experience with a vertically integrated supply chain, designed to sell high-quality vehicles to our customers transparently and efficiently at a low price. The automotive retail industry is large – with approximately 37 million used auto retail transactions in the United States (“U.S.”) in 2024 according to Cox Automotive – and highly fragmented – with the top 10 used auto retailers in the U.S. accounting for less than 10% of the market share in 2024. These dynamics create an exceptional opportunity for disruption that our custom-built business model can capitalize on to remain well-positioned for long term growth. Over the years, we have leveraged our growing logistics network, which spans 316 metropolitan statistical areas, and our in-house distribution network, servicing over 80% of the U.S. population as of December 31, 2025, to sell 2.8 million retail vehicles, generating $84.1 billion in total revenue since inception in 2012 through December 31, 2025.

Business and Growth Strategies The foundation of our business is retail vehicle unit sales, which drives the majority of our revenue and allows us to capture additional revenue streams associated with financing, complementary products offerings, as well as trade-in vehicles. As we evolve, we believe we will continue to improve profitability associated with these revenues and expand our offering of complementary products. Because these additional opportunities originate with retail unit sales, our business strategy continues to center on growing retail units. Our ability to grow retail unit sales depends on penetrating existing markets, prudently expanding our geographic footprint, and strengthening our brand by delivering great value, transparency, and outstanding customer service. We continue to prioritize initiatives that raise conversion, improve delivery speed, and streamline customer support, each of which we believe reinforces brand trust and drives sustained demand.

With more than 37 million transactions in 2024, according to Cox Automotive, the used vehicle retail market represents a massive, highly fragmented industry, of which Carvana currently has an estimated market share of only approximately 1.6%. We believe we are well positioned to benefit from secular e-commerce trends. According to Federal Reserve Economic Data (FRED), e-commerce as a share of non-automotive retail has risen steadily for over 20 years and made up approximately 20% 4 of all non-automotive retail transactions as of 2025. Within the automotive retail industry, e-commerce adoption has lagged behind that of other retail segments, but we believe that as customers continue becoming more accustomed to making larger purchases online, e-commerce will make up an increasing share of automotive retail as it has in other retail segments. The large scale and fragmentation of the used retail vehicle market, coupled with the ongoing adoption of e-commerce more broadly, presents a differentiated opportunity for continued growth. Carvana intends to take advantage of this market opportunity by executing the following key elements of our growth strategy: Increase Sales Through Further Penetration of Our Existing Markets Our growth has historically been driven by opening new markets and increasing market penetration in our existing markets.…

Marketing We believe our customer base is relatively similar to that of the overall market for used cars at the average price points of our vehicles, with a slight shift toward younger customers. Our sales and marketing efforts utilize a multi-channel approach, built on a seasonality-adjusted, market-based model budget. We typically utilize a combination of brand building as well as direct response channels to efficiently seed and scale our local markets. Our paid advertising efforts include, but are not limited 5 to, advertisements through national and local television, search engine marketing, inventory site listing, social media, retargeting, organic referral, display, out-of-home, digital video, digital radio, direct mail, and branded pay-per-click channels. We believe our strong customer focus ensures customer loyalty which can drive both repeat purchases and referrals. In addition to our paid channels, we intend to attract new customers through enhancing our earned media and public relations efforts and further investing in our patented vending machines.

Competition With tens of thousands of automotive retailers in the U.S., the used car marketplace is a highly fragmented and highly competitive industry. We believe the primary competitive factors in this market include transparency, convenience, price, selection, and vehicle quality. Our current and future competitors include: •traditional used vehicle dealerships such as CarMax; •internet and online automotive sites, such as Amazon, Autobytel, AutoTrader, Cars, Carfax, CarGurus, eBay Motors, Edmunds, Google, KBB, and TrueCar; •providers of offline, membership-based car-buying services such as the Costco Auto Program; •new and used vehicle dealers or marketplaces with e-commerce business or online platforms; •marketplaces that could compete with our wholesale marketplace program; •automobile manufacturers such as Ford, General Motors, Toyota, Volkswagen, Tesla, Rivian, and Lucid; and •privately negotiated transactions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm｜as_of：2026-02-18
<<<
On July 19, 2023, the Company entered into an agreement (the "Distribution Agreement") to establish an ATM Program, and on July 31, 2024, the Company refreshed the ATM Program by entering into an Amended and Restated Distribution Agreement with Barclays Capital Inc., Citigroup Global Markets Inc., Moelis & Company LLC, and Virtu Americas LLC. On February 19, 2025, the Company further refreshed the ATM Program by entering into a Second Amended and Restated Distribution Agreement with Barclays Capital Inc., Citigroup Global Markets Inc., and Virtu Americas LLC. Under the ATM Program, the Company could sell up to the greater of (i) shares of Class A common stock representing an aggregate offering price of $1.0 billion, or (ii) an aggregate of 21 million shares of Class A common stock, from time to time. As of December 31, 2025, $461 million of aggregate offering price remained available to be sold under the ATM Program. During the year ended December 31, 2025, we issued 1.5 million shares of Class A common stock at a weighted-average issuance price per share of $364.93, for gross proceeds of $539 million. However, there can be no assurance that we will sell further shares of Class A common stock through the ATM Program, or otherwise.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
