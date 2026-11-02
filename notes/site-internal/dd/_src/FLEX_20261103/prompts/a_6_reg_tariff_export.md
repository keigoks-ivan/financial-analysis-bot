你是 stock-analyst v20 DD 的證據採集子 agent。標的：FLEX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - FLEX Flex tariff section 232 2026
  - Flex export control OR entity list Electronic Components (EMS) 2026
  - FLEX Flex China tariff OR trade restriction 2026
  - Electronic Components (EMS) tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
•Tariffs, trade restrictions, export controls, and changes in trade policy, including heightened trade volatility and uncertainty regarding trade agreements, have in the past adversely affected, and could in the future adversely affect, our business, results of operations, and financial condition.

•We are subject to complex and evolving trade policies, export controls and sanctions.

Our supply chain has in the past been, and could in the future be, impacted by events outside our control, including macro-economic events, tariffs and trade restrictions, political crises, social unrest, terrorism, and geopolitical conflicts (including the conflicts in Ukraine and the Middle East, including the conflict in Israel, recent U.S. military operations in Iran, disruptions in the Strait of Hormuz, attacks on shipping vessels in the Red Sea, and other regional tensions), public health emergencies, or natural or environmental occurrences in locations where we or our customers and suppliers have manufacturing, research, engineering and other operations.

Tariffs, trade restrictions, export controls, and changes in trade policy, including heightened trade volatility and uncertainty regarding trade agreements, have in the past adversely affected, and could in the future adversely affect, our business, results of operations, and financial condition.

Political developments and trends and sentiment toward multinational companies have resulted in, and may continue to result in, tariffs, export controls, trade restrictions, and other barriers, as well as changes to tax and other laws and policies. These measures have been, and are expected to continue to be, disruptive to our business and may impact our global operating model, supply chain, production costs, customer relationships, customer demand and competitive position. Such measures can be imposed suddenly and unpredictably.

Throughout 2025 and into 2026, the U.S. administration imposed varying levels of tariffs on goods imported from China and other countries where we or our customers source materials and manufacture products. Further escalation of trade tensions, including through the imposition of new or increased tariffs (including retaliatory tariffs), expanded trade restrictions, or intensified decoupling between the U.S. (as well as other major economies) and China or other key trading partners could materially increase our product input costs, negatively affect global economic conditions, contract customer demand, or otherwise adversely affect our business. Related declines in confidence or investment activity in global markets could further adversely affect our business performance.

As a global manufacturing and supply chain services partner with operations, suppliers, and customers across multiple jurisdictions, we have been, and expect to continue to be, impacted by tariffs and trade actions through the timing and mechanics of cost recovery and operational complexity. We generally seek to pass tariff costs through to our customers, which can affect reported net sales, operating income margins, and the timing of operating cash flows as tariffs are paid and subsequently recovered. To the extent we are unable to recover tariff costs from certain customers, or experience delays in doing so, our results of operations and cash flows could be adversely affected. The actual impact of tariffs and related trade measures on our business depends on numerous factors, including their scope, effective date, duration, magnitude, products and countries covered, customer contract terms, and the imposition of retaliatory or reciprocal measures by other countries.

In addition, changes to, or uncertainty surrounding, international trade agreements may adversely affect our business. Existing trade agreements, including the United States‑Mexico‑Canada Agreement (“USMCA”), provide preferential tariff treatment and other benefits for qualifying imports and exports, subject to compliance with applicable rules of origin, classification, and other requirements. The USMCA is subject to a joint review process in 2026, and there can be no assurance 25 Table of Contents that the agreement will not be amended, suspended, or terminated, or that its benefits will not be reduced. Any material modification to, or withdrawal from, the USMCA, or the imposition of additional tariffs or trade restrictions affecting North America, could result in increased costs, supply chain disruptions, delays in shipments, additional compliance burdens, or the need to modify sourcing or manufacturing strategies, which could materially adversely affect our business, financial condition, and results of operations.

Recent legal and policy developments have also increased uncertainty regarding the enforceability, duration, and potential re‑imposition of certain tariffs. For example, on February 20, 2026, the U.S. Supreme Court struck down certain tariffs imposed under the International Emergency Economic Powers Act ("IEEPA"). Following that decision, the U.S. administration announced a new 10% global tariff under Section 122 of the Trade Act of 1974, subject to certain exceptions; however, on May 7, 2026, the U.S. Court of International Trade ruled that the Section 122 tariffs were not authorized by law, a decision the administration has appealed. These and similar developments have created uncertainty regarding the future rate, scope, and enforceability of tariffs; the availability and timing of refunds for tariffs that may be invalidated; the potential adoption of alternative legislative or executive actions; and the continued effectiveness of trade arrangements or mitigation actions adopted in response to prior tariffs. Ongoing uncertainty regarding U.S. and global trade policies, sanctions, and tariffs, including actions involving China, North America, and other key manufacturing and sourcing jurisdictions, could adversely affect our business, financial condition, and results of operations.

Changes in U.S. and foreign government policies, including those relating to trade, sanctions, information security, data privacy, national security, and foreign investment, may affect the attractiveness of our services to customers and our ability to conduct business with certain customers or suppliers. We have significant operations in China, which have been, and could continue to be, affected by evolving laws, regulations, and geopolitical developments involving China. We could be subject to reputational harm if any of our customers, former customers or vendors were subject to U.S. sanctions or did business with sanctioned entities or countries or otherwise violated applicable sanctions or export control laws. Furthermore, regional conflicts, including the conflicts in Ukraine and the Middle East, including the conflict in Israel and recent U.S. military operations in Iran, and tension between China and Taiwan, could result in sanctions, regional market instability, increased energy and transportation costs, supply chain disruptions, and other adverse regional and global financial and economic conditions, any of which can impact the demand for, or our ability to sell, our products and services in the impacted regions.…

We are subject to complex and evolving trade policies, export controls, and sanctions, and failure to comply or adapt to changes in these regimes could restrict our business or result in significant penalties.

Due to the global nature of our business, we are subject to a complex system of import- and export-related laws and regulations in the U.S. and other countries, including economic sanctions administered by the U.S. Department of the Treasury's Office of Foreign Assets Control and similar regimes in other jurisdictions. Our products, services, and technology are regulated by these trade control and customs regimes and in some cases require licenses or other authorizations. Our ability to obtain and maintain such licenses and authorizations on a timely basis, or at all, is subject to risks and uncertainties, including changing laws, regulations, foreign policies, and geopolitical factors. Non-compliance by us, our customers, or our suppliers can result in denial of export privileges, fines, criminal penalties, administrative sanctions, seizure of inventory, import detention, and loss of business. Delays or denials of licenses can prevent or defer sales, and previously recognized revenue and profit may need to be reversed. Moreover, we could be subject to reputational harm if any of our customers, former customers, or vendors were subject to U.S. sanctions or conducted business with sanctioned countries. Any restrictions on the export or import of our products could have a material adverse effect on our competitive position, results of operations, financial condition, or liquidity.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
Tariffs The U.S. tariffs initially announced in April 2025, which continue to evolve, and other countries' potential retaliatory tariffs and import/export restrictions may materially increase our product input costs and negatively affect global economic conditions, contracting customer demand. As a contract manufacturer, we expect to recover the cost of tariffs by passing tariff costs to our customers which would increase net sales, decrease operating income margins, and negatively affect operating cash flow timing as we recover paid tariffs from our customers. During the fiscal year ended March 31, 2026, tariff costs paid and recoveries from our customers impacted our revenues and costs of goods by approximately one percent and had a negligible impact on our profitability. If, in the future, we are no longer able to fully pass through these tariffs, our results from operations and cash flows would be negatively impacted. On February 20, 2026, the U.S. Supreme Court struck down tariffs imposed under the International Emergency Economic Powers Act ("IEEPA") and on April 20, 2026 the U.S. government opened a system to facilitate refunds for IEEPA tariffs paid. We are considering our options with respect to claims for refunds on tariffs paid and do not expect that any refunds received would have a material effect on Flex's financial position or performance.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
