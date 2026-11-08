你是 stock-analyst v20 DD 的證據採集子 agent。標的：CAH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - CAH Cardinal Health antitrust OR monopoly investigation 2026
  - Cardinal Health regulation OR regulatory scrutiny Medical Distribution 2026
  - CAH Cardinal Health DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-11）｜章節：全文（無法依 Item 切段）｜url：https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm｜as_of：2026-08-11
<<<
GAAP operating earnings for fiscal 2026 increased 15% to $2.6 billion from the prior year. The increase in GAAP operating earnings was driven by the increased contribution from branded and specialty pharmaceuticals and the performance of our generics program in our Pharma segment, the impact of the acquisitions of MSO platforms and ADS, and growth from existing customers in our GMPD segment. This increase was partially offset by the $184 million pre-tax goodwill impairment charge recognized in fiscal 2026 related to the Navista & Integrated Oncology Network ("ION") reporting unit within our Pharma segment, higher cash and share-based compensation costs resulting from the timing of acquisitions within The Specialty Alliance, and $171 million of net recoveries in class action antitrust litigation recognized in fiscal 2025. See "Critical Accounting Policies and Sensitive Accounting Estimates" section of this MD&A and Note 4 of the "Notes to the Consolidated Financial Statements" for further information on the goodwill impairment.

Cardinal Health | Fiscal 2026 Form 10-K 29 Business Regulatory Matters Our business is highly regulated in the United States, at both the federal and state level, and in foreign countries. Depending upon the specific business, we may be subject to regulation by government entities including: •the U.S. Drug Enforcement Administration (the “DEA”); •certain agencies within the U.S. Department of Health and Human Services, including the U.S. Food and Drug Administration (the “FDA”), the Centers for Medicare and Medicaid Services, the Office of Inspector General, and the Office for Civil Rights; •state and local health departments, insurance departments, Medicaid departments, or other comparable state agencies; •state and local boards of pharmacy and other controlled substance authorities; •the U.S. Nuclear Regulatory Commission (the “NRC”); •the U.S. Environmental Protection Agency and state environmental authorities; •the U.S. Federal Trade Commission (the "FTC"); •U.S. Customs and Border Protection (the "CBP"); and •agencies comparable to those listed above in markets outside the United States.

Antitrust Laws The U.S. federal government, most U.S. states, and many foreign countries have laws that prohibit certain types of conduct deemed to be anti-competitive. Violations of these laws can result in various sanctions, including criminal and civil penalties. Private plaintiffs also could bring civil lawsuits against us in the United States for alleged antitrust law violations, including claims for treble damages.

We are required to comply with laws relating to healthcare fraud and abuse. The requirements of these laws are complex and subject to varying interpretations. From time to time, regulatory authorities, including the DOJ, FDA, DEA, and FTC, investigate our policies or practices, and may challenge them. For example, in November 2023, we received a Civil Investigative Demand ("CID") from the Department of Justice focused on potential violations of the Anti-Kickback Statute and False Claims Act in connection with a 2022 transaction in which we purchased a group purchasing organization and a minority ownership interest in a rheumatology managed services organization. We are cooperating with this investigation. We are also periodically subject to federal or state government investigations or qui tam actions (false claims cases initiated by private parties purporting to act on behalf of federal or state governments), which could result in civil or criminal sanctions, including the loss of licenses or the ability to participate in Medicare, Medicaid, and other federal and state healthcare programs or other remedial measures.

Department of Justice Civil Investigative Demand In November 2023, we received a Civil Investigative Demand ("CID") from the Department of Justice focused on potential violations of the Anti-Kickback Statute and False Claims Act in connection with a 2022 transaction in which we purchased a minority ownership interest in a rheumatology managed services organization and a group purchasing organization. We are cooperating with this investigation.

Antitrust Litigation Proceeds We recognized income for net recoveries in class action antitrust lawsuits in which we were a class member or plaintiff of $24 million, $171 million, and $117 million during fiscal 2026, 2025, and 2024, respectively.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
