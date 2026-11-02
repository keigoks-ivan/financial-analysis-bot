你是 stock-analyst v20 DD 的證據採集子 agent。標的：V。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - V Visa acquisition merger 2025 2026
  - V Visa class action lawsuit securities fraud
  - V Visa clinical trial FDA approval 2025 2026
  - V Visa product launch recall warning letter
  - V Visa SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-06）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm｜as_of：2025-11-06
<<<
Item 3 Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-06）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm｜as_of：2025-11-06
<<<
Litigation Risks We may be adversely affected by the outcome of litigation or investigations. We are subject to numerous litigation matters, investigations, claims, examinations, information gathering requests, subpoenas, government and regulatory proceedings asserted by civil litigants, governments and enforcement bodies investigating or alleging, among other things, violations of competition and antitrust law, consumer protection law, privacy law and intellectual property law (these are referred to as “actions” in this section). Details of the most significant actions we face are described more fully in Note 20—Legal Matters to our consolidated financial statements included in Item 8 of this report. These actions are inherently uncertain, expensive and disruptive to our operations. In the event we are found liable or reach a settlement in any action, particularly in a large class action lawsuit, such as one involving an antitrust claim entitling the plaintiff to treble damages in the U.S., or we incur liability arising from a government investigation, we may be required to pay significant awards or judgments, settlements, costs or fines.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-06）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm｜as_of：2025-11-06
<<<
On August 8, 2022, the district court in Mackmin granted plaintiffs’ motion for final approval of a class action settlement with the three financial institution defendants and entered final judgments of dismissal as to those institutions. On June 23, 2025, the district court in Mackmin granted plaintiffs’ motion for final approval of a class action settlement and entered final judgments of dismissal as to Visa and Mastercard.

Visa and Mastercard entered a class settlement agreement with plaintiffs, and the court granted preliminary approval of that settlement on October 17, 2025.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-06）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm｜as_of：2025-11-06
<<<
10-K 001-33977 10.14 11/21/2014 10.15 Second Amendment, dated October 22, 2015, to Omnibus Agreement regarding Interchange Litigation Judgment Sharing and Settlement Sharing 10-K 001-33977 10.17 11/20/2015 10.16 Settlement Agreement, dated October 19, 2012, by and among Visa Inc., Visa U.S.A. Inc., Visa International Service Association, Mastercard Incorporated, Mastercard International Incorporated, various U.S. financial institution defendants, and the class plaintiffs to resolve the class plaintiffs’ claims in the matter styled In re Payment Card Interchange Fee and Merchant Discount Antitrust Litigation, No. 05-MD-1720 10-Q 001-33977 10.3 2/6/2013 10.17 Superseding and Amended Settlement Agreement, dated September 17, 2018, by and among Visa Inc., Visa U.S.A. Inc., Visa International Service Association, Mastercard Incorporated, Mastercard International Incorporated, various U.S. financial institution defendants, and the damages class plaintiffs to resolve the damages class plaintiffs’ claims in the matter styled In re Payment Card Interchange Fee and Merchant Discount Antitrust Litigation, No. 05-MD-1720 8-K 001-33977 10.1 9/18/2018 10.18 Form of Makewhole Agreement S-4/A 333-276747 99.2 3/11/2024 10.19 Loss Sharing Agreement, dated as of November 2, 2015, among the UK Members listed on Schedule 1 thereto, Visa Inc.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001403161&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 16 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 12 份。
2026-10-27 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-23 8-K Items 8.01 Other Events
2026-07-28 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-15 8-K Items 5.03 Amendments to Articles or Bylaws；9.01 Financial Statements and Exhibits
2026-06-26 8-K Items 8.01 Other Events
2026-05-12 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-11 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-28 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-27 8-K Items 8.01 Other Events
2026-02-13 8-K Items 7.01 Regulation FD Disclosure
2026-02-12 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-01-28 8-K Items 5.03 Amendments to Articles or Bylaws；5.07 Submission of Matters to a Vote of Security Holders
2025-12-30 8-K Items 8.01 Other Events
2025-12-23 8-K Items 8.01 Other Events
2025-11-10 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-12，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1403161/000119312526219432/d64238d8k.htm｜as_of：2026-05-12
<<<
Item 1.01  Entry into a Material Definitive Agreement.
On May 12, 2026, Visa Inc. (“Visa”) settled its previously announced exchange offer (the “Exchange Offer”) for any and all outstanding shares of its Class B-1 and Class B-2 common stock, the terms of which were described in the prospectus, dated April 13, 2026, constituting part of Visa’s registration statement on Form S-4, as amended (File No. 333-294062).
In connection with the Exchange Offer, Visa entered into makewhole agreements (collectively, the “Makewhole Agreements”), effective May 11, 2026, with the holders of the Class B-1 common stock and Class B-2 common stock accepted in the Exchange Offer and, where applicable, such holders’ respective parent guarantors.
Under the Makewhole Agreements, each participating holder is obligated, after the value of the Class B-3 common stock it received in the Exchange Offer has been depleted through downward conversion rate adjustments, to reimburse Visa in cash for the portion of any future deposit into the U.S. covered litigation escrow account that, but for the holder’s participation in the Exchange Offer, would have been absorbed by such holder through downward adjustments to the conversion rate of the Class B-1 common stock or Class B-2 common stock, as applicable, it tendered in the Exchange Offer.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-10-27，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1403161/000140316126000126/v-20261027.htm｜as_of：2026-10-27
<<<
Item 8.01 Other Events.
On October 27, 2026, the Company’s board of directors declared a quarterly cash dividend in the amount of $0.780 per share of class A common stock (determined in the case of all other outstanding common and preferred stock on an as-converted basis), payable on December 1, 2026, to all holders of record as of November 10, 2026.
Item 9.01 Financial Statements and Exhibits.
(d) Exhibits
Exhibit
Number Description
99.1
Earnings Release of Visa Inc., dated October 27, 2026
104 Cover Page Interactive Data File (formatted as Inline XBRL)
>>>

[8] 來源：SEC EDGAR｜文件：8-K（2026-09-23，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1403161/000140316126000121/v-20260918.htm｜as_of：2026-09-23
<<<
Item 8.01 Other Events.
On September 18, 2026, Visa Inc. (the “Company”) authorized the deposit of $405 million into the U.S. litigation escrow account previously established under the Company’s U.S. retrospective responsibility plan (the “Plan”). Under the terms of the Plan, when the Company funds the U.S. litigation escrow account, the value of the Company’s class B-1, B-2, and B-3 common stock, which are held predominantly by U.S. financial institutions and their affiliates and successors, are subject to dilution through downward adjustments to the conversion rates of the class B-1 to class A common stock, class B-2 to class A common stock, and class B-3 to class A common stock. This deposit resulted in the decrease in the conversion rate applicable to the Company’s class B-1 common stock from 1.5445 to 1.5400, the decrease in the conversion rate applicable to the Company’s class B-2 common stock from 1.5014 to 1.4924, and the decrease in the conversion rate applicable to the Company's class B-3 common stock from 1.4953 to 1.4773, effective as of September 18, 2026.
The conversion rate adjustments have the same effect on earnings per share as repurchasing the Company’s class A common stock.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/V_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
