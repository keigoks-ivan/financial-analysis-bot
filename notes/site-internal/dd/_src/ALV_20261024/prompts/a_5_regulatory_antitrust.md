你是 stock-analyst v20 DD 的證據採集子 agent。標的：ALV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - ALV Autoliv antitrust OR monopoly investigation 2026
  - Autoliv regulation OR regulatory scrutiny Auto Tier 1 / Passive Safety 2026
  - ALV Autoliv DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
Item 3. Legal Proceedings
In the ordinary course of its business, the Company is subject to legal proceedings brought by or against the Company and its subsidiaries.
See Note 19, Contingent Liabilities, to the Consolidated Financial Statements in this Annual Report for a summary of certain ongoing legal proceedings. Such information is incorporated into this Part I, Item 3 – “Legal Proceedings” by reference.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
We are involved from time to time in legal proceedings and our business may suffer as a result of adverse outcomes of current or future legal proceedings We are, from time to time, involved in litigation, regulatory proceedings, and commercial or contractual disputes that may be significant. These matters may include, without limitation, disputes with our suppliers and customers, intellectual property claims, shareholder litigation, government investigations, class action lawsuits, personal injury claims, product liability claims, environmental issues, antitrust, customs and VAT disputes, employment, and tax issues. In such matters, government agencies or private parties may seek to recover from us very large, indeterminate amounts in penalties or monetary damages (including, in some cases, treble or punitive damages) or seek to limit our operations in some way. The possibility exists that claims may be asserted against us and their magnitude may remain unknown for long periods of time. For example, we are currently in the early stages of a dispute with the Mexican tax authorities in relation to various issues dealing with certain manufacturing activities that occur in Mexico. An adverse result in this or other similar disputes could have a materially negative impact on our operating results and financial condition.…

13 We are and may be in the future subject to civil antitrust litigation that could negatively impact our business We have previously been the subject of an investigation by the European Commission (“EC”) regarding possible anti-competitive behavior among certain suppliers to the automotive vehicle industry that was resolved in 2019. We are subject to a civil antitrust lawsuit in Germany filed by a customer with respect to allegations over a decade ago and may be subject to such civil antitrust lawsuits in the future in countries that permit such civil claims, including lawsuits or other actions by our customers. These types of lawsuits require significant management time and attention and could result in significant expenses. Any unfavorable outcomes of such lawsuits could have a material adverse impact on our customer relationships, business prospects, reputation, operating results, cash flows, and financial condition, and our insurance may not mitigate such impact. See Note 19, Contingent Liabilities, to the Consolidated Financial Statements in this Annual Report.

21 Negative or unexpected tax developments could adversely affect our effective tax rate, operating results and financial condition Changes in, or changes in the application of, U.S. or foreign tax laws, regulations or accounting principles with respect to matters such as tax base, tax rates, transfer pricing, dividends and restrictions on certain forms of tax relief or limitations on favorable tax treatment could affect the calculation of our income taxes and other tax liabilities, our effective tax rate, and the carrying value of our deferred tax assets. Our annual tax rate is based on our income and the tax laws in the jurisdictions in which we operate. Because of our global operations we face uncertainties and judgments in the application of complex tax regulations in a multitude of jurisdictions. Significant judgment and estimation are required in determining our effective tax rate and in evaluating our tax positions, in many cases where the ultimate tax determination is uncertain. Although we believe that our tax estimates are reasonable, the final determination of our tax liability may be different from what is reflected in our historical income tax provisions and accruals. We are regularly examined by tax authorities around the world and in a number of jurisdictions, we are currently under examination, which inherently creates uncertainty.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
9.55 19 % 8.04 40 % Net cash provided by operating activities 1,157 9.3 % 1,059 7.8 % Return on capital employed, % 26.4 1.5 pp 25.0 7.3 pp 1) Reported figures impacted by costs for capacity alignments and antitrust related matters. See section Items affecting comparability and Note 13 to the Consolidated Financial Statements included herein.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
