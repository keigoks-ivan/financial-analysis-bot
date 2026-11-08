你是 stock-analyst v20 DD 的證據採集子 agent。標的：CW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - CW Curtiss-Wright acquisition merger 2025 2026
  - CW Curtiss-Wright class action lawsuit securities fraud
  - CW Curtiss-Wright clinical trial FDA approval 2025 2026
  - CW Curtiss-Wright product launch recall warning letter
  - CW Curtiss-Wright SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm｜as_of：2026-02-12
<<<
Item 3. Legal Proceedings.
From time to time, we are involved in legal proceedings that are incidental to the operation of our business. Some of these proceedings allege damages relating to asbestos and environmental exposures, intellectual property matters, copyright infringement, personal injury claims, employment and employee benefit matters, government contract issues, commercial or contractual disputes, and acquisitions or divestitures. We continue to defend vigorously against all claims. Although the ultimate outcome of any legal matter cannot be predicted with certainty, based on present information, including assessment of the merits of the particular claim, as well as current accruals and insurance coverage, we do not believe that the disposition of any of these matters, individually or in the aggregate, will have a material adverse effect on our consolidated financial condition, results of operations, and cash flows.
We have been named in pending lawsuits that allege injury from exposure to asbestos. To date, we have not been found liable or paid any material sum of money in settlement in any asbestos-related case. We believe that the minimal use of asbestos in our past operations and the relatively non-friable condition of asbestos in our products make it unlikely that we will face material liability in any asbestos litigation, whether individually or in the aggregate. We maintain insurance coverage for these potential liabilities and we believe adequate coverage exists to cover any unanticipated asbestos liability.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm｜as_of：2026-02-12
<<<
From time to time, we are involved in lawsuits and regulatory actions brought or threatened against us in the ordinary course of business. These actions and proceedings may involve claims for, among other things, asbestos and environmental exposures, intellectual property matters, copyright infringement, compensation for alleged personal injury, workers’ compensation, employment and employee benefit matters, government contract issues, commercial or contract disputes, and acquisitions or divestitures. We also may be subject to class action lawsuits, such as those involving allegations of violations of the Fair Labor Standards Act and state wage and hour laws. Due to the inherent uncertainties of litigation, the ultimate outcome is difficult to assess or quantify, as plaintiffs may seek recovery of very large or indeterminate amounts in these types of lawsuits, including punitive damages, civil penalties, consequential damages or other losses, or injunctive or declaratory relief, and the magnitude of the potential loss may remain unknown for substantial periods of time. These proceedings could also result in substantial cost to defend ourselves and may require us to devote substantial employee resources, which could distract our management from the operation of our business. Moreover, any insurance or indemnification rights that we may have may be insufficient or unavailable to protect us against such losses.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm｜as_of：2026-02-12
<<<
The cost of settlements/curtailments indicated above represents events that are accounted for under guidance on employers’ accounting for settlements and curtailments of defined benefit pension plans. In 2025, the Company recognized settlement charges related to the retirement of a former executive.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm｜as_of：2026-02-12
<<<
8-K February 3, 2005 3.1 Amended and Restated Certificate of Incorporation 8-A12B/A May 24, 2005 3.2 Amended and Restated By-Laws 8-K May 18, 2015 4.1 Form of stock certificate for Common Stock 8-A12B/A May 24, 2005 4.2 Description of Registrant’s Securities DEF 14A April 5, 2005 10.1 Form of Restricted Stock Unit Grant Agreement* 10-K February 13, 2025 10.2 Form of Performance Share Plan Grant Agreement* 10-K February 13, 2025 10.3 Form of Cash-Based Performance Unit Grant Agreement* 10-K February 13, 2025 10.4 Revised Standard Employment Severance Agreement with Senior Management of the Registrant* 10-K February 25, 2021 10.5 Amended and Restated Retirement Benefits Restoration Plan as amended January 1, 2009.* 10-K February 25, 2011 10.6 Instrument of Amendment No. 1 to Amended and Restated Retirement Benefits Restoration Plan as amended January 1, 2009* 10-K February 24, 2012 10.7 Instrument of Amendment No. 2 to Amended and Restated Retirement Benefits Restoration Plan as amended January 1, 2009* 10-K February 19, 2015 83 10.8 Instrument of Amendment No. 3 to Amended and Restated Retirement Benefits Restoration Plan as amended January 1, 2009* 10-K February 19, 2015 10.9 Instrument of Amendment No.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000026324&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 5 份。
2026-11-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-06 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-09-22 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-09-14 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-19 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-11 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-20 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-08 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-07 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-12 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-11-21 8-K Items 8.01 Other Events
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-20，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026036955/cw-20260519.htm｜as_of：2026-05-20
<<<
Item 1.01. Entry into a Material Definitive Agreement
On May 19, 2026, Curtiss-Wright Corporation (the “Company”) entered into a Credit Agreement (the “Credit Agreement”) evidencing a new syndicated $1 billion revolving credit facility (the “Credit Facility”). The Credit Agreement was entered into by and among the Company and certain of its subsidiaries, as borrowers, the lenders party thereto, and JPMorgan Chase Bank, N.A., as administrative agent for the lenders. The obligations under the Credit Facility are guaranteed by certain other subsidiaries of the Company.
The Credit Facility, which matures on May 19, 2031, replaces the Company’s existing $750 million revolving credit facility under its existing Credit Agreement, entered into May 17, 2022, by and among the Company and certain of its subsidiaries, as borrowers, the lenders party thereto, and JPMorgan Chase Bank, N.A., as administrative agent for the lenders (the “Terminated Credit Facility”), which was terminated concurrent with the Company’s entry into the Credit Facility. The Terminated Credit Facility was scheduled to mature on May 17, 2027. No early termination penalties or fees were incurred by the Company as a result of the termination of the Terminated Credit Facility. Certain letters of credit issued and outstanding under the Terminated Credit Facility remain outstanding and are deemed issued under the Credit Facility.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-09-14，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026061788/cw-20260910.htm｜as_of：2026-09-14
<<<
Item 8.01 Other Events
On September 10, 2026, Curtiss-Wright Corporation’s (the “Company”) Board of Directors authorized the Company to repurchase up to an additional $510 million of its common stock. The total available authorization is $700 million, including $190 million of remaining availability under the Company’s previously announced share repurchase authorizations.
Share repurchases may be made through a variety of methods, which could include open market purchases, accelerated share repurchase transactions, negotiated block transactions, 10b5-1 plans, other transactions that may be structured through investment banking institutions or privately negotiated, or a combination of the foregoing. The repurchase authorization does not have an expiration date and may be amended, discontinued, or terminated by the Company’s Board of Directors at any time without prior notice. The timing, price, and volume of share repurchases will depend on market conditions, relevant securities laws, and corporate, tax, regulatory and other relevant considerations. The Company presently expects to repurchase outstanding shares from time to time to offset the dilutive impact of employee equity-based compensation plans, but the Company also may make discretionary, opportunistic share repurchases.
On September 10, 2026, the Company entered into a written trading plan under Rule 10b5-1 of the Securities Exchange Act of 1934, as amended (the “Exchange Act”).…
>>>

[8] 來源：SEC EDGAR｜文件：8-K（2026-08-19，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026057855/cw-20260818.htm｜as_of：2026-08-19
<<<
Item 8.01 Other Events
On August 18, 2026, Curtiss-Wright Corporation (the “Company”) entered into a written trading plan under Rule 10b5-1 of the Securities Exchange Act of 1934, as amended (the “Exchange Act”). The Company implemented this written trading plan in connection with its previously announced share repurchase programs, under which the total amount available for repurchases under current authorizations is $390 million.
The trading plan will include purchases in the total amount of $100 million. The number of shares of Company common stock to be purchased on any purchase day will be up to the maximum daily target volume allowable under Rule 10b-18 of the Exchange Act. This written trading plan will not be effected before August 18, 2026, and will cease upon full use of the $100 million, which is expected to occur by the end of August 2026. Following completion of this plan, the Company expects to have $290 million in authorization remaining.
Adopting a trading plan that satisfies the conditions of Rule 10b5-1 allows a company to repurchase its shares at times when it might otherwise be prevented from doing so due to self-imposed trading blackout periods or pursuant to insider trading laws.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
