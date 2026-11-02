你是 stock-analyst v20 DD 的證據採集子 agent。標的：GRMN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - GRMN Garmin market share gaining OR losing 2026
  - Garmin new entrant OR displace threat Scientific & Technical Instruments 2026
  - GRMN competitor design win 2026
  - Garmin vs Scientific & Technical Instruments peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1121788/000119312526056028/grmn-20251227.htm｜as_of：2026-02-18
<<<
Competition Garmin operates in highly competitive markets, though competitive conditions vary among the diverse target markets and geographies. Garmin believes the principal competitive factors impacting the market for its products are design, functionality, quality and reliability, customer service, brand, price, time-to-market and availability. Garmin believes that it generally competes favorably in each of these areas and as such, is generally a significant competitor in each of the major markets in which it operates.

Garmin believes that its principal competitors for fitness products are Apple, Bryton, Coros, Elite, Google, Huawei, Oura, Polar, Samsung, SRAM, Suunto, Wahoo Fitness, Whoop, Xiaomi, Zepp Health, and Zwift. Garmin believes that its principal competitors for outdoor products are Apple, Casio, Coros, Dogtra, Globalstar, Infinition, Rand McNally, Samsung, Shearwater Research, SportDOG, Suunto, TAG Heuer, Tissot, TomTom, Trackman, Uneekor, Vista Outdoor, and Zoleo. Garmin considers its principal aviation competitors to be Aspen Avionics, Avidyne, Dynon Avionics, Jeppesen ForeFlight, Genesys Aerosystems, Honeywell Aerospace & Defense, Innovative Aerosystems, Collins Aerospace (RTX), Safran, Thales, and Universal Avionics Systems Corporation. For marine products, Garmin believes that its principal competitors are Furuno, Johnson Outdoors, Navico 10 (Brunswick), and Raymarine (Teledyne). Garmin believes that its principal competitors for auto OEM products are Alpine Electronics, Aptiv, Bosch, Continental, Harman (Samsung), LG, Panasonic, and Visteon.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1121788/000119312526056028/grmn-20251227.htm｜as_of：2026-02-18
<<<
If we are unable to compete effectively with existing or new competitors, the associated loss of competitive position could result in price reductions, fewer customer orders, reduced margins and loss of market share.

The markets for many of our products and services are highly competitive, and we expect competition to increase in the future. Some of our competitors have significantly greater financial, technical and marketing resources than we do. They may also be able to devote greater resources to the development, promotion and sale of their products or secure better product positioning with retailers. Additionally, existing and emerging competitors have been able to replicate certain features offered by some of our products and services or respond more rapidly to emerging technologies or changes in customer requirements. Some of our original equipment manufacturer (OEM) customers may develop in-house equipment and components that they currently purchase from us. Increased competition could result in price reductions, fewer customer orders, reduced margins and loss of market share. Our failure to compete successfully against current or future competitors could materially adversely affect our business, financial condition and results of operations.

Some of our products also use satellite signals from Russia’s GLONASS, the European Union Galileo system, and the Chinese BDS. National or European authorities may provide preferential access to signals to companies associated with their markets, including our competitors, which could harm our competitive position. Use of non-U.S. GNSS signals may also be subject to FCC waiver requirements and to restrictions based upon international trade or geopolitical considerations. If we are unable to develop timely and competitive commercial products using these systems, or obtain timely and equal access to service signals, it could materially adversely affect our business, financial condition and results of operations.

We have experienced periods of annual growth in sales and profits in our outdoor and fitness segments, which have benefited from increased sales of wearable devices. However, we have also experienced periods of declines in sales and profits in these segments. If the overall wearable device market declines, or categories of devices within the wearable device market decline significantly, or if we lose significant market share in the wearable device market, our business, financial condition and results of operations could be materially adversely affected.

The market price of our shares has been, and may continue to be, highly volatile. During 2025, the closing price of our shares ranged from a low of $173.63 to a high of $259.77. A variety of factors could cause the price of our shares to fluctuate, perhaps substantially, including but not limited to: •new products or product enhancements by us or our competitors; •general conditions in the worldwide economy, including fluctuations in inflation, interest rates and global currency exchange rates; •announcements of technological innovations; •product obsolescence and our ability to manage product transitions; •developments in our relationships with our customers and suppliers; •the availability, pricing and timeliness of delivery of components, such as semiconductors, flash memory and liquid crystal displays, used in our products; •quarterly fluctuations in our actual or anticipated operating results; •changes and proposed changes in applicable tax laws, tax rates, tariffs and duties; •developments in patents or other intellectual property rights and litigation; •announcements and rumors of developments related to our business, our competitors, our suppliers or the markets in which we compete; •research reports or opinions issued by securities analysts or brokerage houses related to Garmin, our competitors, our suppliers or our customers; •any significant acts of terrorism in locations where we have significant operations or significant markets for our products; and •other factors as…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRMN_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
