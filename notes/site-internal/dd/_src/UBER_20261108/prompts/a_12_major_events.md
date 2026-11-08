你是 stock-analyst v20 DD 的證據採集子 agent。標的：UBER。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - UBER Uber Technologies acquisition merger 2025 2026
  - UBER Uber Technologies class action lawsuit securities fraud
  - UBER Uber Technologies clinical trial FDA approval 2025 2026
  - UBER Uber Technologies product launch recall warning letter
  - UBER Uber Technologies SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm｜as_of：2026-02-13
<<<
ITEM 3. LEGAL PROCEEDINGS
We are a party to various legal actions and government investigations, and similar or other actions could be brought against us in the future. While it is not possible to determine the outcome of the legal actions, investigations, and proceedings brought against us, we believe that, except for the matters described below, the resolution of all such matters will not have a material adverse effect on our consolidated financial position or liquidity, but could be material to our consolidated results of operations in any one accounting period. We are currently involved in, and may in the future be involved in, legal proceedings, litigation, claims, and government investigations in the ordinary course of business. In addition, the nature of our business exposes us to claims related to the classification of Drivers and the compliance of our business with applicable law. This risk is enhanced in certain jurisdictions outside the United States where we may be less protected under local laws than we are in the United States. Although the results of the legal proceedings, claims, and government investigations in which we are involved cannot be predicted with certainty, we do not believe that the final outcome of these matters is reasonably likely to have a material adverse effect on our business, financial condition, or operating results. Regardless of final outcomes, however, any such legal proceedings, claims, and government investigations may nonetheless impose a significant burden on management and employees and may come with costly defense costs or unfavorable preliminary and interim rulings.
Legal Proceedings Described in Note 14 – Commitments and Contingencies to Our Consolidated Financial Statements
Note 14 – Commitments and Contingencies to our consolidated financial statements for the year ended December 31, 2025 contained in this Annual Report on Form 10-K includes information on legal proceedings that constitute material contingencies for financial reporting purposes that could have a material adverse effect on our consolidated financial position, liquidity or results of operations if they were resolved in a manner that is adverse to us.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm｜as_of：2026-02-13
<<<
In addition, we are currently involved in litigation in a number of the jurisdictions in which we operate. We initiated some of these legal challenges to contest the application of certain laws and regulations to our business. Others have been brought by taxicab owners, local regulators, local law enforcement, and platform users, including Drivers and consumers. These include individual, multiple plaintiff, and putative class and class action claims for alleged violation of laws related to, among other things, transportation, competition, advertising, consumer protection, fee calculations, personal injuries, privacy, intellectual property, product liability, discrimination, safety, and employment. For example, in May 2019, a class action was filed against us and certain of our subsidiaries in the Supreme Court of Victoria, Australia on behalf of participants in the taxi, hire-car, limousine, and charter vehicle industry who were licensed to operate in particular regions of Australia during certain periods between April 2014 and August 2017. The class action alleges that we operated unlawfully in such regions during such periods. The court approved the class action settlement with no admission of liability by Uber.…

The nature of our business exposes us to claims, including civil lawsuits in the United States such as those related to the 2016 Breach. These and any past or future privacy or security incidents could result in violation of applicable U.S. and international privacy, data protection, and other laws. Such violations subject us to individual or consumer class action litigation as well as governmental investigations and proceedings by federal, state, and local regulatory entities in the United States and internationally, resulting in exposure to material civil or criminal liability. Our data security and privacy practices have been the subject of inquiries from government agencies and regulators, not all of which are finally resolved. In April 2018, we entered into an FTC consent decree pursuant to which we agreed, among other things, to implement a comprehensive privacy program, undergo biennial third-party assessments, and not misrepresent how we protect consumer information through 2038. In October 2018, the FTC approved the final settlement, which exposes us to penalties for, amongst other activities, future failure to report security incidents. In November and December 2018, UK, Dutch and French supervisory authorities imposed fines totaling approximately $1.6 million. We have also entered into settlement agreements with numerous state enforcement agencies.…

Delaware law and provisions in our amended and restated certificate of incorporation and amended and restated bylaws could make a merger, tender offer, or proxy contest difficult, thereby depressing the trading price of our common stock.
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001543151&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。
2026-11-04 8-K Items 2.02 Results of Operations and Financial Condition；5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-09-15 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-07 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-16 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-11 8-K Items 5.02 Departure/Election of Directors or Officers
2026-05-08 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-09 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-04 8-K Items 2.02 Results of Operations and Financial Condition；5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-01-12 8-K Items 8.01 Other Events
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-08-07，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1543151/000155278126000414/e26328_uber-8k.htm｜as_of：2026-08-07
<<<
Item 1.01 Entry into a Material Definitive Agreement.
Term Loan Credit Agreement
On August 6, 2026, Uber Technologies, Inc. (the “Company”)
entered into a Term Loan Credit Agreement (the “Term Loan Credit Agreement”), among the Company, as borrower, the lenders
party thereto and Morgan Stanley Senior Funding, Inc., as administrative agent. The Term Loan Credit Agreement was entered into in connection
with the previously disclosed Business Combination Agreement, dated as of July 16, 2026, by and among the Company, Uber International
Technologies II Corporation, a Delaware corporation and a wholly-owned subsidiary of the Company (the “Bidder”), and Delivery
Hero SE, a European Company (Societas Europaea) incorporated under German law (“Delivery Hero”), pursuant to which
the Bidder agreed to make a voluntary public takeover offer (the “Offer”) for the shares of Delivery Hero. The entry into
the Term Loan Credit Agreement reduced the commitments under the Bridge Credit Agreement (as defined below) by €4,000,000,000.
The Term Loan Credit Agreement provides for senior
unsecured term loan commitments in two tranches: Tranche A term loans, which will mature on the date that is eighteen (18) months after
the Closing Date (as defined in the Term Loan Credit Agreement), and Tranche B term loans, which will mature on the date that is three
(3) years after the Closing Date.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-07-16，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1543151/000155278126000382/e26302_uber-8k.htm｜as_of：2026-07-16
<<<
Item 1.01 Entry into a Material Definitive Agreement.
Business Combination Agreement
On July 16, 2026, Uber Technologies,
Inc. (the “Company” or “Uber”) entered into a Business Combination Agreement (the “BCA”), by and among,
the Company, Uber International Technologies II Corporation, a Delaware corporation and a wholly-owned subsidiary of the Company
(the “Bidder”), and Delivery Hero SE, a European Company (Societas Europaea) incorporated under German law (“Delivery
Hero”), pursuant to which the Bidder will make a voluntary public takeover offer within the meaning of Section 29 para. 1 of the
German Securities Acquisition and Takeover Act (Wertpapiererwerbs- und Übernahmegesetz, “WpÜG”) for
the purchase of all of the no-par value registered shares (shares without nominal value) (nennwertlose Namens-Stückaktien)
with a proportionate amount of EUR 1.00 per share of the share capital of Delivery Hero (each a “Delivery Hero Share” and
collectively “Delivery Hero Shares”) for cash consideration per Delivery Hero Share of €41.50 (the “Offer”).
The BCA and the transactions contemplated thereby have been approved by
the board of directors of the Company. The management board (Vorstand) and the supervisory board (Aufsichtsrat) of Delivery
Hero (together, the “Delivery Hero Boards”) have unanimously adopted resolutions approving, among other things, entering into
the BCA.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-09-15，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1543151/000155278126000486/e26383_uber-8k.htm｜as_of：2026-09-15
<<<
Item 8.01 Other Events.
On September 15, 2026, Uber Technologies,
Inc. (the “Company”) completed a registered public offering of €750,000,000 aggregate principal amount of the Company’s
3.750% Senior Notes due 2029, €1,000,000,000 aggregate principal amount of the Company’s 4.125% Senior Notes due 2032, €1,000,000,000
aggregate principal amount of the Company’s 4.375% Senior Notes due 2034, €1,000,000,000 aggregate principal amount of the
Company’s 4.750% Senior Notes due 2038, and €750,000,000 aggregate principal amount of the Company’s 5.250% Senior Notes
due 2046 (together, the “Notes”). The Notes are the Company’s senior unsecured debt obligations. The offering was made
pursuant to the Company’s Registration Statement on Form S-3 (File No.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
