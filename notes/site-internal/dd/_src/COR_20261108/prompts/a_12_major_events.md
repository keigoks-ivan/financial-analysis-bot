你是 stock-analyst v20 DD 的證據採集子 agent。標的：COR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - COR Cencora acquisition merger 2025 2026
  - COR Cencora class action lawsuit securities fraud
  - COR Cencora clinical trial FDA approval 2025 2026
  - COR Cencora product launch recall warning letter
  - COR Cencora SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-25）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm｜as_of：2025-11-25
<<<
ITEM 3. LEGAL PROCEEDINGS
Legal proceedings in which we are involved are discussed in Note 12 (Legal Matters and Contingencies) and Note 13 (Antitrust Litigation Settlements) of the Notes to Consolidated Financial Statements appearing in this Annual Report on Form 10-K.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-25）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm｜as_of：2025-11-25
<<<
Ongoing unfavorable publicity regarding the abuse or misuse of prescription opioid pain medications and the role of wholesale distributors in the supply chain of such prescription medications, as well as the continued proliferation of opioid lawsuits, investigations, regulations and legislative actions, and unfavorable publicity in relation to those lawsuits, could continue to have a material adverse effect on our reputation or results of operations.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-25）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm｜as_of：2025-11-25
<<<
The MDL Court selected four cases filed by third-party payors to serve as additional litigation bellwethers. On May 31, 2024, the MDL Court severed and stayed these four cases against the Company and the two other national pharmaceutical distributors, pursuant to ongoing settlement discussions to resolve litigation filed by a putative class of third-party payors. On August 29, 2024, the Company and two other national pharmaceutical distributors entered into a proposed class action settlement agreement to resolve the opioid-related claims of a proposed settlement class of third-party payors. Pursuant to the agreement, the Company recorded a $93.0 million litigation expense accrual in Litigation and Opioid-Related Expenses (Credit), Net in its fiscal 2024 Consolidated Statement of Operations. The MDL Court granted a motion for preliminary approval of the proposed class action settlement on September 3, 2024. Following a time period for submission of any objections or requests to be excluded from the settlement, the MDL granted final approval of the settlement during a fairness hearing held on January 13, 2025 and entered a final approval order on January 15, 2025. On February 13, 2025, the sole objector to the settlement filed a notice of appeal of the final approval order. A settlement agreement with the sole objector was entered into on June 12, 2025.…

On September 26, 2024, the Company and two other national pharmaceutical distributors entered into a proposed class action settlement agreement to resolve the opioid-related claims of a proposed settlement class of hospitals. The Company recorded a $120.9 million litigation expense accrual in Litigation and Opioid-Related Expenses (Credit), Net in its fiscal 2024 77 Table of Contents Consolidated Statement of Operations, representing the Company’s expected share of the potential class action settlement. On October 30, 2024, the United States District Court for the District of New Mexico granted a motion for preliminary approval of the proposed class action settlement. Following notice to class members, a time period for submission of any objections to the settlement or requests to be excluded from the settlement, and a fairness hearing on March 4, 2025, the Court granted final approval of the settlement and entered a final approval order. The settlement became effective on April 4, 2025.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001140859&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 22 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 7 份。
2026-11-04 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-11-04 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-10-21 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-25 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-14 8-K Items 5.02 Departure/Election of Directors or Officers
2026-08-12 8-K Items 7.01 Regulation FD Disclosure
2026-08-05 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-15 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-29 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-06 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-23 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-17 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-06 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-02-18 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-13 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-11 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-10 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-04 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-22 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-16 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2025-12-15 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-08-05，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1140859/000110465926090691/tm2621845d1_8k.htm｜as_of：2026-08-05
<<<
Item 1.01. Entry into
a Material Definitive Agreement.
Amendment
and Restatement of Multi-Currency Revolving Credit Facility
On
July 31, 2026, Cencora, Inc. (the “Company”) and its subsidiary Innomar Strategies Inc. entered into an Amended and Restated
Credit Agreement (the “Amended and Restated Credit Agreement”) to further amend and restate the Amended and Restated Credit
Agreement, dated as of June 4, 2025 and as amended on January 12, 2026, among the Company, the borrowing subsidiaries party thereto, the
lenders party thereto and JPMorgan Chase Bank, N.A., as administrative agent, pursuant to which the Company and such subsidiaries previously
obtained a multi-currency senior unsecured revolving credit facility (the “Multi-Currency Revolving Credit Facility”).
The
Amended and Restated Credit Agreement amends and restates the Multi-Currency Revolving Credit Facility to, among other things, (i) increase
the aggregate amount of the commitments thereunder from $5.5 billion to $7.0 billion, (ii) extend the maturity date to July 2031, and
(iii) make certain changes to the covenants, representations and warranties and other provisions contained therein.
Interest
on borrowings under the Multi-Currency Revolving Credit Facility accrue at specified rates based on the Company’s public debt ratings
by Standard & Poor’s Ratings Services, Moody’s Investors Service, Inc. and Fitch, Inc., and pursuant to…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-02-13，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1140859/000110465926015272/tm265391d5_8k.htm｜as_of：2026-02-13
<<<
Item 1.01. Entry into a Material Definitive
Agreement.
On February 13, 2026, Cencora,
Inc. (the “Company”) completed the sale of $3.0 billion aggregate principal amount of the Company’s Senior Notes as
follows: $500,000,000 aggregate principal amount of the Company’s 3.950% Senior Notes due 2029 (the “2029 Notes”),
$500,000,000 aggregate principal amount of the Company’s 4.250% Senior Notes due 2030 (the “2030 Notes”), $500,000,000
aggregate principal amount of the Company’s 4.600% Senior Notes due 2033 (the “2033 Notes”), $1,000,000,000 aggregate
principal amount of the Company’s 4.900% Senior Notes due 2036 (the “2036 Notes”) and $500,000,000 aggregate principal
amount of the Company’s 5.650% Senior Notes due 2056 (the “2056 Notes” and, together with the 2029 Notes, the 2030
Notes, the 2033 Notes and the 2036 Notes, the “Notes”).
The 2029 Notes were issued
under and are governed by an Indenture, dated as of November 19, 2009 (the “Base Indenture”), by and between the Company
and U.S. Bank Trust Company, National Association (as successor in interest to U.S. Bank National Association), as trustee (the “Trustee”),
as supplemented and amended by an Eighteenth Supplemental Indenture, dated as of February 13, 2026, by and between the Company and the
Trustee (the “Eighteenth Supplemental Indenture” and, together with the Base Indenture, the “2029 Note Indenture”).…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-01-16，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1140859/000110465926004524/tm263332d1_8k.htm｜as_of：2026-01-16
<<<
Item 1.01. Entry into a Material Definitive Agreement.
Amendment to Revolving
Credit Facility
On January 12, 2026, Cencora, Inc.
(the “Company”) entered into an Incremental Facility and Amendment Agreement (the “Amendment”) to that certain
Amended and Restated Credit Agreement (as amended by the Amendment, the “Revolving Credit Agreement”), dated as of June 4,
2025, among the Company, the borrowing subsidiaries party thereto, the lenders party thereto and JPMorgan Chase Bank, N.A., as administrative
agent.
The Amendment increased the
aggregate amount of the commitments under the Revolving Credit Agreement by $1.0 billion to $5.5 billion.
The foregoing description
of the Amendment does not purport to be complete and is qualified in its entirety by reference to the Amendment, which is filed as Exhibit 10.1
to this Current Report on Form 8-K and is incorporated by reference herein.
Multi-Year Term Loan
Facility
On January 12, 2026, the Company
entered into a Term Credit Agreement (the “Term Credit Agreement”), among the Company, the lenders party thereto and JPMorgan
Chase Bank, N.A., as administrative agent, in connection with the previously announced proposed acquisition (the “Acquisition”)
of the majority of the outstanding equity interests that the Company does not currently own in OneOncology. The Term Credit Agreement…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
