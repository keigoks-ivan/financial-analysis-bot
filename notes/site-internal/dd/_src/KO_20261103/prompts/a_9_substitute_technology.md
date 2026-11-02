你是 stock-analyst v20 DD 的證據採集子 agent。標的：KO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - The Coca-Cola product substitute technology threat 2026
  - Beverages - Non-Alcoholic alternative technology disruption 2026 2027
  - KO The Coca-Cola technology obsolescence risk
  - Beverages - Non-Alcoholic next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm｜as_of：2026-02-20
<<<
Other financial uncertainties in our major markets and unstable geopolitical conditions or events in certain markets, including international conflicts, civil unrest, acts of war, terrorism, governmental changes, or changes in international relations, could undermine global consumer confidence and reduce consumers’ purchasing power, thereby reducing demand for our products. Throughout 2025, the Company faced disruption to our operations due to international conflicts. Geopolitical instability has in the past led, and may in the future lead, to logistical, transportation and supply chain disruptions; business disruptions (including labor shortages); increased risk of cybersecurity incidents or other disruptions to our information systems; reduced availability and increased costs of transportation, energy, packaging, raw materials and other input costs; and heightened security risk, impacting employee safety and/or damage to infrastructure or our assets. At times, we have faced product boycotts resulting from political activism, which have reduced demand for our products. Restrictions on our ability to transfer earnings or capital across borders; price controls; limitations on profits; the negotiation of new trade agreements; new, expanded or retaliatory tariffs, including tariffs that increase suppliers’ sourcing costs; import authorization requirements; and other restrictions on business activities, which have been or may be imposed or expanded as a result of political and economic instability, deterioration of economic relations between countries or otherwise, could impact our profitability.…

We believe that improved productivity is essential to achieving our long-term growth objectives and, therefore, a leading priority of our Company is to design and implement the most effective and efficient business model possible. Consequently, we continuously search for productivity opportunities in our business. Some of the actions we may take from time to time in pursuing these opportunities may become a distraction for our managers and employees and may disrupt our ongoing business operations; cause deterioration in employee morale, which may make it more difficult for us to retain or attract qualified managers and employees; disrupt or weaken the internal control structures of the affected business operations; and give rise to negative publicity, which could affect our corporate reputation. If we are unable to successfully manage the potential negative consequences of our productivity initiatives, our business operations could be adversely affected.

The success of our business depends on our Company’s and the Coca-Cola system’s ability to attract, retain and inspire a global workforce of outstanding talent and to nurture a culture that supports our growth and aligns employees around the Company’s purpose and work that matters most. Competition for, along with compensation and benefits expectations of, existing and prospective employees has increased, especially considering changing worker expectations and talent marketplace variability. In addition, the broader labor market is experiencing a shortage of qualified talent, which has further increased the competition we face for qualified employees. We may not be able to successfully compete for, attract or retain the workforce that we want and may require for our future business needs, such as employees with advanced technology, artificial intelligence and digital marketing skills, and/or digital and analytics capabilities. Changes in laws and policies could also make it more difficult for us to recruit or relocate specialized technical, professional and management personnel to meet our business needs. In addition, the unexpected loss of experienced and specialized employees due to an increase in aggressive recruiting for best-in-class talent could deplete our institutional knowledge base and erode our competitiveness.…

At times, we have experienced, and could continue to experience, disruptions in our manufacturing operations and supply chain. In connection with our manufacturing and bottling operations, we and our bottling partners are dependent upon, among other things, various ingredients and other raw materials and packaging materials. For additional information on the raw materials and supplies we use in our business, refer to the heading “Raw Materials” set forth in Part I, “Item 1. Business” of this report. Some of the raw materials and supplies used in the production of our products are available from a limited number of suppliers, or from a sole supplier, or are in short supply when seasonal demand is at its peak. We and our bottling partners may not be able to maintain favorable arrangements and relationships with these suppliers, and our contingency plans may not be effective in preventing disruptions that may arise from shortages of any ingredients or other raw materials. Furthermore, some of our suppliers are located in countries experiencing political instability or other risks and/or unfavorable economic conditions. In addition, adverse and extreme weather conditions may affect the supply of agricultural commodities from which key ingredients for our products are derived and manufactured.…

Due to the highly competitive nature of the commercial beverage industry, the Company continually introduces new products and evolves existing products to stimulate consumer demand. For instance, the Company has directly entered the alcohol beverage category in numerous markets outside the United States, and in the United States, the Company has established a wholly owned, indirect, firewalled subsidiary, which uses third-party manufacturers and distributors to produce, distribute and sell alcohol products in the United States and also authorizes alcohol-licensed third parties to use certain of our trademarks and related intellectual property on alcohol beverages that contain Company beverage bases. The success of new and evolved products depends on several factors, including timely and successful product development, adherence to new global and/or local standards of practice, consumer acceptance and stakeholder perception. Such endeavors may also involve significant risks and uncertainties, including greater execution risks; higher costs; lower rates of sales; distraction of management from existing operations; lower product, category or industry knowledge and expertise; slower than expected or inadequate return on investments; increased competitive pressures; stakeholder scrutiny; and reliance on the performance of third parties.…

In the vast majority of our markets, our products are sold and distributed by independent bottling partners, and we therefore derive a significant portion of our net operating revenues from sales of concentrates and syrups to independent bottling partners. Accordingly, the success of our business depends in part on our bottling partners’ financial strength and profitability. While under our agreements with our bottling partners we generally have the right to unilaterally change the prices we charge for our concentrates and syrups, our ability to do so may be materially limited by our bottling partners’ financial condition and their ability to pass price increases along to their customers. In addition, we have investments in certain of our bottling partners, which we account for under the equity method, and our operating results include our proportionate share of such bottling partners’ income or loss. Our bottling partners’ financial condition is affected in large part by conditions and events that are beyond our and their control, including competitive and general market conditions; the availability of capital and other financing resources on reasonable terms; loss of major customers; changes in or additional regulations; or disruptions of bottling operations that may be caused by strikes, work stoppages, labor unrest, natural disasters, international conflicts, acts of war, health epidemics, pandemics or other catastrophic events.…

We rely on computer systems, software, networks and other technology assets (“information systems”), including the Internet and third-party hosted services, to support a variety of business processes and activities, including procurement and supply chain, manufacturing, distribution, invoicing and collection of payments, employee processes, consumer marketing, mergers and acquisitions, and research and development. We use information systems to process financial information and results of operations for internal reporting purposes and to comply with regulatory financial reporting and legal and tax requirements. In addition, we depend on information systems for digital marketing activities and electronic communications among our locations around the world and between Company employees and our bottlers, customers, suppliers, consumers and other third parties. Because information systems are critical to many of the Company’s operating activities, our business may be impacted by system shutdowns, service disruptions or cybersecurity incidents.…

There is ongoing concern that a gradual increase in global average temperatures due to increased concentration of carbon dioxide and other greenhouse gases in the atmosphere is causing significant changes in weather patterns around the globe and an increase in the frequency and severity of natural disasters. Decreased agricultural productivity in certain regions of the world as a result of changing weather patterns may limit the availability or increase the cost of key agricultural commodities, such as sugarcane, corn, sugar beets, citrus and other fruits, coffee and tea, which are important ingredients for our products, and could impact the food security of communities around the world. Climate change may also exacerbate extreme weather, resulting in water scarcity or flooding, and cause a further deterioration of water quality in affected regions, which could limit water availability for the Coca-Cola system’s bottling operations. Increased frequency or duration of extreme weather conditions could also impair production capabilities, disrupt our supply chain or impact demand for our products. Ongoing concern over climate change also may result in additional legal or regulatory requirements designed to reduce or mitigate the effects of carbon dioxide and other greenhouse gas emissions on the environment, and/or may result in increased disclosure obligations.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KO_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
