你是 stock-analyst v20 DD 的證據採集子 agent。標的：FTV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - FTV Fortive tariff section 232 2026
  - Fortive export control OR entity list Scientific & Technical Instruments 2026
  - FTV Fortive China tariff OR trade restriction 2026
  - Scientific & Technical Instruments tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1659166/000165916626000007/ftv-20251231.htm｜as_of：2026-02-25
<<<
************************************ The following discussion includes information common to all of our segments. Materials Our manufacturing operations employ a wide variety of raw materials, including electronic components, steel, plastics and other petroleum-based products, aluminum, and copper. Prices of oil and gas affect our costs for freight and utilities. We purchase raw materials from a large number of independent sources around the world. Tariffs affect our costs for impacted materials or components we import into the United States. Based on allocation of annual spend among our various suppliers, no single supplier is material. However, some components that require particular specifications or qualifications are dependent on a single supplier or a limited number of suppliers that can readily provide such components. We utilize a number of techniques to address potential disruption in and other risks relating to our supply chain, including in certain cases the use of safety stock, alternative materials that meet the quality and regulatory requirements, and qualification of multiple supply sources.…

Export/Import Regulations We sell products and services to customers all over the world and are required to comply with various U.S. export/import control and economic sanctions laws, such as: •the International Traffic in Arms Regulations administered by the U.S. Department of State, Directorate of Defense Trade Controls, which, among other things, impose license requirements on the export from the United States of defense articles and defense services listed on the United States Munitions List; •the Export Administration Regulations administered by the U.S. Department of Commerce, Bureau of Industry and Security, which, among other things, impose licensing requirements on the export, in-country transfer, and re-export of certain dual-use goods, technology, and software (which are items that have both commercial and military or proliferation applications); •the regulations administered by the U.S. Department of Treasury, Office of Foreign Assets Control, which implement economic sanctions imposed against designated countries, governments, and persons based on United States foreign policy and national security considerations; and •the import regulations administered by U.S. Customs and Border Protection.

Other nations’ governments have implemented similar export/import control and economic sanction regulations, which may affect our operations or transactions subject to their jurisdictions. Together these controls and regulations may impose licensing requirements on exports of certain technology and software from the U.S. and may impact our ability to transact business in certain countries or with certain customers. We have developed compliance programs and training to prevent violations of these programs and regulations, and we regularly monitor changes in the law and regulations. Changes in these or other import or export laws and regulations may restrict or further restrict our ability to sell certain products and solutions and may require us to develop additional compliance programs and training. For a discussion of risks related to export/import control and economic sanctions laws, please refer to “Item 1A. Risk Factors.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1659166/000165916626000007/ftv-20251231.htm｜as_of：2026-02-25
<<<
In 2025, approximately 44% of our sales were derived from customers outside the United States. Our principal markets outside the United States are in Europe and Asia. In addition, many of our manufacturing operations, suppliers, and employees are located outside the United States. Since our growth strategy depends in part on our ability to further penetrate markets outside the United States and increase the localization of our products and services, we expect to continue to increase our sales and presence outside the United States, particularly in high-growth markets, such as Eastern Europe, the Middle East, Africa, Latin America, and Asia. Regional conflicts, including the Russian invasion of Ukraine, conflict in the Middle East, tension between China and Taiwan, could result in sanctions, regional market instability, increased energy and transportation costs, and other adverse regional financial and economic conditions, any of which can impact the demand for, or our ability to sell, our products and services in the impacted regions. Furthermore, our international business, including our business in high-growth markets outside the United States, is subject to additional risks that are customarily encountered in non-U.S.…

As a result, there continues to be significant uncertainty about, and volatility in, the future relationship between the United States and other countries, especially with respect to trade policies, treaties, government regulations, sanctions and tariffs. In particular, there continues to be uncertainty about U.S. foreign trade policy with respect to China, including any changes to the trade policies that have been adopted, and that may result from the IEEPA Ruling, including any alternative legislative or executive actions that may be adopted to reimpose similar tariffs. Any increased sanctions, tariffs, other trade barriers or restrictions or uncertainty on global trade adopted by or against the United States could adversely impact our business and financial results.

In addition to the environmental, health, safety, anticorruption, data privacy, and other regulations noted elsewhere in this Annual Report, our businesses are subject to extensive regulation by U.S. and non-U.S. governmental and self-regulatory entities at the supranational, federal, state, local, and other jurisdictional levels, including the following: •we are required to comply with various import laws and export control and economic sanctions laws, which may affect our transactions with certain customers, business partners, and other persons and dealings between our employees and between our subsidiaries. In certain circumstances, export control and economic sanctions regulations may prohibit the export of certain products, services, and technologies. In other circumstances, we may be required to obtain an export license before exporting the controlled item. Compliance with the various import laws that apply to our businesses can restrict our access to, and increase the cost of obtaining, certain products and at times can interrupt our supply of imported inventory. We may also face audits or investigations by one or more domestic or foreign government agencies relating to our compliance with these regulations.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1659166/000165916626000007/ftv-20251231.htm｜as_of：2026-02-25
<<<
Business Trends Our financial outlook is subject to various assumptions and risks, including but not limited to: ongoing geopolitical events; global economic and consumer trends and sentiments; monetary policies; inflationary pressures on expenses and pricing; uncertainties in governmental policies on international trade, regulations, sanctions, and healthcare; operational challenges from existing, new, or increased tariffs, in some cases, subsequent rollbacks or suspensions; foreign exchange rate volatility, including the impact of unhedged foreign currency debts; reduction in U.S. government spending due to H.R.1, also known as the One Big Beautiful Bill Act (“OBBBA”); and overall fiscal policies, including investment and taxation policy initiatives being considered in the U.S.; the incremental impacts of the Pillar Two initiative from the Organization for Economic Co-operation and Development (“OECD”); and the impact from the Separation.

2.1 % 3.5 % Sales growth in 2025 was driven by favorable pricing of 2.2%, including actions taken to mitigate unfavorable tariff impacts. Volume declined slightly, primarily in professional instrumentation during the first half of the year, partially offset by increases in gas detection products and facilities and asset lifecycle (“FAL”) software and services. Sales growth in 2024 was driven primarily by favorable pricing of 2.7% and volume gains with FAL software and services and gas detection products.

Gross profit 2,641.1 2,619.1 2,477.1 Gross profit margin 63.5 % 64.2 % 63.3 % Gross profit increased during 2025 as compared to 2024, primarily due to favorable pricing, gains from FBS and productivity measures all partially offset by volume declines, higher employee compensation, and discrete restructuring charges. Within the year, the unfavorable impact of tariffs were mitigated by the countermeasures deployed.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTV_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
