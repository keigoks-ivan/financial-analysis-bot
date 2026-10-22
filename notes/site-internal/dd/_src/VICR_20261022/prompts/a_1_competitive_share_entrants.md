你是 stock-analyst v20 DD 的證據採集子 agent。標的：VICR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - VICR Vicor market share gaining OR losing 2026
  - Vicor new entrant OR displace threat 半導體 — 電源管理 / AI 加速器電源 2026
  - VICR competitor design win 2026
  - Vicor vs 半導體 — 電源管理 / AI 加速器電源 peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm｜as_of：2026-03-02
<<<
Our competition varies, depending on the market segment and application. Generally, we compete with developers and manufacturers of integrated circuits and semiconductor-based modules when addressing the needs of customers in enterprise computing and other market segments with implementations of our proprietary Factorized Power ArchitectureTM (“FPA”) using Advanced Products. In contrast, we generally compete with manufacturers of integrated power supplies when addressing the needs of customers, across a wide range of market segments, implementing conventional power systems architectures (e.g., Centralized Power Architecture (“CPA”), Distributed Power Architecture (“DPA”), and Intermediate Bus Architecture (“IBA”)) using Brick Products.

Our Strategy Our strategy emphasizes demonstrable product differentiation and a value proposition based on competitively superior solution performance, advantageous design flexibility, and a compelling total cost of ownership (“TCO”). Since the Company was founded, our competitive position has been maintained by continuous innovations in product design and achievements in product performance, largely enabled by our focus on the research and development of advanced technologies and processes, often implemented in proprietary semiconductor circuitry, materials, and packaging. Many of 3 Table of Contents our products incorporate patented or proprietary implementations of high-frequency switching topologies, which enable the design of power system solutions more efficient and much smaller than conventional alternatives. This efficiency and small size is enabled by our proprietary switching circuitry and magnetic structures, as well as our use of highly differentiated packaging.

Competition and Market Characteristics The competitive characteristics of the markets we serve with Advanced Products and Brick Products can differ significantly. For example, in the higher-performance segments of computing we serve, our Advanced Products most often compete with solutions offered by large integrated device manufacturers (“IDMs”), which offer integrated circuits (“ICs”) and semiconductor-based modules. These IDMs generally offer far broader product portfolios, possess far greater global manufacturing and support resources, and have the ability to aggressively price their products to defend market share. Accordingly, Advanced Products are positioned as highly differentiated alternatives to commodity solutions for customers seeking high levels of performance. The customers we serve with Advanced Products are in market segments generally characterized by an emphasis on product performance differentiation, a compelling TCO, relatively extended and highly competitive design cycles, and product life cycles of generally less than three years. In contrast, the Brick Products competitive landscape is relatively fragmented, with large-scale, low-cost global suppliers of commodity solutions and many smaller manufacturers focused on specialized products or narrowly defined market segments or geographies.…

The size and growth characteristics of the markets we serve with Advanced Products and Brick Products also can differ significantly, and the range and quality of market data is problematic, making summary statements about these markets challenging. We believe our Advanced Products generally compete with power modules and power ICs developed and manufactured by IDMs and other fabless vendors of power semiconductors. We believe our Brick Products generally compete with similarly integrated switching power supply products developed and manufactured by large global competitors and a fragmented group of small regional competitors. The switching power supply market can be segmented by product type (i.e., DC-DC converters, AC-DC converters, and DC-AC inverters), by output power levels, and by numerous vertical markets (i.e., industry-specific applications).

7 Table of Contents Despite our minor share in the overall merchant market and the competitive presence of numerous, far larger vendors in the market segments we serve with both Advanced Products and Brick Products, we believe we maintain an advantageous competitive position in those market segments based on our differentiated technology. However, there are numerous competitors across these market segments that have significantly greater engineering, financial, manufacturing, and marketing and sales resources, as well as longer operating histories and longer customer relationships than we do.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm｜as_of：2026-03-02
<<<
Competitive Risks We compete with many companies possessing far greater resources. Some of our competitors have far greater financial, manufacturing, technical, and sales and marketing resources than we possess or have access to. Our Brick Products compete with those products offered by domestic and foreign manufacturers of integrated power supplies and related power conversion components. With our Advanced Product lines, we compete with global IDMs and fabless developers of semiconductor-based power management modules and power management ICs. These competitors have far larger organizations and broader semiconductor-based product lines. Competition is generally based on product performance, design flexibility (i.e., ease of use), product price, and product availability, but with the relative importance of these factors varying among products, markets, and customers.

Existing or new competitors may develop products or technologies that more effectively address the demands of our customers and markets with enhanced performance, features and functionality, or lower cost. Larger competitors frequently seek to maintain market share and protect customer relationships through heavily-discounted pricing, which we may not be able to match. If we fail to develop and commercialize leading-edge technologies and products that are cost effective and 15 Table of Contents maintain high standards of quality, and introduce them to the market on a timely basis, our competitive position and results of operations could be materially adversely affected.

We operate in an industry in which the ability to compete depends on the development or acquisition of proprietary technologies that must be protected to preserve the exclusive use of such technologies. We devote substantial resources to establish and protect our patents and proprietary rights, and we rely on patent and intellectual property law to protect such rights. This protection, however, may not prevent competitors from independently developing products similar or superior to our products. We may be unable to protect or enforce current patents, may rely on unpatented technology that competitors could restrict or replicate, or may be unable to acquire patents in the future, all of which may have a material adverse effect on our competitive position. In addition, the intellectual property laws of foreign countries may not protect our rights to the 16 Table of Contents same extent as those of the United States. We have been defending and may need to continue to defend or challenge patents. We have incurred and expect to incur significant financial costs in the defense of our patented technologies and have devoted and expect to devote significant resources to these efforts which, if unsuccessful, may have a material adverse effect on our operating results and financial position.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
