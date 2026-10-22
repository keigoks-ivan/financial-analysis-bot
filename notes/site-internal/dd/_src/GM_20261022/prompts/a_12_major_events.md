你是 stock-analyst v20 DD 的證據採集子 agent。標的：GM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - GM General Motors acquisition merger 2025 2026
  - GM General Motors class action lawsuit securities fraud
  - GM General Motors clinical trial FDA approval 2025 2026
  - GM General Motors product launch recall warning letter
  - GM General Motors SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
Item 3. Legal Proceedings
SEC regulations require us to disclose certain information about environmental proceedings if a governmental authority is a party to such proceedings and such proceedings involve potential monetary sanctions that we reasonably believe will exceed a stated threshold. Pursuant to the SEC regulations, the Company will use a threshold of $1 million for purposes of determining whether disclosure of any such proceedings is required.
In GM's 2023 Annual Report on Form 10-K, GM reported that in February 2023, it had self-disclosed to the EPA potential violations of the Toxic Substances Control Act's (TSCA) requirements applicable to the import of new chemical substances at our Ultium Cells LLC joint venture. In November 2023, these potential violations were settled via consent agreement with the EPA, the terms of which include, among other items, payment of civil penalties based upon import activity prior to receipt of a TSCA 5(e) order. As of December 31, 2025, GM has incurred an estimated $18.2 million in civil penalties. These penalties, which will continue to grow until the EPA issues a TSCA 5(e) order, are assessed jointly and severally to GM and Ultium Cells LLC.
The discussion under Note 16 to our consolidated financial statements is incorporated by reference into this Part I, Item 3.
* * * * * * *
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
We could be materially adversely affected by unusual or significant litigation, governmental investigations, or other proceedings. We are subject to legal proceedings in the U.S. and elsewhere involving various issues, including product liability lawsuits, warranty litigations, class action litigations alleging product defects, emissions litigations, privacy matters, stockholder litigations, labor and employment litigations, and claims and actions arising from restructurings and divestitures of operations and assets. In addition, we are subject to various governmental proceedings and investigations. A negative outcome in one or more of these proceedings could result in the imposition of damages, including punitive damages, fines, reputational harm, civil lawsuits, and criminal penalties, interruptions of business, modification of business practices, equitable remedies, and other sanctions against us or our personnel as well as legal and other costs, all of which may be significant. For a further discussion of certain of these matters, refer to Note 16 to our consolidated financial statements.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-27）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm｜as_of：2026-01-27
<<<
There are several putative class actions pending against GM in the U.S. and Canada alleging that various vehicles sold, including model year 2011–2016 Duramax Diesel Chevrolet Silverado and GMC Sierra vehicles, violate federal and state laws because they release more emissions than a reasonable customer would expect. In July 2023, the two putative class actions pending in the U.S. were dismissed with prejudice and judgment entered in favor of GM, and plaintiffs appealed the dismissal. In August 2024, the Sixth Circuit reversed in part and affirmed in part the dismissal in one of the cases. In June 2025, a different panel in the second case affirmed in part, vacated in part, and remanded for further proceedings. We are currently unable to estimate any reasonably possible material loss or range of loss that may result from these actions. GM is also defending other lawsuits in the U.S. based on these allegations, including a shareholder demand lawsuit.

There is one putative class action and one certified class action pending against GM in the U.S. alleging that various 2015–2022 model year vehicles are defective because they are equipped with faulty 8-speed transmissions. In March 2023, the judge overseeing the class action concerning 2015–2019 model year vehicles certified 26 state subclasses and GM appealed. In June 2025, the Sixth Circuit decertified all 26 state subclasses and remanded to the district court for further proceedings. The putative class action concerning 2020–2022 model year vehicles is pending in front of a different judge that has not yet addressed class certification. We have similar cases pending in Canada concerning these vehicles. We are currently unable to estimate any 88 Table of Contents GENERAL MOTORS COMPANY AND SUBSIDIARIES NOTES TO CONSOLIDATED FINANCIAL STATEMENTS – (Continued)
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001467858&type=8-K｜as_of：2026-10-22
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-20 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-08-11 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-21 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-04 8-K Items 5.02 Departure/Election of Directors or Officers；5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-26 8-K Items 5.02 Departure/Election of Directors or Officers
2026-04-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-03-23 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-01-27 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-08 8-K Items 8.01 Other Events
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-08-11，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1467858/000119312526344698/d145571d8k.htm｜as_of：2026-08-11
<<<
Item 1.01.
Entry into a Material Definitive Agreement.
On August 7, 2026, General Motors Company (the “Company”) and General Motors LLC (the “Coordinator”), a wholly owned subsidiary of the Company, entered into a Master IPU Agreement (the “IPU Agreement”) with Procura Auto Parts LLC (the “Paying Agent”), pursuant to which the Company will issue irrevocable payment undertakings (“IPUs”) to the Paying Agent in exchange for the Paying Agent advancing funds to certain suppliers (“Suppliers”) of the Company in exchange for the Suppliers acquiring and holding inventory on behalf of the Company (the “Program”). The purpose of the Program is to secure supply of certain critical inventory for the production of retail and fleet vehicles in the event of supply chain disruptions that may arise for various reasons, including extreme weather, natural disasters, cyberattacks in our supply chain, excessive demand, and other similar events. Under the Program, the Suppliers that receive such funds will acquire and hold the inventory until it is needed by the Company to produce vehicles (the “Inventory”). The Paying Agent will obtain funding for the Program from a syndicate of banks, including JPMorgan Chase Bank, N.A. and Banco Santander, S.A., which will be supported by the Company’s IPUs. The Coordinator will facilitate the administration of the Program on behalf of the Company.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-03-23，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1467858/000119312526119684/d114837d8k.htm｜as_of：2026-03-23
<<<
ITEM 1.01 Entry Into a Material Definitive Agreement
See Item 2.03 below.
ITEM 2.03 Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant
On March 23, 2026, General Motors Company (“GM”) entered into an Eighth Amended and Restated 364-Day Revolving Credit Agreement with JPMorgan Chase Bank, N.A., as administrative agent, Citibank, N.A., as syndication agent, the other lenders named therein, and General Motors Financial Company, Inc. (the “364-Day Facility”). The 364-Day Facility is unsecured, consists of a 364-day, $2.0 billion facility and matures on March 22, 2027.
The 364-Day Facility is available to GM as well as certain of its wholly owned subsidiaries. However, GM has allocated the 364-Day Facility for exclusive use by General Motors Financial Company, Inc. The 364-Day Facility allows for borrowing in U.S. Dollars only. GM has guaranteed the obligations of subsidiary borrowers under the 364-Day Facility.
Interest rates on obligations under the 364-Day Facility are based on prevailing annual interest rates for Term SOFR loans, Daily Simple SOFR loans or an alternative base rate, each subject to an applicable margin. This applicable margin will be based upon the credit rating assigned to the 364-Day Facility or to senior, unsecured long-term indebtedness of GM.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-01-08，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1467858/000146785826000005/gm-20260108.htm｜as_of：2026-01-08
<<<
Item 8.01. Other Events.
For the past several years, the global automotive industry and General Motors Company (the Company, we, our or
GM) have been investing significant capital to develop electric vehicles (EVs) to meet increasingly stringent fuel
economy and emissions regulations in the United States and growing customer demand. Our strategy in North
America has been focused on delivering exceptional vehicles quickly and cost effectively. To realize economies of
scale, GM added EV production to existing assembly plants and developed a dedicated EV architecture and
propulsion strategy. These initiatives helped the Company become the #2 seller of EVs in North America beginning
in the second half of 2024 on the strength of our broad portfolio of award-winning electric SUVs, trucks and luxury
vehicles.
With the termination of certain consumer tax incentives and the reduction in the stringency of emissions regulations,
industry-wide consumer demand for EVs in North America began to slow in 2025. As a result, GM proactively
reduced EV capacity, including by pivoting the Company’s assembly plant in Orion, MI from EV production to the
production of full-size SUVs and full-size pickups powered by internal combustion engines, where we believe we
have unmet demand, and we proactively reduced battery cell capacity, including by selling our interest in Ultium
Cells LLC’s Lansing, MI facility to LG Energy Solution.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
