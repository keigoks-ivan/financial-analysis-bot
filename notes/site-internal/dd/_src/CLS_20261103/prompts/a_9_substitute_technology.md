你是 stock-analyst v20 DD 的證據採集子 agent。標的：CLS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Celestica product substitute technology threat 2026
  - Electronic Components alternative technology disruption 2026 2027
  - CLS Celestica technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
We continue to invest in leading-edge product roadmaps and design capabilities aligned with both market standards and emerging technologies. We deliver both customized and jointly-designed products, and complete platform solutions in technologies including storage, servers, and networking. For customer-owned designs, we augment their design teams, and utilize our proprietary design analysis tools to minimize design revisions and to achieve improved manufacturing yields.

11 Technology and R&D We look ahead at emerging technologies, by strategically investing and collaborating with our ecosystem partners to define future product roadmaps. We aim to address technologies for data centers at the system level, and leverage our capabilities to deliver complete platform solutions, which may include software, and integration and orchestration of various technologies into rack-scale designs.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
Our operating results are highly dependent upon the ability of our customers (both our traditional OEM and hyperscaler customers) to compete and succeed in the marketplace using products we manufacture and services we provide. Factors that may adversely affect our customers include: rapid changes in technology (including evolving AI technologies); evolving industry standards; seasonal demand; their failure to successfully market, and/or a lack of widespread commercial acceptance of, their products and services; supply chain issues; the emergence of substitutes for products and services; dramatic shifts in demand which may cause them to lose market share or exit businesses; recessionary periods in our customers' markets; short product lifecycles resulting from continuous improvements in products and services, commoditization of certain products, changes in preferences by end customers, and the emergence of new entrants or competitors with disruptive products, services, or new business models. For example, competition from lower‑cost and open‑source AI models, together with rapid advances in model efficiency, may reduce user switching costs, increase price sensitivity, and limit our customers' ability to maintain or improve pricing for their AI‑related products and services.…

Our operations and those of our customers, component suppliers and/or our logistics partners may be disrupted by global or local events outside our control, including: fires and related disruptions; political instability; increased political tension between countries (including increased tensions between U.S. and other countries and between mainland China and Taiwan); geopolitical dynamics; terrorism; armed conflict (including the Russia/Ukraine conflict and the conflicts in the Middle East area (Middle East Conflicts)); labor or social unrest; criminal activity; disease or illness or other widespread health concerns, pandemics, epidemics or outbreaks of illness that affects local, regional, national or international economies; natural disasters and unusually adverse weather conditions, such as hurricanes, tornados, other extreme storms, wildfires, droughts and floods; cybersecurity incidents (see "Our operations and our customer relationships may be adversely and materially affected by disruptions to our IT systems, including disruptions from cybersecurity breaches of our IT infrastructure"); and other risks present in the jurisdictions in which we, our customers, our suppliers and/or our logistics partners operate. Our production operations are also subject to energy, power and water dependencies, including upgrades to manufacturing capabilities and power enhancements at certain facilities, permitting and infrastructure constraints, utility supply interruptions, and severe weather and grid reliability issues.…

22 proximity. These events could also lead to higher costs or supply shortages, and may disrupt the delivery of components to us or our ability to provide finished products or services to our customers, any of which could (and in the case of materials constraints, did in the past and may in the future) adversely affect our operating results materially. In addition, some of our facilities possess certifications or unique equipment necessary to work on specialized products that our other locations lack. If work is disrupted at one of these facilities as a result of the foregoing events or otherwise, it may be impractical or we may be unable to transfer such specialized work to another facility without significant costs and delays. Thus, any disruption in operations at a facility possessing specialized certifications or equipment could adversely affect our ability to provide products and services to our customers, and potentially have a negative affect on our relationships and financial results.…

Increased international political volatility, including changes to previously accepted trade or other government policies or legislation in the U.S. and Europe, instability in parts of Europe and the Middle East, as well as the ongoing refugee crisis, anti-immigrant activities, social unrest and fears of terrorism, enhanced national security measures, armed conflicts (including the Russia/Ukraine conflict and the Middle East Conflicts), security issues at the U.S./Mexico border related to illegal immigration or criminal activities associated with illegal drug activities, labor or social unrest, strained international relations, including tensions between the U.S. and other countries, and any related decline in consumer confidence arising from these and other factors may materially hinder our ability to conduct business, or may reduce demand for our products or services. Any escalation in these events or similar future events may disrupt our operations or those of our customers and suppliers and could adversely affect the availability of materials needed to manufacture our products or further disrupt the means to transport those materials to manufacturing sites and finished products to customers. Changes in policies by the U.S. or other governments could negatively affect our operating results due to changes in duties, tariffs or taxes, or limitations on currency or fund transfers, as well as government-imposed restrictions on producing certain products in, or shipping them to, specific countries.

Our operations and our customer relationships may be adversely and materially affected by disruptions to our IT systems, including disruptions from cybersecurity breaches of our IT infrastructure.

Additionally, while we aim to use AI ethically and attempt to identify and mitigate associated ethical or legal issues, we may be unsuccessful in identifying or resolving ethical or legal issues presented by the use of AI. Using AI to support business operations may carry inherent risks related to IP, data privacy and security, such as intended or unintended transmission of personal data or proprietary or sensitive information, as well as challenges related to implementing, integrating, and maintaining AI tools. See also "Our operations and our customer relationships may be adversely and materially affected by disruptions to our IT systems, including disruptions from cybersecurity breaches of our IT infrastructure." Furthermore, inaccurate, biased or harmful outputs, or misuse by third parties, could lead to reputational harm, operational disruption, customer disputes, or regulatory scrutiny.

Transfers of business or operations have increased and may again increase our costs and cause disruptions in our ability to service our customers.

Hostilities or armed conflicts (including the Russia/Ukraine conflict and the Middle East Conflicts), or any related interruption or curtailment of trade or transport among the countries where our and our customers' facilities are located, could adversely affect our business, financial condition and results of operations. Further, political, economic and military instability 30 in these or other regions could lead to an increase in cyberattacks and disruptions and instability in global markets (including increases in inflation rates, increases in energy prices and adverse effects on currency exchange rates and financial markets), supply chains and industries that could negatively impact our business, financial condition and results of operations. Although the impact of geopolitical conflicts on our supply chain has not been significant to date, we cannot assure that this will continue to be the case. Further, tensions between mainland China and Taiwan have escalated in recent periods. Geopolitical developments in China-Taiwan relations, or conflict between China and Taiwan could disrupt our supply chain for semiconductors and other electronic components or the operations of our suppliers, limit access to key ports, and/or result in potential international sanctions, any of which could adversely affect our results of operations or increase our costs. Any such disruptions may also magnify the impact of other risks described in this "Risk Factors" section.

Our ability to borrow or raise capital, or refinance or increase our third-party indebtedness may be impacted if financial markets are unstable. Disruptions in the capital and credit markets could adversely affect our ability to draw on our revolver (or any successor or additional facility), or our ability to sell desired amounts of A/R under our A/R sales program or customer supplier financing programs. Our access to funds under our credit facility (or any successor or additional facility) will be dependent on the ability of our senior lenders to meet their funding commitments. They may not be able to meet their funding commitments to us if they experience shortages of capital and liquidity or if they experience excessive volumes of borrowing requests from us and other borrowers within a short period of time. Longer term disruptions in the capital and credit markets as a result of uncertainty, changing or increased regulation, reduced alternatives, or failures of significant financial institutions could adversely affect our access to liquidity needed for our business. Any disruption could require us to take measures to conserve cash until the markets stabilize or until alternative credit arrangements or other funding sources can be 31 arranged. Such measures could include deferring our planned capital expenditure investments and reducing or eliminating discretionary uses of cash.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
