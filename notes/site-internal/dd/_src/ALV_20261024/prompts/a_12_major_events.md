你是 stock-analyst v20 DD 的證據採集子 agent。標的：ALV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - ALV Autoliv acquisition merger 2025 2026
  - ALV Autoliv class action lawsuit securities fraud
  - ALV Autoliv clinical trial FDA approval 2025 2026
  - ALV Autoliv product launch recall warning letter
  - ALV Autoliv SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
Item 3. Legal Proceedings
In the ordinary course of its business, the Company is subject to legal proceedings brought by or against the Company and its subsidiaries.
See Note 19, Contingent Liabilities, to the Consolidated Financial Statements in this Annual Report for a summary of certain ongoing legal proceedings. Such information is incorporated into this Part I, Item 3 – “Legal Proceedings” by reference.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
We are involved from time to time in legal proceedings and our business may suffer as a result of adverse outcomes of current or future legal proceedings We are, from time to time, involved in litigation, regulatory proceedings, and commercial or contractual disputes that may be significant. These matters may include, without limitation, disputes with our suppliers and customers, intellectual property claims, shareholder litigation, government investigations, class action lawsuits, personal injury claims, product liability claims, environmental issues, antitrust, customs and VAT disputes, employment, and tax issues. In such matters, government agencies or private parties may seek to recover from us very large, indeterminate amounts in penalties or monetary damages (including, in some cases, treble or punitive damages) or seek to limit our operations in some way. The possibility exists that claims may be asserted against us and their magnitude may remain unknown for long periods of time. For example, we are currently in the early stages of a dispute with the Mexican tax authorities in relation to various issues dealing with certain manufacturing activities that occur in Mexico. An adverse result in this or other similar disputes could have a materially negative impact on our operating results and financial condition.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
The trial associated with the lawsuit in the UK concluded and a ruling in the proceeding was in favor of the Company. On February 21, 2025, the United Kingdom Competition Appeal Tribunal unanimously dismissed plaintiffs' claims against the Company.

Product Liability: Autoliv and some of its subsidiaries have been named as one of several defendants in a consolidated class action lawsuit in a multi-district litigation (In Re: ARC Airbag Inflators Products Liability Litigation MDL, No. 3051) in the Northern District of Georgia. The plaintiffs in the multi-district litigation (the "ARC Inflator Class Action") brought claims for fraud, breach of warranty, and violations of consumer protection and trade practices stemming from ARC inflators included in airbag modules that Autoliv or its subsidiaries allegedly supplied after Autoliv acquired certain Delphi assets (the “Delphi Acquisition”) in December 2009. The Company denies these allegations. Autoliv is not aware of any performance issues regarding ARC inflators included with its airbags at the directions of its customers that it shipped following the Delphi Acquisition. The proceedings remain ongoing. The Company has determined pursuant to ASC 450 that a loss is reasonably possible with respect to the ARC Inflator Class Action. However, the Company continues to evaluate this matter, no accrual has been made, and no estimated range of potential loss can be determined at this time. The Company cannot predict the ultimate outcome of the ARC Inflator Class Action.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001034670&type=8-K｜as_of：2026-10-24
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-23 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-17 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-30 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-05-11 8-K Items 2.05 Costs Associated with Exit or Disposal Activities；2.06 Material Impairments；5.07 Submission of Matters to a Vote of Security Holders；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-17 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-11 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-20 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-01-30 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-29 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2025-11-12 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2025-10-29 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-05-11，Item 2.06）｜章節：8-K Item 2.06 Material Impairments｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526216107/alv-20260506.htm｜as_of：2026-05-11
<<<
Item 2.06 Material Impairments.
The information contained in Item 2.05 above is incorporated herein by reference.
Item 5.07 Submission of Matters to a Vote of Security Holders.
On May 7, 2026, the Company held its 2026 Annual Meeting of Stockholders (the “Annual Meeting”), where a total of 74,862,203 shares were represented in person or by valid proxy. The proposals presented at the Annual Meeting are described in detail in the Company’s Definitive Proxy Statement for the Annual Meeting, which was filed with the Securities and Exchange Commission on March 25, 2026. At the Annual Meeting, the Company’s stockholders took the following actions:
Election of Directors
Mr. Mikael Bratt, Ms. Laurie Brlas, Mr. Jan Carlson, Mr. Leif Johansson, Ms. Adriana Karaboutis, Mr. Frédéric Lissalde, Dr. Xiaozhi Liu, Mr. Gustav Lundgren, and Mr. Thaddeus Senko were each elected to the Company’s board of directors (the “Board”) for a one-year term until the 2027 annual meeting of stockholders.
The votes cast were as follows:
Mr. Mikael Bratt:
Ms. Laurie Brlas:
Mr. Jan Carlson:
Mr. Leif Johansson:
Ms. Adriana Karaboutis:
Mr. Frédéric Lissalde:
Dr. Xiaozhi Liu:
Mr. Gustav Lundgren:
Mr. Thaddeus Senko:
53,232,327 votes for, and 504,185 withheld.
53,208,971 votes for, and 527,541 withheld.
51,816,134 votes for, and 1,920,378 withheld.
51,643,917 votes for, and 2,092,595 withheld.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-10-29，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312525254662/alv-20251029.htm｜as_of：2025-10-29
<<<
Item 1.01 Entry into a Material Definitive Agreement
The information contained in Item 2.03 of this Current Report on Form 8-K is incorporated by reference into this Item 1.01.
Item 2.03 Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant
On October 29, 2025, Autoliv, Inc. (the “Issuer”) issued EUR 300,000,000 of notes due October 29, 2030 (the “Notes”). The Notes have a coupon rate of 3.000% per annum, and the issue price of the Notes was 99.771% of the aggregate nominal amount of the Notes. The Notes were offered to third parties in denominations of EUR 100,000 and increments of EUR 1,000 above that. Autoliv ASP, Inc. (the “Guarantor”) is guarantor of all payments due in respect of the Notes. An amount equivalent to the net proceeds from the offering of the Notes will be allocated to new or existing Eligible Projects which fall within the following Eligible Categories: Clean Transportation, Renewable Energy, Energy Efficiency or De-carbonization of Operations and Products.
The Notes were issued pursuant to the Pricing Supplement, dated October 27, 2025 (the “Pricing Supplement”), which supplements the base listing particulars (the “Base Listing Particulars”) of the Issuer’s EUR 3,000,000,000 guaranteed medium term note programme dated March 14, 2025 (the “EMTN Programme”).…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2025-11-12，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312525276259/alv-20251110.htm｜as_of：2025-11-12
<<<
Item 8.01 Other Events.
Fourth Quarter Dividend
In a press release dated November 10, 2025, the Company announced that the Board declared a quarterly dividend of $0.87 cents per share for the fourth quarter of 2025. The dividend will be payable on Wednesday, December 10, 2025 to the holders of Company common stock and on Thursday, December 11, 2025 to the holders of the Company's Swedish Depository Receipts. The dividend payments will be made to holders of record on the close of business on Friday, November 21, 2025.
A copy of the press release dated November 10, 2025 regarding the fourth quarter dividend is filed as Exhibit 99.1 to this report and is incorporated herein by reference.
Item 9.01 Financial Statements and Exhibits.
(d) EXHIBITS
99.1
Press Release of Autoliv, Inc. dated November 10, 2025 (Q4 2025 Dividend).
104
Cover Page Interactive Data File (embedded within the Inline XBRL document).
EXHIBIT INDEX
Exhibit No.
Description
99.1
Press Release of Autoliv, Inc. dated November 10, 2025 (Q4 2025 Dividend).
104
Cover Page Interactive Data File (embedded within the Inline XBRL document).
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
