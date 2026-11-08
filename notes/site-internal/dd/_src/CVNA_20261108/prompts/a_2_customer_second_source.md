你是 stock-analyst v20 DD 的證據採集子 agent。標的：CVNA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_second_source] 客戶 second-source 與 in-house
Q: 最大客戶是否正在導入第二供應商，或將此環節自製（in-house）？
  - CVNA Carvana Co. largest customer second-source OR in-house 2026
  - custom chip OR component second source agreement 2026
  - Carvana Co. single-source risk customer diversify supplier
  - in-house design OR insourcing Auto & Truck Dealerships 2026
  (na_allowed=true)


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

Inspection and Reconditioning. Once we acquire a vehicle, we leverage our in-house logistics network or a vendor to transport the vehicle to one of our inspection and reconditioning centers ("IRC") or auction locations with reconditioning capabilities (together with IRCs, "Reconditioning Sites"), at which point the vehicle enters our inventory management system. We then begin an inspection process covering controls, features, brakes, tires, and cosmetics. Each Reconditioning Site leverages proprietary inventory management technology and includes trained technicians, vehicle lifts, paintless dent repair, and paint capabilities, and receives on-site support from vendors with whom we have integrated systems to expedite ready access to parts and materials. We have a uniform set of cosmetic standards across all Reconditioning Sites to provide a consistent customer experience. When an inspection is complete, we estimate the necessary reconditioning cost for the vehicle to meet our standards and expected timing for that vehicle to be made available for sale on our website. Vehicles that do not meet Carvana standards are sold wholesale, either through our wholesale marketplace platform or through third party auctions.

Financing. We offer integrated financing using our proprietary loan origination platform. Customers who choose to apply for our in-house financing fill out a short prequalification form, and, if approved, are nearly instantaneously presented with an interactive set of conditional financing terms generated by our proprietary credit scoring and deal structuring algorithms for every vehicle in our inventory. Our financing tool is designed to intuitively and transparently show the relationship between down payment, monthly payment, and loan term to assist the customer in selecting a payment plan tailored to their specific needs. This pre-approval involves a short process that does not impact customers’ credit unless they pursue a purchase and finance the transaction. For customers who choose not to utilize our financing, we also accept payment in cash or financing from third party lenders, such as banks or credit unions.

Nationwide Logistics Network and Distinctive Fulfillment Experience. We have developed proprietary logistics software and an in-house nationwide delivery network designed to predictably and efficiently transport cars and provide customers with a distinctive fulfillment experience. Our logistics network and technologies that support it are based on a "hub and spoke" model, which connects Reconditioning Sites to vending machines and hubs via our fleet of multi-car and single-car haulers. This allows us to efficiently manage locations, routes, route capacities, trucks, and drivers while also dynamically optimizing for speed and cost. This proprietary logistics infrastructure enables us to offer our customers and operations team highly accurate predictions of vehicle availability, to minimize delays, and promote a seamless and reliable customer experience. We offer customers in our markets a home delivery option that is typically conducted by a Carvana employee on a branded hauler. Customers in certain markets can also pick up their vehicles at one of our patented car vending machines, which are multi-story glass towers that store purchased vehicles, or at other customer-facing locations. As of December 31, 2025, we estimate that 75% of the U.S. population is within 100 miles of an IRC or auction site, which shortens the distance from our inventory pools to our customers to reduce delivery times.

Purpose-Built Vertically Integrated E-commerce Platform We believe our proprietary technology and vertically integrated business model allow us to enjoy a significantly lower variable cost structure versus traditional dealerships and to provide substantial value to our customers by providing a seamless, best-in-class car buying and selling experience. Our vertically integrated platform gives us control of all critical operations and transaction elements to allow us to facilitate a fast, simple, and consistent user experience. We control the algorithms that help determine the vehicles we make available to our customers, the prices of those vehicles, the financing terms offered to customers, complementary products, and the purchase prices and trade-in values we offer. Additionally, we control the logistics infrastructure that enables us to offer customers fast, specific, and reliable delivery and pick-up times. We have invested heavily in our customer-facing website to provide an intuitive user interface and have built a team of in-house customer advocates that is dedicated to providing first-rate customer service.

Efficient Logistics Network and Distinctive Fulfillment Experience We have developed proprietary logistics software and an in-house delivery network that differentiates us from competitors, and which is designed to predictably and efficiently transport cars while providing customers with a distinctive fulfillment experience. Our home delivery and pickup is typically conducted by a Carvana employee on a branded hauler, as soon as the same day in certain markets, depending on availability and location. Customers in certain markets can also pick up or drop off their vehicles at one of our patented car vending machines, or at another customer-facing location. Our vending machines provide an attractive and unique pickup experience for our customers and develop brand awareness while lowering our variable fulfillment expenses. Following the opening of a vending machine in one of our markets, our market penetration has typically seen a meaningful increase while our variable operating costs per vehicle sold have typically decreased.

Since the launch of our first market thirteen years ago, our vertically integrated, customer-centered offering has enabled us to become one of the largest and fastest growing used automotive retailers in the U.S. as of December 31, 2025. Throughout 2025, we remained focused on profitable growth and fundamental operating efficiency, balancing long-term benefits of scale with the continued opportunities we see to further enhance customer experiences. We have physical infrastructure for continued growth, which gives us capacity to recondition approximately 1.5 million vehicles per year.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/parts/axes_2.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
