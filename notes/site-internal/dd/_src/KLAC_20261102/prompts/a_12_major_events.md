你是 stock-analyst v20 DD 的證據採集子 agent。標的：KLAC。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - KLAC KLA acquisition merger 2025 2026
  - KLAC KLA class action lawsuit securities fraud
  - KLAC KLA clinical trial FDA approval 2025 2026
  - KLAC KLA product launch recall warning letter
  - KLAC KLA SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
Any impact to the availability, integrity or confidentiality of our IT Systems or Confidential Information can materially adversely impact our business, operations and financial condition directly, or indirectly by impacting third parties in the supply chain, including direct or sub-tier suppliers, in many potential ways: disruptions to operations; misappropriation, corruption or theft of Confidential Information; misappropriation of funds and Company assets; reduced value of our investments in research, development and engineering; litigation (including class action lawsuits) with, or payment of damages to, third parties; reputational damage; costs to comply with regulatory inquiries or actions; data privacy issues; costs to rebuild our IT Systems or restore our Confidential Information; and increased cybersecurity protection and remediation costs. Additionally, cybersecurity and data security and protection laws and regulations are evolving and present increasing compliance challenges, which may increase our costs, affect our competitiveness, cause reputational harm and expose us to substantial fines or other penalties.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
NOTE 14 — LITIGATION AND OTHER LEGAL MATTERS We are named, from time to time, as a party to lawsuits and other types of legal proceedings and claims in the normal course of our business. Actions filed against us include commercial, intellectual property (“IP”), customer, and labor and employment related claims, including complaints of alleged wrongful termination and potential class action lawsuits regarding alleged violations of federal and state wage and hour and other laws. In general, legal proceedings and claims, regardless of 83 Table of Contents their merit, and associated internal investigations (especially those relating to IP or confidential information disputes) are often expensive to prosecute, defend or conduct and may divert management’s attention and other Company resources. Moreover, the results of legal proceedings are difficult to predict, and the costs incurred in litigation can be substantial, regardless of outcome. We believe the amounts provided in our Consolidated Financial Statements are adequate in light of the probable and estimated liabilities.…
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-06）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/319201/000031920126000027/klac-20260630.htm｜as_of：2026-08-06
<<<
3. Exhibits The information required by this item is set forth below. Exhibit Number Exhibit Description Incorporated by Reference Form File No. Exhibit Number Filing Date 3.1 Restated Certificate of Incorporation of KLA Corporation 8-K No. 000-09992 3.2 June 12, 2026 3.2 Amended and Restated Bylaws 8-K No. 000-09992 3.1 November 7, 2025 4.1 Description of the Registrant’s securities registered under Section 12 of the Securities Act of 1934 4.2 Indenture dated November 6, 2014 between KLA-Tencor Corporation and Wells Fargo Bank, National Association, as trustee 8-K No. 000-09992 4.1 November 7, 2014 4.3 Form of Officer’s Certificate setting forth the terms of the Notes (with form of Notes attached)
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000319201&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。
2026-10-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-08-06 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-12 8-K Items 5.03 Amendments to Articles or Bylaws；9.01 Financial Statements and Exhibits
2026-05-07 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-03-12 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-02-05 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-11-07 8-K Items 5.03 Amendments to Articles or Bylaws；5.07 Submission of Matters to a Vote of Security Holders；8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-08-06，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/319201/000119312526338242/d165938d8k.htm｜as_of：2026-08-06
<<<
Item 8.01
Other Events.
On August 6, 2026, KLA Corporation (the “Company”) issued a press release announcing that the Company’s Board of Directors declared a cash dividend of $0.23 per share on the Company’s common stock. Such dividend shall be payable on September 1, 2026 to stockholders of record as of the close of business on August 17, 2026. A copy of the press release is attached to this Current Report on Form 8-K as Exhibit 99.1.
Item 9.01
Financial Statements and Exhibits.
(d)
Exhibits
The following exhibits are filed herewith.
Exhibit
No.
Description
99.1
Press release issued August 6, 2026
104
Cover Page Interactive Data File (formatted as inline XBRL and contained in Exhibit 101)
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-07，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/319201/000119312526212093/d116682d8k.htm｜as_of：2026-05-07
<<<
Item 8.01
Other Events.
On May 7, 2026, KLA Corporation (the “Company”) announced that its Board of Directors (the “Board”) had approved a ten-for-one forward stock split (the “Stock Split”) of the Company’s outstanding shares of common stock, par value $0.001 per share (the “Common Stock”), to be effected through an amendment to the Company’s Restated Certificate of Incorporation (the “Charter Amendment”), which will also effect a proportionate increase in the number of authorized shares of the Company’s Common Stock from 500,000,000 to 5,000,000,000.
The Stock Split is expected to become effective after the close of the Nasdaq Global Select Market (the “Nasdaq Stock Market”) on June 11, 2026 (the “Effective Date”). As a result of the Stock Split, each stockholder of record as of the close of the Nasdaq Stock Market on June 4, 2026 (the “Record Date”) will receive nine (9) additional shares of Common Stock for every one (1) share of Common Stock held on the Record Date. Trading in the Common Stock on the Nasdaq Stock Market is expected to commence on a Stock Split-adjusted basis at the market open on June 12, 2026, under the existing trading symbol “KLAC.”
A copy of the press release announcing the Stock Split is attached hereto as Exhibit 99.1 and is incorporated herein by reference.…
>>>

[8] 來源：SEC EDGAR｜文件：8-K（2026-03-12，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/319201/000119312526102999/d105235d8k.htm｜as_of：2026-03-12
<<<
Item 8.01
Other Events.
On March 11, 2026, the Board of Directors of the Company (the “Board”) established a quarterly dividend level of $2.30 per share on the outstanding shares of the Company’s common stock, which represents the anticipated level at which dividends will be declared by the Board until the Board determines otherwise, beginning with the dividend expected to be declared in May 2026. This new dividend level represents a 21% increase over the Company’s most recent quarterly dividend of $1.90 per share declared in February 2026. The declaration and payment of future dividends is subject to the Board’s discretion and will depend on financial and legal requirements and other considerations.
Also, on March 11, 2026, the Board approved a new share repurchase program that authorizes the repurchase of up to $7 billion of shares of the Company’s common stock. This share repurchase program is in addition to the $5 billion share repurchase program announced in April 2025, which as of December 31, 2025 had $3.94 billion of repurchase authority remaining.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
