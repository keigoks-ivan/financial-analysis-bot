你是 stock-analyst v20 DD 的證據採集子 agent。標的：ALV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Autoliv product substitute technology threat 2026
  - Auto Tier 1 / Passive Safety alternative technology disruption 2026 2027
  - ALV Autoliv technology obsolescence risk
  - Auto Tier 1 / Passive Safety next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
When significant volatility in LVP occurs, as we saw in 2022 and 2023 due to supply disruptions, or when there is a shift in regional LVP, the capacity adjustments can take more time and be more costly. During 2025 the volatility of LVP improved, although it is still more volatile than prior to the COVID-19 pandemic. Additionally, when there is significant demand for a given product due to a major recall of a competitor’s product, like certain of the Company's customers have experienced, capacity adjustments may take time.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
We operate in a highly competitive market The market for passive safety systems is highly competitive, and we face competition from a number of other companies that produce and sell similar products. Among other factors, our products compete on the basis of price, quality, manufacturing and distribution capability, design and performance, technological innovation, delivery, and service. Some of our competitors are subsidiaries (or divisions, units or similar) of larger companies with greater financial and other resources than us. Some of our competitors may also have “preferred status” as a result of special relationships or ownership interests with certain customers. Our ability to compete successfully depends, in large part, on our success in continuing to innovate and manufacture products that have commercial success with our customer and end-consumers, differentiating our products from those of our competitors, continuing to deliver quality products in the time frames required by our customers, and maintaining best-cost production. We continue to invest in technology and innovation, which we believe are critical to our long-term growth. Our ability to maintain and improve existing products, while successfully developing and introducing distinctive new and enhanced products that anticipate changing customer and consumer preferences and capitalize upon emerging technologies will be a significant factor in our ability to remain competitive.…

We could experience disruption in our supply or delivery chain, which could cause one or more of our customers to halt or delay production We, as with other component manufactures in the automotive industry, ship our products to customer vehicle assembly facilities throughout the world on a “just-in-time” basis for our customers to maintain low inventory levels. Our suppliers (external suppliers as well as our own production sites) use a similar method in providing raw materials to us. However, this “just-in-time” method makes the logistics supply chain in our industry very complex and vulnerable to disruption. Disruptions in our supply chain may result for many reasons, including closures of one of our own or one of our suppliers’ facilities or critical manufacturing lines due to strikes or other labor disputes, mechanical failures, electrical outages, fires, explosions, critical pollution levels, critical health and safety and other working conditions issues (including epidemics and pandemics), natural disasters, war, geopolitical and economic instability, political upheaval, as well as logistical complications due to labor disruptions, weather or natural disasters, acts of terrorism or violence, mechanical failures, cybersecurity events, and legislation or regulation regarding the transport of hazardous goods. Inflation and pricing pressures have also negatively impacted companies in our supply chain.…

Work stoppages, slow-downs or other labor issues at our customers’ facilities or at our facilities could adversely affect our business, operating results, and financial condition Because the automotive industry relies heavily on “just-in-time” delivery of components during the assembly and manufacture of vehicles, a work stoppage or slow-down at one or more of our facilities could have a material adverse effect on our business. Similarly, if any of our customers were to experience a work stoppage or slow-down, that customer may halt or limit the purchase of our products. Similarly, a work stoppage or slow-down at another supplier could interrupt production at one of our customers’ facilities which would have the same effect. Furthermore, geopolitical instability or conflicts could displace workers or trigger the migration of workers, causing labor shortages in critical areas, which could further disrupt operations. Labor shortages could also increase wages as multiple companies and facilities compete for a shrinking pool of workers. While labor contract negotiations at our facilities historically have rarely resulted in work stoppages, no assurances can be given that we will be able to negotiate acceptable contracts with these unions or that our failure to do so will not result in work stoppages.…

15 business. Because techniques used to obtain unauthorized access or to sabotage systems change frequently and generally are not recognized until they are launched against a target, we may be unable to anticipate these techniques or to implement adequate preventative measures. Disruptions and attacks on our IT systems or the systems of third parties storing our data, or employee malfeasance or human or technological error, could result in the unauthorized access, misappropriation, loss, destruction or corruption of our critical data and confidential or proprietary information, personal information of our employees, our customers’ confidential information, and/or the improper use of our systems and networks, production downtimes and both internal and external supply shortages, which could have a material adverse effect on our operating results. Such disruptions or attacks may also result in the theft of intellectual property or other misappropriation of assets, or otherwise compromise our confidential or proprietary information and materially disrupt our operations.…

Increasing reliance on artificial intelligence technologies exposes us to operational, cybersecurity, and intellectual property risks We increasingly utilize artificial intelligence (“AI”) and machine‑learning technologies across various aspects of our manufacturing operations, including quality assurance, predictive maintenance, production automation, and supply‑chain planning. While these technologies are intended to improve efficiency and reduce costs, their deployment introduces significant risks that could adversely affect our business, operating results, and financial condition. AI systems depend on the availability of accurate, comprehensive, and properly structured data. If the data underlying these systems is incomplete, inconsistent, or of poor quality, AI outputs may be unreliable, resulting in inaccurate demand forecasts, flawed inventory or production decisions, or erroneous quality‑control assessments. Such outcomes could disrupt manufacturing, increase costs, and reduce our ability to fulfill customer requirements. Our integration of AI with interconnected operational technology also increases our vulnerability to cybersecurity threats. AI‑enabled systems and Internet‑of‑Things (“IoT”) devices expand the potential attack surface for threat actors, and certain legacy equipment used in our facilities may not have been designed with modern cybersecurity protections. A successful cyberattack on an AI-enabled system could compromise sensitive data, disrupt production processes, damage equipment, or lead to extended downtime. In addition, the use of AI tools may require processing confidential and proprietary manufacturing data.…

16 Global climate change could negatively affect our business Public awareness and concern regarding global climate change may result in more regional and/or national requirements to reduce or mitigate the effects of greenhouse gas emissions. In addition, our shareholders and customers may, to varying levels, expect us to reduce our greenhouse gas emissions. Current and any future regulations aimed at mitigating climate change may negatively impact the prices of raw materials and energy, which could impact demand for our products and adversely affect our operating results and financial condition. The costs to comply with new or amended laws and violations of these laws, which may result in substantial fines and penalties, remediation costs, third party damages, or a suspension or cessation of our operations, may be significant. The manifestations of climate change, such as extreme weather conditions or more frequent extreme weather events, including wildfires, flooding, water stress and extreme heat, could also disrupt our operations, damage our facilities, disrupt our supply chain, including our customers or suppliers, impact the availability and cost of materials needed for manufacturing or increase insurance and other operating costs.…

Tariffs, sanctions, and geopolitical conflicts may disrupt our multi‑tier automotive supply chain, constrain access to critical components, and adversely affect our production capabilities and financial performance Our operations rely on a geographically distributed, multi‑tier supply chain structure that makes us acutely sensitive to shifts in global trade policy, export‑control regimes, and geopolitical conflict. Recent U.S. trade actions affecting imports from major automotive manufacturing hubs—including broad, rapidly shifting tariff frameworks and sector‑specific levies—have increased global cost volatility and introduced uncertainty regarding long‑term sourcing strategies. Wide‑ranging tariff escalation across key trade partners has reshaped global trade flows and imposed substantial cost burdens on manufacturers dependent on cross‑border supply chains. Such measures can directly affect our ability to procure components and precision‑machined parts at competitive prices. These increased input costs may not be fully recoverable through pricing, particularly under fixed‑price or lifetime‑pricing automotive supply agreements. Semiconductor and sensor sourcing relies heavily on global electronics supply chains, which are increasingly affected by export controls, entity‑list restrictions, and sanctions targeting technology supply routes. Expanding U.S. and international restrictions on transfers of semiconductors and related technologies—such as licensing requirements for chip exports to certain entities—have already produced material disruptions and revenue impacts within the broader electronics ecosystem.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
