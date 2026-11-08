你是 stock-analyst v20 DD 的證據採集子 agent。標的：ALAB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - ALAB Astera Labs market share gaining OR losing 2026
  - Astera Labs new entrant OR displace threat Semiconductors 2026
  - ALAB competitor design win 2026
  - Astera Labs vs Semiconductors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm｜as_of：2026-02-20
<<<
Competition We offer a differentiated and holistic Intelligent Connectivity Platform purpose-built for cloud and AI infrastructure workloads. Our competitors typically compete with us with respect to some, but not all, of our solutions. Our principal competitors include Broadcom, Inc., Credo Technology Group Holding Ltd., Marvell Technology, Inc., Microchip Technology Inc., Montage Technology, Parade Technologies, Ltd., and Rambus, Inc.

Government Regulation We are subject to the laws and regulations of various jurisdictions and governmental agencies affecting our operations and the sale of our products in areas including, but not limited to: intellectual property; tax; import and export requirements; anti-corruption; economic and trade sanctions; national security and foreign investment; foreign exchange controls and cash repatriation restrictions; data privacy and security requirements (such as the California Consumer Privacy Act of 2018 (the “CCPA”) and the European Union General Data Protection Regulation with respect to the European Economic Area, and the United Kingdom (“UK”) General Data Protection Regulation, with respect to the UK, (collectively, the “GDPR”)); competition; advertising; employment; product regulations; environment, health and safety 4 Table of Contents requirements; and consumer laws. To date, costs and accruals incurred to comply with these governmental regulations have not been material to our capital expenditures and results of operations. Although there is no assurance that existing or future governmental laws and regulations applicable to our operations and the sale of our products will not have a material adverse effect on our capital expenditures, results of operations, and competitive position, we do not currently anticipate material expenditures for government regulations. Nonetheless, we believe that significant changes in global trade regulations could potentially have a material impact on our business.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm｜as_of：2026-02-20
<<<
To compete successfully, we must design, develop, market, and sell new products or new generations of existing products that provide increasingly higher levels of performance while meeting evolving industry standards, and the cost and quality expectations, of our customers. The introduction of new products by our competitors, the delay or cancellation of a system for which any of our products are designed in, the market acceptance of products based on new or alternative technologies, or the emergence of new industry standards could render our existing or future products uncompetitive, obsolete, or otherwise unmarketable.

Products for our target markets are based on industry standards that are continually evolving, and industry standards are often developed and promoted by larger companies who are industry leaders and provide other components of the systems into which our products are incorporated. In choosing products to develop, we also make certain assumptions about which industry standards we believe will be adopted by industry leaders. For example, CXL connectivity solutions and UALinkTM are in the early stages of market adoption. If our assumptions are incorrect, and larger companies do not support the same industry standards that we do, or if competing standards emerge, it could be difficult for our products to meet the requirements of certain customers. As a result, if we fail to introduce new products or new generations of our existing products that meet prevailing industry standards and the needs of our customers, or penetrate new markets in a timely fashion, and our designs do not gain acceptance, we will likely lose market share and our competitive position, potentially on an extended basis, and our operating results will be adversely affected.

Our competitiveness and future success depend on our and our third-party manufacturing partners’ ability, as applicable, to design, develop, manufacture, assemble, and test new products and product enhancements on a timely and cost-effective basis. Our failure to anticipate fundamental shifts in technologies in any of our product markets, to develop new technologies or to react to changes in existing technologies could materially delay our development of new products or new generations of our existing products. For example, we anticipate that our customers will continue to have increasing needs for connectivity and memory products as a result of the increased adoption of the cloud and AI infrastructure, and if we are unable to successfully design and produce products that our customers can incorporate into their cloud and AI systems, we expect that our competitive positioning and financial performance would be harmed as our competitors more effectively help our customers scale into these developing sectors.

The industry in which we compete is characterized by rapid technological change, changes in customer requirements, frequent new product introductions and enhancements, short product cycles and evolving industry standards, and new delivery methods. In addition, the fabrication of semiconductor products has transitioned over time to increasingly smaller line width geometries, and failure to successfully transition to product designs utilizing smaller geometry process nodes could impair our competitive position. In order to remain competitive, we have made, and expect to continue to make, significant investments in research and development and often well ahead of the anticipated product revenue. For the years ended December 31, 2025 and 2024, research and developments expenses were $304.0 million and $200.8 million, respectively. If we fail to develop new and enhanced products and technologies, if we focus on technologies that do not become widely adopted, or if new competitive technologies or industry standards that we do not support become widely accepted, demand for our products may be reduced. Increased investments in research and development or unsuccessful research and development efforts could cause our cost structure to fall out of alignment with demand for our products, which would have a negative impact on our financial results.

Our operating results may be impacted by a decline in the pricing for the current generation of our existing products. If competition increases in our target markets, we may need to reduce the prices of our existing products in anticipation of competitive pricing pressures, new product introductions by us or our competitors, new generations of such existing products, or for other reasons. If we are unable to offset any reductions in pricing for existing products by increasing our sales volumes or introducing new products or new product generations of such existing products with higher margins, our revenue and gross margins will suffer. To maintain our revenue and gross margins, we must develop and introduce new products, next-generation products, and product enhancements on a timely basis and continually reduce our costs as well as our customers’ costs. Failure to do so may cause our revenue and gross margins to decline.

The semiconductor industry is extremely competitive. We currently compete with a number of large domestic and international companies, some of which have greater financial, technical, and management resources than us. For example, we are facing, and expect we will continue to face, significant competition in the cloud data center infrastructure market. Our competitors typically compete with us with respect to some, but not all, of our solutions. Our principal competitors include Broadcom, Inc., Credo Technology Group Holding Ltd., Marvell Technology, Inc., Microchip Technology Inc., 26 Table of Contents Montage Technology, Parade Technologies, Ltd., and Rambus Inc,. Our efforts to introduce new products into markets with entrenched competitors will expose us to additional competitive pressures. In addition, many of our competitors have longer operating histories, greater name recognition, larger customer bases, and greater sales, marketing, and distribution resources than we do and some operate and maintain their own fabrication facilities.

Additionally, customer expectations and requirements have been evolving rapidly. As a result, some of our competitors may be better situated to meet changing customer needs and secure design wins. Increasing competition in the markets in which we operate may negatively impact our revenue and gross margins. For example, competitors with greater financial resources may be able to offer lower prices than us, or they may offer additional products, services or other incentives that we may be unable to match.

We also may experience discriminatory or anti-competitive practices by our competitors that could impede our growth, cause us to incur additional expense or otherwise negatively affect our business. In addition, some of these competitors may use their market power to dissuade our customers from purchasing from us. The semiconductor industry has experienced significant consolidation in recent years, which has resulted in several of our competitors becoming much larger in terms of revenue, product offerings, and scale. Our competitors may also establish cooperative relationships among themselves or with third parties or may acquire companies that provide similar products to ours. We expect this trend to continue as companies attempt to improve the leverage of growing research and development costs, strengthen or hold their market positions in an evolving industry, or are unable to continue operations. Companies that are strategic partners in some areas of our business may acquire or form alliances with our competitors, thereby reducing their business with us. We believe that industry consolidation may result in stronger competitors that are better able to compete as sole-source vendors for customers. This could lead to more variability in our operating results.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
