你是 stock-analyst v20 DD 的證據採集子 agent。標的：SNDK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - SNDK Sandisk acquisition merger 2025 2026
  - SNDK Sandisk class action lawsuit securities fraud
  - SNDK Sandisk clinical trial FDA approval 2025 2026
  - SNDK Sandisk product launch recall warning letter
  - SNDK Sandisk SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
Item 3. Legal Proceedings
There are no material legal proceedings, other than ordinary routine litigation incidental to the Company, to which we or any of our subsidiaries is a party or of which any of our or our subsidiaries’ property is subject.
Table of Contents
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
We provide warranties on the majority of our products for periods of one to five years. We test our products in our manufacturing facilities through a variety of means. However, our testing may fail to reveal defects in our products that may not become apparent until after the products have been sold into the market. In addition, our products may be used in a manner that is not intended or anticipated by us, resulting in potential liability. Accordingly, there is a risk that product defects will occur, including as a result of third-party components or applications that we incorporate in our products, which could require a product recall. Product recalls can be expensive to implement. As part of a product recall, we may be required or choose to replace the defective product. Moreover, there is a risk that product defects may trigger an epidemic failure clause in a customer agreement. If an epidemic failure occurs, we may face termination of long-term sales agreements and may be required to replace or refund the value of the defective product and to cover certain other costs associated with the consequences of the epidemic failure.…

From time to time, we may be involved in litigation, including antitrust and commercial matters, putative securities class action suits and other actions. We may be the plaintiff in some of these actions and the defendant in others. Some of the actions may seek injunctive relief, including injunctions against the sale of our products, and substantial monetary damages, which if granted or awarded, could materially harm our business. From time to time, we may also be the subject of inquiries, requests for information, investigations and actions by government and regulatory agencies regarding our business. Any such matters could result in material adverse consequences to our results of operations, financial condition or ability to conduct our business, including fines, penalties or restrictions on our business activities.

Stock markets in general have experienced volatility that has often been unrelated to the operating performance of a particular company. Broad market and industry factors may materially harm the market price of our common stock, regardless of our operating performance. In the past, following periods of volatility in the market price of a company’s securities, shareholder derivative lawsuits and/or securities class action litigation has often been instituted against such company. Such litigation, if instituted against us, could result in substantial costs and a diversion of management’s attention and resources.
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002023554&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 6 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-16 8-K Items 5.02 Departure/Election of Directors or Officers
2026-09-11 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-15 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-30 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-03-25 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-02 8-K Items 5.02 Departure/Election of Directors or Officers
2025-11-20 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2025-11-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-09-11，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/2023554/000119312526389293/d138343d8k.htm｜as_of：2026-09-11
<<<
Item 1.01
Entry Into a Material Definitive Agreement.
On September 9, 2026, Sandisk Corporation (“SDC” or the “Company”) entered into Amendment No. 1 (“Amendment No. 1”) by and among the Company, Sandisk Technologies, Inc. (“SDT”), the banks and other financial institutions party thereto and JPMorgan Chase Bank, N.A., as administrative agent, to the Company’s Loan Agreement dated as of February 21, 2025 by and among the Company, the banks and other financial institutions party thereto and JPMorgan Chase Bank, N.A., as administrative agent (as amended, supplemented or otherwise modified as of the effective date of Amendment No. 1, including by Amendment No. 1, the “Loan Agreement”),.
Amendment No. 1 provides for a revolving credit facility (the “Revolving Credit Facility”) comprising an aggregate principal amount of $1,500.0 million in revolving commitments, which commitments refinanced in full the revolving commitments outstanding under the Loan Agreement prior to Amendment No. 1.
Borrowings under the Revolving Credit Facility, for U.S.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-03-25，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/2023554/000119312526122705/d136592d8k.htm｜as_of：2026-03-25
<<<
Item 1.01
Entry into a Material Definitive Agreement.
On March 25, 2026, Sandisk Technologies, Inc. (the “Company”), a wholly-owned subsidiary of Sandisk Corporation, entered into a Private Placement Subscription Agreement (the “Equity Investment Agreement”) with Nanya Technology Corporation (“Nanya”), pursuant to which the Company agreed to make a strategic equity investment in Nanya through a private placement of Nanya common stock (the “Transaction”).
Under the Equity Investment Agreement, the Company agreed to purchase approximately 139 million shares of Nanya common stock for an aggregate purchase price of approximately $1.0 billion, representing approximately 3.9% of Nanya’s outstanding common stock on a fully diluted basis following the Transaction. The purchase price reflects a 15% discount to Nanya’s 30-day average trading price, consistent with the Taiwan Securities and Exchange Act (“SEA”) and applicable regulations. The private placement is being conducted pursuant to Article 43-6 of the SEA and applicable regulations and is subject to post-closing filings with the Taiwan Stock Exchange and other Taiwanese regulatory authorities. The shares issued to the Company in the private placement will be subject to a statutory lock-up period of three years following delivery, during which the Company will be restricted from transferring or selling the shares, subject to limited exceptions under applicable Taiwanese law.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-10-29，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026068243/sndk-20261029.htm｜as_of：2026-10-29
<<<
Item 8.01 Other Events.
On October 29, 2026, Sandisk Corporation (the “Company”) announced that its Board of Directors approved an eight-for-one forward stock split (the “Stock Split”) of its common stock, par value $0.01 per share ("Common Stock"). The Stock Split will be effected through an amendment (the “Charter Amendment”) to the Company’s Amended and Restated Certificate of Incorporation. The Charter Amendment, when effected, will proportionately increase the number of authorized shares of the Company’s Common Stock from 450 million to 3.6 billion.
In connection with the Stock Split, each of the Company’s stockholders of record as of the close of business on November 9, 2026 will receive seven additional shares for each share held, which will be issued after market close on Thursday, November 19, 2026. The Company’s Common Stock is expected to begin trading on a post-split basis at the market open on Friday, November 20, 2026 under the Company’s existing trading symbol “SNDK”.
Item 9.01 Financial Statements and Exhibits.
(d) Exhibits
99.1 Press release issued by Sandisk Corporation on October 29, 2026 announcing financial results for the fiscal first quarter ended October 2, 2026.
104 Cover Page Interactive Data File (embedded within the Inline XBRL document).
Forward-Looking Statements
This Current Report on Form 8-K contains forward-looking statements within the meaning of U.S.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
