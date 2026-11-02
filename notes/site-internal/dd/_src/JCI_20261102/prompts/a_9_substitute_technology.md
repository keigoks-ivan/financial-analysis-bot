你是 stock-analyst v20 DD 的證據採集子 agent。標的：JCI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Johnson Controls International product substitute technology threat 2026
  - Building Products & Equipment alternative technology disruption 2026 2027
  - JCI Johnson Controls International technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm｜as_of：2025-11-14
<<<
Raw Materials Raw materials used by the Company’s businesses in connection with their operations include steel, aluminum, brass, copper, polypropylene and certain fluorochemicals used in fire suppression agents. The Company also uses semiconductors and other electronic components in the manufacture of its products. At times, the Company has experienced material cost increases due to global inflation, supply chain disruptions, labor shortages, increased demand and other regulatory and macroeconomic factors. Recently, the Company has experienced increased raw material costs due to tariffs and reciprocal tariffs imposed by the United States and other nations. Although the Company has been largely able to mitigate the impact of tariffs that have been enacted to date, if additional tariffs and reciprocal tariffs are implemented (whether as currently proposed or otherwise), such actions could negatively impact the Company's revenue growth and margins in future periods through decreased sales and increased cost of goods sold, as discussed in Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations. The Company could experience further disruptions, shortages, tariffs and price inflation in the future, the effect of which will depend on the Company’s ability to successfully mitigate and offset the impact of these events. In fiscal 2026, commodity prices and availability could fluctuate throughout the year and could significantly affect the Company’s results of operations.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/833444/000083344425000097/jci-20250930.htm｜as_of：2025-11-14
<<<
Our future success depends on our ability to develop or acquire, manufacture and bring competitive, and increasingly complex, products and services to market quickly and cost-effectively. Our ability to develop or acquire new products, services and technologies requires the investment of significant resources. These acquisitions and development efforts divert resources from other potential investments in our businesses, and they may not lead to the development of new technologies, products or services on a timely basis. Further, we must continue to effectively adapt our products and services to a changing technological and regulatory environment to drive growth and defend against disruption caused by competitors, regulators or other external forces impacting our business and operations. If we are unable to be agile and responsive to disruption in the development of new products, services and technologies, including capabilities such as energy efficiency, cooling technology (including liquid 11 cooling), artificial intelligence and machine learning, our business, financial condition, results of operations and cash flows could be adversely affected.

We use a wide range of materials (primarily steel, copper and aluminum) and components (including semiconductors, electronic components, and components utilizing rare earth minerals) in the global production of our products, which come from numerous suppliers around the world. Because not all of our business arrangements provide for guaranteed supply and some key parts may be available only from a single supplier or a limited group of suppliers, we are subject to supply and pricing risk. Our operations and those of our suppliers are subject to disruption for a variety of reasons. For example, we have in the past experienced the following supply chain issues due to economic, political and other factors largely beyond our control: increased input material costs and component shortages; supply chain disruptions and delays and cost inflation. In addition, some of our subcontractors have experienced supply chain and labor disruptions, which have and could in the future impact our ability to timely complete projects and convert our backlog. Such disruptions have and could in the future interrupt our ability to manufacture or obtain certain products and components, thereby adversely impacting our ability to provide products to customers and realize expected profit margins.…

We rely upon the capacity, reliability and security of our IT and data security infrastructure and our ability to expand and continually update this infrastructure in response to the changing needs of our business. As we implement new systems or integrate existing systems, they may not perform as expected. We also face the challenge of supporting our older systems, which are vulnerable to increased risks, including the risk of security breaches, system failures and disruptions, and implementing necessary upgrades. If we experience a problem with the functioning of an important IT system as a result of increased burdens placed on our IT infrastructure or a security breach of our IT systems, the resulting disruptions could have a material adverse effect on our business.

Geopolitical tensions and trade disputes can disrupt supply chains and increase the cost of our products. This could cause our products to be more expensive for customers, which could reduce the demand for, or attractiveness of, such products. In addition, a geopolitical conflict in a region where we operate could disrupt our ability to conduct business operations in that region. Countries also could adopt restrictive trade measures, such as tariffs, laws and regulations concerning investments and limitations on foreign ownership of businesses, taxation, foreign exchange controls, capital controls, employment regulations and the repatriation of earnings and controls on imports or exports of goods, technology, or data, any of which could adversely affect our operations and supply chain and limit our ability to offer our products and services as intended. Changes in laws or policies governing the terms of foreign trade, and in particular increased trade restrictions, tariffs or taxes on imports from countries where we manufacture products or from where we import products or raw materials (either directly or through our suppliers) could have an impact on our competitive position, business operations and financial results.…

Trade restrictions could be adopted with little to no advanced notice, and we may not be able to effectively mitigate the adverse impacts from such measures. Political uncertainty surrounding trade or other international disputes also could have a negative impact on customer confidence and willingness to invest capital, which could impair our future growth. Any of these events could increase the cost of our products, create disruptions to our supply chain and impair our ability to effectively operate and compete in the countries where we do business.

We compete around the world in various geographic regions and product markets. Global economic and political conditions affect each of our primary businesses and the businesses of our customers and suppliers. Recessions, economic downturns, price instability, inflation, slowing economic growth and social and political instability in the industries and/or markets where we compete could negatively affect our revenues and financial performance in future periods, result in future restructuring charges, and adversely impact our ability to grow or sustain our business. For example, recent and ongoing macroeconomic and political instability caused by global supply chain disruptions, inflation, ongoing conflicts between Russia and Ukraine as well as Israel and Hamas, and other geopolitical tensions have and could continue to adversely impact our results of operations. Other consequences arising from ongoing conflicts, the further escalation of geopolitical tensions globally and their effect on our business and results of operations as well as the global economy, cannot be predicted. This may include economic sanctions, embargoes, regional instability, geopolitical shifts, expansion of current conflicts, energy instability, retaliatory action by governments, supply chain disruptions, disruption to local markets, increased cybersecurity attacks against us, our third-party service providers and customers, collateral consequences from cyber conflicts between nation-states or other politically motivated actors targeting critical technology infrastructure. and increased tensions among countries in which we operate.…

We continually evaluate the performance and strategic fit of all of our businesses and may sell businesses or product lines. Recently, we have been engaged in a strategic evaluation of our non-core product lines, leading to the divestiture of our Air Distribution Technologies business and our R&LC HVAC business. Divestitures such as these involve risks, including difficulties in the separation of operations, services, products and personnel, the diversion of management's attention from other business concerns, the disruption of our business, the potential loss of key employees and the retention of uncertain environmental or other contingent liabilities related to the divested business. We may also experience unfavorable reactions to the divestitures by customers, competitors, suppliers and employees, making it more difficult to maintain business and operational relationships. Some divestitures, including the divestiture of our R&LC HVAC business, are or may be dilutive to earnings and we may not be successful in executing restructurings and other actions to minimize or offset dilution. We may also fail to successfully complete divestitures, achieve the strategic objectives of divestitures or not realize such objectives within the expected time frame, including our objective to simplify our portfolio to be a pure-play provider of comprehensive solutions for commercial buildings.…

We are subject to numerous federal, state and local environmental laws and regulations governing, among other things, solid and hazardous waste storage, treatment and disposal, and remediation of releases of hazardous materials. There are significant capital, operating and other costs associated with compliance with these environmental laws and regulations. Environmental laws and regulations may become more stringent in the future, which could increase costs of compliance, decrease demand for our products, create reputational harm or require us to manufacture with alternative technologies and materials.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
