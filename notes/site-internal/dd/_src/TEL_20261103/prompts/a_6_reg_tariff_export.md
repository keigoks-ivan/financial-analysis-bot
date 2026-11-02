你是 stock-analyst v20 DD 的證據採集子 agent。標的：TEL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - TEL TE Connectivity tariff section 232 2026
  - TE Connectivity export control OR entity list Electronic Components / Connectors 2026
  - TEL TE Connectivity China tariff OR trade restriction 2026
  - Electronic Components / Connectors tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1385157/000110465925109150/tel-20250926x10k.htm｜as_of：2025-11-10
<<<
Competition The industries in which we operate are highly competitive, and we compete with thousands of companies that range from large multinational corporations to local manufacturers. Competition is generally based on breadth of product offering, product innovation, price, quality, delivery, and service. We have experienced, and expect to continue to experience, downward pressure on prices. However, as a result of increased costs and tariffs, certain of our businesses implemented price increases in recent years.

Government Regulation and Supervision The import and export of products are subject to regulation by the various jurisdictions where we conduct business. A small portion of our products, including defense-related products, may require governmental import and export licenses, whose issuance may be influenced by geopolitical and other events. We have a trade compliance organization and other systems in place to apply for licenses and otherwise comply with such regulations. Any failure to maintain compliance with domestic and foreign trade regulation could limit our ability to import and export raw materials and finished goods into or from the relevant jurisdiction.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1385157/000110465925109150/tel-20250926x10k.htm｜as_of：2025-11-10
<<<
Our business and operating results have been and will continue to be affected by economic conditions regionally or globally, including new or increased tariffs and other barriers to trade, including escalation of trade and tariff tensions between the United States (“U.S.”), China, the EU, and other countries, changes to fiscal and monetary policy, inflation, slower growth or recession, higher interest rates, labor disruptions, the cost and availability of consumer and business credit, end demand from consumer and industrial markets, significant bank failures, government shutdowns, and concerns as to sovereign debt levels including credit rating downgrades and defaults on sovereign debt. Any of these economic factors could cause our customers to experience deterioration of their businesses, cash flow, financial condition, and ability to obtain financing. As a result, existing or potential customers may delay or cancel plans to purchase our products and may not be able to fulfill their obligations to us in a timely fashion or in full. Further, our vendors may experience similar problems, which may impact their ability to fulfill our orders or meet agreed service and quality levels. If regional or global economic conditions deteriorate, our results of operations, financial position, and cash flows could be materially adversely affected.…

Concerns about deterioration in the global economy, together with concerns about tariffs, credit, inflation, or deflation, have caused and could continue to cause significant volatility in the price of all securities, including fixed income and equity securities, which has reduced and could further reduce the value of our pension plans’ investment portfolios. In addition, the expected returns on plan assets may not be achieved. A decrease in the value of our pension plans’ investment portfolios or a reduction in returns on plan assets could require us to significantly increase funding of such obligations, which would have an adverse effect on our results of operations, financial position, and cash flows.

Our workforce; manufacturing, research, administrative, and sales facilities; markets; customers; and suppliers are located throughout the world. As a result, we are exposed to risks that could negatively affect sales or profitability, including: · changes in global trade policies, including sanctions, tariffs, trade barriers, and trade disputes; · regulations related to customs and import/export matters; · variations in lengths of payment cycles and challenges in collecting accounts receivable; · tax law and regulatory changes, examinations by taxing authorities, changes to the terms of income tax treaties, and difficulties in the tax-efficient repatriation of cash generated or held in a number of jurisdictions; · employment regulations and local labor conditions, including increases in employment costs, particularly in low-cost regions in which we currently operate; · difficulties protecting intellectual property; · instability in economic or political conditions, including elections, sovereign debt levels, government shutdowns, Eurozone uncertainty, inflation, recession, and actual or anticipated military or political conflicts, including the continuing military conflicts in certain parts of the world; and · the impact of each of the foregoing on our outsourcing and procurement arrangements.

We have sizeable operations in China, including 19 principal manufacturing sites. In addition, approximately 25% of our net sales in fiscal 2025 were made to customers in China. Economic conditions in China have been, and may continue to be, volatile and uncertain. In addition, the legal and regulatory system in China continues to evolve and is subject to change. There also continues to be significant uncertainty about the relationship between the U.S. and China, including with respect to geopolitics, trade policies, treaties, government regulations, and tariffs. The current political climate has intensified concerns about trade tensions between the U.S. and China in connection with each country’s recent or proposed tariffs on the other country’s products. Accordingly, our operations and transactions with customers in China could be adversely affected by changes to market conditions, changes to the regulatory environment, increased trade barriers, tariffs, or restrictions, or interpretation of Chinese law.

We are a large buyer of resins, chemicals, additives, and metals, including copper, gold, silver, palladium, aluminum, brass, steel, and zinc. Many of these raw materials are produced in a limited number of countries around the world or are only available from a limited number of suppliers. The prices of many of these raw materials continue to fluctuate, and in many cases increase, and fluctuations may persist in the future. In addition, feedstock for resins and resins themselves, as well as certain other commodities, are increasingly subject to varied and unrelated force majeure events worldwide further impacting price and availability. In recent years, raw material prices and availability have been affected by worldwide economic conditions, including supply chain disruptions, inflationary cost pressures, and tariff and trade policies. If we have difficulty obtaining raw materials, the quality of available raw materials deteriorates, or there are significant price increases for these raw materials, it could have a substantial impact on the price we pay for raw materials. To the extent we cannot compensate for cost increases through productivity improvements or price increases to our customers, our margins may decline, materially affecting our results of operations, financial position, and cash flows. In addition, we use financial instruments to hedge the volatility of certain commodities prices.…

We also must comply with applicable trade regulations in the jurisdictions where we operate. A small portion of our products, including defense-related products, may require governmental import and export licenses, the issuance of which may be influenced by geopolitical and other events. Any failure to maintain compliance with trade regulations could limit our ability to import and export raw materials and finished goods into or from the relevant jurisdiction, which could negatively impact our results of operations, financial position, and cash flows.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-10）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1385157/000110465925109150/tel-20250926x10k.htm｜as_of：2025-11-10
<<<
● Net cash provided by operating activities was $4,139 million in fiscal 2025. Economic Conditions Our business and operating results have been and will continue to be affected by worldwide economic conditions. The global economy has been impacted in recent years by supply chain disruptions, inflationary cost pressures, and, most recently, tariff and trade policies. We are monitoring the current environment and its potential effects on our customers and the end markets we serve.

We are actively monitoring developments in tariff and trade policies and the potential impacts on our business. In addition, we are using pricing actions and sourcing changes to largely mitigate the impacts of new tariffs and changes in existing tariff rates.

Outlook In the first quarter of fiscal 2026, we expect our net sales to be approximately $4.5 billion as compared to $3.8 billion in the first quarter of fiscal 2025. This increase reflects sales growth in both the Industrial Solutions and Transportation Solutions segments. The Industrial Solutions segment will benefit from the acquisition of Richards Manufacturing. We expect diluted earnings per share from continuing operations to be approximately $2.33 per share in the first quarter of fiscal 2026. This outlook reflects the positive impact of foreign currency exchange rates on net sales and earnings per share of approximately $113 million and $0.02 per share, respectively, in the first quarter of fiscal 2026 as compared to the same period of fiscal 2025 and includes the impact of currently enacted tariffs. Also, this outlook is based on foreign currency exchange rates and commodity prices that are consistent with current levels.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TEL_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
