你是 stock-analyst v20 DD 的證據採集子 agent。標的：SNDK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - SNDK Sandisk tariff section 232 2026
  - Sandisk export control OR entity list Computer Hardware 2026
  - SNDK Sandisk China tariff OR trade restriction 2026
  - Computer Hardware tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
Sales and Distribution We sell our products to computer manufacturers and OEMs, cloud service providers, resellers, distributors and retailers throughout the world. We maintain sales offices in selected parts of the world including the major geographies of the Americas, Asia Pacific, Europe and the Middle East. Our international sales, which include sales to foreign subsidiaries of U.S. companies but do not include sales to U.S. subsidiaries of foreign companies, represented 82%, 80% and 86% of our net revenue for 2026, 2025 and 2024, respectively. Sales to international customers are subject to certain risks not normally encountered in domestic operations, including exposure to tariffs and various trade and other regulations. For a discussion of associated risks, see Part I, Item 1A., Risk Factors of this Annual Report on Form 10-K.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
We are subject to risks and regulatory obligations associated with our global manufacturing operations and global sales efforts, as well as risks and regulatory obligations associated with our utilization of global suppliers, including: •obtaining governmental approvals and compliance with evolving domestic and foreign regulations; •the need to comply with regulations on international business, including the Foreign Corrupt Practices Act, the United Kingdom Bribery Act 2010, the anti-bribery laws of other countries and rules regarding conflict minerals; •the impacts of social, political, immigration, and tax and trade policies in the U.S. and abroad; •exchange, currency and tax controls and reallocations; •the continued evolution and implementation of complex global and local tax regimes; •varying levels of protection of intellectual property rights; •policies and financial incentives by governments in China, the U.S. and countries in Europe and Asia designed to reduce dependence on foreign semiconductor manufacturing capabilities; •trade barriers, such as export controls, export bans, import restrictions, embargoes, sanctions, license and certification requirements (including semiconductor, encryption and other technology), tariffs and complex customs regulations; 14 Table of Contents •difficulties in managing international operations, including appropriate internal controls; and •financial volatility and disruptions to supply chain resulting from public health crises.

For example, there are pending and ongoing investigations initiated by the United States under Section 232 of the Trade Expansion Act of 1962 and Section 301 of the Trade Act of 1974 that may impact tariff rates for Sandisk products. We continue to monitor changes to the U.S. tariff regime to assess potential implications on the Company. Though the majority of our products sold in the U.S. are currently exempt from tariffs, additional tariff increases or the loss of applicable exemptions would increase the cost of goods sold for our products sold in the U.S., which could negatively impact our margins and financial performance. Increases in the price of our products in response to increased costs may adversely impact demand for those products in the U.S., which could also negatively impact our performance and financial results. Future trade policies and regulations in the U.S. and other countries, the terms of any trade arrangements that may be negotiated between the U.S.…

Our suppliers have in the past been, and may in the future be, unable or unwilling to meet our requirements, including as a result of events outside of their control such as trade restrictions (including tariffs, quotas, sanctions, and embargoes), supply chain shortages, labor disputes, geopolitical conflicts, industrial accidents, cybersecurity incidents, public health emergencies or natural disasters. If we are unable to purchase sufficient quantities from our current suppliers or qualify and engage additional suppliers, or if we cannot purchase materials at a reasonable price, we may not be able to meet demand for our products. Trade restrictions, including tariffs, quotas and embargoes, demand from other high-volume industries for materials or components used in our products, disruptions in supplier relationships or shortages in other components and materials used in our customers’ products could result in increased costs to us, longer lead times, or decreased demand for our products, which could negatively impact our business. Delays, shortages or cost increases experienced by our suppliers in developing or sourcing materials and components for use in our products or incompatibility or quality issues relating to our products could also harm our business.

Demand for our devices, software and solutions, which we refer to in this “Risk Factors” section as our “products,” depends in large part on the demand for systems manufactured by our customers and on storage upgrades to existing systems. The demand for systems has been volatile in the past and often has had an exaggerated effect on the demand for our products in any given period. Demand for and prices of our products are influenced by, among other factors, actual and projected data growth, the balance between supply and demand in the storage market, including the effects of new fab capacity, macroeconomic factors and geopolitical tensions, including tariffs or trade restrictions, business conditions, technology transitions and other actions taken by us or our competitors. The storage market has in the past experienced, and may continue to experience, periods of excess capacity leading to liquidation of excess inventories, inventory write-downs, underutilization charges, significant reductions in average selling prices and negative impacts on our revenue and gross margins, and volatile product life cycles that harm our ability to recover the cost of product development.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
44 Table of Contents There are pending and ongoing investigations initiated by the United States under Section 232 of the Trade Expansion Act of 1962 and Section 301 of the Trade Act of 1974 that may impact tariff rates for our products. Currently, the majority of our products sold in the U.S. are exempt from tariffs, but additional tariff increases, or the loss of applicable exemptions, would increase the cost of goods sold for our products sold in the U.S., which could negatively impact our margins and financial performance. Increases in the price of our products in response to increased costs may adversely impact demand for those products in the U.S., which could also negatively impact our performance and financial results. Future trade policies and regulations in the U.S. and other countries, the terms of any trade arrangements that may be negotiated between the U.S. and other countries, the scope, amount, or duration of tariffs that may be imposed by any country, and the impact of these factors on our business are uncertain and may contribute to increased costs and reduced demand for our products, each of which could harm our financial performance.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
