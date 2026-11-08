你是 stock-analyst v20 DD 的證據採集子 agent。標的：MTSI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - MTSI MACOM Technology Solutions Holdings tariff section 232 2026
  - MACOM Technology Solutions Holdings export control OR entity list 半導體 / 光通訊 / RF 2026
  - MTSI MACOM Technology Solutions Holdings China tariff OR trade restriction 2026
  - 半導體 / 光通訊 / RF tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm｜as_of：2025-11-14
<<<
Export Regulations We market and sell our products both inside and outside the U.S. Most of our products are subject to the Export Administration Regulations, administered by the U.S. Department of Commerce, Bureau of Industry and Security (“BIS”). Certain of our products and technology require an export license from BIS before we can export them to specified countries. Our European products and technologies are subject to the European Union Dual-Use Regulation (EU) No. 2021/821 (the “EU Regulation”), which governs the export of certain goods, software and technology that can be used for both civil and military applications. Certain of our products and technology require an export license under the EU Regulation before we can export them to specified countries. Similar controls exist in other jurisdictions. Additionally, some of our products are subject to the International Traffic in Arms Regulation (in the U.S.) and the EU Common Military List and French Defense Code (in France), which govern the export of military products and technology to foreign persons. Failure to comply with these laws could result in sanctions by the government, including substantial monetary penalties, denial of export privileges and debarment from government contracts. These regulations are constantly changing and may affect our ability to sell certain products in certain markets.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm｜as_of：2025-11-14
<<<
We have operations in Europe and Asia, and customers around the world. As a result, we are subject to regulatory, geopolitical and other risks associated with doing business outside of the U.S., including currency controls, currency exchange rate fluctuations, new or potential international trade agreements, tariffs, required import and export licenses, and other related international trade restrictions and regulations. Further, there is a risk that language barriers, cultural differences and other factors associated with our global operations may make them more difficult to manage effectively.

Sales to customers located outside the U.S. accounted for 56.3% of our revenue for the fiscal year ended October 3, 2025. Sales to customers located in China and the Asia Pacific region typically account for a large portion of our overall sales to customers located outside the U.S. For example, fiscal year 2025 sales to customers in China and the Asia Pacific region accounted for 28.4% and 11.5% of total fiscal year 2025 sales, respectively. We expect that revenue from international sales generally, and sales to China and the Asia Pacific region specifically, will continue to be a material part of our total revenue. Therefore, any financial crisis, trade war or dispute, domestic semiconductor supply chain initiatives, health crisis or other major event causing business disruption in international jurisdictions generally, and China and the Asia Pacific region in particular, could negatively affect our future revenues and results of operations. For example, in October 2022 and 2023, the BIS introduced restrictions related to semiconductor manufacturing, supercomputer and advanced computing items and end-uses, which restrict or prohibit the ability to sell, ship and support certain equipment and services to China.…

Adverse global economic conditions, including as a result of evolving impacts from global tariffs, sanctions or other trade tensions, and our ability to effectively respond to rapidly changing rules and regulations, could negatively impact our business, results of operations and financial condition and liquidity.

A slowdown in the global economy or in a particular region or industry, uncertainty and volatility in financial markets and other unfavorable changes in economic conditions, such as inflation or major central bank policy actions, as well as an increase in trade tensions and related tariffs, including, but not limited to, the implementation of new tariffs and retaliatory trade measures, could negatively impact our business, financial condition and liquidity. In addition, as rules and regulations rapidly change across multiple jurisdictions, we could be negatively impacted by any failure to effectively respond to such changes. These risks may be particularly acute in the semiconductor industry, where cyclical demand patterns and rapid technological changes can amplify economic headwinds.

Adverse global economic conditions have, in the past, caused significant slowdowns in the industries and markets in which we operate, adversely impacting our business and results of operations. Macroeconomic weakness and uncertainty may also make it more difficult to accurately forecast operating results and raise or refinance debt. An escalation of trade tensions between the United States and its trading partners has resulted in trade restrictions and tensions that may harm our ability to participate in some markets or compete effectively and could limit our ability to sell products in certain markets or source components from specific suppliers, potentially disrupting our supply chain and manufacturing capabilities. Sustained uncertainty about, or worsening of, current global economic conditions and further tariffs and escalations of trade tensions between the U.S. and its trading partners and the decoupling of the global economies could result in an economic slowdown and long-term changes to global trade. Such events may also (i) cause our customers to reduce, delay or forgo technology spending, (ii) result in customers sourcing products from other suppliers not subject to restrictions or tariffs, (iii) intensify pricing pressures and (iv) lead to the insolvency or consolidation of key suppliers and customers. Any or all of these factors could negatively impact demand for our products and our business, financial condition and results of operations.

Changes in U.S. Government Administration Could Materially Affect Our Business, Financial Condition and Results of Operations We operate in a highly regulated industry, and changes in the U.S. political landscape can significantly impact our business. Changes in the U.S. Government Administration may result in substantial modifications to laws and regulations, including, but not limited to, those related to trade policies, tariffs, export controls and technology transfers. New executive orders and legislative actions could alter the business environment in which we operate.

Our future results could be adversely affected by changes in interpretations of existing laws and regulations, or changes in laws and regulations, including, among others, changes in accounting standards, taxation requirements, competition laws, trade laws, import and export restrictions, privacy laws and environmental laws in the U.S. and other countries. The U.S. government has implemented 21 tariff and other trade control policies, and may take further actions, that have led to, and may lead to further, changes to U.S. and international export and import controls or trade policies, including tariffs affecting certain products exported by a number of U.S. trading partners, including China. In response, many of those trading partners, including China, have imposed or proposed new or higher tariffs on American products and export controls related to China’s rare earth metals. It is unknown whether and to what extent new tariffs, export control measures or other new laws or regulations will be adopted, or the effect that any such actions would have on us or our industry and customers.…

If we fail to comply with export control regulations, we could be subject to substantial fines or other sanctions, including loss of export privileges.

Certain of our products are subject to the Export Administration Regulations, administered by the BIS, which require that we obtain an export license before we can export products or technology to specified countries. Other products are subject to the International Traffic in Arms Regulations, which restrict the export of information and material that may be used for military or intelligence applications by a foreign person. Ongoing export control reform that has changed and is expected to continue to change rules applicable to us in the future in ways we do not yet fully understand and we have experienced and will continue to experience challenges in complying with the new rules as they become effective, resulting in difficulties or an inability to ship products to certain countries and customers.

We are also subject to U.S. import regulations and the import and export regimes of other countries in which we operate. Failure to comply with these laws could result in sanctions by the U.S. government, including substantial monetary penalties, denial of export privileges and debarment from government contracts. Any change in export or import regulations or related legislation (or the interpretation thereof), shift in approach by regulators to the enforcement or scope of existing regulations, specific sanctions by regulators or change in the countries, persons or technologies targeted by such regulations, could harm our business by resulting in decreased use of our products by, or our decreased ability to export or sell our products to, existing or potential customers with international operations. In addition, our sale of our products to or through third-party distributors, resellers and sales representatives creates the risk that any violation of these laws they may engage in may disrupt our markets or otherwise bring liability on us.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1493594/000149359425000054/mtsi-20251003.htm｜as_of：2025-11-14
<<<
Certain areas of our end markets continue to be negatively impacted by macroeconomic and geopolitical conditions, which we expect may result in weaker near-term demand for our products across all three of our primary markets. In addition, we could be negatively affected by any weakening of global economic conditions, including as a result of the evolving impacts from tariffs, export bans, sanctions or other trade tensions (including implementation of new tariffs or retaliatory trade measures).
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
