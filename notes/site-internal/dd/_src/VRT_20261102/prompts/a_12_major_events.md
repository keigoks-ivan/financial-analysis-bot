你是 stock-analyst v20 DD 的證據採集子 agent。標的：VRT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - VRT Vertiv Holdings Co acquisition merger 2025 2026
  - VRT Vertiv Holdings Co class action lawsuit securities fraud
  - VRT Vertiv Holdings Co clinical trial FDA approval 2025 2026
  - VRT Vertiv Holdings Co product launch recall warning letter
  - VRT Vertiv Holdings Co SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm｜as_of：2026-02-13
<<<
Item 3. Legal Proceedings
With the exception of the below, we are not a party to any material, pending legal proceedings or claims at December 31, 2025. From time-to-time, we may be a party to, or otherwise involved in, legal proceedings arising in the normal course of business. The nature of our business ordinarily results in a certain amount of pending as well as threatened claims, litigation, investigations, regulatory and legal and administrative cases, matters and proceedings, all of which are considered incidental to the normal conduct of business. When we determine that we have meritorious defenses to the claims asserted, we vigorously defend ourself. We consider settlement of cases when, in management’s judgment, it is in the best interests of both Vertiv and its shareholders to do so.
On May 3, 2022, a putative securities class action, In re Vertiv Holdings Co Securities Litigation, 22-cv-3572, was filed against Vertiv, certain of the Company’s officers and directors, and other defendants in the Southern District of New York. Plaintiffs filed an amended complaint on September 16, 2022. The amended complaint alleges that certain of the Company’s public statements were materially false and/or misleading with respect to inflationary and supply chain pressures and pricing issues, and asserts claims under Sections 10(b) and 20(a) of the Securities Exchange Act of 1934, as amended, and Sections 11, 12(a)(2), and 15 of the Securities Act of 1933, as amended. These claims are asserted on behalf of a putative class of all persons and entities that (i) purchased Vertiv securities between February 24, 2021 and February 22, 2022; and/or (ii) purchased Vertiv securities in or traceable to the November 4, 2021 secondary public offering by a selling stockholder pursuant to a resale registration statement. On January 31, 2024, the Court issued an order dismissing the claims under Sections 11, 12(a)(2), and 15 of the Securities Act. The motion to dismiss the claims under Sections 10(b) and 20(a) of the Exchange Act remains pending.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 3. Legal Proceedings（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm｜as_of：2026-02-13
<<<
On June 9, 2023, two Vertiv shareholders, Matthew Sullivan and Jose Karlo Ocampo Avenido, brought a derivative lawsuit, Sullivan v. Johnson, et al., C.A. No. 2023-0608 (the "Sullivan Action"), against Vertiv (as nominal defendant only) and certain of the Company’s directors and officers in Delaware Court of Chancery for breach of fiduciary duty. Further, on November 19, 2024, another Vertiv shareholder, Laura Hanna, brought a derivative lawsuit, Hanna v. Johnson, et al. (the "Hanna Action"), against Vertiv (as nominal defendant only) and certain of Company’s directors and officers in Delaware Court of Chancery for breach of fiduciary duty. The complaints allege that certain of the named directors and officers caused the Company to issue materially false and/or misleading public statements with respect to inflationary and supply chain pressures and pricing issues, and that the Company suffered damages as a result. The Sullivan Action has been stayed since August 10, 2023 pending the outcome of the motion to dismiss in the securities class action. On February 13, 2025, the Delaware Court of Chancery entered an order that (i) consolidated the Sullivan Action and Hanna Action into a single consolidated derivative lawsuit, In re Vertiv Holdings Co Stockholder Derivative Litigation, Consolidated C.A. No.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1674101/000167410126000008/vrt-20251231.htm｜as_of：2026-02-13
<<<
95 Table of contents On August 3, 2021, an American Arbitration Association arbitration hearing commenced with respect to a 2018 claim filed by Vertiv against SVO Building One, LLC (“SVO”) alleging damages of approximately $12.0 with respect to (i) unremitted payment for work and materials in connection with, the design, engineering, procurement, installation, construction, and commissioning of a data center located in Sacramento, California and (ii) damages and injunctive relief relating to SVO’s unauthorized use of Vertiv’s intellectual property and work product. SVO filed a counterclaim in 2018 alleging damages of approximately $18.0 relating to (i) allegations that Vertiv was not a duly licensed contractor at all times during the project in violation of California’s contractor license regulations, (ii) breach of warranty, and (iii) gross negligence. On September 3, 2021, the arbitrator issued an interim phase one ruling finding (1) that Vertiv was in violation of California contractor license regulations and was barred from recovery of approximately $9.0 for work performed and equipment delivered in connection with the project, as well as requiring disgorgement plus interest of $10.0, (2) SVO was not in violation of California’s contractor license regulations, and (3) Vertiv and SVO agreed to a traditional baseball arbitration provision under the terms and conditions for the project, wherein each party is required to submit a proposed final award…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001674101&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 20 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 8 份。
2026-10-28 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-10-27 8-K Items 2.01 Completion of Acquisition or Disposition of Assets；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-10-26 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-24 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-02 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-02 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-29 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-18 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-06-12 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-03 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-27 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-22 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-13 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-24 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-06 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-03-03 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-11 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-05 8-K Items 2.01 Completion of Acquisition or Disposition of Assets；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-14 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-03 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-10-27，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/1674101/000162828026067393/vrt-20261027.htm｜as_of：2026-10-27
<<<
Item 2.01 Completion of Acquisition or Disposition of Assets
On October 27, 2026 (the “Closing Date”) Vertiv Corporation, an Ohio corporation (“Buyer”) and subsidiary of Vertiv Holdings Co, a Delaware corporation (the “Company”) completed the acquisition (the “Acquisition”) of Utility Innovation Holdings, Inc., a Delaware corporation (“UIG”), pursuant to the merger of Vultra Merger Sub, Inc. (“Merger Sub”), a wholly-owned subsidiary of Buyer, with and into UIG, with UIG being the surviving corporation and becoming a wholly-owned subsidiary of Buyer following the merger. Total consideration paid by Buyer in the Acquisition was: (i) approximately $1.45 billion in upfront cash at closing, subject to customary adjustments for working capital, indebtedness and transaction expenses, plus (ii) additional potential cash consideration of up to $1.15 billion, payable in 2 tranches if earned, which potential additional consideration will be calculated based on the achievement of certain earnings before interest, depreciation, and amortization (EBITDA) targets of the acquired business, as set forth in the previously announced Agreement and Plan of Merger, dated as of September 1, 2026, by and between Buyer, Merger Sub and UIG (the “Merger Agreement”). UIG provides microgrid solutions, advanced power controls and behind-the-meter power architecture design for data centers.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-12-05，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/1674101/000167410125000031/vrt-20251204.htm｜as_of：2025-12-05
<<<
Item 2.01 Completion of Acquisition or Disposition of Assets
On December 4, 2025 (the “Closing Date”) Vertiv Corporation, an Ohio corporation (“Buyer”) and subsidiary of Vertiv Holdings Co, a Delaware corporation (the “Company”) completed the acquisition (the “Acquisition”) of all of the outstanding interests in Purge Rite Intermediate, LLC, a Delaware limited liability company (“PurgeRite”), for approximately $1.0 billion in upfront cash consideration, subject to customary adjustments for target working capital, indebtedness and expenses, plus additional potential cash consideration of up to $250 million in cash, which additional consideration shall be calculated based on post-closing performance metrics of the acquired business, pursuant to the terms and conditions of that previously announced Securities Purchase Agreement, dated as of October 31, 2025, by and between Buyer, the Company, Purge Rite and Purge Rite Holdings, LLC, a Delaware limited liability company (the “Acquisition Agreement”). PurgeRite provides mechanical flushing, purging and filtration services for data centers and other facilities.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VRT_20261102/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
