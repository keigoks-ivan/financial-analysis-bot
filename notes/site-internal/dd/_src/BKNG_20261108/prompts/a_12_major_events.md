你是 stock-analyst v20 DD 的證據採集子 agent。標的：BKNG。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - BKNG Booking Holdings acquisition merger 2025 2026
  - BKNG Booking Holdings class action lawsuit securities fraud
  - BKNG Booking Holdings clinical trial FDA approval 2025 2026
  - BKNG Booking Holdings product launch recall warning letter
  - BKNG Booking Holdings SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm｜as_of：2026-02-18
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm｜as_of：2026-02-18
<<<
A number of jurisdictions have initiated lawsuits or other proceedings against OTCs, including us, related to, among other things, the payment of certain travel transaction taxes that could include historical taxes that are claimed to be owed, interest, penalties, punitive damages, and/or attorney's fees and costs. Additional jurisdictions may assert that we are subject to travel transaction taxes and could seek to collect such taxes, either retroactively, prospectively, or both. We continue to defend against these lawsuits and, where appropriate, intend to continue to assert that we should not be subject to such taxes. Although we believe we do not owe the taxes claimed in these lawsuits, litigation is uncertain, and if there was an adverse outcome in 13 these lawsuits or similar litigation in other jurisdictions, it could result in liabilities for past and/or future bookings, and it could have an adverse effect on our business, reputation, profit margins, and results of operations. Jurisdictions could also seek to amend their tax statutes in order to collect travel transaction taxes from us on a prospective basis.

In the past, we have been a defendant in securities class action litigation. If our stock price declines or is volatile, it could increase the chances that we become the target of securities class action litigation, which could result in substantial costs and divert management's attention and resources, either of which could adversely affect our business, financial condition, and results of operations.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 7. MD&A（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm｜as_of：2026-02-18
<<<
The determination of whether a loss is probable and whether the amount of the loss can be reasonably estimated requires significant judgment and evaluation of all the underlying facts and circumstances including judgments about the potential actions of third-party claimants, regulatory authorities, and courts. Claims, assessments, and litigations involve significant uncertainties such as the complexity of the facts, the legal theories involved, the nature of the claims, the judgment of the courts, the applicable methodology for determining potential damages, and, in the case of class actions, whether a class action can be certified and members of the class choose to participate in the litigation.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm｜as_of：2026-02-18
<<<
Exhibit Number Description 3.1(a) Restated Certificate of Incorporation of the Company. 3.2(b) Certificate of Amendment of the Restated Certificate of Incorporation, dated as of June 4, 2021.

10.6(n)+ OpenTable, Inc. Amended and Restated 2009 Equity Incentive Award Plan. 10.7(o)+ Buuteeq, Inc. Amended and Restated 2010 Stock Plan.

In February 2026, the Company entered into favorable settlement agreements to resolve litigation matters in which it was a plaintiff, for which it expects to receive a benefit of approximately $90 million in the first quarter of 2026, upon completion of various conditions.
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001075531&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-11-03 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-08-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-02 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-11 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-07 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-02 8-K Items 5.03 Amendments to Articles or Bylaws；9.01 Financial Statements and Exhibits
2026-04-02 8-K Items 5.02 Departure/Election of Directors or Officers
2026-04-01 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-18 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-11，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1075531/000110465926058730/tm2614215d1_8k.htm｜as_of：2026-05-11
<<<
Item 1.01 Entry into a Material Definitive Agreement.
Senior Notes
On May 11, 2026, Booking Holdings Inc. (the “Company”)
executed three Officers’ Certificates (the “Officers’ Certificates”), in accordance with Sections 2.02
and 10.04 of the Indenture dated August 8, 2017 (the “Base Indenture” and, together with the Officers’ Certificates,
the “Indenture”) between the Company and U.S. Bank Trust Company, National Association (as successor in interest to
U.S. Bank National Association), as trustee (the “Trustee”) and registrar, in connection with the sale of €600,000,000
aggregate principal amount of the Company’s 3.500% Senior Notes due 2030 (the “2030 Notes”), €700,000,000
aggregate principal amount of the Company’s 4.000% Senior Notes due 2034 (the “2034 Notes”), and €600,000,000
aggregate principal amount of the Company’s 4.500% Senior Notes due 2039 (the “2039 Notes” and, together with
the 2030 Notes and the 2034 Notes, the “Senior Notes”). The 2030 Notes will mature on May 11, 2030, the 2034 Notes
will mature on May 11, 2034, and the 2039 Notes will mature on May 11, 2039, in each case unless earlier redeemed or repurchased. The
Senior Notes are the Company’s general senior unsecured obligations and rank equally with the Company’s other senior unsecured
obligations. Pursuant to an Agency Agreement dated as of May 11, 2026 (the “Agency Agreement”) relating to the Senior…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-07，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1075531/000110465926057239/tm2613920d1_8k.htm｜as_of：2026-05-07
<<<
Item 1.01 Entry into a Material Definitive Agreement.
Senior Notes
On May 7, 2026, Booking Holdings Inc. (the “Company”)
executed an Officers’ Certificate (the “Officers’ Certificate”), in accordance with Sections 2.02 and 10.04
of the Indenture dated August 8, 2017 (the “Base Indenture” and, together with the Officers’ Certificate, the
“Indenture”) between the Company and U.S. Bank Trust Company, National Association (as successor in interest to U.S.
Bank National Association), as trustee (the “Trustee”) and registrar, in connection with the sale of $750,000,000 aggregate
principal amount of the Company’s 5.375% Senior Notes due 2036 (the “Senior Notes”). The Senior Notes will mature
on May 7, 2036, unless earlier redeemed or repurchased. The Senior Notes are the Company’s general senior unsecured obligations
and rank equally with the Company’s other senior unsecured obligations.
The Company will pay interest on the Senior Notes
at a semi-annual rate of 5.375% payable on May 7 and November 7 of each year, beginning on November 7, 2026.
Prior to February 7, 2036, the date that is three
months prior to the maturity date of the Senior Notes (the “Par Call Date”), the Company may redeem some or all of
the Senior Notes at a redemption price equal to the greater of the following amounts plus, in each case, accrued and unpaid interest thereon,…
>>>

[8] 來源：SEC EDGAR｜文件：8-K（2026-02-18，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1075531/000107553126000008/bkng-20260218.htm｜as_of：2026-02-18
<<<
Item 8.01 Other Events.
On February 18, 2026, the Company announced a twenty-five-for-one forward stock split of the Company’s common stock. The stock split will be effected through the filing of an amendment to the Company’s Restated Certificate of Incorporation with the Delaware Secretary of State. The amendment will result in a proportionate increase in the number of shares of authorized common stock. As a result of the stock split, each record holder of common stock as of the close of market on Friday, March 6, 2026 will receive twenty four (24) additional shares of common stock, to be distributed after the close of market on Thursday, April 2, 2026. Trading is expected to commence on a split-adjusted basis at market open on Monday, April 6, 2026.
Item 9.01. Financial Statements and Exhibits.
(d) Exhibits
Exhibit
Number Description
99.1
Press release (which includes a financial and statistical supplement and related information) issued by Booking Holdings Inc. on February 18, 2026 relating to, among other things, its fourth quarter and year ended 2025 earnings.
104 Cover Page Interactive Data File - the cover page interactive data file does not appear in the Interactive Data File because its XBRL tags are embedded within the Inline XBRL document.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
