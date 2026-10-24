你是 stock-analyst v20 DD 的證據採集子 agent。標的：CRS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - CRS Carpenter Technology acquisition merger 2025 2026
  - CRS Carpenter Technology class action lawsuit securities fraud
  - CRS Carpenter Technology clinical trial FDA approval 2025 2026
  - CRS Carpenter Technology product launch recall warning letter
  - CRS Carpenter Technology SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-12）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm｜as_of：2026-08-12
<<<
Item 3. Legal Proceedings
From time to time, we are a party to lawsuits and other proceedings involving alleged violations of, or liabilities arising from, environmental laws. We have environmental remediation liabilities at some of our owned operating facilities and have been designated as a PRP with respect to certain third party Superfund or similar waste disposal sites and other third party owned sites. Additionally, we have been notified that we may be a PRP with respect to other Superfund sites as to which no proceedings have been instituted against us. Estimates of the amount and timing of future costs of environmental remediation requirements are inherently imprecise because of the continuing evolution of environmental laws and regulatory requirements, the availability and application of technology, the identification of currently unknown remediation sites and the allocation of costs among the PRPs. Based upon information currently available, such future costs are not expected to have a material effect on our financial position, results of operations or cash flows over the long-term. However, such costs could be material to our financial position, results of operations or cash flows in a particular future quarter or year.
In addition, from time to time, we are a party to certain routine claims and legal actions and other contingent liabilities incident to the normal course of business which pertain to litigation, product claims, commercial disputes, employment actions, employee benefits, compliance with domestic and foreign laws and regulations, personal injury claims, patent infringement and tax issues. Based on information currently available, the ultimate resolution of our known contingencies, individually or in the aggregate and including the matters described in Note 12 to the consolidated financial statements in this Form 10-K, is not expected to have a material adverse effect on our financial position, cash flows or results of operations. However, there can be no assurance that an increase in the scope of pending matters or that any future lawsuits, claims, proceedings or investigations will not be material to our financial position, results of operations or cash flows in a particular future quarter or year.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-12）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm｜as_of：2026-08-12
<<<
Litigation claims relate to the conduct of our currently and formerly owned businesses, including claims pertaining to product liability, commercial disputes, employment actions, employee benefits, compliance with domestic and international laws and regulations, personal injury, patent infringement and tax issues. Due to the uncertainties of litigation, we can give no assurance that we will prevail on claims made against us in the lawsuits that we currently face or that additional claims will not be made against us in the future. The outcome of litigation cannot be predicted with certainty, and some of these lawsuits, claims or proceedings may be determined adversely to us. The resolution in any reporting period of one or more of these matters could have a material adverse effect on our results of operations for that period. We can give no assurance that any other matters brought in the future will not have a material adverse effect on our results of operations, financial condition and cash flows.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-12）｜章節：Item 7. MD&A（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm｜as_of：2026-08-12
<<<
35 Table of Contents On November 20, 2025, we entered into a Third Amended and Restated Credit Agreement with Bank of America, N.A., as administrative agent, swing line lender and letter of credit issuer and the other lenders, agents and arrangers party thereto (the "Credit Facility"). The Credit Facility amended and restated our then existing Second Amended and Restated Credit Agreement dated as of April 14, 2023, which had been set to expire on April 12, 2028. The Third Amendment extends the maturity to November 20, 2030.

Other We are defending various routine claims and legal actions that are incidental to our business, and that are common to our operations, including those pertaining to product claims, commercial disputes, patent infringement, employment actions, employee benefits, compliance with domestic and foreign laws and regulations, personal injury claims and tax issues. Like many other manufacturing companies in recent years we, from time to time, have been named as a defendant in lawsuits alleging personal injury as a result of exposure to chemicals and substances in the workplace such as asbestos. We provide for costs relating to these matters when a loss is probable and the amount of the loss is reasonably estimable. The effect of the outcome of these matters on our future results of operations and liquidity cannot be predicted because any such effect depends on future results of operations and the amount and timing (both as to recording future charges to operations and cash expenditures) of the resolution of such matters. While it is not feasible to determine the outcome of these matters, we believe that the total liability from these matters will not have a material effect on our financial position, results of operations or cash flows over the long-term.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000017843&type=8-K｜as_of：2026-10-25
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-25 至 2026-10-25 共 18 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。
2026-10-22 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-22 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-15 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-10-08 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-08-25 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-12 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-28 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-17 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-17 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-11-20 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-10 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-10 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2025-11-20，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/17843/000110465925114628/tm2531768d1_8k.htm｜as_of：2025-11-20
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On November 20, 2025,
Carpenter Technology Corporation (the “Company”) completed its previously announced offer and sale of $700.0 million aggregate
principal amount of 5.625% senior notes due 2034 (the “Notes”).
Indenture
The Notes were issued pursuant
to an indenture, dated as of November 20, 2025 (the “Indenture”), among the Company and U.S. Bank Trust Company, National
Association, as trustee (in such capacity, the “Trustee”), which includes a form of Note.
The Notes will pay interest
semiannually on March 1 and September 1, commencing on March 1, 2026, at an annual rate of 5.625%, and will mature on March 1,
2034, unless earlier repurchased or redeemed.
Prior to March 1, 2029,
the Company may, at its option, redeem some or all of the Notes at any time, at a price equal to 100% of the principal amount of the Notes
redeemed plus a “make-whole” premium, plus accrued and unpaid interest, if any. The Company may also redeem, at its option,
up to 40% of the Notes at any time prior to March 1, 2029, using the proceeds of certain equity offerings at a redemption price of
105.625% of the principal amount thereof, plus accrued and unpaid interest, if any. On or after March 1, 2029, the Company may, at…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
