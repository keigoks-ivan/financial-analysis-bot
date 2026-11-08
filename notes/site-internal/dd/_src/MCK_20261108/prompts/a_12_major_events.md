你是 stock-analyst v20 DD 的證據採集子 agent。標的：MCK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - MCK McKesson acquisition merger 2025 2026
  - MCK McKesson class action lawsuit securities fraud
  - MCK McKesson clinical trial FDA approval 2025 2026
  - MCK McKesson product launch recall warning letter
  - MCK McKesson SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
Item 3. Legal Proceedings.
Certain legal proceedings in which we are involved are discussed in Financial Note 17, “Commitments and Contingent Liabilities,” to the consolidated financial statements included in this Annual Report. Disclosure of an environmental proceeding with a governmental agency is generally included only if we expect monetary sanctions in the proceeding to exceed $1 million, unless otherwise material.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 1. Business（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
Competition and Related Laws: Antitrust and competition laws (“competition laws”) in the U.S. and elsewhere prohibit types of conduct, practices, or arrangements deemed to be anti-competitive. Enforcement of competition laws in the healthcare industry remains a focus of the FTC and the U.S. Department of Justice. Some of our strategic transactions may require review by competition regulators, with potential delays or other unfavorable outcomes. Violations of competition laws can result in sanctions and other adverse actions, including criminal and civil penalties. Private plaintiffs also may bring civil lawsuits for alleged violations of competition laws, including claims for treble damages. Additionally, laws may be proposed to restrict certain healthcare ownership structures or arrangements, such as vertical integration involving physician practice administrative or management services and pharmaceutical distribution services, where traditional antitrust standards might not be implicated. Competition and related laws contribute to our compliance efforts and expense, and the enforcement, enactment, expansion, or application of any of the foregoing types of laws might materially adversely affect our operations and growth strategy.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
Non-Governmental Plaintiff Claims The Company has also been a defendant in hundreds of opioid-related cases brought in the U.S. by private plaintiffs, such as hospitals, health and welfare funds, third-party payors, and individuals. These claims, and those of private entities generally, are not included in the settlement agreements described above. The Company and two other national distributors reached class-action settlements with representatives of nationwide groups of acute care hospitals and certain third-party payors. The claims of remaining U.S. non-governmental plaintiffs are not included in the charges recorded by the Company (described below).

Other Litigation and Claims On or about April 25, 2018, a second amended qui tam complaint filed in the U.S. District Court for the Eastern District of New York was served on McKesson Corporation, McKesson Specialty Care Distribution Corporation, McKesson Specialty Distribution LLC, McKesson Specialty Care Distribution Joint Venture, L.P., Oncology Therapeutics Network Corporation, Oncology Therapeutics Network Joint Venture, L.P., US Oncology, Inc., and US Oncology Specialty, L.P. by Omni Healthcare, Inc. as relator, purportedly on behalf of the United States and 33 cities and states alleging that from 2001 through 2010 the defendants repackaged and sold single-dose syringes of oncology medications in a manner that violated the federal False Claims Act and various state and local false claims statutes, and seeking damages, treble damages, civil penalties, attorneys’ fees and costs of suit, all in unspecified amounts. United States of America ex rel. Omni Healthcare, Inc. v. McKesson Corp., et al., 1:12-cv-06440 (E.D.N.Y.). The United States and the other governmental plaintiffs declined to intervene in the suit. In February 2019, the court dismissed all of the defendants except McKesson Corporation and Oncology Therapeutics Network Corp.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000927653&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-11-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-06 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-28 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-24 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-07-01 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-12 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-05-07 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-28 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-04-06 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-03-06 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-05 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-06-12，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000167/mck-20260609.htm｜as_of：2026-06-12
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On June 9, 2026, certain of McKesson Corporation’s (the “Company”) subsidiaries, including McKesson Medical-Surgical Top Holdings, Inc. (the “Borrower”), entered into an amendment (the “Amendment”) to the Credit Agreement , dated as of April 1, 2026, among, the Borrower, the lenders from time to time party thereto and JPMorgan Chase Bank, N.A., as administrative agent and collateral agent (as so amended, the “Credit Agreement”), to provide for a $2,250.0 million senior secured term “B” loan facility due 2032 (the “Term B Loan Facility”). All other terms of the Credit Agreement will remain substantially the same except as amended by the Amendment.
Borrowings under the Term B Loan Facility will bear interest, at the Borrower’s option, at a rate equal to either (i) the Adjusted Term SOFR Rate (as defined in the Credit Agreement), plus an applicable margin equal to 2.25% per annum or (ii) the Base Rate (as defined in the Credit Agreement), plus an applicable margin equal to 1.25% per annum. The Borrower selected an initial interest rate equal to the Adjusted Term SOFR Rate plus the applicable margin of 2.25% per annum.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-04-28，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000053/mck-20260428.htm｜as_of：2026-04-28
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On April 24, 2026, McKesson Corporation (“McKesson” or the “Company”) entered into a Credit Agreement (the “New Revolving Credit Facility”) among the Company, as borrower, the lenders party thereto, Bank of America, N.A., as administrative agent, and the other parties thereto. The New Revolving Credit Facility replaces the Company’s existing $1.0 billion 364-day senior unsecured revolving credit facility, dated as of May 8, 2025 (the “Existing 364-Day Credit Facility”) and the Company’s existing $4.0 billion five-year senior unsecured revolving credit facility, dated as of November 7, 2022, as amended (the “Existing Credit Facility” and, together with the Existing 364-Day Credit Facility, the “Existing Credit Facilities”), which was filed with the Securities and Exchange Commission on November 7, 2022 as Exhibit 10.1 to McKesson’s Current Report on Form 8-K. The Existing 364-Day Credit Facility was scheduled to mature in May 2026 and provided a revolving line of credit of up to $1.0 billion. The Existing Credit Facility was scheduled to mature in November 2029 and provided a revolving line of credit available of up to $4.0 billion and a $3.6 billion aggregate sublimit of availability in Canadian Dollars, British Pound Sterling and Euros. There were no borrowings outstanding under the Existing Credit Facilities at the time of termination.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-04-06，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000045/mck-20260401.htm｜as_of：2026-04-06
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On April 1, 2026, certain of McKesson Corporation’s (the “Company”) subsidiaries, including McKesson Medical-Surgical Top Holdings, Inc. (the “Borrower”), entered into a credit agreement (the “Credit Agreement”) with the lenders and issuing banks party thereto and JPMorgan Chase Bank, N.A., as administrative agent and collateral agent providing for (i) a $750.0 million senior secured term “A” loan facility due 2031 (the “Term Loan A-1 Facility”), (ii) a $250.0 million senior secured term “A” loan facility due 2028 (the “Term Loan A-2 Facility” and, together with the Term Loan A-1 Facility, the “Term Loan A Facilities”) and (iii) a $1,000.0 million senior secured revolving credit facility (the “Revolving Credit Facility” and, together with the Term Loan A Facilities, the “Senior Secured Credit Facilities”). The Revolving Credit Facility matures on April 1, 2031. The Borrower and certain other subsidiaries of the Company also entered into security, guaranty and other related agreements in connection with the Credit Agreement.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
