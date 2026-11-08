你是 stock-analyst v20 DD 的證據採集子 agent。標的：MWA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - MWA Mueller Water Products tariff section 232 2026
  - Mueller Water Products export control OR entity list 工業 — 美國水基建（fire hydrant + iron gate valve + smart water） 2026
  - MWA Mueller Water Products China tariff OR trade restriction 2026
  - 工業 — 美國水基建（fire hydrant + iron gate valve + smart water） tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm｜as_of：2025-11-19
<<<
If significant tariffs or other restrictions continue to be placed on foreign imports by the United States and related countermeasures are taken by impacted foreign countries, our sales and results of operations may be harmed.

If significant tariffs or other restrictions continue to be placed on foreign imports by the United States and related countermeasures are taken by impacted foreign countries, our sales and results of operations may be harmed. For example, ongoing trade tensions between the United States and China have led to a series of significant tariffs being levied on certain of our product categories. Furthermore, the Trump administration has implemented tariffs on foreign imports into the United States from all of our supplier countries, as well as on specific commodities used in our operations, such as steel, aluminum, and copper. The materials subject to these tariffs can be expected to impact our raw material costs as well. If further tariffs are imposed on a broader range of imports, or if further retaliatory trade measures are taken by China or other countries in response to additional tariffs, we may be required to raise our prices or incur additional expenses, which may result in the loss of customers and harm our operating performance, sales and earnings.

The prices of our purchased components and raw materials can be volatile. Our operations require substantial amounts of purchased components and raw materials, such as scrap steel, sand, resin, brass ingot and steel pipe. The cost and availability of these materials are subject to economic forces largely beyond our control, including North American and international demand, inflation, foreign currency exchange rates, freight costs, tariffs, commodity speculation and other external factors, including public health crises (such as the COVID-19 pandemic) or other supply chain challenges. Inflation in material costs has occurred in 2024 and 2025 and we expect it to continue into fiscal 2026.

Geopolitical events, international disputes, wars, terrorism, industrial accidents and other business interruptions can harm or disrupt international commerce as well as the global economy and could have a materially adverse effect on us and our customers, suppliers, logistics providers, distributors and other channel partners. The threat of terrorism and heightened security and military action in response thereto, or any other current or future acts of terrorism, wars, including the Israel-Hamas and Russia-Ukraine wars, and other events, including economic sanctions and trade restrictions, have disrupted the world’s economies and may cause further disruptions that could negatively impact our business, operating results and financial condition.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-19）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm｜as_of：2025-11-19
<<<
Recent Developments In October 2023, the Israel-Hamas war caused a temporary shutdown in our facility in Ariel, Israel. While we reopened the facility in November 2023, the war caused supply chain challenges that hindered our ability to most efficiently manufacture our products produced in Israel. While the facility was adversely impacted by this event, we have mitigated operational risk by expanding our suppliers and improving throughput in order to increase production levels and to meet customer delivery times. While net sales levels have returned to pre-war levels, margin expansion was further hindered by newly implemented tariffs on products manufactured in Israel and imported into the United States.

While newly implemented tariffs are adversely impacting several product lines, Repair and Specialty Valve product lines are bearing most of the higher costs. In response to tariffs that went into effect in the second half of fiscal 2025, we implemented additional pricing actions, which are expected to mostly offset tariff costs in dollar terms but will result in tariff-related impacts being dilutive to margins. As the tariffs remain uncertain and volatile, we will continue to monitor the situation and take appropriate actions to address inflationary and other cost pressures.

At the end of the first quarter, we ceased melting and casting operations at our legacy brass foundry and transitioned production to our state-of-the-art foundry. We expect this transition will improve operational efficiency and enable us to better serve our service brass customers. As part of Mueller’s overall strategy, we will continue investing in our foundries to expand 28 Table of Contents Index to Financial Statements capacity, increase manufacturing efficiencies and strategically position ourselves as the demand for domestic product is expected to increase given the uncertainty in the current geopolitical and tariff environment.

Outlook For fiscal year 2026, we anticipate that consolidated net sales will increase between 1.4% and 2.8% as compared with fiscal 2025. The external operating environment remains uncertain as we face changes in government policies, including possible disruptions to global supply chains resulting from such changes, the interest rate and tariff environment, as well as geopolitical conditions and labor and material inflation and availability. We expect these challenges to continue into fiscal 2026. We continue to anticipate resilient demand associated with the municipal repair and replacement end market driven by the aging water infrastructure and increasing water rates, moderated by budgetary and operational pressures on municipalities. We anticipate that new residential construction activity and new lot and land development will be relatively constrained by the uncertainty in the economy, affordability concerns and interest rate environment, depending on the geographic region.

Our orders and shipments in 2025 reflected a more typical operating environment compared with the high backlog environment we experienced during and after the COVID-19 pandemic. For fiscal 2026, we assume that we will continue to experience a more normalized operating environment leading to normalized seasonality for consolidated net sales. Therefore, we anticipate quarterly consolidated net sales as a percentage of fiscal year 2026 consolidated net sales to be the highest in the third quarter and lowest in the first quarter, with a sequential increase in consolidated net sales in the second quarter as the construction season ramps up for the Spring. For fiscal 2026, we anticipate that inflation will continue to modestly impact manufacturing costs, primarily due to wage inflation, as well as raw materials and purchased parts. In addition, higher direct tariff costs of approximately 3% of costs of goods sold are expected to continue to contribute to inflationary pressures in 2026. While pricing actions were taken in 2025 in response to new tariffs, we will continue to monitor the market and economic conditions impacting our business and take appropriate actions to address inflationary and other cost pressures by implementing price increases, cost containment measures and supplier management measures, among other actions.

Gross profit for 2025 was $516.7 million as compared with $459.0 million in the prior year, an increase of $57.7 million or 12.6%, primarily a result of higher volumes across most product lines, favorable pricing, and benefits from manufacturing performance efficiencies, partially offset by approximately 3% inflation and increased tariffs. Manufacturing performance was negatively impacted by a $4.1 million write-down of inventory and other assets associated with our legacy brass foundry in Decatur, Illinois. Gross margin increased to 36.1% in 2025 as compared with 34.9% in the prior year.

Gross profit for 2025 was $296.3 million as compared with $271.9 million in the prior year, an increase of $24.4 million or 9.0%, primarily as a result of higher volumes in iron gate valves and specialty products, higher pricing and benefits from manufacturing efficiencies, partially offset by approximately 4% inflation and increased tariffs. Gross margin decreased slightly to 35.9% in 2025, as compared with 36.0% in the prior year primarily due to the negative impact of a $4.1 million write-down of inventory and other assets associated with the closure of our legacy brass foundry in Decatur, Illinois.

Gross profit for 2025 was $220.4 million as compared with $187.1 million in the prior year, an increase of $33.3 million or 17.8%, primarily as a result of higher pricing, benefits from manufacturing performance efficiencies, and higher volumes, which were partially offset by increased tariffs and 2% inflation. Gross margin was 36.4% in 2025 and 33.5% in 2024.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
