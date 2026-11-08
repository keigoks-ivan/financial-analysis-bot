你是 stock-analyst v20 DD 的證據採集子 agent。標的：SN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - SN SharkNinja tariff section 232 2026
  - SharkNinja export control OR entity list Furnishings, Fixtures & Appliances 2026
  - SN SharkNinja China tariff OR trade restriction 2026
  - Furnishings, Fixtures & Appliances tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm｜as_of：2026-03-02
<<<
We are also subject to U.S. and foreign laws and regulations that govern or restrict our business and activities in certain countries and with certain persons, including the U.S. Commerce Department’s Export Administration Regulations and economic and trade sanctions regulations maintained by OFAC, as well as anti-bribery and anti-corruption laws and regulations, including the FCPA and the U.K. Bribery Act 2010.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm｜as_of：2026-03-02
<<<
As a result of this international business, we are exposed to increased risks inherent in conducting business outside of the United States. These risks include the following: •adverse changes in foreign currency exchange rates can have a significant and adverse effect upon our business, financial condition and results of operations; •increased difficulty in protecting our intellectual property rights and trade secrets, including litigation costs and the outcome of such litigation in jurisdictions outside the United States; •increased exposure to events that could impair our ability to operate internationally with third parties such as problems with such third parties’ operations, finances, insolvency, labor relations, manufacturing capabilities, costs, insurance, natural disasters, public health emergencies or other catastrophic events; •unexpected legal or government action or changes in legal or regulatory requirements; •difficulties in managing, growing and staffing international operations, including in countries in which foreign employees may become part of labor unions, employee representative bodies or collective bargaining agreements, and challenges relating to work stoppages or slowdowns; •social, economic or political instability; •potential negative consequences from changes to taxation or tariff policies; •increased difficulty in ensuring compliance by employees, agents and contractors with our policies as well as with the laws of multiple jurisdictions, including, but not limited to, the U.S. Foreign Corrupt Practices Act (the “FCPA”) and the U.K.…

Some of the products we manufacture require particular types of glass, metal, paper, plastic, resin, wood, electronics or other materials. Lead times for these items vary significantly and are increasing in light of global shortages of critical components, including semi-conductors. Supply shortages for a particular type of material can delay production or cause increases in the cost of manufacturing our products. Pricing and availability of finished goods, raw materials, energy, transportation and other necessary supplies and services can be volatile due to numerous factors beyond our control, including general, domestic and international economic conditions, supply chain issues, natural disasters, labor costs, production levels, competition, consumer demand, import duties and tariffs, currency exchange rates, international treaties and changes in laws, regulations and related interpretations.

The United States and various foreign governments recently have adopted measures to oppose the use of forced labor. Governments, including the U.S. government, also have imposed sanctions and export control restrictions with respect to entities that are deemed to have engaged in, or supported the use of, forced labor. We have strong policies against the use of forced labor and do not tolerate this practice within our company or by our suppliers. While we do not expect that our operations will be directly impacted by any government measures 26 targeting forced labor, it is possible that customs authorities could detain shipments of goods based on concerns over the possible use of forced labor, resulting in delays, litigation, damages and reputational harm. Likewise, we cannot rule out the possibility that in the future one of our suppliers could be named to a sanctions or restricted party list, such as the U.S. Department of Commerce’s Bureau of Industry and Security Entity List, based on concerns over forced labor, with similar negative effects on our reputation, business, financial condition and results of operations.

Significant changes to U.S. trade policies that restrict imports or increase import tariffs and the responses of other countries have had, and we will expect will continue to have, a material adverse effect on our business.

There is currently significant uncertainty about the future relationship between the United States and various other countries, including China, the European Union, Canada and Mexico, with respect to trade policies, treaties, tariffs and customs duties. In particular, the U.S. government has imposed or announced new or additional tariffs on products imported from certain countries, and some countries have responded with new or increased tariffs of their own. The amount of the import tariff and the number of products subject to tariffs have changed multiple times based on actions by the U.S. government. For example, on February 20, 2026, the United States Supreme Court issued a ruling striking down certain tariffs previously imposed under the International Emergency Economic Powers Act (“IEEPA”). Following the Supreme Court’s decision, the U.S. presidential administration announced its intention to invoke other laws to collect tariffs and announced new tariffs on imports from all countries, in addition to any existing non-IEEPA tariffs. There remains substantial uncertainty regarding the duration of existing and newly announced tariffs, potential changes or pauses to such tariffs, tariff levels, and whether further additional tariffs or other retaliatory actions may be imposed, modified, or suspended, and the impacts of such actions on our business. These imposed and announced tariffs have impacted, or have the potential to impact, our imports from other countries.…

A significant proportion of our products are manufactured in China, Vietnam and other regions outside of the United States. Accordingly, such U.S. policy changes have made it, and may continue to make it, difficult or more expensive for us to obtain certain products manufactured outside the United States, which have affected and could continue to affect our net sales and profitability. At this time, it remains unclear what additional actions, if any, will be taken by the U.S. or other governments with respect to international trade agreements, the imposition of tariffs on goods imported into the U.S., tax policies related to international commerce, export controls, sanctions and investment restrictions, import or use of foreign communications equipment, or other trade matters. Retaliatory tariff and trade measures imposed by other countries could affect our ability to export products and therefore adversely affect our net sales. Any of these factors could depress economic activity and restrict our access to suppliers, retailers or consumers and could have a material adverse effect on our business, financial condition and results of operations as well as affect our strategy in China, Vietnam and elsewhere around the world. There can be no assurance that any tariff exposure mitigation efforts we take will be successful.

The United States and various foreign governments have imposed controls, export license requirements and restrictions on the import or export of certain products, as well as customs and other import regulatory requirements. Our products may be subject to U.S. export controls. Compliance with applicable regulatory requirements regarding the import and export of our products may create delays in the introduction of our products in international markets and, in some cases, prevent the export of our products to some countries altogether. Over the past year, several countries have imposed far-reaching export controls with respect to geopolitical conflicts in addition to export control measures targeting certain industries. We do not believe our products are directly impacted by these recent measures, but we cannot rule out the possibility that these measures could have an indirect negative impact on our business and our ability to source certain products from key jurisdictions.

Furthermore, the U.S. Department of the Treasury’s Office of Foreign Assets Control (“OFAC”) and other relevant agencies of the U.S. government administer certain laws and regulations that restrict U.S. persons and, in some instances, non-U.S. persons, from conducting activities, transacting business with or making investments in certain countries or with governments, entities and individuals subject to U.S. economic sanctions. Similar economic sanctions are imposed by the European Union and other jurisdictions. Sanctions may evolve rapidly and with far-reaching impact on global business—for example, over the past year, the United States, the United Kingdom, the European Union, as well as certain other countries have imposed multiple rounds of significant sanctions in response to geopolitical conflicts. Our international operations subject us to these laws and regulations, which are complex, restrict our business dealings with certain countries, governments, entities and individuals and are constantly changing. Penalties for noncompliance with these complex laws and regulations can be significant and include substantial fines, sanctions or civil and/or criminal penalties and violations can result in adverse publicity, which could harm our business, financial condition and results of operations. Business could be conducted with targets of U.S. sanctions or conducted by our retailers. Any such business could have negative consequences, including government investigations, penalties and reputational harm.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm｜as_of：2026-03-02
<<<
Gross Profit and Gross Margin Gross profit reflects net sales less the cost of sales. Cost of sales primarily consists of the purchase cost of our products from third-party manufacturers, inbound freight costs, tariffs, product quality testing and inspection costs, the costs associated with receiving inventory into our warehouses, depreciation on molds and tooling that we own, warranty costs, damages, obsolescence and shrinkage costs and allocated overhead, including the service fee paid to JS Global for supply chain services.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SN_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
