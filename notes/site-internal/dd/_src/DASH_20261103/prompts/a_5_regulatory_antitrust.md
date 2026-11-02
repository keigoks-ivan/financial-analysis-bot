你是 stock-analyst v20 DD 的證據採集子 agent。標的：DASH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - DASH DoorDash antitrust OR monopoly investigation 2026
  - DoorDash regulation OR regulatory scrutiny Internet Retail 2026
  - DASH DoorDash DOJ OR FTC OR EU competition 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm｜as_of：2026-02-18
<<<
Item 3. Legal Proceedings
We are currently involved in, and may in the future be involved in, legal proceedings, claims, regulatory inquiries, audits, and governmental investigations (collectively, “Legal Proceedings”) in the ordinary course of business, including suits by merchants, consumers, Dashers, or other third parties (individually or as class actions).
The outcomes of our Legal Proceedings are inherently unpredictable and subject to significant uncertainties. When we determine that we have meritorious defenses to any claims asserted, we defend ourselves vigorously; however, we also consider settlement of disputes when, in management’s judgment, it is in the best interests of both DoorDash and its shareholders to do so. For some matters for which a material loss is reasonably possible, an estimate of the amount of loss or range of losses is not possible nor are we able to estimate the loss or range of losses that could potentially result from the application of nonmonetary remedies. Until the final resolution of Legal Proceedings, there may be an exposure to a material loss in excess of the amount recorded or non-monetary damages.
Except as set forth below, we are not, and have not been within the past 12 months, party to any material administrative, legal, or arbitration proceeding that may have or have had a significant effect on the financial position or profitability of DoorDash, and we are not aware of any such proceedings being pending or threatened.
Independent contractor classification matters
We have in the past been, are currently, and may in the future be subject to claims, lawsuits, arbitration proceedings, administrative actions, government investigations, and other legal and regulatory proceedings at the federal, state, and municipal levels challenging the classification of Dashers on our platform as independent contractors, and claims that, by the alleged misclassification, we have violated various labor and other laws that would apply to delivery employees. Laws and regulations that govern the status and classification of independent contractors are subject to change and divergent interpretations by various authorities, which can create uncertainty and unpredictability for us.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm｜as_of：2026-02-18
<<<
We are or may become subject to a variety of laws in the United States and other jurisdictions, including those related to worker classification, Dasher pay and conditions of work, Dasher onboarding and deactivation, Dasher safety, engagement of fleet companies and other third-party service providers, insurance, merchant pricing and commissions, 32 Table of Contents consumer pricing and fees, gratuities, taxes, and other laws governing our relationships with merchants, consumers, and Dashers. In addition, we are or may become subject to more broadly applicable laws governing issues such as worker classification, labor and employment, anti-discrimination, food safety, alcoholic beverages and other highly regulated products, online payments, text messaging, subscriptions and membership products, intellectual property, data retention, data protection, data transfers and sharing, cybersecurity, privacy, age verification, AI and automated decision-making technology, consumer protection, consumer fees, antitrust, background checks, website and mobile application accessibility, environmental sustainability and related disclosures, and tax and other government-imposed fees. These and other laws are often complex, subject to change, and subject to varying interpretations, in many cases due to their lack of specificity. The scope and interpretation of these laws, and whether they are applicable to us, are often uncertain and may be conflicting, including varying standards and interpretations between U.S. law and the laws of other jurisdictions, between U.S.…

In addition, there is an increasingly active litigation and regulatory environment regarding antitrust and competition matters in the jurisdictions in which we operate. We could be subject to claims of violations of competition laws in many aspects of our business, including with respect to alleged market sharing, price fixing or other pricing practices, anticompetitive exclusionary conduct, exchange of competitively sensitive information, and with respect to any acquisitions we undertake. For example, in February 2025, Uber filed a lawsuit in California state court alleging that certain of our business practices are anticompetitive. In addition, competition authorities in some of the jurisdictions in which we operate have made queries regarding, or investigated, our pricing-related terms or other practices and, in certain jurisdictions, competition authorities and courts have issued decisions concerning our pricing-related terms or other practices. Any potential violations of competition laws could result in litigation, fines, restrictions on our operations, render applicable provisions or contracts unenforceable, divert management’s attention, and lead to claims for damages and reputational harm, each of which could adversely affect our business, financial condition, and results of operations.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm｜as_of：2026-02-18
<<<
Regulatory and administrative investigations, audits, demands, and inquiries We have in the past been, are currently, and may in the future be the subject of regulatory and administrative investigations, audits, demands, and inquiries conducted by federal, state, or local governmental agencies concerning our business practices, the classification and compensation of Dashers, DoorDash Dasher pay models and pay practices, compliance with consumer protection laws, privacy, cybersecurity, tax issues, unemployment insurance, workers’ compensation insurance, and other matters. For example, we are currently under audit by the Employment Development Department of the State of California (the "CA EDD") for payroll tax liabilities. In January 2023, the CA EDD issued a negative assessment in connection with such audit. We believe that we have meritorious defenses to the CA EDD’s assessment, and intend to vigorously appeal this assessment. However, the ultimate resolution of the audit is uncertain and, accordingly, we have recorded an accrual for this matter within accrued expenses and other current liabilities on the consolidated balance sheets as of December 31, 2025. We are currently the subject of government investigations, audits, demands, and inquiries in other jurisdictions as well, and we may in the future settle, or record accruals with respect to, such matters.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
