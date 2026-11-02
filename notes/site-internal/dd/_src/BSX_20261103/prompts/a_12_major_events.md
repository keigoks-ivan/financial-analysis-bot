你是 stock-analyst v20 DD 的證據採集子 agent。標的：BSX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - BSX Boston Scientific acquisition merger 2025 2026
  - BSX Boston Scientific class action lawsuit securities fraud
  - BSX Boston Scientific clinical trial FDA approval 2025 2026
  - BSX Boston Scientific product launch recall warning letter
  - BSX Boston Scientific SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm｜as_of：2026-02-17
<<<
ITEM 3. LEGAL PROCEEDINGS
See Note I – Commitments and Contingencies to our consolidated financial statements included in Part II, Item 8. Financial Statements and Supplementary Data of this Annual Report on Form 10-K, which is incorporated herein by reference.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm｜as_of：2026-02-17
<<<
We are currently the subject of product liability litigation proceedings and other proceedings described in more detail under Note I – Commitments and Contingencies to our consolidated financial statements included in Part II, Item 8. Financial Statements and Supplementary Data of this Annual Report. The outcome of litigation, particularly class action lawsuits, is difficult to assess or quantify. Plaintiffs in these types of lawsuits often seek recovery of very large or indeterminate amounts, including not only actual damages, but also punitive damages. The magnitude of the potential losses relating to these lawsuits may remain unknown for substantial periods of time. In addition, the cost to defend against any future litigation may be significant. Product liability claims, securities, commercial and environmental litigation and other litigation in the future, regardless of the outcome, could have a material adverse effect on our financial condition, results of operations or liquidity. Additionally, we maintain an insurance policy providing limited coverage against securities claims and we are substantially self-insured with respect to product liability and environmental claims and fully self-insured with respect to intellectual property infringement claims.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000010/bsx-20251231.htm｜as_of：2026-02-17
<<<
Upon the Company’s acquisition of Axonics on November 15, 2024, the Company assumed responsibility for all litigation pending against Axonics. On September 18, 2023, Axonics commenced an arbitration dispute against the Al Mann Foundation (AMF), in response to which AMF asserted multiple claims against Axonics. This arbitration was to resolve, among other things, whether AMF terminated its licensing agreement with Axonics and whether Axonics owes royalties to AMF for its non-rechargeable sacral neuromodulation products. The parties reached a confidential settlement resolving all claims in the arbitration in December 2025.

Product Liability Litigation Multiple product liability cases or claims related to transvaginal surgical mesh products designed to treat stress urinary incontinence and pelvic organ prolapse have been asserted against us, predominantly in the United States, Canada, the United Kingdom, Scotland, Ireland, and Australia. Plaintiffs generally seek monetary damages based on allegations of personal injury associated with the use of our transvaginal surgical mesh products, including design and manufacturing claims, failure to warn, 98 breach of warranty, fraud, violations of state consumer protection laws and loss of consortium claims. We have entered into individual and master settlement agreements or are in the final stages of entering agreements with certain plaintiffs' counsel, to resolve the majority of these cases and claims. All settlement agreements were entered into solely by way of compromise and without any admission or concession by us of any liability or wrongdoing.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000885725&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 19 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 10 份。
2026-10-28 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-07 8-K Items 5.02 Departure/Election of Directors or Officers；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-09-23 8-K Items 5.02 Departure/Election of Directors or Officers
2026-09-08 8-K Items 1.05 Material Cybersecurity Incidents
2026-08-26 8-K Items 8.01 Other Events
2026-07-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-27 8-K Items 2.05 Costs Associated with Exit or Disposal Activities
2026-05-18 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-18 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-05 8-K Items 5.03 Amendments to Articles or Bylaws；5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-04-22 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-03-30 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-26 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-02-23 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-05 8-K Items 5.02 Departure/Election of Directors or Officers
2026-02-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-15 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-01-15 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-19 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-07-27，Item 2.05）｜章節：8-K Item 2.05 Costs Associated with Exit or Disposal Activities｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000049/bsx-20260721.htm｜as_of：2026-07-27
<<<
Item 2.05 Costs Associated with Exit or Disposal Activities.
On July 21, 2026, the Board of Directors of Boston Scientific Corporation (the “Company”) approved a new global restructuring program (the “2026 Restructuring Plan”). The 2026 Restructuring Plan is intended to support the Company’s efforts to drive sustained cost efficiencies and enable continued growth by ensuring that the Company is structured and resourced to support its strategic priorities.
Key activities under the 2026 Restructuring Plan will include supply chain optimization, including transferring certain production lines among facilities, targeted functional transformation and organizational structure evolution to drive sustained cost efficiencies. These activities are expected to be initiated in 2026 and to be substantially completed by the end of 2029.
While new jobs are created in areas of growth and resources are deployed to support the Company’s portfolio and global market needs, the Company does expect some headcount reductions to result from these restructuring activities.
The implementation of the 2026 Restructuring Plan is estimated to result in total pre-tax charges of approximately $700 million to $800 million, of which approximately $600 million to $700 million is expected to result in future cash outlays, and reduce gross annual pre-tax expenses by approximately $500 million as program benefits are realized.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-02-26，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/885725/000088572526000017/bsx-20260226.htm｜as_of：2026-02-26
<<<
Item 1.01 Entry into a Material Definitive Agreement.
Revolving Credit Agreement
On February 26, 2026, Boston Scientific Corporation (the “Company”) entered into a $3.000 billion revolving credit agreement (the “2026 Revolving Credit Agreement”) by and among the Company, as borrower, the several lenders party thereto, and Wells Fargo Bank, National Association, as administrative agent. The Company may borrow from time to time up to $3,000,000,000 in revolving credit loans under the 2026 Revolving Credit Agreement. The 2026 Revolving Credit Agreement matures on February 26, 2031, with one-year extension options subject to certain conditions, including certain lender approvals. Capitalized terms used in this section but not defined herein shall have the respective meanings set forth in the 2026 Revolving Credit Agreement.
Loans under the 2026 Revolving Credit Agreement will bear interest at (a) the Term SOFR determined for the interest period plus the applicable margin based on the credit rating of the Company for its long term senior unsecured debt (its “Credit Rating”) for SOFR Loans, (b) Alternate Base Rate (“ABR”) plus the applicable margin based on the Credit Rating for ABR Loans, (c) the Eurocurrency Rate plus the applicable margin based on the Credit Rating for Multicurrency Loans, and (d) for Competitive Advance Facility (“CAF”) Advances, at either (i) a fixed rate plus (or minus) a margin or (ii) the…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-01-15，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/885725/000094787126000037/ss5822815_8k.htm｜as_of：2026-01-15
<<<
ITEM 1.01 ENTRY INTO A MATERIAL DEFINITIVE AGREEMENT
On January 14, 2026, Boston Scientific Corporation,
a Delaware corporation (the “Company”), entered into an Agreement and Plan of Merger (the “Merger Agreement”)
with Pinehurst Merger Sub, Inc., a Delaware corporation and wholly owned subsidiary of the Company (“Merger Sub”),
and Penumbra, Inc., a Delaware corporation (“Penumbra”), providing for the merger of Merger Sub with and into Penumbra
(the “Merger”), with Penumbra surviving the Merger as a wholly owned subsidiary of the Company.
At the effective time of the Merger (the “Effective
Time”), each share of common stock, par value $0.001 per share, of Penumbra issued and outstanding immediately prior to the
Effective Time (each, a “Penumbra Share” and collectively, the “Penumbra Shares”), other than Penumbra
Shares (a) held in the treasury of Penumbra or owned by any direct or indirect wholly owned subsidiary of Penumbra, (b) owned by Merger
Sub, the Company or any direct or indirect wholly owned subsidiary of the Company or (c) held by holders who (i) are entitled to demand
appraisal rights under Section 262 of the Delaware General Corporation Law, as amended (the “DGCL”), (ii) have properly
exercised and perfected their respective demands for appraisal of such Shares in the time and manner provided in Section 262 of the DGCL…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BSX_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
