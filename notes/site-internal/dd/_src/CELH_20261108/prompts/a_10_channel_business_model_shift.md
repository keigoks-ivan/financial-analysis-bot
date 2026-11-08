你是 stock-analyst v20 DD 的證據採集子 agent。標的：CELH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Celsius Holdings distribution channel disruption OR shift 2026
  - CELH Celsius Holdings business model transition subscription OR platform 2026
  - Beverages - Non-Alcoholic channel disintermediation D2C 2026
  - Celsius Holdings go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm｜as_of：2026-03-02
<<<
Our products are available in the U.S., Canada, Europe, the Middle East and the Asia-Pacific regions. They are sold through multiple channels, including conventional grocery, natural-food and convenience stores, fitness centers, mass-market and vitamin specialty retailers and e-commerce platforms.

•A&R Distribution Agreements - We entered into the A&R Distribution Agreements, under which Pepsi continues to serve as our primary distributor for Celsius products in the U.S. and Canada and has become the primary distributor of Alani Nu and Rockstar products in these markets. All other material provisions of each of the Original U.S. Distribution Agreement and Original Canadian Distribution Agreement remain in effect.

Across our portfolio, our packaging emphasizes bold graphics and vibrant color palettes to create strong shelf presence and reinforce our brand positioning to reach a broad range of new and existing energy drink consumers. Our products are sold through multiple channels including conventional grocery, natural-food and convenience stores, fitness centers, mass-market and vitamin specialty retailers and e-commerce platforms, allowing us to serve a diverse base of consumers within the functional energy and wellness categories.

Distribution Pepsi Distribution Agreement On the Closing Date of the Pepsi Transactions, we entered into the A&R Distribution Agreements, which amended and restated in their entirety the Original U.S. Distribution Agreement and Original Canadian Distribution Agreement. Under the A&R Distribution Agreements, Pepsi continues to serve as our primary distributor for Celsius products in the U.S. and Canada and has also become the primary distributor of our Alani Nu and Rockstar products in these markets. All other material terms and covenants contained in the original agreements remain in effect.

In connection with expanding Pepsi’s distribution responsibilities to include Alani Nu, we terminated certain former Alani Nu distributors and transitioned territory rights to Pepsi. Pepsi agreed to reimburse us for distributor termination fees up to $275.0 million, to facilitate this transition. Cash received for these reimbursements is contractually restricted and must be used to settle such obligations, and any unspent amounts must be returned to Pepsi. These reimbursements are recognized as deferred revenue and amortized on a straight-line basis over the approximately 17-year term of the A&R U.S. Distribution Agreement.

2 The A&R Distribution Agreements continue to provide Pepsi with certain rights contained in the original agreements, including rights of first offer with respect to distribution in select additional territories or future channels. Except for termination by either party “with cause,” the agreement may be terminated by either party upon 12 months’ written notice in the 19th year of the term (i.e., 2041), the 29th year of the term (i.e., 2051) and in each 10th year thereafter (i.e., 2061, 2071, etc.). Termination provisions, including compensation due upon a termination for cause, remain materially consistent with those contained in the original agreements.

Domestic In the U.S. and Canada, we market and sell our products across a diverse range of retail channels, including supermarkets, convenience stores, drugstores, nutritional stores, food service providers and mass merchants. Our products are widely available in major retail segments, including conventional grocery, natural food stores, convenience stores, fitness centers, mass market retailers, vitamin specialty stores and e-commerce platforms.

Domestically, we distribute our products through a combination of DSD networks, independent distributors and direct sales to retailers. Additionally, our products are available online through leading e-commerce platforms, including Amazon, Shopify, Instacart and Walmart.com, ensuring broad accessibility for consumers.

International We are continuing to make significant strides internationally for our flagship product CELSIUS® in key global markets. We distribute certain of our products in various foreign regions through regional and country-specific distribution partners, leveraging local market expertise to optimize distribution and brand visibility. With partnerships spanning Europe and the Asia-Pacific region, we have strategically positioned the brand to meet growing global demand. To further support these initiatives, we recently appointed a president to oversee our international operations and drive strategic expansion across key global markets. These efforts demonstrate our commitment to leveraging partnerships, such as those within the Suntory Group, to drive product availability and brand visibility in both established and emerging markets, while utilizing local market expertise to optimize our global expansion strategies.

Customers Our customer base primarily consists of distributors, e-commerce retailers and various brick-and-mortar outlets, including grocery and convenience stores, club stores and health-focused locations such as gyms and nutrition stores. To support and incentivize the distribution, sales and marketing of our products, we rely on and provide various financial incentives. These incentives include but are not limited to volume-based rebates and promotions, placement fees, listing fees and other discounts.

Internationally, we rely on outsourced manufacturing and distribution channels, which are subject to compliance with the laws and regulations in the foreign countries where our products are sold. Certain international markets, including countries in the European Union, have specific energy drink standards and ingredient restrictions that we closely monitor and with which we must comply.

We inform our investors and the public of material corporate information through various channels, including SEC filings, press releases, public conference calls, webcasts and our official corporate website at www.celsiusholdingsinc.com. We have used and expect to continue to use, our website as a means of disclosing material information to the public in a broad, non-exclusionary manner, including for purposes of the SEC's Regulation Fair Disclosure. This information may include, without limitation, updates on our financial performance, significant personnel changes, brand developments and other pertinent matters. We regard the content posted on our corporate website as potentially material to our investors. Therefore, we encourage our investors, the media, customers, consumers, business partners and other stakeholders to regularly review the materials we disseminate through these platforms. Periodically, we may modify the list of communication channels for disseminating material information. Any such changes will be communicated and updated on our website. Information contained on, or accessible through, our website is not a part of and is not incorporated by reference into, this Report or any other filings we make with the SEC.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm｜as_of：2026-03-02
<<<
Building on the long-term distribution agreement we originally established with Pepsi in August 2022, on the Closing Date of the Pepsi Transactions, we entered into a series of transactions that expanded our strategic partnership. These included (i) the Rockstar Acquisition, (ii) the issuance of Series B Preferred Stock and amendment of the existing Series A Preferred Stock and (iii) the execution of the A&R Distribution Agreements, which designate Pepsi as the primary distributor of our Alani Nu and Rockstar products in the U.S. and Canada. Under the enhanced commercial arrangement, Pepsi has agreed to use its commercially reasonable efforts to sell and distribute our full portfolio of products in the U.S. in accordance with the Captaincy.

Through this partnership, we benefit from Pepsi’s scale, operational capabilities and established distribution infrastructure which supports product availability, retail execution and market penetration across multiple channels in the U.S. and Canada. The expanded scope of our relationship with Pepsi, including enhanced coordination around sales, placement and promotional priorities, is intended to support execution consistency and improve speed to market as we scale our brand portfolio.

33 Comparability with Prior Year Our financial condition as of December 31, 2025 reflected significant changes compared to the year ended December 31, 2024, primarily driven by the Alani Nu Acquisition and the transactions entered into on the Closing Date of the Pepsi Transactions. As a result of the A&R Distribution Agreements, primarily due to the transition of Alani Nu distribution to Pepsi, we recognized significant costs related to the termination of those distributors in 2025 in our Consolidated Financial Statements.

The decrease in net income attributable to common stockholders for the year ended December 31, 2025 was primarily driven by distributor termination fees incurred in connection with transitioning Alani Nu distribution to the Pepsi distribution network and higher interest expense related to newly incurred debt. This impact was partially offset by a legal accrual which reduced net income and EPS for the year ended December 31, 2024. Additionally, basic and diluted EPS for the year ended December 31, 2025 were impacted by an increase in weighted average shares outstanding, primarily as a result of Common Stock issued in connection with the Alani Nu Acquisition.

Revenue Recognition - Promotional (Billbacks) Allowance The Company’s promotional allowance programs with its distributors or retailers are executed through separate agreements in the ordinary course of business (variable consideration). These agreements provide for one or more arrangements that are of varying durations. The Company’s billbacks are calculated based on various programs with distributors and retail customers and accruals are established for the Company’s anticipated liabilities. These accruals are based on agreed upon terms as well as the Company’s historical experience with similar programs and require management’s judgment with respect to estimating consumer participation and the performance of distributors and retail customers. Differences between estimated and actual promotional and other allowances are recognized in the period such differences are determined.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
