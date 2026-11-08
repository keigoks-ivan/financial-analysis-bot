你是 stock-analyst v20 DD 的證據採集子 agent。標的：CAMT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Camtek product substitute technology threat 2026
  - Semiconductor Equipment & Materials alternative technology disruption 2026 2027
  - CAMT Camtek technology obsolescence risk
  - Semiconductor Equipment & Materials next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-19）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm｜as_of：2026-03-19
<<<
Not applicable. D. Risk Factors. Summary of Risk Factors Investing in our ordinary shares involves a degree of risk. These risks are discussed more fully below and include, but are not limited to, the following, any of which could have a material adverse effect on our financial condition, results of operations and cash flows: Risk Factors Related to Our Business, Markets, and Industry • A slowdown or contraction in AI-related semiconductor investment that may affect our business, results of operations and financial condition; • Disruption to our business by negative effects on the semiconductor industry, including as a result of economic, geopolitical, legal and other changes, in the global or local markets in which we operate; • The adverse effects of the competition in the markets we serve, that have significant market participants, some with greater resources than us; • The impact of changes in global trade policies beyond our control; • The concentration of substantial majority of our sales in the Asia Pacific region, with China being our largest territory; • The effects of global economic trends such as changing inflation, rising interest rates and economic slowdown; • The impact of regional instabilities and continued hostilities; • Supply chain constrains due to sharp increase in demand for electronic components, or disruptions to supply of components due to geopolitical or other reasons; • Introducing new products may adversely affect…

Our business could be materially disrupted by negative effects on the semiconductor industry, including as a result of economic, political, legal, and other changes, in the global or local markets in which we operate.

The markets that we serve are highly competitive and have significant global market participants, some with greater resources than us. The continued growth of the markets in which we operate may attract and result in new market entrants and may also encourage existing competitors to expand their efforts and presence in these markets. Such competitors may be able to respond more quickly to new or emerging technologies or changes in customer requirements, develop additional or superior products, benefit from greater economies of scale, offer more aggressive pricing or devote greater resources to the promotion of their products. Other competitors are local smaller competitors in the markets we operate, which target the low-end market and may offer products at lower prices. Competition could result in lower prices for our products and a corresponding reduction in our gross margin, as well as more favorable payment terms to our customers and a corresponding decline in our cash flow. If we are unsuccessful in effectively responding to our competition, our financial results will be adversely affected by reduced revenues as well as lower margins, which may lead to financial losses.

We may lose business due to the ongoing and revived hostilities, which could also prevent or delay shipments of our products, winning competitive procurement procedures, damage our facilities, harm our operations and product development and cause our sales to decrease. In the event that the hostilities and instabilities in our neighbor countries and/or territories disrupt the ongoing operation of our or our Israeli subcontractors' facilities or the airports and seaports on which we depend to import and export our supplies and products, our operations may be materially adversely affected. An inability to receive supplies and materials, shortages of materials or difficulties in procuring our materials, among others, may adversely impact our ability to commercialize and manufacture our product candidates and products in a timely manner. This could cause a number of delays and/or issues for our operations, including delay of the review of our product candidates by regulatory agencies, which in turn would have a material adverse impact on our ability to commercialize our product candidates. Although the related market disruptions are impossible to predict, they could be substantial, particularly if the current situation continues for an extended period of time or if geopolitical tensions result in expanded military operations on a global scale. See also “Risk Factors Related to Our Operations in Israel”

The markets for our products are characterized by changing technology, evolving industry standards, changes in end-user requirements and new product introductions. Our future success will depend on our ability to accurately predict new market needs and requirements and to enhance accordingly our existing products and develop and introduce new technologies for the markets in which we operate. These products must keep pace with technological developments and address the increasingly sophisticated needs of our customers. If we fail to anticipate correctly, or if we are unable to keep pace with, technological changes, products offered by our competitors or emerging industry standards, our ability to generate revenues may be negatively affected. Adopting new technologies may also result in material inventory write-offs which would adversely affect our results of operations. We cannot assure you that we will successfully forecast technology trends or that we will anticipate innovations made by other companies and respond with our own innovation in a timely manner, which could affect our competitiveness in the market.

Semiconductors and semiconductors equipment manufacturing is dependent on global supply chain of materials and components. Shortage in capacity of suppliers in face of growing demand or disruption to the global supply of electronic components, including integrated circuits, may have, an adverse effect on the lead-time for our components and increase in their prices.

war situation between Iran and Israel, the U.S., and other countries in the region has contributed to disruptions to regional air travel and to maritime traffic through critical routes, including increased risk and disruption around the Strait of Hormuz, and broader impacts on energy and freight markets. In addition, following the February 28, 2026 strikes, Houthi officials indicated an intent to resume missile and drone attacks against commercial shipping in and around the Red Sea and Gulf of Aden, which could lead to diversions, longer transit times, and higher shipping and insurance costs. To date, we have successfully managed our supply chain, but if these factors continue or become more severe, they may have an adverse effect on our supply chain and on our ability to fulfill customer orders in a timely manner, which could in turn have an adverse effect on our position in the market and on our business and operations.

If we fail to successfully develop and introduce new products that gain general market acceptance, or if we experience delays, difficulties, defects or disruptions in doing so, we may not be able to generate sufficient revenue and cash flow to recover our investments, which may result in a write down of inventory. We may also lose market share, customer loyalty, competitive advantage and reputation, and face pricing pressure and litigation risk. Any of these consequences could adversely affect our revenue, profitability and competitive position.

We occasionally use Open Source codes during our development process and in our software products. An unintentional breach of Open Source licenses might compel us to publish certain confidential and proprietary codes, incur damages, and result with intellectual property infringement claims that could be expensive and could disrupt our business.

We occasionally use open source software components under open source licenses. As certain open source copyright licenses may be categorized as “copyleft licenses” that place certain requirements and restrictions on users, we maintain a process to assure the use of permissive licenses that guarantee the freedom to use, modify and redistribute, and creating proprietary derivative works, in order to avoid any limitations on our IP and exposure of confidential proprietary software. Nonetheless, if we do not correctly monitor and manage those licenses, fail to maintain their terms (for example, to provide adequate copyright notices, or avoid modifications) or otherwise fail in identifying limited open source codes, we might be subject to third party copyright and to reciprocity obligation requiring us to make our code open for use by others as well. Such claims may harm our development efforts and competitive advantage and expose us to copyright infringement claims that could be expensive and could disrupt our business.

Climate change resulting from increased concentrations of carbon dioxide and other greenhouse gases in the atmosphere could present risks to our operations. Changes in climate patterns leading to extreme heat waves or unusual cold weather at some of our locations can lead to increased energy usage and costs, or otherwise adversely impact our facilities and operations and disrupt our supply chains and distribution systems. Concern over climate change can also result in new or additional legal or regulatory requirements designed to reduce greenhouse gas emissions or mitigate the effects of climate change on the environment. Any such new or additional legal or regulatory requirements may increase the costs associated with, or disrupt, sourcing, manufacturing and distribution of our products, which may adversely affect our business and financial results.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
