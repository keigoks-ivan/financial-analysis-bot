你是 stock-analyst v20 DD 的證據採集子 agent。標的：F。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Ford Motor product substitute technology threat 2026
  - Auto Manufacturers alternative technology disruption 2026 2027
  - F Ford Motor technology obsolescence risk
  - Auto Manufacturers next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
Ford is highly dependent on its suppliers to deliver components in accordance with Ford’s production schedule and specifications, and a shortage of or inability to timely acquire key components or raw materials has previously disrupted and may, in the future, disrupt Ford’s operations. Our products contain many components that we source globally from a complex network of suppliers, who, in turn, source components from their suppliers. If there is a shortage of a key component in our supply chain or a supplier is unable to deliver a component to us in accordance with our specifications and at the cost contracted for, because of a production issue, a disruption at a supplier’s facility (e.g., fire, explosion, equipment failure, or natural disaster), limited availability of materials, shipping problems, restrictions on transactions with certain countries or companies, implementation of tariffs, or other reason, and the component cannot be easily sourced from a different supplier, or we are unable to obtain a component on a timely basis, the shortage may disrupt our operations or increase our costs of production and our ability to recoup lost production volume may be limited. For example, in 2025, our production was disrupted by fires at one of our major aluminum suppliers, the effects of which are ongoing.

A shortage of, or our inability to acquire or find adequate suppliers of, key components or raw materials as a result of disruptions in the supply chain, import and export bans or tariffs imposed by the U.S. or foreign governments, capacity constraints, limited availability, competition for those items within the automotive industry and other sectors, or otherwise can cause a significant disruption to our production schedule and have a substantial adverse effect on our financial condition or results of operations. For example, China’s restriction on the export of rare earth minerals, which we and our suppliers utilize for a number of components, has impacted (e.g., rescheduling production, changing operating patterns)

Item 1A. Risk Factors (Continued) and caused disruptions in our production operations, increases the risk of future production disruptions, and has increased and may further increase costs (e.g., premium freight and expedited shipping costs to make up for delays in component availability). Moreover, as the industry evolves, suppliers of traditional or EV-specific components may face financial distress or choose to exit certain lines of business, further narrowing our sourcing options and potentially leading to higher prices or supply shortages that could have a substantial adverse effect on our results of operations and reputation.

Ford’s production, as well as Ford’s suppliers’ production, and/or the ability to deliver products to consumers could be disrupted by labor issues, public health issues, natural or man-made disasters, adverse effects of climate change, financial distress, production difficulties, capacity limitations, or other factors. A work stoppage or other limitation on production has occurred, and could in the future occur, at Ford’s facilities, at a facility in its supply chain, or at one of its logistics providers for any number of reasons, including as a result of labor issues, such as shortages of available employees, disputes under existing collective bargaining agreements with labor unions or in connection with negotiation of new collective bargaining agreements, absenteeism, public health issues (e.g., COVID), stay-at-home orders, or in response to potential restructuring actions (e.g., plant closures); as a result of supplier financial distress or other production constraints, such as limited quantities of components or raw materials, quality issues, capacity limitations, or other difficulties; as a result of a natural disaster (including climate-related physical risk); social unrest; cybersecurity incidents; or for other reasons. A suspension or substantial curtailment of our manufacturing operations could have a significant adverse effect on our financial condition and results of operations. The duration of a suspension of manufacturing operations and a return to our full production schedule will vary.…

Ford may not realize the anticipated benefits of restructuring actions and such actions may cause Ford to incur significant charges, disrupt our operations, or harm our reputation. We continually review and evaluate our business to find opportunities to make our operations more efficient and reduce costs. In doing so, we have taken, and may in the future take, restructuring actions, such as strategic divestitures, unwinding an existing venture or relationship, or ceasing operations in a market, particularly for those businesses where a path to sustained profitability is not feasible in light of the capital allocation requirements or for other reasons. Our plans for implementing such actions may be accelerated by shifting industry dynamics and new entrants to our industries with which we must compete. These actions may include employee separations, a reduced footprint (e.g., plant closures or smaller operations at existing plants or plants that are not yet on-line), operating our plants at less than full capacity (e.g., reducing shifts), cancelling products or programs, or shifting our strategy for the deployment of technologies. Such restructuring actions have caused us and may in the future cause us to incur significant costs; record impairments or other charges; subject us to potential claims from employees, suppliers, dealers, other counterparties, or governmental authorities (including a reduction or clawback of 21

Operational information systems, security systems, products, and services could be affected by cybersecurity incidents, ransomware attacks, and other disruptions and impact Ford, Ford Credit, their suppliers, and dealers. We rely on information technology networks and information systems, including in-vehicle systems and mobile devices, some of which are managed by suppliers, some of which are provided by third-party service providers, and some of which ultimately rely on other services provided to these third parties by unaffiliated service providers, to process, transmit, and store electronic information that is important to the operation of our business, our vehicles, and the services we offer. Despite devoting significant resources to our cybersecurity program, we are at risk for interruptions, outages, and compromises of: (i) operational information systems (including business, financial, accounting, product development, consumer receivables, data processing, or manufacturing processes); (ii) facility security systems; and/or (iii) in-vehicle systems or mobile devices, whether caused by a ransomware or other cybersecurity incident, security breach, or other reason (e.g., a natural disaster, fire, acts of terrorism or war, or an overburdened infrastructure system). Additionally, any outage, security breach, misconfiguration, or loss of data within networks and systems managed by or reliant on the products and services of unaffiliated third parties could lead to similar compromises.…

Item 1A. Risk Factors (Continued) Changes in international trade policy can also have a substantial adverse effect on our financial condition, results of operations, or our business in general. To the extent governments in various regions implement or intensify restrictions or barriers to trade, such as tariff or non-tariff barriers, export controls, currency manipulation, or policies that otherwise favor domestic companies, there can be a significant negative impact on manufacturers based in other markets. Steps taken by governments to implement local content requirements, restrict export and import activities, or apply or consider applying additional or new tariffs on automobiles, parts, and other products and materials have disrupted supply chains, imposed additional costs on our business, and led to other countries attempting to retaliate by imposing tariffs or other barriers, which make our products more expensive for customers, and, in turn, our products less competitive, and this trend may continue. Tariffs implemented to date in the United States and elsewhere have caused significant disruption, increased costs, and uncertainty in the automotive industry, including for Ford, other OEMs, suppliers, and dealers, as well as customers. Moreover, tariffs implemented or increased in the United States and elsewhere in the future may exacerbate these impacts. The U.S.…

With operations in various markets with volatile economic or political environments and our global supply chain and utilization of transportation routes and logistics providers around the world, we are exposed to heightened risks as a result of economic, geopolitical, or other events. This could include governmental takeover (i.e., nationalization) of our manufacturing facilities or intellectual property, restrictive exchange or import controls, changes to international trade agreements, disruption of operations as a result of systemic political or economic instability, social unrest, outbreak of war or expansion of hostilities, and acts of terrorism, each of which could impact our supply chain as well as our operations. These events could also have a substantial adverse effect on our financial condition, results of operations, or our business in general. Changes in trade policy may also restrict or limit the ability of logistics providers and customs brokers to process imports timely, which may delay or disrupt our operations and increase our costs. Further, the U.S. government, other governments, and international organizations could impose additional sanctions or export controls that could restrict us from doing business directly or indirectly in or with certain countries or parties, which could include affiliates, disrupt our supply chain and production, and potentially impact the repatriation of earnings.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
