你是 stock-analyst v20 DD 的證據採集子 agent。標的：HWM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - HWM Howmet Aerospace acquisition merger 2025 2026
  - HWM Howmet Aerospace class action lawsuit securities fraud
  - HWM Howmet Aerospace clinical trial FDA approval 2025 2026
  - HWM Howmet Aerospace product launch recall warning letter
  - HWM Howmet Aerospace SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm｜as_of：2026-02-12
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm｜as_of：2026-02-12
<<<
The manufacture and sale of our products expose Howmet to potential product liability, personal injury, property damage, and related claims. In the event that a Howmet product fails to perform as expected, regardless of fault, or is used in an unexpected manner, and such failure or use results in, or is alleged to result in, bodily injury and/or property damage or other losses, Howmet may be subject to product liability lawsuits and other claims, or may participate in a recall or other corrective action involving such product. In addition, if a Howmet product is perceived to be defective or unsafe, Howmet’s sales could decrease, its reputation could be adversely impacted and Howmet could be exposed to government investigations or regulatory enforcement actions. Howmet is also subject to a variety of global legal and regulatory compliance risks in connection with its business and products. These risks include, among other things, potential claims, class action lawsuits or compliance issues, including those relating to securities laws, employment laws, intellectual property rights, cyber, security and privacy, insurance, commercial matters, antitrust and competition, human rights, third-party relationships, governance and sustainability (including climate-related/sustainability and other) rules and regulations, supply chain operations, and the manufacture and sale of products.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm｜as_of：2026-02-12
<<<
81 Table of Contents Legal Proceedings. Indemnified Matters. The Separation and Distribution Agreement, dated October 31, 2016, that the Company entered into with Alcoa Corporation in connection with its separation from Alcoa Corporation, and the Separation and Distribution Agreement, dated March 31, 2020, that the Company entered into with Arconic Corporation in connection with its separation from Arconic Corporation, provide for cross-indemnities for claims subject to indemnification between the Company and Alcoa Corporation and between the Company and Arconic Corporation, respectively. To date, Alcoa Corporation and Arconic Corporation have fulfilled their respective indemnification obligations to the Company, and claims subject to indemnification by Alcoa Corporation or Arconic Corporation have not impacted the Company financially. Among other claims that are covered by these indemnities, Arconic Corporation indemnifies the Company (previously named Arconic Inc. and, prior to that, Alcoa Inc.) for all potential liabilities associated with the fire that occurred at the Grenfell Tower in London, U.K. on June 14, 2017 (“Grenfell Fire”), including the following: (i) Regulatory Investigations. Arconic Architectural Products SAS (“AAP SAS”) (now a subsidiary of Arconic Corporation) supplied Reynobond PE to its customer who used the product as one component of the overall cladding system on Grenfell Tower.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000004281&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 17 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 10 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-08-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-28 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-26 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-07 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-06 8-K Items 7.01 Regulation FD Disclosure
2026-04-06 8-K Items 2.01 Completion of Acquisition or Disposition of Assets
2026-03-10 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-03 8-K Items 2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-17 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-17 8-K Items 8.01 Other Events
2026-02-12 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-12-22 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-17 8-K Items 8.01 Other Events
2025-11-12 8-K Items 2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-03 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-03 8-K Items 8.01 Other Events
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-04-06，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/4281/000110465926039791/tm2611168d1_8k.htm｜as_of：2026-04-06
<<<
Item 2.01 Completion of Acquisition or Disposition of Assets
On April 6, 2026, Howmet Aerospace Inc., a Delaware
corporation (“Howmet Aerospace”), completed its previously announced purchase of Consolidated
Aerospace Manufacturing, LLC (“Consolidated Aerospace Manufacturing”), a wholly owned subsidiary of Stanley Black & Decker,
Inc., a Connecticut corporation (“Stanley Black & Decker”), for a cash purchase price of approximately $1.8 billion, subject
to customary adjustments. Howmet Aerospace acquired Consolidated Aerospace Manufacturing pursuant to a Purchase Agreement between Howmet
Aerospace and Stanley Black & Decker.
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-28，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/4281/000110465926067497/hwm-20260528.htm｜as_of：2026-05-28
<<<
Item 8.01. Other Events
Segment Reorganization
Howmet Aerospace Inc. (the “Company” or "Howmet Aerospace") is filing this Current Report on Form 8-K to recast historical segment information as set forth in the Company's Annual Report on Form 10-K for the year ended December 31, 2025, as filed with the Securities and Exchange Commission (“SEC”) on February 12, 2026 (“Original Report”).
As previously disclosed and as reflected in the Company’s Quarterly Report on Form 10-Q for the quarterly period ended March 31, 2026, in the first quarter of 2026, the Company’s Chief Operating Decision Maker reorganized Howmet’s segments by moving a titanium alloy location from Engine Products to Engineered Structures as it better aligns with the operations of the Engineered Structures segment. The recasting had no impact on the Company’s consolidated results, financial position or cash flows. The titanium alloy location is one of the Company’s facilities at Whitehall, Michigan.
Exhibit 99.1 to this Form 8-K provides recast segment information within the following items of the Company's Original Report to reflect the movement of the titanium alloy location from Engine Products to Engineered Structures:
•Part II Item 7.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-03-03，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/4281/000110465926022905/tm267842d1_8k.htm｜as_of：2026-03-03
<<<
Item 8.01 below, which is incorporated by reference into this Item 2.03.
Item 8.01. Other Events
On
March 3, 2026, Howmet Aerospace Inc. (the “Company” or “Howmet Aerospace”) closed its previously announced
underwritten public offering of $400,000,000 aggregate principal amount of 3.750% notes due 2028 (the “2028 Notes”), $300,000,000
aggregate principal amount of 3.900% notes due 2029 (the “2029 Notes”) and $500,000,000 aggregate principal amount of 4.750%
notes due 2036 (the “2036 Notes” and, together with the 2028 Notes and the 2029 Notes, the “Notes”). The Notes
were issued under the Indenture dated as of September 30, 1993 between Alcoa Inc. (“Alcoa”), a Pennsylvania corporation,
and The Bank of New York Mellon Trust Company, N.A., as successor in interest to J. P. Morgan Trust Company,
N.A. (formerly known as Chase Manhattan Trust Company, National Association, as successor to PNC Bank, National Association), as trustee
(the “Trustee”), as supplemented by the First Supplemental Indenture dated as of January 25, 2007 between Alcoa
and the Trustee, the Second Supplemental Indenture dated as of July 15, 2008 between Alcoa and
the Trustee, the Fourth Supplemental Indenture dated as of December 31, 2017 among Arconic Inc., a Pennsylvania corporation,
Arconic Inc., a Delaware corporation, and the Trustee, the Fifth Supplemental Indenture dated as of April 16,…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HWM_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
