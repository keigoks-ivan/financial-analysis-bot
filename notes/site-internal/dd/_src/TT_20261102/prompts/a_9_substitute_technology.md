你是 stock-analyst v20 DD 的證據採集子 agent。標的：TT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Trane Technologies product substitute technology threat 2026
  - Building Products & Equipment alternative technology disruption 2026 2027
  - TT Trane Technologies technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-05）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm｜as_of：2026-02-05
<<<
These risks could increase our cost of doing business internationally, increase our counterparty risk, disrupt our operations, disrupt the ability of suppliers and customers to fulfill their obligations, limit our ability to sell products in certain markets and have a material adverse impact on our results of operations, financial condition, and cash flows.

We rely on suppliers to secure commodities, particularly steel and non-ferrous metals, and third-party parts and components, including electronic components, required for the manufacture of our products. A disruption in deliveries from our suppliers or decreased availability of commodities and third-party parts and components could adversely affect our ability to meet our commitments to customers, impact pricing, increase our operating costs, or impact timing and delivery of products and services. Disruptions have previously occurred and may occur in the future due to public health crises, natural disasters, regulatory changes, geopolitical events, electronic component shortages, supplier capacity constraints, labor shortages, port congestion, logistical problems, political unrest, and other issues. Some of these disruptions have resulted in supply chain constraints affecting our business including our ability to timely produce and ship our products. The unavailability of some commodities and third-party parts and components could have a material adverse impact on our results of operations and cash flows.

We face significant competition in the markets that we serve. The markets that we serve are highly competitive. We compete worldwide with a number of other manufacturers and distributors that produce and sell similar products. There has been consolidation and new entrants (including non-traditional competitors) within our industries and there may be future consolidation and new entrants, either of which could result in increased competition and pricing pressures and significantly alter the dynamics of the competitive landscape in which we operate. Due to our global footprint we are competing worldwide with large companies and with smaller, local operators who may have customer, regulatory or economic advantages in the geographies in which they are located. In addition, some of our competitors may employ pricing and other strategies that are not traditional. While we understand our markets and competitive landscape, there is always the risk of disruptive technologies coming from companies that are not traditionally manufacturers or service providers of our products. Refer to "Item 1. Business" for additional details. As we integrate acquisitions into our portfolio of solutions, we may face new competitors in our target markets and incur increased competition from alternative solutions, which could lead to decreased demand or reduced market share for our products and services.…

We must efficiently and effectively innovate, develop and commercialize new and enhanced products and services in a rapidly changing technological and business environment in order to remain competitive in our current and future markets and in order to continue to grow our business. The timely development and commercialization of new products and services and the enhancement of existing products and services is required to meet our customer demands, market trends, and regulatory requirements. The ongoing refreshment of our product and service offerings portfolio requires strategic choices of a significant investment of resources, anticipation of the opportunity and risks of new technologies, and the ability to compete with others who may have superior resources in specific technology domains. We cannot provide any assurance that any new or enhanced product or service will be successfully commercialized in a timely manner, if ever, or, if commercialized, will result in returns greater than our investment. Investment in a product or service could divert our attention and resources from other projects that become more commercially viable in the market. We also cannot provide any assurance that any new or enhanced product or service will be accepted by our current and future markets. The accelerating pace of technological change increases the risk of shortened product lifecycles.…

Changes in governmental policies on foreign trade, geopolitical tensions, and trade disputes can disrupt supply chains and increase the cost of our products. This could cause our products to be more expensive for customers, which could reduce the demand for or the attractiveness of such products. The U.S. continues to implement certain trade actions, including imposing tariffs on certain goods imported from several countries, which has resulted in retaliatory tariffs by other countries. Additional tariffs have been proposed by the current U.S. administration and there are active negotiations for extending trade treaties. It is not possible to predict the extent or focus of any such tariffs at this time. In addition, a geopolitical conflict in a region where we operate could disrupt our ability to conduct business operations in that region. In addition to tariffs, duties, quotas, trade embargoes, and sanctions, countries also could adopt other measures, such as controls on imports or exports of goods, technology, or data, which could adversely affect our operations and supply chain and limit our ability to offer our products and services as intended. These kinds of restrictions could be adopted with little to no advance notice, and we may not be able to effectively mitigate the adverse impacts from such measures.…

The global economy has been negatively impacted by geopolitical conflicts, including the military conflict between Russia and Ukraine and conflicts in the Middle East. Governments including the U.S., China, United Kingdom, and those of the European Union have imposed export controls on certain products and financial and economic sanctions on certain industry sectors and parties in Russia which has triggered retaliatory sanctions by the Russian government and its allies. The outcome and future impacts of these world conflicts remain highly uncertain, continue to evolve and may grow more severe the longer the military action and sanctions remain in effect. Risks associated with world geopolitical conflicts that have arisen or could arise in the future, include, but are not limited to, adverse effects on political developments and on general economic conditions, including inflation and consumer spending; disruptions to our supply chains; disruptions to our information systems, including through network failures, malicious or disruptive software, or cyberattacks; trade disruptions; additional tariffs; energy shortages or rationing that may adversely impact our manufacturing facilities and consumer spending, particularly in Europe; rising fuel and/or rising costs of producing, procuring and shipping our products; our exposure to foreign currency exchange rate fluctuations; and constraints, volatility or disruption in the financial markets.

We rely extensively on information technology systems, some of which are supported by third party vendors including cloud-based systems and managed service providers, to manage and operate our business. We invest in new information technology systems designed to improve our operations. These information technology systems can be damaged, disrupted, compromised, or shut down due to cyber attacks, malware, human error or malfeasance (including by employees), power and utility outages, hardware failures, telecommunication issues, or catastrophes or other unforeseen events. If these systems cease to function properly, if these systems experience security breaches or disruptions, if these systems do not provide the anticipated benefits or if we are unable to commit sufficient resources to maintain and enhance our information technology infrastructure to ensure data quality and to keep pace with continuous development in information processing technology, our ability to manage our operations could be impaired, which could have a material adverse impact on our results of operations, financial condition, and cash flows.

18 Table of Contents Security breaches or disruptions of the technology systems, infrastructure or products of the Company or our vendors could negatively impact our business and financial results.

The methods used to obtain unauthorized access, disable or degrade service, or sabotage information technology systems are constantly changing and evolving. Despite having instituted security policies and enhancing business continuity plans, and implementing and regularly reviewing and updating security controls and related processes and procedures to protect against unauthorized access and requiring similar protections from our vendors, the ever-evolving threats mean we are continually evaluating and adapting our systems and processes and ask our vendors to do the same, and there is no guarantee that such systems and processes will be adequate to safeguard against all data security breaches or misuses of data. Hardware, software, AI technology, or applications we develop or obtain from third parties sometimes contain defects in design or deployment or other problems that could unexpectedly result in security breaches or disruptions. Open source software components embedded into certain software that we use have in the past contained vulnerabilities and others may be discovered in the future. Such vulnerabilities can expose our systems to malware or allow unauthorized third-party access to data, including confidential information about our business, customers, dealers, and suppliers; personally identifiable data related to employees, customers, and other business partners; as well as other sensitive matters.…

22 Table of Contents Natural disasters or other unexpected catastrophic events may disrupt our operations and our supply chain, and may adversely affect our results of operations and financial condition, and may not be fully covered by insurance.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TT_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
