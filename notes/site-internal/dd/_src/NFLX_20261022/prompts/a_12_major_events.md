你是 stock-analyst v20 DD 的證據採集子 agent。標的：NFLX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - NFLX Netflix acquisition merger 2025 2026
  - NFLX Netflix class action lawsuit securities fraud
  - NFLX Netflix clinical trial FDA approval 2025 2026
  - NFLX Netflix product launch recall warning letter
  - NFLX Netflix SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-23）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm｜as_of：2026-01-23
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-23）｜章節：Item 7. MD&A（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm｜as_of：2026-01-23
<<<
26 Table of Contents Other Planned Uses of Cash and Debt Capital On December 4, 2025, we entered into a definitive agreement and plan of merger with WBD to acquire WBD's streaming and studios businesses, including its film and television studios, HBO Max and HBO, which was amended and restated by the parties thereto on January 19, 2026 (as so amended and restated, the “Amended and Restated Merger Agreement”). WBD is a leading global media and entertainment company and will separate its Global Linear Networks business, Discovery Global, into a new publicly-traded company prior to the closing of the WBD transaction. Under the terms of the Amended and Restated Merger Agreement, each WBD stockholder will receive $27.75 in cash (as may be adjusted in accordance with the terms of the Amended and Restated Merger Agreement) for each share of WBD common stock outstanding as of immediately prior to the closing of the WBD transaction, for a total equity value of approximately $72.0 billion and an enterprise value of approximately $82.7 billion (in each case, as of December 4, 2025). The total equity value and enterprise value of the WBD transaction may fluctuate based on WBD's capitalization as of the closing of the WBD transaction.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-23）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm｜as_of：2026-01-23
<<<
59 Table of Contents Acquisitions On December 4, 2025, the Company entered into a definitive agreement and plan of merger with WBD to acquire WBD's streaming and studios businesses, including its film and television studios, HBO Max and HBO, which was then amended by the parties thereto on January 19, 2026, by the Amended and Restated Merger Agreement. Under the terms of the Amended and Restated Merger Agreement, each WBD stockholder will receive $27.75 in cash (as may be adjusted in accordance with the terms of the Amended and Restated Merger Agreement) for each share of WBD common stock outstanding as of immediately prior to the closing of the WBD transaction, for a total equity value of approximately $72.0 billion and an enterprise value of approximately $82.7 billion (in each case, as of December 4, 2025). The total equity value and enterprise value of the WBD transaction may fluctuate based on WBD's capitalization as of the closing of the WBD transaction. The Company expects the WBD transaction to close in 12-18 months from December 4, 2025, subject to receipt of required regulatory approvals, approval of WBD stockholders, the consummation of the separation and distribution of Discovery Global and other customary closing conditions.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001065280&type=8-K｜as_of：2026-10-22
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 16 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 8 份。
2026-10-20 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 5.02 Departure/Election of Directors or Officers
2026-07-22 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-16 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-05 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；8.01 Other Events
2026-04-23 8-K Items 8.01 Other Events
2026-04-16 8-K Items 2.02 Results of Operations and Financial Condition；5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-27 8-K Items 1.02 Termination of a Material Definitive Agreement
2026-01-20 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-20 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-22 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2025-12-05 8-K/A Items 9.01 Financial Statements and Exhibits
2025-12-05 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-14 8-K Items 5.03 Amendments to Articles or Bylaws；9.01 Financial Statements and Exhibits
2025-11-04 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2025-10-30 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-01-20，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1065280/000119312526015951/d37713d8k.htm｜as_of：2026-01-20
<<<
Item 1.01
Entry into a Material Definitive Agreement.
Amended and Restated Agreement and Plan of Merger
On January 19, 2026, Netflix, Inc., a Delaware corporation (“Netflix”), Nightingale Sub, Inc., a Delaware corporation and wholly owned subsidiary of Netflix (“Merger Sub”), Warner Bros. Discovery, Inc., a Delaware corporation (“WBD”), and New Topco 25, Inc., a newly formed Delaware corporation and wholly owned subsidiary of WBD (“Newco”), entered into an Amended and Restated Agreement and Plan of Merger (the “Amended and Restated Merger Agreement”), which amends and restates in its entirety the Agreement and Plan of Merger, dated as of December 4, 2025, by and among Netflix, Merger Sub, WBD and Newco (the “Original Merger Agreement”). Pursuant to the Amended and Restated Merger Agreement, Netflix and WBD have agreed to revise the structure of their previously announced transaction to provide that the $27.75 per share merger consideration to be paid to WBD stockholders in the Merger (as defined below) will be paid entirely in cash, instead of a combination of cash and shares of Netflix common stock, subject to the terms and conditions of the Amended and Restated Merger Agreement.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-12-22，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1065280/000119312525327462/d82688d8k.htm｜as_of：2025-12-22
<<<
Item 1.01
Entry into a Material Definitive Agreement.
On December 19, 2025, Netflix, Inc. (“Netflix”) successfully replaced a portion of the commitments under its previously disclosed bridge commitment letter with a more permanent and cost effective funding structure, as further described below.
Revolving Credit Agreement
On December 19, 2025, Netflix entered into a Senior Unsecured Revolving Credit Agreement (the “Revolving Credit Agreement”) with the lenders party thereto and Wells Fargo Bank, National Association, as the administrative agent. The Revolving Credit Agreement provides for a $5,000,000,000 unsecured revolving credit facility. Netflix may use the proceeds of borrowings under the Revolving Credit Agreement (i) to pay the cash portion of the purchase price required under the Agreement and Plan of Merger (the “Merger Agreement”), dated as of December 4, 2025, by and among Netflix, Nightingale Sub, Inc., a Delaware corporation and wholly owned subsidiary of Netflix, Warner Bros. Discovery, Inc., a Delaware corporation (“WBD”), and New Topco 25, Inc., a newly formed Delaware corporation and wholly owned subsidiary of WBD, (ii) to pay certain fees, costs and expenses incurred in connection with the transactions contemplated by the Merger Agreement and the incurrence by Netflix of indebtedness to finance such transactions and (iii) at the option of Netflix, to refinance certain indebtedness.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2025-12-05，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1065280/000119312525308651/d65144d8k.htm｜as_of：2025-12-05
<<<
Item 1.01 Entry into a Material Definitive Agreement.
Agreement and Plan of Merger
On December 4, 2025, Netflix, Inc., a Delaware corporation (“Netflix”), Nightingale Sub, Inc., a Delaware corporation and wholly owned subsidiary of Netflix (“Merger Sub”), Warner Bros. Discovery, Inc., a Delaware corporation (“WBD”), and New Topco 25, Inc., a newly formed Delaware corporation and wholly owned subsidiary of WBD (“Newco”), entered into an Agreement and Plan of Merger (the “Merger Agreement”), pursuant to which, subject to the terms of the Merger Agreement, among other things, (i) a newly formed Delaware corporation and wholly owned subsidiary of Newco will merge with and into WBD (the “Holdco Merger”) in accordance with Section 251(g) of the General Corporation Law of the State of Delaware, with WBD surviving as a wholly owned subsidiary of Newco and with the stockholders of WBD immediately prior to the effective time of the Holdco Merger becoming the stockholders of Newco at and immediately following the effective time of the Holdco Merger, and (ii) following an internal reorganization and the separation and distribution of WBD’s Global Linear Networks business and certain other assets as further described below, as a result of which WBD will hold the Streaming & Studios businesses of WBD (the “Retained Business”), Merger Sub will merge with and into WBD, with WBD surviving as…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
