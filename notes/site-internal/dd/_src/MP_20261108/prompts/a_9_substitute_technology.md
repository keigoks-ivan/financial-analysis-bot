你是 stock-analyst v20 DD 的證據採集子 agent。標的：MP。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - MP Materials product substitute technology threat 2026
  - Rare Earth Mining + Magnet Manufacturing alternative technology disruption 2026 2027
  - MP MP Materials technology obsolescence risk
  - Rare Earth Mining + Magnet Manufacturing next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm｜as_of：2026-02-26
<<<
Suppliers The Materials segment uses certain proprietary chemical reagents in its flotation process, which it currently purchases from third-party suppliers. The hydrometallurgy, separations, and product finishing processes are reliant upon certain commodity reagents. These chemicals are subject to pricing volatility, supply availability and other restrictions and guidelines. In the event of a supply disruption or any other restriction, the Company believes that alternative reagents could be sourced for certain processes. As operations continue to scale at the Independence Facility, starting in the fourth quarter of 2025, the Materials segment began to supply the Magnetics segment with NdPr oxide produced at Mountain Pass. In addition, certain raw materials currently used or expected to be used in the production of metal and magnets are subject to pricing volatility, supply availability and other restrictions and guidelines.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm｜as_of：2026-02-26
<<<
•Our ability to generate revenue will be diminished if we are unable to compete with substitutions for our rare earth materials.

•Outbreaks, epidemics or pandemics could have an adverse effect on our business. •We are subject to a number of operational risks of our business, including power outages or shortages at Mountain Pass or Independence; increasing costs or limited access to raw materials; disruptions in transportation or other 10 Table of Contents services; inability to process REO that meet individual customer specifications; diminished access to water; uncertainty in our estimates of REO reserves; labor matters/labor relations; information technology and cybersecurity breaches; and/or environmental matters.

Our strategy is to produce REE and magnet products that are used in critical existing and emerging technologies, such as xEVs, advanced electronics, aerospace and defense systems, energy products, robotics, and many other high-growth, advanced technologies. The success of our business depends on the continued growth of these end-markets and the successful commercialization of rare earth products, including NdPr, in such markets. If the market for these critical existing and emerging technologies does not grow as we expect, grows slower than we expect, or if the demand for our products in these markets decreases, then our business, prospects, financial condition and operating results could be harmed. In addition, the market for these technologies, particularly in the automotive industry, tends to be cyclical, which exposes us to increased volatility, and it is uncertain as to how such macroeconomic factors will impact our business. Any unexpected costs or delays in the manufacturing of separated REE products or rare earth magnets, or less than expected demand for the critical existing and 13 Table of Contents emerging technologies that use rare earth products, could have a material adverse effect on our financial condition or results of operations.

Some of our competitors have made, or may make, acquisitions or enter into partnerships or other strategic relationships to achieve competitive advantages. In addition, new entrants not currently considered competitors may enter our market through acquisitions, partnerships, or strategic relationships. We expect these trends to continue as demand for rare earth materials increases. Industry consolidation may result in competitors with more compelling product offerings or greater pricing flexibility than we have, or business practices that make it more difficult for us to compete effectively, including on the basis of price, sales, technology or supply. For example, in 2025, China took additional steps to consolidate control of the industry into the two major groups through export and import limitations, as well as adjustments to the production quota system. Outside of China, there are few producers operating at scale, with processing capabilities located in only one other major integrated operator across Australia and Malaysia. These competitive pressures could have a material adverse effect on our business.

Our ability to generate revenue will be diminished if we are unable to compete with substitutions for our rare earth materials.

Technology changes rapidly in the industries and end-markets that utilize our materials. If these industries introduce new technologies or products that no longer require the rare earth materials or NdFeB magnets we produce or may produce in the future, or suitable substitutes become available, this could result in a decline in demand for our rare earth materials or NdFeB magnets. If the demand for our rare earth materials or NdFeB magnets decreases, it will have a material adverse effect on our business and the results of our operations.

Fluctuations in transportation costs or disruptions in transportation services or damage or loss during transport could decrease our competitiveness or impair our ability to supply REE or magnet products to our customers, which could adversely affect our results of operations.

Diminished access to water may adversely affect our operations. Processing of REO requires significant amounts of water. The technology we currently use to beneficiate REO is a sustainable process with dry tailings that limits the need for freshwater usage. Although we believe our current process is sustainable, any disruption in the process could prompt the need for significant access to freshwater. Additionally, with the commencement of our midstream operations in 2023, we require an even greater amount of water for our CHP plant, separation and extraction processes, and product finishing operations, including significant demand for highly-pure water. We maintain and operate one water supply well field for potable and process water and own land and wells in another water supply well field that we may be able to operate in the future. In addition, significant volumes of water are recycled from process brine to reduce groundwater usage. Any disruption to our current process, including our water treatment plant used to make highly-pure water, decreases in available water supply, or inability to recycle sufficient volumes of distillate may have a material adverse effect on our operations and our financial condition or results of operations.

19 Table of Contents Our profitability could be adversely affected if we fail to maintain satisfactory labor relations; work stoppages or similar difficulties could significantly disrupt our operations, reduce our revenues and materially adversely affect our results of operations.

Production at Mountain Pass and Independence is dependent upon the efforts of our employees. Although none of our employees are currently subject to any collective bargaining arrangements, our employees could, in the future, choose to be represented as a collective unit, which may result in labor disputes, work stoppages or other disruptions in our production efforts that could adversely affect us.

A work stoppage by any of the third parties providing services in connection with construction projects at Mountain Pass or Independence could significantly delay the completion of such projects and disrupt our operations, reduce our revenues, and materially adversely affect our results of operations.

We depend on the services of our senior management team and other key personnel, whose experience, relationships and leadership are critical to the execution of our strategy, including the operation and expansion of our mining, separation and magnet manufacturing activities. The loss of the services of any member of senior management could disrupt our operations, delay the execution of strategic initiatives and adversely affect our business.

20 Table of Contents We are dependent upon information technology systems, which are subject to cyber threats, disruption, damage and failure.

We depend upon information technology systems in the conduct of our operations. Our information technology systems are subject to disruption, damage or failure from a variety of sources, including, without limitation, computer viruses, security breaches, cyber-attacks, natural disasters and defects in design. Cybersecurity incidents, in particular, are evolving and include, but are not limited to, malicious software, attempts to gain unauthorized access to data and other electronic security breaches that could lead to disruptions in systems, unauthorized release of confidential or otherwise protected information or the corruption of data. In addition, malicious actors may leverage increasingly sophisticated, artificial intelligence-driven techniques to attempt to gain unauthorized access to our networks, compromise personal or confidential information, or misappropriate intellectual property. We have implemented various measures to manage our risks related to information technology systems and network disruptions. However, given the unpredictability of the timing, nature and scope of information technology disruptions, we have been in the past or could potentially be subject to downtimes, operational delays, the compromising of confidential or otherwise protected information, destruction or corruption of data, security breaches, other manipulation or improper use of our systems and networks or financial losses from remedial actions, any of which could have a material adverse effect on our business, operating results and financial condition.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
