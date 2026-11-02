你是 stock-analyst v20 DD 的證據採集子 agent。標的：BSX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Boston Scientific product substitute technology threat 2026
  - Medical Devices alternative technology disruption 2026 2027
  - BSX Boston Scientific technology obsolescence risk
  - Medical Devices next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm｜as_of：2026-02-17
<<<
We remain committed to maintaining appropriate investments to ensure supply chain stability. We have an ongoing supplier resiliency program which identifies and mitigates risk and have taken measures to mitigate the impact of challenges within the global supply chain in recent years. We consistently monitor our inventory levels, manufacturing, sterilization and distribution capabilities and partnerships and maintain recovery plans to address potential disruptions or material shortages. Many components used in the manufacturing of our products are readily fabricated from commonly available raw materials or off-the- 7 shelf items available from multiple supply sources; however, certain items are custom made to meet our specifications, and certain materials and components are purchased from single sources due to quality considerations, expertise, costs or constraints resulting from regulatory requirements.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm｜as_of：2026-02-17
<<<
Economic, Industry and Geopolitical Risks We face intense competition and may not be able to keep pace with the rapid technological changes in the medical devices industry or low-cost competitive offerings, which could have an adverse effect on our business, financial condition or results of operations.

In addition, the medical device markets in which we participate are characterized by extensive research and development and rapid technological change. Developments by other companies of products and/or services, processes or technologies, including low-cost alternatives, may make our products or proposed products obsolete or less competitive and may negatively impact our net sales. It is necessary for us to devote continued efforts and financial resources to the development or acquisition of scientifically advanced technologies and products. In addition, we will need to apply our technologies cost-effectively across product lines and markets, obtain patent and other protection for our technologies and products, obtain required regulatory and reimbursement approvals and successfully manufacture and market our products consistent with our quality standards. If we fail to develop or acquire new products or enhance existing products, such failure could have a material adverse effect on our business, financial condition or results of operations. In addition, a delay in the timing of the launch of next-generation products and the overall performance of, and continued physician confidence in, those products may result in declines in our market share and have an adverse impact on our business, financial condition or results of operations.

The global macroeconomic environment has continued to experience challenging conditions and uncertainty, including with respect to inflation, interest rates, monetary policy, exchange rates, tariff and trade policies and geopolitical developments, which could adversely impact our business, financial condition, cash flows and results of operations. If there were a general economic slowdown or recession, we may experience decreased customer spending or demand for our products and services, and our customers’ ability to pay for our products on a timely basis, or at all, may be impacted. The same economic conditions could also adversely affect our third-party vendors, including those that we utilize in our supply-chain and manufacturing operations, which may lead to a reduction or interruption in the supply of materials and components used in manufacturing our products or increase the price of such materials or components, as well as the distributors and dealers who offer our products in certain countries and markets. Continued inflationary pressure may also increase certain operational costs, including due to 14 wage increases, or increases in the cost of materials or components.…

Further, uncertainty about global economic conditions, including those resulting from a heightened global interest rate environment, has caused and may continue to cause disruption in the financial markets, including diminished liquidity and credit availability. These conditions could affect our ability to access credit markets, including to obtain financing for mergers and acquisitions (M&A) or for other general purposes. These conditions may adversely affect our suppliers, leading them to experience financial difficulties or be unable to borrow money to fund their operations, which could cause disruptions in our ability to produce our products. Our customers may experience financial difficulties or be unable to borrow money to fund their operations, which may adversely impact their ability or decision to purchase our products, particularly capital equipment, or to pay for our products that they purchase on a timely basis, if at all. In addition, we have accounts receivable factoring programs in certain European and Asian countries. A slowdown in the global economy or sovereign debt issues may impact our ability to transfer receivables to third parties in certain of those countries. Third parties, such as banks, offering factoring programs in these countries are looking to reduce their exposure levels to government owned or supported debt.…

Geopolitical developments related to ongoing global conflicts and tensions are sources of uncertainty and risk, and may cause disruptions to global or regional markets, supply chains or operations in applicable regions, including those related to the Russia/Ukraine war, tension in the Taiwan strait, and conflicts in the Middle East. Sanctions and export restrictions may continue to proliferate, leading to greater uncertainty in emerging and growth markets. Notably the Russia/Ukraine war has continued to create barriers to doing business in Russia and in parts of Eastern Europe and conflicts in the Middle East have disrupted operations of companies doing business in the region, including in Israel. Any significant changes in the political, economic, financial, competitive, legal and regulatory or reimbursement conditions where we conduct, or plan to expand, our international operations may have a material impact on our business, financial condition or results of operations.

We monitor the dynamics of the economy, the health care industry and the markets in which we compete, and assess opportunities for improved operational effectiveness and efficiency and to better align expenses with revenues, while preserving our ability to make investments in research and development projects, capital and our people, which we believe is important to our long-term success. As a result of these assessments, we have undertaken prior restructuring and optimization initiatives to enhance our growth potential and position us for long-term success, and may undertake other restructuring and optimization initiatives in the future. For example, in February 2023, we committed to a global restructuring program (the 2023 17 Restructuring Plan) intended to support our efforts to expand operating performance and meet evolving global market demands and conditions, and which built on our Global Supply Chain Optimization strategy to simplify our manufacturing and distribution network by transferring certain production lines among facilities and expanding operational efficiencies and resiliency across production, sterilization, and distribution. Key activities under the 2023 Restructuring Plan were initiated during the first quarter of 2023 and were substantially complete by the end of 2025.…

Our products are designed and manufactured in technology centers around the world, either by us or third parties. In most cases, the manufacturing of any specific product is concentrated in one or a few locations. Factors such as a failure to follow specific internal protocols and procedures, equipment malfunction, environmental factors or damage to one or more of our facilities could adversely affect our ability to manufacture our products. In the event of an interruption in manufacturing, we may be unable to quickly move to alternate means of producing affected products or to meet customer demand. In the event of a significant interruption, for example, as a result of a failure to follow regulatory protocols and procedures, we may experience lengthy delays in resuming production of affected products due primarily to needs for regulatory approvals. We have also faced and may continue to face disruptions in the transportation of materials, components and our products within our global supply chains, including as a result of labor disputes or shortages, strikes, port closures, public health crises or geopolitical developments, which may cause delays in the shipment of our products or other disruptions to our business, as well as increased freight costs.…

18 Disruptions in the supply of the materials and components used in manufacturing our products by third-party vendors or the sterilization of our products could adversely affect our business, results of operations and financial condition.

Our information systems require an ongoing commitment of significant resources to maintain, protect and enhance existing systems and develop new systems to keep pace with continuing changes in information processing technology, evolving systems and regulatory standards, the increasing need to protect patient and customer information and changing customer patterns. This includes opportunities as well as risks associated with the integration of AI into our or our suppliers' or customers' operations. While AI presents significant opportunities for innovation and efficiency, it could introduce new risks in managing information systems and in the cybersecurity threat landscape. In addition, third parties have and may continue to attempt to hack into our products to obtain data relating to patients, or alter the intended functionality of our medical devices, or disrupt performance of our products, or access our proprietary information and the technology from third party vendors that we rely upon may have defects or vulnerabilities which, in turn, create vulnerabilities or disruptions in our system. Cyber-attacks continue to evolve in complexity and scope, and inherently may be difficult to detect.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BSX_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
