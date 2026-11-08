你是 stock-analyst v20 DD 的證據採集子 agent。標的：GHM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Graham product substitute technology threat 2026
  - Specialty Industrial Machinery alternative technology disruption 2026 2027
  - GHM Graham technology obsolescence risk
  - Specialty Industrial Machinery next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-06-08）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm｜as_of：2026-06-08
<<<
With the acquisition of P3 Technologies, LLC ("P3"), we added scalable and adaptable patent-protected intellectual property that we are leveraging across our customer base. This includes P3's patented multi-channel diffuser ("MCD") and self-contained actuating magnetic pump ("SCAMP"). P3's MCD technology improves the efficiency of pumps and compressors by increasing pressure recovery and measurably increasing operating range. The MCD can be used in new designs or retrofit applications and can work with any pump or compressor that utilizes a centrifugal impeller. SCAMP is a family of positive displacement pumps for low flow, high pressure cryogenic applications compatible with oxygen, hydrogen, methane and nitrogen.

Research and Development Activities During fiscal 2026, fiscal 2025 and fiscal 2024, we spent $6,354, $4,039 and $3,944, respectively, on research and development ("R&D") activities. The majority of our R&D, which is not included in the above numbers, is funded by our customers and is specific to help solve our customers’ problems in order to improve efficiencies, address challenging environments, or redesign for form and function. Additionally, we engineer new products and services for our customers and invest to improve existing products and services that are not customer funded. The portion of R&D that specifically relates to new product development during fiscal 2026, fiscal 2025 and fiscal 2024 was $1,204, $1,124, and $904, respectively. Going forward we expect to increase the amount of our R&D spend on new product development in order to meet our organic growth goals, maintain our technological competitive advantage, and disrupt the markets we serve, but only if those opportunities have the proper return on investment. Going forward we expect our new product development R&D spend, that is not customer funded, to gradually increase to 1% to 2% of revenue and expect to offset a portion of this increase through process improvement and operational efficiencies.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-06-08）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm｜as_of：2026-06-08
<<<
During fiscal 2026, sales to the Defense industry continued to grow and represented 60% of our business compared with 58% and 54% of sales to the Defense industry in fiscal 2025 and 2024, respectively. While these projects are spread across multiple contractors and programs, the end customer for these projects, primarily the U.S. Navy, is the same. This concentration of business could add additional risk to us should there be a disruption, short or long term, in the funding for these projects or our participation in these Defense programs.

Defense orders are subject to annual government funding. A disruption in funding or a lapse in funding could materially and adversely impact our business.

One of our growth strategies is to increase our penetration of Defense opportunities, primarily U.S. Navy-related. Projects for the U.S. Navy and its contractors generally have a much longer order-to-shipment time period than our commercial orders. The time between the awarding of an order and the completion of shipment can take three to seven years. Annual government funding is required to continue the production of this equipment. Disruption of government funding, short or long term, could impact the ability for us to continue our production activity on these orders. Since this business is expected to remain significant as a percentage of our overall business, such a disruption, should it occur, could adversely impact the sales and profitability of our business.

In addition, the U.S. has previously experienced lapses in federal appropriations, which had, in the past, a short-term effect on our business. Any such future lapse (each, a "Government Shutdown") could negatively affect our ability to ship finished products to customers. We rely on federal government personnel, who are not able to perform their duties during a Government Shutdown, to conduct routine business processes related to the inspection and delivery of our products, process export licenses for us, and perform other services for us that, when disrupted, may prevent us from timely shipping products outside the U.S. If we are unable to timely ship our products outside the U.S., there could be a material adverse impact on our results of operations and business. Moreover, our inability to ship products, or the perception by customers that we might not be able to timely ship our products in the future, may cause such customers to look to foreign competitors to fulfill their demand. If our customers look to foreign competitors to source equipment of the type we manufacture, there could be a material and adverse impact on our results of operations and business.

The bladeless mixer industry is characterized by ongoing innovation and technological change. Competitors may develop new technologies or enhanced product features that outperform or otherwise diminish the attractiveness of our current offerings. Our ability to remain competitive depends on successfully anticipating technological trends, investing in research and development and introducing new or improved products in a timely manner. If we fail to keep pace with emerging technologies or shifting customer expectations, our products may become outdated, leading to reduced demand, loss of market share, or pricing pressure, any of which could materially adversely affect our business, financial condition and results of operations.

18 We utilize information systems and computer technology throughout our business. We store sensitive data, classified data, proprietary information and perform engineering designs and calculations on these systems. Threats to these systems, and the laws and regulations governing security of data, including personal data, on information systems and otherwise held by companies is evolving and adding layers of complexity in the form of new requirements and increasing costs of attempting to protect information systems and data and complying with new cybersecurity regulations. Information systems are subject to numerous and evolving cybersecurity threats and sophisticated computer crimes, which pose a risk to the stability and security of our information systems, computer technology, and business. Global cybersecurity threats can range from uncoordinated individual attempts to gain unauthorized access to our information systems and computer technology to sophisticated and targeted measures known as advanced persistent threats and ransomware. The techniques used in these attacks change frequently and may be difficult to detect for periods of time and we may face difficulties in anticipating and implementing adequate preventative measures.…

We have an enterprise resource planning system ("ERP") to assist with the collection, storage, management and interpretation of data from our business activities to support future growth and to integrate significant processes. Our ERP at our Batavia, NY operations is aging and we began implementing a new ERP during fiscal 2024 and is scheduled to go live in fiscal 2027. ERP implementations are complex, distracting to the business and management, and time-consuming and involve substantial expenditures on system software and implementation activities, as well as changes in business processes. Our ERP is critical to our ability to accurately maintain books and records, record transactions, provide important information to our management and prepare our consolidated financial statements. ERP implementations also require the transformation of business and financial processes in order to reap the benefits of the new ERP; any such transformation involves risks inherent in the conversion to a new computer system, including loss of information and potential disruption to our normal operations. Any disruptions, delays or deficiencies in the design and implementation of our new ERP could adversely affect our ability to process orders, provide services and customer support, send invoices and track payments, fulfill contractual obligations, or otherwise operate our business.…

Our business, financial condition and results of operations in the past have been and in the future may be adversely affected as a result of a global health crisis, such as the COVID-19 pandemic. A global health crisis could impact our employees, suppliers, customers, financing sources or others’ ability to conduct business, or negatively affect consumer and business confidence or the global economy. A public health crisis has affected, and could affect in the future, large segments of the global economy, including the markets we operate in, disrupting global supply chains, resulting in significant travel and transport restrictions, and creating significant disruption of the financial markets. Economic uncertainty as a result of any global health crisis could negatively affect our business, suppliers, distribution channels, and customers, including as a result of business shutdowns or disruptions for an indefinite period of time, reduced operations, restrictions on shipping, fabricating or installing products, reduced consumer demand, or customers’ ability to make payments.…

In addition, we operate and compete globally and the response to global health crises by domestic and foreign governments has been and may be in the future varied and those differences may impact our competitiveness. There are uncertain political climates in the regions where our subsidiaries operate, and governmental action in those regions may result in the temporary closure or limited operations of our subsidiaries. Government assistance during a pandemic may also differ between private and public companies, which may provide an advantage to one compared with another. This may affect our competitive position and could disrupt the market access and success of our business compared with other current or new competitors which could have a material adverse impact on our financial condition or results of operation.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
