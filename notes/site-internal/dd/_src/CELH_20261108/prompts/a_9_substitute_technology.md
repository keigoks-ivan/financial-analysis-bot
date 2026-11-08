你是 stock-analyst v20 DD 的證據採集子 agent。標的：CELH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Celsius Holdings product substitute technology threat 2026
  - Beverages - Non-Alcoholic alternative technology disruption 2026 2027
  - CELH Celsius Holdings technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm｜as_of：2026-03-02
<<<
In the event of any disruption or delay in production of product by our co-packers, whether caused by a rift in our relationship or the inability of our co-packers to manufacture our products as required, we would need to secure the services of alternative co-packers. We may be unable to procure alternative packing facilities at commercially reasonable rates or within a reasonably short time period, and any such transition could be costly.

In addition, although we acquired one of our co-packers on November 1, 2024, such acquisition does not mitigate the risks presented by our continued reliance on third-party co-packers and instead exposes us to additional risks associated with owning and operating a manufacturing facility, including operational disruptions, labor and safety issues, capital and maintenance costs, increased regulatory compliance requirements and potential reputational harm, any of which could have a material adverse effect on our business, financial condition, results of operations and cash flows.

The Alani Nu and Rockstar acquisitions have expanded our portfolio into new energy and wellness segments, which may create overlap in consumer bases, retail placement or brand positioning. While we view these acquisitions as complementary to our business, there is a risk that certain product offerings may compete for similar customers or retail shelf space, leading to brand cannibalization or dilution. Effectively managing brand identity, pricing strategies and promotional focus across our expanded portfolio is critical to maintaining distinct market positioning. In addition, the integration of Alani Nu and Rockstar requires the alignment of different brand cultures, marketing approaches and operational models. If we are unable to successfully differentiate our brands, preserve their individual strengths or integrate their operations and teams without disruption, our growth potential could be limited and our results of operations and brand equity could be adversely affected.

The principal raw materials used in producing our products are flavors and ingredient blends as well as aluminum cans, the prices of which are subject to fluctuation. We are uncertain whether the prices of any of the foregoing or any other raw materials or ingredients we utilize will rise in the future and whether we will be able to pass any of such increases on to our customers. We do not use hedging agreements or alternative instruments to manage the risks associated with securing sufficient ingredients or other raw materials. In addition, some of these raw materials are available only from a limited number of suppliers. In the past, our industry has experienced shortages of aluminum cans. Periodic and often unpredictable industry-wide shortages of raw materials, including aluminum cans, could disrupt or delay the production of certain products and adversely affect our financial performance. As alternative sources of supply may not be available, any interruption in the supply of such raw materials could have a material adverse effect on our business, financial condition, results of operations and cash flows.

Tariffs, inflationary pressures and global supply-chain disruptions could increase costs and reduce profitability.

Tariffs, inflationary pressures and global supply-chain disruptions could increase our costs and reduce profitability. The imposition or expansion of tariffs on raw materials, packaging or imported goods, including aluminum, may increase production and distribution costs or limit the availability of key inputs. While tariffs have not materially impacted our results of operations to date, inflationary trends affecting commodities, freight, labor and fuel can also increase our cost base and reduce margins. In addition, supply-chain disruptions, whether driven by geopolitical events, trade restrictions, transportation constraints or macroeconomic volatility, could delay product shipments, increase lead times and impact our ability to meet customer demand. Although we seek to mitigate these risks through supplier diversification and cost management initiatives, our ability to recover increased costs through pricing is limited by competitive market conditions. Sustained or worsening inflation, tariff actions or supply-chain instability could materially adversely affect our operations, financial condition and results of operations.

10 We must continually maintain, protect, and upgrade our information-technology systems, including protecting against internal and external cyber-security threats, data breaches and emerging AI-driven attacks. Any such breach or system failure could result in significant business disruption, reputational harm and regulatory exposure.

IT enables us to operate efficiently, manage and support customer-facing digital interactions, maintain financial accuracy and safeguard proprietary data. If we fail to allocate and manage sufficient resources to build and maintain proper technology infrastructure, we could be exposed to transaction errors, process inefficiencies, data breaches, business interruptions, an inability to process or fulfill customer orders or loss of intellectual property and brand value. Cybersecurity threats, whether from hackers, criminal groups or nation-state actors, continue to evolve and may include malicious software, phishing, social engineering, cyber extortion or unauthorized access to networks and data, including malicious or negligent actions by employees or other insiders. The emergence of AI has further increased the speed, sophistication and frequency of these threats. Any such incident could lead to business disruptions, system outages, loss of customer or confidential information, data alteration or destruction, reputational harm and regulatory or legal exposure.

We rely extensively on enterprise resource planning systems and other IT systems to support key business processes, including financial reporting, accounting, inventory management, supply chain operations and other operational activities. The effective operation of these systems depends on their integrity, availability and ability to integrate with other internal and third-party systems. Any failure, disruption, degradation or security incident affecting our enterprise resource planning systems, including those arising from system defects, human error, power outages, cyber incidents, unsuccessful upgrades or implementations or reliance on third-party vendors, could impair our ability to operate efficiently, process transactions accurately or produce timely and reliable financial information. Such events could result in operational disruptions, control deficiencies, remediation costs or delays in reporting and could materially adversely affect our business, financial condition, results of operations and cash flows.

15 Consequently, we may not be able to successfully attract and maintain a highly skilled and diverse workforce that is necessary to support key capabilities such as e-commerce, social media and digital marketing and advertising and digital analytics. Changes in immigration laws and policies could also make it more difficult for us to recruit or relocate highly skilled technical, professional, and management personnel to meet our business needs. In certain European countries where employees are represented by unions, union activity, collective bargaining disputes or work stoppages could disrupt operations or increase costs and local labor laws may limit our flexibility to make workforce adjustments in response to changing business needs. The unexpected loss of experienced and highly skilled employees due to an increase in aggressive recruiting for best-in-class talent could deplete our institutional knowledge base and erode our competitiveness. Further, failure to attract, retain and develop associates from underrepresented communities can damage our business results and our reputation. Any of the foregoing could have a material adverse effect on our business, financial condition, results of operations and cash flows.

Because of our increasingly global presence, our business could be affected by unstable political conditions, civil unrest, protests and demonstrations, large-scale terrorist acts, especially those directed against the U.S. or other major industrialized countries where our products are distributed or the outbreak or escalation of armed hostilities. Such catastrophic events could impact our operations and our supply chain, including the production or distribution of our products. Materials or personnel may need to mobilize to other locations. Our U.S. headquarters and a large part of our operations are located in Florida, a state at significant risk of impacts from hurricanes. Some of the raw materials we use, including certain sizes of cans, are available from limited suppliers and a regional catastrophic event impacting such suppliers could adversely impact our operations. In addition, such events could disrupt global or regional economic activity, which could affect consumer purchasing power and consumers’ ability to purchase our products, thereby reducing demand for our products. If our operations are disrupted or we are unable to grow our business as a result of these factors, our growth rate could decline, which could have a material adverse effect on our business, financial condition, results of operations and cash flows.

We also rely on our co-packers to provide us with products that comply with our specifications and other applicable requirements. If they fail to do so, or if our raw material suppliers fail to supply us with material that complies with applicable specifications, it could lead to supply chain disruptions, damage to our reputation or otherwise materially adversely impact our business. It could also result in the inability of the co-packers to continue to manufacture product for us or inability of the raw material suppliers to continue to supply product to us, which could result in disruption or increased cost of product. Any of the foregoing could have a material adverse effect on our business, financial condition, results of operations and cash flows.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
