你是 stock-analyst v20 DD 的證據採集子 agent。標的：EXPE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - EXPE Expedia Group acquisition merger 2025 2026
  - EXPE Expedia Group class action lawsuit securities fraud
  - EXPE Expedia Group clinical trial FDA approval 2025 2026
  - EXPE Expedia Group product launch recall warning letter
  - EXPE Expedia Group SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1324424/000132442426000008/expe-20251231.htm｜as_of：2026-02-13
<<<
Part I. Item 3. Legal Proceedings
In the ordinary course of business, Expedia Group and its subsidiaries are parties to legal proceedings and claims involving property, personal injury, contract, alleged infringement of third-party intellectual property rights and other statutory and common law claims. The amounts that may be recovered in such matters may be subject to insurance coverage.
Rules of the SEC require the description of material pending legal proceedings, other than ordinary, routine litigation incident to the registrant’s business, and advise that proceedings ordinarily need not be described if they primarily involve damages claims for amounts (exclusive of interest and costs) not individually exceeding 10% of the current assets of the registrant and its subsidiaries on a consolidated basis. In the judgment of management, none of the pending litigation matters that the Company and its subsidiaries are defending, including those described below, involves or is likely to involve amounts of that magnitude. The litigation matters described below involve issues or claims that may be of particular interest to our stockholders, regardless of whether any of these matters may be material to our financial position or results of operations based upon the standard set forth in the SEC’s rules.
Litigation Relating to Occupancy and Other Taxes
A number of jurisdictions in the United States have filed lawsuits against online travel companies, including Expedia Group companies such as Hotels.com, Expedia, Hotwire, Orbitz and HomeAway, claiming that such travel companies have failed to collect and/or pay taxes (e.g., occupancy taxes, business privilege taxes, excise taxes, sales taxes, etc.), as well as related claims such as unjust enrichment, restitution, conversion and violation of consumer protection statutes, and seeking monetary (including tax, interest, and penalties), injunctive and/or declaratory relief. In addition, we may file complaints contesting tax assessments made by states, counties and municipalities seeking to obligate online travel companies, including certain Expedia Group companies, to collect and remit certain taxes, either retroactively or prospectively, or both. Moreover, certain jurisdictions may require us to pay tax assessments prior to contesting any such assessments.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 3. Legal Proceedings（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1324424/000132442426000008/expe-20251231.htm｜as_of：2026-02-13
<<<
24 Table of Contents Actions Involving Tax Related Claims by Individual States, Cities and Counties Jasper County Development District #1, Texas Litigation. On August 17, 2020, Jasper County Development District # 1 filed a lawsuit in Texas state court against Expedia and HomeAway alleging claims for declaratory judgment, damages and for a legal accounting. The parties have reached a settlement agreement and, on January 5, 2026, the court dismissed the action, thereby ending the matter.

Non-Tax Litigation and Other Legal Proceedings Putative Class Action Litigation Israeli Putative Class Action Lawsuit (Ze’ev). In or around January 2018, a putative class action lawsuit was filed in the District Court in Lod, Israel against a number of online travel companies including Expedia, Inc. and Hotels.com. The plaintiff generally alleges that the defendants violated Israeli consumer laws by limiting hotel price competition. The plaintiff has filed a motion for class certification which defendants have opposed. The motion remains pending.

Other Legal Proceedings Helms-Burton Litigation. Eight complaints have been filed against Expedia Group companies by parties alleging violations of Title III of the Cuban Liberty and Democratic Solidarity Act, also known as the Helms-Burton Act, of which four remain active. On May 2, 2025, plaintiffs in Echevarria v. Expedia Group, Inc., et al. (Echevarria II) filed an amended complaint. Defendants’ motion to dismiss is pending. On July 14, 2025, plaintiffs in Mata et al. v. Expedia Group, Inc. et al. (Mata) filed a third amended complaint. On July 30, 2025, the jury in Central Santa Lucia, LLC v. Expedia Group, Inc. (CSL) returned a verdict in favor of Expedia. Defendant’s motion for sanctions and plaintiff’s motion for equitable relief remain pending. On September 5, 2025, the court in Echevarria v. Expedia Group, Inc. et al. (Echevarria I) entered an order setting aside the jury verdict and entering judgment in favor of defendants. On October 9, 2025, plaintiff filed a notice of appeal with the Eleventh Circuit, which remains pending.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1324424/000132442426000008/expe-20251231.htm｜as_of：2026-02-13
<<<
Legal Proceedings In the ordinary course of business, we are a party to various lawsuits. Management does not expect these lawsuits to have a material impact on the liquidity, results of operations, or financial condition of Expedia Group. We also evaluate other potential contingent matters, including value-added tax, excise tax, sales tax, transient occupancy or accommodation tax and similar matters. We do not believe that the aggregate amount of liability that could be reasonably possible with respect to these matters would have a material adverse effect on our financial results; however, litigation is inherently uncertain and the actual losses incurred in the event that our legal proceedings were to result in unfavorable outcomes could have a material adverse effect on our business and financial performance.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001324424&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 7 份。
2026-11-04 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-06-23 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-07 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-23 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-04-10 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-03-30 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-12 8-K Items 2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-12 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-03-30，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1324424/000110465926036875/tm269986d1_8k.htm｜as_of：2026-03-30
<<<
Item 1.01. Entry into a Material Definitive Agreement.
Revolving Credit Facility
On March 27, 2026 (the “Closing Date”), Expedia
Group, Inc., a Delaware corporation (the “Company”), entered into a Credit Agreement (as amended, supplemented or otherwise
modified from time to time, the “Revolving Credit Facility”) among the Company, as borrower, the lenders party thereto
from time to time, and JPMorgan Chase Bank, N.A., as administrative agent (in such capacity, the “Administrative Agent”).
The obligations of the Company under the Revolving Credit Facility
are unsecured and are not guaranteed by any of the Company’s subsidiaries.
Aggregate commitments under the Revolving Credit Facility total
$2.5 billion (with a $120 million letter of credit sublimit). As of March 27, 2026, no loans were outstanding under the Revolving
Credit Facility and undrawn stand-by letters of credit in an aggregate face amount of approximately $42 million had been issued
under the Revolving Credit Facility. The Revolving Credit Facility matures on March 27, 2031.
Loans under the Revolving Credit Facility will bear interest at a rate
equal to an index rate plus a margin (a) in the case of term benchmark loans, ranging from 1.00% to 1.75% per annum, depending on the
Company’s credit ratings, and (b) in the case of base rate loans, ranging from 0.00% to 0.75% per annum, depending on the Company’s…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-11-04，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1324424/000132442426000059/expe-20261104.htm｜as_of：2026-11-04
<<<
Item 8.01. Other Events.
Expedia Group's Executive Committee, acting on behalf of its Board of Directors, declared a quarterly cash dividend of $0.48 per share of outstanding common stock payable on December 10, 2026 to stockholders of record as of the close of business on November 18, 2026.
Item 9.01. Financial Statements and Exhibits.
(d) Exhibits
Exhibit
Number
Description
99.1
Press Release dated November 4, 2026
99.2
Earnings Presentation dated November 4, 2026
104 Cover Page Interactive Data File, formatted in Inline XBRL
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-08-05，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1324424/000132442426000051/expe-20260805.htm｜as_of：2026-08-05
<<<
Item 8.01. Other Events.
Expedia Group's Executive Committee, acting on behalf of its Board of Directors, declared a quarterly cash dividend of $0.48 per share of outstanding common stock payable on September 17, 2026 to stockholders of record as of the close of business on August 27, 2026.
Item 9.01. Financial Statements and Exhibits.
(d) Exhibits
Exhibit
Number
Description
99.1
Press Release dated August 5, 2026
99.2
Earnings Presentation dated August 5, 2026
104 Cover Page Interactive Data File, formatted in Inline XBRL
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EXPE_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
