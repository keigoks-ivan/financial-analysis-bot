你是 stock-analyst v20 DD 的證據採集子 agent。標的：CAT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Caterpillar product substitute technology threat 2026
  - Farm & Heavy Construction Machinery alternative technology disruption 2026 2027
  - CAT Caterpillar technology obsolescence risk
  - Farm & Heavy Construction Machinery next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm｜as_of：2026-02-13
<<<
Raw Materials and Component Products We source our raw materials and manufactured components from suppliers both domestically and internationally. These purchases include unformed materials and rough and finished parts. Unformed materials include a variety of steel products, which are then cut or formed to shape and machined in our facilities. Rough parts include various sized steel and iron castings and forgings, which are machined to final specification levels inside our facilities. Finished parts are ready to assemble components, which are made either to Caterpillar specifications or to supplier developed specifications. We machine and assemble some of the components used in our machines, engines and power generation units and to support our after-market dealer parts sales. We also purchase various goods and services used in production, logistics, offices and product development processes. We maintain global strategic sourcing models to meet our global facilities’ production needs while building long-term supplier relationships and leveraging enterprise spend. We expect our suppliers to maintain, at all times, industry-leading levels of quality and the ability to timely deliver raw materials and component products for our machine and engine products. However, in some cases, increases in demand or supply chain disruptions have led to parts and components constraints across some products.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm｜as_of：2026-02-13
<<<
The energy, transportation, and mining industries are significant adopters of Caterpillar products. In these industries customers are likely to base their purchase decisions upon expected future commodity dynamics, including price. Commodity price volatility may be abrupt and unpredictable in response to global economic conditions, government actions, regulatory changes, supply/demand dynamics, innovation, and commodity substitutions among others. Economic conditions affecting the industries we serve may reduce capital expenditures in response to a variety of the aforementioned conditions. Reduction in these capital expenditures may lead to decreased demand for Caterpillar products and services as well as aftermarket parts as customers may choose to extend preventative maintenance and delay overhauls when possible.

These catastrophic events can significantly increase economic and customer demand uncertainty, cause inflationary pressure in the U.S. and elsewhere and lead to volatility in customer demand for the Company’s products and services and cause supply chain disruptions. Economic uncertainties could affect customer demand for the Company’s products and services, the value of the equipment financed or leased, the demand for financing and the financial condition and credit risk of our dealers and customers.

A catastrophic event resulting in the destruction or disruption of our workforce, our systems, our ability to produce and distribute our products, any of our data centers or our critical business or information technology systems could adversely affect our ability to conduct normal business operations and our operating results or cash flows. The adverse effects of any such catastrophic event would be exacerbated if experienced at the same time as another unexpected and adverse event.

10 Table of Contents Commodity price changes, material price increases, fluctuations in demand for our products and services, significant disruptions to our supply chains or significant shortages of labor and material may adversely impact our financial results or our ability to meet commitments to customers.

We rely on suppliers to produce or secure material required for the manufacture of our products. Production challenges at suppliers (including suppliers of semiconductors), a disruption in deliveries to or from suppliers or decreased availability of raw materials or commodities could have an adverse effect on our ability to meet our commitments to customers or increase our operating costs. On the other hand, in circumstances where demand for our products is less than we expect, we may experience excess inventories and be forced to incur additional costs and our profitability may suffer. Our business, competitive position, results of operations or financial condition could be negatively impacted if supply is insufficient for our operations, if significant transportation delays interfere with deliveries, if we experience excess inventories or if we are unable to adjust our production schedules or our purchases from suppliers to reflect changes in customer demand and market fluctuations on a timely basis.

Our global operations are dependent upon products manufactured, purchased and sold in the U.S. and internationally, including in countries with political and economic instability or uncertainty. Some countries have greater political and economic volatility and greater vulnerability to infrastructure and labor disruptions than others. Our business could be negatively impacted by adverse fluctuations in freight costs, fuel costs (e.g., diesel, bunker, jet), limitations on shipping and receiving capacity, and other disruptions in the transportation and shipping infrastructure at important geographic points of exit and entry for our products. Operating in different regions and countries exposes us to numerous risks, including: •multiple and potentially conflicting laws, regulations and policies that are subject to change; •imposition of currency restrictions, restrictions on repatriation of earnings or other restraints; •imposition of new or additional tariffs or quotas; 11 Table of Contents •withdrawal from or modification of trade agreements or the negotiation of new trade agreements; •imposition of new or additional trade and economic sanctions laws imposed by the U.S. or foreign governments; •war or acts of terrorism; and •political and economic instability or civil unrest that may severely disrupt economic activity in affected countries.

12 Table of Contents We have experienced cybersecurity threats and vulnerabilities in our systems and those of our third party providers, and we have experienced viruses and attacks targeting our information technology systems and networks. Such prior events, to date, have not had a material impact on our financial condition, results of operations or liquidity. However, the potential consequences of a future material cybersecurity attack include reputational damage, litigation with third parties, government enforcement actions, penalties, disruption to systems, unauthorized release of confidential or otherwise protected information, corruption of data, diminution in the value of our investment in research, development and engineering, and increased cybersecurity protection and remediation costs, which in turn could adversely affect our competitiveness, results of operations and financial condition. Due to the evolving nature of such security threats, the potential impact of any future incident cannot be predicted. Further, the amount of insurance coverage we maintain may be inadequate to cover claims or liabilities relating to a cybersecurity attack.

Unexpected events may increase our cost of doing business or disrupt our operations.

The occurrence of one or more unexpected events, including war, acts of terrorism or violence, civil unrest, fires, tornadoes, tsunamis, hurricanes, earthquakes, floods and other forms of severe weather in the United States or in other countries in which we operate or in which our suppliers are located could adversely affect our operations and financial performance. Natural disasters, pandemic illness, equipment failures, power outages or other unexpected events could result in physical damage to and complete or partial closure of one or more of our manufacturing facilities or distribution centers, temporary or long-term disruption in the supply of component products from some local and international suppliers, and disruption and delay in the transport of our products to dealers, end-users and distribution centers. Existing insurance coverage may not provide protection for all of the costs that may arise from such events.

FINANCIAL RISKS Disruptions or volatility in global financial markets could limit our sources of liquidity, or the liquidity of our customers, dealers and suppliers.

Continuing to meet our cash requirements over the long-term requires substantial liquidity and access to varied sources of funds, including capital and credit markets. Global economic conditions may cause volatility and disruptions in capital and credit markets. Market volatility, changes in counterparty credit risk, the impact of government intervention in financial markets and general economic conditions may also adversely impact our ability to access capital and credit markets to fund operating needs. Global or regional economic downturns could cause financial markets to decrease the availability of liquidity, credit and credit capacity for certain issuers, including certain customers, dealers and suppliers. An inability to access capital and credit markets may have an adverse effect on our business, results of operations, financial condition and competitive position. Furthermore, changes in global economic conditions, including material cost increases and decreases in key markets we serve, and the success of plans to manage cost increases, inventory and other important elements of our business may significantly impact our ability to generate funds from operations.

Market disruption and volatility may also lead to numerous risks in connection with these events, including but not limited to: •Market developments that may affect customer confidence levels and cause declines in the demand for financing and adverse changes in payment patterns, causing increases in delinquencies and default rates, which could increase Cat Financial’s write-offs and provision for credit losses.

•The process Cat Financial uses to estimate losses inherent in its credit exposure requires a high degree of management’s judgment regarding numerous subjective qualitative factors, including forecasts of economic conditions and how economic predictors might impair the ability of its borrowers to repay their loans. Financial market disruption and volatility may impact the accuracy of these judgments.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAT_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
