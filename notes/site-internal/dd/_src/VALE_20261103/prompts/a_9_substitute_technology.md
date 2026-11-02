你是 stock-analyst v20 DD 的證據採集子 agent。標的：VALE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Vale product substitute technology threat 2026
  - Other Industrial Metals & Mining alternative technology disruption 2026 2027
  - VALE Vale technology obsolescence risk
  - Other Industrial Metals & Mining next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：全文（無法依 Item 切段）｜url：https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm｜as_of：2026-03-27
<<<
Labor disputes may disrupt our operations from time to time. A substantial number of our employees, and some of the employees of our subcontractors, are unionized and governed by collective bargaining agreements or other labor arrangements that require regular renegotiation. Strikes or other labor disruptions at any of our operations could adversely affect operational efficiency, delay project completion, and increase project costs. For more information about labor relations, see Management and Employees—Employees. Additionally, our operations could be impacted by labor disputes affecting third-party suppliers that provide us with essential goods or services.

Disruptions caused by pandemics, epidemics or disease outbreaks, could materially adversely impact our financial condition, results of operations, cash flows, and competitive position, particularly as it relates to rising costs and supply chain delays and disruptions. Measures taken by governmental authorities in response to such events may also impact our business, including upon restrictions to our operations, lockdowns, shutdowns, reduced inspections, assessments and authorizations, among other difficulties. We cannot predict when and if any such events will occur and evolve, neither their scope and duration, and therefore cannot estimate the potential impact in our financial condition, results of operations, cash flows and competitive position.

Global prices for metals are subject to significant fluctuations and are affected by many factors, including actual and expected global macroeconomic and political conditions, regional and sectorial factors, levels of supply and demand, the availability and cost of substitutes, inventory levels, technological developments, regulatory and international trade matters, investments by commodity funds and others and actions of participants in the commodity markets. Sustained low market prices for the products we sell may result in the suspension of certain of our projects and operations, decrease in our mineral reserves and resources, reduction of recoverable amounts (including goodwill), impairment of assets, and may adversely affect our cash flows, financial position and results of operations. The price of our products could be subject to volatility in 2026 in case of a slower growth of the global economy.

Due to their characteristics, such technologies can demand a variety of iron ore grades according to each process. Technologies that can allow the competitive use of lower grade iron ores could reduce the relative value in use of our higher-grade portfolio and have a negative impact on the demand and premium of our iron ore products. We continue to monitor disruptive technologies and market trends to deliver appropriate supply answers.

CYBER RISKS Cyber-attacks and other cyber threats may adversely affect our business and reputation. We are exposed to a wide range of cybersecurity threats, including common industry attacks such as ransomware and digital fraud, as well as more sophisticated and coordinated efforts known as advanced persistent threats. These and other threats may result in the disclosure or theft of sensitive information, loss of data integrity, misappropriation of funds and disruptions to or interruption in our business operations and impact our ability to disclose financial results. Threat actors are increasingly using artificial intelligence to accelerate and scale cyberattacks, including more sophisticated social-engineering attempts and targeted intrusions into IT-OT (Information Technology-Operational Technology) environments critical to our mining operations. These AI-enabled threats may heighten the risk of operational disruptions, data compromise, safety impacts and regulatory or financial consequences. Although we continue strengthening controls, evolving AI-driven attack capabilities may exceed our detection and response capacity.

Regarding energy supply, energy costs are a significant component of the nickel production costs for the processing of lateritic ore at the PTVI operations in Indonesia. A major portion of PTVI’s electric furnace power requirements is supplied at a low cost by its three hydroelectric power plants on the Larona River: (i) the Larona plant, which has an average generating capacity of 165 MW, (ii) the Balambano plant, which has an average capacity of 110 MW and (iii) the Karebbe plant, with 90 MW of average generating capacity. These plants help reduce production costs by substituting hydrocarbons for power generation with hydroelectric power, reducing CO2 emissions by replacing non-renewable power generation, and enable us to increase our current nickel production capacity.

In the Middle East, steel production maintained an expansionary trajectory in 2025, reaching 56.9 Mt, an increase of 4.3% compared with the previous year, thereby supporting healthy demand for direct-reduction pellets. Growth was driven by economic diversification programs and continued industrial investments, particularly in countries such as Saudi Arabia, the United Arab Emirates (UAE), and Qatar, which increased steel demand for construction, energy, and infrastructure projects. Despite global volatility, the Middle East continued growing, supported by economic dynamism, efforts to substitute imports, and a focus on consolidating integrated industrial value chains.

The depositary reimburses us for certain expenses we incur in connection with the ADR program and other expenses, upon such terms and conditions agreed between us and the depositary from time to time. These reimbursable expenses may include legal and accounting fees, listing fees, investor relations expenses and fees payable to service providers for the distribution of material to ADR holders. The depositary may make available to us a set amount or a portion of the depositary fees charged in respect of the ADR program or otherwise upon such terms and conditions we and the depositary may agree from time to time. JPMorgan Chase Bank, N.A. substituted Citibank N.A. as the depositary for our ADSs in December 2025. For the year ended December 31, 2025, Citibank N.A. reimbursed us US$25.2 million, including US$16.1 million in dividend fees and JPMorgan Chase Bank, N.A. has not reimbursed us any amounts relating to the deposit agreement.

• Our bylaws provide for a Board of Directors consisting of 11 to 13 members, including one member of the Board of Directors directly elected by our employees, in a separate election. Our employees also elect an alternate for the director elected by them. In the event of any vacancy or impediment of a member of the Board of Directors, the remaining members may appoint a substitute member until the next general shareholders’ meeting.

To support its decarbonization targets and foster economic development aligned with environmental preservation and business sustainability, the Company maintains an extensive portfolio of projects in both research and development and operational phases. These include the restructuring of its production system with a focus on direct reduction products and circular mining, the substitution of fossil energy raw materials with renewable or lower-emission sources, among others.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
