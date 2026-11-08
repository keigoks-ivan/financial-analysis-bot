你是 stock-analyst v20 DD 的證據採集子 agent。標的：NVTS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - NVTS Navitas Semiconductor acquisition merger 2025 2026
  - NVTS Navitas Semiconductor class action lawsuit securities fraud
  - NVTS Navitas Semiconductor clinical trial FDA approval 2025 2026
  - NVTS Navitas Semiconductor product launch recall warning letter
  - NVTS Navitas Semiconductor SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm｜as_of：2026-02-27
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm｜as_of：2026-02-27
<<<
The semiconductor industry is characterized by frequent litigation regarding patent and other intellectual property rights, including by both competitors and so-called “non-practicing entities.” We have received communications, and we expect to receive additional communications from time to time, that allege or imply that our products or technologies infringe the patent or other intellectual property rights of third parties or that invite us to take a license to certain allegedly infringed patents. Lawsuits or other proceedings resulting from allegations of infringement could subject us to significant liability for damages, invalidate our proprietary rights, force us to make changes to our products, and adversely affect our business. In some cases, the allegation of patent infringement is made against our end-customer who may seek indemnification from us. In the event that any third-party succeeds in asserting a valid claim against us or any of our end customers, we could be forced to do one or more of the following: •discontinue selling, importing or using certain technologies that contain the allegedly infringing intellectual property which could cause us to stop manufacturing certain products; •seek to develop non-infringing technologies, which may not be feasible; 31 TABLE OF CONTENTS •incur significant legal expenses, including defense costs under indemnification obligations; •pay substantial monetary damages to the party whose intellectual property rights we may be found to be…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm｜as_of：2026-02-27
<<<
8-K 001-39755 2.1 5/7/2021 2.2 Agreement and Plan of Merger, dated as of August 15, 2022, by and among Navitas Semiconductor Corporation, Gemini Acquisition LLC, GeneSiC Semiconductor Inc., Ranbir Singh and The Ranbir Singh Irrevocable Trust dated February 4, 2022 10-Q 001-39755 2.1 11/14/2022 3.1 Second Amended and Restated Certificate of Incorporation of Navitas Semiconductor Corporation 8-K 001-39755 3.1 10/25/2021 3.2* Amended and Restated Bylaws of Navitas Semiconductor Corporation, as amended 8-K 001-39755 3.1 4/10/2025 4.1 Description of Registrant’s Securities 10-K 001-39755 4.1 3/6/2024 10.1† Navitas Semiconductor Corporation 2021 Equity Incentive Plan 8-K/A 001-39755 10.5 11/15/2021 10.2† Form of Restricted Stock Unit Agreement 8-K 001-39755 10.6 10/25/2021 10.3† Form of Stock Option Agreement 8-K 001-39755 10.7 10/25/2021 10.4† Amended and Restated Navitas Semiconductor Limited 2020 Equity Incentive Plan S-4/A 333-256880 10.16 8/23/2021 10.5 Registration Rights Agreement, dated December 2, 2020, among Live Oak Acquisition Corp. II, Live Oak Sponsor Partners II, LLC and certain other security holders named therein 8-K 001-39755 10.3 12/8/2020 10.6† Form of Indemnification Agreement 8-K 001-39755 10.4 10/25/2021 10.7 Lock-Up Agreement (Management), dated as of May 6, 2021, among Live Oak Acquisition Corp. II, Legacy Navitas and certain equity holders of Legacy Navitas 8-K 001-39755 10.2 5/7/2021 10.8 Lock-Up Agreement (VPs), dated as of May 6, 2021, among Live Oak Acquisition Corp.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001821769&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 24 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 11 份。
2026-11-03 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-10-06 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-21 8-K/A Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-09-21 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-08-25 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-27 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-08 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-26 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-06-15 8-K Items 8.01 Other Events
2026-06-09 8-K Items 5.02 Departure/Election of Directors or Officers
2026-06-04 8-K Items 8.01 Other Events
2026-05-22 8-K Items 8.01 Other Events
2026-05-22 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-05-13 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-11 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-04 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-13 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-03-17 8-K Items 5.02 Departure/Election of Directors or Officers
2026-03-11 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-24 8-K Items 5.02 Departure/Election of Directors or Officers
2026-02-24 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-11-20 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-10 8-K Items 1.01 Entry into a Material Definitive Agreement；3.02 Unregistered Sales of Equity Securities；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-21，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1821769/000110465926109227/tm2625807d2_8ka.htm｜as_of：2026-09-21
<<<
Item 1.01 to “September 18, 2026” (from “September
19, 2026” in the Original Filing). No other changes have been made from the Original Filing.
Item 1.01. Entry into a Material Definitive Agreement.
On September 18, 2026, Navitas Semiconductor Corporation (the
“Company”) entered into a Stock Purchase Agreement (the “Purchase Agreement”) with Magnachip Semiconductor Corporation
(“Magnachip”), pursuant to which Magnachip agreed to issue and sell to the Company 1,461,988 shares of Magnachip’s common
stock, par value $0.01 per share (the “MX Common Stock”), at a purchase price of $3.42 per share, for an aggregate purchase
price of $5,000,000.
The closing of the transactions contemplated by the Purchase Agreement
is expected to occur on or about September 24, 2026, subject to the satisfaction or waiver of customary closing conditions. The Purchase
Agreement contains customary representations, warranties and covenants, which were made only for purposes of the Purchase Agreement and
as of specific dates, were solely for the benefit of the parties to the Purchase Agreement, and may be subject to limitations agreed upon
by the Company and Magnachip.
The Purchase Agreement also provides that Magnachip will file with
the Securities and Exchange Commission (the “SEC”), no later than 30 days after the closing, a registration statement on Form S-3…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-09-21，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1821769/000110465926109125/tm2625807d1_8k.htm｜as_of：2026-09-21
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On September 19, 2026, Navitas Semiconductor Corporation (the
“Company”) entered into a Stock Purchase Agreement (the “Purchase Agreement”) with Magnachip Semiconductor Corporation
(“Magnachip”), pursuant to which Magnachip agreed to issue and sell to the Company 1,461,988 shares of Magnachip’s common
stock, par value $0.01 per share (the “MX Common Stock”), at a purchase price of $3.42 per share, for an aggregate purchase
price of $5,000,000.
The closing of the transactions contemplated by the Purchase Agreement
is expected to occur on or about September 24, 2026, subject to the satisfaction or waiver of customary closing conditions. The Purchase
Agreement contains customary representations, warranties and covenants, which were made only for purposes of the Purchase Agreement and
as of specific dates, were solely for the benefit of the parties to the Purchase Agreement, and may be subject to limitations agreed upon
by the Company and Magnachip.
The Purchase Agreement also provides that Magnachip will file with
the Securities and Exchange Commission (the “SEC”), no later than 30 days after the closing, a registration statement on Form S-3
covering the resale of the shares of MX Common Stock issued in the transaction. Magnachip agreed to use commercially reasonable efforts…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-08-25，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1821769/000110465926100478/tm2623854d1_8k.htm｜as_of：2026-08-25
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On August 24, 2026, Navitas Semiconductor
Corporation (“Navitas” or the “Company”) entered into an Agreement and Plan of Merger (the “Merger Agreement”),
by and among the Company, Claros, Inc., a Delaware corporation (“Claros”), Compass Merger Sub 1 Inc., a Delaware corporation
and a wholly-owned subsidiary of the Company (“Merger Sub 1”), Compass Merger Sub 2 LLC, a Delaware limited liability company
and a wholly-owned subsidiary of the Company (“Merger Sub 2”), and Shareholder Representative Services LLC, a Colorado limited
liability company, solely in its capacity as the representative, agent and attorney-in-fact of the securityholders of Claros (the “Securityholders’
Representative”). The Company, Claros, Merger Sub 1, Merger Sub 2 and Securityholders’ Representative are each referred to
herein as a “Party” and, collectively, as the “Parties.” Pursuant to the Merger Agreement, and subject to the
terms and conditions set forth therein, the parties intend that (i) Merger Sub 1 will be merged with and into Claros, with Claros
being the surviving corporation in such merger (the “First Merger”), and (ii) immediately following the consummation
of the First Merger, Claros will be merged with and into Merger Sub 2, with Merger Sub 2 being the surviving limited liability company…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVTS_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
