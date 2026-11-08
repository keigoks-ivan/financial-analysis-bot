你是 stock-analyst v20 DD 的證據採集子 agent。標的：HUBS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - HUBS HubSpot market share gaining OR losing 2026
  - HubSpot new entrant OR displace threat Software - Application 2026
  - HUBS competitor design win 2026
  - HubSpot vs Software - Application peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm｜as_of：2026-02-11
<<<
Competition Our market is evolving, highly competitive and fragmented, and we expect competition to increase in the future. We believe the principal competitive factors in our market are: •vision for the market, product strategy and pace of innovation; •marketing focus and domain expertise; •integrated all-in-one customer platform; •breadth and depth of product functionality; •ease of use; •scalable, open architecture; •time to value and total cost of ownership; •integration with third-party applications and data sources; •use of CRM data to make strategic business decisions; •use of evolving AI technologies; •AI agents and automation capabilities that handle end-to-end workflows; •unified data platform with AI-powered data quality and enrichment; 13 •AEO and AI-native marketing capabilities; •name recognition and brand reputation; and •“freemium” go-to-market motion.

We believe we compete favorably with respect to all of these factors. We face intense competition from other companies that develop marketing, sales, customer service, operations, commerce, intelligence and content management software. Our competitors offer various point applications that provide certain functions and features that we provide, including: •cloud-based marketing automation providers; •content management systems; •email marketing software vendors; •sales automation software vendors; •CRM software vendors; •customer service platform vendors; •CPQ and billing solution providers; •commerce and payments solution providers; •data enrichment vendors; •AI agent and providers; •AI-native CRM and workflow automation startups; and •large-scale enterprise suites.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm｜as_of：2026-02-11
<<<
16 The software market in which we operate is evolving, highly competitive and significantly fragmented. With the introduction of new technologies and the potential entry of new competitors into the market, we expect competition to persist and intensify in the future, which could harm our ability to increase sales, maintain or increase renewals and maintain our prices.

We face intense competition from other software companies in the market we operate that provide interactive marketing services. Competition could significantly impede our ability to sell subscriptions to our customer platform on terms favorable to us. Our current and potential competitors may develop and market new technologies including as a result of new or better use of evolving AI technologies, whether through greater investments in AI development, access to higher quality training datasets, or more advanced AI models, that render our existing or future products less competitive, or obsolete. We may also face greater competition from non-specialist solutions relying on generic large language models (“LLMs”), generative AI and general-purpose agents to address a broad range of business needs. As we attempt to sell our products and solutions to new and existing customers, we must convince them that our products and solutions are superior to other solutions available to their organizations, including generic LLMs, software created using natural language prompts and generative AI (referred to as vibe coding) and other emerging technologies. In addition, if these competitors develop products with similar or superior functionality to our platform, we may need to decrease the prices or accept less favorable terms for our platform subscriptions in order to remain competitive.…

Our competitors include: •cloud-based marketing automation providers; •email marketing software vendors; •sales force automation and CRM software vendors; •large-scale enterprise suites; •customer service software providers; and •content management systems.

Our current and potential competitors may have significantly more financial, technical, marketing and other resources than we have, be able to devote greater resources to the development, promotion, sale and support of their products and services, may have more extensive customer bases and broader customer relationships than we have, and may have longer operating histories and greater name recognition than we have. As a result, these competitors may respond faster to new technologies and undertake more extensive marketing campaigns for their products. In a few cases, these vendors may also be able to offer a customer platform at little or no additional cost by bundling it with their existing suite of applications. To the extent any of our competitors has existing relationships with potential customers for either marketing software or other applications, those customers may be unwilling to purchase our platform because of their existing relationships with our competitor. If we are unable to compete with such companies, the demand for our customer platform could substantially decline.

In addition, if one or more of our competitors were to merge or partner with another of our competitors, our ability to compete effectively could be adversely affected. Our competitors may also establish or strengthen cooperative relationships with our current or future strategic distribution and technology partners or other parties with whom we have relationships, thereby limiting our ability to promote and implement our platform. We may not be able to compete successfully against current or future competitors, and competitive pressures may harm our business, operating results and financial condition.

To remain competitive, we must continue to develop new product offerings, applications, features and enhancements to our existing customer platform. Maintaining adequate research and development personnel and resources to meet the demands of the market is essential. If we are unable to develop our platform internally due to certain constraints, such as high employee turnover, lack of management ability or a lack of other research and development resources, we may miss market opportunities. Further, many of our competitors expend a considerably greater amount of funds on their research and development programs, and those that do not may be acquired by larger companies that would allocate greater resources to our competitors’ research and development programs. Our failure to maintain adequate research and development resources, including recruiting and retaining highly qualified personnel, (particularly with AI and machine learning backgrounds), or to compete effectively with the research and development programs of our competitors could materially adversely affect our business.

To execute our business strategy, we must attract and retain highly qualified personnel. In particular, we compete with many other companies for software developers with high levels of experience in designing, developing and managing cloud-based software, or with AI and machine learning backgrounds, as well as for skilled information technology, marketing, sales and operations professionals, and we may not be successful in attracting and retaining the professionals we need. Also, our customer platform domain experts are very important to our success and are difficult to replace. We have from time to time in the past experienced, and we expect to continue to experience in the future, difficulty in hiring and difficulty in retaining highly skilled employees with appropriate qualifications worldwide, particularly for engineers with experience in AI. Many of the companies with which we compete for experienced personnel have greater resources than we do. Other companies that continue to offer a remote or hybrid work environment may increase the competition for such employees from employers outside of our traditional office locations. In addition, if we choose to no longer offer a remote or hybrid work environment, we may face more difficulty in retaining our workforce.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
