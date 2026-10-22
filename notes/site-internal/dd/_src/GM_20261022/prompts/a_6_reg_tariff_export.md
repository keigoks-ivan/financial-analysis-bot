你是 stock-analyst v20 DD 的證據採集子 agent。標的：GM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - GM General Motors tariff section 232 2026
  - General Motors export control OR entity list Auto Manufacturers 2026
  - GM General Motors China tariff OR trade restriction 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
As government policies have evolved, we have acted with urgency and discipline to maintain strong positioning within the industry. In 2025, the U.S. and other governments implemented new import tariffs impacting GM and our suppliers, including tariffs on vehicles and parts imported into the U.S. The tariff environment is highly dynamic and the specific tariffs applicable to goods imported by GM and its suppliers into the U.S., including under the U.S.-Mexico-Canada Agreement, and other countries are likely to evolve further. We will continue to adapt as appropriate.

Raw Materials, Services, and Supplies We purchase a wide variety of raw materials, systems, components, parts, supplies, semiconductors, energy, freight, transportation, and other services from numerous suppliers to manufacture our products. The raw materials primarily include steel, aluminum, resins, copper, lead, and precious metals. We do not normally carry substantial inventories of these raw materials in excess of levels reasonably required to meet our production requirements, and while we have not experienced any significant shortages of raw materials, supply disruptions may occur as a result of geopolitical and/or policy actions. Processing and extraction of certain EV battery raw materials is currently concentrated in China and may be subject to import or export restrictions, and/or tariffs. Additionally, to grow and thrive in a competitive global environment will require developing a more resilient, scalable, and sustainable North America-focused supply chain, which includes advancing our strategic sourcing initiatives to secure supply through investments in raw materials suppliers and the execution of strategic, multi-year supply agreements with suppliers throughout the value chain. Focusing on the principle of "buy where we build" will allow the team to work toward greater scalability and stability.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
Many manufacturers, including GM, have relatively high fixed labor costs as well as limitations on their ability to efficiently close facilities and reduce fixed costs, including as a result of collective bargaining agreements. In light of any excess capacity and high fixed costs, many industry participants have attempted to sell more vehicles by providing subsidized financing or leasing programs, offering marketing incentives, or reducing vehicle prices. As a result, we have had, and may in the future need, to offer similar incentives, which may result in vehicle prices that do not offset our costs, including any cost increases or the impact of adverse currency fluctuations or tariffs, which could affect our profitability. Our competitors may also seek to benefit from economies of scale by consolidating or entering into other strategic agreements such as alliances or joint ventures intended to enhance their competitiveness.

Manufacturers in countries that have lower production costs, such as China and India, have become competitors in key emerging markets and have begun offering their products in established markets, as well as low-cost alternatives to established entry-level automobiles. These actions have had, and are expected to continue to have, a significant negative effect on our vehicle pricing, market share, and results of operations in these markets. In addition, foreign governments may decide to implement tax and other policies that favor their domestic manufacturers at the expense of international manufacturers, including GM and its joint venture partners. Introduction or modification of import tariffs or tariff-related measures may lead to further challenges for GM and our global business.

Tariffs applicable to the automotive industry continue to evolve, including in the U.S., where the government has signaled tariff policy may shift in the future. Such tariffs could have a material adverse effect on our financial condition and results of operations. The U.S. and other governments have implemented import tariffs and tariff-related measures—including on vehicles, parts, raw materials, and other inputs—and have indicated further measures may be under consideration. New or existing trade agreements, including the ongoing review of the U.S.-Mexico-Canada Agreement, may also impact the tariff rate applicable to goods imported by GM or our suppliers. Additionally, certain tariffs are subject to pending legal challenges. In these respects, the global tariff environment remains highly dynamic, and the specific tariffs applicable to goods imported by GM and its suppliers into the U.S. and other countries where we operate continue to evolve.

We cannot predict with complete precision the breadth of tariffs and related costs that will impact GM in the future. As a result, the ultimate impact of tariffs on our business could exceed our current estimates, which could have a material adverse effect on our financial condition, results of operations and cash flows, and our expected financial results. Our efforts to mitigate the impact of tariffs, including, but not limited to, making changes to our U.S. production plan and reducing or pausing certain imports, may not be successful, and we do not expect such actions to fully offset the impact of tariffs in the near term. We have made and may need to make additional changes to our global production footprint and workforce, which could require significant capital expenditures and could result in asset impairments and other charges, including restructuring charges, any of which could be material. Evolving tariffs globally, along with other trade barriers and trade restrictions, may lead to supply chain disruptions, potentially resulting in increased production costs and the inability to receive certain critical parts.

In addition, our success in China depends upon our ability to adequately address unique market and consumer preferences driven by advancements related to EVs, infotainment, software-enabled connected services, and other new technologies while achieving affordability. Our ability to fully deploy our technologies in China may be impacted by evolving laws and regulations in the U.S. and China and the unique regulatory landscape in China. Increased competition, continued U.S.-China trade tensions, weakening economic conditions in China or China's level of integration with key components of our global supply chain, among other factors, may result in cost increases, price reductions, reduced sales, profitability, and margins, and challenges to gaining or holding market share.

The international scale and footprint of our operations expose us to additional risks. We manufacture, sell, and service products globally and rely upon an integrated global supply chain to deliver the raw materials, components, systems, and parts that we need to manufacture our products. Our global operations subject us to extensive domestic and foreign legal and regulatory requirements, and a variety of other political, economic, and regulatory risks, which may have a material adverse effect on our financial condition or results of operations, including: (1) changes in government leadership; (2) changes in trade compliance, labor, employment, tax, privacy, environmental, and other laws, regulations, or government policies impacting our overall business model or practices or restricting our ability to manufacture, purchase, or sell products consistent with market demand and our business objectives; (3) political pressures to change any aspect of our business model or practices or that impair our ability to source raw materials, services, components, systems, and parts, or manufacture products on competitive terms in a manner consistent with our business objectives; (4) political uncertainty, instability, civil unrest, government controls over certain sectors, or human rights concerns; (5) political and economic tensions between governments and changes in international economic policies, including restrictions on the repatriation of dividends or in the export of technology, especially between China and the U.S.; (6)…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
Over the course of 2025, the U.S. and other governments implemented new tariffs relevant to GM and its suppliers, including tariffs on vehicles and parts imported into the U.S. The tariff environment remains highly dynamic, and the specific tariffs applicable to goods imported by GM and its suppliers continue to evolve, including with respect to imports under the U.S.-Mexico-Canada Agreement and other trade agreements. We have acted with urgency and discipline to maintain strong positioning within the industry. In 2025, impacts to earnings before interest and taxes (EBIT)-adjusted from tariffs were $3.1 billion. Based on the current tariff environment, we estimate that impacts to EBIT-adjusted could range from $3.0 billion to $4.0 billion for the year ending December 31, 2026. Refer to Part I, Item 1A. Risk Factors for a full discussion of the risks associated with the global tariff environment.

We achieved solid margins in the year ended December 31, 2025 driven by the strength of our product portfolio and ongoing cost discipline. However, the evolving tariff and policy landscape could have a material impact on our profitability going forward. We remain focused on improving our EV profitability while maintaining our focus on cost. In addition, our outlook is dependent on continued supply chain availability, the resiliency of the U.S. economy, and overall economic conditions, including the imposition of tariffs, less available offsets and deductions, or other trade restrictions by the U.S. or its trading partners. Looking ahead, our top priority is returning GMNA to its historical 8.0-10.0% EBIT-adjusted margins as quickly as possible.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
