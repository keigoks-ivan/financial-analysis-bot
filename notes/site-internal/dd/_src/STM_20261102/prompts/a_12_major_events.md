你是 stock-analyst v20 DD 的證據採集子 agent。標的：STM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - STM STMicroelectronics acquisition merger 2025 2026
  - STM STMicroelectronics class action lawsuit securities fraud
  - STM STMicroelectronics clinical trial FDA approval 2025 2026
  - STM STMicroelectronics product launch recall warning letter
  - STM STMicroelectronics SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 8. Financial Information（含 8.A.7 Legal Proceedings）｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
Item 8. Financial Information
Consolidated Statements and Other Financial Information
Please see “Item 18. Financial Statements” for a list of the financial statements filed with this Form 20-F.
Legal Proceedings
For a description of our material pending legal proceedings, please see Note 26 “Commitments, Contingencies, Claims and Legal Proceedings” to our Consolidated Financial Statements, which is incorporated herein by reference.
Dividend Policy
Our dividend policy reads as follows: “STMicroelectronics seeks to use its available cash in order to develop and enhance its position in a competitive semiconductor market while at the same time managing its cash resources to reward its shareholders for their investment and trust in STMicroelectronics. Based on its results, projected capital requirements as well as business conditions and prospects, the Managing Board proposes on an annual basis to the Supervisory Board, whenever deemed possible and desirable in line with STMicroelectronics’ objectives and financial situation, the distribution of a quarterly cash dividend, if any. The Supervisory Board, upon the proposal of the Managing Board, decides or proposes on an annual basis, in accordance with this policy, which portion of the profits or distributable reserves shall not be retained in reserves to fund future growth or for other purposes and makes a proposal concerning the amount, if any, of the quarterly cash dividend”.
On May 28, 2025, our shareholders approved a cash dividend of US$0.36 per outstanding share of our common stock, which was distributed in quarterly installments of US$0.09 in each of the second, third and fourth quarters of 2025 and will also be distributed in the first quarter of 2026. Future dividends, if any, and their timing and amounts may be affected by our accumulated profits, our capacity to generate cash flow, our financial situation, the general economic situation and prospects and any other factors that the Supervisory Board, upon the recommendation of our Managing Board, shall deem important. For a history of dividends paid by us to our shareholders in the past three years, see Note 18 to our Consolidated Financial Statements “Shareholders’ Equity – Dividends”.
Item 9. Listing
Market Information…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 5. Operating and Financial Review（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
Our insurance policy relating to product liability covers third-party physical damages and bodily injury, indirect financial damages as well as immaterial non-consequential damages caused by defective products.
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
The Company’s insurance policy relating to product liability covers third-party physical damages and bodily injury, indirect financial damages as well as immaterial non-consequential damages caused by defective products.

On August 23, 2024, two lawsuits were filed against the Company, and its CEO and CFO, in the United States District Court for the Southern District of New York alleging that the Company provided excessively positive statements to investors concerning 2024 expected revenue and issued false or F-62 misleading statements or concealed negative facts regarding the Company’s business, operations, and prospects, in violation of U.S. securities laws. The lawsuits were consolidated into a single lawsuit and thereafter the plaintiff filed amended complaints asserting claims for violation of Sections 10(b) and 20(a) of the Securities Exchange Act, and expanding the purported class period from March 14, 2023, to January 29, 2025. The Company and its CEO and CFO moved to dismiss the lawsuit which motion was denied by the Court on September 15, 2025. The Company and its CEO and CFO believe that they have strong legal defenses against the allegations in the amended complaints and will vigorously defend themselves in court.

On December 4, 2023, a jury in the United States District Court for the Western District of Texas in Waco, Texas (USA) returned a verdict in a patent infringement lawsuit in favor of the plaintiff, Purdue University. On June 7, 2024, the Court accepted the jury's verdict and entered a judgment against the Company in the amount of $32 million. Thereafter, the Company filed several post-trial motions challenging the verdict. In the event the Court denies the Company's post-trial motions, the Company intends to appeal to the U.S. Court of Appeals for the Federal Circuit in Washington DC. The risk on this case is considered possible with the possible loss currently estimated at $32 million.
>>>

[4] 來源：SEC EDGAR｜文件：6-K 申報清單（近12個月）｜章節：6-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000932787&type=6-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 43 份 6-K（外國發行人以 6-K 公告，無 Item 編號）。
2026-10-29 6-K 6-K
2026-10-29 6-K 6-K
2026-10-26 6-K 6-K
2026-10-19 6-K 6-K
2026-10-13 6-K 6-K
2026-10-13 6-K 6-K
2026-10-05 6-K 6-K
2026-08-31 6-K 6-K
2026-08-25 6-K CURRENT REPORT
2026-08-19 6-K REPORT OF FOREIGN PRIVATE ISSUER
2026-08-19 6-K 6-K
2026-08-17 6-K 6-K
2026-08-10 6-K 6-K
2026-08-04 6-K 6-K
2026-07-30 6-K 6-K
2026-07-27 6-K 6-K
2026-07-23 6-K 6-K
2026-07-20 6-K 6-K
2026-07-13 6-K REPORT OF FOREIGN PRIVATE ISSUER
2026-07-06 6-K 6-K
2026-06-16 6-K REPORT OF FOREIGN PRIVATE ISSUER
2026-06-16 6-K REPORT OF FOREIGN PRIVATE ISSUER
2026-06-02 6-K 6-K
2026-05-27 6-K 6-K
2026-05-27 6-K 6-K
2026-05-04 6-K 6-K
2026-04-23 6-K 6-K
2026-03-27 6-K 6-K
2026-03-26 6-K 6-K
2026-03-02 6-K 6-K
2026-02-26 6-K 6-K
2026-02-09 6-K REPORT OF FOREIGN PRIVATE ISSUER
2026-02-02 6-K 6-K
2026-01-29 6-K 6-K
2025-12-18 6-K 6-K
2025-12-15 6-K 6-K
2025-12-11 6-K 6-K
2025-12-01 6-K 6-K
2025-11-24 6-K 6-K
2025-11-17 6-K REPORT OF FOREIGN PRIVATE ISSUER
2025-11-10 6-K REPORT OF FOREIGN PRIVATE ISSUER
2025-11-05 6-K 6-K
2025-11-03 6-K REPORT OF FOREIGN PRIVATE ISSUER
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
