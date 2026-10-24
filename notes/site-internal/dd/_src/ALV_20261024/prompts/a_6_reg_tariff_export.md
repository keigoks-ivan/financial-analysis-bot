你是 stock-analyst v20 DD 的證據採集子 agent。標的：ALV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - ALV Autoliv tariff section 232 2026
  - Autoliv export control OR entity list Auto Tier 1 / Passive Safety 2026
  - ALV Autoliv China tariff OR trade restriction 2026
  - Auto Tier 1 / Passive Safety tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
We could experience disruption in our supply or delivery chain, which could cause one or more of our customers to halt or delay production We, as with other component manufactures in the automotive industry, ship our products to customer vehicle assembly facilities throughout the world on a “just-in-time” basis for our customers to maintain low inventory levels. Our suppliers (external suppliers as well as our own production sites) use a similar method in providing raw materials to us. However, this “just-in-time” method makes the logistics supply chain in our industry very complex and vulnerable to disruption. Disruptions in our supply chain may result for many reasons, including closures of one of our own or one of our suppliers’ facilities or critical manufacturing lines due to strikes or other labor disputes, mechanical failures, electrical outages, fires, explosions, critical pollution levels, critical health and safety and other working conditions issues (including epidemics and pandemics), natural disasters, war, geopolitical and economic instability, political upheaval, as well as logistical complications due to labor disruptions, weather or natural disasters, acts of terrorism or violence, mechanical failures, cybersecurity events, and legislation or regulation regarding the transport of hazardous goods. Inflation and pricing pressures have also negatively impacted companies in our supply chain.…

Changes in the source, cost, availability of and regulations pertaining to raw materials and components may adversely affect our profit margins Our business uses a broad range of raw materials and components in the manufacture of our products, nearly all of which are generally available from a number of qualified suppliers. Our industry may be affected from time to time by limited supplies or price fluctuations of certain key components and materials. Strong worldwide demand for certain raw materials has had a significant impact on prices and short-term availability in recent years. Such price increases have materially increased, and could continue to materially increase, our operating costs and materially and adversely affect our profit margins, as direct material costs amounted to approximately 54% of our net sales in 2025, of which approximately half represents raw material costs. Commercial negotiations with our customers and suppliers may not always offset all of the adverse impact of higher raw material, energy, labor, logistics, and commodity costs, including those resulting from tariffs and trade restrictions (including retaliatory tariffs). These negotiations may also not be successful in the future.…

RISKS RELATED TO INTERNATIONAL OPERATIONS Our business is exposed to risks inherent in international operations We currently conduct operations in various countries and jurisdictions, including locating certain of our manufacturing and distribution facilities internationally, which subjects us to the legal, political, regulatory and social requirements and economic conditions in these jurisdictions. Some of these countries are considered growth markets and emerging markets. International sales and operations, especially in growth markets, subject us to certain risks inherent in doing business abroad, including: exposure to local economic conditions; unexpected changes in laws, regulations, trade, or monetary or fiscal policy, including interest rates, foreign currency exchange rates, and changes in inflation rates; foreign tax consequences; inability to collect, or delays in collecting, value-added taxes and/or other receivables associated with remittances and other payments by subsidiaries; exposure to local political turmoil and challenging labor conditions; changes in general economic and political conditions in countries where we operate, particularly in emerging markets; expropriation and nationalization; enforcing legal agreements or collecting receivables through foreign legal systems; wage inflation; currency controls, including lack of liquidity in foreign currency due to governmental restrictions, trade protection policies and currency controls, which may create difficulty in repatriating profits or making other remittances; compliance with the requirements of an increasing body of applicable anti-bribery laws; reduced intellectual property protection in various…

Our international operations also depend upon trade relations between the countries where we manufacture and sell products and those countries in which our customers and suppliers have operations. The current U.S. presidential administration has created uncertainty about the relationships between the U.S. and certain of its trading partners, including with respect to the trade policies and agreements, treaties, government regulations, and the tariffs that apply to trade between the U.S. and other nations. For example, in 2025 the U.S. administration imposed tariffs affecting imports to the U.S. from nearly every country by executive action adopted and modified without predictable timelines, creating increased operational and financial exposure for companies dependent on cross-border trade. Other countries, including China, responded with retaliatory tariffs or, like the European Union, announced it is considering retaliatory tariffs.

Increasing our manufacturing footprint in the growth markets and our business relationships with automotive manufacturers in these markets are particularly important elements of our strategy. As a result, our exposure to the risks described above may be greater in the future, and our exposure to risks associated with developing countries, such as the risk of political upheaval and reliability of local infrastructure, may increase. It could also impact importing certain foreign-produced vehicles into the U.S. Changes in national policy or continued uncertainty could depress economic activity and restrict our access to suppliers or customers and have a material adverse effect on our business, operating results, cash flows, and financial condition. Additionally, trade restrictions or material increases in tariffs could impact our targets, earnings guidance, and estimates. The ultimate impact of any tariffs, including any related responses, are uncertain and will depend on various factors, including the timing of implementation, and the amount, scope, and nature of the tariffs. Any or all of these actions could adversely affect our business, financial condition and cash flows.

Tariffs, sanctions, and geopolitical conflicts may disrupt our multi‑tier automotive supply chain, constrain access to critical components, and adversely affect our production capabilities and financial performance Our operations rely on a geographically distributed, multi‑tier supply chain structure that makes us acutely sensitive to shifts in global trade policy, export‑control regimes, and geopolitical conflict. Recent U.S. trade actions affecting imports from major automotive manufacturing hubs—including broad, rapidly shifting tariff frameworks and sector‑specific levies—have increased global cost volatility and introduced uncertainty regarding long‑term sourcing strategies. Wide‑ranging tariff escalation across key trade partners has reshaped global trade flows and imposed substantial cost burdens on manufacturers dependent on cross‑border supply chains. Such measures can directly affect our ability to procure components and precision‑machined parts at competitive prices. These increased input costs may not be fully recoverable through pricing, particularly under fixed‑price or lifetime‑pricing automotive supply agreements. Semiconductor and sensor sourcing relies heavily on global electronics supply chains, which are increasingly affected by export controls, entity‑list restrictions, and sanctions targeting technology supply routes. Expanding U.S. and international restrictions on transfers of semiconductors and related technologies—such as licensing requirements for chip exports to certain entities—have already produced material disruptions and revenue impacts within the broader electronics ecosystem.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
The effects of the new tariffs imposed in 2025 did not have a significant impact on our profitability in 2025, as we achieved customer compensations for more than 80% of tariff costs. Including the dilutive effect of recovered tariffs, operating margin was negatively impacted by around 20 bps. While it is our ambition and expectation to continue passing tariff costs on to our customers, there is significant uncertainty as future recovery levels may vary. Geopolitical developments and the evolving trade environment are likely to continue creating a challenging and unpredictable operating landscape. Any new, increased or modified tariffs or other trade restrictions could materially affect our operations, customer relationships or cost recovery ability as well as contribute to the uncertainty of industry expectations. We continue to closely monitor the tariff policy environment and remain prepared to be agile to adjust our commercial and operational responses to any such developments.

Outlook for 2026 In addition to the assumptions noted below and our business and market update provided herein, the Company's guidance for 2026 is mainly based on its customer call-offs and the achievement of its targeted cost compensation adjustments with its customers, including no material changes to tariffs or trade restrictions, as compared to what is in effect as of January 23, 2026, as well as no significant changes in the macro-economic environment, changes to customer call-off volatility or significant supply chain disruptions.

45 TRADE AND TARIFFS Autoliv is subject to various international trade regulations and regimes and changes in these regimes could lead to increased compliance costs and costs of raw materials and other components. In addition, political conditions leading to trade conflicts and the imposition of tariffs or other trade barriers between countries in which the Company does business could increase its costs of doing business. The effects of the new tariffs imposed in 2025 did not have a material impact on our profitability in 2025, as we achieved customer compensations for more than 80% of tariff costs. Including the dilutive effect of recovered tariffs, operating margin was negatively impacted by around 20 basis points in 2025.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
