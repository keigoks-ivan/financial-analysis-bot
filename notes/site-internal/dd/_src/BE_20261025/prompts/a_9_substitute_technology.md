你是 stock-analyst v20 DD 的證據採集子 agent。標的：BE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - product substitute technology threat 2026
  - alternative technology disruption 2026 2027
  - BE technology obsolescence risk
  - next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
Our differentiation is built on several core attributes: rapid time to power versus traditional OEMs and grid upgrades; our emissions profile on various fuels versus competing technologies; high reliability and resilience; modularity and scalability; and capabilities aligned with AI infrastructure requirements, such as load-following. A multi-year trajectory of cost reductions has expanded the markets we can serve and remains a central focus of our plan. These characteristics allow customers to address power availability constraints, manage deployment timelines and build energy strategies with greater certainty. Near-term, we are prioritizing markets and geographies where these needs are most acute.

Flexibility is designed into the architecture. While most Energy Server deployments use natural gas as fuel, there is no combustion, which results in the Energy Server having a better emissions profile versus competing technologies using natural gas. Moreover, the systems can also operate on biogas, hydrogen, or blends of these fuels, allowing customers to transition toward lower-carbon energy pathways without replacing installed assets. This supports quicker and more sustainable near-term power production while enabling long-term transition pathways as energy systems and customer sustainability objectives evolve.

•Resilient: The Energy Server generates power onsite, avoiding exposure to vulnerabilities associated with conventional transmission and distribution lines. When operating on natural gas, the system uses existing underground pipeline infrastructure, which is typically configured with redundant pathways and designed to maintain high fuel availability. This can help mitigate disruptions from certain natural disasters, extreme weather events, or other conditions that may affect the grid.

The past year presented a number of disruptions throughout the global supply chain, which we worked to mitigate by managing supplier allocations, increasing throughput and productivity at existing suppliers, qualifying new suppliers, and eliminating dependency on constrained materials. We have enacted multiple initiatives to mitigate the impact of trade tariffs and other trade protection measures to our cost and supply availability. While our supply chain does not have significant exposure to China, significant tariffs on imports from other countries where we do source materials could materially impact our costs. Looking ahead to 2026, the challenges affecting all global commerce remain high and unchanged, and we remain vigilant to potential increases in lead times with respect to the delivery of some of our components as well as cost due to a variety of factors, including supply shortages, tariffs, shipping delays and labor shortages.

Bloom has an experienced permitting team that develops project-specific strategies intended to leverage Bloom’s advantages for permitting speed and success. As an example, the Energy Server’s emission profile provides for significant air permitting advantages versus competing technologies and the permitting team supports efforts with customers and agencies to effectuate beneficial outcomes. In addition to developing tactical strategies rooted in an understanding of existing regulations and how they might be leveraged for Bloom’s benefit, we actively work to identify places where legislative and statutory reforms might further benefit Bloom and its permitting timelines.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
•Significant disruption to the operations at our headquarters or manufacturing facilities could delay product production.

Many of our competitors, such as traditional utilities and other companies offering distributed generation products, have longer operating histories, customer incumbency advantages, access to and influence with local and state governments, and access to more capital resources than us. Despite advantages offered by our products, prospective customers may still select such competitors to fulfill their energy needs after weighing all of the foregoing and any other applicable considerations. Significant developments in alternative technologies, such as energy storage, wind, solar or hydro power generation, or improvements in the efficiency or cost of traditional energy sources, including coal, oil, natural gas used in combustion, or nuclear power, may materially and adversely affect our business and prospects in ways we cannot anticipate. We may also face new competitors with better technologies, products, or resources. If we fail to adapt to changing market conditions and to compete successfully with grid electricity or new competitors, our growth will be limited, which would adversely affect our business results.

The failure by us to obtain raw materials or components in a timely manner or to obtain raw materials or components that meet our requirements could impair our ability to manufacture our products, increase the costs of our products or solutions, increase the costs of servicing our existing portfolio of products, or impact our ability to ramp our business at a pace to meet growing demand. If we cannot obtain substitute materials or components on a timely basis or on acceptable terms, we could be prevented from delivering our solutions to our customers or service our existing fleet of products, which could result in sales and installation delays, cancellations, penalty payments, warranty breaches, or damage to our brand and reputation, any of which could have a material adverse effect on our business and results of operations. In addition, we rely on our suppliers to meet quality standards, and the failure of our suppliers to meet those quality standards could cause delays in the delivery of our solutions, unanticipated service costs, and damage to our brand and reputation.

Some of the capital equipment used to manufacture our products and some of the capital equipment used by our suppliers has been developed and made specifically for us, are not readily available from multiple vendors, and would be difficult to repair or replace if they did not function properly. If any of these suppliers were to experience financial difficulties or go out of business or if there was any damage to, or a breakdown of, our manufacturing equipment and we could not obtain replacement equipment in a timely manner, our business would suffer. In addition, a supplier’s failure to supply this equipment in a timely manner of adequate quality and on terms acceptable to us could disrupt our production schedule or increase our costs of production and service.

Our IT Systems and those of our third-party providers, are vulnerable to damage from computer viruses, unauthorized access, misuse, natural disasters, terrorism, cybersecurity threats, war and, internet, telecommunications, data network and electrical failures, as well as security compromises or breaches, which may compromise our systems, infrastructure, data or that of those with whom we share such data or information or upon which our business relies, or lead to data compromise, misuse, misappropriation or leakage. Any damage or significant disruption in the operation of our IT Systems or those of our third-party providers or the failure of such systems to perform as expected (including as a result of any of the events noted in the preceding sentence or otherwise) would disrupt our business and could have a material adverse effect us.

We believe that our success and our ability to reach our strategic objectives are highly dependent on the contributions of our key management, technical, engineering, finance and sales personnel. The loss of the services of any of our key employees could disrupt our operations, delay the development and introduction of our products and services and negatively impact our business, prospects and operating results. In particular, we are highly dependent on the services of Dr. Sridhar, our Founder, President, Chief Executive Officer and Director, and other certain key employees. None of our key employees are bound by employment agreements for any specific term and we cannot assure you that we will be able to successfully attract and retain the senior leadership necessary to grow our business. There is intense competition for talented individuals in our industry, particularly in the San Francisco Bay Area where our principal offices are located. Our failure to attract and retain our executive officers and other key management, technical, engineering, finance and sales personnel, could adversely impact our business, our financial condition and our operating results.

Geopolitical and security issues, such as changes in U.S. government and other nations’ administration and their associated shifts in policy and priorities, armed conflict and civil or military unrest, political instability, terrorist activity and public health emergencies, could adversely affect our business, financial condition and operating results. For example: •Trade tensions have risen between the U.S. and China. China as a country supplies multiple components including rare earth metals and compounds used in electronic and electromechanical components that are part of our tier 2 and tier 3 sub-assembly suppliers. The continued escalation of trade tensions between China and the U.S. could impact our ability to source these rare earth metals and components; •Tensions between mainland China and Taiwan have increased significantly in recent years, presenting an elevated risk of hostilities. Our products contain components which are supplied principally from Taiwan. As such, any disruption impacting Taiwan could adversely impact our ability to obtain these components and supply our customers with products. In addition, such events could adversely affect the potential strength of the Taiwan market for our Energy Server product; •The current administration has implemented new and revised tariffs on all U.S. trade partners as well as sanctions, and is in the process of negotiating trade deals.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
