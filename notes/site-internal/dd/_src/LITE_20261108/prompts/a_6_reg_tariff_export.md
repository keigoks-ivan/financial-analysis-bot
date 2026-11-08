你是 stock-analyst v20 DD 的證據採集子 agent。標的：LITE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - LITE Lumentum Holdings tariff section 232 2026
  - Lumentum Holdings export control OR entity list Communication Equipment 2026
  - LITE Lumentum Holdings China tariff OR trade restriction 2026
  - Communication Equipment tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm｜as_of：2026-08-17
<<<
Due to worldwide operations, we and our customers are also subject to risks relating to the global trade environment. We are actively monitoring and assessing the global trade environment, particularly with respect to various proposed and enacted changes in tariff regulations and trade restrictions. The ongoing uncertainty surrounding trading policies, including the potential for additional tariffs, restrictions related to our customers and retaliatory measures by non-U.S. governments, continues to create a volatile environment that could disrupt our operations. The imposition of tariffs on certain imported goods and materials and export controls on critical components may increase our costs and place upward pressure on the cost of goods sold, which, in turn, may reduce our gross margins if we are unable to pass these costs onto customers through price increases.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm｜as_of：2026-08-17
<<<
U.S. regulatory activity, such as tariffs, export controls, and economic sanctions laws have in the past, and may in the future, materially limit our ability to make sales to customers in certain regions of the world, including China, and which have in the past, and may in the future, increase our costs and harm our results of operations and financial condition. Throughout 2025 and 2026, the U.S. imposed a series of tariffs on imported goods. These tariffs were generally positioned to have the most significant impacts on goods originating from China, but nearly all countries worldwide were impacted at levels ranging from 15% to stacked tariffs in excess of 100% in some cases. While many of the tariffs and surcharges initially proposed were invalidated or expired, the tariff landscape continues to evolve and, as a result, the full impact of current or future tariff measures on our business is uncertain. U.S. government investigations are currently underway that may result in new tariffs on certain products, including semiconductors, machines, and other products derivative of critical minerals. For example, on April 14, 2025, the Secretary of Commerce initiated an investigation under Section 232 of the Trade Expansion Act of 1962 to determine the effects on U.S.…

Outside of the U.S., geopolitical escalations and retaliatory measures from various countries also have in the past, and may in the future, adversely impact business operations. Such measures include tariffs on imports of U.S. products into countries such as China, as well as China’s export control measures targeting the U.S., Europe and Japan. For example, China imposed new export control measures affecting exports of rare earth metals and other critical minerals, limiting our ability to access these materials, which may limit our ability to produce products, increase our selling and/or manufacturing costs, decrease margins, reduce the competitiveness of our products, reduce customer demand for our products, or inhibit our ability to sell products or purchase necessary equipment and supplies. Similarly, China restricted exports to Japan, which affected our substrate supply chain globally. Future changes to the trade policies of the U.S. and China are impossible to predict, but further changes or escalations impacting global trade policies may continue to affect our business.

Adverse regulatory activity, such as export controls, economic sanctions and the imposition of heightened trade tariffs both globally and between the United States and China specifically carry the risk of negatively impacting overall economic conditions, which could have negative repercussions on our industry and our business. Moreover, to the extent the governments of China, the United States or other countries seek to promote use of domestically produced products or to reduce the dependence on or use of products from each other (sometimes referred to as “decoupling”), they may adopt or apply regulations or policies that have the effect of reducing business opportunities for us. Such actions may take the form of specific restrictions on particular customers, products, technology areas, or business combinations. For example, in the area of investments and mergers and acquisitions, the United States has implemented requirements for approval by the United States government of outbound investments; and the approval by China regulatory authorities is required for business combinations of companies that conduct business in China over specific thresholds, regardless of where those businesses are based. Restrictions may also be imposed based on whether the supplier is considered unreliable or a security risk. For example, the Chinese government adopted a law that would restrict purchases from suppliers deemed to be “unreliable suppliers”.…

In August 2020, the Bureau of Industry and Security of the U.S. Department of Commerce (“BIS”) issued final rules that further restricted access by Huawei Technologies Co. Ltd. and certain of its affiliates (collectively, “Huawei”) to U.S. technology, software and equipment produced domestically and abroad. The final rules prevent us from selling certain products subject to the Export Administration Regulations (“EAR”) to identified Huawei entities without a license issued by BIS. Based on internal review conducted in 2023, we determined that our products may be “subject to the EAR” and consequently restricted for export, reexport, and transfer to Huawei. As a result, we stopped all of our product shipments to Huawei, historically our largest networking customer in China, in the beginning of calendar year 2024. Further, even if we are able to obtain an export authorization to sell certain products to Huawei in the future, Huawei may not be able to source products from other suppliers due to the applicable export restrictions, which could then adversely impact Huawei’s demand for our products. All U.S. companies are dependent on the ability to obtain export authorizations to sell to Huawei. Until such export authorizations are available or the export restrictions are lifted, we are limited in our ability to sell our products.

Further, certain of our suppliers are located in China, which exposes us to risks associated with Chinese laws and regulations and U.S. laws, regulations and policies with respect to China, such as those related to export controls, tariffs and retaliatory measures, and risks related to taxation and the treatment of intellectual property. Chinese and U.S. laws and regulations are subject to frequent change, and if our suppliers are unable to obtain or retain the requisite legal permits or otherwise to comply with Chinese and U.S. legal requirements, we may be forced to obtain products from other manufacturers or to make other operational changes, including transferring our manufacturing to another manufacturer or to our own manufacturing facilities. In addition, many of our products are sourced from suppliers based outside of the United States, primarily in Asia. We may continue to face uncertainty with respect to our suppliers’ abilities to supply products due to supply chain and inventory impacts, tax and trade policies, the effects of trade wars, including heightened, scheduled, and threatened tariffs and trade restrictions, and government regulations affecting trade between the United States and other countries. Major developments in tax policy or trade relations, such as the imposition of tariffs on imported products, for example, higher U.S.…

Further, there is increased attention from the government and the media regarding potential threats to U.S. national security and foreign policy relating to certain foreign entities, particularly Chinese entities, and the imposition of enhanced restrictions or sanctions regarding the export of our products or on specific foreign entities that would restrict their ability to do business with U.S. companies may adversely affect our business. For example, on May 16, 2019, Huawei was added to the Entity List, additional regulatory restrictions were imposed in May and August 2020, including the October 2022 changes to the Foreign Direct Product Rule, which imposes limitations on the supply of certain U.S. items and product support to Huawei. FiberHome Technologies was also added to the Entity List on May 22, 2020. These actions, among others, have resulted in escalating tensions between the U.S. and China and create the possibility that the Chinese government may take additional steps to retaliate against U.S. companies or industries. We currently do not supply any products to Huawei, and we cannot predict whether we will again be able to sell to Huawei. Further, we cannot predict what additional actions the U.S.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm｜as_of：2026-08-17
<<<
Due to worldwide operations, we and our customers are also subject to risks relating to the global trade environment. We are actively monitoring and assessing the global trade environment, particularly with respect to various proposed and enacted changes in tariff regulations and trade restrictions. The ongoing uncertainty surrounding trading policies, including the potential for additional tariffs, restrictions related to our customers and retaliatory measures by non-U.S. governments, continues to create a volatile environment that could disrupt our operations. The imposition of tariffs on certain imported goods and materials and export controls on critical components may increase our costs and place upward pressure on the cost of goods sold, which, in turn, may reduce our gross margins if we are unable to pass these costs onto customers through price increases.

Shipping and Handling Costs and Tariffs We record shipping and handling costs and tariffs related to revenue transactions within cost of sales as a period cost. Amounts billed to the customer for shipping and handling costs, including tariff charges, is recorded as revenue when the relevant product is recognized as revenue.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
