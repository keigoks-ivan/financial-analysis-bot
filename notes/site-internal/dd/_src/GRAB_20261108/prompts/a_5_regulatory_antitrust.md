你是 stock-analyst v20 DD 的證據採集子 agent。標的：GRAB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - GRAB Grab Holdings antitrust OR monopoly investigation 2026
  - Grab Holdings regulation OR regulatory scrutiny Software - Application 2026
  - GRAB Grab Holdings DOJ OR FTC OR EU competition 2026
  (na_allowed=true)


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

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
We operate across the deliveries, mobility and financial services segments in over 900 cities in the large, diverse and complex Southeast Asian region. Each of our segments is subject to numerous and often conflicting or evolving regulations from various regulators in each jurisdiction in which we operate. Focus areas of regulatory risk that we are exposed to include, among others: (i) evolution of laws and regulations applicable to deliveries, mobility and/or financial services (including digital bank) offerings, (ii) various forms of data regulation such as data privacy, data localization, data portability, cybersecurity and advertising or marketing, (iii) gig economy regulations, (iv) anti-trust regulations, (v) digital platform regulations, (vi) economic regulations such as price, supply regulation, safety, health and environment regulations, (vii) foreign ownership restrictions, (viii) AI regulation and (ix) regulations regarding the provision of online services, including with respect to the internet, mobile devices and e-commerce.

Competition authorities closely scrutinize us. Antitrust regulators in Southeast Asia and elsewhere are taking a greater interest in potential abuses of market power, anti-competitive agreements, and transactions that lead to substantial lessening of competition or entrenching or strengthening a dominant position, involving big technology companies. If one jurisdiction imposes or proposes to impose new requirements or restrictions on our business or transactions, other jurisdictions may follow suit, which could result in adverse publicity, significant fines, or prevent the implementation of transactions, whether or not valid or subject to appeal.
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
75 Table of Contents Antitrust and Competition Laws Antitrust and Competition laws are in force across all jurisdictions in which we operate and generally focus on three key prohibitions affecting the provision of goods and services in any relevant market: anti-competitive agreements, abuse of a dominant position and mergers which substantially lessen competition or entrench or strengthen a dominant position.

Key Prohibitions The first prohibition is against anti-competitive agreements. These are agreements, often between competitors, that prevent, restrict or distort competition. Typical examples include price-fixing, market allocation (or market-sharing), bid-rigging, and restrictions on output or supply, which are classified as inherently illegal or per se violations in many jurisdictions. Other types of agreements may be illegal if they have the object or effect of a restriction of competition.

The third prohibition is against acquisitions, mergers and consolidations that substantially lessen competition or entrench or strengthen a dominant position in the relevant market for the provision of goods and services in question. In most of the jurisdictions in which we operate, transactions meeting certain financial and/or market share thresholds must be notified to the relevant competition authority for pre- or post-closing clearance or review, as the case may be. Competition authorities generally have the power to review such transactions, approve them, impose conditions such as structural and/or behavioral remedies, or prohibit such transactions.

Enforcement and Penalties Antitrust and Competition laws grant independent competition authorities the power to supervise and enforce the law. Non-compliance can result in severe sanctions, including: •Financial Penalties: Fines are frequently calculated as a percentage of the company's turnover or total sales in the relevant market during the period of infringement. In many jurisdictions, these penalties can reach up to 10% of total domestic or worldwide turnovers, and in the case of Indonesia, it can reach up to 50% of the net profit in the relevant market for the non-compliant period. In certain jurisdictions, additional fixed fines may apply for failure to report notifiable transactions.

•Criminal Penalties: In certain jurisdictions in which we operate, directors and responsible persons may face personal criminal liability for breaches of antitrust and competition laws. Conviction can result in imprisonment, criminal fines, or both. Criminal penalties may also be imposed on individuals for obstructing investigations or failing to comply with investigative orders. In addition, criminal fines may be imposed directly on the entity which committed the violation.
>>>


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
  }
}
```

`clues` 選填、每軸一個陣列，沒有就整個欄位省略。只在你**找到有網址的線索、但沒讀到頁面而拿不到可逐字複製的原文**時放；程式會打開該網址，在全文裡找 `match_terms` 同時出現的一段原文，找到就升級成帶原文的 finding；找不到（或頁面打不開）就照 `excerpt_from: "snippet"`、`excerpt: null` 的 finding 保留，並標為未核原文。
- 只有 clues、findings 是空的時，`status` 填 `none`（程式核實到原文後會自動改成 `found`）。
- `url` 必須是你在搜尋結果裡實際看到的網址；不得編造、不得猜網址、不得填網站首頁。沒有網址的線索不要放（寫進 note）。已經寫在 findings 的網址不要重複放。
- `match_terms` 放 2～5 個預期原文會逐字出現的字串：金額、比例、專有名詞、引號裡的關鍵詞。照原文可能的寫法填，不要改寫或翻譯；不要放公司名、代號、年份或「營收」「公司」這類到處都有的詞。
- 其餘欄位（`claim`、`source`、`as_of`、`direction`、`affects`）規則同 findings；`as_of` 填你推估的文章發布日，程式讀到頁面發布日會以頁面為準。

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
