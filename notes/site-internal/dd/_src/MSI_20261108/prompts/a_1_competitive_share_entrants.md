你是 stock-analyst v20 DD 的證據採集子 agent。標的：MSI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MSI Motorola Solutions market share gaining OR losing 2026
  - Motorola Solutions new entrant OR displace threat Mission Critical Communications 2026
  - MSI competitor design win 2026
  - Motorola Solutions vs Mission Critical Communications peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/68505/000006850526000010/msi-20251231.htm｜as_of：2026-02-12
<<<
Competition We operate in highly competitive markets that are sensitive to technological advances. Competitive factors in these markets include product quality and reliability, technological capabilities, cost-effectiveness and industry experience. In operating in these competitive markets, we have broadened how we work with our customers, expanding from our LMR focus to include an integrated suite of physical security solutions via our Video and Command Center capabilities, complemented by our MANET solutions. The interplay of technologies, guided by our deep knowledge of public safety, government, including defense, and enterprise workflows, delivers customers one connected system to unify their critical communications, video security, access control, data, and analytics streams.

We experience widespread competition from a growing number of existing and new competitors.

Our major competitors within our MCN, Video and Command Center technologies include the following companies: Technology Competitor MCN Airbus, BK Technologies, DTC, Doodle Labs, Hytera, iCOM, JVCKenwood Corporation, L3Harris Technologies, Persistent Systems, RCA, Samsung, Sepura, Tait, TrellisWare Technologies, Zebra Video Axis Communications, Axon Enterprise, Bosch, Brivo, Dahua Technology Company, Eagle Eye Networks, ECAM, Flock, Genetec, Hanwha Group, Hikvision, Honeywell, Johnson Controls, Milestone Systems, NetWatch, Pro-Vigil, Rhombus, Verkada Command Center AlertMedia, AT&T, Axon Enterprise, Carbyne, CentralSquare Technologies, Comtech Telecommunications, Everbridge, Hexagon, Intrado, Mark43, Crisis24, Oracle Public Safety, RapidSOS, Tyler Technologies, Versaterm 7 Other Information Backlog Our backlog includes orders that have been received and are believed to be firm. As of December 31, 2025 and December 31, 2024, our backlog was as follows: December 31 (In millions) 2025 2024 Products and Systems Integration $ 3,812 $ 4,135 Software and Services 11,930 10,562 $ 15,742 $ 14,697 Approximately $4.8 billion of backlog is expected to be recognized as revenue during 2026. The firmness of such orders is subject to future events that may cause the amount recognized to change.

As part of our compensation philosophy, we strive to offer and maintain market-competitive wages, incentives and benefits to attract and retain talent, and we review our rewards programs each year in an effort to ensure they are competitive with local market practices in the industries and countries where we operate. Our total rewards package for our global employees includes broad-based stock grants and bonuses, an employee stock purchase plan, healthcare, wellness and retirement benefits, paid parental and family leave, commuter benefits, paid time off (including flexible time off for U.S. exempt employees), flexible work options and other assistance and support for employees going through life-changing events.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/68505/000006850526000010/msi-20251231.htm｜as_of：2026-02-12
<<<
Risks Related to Our Ability to Grow Our Business As we introduce new products and services and enhance existing products and services, we may face increased areas of risk related to the success of such products and services that we may not be able to properly assess or mitigate, as well as increased competition and additional compliance obligations, each of which could harm our reputation, market share, results of operations and financial condition or result in additional obligations or liabilities for our business.

The markets for certain products and services of ours are characterized by evolving technologies, industry standards and customer preferences. For example, the software and video security industries have been characterized by rapidly changing customer preferences in favor of cloud solutions and the adoption of AI capabilities. In some cases, it is unclear what specific technology will be adopted in the market or what delivery model will prevail. As another example, there have been and are currently initiatives by governments in several countries to transition public safety communications away from LMR networks onto public mobile broadband networks. While such initiatives have gained limited traction to date, if customers conclude that public mobile broadband networks, potentially augmented with emerging technologies, provide adequate resiliency, coverage, control, and cost for their critical communication needs, it could adversely affect our MCN sales. Our MCN sales could also be adversely affected by evolving technologies created to defeat encryption or our products’ ability to communicate in a contested environment, which could result in our MCN radios becoming less secure or effective. The process of developing new products and services and enhancing existing products and services to meet such evolving technologies, industry standards and customer preferences is complex, costly and uncertain.…

In addition, new technologies and new competitors continue to enter our markets at a faster pace than in the past, and customer trends also continue to evolve at a rapid pace, resulting in increased competition. We may continue to face increasing competition from both incumbents and emerging competitors as customer contracts become larger, more complicated, and include an expanded range of services or complex product requirements. For example, with our acquisition of Silvus in August 2025 and expanded defense opportunities, we now face increased competition for certain products and services from startups and defense contractors that may have certain competitive advantages. Another area in which we face significant competition is AI. Other companies may develop AI systems that are similar or superior to our technologies or more cost-effective to develop and deploy, and customer demand for AI-based technologies and analytics may continue to increase at a fast rate. The research and development cost we may incur to compete with such AI systems and meet increased customer demand for AI-based technologies and analytics may increase the cost of our products and services. If we are unable to mitigate these risks, our results of operations, financial condition or reputation may be adversely affected.

We rely on the experience of our senior management, most of whom have been with us for many years and as a result have specific knowledge relating to us and our industry that is difficult to replace, and competition for management with experience in the communications industry is intense. A loss of the CEO, a member of senior management, or an engineer or other key employee, particularly to a competitor, could also place us at a competitive disadvantage. In addition, we face increased demands for technical personnel in areas such as software development, which is an area of particularly high demand for skilled employees. We believe that our future success depends in large part on our continued ability to hire, assimilate, retain and leverage the skills of qualified engineers and other highly-skilled personnel needed to develop successful new products or services. In particular, we have faced, and expect to continue to face, intense competition globally for experienced software and cloud computing infrastructure engineers, as well as employees in data science and AI. The compensation and incentives we have available to attract, retain and motivate employees may not meet the expectations of current and prospective employees.…

Our intellectual property rights protect our innovations and technology, and they may also generate income under license agreements. We attempt to protect our proprietary technology with intellectual property in the form of patents, copyrights, trademarks, trade secret laws, confidentiality agreements and other methods. We also generally restrict access to and distribution of our proprietary information. Despite these precautions, it may be possible for a third-party to obtain and use our proprietary information or develop similar technology independently. As we expand our business, including through acquisitions, and compete with new competitors in new markets, the breadth and strength of our intellectual property portfolio in those new markets may not be as developed as in our longer-standing businesses. This may expose us to a heightened risk of litigation and other challenges from competitors in these new markets. In addition, effective patent, copyright, trademark and trade secret protection may be unavailable or limited in certain foreign countries. Unauthorized use of our intellectual property rights by third-parties and the cost of any litigation necessary to enforce our intellectual property rights could have a negative impact on our financial results and competitive position.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
