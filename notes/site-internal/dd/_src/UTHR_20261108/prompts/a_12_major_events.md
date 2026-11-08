你是 stock-analyst v20 DD 的證據採集子 agent。標的：UTHR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - UTHR United Therapeutics acquisition merger 2025 2026
  - UTHR United Therapeutics class action lawsuit securities fraud
  - UTHR United Therapeutics clinical trial FDA approval 2025 2026
  - UTHR United Therapeutics product launch recall warning letter
  - UTHR United Therapeutics SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
If the ANDA applicant has submitted a Paragraph IV certification to the FDA, the applicant must also send notice of the Paragraph IV certification to the NDA and patent holders once the ANDA has been accepted for filing by the FDA. The NDA and patent holders may then initiate a patent infringement lawsuit in response to the notice of the Paragraph IV certification. The filing of a patent infringement lawsuit within 45 days of the receipt of a Paragraph IV certification automatically prevents the FDA from approving the ANDA until the earlier of 30 months, expiration of the patent, settlement of the lawsuit, or a decision in the infringement case that is favorable to the ANDA applicant.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
We recorded revenue from two distributors in the United States that exceeded ten percent of total revenues. Revenue from these two distributors as a percentage of total revenues is as follows: Year Ended December 31, 2025 2024 2023 Distributor 1 51 % 51 % 51 % Distributor 2 36 % 35 % 34 % Long-lived assets, including PP&E and right-of-use assets, located by geographic area are as follows (in millions): Year Ended December 31, 2025 2024 2023 United States $ 1,743.5 $ 1,240.6 $ 1,057.8 Rest-of-World 15.8 11.7 12.0 Total $ 1,759.3 $ 1,252.3 $ 1,069.8 14. Litigation Sandoz Litigation In April 2019, Sandoz Inc. (Sandoz) and its marketing partner RareGen, LLC (now known as Liquidia PAH, LLC, a subsidiary of Liquidia Corporation) (RareGen), filed a complaint in the U.S. District Court for the District of New Jersey against us and Smiths Medical ASD, Inc. (Smiths Medical), alleging that we and Smiths Medical engaged in anticompetitive conduct in connection with the plaintiffs’ efforts to launch their generic version of Remodulin. In particular, the complaint alleged that we and Smiths Medical unlawfully impeded competition by entering into an agreement for Smiths Medical to produce cartridges used with the CADD-MS®3 (MS-3) infusion system specifically for the delivery of subcutaneous Remodulin for our patients, without making these cartridges available for the delivery of Sandoz’s generic treprostinil injection.…

Smiths Medical was dismissed from the case in November 2020, based on a settlement resolving the disputes between the plaintiffs and Smiths Medical. As part of this settlement, Smiths Medical paid the plaintiffs $4.25 million, disclosed and made available to the plaintiffs certain specifications and other information related to the MS-3 cartridges, and granted to the plaintiffs a non-exclusive, royalty-free license in the United States to Smiths Medical’s patents and copyrights associated with the MS-3 cartridges and certain other information related to the MS-3 pumps and cartridges.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001082554&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。
2026-11-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-22 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-14 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-08 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-23 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-29 8-K Items 5.02 Departure/Election of Directors or Officers；5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-03-30 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-03-09 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-02 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-25 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-22 8-K Items 5.02 Departure/Election of Directors or Officers；5.03 Amendments to Articles or Bylaws；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-08，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1082554/000110465926105953/tm2624887d1_8k.htm｜as_of：2026-09-08
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On September 8, 2026, United Therapeutics Corporation
(the Company) entered into an accelerated share repurchase agreement (the ASR Agreement) with Citibank, N.A. (Citi)
to repurchase approximately $477.6 million in the aggregate of the Company’s common stock (Common Stock) under the Company’s
previously announced share repurchase program (the Share Repurchase Program).
Under the terms of the ASR Agreement, the
Company will make an aggregate upfront payment of approximately $477.6 million to Citi on or around September 10, 2026 and will
receive an initial delivery of approximately 719,376 shares of Common Stock,
representing approximately 75% of the total shares that would be repurchased under the ASR Agreement measured based on the closing
price of the Common Stock on September 8, 2026.
The exact number of shares that the Company will
ultimately repurchase pursuant to the ASR Agreement will be determined based on the average of the daily volume-weighted average price
per share of the Common Stock during the term of the ASR Agreement, less a discount and subject to adjustments pursuant to the terms and
conditions of the ASR Agreement. The final settlement of the ASR Agreement is expected to be completed in the fourth quarter of 2026.
At final settlement of the ASR Agreement, the Company…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-03-09，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1082554/000110465926025331/tm268321d1_8k.htm｜as_of：2026-03-09
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On March 8, 2026, the Board of Directors (the Board)
of United Therapeutics Corporation (the Company) approved a share repurchase program (the Share Repurchase Program), authorizing
the purchase by the Company of up to $2.0 billion of the Company’s common stock (Common Stock) before March 9, 2027.
On March 9, 2026, the Company entered into two
accelerated share repurchase agreements (the ASR Agreements) with Citibank, N.A. (Citi) to repurchase approximately $1.5
billion in the aggregate of Common Stock under the Share Repurchase Program.
Under the terms of the ASR
Agreements, which comprise a $750 million uncollared agreement (the Uncollared ASR) and a $750 million collared agreement (the
Collared ASR), the Company will make an aggregate upfront payment of $1.5 billion to Citi on or before March 11, 2026.
Uncollared ASR
Under the Uncollared ASR, which is being entered
into pursuant to the Master Confirmation between the Company and Citi, dated March 25, 2024, the Company will receive an initial delivery
of approximately 992,120 shares of Common Stock on March 11, 2026 representing approximately 70% of the total shares that would be repurchased
under the Uncollared ASR, measured based on the closing price of the Common Stock on March 9, 2026.
The exact number of shares that the Company will…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-10-22，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1082554/000110465926117964/tm2628087d1_8k.htm｜as_of：2026-10-22
<<<
Item 8.01. Other Events.
On October 21, 2026, the Board of Directors of
United Therapeutics Corporation (the Company) approved a share repurchase program (the Share Repurchase Program), authorizing
the purchase by the Company of up to $2.0 billion of the Company’s common stock. This authorization will remain in effect for a
one-year period ending October 21, 2027.
On October 22, 2026, the Company issued a press
release announcing the Share Repurchase Program. A copy of the press release is attached as Exhibit 99.1 to this Current Report on Form
8-K and is incorporated herein by reference.
Item 9.01. Financial Statements and Exhibits.
(d) Exhibits
Exhibit No.
Description of Exhibit
99.1
Press Release dated October 22, 2026
104
Cover page Interactive Data File - the cover page XBRL tags are embedded within the inline XBRL document.
2
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
