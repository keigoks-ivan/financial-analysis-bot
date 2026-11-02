你是 stock-analyst v20 DD 的證據採集子 agent。標的：LEA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Lear product substitute technology threat 2026
  - Auto Parts alternative technology disruption 2026 2027
  - LEA Lear technology obsolescence risk
  - Auto Parts next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
6 Table of Contents Automotive sales and production can also be affected by the age of the vehicle fleet and related scrappage rates, labor relations issues, unforeseen operational disruptions, labor shortages, fuel prices, regulatory requirements, government initiatives and incentives, trade agreements, tariffs and other non-tariff trade barriers (including recent U.S. tariffs imposed or threatened to be imposed on Mexico, Canada and China, as well as other countries and any retaliatory actions taken by such countries), the availability and cost of raw materials and critical components, logistics issues, cybersecurity incidents, and the availability and cost of credit, as well as vehicle affordability and consumer preferences regarding vehicle powertrains (including preferences regarding electric and hybrid vehicles), size, configuration and features, among other factors. The impact of potential tariffs on our business and financial condition, if any, is subject to a number of factors that are not yet known or are subject to change, including the effective date and duration of such tariffs, the scope and nature of any tariffs, the amount of any tariffs, any countermeasures that the target countries may take in response to such tariffs.…

We continue to embed responsible and sustainable principles into our key business processes and operations. We have developed products such as FlexAir®, a 100% recyclable alternative to traditional foam, ReNewKnit®, a sustainable sueded alternative material that is fully recyclable at its end of life and composed of 100% recycled plastic bottles, and SoyFoamTM, a substitute for certain petroleum-based products. We also have improved energy efficiency in our operations and established climate goals to reduce carbon emissions and increase the use of renewable energy.

We have numerous registered trademarks in the United States and in many foreign countries. The most important of these marks include LEAR CORPORATION® (including our stylized version thereof) and LEAR®, which are widely used in connection with our products and services. Our other principal brands include GUILFORD®, EAGLE OTTAWA®, THAGORA® and IGB AUTOMOTIVE®. ComfortFlex by LearTM technology, ComfortMax Seat by LearTM technology, ConfigurE+TM seating, FlexAir® non-foam alternative, INTU® seating, ProTec® active head restraints, ReNewKnit® fabrics, SoyFoamTM foam substitute and TeXstyleTM fabrics are some of our other trademarks used in connection with certain of our product lines.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
•We operate in a highly competitive industry and efforts by our competitors, as well as new entrants to the industry, to gain market share could adversely affect our financial performance.

We operate in a highly competitive industry. We and most of our competitors are seeking to expand market share with new and existing customers, including in high growth regions. Our customers award business based on, among other things, price, quality, service and technology. Our competitors' efforts to grow market share could exert downward pressure on our product pricing and margins. In addition, the automotive industry has attracted, and will continue to attract, new entrants as a result of the evolving nature of the automotive vehicle market, including the increasing adoption of electric and hybrid vehicles. Certain of these automakers and suppliers are also expanding their operations into regions in which they previously did not have a presence. Traditional automakers are experiencing increased competitive pressures as Chinese domestic automakers continue to expand their market share both in and beyond China. Chinese domestic suppliers that may have lower financial return expectations are also challenging traditional automotive suppliers for market share. Further, the global automotive industry is experiencing a period of significant technological change, including in the areas of electrification and digitization. If we are unable to differentiate our products, maintain a low-cost footprint or compete effectively to win business with newer/emerging automakers, we may lose market share or be forced to reduce prices, thereby lowering our margins.…

•Our increasing use of AI and other emerging technologies may expose us to operational, legal and regulatory risks that could adversely affect our business and reputation.

Our use of AI and machine learning presents risks that could adversely affect our business, financial condition and results of operations. We currently incorporate AI-powered tools into certain internal business operations, such as in our production processes and in certain of our administrative functions. AI algorithms may be flawed, and datasets may be insufficient, inaccurate, biased or otherwise problematic. The rapid evolution and increased adoption of AI technologies may increase the risk of technical disruptions to our operations and the processes and functions for which the technology is deployed. The use of AI tools also raises risks related to privacy and inadvertent disclosure of sensitive information. AI 25 Table of Contents systems may access, process or expose personal, confidential or proprietary data in ways that we do not intend or anticipate. Constraints in hardware (such as GPU availability), power capacity or other supply chain elements may further limit our ability to scale AI responsibly. We also face competitive risk if other companies develop or adopt AI capabilities more effectively, at lower cost or more rapidly than we do. Because our AI capabilities currently depend in part on third-party providers of models, cloud services and infrastructure, changes in their performance, pricing, licensing terms or availability could materially increase our costs.…

•A disruption in our information technology systems, or those of our customers, suppliers, sub-suppliers or other contract parties, including a disruption related to cybersecurity, and other cybersecurity risks, such as a security incident resulting in unauthorized access to or theft of personal or other sensitive information, could adversely affect our financial performance.

We rely on the accuracy, capacity, availability and security of our information technology networks. Despite the security and business continuity measures that we have implemented, including those measures related to cybersecurity, our operational systems (including business, financial, accounting, human resources, product development and manufacturing processes), as well as those of our customers, suppliers and other service providers, and certain of our connected vehicle systems and components that may collect and store sensitive end-user data (which could include personal information) could be breached, disabled or damaged by, without limitation, internal or external threat actors, computer viruses, malware, phishing attacks, denial-of-service attacks, supply chain attacks, human error, ransomware attacks, software bugs, server malfunctions, software or hardware failures, natural or man-made incidents or disasters, or unauthorized physical or electronic access. These types of incidents have become more prevalent and pervasive across industries, including our industry, and are expected to continue, if not increase, in the future. In particular, ransomware or other attacks that are intended to disrupt our and our customers' business operations are becoming increasingly prevalent, particularly for manufacturing companies, and can lead to significant interruptions in operations and the ability to provide products or services, loss of sensitive data and income, reputational harm and diversion of funds.…

Moreover, because the techniques used to gain access to or adversely impact systems often are not recognized until launched against a target, we may be unable to anticipate the methods necessary to defend against these types of attacks, and we cannot predict the extent, frequency or impact these attacks may have on us. It may also be difficult and/or costly to detect, investigate, mitigate, contain and remediate a security incident. Our efforts to do so may not be successful. Actions 26 Table of Contents taken by us or the third parties with whom we work to detect, investigate, mitigate, contain and remediate a security incident could result in outages, data losses and disruptions of our business. In addition, the information technology systems and software that we and our vendors use are vulnerable to outages, breakdowns, software vulnerabilities, coding errors and other damage from service interruptions, system malfunctions, natural disasters, terrorism, war, and telecommunication and electrical failures.…

Pandemics, epidemics or disease outbreaks in the United States or globally have disrupted, and may disrupt in the future, our business, which could materially affect our financial condition including liquidity, operating results and future expectations. Any such events may adversely impact our global supply chain and global manufacturing operations and cause us to again suspend our operations. In particular, we could experience among other things: (1) continued or additional global supply disruptions, including component and material shortages; (2) labor disruptions; (3) an inability to manufacture; (4) a decline in consumer demand; and (5) an impaired ability to access credit and capital markets. Any future public health crises could adversely affect our business, financial condition, operating results and cash flows going forward.

•Global climate change could adversely affect our business. The effects of climate change, such as extreme weather conditions, could impact our business. Such effects could disrupt our operations by, among other things, impacting the availability and cost of materials needed for manufacturing and could increase insurance and other operating costs. These factors may impact our decisions to construct new facilities or maintain existing facilities in areas most prone to physical climate risks, as well as our decisions regarding business strategy, capital allocation and innovation. We could also experience indirect financial risks passed through the supply chain and disruptions that could result in increased prices for our products and the resources needed to produce them.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
