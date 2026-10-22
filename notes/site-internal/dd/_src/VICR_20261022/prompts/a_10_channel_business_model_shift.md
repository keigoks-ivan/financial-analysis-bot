你是 stock-analyst v20 DD 的證據採集子 agent。標的：VICR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Vicor distribution channel disruption OR shift 2026
  - VICR Vicor business model transition subscription OR platform 2026
  - 半導體 — 電源管理 / AI 加速器電源 channel disintermediation D2C 2026
  - Vicor go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm｜as_of：2026-03-02
<<<
Our earliest market focus was on telecommunications infrastructure, which uses a standard DC distribution voltage of 48V (nominally 48V to 54V), the highest distribution voltage that meets Safety Extra-Low Voltage (“SELV”) standard requirements, while leaving sufficient margin for over-voltage protection circuits. While we offer products addressing other DC voltage standards (e.g., 380V for power distribution in data centers, 110V for rail applications, 28V for military and avionics applications, and 24V for industrial automation) and a broad range of customer requirements, we consider our core competencies to be associated with 48V distribution, which offers numerous inherent cost and performance advantages over lower distribution voltages, while remaining within the 60V SELV safety limit.

Reflecting our strategy, we categorize our offerings as either Advanced Products or Brick Products, generally based on design, performance, and form factor considerations, as well as the range of evolving applications for which the respective categories are appropriate. The Advanced Products category consists of our most innovative products, which are used to implement our proprietary distribution architecture, FPA, a highly differentiated approach to power distribution that enables flexible, rapid power system design using individual components optimized to perform a specific function. The Brick Products category largely consists of integrated power converters (i.e., “bricks”), incorporating multiple conversion stages, used in conventional power systems architectures including CPA, DPA, and IBA.

4 Table of Contents Advanced Products We continue to invest in the research and development of power system technologies and product concepts addressing two accelerating trends, the first toward higher required conversion efficiencies, and the second toward more and diverse on-board voltages, higher performance demands of complex loads, and, in particular, higher current requirements of those loads. These trends are most visible in the microprocessor-based applications we target with Advanced Products, for which energy consumption, energy efficiency, processor performance, and computing density are critical priorities. Recognizing the performance and scale limitations of conventional power distribution architectures and products, we introduced FPA and a range of enabling products incorporating our latest advances in power distribution concepts, switching topologies, materials, and packaging.

FPA, which is focused on, but not limited to, 48V DC distribution solutions, increases power system conversion efficiency, density, and power delivery performance by “factorizing” (i.e., separating) the power conversion process into individual components, reducing the design limitations and thermal management challenges, and scaling trade-offs associated with conventional architectures for DC voltage distribution. All such architectures follow a sequence whereby a DC voltage is first transformed, or reduced, and that lower voltage subsequently conducted (i.e., “bussed”) across the circuit to the “load” (i.e., the point of use), where the voltage is regulated and lowered once more, to the required operating voltage of the load. In a FPA implementation, the sequence is reversed. Regulation occurs first, and the regulation module can be placed in the optimal position for space utilization and thermal management. A regulated voltage approaching 48V is bussed across the circuit to the transformation module, which performs what we refer to as current multiplication, adjacent to the load. Bussing high voltage minimizes the current levels across the circuit, thereby minimizing the potential for distribution losses and reducing the volume of the conduit (e.g., the copper wire).…

The advantages of FPA over legacy power distribution architectures are most evident in high performance computing applications. Our “Power-on-Package” power system solutions meet the computational performance requirements of artificial intelligence (“AI”). The microprocessors typically used in AI, particularly in more computationally demanding “machine learning” or “training” applications, are graphics processing units (“GPUs”) and custom application-specific integrated circuits (“ASICs”). Unlike central processing units (“CPUs”), which are designed for serial execution of complex and broad instruction sets, GPUs and AI ASICs are designed for massively parallel (i.e., concurrent) processing of repetitive transactions or calculations. As such, GPUs and AI ASICs generally operate at processing frequencies requiring the higher levels of average and peak current delivered by our FPA-based solutions. Our most popular Power-on-Package solution, consists of one MCD© (Modular Current Driver) unit, providing high-bandwidth, low-noise regulation, and two MCM© (Modular Current Multiplier) units, providing high performance current multiplication. Power-on-Package delivers unprecedented current levels to GPUs and AI ASICs, in part due to the placement of the MCMs directly on the substrate onto which the processor is mounted, thereby minimizing distribution losses associated with high current levels. Placement of MCM units on the substrate also reduces the number of GPU or ASIC processor substrate pins required for power, allowing for their use by other functions (e.g., memory input/output (“I/O”)).…

Our proprietary technologies enable us to offer a range of Advanced Products, in various package formats across functional families, applicable to other market segments and power distribution architectures other than FPA. Within computing, these market segments include AC to DC voltage conversion and DC voltage distribution in server racks and high voltage conversion across datacenter infrastructure. We also offer Advanced Product power system solutions for aerospace and aviation (e.g., for use in satellites, unmanned aerial vehicles, and various airframes, including battery-powered aircraft, for which small size, light weight, and design flexibility are advantageous); defense electronics (e.g., for use in airborne, seaborne, or field communications and radar, for which reliability in harsh environments is a priority); factory automation, instrumentation, and test equipment (e.g., for use in robotics and semiconductor testing, for which high power levels and precision performance are required); telecommunications and networking infrastructure (e.g., for use in high-throughput data distribution and pole-mounted small-cell base stations); and vehicles (e.g., in autonomous driving applications, electric vehicles, and hybrid electric vehicles).

Marketing and Sales We reach and serve customers through several sales channels: a direct sales force; independent, authorized non-stocking distributors in Europe and Asia; and four authorized stocking distributors world-wide: Arrow Electronics, Inc., Digi-Key Corporation, Avnet Electronics, and Mouser Electronics, Inc. All sales channels are supported by regional TSCs, each offering application engineering and sales support for our channel partners. Domestic TSCs are located in: Andover, Massachusetts; Lombard, Illinois; and Santa Clara, California. International TSCs are located in: Beijing, China; Hong Kong, China; Shanghai, China; Shenzhen, China; Munich, Germany; Bangalore, India; Milan, Italy; Tokyo, Japan; Seoul, South Korea; Singapore; Taipei, Taiwan (Republic of China); and Camberley, United Kingdom. Customers do not place purchase orders with TSCs, but do so directly with the Company or with our channel partners. In Japan, customers place purchase orders with authorized distributors or, for certain custom products, VJCL.

Because of the technically complex nature of our products and the applications they address, we maintain an extensive staff of Field Applications Engineers to support our own sales and customer support activities, as well as those of our channel partners. Field Application Engineers, based in our TSCs, provide direct technical support worldwide by reviewing new applications and technical matters with our channel partners in support of existing and potential customers. Product Development Engineering is located in our Andover headquarters, where our Product Development Engineers support the Field Application Engineers assigned to all of our TSCs.

Our direct sales force focuses on higher-volume opportunities involving Advanced Products with global OEMs (and the Original Design Manufacturers (“ODMs”) and contract manufacturers serving these OEMs). Because of the high level of product differentiation and the increasing complexity and challenges of customer requirements, we have experienced, and may continue to experience, extended design cycles before production orders are received.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/751978/000119312526085102/vicr-20251231.htm｜as_of：2026-03-02
<<<
We design, develop, manufacture, and market modular power components and power systems for converting electrical power for use in electrically-powered devices. Our competitive position is supported by innovations in product design and achievements in product performance, largely enabled by our focus on the research and development of advanced technologies and processes, often implemented in proprietary semiconductor circuitry, materials, and packaging. Many of our products incorporate patented or proprietary implementations of high-frequency switching topologies enabling power system solutions that are more efficient and much smaller than conventional alternatives. Our strategy emphasizes demonstrable product differentiation and a value proposition based on competitively superior solution performance, advantageous design flexibility, and a compelling total cost of ownership. While we offer a wide range of alternating current (“AC”) and direct current (“DC”) power conversion products, we consider our core competencies to be associated with 48V DC distribution, which offers numerous inherent cost and performance advantages over lower distribution voltages. However, we also offer products addressing other DC voltage standards (e.g., 380V for power distribution in data centers, 110V for rail applications, 28V for military and avionics applications, and 24V for industrial automation).
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
