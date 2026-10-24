你是 stock-analyst v20 DD 的證據採集子 agent。標的：TSLA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - TSLA tariff section 232 2026
  - export control OR entity list 2026
  - TSLA China tariff OR trade restriction 2026
  - tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm｜as_of：2026-01-29
<<<
Internationally, we also have manufacturing facilities in China and Germany, which allows us to increase the affordability of our vehicles for customers in local markets by reducing transportation and manufacturing costs and limiting the impact of unfavorable tariffs. Generally, we continue to expand production capacity at our existing facilities, and strive to increase cost-competitiveness in our significant markets by strategically adding local manufacturing, including through partnerships with suppliers.

In Europe and other countries that follow the regulations of the United Nations Economic Commission for Europe (“ECE countries”), some requirements restrict the design of both advanced driver-assistance and autonomous systems, which can compromise or prevent their use entirely. On a European Union level, additional layers of regulatory frameworks may impose further obligations in areas such as risk management, data-governance, trainings, technical documentation. Meanwhile, on a national level, the enforcement of certain applicable regulations may vary. Proposed national laws may further hinder or complicate the path of both advanced driver-assistance and autonomous vehicle systems, including the timeline for introducing autonomous vehicles for sale and use in ECE countries. Additionally, certain national and city laws within each ECE country may impose legal restrictions on the marketing of advanced driver-assistance and autonomous vehicle systems, and may vary significantly on commercial ride-hailing with a fleet of autonomous vehicles, in areas such as licenses, permits, competition prohibitions, tariffs and other transport services obligations. When coupled together, the layers of regulation as well as the fragmentation across each ECE country may hinder or complicate the path and timeline to introducing autonomous vehicles and an autonomous vehicle ride-hailing business in them.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm｜as_of：2026-01-29
<<<
Our products contain thousands of parts purchased globally from hundreds of suppliers, including single-source direct suppliers, which exposes us to multiple potential sources of component shortages. Unexpected changes in business conditions, materials pricing, including inflation of raw material costs, labor issues, wars, trade policies, natural disasters, health epidemics, trade and shipping disruptions, port congestions, cyberattacks and other factors beyond our or our suppliers’ control could also affect these suppliers’ ability to deliver technologies or components to us or to remain solvent and operational. U.S. trade policy alterations in 2025, including heightened import tariffs and subsequent retaliatory measures, have impacted our supply chain costs, and may impact the availability of certain technologies or components, depending on the exact scope of the tariffs ultimately implemented and retaliatory export controls. Additionally, if our suppliers do not accurately forecast and effectively allocate production or if they are not willing to allocate sufficient production to us, or face other challenges such as insolvency, it may reduce our access to components and require us to search for new suppliers.…

We are subject to legal and regulatory requirements, political uncertainty and social, environmental and economic conditions in numerous jurisdictions, including markets in which we generate significant sales. We have little control over these matters which are inherently unpredictable. Our operations in such jurisdictions, particularly as a company based in the U.S., with additional manufacturing operations in China and Europe, create risks relating to conforming our products to regulatory and safety requirements and charging and other electric infrastructures; organizing local operating entities; establishing, staffing and managing foreign business locations; attracting local customers; navigating U.S. and foreign government taxes, regulations and permit requirements; enforceability of our contractual rights; trade restrictions, customs regulations, tariffs and price or exchange controls; and preferences in foreign nations for domestically manufactured products. For example, we monitor tax legislation changes on a global basis, including changes arising as a result of the Organization for Economic Cooperation and Development’s multi-jurisdictional plan of action to address base erosion and profit shifting. Further, the United States has recently announced changes to U.S. trade policy, including increasing tariffs on imports, in many cases significantly, and potentially renegotiating or terminating existing trade agreements.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm｜as_of：2026-01-29
<<<
As a result of rapidly evolving trade and fiscal policy, uncertainty in the automotive and energy markets continues, posing risks to our global supply chain and cost structure which could have a meaningfully adverse impact on demand for our products and our profitability. The current tariff regime will have a relatively larger impact on our energy generation and storage business compared to our automotive business. While we prepare for near-term challenges to our business under current policies, we are focused on long-term growth opportunities as we continue to make prudent investments.

These plans are subject to uncertainties inherent in establishing and ramping manufacturing operations, which may be exacerbated by new product and manufacturing technologies we introduce, the number of concurrent international projects, any industry-wide component constraints, labor shortages and any future impact from events outside of our control. For example, changes to fiscal and trade policy with respect to tariffs, export controls and other restrictions may impact our global supply chain cost structure and availability, affecting not only vehicle production, but also facility expansions. Moreover, we have set ambitious technological targets with our plans for battery cells as well as for iterative manufacturing and design improvements for our vehicles.

Changes in government and economic policies, incentives or tariffs may also impact our production, cost structure and the competitive landscape. For instance, while the final scope and application of recently announced changes in trade policy remain uncertain at this time, higher tariffs on imports and subsequent retaliatory tariffs could adversely impact consumer spending and demand for durable goods and related services. Furthermore, certain provisions of the OBBBA, including the removal of tax credits for electric vehicles, may also impact consumer demand for electric vehicles in general. We will continue to adjust accordingly to such developments, and we believe our ongoing cost reduction efforts, including through production innovation, process improvements and logistics optimization, and focus on operating leverage, vertical integration and supply chain localization will continue to benefit us in relation to our competitors. Our new products and our advances in autonomy and robotics, position us for future growth.

Energy Generation and Storage Demand, Production and Deployment The long-term success of this business is dependent upon incremental volume growth. We continue to increase the production and capabilities of our energy storage products to meet high levels of demand, including the ramps of our Megafactories in Shanghai and Lathrop, California, and the construction of a new Megafactory near Houston, Texas. In 2025, we introduced Megapack 3 and Megablock, our next-generation industrial storage product, and began manufacturing a new residential retrofit solar panel. For Megapack, energy storage deployments can vary meaningfully quarter to quarter depending on the timing of specific project milestones and logistics. As these product lines grow, we will have to maintain adequate battery cell supply for our energy storage products. At the same time, changes in government and economic incentives or tariffs may also impact our sales, cost structure and the competitive landscape. For instance, import tariffs by the US government and the provisions of the OBBBA could significantly increase battery cell expenses and impact costs for our consumers, negatively impacting consumer demand. Despite these challenges, as AI infrastructure drives rapid load growth, we see opportunities for our energy storage products to stabilize the grid, shift energy when it is needed most and provide additional power capacity.

Cost of Revenues and Gross Margin Year Ended December 31, 2025 vs. 2024 Change 2024 vs. 2023 Change (Dollars in millions) 2025 2024 2023 $ % $ % Cost of revenues Automotive sales $ 56,267 $ 61,870 $ 65,121 $ (5,603) (9) % $ (3,251) (5) % Automotive leasing 898 1,003 1,268 (105) (10) % (265) (21) % Total automotive cost of revenues 57,165 62,873 66,389 (5,708) (9) % (3,516) (5) % Services and other 11,599 9,921 7,830 1,678 17 % 2,091 27 % Total automotive & services and other segment cost of revenues 68,764 72,794 74,219 (4,030) (6) % (1,425) (2) % Energy generation and storage segment 8,969 7,446 4,894 1,523 20 % 2,552 52 % Total cost of revenues $ 77,733 $ 80,240 $ 79,113 $ (2,507) (3) % $ 1,127 1 % Gross profit total automotive $ 12,361 $ 14,197 $ 16,030 Gross margin total automotive 17.8 % 18.4 % 19.4 % Gross profit total automotive & services and other segment $ 13,292 $ 14,810 $ 16,519 Gross margin total automotive & services and other segment 16.2 % 16.9 % 18.2 % Gross profit energy generation and storage segment $ 3,802 $ 2,640 $ 1,141 Gross margin energy generation and storage segment 29.8 % 26.2 % 18.9 % Total gross profit $ 17,094 $ 17,450 $ 17,660 Total gross margin 18.0 % 17.9 % 18.2 % Automotive & Services and Other Segment Cost of automotive sales revenue includes direct and indirect materials, labor costs, manufacturing overhead, including depreciation costs of tooling and machinery, shipping and logistic costs, tariffs, reserves for estimated warranty expenses, FSD (Supervised) ongoing maintenance costs, vehicle connectivity costs, and allocations…

2025 compared to 2024 Cost of automotive sales revenue decreased $5.60 billion, or 9%, in the year ended December 31, 2025 as compared to the year ended December 31, 2024 due to the decrease in deliveries year over year as discussed above and lower average cost per unit due to sales mix and lower material costs, partially offset by lower fixed cost absorption and an increase in tariffs compared to the prior year.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
