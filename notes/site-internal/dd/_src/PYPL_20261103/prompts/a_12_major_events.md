你是 stock-analyst v20 DD 的證據採集子 agent。標的：PYPL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - PYPL PayPal Holdings acquisition merger 2025 2026
  - PYPL PayPal Holdings class action lawsuit securities fraud
  - PYPL PayPal Holdings clinical trial FDA approval 2025 2026
  - PYPL PayPal Holdings product launch recall warning letter
  - PYPL PayPal Holdings SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm｜as_of：2026-02-03
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm｜as_of：2026-02-03
<<<
Consumer Protection Violations of consumer protection law in applicable jurisdictions, including federal and state laws and regulations in the U.S. such as the Electronic Fund Transfer Act (“EFTA”) and Regulation E as implemented by the Consumer Financial Protection Bureau (“CFPB”), could result in the assessment of significant actual damages or statutory damages or penalties (including treble damages in some instances) and plaintiffs’ attorneys’ fees. We are subject to, and have paid amounts in settlement of, lawsuits alleging that our business violated the EFTA and Regulation E or otherwise advancing claims for relief relating to our business practices (e.g., that we improperly held consumer funds or otherwise improperly limited consumer accounts).

We are regularly subject to claims, individual and class action lawsuits, arbitration proceedings, government and regulatory investigations, inquiries, actions or requests, and other proceedings alleging violations of laws, rules, and regulations with respect to competition, antitrust, intellectual property, privacy, data protection, information security, anti-money laundering, counter-terrorist financing, sanctions, anti-bribery, anti-corruption, consumer protection (including unfair, deceptive, or abusive acts or practices), the terms of our customer agreements, fraud, accessibility, securities, tax, labor and employment, commercial disputes, services, charitable fundraising, contract disputes, escheatment of unclaimed or abandoned property, product liability, use of our services for illegal purposes, the matters described in “Note 13—Commitments and Contingencies—Litigation and Regulatory Matters—General Matters” to our consolidated financial statements, and other matters. We expect that the number and significance of these disputes and inquiries will continue to increase as our products, services, and business expand in complexity, scale, scope, and geographic reach, including through acquisitions of businesses and technology, and as a result of expanded enforcement of certain existing laws and regulations by federal, state and local agencies. For example, there continues to be enforcement activity in connection with federal and state consumer protection laws, including suits which seek civil penalties.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm｜as_of：2026-02-03
<<<
On December 20, 2022, a civil lawsuit captioned State of Hawai‘i, by its Office of Consumer Protection, v. PayPal, Inc., and PayPal Holdings, Inc., Case No. 1CCV-22-0001610, was filed in the Circuit Court of the First Circuit of the State of Hawai‘i (the “Hawai‘i Action”). The Hawai‘i Action asserts claims for unfair and deceptive acts and practices under Hawai‘i Revised Statutes Sections 480-2(a) and 481A-3(a). Plaintiff seeks injunctive relief as well as unspecified penalties and other monetary relief. On July 14, 2023, the court denied Defendants’ motion to dismiss the complaint. We executed a final settlement in this matter on December 17, 2025.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001633917&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-27 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-21 8-K Items 5.02 Departure/Election of Directors or Officers；5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-15 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-30 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-25 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-03 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-03 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-11-17 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-14 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2025-11-17，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1633917/000119312525284822/d93754d8k.htm｜as_of：2025-11-17
<<<
Item 1.01.
Entry into a Material Definitive Agreement
Receivables Purchase Agreement
On November 11, 2025, PayPal (Europe) S.à r.l. et Cie, SCA (as Seller and a Receivables Manager) and PayPal UK Ltd (as a Receivables Manager and collectively with PayPal (Europe) S.à r.l. et Cie, SCA, the Receivables Managers) entered into a Receivables Purchase Agreement with Alps 2.0 Partners S.à r.l. (as Purchaser), BNY Mellon Corporate Trustee Services limited (as Security Agent), Avega S.à r.l. (as Back-Up Receivables Manager Facilitator) and Alps 2.0 Partners (Holding) S.à r.l. (as Class C Lender) to sell up to €65 billion of UK and European buy now, pay later (BNPL) loan receivables originated by the Seller. The Receivables Purchase Agreement consists of a forward-flow arrangement for the sale of future originations of eligible loans over a 28-month commitment period (subject to extension if agreed by the parties) (the “Transaction”). Subject to certain conditions being satisfied, the Transaction is expected to close in the fourth quarter of 2025.
Each of the Seller and Purchaser has made certain representations, warranties and covenants.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-11-14，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1633917/000119312525283161/d60784d8k.htm｜as_of：2025-11-14
<<<
Item 1.01.
Entry into a Material Definitive Agreement.
On November 14, 2025, PayPal Holdings, Inc. (the “Company”) established a commercial paper program (the “Program”) pursuant to which it may issue short-term, unsecured commercial paper notes (the “Notes”) under the exemption from the registration requirements of the Securities Act of 1933, as amended (the “Securities Act”). Amounts available under the Program may be borrowed, repaid and re-borrowed from time to time, with the aggregate face or principal amount of the Notes outstanding under the Program at any time not to exceed $5.0 billion, unless such amount is increased in accordance with the terms of each Dealer Agreement (as defined herein). Net proceeds of the issuances of the Notes are expected to be used for general corporate purposes.
The Notes will be sold under customary market terms in the U.S. commercial paper market at a discount from par or at par and bear interest at rates determined at the time of issuance. The maturities of the Notes may vary, but shall not exceed 397 days from the date of issuance. It is expected that the revolving credit facility of the Company will serve as a liquidity backstop for any issuances under the Program.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-15，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1633917/000119312526226653/d930458d8k.htm｜as_of：2026-05-15
<<<
Item 8.01.
Other Events
Notes Offering
On May 15, 2026, PayPal Holdings, Inc. (the “Company”) issued and sold $2.0 billion aggregate principal amount of senior notes, consisting of $650,000,000 aggregate principal amount of 4.550% notes due 2028 (the “2028 Notes”), $850,000,000 aggregate principal amount of 4.950% notes due 2031 (the “2031 Notes”) and $500,000,000 aggregate principal amount of 5.550% notes due 2036 (the “2036 Notes” and, together with the 2028 Notes and the 2031 Notes, the “Notes”).
The Notes are being issued pursuant to an indenture, dated as of September 26, 2019 (the “Base Indenture”), between the Company and Computershare Trust Company, N.A. as successor to Wells Fargo Bank, National Association, as trustee, together with the officer’s certificate, dated May 15, 2026 (the “Officer’s Certificate” and, together with the Base Indenture, the “Indenture”), issued pursuant to the Indenture establishing the terms of each series of Notes.
The Notes are being issued pursuant to the Company’s Registration Statement on Form S-3 filed with the Securities and Exchange Commission on February 5, 2025 (Registration Statement No. 333-284693) (the “Registration Statement”).
The 2028 Notes will mature on June 1, 2028, the 2031 Notes will mature on June 1, 2031 and the 2036 Notes will mature on June 1, 2036, unless, in each case, earlier redeemed or repurchased.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
