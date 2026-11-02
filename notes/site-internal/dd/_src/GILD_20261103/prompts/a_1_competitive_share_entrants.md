你是 stock-analyst v20 DD 的證據採集子 agent。標的：GILD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - GILD Gilead Sciences market share gaining OR losing 2026
  - Gilead Sciences new entrant OR displace threat Biotech / Specialty Pharma 2026
  - GILD competitor design win 2026
  - Gilead Sciences vs Biotech / Specialty Pharma peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm｜as_of：2026-02-24
<<<
4 Competition We operate in a highly competitive environment. Our products compete with other commercially available products based primarily on efficacy, safety, tolerability, acceptance by doctors, ease of patient compliance, ease of use, price, insurance and other reimbursement coverage, distribution and marketing. We also face significant competition from: (i) large pharmaceutical and biotechnology companies and specialized pharmaceutical firms acting either independently or together with other such companies to pursue the development of products and technologies that may be competitive with our existing products or research programs; (ii) academic institutions, government agencies and other public and private organizations conducting research who may seek patent protection or may establish collaborative arrangements for competitive products or programs; (iii) pricing pressures from private insurers and government payers as our products mature, which often result in a reduction of our net product prices; and (iv) new branded or generic products introduced into major markets, which may impact our ability to maintain pricing and market share.

Patents Patents and other proprietary rights are very important to our business. If we have a properly drafted and enforceable patent, it can be more difficult for our competitors to use our technology to create competitive products and more difficult for our competitors to obtain a patent that prevents us from using technology we create. As part of our business strategy, we actively seek patent protection both in the U.S. and internationally and file additional patent applications, when appropriate, to cover improvements in our compounds, products and technology.

Total Rewards Gilead’s Total Rewards portfolio is a competitive, robust package that is designed to optimize our employees’ performance and support their wellbeing, allowing them to focus on mission-critical work. Each year, we reassess our Total Rewards package to confirm whether it offers benefits and incentives that align with our total rewards philosophy. Our portfolio (which varies by country and is subject to employee eligibility requirements and legal and regulatory requirements) includes but is not limited to: •Competitive base salary •Incentive compensation •Stock awards •Employee stock purchase plan •401(k) savings plan with a company match that vests immediately •Health and wellbeing benefits •Flexible work arrangements •Flexible spending accounts •Paid time off •Paid family leave •Family support services, including family planning and reproductive health (e.g., fertility, adoption and surrogacy)
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm｜as_of：2026-02-24
<<<
HIV We receive a substantial portion of our revenue from sales of our products for the treatment and prevention of HIV infection. We may be unable to sustain or increase sales of our HIV products for any number of reasons, including market share gains by competitive products, including generics, or the inability to introduce new HIV medications necessary to remain competitive. In such case, we may need to scale back our operations, including our future drug development and spending on research and development (“R&D”) efforts.

If we are unable to launch commercially successful new products or new indications for existing products, including approval for earlier lines of therapy, our business will be adversely impacted. The launch of commercially successful products is necessary to grow our business, cover our substantial R&D expenses, and offset revenue losses when existing products lose market share due to factors such as competition and loss of patent exclusivity. There are many difficulties and uncertainties inherent in drug development and the introduction of new products. The product development cycle is characterized by significant investments of resources, long lead times and unpredictable outcomes due to the nature of developing medicines for human use. We expend significant time and resources on our product pipeline as well as on preparations for potential commercial launch without any assurance that we will recoup our investments or that our efforts will be commercially successful. A high rate of failure is inherent in the discovery and development of new products, and failure can occur at any point in the process, including late in the process after substantial investment.…

New branded or generic products entering major markets affect our ability to maintain pricing and market share. Our products compete with other available products based primarily on efficacy, safety, tolerability, acceptance by doctors, ease of patient compliance, ease of use, price, insurance and other reimbursement coverage, distribution and marketing. A number of companies, including large pharmaceutical and biotechnology companies and specialized pharmaceutical firms acting either independently or together with other such companies, are pursuing the development of products and technologies that may be competitive with our existing products or research programs. Furthermore, academic institutions, government agencies and other public and private organizations conducting research may seek patent protection or may establish collaborative arrangements for competitive products or programs. We may be adversely impacted if any of these competitors gain market share as a result of new technologies, commercialization strategies or otherwise.

Any adverse developments affecting or resulting from any single entity within our manufacturing operations or the operations of our CMOs, CTLs and corporate partners can result in shipment delays, inventory shortages, lot failures, product withdrawals or recalls or other interruptions in the development and commercial supply of our products, which may result in us not being able to generate sufficient quantities of clinical or commercial product to meet market demand and may cause delays in our clinical trials and applications for regulatory approval. We have incurred, and will continue to incur, inventory write-off charges and other expenses for products that fail to meet specifications and quality standards as well as changes we may adopt in our manufacturing strategy, and we may need to undertake costly remediation efforts or seek more costly manufacturing alternatives. Such developments could increase our manufacturing costs, cause us to lose revenues or market share and damage our reputation. Our business may be adversely affected if approval of any of our product candidates were delayed or if production of our products were interrupted.

Generic manufacturers have sought, and may continue to seek, FDA approval to market generic versions of our products through an abbreviated new drug application (“ANDA”), the application process typically used by manufacturers seeking approval of a generic drug. For a description of our ANDA litigation, see Note 12. Commitments and Contingencies of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K. ANDA litigation and related settlement and license agreements, in some cases, may result in a loss of exclusivity for our patents sooner than we would otherwise expect. In addition, loss of exclusivity may be earlier than expected under these settlement and license agreements under certain circumstances. For example, settlement and license agreements with generic manufacturers typically include acceleration clauses that permit generic entry before the agreed-upon entry date in certain circumstances, and generic manufacturers may continue to challenge the patents protecting our products. The entry of generic versions of our products has, and may in the future, lead to market share and price erosion.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm｜as_of：2026-02-24
<<<
To arrive at the revised estimated fair values as of June 30, 2025 and December 31, 2025, we used a probability-weighted income approach that discounts expected future cash flows to present value, which requires the use of Level 3 fair value measurements and inputs, including critical estimated inputs, such as: revenues and operating profits related to the planned utilization of bulevirtide outside of the European Union (“EU”), which includes inputs such as addressable patient population, projected market share, treatment duration, and the life of the potential commercialized product; the probability of technical and regulatory success; the time and resources needed to complete the development and approval of bulevirtide outside of the EU; an appropriate discount rate based on the estimated weighted-average cost of capital for companies with profiles similar to our profile; and risks related to the viability of and potential alternative treatments in any future target markets. Our revised discounted cash flows for the June 30, 2025 and December 31, 2025 fair value estimations primarily reflected the updated expectations for bulevirtide’s potential market share outside of the EU.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GILD_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
