你是 stock-analyst v20 DD 的證據採集子 agent。標的：EHC。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - EHC Encompass Health acquisition merger 2025 2026
  - EHC Encompass Health class action lawsuit securities fraud
  - EHC Encompass Health clinical trial FDA approval 2025 2026
  - EHC Encompass Health product launch recall warning letter
  - EHC Encompass Health SEC investigation restatement


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
- 頂層 `events` 五組同樣可引用本摘錄（例如併購、訴訟類查無事件，可引用同一句統計）。

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm｜as_of：2026-02-26
<<<
Item 3.Legal Proceedings
We provide services in the highly regulated healthcare industry. Furthermore, operating inpatient rehabilitation hospitals requires significant staffing and involves intensive therapy for individuals suffering from significant physical or cognitive disabilities or injuries. In the ordinary course of our business, we are subject to regulatory and other governmental audits and investigations and are party to various legal actions, proceedings, and claims, including wage and hour, employment and personal injury claims, some of which seek to be certified as class or collective actions. These matters could potentially subject us to sanctions, damages, recoupments, fines, and other penalties. Some of these matters have been material to us in the past, and others in the future may, either individually or in the aggregate, be material and adverse to our business, financial position, results of operations, and liquidity.
Additionally, the False Claims Act (the “FCA”) allows private citizens, called “relators,” to institute civil proceedings on behalf of the United States alleging violations of the FCA. These lawsuits, also known as “qui tam” actions, are common in the healthcare industry and can involve significant monetary damages, fines, attorneys’ fees and the award of bounties to the relators who successfully prosecute or bring these suits to the government. It is possible that qui tam lawsuits have been filed against us, which suits remain under seal, or that we are unaware of such filings or precluded by existing law or court order from discussing or disclosing the filing of such suits. Therefore, from time to time, we may be party to one or more undisclosed qui tam cases brought pursuant to the FCA.
Information relating to certain legal proceedings in which we are involved is included in Note 16, Contingencies and Other Commitments, to the accompanying consolidated financial statements.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm｜as_of：2026-02-26
<<<
On March 4, 2013, we received document subpoenas from an office of the HHS-OIG addressed to four of our hospitals. On April 24, 2014, we received document subpoenas relating to an additional seven of our hospitals. Those subpoenas requested documents, including copies of patient medical records, related to reimbursement claims submitted during periods ranging from January 2008 through December 2013. The associated investigation led by DOJ was based on whistleblower claims of alleged improper or fraudulent claims submitted to Medicare and Medicaid and requested documents and materials relating to practices, procedures, protocols and policies of certain pre- and post-admissions activities at these hospitals including marketing functions, pre-admission screening, post-admission physician evaluations, patient assessment instruments, individualized patient plans of care, and compliance with the Medicare 60% rule. We settled the DOJ investigation, together with the related qui tam or whistleblower lawsuits, in 2019 for a total payment of $48 million, and we expressly denied any wrongdoing. In return for the settlement payment, the plaintiffs dismissed with prejudice their pending qui tam claims, and DOJ provided Encompass Health and all its subsidiaries with a release from civil liability.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm｜as_of：2026-02-26
<<<
The False Claims Act allows private citizens, called “relators,” to institute civil proceedings on behalf of the United States alleging violations of the False Claims Act. These lawsuits, also known as “whistleblower” or “qui tam” actions, can involve significant monetary damages, fines, attorneys’ fees and the award of bounties to the relators who successfully prosecute or bring these suits to the government. Qui tam cases are sealed at the time of filing, which means knowledge of the information contained in the complaint typically is limited to the relator, the federal government, and the presiding court. The defendant in a qui tam action may remain unaware of the existence of a sealed complaint for years. While the complaint is under seal, the government reviews the merits of the case and may conduct a broad investigation and seek discovery from the defendant and other parties before deciding whether to intervene in the case and take the lead on litigating the claims. The court lifts the seal when the government makes its decision on whether to intervene. If the government decides not to intervene, the relator may elect to continue to pursue the lawsuit individually on behalf of the government.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000785161&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。
2026-10-28 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-13 8-K Items 8.01 Other Events
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-01 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-05-15 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-11 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-04-30 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-10 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-02-20 8-K/A Items 5.02 Departure/Election of Directors or Officers
2026-02-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-02 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2025-12-01 8-K Items 7.01 Regulation FD Disclosure
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-06-01，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000161/ehc-20260529.htm｜as_of：2026-06-01
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On May 29, 2026, Encompass Health Corporation (the “Company”) completed the issuance and sale of $500 million in aggregate principal amount of its 5.875% Senior Notes due 2034 (the “Notes”), along with the related guarantees of the Notes by certain of the Company’s subsidiaries (the “Guarantees”), in a private offering. The Notes were issued at par for net proceeds of approximately $491.2 million after deducting the initial purchasers’ discount and estimated offering expenses. The Company intends to use the net proceeds from the sale of the Notes, together with available cash on hand, to redeem at par $400 million of the $800 million in principal amount outstanding of the Company’s 4.500% senior notes due 2028, to repay $100 million of outstanding amounts under the Company’s revolving credit facility, and to pay certain related fees and expenses. The Notes were sold to the initial purchasers in a transaction exempt from the registration requirements of the Securities Act of 1933, as amended (the “Securities Act”), and will be resold by the initial purchasers to qualified institutional buyers in reliance on Rule 144A under the Securities Act and to non-U.S. persons in transactions outside the United States in reliance on Regulation S under the Securities Act.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-15，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000156/ehc-20260514.htm｜as_of：2026-05-15
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On May 14, 2026, Encompass Health Corporation (the “Company”) and certain of its subsidiaries, as guarantors (the “Guarantors”), entered into a purchase agreement (the “Purchase Agreement”) with Wells Fargo Securities, LLC, as the representative of the initial purchasers (the “Initial Purchasers”), with respect to a private offering (the “Notes Offering”) by the Company of $500,000,000 in aggregate principal amount of 5.875% senior notes due 2034 (the “Notes”), along with the related guarantees of the Notes. The Notes Offering is expected to close on or about May 29, 2026, subject to and in accordance with the terms of the Purchase Agreement.
The Purchase Agreement contains customary representations, warranties and covenants of the Company and the Guarantors, conditions to closing, indemnification obligations of the parties, and termination and other customary provisions. The foregoing description of the Purchase Agreement is not intended to be complete and is qualified in its entirety by reference to the full text of the Purchase Agreement, a copy of which is attached hereto as Exhibit 10.1 and is incorporated herein by reference.
The Notes are being offered and sold in a transaction exempt from the registration requirements under the Securities Act of 1933, as amended (the “Securities Act”).…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-03-10，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000100/ehc-20260309.htm｜as_of：2026-03-10
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On March 9, 2026 (the “Closing Date”), Encompass Health Corporation (the “Company”) entered into the Credit Agreement (the “2026 Credit Agreement”), by and among the Company, certain of its subsidiaries, as guarantors, Truist Bank, as administrative agent and collateral agent, and various other lenders. In connection with the execution of the 2026 Credit Agreement, the Company paid off all outstanding amounts, and terminated the commitments, as of the Closing Date, under the Sixth Amended and Restated Credit Agreement, dated October 7, 2022 (the “2022 Credit Agreement”), by and among the Company, certain of its subsidiaries, as guarantors, Barclays Bank PLC, as administrative agent and collateral agent (“Barclays”), and various other lenders.…
>>>

## major_events 軸另交頂層 events 五組（QC-19）
`validate_evidence.py` 的 strict 檢查讀的是 evidence.json **頂層** `events` 物件，
不是 `coverage.major_events`——這兩個是分開的鍵，只填前者會漏掉後者。

你除了（a）對 `major_events` 這一軸本身作答（寫進 `coverage.major_events`），
**還要**（b）把同一批查證結果拆成下列五組，寫進回傳 JSON 的**頂層** `events` 鍵：
`ma_merger`（併購）／`lawsuit_class_action`（訴訟／集體訴訟）／`clinical_fda`
（臨床／FDA，非藥品器材業務可用 not_applicable）／`product_recall_warning`
（產品召回／警告）／`sec_investigation_restatement`（SEC 調查／重編財報）。

每組欄位規則與 `coverage.<axis>` 相同：found 需 ≥1 條帶 source／as_of／
direction／affects 的 finding；none 需 ≥2 條 queries_run；不適用（如非藥品業務
的 `clinical_fda`）用 `status:"none"`＋queries_run 說明「非藥品/器材業務，已查
證無相關監管動作」，**不得省略該組鍵**。

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
  },
  "events": {
    "ma_merger": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "lawsuit_class_action": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "clinical_fda": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "product_recall_warning": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "sec_investigation_restatement": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""}
  }
}
```

`clues` 選填、每軸一個陣列，沒有就整個欄位省略。只在你**找到有網址的線索、但沒讀到頁面而拿不到可逐字複製的原文**時放；程式會打開該網址，在全文裡找 `match_terms` 同時出現的一段原文，找到就升級成帶原文的 finding；找不到（或頁面打不開）就照 `excerpt_from: "snippet"`、`excerpt: null` 的 finding 保留，並標為未核原文。
- 只有 clues、findings 是空的時，`status` 填 `none`（程式核實到原文後會自動改成 `found`）。
- `url` 必須是你在搜尋結果裡實際看到的網址；不得編造、不得猜網址、不得填網站首頁。沒有網址的線索不要放（寫進 note）。已經寫在 findings 的網址不要重複放。
- `match_terms` 放 2～5 個預期原文會逐字出現的字串：金額、比例、專有名詞、引號裡的關鍵詞。照原文可能的寫法填，不要改寫或翻譯；不要放公司名、代號、年份或「營收」「公司」這類到處都有的詞。
- 其餘欄位（`claim`、`source`、`as_of`、`direction`、`affects`）規則同 findings；`as_of` 填你推估的文章發布日，程式讀到頁面發布日會以頁面為準。

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
