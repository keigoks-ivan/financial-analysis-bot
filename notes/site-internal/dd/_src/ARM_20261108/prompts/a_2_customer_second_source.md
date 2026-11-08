你是 stock-analyst v20 DD 的證據採集子 agent。標的：ARM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_second_source] 客戶 second-source 與 in-house
Q: 最大客戶是否正在導入第二供應商，或將此環節自製（in-house）？
  - ARM Arm Holdings largest customer second-source OR in-house 2026
  - custom chip OR component second source agreement 2026
  - Arm Holdings single-source risk customer diversify supplier
  - in-house design OR insourcing Semiconductors 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
•Customers may decide to license our architecture and develop their own processors based on our architecture, rather than utilize our processor products pursuant to an implementation license.

Any developments in our product offerings, including our entry into production silicon products such as the Arm AGI CPU, and other changes to our products and services, may create real or perceived conflicts with companies that are important to our business. Our direct commercial relationships with hyperscale, cloud, enterprise, and AI infrastructure customers increase the potential for competitive conflicts with our traditional licensing customers. Many of our semiconductor and systems company customers who have historically licensed our IP may face direct competition from us in certain market segments, and our partnerships and certain commercial relationships may be perceived by other customers as preferential treatment or as creating conflicts of interest. As a result, these customers or partners may terminate or materially reduce their relationship with us, seek alternative architectures or products, develop their own proprietary architectures, withhold sensitive roadmap information, reduce collaboration on product development, challenge our pricing models or demand more favorable commercial terms, or pursue legal action. We may also be subject to greater regulatory scrutiny in relation to our business. Accordingly, to the extent that we pursue entry into any new market or offer any new product or solution, we may not realize the anticipated financial benefits of such changes in the amounts we may anticipate, on our expected timeline or at all.…

Customers may decide to license our architecture and develop their own processors based on our architecture, rather than utilize our processor products pursuant to an implementation license.

Our customers may decide to license our ISA and develop their own processors based on our ISA, rather than utilize our predeveloped products through an implementation license, resulting in less fees paid to us. Customers may choose to develop their own processors if they believe they can do so more effectively than us or if supply and capacity constraints within the semiconductor industry further incentivize vertical integration in an effort to secure additional control over their supply chains. Some of these customers may have greater name recognition and substantially greater financial, management, marketing, service, support, technical, distribution and other resources than we do. If our customers, and particularly one or more key customers from whom we generate a significant portion of our total revenues, elect to develop their own processors based on our ISA, the market for our developed processor portfolio would decline, which could have a material adverse effect on our business, results of operations, financial condition and prospects.

A significant portion of our total revenue is generated from a limited number of key customers. In particular, our top five customers (including Arm China and SoftBank Group) collectively accounted for approximately 57%, 56% and 54% of our total revenue for the fiscal years ended March 31, 2026, 2025 and 2024, respectively, and our largest customer individually, Arm China, accounted for approximately 16%, 17% and 21% of our total revenue, respectively, during those fiscal years. A portion of our near-term revenue is dependent on commercial arrangements with SoftBank Group and/or its affiliates. Any reduction, restructuring, delay, or termination of such arrangements could adversely affect our business, results of operations, and financial condition. As a result of this customer concentration, we are particularly susceptible to adverse developments affecting our key customers and their respective businesses, including industry downturns, decreased demand for their products, increased competition, changes in trade protection and other government policies, financial hardship and changes in their business model, purchasing behavior and strategic priorities, among other factors, many of which are beyond our control.…

We may face increasing competition with PRC companies that develop their own IP. Due to various factors, including local requirements, encouragement or incentives from, as well as the policies of, the PRC government promoting self-sufficiency (such as the “Made in China 2025” campaign or the “AI Plus” initiative), 21 concerns over actual, threatened or potential U.S., U.K. or PRC government actions or policies, including trade or national security policies, or other reasons, PRC semiconductor companies and OEMs may increasingly develop their own technology and use such technology in their devices, or use our competitors’ technology in their devices. Specifically, the PRC government’s 15th Five-Year Plan and related initiatives have emphasized self-sufficiency, particularly with respect to key core technologies, such as semiconductors. As part of a government-wide effort to encourage investment and development of domestic semiconductor capabilities, the PRC government could encourage financing opportunities to our competitors in the PRC on favorable terms, or influence major PRC customers to favor adoption of IP of our competitors in the PRC over our own IP.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
We continue to expand the scope of our product offerings, investing in more holistic, end-market optimized designs, expanding beyond individual design IP to providing subsystem designs. Given the complexities of developing chips using the most advanced manufacturing processes, we are making significant investments to better support the increasing number of OEMs and CSPs looking to develop their own customized chips. We also continue to actively consider the impact of next generation technology adopted by market participants, which has resulted in us allocating resources to, and exploring, new markets and/or different products and solutions for existing and prospective customers in various end markets, including, without limitation, new products in our IP portfolio, as well as solutions beyond individual IP designs such as RTL-based CSSs, GDSII-based CSSs, chiplets and complete chip solutions. For example, in 2024, we introduced a CSS targeted at customers in the infrastructure space and, more recently, in March 2026, we expanded our compute platform into production silicon products with the Arm AGI CPU.

Competition We compete based on a variety of factors, including price, performance, energy-efficiency, ease of product customization, product quality, software availability, marketing and distribution capability, customer support, name recognition and financial strength. Given our reliance on our partners and customers, our competitive position is dependent on our partners’ and customers’ competitive positions. In addition, our partners and customers do not license our products exclusively; rather, several of our partners and customers also design, develop, manufacture and market processors based on non-Arm based architectures as well as develop their own Physical IP in-house. Our partners and customers compete with each other and with us in various markets. The level of competition and the nature of the competitor generally varies based on the end market. For established markets where there is an incumbent architecture with a supporting ecosystem, it can be difficult for a new architecture to displace existing architectures and, therefore, to gain market share. For example, we have made significant progress and have established a large market share in markets such as smartphones, consumer electronics and IoT. We face competition primarily from other architectures like x86 and RISC-V in many of these markets.…

•We Satisfy our Customers’ Processor Design Needs in a Mutually Beneficial Way. We invest in creating leading products that can be used across a wide range of end markets and customers. As we expect to license our products to multiple customers, we can typically cover the entire cost of developing new Arm products by charging each customer only a portion of the total development costs. This lowers the costs for each semiconductor designer to license Arm products, versus developing the technology in-house, and enables customers to focus resources on differentiation. In addition, by licensing Arm CPU technology, the licensee immediately gains access to the vast Arm ecosystem, which would be impossible to leverage if they developed their own CPU in-house.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/parts/axes_2.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
