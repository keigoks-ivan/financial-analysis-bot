你是 stock-analyst v20 DD 的證據採集子 agent。標的：STM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - STMicroelectronics product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - STM STMicroelectronics technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
•Our operating results depend on our ability to obtain quality supplies on commercially reasonable terms. As we depend on a limited number of suppliers for materials, equipment and technology, we may experience supply disruptions if suppliers interrupt supply, increase prices or experience material adverse changes in their financial condition.

•Our manufacturing processes are highly complex, costly and potentially vulnerable to impurities, disruptions or inefficient implementation of production changes or interruptions that can significantly increase our costs and delay product shipments to our customers.

•Disruptions in our relationships with any one of our key customers or distributors, and/or material changes in their strategy or financial condition or business prospects, could adversely affect our results of operations.

We may also experience a shortage of certain semiconductor composites and delays in shipments due to supply chain disruptions caused by geopolitical conflicts, natural catastrophes, extreme weather events, or punctual power outages, and sales of our products may be negatively impacted by such events, both directly and indirectly through a reduction of sales or production by our customers in or to affected areas or otherwise.

Geopolitical conflicts have additionally resulted in certain countries imposing sanctions. Further consequences of such conflicts could include a risk of further sanctions, embargoes, regional instability, geopolitical shifts and adverse effects on macro-economic conditions, currency exchange rates and financial markets. This could lead to disruption to international commerce and the global economy, and could have a negative effect on our ability to sell to, ship products to, collect payments from, and support customers in certain regions based on trade restrictions, embargoes, logistics restrictions and export control law restrictions.

Our global asset base and diversified market footprint expose us to adverse impacts from tariffs, trade restrictions, and protectionist policies. These barriers can limit our ability to efficiently place products across key regions, disrupt established supply chains, increase input costs, and reduce market access particularly in jurisdictions where we operate manufacturing hubs or export our products. These risks may be particularly acute in the semiconductor industry, where cyclical demand patterns and rapid technological changes can amplify economic headwinds.

In addition, we may be subject to the imposition of sector-specific tariffs, such as the 100% tariff on imported, foreign-produced semi-conductor chips threatened by the current U.S. administration, or China’s related export controls. Any or all of these measures or restrictions may limit our ability to sell products in certain markets or source components from specific suppliers, potentially disrupting our supply chain and manufacturing capabilities and limiting our ability to service our customer base in a cost-effective manner.

In addition, our customers and suppliers may experience disruptions in their operations and supply chains, which could result in delayed, reduced, or cancelled orders or collection risks, and which may adversely affect our results of operations and financial condition.

An epidemic or pandemic may also lead to increased disruption and volatility in capital markets and credit markets. Unanticipated consequences of an epidemic or pandemic and resulting economic uncertainty could adversely affect our liquidity and capital resources in the future.

We compete in different product lines to various degrees on certain characteristics, for example, price, technical performance, product features, product design, product availability, process technology, manufacturing capabilities and sales and technical support. Given the intense competition in the semiconductor industry, if our products do not meet market requirements based on any of these characteristics, our business, financial condition and results of operations could be materially adversely affected. Our competitors may, among others, have a stronger presence in key markets and geographic regions, greater name recognition, larger customer bases, greater government support and greater financial, R&D, sales and marketing, manufacturing, distribution and technical resources 16 than us. These competitors may be able to adapt more quickly to changes in the business environment, to new or emerging technologies and to changes in customer requirements.

Our operating results depend on our ability to obtain quality supplies on commercially reasonable terms. As we depend on a limited number of suppliers for materials, equipment and technology, we may experience supply disruptions if suppliers interrupt supply, increase prices or experience material adverse changes in their financial condition.

Our ability to meet our customers’ demand to manufacture our products depends upon obtaining adequate supplies of quality materials on a timely basis and on commercially reasonable terms. Certain materials are available from a limited number of suppliers or only from a limited number of suppliers in a particular region. We purchase certain materials whose prices on the world markets have fluctuated significantly in the past and may fluctuate significantly in the future. Although supplies for most of the materials we currently use are adequate, shortages could occur in various essential materials due to interruption of supply or increased demand in the industry. For instance, geopolitical conflicts could disrupt supply chains and cause shortages of certain semiconductor components and corresponding delays in shipments. Any such shortage may impact different geographical markets disproportionately, leading to shortages or unavailability of supplies in specific areas and higher transportation costs. In addition, the costs of certain materials may increase due to inflationary rates and market pressures and we may not be able to pass on such cost increases to our customers.

We also purchase semiconductor manufacturing equipment and third-party licensed technology from a limited number of suppliers and providers and, because such equipment and technology are complex, it is difficult to replace any one supplier or provider with another or to substitute one piece of equipment or type of technology for another. In addition, suppliers and providers may extend lead times, limit our supply, increase prices or change contractual terms related to certain manufacturing equipment and third-party licensed technology, any of which could adversely affect our results. Furthermore, suppliers and technology providers tend to focus their investments on providing the most technologically advanced equipment, materials and technology and may not be able to address our requirements for equipment, materials or technology of older generations. Although we work closely with our suppliers and providers to avoid such shortages, there can be no assurance that we will not encounter these problems in the future.

Our operating results are affected by a wide variety of factors that could materially and adversely affect revenues and profitability or lead to significant variability of our operating results from one period to the next. These factors include changes in demand from our key customers, capital requirements, inventory management, availability of funding and competition, new product developments, start of adoption of our new products by customers, technological changes, manufacturing or supplier issues and changes to effective tax rates. In addition, in periods of industry overcapacity or when our key customers encounter difficulties in their end-markets or product ramps, orders are more exposed to cancellations, reductions, price renegotiation or postponements, which in turn reduce our ability to forecast the next quarter or full year production levels, revenues and margins. Although backlog may provide an indication of future orders, quantities actually purchased by customers, as well as prices, are subject to variations between booking and delivery times and, in some cases, subject to cancellation due to changes in customer needs or industry conditions, as well as seasonality, among other things. As a result, we may not meet our financial targets, which could in turn have an impact on our reputation or brand.…

Our manufacturing processes are highly complex, costly and potentially vulnerable to impurities, disruptions or inefficient implementation of production changes or interruptions that can significantly increase our costs and delay product shipments to our customers.

Disruptions in our relationships with any one of our key customers or distributors, and/or material changes in their strategy or financial condition or business prospects, could adversely affect our results of operations.

We regularly evaluate our IT systems and business continuity plan to make enhancements and periodically implement new or upgraded systems, including the transition and migration of our data systems to cloud-based platforms and critical system migration. Any delay in the implementation of, or disruption in the transition to different systems could adversely affect our ability to record and report financial and management information on a timely and accurate basis and could impact our operations and financial position. In addition, a miscalculation of the level of investment needed to ensure our technology solutions are current and up-to-date as technology advances and evolves could result in disruptions in our business should the software, hardware or maintenance of such items become out-of-date or obsolete and the costs of upgrading our cybersecurity systems and remediating damages could be substantial.

The semiconductor industry is highly competitive and characterized by constant and rapid technological change, short product lifecycles, significant price erosion and evolving standards. Accordingly, our financial performance and future prospects depend to a significant extent on our ability to develop and maximize the opportunities offered by new technologies available to our industry, such as AI or quantum.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
