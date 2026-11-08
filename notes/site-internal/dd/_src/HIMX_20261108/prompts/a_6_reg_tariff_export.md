你是 stock-analyst v20 DD 的證據採集子 agent。標的：HIMX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - HIMX Himax Technologies tariff section 232 2026
  - Himax Technologies export control OR entity list Semiconductors 2026
  - HIMX Himax Technologies China tariff OR trade restriction 2026
  - Semiconductors tariff exposure supply chain 2026


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
Panel Manufacturers, including our customers, experience significant pressure on prices and profit margins, due largely to growing industry capacity and fluctuations in demand for TFT-LCD and OLED panels. Some panel manufacturers have greater access to capital or greater production, research and development, intellectual property, marketing or other resources than our customers, who may not be able to compete and sustain their market positions. Furthermore, our customers’ business performance may fluctuate significantly due to a number of factors, many of which are beyond their control, including and not limited to: (1) changes in consumer demand and deteriorating general economic conditions, such as geopolitical tensions and increasing tariffs; (2) the cyclical nature of the TFT-LCD and OLED industry in average selling price fluctuations, as well as its downstream industries; (3) the speed at which Panel Manufacturers expand production capacity; (4) brand companies’ continued needs for original equipment manufacturing services provided by Panel Manufacturers; (5) access to raw materials, components, equipment and utilities on a timely and economical basis; (6) technological changes; (7) the rescheduling and cancellation of large orders; (8) access to funding on satisfactory terms; and (9) fluctuations in the currencies of TFT-LCD and OLED panels exporting countries against the U.S. dollar.

6 Table of Contents Extra export licenses may be needed for certain product or technology for certain customers. These licenses are regulated by Export Administration Regulations (EAR) which are administered by the U.S. Department of Commerce’s Bureau of Industry and Security (BIS).

Our business is subject to various international laws and legal requirements from the U.S. Export Administration Regulations and other jurisdictions’ applicable executive orders in packaging, product content, labor and import/export regulations, etc. These laws, regulations and orders are complex, may change frequently and with limited notice, have generally become more rigorous and have intensified under the current U.S. administration, especially in recent geopolitical tensions with China. We may be required to incur significant expense to comply with, or to remedy violations of, these regulations. In addition, if our customers fail to comply with these regulations or our customers are sanctioned, or added to the Entity List of EAR by BIS, we may be required to suspend sales to these customers, which could damage our reputation and materially and adversely impact our results of operations. If our foundry, tape, assembly and testing suppliers fail to comply with these regulations or our suppliers are sanctioned or added to the Entity List of EAR by BIS, we may suspend their services and have to obtain alternative services in a timely manner. Considering the amount of time, it usually takes to qualify assembly and testing houses, we may experience significant delays in product shipments.…

The PRC economy differs from the economies of most developed countries in many respects, including the structure, level of government involvement, level of development, foreign exchange control and allocation of resources. The PRC economy has been transitioning from a planned economy to a more market-oriented economy and is growing rapidly. For the past two decades, the PRC government has implemented economic reform measures emphasizing utilization of market forces in the development of the economy and also adjusted its macroeconomic control policies from time to time. These policies have led and may continue to lead to changes in market conditions. Further, if new, US sanctions are imposed on China and any new tariffs, legislation and/or regulations are implemented, or if existing trade agreements are renegotiated, such changes could have an adverse effect on our customers or suppliers in China. We cannot predict whether changes in the PRC’s political, economic and social conditions, laws, regulations and policies will have any adverse effect on our customers in the PRC. In addition, the interpretation of PRC laws and regulations involves uncertainties.…

Changes in U.S. and international trade policies, including the possibility that new tariffs could be imposed by the U.S. or other countries on Taiwanese company products, may adversely impact our business and operating results. In addition, geopolitical tensions and concerns over supply chain resilience may accelerate efforts by our customers and other industry participants to diversify semiconductor supply chains away from regions with high geopolitical risk. Such shifts in semiconductor supply chain structures could lead to changes in customer sourcing strategies, regulatory requirements or competitive dynamics, which could adversely affect our business, financial condition and results of operations.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
● Large-sized Display Drivers. Revenues from display drivers for large-sized application decreased by 28.0% to $90.7 million in 2025 from $125.9 million in 2024. The decline was primarily attributable to weak macroeconomic conditions, including tariff and geopolitical uncertainties, coupled with continued tight inventory management by our key panel customers. In addition, intensified price competition from Chinese peers exerted further pressure on overall performance.

● Small and Medium-sized Display Drivers. Revenues from small and medium-sized display drivers decreased by 8.0% to $575.1 million in 2025 from $625.4 million in 2024. Amid slowing end-market sell-through and tariff-related uncertainties, smartphone and tablet sales were particularly impacted. Nevertheless, our automotive driver sales in 2025 still delivered single-digit year-over-year growth, outperforming overall global automotive industry growth, primarily supported by continued TDDI adoption among customers worldwide.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
