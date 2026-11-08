你是 stock-analyst v20 DD 的證據採集子 agent。標的：EXPE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Expedia Group distribution channel disruption OR shift 2026
  - EXPE Expedia Group business model transition subscription OR platform 2026
  - Travel Services channel disintermediation D2C 2026
  - Expedia Group go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1324424/000132442426000008/expe-20251231.htm｜as_of：2026-02-13
<<<
Travel suppliers distribute and market products via our apps, desktop and mobile offerings, as well as through alternative distribution channels, our business partnerships and our call centers in order to reach our extensive global audience. In addition, our advertising and media businesses help other businesses, primarily travel providers, reach a large multi-platform audience of travelers around the globe.

Leverage Brand and Supply Strength to Power the Travel Ecosystem. We believe the strength of our core brand portfolio and consistent enhancements to our product and service offerings, combined with our global scale and broad-based supply, drive increasing value to customers and customer demand. With our significant global audience of travelers, and our deep and broad selection of travel products, we are also able to provide value to supply partners seeking to grow their business through sophisticated technology, a better understanding of travel retailing and reaching consumers in markets beyond their reach. Our deep product and supply footprint allows us to tailor offerings to target different types of consumers and travel needs, employ geographic segmentation in markets around the world, and leverage brand differentiation, among other benefits. We also market to consumers through a variety of channels, including internet search, metasearch and social and digital media. In 2025, we continued our investments in global market expansion beyond our core markets.

2 Table of Contents Expedia’s B2B partners can benefit from our technology and supply in the way that best suits their business. This includes connecting to Expedia Group's travel content through our API, Rapid; adopting one of our customized white label or co-branded ecommerce template solutions; or using our powerful agent booking tool, Expedia Travel Affiliate Agent Program ("TAAP"). We also offer an “optimized distribution” product to help hotel suppliers distribute wholesale rates through authorized channels.

Our marketing channels primarily include brand advertising through online and offline channels, loyalty programs, mobile apps, search engine marketing and optimization as well as metasearch, social media, direct and/or personalized traveler communications on our websites as well as through direct e-mail communication with our travelers. Our marketing programs and initiatives include promotional offers such as coupons as well as seasonal or periodic special offers from our travel suppliers based on our supplier relationships. More recently, we unified our existing loyalty programs into one global rewards platform called One Key spanning our core consumer brands, which launched in the United States in 2023, United Kingdom in 2024 and to a number of new markets across the globe on Brand Expedia in 2025 with the majority of Expedia Rewards members now migrated to the new program.

4 Table of Contents We developed proprietary technology to assist both hotel and alternative accommodation suppliers in managing and marketing their supply, whether this is direct through our proprietary central reservation tools or through third-party channel managers. Our “direct connect” technology allows suppliers to upload information about available products and services and rates directly from their central reservation systems and dynamically manage reservations and traveler needs through our messaging and chat platforms. Marketing tools assist hotels and alternative accommodations in tailoring demand to their requirements and our revenue management product provides pricing insights. We also offer an “Optimized Distribution” product to help hotel suppliers distribute wholesale rates through authorized channels. Our suite of white label website offerings power hotel, and package bookings on suppliers’own websites.

Competition Our brands compete in rapidly evolving and intensely competitive markets. We believe international markets represent especially large opportunities for Expedia Group and those of our competitors that wish to expand their brands and businesses to achieve global scale. We also believe that Expedia Group is one of only a few companies that are focused on building a truly global, travel marketplace. Our competition, which is strong and increasing, includes online and offline travel companies that target leisure and corporate travelers, including travel agencies, tour operators, travel supplier direct websites and their call centers, consolidators and wholesalers of travel products and services, large online companies including search, social media, marketplace, generative artificial intelligence ("Gen AI") and ride sharing businesses, companies offering AI agents, B2B businesses, as well as traditional consumer ecommerce and group buying websites. We face these competitors in local, regional, national and/or international markets. In some cases, competitors are offering more favorable terms and improved interfaces and technology to suppliers and travelers which make competition increasingly difficult. We also face competition for customer traffic on internet search engines and metasearch websites, which impacts our customer acquisition and marketing costs.

B2C. We differentiate ourselves from our competitors primarily based on the multiple channels we use to generate demand, quality and breadth of travel product supply, product features and usability of our websites and mobile apps, price or promotional offers, customer service, breadth and flexibility of our loyalty programs, as well as offline brand efforts. The emphasis on one or more of these factors varies, depending on the brand or business and the related target demographic. We face increasing competition from travel supplier direct websites. In some cases, supplier direct channels offer advantages to travelers, such as their own specific loyalty programs, complimentary services such as Wi-Fi, and better pricing. Our websites and apps feature travel products and services from numerous travel suppliers and allow travelers to combine products and services from multiple providers in one transaction. We face competition from airlines, hotels, alternative accommodation websites, rental car companies, cruise operators and other travel service providers, whether working individually or collectively, some of which are suppliers to our websites. Our business is generally sensitive to changes in the competitive landscape, including the emergence of new competitors or business models, and supplier consolidation.

B2B. We are one of the leading players in the global B2B travel space today servicing a wide range of customers across both travel and non-travel verticals including corporate travel management, airlines, offline travel agents, online retailers and financial institutions. We face competition from travel consolidators and wholesalers of travel products, other OTAs with B2B offerings, and other technology and content providers. We differentiate ourselves from our B2B competitors primarily with our breadth and depth of global supply, dedicated partner and traveler support, and market leading travel technology through our Rapid API, white label or co-branded template offerings, and Expedia TAAP, a powerful agent booking tool. We also offer an “optimized distribution” product to help hotel suppliers distribute wholesale rates through authorized channels. Our extensive work building out our global supply has allowed us to negotiate competitive pricing with suppliers and provide added value to travelers. We intend to continue to grow the business via a combination of increasing our wallet share with existing customers, winning contracts with new customers, as well as the introduction of additional products and services.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EXPE_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
