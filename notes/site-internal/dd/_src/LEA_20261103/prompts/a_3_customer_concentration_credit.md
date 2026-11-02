你是 stock-analyst v20 DD 的證據採集子 agent。標的：LEA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - LEA Lear top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Lear customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
Customers In 2025, General Motors, one of the largest automotive and light truck manufacturers in the world, accounted for 22% of our net sales. In addition, Ford accounted for 12%, Mercedes-Benz and Volkswagen each accounted for 10% and Stellantis accounted for 9% of our 2025 net sales. Through acquisitions and organic growth, we strive to diversify our customer base to be reflective of the evolving regional markets in which we operate. We supply and have expertise in all vehicle segments of the automotive market. Our sales content tends to be higher on those vehicle platforms and segments which offer more features and functionality. The popularity of particular vehicle platforms and segments varies over time and by regional market. We expect to continue to win new business and grow sales in-line with or at a rate greater than overall automotive industry production. For further information related to our customers and domestic and foreign sales and operations, see Note 13, "Segment Reporting," to the consolidated financial statements included in this Report.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
ITEM 1A – RISK FACTORS Our business, financial condition, operating results and cash flows may be impacted by a number of factors. In addition to the factors affecting our business identified elsewhere in this Report, the material risk factors affecting our operations include the following: Risks Related to Our Business •Our industry is cyclical and a decline or significant fluctuation in the production levels of our major customers, particularly with respect to models for which we are a significant supplier, or the financial distress of or operational disruptions to one or more of our major customers could adversely affect our financial performance.

Our sales and production may be further affected by new entrants to the industry, as well as various automakers entering or expanding in certain regions, and the restructuring actions, including facility closures, of our customers. Chinese domestic automakers, in particular, continue to expand their market share in China (through electric vehicles) and outside of China with both innovative designs and attractive pricing. As a result, several traditional automakers have experienced declines in revenue and market share. As these traditional automakers are among our largest customers, our business and financial results may be adversely affected by decreases in their businesses or market share.

An economic downturn or other adverse industry conditions that result in a decline or significant fluctuation in the production levels of our major customers, particularly with respect to models for which we are a significant supplier, or the financial distress of or operational disruptions to one or more of our major customers could reduce our sales, increase our costs or otherwise adversely affect our financial condition, operating results and cash flows. Further, our ability to reduce the risks inherent in certain concentrations of business, and thereby maintain our financial performance in the future, will depend, in part, on our ability to continue to diversify our sales on a customer, product, platform and geographic basis to reflect the market overall. We may not be successful in such diversification.

A substantial number of our employees and the employees of our largest customers and suppliers are members of industrial trade unions and are employed under the terms of various labor agreements. We have labor agreements covering approximately 75,000 employees globally. In the United States and Canada, each of our unionized facilities has a separate collective bargaining agreement with the union that represents the workers at such facility, with each such agreement having an expiration date that is independent of the other agreements. Labor agreements covering approximately 67% of our global unionized work force are scheduled to expire in 2026. There can be no assurances that these upcoming negotiations or any other future negotiations with the unions will be resolved favorably or that we will not experience a work stoppage or disruption that could adversely affect our financial condition, operating results and cash flows. A labor dispute involving us, any of our customers or suppliers or any other suppliers to our customers or that otherwise affects our operations, or the inability by us, any of our customers or suppliers or any other suppliers to our customers to negotiate, upon the expiration of a labor agreement, an extension of such agreement or a new agreement on satisfactory terms could adversely affect our financial condition, operating results and cash flows.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
Gross profit and gross margin were $1.5 billion and 6.5% of net sales in 2025, as compared to $1.6 billion and 7.0% of net sales in 2024. Lower production volumes on Lear platforms (including the JLR production disruption), net of new business, reduced gross profit by $191 million. The impact of favorable operating performance, including the benefit of restructuring actions, was largely offset by selling price reductions, higher restructuring costs, and the winddown and divestiture of certain businesses. These factors had a corresponding impact on gross margin. Although customer recoveries largely offset the impact of tariff costs on gross profit, gross margin was negatively impacted by the dilutive effect of tariff recoveries, which increased net sales without a corresponding increase in gross profit.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：其他章節（財報附註等）｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
Revenue is recognized at a point in time when control of the product is transferred to the customer under standard commercial terms, as the Company does not have an enforceable right to payment prior to such transfer. The amount of revenue recognized reflects the consideration that the Company expects to be entitled to in exchange for those products based on the current purchase orders, annual price reductions and ongoing price adjustments. Revenue recognized related to prior years represented approximately 1% of consolidated net sales during the years ended December 31, 2025, 2024 and 2023. The Company's 70 Table of Contents Lear Corporation and Subsidiaries Notes to Consolidated Financial Statements (continued)
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
