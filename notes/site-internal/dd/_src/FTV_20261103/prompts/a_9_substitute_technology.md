你是 stock-analyst v20 DD 的證據採集子 agent。標的：FTV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Fortive product substitute technology threat 2026
  - Scientific & Technical Instruments alternative technology disruption 2026 2027
  - FTV Fortive technology obsolescence risk
  - Scientific & Technical Instruments next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1659166/000165916626000007/ftv-20251231.htm｜as_of：2026-02-25
<<<
************************************ The following discussion includes information common to all of our segments. Materials Our manufacturing operations employ a wide variety of raw materials, including electronic components, steel, plastics and other petroleum-based products, aluminum, and copper. Prices of oil and gas affect our costs for freight and utilities. We purchase raw materials from a large number of independent sources around the world. Tariffs affect our costs for impacted materials or components we import into the United States. Based on allocation of annual spend among our various suppliers, no single supplier is material. However, some components that require particular specifications or qualifications are dependent on a single supplier or a limited number of suppliers that can readily provide such components. We utilize a number of techniques to address potential disruption in and other risks relating to our supply chain, including in certain cases the use of safety stock, alternative materials that meet the quality and regulatory requirements, and qualification of multiple supply sources.…

Anti-Bribery and Anti-Corruption Laws Given the international scope of our operations, we are subject to various U.S. and non-U.S. laws outlawing bribes, kickbacks, payoffs, and other improper payments. In particular, the U.S. Foreign Corrupt Practices Act (“FCPA”), the UK Bribery Act, and other similar laws in other jurisdictions prohibit companies, their officers and employees, and their intermediaries from making improper payments to public officials to influence those officials or secure an improper advantage in order to obtain or retain business. In the past several years, there has been a substantial increase in the enforcement of these global anti-bribery and anti-corruption laws. Our operations throughout the world, including in developing countries with heightened risks of corruption, and interactions with individuals who are considered public officials under these laws, such as healthcare professionals in countries with state-run healthcare systems, expose us to the risk of violating these laws. Violations of these laws or even allegations of violations of these laws could pose reputational risks, subject us to investigations and related litigation, cause disruptions to our business, and result in monetary fines and damages and other sanctions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1659166/000165916626000007/ftv-20251231.htm｜as_of：2026-02-25
<<<
ITEM 1A. RISK FACTORS You should carefully consider the risks and uncertainties described below, together with the information included elsewhere in this Annual Report on Form 10-K and other documents we file with the SEC. The risks and uncertainties described below are those that we have identified as material, but are not the only risks and uncertainties facing us. Our business is also subject to general risks and uncertainties that affect many other companies, such as market conditions, economic conditions, geopolitical events, changes in laws, regulations, or accounting rules, fluctuations in interest rates, terrorism, wars or conflicts, major health concerns, natural disasters, or other disruptions of expected business conditions. Additional risks and uncertainties not currently known to us or that we currently believe are immaterial also may impair our business, including our results of operations, liquidity, and financial condition.

If we cannot adjust our manufacturing capacity, supply chain management or the purchases required for our manufacturing activities to reflect changes in market conditions, international trade policies, customer demand and supply chain disruptions, our profitability may suffer. In addition, our reliance upon sole or limited sources of supply for certain materials, components, and services could cause production interruptions, delays and inefficiencies.

We purchase materials, components, and equipment from third parties for use in our manufacturing operations. Our income could be adversely impacted if we are unable to adjust our purchases and supply chain management to reflect any supply chain or transportation disruptions or changes in customer demand and market fluctuations, geopolitical disruptions, severe weather events, increases in demand outpacing supply capabilities, labor shortages, seasonality or cyclicality. During a market upturn or general supply chain disruptions, suppliers have extended lead times, limited supplies, or increased prices. If we cannot purchase sufficient products at competitive prices and quality and on a timely enough basis to meet demand for our products, we may not be able to satisfy market demand, product shipments may be delayed, our costs may increase, or we may breach our contractual commitments and incur liabilities.

We generally sell our products and services in industries that are characterized by rapid technological changes, frequent new product introductions and changing industry standards. If we do not develop innovative new and enhanced products and services on a timely basis, our offerings will become obsolete over time and our competitive position and financial results will suffer. Our success will depend on several factors, including our ability to: •accurately identify customer needs and preferences and predict future needs and preferences; •allocate our research and development funding to products and services with higher growth prospects; •anticipate and respond to our competitors’ development of new products and services and technological innovations; •differentiate our offerings from our competitors’ offerings and avoid commoditization; •innovate and develop new technologies and applications, and acquire or obtain rights to third-party technologies that may have valuable applications in our served markets; •obtain adequate intellectual property rights with respect to key technologies before our competitors do; •successfully commercialize new technologies in a timely manner, price them competitively, and cost-effectively manufacture and deliver sufficient volumes of new products of appropriate quality on time; and •stimulate customer demand for and convince customers to adopt new technologies.

Disruptions in, or breaches in security of, our information technology systems, exfiltration of confidential or sensitive data, and other cyberattacks have adversely affected, and in the future could adversely affect, our business.

We collect, store, have access to and otherwise process certain confidential or sensitive data, including proprietary business information, customer data, personal data, and other information that is subject to privacy and security laws, regulations and/or customer-imposed controls. We rely on information technology systems, some of which are managed by third parties and some of which are managed on a decentralized, independent basis by our operating companies, to process, transmit, and store electronic information (including sensitive data such as confidential business information and personally identifiable data relating to employees, customers, and other business partners), and to manage or support a variety of critical business processes and activities. These systems can be, and in the past have been, damaged, disrupted, accessed, or shut down due to attacks by computer hackers, nation states, cyber-criminals, computer viruses, error or malfeasance by employee or former employees, power outages, hardware failures, telecommunication or utility failures, catastrophes, or other similar events, and in any such circumstances our system redundancy and other disaster recovery planning may be ineffective or inadequate.…

We are subject to a variety of litigation and other legal and regulatory proceedings incidental to our business (or the business operations of previously owned entities), including claims for damages arising out of the use of products or services and claims relating to intellectual property matters, employment matters, tax matters, commercial disputes, disputes with our suppliers or vendors, competition and sales and trading practices, environmental matters, personal injury, insurance coverage, and acquisition or divestiture-related matters, as well as regulatory investigations or enforcement. We may also become subject to lawsuits as a result of past or future acquisitions or as a result of liabilities retained from, or representations, warranties, or indemnities provided in connection with, divested businesses. These lawsuits may include claims for compensatory damages, punitive and consequential damages, and/or injunctive relief. The defense of these lawsuits may divert our management’s attention, we may incur significant expenses in defending these lawsuits, we may experience disruption in supply or sales, and we may be required to pay damage awards or settlements or become subject to equitable remedies that could adversely affect our operations and financial results. Moreover, any insurance or indemnification rights that we may have may be insufficient or unavailable to protect us against such losses.…

Climate change resulting from increased concentrations of carbon dioxide and other greenhouse gases in the atmosphere could present risks to our operations. Physical risk resulting from acute changes (such as hurricane, tornado, wildfire or flooding) or chronic changes (such as droughts, heat waves or sea level changes) in climate patterns can adversely impact our facilities and operations and disrupt our supply chains and distribution systems. Concern over climate change can also result in new or additional legal or regulatory requirements designed to reduce greenhouse gas emissions and/or mitigate the effects of climate change on the environment (such as taxation of, or caps on the use of, carbon-based energy). Any such new or additional legal or regulatory requirements, including extensive disclosure requirements in various jurisdictions, including in the E.U. and domestically, may increase the costs associated with, or disrupt, sourcing, manufacturing and distribution of our products, which may adversely affect our business and financial results. In addition, any failure to adequately address stakeholder expectations with respect to environmental, social and governance matters may result in the loss of business, adverse reputational impacts, diluted market valuations and challenges in attracting and retaining customers and talented employees.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTV_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
