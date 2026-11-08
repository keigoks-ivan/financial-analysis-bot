你是 stock-analyst v20 DD 的證據採集子 agent。標的：SEZL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - SEZL Sezzle acquisition merger 2025 2026
  - SEZL Sezzle class action lawsuit securities fraud
  - SEZL Sezzle clinical trial FDA approval 2025 2026
  - SEZL Sezzle product launch recall warning letter
  - SEZL Sezzle SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm｜as_of：2026-02-26
<<<
ITEM 3. LEGAL PROCEEDINGS
Except as set forth below, we are not currently involved in any material legal proceedings, other than ordinary routine litigation incidental to the business, to which we or any of our subsidiaries is a party or of which any of their property is subject.
On June 9, 2025, we filed a lawsuit against Shopify, Inc., in the U.S. District Court for the District of Minnesota asserting federal and state antitrust violations. The lawsuit alleges that Shopify has been engaging and continues to engage in monopolistic and anticompetitive business practices in order to stifle competition for “buy now, pay later” service options on Shopify’s e-commerce platform. Sezzle is a seeking an injunction to prevent Shopify from continuing its anticompetitive conduct and to restore competition and consumer choice. Sezzle is also seeking damages, which could be tripled under applicable laws. Shopify has denied the allegations and filed a motion to dismiss the complaint. A hearing on such motion was held on December 8, 2025. As of the date of this report, the court has not issued a ruling on such motion and its outcome, including the timing of that outcome, cannot be predicted with certainty.
While the outcome of these matters cannot be predicted with certainty, we do not believe that the outcome of any of these matters, individually or in the aggregate, will have a material adverse effect on our consolidated balance sheets, operations and comprehensive income, or cash flows.
Table of Contents
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1. Business（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm｜as_of：2026-02-26
<<<
15 Table of Contents Regulatory Environment Overview Various aspects of our business and services are subject to U.S. federal, state, and local regulation, as well as regulation outside the United States including Canada. Certain of our services also are subject to rules promulgated by various card networks and other authorities, as more fully described below. These descriptions are not exhaustive, and these laws, regulations and rules frequently change and are increasing in number and scope. Failure to comply with these laws, regulations and rules may result in, among other things, revocation of required licenses or registrations, voiding or rescission of lending agreements, class action lawsuits, administrative enforcement actions and civil and/or criminal liability.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1662991/000166299126000016/szl-20251231.htm｜as_of：2026-02-26
<<<
Compliance with these laws and regulations is costly, time-consuming, and limits our operational flexibility. Any failure or perceived failure to comply with any statute, ordinance, regulation, rules and/or guidance may subject us to significant fines, penalties, criminal and civil lawsuits, and enforcement actions in one or more jurisdictions; result in significant compliance costs and licensing requirements, cause us to lose existing licenses or prevent or delay us from obtaining pending licenses; restrict our operations or force us to make changes to our business practices; and incur significant reputational damage. Legal proceedings brought under state consumer protection statutes or under federal consumer financial services statutes subject to the jurisdiction of the CFPB and FTC, in particular, may result in a separate fine for each violation of the statute, which, particularly in the case of class action lawsuits, could result in damages in excess of the amounts we earned from the underlying activities.

In addition, a number of participants in the consumer finance industry have been and are the subject of putative class action lawsuits; state attorney general actions and other state regulatory actions; federal regulatory enforcement actions, including actions relating to alleged UDAAP; violations of state licensing and lending laws, including state interest rate limits; actions alleging discrimination on the basis of race, ethnicity, gender, or other prohibited bases; and allegations of noncompliance with various state and federal laws and regulations relating to originating and servicing consumer finance loans. BNPL competitors in the BNPL space are subject to ongoing class action litigation, including allegations of unfair business and deceptive practices, and we may become subject to similar types of litigation in the future. The current regulatory environment, increased regulatory compliance efforts, and enhanced regulatory enforcement have resulted in significant operational and compliance costs and may prevent us from providing certain products and services. There is no assurance that these regulatory matters or other factors will not, in the future, affect how we conduct our business and, in turn, have a material adverse effect on our business.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001662991&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 19 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。
2026-11-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-08 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-08-28 8-K Items 8.01 Other Events
2026-08-18 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-08-12 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-14 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-13 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-12 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-15 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-09 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-03-20 8-K Items 4.01 Changes in Registrant's Certifying Accountant；9.01 Financial Statements and Exhibits
2026-03-06 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-25 8-K Items 2.02 Results of Operations and Financial Condition；4.02 Non-Reliance on Previously Issued Financial Statements；9.01 Financial Statements and Exhibits
2026-02-02 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-15 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-14 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-02-25，Item 4.02）｜章節：8-K Item 4.02 Non-Reliance on Previously Issued Financial Statements｜url：https://www.sec.gov/Archives/edgar/data/1662991/000166299126000014/sezl-20260219.htm｜as_of：2026-02-25
<<<
Item 4.02. Non-Reliance on Previously Issued Financial Statements or a Related Audit Report or Completed Interim Review
In connection with the preparation of the Company’s Annual Report on Form 10-K for the year ended December 31, 2025 (“2025 Form 10-K”), the Company concluded that it had not appropriately classified purchases and originations of notes receivable, and proceeds from repayments thereof, as “investing activities” within its Consolidated Statements of Cash Flows for the year ended December 31, 2024. The impacts of the restatement for the year ended December 31, 2024, as described above, are reflected in the Consolidated Statements of Cash Flows and had no impact on the Consolidated Balance Sheets, Consolidated Statements of Operations and Comprehensive Income, Consolidated Statements of Stockholders’ Equity, or the Notes to the Consolidated Financial Statements. As a result, the Company’s Consolidated Statements of Cash Flows for the following periods (collectively, the “Restated Consolidated Statements of Cash Flows”) should no longer be relied upon: (1) the year ended December 31, 2024, (2) the three months ended March 31, 2024, and 2025, (3) the six months ended June 30, 2024 and 2025, and (4) the nine months ended September 30, 2024 and 2025.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-08-18，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1662991/000166299126000144/sezl-20260812.htm｜as_of：2026-08-18
<<<
Item 1.01. Entry into a Material Definitive Agreement
On August 12, 2026, Sezzle Inc. (“Sezzle” or the “Company”) and WebBank, a Utah-chartered industrial bank (“WebBank”), entered into a Second Amended and Restated Loan and Receivables Sale Agreement (the “Receivables Sale Agreement”) and a Second Amended and Restated Marketing and Servicing Agreement (the “Servicing Agreement” and, together with the Receivables Sale Agreement, the “Second Amended Bank Program Agreements”). The Second Amended Bank Program Agreements amend and restate the previously disclosed Amended and Restated Loan and Receivables Sale Agreement and Amended and Restated Marketing and Servicing Agreement, each dated as of September 26, 2024, between the Company and WebBank, governing the parties’ existing bank partnership program (the “Program”). Under the Program, WebBank originates and funds the consumer installment loans offered in connection with the Company’s products.
The Second Amended Bank Program Agreements expand the Program to support two additional Company products: SezzleCash, a cash advance product, and Sezzle Send, a payments product supported by installment loans whose proceeds are disbursed by WebBank to deposit accounts established by WebBank.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-12，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1662991/000166299126000071/sezl-20260507.htm｜as_of：2026-05-12
<<<
Item 1.01. Entry into a Material Definitive Agreement
Revolving Credit and Security Agreement
On May 7, 2026, Sezzle Funding SPE II, LLC (the “Borrower”), a wholly owned indirect subsidiary of Sezzle Inc. (“Sezzle” or the “Company”), Bastion Funding VI, LP, as administrative agent (the “Agent”), and certain lenders party thereto, executed the Amended and Restated Revolving Credit and Security Agreement (the “Credit Agreement”). Under the Credit Agreement, the Borrower entered into a senior, secured, asset-based revolving credit facility (the “Revolving Credit Facility”) with a borrowing capacity of up to $300 million, and the option to increase the borrowing capacity by an additional $75 million.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261108/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
