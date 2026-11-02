你是 stock-analyst v20 DD 的證據採集子 agent。標的：AMKR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - AMKR Amkor Technology top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Amkor Technology customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
End Markets The following table lists the end markets that use our products and sets forth, for the periods indicated, the percentage of net sales in each end market: 2025 2024 2023 End Market Distribution Data (an approximation including representative devices and applications based on a sampling of our largest customers): Communications (smartphones, tablets) 46 % 48 % 50 % Computing (data center, infrastructure, PC/laptop, storage) 20 % 19 % 16 % Automotive, industrial and other (ADAS, electrification, infotainment, safety) 19 % 18 % 21 % Consumer (AR & gaming, connected home, home electronics, wearables) 15 % 15 % 13 % Total net sales 100 % 100 % 100 % RESEARCH AND DEVELOPMENT We believe that technology development is one of the keys to success in the semiconductor packaging and test industry. Our research and development efforts focus on developing new packaging technologies and test solutions to meet evolving customer needs for higher performance, greater integration, smaller form factors and lower costs. Key areas of focus include: •Heterogeneous integration: Developing multi-chip module solutions, including 2.5D and HDFO with and without bridges to provide high-bandwidth die-to-die interconnects, that enable package level integration of different types and levels of silicon technologies for high performance computing, networking and data center applications. This is accomplished by combining processors, chiplets or integrated passive devices into one packaged module.…

CUSTOMERS Our customers include most of the world’s largest semiconductor companies. Our ten largest customers accounted for 72% of our net sales in 2025. Direct sales to Apple and Qualcomm accounted for 29.8% and 11.1% of our net sales, respectively, for the year ended December 31, 2025.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
We have derived and expect to continue to derive a large portion of our revenues from a small group of customers during any particular period due in part to the concentration of market share in the semiconductor industry. Our ten largest customers accounted for, in the aggregate, 72% of our net sales for the year ended December 31, 2025. In addition, we have significant customer concentration within our end markets. The loss of a significant customer, a business combination among our customers, a reduction in orders or decrease in price from a significant customer or disruption in any of our significant commercial arrangements may result in a decline in our sales and profitability and could have a material adverse effect on our business, liquidity, results of operations, financial condition and cash flows.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 8. Financial Statements｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
A significant portion of our revenues is concentrated with a small group of customers (Note 18). Direct sales to our two largest customers accounted for 29.8% and 11.1% of our net sales for the year ended December 31, 2025. The loss of a significant customer, a business combination among customers, a reduction in orders or decrease in price from a significant customer or disruption in any of our significant strategic partnerships or other commercial arrangements could have a material adverse effect on our business, liquidity, results of operations, financial condition and cash flows.

18. Business Segments, Customer Concentrations and Geographic Information We operate as a single operating segment as managed by our Chief Executive Officer, who is considered our chief operating decision maker (“CODM”). The CODM bears the ultimate responsibility for, and is actively engaged in, the allocation of resources and the evaluation of our operating and financial results. We have concluded that we have a single operating segment based on the following: •We are managed under a functionally-based organizational structure with the head of each function reporting directly to the CODM; •Our CODM assesses performance, including resource allocation, trend identification and variance analysis, based on consolidated operating performance and financial results based on net income; •Our CODM allocates resources and makes other operating decisions based on specific customer business opportunities; and •We have an integrated process for the design, development and manufacturing services we provide to all of our customers. We also have centralized sales and administrative functions.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
