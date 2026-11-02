你是 stock-analyst v20 DD 的證據採集子 agent。標的：KLAC。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - KLAC KLA market share gaining OR losing 2026
  - KLA new entrant OR displace threat Semiconductor Equipment & Materials 2026
  - KLAC competitor design win 2026
  - KLA vs Semiconductor Equipment & Materials peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
The strength of our competitive positions in many of our existing markets is primarily due to our leading technology, which is the result of our continuing significant investments in product R&D. Even during down cycles in the semiconductor industry, we have remained committed to significant engineering efforts toward both product improvement and new product development to enhance our competitive position.

Customers We count among our largest customers the leading semiconductor, semiconductor-related and electronic device manufacturers in Asia, the U.S. and Europe. Our future performance depends, in part, on our ability to continue to compete successfully in Asia, one of the largest markets for our equipment. Our business depends on capital expenditures from these manufacturers which, in turn, depend on many factors including general economic conditions, anticipated market demand, evolving government regulations and capacity constraints. Our ability to compete in this region depends on the continuation of favorable trading relationships between countries in the region and the U.S., and our continuing ability to maintain satisfactory relationships with leading semiconductor companies in the region.

Competition The worldwide market for technologically advanced process control, process-enabling and yield management solutions used by semiconductor and electronics manufacturers is highly competitive, with important competitive factors including system performance, ease of use, reliability, technical service and support, and overall cost of ownership. However, we believe that, while these competitive factors are important, our customers’ overriding requirement is for systems that effectively incorporate automated capabilities into their existing development and manufacturing processes to enhance productivity, improve yields and reduce waste. To remain competitive, we use significant financial resources to offer a broad range of products, maintain customer service and support centers worldwide, and invest significantly in product R&D. In each of our product markets, we have many competitors, including companies such as Applied Materials, Inc., ASML Holding N.V., Hitachi High-Tech Corporation, Lasertec, Inc. and Onto Innovation, Inc., some of which may have greater financial, research, engineering, manufacturing and marketing resources than we have. We expect our competitors to continue to improve the design and performance of their current products and to introduce new products with improved pricing and performance characteristics. We may also face future competition from new market entrants overseas or domestically.…

No assurance can be given that patents will be issued on any of our applications, that license assignments will be made as anticipated, or that our patents, licenses or other proprietary rights will be sufficiently broad to protect our technology. No assurance can be given that any patents issued to or licensed by us will not be challenged, invalidated or circumvented or that the rights granted thereunder will provide us with a competitive advantage. In addition, there can be no assurance that we will be able to protect our technology or that competitors will not be able to independently develop similar or functionally competitive technology.

Human Capital Management KLA’s performance and long-term success depend on the skills, experience and engagement of its workforce. We view our employees and the technology they develop as a key competitive advantage. Our human capital strategy focuses on anticipating workforce needs and attracting, developing, and retaining talent aligned to our core values. In response to competitive labor markets, we take a proactive and inclusive approach to talent development, retention and employee wellbeing. Our programs are designed to support professional growth, workforce capability building, and employee engagement while maintaining a safe, secure, and healthy workforce.

Compensation and Benefits KLA seeks to provide competitive and equitable compensation and benefits that support employee engagement and retention across its global workforce. We conduct annual compensation reviews to assess market competitiveness and internal alignment, and a significant portion of employee compensation is linked to company and business unit performance. Eligible employees may participate in long-term incentive programs, including restricted stock units (“RSUs”) and an Employee Stock Purchase Plan (“ESPP”), as well as incentive bonus or profit-sharing programs.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
These rules and regulations may significantly harm our business unless we are able to obtain required licenses. We will continue to apply for export licenses, when required, in an effort to avoid disruption to our and our customers’ operations, but there can be no assurance that export licenses applied for by either us or our customers, now or in the future, will be granted. To the extent Commerce does issue licenses to us or to our customers, such licenses may have a short duration or require us to satisfy various conditions. If pending and future export license applications are not granted, or additional restrictions are imposed, or if regulators adopt new interpretations of existing regulations, the potential impact on us could be material by disrupting our supply chain and product shipment, impairing our ability to complete product development in a timely manner, or our ability to support existing customers of covered products or supply customers of covered products outside the impacted regions, and requiring us to transition certain operations out of one or more of the identified countries.…

Our employees are vital to our success, and our key management, engineering and other employees are difficult to replace. We generally do not have employment contracts with our key employees. Further, we do not maintain key person life insurance for any of our employees. The expansion of high technology companies worldwide and the elevated demand for talent from the growth in demand for semiconductors in recent years has increased competition for qualified personnel. Competition for engineering and other technical personnel in many areas of the world in which we operate is especially intense due to the proliferation of technology companies worldwide. Our competitors have targeted individuals in our organization who have desired skills and experience. In addition, current or future immigration laws, policies or regulations may limit our ability to attract, hire and retain qualified personnel. If we are unable to attract, onboard and retain key personnel, or if we are not able to attract, assimilate, onboard and retain additional highly qualified employees to meet our current and future needs, our business and operations could be harmed.

Success in the industries in which we serve, including the semiconductor and PCB industries depends, in part, on the continual improvement of existing technologies and rapid innovation of new solutions. The primary driver of technology advancement in the semiconductor industry has been to shrink the lithography that prints the circuit design on semiconductor chips. To the extent that driver slows, semiconductor manufacturers may delay investments in equipment, investigate more complex device architectures, use new materials and develop innovative fabrication processes. These and other evolving customer plans and needs require us to respond with continued development programs and cut back or discontinue older programs, which may no longer have industry-wide support. Technical innovations are inherently complex and require long development cycles and appropriate staffing of highly qualified employees. Our competitive advantage and future business success depend on our ability to accurately predict evolving industry standards, develop and introduce new products and solutions that successfully address changing customer needs, win market acceptance of these new products and solutions, and manufacture these new products in a timely and cost-effective manner.…

Our industry includes large manufacturers with substantial resources to support customers worldwide. Some of our competitors are diversified companies with greater financial resources and more extensive research, engineering, manufacturing, marketing, and customer service and support capabilities than we possess. We face competition from companies whose strategy is to provide a broad array of products and services, some of which compete with the products and services we offer. These competitors may bundle their products in a manner that may discourage customers from purchasing our products, including pricing such competitive tools significantly below our product offerings. In addition, we face competition from smaller emerging companies whose strategy is to provide a portion of the products and services that we offer, using innovative technology to sell products into specialized markets. The strength of our competitive positions in many of our existing markets is largely due to our leading technology, which is the result of continuing significant investments in product R&D. However, we may enter new markets, whether through acquisitions or new internal product development, in which competition is based primarily on product pricing, not technological superiority. Further, some new growth markets that emerge may not require leading technologies.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
