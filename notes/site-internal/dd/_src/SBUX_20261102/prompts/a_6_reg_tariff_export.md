你是 stock-analyst v20 DD 的證據採集子 agent。標的：SBUX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - SBUX Starbucks tariff section 232 2026
  - Starbucks export control OR entity list Restaurants 2026
  - SBUX Starbucks China tariff OR trade restriction 2026
  - Restaurants tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
The price of coffee is subject to volatility and has steadily increased over the past five years with significant increases over the last two years. Although most coffee trades in the commodity market, high-altitude arabica coffee of the quality sought by Starbucks tends to trade on a negotiated basis at a premium above the “C” coffee commodity price. Both the premium and the commodity price depend upon the supply and demand at the time of purchase. Supply and price can be affected by multiple factors in the producing countries, including weather and extreme weather events, water supply quality and availability throughout the coffee production chain, natural disasters, crop disease and pests, general increases in farm inputs and costs of production, inventory levels, and political and economic conditions. Climate change may further exacerbate many of these factors. Price is also impacted by geopolitical conditions, including new and existing tariffs on coffee imports and other trade controls, and by trading activities in the arabica coffee futures market, including hedge funds and commodity index funds. In addition, green coffee prices have been affected in the past, and may be affected in the future, by the actions of certain organizations and associations that have historically attempted to influence prices of green coffee through agreements establishing export quotas or by restricting coffee supplies.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
Operating in 89 global markets, we face diverse cultural, regulatory, geopolitical, and economic environments. Our success depends on navigating these differences effectively and leveraging operational strengths across markets. However, planned initiatives may not resonate uniformly with customers and could lead to unexpected shifts in perception or market share. Our international operations are also subject to additional inherent risks of conducting business abroad, such as: •Uncertainty in economic, legal, regulatory, social, and political conditions, including rising anti-American sentiment in certain markets; •Governmental trade and investment restrictions, such as tariffs, export duties, ownership limits, and favoritism toward local competitors; •Economic or trade sanctions limiting product sourcing or business operations; •Delays in store openings due to external factors, competition, or limited access to affordable real estate, potentially impacting financial performance; •Operational and supply chain challenges abroad, including staffing, logistics, product consistency, and cultural or language barriers; •Slower-than-expected growth in disposable income in developing economies; •Complex and varying interpretations of laws and regulations, including those related to taxes, labor, privacy, and responsible business matters; •Local employment laws increasing the cost and complexity of hiring and termination; •Labor disruptions due to geopolitical instability or social unrest; •Health and safety regulations affecting store operations; •Challenges in enforcing intellectual property and contract rights; •Foreign currency fluctuations and restrictions on currency use or fund repatriation; and •Licensing and…

Coffee supply and pricing are influenced by factors in producing countries, including weather and extreme weather events, water availability, natural disasters, crop disease, input costs, inventory levels, political and economic conditions, and actions by organizations seeking to influence global prices. Climate change may intensify these risks—for example, droughts or frosts in Brazil have in the past driven price increases. Speculative trading also contributes to volatility. Tariffs have also affected, and in the future may affect, our costs to procure coffee. Given coffee’s central role in our operations and our limited ability to fully hedge against price increases, rising costs or supply shortages could materially impact our profitability and ability to meet customer demand. We supply strategic products, including coffee, to our licensees, and we may have limited ability to pass along increased costs.

We also rely on significant quantities of dairy products and plant-based alternatives, such as oat and almond milk, as well as other commodities including tea, cocoa, produce, meats, eggs, energy, and packaging materials. Price increases or supply disruptions—whether due to shortages, processing delays, tariffs, or other factors—could materially affect our profitability, particularly in international markets.

We are subject to risks from changes to the trade policies and tariff and import/export regulations by the U.S. and other foreign governments.

Changes in the import and export policies, including trade restrictions such as new, increased, threatened, or retaliatory tariffs or quotas, embargoes, sanctions and countersanctions, safeguards, or customs restrictions by the U.S. and foreign governments, have in the past required, and could in the future require, us to change the way we conduct business and such changes have in the past adversely affected, and could in the future adversely affect, our financial condition, results of operations, reputation, and our relationships with customers, suppliers, and employees in the short- or long-term. It may be time-consuming and expensive for us to alter our business operations to adapt to or comply with any such changes. Likewise, changes in laws and 15 Table of Contents policies governing foreign trade, manufacturing, development, and investment in the territories or countries where we currently sell our products or conduct our business could adversely affect our business.

Our operating results have been, and will continue to be, subject to a number of other macroeconomic and other factors, many of which are largely outside our control. Any one or more of the factors listed below could have a material adverse impact on our business, financial condition, or results of operations: •Rising real estate costs in certain domestic and international markets; •Supply chain disruptions; •Climate change and extreme weather affecting input costs and availability; •Changes in tax laws and government regulations, such as the One Big Beautiful Bill Act, enacted in the U.S. in July 2025; •Adverse litigation outcomes; •Inflation and interest rate fluctuations; •Natural or man-made disasters disrupting major markets; •Government shutdowns and election-related impacts globally, including regime change and political and civil unrest; •Terminations of, or changes in, existing trade agreements among the countries in which we operate; •Tariffs imposed on commodities or goods, including recent tariffs imposed or threatened to be imposed by the U.S. on other countries, and any retaliation measures taken by such countries; •Labor unrest, geopolitical instability, terrorism, anti-American sentiment, or public health crises—especially in key markets; and •Foreign currency exchange rate volatility.

Environmental regulations are evolving, with new or expanded rules targeting carbon emissions, plastic use, and commercial water consumption. These changes may lead to higher compliance costs, capital expenditures, and other financial obligations for us and our partners, potentially affecting profitability. Additional emerging regulations, such as import tariffs tied to alleged human rights violations, may also impact operations. Certain jurisdictions have enacted or proposed taxes or other restrictions on the manufacture, distribution, or sale of certain of our products, particularly beverages containing caloric sweeteners. These taxes and other measures vary in structure and may apply broadly or selectively. Additionally, environmentally focused taxes or other measures, such as plastic packaging levies or extended producer responsibility laws, are gaining traction. These measures can adversely affect our financial performance by raising product costs, reducing consumption, or generating negative publicity.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
We expect that the macroeconomic challenges we have been experiencing, including impacts from new tariffs and dynamic coffee prices, will continue; however, we are encouraged by the results we have seen from our “Back to Starbucks” initiatives. Following our Green Apron Service model going live across our full U.S company-operated store portfolio in the fourth quarter of fiscal 2025, we are focused on empowering coffeehouse leaders to take ownership of sustaining the model as our permanent way of working, which we expect to enhance the customer experience and drive future transaction growth. Further, as announced in early November 2025, we look forward to working with our new strategic joint venture partner, Boyu Capital, to accelerate long-term growth in China. We believe, through strategic prioritization, that we are taking the right actions now and in the future, specifically through our investments in store partners, uplifting the coffeehouse experience through disciplined capital deployment, introducing new food and beverage platforms, reimagining the Starbucks rewards program, and enhancing support for our licensee partners. These actions, while driving more efficiency, accountability, and agility as a company, will lay the foundation for the future of Starbucks.

37 Table of Contents COMMODITY PRICES, AVAILABILITY, AND GENERAL RISK CONDITIONS Commodity price risk represents our primary market risk, generated by our purchases of green coffee and dairy products, among other items. We purchase, roast, and sell high-quality arabica coffee and related products, and risk arises from the price volatility of green coffee. In addition to coffee, we also purchase significant amounts of dairy products to support the needs of our company-operated stores. The price and availability of these commodities, including impacts from volatility in green coffee prices and new tariffs, directly impact our results of operations, and we expect commodity prices, particularly coffee, to continue to impact future results of operations. For additional details see Product Supply in Item 1 of Part I of this 10-K, as well as Risk Factors in Item 1A of Part I of this 10-K.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
