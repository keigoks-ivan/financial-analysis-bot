你是 stock-analyst v20 DD 的證據採集子 agent。標的：LIN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - LIN Linde acquisition merger 2025 2026
  - LIN Linde class action lawsuit securities fraud
  - LIN Linde clinical trial FDA approval 2025 2026
  - LIN Linde product launch recall warning letter
  - LIN Linde SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm｜as_of：2026-02-25
<<<
Item 3: Legal Proceedings
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm｜as_of：2026-02-25
<<<
Linde’s subsidiaries are party to various lawsuits and governmental investigations arising in the ordinary course of business. Adverse outcomes in some or all of the claims pending may result in significant monetary damages or injunctive relief that could adversely affect Linde’s ability to conduct business. Linde and its subsidiaries may in the future become subject to further claims and litigation, which is impossible to predict. The litigation and other claims Linde faces are subject to inherent uncertainties. Legal or regulatory judgments or agreed settlements might give rise to expenses which are not covered, or are not fully covered, by insurance benefits and may also lead to negative publicity and reputational damage. An unfavorable outcome or determination could cause a material adverse impact on the company’s results of operations.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm｜as_of：2026-02-25
<<<
•On and after April 23, 2019 former shareholders of Linde AG filed appraisal proceedings at the District Court (Landgericht) Munich I (Germany), seeking an increase of the cash consideration paid in connection with the previously completed cash merger squeeze-out of all of Linde AG’s minority shareholders for €189.46 per share. Any such increase would apply to all 14,763,113 Linde AG shares that were outstanding on April 8, 2019, when the cash merger squeeze-out was completed. The period for plaintiffs to file claims expired on July 9, 2019. In 83 Table of Contents November 2023, the court issued a decision rejecting the plaintiffs’ claims in their entirety and determining that the cash merger squeeze-out consideration was appropriate. The plaintiffs have appealed this decision.

Dispute resolution provisions In accordance with the dispute resolution provisions of the agreements, in 2023, Linde filed a notice of arbitration with the Hong Kong International Arbitration Centre ("HKIAC") against RCA to claim that (i) RCA has no entitlement to payment, (ii) RCA’s Russian Claims are in breach of the arbitration agreement which requires HKIAC arbitration, and (iii) RCA must compensate Linde for the losses and damages caused by the injunction. During 2024, Linde secured awards on exclusive jurisdiction with HKIAC.

Despite the judgments of the Hong Kong court and similar orders issued by the HKIAC arbitration tribunals, RCA is continuing to pursue its claims in Russia and neither the St. Petersburg injunction affecting Linde’s shares and assets has been lifted, nor the proceeding in St. Petersburg been stayed. The HKIAC arbitration proceedings are ongoing.

Linde intends to claim all damages related to or rising from RCA's enforcement of the GPP and LNG Decisions in the HKIAC arbitration proceedings. Linde subsidiaries affected by the GPP Decision have also filed claims for damages against RCA and/or its controlling shareholder in the Southern District of New York, the Netherlands and Germany.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001707925&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-31 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-13 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-01 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-12-03 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2025-11-20 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2025-12-03，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1707925/000119312525306646/d51438d8k.htm｜as_of：2025-12-03
<<<
Item 1.01. Entry into a Material Definitive Agreement.
364-Day Credit Agreement
On December 3, 2025, Linde plc (the “Company”) and certain of its subsidiaries entered into an unsecured 364-day revolving credit agreement (the “Credit Agreement”) with Bank of America, N.A., as administrative agent, and a syndicate of banking institutions as lenders.
The initial borrowers under the Credit Agreement are the Company, Linde Inc., Linde GmbH and Linde Finance B.V. Additional subsidiaries of the Company may become borrowers under the Credit Agreement, subject to satisfaction of customary conditions.
The Company fully and unconditionally guarantees all obligations of the subsidiary borrowers under the Credit Agreement. Linde Inc. and Linde GmbH also fully and conditionally guarantee all obligations of the Company under the Credit Agreement. Under certain circumstances, certain other subsidiaries of the Company may become subsidiary guarantors under the Credit Agreement.
The Credit Agreement provides for total commitments of $1,500,000,000.
The Credit Agreement is available for general corporate purposes of the Company and its subsidiaries. Revolving loans may be borrowed in U.S. Dollars, Pounds Sterling, Euros and other currencies agreed to by the administrative agent and the lenders. The Credit Agreement also includes commitments for swingline loans of up to $50,000,000 (for U.S. Dollar-denominated swingline loans) and up to €25,000,000 (for Euro-denominated swingline loans).…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-13，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1707925/000119312526221558/d108557d8k.htm｜as_of：2026-05-13
<<<
Item 8.01.
Other Events.
On May 13, 2026, Linde plc (the “Company”) issued €600 million aggregate principal amount of Floating Rate Notes due 2028 (the “2028 Notes”), issued €500 million aggregate principal amount of 3.200% Notes due 2030 (the “2030 Notes”) and issued €500 million aggregate principal amount of 3.800% Notes due 2036 (the “2036 Notes”). The 2028 Notes, the 2030 Notes and the 2036 Notes were issued pursuant to a Subscription Agreement, dated May 11, 2026, by and among the Company, as issuer, and the financial institutions named as bookrunners and other managers therein (the “Managers”). The terms of the 2028 Notes, the 2030 Notes and the 2036 Notes are set out in the Final Terms filed as Exhibit 4.1 which is incorporated herein by reference.
The net proceeds of the offering were approximately €1,595 million, after giving effect to the fees to the Managers but before other fees and expenses of the offering. Net proceeds of the offering will be used for general corporate purposes.
The 2028 Notes, the 2030 Notes and the 2036 Notes have been admitted to the official list of the Luxembourg Stock Exchange and for trading on the Euro MTF market operated by the Luxembourg Stock Exchange.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2025-11-20，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1707925/000119312525289724/d11623d8k.htm｜as_of：2025-11-20
<<<
Item 8.01.
Other Events.
On November 20, 2025, Linde plc (the “Company”) issued €600 million aggregate principal amount of Floating Rate Notes due 2027 (the “2027 Notes”), issued €650 million aggregate principal amount of 3.125% Notes due 2032 (the “2032 Notes”) and issued €500 million aggregate principal amount of 3.750% Notes due 2038 (the “2038 Notes”). The 2027 Notes, the 2032 Notes and the 2038 Notes were issued pursuant to a Subscription Agreement, dated November 18, 2025, by and among the Company, as issuer, and the financial institutions named as bookrunners and other managers therein (the “Managers”). The terms of the 2027 Notes, the 2032 Notes and the 2038 Notes are set out in the Final Terms filed as Exhibit 4.1 which is incorporated herein by reference.
The net proceeds of the offering were approximately €1,737 million, after giving effect to the fees to the Managers but before other fees and expenses of the offering. Net proceeds of the offering will be used for general corporate purposes.
The 2027 Notes, the 2032 Notes and the 2038 Notes have been admitted to the official list of the Luxembourg Stock Exchange and for trading on the Euro MTF market operated by the Luxembourg Stock Exchange.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
