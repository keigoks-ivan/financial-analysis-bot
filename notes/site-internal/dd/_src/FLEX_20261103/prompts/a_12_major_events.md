你是 stock-analyst v20 DD 的證據採集子 agent。標的：FLEX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - FLEX Flex acquisition merger 2025 2026
  - FLEX Flex class action lawsuit securities fraud
  - FLEX Flex clinical trial FDA approval 2025 2026
  - FLEX Flex product launch recall warning letter
  - FLEX Flex SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
We are, from time to time, subject to claims, lawsuits, investigations, and regulatory or administrative proceedings across the jurisdictions where we operate. These matters may involve commercial disputes, regulatory compliance, intellectual property, antitrust, product liability, employment and labor, privacy and data protection, securities laws, governance, and tax. Adverse outcomes, whether by judgment, settlement, consent decree, or otherwise, could require monetary payments, penalties, injunctive relief, operational changes, monitorships, remedial measures, or enhanced compliance controls. Even if we prevail, we may incur substantial costs, increased insurance premiums, and management distraction that disrupts our operations and harms our reputation with customers, suppliers, employees, and regulators. Outcomes are inherently unpredictable, and our accruals and insurance coverage may be insufficient or unavailable. Any of these matters could materially adversely affect our business, financial condition, results of operations, and cash flows.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
Reductions related to lapse of applicable statute of limitations (13) (23) Settlements (52) — Impact from foreign exchange rates fluctuation 7 — Balance, end of fiscal year $ 159 $ 180 The Company’s unrecognized tax benefits are subject to change over the next twelve months primarily as a result of the expiration of certain statutes of limitations and as audits are settled. The Company believes it is reasonably possible that the total amount of unrecognized tax benefits could decrease by an additional approximate $10 million within the next twelve months primarily due to potential settlements of various audits and the expiration of certain statutes of limitations.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
8-K 000-23354 3/7/2025 10.1 10.06 Form of Restricted Share Unit Award Agreement under the Flex Ltd. Amended and Restated 2017 Equity Incentive Plan for Non-Employee Directors† 10-Q 000-23354 10/31/2022 10.02 10.07 Form of Restricted Share Unit Award Agreement under the Amended and Restated Flex Ltd. 2017 Equity Incentive Plan for performance-based vesting awards (FY24)† 10-Q 000-23354 7/31/2023 10.03 10.08 Form of Restricted Share Unit Award Agreement under the Amended and Restated 2017 Equity Incentive Plan for service-based vesting awards (FY25)† 10-Q 000-23354 7/26/2024 10.03 10.09 Form of Restricted Share Unit Award Agreement under the Amended and Restated 2017 Equity Incentive Plan for performance-based vesting awards (FY25)† 10-Q 000-23354 7/26/2024 10.04 10.10 Form of Restricted Share Unit Award Agreement under the Amended and Restated 2017 Equity Incentive Plan for service-based vesting awards (FY25 2-year prorated)† 10-Q 000-23354 10/31/2024 10.01 10.11 Form of Restricted Share Unit Award Agreement under the Amended and Restated 2017 Equity Incentive Plan for service-based vesting awards (FY25 supplemental equity)† 10-Q 000-23354 10/31/2024 10.02 104 Table of Contents Incorporated by Reference Exhibit No. Exhibit Form File No. Filing Date Exhibit No.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000866374&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 17 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 10 份。
2026-10-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-14 8-K Items 1.01 Entry into a Material Definitive Agreement；2.01 Completion of Acquisition or Disposition of Assets；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-13 8-K Items 3.02 Unregistered Sales of Equity Securities；9.01 Financial Statements and Exhibits
2026-10-05 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；3.02 Unregistered Sales of Equity Securities；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-02 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-09-15 8-K Items 5.02 Departure/Election of Directors or Officers；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-04 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-07 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；8.01 Other Events
2026-07-29 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-12 8-K Items 5.02 Departure/Election of Directors or Officers
2026-06-02 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-05-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-04 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-30 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-11-13 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-10-14，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/866374/000119312526421058/d147467d8k.htm｜as_of：2026-10-14
<<<
Item 2.01 and Item 2.03 of this Current Report on Form 8-K regarding the use of proceeds under the Bridge Credit Facility is hereby incorporated by reference into this Item 1.01.
A copy of the Bridge Credit Agreement is filed with this Current Report on Form 8-K as Exhibit 10.1 and is incorporated by reference into this Item 1.01 as though fully set forth herein. The foregoing summary description of the Bridge Credit Agreement is not intended to be complete and is qualified in its entirety by the complete text of the Bridge Credit Agreement.
Item 2.01.
Completion of Acquisition or Disposition of Assets.
As previously disclosed, on September 3, 2026, the Company, ACS Acquisitions, Inc., a Delaware corporation and wholly owned subsidiary of the Company (the “Purchaser”), EPC Power Corp., a Delaware corporation (“EPC Power”), and Charge Parent, LLC, a Delaware limited liability company (the “Seller”), entered into a Stock Purchase Agreement (the “Purchase Agreement”), pursuant to which the Purchaser agreed to acquire all of the equity interests of EPC Power from the Seller (such transaction, the “Transaction”). On October 14, 2026, the Company completed the Transaction.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-10-05，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/866374/000119312526413173/d123485d8k.htm｜as_of：2026-10-05
<<<
Item 1.01. Entry into a Material Definitive Agreement
Series A Convertible Preferred Stock Investment Agreement
As previously announced, Flex Ltd., a company organized under the laws of Singapore (the “Company” or “Flex”), intends to separate its Cloud and Power Infrastructure business into an independent publicly traded company, Axiom Solutions International, Inc., a Texas corporation and currently a wholly owned subsidiary of Flex (“Axiom”), in the first quarter of 2027 (the “Spin-Off”). As also announced, on September 3, 2026, a wholly owned subsidiary of Flex entered into a stock purchase agreement (the “EPC Purchase Agreement”) to acquire all of the equity interests of EPC Power Corp., a Delaware corporation (“EPC Power”), with Flex guaranteeing such subsidiary’s obligations thereunder (such transaction, the “EPC Power Acquisition”). The EPC Power Acquisition is expected to close in the fourth quarter of 2026 and, upon the closing of the EPC Power Acquisition, EPC Power is expected to become part of the Company’s Cloud and Power Infrastructure business prior to the Spin-Off.…
>>>

[8] 來源：SEC EDGAR｜文件：8-K（2026-10-02，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/866374/000110465926113282/tm2626870d1_8k.htm｜as_of：2026-10-02
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On
September 29, 2026 (the “Closing Date”), Flex Ltd. (the “Company” or “Flex”) entered into a Credit
Agreement (the “Credit Agreement”), by and among the Company, as borrower, the lenders party thereto, and Citibank, N.A.,
as administrative agent, which provides a senior term loan credit facility (the “Credit Facility”) in an aggregate committed
amount of $3.3 billion. The Credit Facility was not drawn on the Closing Date. Subject to the satisfaction of the conditions set forth
in the Credit Agreement, the Company may borrow under the Credit Facility in a single advance during the availability period provided
therein. The Credit Facility will mature 364 days after the date on which it is funded.
Loans
under the Credit Agreement bear interest at a floating rate, which can be, at the Company’s option, either (a) Term SOFR (as
defined in the Credit Agreement) plus an applicable margin or (b) the Base Rate (as defined in the Credit Agreement) plus an applicable
margin, in each case, with such margin determined based on the Company’s senior unsecured long-term debt ratings.
The
Credit Agreement contains various customary covenants, including, but not limited to, restrictions on the ability of the Company and its…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
