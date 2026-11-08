你是 stock-analyst v20 DD 的證據採集子 agent。標的：GFS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_second_source] 客戶 second-source 與 in-house
Q: 最大客戶是否正在導入第二供應商，或將此環節自製（in-house）？
  - GFS GLOBALFOUNDRIES largest customer second-source OR in-house 2026
  - custom chip OR component second source agreement 2026
  - GLOBALFOUNDRIES single-source risk customer diversify supplier
  - in-house design OR insourcing Semiconductors 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-27）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm｜as_of：2026-02-27
<<<
We endeavor to utilize our existing manufacturing capacity and pursue growth beyond our existing capacity via a design funnel to design award process, with the aim of securing as many single-sourced awards through differentiation as possible. We define single-sourced products as those that we believe can only be manufactured with our technology and cannot be manufactured elsewhere without significant customer redesigns. Given the time and costs associated with moving a single-sourced product to a competitor, clients are more likely to continue awarding us single-source contracts for such products. If we are unable to fill the funnel and convert enough opportunities into design wins and ultimately awards due to differentiation, pricing, competition, or any other reasons, there will be a material adverse impact on our financial performance.

In past years, and especially during peak periods of demand when global supply is tight, we were able to sell reserved production capacity through LTAs as opposed to shorter contracts or via more traditional purchase order based contracts. In light of current demand dynamics, our ability to enter into LTAs has diminished, and the focus of our commercial operations has shifted to building a wider funnel of potential customers across a breadth of end markets, aiming to secure more single-sourced design wins.

Some of our customers may alter their process technology roadmaps and adopt single-digit nanometer manufacturing technologies (e.g., 3nm, 5nm, 7nm) faster than their original plans. Some original equipment manufacturers may develop their own in-house application-specific ICs, cut out the fabless GF customer and adopt a different foundry strategy. Nearly all of our customers already maintain their own semiconductor design capability, and they may choose to leverage those design resources instead of utilizing our services. If this happens and we are unable to offset with additional revenue from existing and new customers in the technology offerings and services we do provide, our results of operations, financial condition, business and prospects may be materially and adversely affected.

Our production operations require that we obtain adequate supplies of raw materials, such as silicon wafers, gases, chemicals and photoresist, on a timely basis and at commercially reasonable prices, many of which are not commodities easily replaced with substitutions. In the past, shortages in the supply of some materials, whether by specific vendors or by the industry generally, have resulted in occasional industry-wide price adjustments and delivery delays. Moreover, major natural disasters, trade barriers and political or economic turmoil occurring within the country of origin of such raw materials may also significantly disrupt the availability of such raw materials or increase their prices. Further, since we procure some of our raw materials from sole-sourced suppliers, including raw materials that are significant to our production operations, there is a risk that our need for such raw materials may not be met or that back-up supplies may not be readily available. In addition, escalating trade tensions between the United States and China, as well as the conflict in Ukraine, have resulted in, and could further exacerbate, substantial price volatility and reduced availability of raw materials, including rare earth metals and natural gas used in our products or in our production operations. Similar price volatility risks may be presented by the conflict in Israel and its potential expansion.…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-27）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/1709048/000170904826000022/gfs-20251231.htm｜as_of：2026-02-27
<<<
GlobalFoundries remains one of the world’s leading semiconductor foundries, manufacturing complex ICs that enable billions of electronic devices that are pervasive throughout nearly every sector of the global economy. Our ability to attract a significant share of single-sourced products is supported by our scaled manufacturing footprint and highly differentiated technology offerings. As we look forward, factors influencing our business performance include: •Global demand for semiconductor products •Customer demand for diversified global semiconductor supply including non-China and non-Taiwan based suppliers •Design wins with new and existing customers •Single-sourced revenue mix •Technology solutions mix and pricing •Long-term agreements •Supply chain •Shipment utilization •Government policy and grants, see “Item 4. Information on the Company - Government Regulations.”

Single-sourced Revenue Mix We manufacture products based on a combination of our own technologies and our customers’ IP, resulting in a significant number of products that can only be sourced from us. Our sales and marketing strategy centers on deepening relationships with top customers and investing in technologies to become their single-source supplier for mission-critical applications. We believe a key measure of our success as a differentiated technology partner to our customers is the mix of our wafer shipment volume attributable to single-sourced business, which represented approximately 63% of wafer shipment volume in 2025. We define single-sourced products as those that we believe can only be manufactured with our technology or cannot be manufactured elsewhere without significant customer redesigns. We believe that single-sourced business will continue to represent a stable percentage of our wafer shipment volume.

End Markets (in millions): Year ended December 31, 2025 2024 Change % Change Smart Mobile Devices $ 2,678 $ 3,048 $ (370) (12.1) % Communications Infrastructure & Data Center 745 577 168 29.1 % Home and Industrial IoT 1,189 1,267 (78) (6.2) % Automotive 1,410 1,206 204 16.9 % Non wafer revenue 769 652 117 17.9 % Total $ 6,791 $ 6,750 $ 41 0.6 % For the year ended December 31, 2025, two of four end markets experienced growth compared to the year ended December 31, 2024. Communications, Infrastructure & Data Center grew 29.1% year-over-year, supported by growth in silicon photonics optical networking and satellite communications. Automotive increased 16.9% year-over-year, driven by continued content expansion, diversification and share gains, supported by growing business associated with the introduction of new products at key customers. Home and Industrial IoT declined 6.2% year over year, primarily due to a reduction of revenue from wafer shipments to certain aerospace and defense (“A&D”) customers with end-of-life products. Smart Mobile Devices decreased by 12.1% year-over-year, primarily due to lower underutilization payments from customers and pricing adjustments where customers are dual sourced. Additionally, non-wafer revenue increased 17.9% year-over-year, driven by strength in license activity and non-recurring engineering services revenue.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
