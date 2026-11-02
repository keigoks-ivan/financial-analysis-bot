你是 stock-analyst v20 DD 的證據採集子 agent。標的：APH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - APH Amphenol acquisition merger 2025 2026
  - APH Amphenol class action lawsuit securities fraud
  - APH Amphenol clinical trial FDA approval 2025 2026
  - APH Amphenol product launch recall warning letter
  - APH Amphenol SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926013549/aph-20251231x10k.htm｜as_of：2026-02-11
<<<
Item 3. Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926013549/aph-20251231x10k.htm｜as_of：2026-02-11
<<<
​ The Company is currently engaged in, or subject to, various customer claims, litigation and other regulatory and legal matters and may be subject to additional claims, litigation and other regulatory or legal proceedings in the future. Such matters expose the Company to risks that could be material, including, but not limited to, risks related to employment disputes, tax controversies, government investigations, intellectual property infringement, compliance with environmental laws, securities laws violations, unfair sales practices, product safety and liability, and product warranty, indemnity and other contract-related claims. These matters may subject the Company to lawsuits, voluntary or forced product recalls, government investigations and criminal liability, including claims for compensatory, punitive or consequential damages, and could result in diverting our management’s attention, disruptions to our business and significant legal expenses. These matters could also damage our reputation, harm our relationships with customers or negatively affect product demand.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 7. MD&A（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926013549/aph-20251231x10k.htm｜as_of：2026-02-11
<<<
​ On March 21, 2024, the Company entered into a third amended and restated credit agreement, which amended and restated its $2,500.0 unsecured revolving credit facility, increasing the lenders’ aggregate unsecured revolving commitments under the facility by $500.0 to $3,000.0 (the “Revolving Credit Facility”). The Revolving Credit Facility matures in March 2029 and gives the Company and certain of its subsidiaries the ability to borrow, in various currencies, at a spread that varies, based on the Company’s debt rating, over certain currency-specific benchmark rates, which benchmark rates, in the case of U.S. dollar borrowings, are either the base rate or the adjusted term Secured Overnight Financing Rate (“SOFR”). The Revolving Credit Facility was undrawn on the date it was amended and restated. The Company may utilize the Revolving Credit Facility for general corporate purposes. As of December 31, 2025 and 2024, there were no outstanding borrowings under the Revolving Credit Facility. The Revolving Credit Facility requires payment of certain annual agency and commitment fees and requires that the Company satisfy certain financial covenants. On December 31, 2025, the Company was in compliance with the financial covenants under the Revolving Credit Facility.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000820313&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 17 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 9 份。
2026-10-28 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-06 8-K Items 5.02 Departure/Election of Directors or Officers
2026-09-04 8-K Items 8.01 Other Events
2026-08-06 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-22 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-12 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-05-06 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-03-30 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-03-27 8-K/A Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-24 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-05 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-12 8-K Items 2.01 Completion of Acquisition or Disposition of Assets；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-08 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-10 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-01-12，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926002737/tm262701d1_8k.htm｜as_of：2026-01-12
<<<
Item 2.01.
Completion of Acquisition or Disposition of Assets.
On January 9, 2026, Amphenol Corporation,
a Delaware corporation (the “Company”), completed its acquisition of the Connectivity and Cable Solutions business of CommScope
Holding Company, Inc., a Delaware corporation (“CommScope”), for approximately $10.5 billion in cash, subject to customary
post-closing adjustments (the “Acquisition”), pursuant to the previously disclosed Purchase Agreement, dated as of August 3,
2025, by and between the Company and CommScope.
Item 7.01.
Regulation FD Disclosure.
On January 9, 2026, the Company issued a
press release announcing the closing of the Acquisition. A copy of the press release is furnished as Exhibit 99.1 to this Current
Report on Form 8-K.
The information
in this Item 7.01 of this Current Report on Form 8-K, including Exhibit 99.1, is being furnished herewith and shall not be deemed
“filed” for the purposes of Section 18 of the Securities Exchange Act of 1934, as amended (the “Exchange Act”),
or otherwise subject to the liabilities of that section, nor shall it be deemed incorporated by reference into any filing under the Securities
Act of 1933, as amended, or the Exchange Act, except as expressly set forth by specific reference in such filing.
Item 9.01.
Financial Statements and Exhibits.
(a)
Financial Statements of Businesses or Funds Acquired.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-12，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926059404/tm2613386d5_8k.htm｜as_of：2026-05-12
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On May 12, 2026,
Amphenol Corporation (the “Company”) issued and sold €600,000,000 aggregate principal amount of the Company’s
3.375% Senior Notes due 2029 (the “2029 Notes”) and €500,000,000 aggregate principal amount of the Company’s 3.875%
Senior Notes due 2034 (the “2034 Notes” and, together with the 2029 Notes, the “Notes”), pursuant to the Company’s
Registration Statement on Form S-3 (No. 333-293923) (the “Registration Statement”), including the related prospectus
dated March 2, 2026, as supplemented by the prospectus supplement dated May 5, 2026. The Notes were sold in an underwritten
public offering pursuant to an underwriting agreement, dated May 5, 2026, by and between the Company and Barclays Bank PLC, Citigroup
Global Markets Limited, Commerzbank Aktiengesellschaft, HSBC Bank plc, BNP PARIBAS, J.P. Morgan Securities plc, Mizuho International
plc, Standard Chartered Bank, ING Bank N.V., Belgian Branch and Siebert Williams Shank & Co., LLC.
The Company received
net proceeds from the offering of the Notes, after deducting the underwriting discounts and estimated offering expenses payable by the
Company, of approximately €1,093.1 million. The Company intends to use the net proceeds from the offering of the Notes to repay
borrowings under its U.S. commercial paper program and its 364-day unsecured delayed draw term loan credit agreement, and for general
corporate purposes.
The Notes were issued…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-06，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926055888/tm2613386d4_8k.htm｜as_of：2026-05-06
<<<
Item 1.01
Entry into a Material Definitive Agreement.
On
May 5, 2026, Amphenol Corporation (the “Company”) entered into an underwriting agreement (the “Underwriting Agreement”)
by and among the Company and Barclays Bank PLC, Citigroup Global Markets Limited, Commerzbank Aktiengesellschaft, HSBC Bank plc,
BNP PARIBAS, J.P. Morgan Securities plc, Mizuho International plc, Standard Chartered Bank, ING Bank N.V., Belgian Branch and Siebert
Williams Shank & Co., LLC, relating to the offer and sale of €600 million aggregate principal
amount of the Company’s 3.375% Senior Notes due 2029 (the “2029 Notes”) and €500 million aggregate principal amount
of the Company’s 3.875% Senior Notes due 2034 (the “the 2034 Notes” and, together with the 2029 Notes, the “Notes”).
The closing of the Notes offering (the “Notes
Offering”) is expected to occur on May 12, 2026, subject to the satisfaction of customary closing conditions.
A copy
of the Underwriting Agreement is attached hereto as Exhibit 1.1 and is filed herewith for purposes of incorporation by reference into
the Company’s Registration Statement (No. 333-293923).
The above
description of the Underwriting Agreement is qualified in its entirety by reference to the Underwriting Agreement, a copy of which is
attached as Exhibit 1.1 to this Current Report on Form 8-K and is incorporated by reference herein.
Item 8.01
Other Events.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APH_20261102/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
