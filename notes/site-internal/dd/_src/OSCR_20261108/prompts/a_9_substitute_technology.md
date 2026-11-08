你是 stock-analyst v20 DD 的證據採集子 agent。標的：OSCR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Oscar Health product substitute technology threat 2026
  - Healthcare Plans alternative technology disruption 2026 2027
  - OSCR Oscar Health technology obsolescence risk
  - Healthcare Plans next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm｜as_of：2026-02-13
<<<
We continue to believe ICHRA will disrupt employer group coverage and expand individual insurance beyond the traditional ACA market. Our goal is to position Oscar as the preferred carrier for employees enrolling in health insurance through an ICHRA program. Employers can now offer defined contributions to their employees to access Oscar’s suite of products in the markets where Oscar offers health plans. We are partnering with a variety of ICHRA platforms to transition small-, mid- and large-sized employers to the individual market where their employees can choose an Oscar product that meets their individual needs. The businesses that we purchased in 2025, including Lucie, Inc. and IHC Specialty Benefits, Inc., provide important building blocks to support our ICHRA strategy and long-term vision to build the leading consumer health marketplace.

12 Table of Contents Our information systems and applications require continual maintenance, upgrading, and enhancement to meet our current and expected operational needs and regulatory requirements. We aim to regularly upgrade and expand our information systems’ capabilities. For information on risks associated with our information technology systems, see Part I, Item 1A. “Risk Factors—Risks Related to our Business—If we are unable to integrate and manage our information systems effectively, our operations could be disrupted” and “Risk Factors—Risks Related to our Business—If we or our partners or other third parties with whom we collaborate fail to protect confidential information and/or sustain a data security incident, we could suffer increased costs, material financial penalties, exposure to significant liability, adverse regulatory consequences, and reputational harm, which would materially adversely affect our business, results of operations, and financial condition.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm｜as_of：2026-02-13
<<<
Even though the eAPTCs expired at the end of 2025, it is possible that they could be renewed, but the timing of such a decision, and the manner in which the eAPTCs could be renewed, is uncertain and could occur in 2026, which could cause potential disruption and uncertainty for the 2026 OEP. Our failure to effectively anticipate, implement, and manage the operational and regulatory complexities associated with the extension of eAPTCs could also result in a negative member experience and make it difficult to manage membership changes effectively, and negatively affect our reputation, financial condition, and results of operations. If the eAPTCs are renewed, it is possible that a SEP would be initiated which could alter member mix and enrollment levels (including by allowing individuals who enrolled with us during open enrollment to switch to a competitor’s plan), as well as shift consumer behavior. Because these changes would likely occur with limited advance notice and implementation guidance, we may be required to quickly modify our systems, pricing, enrollment processes, and customer support operations to accommodate new eligibility rules, or marketplace workflows. Accelerated timelines increase the risk of operational errors, system disruptions, and member service issues, including delayed or incorrect premium billing, or data reconciliation challenges with federal and state marketplaces.…

Even though the eAPTCs expired at the end of 2025, it is possible that they could be renewed, but the timing of such a decision, and the manner in which the eAPTCs could be renewed, is uncertain and could occur in 2026, which could cause potential disruption and uncertainty for the 2026 OEP. If eAPTCs are renewed, in whole or in part, failure to effectively anticipate, implement, and manage the regulatory and operational complexities could negatively affect our financial condition and results of operations. There are a number of scenarios that regulators could implement, such as requiring plans to refile rates, attempting to reduce premiums on a uniform basis, or requiring us to rebate a portion of our premiums to members or the federal government. Any of these efforts would need to be implemented in a highly compressed timeline, could strain our operational resources and lead to delays, errors, or increased costs, and increase the risk of pricing inaccuracies, margin compression, and/or that premiums are insufficient to cover the cost of our members’ medical expenses. The overall market disruption caused by this uncertainty could also create an unstable operating environment, making it challenging to accurately forecast enrollment and manage our financial outlook.…

Risks Related to the Regulatory Framework that Governs Us Our business activities are subject to ongoing, complex, and evolving regulatory obligations, and to continued regulatory review, which result in significant additional expense and the diversion of our management’s time and efforts. If we fail to comply with regulatory requirements, or are unable to meet performance standards applicable to our business, our operations could be disrupted or we may become subject to significant penalties.

Our Chief Executive Officer, each of our Co-Founders, other members of our senior management team, specialized technology and insurance experts, key technical personnel, and other employees could terminate their relationship with us at any time. The loss of key personnel might significantly delay or prevent the achievement of our strategic business objectives and could harm our business. In addition, much of our essential technology and infrastructure are custom-made for our business by our personnel. The loss of key technology personnel, including members of management, as well as our engineering and product development personnel, could disrupt our operations and harm our business. We also rely on a number of highly-specialized insurance experts, the loss of any one of whom could also have a disproportionate impact on our business. We face significant competition for personnel across all areas of our business, and we may not be able to replace key personnel in a timely manner or at all.

If we are unable to integrate and manage our information systems effectively, our operations could be disrupted.

We make virtual healthcare services available to our members through Oscar Medical Group, in which we do not own any equity or voting interest, and our virtual care availability may be disrupted if our arrangements with providers like the Oscar Medical Group become subject to legal challenges.

49 Table of Contents We have registered, or applied to register, those trademarks that we believe are important to our business, but to date we have not filed patent applications to protect our innovations and proprietary technology. If in the future we decide to file patent applications to protect our innovations and proprietary technology, we do not know whether they would result in the issuance of a patent, or effective copyrights, in our content and proprietary coding, as applicable, or whether the examination process will require us to narrow any proposed patent claims. The applications we file may not result in issued patents, and if patents are issued as a result, they may not allow us to receive competitive advantages or effectively block competitors creating competing technology. In addition, given the costs, effort, and risks of obtaining patent protection, including the requirement to ultimately disclose the invention to the public, we continue to choose not to seek patent protection. Any failure to adequately obtain patent protection, or other intellectual property protection, could later prove to adversely impact our business.

We may be required to spend significant resources in order to monitor, protect, and defend our intellectual property rights. Litigation to protect and enforce our intellectual property rights could be costly, time-consuming, and distracting to management, and could result in the impairment or loss of portions of our intellectual property. Our efforts to enforce our intellectual property rights may be met with defenses, counterclaims, and countersuits attacking the validity and enforceability of our intellectual property rights. Our inability to protect our proprietary technology against unauthorized copying or use, as well as any costly litigation or diversion of our management’s attention and resources, could impair the functionality of our platform, delay introductions of enhancements to our platform, result in our substituting inferior or more costly technologies into our platform, or harm our reputation or brand.

We also recently acquired Lucie, Inc., an approved EDE entity that facilitates consumer enrollment in health insurance coverage, including plans offered on the Health Insurance Marketplaces. The operation of an EDE platform differs significantly from our traditional health insurance operations and exposes us to increased regulatory oversight, operational complexity, and compliance obligations. For example, EDE platforms operate pursuant to approvals, technical requirements, and ongoing oversight by CMS and, in some cases, state regulators. These requirements govern platform functionality, consumer disclosures, data sharing, marketing practices, enrollment processes, and audit rights. Failure to comply with applicable federal or state rules, technical standards, or program guidance could result in corrective action plans, suspension or revocation of EDE approval, civil monetary penalties, reputational harm, or restrictions on our ability to enroll members through the platform. In addition, the EDE platform depends on real-time integration with HealthCare.gov (the Federally Facilitated Marketplace), applicable state-based exchanges, and other third-party systems to determine eligibility, subsidies, and enrollment status. System outages, interface changes, data transmission errors, or delays caused by government systems or third-party service providers could disrupt enrollment activity, impair the consumer experience, lead to inaccurate enrollments, or result in compliance violations.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
