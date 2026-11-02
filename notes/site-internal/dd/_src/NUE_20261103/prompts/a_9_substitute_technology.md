你是 stock-analyst v20 DD 的證據採集子 agent。標的：NUE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Nucor product substitute technology threat 2026
  - Steel alternative technology disruption 2026 2027
  - NUE Nucor technology obsolescence risk
  - Steel next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm｜as_of：2026-02-25
<<<
Steel mills segment In the steel mills segment, Nucor produces sheet steel (hot-rolled, cold-rolled and galvanized), plate steel, structural steel (wide-flange beams, beam blanks, H-piling and sheet piling) and bar steel (blooms, billets, concrete reinforcing bar, merchant bar and engineered special bar quality (“SBQ”)). Nucor manufactures steel principally from scrap steel and scrap steel substitutes using electric arc furnaces (“EAFs”) along with continuous casting and automated rolling mills. The steel mills segment also includes Nucor’s equity method investment in NuMit LLC (“NuMit”) (see “Steel joint venture”- below), as well as international trading and distribution companies that buy and sell steel manufactured by the Company and other steel producers.

Our primary external customers for ferrous scrap are EAF steel mills and foundries that use ferrous scrap as a raw material in their manufacturing process. External customers purchasing non-ferrous scrap metal include aluminum can producers, secondary aluminum smelters, steel mills, and other processors and consumers of various non-ferrous metals. We market scrap metal products and related services to our external customers through in-house sales forces. In 2025, approximately 7% of the ferrous and non-ferrous metals and scrap substitute tons we brokered and processed were sold to external customers. We consumed the balance in our steel mills.

6 •Direct reduced iron operations - DRI is a substitute material for high-quality grades of scrap and pig iron. Nucor operates two DRI plants which supplied approximately 3,300,000 metric tons of material with world-class metallization rates and carbon content to our steel mills in 2025. Nucor’s wholly owned subsidiary, Nu-Iron Unlimited, is located in Trinidad and benefits from a low-cost supply of natural gas and favorable logistics for inbound iron ore and shipment of DRI to the United States. Nucor’s second DRI plant in Louisiana also benefits from favorable logistics and proximity to its steel mill customers.

Nucor’s DRI production and brokering capabilities provide our steel mills flexibility to quickly adjust their metallic input mix to changing market conditions, enabling them to maintain competitiveness in the often-volatile ferrous scrap market. With the potential for high-quality scrap to become scarcer, coupled with the risk of third-party supplier disruptions, Nucor’s DRI facilities provide a greater degree of certainty over metallics supply to its steel mills.

Sources and Availability of Raw Materials An ample supply of high-quality scrap and scrap substitutes is critical to support Nucor’s ability to produce high-quality steel. The goal of Nucor’s raw materials segment is to safely produce, source, trade and transport steelmaking raw materials. Nucor’s raw materials investments are focused on creating an advantage for our steelmaking operations, through a global information network and flexible approach to metallics supply.

Scrap and scrap substitutes are the most significant element in the total cost of steel production. The average cost of scrap and scrap substitutes used in our steel mills segment remained relatively stable from $394 per gross ton used in 2024 to $392 per gross ton used in 2025. On average, it takes approximately 1.1 tons of scrap and scrap substitutes to produce one ton of steel. We employ variable steel pricing mechanisms so that we are better able to maintain operating margins and meet our customer commitments as scrap and scrap substitute costs fluctuate.

Nucor remains focused on securing reliable access to low-cost raw material inputs as they are the Company’s largest expense. We believe Nucor’s broad, balanced supply chain is an important strength which allows us to reduce the cost of our steelmaking operations, create a shorter supply chain and have greater control over our metallic inputs. Our investment in DRI production facilities and scrap yards, as well as our access to international raw materials markets, provides Nucor with significant flexibility in optimizing our raw material mix. Additionally, having a significant portion of our raw materials supply under our control minimizes risk associated with the global sourcing of raw materials, particularly since a good deal of scrap substitutes comes from regions of the world that have historically experienced greater political turmoil, such as Ukraine, Russia and Brazil. We believe the continued successful implementation of our raw material strategy, including key investments in DRI production, as well as in the scrap brokerage and processing services performed by our team at DJJ, gives us greater control over our metallic inputs and thus helps us navigate significant fluctuations in the availability and costs of critical inputs.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm｜as_of：2026-02-25
<<<
In many applications, steel competes with other materials, such as concrete, aluminum, plastics, composites and wood. Increased use or availability of these materials in substitution for steel products could have a material adverse effect on prices and demand for our steel products.

Our steel mills are large consumers of electricity and natural gas. In addition, our DRI facilities are also large consumers of natural gas. We rely upon third parties for our supply of energy resources consumed in the manufacture of our products. The prices for and availability of electricity and natural gas can be volatile. They are often affected by weather, political, regulatory and economic factors beyond our control, and we may be unable to raise the price of our products to offset increased energy costs. Disruptions, including physical or information systems related issues, that impact the supply of our energy resources could temporarily impair our ability to manufacture our products for our customers. Increases in our energy costs that are not similarly applicable to our competitors' operations could materially adversely affect our business, results of operations, financial condition and cash flows.

We rely to an extent on outside vendors to supply us with key consumables such as graphite electrodes, alloys and other raw materials, including both scrap and scrap substitutes (e.g., prime scrap, pig iron and DRI) that are critical to the manufacture of our steel products. The raw material required to produce DRI is pelletized iron ore. Although we have vertically integrated our business by constructing our DRI facilities in Trinidad and Louisiana and also by acquiring our scrap processing and brokerage operations, DJJ, in 2008, we still must purchase most of our primary raw material, steel scrap, from numerous other sources located throughout the United States and internationally. Although we believe that the supply of scrap and scrap substitutes will remain adequate to operate our facilities, prices of these critical raw materials are volatile and are influenced by changes in scrap exports in response to changes in the scrap, scrap substitutes and iron ore demands of our global competitors, as well as volatility in currency rates and political conditions.

We utilize various information technology systems to efficiently address business functions ranging from the operation of our production equipment to administrative computation to the storage of data such as intellectual property and proprietary business information. We also utilize third-party service providers for certain information technology services that are important to our operations. We continuously evaluate our cybersecurity systems and practices, assess potential threats, and improve our information technology networks, policies and procedures to address potential vulnerabilities. Despite efforts to assure secure and uninterrupted operations, threats from increasingly sophisticated cyberattacks or system failures could result in materially adverse operational disruptions or security breaches of our systems or those of our third-party service providers. These risks could result in disclosure or destruction of key proprietary information or personal data or reputational damage, theft of assets or trade secrets, or could adversely affect our ability to physically produce or transport steel, resulting in lost revenues, as well as delays in reporting our financial results. We also could be required to spend significant financial and other resources to remedy the damage caused by a cybersecurity breach, including to repair or replace networks and information technology systems. We may also contend with potential liability for stolen information, increased cybersecurity protection costs, litigation expense and increased insurance premiums.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NUE_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
