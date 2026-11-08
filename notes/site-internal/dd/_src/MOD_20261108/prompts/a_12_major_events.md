你是 stock-analyst v20 DD 的證據採集子 agent。標的：MOD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - MOD Modine Manufacturing acquisition merger 2025 2026
  - MOD Modine Manufacturing class action lawsuit securities fraud
  - MOD Modine Manufacturing clinical trial FDA approval 2025 2026
  - MOD Modine Manufacturing product launch recall warning letter
  - MOD Modine Manufacturing SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
ITEM 3. LEGAL PROCEEDINGS.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 7. MD&A（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
In July 2025, we executed an amended and restated credit agreement with a syndicate of banks that provides for a multi-currency $400 million revolving credit facility and a $200 million term loan facility maturing in July 2030. This credit agreement modified our then-existing revolving credit and term loan facilities, which would have matured in October 2027. We also amended the agreement governing our Senior Notes, to conform the applicable terms to those of the aforementioned amended and restated credit agreement. In December 2025, we further amended the credit agreement primarily to increase the borrowing capacity under the revolving credit facility by $150 million to $550 million.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
​ Note 5: Stock-Based Compensation The Company’s stock-based compensation programs consist of the following: (i) a long-term incentive plan (“LTIP”) for officers and other executives that authorizes grants of stock awards, stock options, and performance-based awards granted for retention and performance, (ii) a discretionary equity program for other management and key employees, and (iii) stock awards for non-employee directors. The Company’s Board of Directors and the Human Capital and Compensation Committee, as applicable, have discretionary authority to set the terms of the stock-based awards. Grants to employees during fiscal 2026 were issued under the Company’s Amended and Restated 2020 Incentive Compensation Plan. In fiscal 2026, 2025 and 2024, the Company granted performance-based stock awards and restricted stock awards. At present, the Company settles equity-based grants through newly issued shares of common stock. As of March 31, 2026, approximately 1.0 million shares authorized under the Amended and Restated 2020 Incentive Compensation Plan remain available for future grants. Employee participants have the opportunity to deliver back to the Company the number of shares from the vesting of stock awards sufficient to satisfy the individual’s minimum tax withholding obligations. These shares are held as treasury shares. The Company recorded stock-based compensation expense of $22.1 million, $26.4 million, and $10.8 million in fiscal 2026, 2025 and 2024, respectively.…

Other litigation In the normal course of business, the Company and its subsidiaries are named as defendants in various lawsuits and enforcement proceedings by private parties, governmental agencies and/or others in which claims are asserted against Modine. The Company believes that any additional loss in excess of amounts already accrued would not have a material effect on the Company’s consolidated balance sheet, results of operations, and cash flows. In addition, management expects that the liabilities which may ultimately result from such lawsuits or proceedings, if any, would not have a material adverse effect on the Company’s financial position.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000067347&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 17 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。
2026-11-03 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-27 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-10-07 8-K/A Items 9.01 Financial Statements and Exhibits
2026-10-01 8-K Items 1.01 Entry into a Material Definitive Agreement；2.01 Completion of Acquisition or Disposition of Assets；5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-17 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-10 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-21 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-07-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-24 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-26 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-05 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-02-17 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-29 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2025-12-09 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2025-11-14 8-K Items 5.02 Departure/Election of Directors or Officers
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-10-01，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926112870/tm2626618d1_8k.htm｜as_of：2026-10-01
<<<
Item 2.01. Completion of Acquisition or Disposition of Assets.
The information set forth in the Introductory
Note to this Current Report on Form 8-K is incorporated by reference into this Item 2.01.
On the Closing Date, the Company completed the
disposition of the Performance Technologies Business, which constituted the Company’s Performance Technologies reportable segment,
through the Separation, the Distribution and the Merger. In the Transactions, the Company received the Cash Distribution and the Record
Date Shareholders received shares of Gentherm Common Stock as described in the Introductory Note. The term loan incurred by SpinCo to
fund the Cash Distribution is an obligation of SpinCo and, following the Merger, Gentherm and its subsidiaries, and not of the Company.
Effective as of the Effective Time, Paul A. Mascarenas,
the director designated by Modine pursuant to the Merger Agreement, was appointed to the Gentherm board of directors. Modine waived its
right to designate a second director.
Item 5.02. Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of
Certain Officers.
In connection with the completion of the Transactions,
and effective as of the Effective Time, Jeremy M. Patten ceased to serve as President, Performance Technologies of the Company in connection
with his transition to Gentherm.
Item 7.01. Regulation FD Disclosure.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-05，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926055654/mod-20260430x8k.htm｜as_of：2026-05-05
<<<
Item 1.01.Entry into a Material Definitive Agreement.
On April 30, 2026, Modine Manufacturing Company (the “Company”) and Airedale International Air Conditioning Limited, as borrowers (collectively, the “Borrowers”), entered into Amendment No. 2 (the “Amendment”) to the Sixth Amended and Restated Credit Agreement, dated as of July 10, 2025 (as previously amended, the “Credit Agreement”), by and among the Borrowers, the lenders party thereto, and JPMorgan Chase Bank, N.A., as administrative agent.
The Amendment modifies the Credit Agreement to, among other things, (i) permit the separation, disposition and spin-off of the Company’s Performance Technologies business and the related transactions contemplated by that certain Agreement and Plan of Merger, dated January 29, 2026 (collectively, the “PT Transaction”), and (ii) provide for the incurrence of indebtedness by a newly formed subsidiary in connection with the PT Transaction and the use of the proceeds thereof.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-01-29，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926008087/mod-20260129x8k.htm｜as_of：2026-01-29
<<<
Item 1.01.Entry into a Material Definitive Agreement.
On January 29, 2026, Modine Manufacturing Company, a Wisconsin corporation (the “Company” or “Modine”), entered into definitive agreements with Gentherm Incorporated, a Michigan corporation (“Gentherm”), pursuant to which the Company’s Performance Technologies business (the “Performance Technologies Business”) will be combined with Gentherm in a Reverse Morris Trust transaction. As a result of the transaction, the Company will receive $210 million in cash, subject to adjustment as described below, and the Company’s shareholders will own approximately 40% of the outstanding Gentherm common stock following the transaction, disregarding any shareholder overlap.
The transaction will occur through the following steps:
​
● First, the Company will separate (the “Separation”) the Performance Technologies Business from the remainder of the Company’s businesses so that the Performance Technologies Business is held by Platinum SpinCo Inc., a Delaware corporation and a wholly owned subsidiary of the Company (“SpinCo”).
​
● Second, in connection with the Separation, SpinCo will distribute $210 million in cash to the Company, with the amount of such distribution subject to adjustment for cash, working capital and indebtedness of SpinCo subject to decrease if additional shares of Gentherm common stock will be issued to the Company shareholders to meet the Tax Threshold (as described below).
​…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
