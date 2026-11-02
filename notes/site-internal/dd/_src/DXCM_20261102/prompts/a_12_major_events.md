你是 stock-analyst v20 DD 的證據採集子 agent。標的：DXCM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - DXCM DexCom acquisition merger 2025 2026
  - DXCM DexCom class action lawsuit securities fraud
  - DXCM DexCom clinical trial FDA approval 2025 2026
  - DXCM DexCom product launch recall warning letter
  - DXCM DexCom SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm｜as_of：2026-02-12
<<<
ITEM 3 - LEGAL PROCEEDINGS
We are subject to various claims, complaints and legal actions that arise from time to time in the normal course of business, including commercial insurance, product liability, intellectual property and employment related matters. In addition, from time to time we may bring claims or initiate lawsuits against various third parties with respect to matters arising out of the ordinary course of our business, including commercial and employment related matters.
Securities Class Actions
Between August 21 and October 9, 2024, three substantially similar putative class action complaints were filed against us and certain of our executive officers in the United States District Court for the Southern District of California. On December 13, 2024, the court appointed lead plaintiff and consolidated the three actions (now captioned In re Dexcom, Inc. Class Action Securities Litigation, Lead Case No.: 24-cv-1485-RSH-VET). On January 27, 2025, lead plaintiff filed a consolidated complaint. The consolidated complaint alleges violations of the Exchange Act against us and certain of our current and former executive officers for allegedly making false and misleading statements between April 28, 2023 and July 25, 2024, with respect to our expected revenue for fiscal 2024 and ability to capitalize on our growth potential. On March 13, 2025, we filed a motion to dismiss the consolidated complaint. On May 14, 2025, the court granted the motion to dismiss with leave to amend. On May 28, 2025, lead plaintiff filed an amended consolidated complaint. On June 11, 2025, we filed a motion to dismiss the amended consolidated complaint. On September 9, 2025, the court granted in part and denied in part the motion to dismiss. On October 7, 2025, defendants answered the amended consolidated complaint. On October 10, 2025, defendants filed a motion for judgment on the pleadings as to the two surviving challenged statements. On January 7, 2026, the court granted defendants’ motion for judgment on the pleadings with leave to amend. On February 6, 2026, lead plaintiff filed a second amended consolidated complaint. Defendants’ deadline to respond to the second amended consolidated complaint is February 20, 2026.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm｜as_of：2026-02-12
<<<
Securities class action litigation has often been brought against public companies that experience periods of volatility in the market prices of their securities. For example, we have pending securities class action litigation and derivative actions pending against us. Securities class action litigation could result in substantial costs and a diversion of our management’s attention and resources, which could seriously harm our business.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 3. Legal Proceedings（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1093557/000109355726000027/dxcm-20251231.htm｜as_of：2026-02-12
<<<
73 Derivative Actions Between September 13 and April 14, 2025, three putative stockholders filed derivative lawsuits against us and certain of our current and former executive officers and directors in the United States District Court for the Southern District of California. The derivative complaints allege factual allegations largely tracking allegations made in the In re Dexcom, Inc. Securities Class Action Litigation and seek, among other things, damages and restitution to be paid to the Company by the individual defendants, punitive damages, and attorney’s fees and costs. These actions have been consolidated (captioned In Re: Dexcom, Inc. Stockholder Derivative Litigation, Lead Case No.: 24-cv-1645-RSH-VET), and are currently stayed pending a resolution of the anticipated motion to dismiss in the In re Dexcom, Inc. Securities Class Action Litigation.

On September 25, 2025, an additional derivative lawsuit was filed against us and certain of our current and former executive officers and directors in the Court of Chancery of the State of Delaware. The allegations largely track those made in the In re Dexcom, Inc. Securities Class Action Litigation and seek, among other things, damages and restitution to be paid to the Company by the individual defendants, punitive damages, and attorney’s fees and costs. This action This action is currently stayed pending a resolution of the anticipated motion to dismiss in the In re Dexcom, Inc. Securities Class Action Litigation.

G6 and G7 Class Action Litigation Between September 29, 2025, and January 8, 2026, various plaintiffs, purported users of G6 or G7 devices, filed six overlapping putative class action complaints against us. Four of the complaints originally were filed and are pending in the United States District Court for the Southern District of California (Levens, et al. v. Dexcom, Inc., No. 3:25-cv-02565-BJC-BLM; Estravit v. Dexcom, Inc., No. 3:25-cv-02845-BJC-BLM; and Dalora v. Dexcom, Inc., No. 3:25-cv-03210-BJC-BLM; Dickinson, et al. v. Dexcom, Inc. Dickinson, et al. v. Dexcom, Inc., No. 3:26-cv-00102-BJC-BLM); one of the complaints originally was filed in United States District Court for the Central District of California, and subsequently transferred to the United States District Court for the Southern District of California (Grisoli, et al. v. Dexcom, Inc., No. 3:25-cv-03488-BJC-BLM); and one of the complaints was filed and is pending in the Superior Court of Los Angeles County, California (Chatelain v. Dexcom, Inc., No. 25STCV30722).…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001093557&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-14 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-10 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-28 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-15 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-04-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-03-02 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-26 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-12 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-12 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-12-22 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-10-29，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1093557/000109355726000193/dxcm-20261029.htm｜as_of：2026-10-29
<<<
ITEM 8.01.
OTHER EVENTS.
On October 29, 2026, Dexcom announced that its Board of Directors authorized and approved a share repurchase program of up to $1.0 billion of Dexcom’s outstanding common stock, par value $0.001 per share (“Common Stock”), with a repurchase period ending no later than December 31, 2027 (the “Share Repurchase Program”).
Repurchases of Common Stock under the Share Repurchase Program may be made from time to time in the open market, in privately negotiated transactions or by other methods, including through the use of trading plans intended to qualify under Rule 10b5-1 under the Exchange Act, at Dexcom’s discretion, and in accordance with the limitations set forth in Rule 10b-18 promulgated under the Exchange Act and other applicable federal and state laws and regulations. The timing of any repurchases will depend on market conditions and will be made at Dexcom’s discretion.
The Share Repurchase Program does not obligate Dexcom to repurchase any dollar amount or number of shares of Common Stock, and the program may be extended, modified, suspended, or discontinued at any time.
ITEM 9.01. FINANCIAL STATEMENTS AND EXHIBITS.
(d) Exhibits.
Number Description
99.1 Press release dated October 29, 2026
104 Cover Page Interactive Data File (formatted as Inline XBRL)
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-15，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1093557/000109355726000085/dxcm-20260514.htm｜as_of：2026-05-15
<<<
ITEM 8.01. OTHER EVENTS.
On May 14, 2026, Dexcom announced that its Board of Directors authorized and approved a share repurchase program of up to $1.0 billion of Dexcom’s outstanding common stock, par value $0.001 per share (“Common Stock”), with a repurchase period ending no later than June 30, 2027 (the “Share Repurchase Program”). In connection with the approval of the Share Repurchase Program, the Board of Directors terminated its existing share repurchase program, of which $250.0 million remained available to be repurchased under the program.
Repurchases of Common Stock under the Share Repurchase Program may be made from time to time in the open market, in privately negotiated transactions or by other methods, including through the use of trading plans intended to qualify under Rule 10b5-1 under the Exchange Act, at Dexcom’s discretion, and in accordance with the limitations set forth in Rule 10b-18 promulgated under the Exchange Act and other applicable federal and state laws and regulations. The timing of any repurchases will depend on market conditions and will be made at Dexcom’s discretion.
The Share Repurchase Program does not obligate Dexcom to repurchase any dollar amount or number of shares of Common Stock, and the program may be extended, modified, suspended, or discontinued at any time.
Cautionary Statement Regarding Forward Looking Statements…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
