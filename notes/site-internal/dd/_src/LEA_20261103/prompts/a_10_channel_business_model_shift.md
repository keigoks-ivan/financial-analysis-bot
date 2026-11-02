你是 stock-analyst v20 DD 的證據採集子 agent。標的：LEA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Lear distribution channel disruption OR shift 2026
  - LEA Lear business model transition subscription OR platform 2026
  - Auto Parts channel disintermediation D2C 2026
  - Lear go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
BUSINESS OF THE COMPANY General Lear Corporation is a global automotive technology leader in Seating and E-Systems, enabling superior in-vehicle experiences for consumers around the world. We supply complete seat systems, key seat components, complete electrical distribution and connection systems, high-voltage power distribution products, including battery disconnect units ("BDUs"), and low-voltage power distribution products and electronic controllers to all of the world's major automotive manufacturers. At Lear, we are Making every drive betterTM by providing technology for safer, smarter and more comfortable journeys, while adhering to our values — Be Inclusive. Be Inventive. Get Results the Right Way.

•E-Systems — Our E-Systems segment consists of the design, development, engineering and manufacture of complete electrical distribution and connection systems; high-voltage power distribution products, including BDUs; and low-voltage power distribution products and electronic controllers. These capabilities enable us to provide our customers with customizable solutions with optimized designs at competitive costs for both low-voltage and high-voltage vehicle architectures.

–Electrical distribution and connection systems utilize low-voltage and high-voltage wire and high-speed data cables to connect networks' electrical signals and manage electrical power within the vehicle for all types of powertrains – from traditional ICE architectures to the full range of electrified powertrains that require management of higher voltage and power. Key components of our electrical distribution and connection systems 3 Table of Contents portfolio include wire harnesses, terminals and connectors, high-voltage battery connection systems and engineered components. High-voltage battery connection systems include intercell connect boards, bus bars and main battery interface connection systems.

–High-voltage power distribution products control the flow and distribution of high-voltage power throughout electric and hybrid vehicles and include BDUs, which control all electrical energy flowing into and out of high-voltage batteries in electrified vehicles.

–Low-voltage power distribution products and electronic controllers facilitate signal, data and/or power management within the vehicle and include the associated software required to facilitate these functions. Key components of this portfolio include zonal controllers, body domain control modules, and smart and passive power distribution modules. Our software offerings include embedded control, cybersecurity software and software to control hardware devices. Our customers traditionally have sourced our electronic hardware together with the software that we integrate and embed in it.

In our E-Systems business, our broad capabilities in electrical distribution and connection systems; high-voltage power distribution products, including BDUs; and low-voltage power distribution products and electronic controllers support the trend toward electrification, as well as the evolution toward zone-based vehicle electrical architectures for both ICE and electrified powertrains. We are investing in and expanding our electrical distribution and connection systems business. This business is benefiting from expanded content per vehicle in line with higher circuit counts supporting high-speed data movement within the vehicle, as well as high-voltage wire harnesses and high-voltage battery components such as intercell connect boards on electrified powertrains. In addition, we have enhanced our vertical integration capabilities in connection systems through the acquisition of M&N Plastics. Our high-voltage power distribution business, including our BDU business, and our low-voltage power distribution business are benefiting from the increased adoption of electrified powertrains. Differentiation through higher power management capacity, lighter weight solutions, and optimized and vertically integrated manufacturing solutions provide us with a competitive advantage in the electrification market. Our electronic controllers business is benefiting from the adoption of new vehicle electrical architectures with more integrated power management and control, which is aligned with our strong history of providing highly complex and integrated electronics to our customers.…

E-Systems Segment Our E-Systems segment consists of the design, development, engineering and manufacture of complete electrical distribution and connection systems; high-voltage power distribution products, including BDUs; and low-voltage power distribution products and electronic controllers for vehicles globally. We are a leader in signal distribution and power management within the vehicle for all types of powertrains – from traditional ICE architectures to the full range of electrified powertrains. Our expertise and product portfolio support new vehicle electrical architectures, including the adoption of high-voltage electrified vehicle architectures and the transition to zone-based vehicle electrical architectures. We are expanding our capabilities and introducing new product lines, primarily within our electrical distribution and connections systems business and including intercell connect boards, BDUs, engineered components, high-voltage wire, high-speed data cables and zonal controllers. Further, we are de-emphasizing and exiting certain electronics product lines, including audio modules, lighting modules, on-board chargers, telematics control units and niche electronic controllers, where we do not see a path to sustainable risk-adjusted financial returns.

Electrical Distribution and Connection Systems Electrical distribution and connection systems route network and electrical signals and manage electrical power within the vehicle for all types of powertrains, including traditional ICE architectures and the full range of electrified powertrains, supporting the current industry trend toward electrification. Key components of electrical distribution and connection systems 12 Table of Contents include wire harnesses, terminals and connectors, high voltage battery connection systems and engineered components for both ICE architectures and electrified powertrains that require management of higher voltage and power.

Connection systems include terminals and connectors, high-voltage battery connection systems and engineered components that join wire harnesses together at their respective end points or connect electronic devices to wire harnesses. Connection systems can vary significantly in size and complexity depending on the amount of power or data being transferred and the number of connections being made at any particular point in the electrical distribution system. Connection systems support both low-voltage and high-voltage power distribution. Low-voltage connection systems are used on all light duty vehicles and high-voltage connection systems are used on vehicles with electrified powertrains. Our connection systems are produced using highly automated processes, including stamping, injection molding and automated assembly processes. Our connection systems are currently manufactured in Germany, the Czech Republic, Morocco, China and the United States. Key material inputs to our connection systems business include metals, such as copper and aluminum, and various resins.

Engineered components consist of molded components included in wire harness assemblies. These components perform specific functions, such as protection, routing, sealing or covering, to ensure that the wire harness assembly properly performs its function. In 2021, we acquired M&N Plastics, a privately owned injection molding specialist and manufacturer of engineered plastic components for automotive electrical distribution applications, which enabled the significant expansion of our footprint and capabilities with respect to engineered components. Engineered component capabilities are a significant contributor to vertically integrated product assemblies and enable business growth across electrical distribution and connection systems and our Seating business due to increased control of product cost and quality, as well as the supply chain. Engineered components are applicable to all vehicle architectures and are produced using molding processes. Our engineered components are currently manufactured in Germany, the Czech Republic, Morocco, China and the United States. Key material inputs to our engineered components are various resins.

High-Voltage Power Distribution Products, including BDUs In our E-Systems segment, we also design, develop, engineer and manufacture high-voltage power distribution products, including BDUs. These products control the flow and distribution of high-voltage power throughout electric and hybrid vehicles and include BDUs, which control all electrical energy flowing into and out of high-voltage batteries in electric and hybrid vehicles. More than fifteen years of experience in high-voltage power distribution products, together with our expertise in areas integral to the performance of BDUs, such as power and thermal management and electrical architecture integration, have contributed to our well-established market position and our ability to effectively and competitively supply BDUs. High-voltage power distribution products are applicable to all electrified powertrain vehicles, but the size, complexity and configuration can vary widely dependent upon the power requirements of individual vehicle platforms. Our high-voltage power distribution products are currently manufactured in Mexico, China, Spain and Morocco. Key material inputs to our high-voltage power distribution products include metals, including copper and aluminum, various resins, and power components, such as fuses, e-fuses and contactors.

Low-Voltage Power Distribution Products and Electronic Controllers In our E-Systems segment, we also design, develop, engineer and manufacture low-voltage power distribution products and electronic controllers that control various functions and power distribution within the vehicle. Our electronic product offerings include zonal controllers, body domain modules, and smart and passive power distribution units. These units are typically 13 Table of Contents purchased with embedded software to manage vehicle functions, control power distribution and ensure vehicle network connection. We assemble these modules using specialized, high-speed surface mount placement equipment and assembly processes in Mexico, Europe, Morocco and China.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
ITEM 7 – MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS Executive Overview Lear Corporation is a global automotive technology leader in Seating and E-Systems, enabling superior in-vehicle experiences for consumers around the world. We supply complete seat systems, key seat components, complete electrical distribution and connection systems, high-voltage power distribution products, including battery disconnect units ("BDUs"), and low-voltage power distribution products and electronic controllers to all of the world's major automotive manufacturers.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
