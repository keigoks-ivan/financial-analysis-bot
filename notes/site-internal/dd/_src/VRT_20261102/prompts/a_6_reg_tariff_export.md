你是 stock-analyst v20 DD 的證據採集子 agent。標的：VRT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - VRT Vertiv Holdings Co tariff section 232 2026
  - Vertiv Holdings Co export control OR entity list Electrical Equipment & Parts 2026
  - VRT Vertiv Holdings Co China tariff OR trade restriction 2026
  - Electrical Equipment & Parts tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm｜as_of：2026-02-13
<<<
Our operations, particularly our manufacturing and service operations, depend on raw materials, components, products and services from third-party suppliers, and such suppliers’ ability to timely deliver the quantities and quality required at acceptable prices. Successful operations depend on our ability to accurately anticipate these needs and prices. We have a large number of providers to support our global operations and breadth of offerings, some of whom are also competitors of ours in one or more parts of our business and those suppliers may decide to discontinue business with us. As described in our prior filings, at times in the past we did not accurately anticipate the magnitude of inflationary cost increases and customs duties and tariffs for our materials, freight and labor, which resulted in such cost increases not being immediately reflected in the prices for our offerings. Other supply chain issues that we have faced, and may face in the future include, but are not limited to, the following: •Volatility in the supply or price of raw materials, freight and labor - Our products rely on a variety of raw materials and components, including steel, copper, aluminum and various electronic components. We may experience a shortage of, or a delay in receiving, such materials or components because of strong demand, supplier constraints or other operational disruptions.…

War and conflict, such as the conflict in the Middle East, the ongoing Russian-Ukraine war, and any associated diplomatic measures or resulting sanctions by the U.S., European Union, and other countries may have a broad range of adverse impacts on global business and financial markets, some of which may have adverse impacts on our business. These include increased inflation, significant market disruptions, increased volatility in commodity prices, the imposition of additional tariffs by the U.S. on certain of its trading partners, which could trigger retaliatory tariffs by those trading partners, and the possibility of additional potential tariffs or other trade restrictions by the U.S. on other jurisdictions. The U.S. government and other governments in jurisdictions in which we operate may impose severe sanctions and export controls. Any sanctions imposed or actions taken by the U.S. or other countries, and any retaliatory measures could increase our costs, reduce our sales and earnings or otherwise have an adverse effect on our operations.

Serving a global customer base requires that we place more materials, production and service assets in emerging markets to capitalize on market opportunities and maintain our cost position. Emerging geographic markets may be relatively less profitable due to the investments needed to enter such markets and local pricing pressures, and we may have difficulty establishing and maintaining the operating infrastructure necessary to support the high growth rates associated with some of those markets. Manufacturers in countries that have lower production costs, such as China and 21 Table of contents India, may become competitors in key emerging markets and could offer their products in established markets. These actions may have a negative effect on our pricing, market share and operating results in these markets. In addition, foreign governments may decide to implement tax and other policies that favor their domestic manufacturers at the expense of international manufacturers. Similarly, the potential imposition of retaliatory tariffs or additional tariffs or modifications of free-trade agreements by the U.S. on other countries or regions, could increase our cost of doing business internationally, perhaps significantly, and may lead to further challenges for us in the various foreign markets in which we operate.

We operate manufacturing facilities worldwide and continue to expand and open new facilities in different locales. Our manufacturing facilities and operations could be disrupted by natural disasters, labor strikes, shortages in suppliers, components and parts, war, political unrest, terrorist activity, economic upheaval, changes in governmental regulations, including but not limited to regulations regarding taxes, tariffs, custom duties, restricted and/or sanctioned parties, government mandated shutdowns or shelter in place orders, or public health concerns. Some of these conditions are more likely in certain geographic regions in which we operate. Any such disruption could cause delays in the manufacture and/or shipments of products, performance of services, and the loss of sales and customers, and insurance proceeds may not adequately compensate for losses.

We are subject to various anti-corruption laws, including the U.S. Foreign Corrupt Practices Act ("FCPA"), which prohibit payments or offers of payments to foreign governments and their officials for the purpose of obtaining or retaining business. We operate in several less-developed regions that are recognized as having a greater risk of potentially corrupt business environments and, in certain circumstances, strict compliance with anti-corruption laws may conflict with local customs and practices. Our legal compliance and ethics programs and policies, including our code of business conduct, existing policies on anti-bribery, export controls, environmental and other legal compliance, and periodic training on these matters, mandate compliance with anti-corruption laws and are designed to reduce the likelihood of a compliance violation. In the event that we have reason to believe that our employees or business partners have or may have violated applicable laws, regulations or policies, including anti-corruption laws, we are required to investigate the relevant facts and circumstances, which can be expensive and require significant time and attention from senior management. Nevertheless, such a violation could still occur, disrupting our business through fines, penalties, diversion of internal resources, negative publicity and possibly severe criminal or civil sanctions.

We, and certain of our products (including components of such products), are subject to applicable import laws, export controls and economic sanctions laws and regulations, including rule changes, evolving enforcement practices, and other government actions. Changes in import and export control or trade sanctions laws, the imposition of tariffs on certain U.S. trading partners, the potential for or imposition of retaliatory tariffs, or the potential for or imposition of additional tariffs or other trade restrictions, including potential control from China on rare earth elements, may increase our costs, and may restrict our business practices, including cessation of business activities in sanctioned countries or with sanctioned entities, and may result in claims for breach of existing contracts and modifications to existing compliance programs and training schedules. While we train our employees to comply with these regulations and have systems in place designed to prevent failure of compliance, we cannot provide assurance that a violation will not occur, whether knowingly or inadvertently. Violations may result in penalties, including fines, debarments from export and import privileges, and loss of authorizations or certifications needed to conduct aspects of our international business, and may harm our ability to enter into contracts with our customers and suppliers who have contracts with the U.S. government.…

There is currently significant uncertainty about the future relationship between the U.S. and various other countries with respect to trade policies and tariffs. For example, the current U.S. administration has instituted substantial changes to U.S. foreign trade policy with respect to China and other countries, including a significant increase in tariffs on goods imported into the U.S. and the possibility of imposing further restrictions on international trade. The current administration has taken a different approach to U.S. foreign trade policy than their predecessors, so there remains uncertainty as to whether, and to what degree, trade between the U.S and other countries, including countries in which we operate, will be impacted by these policy shifts on an ongoing and/or long-term basis. Additional policy changes or continued uncertainty could depress economic activity and restrict our access to suppliers or customers. Furthermore, counter- or retaliatory tariffs imposed against the U.S. could impact our sales internationally. Tariffs implemented on our products (or on materials, parts or components we use to manufacture our products or to provide service for our products) have in the past increased the cost of our products manufactured in the U.S. and imported into the U.S.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm｜as_of：2026-02-13
<<<
Outlook and Trends Below is a summary of trends and events that are currently affecting, or may in the future affect, our business, operations and short-term outlook: •Trade and Economic Uncertainty: The global trade and economic environment continues to evolve rapidly with the imposition of new U.S. tariffs and retaliatory tariffs being imposed by foreign countries. In response to these escalating pressures and the geopolitical and macroeconomic uncertainties surrounding global supply chains and customer demand, we continue to pursue our supply chain strategy of supplier and geographic resilience. This includes, but is not limited to, continuing to add regional sourcing and manufacturing capabilities and capacity to complement our existing global supply chain. We’re strengthening our supply base and manufacturing footprint in the U.S. and other strategic jurisdictions around the world as part of our overall capacity strategy to grow with customer demand in the U.S. and other jurisdictions.

The imposition of U.S. tariffs and foreign country retaliatory tariffs, or the proposed imposition of additional or similar tariffs, in jurisdictions where we have manufacturing facilities or where our customers operate could increase our cost of doing business and could significantly impact our financial performance.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VRT_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
