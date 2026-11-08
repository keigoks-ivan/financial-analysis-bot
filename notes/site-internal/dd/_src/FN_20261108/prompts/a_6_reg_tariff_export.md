你是 stock-analyst v20 DD 的證據採集子 agent。標的：FN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - FN Fabrinet tariff section 232 2026
  - Fabrinet export control OR entity list Electronic Components 2026
  - FN Fabrinet China tariff OR trade restriction 2026
  - Electronic Components tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm｜as_of：2026-08-18
<<<
Trade Regulations We and our suppliers and service providers could be affected by tariffs, embargoes, or other trade restrictions, as well as laws and regulations enacted in response to concerns regarding climate change, conflict minerals, responsible sourcing practices, public health crises, contagious disease outbreaks, or other matters, which could limit the supply of our materials and increase their cost. In addition, compliance with trade regulations may result in disruptions in logistics, which could delay our receipt of materials. We have experienced increased lead times and expedite fees for the supply of materials. The disruption of our supply of parts and materials, including where such disruption results in the extension of our lead times, could have a material adverse effect on our business, results of operations, or financial condition. Similarly, if our customers experience disruptions to their supplies or materials, or the extension of their lead times, they may reduce, cancel, or alter the timing of their purchases with us, which could have a material adverse effect on our business, financial condition and operating results.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1408710/000140871026000028/fn-20260626.htm｜as_of：2026-08-18
<<<
Our customers are located throughout the world, and our principal manufacturing facilities are located in Thailand. Beginning in the fourth quarter of fiscal year 2026, we updated our geographic area presentation from the bill-to-location of our customers to the ship-to-location of our customers. Prior periods have been recast to conform to the current presentation. See Note 3 of the Notes to Consolidated Financial Statements. Revenues from the ship-to-location of customers outside of North America accounted for 77.3%, 78.4% and 81.8% of our revenues for fiscal year 2026, fiscal year 2025 and fiscal year 2024, respectively. We expect that revenues from the ship-to-location of customers outside of North America will continue to account for a significant portion of our revenues. Our customers also depend on international sales, which further exposes us to the risks associated with international operations. Conducting business outside the United States subjects us to a number of risks and challenges, including: •compliance with a variety of domestic and foreign laws and regulations, including trade regulatory requirements; •periodic changes in a specific country or region’s economic conditions, such as recession; •unanticipated restrictions on our ability to sell to foreign customers where sales of products and the provision of services may require export licenses or are prohibited by government action (for example, the U.S.…

We are subject to governmental export and import controls in Thailand, the PRC, Israel and the United States that may limit our business opportunities. Various countries regulate the import of certain technologies and have enacted laws or taken actions that could limit (1) our ability to export or sell the products we manufacture and (2) our customers’ ability to export or sell products that we manufacture for them. The export of certain technologies from the United States and other nations to the PRC is barred by applicable export controls, and similar prohibitions could be extended to Thailand, thereby limiting our ability to manufacture certain products. Any change in export or import regulations or related legislation, shift in approach to the enforcement of existing regulations, or change in the countries, persons or technologies targeted by such regulations could limit our ability to offer our manufacturing services to existing or potential customers, which could harm our business, financial condition and operating results.

We are subject to risks related to changes in U.S. and international trade policies, including new or increased tariffs on materials that we use in manufacturing, which could adversely affect our business, financial condition and operating results.

Our business may be adversely affected by evolving global trade policies, including tariffs and other trade restrictions. We are subject to risks associated with changes in international trade policies, regulations, and relationships. In recent years, multiple countries, including the United States, the PRC, and members of the European Union, among others have enacted tariffs, export controls, quotas, and other forms of trade restrictions on a variety of goods and services. These measures have led to increased costs, supply chain disruptions, and reduced demand across several industries. Although certain tariffs have been reduced or delayed, the potential for future escalation or the imposition of new trade restrictions remains. Ongoing or future trade disputes may impact the availability and cost of materials used in our manufacturing processes. In some cases, suppliers may struggle to meet increased demand resulting from accelerated purchasing ahead of anticipated policy changes, further exacerbating supply chain instability. Additionally, retaliatory actions or changes in trade policies by foreign governments may reduce the demand for our customers’ products in impacted regions, which could lead to reduced orders and revenue for us. If we are unable to mitigate the effects of increased costs or pass them on to our customers, our gross margins, financial condition, and results of operations could be materially and adversely affected.

We anticipate that we will continue to invest in our customized optics manufacturing facilities located in Fuzhou, the PRC. Because these operations are located in the PRC, they are subject to greater political, legal and economic risks than the geographies in which the facilities of many of our competitors and customers are located. In particular, the political and economic climate in the PRC (both at national and regional levels) is fluid and unpredictable. A large part of the PRC’s economy is still being operated under varying degrees of control by the PRC government. By imposing industrial policies and other economic measures, such as control of foreign exchange, taxation, import and export tariffs, environmental regulations, land use rights, intellectual property and restrictions on foreign participation in the domestic market of various industries, the PRC government exerts considerable direct and indirect influence on the development of the PRC economy. Many of the economic reforms carried out by the PRC government are unprecedented or experimental and are expected to change further. Any changes to the political, legal or economic climate in the PRC could harm our business, financial condition and operating results.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
