你是 stock-analyst v20 DD 的證據採集子 agent。標的：OSCR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - OSCR Oscar Health market share gaining OR losing 2026
  - Oscar Health new entrant OR displace threat Healthcare Plans 2026
  - OSCR competitor design win 2026
  - Oscar Health vs Healthcare Plans peers market share trend 2025 2026


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
We compete to hire and retain highly talented individuals from all backgrounds, and we offer our employees compensation packages designed to be competitive and aligned with market best practices. Our compensation packages include base salary and some of the following components, depending on the role, level, and business function: a short-term incentive that takes into account company and individual performance, long-term incentive equity, performance-based equity, commissions, and overtime pay. We believe our compensation philosophy and practice, which is rooted in data and benchmarked to a cohort of peer and broader industry companies, is transparent, systematic, and equitable.

COMPETITION We operate in a highly competitive environment in an industry subject to significant and ongoing changes, including business and hospital system consolidations, new strategic alliances, market pressures, scientific and technological advances in medical care and therapeutics, as well as regulatory and legislative challenges and reform both at the federal and state levels. This reform includes, but is not limited to, the federal and state healthcare reform legislation described under “—Government Regulation.” In addition, changes to the political environment may drive additional shifts in the competitive landscape.

We compete directly and through independent intermediaries to enroll new and retain existing members, as we currently derive substantially all of our revenue from direct policy premiums. We believe that our principal competitive features affecting our ability to retain and increase membership include the range and prices of health plans offered, breadth and quality of provider network, comprehensiveness of coverage, benefits and wellness programs, quality of service, and member experience, responsiveness to member needs, market presence, financial stability, and reputation.

As attracting new members depends in part on our ability to provide access to competitive provider networks, we compete in establishing such provider networks. We believe that the factors providers consider in deciding whether to contract with a health insurer or HMO (a “Health Insurance Entity”) include existing and potential member volume, reimbursement rates, timeliness and accuracy of claims payment and administrative service capabilities. While our Health Insurance Subsidiaries are required to meet various federal and state requirements regarding the size and composition of our participating provider networks, our business model is based on contracting with selected healthcare systems and other providers, not all systems and providers in a given area. This allows us to work more closely with high quality healthcare systems that engage with us using our technology and to negotiate more favorable reimbursement rates from these healthcare systems.

The relative importance of each of the competitive factors mentioned in the above paragraphs and the identity of our principal competitors for members and providers varies by market and geography. Our principal competitors in the individual market primarily consist of plans offered by national carriers, regional carriers, Medicaid-focused insurers offering Health Insurance Marketplaces products, and local Blue Cross plans.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm｜as_of：2026-02-13
<<<
21 Table of Contents Further, we may experience delays in operational start dates as we enter new markets or decide to exit geographic markets or terminate insurance products, which we have done historically from time to time, which could not only result in financial harm, but also reputational harm to our brand. In addition, if competitors seek to retain market share by reducing prices, we may be forced to reduce our prices on similar plan offerings in order to remain competitive. A reduction in our plan pricing may not enable us to maintain our competitive position, and any such reduction could impact our financial condition or require a change in our operating strategies. As a result of these factors, entering new markets or introducing new health plans may decrease our profitability.

We operate in a highly competitive environment and some of the Health Insurance Entities with which we compete have greater financial and other resources, offer a broader scope of products, and may be able to price their products more competitively than ours. Many of our competitors also have relationships with more providers and provider groups than we do, and can offer a larger network or obtain better unit cost economics. Our inability to overcome these challenges could impair our ability to attract new members and retain existing members, and could have a material adverse effect on our business, revenue, operating results, and financial condition. Additionally, if we are not able to grow our membership, we may be unable to attract additional partners to our +Oscar platform or maintain existing +Oscar partnerships, which could impact our ability to execute our growth strategy.

In addition, on February 9, 2026, HHS released the proposed NBPP for policy year 2027. The NBPP is a rulemaking proposal, and it is unknown whether the provisions proposed in the NBPP ultimately will be adopted, either in whole or in part, or what changes to the proposed provisions may ultimately be adopted in the final NBPP. However, the NBPP includes a number of proposed provisions that, if adopted, could significantly impact the Health Insurance Marketplace. For instance, certain of the proposed provisions could provide greater flexibility with respect to plan designs, but given the uncertainty around the final terms of the rule and the short timeline for implementation once finalized, we may or may not be able to take advantage of that flexibility, and in the event that our competitors are able to take advantage of that flexibility and we are not, this could put us at a competitive disadvantage. Certain aspects of the proposed provisions could also lead to new 28 Table of Contents entrants entering the market, or otherwise create market instability.…

We launched our business in 2012 and have limited experience operating our business at current scale. Due to this limited operating history and the rapid growth we have experienced since we began operations, there is greater uncertainty in estimating our operating results, and our historical results may not be indicative of, or comparable to, our future results. In addition, we have limited data to validate key aspects of our business model, including our growth strategy. For example, our efforts to partner with ICHRA platforms to transition small, mid- and large-sized employers to the individual market where their employees can choose an Oscar product may not be successful, take significantly more time than expected to be successful and/or incur significant or unexpected expense. Furthermore, we are a relatively new entrant in the third party services market and in the past have experienced challenges in developing this area of our business. We are unable to predict if we will always be able to effectively and consistently service our current +Oscar arrangements and any future +Oscar arrangements, which risk may increase over time as we enter into more material +Oscar arrangements. In addition, though we recently acquired new business lines, through our purchase of Lucie, Inc.…

While we take precautions designed to protect our intellectual property, it may still be possible for competitors and other unauthorized third parties to copy our technology and use our proprietary brand, content, and information to create or enhance competing solutions and products, which could adversely affect our competitive position in our rapidly evolving and highly competitive industry. Our existing intellectual property, and any intellectual property granted to us, or that we otherwise acquire in the future, may be contested, circumvented, or invalidated. Some license provisions that protect against unauthorized use, copying, decompiling, transfer, and disclosure of our technology may be unenforceable under the laws of certain jurisdictions and foreign countries, and the remedies for such events may not be sufficient to compensate for such breaches. We enter into confidentiality and invention assignment agreements with our employees and consultants, and enter into confidentiality agreements with our third-party providers and strategic partners. These agreements may be breached, and may not be effective in controlling access to, and use and distribution of, our platform and proprietary information. Further, these agreements do not prevent our competitors from independently developing technologies that are substantially equivalent or superior to our offerings.…

49 Table of Contents We have registered, or applied to register, those trademarks that we believe are important to our business, but to date we have not filed patent applications to protect our innovations and proprietary technology. If in the future we decide to file patent applications to protect our innovations and proprietary technology, we do not know whether they would result in the issuance of a patent, or effective copyrights, in our content and proprietary coding, as applicable, or whether the examination process will require us to narrow any proposed patent claims. The applications we file may not result in issued patents, and if patents are issued as a result, they may not allow us to receive competitive advantages or effectively block competitors creating competing technology. In addition, given the costs, effort, and risks of obtaining patent protection, including the requirement to ultimately disclose the invention to the public, we continue to choose not to seek patent protection. Any failure to adequately obtain patent protection, or other intellectual property protection, could later prove to adversely impact our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
