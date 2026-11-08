你是 stock-analyst v20 DD 的證據採集子 agent。標的：AAPL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - AAPL Apple tariff section 232 2026
  - Apple export control OR entity list Consumer Electronics 2026
  - AAPL Apple China tariff OR trade restriction 2026
  - Consumer Electronics tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm｜as_of：2026-11-03
<<<
The Company has a large, global business with sales outside the U.S. representing a majority of the Company’s total net sales, and the Company believes that it generally benefits from growth in international trade. A significant majority of the Company’s manufacturing is performed in whole or in part by outsourcing partners located primarily in China mainland, India, Japan, South Korea, Taiwan and Vietnam, in addition to sourcing from partners and facilities located in the U.S. Global supply chains can be highly concentrated, and an escalation of geopolitical tensions, conflict or instability, particularly in regions where the Company relies on single or limited sources for critical components, such as advanced semiconductors, memory and storage, or that are significant to global commodity markets such as oil, gas, rare earths, and other raw materials, could result in significant disruptions. Restrictions on international trade, such as tariffs and other controls on imports or exports of goods, technologies, including artificial intelligence and super intelligence technologies, or data, can materially adversely affect the Company’s business and supply chain, particularly if such measures apply to countries and regions where the Company generates significant revenue or has significant supply chain operations.…

Beginning in the second quarter of 2025, new tariffs were announced on imports to the U.S., including additional tariffs on imports from China mainland, India, Japan, South Korea, Taiwan, Vietnam and the European Union (“EU”), among others. In response, several countries have imposed, or threatened to impose, reciprocal tariffs on imports from the U.S. and other retaliatory measures. Various modifications to U.S. tariffs have been announced and further changes could be made in the future, which may include additional sector-based tariffs or other measures. The ultimate impact remains uncertain and will depend on several factors, including whether additional or incremental U.S. tariffs or other measures are announced or imposed, to what extent other countries implement tariffs or other retaliatory measures in response, and the overall magnitude and duration of these measures. If tariffs are subsequently rescinded or revoked, the Company may not be able to successfully claim and collect tariff refunds. If disputes and conflicts further escalate, actions by governments in response could be significantly more severe and restrictive.

Much of the Company’s future success depends on the talents and efforts of its team members and the continued availability and service of key personnel, including its Chief Executive Officer, executive team and other highly skilled employees. Experienced personnel in the technology industry are in high demand and competition for their talents is intense, especially in Silicon Valley, where most of the Company’s key personnel are located. Periods of intense competition for talent in particular fields have led and are expected to continue to lead to increased costs as the Company seeks to offer competitive compensation to recruit and retain highly skilled employees. In addition to competition for talent, workforce dynamics are constantly evolving, and the Company must navigate changes effectively in order to achieve its strategic initiatives. Laws and regulations, including immigration, labor and employment laws and export controls, among others, can materially adversely affect the Company’s ability to recruit and retain a highly skilled, global workforce. If the Company does not effectively manage changing workforce dynamics and regulatory requirements, it could materially adversely affect the Company’s culture, operational flexibility, strategy and costs.

For example, the Company’s artificial intelligence efforts may give rise to risks related to, among other things: competition and strategy; recouping costs and returns on investments; product liability; intellectual property infringement; data privacy; cybersecurity; sanctions and export controls; unauthorized access to or inadvertent releases of confidential information or other unexpected access to or use of user information; exposing users to harmful, inaccurate or other negative content or experiences; unintended or unauthorized actions by autonomous or agentic systems; misuse of artificial intelligence by employees and other personnel; changing public sentiment; bias and discrimination; and online safety and protection of minors. While the Company is committed to developing and deploying artificial intelligence responsibly, the Company may be unsuccessful in identifying or resolving all potential issues and failures before they arise. As a result, the Company could be exposed to reputational and competitive harm, regulatory action, legal liability, and other adverse effects to its business.

The Company’s gross margins vary significantly across its products, services, geographic segments and distribution channels and can change over time. The Company’s net sales, gross margins and results of operations are subject to volatility and downward pressure due to a variety of factors, including: industry-wide supply constraints and rising costs for key components such as advanced semiconductors, memory and storage; product pricing pressures and product pricing actions that the Company takes in response to such pressures; increased competition; the Company’s ability to effectively stimulate demand for certain of its products and services; compressed product life cycles; supply shortages; potential increases in the cost of outside manufacturing services, and developing, acquiring and delivering content for the Company’s services; the Company’s ability to manage product quality and warranty costs effectively; shifts in the mix of products and services, or in the geographic, currency or channel mix, including to the extent that regulatory changes require the Company to modify its product and service offerings; investments in new business strategies, including in artificial intelligence technologies; seasonality; changes to the Company’s licensing arrangements, whether as a result of legal proceedings, adverse regulatory developments, changes in commercial relationships or other circumstances; fluctuations in foreign exchange rates; inflation and other macroeconomic pressures; the imposition of new or increased tariffs and other trade restrictions, their overall magnitude and…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-03）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm｜as_of：2026-11-03
<<<
Apple Inc. | 2026 Form 10-K | 24 Tariffs and Other Measures Beginning in the second quarter of 2025, new tariffs were announced on imports to the U.S., including additional tariffs on imports from China mainland, India, Japan, South Korea, Taiwan, Vietnam and the EU, among others. In response, several countries have imposed, or threatened to impose, reciprocal tariffs on imports from the U.S. and other retaliatory measures. On January 14, 2026, initial results were published of the previously announced U.S. Department of Commerce investigation under Section 232 of the Trade Expansion Act of 1962, as amended, into imports of semiconductors, semiconductor manufacturing equipment, and their derivative products, including downstream products that contain semiconductors. The announcement of the initial results of the investigation did not impose any additional tariffs affecting the Company’s products. Separately, on February 20, 2026, the Supreme Court issued a ruling striking down certain tariffs previously imposed under the International Emergency Economic Powers Act of 1977. The Company has applied for a refund of tariffs paid, following the processes established by U.S. Customs and Border Protection, and has recognized any refunds received as a reduction of products cost of sales. Various modifications to U.S.…

Apple Inc. | 2026 Form 10-K | 26 Gross Margin Products and Services gross margin and gross margin percentage for 2026, 2025 and 2024 were as follows (dollars in millions): 2026 2025 2024 Gross margin: Products $ 139,659 $ 112,887 $ 109,633 Services 93,943 82,314 71,050 Total gross margin $ 233,602 $ 195,201 $ 180,683 Gross margin percentage: Products 39.3 % 36.8 % 37.2 % Services 76.2 % 75.4 % 73.9 % Total gross margin percentage 48.8 % 46.9 % 46.2 % Products Gross Margin Products gross margin and gross margin percentage increased during 2026 compared to 2025 primarily due to product mix and tariff refunds, partially offset by higher costs, including memory.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
