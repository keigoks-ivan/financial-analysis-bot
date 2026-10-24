你是 stock-analyst v20 DD 的證據採集子 agent。標的：TTMI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - TTM Technologies product substitute technology threat 2026
  - Electronic Components alternative technology disruption 2026 2027
  - TTMI TTM Technologies technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm｜as_of：2026-02-17
<<<
The conflict between Russia and Ukraine and in other global regions has contributed to volatility in the global economy and markets and ongoing geopolitical instability and is likely to have further global economic consequences, including ongoing disruptions of the global supply chain and energy markets. The effects of the conflict have contributed to significant volatility in credit and capital markets, spikes in energy prices, changes in laws and regulations that may affect our business, sanctions or counter‑sanctions, and increased cybersecurity threats and concerns. As a result, there is a risk that supplies of our products may be significantly delayed by or may become unavailable as a result of the conflict between Russia and Ukraine and in other global regions affecting us or our suppliers. The conflicts may, at times, reduce demand for our products because of reduced global or national economic activity, disruptions and extreme volatility in global financial markets, increased rates of default and bankruptcy, and reduced levels of business and consumer spending. The effects of these conflicts could heighten or exacerbate many of the risk factors described in this Item 1A, Risk Factors, and may adversely affect our business, financial condition, and results of operation.

We rely on suppliers and equipment manufacturers for the timely delivery of raw materials, components, equipment, and spare parts used in manufacturing our products. If a raw material supplier or equipment manufacturer experiences disruptions to their supply chain or operations, or otherwise fails to satisfy our product quality standards, or if the prices or availability of raw materials change, it could harm our ability to purchase new manufacturing equipment, service the equipment we have, or timely produce our products, thereby affecting our customer relationships.

In addition, we generally schedule our quick turnaround production facilities at less than full capacity to retain our ability to respond to unexpected additional quick-turn orders. However, if these orders are not received, we may forego some production and could experience continued excess capacity. If we conclude we have significant, long-term excess capacity, we may decide to permanently close one or more of our facilities and lay off some of our employees. Closures or lay-offs could result in our recording of restructuring charges such as severance, other exit costs, and asset impairments, as well as potentially causing disruptions in our ability to supply customers.

The PCB industry is intensely competitive, highly fragmented, and rapidly changing. The worldwide electronics industry is characterized by relatively short product life cycles and significant fluctuations in product demand, and is subject to economic cycles 15 and recessionary periods. We expect competition to continue, which could result in price reductions, reduced gross margins, and loss of market share. In addition, we increasingly compete on an international basis, and new and emerging technologies may result in new competitors entering our markets.

In addition, these competitors may respond more quickly to new or emerging technologies or adapt more quickly to changes in customer requirements than we do. We must continually develop improved manufacturing processes to meet our customers’ needs for complex products, and our manufacturing process technology is generally not subject to significant proprietary protection. During recessionary periods in the electronics industry, we may need to compete more on the basis of price, which would cause our gross margins to decline.

If we are unable to adapt our design and production processes in response to rapid technological change and process development, we may not be able to compete effectively.

The markets for our products and manufacturing services are characterized by rapidly changing technology and continual implementation of new designs and production processes. Our future success highly depends on our ability to maintain and enhance our technological capabilities, design and manufacture products that meet changing customer needs, and successfully anticipate or respond to technological changes on a cost-effective and timely basis. We expect that the investment necessary to maintain our technological position will increase as customers make demands for products and services requiring more advanced technology on a quicker turnaround basis. In addition, our failure to adopt and implement technological improvements quickly may cause inefficiencies in our production process as our product yields or quality may decrease, resulting in increased costs, and may lead to customers not adopting our product designs.

New emerging technology trends, such as AI, require us to keep pace with evolving regulations and industry standards. In the United States, there are various current and proposed regulatory frameworks relating to the use of AI in products and services. We expect that the legal and regulatory environment relating to emerging technologies such as AI will continue to develop and could increase the cost of doing business, and create compliance risks and potential liability, all which may have a material adverse effect on our financial condition and results of operations. Governments are also considering the new issues in intellectual property law that AI creates, which could result in different intellectual property rights in technology we create with AI and development processes and procedures and could have a material adverse effect on our business.

In the event one or more of our facilities is closed on a temporary or permanent basis as a result of a natural disaster, required maintenance or other event, our operations could be significantly disrupted. Such events could delay or prevent product manufacturing and shipment for the time required to transfer production or repair, rebuild, or replace the affected manufacturing facilities. This time frame could be lengthy and result in significant expenses for repair and related costs. While we have disaster recovery plans in place, there can be no assurance that such plans will be sufficient to allow our operations to continue in the event of every natural or man‑made disaster, required repair, or other extraordinary event. Any extended inability to continue our operations at unaffected facilities following such an event would reduce our revenue and potentially damage our reputation as a reliable supplier.

Rising labor costs and labor shortages, including due to pandemics and other disasters, employee strikes, and other labor‑related disruptions may materially adversely affect our business, financial condition, and results of operations.

Strikes or labor disputes with our unionized employees, primarily in China, may adversely affect our ability to conduct our business. If we are unable to reach agreement with any of our unionized work groups on future negotiations regarding the terms of their collective bargaining agreements, we may be subject to work interruptions or stoppages. Any of these events could be disruptive to our operations and could result in negative publicity, loss of contracts, and a decrease in revenues. We may also become subject to additional collective bargaining agreements in the future if more employees or segments of our workforce become unionized, including any of our employees in the United States.

We rely on IT networks and systems, some of which are owned and operated by third parties, to collect, process, transmit, and store electronic information. We depend on our information systems for a variety of functions, including worldwide financial reporting, inventory management, procurement, invoicing, and email communications. These information systems are susceptible to outages due to fire, floods, power loss, telecommunications failures, hacking, terrorist attacks, and similar cybersecurity threats. In the ordinary course of our business, we collect and store sensitive data in our data centers and on our networks, including intellectual property, our proprietary and confidential business information and that of our customers, suppliers and business partners, and personally identifiable information of our employees. The secure collection, processing, storage, maintenance, and transmission of this information is critical 22 to our operations. Despite the implementation of network security measures, our information systems, including those owned and operated by third parties, on which we rely are vulnerable to computer viruses, break-ins, cyber-attacks, attacks by hackers or breaches due to employee or third-party (including suppliers and business partners) error, malfeasance, or other disruptions that are material and adverse. Further, our operations could also be materially disrupted if our vendors experience such outages or breaches.…

We are continuing the process of upgrading our ERP to enhance operating efficiencies and provide more effective management of our business operations. We are investing significant financial and personnel resources into this project. However, there is no 23 assurance that the system upgrade will meet our current or future business needs or that it will operate as designed. The transition to the new ERP will affect numerous systems necessary for our operation. If we fail to correctly implement one or more components of the ERP, we could experience significant disruption to our operations. Such disruptions could include, among other things, temporary loss of data, inability to process certain orders, failure of systems to communicate with each other, and the inability to track or reconcile key data. We are heavily dependent on automated management systems, and any significant failure or delay in the system upgrade could cause a substantial interruption to our business and additional expense, which could result in an adverse impact on our operating results, cash flows, or financial condition.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
