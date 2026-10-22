你是 stock-analyst v20 DD 的證據採集子 agent。標的：TDY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - TDY Teledyne Technologies top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Teledyne Technologies customer concentration risk disclosure
  - bankruptcy OR downgrade OR guidance cut 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm｜as_of：2026-02-20
<<<
Customers We have a broad and diversified customer base in the various markets we serve. No commercial customer in 2025 or 2024 accounted for more than 10% of net sales for any of our segments or for the total Company.

In both 2025 and 2024, we sold products to customers in over 100 foreign countries. Approximately 90% of our net sales to international customers during 2025 were made to customers in 30 foreign countries. In 2025, the top five countries for sales to international customers, ranked by net sales, were the United Kingdom (“UK”), Germany, Japan, China and France and represented approximately 20% of our total net sales. There were no sales to individual countries outside of the United States in excess of 10% of our sales.

3 Table of Contents Information on our net sales to the U.S. Government, including direct sales to agencies as a prime contractor and indirect sales as a subcontractor, was as follows (in millions): 2025 2024 2023 Digital Imaging $ 645.5 $ 557.1 $ 570.7 Instrumentation 125.5 123.5 95.9 Aerospace and Defense Electronics 420.1 307.5 330.3 Engineered Systems 368.3 389.0 384.8 Total U.S. Government sales $ 1,559.4 $ 1,377.1 $ 1,381.7 Total U.S. Government sales as a percent of total net sales 25.5 % 24.3 % 24.5 % Our principal U.S. Government customer is the U.S. Department of War (formerly referred to as the U.S. Department of Defense), with total net sales of $1,203.6 million and $1,062.7 million in 2025 and 2024, respectively. With the exception of the Engineered Systems segment, no U.S. Government program in 2025 or 2024 accounted for more than 10% of net sales for any of our segments or for the total Company.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm｜as_of：2026-02-20
<<<
In both 2025 and 2024, sales to customers outside the United States accounted for approximately 48% of total net sales. In both 2025 and 2024, we sold products to customers in over 100 foreign countries. In 2025, the top five countries for sales to international customers, ranked by net sales, were the UK, Germany, Japan, China and France and represented approximately 20% of our total net sales. We anticipate that future sales to international customers will continue to account for a significant and increasing percentage of our revenues.

An economic slowdown in China may adversely affect us. Our net sales to China-based customers represented approximately 4% of total revenues in 2025 and 2024, respectively. Economic growth in China has slowed since the coronavirus disease (“COVID”) pandemic. Continued growth in many of our businesses, including those in our Environmental Instrumentation group, could be negatively impacted if another economic downturn occurs in China.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm｜as_of：2026-02-20
<<<
1,149.8 989.1 160.7 16.2 % Interest and debt expense, net (59.6) (57.9) (1.7) 2.9 % Non-service retirement benefit income 10.9 10.8 0.1 0.9 % Gain (loss) on debt extinguishment 15.0 — 15.0 * Other income (expense), net (21.6) (4.1) (17.5) 426.8 % Income (loss) before income taxes 1,094.5 937.9 156.6 16.7 % Provision (benefit) for income taxes 198.8 117.2 81.6 69.6 % Net income (loss) including noncontrolling interest 895.7 820.7 75.0 9.1 % Less: Net income (loss) attributable to noncontrolling interest 0.9 1.5 (0.6) (40.0) % Net income (loss) attributable to Teledyne $ 894.8 $ 819.2 $ 75.6 9.2 % * Not meaningful Net Sales Net sales increased across three of our four business segments. Total year 2025 net sales included $270.1 million in incremental net sales from current and prior year acquisitions. Refer to “Business Segment Operating Results” later in this section for additional discussion of changes in net sales. In both 2025 and 2024, sales to international customers represented approximately 48% of total net sales. Approximately 25% and 24% of our total net sales in 2025 and 2024, respectively, were derived from contracts with agencies of, or prime contractors to, the U.S. Government.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TDY_20261022/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
