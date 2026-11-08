你是 stock-analyst v20 DD 的證據採集子 agent。標的：CW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Curtiss-Wright product substitute technology threat 2026
  - Specialty Defense + Commercial Nuclear alternative technology disruption 2026 2027
  - CW Curtiss-Wright technology obsolescence risk
  - Specialty Defense + Commercial Nuclear next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm｜as_of：2026-02-12
<<<
RISKS RELATED TO OUR OPERATIONS Intrusion on our systems could damage our business. We store sensitive data, including intellectual property, proprietary business information, and confidential employee information on our servers and databases. As a result, we are increasingly dependent upon our information systems to operate and manage our business. Our ability to effectively operate and manage our business depends on the security, reliability, and adequacy of our information systems. In addition, various privacy and cybersecurity laws and regulations, both in the U.S. and globally, require us to manage and protect sensitive and confidential information, including personal data of our employees, from disclosure. For example, the European Union’s General Data Protection Regulation, which became effective in May 2018, extends the scope of the European Union data protection laws to all companies processing data of European Union residents, regardless of the company’s location. Despite our implementation of firewalls, switchgear, and other network security measures, our servers, databases, and other systems may be vulnerable to various cyber and other security threats, including those caused by computer hackers, physical or electronic break-ins, sabotage, computer viruses, malware, worms, and similar disruptions from unauthorized access and tampering with our computer systems, including through social engineering such as phishing attacks, coordinated denial-of-service attacks, and similar incidents.…

Our business involves risks associated with complex manufacturing processes. Our manufacturing processes depend on certain sophisticated and high-value equipment. Unexpected failures of this equipment may result in production delays, revenue loss, and significant repair costs. In addition, equipment failures could result in injuries to our employees. Moreover, the competitive nature of our businesses requires us to continuously implement process changes intended to achieve product improvements and manufacturing efficiencies. These process changes may at times result 12 in production delays, quality concerns, and increased costs. Any disruption of operations at our facilities due to equipment failures or process interruptions could have a material adverse effect on our business.

The commercial and government markets in which we operate are characterized by rapidly changing technologies. In addition, product and program needs of our government and commercial customers change and evolve regularly. Accordingly, to remain competitive in the future, we will need to continue to invest financial resources, including through internal research and development, acquisitions, or other teaming arrangements, to: (a) identify emerging technological trends in our current and target markets; (b) develop and manufacture competitive products, systems, and services; (c) enhance our offerings by adding technological innovations that differentiate our products, systems, and services from those of our competitors; and (d) develop, manufacture, and bring those products, systems, and service to market quickly at cost-effective prices. These expenditures could divert our attention and resources from other projects, and we cannot be sure that these expenditures will ultimately lead to the timely development of new offerings and technologies or identification of and expansion into new markets. Due to the design complexity of our products, we may, in the future, experience delays in completing the development and introduction of new products. Any delays could result in increased costs of development or deflect resources from other projects.…

Any significant disruption in the commercial nuclear power industry, including delays in the development of small modular reactors, could adversely affect our results of operations or future outlook.

Climate change regulations at the federal, state, or local level or in international jurisdictions could require us to limit emissions, change our manufacturing processes, obtain substitute materials which may cost more or be less available, increase our investment in control technology for greenhouse gas emissions, fund offset projects, or undertake other costly activities. These regulations could significantly increase our costs and restrict our manufacturing operations by virtue of requirements for new equipment. New permits may be required for our current operations, or expansions thereof. Failure to timely receive permits could result in fines, suspension of production, or cessation of operations at one or more facilities. In addition, restrictions on carbon dioxide or other greenhouse gas emissions could result in significant costs such as higher energy costs and the passing down of carbon taxes, emission cap and trade programs, and renewable portfolio standards by utility companies. The cost of complying, or of failing to comply, with these and other climate change and emissions regulations could have an adverse effect on our operating results.

Although we have significant discretionary funding capacity through our generation of significant operating cash flows coupled with access to the credit markets, our ability to fund our operations could be negatively impacted by the following factors: (a) global macroeconomic uncertainty, (b) the ongoing trade disputes between the United States, Canada, and China, (c) armed conflicts around the world, such as those in Ukraine, (d) any conflict or threatened conflict between China and Taiwan (including the imposition of related sanctions by the United States and other countries as well as measures taken in response to such sanctions), (e) any prolonged future U.S. government shutdown, (f) inflationary pressures, (g) rising interest rates, (h) labor shortages, (i) global supply chain disruptions, and (j) uncertainty regarding the stability of global credit and financial markets. In addition, certain of our customers and suppliers could be affected directly by an economic downturn and could face credit issues or cash flow problems that could give rise to payment delays, increased credit risk, bankruptcies, and other financial hardships, which could impact customer demand for our products as well as our ability to manage normal commercial relationships with our customers and suppliers.…

Approximately 6% of our workforce is employed under collective bargaining agreements, which from time to time are subject to renewal and negotiation. We cannot ensure that we will be successful in negotiating new collective bargaining agreements, that such negotiations will not result in significant increases in the cost of labor, including healthcare, pensions, or other benefits, or that a breakdown in such negotiations will not result in the disruption of our operations, including by way of strikes or work stoppages. Although we have generally enjoyed good relations with both our unionized and non-unionized employees, we may experience an adverse impact on our operating results if we are subject to labor actions.

Despite our concerted effort to minimize risk to our production capabilities and corporate information systems and to reduce the effect of unforeseen interruptions through insurance or other risk transfer mechanisms, such as our business continuity planning and disaster recovery plans, we could be adversely impacted by terror attacks, war (including the Russia-Ukraine war), natural disasters such as earthquakes, hurricanes, floods, tornadoes, ice storms, climate change-related events, or other events such as strikes by the workforce of a significant customer or supplier (e.g., the International Association of Machinists and Aerospace workers union work stoppages at Boeing). Several of our facilities, because of their locations, could be subject to catastrophic loss caused by the above-mentioned natural disasters. Global climate change may aggravate natural disasters and increase severe weather events that affect our business operations. These risks could negatively impact demand for or supply of our products and could also cause disruption to our facilities or systems, which could also interrupt operational processes and adversely impact our ability to manufacture our products and provide services and support to our customers. The insurance we maintain may be insufficient to cover our losses, and any incidents may result in loss of, or increased costs of, such insurance.…

A pandemic, including COVID-19 or other epidemic or public health emergency, together with preventative measures taken to contain or mitigate such crises, could impact our business, operations and financial condition in a variety of ways, such as: (i.) impact our customers such that the demand for our products and services could change; (ii.) disrupt our supply chain and impact the ability of our suppliers to provide products or services as required; (iii.) disrupt our ability to sell and provide our products and services and otherwise operate effectively; (iv.) increase incremental costs resulting from the adoption of preventative measures and compliance with regulatory requirements; (v.) create financial hardship on customers, including by creating restrictions on their ability to pay for our products and services; and (vi.) result in closures of our facilities or the facilities of our customers or suppliers. Even after a public health crisis subsides, there may be long-term effects on our business practices and customers in economies in which we operate that could severely disrupt our operations and could have a material adverse effect on our business, operations, and financial results. As we cannot predict the duration, scope or severity of future public health crises, the negative financial impact to our results cannot be reasonably estimated and could be material.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
