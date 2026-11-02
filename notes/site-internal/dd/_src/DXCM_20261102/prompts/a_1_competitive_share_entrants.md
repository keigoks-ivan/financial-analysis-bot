你是 stock-analyst v20 DD 的證據採集子 agent。標的：DXCM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - DXCM DexCom market share gaining OR losing 2026
  - DexCom new entrant OR displace threat Medical Devices 2026
  - DXCM competitor design win 2026
  - DexCom vs Medical Devices peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm｜as_of：2026-02-12
<<<
13 Competition The market for glucose monitoring devices is intensely competitive, subject to rapid change and significantly affected by new product introductions and other market activities of industry participants. In selling our current CGM systems, we compete directly with the Diabetes Care division of Abbott Laboratories; Medtronic plc’s Diabetes Group (which implemented a spinoff of its diabetes business into a separate company called MiniMed); Roche Diabetes Care, a division of Roche Diagnostics; privately-held LifeScan, Inc.; Ascensia Diabetes Care; and other smaller market entrants, each of which manufactures and markets products for the single-point finger stick device market. Collectively with us, these companies currently account for the majority of the worldwide sales of self-monitored glucose testing systems.

Several companies are developing or commercializing products for continuous or periodic monitoring of glucose levels in the interstitial fluid under the skin that compete directly with our products. We have competed with Abbott and their Libre family of CGM products for many years. Medtronic (MiniMed) markets and sells a standalone glucose monitoring product called Guardian Connect, both internationally and in the United States, and a disposable CGM system called Simplera in the U.S. and international markets.

We are also aware of companies outside the traditional medical device sector that are attempting to develop competitive products and services, including for the general health and wellness, or population health space. Some of the companies developing or marketing competing devices are large and well-known publicly traded companies. Such competitors may benefit from guidance issued on January 6, 2026 by the FDA’s Center for Devices and Radiological Health that effectively broadens the range of products that may be considered “general wellness devices,” including wearables that provide readings around bodily functions and vital signs such as heart rate, blood pressure, and blood glucose.

For additional information on competition, please see our Risk Factor entitled “We operate in a highly competitive market and face competition from large, well-established companies with significant resources, and, as a result, we may not be able to compete effectively.”

In late 2025, CMS extended the Durable Medical Equipment, Prosthetics, Orthotics and Supplies (DMEPOS) competitive bidding program to include our CGMs and receivers beginning with contracting in 2027, and payment changes effective January 1, 2028. Under the program, DMEPOS suppliers compete to become Medicare contract suppliers by submitting bids to furnish certain items. CMS anticipates that ten (10) contracts will be awarded for CGMs. However, while the competitive bidding program previously used competitive bidding areas, or CBAs, for contract awards, CMS determined that for CGMs and certain other DME, a Remote Item Delivery, or RID, CBA was more appropriate. It remains to be seen whether CGMs will be covered under a single, nationwide RID CBA or whether regional RID CBAs will be established. In any event, the bid process is expected to result in lower Medicare reimbursement for CGM systems, particularly because CMS is changing the pricing under the RID CBA by setting a single payment amount for covered items at the 75th percentile of the winning bids, rather than using the maximum winning bid. Further, CMS has reclassified CGMs and insulin infusion pumps to items that require frequent and substantial servicing and will phase in monthly rental payments for these items.…

Total Rewards and Pay Equity Our total rewards package includes market competitive pay, comprehensive and competitive global benefits and retirement offerings, paid time off and family leave, tuition reimbursement and on-site services. To foster a stronger sense of ownership and align the interests of employees with shareholders, we offer an Employee Stock Purchase Plan, and restricted stock units are provided to eligible employees under our broad-based stock incentive programs.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm｜as_of：2026-02-12
<<<
In the United States and other countries, government and private sector access to health care products continues to be a subject of focus, and efforts to reduce health care costs are being made by third-party payors. Most of our customers rely on third-party payors, including government programs and private health insurance plans, to cover the cost of the G6, G7, G-7 15 Day, Dexcom One, and Dexcom ONE+. We expect that these continuing cost reduction and containment measures could result in lower prices for these products and lower reimbursement rates, as well as could lead to patients being unable to obtain approval for coverage or payment from these third-party payors resulting in costs being shifted to patients for these products. Additionally, we may experience pricing pressure if our products are increasingly subject to competitive bidding processes, which include substantial costs and managerial time to prepare bids and proposals for contracts that may not be awarded to us or may be split among competitors. For example, in June 2025, the Centers for Medicare & Medicaid Services published a proposed rule that would subject continuous glucose monitors to the competitive bidding process, which could negatively impact our reimbursement and result in price decreases.…

Nevertheless, third-party payors are increasingly attempting to contain healthcare costs by limiting both coverage and the level of reimbursement of new and existing medical devices, and, as a result, they may be restrictive, or they may not cover or provide adequate payment for our products. In order to obtain additional reimbursement arrangements, including under pharmacy benefits, we may have to agree to a net sales price lower than the net sales price we might charge in other sales channels. Our revenue may be limited by the continuing efforts of government and third-party payors to contain or reduce the costs of healthcare through various increasingly sophisticated means, such as leveraging increased competition, increasing eligibility requirements such as second opinions and other documentation, purchasing in a bundle, or redesigning benefits. In December 2021, CMS published a final rule expanding the classification of DME under Medicare Parts B & C to include adjunctive CGMs (i.e., CGMs that do not replace standard blood glucose monitors for treatment decisions) and related supplies. This final rule expanded coverage of CGMs to include competing devices, which may continue to have a negative impact on our sales as a result of increased market competition.

Many of the companies that we collaborate with are also competitors or potential competitors who may decide to terminate our collaborative arrangement. In the event of such a termination, we may be required to devote additional resources to product development and commercialization, we may need to cancel some development programs and we may face increased competition. Additionally, collaborations may not result in the development of products that achieve commercial success and could be terminated prior to developing any products. Former collaborators may use the experience and insights they develop in the course of their collaborations with us to initiate or accelerate their development of products that compete with our products, which may create competitive disadvantages for us. Accordingly, we cannot provide assurance that any of our collaborations will result in the successful development of a commercially viable product or result in significant additional future revenues.

We are also aware of companies outside the traditional medical device sector that are attempting to develop competitive products and services, including for the general health and wellness, or population health space. Some of the companies developing or marketing competing devices are large and well-known publicly traded companies. Such competitors may benefit from guidance issued on January 6, 2026 by the FDA’s Center for Devices and Radiological Health that effectively broadens the range of products that may be considered “general wellness devices,” including wearables that provide readings around bodily functions and vital signs such as heart rate, blood pressure, and blood glucose.

33 We have experienced manufacturing and inventory challenges for G7 in the past that resulted in disruptions in our ability to supply certain markets, including in the U.S. and other countries. If we fail to produce a sufficient amount of our products, our ability to supply our markets will be compromised and health care providers and people with diabetes’ decisions to use our products may be negatively impacted. This could lead to loss of sales of and revenues from our products, could potentially decrease our market share, and/or our business, financial condition, results of operations and growth prospects could be materially adversely affected.

We operate in a highly competitive market and face competition from large, well-established companies with significant resources, and, as a result, we may not be able to compete effectively.

In selling our G6, G7, G7 15 Day, Dexcom One and Dexcom ONE+, we compete directly with the Diabetes Care division of Abbott Laboratories; Medtronic (MiniMed); Roche Diabetes Care, a division of Roche Diagnostics; privately-held LifeScan, Inc.; Ascensia Diabetes Care; and other smaller market entrants, each of which manufactures and markets products for the single-point finger stick device market. In selling Stelo, we compete directly with the Diabetes Care division of Abbott Laboratories. Collectively with us, these companies currently account for the majority of the worldwide sales of self-monitored glucose testing systems. We are also aware of emerging competitors primarily located in China.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
