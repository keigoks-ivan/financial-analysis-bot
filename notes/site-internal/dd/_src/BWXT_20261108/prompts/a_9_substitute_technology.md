你是 stock-analyst v20 DD 的證據採集子 agent。標的：BWXT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - BWX Technologies product substitute technology threat 2026
  - Aerospace & Defense alternative technology disruption 2026 2027
  - BWXT BWX Technologies technology obsolescence risk
  - Aerospace & Defense next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-23）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm｜as_of：2026-02-23
<<<
From time to time, the U.S. Government operates under a continuing resolution to continue funding the U.S. Government. Under such a continuing resolution, funding at amounts consistent with appropriated levels for the prior fiscal year are typically available, subject to certain restrictions, but new contract and program starts are not authorized. During periods covered by a continuing resolution, we expect our key programs will continue to be supported and funded under the continuing resolution. However, during periods covered by a continuing resolution, we may experience delays in new awards of our products and services, and those delays could have a material adverse effect on our financial condition, results of operations and cash flows. If Congress is not able to enact appropriations bills or extend a continuing resolution, the U.S. Government would enter a whole or partial shutdown. Additionally, there is a risk that no continuing resolution would be entered into in certain circumstances, which would also cause a whole or partial government shutdown. In the event of a government shutdown, there is uncertainty regarding which government functions would shut down or continue operations during a lapse in appropriations, and corresponding uncertainty regarding the extent or magnitude of potential impacts to our operations.…

These variations and the risks generally inherent in our industries may result in actual revenues or costs being different from those we originally estimated and may result in reduced profitability or losses on projects. Some of these risks include: •difficulties encountered on our large-scale projects related to the procurement of materials or due to schedule disruptions, equipment performance failures, unforeseen site conditions, rejection clauses in customer contracts or other factors that may result in additional costs to us, reductions in revenue, claims or disputes; •our inability to obtain compensation for additional work we perform or expenses we incur as a result of our customers providing deficient design, engineering information, equipment or materials; •requirements to pay liquidated damages upon our failure to meet schedule or performance requirements of our contracts; and •difficulties in engaging third-party subcontractors, equipment manufacturers or materials suppliers or failures by third-party subcontractors, equipment manufacturers or materials suppliers to perform could result in project delays and cause us to incur additional costs.

Tariffs and other restrictive trade measures may require us to take various actions, including changing suppliers and restructuring business relationships. Changing our operations in accordance with new or changed trade restrictions can be expensive, time-consuming, disruptive to our operations and distracting to management. Tariffs and trade restrictions can be announced with little or no advance notice, and we may not be able to effectively mitigate all adverse impacts from such measures.

Operational Risks Our business could be negatively impacted by security threats, including physical and cybersecurity threats, and other disruptions.

We face various security threats, including cyber threats, threats to the physical security of our facilities and infrastructure (including those that we manage and operate for our customers), and threats from terrorist acts, as well as the potential for business disruptions associated with these threats. Further, security breaches within our supply chain or unauthorized disclosures of confidential information could also adversely affect our business and reputation. Although we utilize a combination of tailored and industry standard security measures and technology to monitor and mitigate these threats, we cannot guarantee that these measures and technology will be sufficient to prevent security threats from materializing.

We have been, and will likely continue to be, subject to cyber-based attacks and other attempts to threaten our information technology systems, including attempts to gain unauthorized access to our proprietary and sensitive information and attacks from computer hackers, viruses, malicious code, internal threats and other security problems. As a U.S. Government contractor, we may be prone to a greater number of these threats than companies in other industries. These threats range from attacks common to most industries to more advanced and persistent threats from highly-organized adversaries targeting us because we are a U.S. Government contractor. We are required to maintain minimum security standards for handling information under our government contracts and failure to do so could result in termination of those contracts. For example, as a contractor to the DoW, we are required to comply with applicable cybersecurity standards, including the DoW's Cybersecurity Maturity Model Certification, ("CMMC") program. CMMC requirements may change over time and could impose additional compliance obligations on us and our suppliers, and failure to meet applicable CMMC requirements could affect our ability to receive or perform certain defense-related contracts. We continue to monitor evolving data-privacy requirements and the use of emerging technologies, such as artificial intelligence, and maintain policies intended to promote their secure and responsible use.…

The costs related to cyber or other security threats or disruptions may not be fully insured or indemnified by other means. Occurrence of any of these events could adversely affect our internal operations, the services we provide to customers, the value of our investment in research and development efforts and other intellectual property, our future financial results, our reputation or our stock price.

In addition, we maintain, replace and/or upgrade current financial, human resources and other information technology systems. These activities subject us to inherent costs and risks associated with replacing and updating these systems, including potential disruption of our internal control structure, substantial capital expenditures, demands on management time and other risks of delays or difficulties in transitioning to new systems or of integrating new systems into our current systems. Our systems implementations and upgrades may not result in productivity improvements at the levels anticipated, or at all. In 17 Table of Contents addition, the implementation of new technology systems may cause disruptions in our business operations. Such disruptions and any other information technology system disruptions, and our ability to mitigate these disruptions, if not anticipated and appropriately mitigated, could have a material adverse effect on our business.

We operate a number of large manufacturing facilities in the U.S. and Canada, including NRC Category 1 and CNSC-licensed nuclear manufacturing and fuel facilities. While we have experienced disruptions due to severe weather, environmental and natural disasters and other natural and man-made events in the past, including a recent facility closure due to Hurricane Helene, none have had a material adverse effect on our business or operations to date. Similar events impacting the facilities of our customers, suppliers and other subcontractors could also impact our business or disrupt our operations. If insurance or other risk mitigating mechanisms are insufficient for us to recover our costs and resume operations in a timely fashion, it could have a material adverse effect on our business, financial condition and results of operations.

Negotiations with labor unions and possible work stoppages and other labor problems could divert management's attention and disrupt operations. In addition, new collective bargaining agreements or amendments to agreements could increase our labor costs and operating expenses.

Our future growth will depend on our ability to continue to innovate by developing and commercializing new product and service offerings. Investments in new technologies involve varying degrees of uncertainties and risk. Commercial success depends on many factors, including the levels of innovation, the development costs and the availability of capital resources to fund those costs, the levels of competition from others developing similar or other competing technologies, our ability to obtain or maintain government permits or certifications, the effectiveness of production, distribution and marketing efforts, market demand, market growth or shrinkage, market acceptance and the costs to customers to deploy and provide support for the new technologies. We may not achieve significant revenue from new product and service investments for a number of years, if at all. Additionally, there can be no assurance that the current technologies that our business relies upon will remain competitive, or that competing technologies will not disrupt our business. Moreover, new products and services may not be profitable, and, even if they are profitable, our operating margins from new products and services may not be as high as the margins we have experienced historically. Lastly, new technologies may not be patentable and, as a result, we may face increased competition.

Among our opportunities involving new technologies, we are developing new medical radioisotope technology. The costs to develop and commercialize this technology require a substantial amount of investment over a period of years, and commercialization of this technology also requires authorizations from government agencies, including the U.S. Food and Drug Administration ("FDA"), Health Canada and the CNSC. There can be no assurance that we will be successful in addressing all of the technological challenges to developing and commercializing this technology or in obtaining the required authorizations 21 Table of Contents from the FDA, Health Canada or the CNSC. In addition, commercialization of the medical radioisotope technology could subject us to product liability claims. The potential also exists for competitors to emerge with alternative technologies. We can provide no assurance that those competitors will not develop and commercialize similar or superior technologies sooner than we can or at a significant cost or price advantage.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
