你是 stock-analyst v20 DD 的證據採集子 agent。標的：ON。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - ON ON Semiconductor market share gaining OR losing 2026
  - ON Semiconductor new entrant OR displace threat Semiconductors 2026
  - ON competitor design win 2026
  - ON Semiconductor vs Semiconductors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm｜as_of：2026-02-09
<<<
Automotive Industrial Other 2025 Revenue (%) 51% 28% 21% Sample applications EV Energy generation, storage, & EV charging infrastructure AI data center ADAS and advanced safety Industrial automation 5G base stations Power management Aerospace, defense, & security Gaming, home entertainment systems, & set top boxes Powertrain Machine vision Routers In-Vehicle networking Smart cities & buildings Notebooks, laptops, desktop PCs & tablets Body & interior Hearing health, diagnostic, therapy, & monitoring White goods Lighting Power solutions Power supplies Sensors Motor control Smart phones Engine control Robotics and humanoids Competition We face significant competition from major international semiconductor companies, as well as smaller companies focused on specific market niches. Because some of our components include functionality that in some cases may be integrated into more complex ICs, we also face competition from manufacturers of ICs, ASICs and fully-customized ICs, as well as customers who develop their own IC products. See "Risk Factors — Trends, Risks and Uncertainties Related to Our Business" included elsewhere in this Form 10-K for additional information.

Some of our competitors have greater financial and other resources to pursue development, engineering, manufacturing, marketing and distribution of their products and may generally be better situated to withstand adverse economic or market conditions. The semiconductor industry has experienced, and may continue to experience, significant consolidation among companies and vertical integration among customers. The following discusses the effects of competition on our three operating segments: PSG Our competitive strengths include core competencies such as leading-edge fabrication technologies, micro and module packaging expertise, breadth of product line and IP portfolio, high-quality, cost-effective manufacturing and supply chain management. Our commitment to continuous innovation allows us to provide a broad range of semiconductor solutions to our customers who differentiate in power density and power efficiency, the key performance characteristics driving our markets.

New products and package innovation that enable enhanced performance over existing portfolios drive competition. A central focus of our portfolio is intelligent power technology based on silicon, silicon carbide, and GaN. These wide bandgap technologies are designed and manufactured by onsemi and supplied to customers in multiple forms, including bare die, packaged discrete products, and complete power modules. In addition to our power technologies, we believe our integrated circuit, signal, and protection technologies have significant performance advantages over our competition. PSG’s primary competitors include: Infineon Technologies AG ("Infineon"), STMicroelectronics N.V. ("STMicroelectronics"), Wolfspeed Inc., ROHM Semiconductor and Nexperia BV.

AMG AMG principally competes on design experience, manufacturing capability, depth and quality of IP, ability to service customer needs from the design phase to the shipping of a completed product, length of design cycle, longevity of technology support and 10 Table of Contents experience of sales and technical support personnel. Our competitive position with respect to the above is enhanced by long-standing relationships with leading customers.

Our ability to compete successfully depends on internal and external variables. These variables include, but are not limited to, the timeliness with which we can develop new products and technologies, product performance and quality, manufacturing yields and availability of supply, customer service, pricing, industry trends and general economic trends. Competitors for certain of AMG's products and solutions include: Texas Instruments Incorporated, Analog Devices, Inc., Infineon, STMicroelectronics, Renesas Electronics Corporation, Monolithic Power Systems Inc. and NXP Semiconductors N.V.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm｜as_of：2026-02-09
<<<
The semiconductor industry requires substantial investment in research and development in order to develop and bring to market enhanced technologies and products. The development of new products is complex and time-consuming, often requiring significant capital investment and lead time for development and testing. We cannot assure you that we will have sufficient resources to maintain the level of investment in research and development required to remain competitive. In addition, the lengthy development cycle for certain of our products could limit our ability to adapt quickly to changes affecting the product markets and requirements of our customers and end-users, and we may be unable to develop innovative responses to our customers’ and end-users’ evolving needs on the timelines they require or at all. There can be no assurance that we will win competitive bid selection processes, known as "design wins," for new products. In addition, design wins do not guarantee that we will make customer sales or generate sufficient revenue to recover design and development investments, realize a return on the capital expended or achieve expected gross margins, as expenditures for technology and product development are generally 18 made before the commercial viability for such developments can be assured.…

Our ability to compete successfully in the highly competitive semiconductor industry depends on elements both within and outside of our control. We face significant competition within each of our product lines from major global semiconductor companies as well as smaller companies focused on specific market niches. In addition, companies not currently in direct competition with us may introduce competing products in the future.

If we are unable to compete effectively, our competitive position could be weakened relative to our peers, which would have a material adverse effect on our business and results of operations. Our future success depends on many factors, including the development of new technologies and effective commercialization and customer acceptance of our products, and our ability to increase our position in current markets, expand into adjacent and new markets, and optimize operational performance. Products or technologies developed by competitors may render our products or technologies obsolete or noncompetitive. We also may be unable to market and sell our products if they are not competitive on the basis of price, quality, technical performance, features, system compatibility, ease of use, customized design, innovation, availability, delivery timing and reliability. If we fail to compete effectively on developing strategic relationships with customers and customer sales and technical support, our sales and revenue may be materially adversely affected. Competitive pressures may limit our ability to raise prices, and any inability to maintain revenue or raise prices to offset increases in costs could have a significant adverse effect on our gross margin. Our gross margins may fluctuate across time periods and operating segments and could experience volatility or downward pressure due to a variety of factors.…

The semiconductor industry has experienced, and may continue to experience, significant consolidation among companies and vertical integration among customers. Larger competitors resulting from consolidations may have certain advantages over us, and we may be at a competitive disadvantage if we fail to identify attractive opportunities to acquire companies to expand our business. Consolidation among competitors and integration among customers could erode our market share, impair our capacity to compete and require us to restructure our operations, any of which could have a material adverse effect on our business.

In addition, some of our competitors may receive governmental subsidies or other incentives that give them a competitive advantage over us. For example, the United States and the European Union have enacted legislation to provide funding and incentives for semiconductor research, development, and manufacturing in their respective regions. If we are unable to access such funding or incentives, or if any awards or incentives we do receive are reduced, terminated or clawed back, or if our competitors receive more funding or incentives than we do, we may be at a disadvantage in developing and producing new or improved products or technologies, which could adversely affect our market share, revenue and profitability.

Our power technologies designed for AI use may not capture market share as expected, and issues related to the responsible use of AI may adversely affect our business.

Our extensive range of power technologies are used to help power AI data centers and we expect this part of our business to grow. The emergence of big data and new tools such as machine learning and AI that capitalize on the availability of large data sets is leading semiconductor manufacturers to pursue new products and approaches, and there is intense competition to capture a share of this emerging market. We may not be able to develop and offer the technology solutions that our AI-focused customers demand in a timely manner or effectively, which could have a materially adverse effect on our business. Our failure to commercialize new technologies that can power AI data centers in a timely manner or at all could result in a loss of market share, unanticipated costs and inventory obsolescence, which could adversely affect our financial results. In addition, if AI-related technologies fail to achieve the effectiveness or adoption levels currently anticipated, including due to insufficient available power or other utilities, or if our customers delay or scale back their AI deployments, demand for our AI-related products and solutions and returns on associated investments could be materially lower than we currently expect.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
