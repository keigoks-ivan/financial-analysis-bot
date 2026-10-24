你是 stock-analyst v20 DD 的證據採集子 agent。標的：LRCX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - LRCX Lam Research market share gaining OR losing 2026
  - Lam Research new entrant OR displace threat Semiconductor Equipment & Materials 2026
  - LRCX competitor design win 2026
  - Lam Research vs Semiconductor Equipment & Materials peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-07）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm｜as_of：2026-08-07
<<<
Competition The semiconductor capital equipment industry is characterized by rapid change and is highly competitive throughout the world. To compete effectively, we invest significant financial resources targeted to strengthen and enhance our product and services portfolio and to maintain customer service and support locations globally. Semiconductor manufacturers evaluate capital equipment suppliers in many areas, including but not limited to process performance, productivity, defect control, customer support, and overall cost of ownership, which can be affected by many factors such as equipment design, reliability, software advancements, and similar factors. Our ability to succeed in the marketplace depends upon our ability to manufacture and ship products on a timeline that meets our customers’ needs, maintain existing products, and introduce product enhancements and new products that meet customer requirements on a timely basis. In addition, semiconductor manufacturers must make a substantial investment to qualify and integrate new capital equipment into semiconductor production lines. As a result, once a semiconductor manufacturer has selected a particular supplier’s equipment and qualified it for production, the manufacturer generally maintains that selection for that specific production application and technology node as long as the supplier’s products demonstrate performance to specification in the installed base. Accordingly, we may experience difficulty in selling to a given customer if that customer has qualified a competitor’s equipment.…

We face significant competition with all of our products and services. Our primary competitor in the dielectric and metals deposition market is Applied Materials, Inc. For ALD and PECVD, we also compete against ASM International and Wonik IPS. In the etch market, our primary competitors are Applied Materials, Inc.; Hitachi, Ltd.; and Tokyo Electron, Ltd., and our primary competitors in the wet clean market are Screen Holding Co., Ltd.; Semes Co., Ltd.; and Tokyo Electron, Ltd.

We face competition from a number of established and emerging equipment companies in the industry. We expect our competitors to continue to improve the design and performance of their current products and processes, to introduce new products and processes with enhanced price/performance characteristics, and to provide more comprehensive offerings of products. If our competitors make acquisitions or enter into strategic relationships with leading semiconductor manufacturers, or other entities, covering products similar to those we sell, our ability to sell our products to those customers could be adversely affected. Government and other initiatives to encourage local semiconductor manufacturing and supply chain in countries outside of the U.S., including China, could increase competition from domestic equipment and spare parts manufacturers in those countries. Additionally, the U.S. Government has enacted a number of export controls regulating the sales of certain technologies to customers in China, including entity listings of multiple customers, thus restricting the sales of equipment and spare parts by U.S. equipment suppliers. This provides an advantage to our international competitors that are not subject to these restrictions. There can be no assurance that we will continue to compete successfully in the future.

Patents and Licenses Our policy is to seek patents on inventions relating to new or enhanced products and processes developed as part of our ongoing research, engineering, manufacturing, and support activities. We currently hold a number of U.S. and foreign patents and applications covering various aspects of our products and processes. Our patents, which cover innovative and valuable aspects of our past and present core products, have current durations ranging from approximately one to twenty years. We believe that, although the patents we own and may obtain in the future will be of value, they alone will not determine our success. Our success depends principally upon our research and development, engineering, marketing, support, and delivery skills. However, in the absence of patent protection, we may be vulnerable to competitors who attempt to imitate our products, manufacturing techniques, and processes and may be more limited in our ability to exclude competitors than would otherwise be the case. In addition, other companies and inventors may receive patents that contain claims applicable to our products and processes. The sale of products covered by patents of others could require licenses that may not be available on terms acceptable to us, or at all. For further discussion of legal matters, see Item 3, “Legal Proceedings,” of this report.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-07）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm｜as_of：2026-08-07
<<<
Lam Research Corporation 2026 10-K 13 Table of Contents INDUSTRY AND CUSTOMER RISKS We Depend on Creating New Products and Processes and Enhancing Existing Products and Processes for Our Success; Consequently, We Are Subject to Risks Associated with Rapid Technological Change Rapid technological changes in semiconductor manufacturing processes subject us to increased pressure to develop technological advances that enable those processes. We believe that our future success depends in part upon our ability to develop and offer new products with improved capabilities and to continue to enhance our existing products. If new products or existing products have reliability, quality, design, or safety problems, our performance may be impacted by reduced orders, higher manufacturing costs, delays in acceptance of and payment for new products, additional service and warranty expenses, and loss of market share. If we are unable to develop and manufacture products successfully, or the products that we introduce fail in the marketplace, our business, results of operations and financial condition could be materially and adversely affected. For more than 25 years, the primary driver of technology advancement in the semiconductor industry has been to shrink the lithography that prints the circuit design on semiconductor chips.…

In order to develop new products and processes and enhance existing products and processes, we expect to continue to make significant investments in R&D, to investigate the acquisition of products and technologies, to invest in or acquire businesses or technologies, and to pursue joint development relationships with customers, suppliers, or other members of the industry. Our investments and acquisitions may not be as successful as we may expect, particularly in the event that we invest in or acquire product lines and technologies that are new to us. We may find that acquisitions are not available to us, for regulatory or other reasons, and that we must therefore limit ourselves to collaboration and joint venture development activities that do not have the same benefits as acquisitions. Pursuing development through collaboration and/or joint development activities rather than through an acquisition may pose substantial challenges for management, including those related to aligning business objectives; sharing confidential information, intellectual property and data; sharing value with third parties; and realizing synergies that might have been available in an acquisition but are not available through a joint development project.…

We regularly assess our strategic resource allocation choices in response to the changing business environment. If we do not adequately adapt to the changing business environment, we may lack the infrastructure and resources to scale up our business to meet customer expectations and compete successfully during a period of growth, which could have a material adverse effect on our business, reputation, results of operations, financial condition, and/or our market share, or we may expand our capacity and resources too rapidly and/or beyond what is appropriate for the actual demand environment, which could result in excess fixed costs and have a material adverse effect on our results of operations and financial condition. For example, the growth of AI technologies and related infrastructure has been and is expected to continue to be a significant driver of capital equipment expenditures by semiconductor manufacturers across both the memory and non-memory market segments and requires us to respond (sometimes rapidly) to changes in demand for our products and services, including by expanding our equipment manufacturing capabilities and hiring additional personnel. If we are unable to effectively scale our business to meet our customers’ requirements in response to AI-driven demand, we may lose market share, and our business, reputation, results of operations, and financial condition could be harmed.

Similarly, our customers may partner with, or follow the lead of, educational or research institutions that establish processes for accomplishing various tasks or manufacturing steps. If those institutions utilize a competitor’s equipment when they establish those processes, it is likely that customers will tend to use the same equipment in setting up their own manufacturing lines. Even if they select our equipment, the institutions and the customers that follow their lead could impose conditions on acceptance of that Lam Research Corporation 2026 10-K 16 Table of Contents equipment, such as adherence to standards and requirements or limitations on how we license our proprietary rights, that increase our costs or require us to take on greater risk. These actions could adversely impact our market share, results of operations, and financial condition.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
