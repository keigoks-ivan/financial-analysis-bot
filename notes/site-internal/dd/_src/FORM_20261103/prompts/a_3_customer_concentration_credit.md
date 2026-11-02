你是 stock-analyst v20 DD 的證據採集子 agent。標的：FORM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - FORM FormFactor top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - FormFactor customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
Information concerning revenue concentration by customer appears under Note 2 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K. The following customers represented 10% or more of our quarterly revenues for the quarters indicated: Fiscal Quarters Ended Dec 27, 2025 Sep 27, 2025 Jun 28, 2025 Mar 29, 2025 Dec 28, 2024 Sep 28, 2024 Jun 29, 2024 Mar 30, 2024 SK hynix Inc. 19.2 % 24.5 % 25.0 % 23.3 % 22.0 % 18.1 % 19.5 % 15.5 % Intel Corporation * * 12.4 % 12.0 % * 17.1 % 16.7 % 15.7 % Taiwan Semiconductor Manufacturing Company Ltd. * * 10.4 % * * * * * Samsung Electronics Co., Ltd. * * * * * * * 12.4 % 19.2 % 24.5 % 47.8 % 35.3 % 22.0 % 35.2 % 36.2 % 43.6 % * Less than 10% of revenues.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
A relatively small number of customers account for a significant portion of our revenues. One customer represented 22.9% of total revenues in fiscal 2025, two customers represented a combined 33.5% of total revenues in fiscal 2024 and one customer represented 17.1% of total revenues in fiscal 2023. We anticipate that sales of our products to a relatively small number of customers will continue to account for a significant portion of our revenues, which can drive material fluctuations in sales volume, gross margins due to changes in mix, and leverage on fixed costs. Consolidation in the semiconductor industry may increase this concentration. In the future, the loss of any of these customers, or cancellation, reduction or deferral of even a small number of purchases of our products by these customers, could significantly reduce our revenues. A decline in our 12 customers' market share and commercial success, including their ability to compete favorably within their respective end markets, could significantly impact demand for our products and reduce our revenues. Cancellations, reductions, deferrals or non-payment of invoices could result from downturns in the semiconductor industry, manufacturing delays, quality or reliability issues with our products, or from interruptions to our customers’ operations due to fire, natural disasters or other events, or other issues with the financial stability of our customers.…

Our operations, including data processing and transfer activities, are subject to the evolving geopolitical landscape and the increasingly stringent regulatory environment in jurisdictions where we operate or from which we process data. Specifically, escalating trade tensions and policy divergence between the U.S. and China, including restrictions on technology transfers, cross-border data transfers, export controls, and investment limitations, could impact our ability to conduct business, access critical technologies, or operate effectively in the Chinese market. The sale of our products as a percentage of our revenues to customers inside of China represented 7%, 14%, and 14% of total revenue for fiscal 2025, 2024 and 2023, respectively.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：其他章節（財報附註等）｜url：https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm｜as_of：2026-02-20
<<<
Concentration of Credit Risk and Other Risks and Uncertainties Financial instruments that potentially subject us to concentrations of credit risk consist primarily of cash equivalents, marketable securities and accounts receivable. Our cash equivalents and marketable securities are held in safekeeping by large, credit-worthy financial institutions. We invest our excess cash primarily in U.S. banks, government and agency bonds, money market funds and corporate obligations. We have established guidelines relative to credit ratings, diversification and maturities that seek to maintain safety and liquidity. Deposits in these banks may exceed the amounts of insurance provided on such deposits. To date, we have not experienced any losses on our deposits of cash and cash equivalents. We market and sell our products to a relatively narrow base of customers and generally do not require collateral.

The following customers represented 10% or more of our revenues: Fiscal Year Ended December 27, 2025 December 28, 2024 December 30, 2023 SK hynix Inc. 22.9 % 18.9 % * Intel Corporation * 14.6 % 17.1 % * Less than 10% of revenues.

At December 27, 2025, two customers accounted for 15.8% and 10.8% of gross accounts receivable. At December 28, 2024, one customer accounted for 22.0% of gross accounts receivable. No other customers accounted for 10% or more of gross accounts receivable for these fiscal period ends.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
