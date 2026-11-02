你是 stock-analyst v20 DD 的證據採集子 agent。標的：SBUX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - SBUX Starbucks acquisition merger 2025 2026
  - SBUX Starbucks class action lawsuit securities fraud
  - SBUX Starbucks clinical trial FDA approval 2025 2026
  - SBUX Starbucks product launch recall warning letter
  - SBUX Starbucks SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
Item 3 Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
Reports—whether accurate or not—of food- or beverage-safety issues such as contamination, mislabeling, or adulteration during any stage of production or preparation have historically harmed the reputations of companies in our industry. Any perceived association with such incidents, even if unfounded, could harm our reputation and materially impact our business and financial performance. Food-safety incidents involving competitors or shared suppliers, even if unrelated to Starbucks, could generate negative publicity and impact our sales regionally or globally. In addition, real or perceived concerns about food safety issues, such as phthalates, per- and polyfluoroalkyl substances (PFAS), microplastics or heavy metals in the U.S. food supply chain, could impact consumers’ confidence in our offerings. Confirmed food-safety issues may also result in product recalls. A widespread product recall could lead to significant financial losses from recall costs, inventory destruction, lost sales, and reputational damage. Declines in customer traffic due to safety concerns, negative publicity, or store closures could adversely affect our operations.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
58 Table of Contents Note 3: Derivative Financial Instruments Interest Rates From time to time, we enter into designated cash flow hedges to manage the variability in cash flows due to changes in benchmark interest rates. We enter into interest rate swap agreements, including forward-starting interest rate swaps and treasury locks, settled in cash based upon the difference between an agreed-upon benchmark rate and the prevailing benchmark rate at settlement. These agreements are generally settled around the time of the pricing of the related debt. Each derivative agreement’s gain or loss is recorded in AOCI and is subsequently reclassified to interest expense over the life of the related debt.
>>>

[4] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
8-K 000-20322 5/7/2018 2.1 3.1 Restated Articles of Incorporation of Starbucks Corporation 10-Q 000-20322 4/28/2015 3.1 3.2 Amended and Restated Bylaws of Starbucks Corporation (As amended and restated through June 25, 2025)
>>>

[5] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000829224&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-09-24 8-K Items 2.05 Costs Associated with Exit or Disposal Activities；7.01 Regulation FD Disclosure
2026-07-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-12 8-K Items 5.02 Departure/Election of Directors or Officers
2026-05-20 8-K Items 8.01 Other Events
2026-05-15 8-K Items 2.05 Costs Associated with Exit or Disposal Activities
2026-04-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-02 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-30 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-01-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-11-17 8-K/A Items 5.02 Departure/Election of Directors or Officers
2025-11-03 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-09-24，Item 2.05）｜章節：8-K Item 2.05 Costs Associated with Exit or Disposal Activities｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922426000145/sbux-20260922.htm｜as_of：2026-09-24
<<<
Item 2.05 Costs Associated with Exit or Disposal Activities
On September 22, 2026, the Board of Directors of Starbucks Corporation (the “Company”) approved further actions under its previously announced “Back to Starbucks” strategy.
The “Back to Starbucks” strategy focuses on revitalizing coffeehouses, enhancing the customer experience, and strengthening the Company’s coffeehouse portfolio. As part of that strategy, the Company further assessed its existing North America store portfolio and will close approximately 1% of its more than 18,000 North America coffeehouses that do not deliver the coffeehouse experience and financial performance expected of the brand.
The Company expects the majority of the coffeehouse closures will be completed by the end of fiscal year 2026 with a significant portion of the associated cash and non-cash charges incurred in fiscal year 2026. Of the approximately $300 million of restructuring charges to be incurred, the Company anticipates that approximately $200 million will be cash charges primarily related to lease exit costs and employee separation benefits. The remaining $100 million will be non-cash charges due to disposal and impairment of company-operated coffeehouse assets.
Item 7.01 Regulation FD Disclosure.
The Company expects that full fiscal year 2026 net new global company-operated and licensed coffeehouse openings will be approximately 440, compared with its prior guidance of 600 to 650 net new openings.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-15，Item 2.05）｜章節：8-K Item 2.05 Costs Associated with Exit or Disposal Activities｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922426000088/sbux-20260513.htm｜as_of：2026-05-15
<<<
Item 2.05 Costs Associated with Exit or Disposal Activities
On May 13, 2026, the Board of Directors of Starbucks Corporation (the “Company”) approved further actions under its previously announced “Back to Starbucks” strategy that focuses on revitalizing coffeehouses and enhancing the customer experience, which the Company believes will drive long-term growth and value for partners and shareholders.
As part of its strategy, the Company has previously communicated that it is pursuing $2 billion in cost savings initiatives and that its international business has moved towards a model where nearly 90% of its coffeehouses are licensed.
Under the approved restructuring plan, the Company plans to capture cost savings by further streamlining its domestic and international support organization and non-retail facilities. In addition, the Company is reducing the future operational complexity of its Starbucks Reserve and Roastery locations, taking learnings from its core coffeehouse operations.
The Company expects that a majority of the plan actions will be completed by the end of this fiscal year with a significant portion of the associated cash and non-cash charges incurred in fiscal year 2026.…
>>>

[8] 來源：SEC EDGAR｜文件：8-K（2026-05-20，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922426000094/sbux-20260520.htm｜as_of：2026-05-20
<<<
Item 8.01 Other Events.
On May 20, 2026, Starbucks Corporation (the “Company”) completed the settlement of its previously announced cash tender offers to purchase certain series of the Company’s notes (the “Tender Offers”). After giving effect to the Company’s purchase and cancellation of the notes set forth in the table below, the amounts remaining outstanding are as follows:
Description of Notes
Aggregate Principal Amount Accepted for Purchase
Total Purchase Price (includes accrued and unpaid interest)
Aggregate Principal Amount Remaining Outstanding
4.800% Senior Notes due 2030
$321,824,000
$325,720,215.89
$178,176,000
4.500% Senior Notes due 2028
$273,468,000
$274,664,422.50
$476,532,000
4.000% Senior Notes due 2028
–
–
$750,000,000
4.500% Senior Notes due 2048
$200,000,000
$166,067,000.00
$800,000,000
5.400% Senior Notes due 2035
$410,249,000
$423,011,846.39
$89,751,000
5.000% Senior Notes due 2034
$110,351,000
$112,709,691.32
$389,649,000
4.900% Senior Notes due 2031
–
–
$500,000,000
4.800% Senior Notes due 2033
–
–
$500,000,000
Under the terms of the Tender Offers as set forth in the Offer to Purchase, dated May 4, 2026, as amended by the Company’s press release announcing the early results and upsizing of the Tender Offers issued on May 15, 2026 (together, the “Offer to Purchase”), the Company elected to settle on the Early Settlement Date (as such term is defined in the Offer to Purchase) and does not intend to purchase any additional notes.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
