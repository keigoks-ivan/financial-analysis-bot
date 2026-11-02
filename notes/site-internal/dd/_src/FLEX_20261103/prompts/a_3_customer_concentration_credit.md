你是 stock-analyst v20 DD 的證據採集子 agent。標的：FLEX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - FLEX Flex top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Flex customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
In fiscal year 2026, our ten largest customers accounted for 45% of net sales. No customer accounted for greater than 10% of the Company's net sales in fiscal year 2026.

Long-Standing, Diverse Customer Relationships. We believe our long-term relationships with key customers are the result of our track record of meeting commitments and delivering value. We serve a wide range of customers across seven reporting units within the ITS, RMS and CPI segments. No customer accounts for more than 10% of our annual revenue and the ten largest accounted for 45% of our net sales in fiscal year 2026.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
•A significant percentage of our sales come from a small number of customers and a decline in sales to any of our largest customers has in the past adversely affected, and could in the future adversely affect, our business, results of operations, cash flows, and financial condition.

A significant percentage of our sales come from a small number of customers and a decline in sales to any of our largest customers has in the past adversely affected, and could in the future adversely affect, our business.

Sales to our ten largest customers represent a significant percentage of our net sales. Our ten largest customers accounted for 45%, 44% and 37% of net sales in fiscal years 2026, 2025 and 2024, respectively. No customer accounted for more than 10% of net sales in fiscal year 2026, 2025 or 2024. Our principal customers have varied from year to year. Customers have in the past experienced, and could in the future experience, dramatic declines in their market shares, competitive position, or demand for their products and services, due to economic or other forces, that may cause them to reduce their purchases from us or, in some cases, result in the termination of their relationship with us. Significant reductions in sales to any of our largest customers, or the loss of major customers, have in the past harmed, and could in the future materially harm, our business, results of operations, cash flows, and financial condition. If we are not able to replace expired, canceled or reduced contracts with new business in a timely manner, including due to qualification, ramp‑up or customer approval requirements, our revenues and profitability would be harmed.…

Customer concentration is particularly pronounced in our Cloud and Power Infrastructure businesses, where a limited number of hyperscale cloud providers, colocation companies, and large enterprise data center operators represent a substantial portion of demand. Hyperscale customers typically have substantial purchasing power and negotiating leverage, which they may use to obtain favorable pricing, extended payment terms, volume flexibility, or other concessions that could reduce our margins or adversely affect our cash flows. As these customers grow larger through consolidation or organic growth, their bargaining power may increase further. In addition, certain hyperscale customers have developed, or may develop, internal design, engineering, or manufacturing capabilities that compete with our offerings. These customers may choose to reduce their reliance on third-party providers like us over time, which could result in reduced order volumes, loss of programs, or increased pricing pressure. Any decision by one or more significant hyperscale customers to vertically integrate, in-source production, or shift purchases to competitors could have a material adverse effect on our business, results of operations, and financial condition.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
Our ten largest customers during fiscal years 2026 and 2025 accounted for 45% and 44% of net sales, respectively. We maintain a diverse portfolio which allows us to operate at scale in many different industries, and, as a result, no customer accounted for greater than 10% of net sales in fiscal year 2026 or 2025.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 8. Financial Statements｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
No customer accounted for greater than 10% of the Company's net sales in fiscal years 2026, 2025 or 2024. A single customer accounted for 16% of the Company's total balance of accounts receivable, net as of fiscal year ended March 31, 2026, which is almost entirely within the CPI segment. No other customers accounted for greater than 10% during the same period. No customer accounted for greater than 10% of the Company's total balance of accounts receivable, net as of the fiscal years ended March 31, 2025 or March 31, 2024.

The Company's ten largest customers accounted for 45%, 44% and 37%, of its net sales in fiscal years 2026, 2025 and 2024, respectively.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
