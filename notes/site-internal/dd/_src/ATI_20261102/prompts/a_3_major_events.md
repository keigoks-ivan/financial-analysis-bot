你是 stock-analyst v20 DD 的證據採集子 agent。標的：ATI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - ATI ATI acquisition merger 2025 2026
  - ATI ATI class action lawsuit securities fraud
  - ATI ATI clinical trial FDA approval 2025 2026
  - ATI ATI product launch recall warning letter
  - ATI ATI SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm｜as_of：2026-02-20
<<<
Item 3. Legal Proceedings
From time to time, we become involved in various lawsuits, claims and proceedings relating to the conduct of our current and formerly owned businesses, including those pertaining to product liability, environmental, health and safety matters and occupational disease (including as each relates to alleged asbestos exposure), as well as patent infringement, commercial, government contracting, construction, employment, employee and retiree benefits, taxes, environmental, and stockholder and corporate governance matters. While we cannot predict the outcome of any lawsuit, claim or proceeding, our management believes that the disposition of any pending matters is not likely to have a material adverse effect on our financial condition or liquidity. The resolution in any reporting period of one or more of these matters, including those described above, however, could have a material adverse effect on our results of operations for that period.
In August 2024, the Company received notice that it and certain of its affiliates are parties to two lawsuits captioned (1) William L. Schoen, Mary J. Nesbit, Robin L. Rosewicz, George E. Poole and James E. Swartz, Jr., individually and as representatives of a class of participants and beneficiaries of the Allegheny Technologies Incorporated Pension Plan v. ATI Inc., The Allegheny Technologies Incorporated Pension Plan Administrative Committee, State Street Global Advisors Trust Co., and John Does 1-5 (Case No. 2:24-cv-01109) and (2) John Souza and Karen Souza, individually and as representatives on behalf of a class of similarly situated persons v. ATI Inc. and State Street Global Advisors Trust Co. (Case No. 2:24-cv-01214), both of which are filed in federal district court for the Western District of Pennsylvania. These lawsuits, which were consolidated in late 2024, assert various claims associated with the Company’s October 2023 purchase of group annuity contracts to transfer a portion of its U.S. qualified defined benefit pension plan obligations to Athene Annuity and Life Company and Athene Annuity & Life Assurance of New York. We filed a Motion to Dismiss the consolidated claims in January 2025.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm｜as_of：2026-02-20
<<<
Risks Associated with Current or Future Litigation and Claims. A number of lawsuits, claims and proceedings have been or may be asserted against us relating to the conduct of our currently and formerly owned businesses, including those pertaining to product liability, patent infringement, commercial disputes, government contracting, employment matters, employee and retiree benefits, taxes, environmental matters, personal injury and health and safety and occupational disease, and stockholder and corporate governance matters. Due to the uncertainties of litigation, we can give no assurance that we will prevail on all claims made against us in the lawsuits that we currently face or that additional claims will not be made against us in the future. While the outcome of litigation cannot be predicted with certainty, and some of these lawsuits, claims or proceedings may be determined adversely to us, we do not believe that the disposition of any such pending matters is likely to have a material adverse effect on our financial condition or liquidity. However, the resolution in any reporting period of one or more of these matters could have a material adverse effect on our results of operations for that period. Also, we can give no assurance that any other claims brought in the future will not have a material effect on our financial condition, liquidity or results of operations.

In August 2024, the Company received notice that it and certain of its affiliates are parties to two lawsuits, filed in federal district court for the Western District of Pennsylvania, that assert various claims associated with the Company’s October 2023 purchase of group annuity contracts to transfer a portion of its U.S. qualified defined benefit pension plan obligations to Athene Annuity and Life Company and Athene Annuity & Life Assurance of New York. These two lawsuits were consolidated in late 2024, and in January 2025, we filed a motion to dismiss the consolidated claims. Following an August 2025 hearing on the motion to dismiss, the magistrate judge covering the Motion issued a report recommending that all of the plaintiffs’ claims be dismissed for lack of standing. The recommendation remains subject to review and disposition by the presiding judge. We intend to vigorously defend against these claims, but given the preliminary nature of these matters, cannot predict their outcome or estimate any range of reasonably possible loss at this time.
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001018963&type=8-K｜as_of：2026-11-02
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-08-06 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-08 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-06-03 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-06-03 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-19 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-04-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-19 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-02-03 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-12-08 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2025-11-18 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-06-08，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1018963/000119312526261769/d163250d8k.htm｜as_of：2026-06-08
<<<
Item 1.01
Entry into a Material Definitive Agreement
On June 8, 2026, ATI Inc. (the “Company”) completed its offering and sale of $450 million aggregate principal amount of the Company’s unsecured 5.875% Senior Notes due 2033 (the “Notes”). The offering and sale of the Notes (the “Offering”) were made pursuant to the Company’s shelf registration statement filed with the Securities and Exchange Commission.
The Notes were issued pursuant to the Indenture, dated as of September 14, 2021 (the “Indenture”), between the Company and Computershare Trust Company, N.A., as successor trustee to Wells Fargo Bank, National Association, as trustee (the “Trustee”), as supplemented by the Third Supplemental Indenture, dated as of June 8, 2026 (the “Supplemental Indenture”), between the Company and the Trustee.
The Notes will accrue interest at the rate of 5.875% per annum and will mature on June 15, 2033. The Notes will be payable in cash semi-annually in arrears on each June 15 and December 15, commencing December 15, 2026.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-06-03，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1018963/000119312526255755/d74245d8k.htm｜as_of：2026-06-03
<<<
Item 8.01
Other Events.
On June 3, 2026, ATI Inc. (the “Company”) announced the pricing of its offering of unsecured 5.875% Senior Notes due 2033 (the “Notes”). The Company’s press release announcing the pricing of its offering of the Notes is set forth in its entirety and filed as Exhibit 99.1 to this Current Report on Form 8-K and is incorporated herein by reference.
Item 9.01
Financial Statements and Exhibits.
(d) Exhibits
Exhibit 99.1
Press Release dated June 3, 2026.
Exhibit 104
Cover Page Interactive Data File (embedded within the Inline XBRL document).
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-06-03，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1018963/000119312526254681/d100672d8k.htm｜as_of：2026-06-03
<<<
Item 8.01
Other Events
On June 3, 2026, ATI Inc. (the “Company”) issued a press release announcing its intention to offer a series of seven-year senior notes in an underwritten public offering. The Company’s press release announcing this intention is filed herewith as Exhibit 99.1 and is incorporated herein by reference.
Item 9.01
Financial Statements and Exhibits
(d) Exhibits
Exhibit 99.1
Press Release dated June 3, 2026.
Exhibit 104
Cover Page Interactive Data File (embedded within the Inline XBRL document).
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
