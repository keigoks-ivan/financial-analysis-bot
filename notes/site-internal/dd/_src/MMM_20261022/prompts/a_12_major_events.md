你是 stock-analyst v20 DD 的證據採集子 agent。標的：MMM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - MMM 3M acquisition merger 2025 2026
  - MMM 3M class action lawsuit securities fraud
  - MMM 3M clinical trial FDA approval 2025 2026
  - MMM 3M product launch recall warning letter
  - MMM 3M SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm｜as_of：2026-02-03
<<<
Item 3. Legal Proceedings
Discussion of legal matters is incorporated by reference from Part II, Item 8, Note 17, “Commitments and Contingencies,” of this document, and should be considered an integral part of Part I, Item 3, “Legal Proceedings.”
Table of Contents
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm｜as_of：2026-02-03
<<<
Process for Disclosure and Recording of Liabilities Related to Legal Proceedings: Many lawsuits and claims involve highly complex issues relating to causation, scientific evidence, and alleged actual damages, all of which are subject to substantial uncertainties. Assessments of lawsuits and claims can involve a series of complex judgments about future events and can rely heavily on estimates and assumptions. The categories of legal proceedings in which the Company is involved may include multiple lawsuits and claims, may be spread across multiple jurisdictions and courts which may handle the lawsuits and claims differently, may involve numerous and different types of plaintiffs, raising claims and legal theories based on specific allegations that may not apply to other matters, and may seek substantial compensatory and, in some cases, punitive, damages. These and other factors contribute to the complexity of these lawsuits and claims and make it difficult for the Company to predict outcomes and make reasonable estimates of any resulting losses. The Company's ability to predict outcomes and make reasonable estimates of potential losses is further influenced by the fact that a resolution of one or more matters within a category of legal proceedings may impact the resolution of other matters in that category in terms of timing, amount of liability, or both.

Claims in the MDL are asserted by individuals, public water systems, putative class members, state and territorial sovereigns, and other entities. Plaintiffs seek a variety of forms of relief in cases in the MDL, including, where applicable, damages for personal injury, property damage, water treatment costs, medical monitoring, natural resource damages, and punitive damages. 3M also continues to defend certain AFFF cases that remain in state court and is in discussions with pre-suit claimants for possible resolutions where appropriate. In general, preliminary judicial proceedings evaluate whether these lawsuits should proceed in the AFFF MDL or outside of the AFFF MDL, with some cases being moved to the AFFF MDL or remanded to another venue, such as state court.

Another case currently pending in federal court in Georgia was brought by individuals asserting PFAS contamination by 3M and other defendants, seeks economic damages and injunctive relief on behalf of a putative class of Rome and Floyd County water subscribers. Class certification has been fully briefed, and the plaintiff's injunctive relief claims were recently dismissed. Plaintiff's claims for economic damages related to alleged increases in their water rates due to the presence of PFAS remain pending. Discovery was reopened in a limited fashion due to plaintiffs’ request to investigate whether recent increases in water utility rates by the City of Rome was attributable to PFAS. Defendants filed a consolidated motion for summary judgment in December 2025. No trial date has been set.
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000066740&type=8-K｜as_of：2026-10-22
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-20 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-19 8-K Items 7.01 Regulation FD Disclosure
2026-09-10 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-19 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation
2026-07-21 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-08 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-05-13 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-06 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation
2026-04-21 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-05 8-K Items 5.02 Departure/Election of Directors or Officers
2026-01-20 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-08-19，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/66740/000006674026000268/mmm-20260817.htm｜as_of：2026-08-19
<<<
Item 1.01. Entry Into a Material Definitive Agreement
On August 17, 2026 (the “Effective Date”), 3M Company (the “Company”) entered into a new credit agreement (the “Credit Agreement”) with JPMorgan Chase Bank, N.A., as administrative agent; certain subsidiaries of the Company from time to time party thereto, as subsidiary borrowers (together with the Company, the “Borrowers”); and certain financial institutions as lenders. Pursuant to the terms of the Credit Agreement, the lenders thereunder have agreed to provide the Borrowers with a $4.25 billion revolving credit facility on an unsecured basis (the “Facility”) which is available for borrowing until the maturity date or the earlier termination of the Facility in accordance with the terms of the Credit Agreement. Any advances under the Facility will mature and be payable on the fifth anniversary of the Effective Date. The Credit Agreement replaced the $4.25 billion five-year revolving credit agreement dated as of May 11, 2023 (as amended by Amendment No. 1, dated as of July 7, 2023 and Amendment No. 2, dated as of September 18, 2023, the “Former Revolving Credit Agreement”), among the Company, the lenders named therein and JPMorgan Chase Bank, N.A. as administrative agent. The Former Revolving Credit Agreement and the commitments thereunder were terminated on the Effective Date.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-05-06，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/66740/000006674026000188/mmm-20260430.htm｜as_of：2026-05-06
<<<
Item 1.01. Entry Into a Material Definitive Agreement
On April 30, 2026 (the “Effective Date”), 3M Company (the “Company”) and its indirect subsidiary Fire Safety Platform Holdco, Inc. (the “Borrower”) entered into a credit agreement (the “Credit Agreement”) with Morgan Stanley Senior Funding, Inc. as administrative agent, sole lead arranger and sole bookrunner, Citibank, N.A. and U.S. Bank National Association as co-syndication agents, and certain financial institutions as lenders. Pursuant to the terms of the Credit Agreement, the lenders have agreed to provide the Borrower with a $1.43 billion term loan facility (the “Facility”), which is available for borrowing on the Closing Date (as defined in the Credit Agreement) (unless the commitments thereunder are terminated prior to such date in accordance with the Credit Agreement), and a $200 million revolving credit facility (the “RCF” and together with the Facility, the “Facilities”), which is available for borrowing on a revolving basis from the Closing Date until the maturity date applicable to the RCF. The loans under the Facility and the RCF each mature on the date falling 364 days after the Closing Date, subject, in each case, to an extension of up to 12 months at the Borrower’s request, subject to the satisfaction of certain conditions (including the payment of an extension fee).…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-09-10，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/66740/000110465926106710/tm2624999d1_8k.htm｜as_of：2026-09-10
<<<
Item 8.01. Other Events
On September 3, 2026, 3M Company (the “Company”) entered
into an Underwriting Agreement with Deutsche Bank AG, London Branch, Merrill Lynch International, Citigroup Global Markets Limited and
J.P. Morgan Securities plc, as representatives of the several underwriters named therein (the “Underwriting Agreement”), relating
to the sale of €500,000,000 aggregate principal amount of the Company’s 3.500% Notes due 2028, €500,000,000 aggregate
principal amount of the Company’s 3.900% Notes due 2031 and €500,000,000 aggregate principal amount of the Company’s
4.100% Notes due 2034 (collectively, the “Notes”). The closing of the offering of Notes occurred on September 10, 2026.
The Notes were offered pursuant to the Company’s Registration
Statement on Form S-3 (file no. 333-293169), filed with the Securities and Exchange Commission (the “SEC”) on February 3,
2026, including the prospectus contained therein, a related preliminary prospectus supplement dated September 3, 2026 and a final
prospectus supplement dated September 3, 2026 (collectively, the “Registration Statement”). The Notes were issued pursuant
to an indenture dated as of November 17, 2000 (the “Base Indenture”), as supplemented by the First Supplemental Indenture
dated as of July 29, 2011 (the “First Supplemental Indenture”) and the Second Supplemental Indenture dated February 3,
2026 (the “Second Supplemental Indenture”, and together with the First Supplemental Indenture and the Base Indenture, the…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MMM_20261022/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
