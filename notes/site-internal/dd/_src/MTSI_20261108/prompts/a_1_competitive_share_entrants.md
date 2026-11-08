你是 stock-analyst v20 DD 的證據採集子 agent。標的：MTSI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MTSI MACOM Technology Solutions Holdings market share gaining OR losing 2026
  - MACOM Technology Solutions Holdings new entrant OR displace threat 半導體 / 光通訊 / RF 2026
  - MTSI competitor design win 2026
  - MACOM Technology Solutions Holdings vs 半導體 / 光通訊 / RF peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm｜as_of：2025-11-14
<<<
Certain of our products have long life cycles ranging from five to ten years, with some of our products generating revenue for over 20 years while others may have shorter life cycles of less than five years. We continue to develop new products and technologies to improve our ability to serve our primary markets. Our growth strategy is focused on expanding our addressable markets and product portfolio, strengthening our customer relationships and capturing more design wins in order to increase our market share. As we grow our portfolio and technology base, we believe our customers will select more of our components for use in their systems.

Research and Development Our research and development efforts aim to rapidly develop new and innovative products, process technologies and packaging techniques. The interaction of semiconductor process technology, circuit design and packaging technology defines the performance parameters and differentiation of our products. We believe some of our core competencies are the ability to model, design, test, integrate, package and manufacture differentiated solutions for our customers. We leverage these core competencies to solve difficult and complex challenges that our customers face during their system design phases. We believe our integrated and customized solutions offer customers high performance, quality, reliability and faster time to market.

Competition The markets for our products are highly competitive and are characterized by continuously evolving customer requirements. We believe that the principal competitive factors in our markets include: ▪the ability of engineering talent to drive innovation and new product development; ▪the ability to timely design and deliver products and solutions that meet or exceed customers’ performance, reliability and price requirements; ▪the breadth and diversity of product offerings; 6 ▪the ability to provide a reliable supply of products in sufficient quantities and in a timely manner; ▪the quality of customer service and technical support; and ▪the financial reliability, operational stability and reputation of the supplier.

We believe that we compete favorably with respect to these factors. We compete primarily with both our customers’ internal design resources and other suppliers of high-performance analog semiconductor solutions for use in wireless and wireline RF, microwave, millimeter wave and photonic applications, some of whom have greater financial resources and scale than us. We expect competition in our markets to change as new competitors enter these markets, existing competitors merge or form alliances and new technologies emerge. We believe that in the future there will be increased competition from companies utilizing alternative technologies, including high-volume manufacturers using low-cost silicon process technology. Some of our competitors are also our customers, and in certain product categories we compete with semiconductor manufacturers from which we also obtain foundry services.

The majority of our internal wafer fabrication and internal assembly and test operations are conducted at our Lowell, Massachusetts headquarters and our RTP, North Carolina wafer fabrication facility. We also operate other wafer fabrication facilities in Ann Arbor, Michigan and in Limeil-Brévannes, France. We believe having U.S.-based wafer fabrication is a competitive advantage for us over competitors that do not have this capability, because it enables us to offer proprietary processes, and provides us with greater control over quality, a secure source of supply and a domestic source for U.S. I&D customers. We also believe that our U.S.-based wafer fabrication facilitates shorter time to market for both new and existing products, shorter production lead times than if we 7 utilized external foundries and allows us to efficiently produce a wide range of low, medium and high-volume products. We perform internal assembly and test functions at our Lowell, Massachusetts, Nashua, New Hampshire, Ann Arbor, Michigan, Hamilton, New Jersey, Morgan Hill, California, Limeil-Brévannes, France and Hsinchu, Taiwan locations.

Compensation. Our compensation policies recognize and reward individual and collective contributions to our growth and success. We offer, among other things, competitive and balanced compensation programs commensurate with those of our peers and competitors, including, but not limited to, well-rounded healthcare, prescription drug and disability insurance benefits for our employees and their families, a 401(k) plan for our U.S.-based employees and similar retirement savings programs for certain of our non-U.S.-based employees with a matching contribution by the Company and an employee stock purchase plan. We provide competitive paid time-off benefits, a parental leave program following the birth, adoption or fostering of a child and an employee assistance plan that provides professional support, access to special programs and certain resources to our employees experiencing personal-, work-, financial- or family-related issues.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm｜as_of：2025-11-14
<<<
A new product design effort may last over one year, and requires significant investment in engineering, as well as sales and marketing, which may take several years to recoup, if at all. Our failure to anticipate or timely develop new or enhanced products or technologies in response to technological shifts could result in decreased revenue and others obtaining design wins. As a result, our gross margin may decrease, we may not reach our expected level of production orders and we may lose market share, which could adversely affect our ability to sustain our revenue growth or maintain our current revenue levels.

11 We generally sell our products on the basis of purchase orders rather than long-term purchase commitments from our customers. Our customers can typically cancel purchase orders or defer product shipments for some period without incurring liability to us. We typically plan production and inventory levels based on internal forecasts of customer demand, which can be highly unpredictable and can fluctuate substantially, leading to excess inventory write-downs and resulting negative impacts on gross margin and net income. We have limited visibility into our customers’ inventories, future customer demand and the product mix that our customers will require, which could adversely affect our production forecasts and operating margins. The difficulty in predicting demand may be compounded when we sell to OEM customers indirectly through distributors or contract manufacturers, as our forecasts of demand are then based on estimates provided by multiple parties. If we overestimate our customers’ requirements, we may have excess inventory, which could lead to obsolete inventory, write-downs and unexpected costs. Conversely, if we underestimate our customers’ requirements or are not able to secure components, materials and/or fabrication facility capacity, we may have inadequate inventory, which could lead to foregone revenue opportunities, loss of potential market share and damage to customer relationships.…

The semiconductor industry is highly competitive. While we compete with a wide variety of companies, our significant competitors include, among others, ADI, Broadcom, Credo, Marvell, MaxLinear, Microchip, NXP, Qorvo, Semtech, Skyworks and Sumitomo as well as increased competition from Chinese companies.

We believe future competition could also come from companies developing new alternative technologies, component suppliers based in countries with lower production costs and IC manufacturers achieving higher levels of integration that exceed the functionality offered by our products. Our customers and suppliers could also develop products that compete with or replace our products. Increased competition has in the past and could in the future lead to lower prices for our products, reduced demand for our products and a corresponding reduction in our ability to recover development, engineering and manufacturing costs.

Many of our existing and potential competitors have entrenched market positions, historical affiliations with OEMs, considerable internal manufacturing capacity, established intellectual property rights, strong brand recognition and substantial technological capabilities. Many of them may also have greater financial, technical, manufacturing or marketing resources than we do. Consolidation among our competitors could negatively impact our competitive position and market share and harm our results of operations. In addition, certain countries such as China have begun implementing initiatives to build domestic semiconductor supply chains and we may be at a disadvantage in attempting to compete with entities associated with such foreign government efforts. Our failure to successfully compete could result in lower revenue, decreased profitability and a lower stock price.

We sell products in markets that are characterized by rapid technological changes, evolving industry standards, frequent new product introductions and increasing levels of integration. Our ability to keep pace with these markets at times depends on our ability to obtain technology from third parties on commercially reasonable terms to allow our products to remain competitive. If licenses to such technology are not available on commercially reasonable terms and conditions or at all and we cannot otherwise acquire or integrate such technology, our products or our customers’ products could become unmarketable or obsolete, we could lose market share and our revenue and results of operations could materially decline. In addition, disputes with third-party licensors over required payments, scope of licensed rights and compliance with contractual terms are common in our industry and we have in the past and may in the future be subjected to disputes over the terms of such licenses which could result in substantial unanticipated costs or delays in developing substitute technology to deliver competitive products, damaged customer and vendor relationships, indemnification liabilities and declining revenues and profitability. Such events could have an adverse effect on our financial condition and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
