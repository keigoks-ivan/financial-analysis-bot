你是 stock-analyst v20 DD 的證據採集子 agent。標的：FTNT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - FTNT Fortinet tariff section 232 2026
  - Fortinet export control OR entity list Software - Infrastructure 2026
  - FTNT Fortinet China tariff OR trade restriction 2026
  - Software - Infrastructure tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm｜as_of：2026-02-25
<<<
Adverse economic conditions, such as a possible recession and possible impacts of inflation or stagflation, tariffs or other trade disruptions, changing interest rates, reduced information technology spending, including firewall and other security spending, or any economic downturn or recession, may adversely impact our business.

Any efforts to withdraw from or materially modify international trade agreements, change tax provisions related to global manufacturing and sales or impose new tariffs, economic sanctions or related legislation, could adversely affect our financial condition and results of operations.

Moreover, efforts to implement changes related to export or import regulations (including the imposition of new or increases in border taxes or tariff rates, changes in customs or tariffs classifications or modifications to tariff exemptions on foreign imports), trade barriers, economic sanctions and other related policies could harm our results of operations. While we do not currently expect tariffs to have a significant effect on our raw material and product import costs, if the United States expands increased tariffs, changes in customs or tariffs classifications or modifications to tariff exemptions or if retaliatory trade measures are taken by other countries in response to the U.S. tariffs, the cost of our products could increase, our operations could be disrupted or we could be required to raise our prices, which may result in the loss of customers and harm to our reputation and operating performance. U.S. tariffs, and any new or additional retaliatory tariffs that may be imposed by foreign countries, may also adversely affect our customers and, consequently, demand for our products. We are monitoring this evolving situation and there can be no assurance that we will be able to mitigate the impacts of any trade measures on our business, which could adversely impact our business, operating results, financial condition, and our stock price.

We market and sell our products throughout the world and have established sales offices in many parts of the world. Our international sales have represented a majority of our total revenue in recent periods. Therefore, we are subject to risks associated with having worldwide operations. We are also subject to a number of risks typically associated with international sales and operations, including: •disruption in the supply chain or in manufacturing or shipping, or decreases in demand by channel partners or end-customers, including any such disruption or decreases caused by factors outside of our control such as international trade disputes or tariffs, labor or supply chain disruptions, inflation and other cost increases, international conflicts, terrorism, wars, such as the war in Ukraine, tensions between China and Taiwan, conflicts in the Middle East, critical infrastructure attacks, natural disasters, health emergencies, epidemics and pandemics, power outages and civil unrest; •fluctuations in foreign currency exchange rates or a weakening of the U.S. dollar, as a significant portion of our expenses are incurred and paid in currencies other than the U.S.…

•management communication and integration problems resulting from cultural differences and geographic dispersion; and •changes in tax, tariff, employment and other laws.

Our business is subject to regulation by various federal, state, regional, local and foreign governmental agencies, including agencies responsible for monitoring and enforcing employment and labor laws, workplace safety, product safety, product labeling, environmental laws, consumer protection laws, anti-bribery laws, data privacy laws, import and export controls, federal securities laws and tax laws and regulations. In certain jurisdictions, these regulatory requirements may be more stringent than in the United States. Non-compliance with applicable regulations or requirements could subject us to investigations, sanctions, enforcement actions, disgorgement of profits, fines, damages and civil and criminal penalties or injunctions. If any governmental sanctions are imposed, or if we do not prevail in any possible civil or criminal litigation, our business, operating results and financial condition could be adversely affected. In addition, responding to any action will likely result in a significant diversion of management’s attention and resources and an increase in professional fees. Enforcement actions and sanctions could harm our business, operating results and financial condition.

Because we incorporate encryption technology into our products, certain of our products are subject to U.S. export controls and may be exported outside the United States only with the required export license or through an export license exception, or may be prohibited altogether from export to certain countries. If we were to fail to comply with U.S. export laws, U.S. Customs regulations and import regulations, U.S. economic sanctions and other countries’ import and export laws, we could be subject to substantial civil and criminal penalties, including fines for the company and incarceration for responsible employees and managers, and the possible loss of export or import privileges. In addition, if our channel partners fail to obtain appropriate import, export or re-export licenses or permits (e.g., for stocking orders placed by our partners), we may also be adversely affected through reputational harm and penalties and we may not be able to provide support related to appliances shipped pursuant to such orders. Obtaining the necessary export license for a particular sale may be time-consuming and may result in the delay or loss of sales opportunities.

41 Table of Contents Furthermore, U.S. export control laws and economic sanctions prohibit the shipment of certain products to U.S. embargoed or sanctioned countries, governments and persons, such as the sanctions and trade restrictions that have been implemented against Russia and Belarus. Even though we take precautions to prevent our product from being shipped to U.S. sanctions targets, our products could be shipped to those targets by our channel partners, despite such precautions. Any such shipment could have negative consequences including government investigations and penalties and reputational harm. In addition, various countries regulate the import of certain encryption technology, including import permitting and licensing requirements, and have enacted laws that could limit our ability to distribute our products or could limit our customers’ ability to implement our products in those countries. Changes in our products or changes in export and import regulations may create delays in the introduction of our products in international markets, prevent our customers with international operations from deploying our products globally or, in some cases, prevent the export or import of our products to certain countries, governments or persons altogether.…

Economic uncertainty in various global markets caused by political instability and conflict, such as the war in Ukraine, tensions between China and Taiwan or conflicts in the Middle East has resulted, and may continue to result in weakened demand for our products and services and difficulty in forecasting our financial results and managing inventory levels. Geopolitical developments impacting government spending and international trade, including potential government shutdowns and trade disputes and tariffs may negatively impact markets and cause weaker macroeconomic conditions. The effects of these events may continue due to potential U.S. government shutdowns, the transition in administrations, changing in the U.S. government’s trade policy and the United States’ ongoing trade disputes with Russia, China and other countries, including the United States’ tariffs, and any new or additional retaliatory tariffs from foreign countries. For example, the Chinese government recently instructed domestic companies in certain industries not to use cybersecurity products manufactured by the companies 47 Table of Contents based in the United States or Israel, including us and certain of our competitors. The continuing effect of any or all of these events could adversely impact demand for our products, harm our operations and weaken our financial results.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm｜as_of：2026-02-25
<<<
59 Table of Contents Impact of Macroeconomic and Geopolitical and Supply Chain Developments Our overall performance depends in part on worldwide economic and geopolitical conditions, such as trade policies and tariffs, GDP growth or contraction (both domestically and internationally), geopolitical instability and uncertainty, the war in Ukraine, tensions between China and Taiwan or conflicts in the Middle East, and their impact on customer behavior. Worsening economic conditions, including tariffs, inflation, changing interest rates and other trade disruptions, slower growth, any recession, fluctuations in foreign exchange rates and other changes in economic conditions, may result in decreased sales productivity, lower growth and adversely affect our results of operations and financial performance. We have seen, and could continue to see, certain impacts on our business, results of operations, financial condition, cash flows, liquidity and capital and financial resources such as longer sales cycles, delayed purchases and increased commitments with certain suppliers and increased inventory and inventory purchase commitment reserves. Tariffs imposed by the United States, as well as any new or additional retaliatory tariffs that could be imposed by other countries in response, could have a material adverse impact on global trade, supply chains and other worldwide economic and geopolitical conditions, which could increase our product costs and also affect customer sentiment in deciding whether to purchase our products.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTNT_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
