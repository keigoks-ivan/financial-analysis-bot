你是 stock-analyst v20 DD 的證據採集子 agent。標的：AAPL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - AAPL Apple antitrust OR monopoly investigation 2026
  - Apple regulation OR regulatory scrutiny Consumer Electronics 2026
  - AAPL Apple DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-03）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm｜as_of：2026-11-03
<<<
Item 3. Legal Proceedings
Digital Markets Act Investigations
On March 25, 2024, the Commission announced that it had opened a formal noncompliance investigation against the Company under Article 5(4) of the EU DMA (“Article 5(4) Investigation”). The Article 5(4) Investigation relates to how developers may communicate and promote offers to end users for apps distributed through the App Store, as well as how developers may conclude contracts with those end users. On June 24, 2024, the Commission announced that it had opened an additional formal investigation against the Company regarding whether the Company’s new contractual requirements for third-party app developers and app marketplaces may violate the DMA (“Article 6(4) Investigation”). On April 23, 2025, the Commission fined the Company €500 million in the Article 5(4) Investigation and issued a cease and desist order requiring the Company to remove technical and commercial restrictions that prevent developers from steering users to alternative distribution channels outside the App Store. The Company has appealed the Commission’s Article 5(4) decision. Also on April 23, 2025, the Commission issued preliminary findings in the Article 6(4) Investigation. If the Commission makes a final determination in the Article 6(4) Investigation that there has been a violation, it can issue a cease and desist order and may impose fines up to 10% of the Company’s annual worldwide net sales. The Commission may also seek to impose additional fines if it deems that the Company has violated a cease and desist order. The Company believes that it complies with the DMA and has continued to make changes to its compliance plan in response to feedback and engagement with the Commission.
Apple Inc. | 2026 Form 10-K | 20
Department of Justice Lawsuit
On March 21, 2024, the DOJ and a number of state and district attorneys general filed a civil antitrust lawsuit in the U.S. District Court for the District of New Jersey against the Company alleging monopolization or attempted monopolization in the markets for “performance smartphones” and “smartphones” in violation of U.S. antitrust laws.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm｜as_of：2026-11-03
<<<
The Company has also continued to make changes to its DMA compliance plan in response to feedback and engagement with the European Commission (“Commission”). Although the Company’s DMA compliance plan is intended to address the DMA’s obligations, it has been challenged by the Commission and may be challenged further by private litigants. The DMA provides for significant fines and penalties for noncompliance. While the changes introduced by the Company in the EU are intended to reduce new privacy and security risks that the DMA poses to EU users, many risks will remain. Changes to the Company’s business in response to the DMA or other laws and regulations in the EU or in other jurisdictions, including the U.S., could materially adversely affect the Company’s business, reputation, results of operations, financial condition and stock price.

The Company is also currently subject to antitrust investigations and litigation in various jurisdictions around the world, which can result in legal proceedings and claims that could, individually or in the aggregate, have a material adverse effect on the Company’s business, reputation, results of operations, financial condition and stock price. For example, the Company is subject to civil antitrust lawsuits in the U.S. alleging monopolization or attempted monopolization in the markets for “performance smartphones” and “smartphones” generally in violation of U.S. antitrust laws. In addition, the Company is the subject of investigations in Europe and other jurisdictions relating to App Store terms and conditions. If such investigations or litigation are resolved against the Company, the Company can be exposed to significant fines and other penalties and may be required to make further changes to its business practices.

Apple Inc. | 2026 Form 10-K | 16 Further, the Company has commercial relationships with other companies in the technology industry that are or may become subject to investigations and litigation that, if resolved against those other companies, could materially adversely affect the Company’s commercial relationships with those business partners. For example, the Company earns revenue from licensing arrangements with Google LLC (“Google”) and other companies to offer their search services on the Company’s platforms and applications, and certain of these arrangements are currently subject to government investigations and legal proceedings. On August 5, 2024, Google was found to have violated U.S. antitrust laws. In connection with this finding, on September 2, 2025, the U.S. District Court for the District of Columbia (“D.C. District Court”) ordered certain remedies. The court’s order is subject to further proceedings before the D.C. District Court, which may result in changes to the interpretation or application of the remedies ordered by the court, as well as new or changed remedies being ordered. The court’s order was appealed by both the U.S. Department of Justice (“DOJ”) and Google. A reversal of the order on appeal could result in the imposition of certain remedies initially proposed by the DOJ, such as those prohibiting Google from offering the Company commercial terms for search distribution.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-03）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm｜as_of：2026-11-03
<<<
Apple Inc. | 2026 Form 10-K | 20 Department of Justice Lawsuit On March 21, 2024, the DOJ and a number of state and district attorneys general filed a civil antitrust lawsuit in the U.S. District Court for the District of New Jersey against the Company alleging monopolization or attempted monopolization in the markets for “performance smartphones” and “smartphones” in violation of U.S. antitrust laws. The DOJ is seeking equitable relief to redress the alleged anticompetitive behavior. In addition, various civil litigation matters have been filed in state and federal courts in the U.S. alleging similar violations of U.S. antitrust laws and seeking monetary damages and other nonmonetary relief. The Company believes it has substantial defenses and intends to vigorously defend itself.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
