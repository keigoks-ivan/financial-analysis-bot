你是 stock-analyst v20 DD 的證據採集子 agent。標的：LLY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Eli Lilly and product substitute technology threat 2026
  - Drug Manufacturers - General alternative technology disruption 2026 2027
  - LLY Eli Lilly and technology obsolescence risk
  - Drug Manufacturers - General next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm｜as_of：2026-02-12
<<<
Further, public and private payers typically encourage the use of generics as alternatives to branded products. Laws in the U.S. generally allow, and in many cases require, pharmacists to substitute generics that have been rated under government procedures to be essentially equivalent to a branded product. Where substitution is mandatory, it must be made unless the prescribing physician expressly forbids it. In certain countries, intellectual property protection is weak, and we must compete with generic versions of our products at or relatively shortly after launch.

In most international markets, we operate in an environment of government-mandated cost-containment programs, which may include price controls, international reference pricing, discounts and rebates, therapeutic reference pricing (to other, often generic, pharmaceutical choices), health technology assessments, regulatory hurdles, restrictions on physician prescription levels, and mandatory generic substitution. In these markets, healthcare services and the determination of pricing and reimbursement for pharmaceutical products are impacted by government control at the point of care or as the primary payer.

Our active ingredient manufacturing and finishing operations, including formulation, filling, assembling, delivery device manufacturing, and packaging, take place at sites in the U.S., including Puerto Rico, Ireland and a number of other sites throughout the world. To support anticipated demand for our current and prospective products, we have undertaken significant manufacturing expansion initiatives. Investments to increase our manufacturing capacity include new sites in North Carolina, Wisconsin, Indiana, Virginia, Texas, Alabama, Pennsylvania, Ireland, Germany, and the Netherlands. We also utilize third parties for certain active ingredient manufacturing, filling, finishing operations, and for device or component production and assembly. Among other third-party providers, we, and the pharmaceutical industry generally, depend on China-based suppliers for portions of our supply chain. U.S. officials have enacted and continue to consider legislation or other actions that are intended to limit supply chain reliance on China, including the BIOSECURE Act. In addition, historically, geopolitical tensions between the U.S. and China have led to the imposition of tariffs, sanctions, and certain 21 other business restrictions between the U.S. and China. In 2025, the U.S. government imposed new tariffs on Chinese goods, and China responded with tariffs on select U.S. goods.…

However, pharmaceutical production processes are complex, highly regulated, and vary widely from product to product. Shifting or adding manufacturing capacity is a very lengthy process requiring significant capital expenditures, process modifications, and regulatory approvals. Accordingly, developments such as unanticipated demand, unplanned plant shutdowns, manufacturing or quality assurance difficulties at one of our facilities or contracted facilities, failure or refusal of a supplier or contract manufacturer to supply contracted quantities in a timely manner or at all, increases in demand on a supplier, or difficulties in predicting or variability in demand for or supply of our products or those of our competitors have led, and may in the future lead, to interruption or higher costs in the supply of certain products, product shortages, or pauses or discontinuations of product sales in one or more markets. Supply and channel dynamics in some cases also contribute to variability in financial results for our products from period to period.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm｜as_of：2026-02-12
<<<
Cyber-attacks are growing in their frequency, sophistication, and intensity, and are becoming increasingly difficult to detect, mitigate, or prevent. Cyber-attacks come in many forms, including the deployment of harmful malware, exploitation of vulnerabilities (including those of third-party software or systems), denial-of-service attacks, the use of social engineering (including phishing), and other means to compromise the confidentiality, integrity, and availability of IT systems, confidential information, and other data. Breaches 31 resulting in the compromise, disruption, degradation, manipulation, loss, theft, exfiltration, destruction, or unauthorized disclosure or use of confidential information, or the unauthorized access to, disruption of, interference with, or attack of, our IT systems, products and services, can occur in a variety of ways, including negligent or wrongful conduct by employees or others with permitted access to our systems and information, or wrongful conduct by hackers, competitors, organized criminal groups, nation-states, state-sponsored or affiliated groups, current or former company personnel, and other actors. Our third-party partners, including third-party providers of data hosting or cloud services, as well as suppliers, distributors, alliances, and other third parties with whom we may share data, face similar risks, which could affect us directly or indirectly. Third-party access to our proprietary data may also enable such party's development of competing products or enhancement of services sold to competitors, thereby eroding our competitive advantage.…

The failure, inadequacy, or breach of our IT systems or business processes or controls or procedures, the compromise, disruption, degradation, manipulation, loss, theft, exfiltration, destruction, or unauthorized access to, disclosure of, or use of confidential information, or the unauthorized access to, disruption of, or interference with our products and services that rely on IT systems or business processes, could impair our ability to secure and maintain intellectual property rights; result in a product manufacturing interruption or failure, or in the interruption or failure of products or services that rely on IT systems or business processes; damage our operations, patient and other relationships, or reputation; undermine integration activities or otherwise delay or prevent the launch of products; result in unfavorable clinical trial results by virtue of incorrect or unreliable data; expose us to ransom payment, other demands, or paralyze our operations; give rise to legal liability and regulatory action under data protection and privacy laws; require disclosure to government authorities and/or regulators; expose us to civil and criminal investigations; and/or cause us to lose trade secrets or other competitive advantages, any of which effects could endure for a long period of time.…

Difficulties related to supply chain activities have resulted and may in the future result in delays and disruptions in the manufacturing, distribution, and sale of our products and/or product shortages, leading to lost revenue, increased costs, reduced market opportunities, and the possibility of additional market entrants. In select cases, supply constraints may also lead to pauses, discontinuations, or other product availability issues in one or more markets, which could have a material adverse effect on our consolidated results of operations, cash flows, and reputation. Challenges and disruptions may include (i) actual or perceived quality, oversight, or regulatory compliance problems; (ii) equipment, mechanical, data, or IT system vulnerabilities, such as system inadequacies, inadequate controls or procedures, operating failures, unauthorized access, service interruptions or failures, security breaches, malicious intrusions, theft, exfiltration, ransomware or other cyber-attacks from a variety of sources; (iii) labor deficiencies; (iv) inability to obtain single-source or other raw or intermediate materials; or (v) issues related to contractors and suppliers, including the failure, inability, or refusal of a supplier or contract manufacturer to supply contracted quantities in a timely or compliant manner or at all, increases in demand on a supplier with constrained capacity, contractual disputes with our suppliers and contract manufacturers, and vertical integration by competitors within our supply chain.

Outsourcing involves many risks, including the risk that third parties may not perform to our standards or legal requirements; may not produce reliable results; may not perform in a timely manner; may misuse or not maintain the confidentiality, integrity, and availability of confidential and proprietary information relating to us, our clinical trial subjects, or patients; may experience disruption or fail to perform due to IT system vulnerabilities, such as inadequacies, inadequate controls or procedures, operating failures, unauthorized access, service interruptions or failures, security breaches, malicious intrusions, fraud, theft, exfiltration, ransomware or other cyber-attacks; may be unable to satisfy their commitments to us in which case we may not be able to achieve acceptable alternative sourcing; or may fail to perform at all. The foregoing risks may be heightened in jurisdictions outside the U.S., where we may have fewer alternative providers as well as face additional costs, uncertainties, and risks. Among other third-party providers, we, and the pharmaceutical industry generally, depend on China-based suppliers for portions of our supply chain. U.S. officials have enacted and continue to consider legislation or other actions that are intended to limit supply chain reliance on China, including the BIOSECURE Act. In addition, historically, geopolitical tensions between the U.S.…

We deploy AI and other emerging technologies in various facets of our operations and we continue to explore the development and use of AI technologies. We have also entered into, and may continue to enter into, partnerships and collaborations relating to the use of AI technology to aid in drug discovery and other efforts. The rapid advancement of these technologies presents opportunities for us in research, manufacturing, commercialization, and other business endeavors but also entails risks, including that AI-generated content, 34 analyses, or recommendations we utilize could be inadequate, or that our competitors may more quickly or effectively adopt AI capabilities. There are significant risks involved in developing and deploying AI, and there can be no assurance that our usage of AI or our significant investments in AI will enhance our products or services or be beneficial to our business, including our efficiency or profitability. Our use of AI or other emerging technologies could also exacerbate regulatory, cybersecurity, and other significant risks.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LLY_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
