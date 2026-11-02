你是 stock-analyst v20 DD 的證據採集子 agent。標的：EBAY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - EBAY eBay tariff section 232 2026
  - eBay export control OR entity list Internet Retail 2026
  - EBAY eBay China tariff OR trade restriction 2026
  - Internet Retail tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm｜as_of：2026-02-19
<<<
In 2025, the United States government eliminated the long-standing “de minimis” exemption (under Section 321 of the Tariff Act of 1930), which previously allowed low-value parcels (valued at USD $800 or less) to enter the United States without duties or formal customs clearance. The exemption was first eliminated for shipments originating in China and Hong Kong on May 2, 2025, and then for all parcels effective August 29, 2025. As a result, all imports, regardless of value, are now subject to applicable duties, taxes, fees and standard customs compliance procedures. Importers, such as eBay buyers and sellers, must supply additional data for entry (e.g., 10-digit Harmonized Tariff Schedule codes, Country of Origin, etc.) and all shipments are now subject to applicable tariffs. These developments fundamentally change how cross-border transactions are handled, especially when sellers ship directly to U.S. buyers, and they increase cost, complexity and compliance burden for many cross-border sellers, which could lead to reduced cross-border volume or reconfiguration of supply-chain and fulfillment strategies.

Seasonality We expect volume on our Marketplace platforms to trend with general consumer buying patterns. Seasonal trends have been, and we expect in the future will be, influenced by macroeconomic conditions, including tariffs and global trade policies, foreign exchange rate fluctuations, as well as new and updated products and initiatives by us and our competitors. Please see the additional information in “Item 7: Management’s Discussion and Analysis of Financial Condition and Results of Operations” under the caption “Seasonality.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm｜as_of：2026-02-19
<<<
Our business model is dependent upon consumer engagement and spending, which is difficult to predict and which can vary materially due to many factors, including macroeconomic conditions (such as job losses, inflation, changes in tax liabilities, access to credit, changes in global trade and tariff policies, recessionary fears, general economic uncertainty, and changes in consumer confidence); geopolitical events and events that capture public attention (such as war, the threat of war, social or political unrest, or terrorist activity); natural and human caused disasters and the impact of climate change (such as earthquakes, hurricanes, droughts, flooding, wildfires, sea level rise, and increased energy and shipping costs); power shortages or outages; major public health issues and pandemics; seasonal and potentially non-durable buying and selling trends; general shifts in the cultural appetite for re-commerce; our promotional and marketing campaigns; and new technologies (such as live commerce and AI shopping agents). For example, we saw significant changes to consumer spending throughout 2025 as our users around the world adjusted to changing global trade policies and tariffs. In addition, over the years, we have experienced numerous non-durable spikes in demand as buyers chase the latest popular items.…

Governments in various countries have imposed sanctions and export controls that prohibit us and our customers from engaging in or facilitating trade or financial transactions with various countries, businesses, organizations and individuals. Expanding our operations internationally increases the export controls and economic 17 Table of Contents sanctions laws and regulations that apply to us, as well as the risk of a violation. These laws and regulations, and their interpretation and enforcement, change frequently, involve substantial uncertainty and may be driven by political and other factors that are out of our control. In addition, we can be held liable for the actions of our employees, contractors, agents, and customers regardless of the policies and procedures we put in place to comply with these laws and regulations. We have limited control over our customers’ conduct, and some may attempt to circumvent sanctions or export controls through misrepresentation, transshipment, use of intermediaries, or false product descriptions, increasing compliance and enforcement risk. We rely on automated and manual compliance controls to identify and prevent prohibited transactions, but these controls may not be fully effective, particularly where information is incomplete, inaccurate, or intentionally misrepresented by third parties.

Cross-border trade is an important source of both revenue and profits for us. Cross-border trade also represents our primary (or in some cases, only) presence in certain important markets, such as Greater China, and various other countries. Therefore, changes in global trade policies can have a significant impact on buyers and sellers, which can materially harm our business. For example, trade policies that increase tariffs, shipping fees, delivery times or that otherwise restrict or make cross-border trade more difficult or impractical can reduce buying and selling activity on our platforms, which could materially adversely affect our business and results of operations.

Global trade policies underwent significant changes throughout 2025. For example, the United States implemented tariffs and other trade restrictions on several countries, many of which responded by implementing their own tariffs and trade restrictions. In some cases, the amount of tariffs and restrictions changed throughout 2025, adding complexity. In addition, the United States eliminated the $800 “de minimis” exemption from customs duties on imported goods, which has impacted certain eBay transactions that were previously able to use this exemption. Such changes have and may continue to lead to escalations of trade measures. For example some countries have announced retaliatory tariffs, the E.U. has announced it will remove its €150 “de minimis” exemption in July 2026 and require a €3 fee per parcel, and the U.K. is expected to follow with eliminating its £135 “de minimis threshold” for low-value imports. These developments fundamentally change how cross-border transactions are handled, especially when sellers ship directly to the U.S., E.U., and potentially U.K., and they increase cost, complexity and compliance burden for many cross-border sellers, which could lead to reduced cross-border volume or reconfiguration of supply-chain and fulfillment strategies. In July 2026, U.S. customs authorities are expected to implement new electronic filing requirements for importers of regulated consumer products to certify compliance with U.S.…

Any further trade policy developments, especially in key geographies such as the U.S, the U.K., and the E.U., could significantly impact the cost of items and available inventory to be bought and sold on our platforms, limit our ability and the ability of our sellers to offer and deliver products on a timely or cost-effective basis, or otherwise adversely impact our consumers’ ability to buy and sell on our platforms. Further, adapting to new and changed trade restrictions can be expensive, time-consuming and very disruptive to our buyers and sellers. For example, tariffs generally apply based on the manufacturing location, rather than the selling location, of goods. These distinctions can be confusing for our sellers and lead to platform solutions that fail to satisfy all of our customers. Our business to consumer sellers may be dissuaded from using our platforms if we do not have solutions that accurately calculate customs fees based on manufacturing location. However, those same solutions may dissuade our consumer-to-consumer sellers from using our platforms, because they serve to increase the cost of the items they are selling. The loss of sellers from one or more geographies could negatively impact the breadth and relevance of inventory available on our platforms, which could lead to decreased buyer traffic and harm our business.

Regulators and civil litigants have sought, and will likely continue to seek, to hold us liable when our sellers list or sell products on our platforms that they claim are regulated, unlawful, unsafe or infringing. For example, the Department of Justice (“DOJ”) has sought to hold us liable for the third-party sales of products they claim violate federal law. Other third parties, including government regulators and law enforcement officials, have, at times, alleged that our services aid and abet violations of laws regarding the sale of counterfeit items, laws restricting or prohibiting the transferability (and by extension, the resale) of digital goods (e.g., books, music and software), the fencing of stolen goods, recalled item laws, selective distribution channel laws, customs laws, distance selling laws, and the sale of items outside of the U.S. that are regulated by U.S. export controls. Similarly, allegations of infringement of intellectual property rights, including but not limited to counterfeit items, have resulted and may continue to result in threatened and actual litigation, at times, by rights owners. Further, we are also subject to claims by consumers that products they purchased from third-party sellers caused them bodily injury or harmed their property.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm｜as_of：2026-02-19
<<<
Our Marketplace platforms operate globally, resulting in certain revenues that are denominated in foreign currencies, primarily the British pound and euro. Year-over-year appreciation or depreciation of the U.S. dollar may have a material impact to our financial results; we have experienced and may continue to experience elevated foreign currency volatility in the future, including as a result of tariffs and global trade announcements. Through our hedging programs, we actively monitor foreign currency volatility and attempt to mitigate significant movements. As shown in the table above, we generate approximately half of our net revenues internationally. Therefore, we are subject to the risks related to conducting business in foreign countries as discussed under “Item 1A: Risk Factors” in Part I of this report.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EBAY_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
