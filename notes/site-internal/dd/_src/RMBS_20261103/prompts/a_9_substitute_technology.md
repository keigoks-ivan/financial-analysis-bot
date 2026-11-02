你是 stock-analyst v20 DD 的證據採集子 agent。標的：RMBS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Rambus product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - RMBS Rambus technology obsolescence risk
  - Semiconductors next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm｜as_of：2026-02-18
<<<
To the extent that alternative technologies, which might provide comparable system performance at lower or similar cost to our patented technologies, are perceived to require the payment of no or lower fees or royalties, or to the extent other factors influence the industry, our customers and prospective customers may adopt and promote such alternative technologies. Even to the extent we determine that such alternative technologies infringe our patents, there can be no assurance that we would be able to negotiate agreements that would result in royalties being paid to us without litigation, which could be costly and the results of which would be uncertain. As in the past, litigation may be required to enforce and protect our IP rights, on top of the substantial investments undertaken to research and develop our innovations and technologies.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm｜as_of：2026-02-18
<<<
To the extent that alternative technologies might provide comparable system performance at lower or similar cost to our technologies, or are perceived to require the payment of no or lower fees and/or royalties, or to the extent other factors influence the industry, our customers and prospective customers may adopt and promote such alternative technologies. Even to the extent we determine that such alternative technologies infringe our patents, there can be no assurance that we would be able to negotiate agreements that would result in royalties being paid to us without litigation, which could be costly and the results of which would be uncertain.

Our ability to generate significant revenue from new markets will depend on various factors, including the development and growth of these markets; the ability of our technologies and products to address the needs of these markets; the price and 14 Table of Contents performance requirements of our customers and the preferences of end users; and our ability to provide our customers with products that provide advantages compared with alternative products.

We rely on third parties for a variety of services, including our manufacturing supply chain partners and third parties within our sales and distribution channels. Some of these third parties are, and may be, our sole manufacturer or sole source of certain 20 Table of Contents production materials and may be located in regions subject to geopolitical uncertainty (e.g., tensions between China and Taiwan and evolving export/import and national security restrictions). If we fail to manage our relationships with these manufacturers and suppliers effectively, or if they experience delays, disruptions, geopolitical changes, capacity constraints/allocation pressures or quality control problems in their operations, our ability to ship products to our customers could be impaired and our competitive position and reputation could be harmed. In addition, any adverse change in any of our manufacturers and suppliers’ financial or business condition could disrupt our ability to supply quality products to our customers. If we are required to change our manufacturers, we may lose revenue, incur increased costs and damage our end-customer relationships. In addition, porting to and qualifying a new manufacturer and commencing production can be an expensive and lengthy process.…

Semiconductor supply chain disruptions have been well publicized in the recent past. We believe that we could experience various supply constraints related to our memory interface chip business in the future. For example, to the extent we do not have sufficient wafer and packaging substrate firm commitments from our third-party suppliers or they are otherwise unable to provide such services and materials, we may not obtain the materials needed on our desired timelines or at reasonable prices. Large swings in demand could exceed our contracted supply and/or our suppliers’ capacity to meet those demand changes resulting in a shortage of parts, materials or capacity needed to manufacture our products. While we continually work with our suppliers to mitigate the impact of the supply constraints to our customer deliveries, in the event of a shortage or supply interruption from suppliers of our components, we may not be able to develop alternate sources quickly, cost-effectively or at all. An extended period of global supply chain and economic disruption, including as a result of tariffs or trade restrictions, could have a material negative impact on our business, results of operations, access to sources of liquidity and financial condition, though the full extent and duration is uncertain.

21 Table of Contents From time to time, there have been disruptions in our subcontractors’ operations as a result of power outages, improperly functioning equipment, disruptions in supply of raw materials or components or equipment failures. Our subcontractors have manufacturing and other operations in locations subject to natural disasters and possible climate changes, such as severe and variable weather and geological events resulting in increased costs, or disruptions to our manufacturing operations or those of our suppliers or customers. In addition, climate change may pose physical risks to our manufacturing facilities or our suppliers’ facilities, including increased extreme weather events that could result in supply delays or disruptions. Other events, including political or public health crises, such as an outbreak of contagious diseases, may also affect our subcontractors’ production capabilities.

Attempts by others to gain unauthorized access to and disrupt our information technology systems and IP assets are becoming more sophisticated. These attempts, which might be related to industrial or other espionage, may include (to Rambus, our customers and/or our third-party service providers), covertly introducing malware to our computers and networks and impersonating authorized users, phishing attempts and other forms of social engineering, employee or contractor malfeasance, 22 Table of Contents denial of service attacks and ransomware attacks, among others. We seek to detect and investigate all security incidents impacting our systems and to prevent their recurrence, but in some cases, we might be unaware of an incident or its magnitude and effects. We also utilize third-party service providers to host, transmit or otherwise process electronic data in connection with our business activities, including our supply chain processes, operations and communications. Our customers also often have access to and host our confidential IP and business information on their own internal and directed third-party systems.…

All of our officers and other U.S. employees are at-will employees, which means they may terminate their employment relationship with us at any time, and their knowledge of our business and industry would be extremely difficult to replace. Any changes in our senior management team in particular, even in the ordinary course of business, may be disruptive to our business. While we seek to manage these transitions carefully, including by establishing strong processes and procedures and succession planning, such changes may result in a loss of institutional knowledge and cause disruptions to our business. If our senior management team fails to work together effectively or execute our plans and strategies on a timely basis as a result of management turnover or otherwise, our business could be harmed.

Our future success depends in large part upon the continued service and enhancement of our management team and our employees. If there are unexpected changes in management, such changes could be disruptive and could negatively affect our sales, operations, culture, future recruiting efforts and strategic direction. Competition for qualified executives is intense, and if we are unable to compensate our key talent appropriately and continue expanding our management team, or successfully integrate new additions to our management team in a manner that enables us to scale our business and operations effectively, our ability to operate effectively and efficiently could be limited or negatively impacted. In addition, changes in key management positions may temporarily affect our financial performance and results of operations as new management becomes familiar with our business, processes and strategy. The loss of any of our key personnel, or our inability to attract, integrate and retain qualified employees who join us organically and through acquisitions, could require us to dedicate significant financial and other resources to such personnel matters, disrupt our operations and seriously harm our operations and business.

Our success and ability to compete are also dependent upon our ability to operate without infringing upon the patent, trademark and other IP rights of others. Third parties may claim that our current or future products or services infringe upon their IP rights. Defense of any such claim, with or without merit, could be time consuming, divert management’s attention from our business operations and result in significant expenses. We cannot assure you that we would be successful in defending against any such claims. In addition, parties making these claims may be able to obtain injunctive or other equitable relief affecting our ability to commercialize the products that incorporate the challenged IP. As a result of such claims, we may be required to obtain licenses from third parties, develop alternative technology or redesign our products. We cannot be sure that such licenses would be available on terms acceptable to us, if at all. We also may not have sufficient indemnification from our applicable vendors, if any. If a successful claim is made against us and we are unable to develop or license alternative technology, our business, financial condition, operating results and cash flows could be materially adversely affected.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
