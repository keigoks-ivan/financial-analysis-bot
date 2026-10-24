你是 stock-analyst v20 DD 的證據採集子 agent。標的：META。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Meta Platforms product substitute technology threat 2026
  - Internet Content & Information alternative technology disruption 2026 2027
  - META Meta Platforms technology obsolescence risk
  - Internet Content & Information next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
Competition Our business is characterized by innovation, rapid change, and disruptive technologies. We compete with companies providing connection, sharing, discovery, and communication products and services to users online, as well as companies that sell advertising to businesses looking to reach consumers and/or develop tools and systems for managing and optimizing advertising campaigns. We face significant competition in every aspect of our business, including, but not limited to, companies that facilitate the ability of users to create, share, communicate, and discover content and information online or enable marketers to reach their existing or prospective audiences. We compete to attract, engage, and retain people who use our products, to attract and retain businesses that use our free or paid business and advertising services, and to attract and retain developers who build compelling applications that integrate with our products. We also compete with companies in the development and application of AI, particularly with respect to the development of frontier AI models, as well as the development and delivery of consumer hardware and augmented and virtual reality products and services.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
Some of our current and potential competitors may have greater resources, experience, or stronger competitive positions in certain product segments, geographic regions, or user demographics than we do. For example, some of our competitors may be domiciled in different countries and subject to political, legal, and regulatory regimes that enable them to compete more effectively than us. These factors may allow our competitors to respond more effectively than us to new or emerging technologies and changes in market conditions. We believe that some users, particularly younger users, are aware of and actively engaging with other products and services similar to, or as a substitute for, our products and services, and we believe that some users have reduced their use of and engagement with our products and services in favor of these other products and services. In addition, from time to time we make updates to our products and services to improve the user experience (including to help provide users with safe, positive, age-appropriate experiences), and these changes have had, and may in the future have, the effect of reducing time spent and some measures of user engagement with our products and services.…

We are subject to the risk of public health crises such as pandemics, earthquakes, adverse weather conditions, other natural disasters, terrorism, geopolitical conflict, other physical security threats, power loss, cyber-attacks, and other catastrophic events and crises. For example, the COVID-19 pandemic previously significantly impacted our business and results of operations. In particular, the pandemic led to volatility in the demand for and pricing of our advertising services at various points throughout the pandemic, and we may experience similar effects in the future as a result of other catastrophic events. Such events also expose our business, operations, and workforce to a variety of other risks, including: volatility in the size of our user base and user engagement; delays in product development or releases, or reductions in manufacturing production and sales of consumer hardware, as a result of inventory shortages, supply chain or labor shortages; significant volatility and disruption of global financial markets, which could cause fluctuations in currency exchange rates or negatively impact our ability to access capital in the future; illnesses to key employees, or a significant portion of our workforce, which may result in inefficiencies, delays, and disruptions in our business; and increased volatility and uncertainty in the financial projections we use as the basis for estimates used in our financial statements.…

Our business is dependent on our ability to maintain and scale our technical infrastructure, and any significant disruption in our products and services could damage our reputation, result in a potential loss of users and engagement, and adversely affect our financial results.

Our reputation and ability to attract, retain, and serve our users is dependent upon the reliable performance of our products and services and our underlying technical infrastructure. We have experienced, and may in the future experience, interruptions in the availability or performance of our products and services from time to time. Our systems may not be adequately designed or may not operate with the reliability and redundancy necessary to avoid performance delays or outages 26 Table of Contents that could be harmful to our business. If our products or services are unavailable when users attempt to access them, or if they do not load as quickly as expected, users may not use our products or services as often in the future, or at all, and our ability to serve ads may be disrupted, any of which could adversely affect our business and financial performance. We have experienced such issues to varying degrees from time to time.…

We have designed and built our own data centers and key portions of our technical infrastructure through which we serve our products, and we plan to continue to significantly expand the size of our infrastructure primarily through data centers, subsea and terrestrial fiber optic cable systems, and other projects. The infrastructure expansion we are undertaking is complex and involves projects in multiple locations around the world, including in developing regions that expose us to increased risks relating to anti-corruption compliance, trade compliance, environmental, health, and safety compliance, and political challenges, among others. We have changed, suspended, and terminated certain of these projects as a result of various factors, and may continue to do so in the future. Additional unanticipated delays or disruptions in the completion of these projects, including due to the availability of components, power or network capacity, or any shortage of labor necessary in building portions of such projects, challenges in obtaining required government or regulatory approvals, or other geopolitical challenges or actions by governments, including trade disputes or other developments, may lead to increased project costs, operational inefficiencies, interruptions in the delivery or degradation of the quality or reliability of our products and services, or impairment of assets on our balance sheet.…

We rely on third parties to manufacture and manage the logistics of transporting and distributing our consumer hardware products, which subjects us to a number of risks. The manufacturing of our consumer hardware products depends on a small number of third parties, often with significant operations in a single region such as Asia. We have experienced, and may in the future experience, supply or labor shortages, strikes or other disruptions in logistics and the supply chain, which could result in shipping delays and negatively impact our operations, product development, and sales. We could be negatively affected if we are not able to engage third parties with the necessary capabilities or capacity on reasonable terms, or if those we engage with fail to meet their obligations (whether due to financial difficulties, manufacturing or supply constraints, or other reasons), or make adverse changes in the pricing or other material terms of such arrangements with them. The manufacturing, distribution, and sale of our consumer hardware products also may be negatively impacted by macroeconomic conditions, geopolitical challenges, trade disputes, or other actions by governments or non-state actors (including international conflicts, tariffs, sanctions, export controls, and other measures that restrict international trade) that subject us to supply shortages, increased costs, or supply chain or logistics disruptions.

We also require the suppliers and business partners of our consumer hardware products to comply with laws and certain company policies regarding sourcing practices and standards on labor, trade compliance, health and safety, the environment, and business ethics, but we do not control them or their practices and standards and have experienced violations of these requirements from time to time. If any supplier or business partner violates laws, fails to implement changes in accordance with newly enacted laws, or implements practices or standards regarded as unethical, corrupt, or non-compliant, we could experience supply chain disruptions, government action or fines, canceled orders, or damage to our reputation.

Our industry is prone to cyber-attacks by parties seeking unauthorized access to our data or users' data or to disrupt our ability to provide service or otherwise harm us. Our products and services involve the collection, storage, processing, and transmission of a large amount of data. Any failure to prevent or mitigate security breaches and improper access to or disclosure of our data or user data, including personal information, content, or payment information from users, information from marketers, and other intellectual property or content on our systems, could result in the loss, modification, disclosure, destruction, or other misuse of such data, which could harm our business and reputation and diminish our competitive position. In addition, computer malware, viruses, social engineering (such as spear phishing attacks), scraping, and general hacking continue to be prevalent in our industry, have occurred on our systems, and will occur on our systems in the future. We also regularly encounter attempts to create false or undesirable user accounts, purchase ads, or take other actions on our platform for purposes such as spamming, spreading misinformation, or other illegal, illicit, or otherwise objectionable ends.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
