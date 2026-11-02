你是 stock-analyst v20 DD 的證據採集子 agent。標的：VRT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - VRT Vertiv Holdings Co market share gaining OR losing 2026
  - Vertiv Holdings Co new entrant OR displace threat Electrical Equipment & Parts 2026
  - VRT competitor design win 2026
  - Vertiv Holdings Co vs Electrical Equipment & Parts peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm｜as_of：2026-02-13
<<<
Competition The majority of our competitors target a specific offering or a specific geographic location. Competition in our markets is primarily on the basis of reliability, quality, price, service and customer relationships. Across our three geographic segments, we encounter two principal types of competitors: niche players (e.g., Delta Electronics, Inc., Stulz GmbH, Johnson Controls International PLC, and Socomec Holding SA) and large-scale global competitors (e.g., Schneider Electric, S.E., Eaton Corporation Plc, Legrand SA, and Huawei Investment & Holding Co., Ltd.) We believe we differentiate ourselves through: (i) application expertise and customer collaboration to envision and build future-ready infrastructure; (ii) most complete portfolio and continual innovation; (iii) proven superior reliability and quality; (iv) truly global presence and ability to scale for our customers' operating flexibility and resilience; and (v) our industry-leading global service network to safeguard uptime and support.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm｜as_of：2026-02-13
<<<
The industries and markets in which we operate are highly competitive, and we experience competitive pressures from numerous and varied competitors.

We encounter competition from numerous and varied competitors targeting all areas of our business on a global and regional basis. We compete primarily on the basis of our technology, reliability, quality, price, service and customer relationships. A significant element of our competitive strategy is focused on delivering reliable, high-quality products and solutions at the best relative global cost. If our products, services, and cost structure do not enable us to compete successfully, we may experience a decline in product sales and a corresponding loss of customers.

Our competitors, any of which could introduce new technologies or business models that disrupt significant portions of our markets and cause our customers to move a material portion of their business away from us, primarily include: 16 Table of contents •Large-scale, global competitors with broad product portfolios and service offerings. These competitors may have comparatively greater financial, technical and marketing resources available to them and would include Schneider Electric, S.E., Eaton Corporation Plc, Legrand SA, and Huawei Investment & Holding Co., Ltd, each of which has a large, global presence and compete directly in the markets in which we operate. If we do not successfully anticipate technological shifts, market needs and opportunities, we may not be able to compete effectively and our ability to generate revenues will suffer. Industry consolidation may also impact the competitive landscape by creating larger, more homogeneous and potentially stronger competitors in the markets in which we operate.

•Offering-specific competitors with products and services that compete globally but with a limited set of product offerings, which would include Delta Electronics, Inc., Stulz GmbH, Johnson Controls International PLC, and Socomec Holding SA. These competitors may be able to focus more closely on a particular product or service segment of the market and apply targeted financial, technical and marketing resources in ways that we do not, potentially leading to stronger brand recognition, technological advancement and more competitive pricing within that targeted segment.

•Regional or country-level competitors. These are competitors that compete with us in a limited geographic area.

•Increasing Demand - As the demand for our products increases, or if we experience unexpected large orders, we will need to increase production and obtain sufficient supply of materials. If we fail to meet this increased customer demand in a timely manner, or at all, of if we fail to obtain the necessary raw materials or otherwise satisfy the performance obligations in our contracts related to these orders, we could be subject to penalty provisions, liquidated damages or other claims. Additionally, our reputation and customer relationships could be damaged and we could lose revenue and market share.

Serving a global customer base requires that we place more materials, production and service assets in emerging markets to capitalize on market opportunities and maintain our cost position. Emerging geographic markets may be relatively less profitable due to the investments needed to enter such markets and local pricing pressures, and we may have difficulty establishing and maintaining the operating infrastructure necessary to support the high growth rates associated with some of those markets. Manufacturers in countries that have lower production costs, such as China and 21 Table of contents India, may become competitors in key emerging markets and could offer their products in established markets. These actions may have a negative effect on our pricing, market share and operating results in these markets. In addition, foreign governments may decide to implement tax and other policies that favor their domestic manufacturers at the expense of international manufacturers. Similarly, the potential imposition of retaliatory tariffs or additional tariffs or modifications of free-trade agreements by the U.S. on other countries or regions, could increase our cost of doing business internationally, perhaps significantly, and may lead to further challenges for us in the various foreign markets in which we operate.

In order to successfully operate as a public company and implement our business plans, we must identify, attract, develop, motivate, train and retain key employees, including qualified executives, management, engineering, sales, marketing, IT support and service personnel. The market for such individuals may be highly competitive. We may not be successful in attracting, integrating or retaining qualified personnel to meet our current growth plans or future needs. Our productivity may be adversely affected if we do not integrate and train our new employees quickly and effectively. Attracting and retaining key employees in a competitive marketplace requires us to provide a competitive compensation package, which often includes cash- and equity-based compensation. If our total compensation package is not viewed as competitive, our ability to attract, motivate and retain key employees could be weakened and failure to successfully hire or retain key employees and executives could adversely impact us.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VRT_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
