你是 stock-analyst v20 DD 的證據採集子 agent。標的：META。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - META Meta Platforms acquisition merger 2025 2026
  - META Meta Platforms class action lawsuit securities fraud
  - META Meta Platforms clinical trial FDA approval 2025 2026
  - META Meta Platforms product launch recall warning letter
  - META Meta Platforms SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
Item 3.Legal Proceedings
As a multinational company with a complex and evolving business, we are, and expect to continue to be, subject to numerous claims, litigation, regulatory, tax, and government inquiries and investigations, and other legal proceedings in jurisdictions around the world. Although we believe many of these matters are without merit and are vigorously defending them, we may not be successful. Any litigation to which we are a party may be resolved adversely or we may be subject to an unfavorable judgment that may not be reversed upon appeal. We may also decide to settle litigation, disputes, or other legal proceedings in some instances on terms that are unfavorable to us. In addition, we may become subject to orders or consent decrees imposed by government or regulatory authorities. Any such developments could cause us to incur substantial costs, expose us to civil and criminal liability (including liability for our personnel) or penalties (including substantial monetary remedies), interrupt or require us to change our business practices in a manner materially adverse to our business (including changes to our products and services or user data practices), result in negative publicity and reputational harm, divert resources and the time and attention of management from our business, or subject us to other structural or behavioral remedies that adversely affect our business. We have experienced such outcomes to varying degrees in the past, and we expect to continue to face a challenging litigation and regulatory environment, including in light of complex and evolving laws and regulations, as well as the scale of our business and the size of our user and advertiser base.
Over the last several years, the number and potential significance of the litigation and investigations involving the company have increased, and there can be no assurance that this trend will not continue.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
We are involved in numerous class action lawsuits and other litigation matters that are expensive and time consuming, and, if resolved adversely, could harm our business, financial condition, or results of operations.

We are involved in numerous lawsuits, including stockholder derivative lawsuits and putative class action lawsuits, many of which claim statutory damages and/or seek significant changes to our business operations, and we anticipate that we will continue to be a target for numerous lawsuits in the future. Because of the scale of our user, advertiser, and developer base, the plaintiffs in class action cases filed against us typically claim enormous monetary damages even if the alleged per-user or entity harm is small or non-existent. In addition, we have faced, currently face, and will continue to face additional class action and other lawsuits based on claims related to advertising, antitrust, privacy, security, biometrics, content, algorithms, copyright, user well-being, younger users, employment, contingent workers, activities on our platform, consumer protection, unfair and deceptive trade practices, or product performance or other claims related to the use of consumer hardware and software, including virtual reality technology and products, which are new and unproven.…

From time to time, we receive notice from patent, copyright, and trademark holders and other parties alleging that certain of our products and services, trademarks, or user content, infringe their intellectual property rights or that certain employees may have misappropriated trade secrets from their former employers. We presently are involved in a number of intellectual property lawsuits, and as we face increasing competition and develop new products and services, we expect the number of intellectual property claims against us to grow. For example, we and other companies are, and expect to continue to be, the subject of litigation in the United States, Europe, Canada, and elsewhere alleging copyright infringement in connection with the acquisition, distribution, and use of copyrighted materials for AI training as well as potential reproduction of copyrighted materials in AI outputs, including cases addressing the applicability of the fair use defense in the United States. There can be no assurances that favorable final outcomes will be obtained in these cases. In addition, plaintiffs may seek, and we may become subject to, preliminary or provisional rulings in the course of any such litigation, including potential preliminary injunctions requiring us to change or cease some or all of our operations. We may decide to settle such lawsuits and disputes on terms that are unfavorable to us.…
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001326801&type=8-K｜as_of：2026-10-24
<<<
【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。
2026-10-21 8-K Items 1.01 Entry into a Material Definitive Agreement；2.02 Results of Operations and Financial Condition；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-29 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-04 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-04-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-04-14 8-K Items 5.02 Departure/Election of Directors or Officers
2026-01-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-16 8-K Items 5.02 Departure/Election of Directors or Officers
2025-12-19 8-K Items 5.02 Departure/Election of Directors or Officers
2025-12-12 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-03 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2025-10-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-10-21，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026066700/meta-20261019.htm｜as_of：2026-10-21
<<<
Item 1.01. Entry into a Material Definitive Agreement.
On October 19, 2026, the board of directors (the “Board”) of Meta Platforms, Inc. (the “Company” or “Meta”) approved and declared advisable, based on the unanimous recommendation of a special committee consisting of disinterested and independent directors established to review such transaction, and recommended to the Company’s shareholders, the amendment and restatement of the Company’s certificate of incorporation (as so amended and restated, the “Restated Charter”) to, among other things, adjust the Company’s capital structure by establishing a new class of non-voting Class C common stock, par value $0.000006 (the “Recapitalization”), which was subsequently approved by the requisite shareholders by written consent on October 20, 2026. The Company expects to file the Restated Charter with the Secretary of State of the State of Delaware on or about October 21, 2026 with an effective date of January 19, 2027.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-05-04，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1326801/000119312526204128/d134616d8k.htm｜as_of：2026-05-04
<<<
Item 8.01
Other Events.
On May 4, 2026, Meta Platforms, Inc. (the “Company”) completed an offering of $3,000,000,000 aggregate principal amount of its 4.550% Senior Notes due 2031 (the “2031 Notes”), $2,000,000,000 aggregate principal amount of its 4.875% Senior Notes due 2033 (the “2033 Notes”), $6,000,000,000 aggregate principal amount of its 5.250% Senior Notes due 2036 (the “2036 Notes”), $4,000,000,000 aggregate principal amount of its 6.200% Senior Notes due 2046 (the “2046 Notes”), $6,000,000,000 aggregate principal amount of its 6.300% Senior Notes due 2056 (the “2056 Notes”), and $4,000,000,000 aggregate principal amount of its 6.450% Senior Notes due 2066 (the “2066 Notes” and, together with the 2031 Notes, the 2033 Notes, the 2036 Notes, the 2046 Notes, and the 2056 Notes, the “Notes”). The offering of the Notes was made pursuant to the Company’s Registration Statement on Form S-3 (File No. 333-295425), which Registration Statement relates to the offer and sale on a delayed basis from time to time of an indeterminate amount of the Company’s debt securities. Further information concerning the Notes and related matters is set forth in the Company’s Prospectus Supplement dated April 30, 2026, which was filed with the Securities and Exchange Commission on May 1, 2026.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-12-12，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828025056768/meta-20251205.htm｜as_of：2025-12-12
<<<
Item 8.01 Other Events.
As previously disclosed, on July 17, 2025, the parties to the stockholder derivative action in the Delaware Court of Chancery, captioned In re Facebook Inc. Derivative Litigation, Consolidated C.A. 2018-0307-KSJM (Del. Ch.) (the "Matter"), agreed to a settlement in principle to resolve all claims in the Matter, which is subject to court approval.
On December 5, 2025, the Court of Chancery entered a Scheduling Order pursuant to which a settlement hearing will be held at 1:30 pm ET on April 7, 2026. The Scheduling Order requires that the parties' Stipulation and Agreement of Settlement, Compromise, and Release (the "Stipulation") and the Notice of Pendency of the Matter, Proposed Settlement of the Matter, and Settlement Hearing (the "Notice") be distributed to stockholders of Meta Platforms, Inc. (the "Company") in the form of this Current Report on Form 8-K. The Stipulation is attached hereto as Exhibit 99.1 and the Notice is attached hereto as Exhibit 99.2.
Pursuant to the Scheduling Order, the Stipulation and the Notice are available on the Company's website at investor.atmeta.com/Legal-Notices/default.aspx.
Item 9.01 Financial Statements and Exhibits.
(d) Exhibits
Exhibit Number
Exhibit Title or Description
99.1
Stipulation and Agreement of Settlement, Compromise, and Release.
99.2 Notice of Pendency, Proposed Settlement, and Settlement Hearing.
104…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
