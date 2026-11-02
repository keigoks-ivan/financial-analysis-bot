你是 stock-analyst v20 DD 的證據採集子 agent。標的：STX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - STX Seagate Technology Holdings acquisition merger 2025 2026
  - STX Seagate Technology Holdings class action lawsuit securities fraud
  - STX Seagate Technology Holdings clinical trial FDA approval 2025 2026
  - STX Seagate Technology Holdings product launch recall warning letter
  - STX Seagate Technology Holdings SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-04）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1137789/000113778926000159/stx-20260703.htm｜as_of：2026-08-04
<<<
ITEM 3.LEGAL PROCEEDINGS
See “Item 8. Financial Statements and Supplementary Data—Note 12. Legal, Environmental and Other Contingencies”.
Table of Contents
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-04）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1137789/000113778926000159/stx-20260703.htm｜as_of：2026-08-04
<<<
We are subject from time-to-time to legal proceedings and claims, including claims of alleged infringement of the patents, trademarks and other intellectual property rights of third parties by us, or our customers, in connection with the manufacturing, use, sale or offering for sale of our products. Intellectual property litigation can be expensive and time-consuming, regardless of the merits of any claim, and could divert management’s attention and resources away from our business. In addition, intellectual property lawsuits are subject to inherent uncertainties due to the complexity of the technical issues involved, which may cause actual results to differ materially from our expectations. Some of the actions that we face from time-to-time seek injunctions against the sale of our products and/or substantial monetary damages, which, if granted or awarded, could materially harm our business, financial condition and operating results.

In addition, in the past, following periods of decline in the market price of a company’s securities, class action lawsuits have often been pursued against that company. Similar litigation has been pursued against us, and it could result in substantial costs and a diversion of management’s attention and resources, which could materially and adversely affect our results of operations, financial condition and liquidity.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-04）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1137789/000113778926000159/stx-20260703.htm｜as_of：2026-08-04
<<<
In re Seagate Technology Holdings plc Securities Litigation. On July 10, 2023 and July 26, 2023, two securities class action lawsuits were filed in the U.S. District Court for the Northern District of California against Seagate Technology Holdings plc, Dr. William D. Mosley, and Gianluca Romano. The cases were consolidated on September 25, 2023. On September 12, 2024, the plaintiffs filed the currently operative complaint, asserting claims under Sections 10(b) and 20(a) of the Securities Exchange Act of 1934 and SEC Rule 10b-5, and a class period between September 14, 2020 and April 19, 2023, inclusive. On April 3, 2026, the parties agreed to a settlement in principle to resolve the matter for a total amount of $175 million, approximately $70 million of which will be paid by the Company’s insurers. The parties have since executed a stipulation of settlement. The Company recorded a charge of $105 million which was included in Legal settlement in its Consolidated Statements of Operations and Comprehensive Income. On July 7, 2026, the court granted preliminary approval of the settlement, and a final approval hearing will be held on November 17, 2026.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001137789&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 15 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 8 份。
2026-10-28 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-10-27 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-09 8-K Items 3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-04 8-K Items 5.02 Departure/Election of Directors or Officers
2026-07-28 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-12 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-28 8-K Items 3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-21 8-K Items 3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-06 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-04-28 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-19 8-K Items 3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-12 8-K Items 3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-01-27 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-13 8-K Items 3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-05 8-K Items 3.02 Unregistered Sales of Equity Securities；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-09，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1137789/000119312526385961/d109585d8k.htm｜as_of：2026-09-09
<<<
Item 8.01 is incorporated into this Item 3.02 by reference.
On September 8, 2026, Seagate Technology Holdings plc (the “Company” or “Seagate”) issued, and Seagate HDD Cayman (the “Issuer” or “Seagate HDD”), a subsidiary of Seagate, delivered 1,647,862 ordinary shares of Seagate, par value $0.00001 per share (the “Ordinary Shares”) to settle exchanges of $150.51 million aggregate principal amount of the Issuer’s outstanding 3.50% Exchangeable Senior Notes due 2028 (the “Notes”). The Ordinary Shares were issued and delivered in reliance upon the exemption from registration provided by Section 3(a)(9) of the Securities Act of 1933.
Item 7.01.
Regulation FD Disclosure.
On September 9, 2026, Seagate issued a press release regarding the Redemption (described below), a copy of which is attached as Exhibit 99.1 hereto.
The information in this Item 7.01 (including Exhibit 99.1 hereto) shall not be deemed “filed” for purposes of Section 18 of the Securities Exchange Act of 1934, as amended (the “Exchange Act”), or otherwise subject to the liabilities of that section, nor shall it be deemed incorporated by reference in any filing under the Securities Act of 1933, as amended, or the Exchange Act, except as expressly set forth by specific reference in such a filing.
Item 8.01
Other Events.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-06-12，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1137789/000119312526268170/d24300d8k.htm｜as_of：2026-06-12
<<<
Item 8.01
Other Events.
On June 11, 2026, Seagate HDD Cayman, a subsidiary of Seagate (the “Issuer” or “Seagate HDD”), issued a notice (the “Redemption Notice”) to holders of the Issuer’s 3.50% Exchangeable Senior Notes due 2028 (the “Notes”) calling for redemption (the “Redemption”) of all outstanding Notes.
On September 8, 2026 (the “Redemption Date”), all then-outstanding Notes that are called for Redemption and have not been submitted for exchange will be redeemed for cash at a price (the “Redemption Price”) equal to the principal amount of such Notes plus accrued and unpaid interest on such Notes to, but excluding, the Redemption Date. On the Redemption Date, the Redemption Price will become due and payable upon each note to be redeemed and interest thereon will cease to accrue on and after the Redemption Date (unless Seagate HDD fails to pay the Redemption Price due on the Redemption Date in full, in which case interest thereon will continue to accrue until such time as Seagate HDD pays such Redemption Price in full).
The Notes may be exchanged by holders at any time before 5:00 p.m.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-28，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1137789/000119312526243110/d106085d8k.htm｜as_of：2026-05-28
<<<
Item 8.01 is incorporated into this Item 3.02 by reference.
The Exchanges (as defined below) were conducted as private placements, and the aggregate of 2,023,124 ordinary shares issued in the Exchanges were issued pursuant to the exemption from the registration requirements of the Securities Act of 1933, as amended (the “Securities Act”), afforded by Section 4(a)(2) of the Securities Act in transactions not involving any public offering.
Item 7.01.
Regulation FD Disclosure.
On May 28, 2026, Seagate Technology Holdings Public Limited Company (the “Company”) issued a press release relating to the closing of the Exchanges.
The information in Item 7.01, including Exhibit 99.1, of this Current Report on Form 8-K is being furnished and shall not be deemed “filed” for purposes of Section 18 of the Securities Exchange Act of 1934, as amended (the “Exchange Act”), or otherwise subject to the liabilities of that section, nor shall it be deemed to be incorporated by reference into any filing of the Company under the Securities Act of 1933, as amended, or the Exchange Act, whether made before or after the date hereof, except as shall be expressly set forth by specific reference in such a filing.
Item 8.01
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20261102/parts/axes_2.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
