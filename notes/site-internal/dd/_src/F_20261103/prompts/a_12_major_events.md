你是 stock-analyst v20 DD 的證據採集子 agent。標的：F。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - F Ford Motor acquisition merger 2025 2026
  - F Ford Motor class action lawsuit securities fraud
  - F Ford Motor clinical trial FDA approval 2025 2026
  - F Ford Motor product launch recall warning letter
  - F Ford Motor SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
ITEM 3. Legal Proceedings.
The litigation process is subject to many uncertainties, and the outcome of individual matters is not predictable with assurance. See Note 24 of the Notes to the Financial Statements for a discussion of loss contingencies. Following is a discussion of our significant pending legal proceedings:
PRODUCT LIABILITY MATTERS
We are a defendant in numerous actions in state and federal courts within and outside of the United States alleging damages from injuries resulting from (or aggravated by) alleged defects in our vehicles. In many actions, no monetary amount of damages is specified or the specific amount alleged is the jurisdictional minimum. Our experience with litigation alleging a specific amount of damages suggests that such amounts, on average, bear little relation to the actual amount of damages, if any, that we will pay in resolving such matters.
In addition to pending actions, we assess the likelihood of incidents that likely have occurred but not yet been reported to us. We also take into consideration specific matters that have been raised as claims but have not yet proceeded to litigation. Individual product liability matters that have more than a remote risk of loss and such loss would likely be significant if the matter is resolved unfavorably to us would be described herein. Currently, there is one such matter to report:
Hetsler v. Ford. Plaintiff, Robert Hetsler, filed this product liability action against Ford in the Circuit Court of the Fourth Judicial Circuit in and for Duval County, Florida on April 24, 2020 alleging that a 2016 Roush Mustang had a manufacturing defect in an unidentified component of the engine compartment that resulted in a fire. After a trial in February 2024, a jury found Ford liable and awarded plaintiff $103 million in damages. On August 22, 2024, Ford appealed the judgment to the Fifth District Court of Appeal. Ford believes a new trial is warranted based on the trial court’s improper instructions to the jury and the trial court’s improper admission of undisclosed expert opinions.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
Item 1. Business (Continued) Regulators around the world continue to scrutinize automakers’ emission testing, which has led to a number of defeat device settlements by various manufacturers. EPA is carrying out additional non-standard tests as part of its vehicle certification program. CARB has also been conducting extensive non-standard emission tests, which in some cases have resulted in certification delays for diesel vehicles. In the past, several European countries have conducted non-standard emission tests and published the results, and, in some cases, this supplemental testing has triggered investigations of manufacturers for possible defeat devices. Testing is expected to continue on an ongoing basis, with new testing methods continually under development. In addition, plaintiffs’ attorneys are pursuing consumer class action lawsuits based on alleged excessive emissions from cars and trucks, which could, in turn, prompt further investigations by regulators.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
Moreover, compliance with governmental standards does not necessarily prevent individual or class action lawsuits, which can entail significant cost and risk, in addition to defending litigation and claims concerning instances of alleged non-compliance. In certain circumstances, courts may permit civil actions even where our products, services, and financial products comply with federal and/or other applicable law. Furthermore, simply responding to actual or threatened litigation, government investigations, subpoenas, or information requests concerning our compliance with regulatory standards, whether related to our products, services, or business or commercial relationships, requires significant expenditures of time and other resources and may be disruptive to our operations. Litigation also is inherently uncertain, and we have in the past experienced, and could in the future experience, significant adverse results, including compensatory and punitive damage awards, a disgorgement of profits or revenue, or injunctive relief, any of which could have an adverse effect on our financial condition, results of operations, or our business in general, particularly with larger jury verdicts becoming more prevalent. We may decide to settle a matter in anticipation of or during litigation, which may require a monetary or non-monetary payment, a change to our business practices (e.g., to undertake or cease a particular activity), or other remedies. However, a settlement on acceptable terms may not always be feasible.…
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
102 Designation Description Method of Filing Exhibit 10-W-4 Eleventh Amendment dated as of April 30, 2015 to our Credit Agreement dated as of December 15, 2006, as amended and restated as of November 24, 2009, as amended and restated as of April 30, 2014, and as further amended, including the Third Amended and Restated Credit Agreement. (d) Filed as Exhibit 10.1 to our Current Report on Form 8-K filed May 1, 2015. (a)
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000037996&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 17 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 8 份。
2026-10-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-02 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-02 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-21 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-19 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-04-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-15 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-15 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-04-02 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-03-13 8-K Items 8.01 Other Events
2026-02-10 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 7.01 Regulation FD Disclosure
2026-01-06 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2025-12-15 8-K Items 2.06 Material Impairments；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-12 8-K Items 5.02 Departure/Election of Directors or Officers；5.03 Amendments to Articles or Bylaws；9.01 Financial Statements and Exhibits
2025-11-21 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-12-15，Item 2.06）｜章節：8-K Item 2.06 Material Impairments｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799625000238/f-20251209.htm｜as_of：2025-12-15
<<<
Item 2.06. Material Impairments.
As previously disclosed, although we are investing in our electric vehicle (“EV”) strategy, we anticipate that the market for EVs will continue to be challenging. As a result, we are taking several actions to adjust our business strategy, which impact our EV manufacturing capacity and product roadmap.
BlueOval SK, LLC
On December 9, 2025, Ford Motor Company (“Ford”), SK On Co., Ltd. (“SK On”), SK Battery America, Inc. (“SKBA,” a wholly owned subsidiary of SK On), and BlueOval SK, LLC (“BOSK”), a joint venture company formed by Ford, SK On, and SKBA to build and operate an EV battery plant in Tennessee and two EV battery plants in Kentucky, entered into a Joint Venture Disposition Agreement. Pursuant to the Joint Venture Disposition Agreement, Ford’s membership interest in BOSK will be redeemed and a Ford subsidiary will acquire the two BOSK plants and related equipment in Kentucky. Closing on the transactions contemplated by the Joint Venture Disposition Agreement is expected in the first half of 2026.
As a result of Ford’s entry into the Joint Venture Disposition Agreement, on December 9, 2025, we concluded that we will recognize a charge related to our share of BOSK’s long-lived asset impairment and the impairment of our remaining investment in BOSK.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-21，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000093/f-20260520.htm｜as_of：2026-05-21
<<<
Item 1.01. Entry into a Material Definitive Agreement.
Item 2.03. Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant.
Item 8.01. Other Events.
As previously disclosed, on December 13, 2024, BlueOval SK, LLC (“BOSK”), a joint venture company formed by Ford Motor Company (“Ford” or “Company”), SK On Co., Ltd. (“SK On”), and SK Battery America, Inc. (“SKBA,” a wholly owned subsidiary of SK On) to build and operate an EV battery plant in Tennessee and two EV battery plants in Kentucky, entered into a Loan Arrangement and Reimbursement Agreement (the “BOSK DOE Loan Agreement”) pursuant to which the U.S. Department of Energy (“DOE”) agreed to arrange for the Federal Financing Bank to purchase a note or notes from BOSK and to make advances from time to time thereunder up to $9,633,040,000 (the “BOSK DOE Loan”) to finance the construction of battery manufacturing plants in Tennessee and Kentucky. Advances totaling $7,835,540,000 were subsequently made to BOSK.
In conjunction with the BOSK DOE Loan Agreement, on December 13, 2024, each of Ford, SK On, SKBA, and SK Innovation Co., Ltd., entered into a Sponsor Support, Share Retention and Subordination Agreement (the “SSA”) with BOSK and DOE.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
