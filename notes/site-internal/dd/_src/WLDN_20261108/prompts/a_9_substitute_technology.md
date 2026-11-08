你是 stock-analyst v20 DD 的證據採集子 agent。標的：WLDN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Willdan Group product substitute technology threat 2026
  - Engineering & Construction alternative technology disruption 2026 2027
  - WLDN Willdan Group technology obsolescence risk
  - Engineering & Construction next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm｜as_of：2026-02-27
<<<
Our overall growth strategy revolves around a combination of strong organic expansion and strategic acquisitions which provides us the ability to expand the breadth and depth of the services we provide to new and existing clients. We believe that we are well positioned to capitalize on the ongoing expansion and transformation of the energy and infrastructure environments as they adapt to climate change and other environmental challenges, electrification, and technology advancements, including the growing demand in load growth being fueled by artificial intelligence (“AI”) data centers, electric vehicles and other political and technological changes.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1370450/000110465926020767/wldn-20260102x10k.htm｜as_of：2026-02-27
<<<
Our engagements often involve large-scale, complex projects. The quality of our performance on such projects depends in large part upon our ability to manage the relationship with our clients and our ability to effectively manage the project and deploy appropriate resources, including third-party contractors and our own personnel, in a timely manner. We may commit to a client that we will complete a project by a scheduled date or that, when completed, a project will achieve specified performance standards (e.g., some of our contracts stipulate certain energy savings requirements). If the project is not completed by the scheduled date or fails to meet required performance standards, we may either incur significant additional costs or be held responsible for the costs incurred by the client to rectify damages due to late completion or failure to achieve the required performance standards. The uncertainty of the timing of a project can present difficulties in planning the amount of personnel needed for the project. If the project is delayed or canceled, we may bear the cost of an underutilized workforce that was dedicated to fulfilling the project.…

Unavailability or cancellation of third-party insurance coverage would increase our overall risk exposure as well as disrupt the management of our business operations.

18 Table of Contents If any of our third-party insurers fail, suddenly cancel our coverage, or otherwise are unable to provide us with adequate insurance coverage, then our overall risk exposure and our operational expenses would increase and the management of our business operations would be disrupted. In addition, if we expand into new markets, we may not be able to obtain insurance coverage for these new activities or, if insurance is obtained, the dollar amount of any liabilities incurred could exceed our insurance coverage. There can be no assurance that any of our existing insurance coverage will be renewable upon the expiration of the coverage period or that future coverage will be affordable at the required limits.

​ Events outside our control, including natural and man-made disasters, could negatively impact the economies in which we operate or disrupt our operations, which may adversely affect our business, results of operations and financial condition.

Risks Related to Growth and Acquisitions Acquisitions could disrupt our operations and adversely impact our business, results of operations and financial condition as a result of our failure to conduct due diligence effectively, or our inability to successfully integrate the acquiree. This could impede us from realizing all of the benefits of the acquisitions, which could weaken our results of operations.

​ Acquisitions involve certain known and unknown risks that could cause our actual growth or operating results to differ from our expectations or the expectations of securities analysts. If we fail to conduct due diligence on our potential targets effectively, we may, for example, not identify problems at target companies, or fail to recognize incompatibilities or other obstacles to successful integration. Our inability to successfully integrate future acquisitions within the intended timeframes or at all could impede us from realizing all of the benefits of those acquisitions and could severely weaken our business operations. The integration process may disrupt our business and, if implemented ineffectively, may preclude realization of the full benefits expected by us and could harm our results of operations. In addition, the overall integration of the combining companies may result in unanticipated problems, expenses, liabilities and competitive responses and may cause our stock price to decline.

In the ordinary course of business, we have been and may be in the future be targeted by malicious cyber-attacks. Cybersecurity attacks in particular are evolving, and we and the third parties with whom we work face the constant risk of cybersecurity threats, including, among other things, computer viruses, malicious code, social-engineering attacks (including through deep fakes, which may be increasingly more difficult to identify as fake, and phishing attacks), denial-of-service attacks, credential stuffing attacks, credential harvesting, personnel misconduct or error, ransomware attacks, supply-chain attacks, software bugs, server malfunctions, software and hardware failures, attacks enhanced or facilitated by AI, and other electronic security breaches that could lead to disruptions in critical systems, unauthorized, unlawful, or accidental acquisition, modification, destruction, loss, encryption, access to, release or other compromise of confidential or sensitive information. In particular, severe ransomware attacks are becoming increasingly prevalent and can lead to material adverse consequences. Such threats are prevalent and continue to rise, are increasingly difficult to detect, and come from a variety of sources, including traditional computer “hackers,” threat 28 Table of Contents actors, “hacktivists,” organized criminal threat actors, personnel (such as through theft or misuse), sophisticated nation states, and nation-state-supported actors.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
