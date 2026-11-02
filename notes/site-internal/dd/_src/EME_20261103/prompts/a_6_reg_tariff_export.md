你是 stock-analyst v20 DD 的證據採集子 agent。標的：EME。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - EME EMCOR Group tariff section 232 2026
  - EMCOR Group export control OR entity list Engineering & Construction 2026
  - EME EMCOR Group China tariff OR trade restriction 2026
  - Engineering & Construction tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/105634/000010563426000025/eme-20251231.htm｜as_of：2026-02-26
<<<
Volatility in the prices or availability of certain materials, equipment, and commodities used in our businesses and those of our customers, including as a result of inflation, supply chain disruptions, geopolitical instability, and protectionist trade measures, could adversely affect our businesses. We are exposed to market risk of increases in certain commodity prices of materials, such as copper and steel, which are used as components of supplies or materials utilized in our operations. We are also exposed to increases in energy prices, particularly as they relate to gasoline prices for our fleet of approximately 14,400 vehicles. While we believe we can increase our prices to adjust for some price increases in commodities, there can be no assurance that price increases of commodities, if they were to occur, would be recoverable. Further, the timing of our price increases may lag the timing of the underlying increases in commodity or material prices and certain of our contracts do not allow us to adjust our prices. As a result, increases in material or fuel costs could reduce our profitability with respect to projects in progress. Additionally, we rely on third-party vendors and manufacturers to supply much of the materials and equipment necessary for our operations.…

Changes in U.S. foreign trade policies could lead to the imposition of additional trade barriers and tariffs. We cannot predict the full extent of new, extended, or changed trade policies, including tariffs, that may be made by the current or a future presidential administration or Congress, including whether existing tariff policies will be maintained or modified or if changes in the U.S. trade policy could result in reactions from U.S. trading partners, such as adopting responsive trade policies making it more difficult or costly for us to purchase materials or supplies. Judicial review of certain trade policies and the potential consequences of court decisions on challenges to such policies, including tariffs imposed by executive order, could result in 9 Table of Contents additional changes to, or reversal of, such trade policies and practices. Changes in U.S. trade policy or in laws and policies governing foreign trade, and any resulting negative sentiments towards the United States as a result of such changes, could have an adverse impact on our business, financial position, results of operations, and liquidity.

Our failure to comply with anti-bribery statutes, such as the Foreign Corrupt Practices Act, or sanction regulations, could result in fines, criminal penalties, and other sanctions that could have an adverse effect on our business. The U.S. Foreign Corrupt Practices Act (the “FCPA”), and similar anti-bribery laws in other jurisdictions, generally prohibit companies and their intermediaries from making improper payments to foreign officials for the purpose of obtaining or retaining business or securing an improper advantage. In addition, sanctions against foreign persons and entities have increased in recent years, especially in connection with the war in Ukraine and ongoing trade and diplomatic disputes between the U.S. and China. Our policies require that all of our employees, subcontractors, vendors, and agents worldwide must comply with applicable anti-bribery and sanction laws. However, there is no assurance that our policies and procedures to ensure compliance with the FCPA and similar anti-bribery and sanction laws will eliminate the possibility of liability under such laws for actions taken by our employees, agents, and intermediaries.…

We may be unable to achieve our current or future climate commitments and targets, or we may incur substantial costs in meeting such targets. To help mitigate the impacts of GHG emissions on climate change, EMCOR has established initial carbon-based fuel consumption and GHG emission reduction targets. However, achievement of such targets, or similar targets that may be established in the future, is subject to risks and uncertainties, many of which are outside of our control. These risks and uncertainties include, but are not limited to: (a) our ability to execute our operational strategies and achieve our goals within the currently projected costs and the expected timeframes; (b) the availability and cost of alternative fuels, electrical charging infrastructure, off-site renewable energy, and other materials and components; (c) unforeseen design, operational, and technological difficulties; (d) the outcome of research efforts and future technology developments, including alternate or more fuel efficient vehicles for our fleet, such as hybrid or electric vehicles, the availability and prices of which have been and may in the future be impacted by the rescission of electric vehicle tax credits, tariffs imposed on the import of vehicles to the United States, and other disruptions to the global supply of vehicles generally; (e) regulations and requirements that restrict or prohibit our ability to impose requirements on third-party contractors; (f)…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
