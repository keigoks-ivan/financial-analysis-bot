你是 stock-analyst v20 DD 的證據採集子 agent。標的：NVT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - NVT nVent Electric acquisition merger 2025 2026
  - NVT nVent Electric class action lawsuit securities fraud
  - NVT nVent Electric clinical trial FDA approval 2025 2026
  - NVT nVent Electric product launch recall warning letter
  - NVT nVent Electric SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm｜as_of：2026-02-17
<<<
ITEM 3. LEGAL PROCEEDINGS
We have been made parties to a number of actions filed or have been given notice of potential claims relating to the conduct of our business, including those pertaining to commercial disputes, product liability, asbestos, environmental, safety and health, patent infringement and employment matters.
While we believe that a material impact on our financial position, results of operations or cash flows from any such future claims or potential claims is unlikely, given the inherent uncertainty of litigation, a remote possibility exists that a future adverse ruling or unfavorable development could result in future charges that could have a material adverse impact. We do and will continue to periodically reexamine our estimates of probable liabilities and any associated expenses and receivables and make appropriate adjustments to such estimates based on experience and developments in litigation. As a result, the current estimates of the potential impact on our financial position, results of operations and cash flows for the proceedings and claims described in the notes to our consolidated financial statements could change in the future.
Environmental matters
We have been named as defendant, target or a potentially responsible party ("PRP") in a number of environmental clean-ups relating to our current or former businesses. We may be named as a PRP at other sites in the future for existing businesses, as well as both divested and acquired businesses. In addition to clean-up actions brought by governmental authorities, private parties could bring personal injury or other claims due to the presence of, or exposure to, hazardous substances.
Certain environmental laws impose liability on current or previous owners or operators of real property for the cost of removal or remediation of hazardous substances at their properties or at properties at which they have disposed of hazardous substances. Our accruals for environmental matters are recorded on a site-by-site basis when it is probable that a liability has been incurred and the amount of the liability can be reasonably estimated, based on current law and existing technologies.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 3. Legal Proceedings（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm｜as_of：2026-02-17
<<<
Product liability claims We are subject to various product liability lawsuits and personal injury claims. A substantial number of these lawsuits and claims are insured and accrued for by Tonka Bay, a captive insurance subsidiary of nVent. Tonka Bay records a liability for these claims based on actuarial projections of ultimate losses. For all other claims, accruals covering the claims are recorded, on an undiscounted basis, when it is probable that a liability has been incurred and the amount of the liability can be reasonably estimated based on existing information. The accruals are adjusted periodically as additional information becomes available. We have not experienced significant unfavorable trends in either the severity or frequency of product liability lawsuits or personal injury claims.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 7. MD&A（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm｜as_of：2026-02-17
<<<
In June 2025, nVent and its subsidiaries nVent Finance and Hoffman Schroff Holdings, Inc. entered into an amended and restated credit agreement (the "Credit Agreement") with a syndicate of banks providing for a five-year $275.0 million senior unsecured term loan facility (the "2025 Term Loan Facility") and a five-year $600.0 million senior unsecured revolving credit facility (the "Revolving Credit Facility" and, together with the 2025 Term Loan Facility, the "Senior Credit Facilities"). The Credit Agreement amended and restated in its entirety the 2021 Credit Agreement. Borrowings under the Revolving Credit Facility are permitted from time to time during the full five-year term of the Revolving Credit Facility. nVent Finance has the option to request to increase the Revolving Credit Facility in an aggregate amount of up to $300.0 million, subject to customary conditions, including the commitment of the participating lenders.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm｜as_of：2026-02-17
<<<
In 2023, a cash flow hedge instrument and a net investment hedge instrument each reached maturity, resulting in settlement amounts reflected as a component of financing and investing cash inflows in the amount of $4.5 million and $3.1 million, respectively. Upon maturity of the previous agreement, we entered into a new net investment hedge with a gross notional U.S. dollar equivalent amount of $66.1 million. This net investment hedge was then settled early in the fourth quarter of 2023, resulting in a $1.7 million settlement, which is reflected as a component of investing cash inflows. Subsequent to the termination, we entered into a new net investment hedge with an initial gross notional U.S. dollar equivalent amount of $126.5 million.
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001720635&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。
2026-10-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-09-29 8-K Items 2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-17 8-K Items 2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-09-16 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-15 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-18 8-K Items 5.02 Departure/Election of Directors or Officers
2026-07-31 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-17 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-05-18 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-01 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-17 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-02-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-02-17，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1720635/000110465926015527/tm266212d3_8k.htm｜as_of：2026-02-17
<<<
ITEM 1.01 Entry into a Material Definitive Agreement
On February 16, 2026, nVent Electric plc (the “Company”)
and its subsidiaries nVent Finance S.à r.l. (“nVent Finance”) and Hoffman Schroff Holdings, Inc. (“Hoffman”)
entered into Amendment No. 1 (the “Amendment”) to that Second Amended and Restated Credit Agreement, dated as of June 30,
2025, among the Company, nVent Finance, Hoffman and a syndicate of banks (as amended by the Amendment, the “Credit Agreement”).
nVent Finance has historically been the primary borrower under the Credit Agreement, Hoffman has been a limited affiliate borrower under
the Credit Agreement and the Company has guaranteed the obligations of nVent Finance under the Credit Agreement, which provides for the
extension of revolving credit, term credit and other forms of financing arrangements in an aggregate principal amount of up to $875 million.
The Amendment permits Hoffman to be a primary borrower under the Credit Agreement in addition to nVent Finance and provides that nVent
Finance and Hoffman will cross-guarantee the obligations of each other under the Credit Agreement in addition to the Company guaranteeing
the obligations of nVent Finance and Hoffman under the Credit Agreement.
In addition, on February 16, 2026, the Company, nVent Finance
and Hoffman entered into a Sixth Supplemental Indenture (the “Supplemental Indenture”) to the Indenture, dated as of March 26,…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-09-29，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1720635/000110465926111938/tm2626249d1_8k.htm｜as_of：2026-09-29
<<<
ITEM 8.01 Other Events
The Notes and the Guarantees are registered under
the Securities Act of 1933, as amended, pursuant to a Registration Statement on Form S-3 (Registration No. 333-293530, 333-293530-01
and 333-293530-02) that the Company, Hoffman Schroff and nVent Finance filed with the Securities and Exchange Commission on February 17,
2026. The Company is also filing certain exhibits as part of this Current Report on Form 8-K for purposes of such Registration Statement.
See “Item 9.01. Financial Statements and Exhibits.”
ITEM 9.01 Financial Statements and Exhibits
(d)           Exhibits.
The exhibits listed in the Exhibit Index below are filed as part of this report.
Exhibit Index
Exhibit
Description
4.1
Indenture, dated as of September 29, 2026, among nVent Electric plc, Hoffman Schroff Holdings, Inc., nVent Finance S.à r.l. and U.S. Bank Trust Company, National Association.
4.2
First Supplemental Indenture, dated as of September 29, 2026, among nVent Electric plc, Hoffman Schroff Holdings, Inc., nVent Finance S.à r.l. and U.S. Bank Trust Company, National Association.
5.1
Opinion of Foley & Lardner LLP with respect to the Notes and the Guarantees.
5.2
Opinion
of Allen Overy Shearman Sterling SCS, société en commandite simple (inscrite au barreau de Luxembourg), with
respect to the Guarantee issued by nVent Finance S.à r.l.
5.3…
>>>

[8] 來源：SEC EDGAR｜文件：8-K（2026-09-16，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1720635/000110465926108250/tm2625115d7_8k.htm｜as_of：2026-09-16
<<<
ITEM 8.01 Other Events
On September 15, 2026, nVent Electric plc (the “Company”),
Hoffman Schroff Holdings, Inc. (“Hoffman Schroff”) and nVent Finance S.à r.l. (“nVent Finance”) entered
into an Underwriting Agreement (the “Underwriting Agreement”) with BofA Securities, Inc., Citigroup Global Markets Inc. and
J.P. Morgan Securities LLC, as representatives of the several underwriters listed therein (the “Underwriters”), pursuant to
which Hoffman Schroff agreed to sell, and the Underwriters agreed to purchase, subject to the terms and conditions set forth therein,
$800.0 million aggregate principal amount of Hoffman Schroff’s 6.150% Senior Notes due 2036 (the “Notes”), in a public
offering (the “Offering”). The Notes will be fully and unconditionally and jointly and severally guaranteed as to payment
of principal and interest by the Company and nVent Finance. The Offering is expected to close on September 29, 2026, subject to customary
closing conditions.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
