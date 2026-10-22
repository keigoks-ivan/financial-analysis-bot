你是 stock-analyst v20 DD 的證據採集子 agent。標的：COF。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - COF Capital One Financial acquisition merger 2025 2026
  - COF Capital One Financial class action lawsuit securities fraud
  - COF Capital One Financial clinical trial FDA approval 2025 2026
  - COF Capital One Financial product launch recall warning letter
  - COF Capital One Financial SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm｜as_of：2026-02-19
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm｜as_of：2026-02-19
<<<
Discover Card Product Misclassification Discover and certain of its subsidiaries entered into a settlement agreement to resolve putative class actions filed on behalf of merchants allegedly affected by the Card Product Misclassification. The court granted preliminary approval of the settlement on July 30, 2025. Discover reserved $1.2 billion related to this matter and the class action settlement will be the primary means through which restitution will be paid to adversely affected merchants, merchant acquirers and other intermediaries.

Discover was also named as a defendant in a putative class action on behalf of shareholders alleging securities and other claims based on the Card Product Misclassification, among other subjects. On March 31, 2025, the court dismissed the putative shareholder class action without prejudice, and on May 14, 2025, plaintiffs moved for leave to file an amended complaint. Discover was also subject to an SEC investigation into the Card Product Misclassification matter. We are cooperating with the investigation.

Interchange Litigation In 2005, a putative class of retail merchants filed antitrust lawsuits against Mastercard and Visa and several issuing banks, including Capital One, seeking both injunctive relief and monetary damages for an alleged conspiracy by defendants to fix the level of interchange fees. The Visa and Mastercard payment networks and issuing banks entered into settlement and judgment sharing agreements allocating the liabilities of any judgment or settlement arising from all interchange-related cases.

The lawsuits were consolidated before the U.S. District Court for the Eastern District of New York for certain purposes and were settled in 2012. The class settlement, however, was invalidated by the United States Court of Appeals for the Second Circuit in June 2016, and the suit was bifurcated into separate class actions seeking injunctive and monetary relief, respectively. In addition, numerous merchant groups opted out of the 2012 settlement.

245 Capital One Financial Corporation (COF) Table of Contents CAPITAL ONE FINANCIAL CORPORATION NOTES TO CONSOLIDATED FINANCIAL STATEMENTS We are named as a defendant in four putative consumer class action cases in Canadian courts alleging harm from the 2019 Cybersecurity Incident. The lawsuits allege breach of contract, negligence, violations of various privacy laws and a variety of other legal causes of action. Courts in British Columbia and Quebec have certified classes of consumers. The final two putative class actions, both of which are pending in Alberta have not advanced beyond a preliminary stage.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm｜as_of：2026-02-19
<<<
3.1 Restated Certificate of Incorporation of Capital One Financial Corporation (as restated July 26, 2023) (incorporated by reference to Exhibit 3.1 of the Quarterly Report on Form 10-Q, filed on July 27, 2023).
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000927628&type=8-K｜as_of：2026-10-22
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 31 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。
2026-10-20 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-10-20 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-09-15 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-15 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-15 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-01 8-K Items 5.03 Amendments to Articles or Bylaws；9.01 Financial Statements and Exhibits
2026-08-20 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-17 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-21 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-21 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-15 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-09 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-06-08 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-15 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-08 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-04-23 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-21 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-21 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-07 8-K Items 3.02 Unregistered Sales of Equity Securities；5.02 Departure/Election of Directors or Officers
2026-03-16 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-17 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-09 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-06 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-02 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-01-22 8-K Items 3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-22 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-22 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-12-15 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-08 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-17 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-07 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-15，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/927628/000119312526391921/d458116d8k.htm｜as_of：2026-09-15
<<<
Item 8.01
Other Events.
On September 15, 2026, Capital One Financial Corporation (the “Company”) closed the public offering of €750,000,000 aggregate principal amount of 4.326% Fixed-to-Floating Rate Senior Notes due 2032 (the “2032 Fixed-to-Floating Rate Notes”) and €750,000,000 aggregate principal amount of 4.832% Fixed-to-Floating Rate Senior Notes due 2037 (the “2037 Fixed-to-Floating Rate Notes” and, together with the 2032 Fixed-to-Floating Rate Notes, the “Notes”), pursuant to an underwriting agreement (the “Underwriting Agreement”), dated September 9, 2026, with Barclays Bank PLC, Deutsche Bank AG, London Branch, Goldman Sachs & Co. LLC, Morgan Stanley & Co. International plc and Capital One Securities, Inc., as representatives of the several underwriters listed therein. In connection with the closing of the offering, the Company entered into a paying agency agreement (the “Paying Agency Agreement”) with The Bank of New York Mellon, London Branch, as paying agent. The Notes were issued pursuant to a Senior Indenture dated as of November 1, 1996 (the “Base Indenture”) between the Company and The Bank of New York Mellon Trust Company, N.A., formerly known as The Bank of New York Trust Company, N.A. (as successor to Harris Trust and Savings Bank), as Indenture Trustee (the “Trustee”), as supplemented by the First Supplemental Indenture dated as of November 2, 2021 between the Company and the Trustee (the “Supplemental Indenture”).…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-08-20，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/927628/000119312526358268/d825041d8k.htm｜as_of：2026-08-20
<<<
Item 8.01
Other Events.
On August 20, 2026, Capital One Financial Corporation (the “Company”) issued a press release announcing that it will redeem all outstanding shares of its Fixed Rate Reset Non-Cumulative Perpetual Preferred Stock, Series M, $0.01 par value per share (“Series M Preferred Stock”).
The Series M Preferred Stock (CUSIP: 14040HCF0) will be redeemed on September 1, 2026 (the “Series M Redemption Date”) at a redemption price of $1,000 per share of Series M Preferred Stock. All 1,000,000 outstanding shares of the Series M Preferred Stock will be redeemed on the Series M Redemption Date.
Regular dividends on the outstanding shares of the Series M Preferred Stock will be paid separately on the Series M Redemption Date to holders of record as of the close of business on August 17, 2026, in the customary manner. On and after the Series M Redemption Date, all dividends on the shares of Series M Preferred Stock will cease to accrue.
A copy of the press release is attached as Exhibit 99.1 hereto and incorporated by reference into this Item 8.01.
Item 9.01
Financial Statements and Exhibits.
(d) Exhibits
Exhibit
No.
Description
99.1
Press Release, dated August 20, 2026
104
The cover page from this Current Report on Form 8-K, formatted in Inline XBRL
1
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-06-09，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/927628/000119312526263735/d94250d8k.htm｜as_of：2026-06-09
<<<
Item 8.01
Other Events.
This current report on Form 8-K is filed for the purpose of filing the attached exhibit in connection with the prospectus supplement no. 2, dated June 9, 2026 (the “Resale Prospectus Supplement No. 2”), filed by Capital One Financial Corporation (the “Company”) with the Securities and Exchange Commission, which amends and supplements the prospectus supplement, dated April 23, 2026 (the “Initial Resale Prospectus Supplement”) and forms a part of the Company’s automatic shelf registration statement on Form S-3 (File No. 333-277813).
The Resale Prospectus Supplement No. 2 registers the offer and sale of an additional 39,843 shares of common stock, $0.01 par value per share, of the Company (“Company Common Stock”). The Company previously registered the offer and sale of up to 10,345,906 shares of Company Common Stock under the Initial Resale Prospectus Supplement. Accordingly, the selling security holders referred to in the Initial Resale Prospectus Supplement, as amended and supplemented by the Resale Prospectus Supplement No. 2, may offer and sell up to 10,385,749 shares of Company Common Stock.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
