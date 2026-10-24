你是 stock-analyst v20 DD 的證據採集子 agent。標的：BE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - BE acquisition merger 2025 2026
  - BE class action lawsuit securities fraud
  - BE clinical trial FDA approval 2025 2026
  - BE product launch recall warning letter
  - BE SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
Item 3—Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
In addition, our restated certificate of incorporation and our amended and restated bylaws provide that the Court of Chancery of the State of Delaware will be the exclusive forum for: any derivative action or proceeding brought on our behalf; any action asserting a breach of fiduciary duty; any action asserting a claim against us arising pursuant to the Delaware General Corporation Law, our restated certificate of incorporation or our amended and restated bylaws; or any action asserting a claim against us that is governed by the internal affairs doctrine. Our restated certificate of incorporation and our amended and restated bylaws provide that unless we consent in writing to the selection of an alternative forum, the federal district courts of the U.S. shall be the exclusive forum for the resolution of any complaint asserting a cause of action arising under the Securities Act. These choice of forum provisions may limit a stockholder’s ability to bring a claim in a judicial forum that it finds favorable for disputes with us or any of our directors, officers, or other employees, which thereby may discourage lawsuits with respect to such claims.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
In February 2022, Plansee SE/Global Tungsten & Powders Corp. (“Plansee/GTP”), a former supplier, filed a request for expedited arbitration with the World Intellectual Property Organization Arbitration and Mediation Center in Geneva Switzerland (“WIPO”), for various claims allegedly in relation to an Intellectual Property and Confidential Disclosure Agreement between Plansee/GTP and Bloom Energy Corporation. Plansee/GTP’s statement of claims includes allegations of infringement of U.S. Patent Nos. 8,802,328, 8,753,785 and 9,434,003. On April 3, 2022, we filed a complaint against Plansee/GTP in the Eastern District of Texas to address the dispute between Plansee/GTP and Bloom Energy Corporation in a proper forum before a U.S. Federal District Court. Our complaint seeks the correction of inventorship of U.S. Patent Nos. 8,802,328, 8,753,785 and 9,434,003 (the “Patents-in-Suit”); declaratory judgment of invalidity, unenforceability, and non-infringement of the Patents-in-Suit; and declaratory judgment of no misappropriation. Further, our complaint seeks to recover damages we have suffered in relation to Plansee/GTP’s business dealings that, as alleged, constitute acts of unfair competition, tortious interference contract, breach of contract, violations of the Racketeer Influenced and Corrupt Organizations (RICO) Act and violations of the Clayton Antitrust Act. On June 9, 2022, Plansee/GTP filed a motion to dismiss the complaint filed in the Eastern District of Texas and compel arbitration (or alternatively to stay).…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001664703&type=8-K｜as_of：2026-10-25
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-25 至 2026-10-25 共 16 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 6 份。
2026-10-22 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-28 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-09 8-K Items 7.01 Regulation FD Disclosure
2026-06-22 8-K/A Items 5.02 Departure/Election of Directors or Officers
2026-06-17 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-05-27 8-K Items 5.03 Amendments to Articles or Bylaws；5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-04-28 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-27 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-13 8-K Items 1.01 Entry into a Material Definitive Agreement；3.02 Unregistered Sales of Equity Securities；9.01 Financial Statements and Exhibits
2026-03-26 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-23 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2025-11-04 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；3.02 Unregistered Sales of Equity Securities；8.01 Other Events；9.01 Financial Statements and Exhibits
2025-10-30 8-K Items 8.01 Other Events
2025-10-30 8-K Items 1.01 Entry into a Material Definitive Agreement；3.02 Unregistered Sales of Equity Securities
2025-10-28 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-04-13，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026024896/be-20260413.htm｜as_of：2026-04-13
<<<
Item 1.01. Entry into a Material Definitive Agreement.
Warrant
As previously disclosed in Bloom Energy Corporation’s (the “Company”) Current Report on Form 8-K filed on October 30, 2025, in connection with the partnership between the Company and Oracle Corporation (“Oracle”) to provide on-site solid state power for AI data centers, subject to the negotiation of a warrant mutually acceptable to the Company and Oracle, the Company agreed to issue to Oracle a warrant (the “Warrant”) to purchase up to an aggregate of 3,531,073 shares (the “Warrant Shares”) of Class A Common Stock, par value $0.0001 per share (the “Class A Common Stock”), of the Company, with an exercise price of $113.28 per share, the closing price of the Class A Common Stock on the New York Stock Exchange on October 28, 2025. On April 9, 2026, the Company issued the Warrant to Oracle. The Warrant is fully vested and immediately exercisable, in whole or in part, at any time until 5:00 p.m. (Eastern time) on October 9, 2026, at Oracle’s election, by cash payment or by cashless exercise. The Warrant includes customary anti-dilution adjustments and provides Oracle with certain registration rights with respect to the Warrant Shares. The Warrant may not be transferred or assigned without the prior written consent of the Company.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-12-23，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828025058618/be-20251219.htm｜as_of：2025-12-23
<<<
Item 1.01. Entry into a Material Definitive Agreement.
Credit Agreement
Parties
On December 19, 2025, Bloom Energy Corporation (the “Company”) entered into a Credit Agreement (the “Credit Agreement”) with Wells Fargo Bank, National Association, as administrative agent and collateral agent, the letter of credit issuer party thereto, and the financial institutions party thereto as lenders.
Borrowings
The Credit Agreement provides for a $600 million senior secured multicurrency revolving credit facility (the “revolving credit facility”). Borrowings under the revolving credit facility will be available in U.S. dollars, British pounds sterling, euros, Japanese yen, Singapore dollars, and other approved foreign currencies.
Use of Proceeds
Proceeds of borrowings under the revolving credit facility may be used to finance working capital, capital expenditures, and permitted acquisitions, and for other general corporate purposes.
Maturity Date
Subject to acceleration upon the occurrence of certain events (as described in the Credit Agreement), the revolving credit facility matures on December 19, 2030.
Interest Rate
Loans under the revolving credit facility bear interest, at the Company’s option, at an annual rate equal to Term SOFR plus an applicable margin ranging from 1.50% to 2.25% or an adjusted base rate plus an applicable margin ranging from 0.50% to 1.25%, based on the Company’s Total Leverage Ratio.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2025-11-04，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828025049016/be-20251030.htm｜as_of：2025-11-04
<<<
Item 1.01. Entry into a Material Definitive Agreement.
Indenture and Notes
On November 4, 2025, Bloom Energy Corporation (the “Company”) issued $2,500,000,000 aggregate principal amount of its 0% Convertible Senior Notes due 2030 (the “Notes”). The Notes were issued pursuant to, and are governed by, an indenture (the “Indenture”), dated as of November 4, 2025, between the Company and U.S. Bank Trust Company, National Association, as trustee (the “Trustee”). Pursuant to the purchase agreement among the Company and the representatives of the initial purchasers of the Notes, the Company granted the initial purchasers an option to purchase, for settlement within a period of 13 days from, and including, the date the Notes are first issued, up to an additional $300,000,000 principal amount of Notes. The Notes issued on November 4, 2025 include $300,000,000 principal amount of Notes issued pursuant to the full exercise by the initial purchasers of such option.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
