你是 stock-analyst v20 DD 的證據採集子 agent。標的：AXTI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - AXTI AXT acquisition merger 2025 2026
  - AXTI AXT class action lawsuit securities fraud
  - AXTI AXT clinical trial FDA approval 2025 2026
  - AXTI AXT product launch recall warning letter
  - AXTI AXT SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
Item 3. Legal Proceedings
From time to time we may be involved in judicial or administrative proceedings concerning matters arising in the ordinary course of business. We do not expect that any of these matters, individually or in the aggregate, will have a material adverse effect on our business, financial condition, cash flows or results of operations.
Shareholder Class Action
On May 6, 2024, a putative shareholder class action complaint was filed in the U.S. District Court for the Eastern District of New York on behalf of persons or entities who purchased or acquired our publicly traded securities, against us, Morris S. Young, our Chief Executive Officer, and Gary L. Fischer, our Chief Financial Officer. The court transferred the case to the Northern District of California, where our headquarters are located. A lead plaintiff has been appointed and an amended complaint was filed. The amended complaint asserts a putative class period from March 24, 2021 and April 3, 2024, inclusive (the “Class Period”). The amended complaint alleges violations of Sections 10(b) and 20(a) of the Securities Exchange Act of 1934, as amended (the “Exchange Act”), and Rule 10b-5 promulgated thereunder by the defendants, and seeks unspecified monetary relief, interest, and attorneys’ fees. Defendants’ motion to dismiss is fully briefed and pending before the Court.
Derivative Action
On August 22, 2024, a derivative lawsuit was filed in the Northern District of California by an alleged shareholder against Morris S. Young, our Chief Executive Officer, Gary L. Fischer, our Chief Financial Officer, then-serving directors David C. Chang, Jesse Chen, and Christine Russell, and former director Leonard J. LeBlanc, with the Company named as a nominal defendant (together, “Defendants”). Defendants moved to dismiss on November 6, 2024, following which the plaintiff filed an amended complaint on November 20, 2024. The amended complaint asserted that the Defendants breached their fiduciary duties to the Company based on the allegations asserted in the original complaint in the putative shareholder class action. On November 27, 2024, Defendants again moved to dismiss.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
In 2005, a complaint was filed against us alleging personal injury, general negligence, intentional tort, wage loss and other damages, including punitive damages, as a result of exposure of plaintiffs to high levels of gallium arsenide in gallium arsenide wafers, and methanol. Other current and/or former employees could bring litigation against us in the future. Although we have in place engineering, administrative and personnel protective equipment programs to address these issues, our ability to expand or continue to operate our present locations could be restricted or we could be required to acquire costly remediation equipment or incur other significant expenses if we were found liable for failure to comply with environmental and safety regulations. Existing or future changes in laws or regulations in the United States or China may require us to incur significant expenditures or liabilities, or may restrict our operations. In addition, our employees could be exposed to chemicals or other hazardous materials at our facilities and we may be subject to lawsuits seeking damages for wrongful death or personal injuries allegedly caused by exposure to chemicals or hazardous materials at our facilities.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：Item 3. Legal Proceedings（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
​ Shareholder Class Action ​ On May 6, 2024, a putative shareholder class action complaint was filed in the U.S. District Court for the Eastern District of New York on behalf of persons or entities who purchased or acquired our publicly traded securities, against us, Morris S. Young, our Chief Executive Officer, and Gary L. Fischer, our Chief Financial Officer. The court transferred the case to the Northern District of California, where our headquarters are located. A lead plaintiff has been appointed and an amended complaint was filed. The amended complaint asserts a putative class period from March 24, 2021 and April 3, 2024, inclusive (the “Class Period”). The amended complaint alleges violations of Sections 10(b) and 20(a) of the Securities Exchange Act of 1934, as amended (the “Exchange Act”), and Rule 10b-5 promulgated thereunder by the defendants, and seeks unspecified monetary relief, interest, and attorneys’ fees. Defendants’ motion to dismiss is fully briefed and pending before the Court.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
​ Second Amended and Restated By Laws 3.6(6) ​ Amended and Restated Section 5.1 of Article V of the Second Amended and Restated Bylaws of AXT, Inc.
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001051627&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 19 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 7 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-28 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-29 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-07-29 8-K Items 3.03 Material Modification to Rights of Security Holders；5.03 Amendments to Articles or Bylaws；9.01 Financial Statements and Exhibits
2026-07-22 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-07-08 8-K Items 2.04 Triggering Events That Accelerate an Obligation
2026-07-02 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-06-22 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-17 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-06-09 8-K Items 3.03 Material Modification to Rights of Security Holders；5.03 Amendments to Articles or Bylaws；5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-15 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-21 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-20 8-K Items 2.02 Results of Operations and Financial Condition
2026-02-19 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-29 8-K Items 5.02 Departure/Election of Directors or Officers
2026-01-09 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-30 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-10-28，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1051627/000121390026113058/ea0309774-8k_axt.htm｜as_of：2026-10-28
<<<
Item 1.01 Entry into a Material Definitive
Agreement
On October 27, 2026, Tongmei and AXT, as Tongmei’s controlling shareholder, entered into a Share Subscription Agreement, a Supplemental
Agreement (Investor’s Rights Agreement) and a Redemption Support Agreement (collectively, the “Agreements”) with BNK-B3
HK Holdings Limited, a limited liability company duly established and validly existing under the laws of Hong Kong, which entity is managed
by a leading Asia asset manager (the “Lead Investor”), and certain institutional investors, including an institutional investor
who is an affiliate of an existing customer (collectively, the “Investors”). The Agreements provide for an investment by the
Investors of a minimum of RMB 1,912,350,000 (approximately US$285 million) (the “Minimum Amount”) and up to a maximum of RMB
3,668,639,053.25 (approximately US$545 million) (the “Maximum Amount”) in the ordinary shares of Tongmei, subject to customary
closing conditions. Concurrently with the Agreements, AXT agreed to recapitalize Tongmei by subscribing for 342,998,797 ordinary shares
for the RMB equivalent of US$400 million on or prior to the closing of transactions contemplated by the Agreements. Tongmei intends to
use the proceeds for further expansion of its manufacturing capacity for its indium phosphide semiconductor substrates, expansion of its
principal business operations, capital expenditures and general working capital. Assuming the Maximum Amount of the investment, AXT will…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-07-29，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926024883/axti20260715_8k.htm｜as_of：2026-07-29
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On July 26, 2026, AXT Inc., a Delaware corporation, (the “Registrant”, and collectively with its affiliates, “AXT”) and Lumentum Operations LLC, a Delaware limited liability company (collectively with its affiliates, “Lumentum”) entered into a Capacity Reservation Agreement (the “Agreement”) for the supply and capacity reservation of indium phosphide (“InP”) wafer substrates (the “Products”). Under the terms of the Agreement, AXT has agreed to reserve a minimum annual commitment of the Products by Lumentum (the “Product Capacity”) for a six (6) year period beginning upon entry into the Agreement and to support any additional capacity that may be required. The Agreement may be renewed for additional one (1) year periods.
In consideration for the reservation of the Product Capacity, Lumentum has agreed to pay AXT (i) an initial deposit of $43,500,000, due within thirty (30) business days after entry into the Agreement, and (ii) a second deposit of $43,500,000, with the timing and terms surrounding payment to be subsequently determined during calendar year 2028. The deposits shall be applied as shipment credits towards the purchase of the Products, until such deposit is exhausted.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
