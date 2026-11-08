你是 stock-analyst v20 DD 的證據採集子 agent。標的：TLN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - TLN Talen Energy acquisition merger 2025 2026
  - TLN Talen Energy class action lawsuit securities fraud
  - TLN Talen Energy clinical trial FDA approval 2025 2026
  - TLN Talen Energy product launch recall warning letter
  - TLN Talen Energy SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm｜as_of：2026-02-26
<<<
ITEM 3. LEGAL PROCEEDINGS
Susquehanna ISA Amendment. As previously disclosed, in November 2024, the FERC issued an order denying an Amended Interconnection Service Agreement (the “ISA Amendment”) between PJM, a subsidiary of PPL Corporation, and Susquehanna that would have permitted Susquehanna to decrease by up to 480 MW the amount of power it would have otherwise supplied to the grid and instead supply that power directly to AWS in a co-located “behind-the-meter” arrangement. Talen promptly filed a motion for rehearing of the denial and the FERC subsequently stated, in an order issued in December 2024 and reaffirmed in April 2025, that it would address our request for rehearing in a future order. We subsequently filed an appeal in the U.S. Court of Appeals for the Fifth Circuit, which was transferred to the Third Circuit in November 2025.
Meanwhile, in June 2025, we entered into an amended AWS PPA to, among other things, transition to a “front-of-the-meter” arrangement with AWS. See “—Our Key Markets and Revenue Streams—Contracted Revenues—AWS PPA” for additional information. Following this revision, the load that was previously behind-the-meter was moved into PJM’s load forecast and, as a result, in October 2025, PJM filed a waiver request at the FERC to restore 148 MW of capacity interconnection rights (“CIRs”) to Susquehanna and add the corresponding generation back into the capacity auction. The FERC approved the request and the additional CIRs were available for the 2027/2028 BRA in December 2025 and should continue to be available for future auctions. In January 2026, following approval of the CIR waiver request, the ISA Amendment appeal was voluntarily dismissed by Talen. This matter is now closed.
FERC Co-Location Proceedings. Several consolidation matters before the FERC are likely to shape FERC and PJM policy around co-located load. In August 2024, Exelon sought to amend portions of the PJM tariff to clarify that co-located load arrangements must be categorized as either network load or point-to-point service (the “Exelon 205 Proceeding”), making them subject to the same transmission charges and fees for transmission-related services as grid-connected load pays.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1622536/000162253626000017/tln-20251231.htm｜as_of：2026-02-26
<<<
ERCOT Weather Event (Winter Storm Uri) Lawsuits. In connection with the ERCOT Sale, the Company retained certain potential liabilities relating to claims filed from 2021 onward against its former Texas subsidiaries seeking unspecified damages for alleged losses caused by the defendants’ failure to provide sufficient power to the grid during Winter Storm Uri. The claims also allege similar liability against numerous other ERCOT power market participants. In December 2023, five multi-district litigation (“MDL”) bellwether lawsuits, which were selected by the MDL court as representative of all 58 cases filed in the Uri litigation, were dismissed by the MDL court, a ruling subsequently upheld by the Texas First Court of Appeals. In January and February 2025, the plaintiffs (in two groups) filed for relief in the Texas Supreme Court, seeking to overturn the lower courts. In July 2025, the Texas Supreme Court ordered merits briefing by the parties, which has since concluded. If the Court of Appeals decision is affirmed by the Texas Supreme Court, Talen expects the dismissal ruling to apply broadly to all Uri cases against Talen’s former subsidiaries. Pursuant to the Plan of Reorganization, Talen’s maximum potential damages on prepetition Uri claims are expressly limited to payments from Talen’s insurers.…

Talen Montana Fuel Supply. Talen Montana purchases coal from a mine owned by Westmoreland Rosebud Mining, LLC (the “Rosebud Mine”) for its interest in Colstrip Units 3 and 4 under a full requirements contract with the mine operator. Several lawsuits have been brought against the Rosebud Mine challenging permits and approvals to expand its operations. Talen Montana is not party to these lawsuits but is monitoring the progress of each to assess the impact to its operations. In the first lawsuit, the Montana Supreme Court in 2023 affirmed a lower court’s ruling to vacate a mining permit and require the Montana Board of Environmental Review to perform an additional review of the permit. In the second lawsuit, the Montana Federal District Court ordered a branch of the U.S. Department of the Interior to complete an updated Environmental Impact Statement (“EIS”) for a separate expansion project. In August 2025, the U.S. Department of Interior issued a supplemental EIS and approved an expansion of operations to authorize the mining of federal coal through 2039. In the third lawsuit, plaintiffs challenged a water pollution permit authorizing a separate expansion to the mine in 2023. In September 2025, a Montana State District Court upheld the permit. Plaintiffs appealed that ruling to the Montana Supreme Court in November 2025.…
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001622536&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 17 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 6 份。
2026-11-03 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-09-29 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-12 8-K/A Items 9.01 Financial Statements and Exhibits
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-14 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-18 8-K/A Items 9.01 Financial Statements and Exhibits
2026-06-15 8-K Items 1.01 Entry into a Material Definitive Agreement；2.01 Completion of Acquisition or Disposition of Assets；2.03 Creation of a Direct Financial Obligation；3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-21 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-05-07 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-17 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-26 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-09 8-K/A Items 9.01 Financial Statements and Exhibits
2026-01-15 8-K Items 1.01 Entry into a Material Definitive Agreement；3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-17 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-15 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-25 8-K Items 1.01 Entry into a Material Definitive Agreement；2.01 Completion of Acquisition or Disposition of Assets；2.03 Creation of a Direct Financial Obligation；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-06-15，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/1622536/000162253626000048/tln-20260615.htm｜as_of：2026-06-15
<<<
Item 2.01. Completion of Acquisition or Disposition of Assets.
The disclosure set forth under the Introductory Note and Item 1.01 of this Report is incorporated into this Item 2.01 by reference.
On the Closing Date, the Company completed the previously announced Acquisition contemplated by the Merger Agreement. As a result of the Acquisition, the Acquired Companies became indirect, wholly owned subsidiaries of the Company.
Subject to the terms and conditions of the Merger Agreement, the purchase price for the Acquisition consisted of (a) the Cash Consideration of approximately $2.55 billion, subject to customary adjustments for net working capital, cash, indebtedness, certain casualty losses and transaction expenses, and (b) the Stock Consideration of 2,399,998 shares of common stock, par value $0.001 per share, of the Company. The Cash Consideration was funded using a portion of the proceeds of the 6.125% Senior Unsecured Notes due 2031 and 6.375% Senior Unsecured Notes due 2033 issued in April 2026.
The summary description of the terms of the Merger Agreement, including the description of the transactions contemplated thereby, does not purport to be complete and is qualified in its entirety by reference to the full text of the Merger Agreement.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2025-11-25，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/1622536/000162253625000037/tln-20251125.htm｜as_of：2025-11-25
<<<
Item 2.01. Completion of Acquisition or Disposition of Assets.
The disclosure set forth under the Introductory Note of this Report is incorporated into this Item 2.01 by reference.
On the Closing Date, the Company, through Talen Generation, consummated the Acquisitions pursuant to the Purchase Agreements and acquired all of the issued and outstanding membership interests in (i) Moxie Freedom LLC, a Delaware limited liability company and (ii) Guernsey Power Holdings, LLC, a Delaware limited liability company (which owns 100% of the membership interests in Guernsey Power Station LLC, a Delaware limited liability company) (collectively, the “Acquired Entities”).
Pursuant to the Purchase Agreements, the Company paid approximately $1.5 billion in connection with the Freedom Acquisition and approximately $2.3 billion in connection with the Guernsey Acquisition. The purchase price for each Acquisition is subject to certain post-closing adjustments for net working capital and other customary items, as further set forth in each Purchase Agreement. The Acquisitions were funded with the proceeds from the Offerings and the New Term Loan B Facility.
The summary description of the terms of each Purchase Agreement, including the description of the transactions contemplated thereby, does not purport to be complete and is qualified in its entirety by reference to the full text of each Purchase Agreement.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TLN_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
