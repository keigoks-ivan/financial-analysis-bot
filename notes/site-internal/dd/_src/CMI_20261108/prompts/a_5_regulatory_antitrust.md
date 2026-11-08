你是 stock-analyst v20 DD 的證據採集子 agent。標的：CMI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - CMI Cummins antitrust OR monopoly investigation 2026
  - Cummins regulation OR regulatory scrutiny Specialty Industrial Machinery 2026
  - CMI Cummins DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
ITEM 3. Legal Proceedings
The matters described under “Legal Proceedings” in NOTE 14, “COMMITMENTS AND CONTINGENCIES,” to our Consolidated Financial Statements are incorporated herein by reference.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
Settlement Agreements In December 2023, we announced that we reached an agreement in principle with the EPA, CARB, the DOJ and the California Attorney General’s Office to resolve certain regulatory civil claims regarding our emissions certification and compliance process for certain engines primarily used in pick-up truck applications in the U.S., which became final and effective in April 2024 (collectively, the Settlement Agreements). In the second quarter of 2024, we made $1.9 billion of payments required by the Settlement Agreements. See NOTE 14, “COMMITMENTS AND CONTINGENCIES,” to our Consolidated Financial Statements for additional information.

ENVIRONMENTAL COMPLIANCE Settlement Agreements In December 2023, we announced that we reached an agreement in principle with the EPA, CARB, DOJ and the California Attorney General’s Office to resolve certain regulatory civil claims regarding our emissions certification and compliance process for certain engines primarily used in pick-up truck applications in the U.S., which became final and effective in April 2024, (collectively, the Settlement Agreements). As part of the Settlement Agreements, among other things, we agreed to pay civil penalties, complete recall requirements, undertake mitigation projects, provide extended warranties, undertake certain testing, take certain corporate compliance measures and make other payments. Failure to comply with the terms and conditions of the Settlement Agreements subjects us to stipulated penalties. We recorded a charge of $2.0 billion in the fourth quarter of 2023 to resolve the matters addressed by the Settlement Agreements involving approximately one million of our pick-up truck applications in the U.S. This charge was in addition to the previously announced charges of $59 million for the recalls of model years 2013 through 2018 RAM 2500 and 3500 trucks and model years 2016 through 2019 Titan trucks. We made $1.9 billion of payments required by the Settlement Agreements in the second quarter of 2024.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
GOVERNMENT REGULATION While we have reached Settlement Agreements with the EPA, CARB, the Environmental and Natural Resources Division of the U.S. Department of Justice and the California Attorney General's Office to resolve certain regulatory civil claims regarding our emissions certification and compliance process for certain engines primarily used in pick-up truck applications in the U.S., we have incurred, and likely will incur, other additional claims, costs and expenses in connection with the matters covered by the Settlement Agreements and other matters related to our compliance with emission standards for our engines, including with respect to additional regulatory action and collateral litigation related to these matters. Those and related expenses and reputational damage could have a material adverse impact on our results of operations, financial condition and cash flows.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
Settlement Agreements In December 2023, we announced that we reached an agreement in principle with the U.S. Environmental Protection Agency (EPA), the California Air Resources Board (CARB), the Environmental and Natural Resources Division of the U.S. Department of Justice (DOJ) and the California Attorney General’s Office to resolve certain regulatory civil claims regarding our emissions certification and compliance process for certain engines primarily used in pick-up truck applications in the U.S., which became final and effective in 34 Table of Contents April 2024 (collectively, the Settlement Agreements). We recorded a charge of $2.0 billion in the fourth quarter of 2023 to resolve the matters addressed by the Settlement Agreements involving approximately one million of our pick-up truck applications in the U.S. In the second quarter of 2024, we made $1.9 billion of payments required by the Settlement Agreements. See NOTE 14, COMMITMENTS AND CONTINGENCIES,” to our Consolidated Financial Statements for additional information.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
