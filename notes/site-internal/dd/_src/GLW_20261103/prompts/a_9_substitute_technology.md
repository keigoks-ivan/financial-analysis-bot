你是 stock-analyst v20 DD 的證據採集子 agent。標的：GLW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Corning product substitute technology threat 2026
  - Electronic Components alternative technology disruption 2026 2027
  - GLW Corning technology obsolescence risk
  - Electronic Components next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm｜as_of：2026-02-12
<<<
Risks Related to Our Business Inflationary price pressures and uncertain availability of commodities, raw materials, utilities, labor or other inputs used by us and our suppliers, or instability in logistics and related costs, among other factors, could negatively impact our profitability Increases in the price of commodities, raw materials, utilities, labor or other inputs that we or our suppliers use in manufacturing and supplying products, components and parts, along with logistics and other related costs, may lead to higher production and shipping costs for our products, parts and components. Further, increasing global demand for, and uncertain supply of, such materials could disrupt our or our suppliers’ ability to obtain such materials in a timely manner to meet our supply needs and/or could lead to increased costs. Any increase in the cost of inputs to our production could lead to higher costs for our products and could negatively impact our operating results, future profitability and ability to successfully deliver on our strategy. Increasing our prices to our customers may cause certain of our customers to push out, cancel or refrain from purchasing our products, which could materially adversely impact demand for our products, and thereby also negatively impact our operating results, future profitability and ability to successfully deliver on our strategy.

Factors such as supply chain disruptions, manufacturing interruptions or delays, or the failure to accurately forecast customer demand, could affect our ability to meet customer demand, lead to higher costs, or result in excess or obsolete inventory; if we are unable to obtain the necessary equipment, raw and batch materials, natural resources, utilities and other essentials required in our products or processes, our business will be negatively impacted Corning’s business relies on the timely supply of raw materials, precious metals, natural resources or utilities including energy and industrial water, equipment, parts and components, services and related products to meet the changing technical and volume requirements of its customers, which depends in part on the timely delivery of materials, equipment and services, from suppliers and contract manufacturers. Significant or sudden increases in demand for such materials, equipment and services, as well as delays in and unpredictability of shipments due to transportation interruptions, have resulted in, and may continue to result in, a shortage of materials, equipment and services needed to manufacture Corning’s products. Such shortages have adversely impacted, and may continue to adversely impact, our suppliers’ ability to meet our demand requirements and Corning’s manufacturing operations and its ability to meet customer demand.…

12 Table of Contents Health crisis events, such as epidemics or pandemics, have adversely impacted, and may continue to impact, the economy and disrupt our operations and supply chains, which may have an adverse effect on our results of operations Health crisis events, including epidemics or pandemics, such as COVID-19, have impacted and may further impact the economy and could have additional impacts on economic growth, supply chains, the proper functioning of financial and capital markets, foreign currency exchange rates and interest rates. A pandemic may result in authorities around the world implementing numerous unprecedented measures such as travel restrictions, quarantines, shelter in place orders, vaccine mandates and facility shutdowns. These measures have impacted our workforce, operations and supply chains, and those of our customers, contract manufacturers and suppliers, and may continue to have an impact particularly in the event of another significant global health crisis. There is considerable uncertainty regarding the duration, scope and severity of a health crisis event and the impacts on our business and the economy from the effects of such an event and response measures.

The following table details the number of combined customers of our reportable segments that accounted for a large percentage of segment net sales, not adjusted for constant-currency: Number of combined end customers % of total segment net sales in 2025 Optical Communications 2 28 % Display 3 59 % Specialty Materials 2 43 % Automotive 3 61 % Life Sciences 2 45 % 13 Table of Contents Events outside of Corning’s control, or those of our contract manufacturers, could cause a disruption to our manufacturing operations and our ability to serve our customers, resulting in a negative impact to Corning’s net sales, net income, asset values and liquidity Disruption to our manufacturing operations, or those of our contract manufacturers, could significantly impact Corning’s ability to supply its customers and could produce a near-term severe impact on our individual business units and the Company. Given the geographical concentration of certain of the Company’s and our contract manufacturers’ plants in Asia Pacific, the highly engineered nature of the facilities and the globally dispersed talent required to run these facilities, any event that adversely affects or restricts movement into or out of a specific geographic area where we, our contract manufacturers, suppliers, or customers have a presence, could adversely impact our results.…

Information technology dependency and cybersecurity vulnerabilities could lead to reduced revenue, liability claims, competitive or reputational harm, and result in material adverse effects on our operations and financial results The Company is dependent on information technology systems and infrastructure (“IT systems”) owned and operated by the Company or managed by third-party service providers, suppliers and contract manufacturers. IT systems enable us to conduct, monitor and/or protect our business, operations, systems, data and other assets. In the ordinary course of our business, we and our providers collect, process, transmit and store sensitive data, including intellectual property, our proprietary information and that of our customers, suppliers and business partners, as well as personally identifiable information. Intrusion into a supplier or contract manufacturer system not integrated with a Corning IT system could result in service disruption and/or loss of financial control.

Our IT systems, and those of our providers, may be vulnerable to compromise or disruption due to human error or malfeasance, outdated applications, computer viruses or malware (e.g., ransomware), natural disasters, unauthorized access, cyber-attacks and other similar incidents and disruptions. Inadequate account security or organizational security practices may also result in unauthorized access. Increased work-from-home, at both the Company and our providers, presents additional operational risk. Companies that provide utilities, water, transportation, natural gas and other resources and services across our supply chain, are critical to our manufacturing operations and are vulnerable to cyber-attacks. From time to time, both we and certain of our providers, have been subject to cyberattacks and security incidents. Our security processes and initiatives may not be capable of anticipating, detecting, preventing or remediating all attacks, particularly as attackers are becoming more sophisticated in their ability to circumvent controls and remove forensic evidence. The rapid development and increasing adoption of emerging technologies, such as artificial intelligence and machine learning, may further complicate our ability to anticipate and implement effective protective measures against cyber events.

Any significant disruption, breakdown, intrusion, interruption or corruption, data breach, or compromise to the accessibility, security or integrity of our or our providers’ IT systems, or the misappropriation or disclosure of any confidential, proprietary or personally identifiable information, could result in the loss of data or intellectual property, equipment or systems damage, downtime, safety related issues and could have a material adverse effect on our business, including by harming our competitive position and reputation, disrupting our manufacturing, reducing the value of our investment in research and development and other strategic initiatives, impairing our ability to access suppliers, contract manufacturers, customers and cloud-based services, subjecting us to litigation or 14 Table of Contents regulatory investigations or fines, increasing the costs of compliance and remediation, or otherwise adversely affecting our business. We may be required to invest significant additional resources to comply with evolving cybersecurity regulations and to modify and enhance our IT systems, information security and controls, and to investigate and remediate any security vulnerabilities. Any losses, costs or liabilities may not be covered by, or may exceed the coverage limits of, any, or all, of our applicable insurance policies.

We may not earn a positive return from our research, development and engineering investments Developing our products through our innovation model of research and development is costly and often involves a long investment cycle. We make significant investments in research, development and engineering that may not earn an economic return. If our investments do not provide a pipeline of products or technologies that our customers demand or lower our manufacturing costs, or if our products or technologies become obsolete or disrupted by emerging technologies, it could negatively impact our revenue and operating margins for both near- and long-term.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLW_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
