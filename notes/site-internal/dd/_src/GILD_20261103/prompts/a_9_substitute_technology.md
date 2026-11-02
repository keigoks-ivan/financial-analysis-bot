你是 stock-analyst v20 DD 的證據採集子 agent。標的：GILD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Gilead Sciences product substitute technology threat 2026
  - Biotech / Specialty Pharma alternative technology disruption 2026 2027
  - GILD Gilead Sciences technology obsolescence risk
  - Biotech / Specialty Pharma next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm｜as_of：2026-02-24
<<<
The development of product candidates and investigational therapies in our pipeline is subject to various risks and uncertainties that could result in delays or prevent completion of the development and approval of our product candidates. For more information about these risks and uncertainties, see Item 1A. Risk Factors “We face risks in our clinical trials, including the potential for unfavorable results, delays in anticipated timelines and disruption.” Drug development is inherently risky, and many product candidates and investigational therapies fail during the development process.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm｜as_of：2026-02-24
<<<
We rely on third-party sites to collect patients’ white blood cells, known as apheresis centers, as well as shippers, couriers, and hospitals for the logistical collection of patients’ white blood cells and ultimate delivery of Yescarta and Tecartus to patients. Disruptions or difficulties at these vendors could result in product loss and regulatory action. Apheresis centers may also decline to participate in our quality certification process, or we may be unable to complete such certification in a timely manner or at all, which could delay or constrain our manufacturing and commercialization efforts.

•U.S. Congress has enacted the One Big Beautiful Bill (“OBBB”) Act, which made several changes to the Medicaid program, such as imposing Medicaid work requirements and imposing stricter eligibility and enrollment standards. Most of these policies will take effect in 2027. In addition, the OBBB Act did not extend the availability of enhanced premium subsidies, which subsidize patient premiums for Affordable Care Act (“ACA”) health insurance exchange 19 plans and expired at the end of 2025. If these subsidies are not reinstated, it is possible that patient enrollment in ACA exchange plans could substantially decrease. These changes, individually or in combination, could decrease health insurance coverage for patients taking our medicines, potentially disrupt access to our medicines for some individuals and negatively impact our financial results.

Product Development and Supply Chain Risks We face risks in our clinical trials, including the potential for unfavorable results, delays in anticipated timelines and disruption.

There are also risks associated with the use of third parties in our clinical trial activities. We extensively outsource our clinical trial activities and usually perform only a small portion of the start-up activities in-house. We rely on third-party contract research organizations (“CROs”) to perform most of our clinical studies, including document preparation, site identification, screening and preparation, pre-study visits, training, program management, patient enrollment, ongoing monitoring, site management and bioanalysis. Many important aspects of the services performed for us by the CROs are not within our direct control. If there is any dispute or disruption in our relationships with our CROs, including as a result of legislative or regulatory actions (such as the recently enacted BIOSECURE Act in the U.S.), our clinical trials and regulatory submissions may be delayed and our costs may increase. Moreover, in our regulatory submissions, we rely on the quality and validity of the clinical work performed by our CROs and investigators at the clinical trial sites. If any of their processes, methodologies or results were determined to be invalid, inadequate or in violation of Good Clinical Practices and related regulations, our own clinical data and results and related regulatory approvals may be adversely affected.

The products we develop must be approved for marketing and sale by regulatory authorities and, once approved, are subject to extensive regulation by FDA, EMA and comparable regulatory agencies in other countries. We have filed, and anticipate that we will continue to file, for marketing approval in additional countries and for additional indications and products. These and any future marketing applications we file may not be approved by the regulatory authorities on a timely basis, or at all, and changes or disruptions at FDA or other regulatory agencies, including as a result of budget cuts and employee layoffs, could impair the ability of these agencies to timely review and process our applications. Even if marketing approval is granted for our product candidates, there may be significant limitations on their use. We cannot state with certainty when or whether any of our product candidates under development will be approved or launched; whether we will be able to develop, license or acquire additional product candidates or products; or whether any products, once launched, will be commercially successful.

If we are found to infringe the valid patents of third parties, we may be required to pay significant monetary damages or we may be prevented from commercializing products or may be required to obtain licenses from these third parties. We may not be able to obtain alternative technologies or any required license on commercially reasonable terms or at all. If we fail to obtain these licenses or alternative technologies, we may be unable to develop or commercialize some or all of our products. For example, we are aware of patents and patent applications owned by other parties that such parties may claim to cover the use of our products and research activities. For a description of our pending patent litigation, see Note 12. Commitments and 25 Contingencies of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K.

Actual or threatened outbreaks of epidemic, pandemic or contagious diseases, or other public health emergencies, may significantly disrupt our global operations and adversely affect our business, financial condition and results of operations. As seen during the COVID-19 pandemic, outbreaks can result in global supply chain and logistics disruptions and distribution constraints. The impact of an outbreak or other public health crisis on our results of operations and financial condition would depend on numerous evolving factors, but could involve higher operating expenses, lower demand for our products as a result of governmental, business and individuals’ actions taken in response to such an event (including quarantines, travel restrictions and interruptions to healthcare services, which can impact enrollment in or operation of our clinical trials or limit patients’ ability or willingness to access and seek care), challenges associated with the safety of our employees and safe occupancy of our job sites, and financial market volatility and significant macroeconomic uncertainty in global markets. An outbreak or public health emergency also could amplify many of the other risks described throughout the “Risk Factors” section of this Annual Report on Form 10-K.

•Political instability or disruption in a geographic region where we operate, regardless of cause, including war, terrorism, social unrest and political changes, including in China, Russia, Ukraine, Israel and surrounding areas.

Many of our operations and facilities, including those essential to our manufacturing, R&D and commercialization/distribution activities, are located in regions subject to natural or man-made disasters, such as climate change, earthquakes, hurricanes, rising sea levels and flooding, fires, extreme heat, drought or other extreme weather conditions, or efforts taken by third parties to prevent or mitigate such disasters, such as public safety power shutoffs and facility shutdowns. The severity and frequency of weather-related events has been amplified, and is expected to continue to be amplified, by climate change. Such natural disasters have caused, and in the future may cause, damage to and/or disrupt our operations, which may result in a material adverse effect on our business and financial results. Additionally, our corporate headquarters in Foster City and certain R&D and manufacturing facilities are located in California, a region that is seismically active and prone to wildfires. Our business continuity plans and contingencies, including periodic assessments of our natural disaster risk as part of our overall enterprise risk management program, may be insufficient, and a major earthquake or other natural disaster can result in significant recovery time and a prolonged interruption to our operational and business activities.…

We rely on a number of collaborative relationships with third parties for our sales and marketing performance in certain territories. In some countries, we rely on international distributors for sales of certain of our products. Some of these relationships also involve the clinical development of these products by our partners. Reliance on collaborative relationships poses a number of risks, including the risk that: •we are unable to control the resources our corporate partners devote to our programs or products; •disputes may arise with respect to the ownership of rights to technology developed with our corporate partners; •disagreements with our corporate partners could cause delays in, or termination of, the research, development or commercialization of product candidates or result in litigation or arbitration; •contracts with our corporate partners may fail to provide significant protection or may fail to be effectively enforced if one of these partners fails to perform; •our corporate partners have considerable discretion in electing whether to pursue the development of any additional products and may pursue alternative technologies or products either on their own or in collaboration with our competitors; •our corporate partners with marketing rights may choose to pursue competing technologies or to devote fewer resources to the marketing of our products than they do to products of their own development; and •our distributors and our corporate…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GILD_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
