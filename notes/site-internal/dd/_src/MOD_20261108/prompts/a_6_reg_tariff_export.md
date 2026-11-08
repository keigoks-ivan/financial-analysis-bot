你是 stock-analyst v20 DD 的證據採集子 agent。標的：MOD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - MOD Modine Manufacturing tariff section 232 2026
  - Modine Manufacturing export control OR entity list Building Products & Equipment 2026
  - MOD Modine Manufacturing China tariff OR trade restriction 2026
  - Building Products & Equipment tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
​ 6 Table of Contents During fiscal 2026, the commercial vehicle market in India experienced strong growth, while the commercial vehicle markets in Brazil and China were relatively flat. In North America and Europe, the commercial vehicle markets experienced continued weakness during 2026. Uncertainties, including those related to the impacts of tariffs, geopolitical tensions and emissions regulations, have been negatively impacting the commercial vehicle markets. While we expect market softness will continue in fiscal 2027, we are optimistic that the medium- and heavy-duty truck markets may begin to recover based upon recent OEM order trends and reported outlooks. In North America, we are monitoring the U.S. Environmental Protection Agency’s upcoming Greenhouse Gas Phase 3 regulations for commercial vehicles, which include stricter emission regulations for heavy-duty trucks starting with the 2027 model year. If these regulations are significantly rolled back or eased, it would likely dampen the anticipated surge of heavy-duty truck orders prior to the new regulations going into effect.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
​ ​ 13 Table of Contents Changes in U.S. or international trade policies, including the imposition of or increases in tariffs, could adversely affect our business, financial position, results of operations and cash flows.

There is uncertainty regarding future relationships between the U.S. and numerous other countries, particularly China, Canada, Mexico, and in Europe, with respect to trade policies, tariffs, treaties, and government regulations. Changes in U.S. policies could lead to changes to existing trade agreements, significant increases in tariffs, more restrictions on free trade, and restrictions on the importation of certain goods and components into the U.S. or other countries. A trade war or escalation of trade tensions, including increased tariffs and retaliatory measures by foreign governments, should they be sustained for an extended period of time, or changes in U.S. or international trade agreements, could negatively impact our supply chain, increase costs, and reduce demand for our products. Changes to or uncertainty in the marketplace related to U.S. social, political, regulatory and economic conditions or in laws and policies related to foreign trade in countries where we currently manufacture and sell our products, and any resulting negative sentiments towards the U.S., could adversely affect our business, financial position, results of operations and cash flows.

In February 2026, the U.S. Supreme Court ruled that tariffs imposed in 2025 under the International Emergency Economic Powers Act were invalid (the “IEEPA Ruling”). However, other tariffs remain in effect and trade policies are unpredictable. There is also uncertainty with regard to the IEEPA Ruling, including the availability and timing of refunds, the potential for new tariffs to be invoked under alternative laws, the impacts on trade agreements between the U.S. and other countries, and the expectations of customers, suppliers, and others impacted by the tariffs. In addition, the rapid evolution, reversal, or replacement of trade measures following the IEEPA Ruling may contribute to increased policy volatility and uncertainty, which could complicate planning, pricing, sourcing, and contractual arrangements.

Increases in the costs of raw materials and other purchased components, which may be impacted by a variety of factors, including changes in trade laws, tariffs, sanctions, geopolitical and military conflicts, inflation, the behavior of our suppliers and significant fluctuations in demand, could have a significant negative impact on our results of operations. In the shorter-term, our ability to adjust for cost increases is limited when prices are fixed for current orders. In these cases, if we are not able to recover such cost increases through price increases to our customers, such cost increases will have an adverse effect on our results of operations. With regard to our longer-term sales programs, we have sought to reduce the risk of cost increases by including provisions within our customer contracts, where possible, which provide for prospective price adjustments based upon increases and decreases in the cost of key raw materials. However, where these contract provisions are applicable, there can often be a three-month to one-year lag until the time of the price adjustment. To further mitigate our exposure, from time to time we enter into forward contracts to hedge a portion of our forecasted aluminum and copper purchases.…

Strong or rapidly increasing demand, including significant or unanticipated increases in demand for certain components driven by elevated levels of capital investment in end markets such as data centers, as well as the potential effects of trade laws and tariffs, sanctions, geopolitical and military conflicts, capacity constraints, financial instability, public health crises, such as pandemics and epidemics, or other circumstances experienced by our suppliers could result in shortages or delays in their supply of product to us, or significant price increases. In certain cases, such demand may exceed available market supply for key components, limiting our ability to obtain sufficient quantities from existing or alternative suppliers. We began experiencing supply shortages of certain data center product components in the fourth quarter of fiscal 2026, which are negatively impacting our production schedules for the first quarter of fiscal 2027. If we experience significant or prolonged shortages of critical components or materials from our suppliers and could not procure the components or materials from other sources, we may be unable to meet our production schedules and could miss product delivery dates, which would adversely affect our sales, results of operations, cash flows and customer relationships.

We experience competition from companies in other parts of the world that enjoy economic advantages, such as lower labor costs, lower health care costs, lower tariff or tax rates, lower costs associated with legal compliance, and, in some cases, export or raw materials subsidies. In addition, consolidation and vertical integration within the supply base have introduced new or restructured competitors to our markets. Increased competition could adversely affect our business and results of operations.

Changes in policies or laws governing the terms of foreign trade, and in particular increased trade restrictions, tariffs or taxes on imports from countries where we either manufacture products or buy raw materials, such as Mexico, China, and Canada, could have a material adverse impact on our results of operations. Certain of our current manufacturing facilities in Mexico operate under the Mexican Maquiladora (IMMEX) program, which provides for reduced tariffs and eased import regulations. We could be adversely affected by changes in the IMMEX program or our failure to comply with its requirements. Regarding imported goods and raw materials, increased tariffs or taxes on purchases from countries, such as China, could materially impact our results of operations if we cannot effectively source such goods and raw materials from other suppliers in the U.S. or alternative countries. In addition, compliance with multiple and often conflicting laws and regulations of various countries can be challenging and expensive.

Embargoes or sanctions imposed by the U.S. government or those abroad that restrict or prohibit sales to or purchases from specific persons or countries or based upon product classification may expose us to potential criminal and civil sanctions to the extent that we are alleged or found to be in violation, whether intentional or unintentional. In connection with the military conflict with Iran, the U.S. government has expanded sanctions against Iran, including entities involved in Iran’s oil transportation infrastructure and countries that trade with Iran. In addition, governments in the U.S. and abroad have extended and expanded sanctions against Russia and entities known to be supporting Russian interests, including on certain companies located in countries in which we operate, including China, Germany, and Serbia. We do not have manufacturing operations in the Middle East, Ukraine, or Russia, nor any significant business relationships in or associated with Iran, Ukraine or Russia, however we are continuing to monitor the sanctions requirements and reacting as necessary to ensure compliance. We cannot predict future regulatory requirements to which our business operations may be subject or the manner in which existing laws might be administered or interpreted. Significant developments or changes in these regulatory requirements could have a material adverse impact on our results of operations and cash flows.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
Performance Technologies cost of sales decreased $6 million, or 1 percent, in fiscal 2026, primarily due to lower sales volume and, to a lesser extent, improved operating efficiencies. These drivers, which decreased cost of sales, were partially offset by higher raw material costs, which increased $10 million and included the impact of tariffs, and a $21 million unfavorable impact of foreign currency exchange rates. As a percentage of sales, cost of sales increased 170 basis points to 81.9 percent, primarily due to the higher raw material and tariff costs, partially offset by improved operating efficiencies and higher average selling prices.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
