你是 stock-analyst v20 DD 的證據採集子 agent。標的：MOD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Modine Manufacturing product substitute technology threat 2026
  - Building Products & Equipment alternative technology disruption 2026 2027
  - MOD Modine Manufacturing technology obsolescence risk
  - Building Products & Equipment next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
Heat exchanger coils, primarily of round tube plate fin construction, are primarily sold to the HVAC&R and data center cooling markets in North America, Europe, and Asia. Customers include commercial and industrial equipment manufacturers, distributors, contractors, and end users in a variety of commercial and industrial applications, including data center management, commercial and residential HVAC, mobile air conditioning, refrigeration, and precision and industrial cooling. In fiscal 2026, the HVAC&R markets experienced moderate growth, recovering from market declines in fiscal 2025. The data center markets experienced exceptionally strong growth in fiscal 2026 and we expect strong growth during fiscal 2027, supported by the sustained global reliance on digital technologies. We expect the commercial and residential markets that we serve will be relatively flat during fiscal 2027. Trends influencing our primary HVAC&R markets include refrigerant substitution and energy efficiency requirements, both of which are expected to benefit the commercial HVAC&R markets. Demand for more efficient HVAC&R systems is driven by more stringent energy efficiency regulations.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
We operate in numerous countries on four continents and serve customers in a wide array of commercial, industrial, HVAC&R, and vehicular markets. As such, our business is impacted by general economic, political, and industry conditions globally as well as in the regions and countries in which we conduct business. We are subject to the risk of disruptions or significant deterioration in market conditions, which could have a material impact on our business, financial position, results of operations and cash flows. Geopolitical tensions and military conflicts, including the conflict between the U.S. and Iran, as well as related regional instability or proxy conflicts, could negatively impact or cause significant business disruptions in the global markets we operate in. Ongoing conflicts and any potential further escalation, could lead to significant disruption near major oil producing regions or in shipping corridors and could result in higher energy and fuel prices, shipping delays, increased freight and manufacturing costs, and increased cyberattacks from state-sponsored or other actors. Such developments could also contribute to broader inflationary pressures across the global economy and supply chains, including increased costs for materials, transportation and labor, which may not be fully recoverable through pricing and could impact the availability, reliability, and overall viability of certain supply sources.

In addition, customer demand for our products and system solutions is impacted by the overall strength of the economy, employment levels, consumer confidence levels, the availability and cost of credit, and the cost of fuel. For example, rising interest rates associated with inflationary market conditions may drive a higher cost of capital for our customers, which may have a deteriorating impact on overall economic activity and the financial condition of our customers, which could negatively impact the demand for our products. Prolonged recessionary or adverse economic conditions, such as disruptions in the global financial system, could result in our customers or suppliers experiencing significant economic constraints, including potential bankruptcies.

An outbreak of a disease or public health threat could create economic and financial disruptions and adversely affect our businesses around the world. Potential impacts of epidemics, pandemics, or other health crises include, but are not limited to, (i) staffing shortages if portions of our workforce are unable to work effectively due to illness, quarantines, government actions, facility closures, or other restrictions; (ii) short- or long-term disruptions in our supply chain and our ability to deliver products to our customers; (iii) deterioration in the markets that we or our customers operate in, which may result in lower sales or a deterioration in the ability of our customers to pay us; and (iv) significant volatility or negative pressure in the financial markets, which could adversely affect our access to capital and/or financing and could have a material impact on our business, financial position, results of operations and cash flows.

Climate changes, such as extreme weather conditions, also create financial risk and uncertainty for our business. Demand for our products and services may be affected by unpredictable or unseasonable weather conditions. Climate changes could also disrupt our operations by impacting the availability and cost of materials and resources needed for manufacturing and could increase our insurance and other operating costs. In addition, natural disasters or extreme weather events, including those as a result of climate changes, could disrupt our manufacturing operations and our ability to manufacture and deliver products to our customers and adversely impact our results of operations and cash flows.

17 Table of Contents In addition, the U.S. Foreign Corrupt Practices Act, the U.K. Bribery Act and other similar anti-corruption laws generally prohibit companies and their intermediaries from making payments to improperly influence foreign government officials or other persons for the purpose of obtaining or retaining business. In recent years, there has been a substantial increase in the global enforcement of anti-corruption laws. In the event that we believe our employees or agents may have violated applicable anti-corruption laws, or if we are subject to allegations of any such violations, we may have to expend significant time and financial resources toward the investigation and remediation of the matter, which could disrupt our business and result in a material adverse impact on our results of operations, cash flows and reputation.

Information technology (“IT”) systems We may be adversely affected by a substantial disruption in, or material breach of, our IT systems or IT systems of our service providers.

We are dependent upon IT infrastructure, including network, hardware, and software systems owned by us and our service providers, to conduct our business. Despite network and other cybersecurity measures we and our service providers have in place, IT systems could be damaged, compromised, or interrupted by intentional or unintentional events or natural disasters. We could also be negatively impacted by a cybersecurity breach from malware, ransomware, phishing, unauthorized access or similar disruptions. Cybersecurity risk may be heightened by the increased prevalence of hybrid and/or remote work arrangements, mergers, acquisitions and dispositions, rapid business growth activities, and reliance on third-party service providers. Further, the military conflicts in the Middle East and Ukraine, as well as current geopolitical uncertainties involving Russia, Iran and China, among other nations, may increase the threat of cyberattacks on the global financial markets, supply chain, and IT infrastructure, which could directly or indirectly have an adverse impact on our results of operations and cash flows.

A material breach or a substantial disruption in our IT systems for a prolonged time period, or the failure of one or more legacy IT systems no longer supported by service providers, could result in delays in receiving inventory and supplies or filling customer orders. Further, we continue to expand our IT systems to enable our businesses to run more efficiently, including the incorporation of artificial intelligence in certain areas. The increased use of and evolution in advanced technology solutions creates potential risks. A material breach in our IT systems or the improper use of artificial intelligence could result in the release of otherwise confidential information, including personal information that is protected by the General Data Protection Regulation. Any such events and the related delays, problems or costs, including potentially significant remediation expenses and litigation risks, could have material adverse impacts on our business, financial condition, results of operations, business relationships and reputation.

We are highly susceptible to unfavorable trends or disruptions in the markets we serve, as our customers’ financial condition and performance are affected by demand for their goods or services, regulatory initiatives and incentives and general economic conditions, including supply chain challenges, access to credit, the price of fuel and electricity, employment levels and trends, interest rates, labor relations issues, regulatory requirements and incentives, technology demands and advancements, government-imposed restrictions relating to health crises or other events, trade agreements and other market factors, as well as by customer-specific issues. Any significant decline in demand for our products and solutions, including those driven by end-market demands or demand for our customer’s products or services, by current and future customers could result in asset impairment charges and a reduction in our sales, thereby adversely impacting our results of operations, cash flows and financial condition.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
