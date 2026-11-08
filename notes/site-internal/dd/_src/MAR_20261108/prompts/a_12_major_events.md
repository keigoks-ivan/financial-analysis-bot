你是 stock-analyst v20 DD 的證據採集子 agent。標的：MAR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - MAR Marriott International acquisition merger 2025 2026
  - MAR Marriott International class action lawsuit securities fraud
  - MAR Marriott International clinical trial FDA approval 2025 2026
  - MAR Marriott International product launch recall warning letter
  - MAR Marriott International SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm｜as_of：2026-02-10
<<<
Item 3. Legal Proceedings.
See the information under the “Litigation, Claims, and Government Investigations” caption in Note 7, which we incorporate here by reference. Within this section, we use a threshold of $1 million in disclosing material environmental proceedings involving a governmental authority, if any.
Table of Contents
In the 2025 second quarter, we received a letter from the U.S. Environmental Protection Agency (the “EPA”) offering to engage in settlement discussions in relation to violations of the Clean Air Act that the EPA alleges occurred at a hotel we manage. We do not believe this matter will have a material adverse effect on our business, financial condition, results of operations, or cash flows.
From time to time, we are also subject to other legal proceedings and claims, including adjustments proposed during governmental examinations of the various tax returns we file. While management presently believes that the ultimate outcome of these other proceedings, individually and in aggregate, will not materially harm our business, financial condition, cash flows, or overall trends in results of operations, legal proceedings are inherently uncertain, and unfavorable rulings could, individually or in aggregate, have a material adverse effect on our business, financial condition, operating results, or cash flows.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm｜as_of：2026-02-10
<<<
The Data Security Incident, and other information security incidents, could have numerous adverse effects on our business. As a result of the data security incident involving unauthorized access to the Starwood Hotels & Resorts Worldwide, LLC, formerly known as Starwood Hotels & Resorts Worldwide, Inc. (“Starwood”), reservations database that we disclosed in November 2018 (the “Data Security Incident”), numerous lawsuits and investigations were filed or initiated against us, as described further in Note 7, and we may become subject to additional actions related to the Data Security Incident. Responding to and resolving these lawsuits, claims, and/or investigations has resulted in payments and other expenses, and could result in material additional payments or remedial or other expenses. In 2024, we reached final resolutions with the U.S. Federal Trade Commission (“FTC”) and the Attorney General offices from 49 U.S. states and the District of Columbia (the “AG Offices”) in relation to the Data Security Incident, which include, among other terms, various long-term requirements relating to our data privacy and information security programs.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm｜as_of：2026-02-10
<<<
Litigation, Claims, and Government Investigations Following our announcement of the Data Security Incident, approximately 100 lawsuits were filed by consumers and others against us in U.S. federal, U.S. state and Canadian courts related to the incident. The plaintiffs in these cases, who generally purport to represent various classes of consumers, generally claim to have been harmed by alleged actions and/or omissions by the Company in connection with the Data Security Incident and assert a variety of common law and statutory claims seeking monetary damages, injunctive relief, costs and attorneys’ fees, and other related relief. The U.S. cases were consolidated in the U.S. District Court for the District of Maryland (the “District Court”), pursuant to orders of the U.S. Judicial Panel on Multidistrict Litigation (the “MDL”). On June 3, 2025, the U.S. Court of Appeals for the Fourth Circuit reversed the District Court’s certification of a class of consumer plaintiffs, holding that a class-action waiver signed by putative class members was enforceable. Following the Fourth Circuit’s reversal of class certification, some plaintiffs filed lawsuits in New York state court on an individual basis, alleging violations of New York statutory law and seeking monetary damages, attorneys’ fees, and other related relief. We have been engaged in mediation discussions with the consumer plaintiffs in the MDL.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001048286&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-11-02 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-09-24 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-08-13 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-03 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-13 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-20 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-10 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-06 8-K Items 5.02 Departure/Election of Directors or Officers
2026-01-09 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-24，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1048286/000119312526401051/d145370d8k.htm｜as_of：2026-09-24
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On September 23, 2026, Marriott International, Inc. (“Marriott” or the “Company”) entered into the Seventh Amended and Restated Credit Agreement with Bank of America, N.A., as administrative agent and certain banks (the “Amended Agreement”). The Amended Agreement amends and restates Marriott’s $4.50 billion multicurrency revolving credit agreement, dated as of December 14, 2022 (filed as Exhibit 10 to the Company’s Form 8-K filed on December 15, 2022) (as amended by the First Amendment to Credit Agreement, dated as of May 17, 2024, the “Prior Agreement”).
The Amended Agreement increases the aggregate commitments under the Prior Agreement from $4.50 billion to $5.00 billion and increases the maximum aggregate commitments permitted upon exercise of the commitment increase option from $5.00 billion to $5.50 billion.
The Amended Agreement extends the maturity date of the Prior Agreement from December 14, 2027 to September 23, 2031.
The Amended Agreement adjusts the interest rate margins and facility fees, adjusts the calculation of “EBITDA”, provides for the ability to amend the Amended Agreement to adjust interest rates and fees based on to-be-agreed upon environmental key performance indicators, and adjusts certain other provisions to reflect current documentation standards and other agreed modifications.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-08-13，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1048286/000119312526349395/d162127d8k.htm｜as_of：2026-08-13
<<<
Item 8.01.
Other Events.
On August 11, 2026, Marriott International, Inc. (“we”) entered into a Terms Agreement with J.P. Morgan Securities LLC, PNC Capital Markets LLC, Truist Securities, Inc., U.S. Bancorp Investments, Inc. and the other Underwriters listed on Schedule I thereto (the “Terms Agreement,” which incorporates by reference the Underwriting Agreement General Terms and Provisions, dated March 3, 2021 (which we previously filed on March 5, 2021 as Exhibit 1.1 to our Current Report on Form 8-K)) to issue $250,000,000 aggregate principal amount of our 4.875% Series NN Notes due 2029 (the “Series NN Notes”) and $1,000,000,000 aggregate principal amount of our 5.650% Series YY Notes due 2036 (the “Series YY Notes” and, together with the Series NN Notes, the “Notes”). We issued the Notes on August 13, 2026. The Series NN Notes issued pursuant to the Terms Agreement (the “New Series NN Notes”) constitute an additional issuance of, and a single series (the “Series NN”) with, the $500 million aggregate principal amount of 4.875% Series NN Notes due 2029 which we issued on February 22, 2024.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-02-20，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1048286/000119312526061350/d109911d8k.htm｜as_of：2026-02-20
<<<
Item 8.01.
Other Events.
On February 18, 2026, Marriott International, Inc. (“we”) entered into a Terms Agreement with Deutsche Bank Securities Inc., Citigroup Global Markets Inc., Fifth Third Securities, Inc., Goldman Sachs & Co. LLC and the other Underwriters listed on Schedule I thereto (the “Terms Agreement,” which incorporates by reference the Underwriting Agreement General Terms and Provisions, dated March 3, 2021 (which we previously filed on March 5, 2021 as Exhibit 1.1 to our Current Report on Form 8-K)) to issue $600,000,000 aggregate principal amount of our 4.500% Series WW Notes due 2033 (the “Series WW Notes”) and $850,000,000 aggregate principal amount of our 5.100% Series XX Notes due 2038 (the “Series XX Notes” and, together with the Series WW Notes, the “Notes”). We issued the Notes on February 20, 2026. Net proceeds of the offering are approximately $1.425 billion, after deducting the underwriting discount and estimated expenses of the offering. We intend to use the net proceeds from the offering of the Notes for general corporate purposes, which may include working capital, capital expenditures, acquisitions, stock repurchases or repayment of outstanding indebtedness.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MAR_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
