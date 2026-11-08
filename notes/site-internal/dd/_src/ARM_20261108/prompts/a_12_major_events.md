你是 stock-analyst v20 DD 的證據採集子 agent。標的：ARM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - ARM Arm Holdings acquisition merger 2025 2026
  - ARM Arm Holdings class action lawsuit securities fraud
  - ARM Arm Holdings clinical trial FDA approval 2025 2026
  - ARM Arm Holdings product launch recall warning letter
  - ARM Arm Holdings SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 8. Financial Information（含 8.A.7 Legal Proceedings）｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
Item 8. Financial Information
A. Consolidated Statements and Other Financial Information
Legal Proceedings
From time to time, we are involved in various legal, administrative, and regulatory proceedings, claims, demands and investigations relating to our business, which may include claims with respect to commercial, product liability, IP, cybersecurity, privacy, data protection, antitrust, breach of contract, labor and employment, whistleblower, mergers and acquisitions and other matters. In addition, under our customer agreements, we agree in some cases to indemnify our customers if a third party files a claim in court or another venue asserting that our products infringe such third party’s IP rights. Although we do not agree to indemnify our customers’ end customers, such end customers may be subject to infringement claims and may initiate claims against us as a result. We are currently involved in pending litigation, including, but not limited to, litigation proceedings with Qualcomm and Nuvia. See “Item 3. Key Information—D. Risk Factors—Risks Relating to Our Business and Industry—We are currently involved in pending litigation, and may in the future become involved in litigation, government investigations or regulatory proceedings that may adversely affect us.” In addition, our products are involved in pending litigation to which we are not a party. We cannot provide you any assurances regarding how any such litigation will be resolved, what benefits we will obtain or what losses we might incur. The results of any current or future litigation cannot be predicted with certainty, and regardless of the outcome, litigation can have an adverse impact on us because of defense and settlement costs, diversion of management resources and other factors. See “Item 3. Key Information—D. Risk Factors—Risks Relating to Our Business and Industry—We may be sued by third parties for alleged infringement, misappropriation or other violation of their IP rights or proprietary rights and our defense against these claims can be costly.”
Dividend Policy
We intend to retain any earnings for use in our business and do not currently intend to pay dividends on our ordinary shares or ADSs.…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
On January 7, 2026, Qualcomm’s motion seeking to add Arm Limited, our wholly-owned subsidiary through which we have historically conducted our business, to the April 2024 lawsuit was denied. Subsequently, Qualcomm filed a separate lawsuit against Arm Limited seeking to make the April 2024 lawsuit’s allegations against Arm Limited. In March 2026, the lawsuit against Arm Limited was consolidated with the April 2024 lawsuit against us. On March 30, 2026, Qualcomm filed an amended complaint against only Arm Limited seeking to add another breach of contract claim. We have moved to strike this new claim. We disagree with the assertions made by Qualcomm (as referred to above) and intend to vigorously defend against them. The case is expected to go to trial in the fourth calendar quarter of 2026.

If you or any other holders or beneficial owners of ADSs bring a claim against us or the depositary in connection with matters arising under the deposit agreement or the ADSs, including claims under federal securities laws, you or such other holder or beneficial owner may not be entitled to a jury trial with respect to such claims, which may have the effect of limiting and discouraging lawsuits against us and/or the depositary. If a lawsuit is brought against us and/or the depositary under the deposit agreement, it may be heard only by a judge or justice of the applicable trial court, which would be conducted according to different civil procedures and may result in different outcomes than a trial by jury would have had, including results that could be less favorable to the plaintiff(s) in any such action, depending on, among other things, the nature of the claims, the judge or justice hearing such claims, and the venue of the hearing.
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 5. Operating and Financial Review（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
On January 7, 2026, Qualcomm’s motion seeking to add Arm Limited, our wholly-owned subsidiary through which we have historically conducted our business, to the April 2024 lawsuit was denied. Subsequently, Qualcomm filed a separate lawsuit against Arm Limited seeking to make the April 2024 lawsuit’s allegations against Arm Limited. In March 2026, the lawsuit against Arm Limited was consolidated with the April 2024 lawsuit against us. On March 30, 2026, Qualcomm filed an amended complaint against only Arm Limited seeking to add another breach of contract claim. We have moved to strike this new claim. We disagree with the assertions made by Qualcomm (as referred to above) and intend to vigorously defend against them. The case is expected to go to trial in the fourth calendar quarter of 2026.
>>>

[4] 來源：SEC EDGAR｜文件：6-K 申報清單（近12個月）｜章節：6-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001973239&type=6-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 13 份 6-K（外國發行人以 6-K 公告，無 Item 編號）。
2026-11-04 6-K 6-K
2026-11-04 6-K 6-K
2026-09-18 6-K 6-K
2026-09-10 6-K 6-K
2026-08-10 6-K 6-K
2026-07-29 6-K 6-K
2026-07-29 6-K 6-K
2026-05-06 6-K 6-K
2026-04-21 6-K 6-K
2026-03-24 6-K 6-K
2026-03-24 6-K 6-K
2026-02-04 6-K 6-K
2026-02-04 6-K 6-K
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
