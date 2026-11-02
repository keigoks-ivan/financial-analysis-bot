你是 stock-analyst v20 DD 的證據採集子 agent。標的：GLW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - GLW Corning market share gaining OR losing 2026
  - Corning new entrant OR displace threat Electronic Components 2026
  - GLW competitor design win 2026
  - Corning vs Electronic Components peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm｜as_of：2026-02-12
<<<
5 Table of Contents Competition We compete with many large and varied manufacturers, both domestic and foreign. Some of these competitors are larger than we are, and some have broader product lines. We strive to maintain and improve our market position through technology and product innovation. For the foreseeable future, our competitive advantage lies in our commitment to research and development, deep customer relationships, reliability of supply, product quality, superior customer service and technical specification of our products. There is no assurance that we will be able to maintain or improve our market position or competitive advantage.

Optical Communications Segment We maintain a leadership position in the segment’s principal product groups, which include carrier and enterprise networks. The competitive landscape includes industry consolidation, pricing pressure and competition for the innovation of new products. These competitive conditions are likely to persist. Our large-scale manufacturing experience, fiber process, technology leadership and intellectual property provide cost advantages relative to several of our competitors. Our principal competitors include Amphenol, Fujikura and their subsidiary America Fujikura Ltd., Sumitomo and Prysmian Group S.p.A.

Display Segment We are the largest worldwide producer of glass substrates for flat panel displays. The environment for high-performance display glass substrate products is very competitive and we have maintained our competitive advantages by investing in new products, continually improving our proprietary fusion manufacturing process and providing a consistent and reliable supply of high-quality products. Our process allows us to deliver glass that is larger, thinner and lighter, with exceptional surface quality and without heavy metals. Our principal competitors include AGC Inc. and Nippon Electric Glass Co., Ltd.

Specialty Materials Segment We have deep capabilities in materials science, optical design, shaping, coating, finishing, metrology and optical system assembly. Our products and capabilities in this segment position us to meet the needs of a broad array of markets, including semiconductor, aerospace, defense, industrial, commercial and telecommunications. Our principal competitors include Schott AG, AGC Inc., Nippon Electric Glass Co., Ltd., Heraeus and JENOPTIK Industrial Metrology Germany GmbH.

Automotive Segment We maintain a strong market position with our automotive products including automotive ceramic substrate and filter products, and technical glass solutions for global light-duty and heavy-duty vehicle markets. Our competitive advantage in automotive ceramic substrate products for catalytic converters and filter products for particulate emissions in exhaust systems is based on an advantaged product portfolio, collaborative engineering design services, customer service and support, strategic global presence and continued product innovation. In automotive glass, our competitive advantage is in more reliable, large and shaped digital display covers. Our principal competitors include NGK Insulators, Ltd., Ibiden Co., Ltd., AGC Inc. and LENS.

Life Sciences Segment We seek to maintain a competitive advantage by emphasizing product quality, global distribution, supply chain efficiency, a broad product line, technical support and superior product attributes. Our principal competitors include Thermo Fisher Scientific Inc., Avantor, Inc., Greiner AG, Eppendorf SE, Sarstedt AG & Co. KG and Danaher Corporation. Corning also faces competition from large distributors that have pursued backward integration or introduced private label products.

Each business segment possesses a patent portfolio that provides certain competitive advantages in protecting our innovations. We have historically enforced, and will continue to enforce, our intellectual property rights. At the end of 2025, we owned about 11,375 unexpired patents in various countries, of which about 4,015 were U.S. patents. Between 2026 and 2028, approximately 740, or 6.5%, of these worldwide patents will expire, while at the same time we intend to seek patents protecting our newer innovations. Worldwide, we have about 5,650 patent applications in process, with about 1,740 in process in the U.S. Our patent portfolio will continue to provide a competitive advantage in protecting our innovation, although our competitors in each of our businesses are actively seeking patent protection as well.

The following table presents the approximate number of patents granted to our reportable segments: Number of patents worldwide U.S. patents Important U.S. patents expiring between 2026 and 2028 Optical Communications 4,121 1,625 44 Display 1,430 191 12 Specialty Materials 2,245 845 12 Automotive 1,351 506 12 Life Sciences 1,091 315 6 Many of our patents are used in operations or are licensed for use by others, and we are licensed to use patents owned by others. We have entered into cross-licensing arrangements with some major competitors, but the scope of such licenses has been limited to specific product areas or technologies.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm｜as_of：2026-02-12
<<<
Corning’s Optical Communications and Display segments generate a significant amount of the Company’s profits and cash flow; any significant decrease in pricing, volume or market share could have a material and negative impact on our financial results Corning’s ability to generate profits and operating cash flow could be significantly impacted by the profitability of these businesses, which are subject to pricing pressure, industry competition, potential over-capacity or under capacity, development of new technologies and operational and regulatory risks. Further, the optical communications business faces risks related to fluctuations in telecommunication and hyperscale data center capital spending, which may negatively affect the demand for our products and have a material adverse impact on our financial results. Additionally, the display glass business is exposed to exchange rate movements. If we are not able to achieve proportionate reductions in costs and/or increases in volume or price to offset the aforementioned factors, it could have a material adverse impact on our financial results.

We may experience difficulties in enforcing our intellectual property rights, which could result in loss of market share and decreased sales and profits, and we may be subject to claims of infringement of the intellectual property rights of others We rely on patent and trade secret laws, copyright, trademark, confidentiality procedures, controls and contractual commitments to protect our intellectual property rights. Despite our efforts, these protections may be limited and we may encounter difficulties in protecting our intellectual property rights or obtaining rights to additional intellectual property necessary to permit us to continue or expand our businesses. We cannot provide assurance that the patents we hold or may obtain will provide meaningful protection against our competitors. Changes in or enforcement of laws concerning intellectual property may affect our ability to prevent or address the misappropriation of, or the unauthorized use of, our intellectual property, potentially resulting in loss of market share. Litigation may be necessary to enforce our intellectual property rights. Litigation is inherently uncertain and outcomes are unpredictable. If we cannot protect our intellectual property rights against unauthorized copying or use, or other misappropriation, we may not remain competitive.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLW_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
