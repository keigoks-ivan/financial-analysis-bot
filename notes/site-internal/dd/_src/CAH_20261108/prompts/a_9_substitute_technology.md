你是 stock-analyst v20 DD 的證據採集子 agent。標的：CAH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Cardinal Health product substitute technology threat 2026
  - Medical Distribution alternative technology disruption 2026 2027
  - CAH Cardinal Health technology obsolescence risk
  - Medical Distribution next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-11）｜章節：全文（無法依 Item 切段）｜url：https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm｜as_of：2026-08-11
<<<
In addition to analyzing our business based on financial information prepared in accordance with GAAP, we use these non-GAAP financial measures internally to evaluate our performance, engage in financial and operational planning, and determine incentive compensation because we believe that these measures provide additional perspective on and, in some circumstances are more closely correlated to, the performance of our underlying, ongoing business. We provide these non-GAAP financial measures to investors as supplemental metrics to assist readers in assessing the effects of items and events on our financial and operating results on a year-over-year basis and in comparing our performance to that of our competitors. However, the non-GAAP financial measures that we use may be calculated differently from, and therefore may not be comparable to, similarly titled measures used by other companies. The non-GAAP financial measures disclosed by us should not be considered a substitute for, or superior to, financial measures calculated in accordance with GAAP, and the financial results calculated in accordance with GAAP and reconciliations to those financial statements set forth below should be carefully evaluated.

We have taken actions to reduce the impact of IEEPA and other tariffs on our financial results, including through cost optimization initiatives and by increasing prices on impacted products to customers; however, these measures have not fully offset the negative impact. Tariffs imposed or threatened to be imposed on goods, materials, and products from countries where we do business, and any retaliatory actions taken by such countries could result in us incurring substantial additional costs to source materials, directly and indirectly, from affected countries, and require us to raise prices on certain products and seek alternative sources of supply. If our competitors do not increase prices, or increase prices to a lesser extent than we do, or are able to offset the impact of tariffs through other actions, our competitive and financial position may be adversely affected. Additionally, if we are not able to find adequate alternate sources of supply, we may experience supply shortages or disruptions. Additionally, in certain circumstances, including in our other operating segments, we may not receive increased reimbursement commensurate with the increase in costs, which may negatively impact our results of operations.

We are also subject to government import and export controls and regulations, including the requirement that we make a determination as to the country of origin of products that we source or manufacture outside the United States. From time to time, Customs and Border protection agencies, whether in the U.S. or other jurisdictions, have challenged these determinations. These and other actions by border protection have resulted in products being detained or delayed and supply disruptions and could result in the imposition of fines and penalties. We have experienced supply constraints as a result of these and similar regulations, and it is possible that our business or results of operations could be further negatively impacted by future determinations and disruptions.

As described in greater detail in the "Business" section, we operate in markets that are highly competitive and dynamic. In recent years, U.S. healthcare industry participants, including distributors, manufacturers, suppliers, management services organizations, healthcare providers, insurers, and pharmacy chains, among others, have consolidated or formed strategic alliances. Consolidations create larger enterprises with greater negotiating power and could result in the possible loss of a customer in the situation where the combined enterprise selects one distributor from two incumbents or a reduction in our ability to market our products and services to new customers. Competitive pressures in each of our businesses may also be increased by new business models, new entrants, new regulations, or changes in enforcement priorities, changes in consumer demand, or general competitive dynamics. Our businesses face continued pricing pressure from these and other factors, which adversely affects our margins. Industry consolidation also impacts other objectives, including our ability to expand or complement our existing businesses through acquisitions. If we are unable to offset margin reductions caused by these pressures through steps such as sourcing or cost control measures, additional service offerings and sales of higher margin products, our results of operations could continue to be adversely affected.

Our business also depends on the proper functioning and security of our and our suppliers' business processes, critical facilities, including our national logistics center, and our distribution networks. Our results of operations could be adversely affected if our or a service provider's business processes, information systems, critical facilities, or distribution networks are disrupted (including disruption of access), are damaged or fail, whether due to physical disruptions, such as extreme weather events, including wildfires, hurricanes, extreme temperatures, or other natural disasters, pandemics (as they were by the COVID-19 pandemic), supply chain disruptions, or power outages, systems updates, or due to cybersecurity incidents, ransomware, or other actions of third parties, including labor strikes or shortages, political unrest, and terrorist attacks. In addition, hardware, software, and other applications and updates procured from third parties may contain defects that have and may in the future unexpectedly restrict or prevent access to or interfere with the proper operation of our information systems and hardware. Manufacturing disruptions also can occur due to regulatory action, production quality deviations, safety issues, or raw material shortages or defects, planned shifts in production sites, or because we need to transition manufacturing facilities for any key products or components that is manufactured at a single manufacturing facility where there are limited alternate facilities.…

We have experienced and expect to continue to experience weather-related impacts to the business, primarily driven by risks to certain physical components of our operations. For example, our properties have experienced physical damage resulting from adverse or extreme weather resulting in costs for repairs and may cause disruptions or changes in operations. Additionally, storms have negatively impacted our transportation network, resulting in delivery delays or disruptions.

Other events outside of our control also have, and will continue to, directly and indirectly adversely impact our operations and financial results. These events include those related to public health crises, including epidemics or pandemics; geopolitical events or tensions, including civil unrest, trade sanctions, tariffs and other trade restrictions, armed conflicts, or terrorism; negative or declining global economic conditions, or unstable international governments and legal systems. Among other potential affects, these events may have a disruptive and unpredictable impact on our operations and those of our suppliers and vendors, or customers, hinder manufacturing and transportation, result in significant excess costs, lead to shifts in customer demand, or have a negative impact on capital markets. For example, the recent conflict in Iran has resulted in increased fuel prices which may lead to increased costs for products that we source, manufacture, or distribute, and may also cause supply chain or manufacturing disruptions, impacting our ability to meet demand. Such events are inherently unpredictable, and our responses may involve the implementation of measures which may not be as successful as intended in mitigating adverse impacts.

The company’s Board oversees our overall risk management process. The Board has delegated to the Risk Oversight Committee of the Board primary responsibility for (i) overseeing cybersecurity and other major technology-related risks and our actions to monitor and mitigate such risks and (ii) monitoring emerging technologies such as artificial intelligence, including how such technologies are, or may be, incorporated into our operations, services and strategies and discussing risks related to these emerging technologies. The Risk Oversight Committee also monitors Cardinal Health’s compliance with applicable legal and regulatory requirements, including with respect to data privacy and security. The Risk Oversight Committee receives at least quarterly updates from the CISO and CIO and the Board receives at least annual cybersecurity updates. Among other items, these updates cover a range of matters relevant to our cybersecurity program, including: the threat environment and related business risks; the state, priorities of, and investments in our cybersecurity program; the availability of cyber insurance; review of certain cybersecurity incidents that have occurred within the company and the industry; and relevant cybersecurity operational metrics.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
