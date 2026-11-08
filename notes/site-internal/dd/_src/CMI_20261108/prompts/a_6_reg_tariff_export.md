你是 stock-analyst v20 DD 的證據採集子 agent。標的：CMI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - CMI Cummins tariff section 232 2026
  - Cummins export control OR entity list Specialty Industrial Machinery 2026
  - CMI Cummins China tariff OR trade restriction 2026
  - Specialty Industrial Machinery tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
We operate our business on a global basis and changes in tariffs and other trade disruptions could adversely impact the demand for our products and our competitive position.

We manufacture, sell and service products globally and rely upon a global supply chain to deliver the raw materials, components, systems and parts that we need to manufacture and service our products. There is currently significant uncertainty about the future relationship between the U.S. and various other countries with respect to tariffs and other trade disruptions (such as embargoes, sanctions and export controls). The uncertain tariff environment, marked by the U.S. imposition of tariffs on certain countries, followed by the imposition of retaliatory tariffs on U.S. goods and services by certain countries has introduced significant market volatility and raised concerns about potential economic impacts. The extent to which tariffs and/or other trade disruptions will be enacted and the duration for which enacted tariffs and/or other trade disruptions will be in place remain uncertain and could adversely impact our production costs, customer demand and our relationships with customers and suppliers. Any of these consequences could have a material adverse effect on our results of operations, financial condition and cash flows.…

We manufacture, sell and service products globally and rely upon a global supply chain to deliver the raw materials, components, systems and parts that we need to manufacture and service our products. Changes in laws, regulations and government policies on foreign trade and investment can affect the demand for our products and services, cause non-U.S. customers to shift preferences toward domestically manufactured or branded products and impact the competitive position of our products or prevent us from being able to sell products in certain countries. Our business benefits from international trade agreements, such as the United States-Mexico-Canada Agreement and the U.S. trade relationships including those with China, Brazil, E.U. and the U.K. More restrictive trade policies, such as efforts to withdraw from or substantially modify such agreements or arrangements, including, without limitation, higher tariffs or new barriers to entry could adversely impact our production costs, customer demand and our relationships with customers and suppliers. Any of these consequences could have a material adverse effect on our results of operations, financial condition and cash flows.

Embargoes, sanctions and export controls imposed by the U.S. and other governments restricting or prohibiting transactions with certain persons or entities, including financial institutions, to certain countries or regions, or involving certain products, could limit the sales of our products. Embargoes, sanctions and export control laws are changing rapidly for certain geographies, including with respect to China. In particular, changing U.S. export controls and sanctions on China, as well as other restrictions affecting transactions involving China and Chinese parties, could affect our ability to collect receivables, access cash generated in China, provide aftermarket and warranty support for our products, sell products and otherwise impact our reputation and business, any of which could have a material adverse effect on our results of operations, financial condition and cash flows.

We continue to experience pockets of supply chain disruptions and related challenges throughout the supply chain which are further impacted by the current global tariff environment. We single source a number of parts and raw materials critical to our business operations. Any delay in our suppliers' deliveries may adversely affect our operations at multiple manufacturing locations, forcing us to seek alternative supply sources to avoid serious disruptions. Delays may be caused by factors affecting our suppliers (including, but not limited to, raw material availability, capacity constraints, port congestion, labor disputes or unrest, shortages of labor, economic downturns, availability of credit, impaired financial condition, sanctions/tariffs, restrictions on the sale or distribution of critical rare earth metals, energy inflation/availability, suppliers' allocations to other purchasers, weather emergencies, natural disasters, acts of government or acts of war or terrorism). The effects of climate change, including extreme weather events, long-term changes in temperature levels and water availability may exacerbate these risks. Any extended delay in receiving critical supplies could impair our ability to deliver products to our customers and have a material adverse effect on our results of operations, financial condition and cash flows.

In addition, there continues to be significant uncertainty about the future relationships between the U.S. and China, including with respect to trade policies, treaties, government regulations and tariffs. Any increased trade barriers or restrictions on global trade, especially trade with China, could adversely impact our competitive position, results of operations, financial condition and cash flows.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
Uncertain Global Trade Environment We operate our business on a global basis and changes in international, national and regional trade laws, regulations and policies affecting and/or restricting international trade, including higher tariffs, trade disruptions (such as embargoes, sanctions and export controls) and broader geopolitical tensions, could adversely impact the demand for our products and our competitive position. The uncertain global trade environment, marked by the U.S. imposition of tariffs on certain countries, followed by the imposition of retaliatory tariffs and other actions against U.S. goods and services by certain countries has introduced significant market volatility and raised concerns about potential economic impacts. Our primary risks include reduced global movement of goods impacting freight activity, increased costs for suppliers and end-users and uncertainty around the availability of supply, all of which could contribute to a decline in business confidence, a reduction in demand for our products and increased product costs. We have and continue to look for ways to mitigate these costs including discussions with our suppliers, sourcing alternatives and agreements with our customers to recover these costs. The financial impact of tariffs, net of mitigation actions, was immaterial to our profitability and operating cash flows during 2025.…

Years ended December 31, 2025 vs. 2024 2024 vs. 2023 In millions 2025 2024 2023 Amount Percent Amount Percent United States and Canada $ 20,165 $ 20,820 $ 20,650 $ (655) (3) % $ 170 1 % International 13,505 13,282 13,415 223 2 % (133) (1) % Total net sales $ 33,670 $ 34,102 $ 34,065 $ (432) (1) % $ 37 — % Worldwide revenues decreased by 1 percent in 2025 compared to 2024, mainly due to weaker demand in on-highway commercial truck markets and the divestiture of Atmus in the first quarter of 2024, partially offset by higher demand in power generation markets, especially data center and commercial markets, non-tariff pricing mainly related to the launch of updated engine products in light-duty automotive markets and customer tariff recoveries. Net sales in the U.S. and Canada declined by 3 percent mainly due to lower demand in heavy-duty and medium-duty truck markets and the divestiture of Atmus, partially offset by higher sales in power generation markets and non-tariff pricing mainly related to the launch of updated engine products in light-duty automotive markets. International sales (excludes the U.S. and Canada) improved by 2 percent, primarily due to higher sales in China and Europe, partially offset by lower sales in Latin America.…

Gross Margin Gross margin increased $77 million and increased 0.6 points as a percentage of sales. The increases were mainly due to strong growth in power generation markets, especially data center and commercial markets, as well as favorable non-tariff related pricing mainly due to the launch of updated engine products in light-duty automotive markets, partially offset by lower demand in on-highway commercial truck markets and the absence of Atmus sales. The net impact of tariff costs and related recoveries was immaterial for the year ended December 31, 2025. The provision for base warranties issued as a percentage of sales was 1.9 percent in 2025 and 1.9 percent in 2024.

Tariff related costs and recoveries in 2025 were evaluated independently of all other drivers included in the disclosures below and all references to "price" and "material cost" variances exclude these separately evaluated tariff costs and recoveries. The net impact of tariff costs and related recoveries were immaterial to each reportable segment's EBITDA, unless specifically noted.

These decreases were partially offset by the following increases: •Light-duty automotive sales increased $335 million primarily due to non-tariff pricing mainly related to the launch of updated engine products.

Segment EBITDA Power Systems segment EBITDA increased $514 million, primarily due to favorable pricing and higher volumes, partially offset by net tariff costs.

46 Table of Contents OUTLOOK The uncertain global trade environment, characterized by tariffs, export controls and broader geopolitical tensions, has created significant market volatility while introducing uncertainty around future demand for capital goods as well as potential impacts to our supply chain and our related product costs. Given the breadth, severity and uncertain duration of these global trade measures, our outlook presented below could be negatively impacted by policy-driven volatility. We are proactively taking steps in our supply chain to mitigate impacts where possible and we are working with our customers to pass through incremental costs.

•Increases in costs, tariffs, as well as other inflationary pressures, could negatively impact earnings.

•The potential for trade disruption, including embargoes, sanctions and export controls, could cause production disruptions and negatively impact earnings.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
