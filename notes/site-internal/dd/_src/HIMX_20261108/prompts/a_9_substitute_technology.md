你是 stock-analyst v20 DD 的證據採集子 agent。標的：HIMX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Himax Technologies product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - HIMX Himax Technologies technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
Panel Manufacturers, including our customers, experience significant pressure on prices and profit margins, due largely to growing industry capacity and fluctuations in demand for TFT-LCD and OLED panels. Some panel manufacturers have greater access to capital or greater production, research and development, intellectual property, marketing or other resources than our customers, who may not be able to compete and sustain their market positions. Furthermore, our customers’ business performance may fluctuate significantly due to a number of factors, many of which are beyond their control, including and not limited to: (1) changes in consumer demand and deteriorating general economic conditions, such as geopolitical tensions and increasing tariffs; (2) the cyclical nature of the TFT-LCD and OLED industry in average selling price fluctuations, as well as its downstream industries; (3) the speed at which Panel Manufacturers expand production capacity; (4) brand companies’ continued needs for original equipment manufacturing services provided by Panel Manufacturers; (5) access to raw materials, components, equipment and utilities on a timely and economical basis; (6) technological changes; (7) the rescheduling and cancellation of large orders; (8) access to funding on satisfactory terms; and (9) fluctuations in the currencies of TFT-LCD and OLED panels exporting countries against the U.S. dollar.

Our financial condition and results of operations may be adversely affected if a public health epidemic, such as the global Covid-19 pandemic, interferes with our ability, or that of our employees, suppliers, customers and other business partners to fulfill our and their respective responsibilities and obligations related to the conduct of our business. The outbreak of Covid-19 has caused significant disruption not only to the financial markets but also to global supply chains, which can substantially depress global business activities, restrict access to capital and result in a long-term economic downturn that would negatively affect our operating results.

Certain of our competitors have established or may establish strategic or strong relationships with Panel Manufacturers that are also our existing or potential customers. Marketing our display drivers to such Panel Manufacturers that have established relationships with our competitors may be difficult. Moreover, several Panel Manufacturers have in-house design capabilities and therefore may not need to source semiconductor products from us. If our customers successfully develop in-house capabilities to design and develop semiconductors that can substitute for our products, they would likely reduce or stop purchasing our products. To sell new products, we will likely need to target new market segments and new customers with whom we do not have current relationships, which may require different strategies and may present difficulties that we have not encountered before. Failure to broaden our customer base and attract new customers may limit our growth prospects.

We use several foundries for different semiconductor products, and certain of our products are manufactured at only one of these foundries. If any one of the foundries is unable to provide the required capacity to us, or does not deliver in a timely manner, or the quality or pricing terms are not acceptable to us, or any of the foundries experience financial difficulties or insolvency risks due to the impact of the global economic turmoil or any company-specific reasons or otherwise, if their operations are damaged or if there is any other disruption, directly or indirectly, of their foundry operations and we cannot qualify an alternative foundry in a timely manner, we could experience significant delays in receiving the product being manufactured by that foundry or incur additional costs to obtain substitutes, or interruption in our supply of the affected products. If we choose to use a new foundry or process technology for a particular semiconductor product, it will take us several quarters to qualify the new foundry or process before we can begin shipping. If we cannot qualify a new foundry in a timely manner, we may experience and incur damages as above mentioned and harm our customer relationships.

Our inability to secure sufficient capacity from any of our third-party tape, assembly and testing houses at competitive prices could disrupt our shipments, harm customer relationships and reduce sales.

Access to third-party tape, assembly and testing capacity is critical to our business because we do not have in-house tape, assembly and testing capabilities for commercial production and instead rely on third-party service providers. Access to these services is especially important to our business because display drivers require specialized tape, assembly and testing services. A limited number of third-party tape, assembly and testing houses tape, assemble and test substantially all of our current products. Therefore, suppliers could be in a better position to bargain for higher prices, longer contract terms, higher deposit and/or higher contract breach penalties for their services and products, which could result in an increase in our average unit cost and/or penalty expenses. If the primary tape, assembly and testing service providers that we rely upon are not able to meet our requirements in price, quality, and service, or if our business relationships with these service providers were adversely affected, we would not be able to obtain the required capacity and would have to seek alternative providers, which may not be available on commercially reasonable terms, or at all. As a result, we do not directly control our product delivery schedules, tape, assembly and testing costs, and quality assurance and control.…

In addition, climate change could cause certain natural disasters to occur more frequently or with greater intensity. Most of our operations, and the operations of many of our semiconductor manufacturing service providers, suppliers and customers are located in Taiwan, which is vulnerable to natural disasters, in particular, earthquakes and typhoons. Our principal foundries, tape and assembly and testing houses upon which we have relied to manufacture substantially all of our display drivers are located in Taiwan. As a result of this geographic concentration, disruption of operations at our facilities or the facilities of our semiconductor manufacturing service providers and suppliers for any reason, including work stoppages, power outages, water supply shortages, fire, typhoons, earthquakes or other natural disasters, could cause delays in production and shipments of our products. In addition, shortages or interruptions in electricity supply could further be exacerbated by changes in the energy policy of the government, such as to make Taiwan a nuclear-free country. Any delays or disruptions could result in our customers seeking to source products from our competitors. If such disruptions of operation occur at our customers’ facilities and our customers may be required to shut down temporarily or to substantially reduce the operations of their fabs, these events would seriously affect demand for our products.

Disruptions in Taiwan’s political environment could negatively affect our business and ADSs market price.

17 Table of Contents In addition, the worldwide financial crisis, disruptions in business and manufacture due to sluggish demand, and global developments relating to Russia’s invasion of Ukraine, global stock markets have experienced extreme price and volume fluctuations. This volatility has had a significant effect on the market prices of securities issued by many companies for reasons which may not be directly related to their operating performance, including but not limited to events such as tax-loss selling, mutual fund redemptions, hedge fund redemptions and margin calls. These market fluctuations may also materially and adversely affect the market price of our ADSs.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
22 Table of Contents Supply Chain Management The manufacturing of display drivers is complex and requires several manufacturing stages such as wafer fabrication, gold bumping, and assembly and testing, and the availability of materials such as the processed tape used in TAB packaging. We refer to these manufacturing stages and material requirements collectively as the “supply chain”. Panel manufacturers typically operate at high levels of capacity utilization and require a reliable supply of display drivers. A shortage of display drivers, or a disruption to this supply, may disrupt panel manufacturers’ operations. As a result, a company’s ability to deliver its products on a timely basis at the quality and quantity required is critical to satisfying its existing customers and winning new ones. Such supply chain management is particularly crucial to fabless display driver companies that do not have their own in-house manufacturing capacity. In the case of display drivers, supply chain management is further complicated by the high-voltage CMOS process technology and the special assembly and testing requirements that are not standard in the semiconductor industry. Access to this capacity also depends in part on display driver companies having received assurances of demand for their products since semiconductor manufacturing service providers require credible demand forecasts before allocating capacity among customers and investing to expand their capacity to support growth.

Competition The market characteristics for our products are, in general, intensely competitive, characterized by continuous technological change, evolving industry standards, and declining average selling prices. We believe key factors that differentiate the competition in our industry include: ● customer relations; ● product performance; ● design customization; ● development time / product release; ● product integration; ● technical services; ● manufacturing costs; ● supply chain management; ● timely delivery; ● economies of scale; and ● broad product portfolio.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
