你是 stock-analyst v20 DD 的證據採集子 agent。標的：TTMI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - TTMI TTM Technologies acquisition merger 2025 2026
  - TTMI TTM Technologies class action lawsuit securities fraud
  - TTMI TTM Technologies clinical trial FDA approval 2025 2026
  - TTMI TTM Technologies product launch recall warning letter
  - TTMI TTM Technologies SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm｜as_of：2026-02-17
<<<
ITEM 3. LEGAL PROCEEDINGS
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1116942/000119312526051976/ttmi-20251229.htm｜as_of：2026-02-17
<<<
10-Q 000-31285 10.6 August 10, 2023 10.13‡ TTM Technologies, Inc. 2023 Form of Performance-Based RSU Grant Notice and Award Agreement pursuant to TTM Technologies, Inc. 2023 Incentive Compensation Plan 10-Q 000-31285 10.7 August 10, 2023 10.14‡ TTM Technologies, Inc. 2024 Form of Restricted Stock Unit Award Grant Notice (for non-employee directors) pursuant to TTM Technologies, Inc. 2023 Incentive Compensation Plan 10-K 000-31285 10.14 February 21, 2025 10.15‡ Letter Agreement, dated as of July 28, 2023, by and between the Company and Daniel L. Boehle 8-K 000-31285 10.1 August 2, 2023 10.16 Amended & Restated Facility Agreement, dated as of June 14, 2023, by and among TTM Technologies China Limited and TTM Technologies Trading (Asia) Company Limited, as borrowers, TTM Technologies (Asia Pacific) Limited and other parties as guarantors, The Hong Kong and Shanghai Banking Corporation Limited and Barclays Bank PLC as original lenders, and The Hong Kong and Shanghai Banking Corporation Limited as arranger, facility agent, security trustee and issuing bank 8-K 000-31285 10.1 June 20, 2023 10.17 First Amendment, dated as of June 10, 2024, to that certain Amended and Restated ABL Credit Agreement, dated as of May 30, 2023, by and among TTM Technologies, Inc., as Borrower, the several Lenders from time to time parties thereto, JPMorgan Chase Bank, N.A., as Administrative Agent, Barclays Bank PLC, Bank of America,…
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001116942&type=8-K｜as_of：2026-10-25
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-25 至 2026-10-25 共 20 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 7 份。
2026-10-22 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-19 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-13 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-30 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-24 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；3.03 Material Modification to Rights of Security Holders；9.01 Financial Statements and Exhibits
2026-09-10 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-17 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-06 8-K/A Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-08-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-18 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-06-03 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；3.03 Material Modification to Rights of Security Holders；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-27 8-K Items 7.01 Regulation FD Disclosure
2026-05-18 8-K Items 7.01 Regulation FD Disclosure
2026-05-08 8-K/A Items 5.02 Departure/Election of Directors or Officers
2026-05-08 8-K Items 5.02 Departure/Election of Directors or Officers；5.07 Submission of Matters to a Vote of Security Holders；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-02 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-13 8-K Items 7.01 Regulation FD Disclosure
2025-10-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-09-30，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1116942/000119312526409136/d147406d8k.htm｜as_of：2026-09-30
<<<
Item 1.01.
Entry into a Material Definitive Agreement.
In connection with the completion of the Acquisition (as defined and discussed below in Item 8.01), on September 30, 2026 (the “Closing Date”), TTM Technologies, Inc. (the “Company”) entered into the Third Amended and Restated Credit Agreement, dated as of September 30, 2026, by and among the Company, the foreign subsidiary borrowers party thereto, any designated borrowers party thereto, JPMorgan Chase Bank, N.A. (“JPM”), as Administrative Agent, and the other parties thereto (the “Third A&R Credit Agreement”). The Third A&R Credit Agreement, (which amends and restates the Company’s Second Amended and Restated Credit Agreement, dated as of June 1, 2026, by and among the Company, the foreign subsidiary borrowers party thereto, any designated borrowers party thereto, JPM, as Administrative Agent, and the other parties thereto (the “Prior Credit Agreement”)) provides for (i) an incremental senior secured term loan A facility in an aggregate principal amount of $300 million (the “Term A Incremental Facility”) and (ii) a seven-year incremental senior secured term loan B facility in an aggregate principal amount of $800 million (the “Term B Incremental Facility” and, together with the Term A Incremental Facility, the “Incremental Facilities”).…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-24，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1116942/000119312526401013/d186334d8k.htm｜as_of：2026-09-24
<<<
Item 1.01. Entry Into a Material Definitive Agreement.
On September 24, 2026, TTM Technologies, Inc. (the “Company”) completed its previously announced private offering (the “Offering”) of $500 million in aggregate principal amount of its 6.750% senior notes due 2034 (the “Notes”). The Offering was conducted as a private placement exempt from registration under the Securities Act of 1933, as amended (the “Securities Act”). The Company intends to use the net proceeds of the Offering, together with expected borrowings from a $300 million incremental senior secured term loan A and a $800 million incremental senior secured term loan B (collectively, the “Incremental Facilities”), to fund the purchase price for the previously announced proposed acquisition of EDS Intermediate Holding, LLC (the “Acquisition”), for general corporate purposes, which may include reducing outstanding borrowings under the Revolving Credit Facility (as defined below) to fund the purchase price for the previously announced acquisition of Swiss Technology Group AG, and to pay related fees and expenses.
On September 24, 2026, the Company issued and sold the Notes, which were priced at par value. Interest on the Notes accrues at the rate of 6.750% per annum and is payable semi-annually in cash in arrears on April 1 and October 1 of each year, beginning on April 1, 2027.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-08-17，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1116942/000119312526353148/d375900d8k.htm｜as_of：2026-08-17
<<<
Item 1.01.
Entry Into a Material Definitive Agreement.
Purchase Agreement
On August 15, 2026, TTM Technologies, Inc., a Delaware corporation (the “Company”), TTM Technologies North America, LLC, a Delaware limited liability company and a wholly-owned subsidiary of the Company (the “Buyer”), EDS Intermediate Holding, LLC, a Delaware limited liability company (“Epiq Solutions”), and EDS TopCo, LP, a Delaware limited partnership (the “Seller”), entered into a definitive securities purchase agreement (the “Purchase Agreement”) pursuant to which the Buyer agreed to purchase from the Seller all of the issued and outstanding membership interests of Epiq Solutions for a purchase price of $1,100,000,000 in cash (the “Purchase Price”), subject to customary working capital and certain other adjustments (the “Acquisition”). The Acquisition has been unanimously approved by the board of directors of the Company. Pursuant to the Purchase Agreement, the Company has guaranteed the payment and performance obligations of the Buyer under the Purchase Agreement, including the obligation of Buyer to pay the Purchase Price (the “Parent Guarantee”), and the Company is a party to the Purchase Agreement solely for the limited purpose of providing the Parent Guarantee.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
