你是 stock-analyst v20 DD 的證據採集子 agent。標的：CVNA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - CVNA Carvana Co. market share gaining OR losing 2026
  - Carvana Co. new entrant OR displace threat Auto & Truck Dealerships 2026
  - CVNA competitor design win 2026
  - Carvana Co. vs Auto & Truck Dealerships peers market share trend 2025 2026


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

Strengths and Competitive Advantages We aim to deliver the best selection, the best value, and the best experience for used car buyers and sellers. Since our inception, we have been developing and leveraging the following key strengths, which we believe provide for significant competitive advantages.

With more than 37 million transactions in 2024, according to Cox Automotive, the used vehicle retail market represents a massive, highly fragmented industry, of which Carvana currently has an estimated market share of only approximately 1.6%. We believe we are well positioned to benefit from secular e-commerce trends. According to Federal Reserve Economic Data (FRED), e-commerce as a share of non-automotive retail has risen steadily for over 20 years and made up approximately 20% 4 of all non-automotive retail transactions as of 2025. Within the automotive retail industry, e-commerce adoption has lagged behind that of other retail segments, but we believe that as customers continue becoming more accustomed to making larger purchases online, e-commerce will make up an increasing share of automotive retail as it has in other retail segments. The large scale and fragmentation of the used retail vehicle market, coupled with the ongoing adoption of e-commerce more broadly, presents a differentiated opportunity for continued growth. Carvana intends to take advantage of this market opportunity by executing the following key elements of our growth strategy: Increase Sales Through Further Penetration of Our Existing Markets Our growth has historically been driven by opening new markets and increasing market penetration in our existing markets.…

Competition With tens of thousands of automotive retailers in the U.S., the used car marketplace is a highly fragmented and highly competitive industry. We believe the primary competitive factors in this market include transparency, convenience, price, selection, and vehicle quality. Our current and future competitors include: •traditional used vehicle dealerships such as CarMax; •internet and online automotive sites, such as Amazon, Autobytel, AutoTrader, Cars, Carfax, CarGurus, eBay Motors, Edmunds, Google, KBB, and TrueCar; •providers of offline, membership-based car-buying services such as the Costco Auto Program; •new and used vehicle dealers or marketplaces with e-commerce business or online platforms; •marketplaces that could compete with our wholesale marketplace program; •automobile manufacturers such as Ford, General Motors, Toyota, Volkswagen, Tesla, Rivian, and Lucid; and •privately negotiated transactions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1690820/000169082026000009/cvna-20251231.htm｜as_of：2026-02-18
<<<
The used car marketplace is a highly fragmented and highly competitive industry. We face significant competition from companies that provide listings, information, lead generation, and car-buying and selling services designed to reach businesses and consumers and enable dealers to reach these consumers and inventory sources. Our current and future competitors may include: •traditional used vehicle dealerships such as CarMax; •internet and online automotive sites, such as Amazon, Autobytel, AutoTrader, Cars, Carfax, CarGurus, eBay Motors, Edmunds, Google, KBB, and TrueCar; 13 •providers of offline, membership-based car-buying services such as the Costco Auto Program; •new and used vehicle dealers or marketplaces with e-commerce business or online platforms; •marketplaces that could compete with our wholesale marketplace program; •automobile manufacturers such as Ford, General Motors, Toyota, Volkswagen, Tesla, Rivian, and Lucid; and •privately negotiated transactions.

We also expect that competitors, both new and existing, will continue to enter the online and traditional automotive retail industry with competing brands, business models, products, and services, which could make it difficult to acquire inventory, attract customers, and sell vehicles at a profitable price. Some of these companies may have significantly greater resources than we do and may be able to provide customers access to a greater inventory of vehicles at lower prices or purchase vehicles from consumers at higher prices while delivering a competitive online experience. Additionally, there can be no assurance we will not experience competition from DriveTime, the company from which we were spun off and with which we currently have certain business relationships. Furthermore, we have a cross-license agreement with DriveTime pursuant to which DriveTime has obtained limited licenses to some of our intellectual property, which could impact our competitive position.

Our competitors may also develop and market new technologies that render our existing or future business model, products, and services less competitive, unmarketable, or obsolete. For example, rapid changes in technology, including rideshare services and the development of autonomous vehicles, including those developed by Waymo and Tesla, could lead to a decrease in demand for our products. Competitors may also impede our ability to reach consumers or commence operations in certain jurisdictions. For example, we depend in part on internet search engines, lead generators, automotive finance partners, social networking sites, AI tools, and vehicle listing sites to drive traffic to our website and mobile application and our competitors may increase their search engine optimization efforts and outbid us for search terms on various search engines, use their political influence and increase lobbying efforts, or align with Internet search engine providers to receive a higher search result page ranking than ours. Any reduction in the number of users directed to our website and mobile application through internet search engines, lead generators, automotive finance providers, social networking sites, AI tools, or vehicle listing sites, could harm our business and operating results. In addition, technology related to generative AI is advancing rapidly, and its future impact on the automotive ecosystem is unknown.…

In addition, if one or more of our competitors, or DriveTime, were to merge or partner with another of our competitors, the change in the competitive landscape could adversely affect our ability to compete effectively. Our competitors may also establish or strengthen cooperative relationships with our current or future data providers, technology partners, or other parties with whom we have relationships, thereby limiting our ability to develop, improve, and promote our solutions. We may not be able to compete successfully against current or future competitors, and competitive pressures may harm our revenue, business, and financial results.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
