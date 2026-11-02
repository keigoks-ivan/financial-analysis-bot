你是 stock-analyst v20 DD 的證據採集子 agent。標的：PWR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - PWR Quanta Services acquisition merger 2025 2026
  - PWR Quanta Services class action lawsuit securities fraud
  - PWR Quanta Services clinical trial FDA approval 2025 2026
  - PWR Quanta Services product launch recall warning letter
  - PWR Quanta Services SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm｜as_of：2026-02-19
<<<
ITEM 3.Legal Proceedings
We are from time to time party to various lawsuits, claims and other legal proceedings that arise in the ordinary course of business. These actions typically seek, among other things, compensation for alleged personal injury, property damage, breach of contract, negligence or gross negligence, environmental liabilities, wage and hour claims and other employment-related damages, punitive damages, consequential damages, civil penalties or other losses, or injunctive or declaratory relief, as well as interest and attorneys’ fees associated with such claims. With respect to all such lawsuits, claims and proceedings, we record a reserve when we believe it is probable that a loss has been incurred and the amount of loss can be reasonably estimated. In addition, we disclose matters for which management believes a material loss is at least reasonably possible. See Note 16 of the Notes to Consolidated Financial Statements in Item 8. Financial Statements and Supplementary Data in Part II of this Annual Report, which is incorporated by reference in this Item 3, for additional information regarding litigation, claims and other legal proceedings.
Environmental Matters
Item 103 of Regulation S-K requires disclosure of certain environmental matters in which a governmental authority is a party to the proceedings and when such proceedings involve the potential for monetary sanctions that management reasonably believes will exceed a specified threshold. Pursuant to SEC regulations, we use a threshold of $1.0 million for such proceedings.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm｜as_of：2026-02-19
<<<
We have in the past been, and may in the future be, named as a defendant in lawsuits, claims and other legal proceedings that arise in the ordinary course of our business. These actions seek, among other things, compensation for alleged personal injury (including claims for loss of life), workers’ compensation, employment discrimination, sexual harassment, workplace misconduct, wage and hour claims and other employment-related damages, compensation for breach of contract, negligence or gross negligence or property damage, environmental liabilities, multiemployer pension plan withdrawal liabilities, punitive damages, consequential damages, and civil penalties or other losses or injunctive or declaratory relief, as well as interest and attorneys’ fees associated with such claims. Furthermore, given the growth that we have experienced, we have become a more attractive target for lawsuits by various third parties.

In addition, we generally indemnify our customers for claims related to the services we provide and actions we take under our contracts, and, in some instances, we are allocated risk through our contract terms for actions by our customers, subcontractors or other third parties. Because our services in certain instances can be integral to the operation and performance of our customers’ infrastructure, we have been and may become subject to lawsuits or claims for any failure of the systems that we work on or damages caused by accidents and events related to such systems, even if our services are not the cause of such failures and damages. We could also be subject to civil and criminal liabilities, which could be material. Insurance coverage may not be available or may be insufficient for these lawsuits, claims or legal proceedings. The outcome of any allegations, lawsuits, claims or legal proceedings, as well as any public reaction thereto, is inherently uncertain and could result in significant costs, damage to our brands or reputation and diversion of management’s attention from our business. Payments of significant amounts, even if reserved, could materially and adversely affect our business, reputation, financial condition, results of operations and cash flows.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm｜as_of：2026-02-19
<<<
Stock-Based Compensation Restricted Stock Units to be Settled in Stock Quanta recognizes compensation expense for restricted stock units (RSUs) to be settled in common stock based on the grant date fair value of the awards, which is the number of RSUs granted multiplied by the closing price of Quanta’s common stock on the date of grant, net of estimated forfeitures. The resulting compensation expense for time-based RSU awards is recognized on a straight-line basis over the requisite service period, which is generally the vesting period. The non-cash stock compensation expense related to RSUs to be settled in common stock is included in “Selling, general and administrative expenses.”
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001050915&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-15 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-06 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-08-04 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-27 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-30 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-16 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-03-04 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-19 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-08-06，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1050915/000119312526337945/d164254d8k.htm｜as_of：2026-08-06
<<<
Item 1.01
Entry into a Material Definitive Agreement.
On August 6, 2026 (the “Closing Date”), Quanta Services, Inc. (the “Company”) issued (i) $500,000,000 aggregate principal amount of its 4.850% Senior Notes due 2029 (the “2029 Notes”), (ii) $750,000,000 aggregate principal amount of its 5.300% Senior Notes due 2033 (the “2033 Notes”) and (iii) $750,000,000 aggregate principal amount of its 5.550% Senior Notes due 2036 (the “2036 Notes,” and together with the 2029 Notes and the 2033 Notes, the “Notes”). The Notes were sold pursuant to an underwriting agreement, dated as of August 3, 2026 (the “Underwriting Agreement”), by and among the Company and BofA Securities, Inc., Wells Fargo Securities, LLC, J.P. Morgan Securities LLC, PNC Capital Markets LLC and Truist Securities, Inc., as representatives of the several underwriters named in Schedule A to the Underwriting Agreement, as previously reported on the Company’s Current Report on Form 8-K filed on August 4, 2026.
The 2029 Notes were issued under the indenture, dated as of September 22, 2020, between the Company, as issuer, and U.S. Bank Trust Company, National Association (as successor in interest to U.S. Bank National Association), as trustee (the “Trustee”) (the “Base Indenture”), as supplemented and amended by the tenth supplemental indenture, dated as of August 6, 2026, between the Company and the Trustee (the “Tenth Supplemental Indenture”).…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-08-04，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1050915/000119312526331400/d114917d8k.htm｜as_of：2026-08-04
<<<
Item 1.01
Entry into a Material Definitive Agreement.
On August 3, 2026, Quanta Services, Inc. (the “Company”) entered into an underwriting agreement (the “Underwriting Agreement”) with BofA Securities, Inc., Wells Fargo Securities, LLC, J.P. Morgan Securities LLC, PNC Capital Markets LLC and Truist Securities, Inc., as representatives of the several underwriters named in Schedule A to the Underwriting Agreement (the “Underwriters”), with respect to the issuance and sale in an underwritten public offering (the “Offering”) by the Company of (i) $500,000,000 aggregate principal amount of the Company’s 4.850% Senior Notes due 2029 (the “2029 Notes”), (ii) $750,000,000 aggregate principal amount of the Company’s 5.300% Senior Notes due 2033 (the “2033 Notes”) and (iii) $750,000,000 aggregate principal amount of the Company’s 5.550% Senior Notes due 2036 (together with the 2029 Notes and the 2033 Notes, the “Notes”).
The material terms of the Offering are described in the prospectus supplement dated August 3, 2026, as filed by the Company with the Securities and Exchange Commission (the “Commission”). The offer and sale of the Notes is registered with the Commission pursuant to the Company’s Registration Statement on Form S-3 (File No. 333-281209) that was filed with the Commission on August 2, 2024.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-27，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1050915/000119312526241989/d122565d8k.htm｜as_of：2026-05-27
<<<
Item 8.01
Other Events
On May 22, 2026, Quanta issued a press release announcing the election of Joseph Kim, a new independent director, to the Board of Directors at its 2026 Annual Meeting of Stockholders.
On May 22, 2026, the Company also announced that the Board authorized a new stock repurchase program. The new repurchase program, which was effective as of May 21, 2026, authorizes the Company to purchase, from time to time up to $1.0 billion of its outstanding common stock. Repurchases may be implemented through open-market or privately negotiated transactions, at management’s discretion, based on market and business conditions, applicable contractual and legal requirements and other factors. Quanta is not obligated to acquire any specific amount of common stock, and the Board may modify or terminate the new repurchase program at any time at its sole discretion and without notice.
Copies of the press releases are attached to this Current Report on Form 8-K as Exhibit 99.1 and Exhibit 99.2 and are incorporated herein by reference.
Item 9.01
Financial Statements and Exhibits.
(d) Exhibits.
Exhibit No.
Exhibit
99.1
Press Release of Quanta Services, Inc.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
