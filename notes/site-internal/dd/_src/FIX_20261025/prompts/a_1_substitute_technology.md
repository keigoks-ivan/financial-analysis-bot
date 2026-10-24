你是 stock-analyst v20 DD 的證據採集子 agent。標的：FIX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - product substitute technology threat 2026
  - alternative technology disruption 2026 2027
  - FIX technology obsolescence risk
  - next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1035983/000110465926017530/fix-20251231x10k.htm｜as_of：2026-02-19
<<<
The markets we serve are highly fragmented and competitive. Our industry is characterized by many small companies whose activities are geographically concentrated. We compete on the basis of our technical expertise and experience, financial and operational resources, nationwide presence, industry reputation and dependability. While we believe our customers consider a number of these factors in awarding contracts, a large portion of our work is awarded through a bid process. Consequently, price is often the principal factor in determining which contractor is selected, especially on smaller, less complex projects. Smaller competitors are sometimes able to win bids for these projects based on price alone due to their lower cost and financial return requirements. We expect competition to continue in our industry, presenting us with significant challenges in our ability to maintain strong growth rates and acceptable profit margins. We also expect increased competition from in-house service providers because some of our customers have employees who perform service work similar to the services we provide. Vertical consolidation could also contribute to competition in our industry.…

We may choose to finance future acquisitions with debt, equity, cash or a combination of the three. Future acquisitions could dilute earnings or disrupt the payment of a stockholder dividend. To the extent we make acquisitions, a number of risks will result, including: ● the assumption of material liabilities (including for environmental-related costs); ● failure of due diligence to uncover situations that could result in legal exposure or to quantify the true liability exposure from known risks; ● the diversion of management’s attention from the management of daily operations to the integration of operations; ● difficulties in the assimilation and retention of employees, in the assimilation of different cultures and practices, in the assimilation of broad and geographically dispersed personnel and operations, and the retention of employees generally; 12 Table of Contents ● the risk of additional financial and accounting challenges and complexities in areas such as tax planning, treasury management, financial reporting and internal controls; and ● we may not be able to realize the cost savings, other financial benefits or synergies we anticipated prior to the acquisition.

Our business can be highly cyclical and subject to seasonal and other variations that can result in significant differences in operating results from quarter to quarter. Moreover, our business may be adversely affected by severe weather in areas where we have significant operations, which could have a material adverse effect on our financial condition, results of operations, and cash flows. Repercussions of severe weather conditions may include: ● curtailment of services; ● suspension of operations; ● inability to meet performance schedules in accordance with contracts and potential liability for liquidated damages; ● injuries or fatalities; ● weather-related damage to our facilities; ● disruption of information systems; ● inability to receive machinery, equipment and materials at jobsites; and ● loss of productivity.

​ The last several years have been marked by worldwide political and economic uncertainty resulting from a number of factors, including decreased consumer confidence, the effects of international conflicts such as the wars between Russia and Ukraine and unrest in the Middle East, supply chain disruptions, tariffs, rising energy costs and inflation. This uncertainty has made (and may continue to make) it extremely difficult for our customers, vendors and us to accurately forecast and plan future business activities, and could lead to constrained spending on our services, delays and a lengthening of our business development efforts, the demand for more favorable pricing or other terms, and/or difficulty in collection of our accounts receivable. Our government clients may face budget deficits that prohibit them from funding proposed and existing projects. Further, ongoing political and economic instability has caused (and could continue to cause) supply chain disruptions and volatility in the capital markets, which may increase our costs of capital and limit our ability to access the capital markets at a time when we would like, or need, to raise capital. These conditions could have a material adverse effect on our business, financial conditions, results of operation and cash flows.

Information technology system failures, network disruptions or cybersecurity breaches could adversely affect our business.

We face numerous and evolving cybersecurity risks that threaten the confidentiality, integrity and availability of our IT Systems and Confidential Information, including from diverse threat actors, such as state-sponsored organizations, opportunistic hackers and hacktivists, as well as through diverse attack vectors, such as social engineering/phishing, malware (including ransomware), malfeasance by insiders, human or technological error (including the misuse of artificial intelligence tools by our employees), and as a result of malicious code embedded in open-source software, or misconfigurations, bugs or other vulnerabilities in commercial software that is integrated into our (or our suppliers’ or service providers’) IT Systems, products or services. Because we make extensive use of third-party suppliers and service providers, such as cloud services that support our internal and customer-facing operations, successful cyberattacks that disrupt or result in unauthorized access to third party IT Systems can materially impact our operations and financial results. Remote and hybrid working arrangements at the Company (and at many third-party providers) also increase cybersecurity risks due to the challenges associated with managing remote computing assets and security vulnerabilities that are present in many non-corporate and home networks. Additionally, any integration of artificial intelligence in our or any service providers’ operations, products or services is expected to pose new or unknown cybersecurity risks and challenges.…

Moreover, cyberattacks are expected to accelerate on a global basis in frequency and magnitude as threat actors are becoming increasingly sophisticated in using techniques and tools—including artificial intelligence to engage in automated, targeted, and coordinated attacks—that circumvent security controls, evade detection and remove forensic evidence. Because the techniques used to obtain unauthorized access or sabotage systems change frequently and generally are not identified until they are launched against a target, we may be unable to anticipate these techniques or to implement adequate preventative measures. As a result, we may be required to expend significant resources to protect 16 Table of Contents against the threat of system disruptions and security breaches or to alleviate problems caused by these disruptions and breaches.

IT Systems failures could disrupt our operations by causing transaction errors, processing inefficiencies, the loss of customers, other business disruptions or the loss of Confidential Information. We have in the past experienced system interruptions and delays and expect that such interruptions and delays may occur in the future, given the increasing diversity and sophistication of cybersecurity threats. In addition, our IT Systems could be damaged or interrupted by natural disasters, power loss, or telecommunications failures. These events could impact our customers, employees and reputation and lead to financial losses from remediation actions, loss of business or access to our business data, potential liability or an increase in expenses, all of which may have a material adverse effect on our business. Similar risks could affect our customers and vendors, indirectly affecting us.

We also periodically evaluate the need to upgrade or replace our IT Systems to protect our information technology environment, to stay current on vendor supported products and to improve the efficiency and scope of our IT Systems and information technology capabilities. The implementation of new IT Systems and information technology could adversely impact our operations by requiring substantial capital expenditures, diverting management’s attention, or causing delays or difficulties in transitioning to new IT Systems. In addition, our IT Systems implementations may not result in productivity improvements at the levels anticipated. IT Systems implementation disruption and any other information technology disruption, if not anticipated and appropriately mitigated, could have an adverse effect on our business. Any failure by us or our third party vendors to maintain the security, proper function and availability of our IT Systems or Confidential Information could result in financial losses, interrupt our operations, damage to our reputation, cause us to be in default of material contracts and subject us to liability claims or proceedings (such as class actions), regulatory investigations or enforcement actions, fines and penalties, and/or significant incident response, system restoration or remediation and future compliance costs, any of which could materially and adversely affect our business, financial condition, results of operations, cash flows, and the value of our securities.

Deliberate, malicious acts, including terrorism and sabotage, could damage our facilities, disrupt our operations or injure employees, contractors, customers or the public and result in liability to us.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261025/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
