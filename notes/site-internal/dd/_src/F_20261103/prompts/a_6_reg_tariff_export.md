你是 stock-analyst v20 DD 的證據採集子 agent。標的：F。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - F Ford Motor tariff section 232 2026
  - Ford Motor export control OR entity list Auto Manufacturers 2026
  - F Ford Motor China tariff OR trade restriction 2026
  - Auto Manufacturers tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
Macroeconomic, Market, and Strategic Risks With a global footprint and supply chain, Ford’s results and operations have been and could continue to be adversely affected by economic or geopolitical developments, including protectionist trade policies such as tariffs, or other events. Because of the interconnectedness of the global economy, financial crises, economic downturns or recessions (including reduced consumer spending), pandemics, natural disasters, wars, social unrest, geopolitical crises, or other significant events in one market can have an immediate and material adverse impact on other markets where Ford operates. Unprecedented trade policy (including tariffs) in the United States and foreign governments’ reactions limit our ability to conduct effective long-term planning and make capital allocation decisions. The continued strain in U.S.-China relations presents unique risks to U.S. automakers, as does China’s unique regulatory landscape, the level of integration with key components in our global supply chain, the limited availability of various components and materials (including certain rare earth minerals and related products from China), and the rapid development of the Chinese EV industry, with Chinese electrified vehicle manufacturers exporting their products to some key markets in which we operate.

Item 1A. Risk Factors (Continued) Changes in international trade policy can also have a substantial adverse effect on our financial condition, results of operations, or our business in general. To the extent governments in various regions implement or intensify restrictions or barriers to trade, such as tariff or non-tariff barriers, export controls, currency manipulation, or policies that otherwise favor domestic companies, there can be a significant negative impact on manufacturers based in other markets. Steps taken by governments to implement local content requirements, restrict export and import activities, or apply or consider applying additional or new tariffs on automobiles, parts, and other products and materials have disrupted supply chains, imposed additional costs on our business, and led to other countries attempting to retaliate by imposing tariffs or other barriers, which make our products more expensive for customers, and, in turn, our products less competitive, and this trend may continue. Tariffs implemented to date in the United States and elsewhere have caused significant disruption, increased costs, and uncertainty in the automotive industry, including for Ford, other OEMs, suppliers, and dealers, as well as customers. Moreover, tariffs implemented or increased in the United States and elsewhere in the future may exacerbate these impacts. The U.S.…

In addition, instability in the supply chain exacerbated by tariffs and other industry concerns, such as China’s restriction on the export of rare earth minerals and various components, has resulted in production disruptions and increased costs and heightens the risk of future production disruptions and further cost increases. Although there is uncertainty regarding the application, scope, and duration of tariffs, those that have been implemented have had a significant adverse effect, both operationally and financially, on the overall automotive industry, Ford, and our supply chain. Any additional tariffs or other measures that are implemented in the United States and any retaliatory tariffs or other measures or restrictions that are implemented by other governments, and the potential related market impacts, should they be sustained for an extended period of time, may have a significant adverse effect.

With operations in various markets with volatile economic or political environments and our global supply chain and utilization of transportation routes and logistics providers around the world, we are exposed to heightened risks as a result of economic, geopolitical, or other events. This could include governmental takeover (i.e., nationalization) of our manufacturing facilities or intellectual property, restrictive exchange or import controls, changes to international trade agreements, disruption of operations as a result of systemic political or economic instability, social unrest, outbreak of war or expansion of hostilities, and acts of terrorism, each of which could impact our supply chain as well as our operations. These events could also have a substantial adverse effect on our financial condition, results of operations, or our business in general. Changes in trade policy may also restrict or limit the ability of logistics providers and customs brokers to process imports timely, which may delay or disrupt our operations and increase our costs. Further, the U.S. government, other governments, and international organizations could impose additional sanctions or export controls that could restrict us from doing business directly or indirectly in or with certain countries or parties, which could include affiliates, disrupt our supply chain and production, and potentially impact the repatriation of earnings.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
Key Trends and Economic Factors Affecting Ford and the Automotive Industry Trade Policy. To the extent governments in various regions implement or intensify restrictions or barriers to trade, such as tariff or non-tariff barriers, export controls, currency manipulation, or policies that otherwise favor domestic companies, there can be a significant negative impact on manufacturers based in other markets.

Tariffs implemented to date in the United States and elsewhere have caused significant disruption, increased costs (both directly and indirectly), and uncertainty in the automotive industry, including for Ford, other OEMs, suppliers, and dealers, as well as customers. Moreover, tariffs implemented or increased in the United States and elsewhere in the future may exacerbate these impacts. Further, instability in the supply chain exacerbated by tariffs and other industry concerns, such as China’s restriction on the export of rare earth minerals and various components, has resulted in production disruptions and increased costs and heightens the risk of future production disruptions and additional cost increases. Tariffs have affected and will continue to affect all OEMs, to various degrees.

In 2025, Ford’s gross costs related to tariffs implemented or revised in 2025 was about $3 billion, including the impact of tariff relief, and the net EBIT impact was about $2 billion after offsets. This relief is subject to periodic approval by the U.S. Department of Commerce and may be revised based on factors such as U.S. production and import content levels. As of December 31, 2025, we recognized a receivable of $974 million reflecting tariffs paid but for which we had not yet received refunds. Although we have started to receive refunds, the timing for our receipt of refunds is uncertain and is subject to changes in trade policy. Tariffs, particularly on auto parts for U.S. assembly, if sustained for an extended period of time, will have a significant adverse effect on U.S. production and the overall automotive industry.

For additional information regarding the impact and potential impact of trade policy and tariffs on our business, see the Outlook section on page 74 of this Report and Item 1A. Risk Factors.

Ford Pro’s 2025 full year EBIT was $6,843 million, a decrease of $2,164 million from a year ago, with an EBIT margin of 10.3%. The lower EBIT was primarily driven by unfavorable fleet pricing (including daily rental), unfavorable mix, and higher tariff-related costs. Excluding tariffs, cost improved year-over-year, driven by lower material and warranty costs.

OUTLOOK We provided 2026 Company guidance in our earnings release furnished on Form 8-K dated February 10, 2026. The guidance is based on our expectations as of February 10, 2026, and assumes no material change to our current assumptions for inflation, logistics issues, production, or macroeconomic conditions. Moreover, our guidance has not factored in any new policy changes by the administration in the United States, including future or revised tariffs or related offsets, that have not been announced or tariffs or other policy changes that may be announced by other governments after the date hereof. Our actual results could differ materially from our guidance due to risks, uncertainties, and other factors, including those set forth in “Risk Factors” in Item 1A of Part I.

On a segment basis we expect: •Ford Pro EBIT of $6.5 billion to $7.5 billion •Ford Blue EBIT of $4.0 billion to $4.5 billion •Ford Model e EBIT loss of $4.0 billion to $4.5 billion •Ford Credit EBT of about $2.5 billion Our outlook for 2026 assumes: •U.S. SAAR of 16.0 million to 16.5 million •Flat U.S. industry pricing •With respect to Novelis, in 2025, the fires were a headwind of $2 billion. In 2026, we expect a year-over-year improvement of about $1.0 billion, which includes $1.5 billion to $2.0 billion of temporary costs, including tariffs, attributable to continuity in aluminum supply •Excluding the impact of Novelis: ◦Positive market factors, including favorable mix associated with the sunset of low-margin nameplates and benefits from changes in the U.S. regulatory environment ◦About flat cost–We expect lower tariff costs of about $1.0 billion, reflecting a full year’s worth of credit expansion, and further material and warranty cost reductions. We expect these lower costs to offset about $1.0 billion of higher commodity prices, driven by inflation, and incremental investment in support of our Universal EV platform, the ramp of Ford Energy, and cycle plan actions 74
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
