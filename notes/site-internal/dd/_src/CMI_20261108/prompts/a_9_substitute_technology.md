你是 stock-analyst v20 DD 的證據採集子 agent。標的：CMI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Cummins product substitute technology threat 2026
  - Specialty Industrial Machinery alternative technology disruption 2026 2027
  - CMI Cummins technology obsolescence risk
  - Specialty Industrial Machinery next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
26 % 28 % 28 % Percent of consolidated EBITDA (1) 26 % 33 % 32 % (1) Measured before intersegment eliminations The Engine segment manufactures and markets a broad range of diesel, natural gas and gasoline-powered engines under the Cummins brand name, as well as certain customer brand names, for the heavy-duty truck, medium-duty truck and bus, light-duty automotive and off-highway markets. We manufacture a wide variety of engine products including: •Engines with a displacement range of 2.8 to 15 liters and horsepower ranging from 48 to 715; and •New and remanufactured parts and engines, which are sold and serviced primarily through our extensive distribution network.

The Engine segment is organized by engine displacement size and serves these end-user markets: •Heavy-duty truck - We manufacture diesel and natural gas engines that range from 310 to 615 horsepower serving global heavy-duty truck customers worldwide, primarily in North America, China and Australia.

Disruption risk in certain categories of our supply chains exist and could negatively impact our ability to meet customer demand. We continue to monitor the supply chain disruptions utilizing early detection methods complemented by structured supplier risk and resiliency assessments. We increased frequency of formal and informal supplier engagement to address potentially impactful supply base constraints and enhanced collaboration to develop specific countermeasures to mitigate risks.

BACKLOG Disruption risk in certain categories of our supply chains exist and could negatively impact our ability to meet customer demand. We have supply agreements with some truck and off-highway equipment OEM customers; however a large portion of our business is transacted through open purchase orders. Many of these open orders are historically subject to month-to-month releases and are subject to cancellation on reasonable notice without cancellation charges and therefore are not considered firm. We also have strong demand for our data center products extending out six to eight quarters. We continue to work closely with our suppliers and customers to meet the demand.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
We operate our business on a global basis and changes in tariffs and other trade disruptions could adversely impact the demand for our products and our competitive position.

We manufacture, sell and service products globally and rely upon a global supply chain to deliver the raw materials, components, systems and parts that we need to manufacture and service our products. There is currently significant uncertainty about the future relationship between the U.S. and various other countries with respect to tariffs and other trade disruptions (such as embargoes, sanctions and export controls). The uncertain tariff environment, marked by the U.S. imposition of tariffs on certain countries, followed by the imposition of retaliatory tariffs on U.S. goods and services by certain countries has introduced significant market volatility and raised concerns about potential economic impacts. The extent to which tariffs and/or other trade disruptions will be enacted and the duration for which enacted tariffs and/or other trade disruptions will be in place remain uncertain and could adversely impact our production costs, customer demand and our relationships with customers and suppliers. Any of these consequences could have a material adverse effect on our results of operations, financial condition and cash flows.…

Our numerous foreign subsidiaries, affiliates and joint venture partners are governed by laws, rules and business practices that differ from those of the U.S. The activities of these entities may not comply with U.S. laws or business practices or our Code of Business Conduct. Violations of these laws may result in severe criminal or civil sanctions, could disrupt our business and result in an adverse effect on our reputation, business and results of operations, financial condition and cash flows. We cannot predict the nature, scope or effect of future regulatory requirements to which our operations might be subject or the manner in which existing laws might be administered or interpreted.

BUSINESS CONDITIONS / DISRUPTIONS We are vulnerable to raw material, transportation and labor price fluctuations and supply shortages, which impacted and could continue to impact our results of operations, financial condition and cash flows.

We continue to experience pockets of supply chain disruptions and related challenges throughout the supply chain which are further impacted by the current global tariff environment. We single source a number of parts and raw materials critical to our business operations. Any delay in our suppliers' deliveries may adversely affect our operations at multiple manufacturing locations, forcing us to seek alternative supply sources to avoid serious disruptions. Delays may be caused by factors affecting our suppliers (including, but not limited to, raw material availability, capacity constraints, port congestion, labor disputes or unrest, shortages of labor, economic downturns, availability of credit, impaired financial condition, sanctions/tariffs, restrictions on the sale or distribution of critical rare earth metals, energy inflation/availability, suppliers' allocations to other purchasers, weather emergencies, natural disasters, acts of government or acts of war or terrorism). The effects of climate change, including extreme weather events, long-term changes in temperature levels and water availability may exacerbate these risks. Any extended delay in receiving critical supplies could impair our ability to deliver products to our customers and have a material adverse effect on our results of operations, financial condition and cash flows.

Climate change may exacerbate the frequency and intensity of natural disasters and adverse weather conditions, which may cause disruptions to our operations, including disrupting manufacturing, distribution and our supply chain.

Similarly, any strategic divestiture of a product line or business or exit of a product line or product category may reduce our revenue and earnings, reduce the diversity of our business, result in material costs and expenses and cause disruption to our employees, customers, vendors and communities in which we operate.

Our IT environment and our products are exposed to potential security breaches or other disruptions, which may adversely impact our competitive position, reputation, results of operations, financial condition and cash flows.

We rely on the capacity, reliability and security of our IT environment and data security infrastructure in connection with various aspects of our business activities. We also rely on our ability to expand and continually update these technologies and related infrastructure in response to the changing needs of our business. As we implement new technologies, they may not perform as expected. We face the challenge of supporting our older technologies and implementing necessary upgrades. In addition, some of these technologies are managed by third-party service providers and are not under our direct control. If we experience a problem with an important technology, including during upgrades and/or new implementations of technologies, the resulting disruptions could have an adverse effect on our business and reputation. As customers adopt and rely on cloud-based digital technologies and services we offer, any disruption of the confidentiality, integrity or availability of those services could have an adverse effect on our business and reputation.

The data handled by our technologies is vulnerable to security threats. Our operations routinely involve receiving, storing, processing and transmitting sensitive information pertaining to our business, customers, dealers, suppliers, employees and other sensitive matters. As such, our IT environment faces information technology security threats, such as security breaches, computer malware, ransomware attacks and other "cyber attacks," which are increasing in both frequency and sophistication, along with power outages or hardware failures. Increasing use of AI may increase these risks. These threats could result in unauthorized public disclosures of information, create financial liability, subject us to legal or regulatory sanctions, disrupt our ability to conduct our business, result in the loss of intellectual property or damage our reputation with customers, dealers, suppliers and other stakeholders. As the result of changing market conditions, a large percentage of our salaried employees continue to work remotely full or part-time. This remote working environment may pose a heightened risk for security breaches or other disruptions of our IT environment.

In addition, our products, including our engines, contain interconnected and increasingly complex technologies that control various processes, and these technologies are potentially subject to "cyber attacks" and disruption. The impact of a significant IT event on either our IT environment or our products could have a material adverse effect on our competitive position, reputation, results of operations, financial condition and cash flows.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
