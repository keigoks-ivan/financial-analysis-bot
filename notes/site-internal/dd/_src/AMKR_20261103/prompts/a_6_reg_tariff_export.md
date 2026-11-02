你是 stock-analyst v20 DD 的證據採集子 agent。標的：AMKR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - AMKR Amkor Technology tariff section 232 2026
  - Amkor Technology export control OR entity list Semiconductor Equipment & Materials 2026
  - AMKR Amkor Technology China tariff OR trade restriction 2026
  - Semiconductor Equipment & Materials tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
12 Table of Contents COMPETITION The outsourced semiconductor packaging and test market is highly competitive, and geopolitical trade tensions have increased competition from Chinese firms supporting a China-for-China supply chain. We face competition from established packaging and test service providers primarily located in Asia, including ASE Technology, JCET Group and Powertech Technology.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
•challenges with integrating diverse operations. Risks Related to Our International Sales and Operations •dependence on international factories and operations, and risks relating to trade restrictions and regional conflict, including restrictive trade barriers, export controls, tariffs, customs and duties.

In recent years, the U.S. Bureau of Industry and Security has announced export control regulations applicable to the sale of U.S. semiconductor technology in China (collectively, the “BIS Regulations”). The above factors, in addition to the BIS Regulations and other similarly restrictive trade barriers adopted by U.S. and foreign governments applicable to the semiconductor supply chain, could impact our business and the businesses of our customers. These factors may have a material and adverse effect on our business, liquidity, results of operations, financial condition and cash flows or lead to significant volatility in our quarterly or annual operating results. In addition, these factors may materially and adversely affect our credit ratings, which could make it more difficult and expensive for us to raise capital and could materially and adversely affect the price of our securities.

We provide packaging and test services through our factories and other operations located in China, Japan, Korea, Malaysia, the Philippines, Portugal, Singapore, Taiwan and Vietnam. A significant portion of our property, plant and equipment is located outside of the United States, and many of our customers and the vendors in our supply chain are also located outside the United States. The following are some of the risks we face in doing business internationally: •restrictive trade barriers considered or adopted by U.S. and foreign governments applicable to the semiconductor supply chain, including laws, rules, regulations and policies in areas such as national security, licensing requirements for exports, tariffs, customs and duties, including the export rules and regulations applicable to U.S. companies that sell certain semiconductor and chipmaking equipment products to customers in China; •international trade disputes, geopolitical tensions, increasing protectionism and economic nationalism leading to increasing export restrictions, trade barriers, tariffs, and other changes in trade policy; •laws, rules, regulations and policies within China and other countries that may favor domestic companies over non-domestic companies, including customer- or government-supported efforts to promote the development and growth of local competitors; •health and safety concerns, including widespread outbreak of infectious diseases and governmental responses thereto; •changes in consumer demand resulting from current or expected inflation or other variations in local economies; 23 Table…

Many of these factors and risks are present and may be heightened within our business operations in China. For example, changes in U.S.-China relations, the political environment or international trade policies could result in further revisions to laws or regulations or their interpretation and enforcement, increased taxation, trade sanctions, the imposition of import or export duties and tariffs, restrictions on imports or exports, currency revaluations or retaliatory actions, which have had and may continue to have an adverse effect on our business plans and operating results. Additionally, the BIS Regulations place limitations on the ability of companies to export certain advanced computing semiconductor chips, as well as chipmaking equipment, by requiring companies to obtain licenses to export such products and equipment into China or other designated countries. These expanded export restrictions limit our ability to sell to certain Chinese companies and to third parties that do business with those companies. Certain of the Company’s competitors may be exempt from the BIS Regulations by virtue of being non-U.S. manufacturers.…

Over the course of 2025, the United States government announced multiple tariff increases and tariff changes for goods imported into the United States from numerous countries, as well as product-based sectoral tariffs. The U.S. government also announced various export control changes. Some countries countered with tariffs, export control changes or other actions, and the U.S. entered into broad trade negotiations with many countries. Many of the U.S. actions, as well as 24 Table of Contents those of other countries, were subsequently paused or revised. We cannot predict what further actions may ultimately be taken by the U.S. with respect to tariffs, export restrictions or other trade measures, what products or entities may be subject to such actions, or what actions may be taken by other countries in response to these U.S. actions. Imposed tariffs may affect end-user demand in each geography where our customers sell their products and services, which may materially and adversely affect demand for our services, our operating results and our financial condition.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
Our results of operations and cash flows have historically fluctuated significantly from quarter to quarter due to many factors, including the seasonality of our business, the cyclical nature of the semiconductor industry and other factors discussed in Part 1, Item 1A of this Form 10-K. We continue to monitor the recent changes in global trade policy, including tariffs and related trade actions announced by the U.S. and other countries. The degree to which such tariffs and other related actions impact our business, financial condition and results of operations will depend on future developments, which are uncertain. We will continue to make prudent investments, and we will closely manage capacity expansion and control costs in response to any changes in market conditions.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
