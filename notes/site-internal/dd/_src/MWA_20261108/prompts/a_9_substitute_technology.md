你是 stock-analyst v20 DD 的證據採集子 agent。標的：MWA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Mueller Water Products product substitute technology threat 2026
  - 工業 — 美國水基建（fire hydrant + iron gate valve + smart water） alternative technology disruption 2026 2027
  - MWA Mueller Water Products technology obsolescence risk
  - 工業 — 美國水基建（fire hydrant + iron gate valve + smart water） next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm｜as_of：2025-11-19
<<<
Water Leak Detection and Pipe Condition Assessment Products and Services. Water Management Solutions develops technologies and offers products and services under the Echologics® brand name that can non-invasively (i.e., without disrupting service or introducing a foreign object into the water system) detect underground leaks and assess the condition of water mains comprised of a variety of materials. We leverage our proprietary acoustic technology to offer leak detection and condition assessment surveys. We also offer fixed leak detection systems that allow customers to continuously monitor and detect leaks on water distribution and transmission mains. We believe Water Management Solutions’ ability to offer non-invasive leak detection and pipe condition assessment services is a key competitive advantage. With our Singer Valve and i2O products, we provide a range of intelligent water solutions including pressure control valves, advanced pressure management, network analytics, event management and data logging.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm｜as_of：2025-11-19
<<<
We offer several technologically enhanced, complex hardware and software products, services and solutions that can be negatively impacted by design and manufacturing defects. Defects can also exist in components and products we purchase from third parties. Component defects could make our products unsafe and create a risk of environmental or property damage and personal injury. In addition, our products, services and solutions can have quality issues and from time-to-time experience outages, disruptions, slowdowns or errors. As a result, our products and services may not perform as anticipated and may not meet customer expectations. There can be no assurance we will be able to detect and fix all issues and defects in products, services and solutions we offer. Failure to do so can result in widespread technical and performance issues negatively impacting our products, services and solutions. In addition, we can be exposed to product liability claims, recalls, product replacements or modifications, write-offs of inventory, property, plant and equipment, and/or intangible assets, and significant warranty and other expenses, including litigation costs. Quality problems can also adversely affect the experience for our customers and result in harm to our reputation, loss of competitive advantage, poor market acceptance, reduced demand for products, services and solutions, new products, services and solutions introduction delays and lost sales.

In addition, compliance with the laws, regulations and taxes of multiple international jurisdictions increases our cost of doing business. International operations are subject to anti-corruption laws and anti-competition regulations, among others. For example, the United States Foreign Corrupt Practices Act and similar anti-corruption laws outside of the United States generally prohibit companies and their intermediaries from making improper payments or providing anything of value to improperly influence foreign government officials and certain others for the purpose of obtaining or retaining business or obtaining an unfair advantage. Violations of these laws and regulations could result in criminal and civil sanctions, disrupt our business and adversely affect our brands, international expansion efforts, business and operating results.

13 Table of Contents Index to Financial Statements These relationships reduce our direct control over production. Our reliance on these vendors subjects us to a greater risk of shortages, and reduced control over delivery schedules of products, as well as a greater risk of increased product costs. In instances where we stock lower levels of product inventories, a disruption in product availability could harm our financial performance and our ability to satisfy customer needs. In addition, defective products from these manufacturers could reduce product reliability and harm our reputation.

A disruption within our logistics or supply chain network at any of the freight companies that deliver components for our manufacturing operations in the United States or ship our fully assembled products to our customers could adversely affect our business and result in lost sales and increased expenses or harm to our reputation. Our supply chain is dependent on third-party ocean-going container ships, rail, barge, air and trucking systems and, therefore, disruption in these logistics services because of weather-related problems, such as hurricanes, strikes, bankruptcies, inflation, public health crises, such as pandemics, or other events could adversely affect our financial performance and financial condition, negatively impacting sales, profitability and cash flows.

The Israel-Hamas war caused a temporary shutdown in our facility in Ariel, Israel, in October 2023. While we continue to operate the facility since reopening in November 2023, continued disruptions and escalations of conflicts in the area may increase the likelihood of supply interruptions and may continue to hinder our ability to acquire the necessary materials we need to make our products. Supply disruptions from lack of access to materials has impacted, and continues to impact, our ability to produce and deliver our products on time and at favorable pricing.

Transportation costs are relatively high for most of our products. Transportation costs can be an important factor in a customer’s purchasing decision. Many of our products are big, bulky and heavy, which tends to increase transportation costs. We also have relatively few manufacturing sites, which tends to increase transportation distances to our customers and consequently increases our transportation costs. Additionally, energy and fuel costs can fluctuate markedly, which may result in significant cost increases particularly for the price of oil and gasoline. High transportation costs could make our products less competitive compared to similar or alternative products offered by competitors.

We depend on the Internet and our information technology infrastructure for electronic communications among our locations around the world and among our personnel, suppliers and customers. Cyber and other data security breaches of this infrastructure can create system disruptions, shutdowns or unauthorized disclosure of confidential information. Likewise, if we or our service providers are unable to prevent future cybersecurity incidents, our operations could be disrupted, or we may suffer financial, reputational or other harm. We continue to incur costs in connection with efforts to investigate potential threats, assess relevant impacts, enhance our data security and protect against unauthorized access to, or manipulation of, our systems and data. Despite incurring these costs, we may not be able to prevent future cyber incidents. Further, customers and third-party providers increasingly demand rigorous contractual provisions regarding privacy, cybersecurity, data protection, confidentiality and intellectual property, which may also increase our overall compliance burden and related costs.

Further, we face risks of competitive disadvantage if our competitors more effectively leverage AI to drive operational efficiencies, create new or enhanced products, services and solutions or otherwise disrupt the marketplace. Failure to effectively develop, implement, use and manage AI may negatively impact our ability to compete, reduce revenue and adversely impact our business.

Concern over climate change also may result in additional legal or regulatory requirements designed to reduce or mitigate the effects of carbon dioxide and other greenhouse gas emissions on the environment. Many of our manufacturing plants use significant amounts of electricity generated by burning fossil fuels, which release carbon dioxide. Increased energy or compliance costs and expenses as a result of increased legal or regulatory requirements may cause disruptions in, or an increase in the costs associated with, the manufacturing and distribution of our products. The impacts of climate change and legal or regulatory initiatives to address climate change could have a long-term adverse impact on our business and results of operations. Climate change and efforts to limit climate change may impair our production capabilities, disrupt our supply chain or impact demand for our products. If we fail to achieve or improperly report on our progress toward achieving our goals and commitments to reduce our carbon footprint or in environmental and sustainability programs and initiatives, the results could have an adverse impact on our business and results of operations.

Geopolitical events, international disputes, wars, terrorism, industrial accidents and other business interruptions can harm or disrupt international commerce as well as the global economy and could have a materially adverse effect on us and our customers, suppliers, logistics providers, distributors and other channel partners. The threat of terrorism and heightened security and military action in response thereto, or any other current or future acts of terrorism, wars, including the Israel-Hamas and Russia-Ukraine wars, and other events, including economic sanctions and trade restrictions, have disrupted the world’s economies and may cause further disruptions that could negatively impact our business, operating results and financial condition.

Future outbreaks of infectious diseases may result in widespread or localized health crises that adversely affect general commercial activity and the economies and markets of the countries and localities in which we operate, sell and purchase goods and services. Any outbreak of infectious disease poses the risk that we or our employees, contractors, suppliers, customers, transportation providers and other business partners may be prevented or impaired from conducting ordinary business activities for an indefinite period of time, including self-imposed facility shutdowns to protect the health and well-being of our employees or government-mandated shutdowns. In addition, our suppliers, business partners and customers may also experience similar negative impacts. Global supply chains may be disrupted, causing shortages, which could impact our ability to manufacture or supply our products. This disruption of our employees, distributors, suppliers and customers may impact our sales and future operating results.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
