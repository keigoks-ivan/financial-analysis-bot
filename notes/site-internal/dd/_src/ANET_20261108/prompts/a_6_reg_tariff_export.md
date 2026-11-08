你是 stock-analyst v20 DD 的證據採集子 agent。標的：ANET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - ANET Arista Networks tariff section 232 2026
  - Arista Networks export control OR entity list Computer Hardware 2026
  - ANET Arista Networks China tariff OR trade restriction 2026
  - Computer Hardware tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
Over the last decade, and especially under the current administration, the U.S. government has enacted various new and increased tariffs affecting the import of various items from various countries. For example, since 2018, the U.S. government has enacted various tariffs on products from China under Section 301 trade authorities, including on communications equipment products and components manufactured and imported from China. Since February 2025, the U.S. has also imposed additional country-specific tariffs on most trading partners, including China, as well as additional commodity-specific tariffs on certain imported items, in both instances pursuant to executive orders issued under various trade authorities, including the International Emergency Economic Powers Act and Section 232 of the Trade Expansion Act of 1962.

In response to these and other U.S. measures, China, Mexico and other countries have taken or threatened to take a range of retaliatory measures. These include the imposition of retaliatory tariffs on certain U.S.-origin goods; the implementation of new export controls by China on various critical minerals, including rare earths metals; the scheduling of further retaliatory tariff measures; and other actions that may affect us directly or indirectly.

An increase in trade-related costs associated with these tariff actions may affect our cost of production, impair the profitability of our international production, affect our ability to procure certain items, strain our suppliers’ ability to provide 15 inputs necessary to produce certain items, and otherwise affect our manufacturing partners’ ability to provide our products at previously contracted prices. We also may not be able to pass on the full burden of the increase in trade-related costs to our partners and/or customers which could impact our profitability and/or our competitiveness. We are adjusting our supply chain and manufacturing practices to minimize the impact of the tariffs and any impact on the supply chain of components sourced from affected countries, but our efforts may not be successful. In addition, there can be no assurance that we will not experience a disruption in our business related to these or other changes in trade practices, and the process of changing suppliers in order to mitigate any such tariff costs could be complicated, time-consuming, and costly.

Tariffs may also cause customers to delay or to request an expedition for their orders as they evaluate where to take delivery of our products in connection with their efforts to mitigate their own tariff exposure. Such delays or expeditions may create forecasting difficulties for us and increase the risk that orders might be canceled or might never be placed. Current or future tariffs may also negatively impact our customers' sales, thereby causing an indirect negative impact on our own sales. Even in the absence of further tariffs, the related uncertainty and the market's fear of escalating trade tensions and related macroeconomic effects might cause our distributors and customers to place fewer orders for our products, which could have a material adverse effect on our business, liquidity, financial condition, and/or results of operations.

Over the past several years, the U.S. government has enacted a series of enhanced international trade restrictions affecting China and other countries which have included additional export controls and sanctions, import regulations and foreign investment regulations. For example, the U.S. has added additional entities, from China and elsewhere, to restricted party lists impacting the ability of U.S. companies to provide products, and in certain cases services, to these entities and, in some cases, receive products or services from these entities. Beginning in October 2022, the U.S. expanded controls restricting the ability to send certain products and technology related to semiconductors, semiconductor manufacturing, and supercomputing. Although new regulations introduced in January 2025 further expanding the controls to impose a worldwide licensing requirement on certain ICs and computing resources that are used for training of AI models were rescinded prior to the scheduled compliance date, we expect the U.S. government may issue new controls on similar technologies in the future. The U.S. government also expanded the scope of restrictions on the development or production of advanced ICs and certain semiconductor manufacturing equipment, and the restrictions on supercomputing, though certain U.S. export controls have been partially relaxed pursuant to the bilateral trade negotiations between the U.S. and China since May 2025. Further changes to any of these policies are possible.

The Chinese government has retaliated to, and may continue to retaliate to, these or other U.S. trade restrictions in ways that could impact our business. For example, China has announced controls on both the use of Micron products and export controls on certain materials used, among other things, in the production of semiconductors, optical components, and other electronic devices including germanium and gallium. These Chinese export controls have been the subject of bilateral trade negotiations between the U.S. and China, and have been partially relaxed since May 2025, though further changes are possible. Further, the Chinese government has responded to these U.S. actions by adding U.S. entities to an unreliable entity list, which limits the ability of companies on the list to engage in business with Chinese customers. These restrictions could disrupt the ability of China to procure or produce semiconductors and other electronics, impact our ability to source components from China, or impact the cost of components or inputs used to produce our products.

From time to time, we may receive inquiries from governmental agencies, or we may make voluntary disclosures regarding our compliance with applicable governmental regulations or requirements relating to various matters, including import/export controls, federal securities laws and tax laws and regulations which could lead to formal investigations. Actual or alleged noncompliance with applicable laws, regulations or other governmental requirements could lead to regulatory investigations, enforcement actions, and other proceedings, private claims and litigation, and potentially may subject us to 39 sanctions, mandatory product recalls, enforcement actions, disgorgement of profits, fines, damages, civil and criminal penalties or injunctions. If any governmental fines, penalties, or other sanctions are imposed, or if we do not prevail in any possible civil or criminal litigation, our business, financial condition, results of operations and prospects could be materially adversely affected. In addition, responding to any investigation, action or other proceeding will likely result in a significant diversion of management’s attention and resources and an increase in professional fees. Enforcement actions, investigations, fines, penalties, and other sanctions could harm our business, financial condition, results of operations and prospects.

Export Controls Our products are subject to various export controls and because we incorporate encryption technology into certain of our products, certain of our products may be exported from various countries only with government authorization. If we were to fail to comply with the applicable export control laws, customs regulations, economic sanctions or other applicable laws, we could be subject to monetary damages or the imposition of restrictions which could be material to our business, operating results and prospects and could also harm our reputation. Further, there could be criminal penalties for knowing or willful violations, including incarceration for culpable employees and managers. Obtaining the necessary export authorizations for a particular sale may be time-consuming and may result in the delay or loss of sales opportunities.

It also is possible that the Chinese government will retaliate to these export controls in ways that could impact our business. For example, China has announced controls on both the use of Micron products and export controls on certain materials used, among other things, in the production of semiconductors, optical components, and other electronic devices 41 including germanium and gallium. These Chinese export controls have been the subject of bilateral trade negotiations between the U.S. and China and have been partially relaxed since May 2025, though further changes are possible. Further, the Chinese government has responded to U.S. actions by adding U.S. entities to an unreliable entity list, which limits the ability of companies on the list to engage in business with Chinese customers. These restrictions could disrupt the ability of China to procure or produce semiconductors and other electronics and impact our ability to source components from China and could impact the cost of components or inputs used to produce our products.

The United States may also continue to leverage the use of “secondary tariffs” and/or “secondary sanctions” to achieve certain foreign policy goals, or increase its enforcement of such tools, which may directly or indirectly affect our business (see also the “Escalated or escalating U.S. tariffs, as well as countermeasures taken by affected countries may have a negative effect on global economic conditions, financial markets and our business, as may retaliatory actions by other countries, including China, in response to these U.S. policies” risk factor above). Even though we take precautions to ensure that we and our channel partners comply with all relevant regulations, any failure by us or our channel partners to comply with such regulations could have negative consequences, including reputational harm, government investigations and penalties. In addition, economic sanctions that are vague and not subject to guidance by regulators lead to heightened compliance risk.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
