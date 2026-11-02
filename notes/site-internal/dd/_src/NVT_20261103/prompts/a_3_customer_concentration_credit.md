你是 stock-analyst v20 DD 的證據採集子 agent。標的：NVT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - NVT nVent Electric top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - nVent Electric customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm｜as_of：2026-02-17
<<<
7 A loss of, or material cancellation, reduction, or delay in purchases by or delivery of products to, one or more of our largest customers could harm our business.

Our net sales to our largest customer represented approximately 11% of our consolidated net sales in 2025. While we do not have any other customers that accounted for more than 10% of our consolidated net sales in 2025, we have other customers that are key to the success of our business. Our concentration of sales to a number of larger customers makes our relationship with each of these customers important to our business. Our success is dependent on retaining these customers, which requires us to successfully manage relationships and anticipate the needs of our customers in the channels in which we sell our products. Our customers also may be impacted by economic conditions in the industries of those customers, which could result in reduced demand for or a delay in purchases of our products. In addition, our customers may cancel orders for purchases of our products or may not order products at rates consistent with past order levels, or we may not be able to timely deliver products to our largest customers due to supply chain interruptions or otherwise. We cannot provide assurance that we will be able to retain our largest customers. In addition, some of our customers may shift their purchases to our competitors in the future.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 8. Financial Statements｜url：https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm｜as_of：2026-02-17
<<<
Our performance obligations are satisfied at a point in time or over time as work progresses. Revenue from products and services transferred to customers at a point in time accounted for 65%, 76% and 79% of our revenue for the years ended 45 nVent Electric plc Notes to consolidated financial statements December 31, 2025, 2024 and 2023, respectively. Revenue on these contracts is recognized when obligations under the terms of the contract with our customer are satisfied; generally this occurs with the transfer of control upon shipment.

Revenue from products and services transferred to customers over time accounted for 35%, 24% and 21% of our revenue for the years ended December 31, 2025, 2024 and 2023, respectively. For the majority of our revenue recognized over time, we use an input measure to determine progress towards completion. Under this method, sales and gross profit are recognized as work is performed generally based on the relationship between the actual costs incurred and the total estimated costs at completion ("the cost-to-cost method") or based on efforts for measuring progress towards completion in situations in which this approach is more representative of the progress on the contract than the cost-to-cost method. Contract costs include labor, material, overhead and, when appropriate, general and administrative expenses. Changes to the original estimates may be required during the life of the contract and such estimates are reviewed on a regular basis. Sales and gross profit are adjusted using the cumulative catch-up method for revisions in estimated total contract costs. These reviews have not resulted in adjustments that were significant to our results of operations.…

Trade receivables and concentration of credit risk We record an allowance for doubtful accounts to reduce our receivables balance by the amount that is estimated to be uncollectible from our customers, or the expected loss. Estimates used in determining the allowance for doubtful accounts are based on historical collection experience, including write-offs and recoveries, periodic credit evaluations of our customers' financial situation and current circumstances, as well as reasonable and supportable forecasts of future economic conditions. We generally do not require collateral. Accounts receivable from one customer represented approximately 11% of total accounts receivable as of December 31, 2025. No customer receivable balance exceeded 10% of total net receivable balance as of December 31, 2024.

One customer within our Systems Protection segment represented approximately 11% of consolidated net sales for the year ended December 31, 2025. No customer accounted for more than 10% of net sales in 2024 or 2023.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
