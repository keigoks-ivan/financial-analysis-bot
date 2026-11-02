你是 stock-analyst v20 DD 的證據採集子 agent。標的：FSLR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - FSLR First Solar acquisition merger 2025 2026
  - FSLR First Solar class action lawsuit securities fraud
  - FSLR First Solar clinical trial FDA approval 2025 2026
  - FSLR First Solar product launch recall warning letter
  - FSLR First Solar SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm｜as_of：2026-02-24
<<<
Item 3. Legal Proceedings
JinkoSolar
On February 25, 2025, First Solar filed suit in the district court for the District of Delaware asserting that JinkoSolar Holding Co., Ltd.; Jinko Solar Co., Ltd.; Jinko Solar (Vietnam) Industries Co. Ltd.; Jinko Solar Technology Sdn. Bhd.; Zhejiang Jinko Solar Co., Ltd.; JinkoSolar (U.S.) Holding Inc.; JinkoSolar (U.S.) Inc.; Jinko Solar (U.S.) Manufacturing Inc.; and Jinko Solar (U.S.) Industries Inc. (collectively, “JinkoSolar”) directly and indirectly infringe a First Solar patent through JinkoSolar’s manufacture, import, use, sale, and offering for sale of certain tunnel oxide passivated contact (“TOPCon”) solar products. First Solar alleges that the JinkoSolar TOPCon products contain solar cells manufactured using a method claimed in the patent. First Solar seeks both monetary damages and injunctive relief. On June 27, 2025, JinkoSolar filed an answer to the complaint and counterclaims asserting that the patent-in-suit is not valid and that it is not infringed by JinkoSolar. On July 18, 2025, First Solar filed an answer to the counterclaims.
On July 18, 2025, JinkoSolar Co. Ltd. filed an inter partes review before the U.S. Patent and Trademark Office (the “USPTO”) alleging First Solar’s patent asserted in the District of Delaware litigation (the “’074 Patent”) is invalid over certain prior art. On September 29, 2025, First Solar filed a brief requesting that the inter partes review be discretionarily denied. On November 20, 2025, the U.S. Patent Trial and Appeal Board declined the petition, ending the proceeding.
On December 15, 2025, JinkoSolar filed a petition for an ex parte reexamination of First Solar’s ‘074 patent. First Solar is evaluating the petition and preparing its response. The USPTO decision on whether to issue an order granting or denying the reexamination is due on March 15, 2026.
Mundra
On April 15, 2025, Mundra Solar PV Limited (“Mundra”) filed suit in the district court of the District of Delaware seeking declaratory judgment that it does not infringe two of First Solar’s patents (the ’074 Patent and the ’732 Patent) through its manufacture, import, use, sale, and offering for sale of certain TOPCon solar products.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm｜as_of：2026-02-24
<<<
From time to time, we have been and may be subject to disputes and litigation, with and without merit, that may be costly and which may divert the attention of our management and our resources in general, whether or not any dispute actually proceeds to litigation. The results of complex legal proceedings are difficult to predict. Moreover, complaints filed against us may not specify the amount of damages that plaintiffs seek, and we therefore may be unable to estimate the possible range of damages that might be incurred should these lawsuits be resolved against us. Even if we are able to estimate losses related to these actions, the ultimate amount of loss may be materially higher than our estimates. Any resolution of litigation, or threatened litigation, could involve the payment of damages or expenses by us, which may be significant or involve an agreement with terms that restrict the operation of our business. For example, in September 2025, First Solar filed a complaint in the Supreme Court of the State of New York asserting that BP Solar Holding LLC and its affiliate Lightsource Renewable Energy Trading, LLC (together, the “Defendants”) breached their contractual obligations with First Solar and demanding payment from the Defendants of $323.6 million, along with certain other receivables for solar modules previously delivered to the Defendants.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm｜as_of：2026-02-24
<<<
In April 2019, a subcontractor of First Solar sustained certain injuries while performing work at a former project site and, in May 2019, commenced legal action against a subsidiary of the Company. In June 2023, a jury awarded damages of approximately $51.3 million to the plaintiff. On September 21, 2023, the Superior Court of California for Monterey County ruled, in response to a motion for remittitur filed by the Company, that the damages awarded to the plaintiff were excessive and reduced the award from $51.3 million to $21.8 million. The plaintiff and defendant have appealed and cross appealed varying aspects of the verdict and the remittitur. Accordingly, due to the uncertainty surrounding the multiple decisions and appeals, as of December 31, 2025, we recorded a $21.8 million accrued litigation payable included in “Other current liabilities” in our consolidated balance sheet. We 113 Table of Contents believe the full amount of awarded damages will be covered by our various insurance policies. Accordingly, we also recorded a $21.8 million receivable included in “Other current assets” in our consolidated balance sheet as of December 31, 2025. The plaintiff did not accept the reduced award by the court ordered deadline of October 10, 2023. As a result, the $21.8 million award has been vacated, and a new trial is expected to be scheduled.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001274494&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-15 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-04-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-24 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-19 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-02-19，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1274494/000127449426000016/fslr-20260213.htm｜as_of：2026-02-19
<<<
Item 1.01. Entry into a Material Definitive Agreement
On February 13, 2026, First Solar, Inc. (the “Company”) entered into a Revolving Credit and Guaranty Agreement (the “Credit Agreement”), among the Company, the guarantors from time to time party thereto, the several banks and other financial institutions or entities from time to time parties thereto (the “Lenders”), and JPMorgan Chase Bank, N.A., as administrative agent (the “Administrative Agent”). The Credit Agreement provides the Company with a senior unsecured five-year revolving credit facility (the “Credit Facility”) in an aggregate principal amount of $1,500,000,000, with a sub-limit of $450,000,000 available for the issuance of letters of credit. Borrowings under the Credit Facility are available for working capital and other general corporate purposes. Subject to receipt of commitments from one or more debt financing sources and certain other conditions, the Company has the right to increase the aggregate commitments under the Credit Facility by an additional $1,000,000,000. The Company may request up to two one-year extensions of the Credit Facility.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-10-29，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1274494/000127449426000211/fslr-20261029.htm｜as_of：2026-10-29
<<<
Item 8.01. Other Events
On October 29, 2026, the Company announced that its board of directors authorized the repurchase (the “Repurchase Program”) of up to $500 million of the Company’s outstanding common stock, $0.001 par value (“Common Stock”). The Repurchase Program has no expiration date, may be suspended or discontinued at any time, and does not obligate the Company to acquire any amount of Common Stock.
The timing and total amount of share repurchases under the Repurchase Program will be determined by the Company from time to time at its discretion based on its evaluation of business, economic, and market conditions, corporate regulatory requirements, prevailing stock prices, and other considerations. The Company may repurchase shares of Common Stock from time to time through a variety of methods, such as open market purchases, including in reliance upon the safe harbors under Rule 10b-18 and/or Rule 10b5-1 of the Securities Exchange Act of 1934, as amended, privately negotiated transactions, accelerated share repurchase transactions, or by other means, in accordance with applicable securities laws and other restrictions.
Item 9.01. Financial Statements and Exhibits
(d) Exhibits.
Exhibit Number Description
99.1
Press Release of First Solar, Inc. dated October 29, 2026
104 Cover Page Interactive Data File (embedded within the Inline XBRL Document)
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20261103/parts/axes_4.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
