你是 stock-analyst v20 DD 的證據採集子 agent。標的：HON。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - HON Honeywell International tariff section 232 2026
  - Honeywell International export control OR entity list Conglomerates 2026
  - HON Honeywell International China tariff OR trade restriction 2026
  - Conglomerates tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：全文（無法依 Item 切段）｜url：https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm｜as_of：2026-02-17
<<<
BUSINESS UPDATE MACROECONOMIC CONDITIONS We continue to monitor macroeconomic and geopolitical developments that continue to be characterized by elevated trade tensions, economic policy uncertainty, and evolving inflationary pressures. While continued global growth proved more resilient than widely anticipated, new tariffs imposed in 2025 and 2026 to date, along with ongoing rollbacks and negotiations, are driving volatility in global markets. Global conflicts, tariffs, labor disruptions, and new regulations continue to generate volatility in global markets and contribute to supply chain vulnerabilities and pricing fluctuations. We remain proactive in our collaboration with suppliers to minimize shortages and mitigate supply chain and price volatility.

See the section titled Risk Factors for a discussion of risks associated with the potential adverse effects of inflationary cost pressures, supply chain disruptions, tariffs and other trade restrictions and barriers, and labor shortages to our businesses.

In addition, the Company and each of its businesses has been, and may continue to be, negatively affected by global macroeconomic conditions, including the impacts of inflation, high interest rates, supply chain and labor disruptions, unemployment rates, geopolitical instability and regional conflicts, the adoption and expansion of, and other changes to, trade restrictions and tariffs, quotas, embargoes, and other related actions, and the occurrence or threat of a trade war or other governmental action related to tariffs or trade agreements or policies. Such factors could adversely impact, demand for our products, our costs, our customers, our suppliers, and the world and U.S. economies. The impact of such factors could have a material adverse effect on our business, operating results, cash flows, and financial condition.

Our international operations, including U.S. exports, represent more than half of the Company’s sales. Risks related to international operations include exchange control regulations, wage and price controls, fluctuations in foreign currency exchange rates, antitrust regulations, employment regulations, foreign investment laws, import, export, and other trade restrictions and barriers (such as tariffs, sanctions, and embargoes), differing levels of protection of intellectual property, acts of industrial espionage, violations by our employees or business partners of anti-corruption or anti-money-laundering laws (despite our efforts to mitigate such risk), changes in regulations regarding transactions with state-owned enterprises, nationalization of private enterprises, acts of terrorism, acts of war, civil strife, and our ability to hire and maintain qualified staff and maintain the safety of our employees in these regions. Instability and uncertainties arising from the global geopolitical environment and the evolving international and domestic political, 30 Honeywell International Inc.

Existing free trade laws and regulations provide certain beneficial duties and tariffs for qualifying imports and exports. Changes in laws or policies governing the terms of foreign trade, and in particular increased trade restrictions, tariffs, or taxes on imports from countries where we manufacture products or from where we import products or raw materials, either directly or through our suppliers, could have an impact on our competitive position and financial results.

The U.S. continues to implement certain trade actions, including imposing tariffs on certain goods imported from China and other countries, which has resulted in retaliatory tariffs by China and other countries. The recent changes in U.S. trade policy involving the application or increase of tariffs and the subsequent retaliatory measures against the U.S. have created a dynamic environment that may have a material adverse impact on our business. While we have deployed strategies to mitigate the impact of these dynamic trade policies, there is no assurance that we will be able to mitigate the full impact of all such tariffs, retaliatory tariffs or other trade policies that have or may develop in this rapidly changing environment. Increasing trade tensions and changes in trade policies have the potential to adversely impact our costs, the demand for our products, our supply chain and the global economy, and could result in fines and penalties or reputational harm if we are found not to be in compliance, which may have an adverse impact on our business, including operating and financial results and conditions.

In response to the conflict between Russia and Ukraine, the U.S. and other countries imposed actions including sanctions, export and import controls, and trade restrictions with respect to Russian and Belarusian governments, government-related entities, and other entities and individuals. Further, the Russian government implemented retaliatory actions against the U.S. and other nation members of the North Atlantic Treaty Organization (NATO) as well as certain other nations. Given the uncertainty inherent in our remaining obligations related to our contracts with Russian counterparties, we do not believe it is possible to develop estimates of reasonably possible loss in excess of current accruals for these matters. As the conflict continues to evolve, existing conditions may worsen, or other impacts, including escalation of the conflict in other regions of Europe where there is a material portion of our business, increased tension between Russia and the U.S. and other NATO members and other countries, or other impacts that are unknown at this time, could lead to increased charges and could have a material adverse effect on our consolidated financial position. These impacts may result in increased costs or additional impacts on our operations and may adversely affect our ability to meet contractual and financial obligations, results of operations, and financial condition.

Many major components, product equipment items, and raw materials, particularly in Aerospace Technologies, are procured or subcontracted on a single or sole-source basis. Although we maintain a qualification and performance surveillance process and we believe that sources of supply for raw materials and components are generally adequate, it is difficult to predict what effects shortages or price increases, in addition to other supply chain disruptions, may have in the future. Our ability to manage inventory and meet delivery requirements may be constrained by our suppliers’ inability to scale production and adjust delivery of long-lead time products during times of volatile demand. In addition, current or future global economic uncertainty, including inflation and high interest rates, supply chain and labor disruptions, tariffs and other trade barriers and restrictions, unemployment rates, banking instability, any U.S. government shutdown, any downgrades in the U.S. government's sovereign credit rating, public health crises, volatile financial markets, geopolitical instability and regional conflicts, and potential recession may affect the financial stability of our key suppliers or their access to financing, which may in turn affect their ability to perform their obligations to us.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
