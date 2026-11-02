你是 stock-analyst v20 DD 的證據採集子 agent。標的：CMG。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Chipotle Mexican Grill product substitute technology threat 2026
  - Restaurants alternative technology disruption 2026 2027
  - CMG Chipotle Mexican Grill technology obsolescence risk
  - Restaurants next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-04）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm｜as_of：2026-02-04
<<<
The aggressive pace at which we open new restaurants can make it increasingly difficult to recruit and hire sufficient numbers of qualified employees to manage and work in our restaurants, to train employees to deliver a consistently high-quality product and guest experience and to maintain an effective system of internal controls for a dispersed workforce, which could materially harm our business and results of operations. Maintaining appropriate staffing in our restaurants requires precise workforce planning, which has become more complex due to predictive scheduling laws (also called “fair workweek” or “secure scheduling”) and “just cause” termination legislation in certain geographic areas where we operate. The market for qualified talent continues to be competitive and we must continue to offer competitive wages, benefits and workplace conditions to retain qualified employees. We have experienced and may continue to experience challenges in hiring and retaining restaurant employees and in maintaining full restaurant staffing in various locations, which may have resulted in longer wait times for guest orders, temporary closures of the digital make line and decreased employee and guest satisfaction.…

We continue to invest in and utilize emerging technologies that have potential to make business tasks easier, more efficient and less labor intensive, including artificial intelligence and machine learning. These new technologies may not deliver the expected efficiencies and could expose us to new risks, including risks related to cybersecurity, data privacy, inaccuracies, hallucinations, bias or discrimination and claims of intellectual property infringement.

In addition, individuals performing work for us and our third-party business partners may access some of this data, including on personally owned digital devices. To the extent we, a third party or any such individual were to experience a breach of our or their information technology systems that results in the unauthorized access, theft, use, destruction or other compromises of guests’ or employees’ data or confidential information of Chipotle, including through cyber-attacks or other external or internal methods, it could have an adverse impact on our reputation and brand and we could experience a material loss of revenues, a decrease in our ability to retain guests or attract new ones, the imposition of potentially significant costs (including loss of data or payment for recovery of data) and liabilities, loss of business partners and the disruption to our supply chain and business plans. Unauthorized access, theft, use, destruction or other compromises are becoming increasingly sophisticated and may occur through a variety of methods, including attacks using malicious code, vulnerabilities in software, hardware or other infrastructure (including systems used by our supply chain), system misconfigurations, phishing, deepfakes, ransomware, malware or social engineering. Our logging capabilities, or the logging capabilities of third parties, are not always complete or sufficiently granular, affecting our ability to fully understand the scope of security breaches.

Our business is dependent on frequent and consistent deliveries of ingredients that comply with our Food with Integrity specifications, such as dairy (for cheese, sour cream and queso), and beef, pork and chicken that meets our Responsibly Raised requirements. We may experience shortages, delays or interruptions in the supply of ingredients and other supplies to our restaurants due to higher or more lucrative demand from other sources; inclement weather or natural disasters; animal disease outbreaks (such as avian flu); social or labor unrest; shortages of agricultural workers (including due to changes in immigration laws); operational disruptions at our suppliers, distributors or transportation providers (including due to cyberattacks, malware or ransomware); financial distress or insolvency of suppliers or distributors, or the inability of suppliers or distributors to manage adverse business conditions; or other conditions beyond our control. Several states have adopted, and others are considering adopting, extended producer requirement (EPR) laws covering end-of-life management of packaging, which aim to reduce waste and encourage sustainable product design through fees and processing requirements. We could incur shortages of or increased costs for certain food packaging we use due to changes made by our suppliers to comply with these EPR laws. In addition, we have a limited number of suppliers for some of our ingredients, including lemon and lime juice, tomatoes and adobo.…

We have set aggressive goals for the number of new restaurants we plan to open over the next few years. Even in the absence of extraordinary disruptions, we may not be able to increase the capacity of our supply chain to keep pace with our growth and fully meet our future business needs. We have experienced and may in the future experience limited available supplies of Responsibly Raised proteins and ingredients that meet our Food with Integrity specifications. In addition, we rely on independent third-party distributors to maintain an inventory of our ingredients and supplies, and deliver them to our restaurants on a timely, as needed basis. There can be no assurance that our suppliers or distributors will be able to accommodate our planned growth or continue to supply required ingredients at preferential prices or at all. The inability of our suppliers to accommodate our growth in a timely or cost-effective manner could impair our growth and have an adverse effect on our business, financial condition, results of operations, and prospects.

Compliance with these laws and regulations, and future new laws or changes in these laws or regulations that impose additional requirements, can be costly. If the Food and Drug Administration or other government agency adopts new laws and regulations in response to real or perceived emerging food safety, such as concerns over phthalates, PFAS, microplastics or heavy metals in the U.S. food supply, it could impose new processes that disrupt our suppliers’ operations, increase costs or both. Any failure or perceived failure to comply with applicable laws or regulations could result in, among other things, revocation of required licenses, administrative enforcement actions, fines and civil and criminal liability.

18 Table of Contents Our operating results have been, and will continue to be, subject to a number of other macroeconomic and other factors, many of which are largely outside our control. Any one or more of the factors listed below could have a material adverse impact on our business, financial condition, or results of operations: •Rising real estate costs in certain markets; •Supply chain disruptions; •Climate change and extreme weather affecting costs and availability of ingredients; •Changes in tax laws and government regulations, such as the One Big Beautiful Bill Act, enacted in the U.S. in July 2025; •Adverse litigation outcomes; •Inflation and interest rate fluctuations; •Natural or man-made disasters disrupting major markets; •Government shutdowns and election-related impacts globally, including regime change and political and civil unrest; •Terminations of or changes in existing trade agreements among the countries in which we purchase ingredients; and •Tariffs imposed on commodities or goods, including recent tariffs imposed or threatened to be imposed by the U.S. on other countries, and any retaliation measures taken by such countries.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMG_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
