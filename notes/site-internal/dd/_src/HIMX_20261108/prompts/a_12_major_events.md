你是 stock-analyst v20 DD 的證據採集子 agent。標的：HIMX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - HIMX Himax Technologies acquisition merger 2025 2026
  - HIMX Himax Technologies class action lawsuit securities fraud
  - HIMX Himax Technologies clinical trial FDA approval 2025 2026
  - HIMX Himax Technologies product launch recall warning letter
  - HIMX Himax Technologies SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 8. Financial Information（含 8.A.7 Legal Proceedings）｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
ITEM 8. FINANCIAL INFORMATION
8.A. Consolidated Statements and Other Financial Information
8.A.1. See “Item 18. Financial Statements” for our audited consolidated financial statements.
8.A.2. See “Item 18. Financial Statements” for our audited consolidated financial statements, which cover the last three financial years.
8.A.3. See page F-2 for the report of our independent registered public accounting firm.
8.A.4. Not applicable.
Table of Contents
8.A.5. Not applicable.
8.A.6. See Note 28 to our audited consolidated financial statements included in “Item 18. Financial Statements.”
8.A.7. Litigation
We may be subject to legal proceedings, investigations and claims relating to the conduct of our business from time to time. We may also initiate legal proceedings in order to protect our contractual and property rights. However, as of the date of this annual report, we are not currently a party to, nor are we aware of, any legal proceeding, investigation or claim which, in the opinion of our management, is likely to have a material adverse effect on our business, financial condition or results of operations.
8.A.8. Dividends and Dividend Policy
Subject to the Cayman Islands Companies Law, we may declare dividends in any currency, but no dividend may be declared in excess of the amount recommended by our board of directors. Whether our board of directors recommends any dividends and the form, frequency and amount of dividends, if any, will depend upon our future operations and earnings, capital requirements and surplus, general financial condition, contractual restrictions and other factors as the board of directors may deem relevant.
On June 27, 2008, we paid a cash dividend in the amount of $66.8 million, or the equivalent of $0.350 per ADS. In 2009, we paid a cash dividend on June 29, 2009 in the amount of $55.5 million, or the equivalent of $0.300 per ADS, and distributed a stock dividend on August 10, 2009 of 5,999 ordinary shares of par value $0.0001 for each ordinary share of par value $0.0001 held by shareholders of record as of August 7, 2009.…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 3. Key Information (含 3.D Risk Factors)（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
The semiconductor industry is characterized by vigorous protection and pursuit of intellectual property rights and positions, which results in protracted and expensive litigation for many companies. We have received, and expect to continue to receive, notices of infringement of third-party intellectual property rights. We may receive claims from various industry participants alleging infringement of their patents, trade secrets or other intellectual property rights in the future. Any lawsuit resulting from such allegations could subject us to significant liability for damages and invalidate our proprietary rights. These lawsuits, regardless of their success, would likely be time-consuming and expensive to resolve and would divert management time and attention. Any potential intellectual property litigation also could force us to do one or more of the following: (1) desist and stop selling products or using technology or manufacturing processes that contain the allegedly infringing intellectual property; (2) pay damages to the party claiming infringement; (3) attempt to obtain a license for the relevant intellectual property, which may not be available on commercially reasonable terms or at all; and (4) attempt to redesign those products that contain the allegedly infringing intellectual property with non-infringing intellectual property, which may not be possible.
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
81 Table of Contents At our annual general meeting on August 6, 2009, our shareholders adopted the Second Amended and Restated Memorandum and Articles of Association, which became effective on August 10, 2009 and were filed as exhibits to our current report on Form 6-K with the SEC on July 13, 2009. These were adopted primarily in connection with our proposed Taiwan listing to meet the Taiwan Stock Exchange’s primary listing requirement concerning protection of material shareholders’ rights under the ROC’s Company Act and Securities Exchange Act. At the same time, our shareholders also adopted the Third Amended and Restated Memorandum and Articles of Association, which were filed as an exhibit to our annual report on Form 20-F for the fiscal year ended December 31, 2009 with the SEC on June 3, 2010 and are substantially the same as the Amended and Restated Memorandum and Articles of Association of our company except that our authorized share capital is stated to be $300,000,000 divided into 1,000,000,000 shares of nominal or par value of $0.3 each, on the condition that it shall become effective if the application made by our company to list its ordinary shares on the Taiwan Stock Exchange is rejected or aborted.…
>>>

[4] 來源：SEC EDGAR｜文件：6-K 申報清單（近12個月）｜章節：6-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001342338&type=6-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 8 份 6-K（外國發行人以 6-K 公告，無 Item 編號）。
2026-11-05 6-K FORM 6-K
2026-08-12 6-K FORM 6-K
2026-08-06 6-K FORM 6-K
2026-07-01 6-K FORM 6-K
2026-06-12 6-K FORM 6-K
2026-05-07 6-K FORM 6-K
2026-05-07 6-K FORM 6-K
2026-02-12 6-K FORM 6-K
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
