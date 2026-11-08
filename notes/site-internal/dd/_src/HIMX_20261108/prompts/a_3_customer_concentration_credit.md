你是 stock-analyst v20 DD 的證據採集子 agent。標的：HIMX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - HIMX Himax Technologies top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Himax Technologies customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
In 2025, Customer A and its affiliates accounted for 24.0% of our revenues. Our two largest customers together accounted for over 33% of our revenues in 2025. See “Item 5.A. Operating Results—Description of Certain Statements of Profit or Loss Line Items—Revenues” for our revenues description. Our results of operations and financial condition would be significantly linked to the success and purchase policy of any such customer. As of December 31, 2025, our accounts receivable from Customer A and its affiliates were $57.8 million, which represented approximately 28.8% of our accounts receivable, net. The concentration of our accounts receivable exposes us to increased credit risk. Moreover, we have at times agreed to extend the payment terms for certain of our customers. As a result, any loss of or a sharp reduction in any such customer’s sales, a default by any such customer, a prolonged delay in the payment of accounts receivable or the extension of payment terms for our customers could adversely affect our cash flow, liquidity and operating results.

We have been increasingly selling our products to customers in the PRC. In 2024 and 2025, approximately 73.4% and 73.8% of our revenues, respectively, were from customers headquartered in the PRC. We expect to continue to increase our sales to customers in the PRC in the future. With regional customer concentration, we are particularly subject to economic and political events and other developments that affect our customers in the PRC.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
Customers Our customers for display drivers are primarily Panel Manufacturers and mobile device module manufacturers, who in turn design and market their products to manufacturers of end-use products such as notebook computers, desktop monitors, televisions, smartphone, tablet, automotive and consumer electronics products. We may sell our products through agents or distributors for certain products or in certain regions. As of December 31, 2025, we sold our products to around 300 customers. Our ten largest customers together accounted for approximately 74.1%, 73.6% and 71.3% of our revenues in 2023, 2024 and 2025, respectively. In 2023, 2024 and 2025, our two largest customers accounted for 10% or more of our net revenue: customer A and its affiliates accounted for 28.7%, 26.4% and 24.0% of our revenues, respectively; and customer C accounted for 11.0%, 8.3% and 7.8%, respectively.
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
A limited number of customers account for substantially all our revenues. For example, Customer A and its affiliates accounted for 28.7%, 26.4% and 24.0% of our revenues in 2023, 2024 and 2025, respectively. Customer C accounted for 11.0%, 8.3% and 7.8% of our revenues in 2023, 2024 and 2025, respectively.

Customer A and its affiliates ​ $ 271,351 ​ 28.7 ​ $ 239,001 ​ 26.4 ​ $ 200,105 ​ 24.0 Customer C ​ 103,839 ​ 11.0 ​ ​ 75,564 ​ 8.3 ​ ​ 64,755 ​ 7.8 Others ​ 570,238 ​ 60.3 ​ ​ 592,237 ​ 65.3 ​ ​ 567,313 ​ 68.2 Total ​ $ 945,428 ​ 100.0 ​ $ 906,802 ​ 100.0 ​ $ 832,173 ​ 100.0 ​ The global TFT-LCD and OLED panel market is highly concentrated, with only a limited number of TFT-LCD and OLED panel manufacturers producing TFT-LCD and OLED panels in high volumes. We sell panel display drivers to many of these panel manufacturers. Our revenues, therefore, will depend on our ability to capture an increasingly larger percentage of each panel manufacturer’s display driver requirements. The sales to panel makers in China have become a significant portion of our revenue due to the Chinese panel maker business expansion which started in 2011. We derive substantially all of our revenues from sales to Asia-based customers whose end products are sold worldwide. In 2023, 2024 and 2025, approximately 15.0%, 15.3% and 14.7% of our revenues, respectively, were from customers headquartered in Taiwan and approximately 76.2%, 73.4% and 73.8% of our revenues, respectively, were from customers headquartered in China. We believe that substantially all of our revenues will continue to be from customers located in Asia, where almost all of the panel manufacturers and mobile device module manufacturers are located.…
>>>

[4] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：其他章節（財報附註等）｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
The Company depends on two customers for majority of its revenues. The Company’s sales to these two customers as a percentage of revenues are as follows: ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ Year Ended December 31, ​ ​ ​ ​ 2023 ​ 2024 ​ ​ ​ 2025 Customer A and its affiliates 28.7 % 26.4 % 24.0 % Customer C 11.0 % 8.3 % 7.8 % ​ The percentage of the Company’s accounts receivable accounted by customers, those representing more than 10% of total accounts receivable balance, is summarized as follows: ​ ​ ​ ​ ​ ​ ​ ​ ​ December 31, ​ December 31, ​ ​ ​ ​ 2024 ​ ​ ​ 2025 Customer A and its affiliates 29.1 % 28.8 % Customer C 8.7 % 6.0 % ​ Refer to Note 10 for aging analysis of accounts receivable and the movement in the loss allowance.

Taiwan ​ $ 117,784 ​ 116,829 U.S. ​ 1,433 ​ 1,299 China ​ 1,688 ​ 1,392 Korea ​ 286 ​ 476 Japan ​ 89 ​ 35 ​ ​ $ 121,280 ​ 120,031 ​ Revenues from significant customers, those representing 10% or more of total revenue for the respective periods, are summarized as follows: ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ Year ended December 31, ​ ​ ​ ​ 2023 ​ ​ ​ 2024 ​ ​ ​ 2025 ​ ​ (in thousands)

Driver IC segment: ​ ​ ​ ​ ​ Customer A and its affiliates ​ $ 234,581 ​ 207,725 ​ 176,457 Customer C ​ ​ 102,719 ​ 73,696 ​ 61,701 ​ ​ $ 337,300 ​ 281,421 ​ 238,158 Non-driver products segment: ​ ​ ​ ​ ​ ​ ​ Customer A and its affiliates ​ $ 36,770 ​ 31,276 ​ 23,648 Customer C ​ ​ 1,120 ​ 1,868 ​ 3,054 ​ ​ $ 37,890 ​ 33,144 ​ 26,702 ​ Accounts receivable from significant customers, those representing 10% or more of total accounts receivable for the respective dates, is summarized as follows: ​ ​ ​ ​ ​ ​ ​ ​ ​ December 31, December 31, ​ ​ ​ ​ 2024 ​ ​ ​ 2025 ​ ​ (in thousands)
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
