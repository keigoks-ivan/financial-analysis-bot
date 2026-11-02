你是 stock-analyst v20 DD 的證據採集子 agent。標的：DASH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - DASH DoorDash acquisition merger 2025 2026
  - DASH DoorDash class action lawsuit securities fraud
  - DASH DoorDash clinical trial FDA approval 2025 2026
  - DASH DoorDash product launch recall warning letter
  - DASH DoorDash SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm｜as_of：2026-02-18
<<<
Item 3. Legal Proceedings
We are currently involved in, and may in the future be involved in, legal proceedings, claims, regulatory inquiries, audits, and governmental investigations (collectively, “Legal Proceedings”) in the ordinary course of business, including suits by merchants, consumers, Dashers, or other third parties (individually or as class actions).
The outcomes of our Legal Proceedings are inherently unpredictable and subject to significant uncertainties. When we determine that we have meritorious defenses to any claims asserted, we defend ourselves vigorously; however, we also consider settlement of disputes when, in management’s judgment, it is in the best interests of both DoorDash and its shareholders to do so. For some matters for which a material loss is reasonably possible, an estimate of the amount of loss or range of losses is not possible nor are we able to estimate the loss or range of losses that could potentially result from the application of nonmonetary remedies. Until the final resolution of Legal Proceedings, there may be an exposure to a material loss in excess of the amount recorded or non-monetary damages.
Except as set forth below, we are not, and have not been within the past 12 months, party to any material administrative, legal, or arbitration proceeding that may have or have had a significant effect on the financial position or profitability of DoorDash, and we are not aware of any such proceedings being pending or threatened.
Independent contractor classification matters
We have in the past been, are currently, and may in the future be subject to claims, lawsuits, arbitration proceedings, administrative actions, government investigations, and other legal and regulatory proceedings at the federal, state, and municipal levels challenging the classification of Dashers on our platform as independent contractors, and claims that, by the alleged misclassification, we have violated various labor and other laws that would apply to delivery employees. Laws and regulations that govern the status and classification of independent contractors are subject to change and divergent interpretations by various authorities, which can create uncertainty and unpredictability for us.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000013/dash-20251231.htm｜as_of：2026-02-18
<<<
We are subject to claims, lawsuits, arbitration proceedings, administrative actions, government investigations, and other legal and regulatory proceedings at the U.S. federal, state, and municipal levels, as well as in non-U.S. jurisdictions, challenging the classification of Dashers that utilize our platform as independent contractors. We are currently involved in, or may become involved in, a variety of actual or threatened claims, including those brought in arbitration or compelled pursuant to the terms of our independent contractor agreements to arbitration, challenging the classification of Dashers that utilize our platform as independent contractors.

We face potential liability, legal expenses, and harm to our business relating to the nature of our business generally, and with the delivery services we facilitate in particular. Specifically, we are subject to claims, lawsuits, arbitration proceedings, government investigations, audits, and demands, and other legal, regulatory, and administrative proceedings, including those involving personal injury, property damage, worker classification, labor and employment, anti-discrimination, commercial disputes, competition, consumer complaints, cybersecurity incidents, intellectual property disputes, marketing and advertising to merchants, consumers, and Dashers, compliance with regulatory requirements, and other matters, and we may become subject to additional types of claims, lawsuits, government investigations, and legal or regulatory proceedings as our business grows and as we deploy new products and services. We are also subject to claims, lawsuits, and other legal proceedings seeking to hold us vicariously liable for the actions of merchants, consumers, and Dashers.

The results of any such claims, lawsuits, arbitration proceedings, government investigations, audits, and demands, or other legal or regulatory proceedings cannot be predicted with any degree of certainty. Any claims against us, whether meritorious or not, could be time-consuming, result in costly litigation, be harmful to our reputation, require significant management attention, and divert significant resources. It is possible that a resolution of one or more such proceedings could result in substantial damages, settlement costs, fines, and penalties that could adversely affect our business, financial condition, and results of operations. Determining reserves for our pending litigation is a complex and fact-intensive process that requires significant subjective judgment and speculation. There is no guarantee that our litigation reserves will be sufficient to offset such liabilities. These proceedings could also result in harm to our reputation and brand, sanctions, consent decrees, injunctions, or other orders requiring a change in our business practices. Further, under certain circumstances, we have contractual and other legal obligations to indemnify and to incur legal expenses on behalf of our business and commercial partners and current and former directors and officers. Any of these outcomes and obligations could adversely affect our business, financial condition, and results of operations.
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001792789&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-29 8-K Items 1.01 Entry into a Material Definitive Agreement；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-18 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-11 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-06-12 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；8.01 Other Events
2026-05-06 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-18 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-01-20 8-K Items 5.02 Departure/Election of Directors or Officers
2025-11-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-10-29，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1792789/000114036126041111/ef20084547_8k.htm｜as_of：2026-10-29
<<<
Item 1.01
Entry into a Material Definitive Agreement.
Merger Agreement
On October 28, 2026, DoorDash, Inc., a Nevada corporation (“DoorDash”
or the “Company”), entered into an Agreement and Plan of Merger (the “Merger Agreement”) with Maplebear
Inc., a Delaware corporation (“Instacart”), and Ibiza Merger Sub, Inc., a Delaware corporation and wholly owned subsidiary of DoorDash (“Merger Sub”), pursuant to which, among other things, subject to its terms, Merger Sub will merge with and into Instacart, with Instacart continuing as the surviving corporation as a wholly owned subsidiary of
DoorDash (the “Merger”).
Subject to the terms and conditions of the Merger Agreement, at the effective time of the Merger (the “Effective
Time”), each share of common stock, par value $0.0001 per share, of Instacart (the “Instacart Common Stock”) issued and outstanding (other than Excluded Shares and
Appraisal Shares (as defined in the Merger Agreement)) will be converted into the right to receive, at the election of the holder thereof and subject to proration as described below, (i) $65.00 in cash, without interest (the “Cash Consideration”), (ii) 0.3372 shares (the “Stock Exchange Ratio”) of Class A Common Stock, par value
$0.00001 per share, of the Company (“Company Class A Common Stock”) (the “Stock Consideration”), subject…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-18，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1792789/000114036126037109/ef20081998_8k.htm｜as_of：2026-09-18
<<<
Item 8.01
Other Events.
On September 17, 2026, DoorDash, Inc. (the “Company”) filed (i) a certificate of conversion
with the Secretary of State of the State of Delaware and (ii) articles of conversion with the Secretary of State of the State of Nevada, pursuant to which the reincorporation of the Company from the State of Delaware to the State of Nevada (the “Nevada Reincorporation”) became effective on September 18, 2026, at 12:02 a.m. Pacific Time (the “Effective Time”).
At the Effective Time:
•
the Company’s state of incorporation changed from the State of Delaware to the State of Nevada; and
•
the affairs of the Company ceased to be governed by the laws of the State of Delaware and the Company’s existing restated certificate of incorporation and amended and restated bylaws, and instead
became governed by the laws of the State of Nevada and the articles of incorporation filed with the Secretary of State of the State of Nevada (the “Nevada Charter”) and
the bylaws approved by the Company’s board of directors (the “Nevada Bylaws”).
The Nevada Reincorporation did not result in any change in the business, jobs, management, properties, location of any offices or facilities, number of employees,…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-06-12，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1792789/000179278926000040/dash-20260610.htm｜as_of：2026-06-12
<<<
Item 8.01 Other Events.
In connection with the Company’s 2027 annual meeting of stockholders (the “2027 Annual Meeting”), the Company is providing updated contact information for stockholders to submit their proposals to be considered for inclusion in the Company’s proxy statement for the 2027 Annual Meeting. Any such proposals should be addressed to:
DoorDash, Inc.
Attention: General Counsel and Secretary
303 2nd Street, South Tower, 8th Floor
San Francisco, California 94107
with a copy sent to: shareholderoutreach@doordash.com
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
