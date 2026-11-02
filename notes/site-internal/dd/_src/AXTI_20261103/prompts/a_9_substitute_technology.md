你是 stock-analyst v20 DD 的證據採集子 agent。標的：AXTI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - AXT product substitute technology threat 2026
  - 半導體基板 / InP / GaAs alternative technology disruption 2026 2027
  - AXTI AXT technology obsolescence risk
  - 半導體基板 / InP / GaAs next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
Competition The semiconductor substrate industry is characterized by narrow technological boundaries, price erosion and generally intense competition. Certain wafer substrates, such as low-quality wafer substrates for consumer products using LED lighting, compete almost entirely on price. Other products, such as InP and low EPD GaAs wafers, have fewer competitors and quality is a key competitive factor in addition to price. We face actual and potential competition from a number of established companies who have the advantages of greater name recognition and more established relationships in the industry. In some cases, our competitors have substantially greater financial, technical and marketing resources as they are divisions of much larger companies. They may utilize these advantages to expand their product offerings more quickly, adapt to new or emerging technologies and changes in customer requirements more quickly, and devote greater resources to the marketing and sale of their products. We believe a critical factor in our business is the level of technical support we provide to the customer or prospective customer and we attempt to counter possible advantages of name recognition or size with superior technical support through our team of technical sales support professionals, the majority of whom hold PhDs in physics or materials science.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
Cyber-attacks, system security risks and data protection issues could disrupt our internal operations and cause a reduction in revenue, increase in expenses, negatively impact our results of operations or result in other adverse consequences.

Breaches of our security measures could create system disruptions or cause shutdowns or result in the accidental loss, inadvertent disclosure or unapproved dissemination of proprietary information or sensitive or confidential data about us. Cyber-attacks could use fraud, trickery or other forms of deception. In addition, the rapid evolution of AI has the potential to disrupt existing business models and markets and could result in a material adverse effect on our business. The increased adoption of AI technologies may also increase our cybersecurity risks. A cyber-attack could expose us to a risk of loss or misuse of information, result in litigation and potential liability, damage our reputation or otherwise harm our business. In addition, the cost and operational consequences of implementing further data protection measures could be significant.

Portions of our information technology infrastructure might also experience interruptions, delays or cessations of service or produce errors in connection with upgrades, systems integration or migration work that takes place from time to time, which may have a material impact on our business. We may not be successful in implementing upgrades, new systems and transitioning data, which could cause business disruptions and be more expensive, time consuming, disruptive and resource-intensive than originally anticipated. Such disruptions could adversely impact our ability to fulfill orders and interrupt other processes. Delayed sales, lower margins or lost customers could adversely affect our financial results and reputation.

We face risks related to health epidemics and other outbreaks, which could significantly disrupt our business operations.

We have invested in raw material companies in China that produce materials, including 99.99% pure gallium (4N Ga), high purity gallium (6N and 7N Ga), arsenic, germanium, germanium dioxide, pyrolytic boron nitride (pBN) crucibles and boron oxide (B2O3). We purchase a portion of the materials produced by these companies for our use and they sell the remainder of their production to third parties. We consolidate the companies in which we have a majority or controlling financial interest and employ equity accounting for the companies in which we have a smaller ownership interest. Several of these companies occupy space within larger facilities owned and/or operated by one of the other investment partners. Several of these partners are engaged in other manufacturing activities at or near the same facility. In some facilities, we share access to certain functions, including water, hazardous waste treatment or air quality treatment. If a partner in any of these ventures experiences problems with its operations, or deliberately withholds or disrupts services, disruptions in the operations of our companies could occur, having a material adverse effect on the financial condition and results of operation in these companies, and correspondingly on our financial condition or results of operations.…

Our success depends on our ability to offer new product features, improved performance characteristics and new products, such as larger diameter substrates, low defect density substrates, thicker or thinner substrates, substrates with extreme surface flatness specifications, substrates that are manufactured with a doped crystal growth process or substrates that incorporate leading technology and other technological advances. This is an ongoing iterative research and development process performed by our China team in collaboration with our product marketing managers. New products must meet customer needs and compete effectively on quality, price and performance. The markets for our products are characterized by rapid technological change, changing customer needs and evolving industry standards. If our competitors introduce products employing new technologies or performance characteristics, our existing products could become obsolete and unmarketable. Over time, we have seen our competitors selling more substrates manufactured using a crystal growth technology similar to ours, which has eroded our technological differentiation.

​ We manufacture our substrates in China and, in the year ended December 31, 2025, approximately 98% of our sales were to customers located outside the United States. Further, we have partial ownership of raw material companies in China as part of our supply chain. The United States’ current foreign policy has created uncertainty and caution in the international business community, resulting in disruptions in manufacturing, import/export, trade tariffs, sales, investments and other business activity. Such disruptions have had an adverse impact on our financial performance and could continue in the future.

Outbreaks of epidemic, pandemic, or contagious diseases, such as the recent COVID-19 pandemic could result in business disruptions and impact our operations and financial performance. The outbreak of COVID triggered references to the SARS outbreak, which occurred in 2003 and affected our business operations. Any severe occurrence of an outbreak of a contagious disease such as COVID-19, SARS, Avian Flu or Ebola may cause us or the government to temporarily close our manufacturing operations in China. In January 2020, virtually all companies in China were ordered to remain closed after the traditional Lunar New Year holiday ended, including our subsidiaries in China. If there is a renewed surge of the COVID-19 pandemic or of other contagious diseases in cities in which our PRC subsidiaries and PRC joint ventures are located, the Chinese government may require these companies to close again. If one or more of our key suppliers is required to close for an extended period, we might not have enough raw material inventories to continue manufacturing operations. In addition, during COVID-19, travel restrictions between China and the U.S. were disrupted and this impacted our efficiency.…

We are subject to the risks arising from adverse changes and uncertainty in domestic and global economies and policies. Uncertain global economic and political conditions or low or negative growth in China, Europe or the United States, along with volatility in the financial markets and U.S. financial system, increasing national debt and fiscal concerns in various regions and the adoption and availability of fiscal and monetary stimulus measures, pose challenges to our industry. Currently China’s economy is slowing and this could impact our financial performance. In addition, tariffs, trade restrictions, trade wars, high levels of inflation, high interest rates, the Russian invasion of Ukraine, the Middle East conflict, the Red Sea shipping disruptions, Brexit, heightened tensions between the U.S. and China, and U.S. bank failures in 2023, among other factors, are creating an unstable environment and can disrupt or restrict commerce. The cost and availability of funds may be adversely affected by illiquid credit markets. Volatility in U.S. and international markets and economies may adversely affect our liquidity, financial condition and profitability.…

We are subject to lawsuits, investigations and claims in the normal course of our business, which can be expensive, lengthy, and disruptive to normal business operations. As described under the heading in the “Legal Proceedings” section elsewhere in this report, we, along with our Chief Executive Officer, Morris Young, and our Chief Financial Officer, Gary Fischer, are the subject of a complaint alleging violations of federal securities laws. Our current and former directors and certain officers, are also the subject of a derivative lawsuit arising from the same allegations. In the future, we could be subject to other proceedings. This litigation and any other regulatory proceedings or claims may be time consuming, could cause us to incur significant defense costs, are disruptive to our normal business operations, and could damage our reputation or adversely affect our stock price. In the event there is an adverse ruling in any legal or regulatory proceeding or action, we may be required to make payments to third parties that could have a material adverse effect on our business, financial condition, results of operations or cash flows. Further, if we become involved in other class action litigation in the future, it could result in substantial costs and diversion of our management’s attention and resources, thus harming our business.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
