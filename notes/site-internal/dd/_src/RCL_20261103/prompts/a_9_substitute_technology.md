你是 stock-analyst v20 DD 的證據採集子 agent。標的：RCL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Royal Caribbean Cruises product substitute technology threat 2026
  - Travel Services alternative technology disruption 2026 2027
  - RCL Royal Caribbean Cruises technology obsolescence risk
  - Travel Services next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm｜as_of：2026-02-11
<<<
We are susceptible to a wide range of adverse events, including terrorist attacks, war, conflicts, civil unrest and other hostilities. The occurrence of these events or an escalation in the frequency or severity of them, and the resulting political instability, travel restrictions and advisories and concerns over safety and security aspects of traveling or the fear of any of the foregoing, have had, and could have in the future, a significant adverse impact on demand and pricing in the travel and vacation industry. These events could also result in additional security measures taken by local authorities which have, and may in the future, impact access to ports and/or destinations. In addition, such events have led, and could lead, to disruptions, instability and volatility in global markets, supply chains and industries, increased operating costs, such as fuel and food, and disruptions affecting our newbuild construction and fleet modernization efforts, any of which could materially and adversely impact our business and results of operations. Further, such events could have the effect of heightening the other risks we have described in this report, any of which also could materially and adversely affect our business and results of operations.

Disease outbreaks or an increase in concern about the risk of illness could adversely impact our business and results of operations, and may cause significant disruptions, create new risks, and exacerbate existing risks.

Natural disasters (e.g., earthquakes, volcanos, wildfires), weather and/or climate events (including hurricanes and typhoons) could impact our source markets and operations resulting in travel restrictions, guest cancellations, an inability to source our crew or our provisions and supplies from certain places. We may be required to alter itineraries and cancel a cruise or a series of cruises or to redeploy our ships due to these types of events, which could have an adverse effect on our sales, operating costs and profitability in the current and future periods. Increases in the frequency, severity or duration of these types of events would exacerbate their impact and could disrupt our operations or make certain destinations less desirable or unavailable impacting our revenues and profitability further. Any of the foregoing could have an adverse impact on our results of operations and on industry performance.

We rely on shipyards, their subcontractors and our suppliers to effectively construct our new ships and to repair, maintain, and upgrade our existing ships on a timely basis and in a cost effective manner. There are a limited number of shipyards with the capability and capacity to build, repair, maintain and/or upgrade our ships. As such, any disruptions affecting the shipyard supply chain will adversely impact our business as there are limited substitutes.

These projects increase the complexity of our business and require significant levels of investment to develop. In addition, we face greater exposure to certain key risks depending on the scope, location, and the ownership and management structure of these projects. Development activities may be delayed or adversely affected by construction challenges, supply chain disruptions, weather events, labor availability, environmental or site-specific conditions, and delays in obtaining or maintaining permits, any of which could adversely affect our ability to complete our projects as planned. We may also face opposition or challenges from non-governmental organizations (NGOs), community groups, or other stakeholders, including claims related to environmental impact, cultural heritage, or land use. Such challenges may result in litigation, administrative proceedings, reputational harm, or additional compliance costs.

Once operational, these projects are also subject to ongoing regulatory, labor and political risks in foreign jurisdictions, including changes in government policies, tax or regulatory regimes, any of which could disrupt operations or increase costs. These projects can also strain our management, personnel, operations and systems.

We rely on travel advisors to generate bookings for our global brands. Accordingly, we must maintain competitive commission rates and incentive structures. If we fail to offer competitive compensation packages or fail to maintain our relationships, these agencies may be incentivized to sell cruises offered by our competitors, which could adversely impact our operating results. Our reliance on third-party sellers is particularly pronounced in certain markets. In addition, the travel advisor community is sensitive to economic conditions that impact discretionary income of consumers. Significant disruptions or contractions in the industry could reduce the number of travel advisors available for us to market and sell our cruises, which could have an adverse impact on our financial condition and results of operations.

We rely on supply chain vendors to deliver key products to the operations of our businesses around the world. Any event impacting a vendor’s ability to deliver goods of the expected quality at the location and time needed could negatively impact our ability to deliver our cruise experience. Events impacting our supply chain could be caused by factors beyond the control of our suppliers or us, including inclement weather, natural disasters, labor actions, increased demand, problems in production or distribution, cybersecurity events, and/or disruptions in third-party logistics or transportation systems. Our supply chain can also be impacted by new laws and regulations, such as tariffs and trade sanctions. For example, the imposition by the U.S. government of tariffs on products imported from certain countries and trade sanctions against certain countries have introduced greater uncertainty with respect to policies affecting trade between the United States and other countries. Major developments in trade relations, including the imposition of new or increased tariffs by the United States and/or other countries, could have a material adverse effect on our business, financial condition and results of operations.

Disruptions in our shoreside or shipboard operations or our information systems may adversely affect our results of operations.

Although we believe we can access sufficient liquidity to fund our operations, investments and obligations as expected, there can be no assurances to that effect. Our ability to access additional funding as and when needed, our ability to timely refinance and/or replace our outstanding debt securities and credit facilities on acceptable terms and our cost of funding will depend upon numerous factors including, but not limited to, the strength of the financial markets, global market conditions, including inflationary pressures, interest rate fluctuations, credit ratings, our financial performance, the performance of our industry in general and the size, scope and timing of our financial needs. In addition, even where financing commitments have been secured, significant disruptions in the capital and credit markets could cause our banking and other counterparties to breach their contractual obligations to us or could cause the conditions to the availability of such funding not to be satisfied. This could include failures of banks or other financial service companies to fund required borrowings under our loan agreements or to pay us amounts that may become due. If any of the foregoing occurs for a prolonged period of time it will have a long-term negative impact on our cash flows, our ability to meet our financial obligations, our results of operations and our financial condition.

The loss of key personnel, our inability to recruit or retain qualified personnel, or disruptions among our shipboard personnel could adversely affect our results of operations.

As of December 31, 2025, approximately 87% of our shipboard employees were covered by collective bargaining agreements. A dispute under our collective bargaining agreements could result in a work stoppage of those employees covered by the agreements. We may not be able to satisfactorily or favorably renegotiate these collective bargaining agreements when they expire. In addition, existing collective bargaining agreements may not prevent a strike or work stoppage on our ships. We may also be subject to or affected by work stoppages unrelated to our business or collective bargaining agreements. Any such work stoppages or potential work stoppages could have a material adverse effect on our financial results, as could a loss of key employees, our inability to recruit or retain qualified personnel or disruptions among our personnel.

If we are unable to keep pace with developments, design, and implementation in technology, our operations or competitive position could become impaired. Our use of emerging technologies, including artificial intelligence, may present business, compliance and reputational risks.

As global technology‑related regulatory frameworks continue to evolve, our use of these technologies may subject us to additional compliance obligations, including restrictions on the usage of certain technologies or additional requirements on data usage and transparency. Compliance with these regulations could increase our compliance costs, expose us to regulatory enforcement or legal liability, constrain our ability to implement or expand technology‑based solutions, or otherwise affect the timing and effectiveness of our initiatives. In addition, emerging technologies may not always perform as intended, may generate inaccurate outputs, or may depend on third‑party systems that we do not control. Any such operational deficiencies could impair the performance of systems that support key business functions, disrupt guest‑facing experiences, or subject us to legal liability, which could adversely affect our business, reputation, financial condition, or results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
