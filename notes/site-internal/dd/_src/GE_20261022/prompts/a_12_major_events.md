你是 stock-analyst v20 DD 的證據採集子 agent。標的：GE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - GE GE Aerospace acquisition merger 2025 2026
  - GE GE Aerospace class action lawsuit securities fraud
  - GE GE Aerospace clinical trial FDA approval 2025 2026
  - GE GE Aerospace product launch recall warning letter
  - GE GE Aerospace SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/40545/000004054526000008/ge-20251231.htm｜as_of：2026-01-29
<<<
Item 3. Legal Proceedings 70-71
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/40545/000004054526000008/ge-20251231.htm｜as_of：2026-01-29
<<<
(b) Restructuring and other cash expenditures were primarily related to employee severance payments. Additionally, included $363 million for the final settlement payment for the Sjunde AP-Fonden shareholder lawsuit for the year ended December 31, 2024. See Note 24 for further information.

Other changes 3 (1) — Balance at December 31 595 $ 592 $ 639 LEGAL MATTERS. In the normal course of our business, we are involved from time to time in various arbitrations, class actions, commercial litigation, investigations and other legal, regulatory or governmental actions, including the significant matters described below that could have a material impact on our results of operations. In many proceedings, including the specific matters described below, it is inherently difficult to determine whether any loss is probable or even reasonably possible or to estimate the size or range of the possible loss, and accruals for legal matters are not recorded until a loss for a particular matter is considered probable and reasonably estimable. Given the nature of legal matters and the complexities involved, it is often difficult to predict and determine a meaningful estimate of loss or range of loss until we know, among other factors, the particular claims involved, the likelihood of success of our defenses to those claims, the damages or other relief sought, how discovery or other procedural considerations will affect the outcome, the settlement posture of other parties and other factors that may have a material effect on the outcome. For these matters, unless otherwise specified, we do not believe it is possible to provide a meaningful estimate of loss at this time.…

Shareholder and related lawsuits. Since February 2018, multiple shareholder derivative lawsuits were filed against current and former GE executive officers and members of GE’s Board of Directors and GE (as nominal defendant). These lawsuits have alleged violations of securities laws, breaches of fiduciary duties, unjust enrichment, waste of corporate assets, abuse of control and gross mismanagement, although the specific matters underlying the allegations in the lawsuits have varied. Two shareholder derivative lawsuits are currently pending: the Lindsey and Priest/Tola cases, which were filed in New York state court. The allegations in these two cases relate to substantially the same facts as those underlying the Sjunde AP-Fonden case, which settled in April 2025. The plaintiffs seek unspecified damages and improvements in GE’s corporate governance and internal procedures. The Lindsey case has been stayed by agreement of the parties, and GE filed a motion to dismiss the Priest/Tola complaint in March 2021. In August 2024, the plaintiffs in the Priest/Tola case filed an amended consolidated complaint asserting substantially the same claims as in the prior derivative actions, and the Company filed a motion to dismiss this amended complaint in October 2024.
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000040545&type=8-K｜as_of：2026-10-22
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。
2026-10-20 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-09-22 8-K Items 5.02 Departure/Election of Directors or Officers；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-08 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-16 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-25 8-K Items 5.03 Amendments to Articles or Bylaws；9.01 Financial Statements and Exhibits
2026-06-11 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-05-07 8-K Items 5.02 Departure/Election of Directors or Officers；5.07 Submission of Matters to a Vote of Security Holders
2026-04-21 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-22 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-15 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-09-22，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/40545/000004054526000059/ge-20260921.htm｜as_of：2026-09-22
<<<
Item 8.01 Other Events.
On September 21, 2026, the independent directors of the Board appointed Wesley Bush to be the independent Lead Director, effective as of that date. A copy of the press release announcing Mr. Bush’s appointment as independent Lead Director is attached as Exhibit 99.1 and incorporated herein by reference.
Item 9.01 Financial Statements and Exhibits.
(d) Exhibits
Exhibit Description
99.1
Press release, dated September 22, 2026, issued by GE Aerospace.
104 The cover page of this Current Report on Form 8-K formatted as Inline XBRL.
2
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-08，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/40545/000095014226002501/eh260827362_8k.htm｜as_of：2026-09-08
<<<
Item 8.01, General
Electric Company, operating as GE Aerospace (the “Company”), posted an investor presentation to its investor website. Copies
of the investor presentation and related press release are furnished as Exhibits 99.1 and 99.2, respectively.
The information provided pursuant to this Item 7.01, including Exhibits
99.1 and 99.2, are being furnished and shall not be deemed "filed" for purposes of Section 18 of the Securities Exchange Act
of 1934 (the "Exchange Act") or otherwise subject to the liabilities under that Section and shall not be deemed to be incorporated
by reference into any filing of the Company under the Securities Act of 1933 or the Exchange Act.
Item 8.01 Other Events.
On September 8, 2026, the Company issued a press release announcing the
entry into an agreement to acquire Consolidated Precision Products (“CPP”), a leading manufacturer of highly engineered castings,
for a cash purchase price of $11.75 billion, subject to closing adjustments. The transaction is expected to close in the second half of
2027 and is subject to regulatory approvals and other customary closing conditions.
Item 9.01 Financial Statements and Exhibits.
(d) Exhibits
Exhibits 99.1 and 99.2 are being furnished as part of this report.
Exhibit
Description
99.1
Investor presentation, dated September 8, 2026, issued by GE Aerospace.
99.2…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
