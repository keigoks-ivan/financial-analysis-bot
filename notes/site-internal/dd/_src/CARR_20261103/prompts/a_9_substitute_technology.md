你是 stock-analyst v20 DD 的證據採集子 agent。標的：CARR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Carrier Global product substitute technology threat 2026
  - Building Products & Equipment alternative technology disruption 2026 2027
  - CARR Carrier Global technology obsolescence risk
  - Building Products & Equipment next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-05）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1783180/000178318026000008/carr-20251231.htm｜as_of：2026-02-05
<<<
•Cybersecurity incidents could disrupt business operations, result in the loss of critical and confidential information, and adversely impact our reputation and results of operations.

•We use a variety of raw materials, supplier-provided parts, and third-party service providers in our business. The ability of suppliers to deliver materials, parts, components and manufacturing equipment to our manufacturing facilities, and our ability to manufacture without disruption, could affect our business performance. Significant shortages, supplier capacity constraints or production disruptions, price increases, duties, tariffs or other government actions could increase our operating costs, disrupt our operations and adversely impact the competitive positions of our products.

Our business has been and may again in the future be impacted by disruptions to our or third-party providers’ Technology infrastructure, which have resulted and could in the future result from (among other causes) cyber-attacks, infrastructure failures or compromises to our physical security. Cyber-based risks are evolving and include attacks: (i) on our Technology infrastructure; (ii) targeting the security, integrity and/or availability of hardware and software; (iii) exploiting weaknesses or vulnerabilities in our products, or capturing information installed, stored or transmitted in our products (including after the purchase of those products and when they are installed into, or into environments using, third-party products); and (iv) on facilities or similar infrastructure. Such attacks could disrupt our systems (or those of third parties) and business operations, impact the ability of our products to work as intended or result in the unauthorized access, use, disclosure, modification or destruction of information in violation of applicable law and/or contractual obligations. We continue to make investments and adopt measures to enhance our protection, detection, response and recovery capabilities, and to mitigate potential risks to our technology, products, services, operations and confidential data. However, depending on the nature, sophistication and scope of cyber-attacks, it is possible that potential vulnerabilities could go undetected for an extended period.…

In addition, because of the global nature of our business, our internal systems and products must comply with applicable laws, regulations and standards in a number of jurisdictions, and government enforcement actions and violations of data privacy and cybersecurity laws could be costly or interrupt our business operations. Any disruption to our business arising from such issues, or an increase in our costs to cover these issues that is greater than what we have anticipated, could have an adverse effect on our reputation, competitive position, results of operations, cash flows or financial condition.

In addition, we may be the target of competitor or other third-party patent enforcement actions (for example, brought by owners of Standard Essential Patents or other relevant patents) seeking substantial monetary damages or seeking to prevent the sale and marketing of certain of our products. Our competitive position also may be adversely impacted by limitations on our ability to obtain possession, ownership or necessary licenses concerning data important to the development or sale of our products or service offerings, or by limitations on our ability to restrict the use by others of data related to our products or services. Any of these events or factors could subject us to judgments, penalties and significant litigation costs or temporarily or permanently disrupt our sales and marketing of the affected products or services and could have a material adverse effect on our competitive position, results of operations, cash flows or financial condition.

17 Table of Contents We use a variety of raw materials, supplier-provided parts, finished goods, and third-party service providers in our business. The ability of suppliers to deliver materials, parts, components, finished goods, and manufacturing equipment to our manufacturing facilities, and our ability to manufacture and distribute without disruption, could affect our business performance. Significant shortages, supplier capacity constraints, supplier disputes, supplier quality issues, or production disruptions, price increases, duties, tariffs or other government actions could increase our operating costs, disrupt our operations and adversely impact the competitive positions of our products.

Our reliance on suppliers and commodity markets to secure components (such as motors and valves), finished goods (including products purchased directly from suppliers for resale), and raw materials (such as copper, aluminum and steel), as well as on service providers to deliver our products, exposes us to volatility in the prices and availability of these materials, products, and services. We use a wide range of materials, finished goods, and components in the global production and distribution of our products, which come from numerous suppliers around the world. Because some key parts and finished goods may be available only from a single supplier or a limited group of suppliers, we are subject to supply and pricing risk. In addition, certain proprietary component parts used in some of our products are provided by single-source unaffiliated third-party suppliers. We would be unable to obtain these proprietary components for an indeterminate period of time if these single-source suppliers were to cease or interrupt production or otherwise fail to supply these components to us, which could adversely affect our product sales and operating results. Our supply chain could be impacted by climate events through extreme weather, resulting in delivery or production disruptions and increased material costs.…

Our operations and those of our suppliers are subject to disruption for a variety of reasons, including epidemics, pandemics, supplier plant shutdowns or slowdowns, transportation delays, work stoppages, utility outages, labor relations, changes in laws or regulations, governmental regulatory and enforcement actions, intellectual property claims against suppliers, financial issues such as a supplier bankruptcy, Technology failures and hazards such as fire, earthquakes, flooding or other natural disasters. Insurance for certain disruptions may not be available, affordable or adequate. The effects of climate-related matters, including extreme weather events, long-term changes in temperature levels and water availability may exacerbate these risks. Such disruption has in the past and could in the future interrupt our ability to manufacture certain products. Any significant disruption could have a material adverse impact on our competitive position.

Our research and development efforts, including those that advance environmental sustainability, may not culminate in new technologies or timely products, or may not meet the needs of our customers as effectively as competitive offerings. Our competitors may develop competing technologies that gain market acceptance before or instead of our products. In addition, we may not be successful in anticipating or reacting to changes in the regulatory or policy environments in which our products are sold, and the markets for our products may not develop or grow as we anticipate.

Customers and others may take disruptive actions. From time to time customers and others may seek to become suppliers or integrators of products and services that compete with our own or pursue other strategies to disrupt our business model. For example, an affiliate of a customer in our transport refrigeration business produces refrigeration units for shipping containers that compete with our products, and another one of our transport refrigeration customers produces refrigeration units for truck trailers that compete with our refrigeration units. In addition, our customers or existing or future competitors may seek to introduce non-traditional business models or disruptive technologies and products in the industries in which we participate, resulting in increased competition and new dynamics in these industries.

We must comply with U.S. Foreign Corrupt Practices Act (“FCPA”), antitrust, anti-money laundering, and other anti-corruption and anti-collusion laws. Despite meaningful measures to ensure lawful conduct, which include training, audits and internal control policies and procedures, violations or allegations of violations of such laws may occur, and could disrupt our operations, cause reputational harm, involve significant management distraction, subject us to criminal and civil penalties, as well as disgorgement, and result in a material adverse effect on our competitive position, results of operations, cash flows or financial condition. We could be required to make changes or enhancements to our compliance measures that could increase our costs, and we could be subject to other remedial actions.

The occurrence of one or more natural disasters, power outages or other unexpected events, including hurricanes, fires, earthquakes, volcanic eruptions, tsunamis, floods and other forms of severe weather, health epidemics, pandemics or other contagious outbreaks, conflicts, wars or terrorist acts, in the U.S. or in other countries in which we or our suppliers or customers operate have in the past and could in the future adversely affect our operations and financial performance. Natural disasters, power outages or other unexpected events could damage or close one or more of our facilities or disrupt our operations temporarily or long-term, such as by causing business interruptions or by affecting the availability and/or cost of materials needed for manufacturing. In some cases, we have one factory that can manufacture a specific product or product line. As a result, damage to or the closure of a certain factory or factories may disrupt or prevent us from manufacturing certain products. Existing insurance arrangements may not cover all of the costs or lost cash flows that may arise from such events. The occurrence of any of these events could also increase our insurance and other operating costs or harm our sales.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CARR_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
