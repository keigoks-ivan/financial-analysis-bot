你是 stock-analyst v20 DD 的證據採集子 agent。標的：CAH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Cardinal Health distribution channel disruption OR shift 2026
  - CAH Cardinal Health business model transition subscription OR platform 2026
  - Medical Distribution channel disintermediation D2C 2026
  - Cardinal Health go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-11）｜章節：全文（無法依 Item 切段）｜url：https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm｜as_of：2026-08-11
<<<
Pharmaceutical and Specialty Pharmaceutical Distribution and Services Our Pharmaceutical Distribution businesses' gross margin includes margin from our generic pharmaceutical program, from distribution services agreements with branded pharmaceutical manufacturers, including manufacturers of Specialty pharmaceutical products, and from over-the-counter healthcare and consumer products. It also includes manufacturer cash discounts.

In the Pharma segment, we compete with wholesale distributors with national reach, including McKesson Corporation and Cencora, Inc., regional wholesale distributors, self-warehousing chains, specialty distributors, third-party logistics companies, and companies that provide specialty pharmaceutical services and managed services to specialty physicians, among others. In addition, the Pharma segment has experienced competition from a number of organizations offering generic pharmaceuticals, including telemarketers. We also compete with manufacturers that distribute their products directly to customers.

Distribution State Boards of Pharmacy, FDA, DEA, and various other state authorities regulate the marketing, purchase, storage, and distribution of pharmaceutical and medical products under various federal and state statutes including the federal Prescription Drug Marketing Act of 1987, Drug Quality and Security Act of 2013 (the “DQSA”) and Controlled Substances Act (the "CSA"). The CSA governs the sale, packaging, storage, and distribution of controlled substances. Wholesale distributors of controlled substances must hold valid DEA registrations and state-level licenses, meet various security and operating standards including effective anti-diversion programs, and comply with the CSA. They must also comply with state requirements relating to controlled substances that differ from state to state.

As described in greater detail in the "Business" section, we operate in markets that are highly competitive and dynamic. In recent years, U.S. healthcare industry participants, including distributors, manufacturers, suppliers, management services organizations, healthcare providers, insurers, and pharmacy chains, among others, have consolidated or formed strategic alliances. Consolidations create larger enterprises with greater negotiating power and could result in the possible loss of a customer in the situation where the combined enterprise selects one distributor from two incumbents or a reduction in our ability to market our products and services to new customers. Competitive pressures in each of our businesses may also be increased by new business models, new entrants, new regulations, or changes in enforcement priorities, changes in consumer demand, or general competitive dynamics. Our businesses face continued pricing pressure from these and other factors, which adversely affects our margins. Industry consolidation also impacts other objectives, including our ability to expand or complement our existing businesses through acquisitions. If we are unable to offset margin reductions caused by these pressures through steps such as sourcing or cost control measures, additional service offerings and sales of higher margin products, our results of operations could continue to be adversely affected.

Inventories A portion of our inventories (52 percent at both June 30, 2026 and 2025) are valued at the lower of cost, using the last-in, first-out ("LIFO") method, or market. These inventories are included within the core pharmaceutical distribution facilities of our Pharma segment (“distribution facilities”) and are primarily merchandise inventories. The LIFO method presumes that the most recent inventory purchases are the first items sold, so LIFO helps us better match current costs and revenue. We believe that the average cost method of inventory valuation provides a reasonable approximation of the current cost of replacing inventory within the distribution facilities. As such, the LIFO reserve is the difference between (a) inventory at the lower of LIFO cost or market and (b) inventory at replacement cost determined using the average cost method of inventory valuation.

Distribution Services Agreement and Other Vendor Fees Our Pharma segment recognizes fees received from distribution services agreements and other fees received from vendors related to the purchase or distribution of the vendors’ inventory when those fees have been earned and we are entitled to payment. Since the benefit provided to a vendor is related to the purchase and distribution of the vendor’s inventory, we recognize the fees as a reduction in the carrying amount of the inventory that generated the fees, and as such, a reduction of cost of products sold in our consolidated statements of earnings when the inventory is sold.

Segment Assets The following table presents total assets for the two reportable segments and the remaining operating segments, included in Other, and Corporate at June 30: (in millions) 2026 2025 Pharmaceutical and Specialty Solutions $ 40,777 $ 37,313 Global Medical Products and Distribution 6,651 6,889 Other 4,098 4,045 Corporate 5,773 4,875 Total assets $ 57,299 $ 53,122 The following tables present depreciation and amortization and additions to property and equipment for the two reportable segments and the remaining operating segments, included in Other, and Corporate: (in millions) 2026 2025 2024 Pharmaceutical and Specialty Solutions $ 257 $ 185 $ 184 Global Medical Products and Distribution 219 212 205 Other 112 88 79 Corporate 368 305 242 Total depreciation and amortization $ 956 $ 790 $ 710 (in millions) 2026 2025 2024 Pharmaceutical and Specialty Solutions $ 160 $ 118 $ 76 Global Medical Products and Distribution 134 133 136 Other 111 88 81 Corporate 244 208 218 Total additions to property and equipment $ 649 $ 547 $ 511 The following table presents property and equipment, net by geographic area at June 30: (in millions) 2026 2025 United States $ 2,607 $ 2,422 International 424 436 Property and equipment, net $ 3,031 $ 2,858 14. Share-Based Compensation We maintain Cardinal Health, Inc. stock incentive plans (collectively, the “Plans”) for the benefit of certain of our officers, directors, and employees.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
