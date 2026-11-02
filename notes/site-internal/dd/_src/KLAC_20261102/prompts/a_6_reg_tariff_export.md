你是 stock-analyst v20 DD 的證據採集子 agent。標的：KLAC。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - KLAC KLA tariff section 232 2026
  - KLA export control OR entity list Semiconductor Equipment & Materials 2026
  - KLAC KLA China tariff OR trade restriction 2026
  - Semiconductor Equipment & Materials tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
Export controls, sanctions and other trade-related regulations issued by Commerce and other governmental authorities may limit our ability to sell certain products or provide certain services to certain customers, particularly in 11 Table of Contents China, and may significantly harm our business, results of operations, financial condition and cash flows, unless we are able to obtain required licenses.

We maintain significant operations outside the United States, and existing and evolving trade restrictions imposed by the U.S. and other governments could significantly disrupt our global operations. The U.S. government has tightened export controls for commodities, software, and technology (collectively, “items”) destined to China over the past several years. These controls have included, for example, restrictions on exporting certain items to military end users and for military end uses, the addition of numerous entities to the U.S. Entity List (a list of parties that are generally ineligible to receive U.S.-regulated items without prior licensing from Commerce), and the creation of new licensing requirements that apply to the export, re-export, and transfer of certain foreign-made items that are the direct product of U.S.-origin technology or produced by a plant or major component of a plant that itself is the direct product of U.S.-origin technology and that are destined to Huawei or its affiliates and other specified companies on the U.S. Entity List, and other facilities in China where the production of advanced node ICs occurs.

In October 2022, Commerce published the 2022 BIS Rules, which introduced restrictions related to semiconductor, semiconductor manufacturing, supercomputer and advanced computing items and end uses. These rules impose restrictions on our ability to sell, ship and support certain equipment and otherwise conduct business with certain counterparties, primarily including China-based companies involved in advanced semiconductor manufacturing. Further, the 2022 BIS Rules impose restrictions on the activities of U.S. persons with respect to certain items that are not subject to the Export Administration Regulations (“EAR”), which departs from Commerce’s typical practice of controlling items that are subject to the EAR and could further restrict our ability to conduct business in China. In October 2023, Commerce issued the 2023 BIS Rules designed to update export controls on advanced computing semiconductors and semiconductor manufacturing equipment, as well as items that support supercomputing applications and end uses, to certain D1, D4 and/or D5 countries in Supplement No. 1 of Part 740 of the U.S. EAR, including China. The 2023 BIS Rules adjust the parameters included in the 2022 BIS Rules that determine whether an advanced computing chip is restricted and impose new measures to address risks of circumvention of the controls established by the 2022 BIS Rules.

In September 2025, Commerce released an interim final rule that further expands export control restrictions and licensing requirements for foreign entities 50% or more directly or indirectly owned by one or more listed parties on the U.S. Entity List, Military End-User List, and certain entities on the Specially Designated Nationals and Block Persons List, which Commerce has labeled the “Affiliates Rule.” The new rule increases compliance requirements with the EAR by imposing on exporters, re-exporters, and transferors of items subject to the EAR a responsibility to know the ownership of the parties to a transaction. In November 2025, the BIS suspended the Affiliates Rule for one year until November 2026.

Commerce may continue to add China-based entities to the U.S. Entity List and impose other end use or end user export restrictions, which could disrupt or prevent our product shipments to China-based entities, and further disrupt our revenue recognition, business operations and our ability to support our customers in China.

These rules and regulations may significantly harm our business unless we are able to obtain required licenses. We will continue to apply for export licenses, when required, in an effort to avoid disruption to our and our customers’ operations, but there can be no assurance that export licenses applied for by either us or our customers, now or in the future, will be granted. To the extent Commerce does issue licenses to us or to our customers, such licenses may have a short duration or require us to satisfy various conditions. If pending and future export license applications are not granted, or additional restrictions are imposed, or if regulators adopt new interpretations of existing regulations, the potential impact on us could be material by disrupting our supply chain and product shipment, impairing our ability to complete product development in a timely manner, or our ability to support existing customers of covered products or supply customers of covered products outside the impacted regions, and requiring us to transition certain operations out of one or more of the identified countries.…

Recently announced and future U.S. tariffs, retaliatory trade measures and other trade restrictions, as well as uncertainty regarding tariff authority, implementation and refund processes, may have a material adverse impact on our results of operations.

In 2025, the U.S. implemented a number of tariffs on goods imported into the U.S., on a country and industry-specific basis (including aluminum, copper and steel). While some of the U.S. tariffs have been paused, certain U.S. tariffs are currently in effect, including a base tariff on nearly all imports into the U.S., certain reciprocal tariffs by country, and certain sectoral tariffs on copper, aluminum and steel, among others. In retaliation to the tariffs imposed on U.S. imports, a number of other countries announced reciprocal tariffs on goods imported from the U.S. While most countries paused their reciprocal tariffs on U.S. imported goods, those reciprocal tariffs could be reinstated at any time. Tariffs imposed by the U.S. on goods imported into the U.S. and tariffs imposed by other countries on U.S. goods imported into those countries may continue to evolve.

In April 2025, Commerce announced the initiation of investigations into the effects on U.S. national security of imports of semiconductors under Section 232 of the Trade Expansion Act of 1962. The scope of the investigations includes semiconductors, semiconductor manufacturing equipment and their derivative products, including semiconductor substrates and bare wafers, legacy chips, leading-edge chips, microelectronics and other components. While the results of the investigations are currently unknown, they may result in additional tariffs and trade restrictions, which may adversely impact our business.

In February 2026, the U.S. Supreme Court ruled that tariffs imposed under the International Emergency Economic Powers Act were not authorized, creating uncertainty around the status of prior tariffs, potential refund processes and the scope of future presidential tariff authority. This ruling adds volatility to an already fluid tariff environment and may result in rapid changes in tariff rates, shifts in enforcement, delays in customs processing and increased uncertainty in supply chain and capital planning for us and our customers.

The U.S. tariffs have increased our cost of revenues due to the increase in the cost of importing foreign sourced components to our U.S. facilities to build the products that we manufacture in the U.S. Tariffs imposed on U.S. goods by other countries may harm demand for our products from customers in those regions, or may cause our customers in those regions to push out or cancel previously placed purchase orders. In addition, we have had to return deposits given to us by our customers upon cancellation of their purchase orders. Moreover, tariffs can make it difficult for us and our customers and suppliers to make and execute business and capital equipment investment plans or increase supply chain complexity, which may have an impact on our ability to source the materials necessary to manufacture our products.

Unless rescinded or exemptions apply, tariffs and any escalations in the trade war could significantly harm our business, financial condition and results of operations.

We are subject to various risks related to compliance with laws, rules and regulations enacted by legislative bodies and/or regulatory agencies in the countries in which we operate and with which we must comply, including environmental, safety, antitrust, anti-corruption/anti-bribery, unclaimed property, conflict minerals and other responsible sourcing practices, economic sanctions and export control regulations. We have policies and procedures designed to promote compliance with applicable laws, but there can be no assurance our policies and procedures will prove completely effective in ensuring compliance by all our personnel, business partners and representatives, for whose misconduct we may under some circumstances be legally responsible. Our failure or inability to comply with existing or future laws, rules or regulations in the countries in which we operate could result in government investigations and/or enforcement actions, which could result in significant financial cost (including investigation expenses, defense costs, assessments and criminal or civil penalties), reputational harm and other consequences that may adversely affect our operating results, financial condition and ability to conduct our business. For instance, in response to the war between Russia and Ukraine, the U.S., the European Union and other countries have imposed sanctions against Russia, Belarus and certain other regions, entities and individuals, and may impose additional sanctions, export controls or other measures.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
