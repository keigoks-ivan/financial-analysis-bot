你是 stock-analyst v20 DD 的證據採集子 agent。標的：GRAB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - GRAB Grab Holdings acquisition merger 2025 2026
  - GRAB Grab Holdings class action lawsuit securities fraud
  - GRAB Grab Holdings clinical trial FDA approval 2025 2026
  - GRAB Grab Holdings product launch recall warning letter
  - GRAB Grab Holdings SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 8. Financial Information（含 8.A.7 Legal Proceedings）｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
ITEM 8. FINANCIAL INFORMATION
A.Consolidated Statements and Other Financial Information
Financial Statements
Consolidated financial statements have been filed as part of this annual report.
Legal Proceedings
We are from time to time involved in private actions, collective actions, class actions, investigations and various other legal proceedings by consumers, driver- and merchant-partners, restaurants, employees, commercial partners, competitors and government agencies, among others, relating to, for example, personal injury or property damage cases, employment or labor-related disputes such as worker classification, wrongful termination of employment, consumer complaints, disputes with driver- and merchant-partners, contractual disputes with suppliers or commercial partners, disputes with third parties and regulatory inquiries and proceedings relating to compliance with competition, consumer protection, privacy or other applicable regulations. We may also initiate various legal proceedings such as against former employees, suppliers or driver- and merchant-partners to enforce our rights. There are inherent uncertainties in these matters, some of which are beyond our management’s control, making the ultimate outcomes difficult to predict.
Information is provided below regarding the nature and status of certain legal proceedings against Grab. Other than as set forth below, we are not a party to, nor are we aware of, any legal proceeding, investigation or claim which, in the opinion of our management, is likely to have a material adverse effect on our business, financial condition or results of operations.
Government Proceedings
In Indonesia, the Business Competition Supervisory Commission (“KPPU”) has raised its concern on the fairness in partnerships between large and medium enterprises with small and micro enterprises. In 2024 and 2025, KPPU investigated our partnership arrangements with driver-partners for (i) GrabExpress and GrabFood delivery and (ii) special rental transportation with other ride-hailing applicators. In addition, KPPU has initiated proceedings regarding a cartel allegation involving the determination of P2P interest rates by the Indonesian Fintech Peer-to-Peer Funding Association,of which our relevant subsidiary is a member. The proceedings are still ongoing.
Other Actions
We are currently also involved in the following actions:…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 3. Key Information (含 3.D Risk Factors)（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
The market price of our Class A Ordinary Shares and Warrants may be volatile and, in the past, companies that have experienced volatility in the market price of their stock have been subject to securities class action litigation. We have been and may be the target of this type of litigation and investigations. Beginning in March 2022, various putative shareholder class action lawsuits were filed against our Company and certain of its officers in the U.S. District Court for the Southern District of New York, which were later consolidated under the caption In re Grab Holdings Limited Securities Litigation, No. 1:22-cv-02189-VM. On August 22, 2022, Lead Plaintiffs filed an Amended Class Action Complaint against the Company, certain of its officers and directors, and certain officers and directors of Altimeter Growth Corp. The class action was purportedly brought on behalf of various classes of persons who allegedly suffered damages as a result of alleged misstatements and omissions regarding our proxy and registration statements, business operations, potential impact on our financial results, and future prospects, in violation of the U.S. Securities Act, the U.S. Securities Exchange Act of 1934, and Rules 10b-5 and 14a-9 promulgated thereunder. On March 12, 2024, the Court granted in part and denied in part Defendants’ motion to dismiss.…
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 8. Financial Information（含 8.A.7 Legal Proceedings）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
Other Actions We are currently also involved in the following actions: •On September 21, 2021, Grab Greco LLP was served with a claim in the Bangalore City Civil Court in India by a former employee and a company from which Grab Greco LLP had acquired intellectual property assets in 2018. The plaintiffs allege that Grab’s wallet platform breaches the plaintiffs’ intellectual property rights. The relief sought from the Bangalore City Civil Court includes an injunction to restrain Grab from using the claimants’ purported copyright and patents and an account of profits. Grab believes the case has no merit and is contesting it on the basis that, among other things, Grab completed the purchase of the relevant intellectual property in 2018. The case was dismissed on May 31, 2023 but the plaintiffs have since filed a petition to review the dismissal and the petition is pending.
>>>

[4] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
v) Accrued operating expenses These amounts include $80 million related to a settlement in 2024 with regard to class action lawsuits filed against the Company and certain of its officers in 2022. The associated accrual was settled in 2025.
>>>

[5] 來源：SEC EDGAR｜文件：6-K 申報清單（近12個月）｜章節：6-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001855612&type=6-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 32 份 6-K（外國發行人以 6-K 公告，無 Item 編號）。
2026-11-03 6-K 6-K
2026-11-03 6-K 6-K
2026-10-30 6-K 6-K
2026-10-30 6-K 6-K
2026-09-15 6-K 6-K
2026-09-15 6-K 6-K
2026-09-15 6-K 6-K
2026-08-13 6-K 6-K
2026-08-04 6-K 6-K
2026-08-04 6-K 6-K
2026-07-06 6-K 6-K
2026-07-06 6-K 6-K
2026-07-01 6-K 6-K
2026-05-20 6-K 6-K
2026-05-20 6-K 6-K
2026-05-05 6-K 6-K
2026-05-05 6-K 6-K
2026-03-24 6-K 6-K
2026-03-24 6-K 6-K
2026-03-24 6-K 6-K
2026-03-23 6-K 6-K
2026-03-23 6-K 6-K
2026-02-20 6-K 6-K
2026-02-11 6-K 6-K
2026-02-11 6-K 6-K
2026-02-11 6-K 6-K
2026-02-11 6-K 6-K
2025-12-01 6-K 6-K
2025-12-01 6-K 6-K
2025-11-12 6-K 6-K
2025-11-10 6-K 6-K
2025-11-10 6-K 6-K
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
