你是 stock-analyst v20 DD 的證據採集子 agent。標的：MSI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - MSI Motorola Solutions tariff section 232 2026
  - Motorola Solutions export control OR entity list Mission Critical Communications 2026
  - MSI Motorola Solutions China tariff OR trade restriction 2026
  - Mission Critical Communications tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/68505/000006850526000010/msi-20251231.htm｜as_of：2026-02-12
<<<
We currently procure certain materials and components, inclusive of memory, from single-source vendors. A material disruption from a single-source vendor may have a material adverse impact on our results of operations. If certain single-source suppliers were to become capacity-constrained or insolvent, it could result in a reduction or interruption in supplies or an increase in the price of supplies and adversely impact our financial results. In addition, we import products, materials and components that are subject to import duties, and various trade actions affecting these imported products could have a negative impact on our results of operations. In 2025, the U.S. initiated a series of trade actions that imposed new tariffs and increased existing tariffs on goods imported from various countries, contributing to higher import duties applicable to us in 2025.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/68505/000006850526000010/msi-20251231.htm｜as_of：2026-02-12
<<<
Our ability to meet customers' demands depends, in part, on our ability to timely obtain an adequate delivery of quality materials, parts, and components, as well as software and services, from our suppliers. If demand for our products or services increases from our current expectations or if, as we have experienced in the past, suppliers are unable to meet our demand for other reasons, including as a result of supply chain constraints; natural disasters; trade policy decisions, such as new, expanded or retaliatory tariffs, sanctions, quotas, import/export restrictions or trade barriers (including restrictions around rare earth minerals); financial issues or other factors, we have, and could continue to experience an interruption in supply or a significant increase in the price of supply. Recently, we have experienced increased costs on materials and components as a result of the dynamic global supply chain environment. Mitigation actions that we develop going forward, such as working with our global supply base to mitigate our exposure to such risks, may not be successful in counteracting any such increased costs. We expect that any future supply chain effects could also impact our ability to meet customer demand and negatively impact our results of operations.

Because of these sizable sales and operations outside of the U.S., we have more complexity in our operations and are exposed to a unique set of global risks that could negatively impact our business, financial condition, results of operations, and cash flows, including but not limited to: (i) currency fluctuations, including but not limited to increased pressure to agree to established currency conversion rates and cost of living adjustments as a result of foreign currency fluctuations, (ii) import/export regulations, tariffs, trade barriers and trade disputes, customs classifications and certifications, including but not limited to changes in classifications or errors or omissions related to such classifications and certifications, (iii) compliance with and changes in U.S. and non-U.S. laws or regulations related to antitrust and competition (such as the EU Foreign Subsidies Regulation), anti-corruption (such as the Foreign Corrupt Practices Act and the U.K.…

Our business with or funded by the U.S. government is subject to specific laws and regulations with numerous and unique compliance requirements relating to formation, administration and performance of U.S. federal or federally funded contracts. These requirements, which may increase or change over time, may increase our performance and compliance costs thereby reducing our margins, which could have an adverse effect on our financial condition. Changes to these compliance requirements could result in our inability to renew or perform under certain contracts. Violations or other failures to comply with these laws, regulations or other compliance requirements could lead to terminations for default, suspension or debarment from U.S. government contracting or subcontracting for a period of time or other adverse actions. Such laws, regulations or other compliance requirements include those related to procurement integrity, export control, U.S. government security and information security regulations, supply chain and sourcing requirements and restrictions, employment practices, protection of criminal justice data, protection of the environment, accuracy of records, proper recording of costs, foreign corruption, Trade Agreements Act, Buy America Act, other domestic content requirements, and the False Claims Act.

In addition, global conflicts, as well as the results of elections or other political conditions such as government shutdowns, have created, and could create in the future, many economic and political uncertainties that impact worldwide markets, including impacts relating to trade policy decisions, such as new or increased tariffs or retaliatory measures imposed or proposed by governments and their trade partners, potential trade wars and related legal challenges or prolonged uncertainty in trade relationships, and threats to national security vulnerabilities linked to country of origin. The length of time these adverse economic and political conditions may persist is unknown.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/68505/000006850526000010/msi-20251231.htm｜as_of：2026-02-12
<<<
Recent Events Macroeconomic Environment Update The current global trade environment is complex and evolving. In 2025, the U.S. initiated a series of trade actions which imposed new tariffs and increased existing tariffs on goods imported from various countries, contributing to a global trade landscape subject to evolving tariffs, import/export regulations, including restrictions around rare earth minerals, trade barriers and trade disputes. We continue to monitor the impact of the current trade environment, including tariffs implemented under the International Emergency Economic Powers Act (IEEPA), for the impacts of policy volatility, pending judicial outcomes, and evolving geopolitical events that may impact our supply chain costs and operational efficiency. In addition, we are observing shifting dynamics in the memory market driven by substantial demand from the AI data center sector. As a result, we continue to observe elevated volatility and uncertainty around the global supply chain.

35 We engage with global suppliers across a diverse network of locations around the world. We continue to work with our global supply base to mitigate our exposure to the risks to global reciprocal (and sectoral) tariffs, navigate import/export regulations that have developed, and which may continue to develop, and mitigate our exposure to rising costs to facilitate continued supply at levels in order to meet our current customer demand. As a result of the dynamic global supply chain environment, we have experienced increased costs on materials and components, which we have substantially mitigated during 2025 and for which we expect to continue to develop mitigation actions going forward.

38 Gross Margin Years ended December 31 (In millions) 2025 2024 % Change Gross margin from Products and Systems Integration $ 3,915 $ 3,668 7 % Gross margin from Software and Services 2,120 1,844 15 % Gross margin $ 6,035 $ 5,512 9 % Gross margin was 51.7% of net sales in 2025 compared to 51.0% of net sales in 2024. The primary drivers of this increase in gross margin as a percentage of net sales were: •a 1.0% increase in gross margin as a percentage of net sales in the Software and Services segment, inclusive of acquisitions, primarily driven by higher sales and expanded margins, including favorable mix; and •a 0.7% increase in gross margin as a percentage of net sales in the Products and Systems Integration segment, inclusive of acquisitions, primarily driven by higher sales and lower direct material costs, despite higher tariffs.

Operating Earnings Years ended December 31 (In millions) 2025 2024 Operating earnings from Products and Systems Integration $ 1,761 $ 1,676 Operating earnings from Software and Services 1,227 1,012 Operating earnings $ 2,988 $ 2,688 Operating earnings increased $300 million, or 11% in 2025 compared to 2024. The increase in operating earnings was due to: •a $215 million increase in the Software and Services segment from 2024 to 2025, primarily driven by higher sales, expanded margins, including favorable mix, improved operating leverage and lower expenses related to legal matters, partially offset by higher expenses associated with acquired businesses and higher employee incentive costs, including share-based compensation; and •a $85 million increase in the Products and Systems Integration segment from 2024 to 2025, primarily driven by higher sales, a gain on the Hytera litigation (for further information regarding the Hytera litigation, refer to “Hytera Civil Litigation” within "Note 12: Commitments and Contingencies" in "Part II. Item 8. Financial Statements and Supplementary Data" of this Form 10-K), improved gross margins driven by lower direct material costs, despite higher tariffs, partially offset by higher employee incentive costs, including share-based compensation and investments in video, an increase in intangible amortization expense, an increase in acquisition related transaction fees, primarily related to the Silvus acquisition, and higher expenses associated with acquired businesses.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
