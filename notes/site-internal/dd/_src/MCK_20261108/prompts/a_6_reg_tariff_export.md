你是 stock-analyst v20 DD 的證據採集子 agent。標的：MCK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - MCK McKesson tariff section 232 2026
  - McKesson export control OR entity list Pharmaceutical Distribution + Specialty Solutions 2026
  - MCK McKesson China tariff OR trade restriction 2026
  - Pharmaceutical Distribution + Specialty Solutions tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
We rely on third parties for the supply of pharmaceutical and other products, and our operations are subject to our suppliers’ continued ability to supply the products that we require. From time to time, we experience difficulties and delays in sourcing and selling products due to a variety of causes that result in suppliers’ failure to satisfy production demand. Among these causes are suppliers’ challenges in complying with legal requirements (including product and production quality standards), access to raw materials, inputs, and finished goods, manufacturing shutdowns, and operational and systems difficulties. Supply disruptions also arise from other factors beyond our control, such as product rationalization; government actions or policies (including trade sanctions, tariffs and other trade restrictions, as well as the requisition, diversion, or allocation of inventory); shifts in customer or societal demand for products; labor disputes or shortages; ethical sourcing issues; supplier financial distress; natural disasters and weather-related events; civil unrest; military conflicts; and epidemics or pandemics. In these types of situations, our alternative sourcing efforts are not always fully successful. We might experience extended delays or incur higher sourcing costs or suffer harm to our customer relationships and reputation. Furthermore, changes in the healthcare industry’s or our suppliers’ pricing, selling, inventory, distribution, or supply policies or practices could significantly reduce our revenues and net income.…

Inflationary conditions result in increased costs associated with our normal business operations and decreased levels of consumer commercial spending and, to the extent we are not able to offset such cost increases from our suppliers, increase the costs which we incur to purchase inventories and services. Inflationary pressure is increased by factors such as supply chain disruptions, labor market tightness, actual or announced tariffs, government policies, interest rate changes, and foreign exchange rate changes. An economic slowdown or a recession could also reduce the prices our customers are able or willing to pay for our products and services and reduce the volume of their purchases. In addition to rising inflation, rising interest rates, the impact of banking failures or perceived failures and related contagion, consumer sentiment, political circumstances, military conflicts, and civil unrest may contribute to recessionary pressure. Our non-U.S. operations, import and export of products sold in currencies other than U.S. dollar (non-USD), non-USD intercompany loans, and our substantial international net assets also expose us to foreign currency exchange rate risk. Changes in the economic environments in which we operate might have a materially adverse impact on our business operations and our financial position or results of operations.

From time to time we are adversely affected by conditions and events outside of our control, including: widespread public health issues such as epidemic or pandemic infectious diseases; natural disasters and other catastrophic events such as earthquakes, floods, or severe weather; and geopolitical factors such as terrorism, military conflicts, civil unrest, political circumstances (including changes in international relations), changes or uncertainty in government policies (including with respect to U.S. or international trade), actual or announced tariffs or other trade restrictions, government shutdowns, or changes in laws or their interpretation. These conditions and events can disrupt operations for us, our suppliers, our vendors, and our customers, as well as impair product manufacturing, supply, and transport availability and cost in unpredictable ways that depend on highly uncertain future developments. They might affect consumer confidence levels and spending or the availability of certain goods, commodities, raw materials, and other inputs. In response to these types of conditions and events, we might seek alternate sources for product supply, incur additional sourcing or distribution costs, suspend operations, implement extraordinary procedures, or suffer consequences that are unexpected and difficult to mitigate. For example, the trade environment remains highly dynamic and uncertain, and trade policies may be interrelated with other government initiatives.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
FOREIGN OPERATIONS Our foreign operations represented approximately 4% of our consolidated revenues in each of fiscal 2026 and fiscal 2025, respectively. Foreign operations are subject to certain risks, including currency fluctuations. Refer to Item 1A - Risk Factors in Part I of this Annual Report for a risk factor related to fluctuations in foreign currency exchange rates, and risks from trade and tariffs. We monitor our operations and adopt strategies responsive to changes in the economic and political environment in each of the countries in which we operate. We conduct our business worldwide in local currencies, including the Canadian dollar. As a result, the comparability of our results reported in U.S. dollars can be affected by changes in foreign currency exchange rates. In discussing our operating results, we may use the term “foreign currency exchange fluctuations,” which refers to the effect of changes in foreign currency exchange rates used to convert the local currency results of our operations in foreign countries where the functional currency is not the U.S. dollar. We present this information to provide a framework for assessing how our business performed excluding the effect of foreign currency exchange rate fluctuations. In computing the foreign currency exchange fluctuations, we translate our current year results of our operations in foreign countries recorded in local currencies into U.S.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
