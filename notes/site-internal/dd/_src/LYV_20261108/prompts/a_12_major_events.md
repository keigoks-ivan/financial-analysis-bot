你是 stock-analyst v20 DD 的證據採集子 agent。標的：LYV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - LYV Live Nation Entertainment acquisition merger 2025 2026
  - LYV Live Nation Entertainment class action lawsuit securities fraud
  - LYV Live Nation Entertainment clinical trial FDA approval 2025 2026
  - LYV Live Nation Entertainment product launch recall warning letter
  - LYV Live Nation Entertainment SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm｜as_of：2026-02-19
<<<
ITEM 3. LEGAL PROCEEDINGS
Information regarding our legal proceedings can be found in Part II—Financial Information—Item 8. Financial Statements and Supplementary Data—Note 7 – Commitments and Contingent Liabilities.
PART II—FINANCIAL INFORMATION
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm｜as_of：2026-02-19
<<<
For instance, on November 5, 2021, the Astroworld music festival was held in Houston, Texas. During the course of the festival, ten members of the audience sustained fatal injuries and others suffered non-fatal injuries. Following these events, hundreds of civil lawsuits were filed against Live Nation Entertainment, Inc. and related entities, asserting insufficient crowd control and other theories, seeking compensatory and punitive damages. All lawsuits relating to Astroworld have been resolved since early 2025. We incurred losses in excess of our insurance recovery in connection with those lawsuits.

Our results may be affected by the outcome of pending and future litigation. Unfavorable rulings in our legal proceedings may have a negative impact on us that may be greater or smaller depending on the nature of the rulings. In addition, we are currently, and from time to time in the future may be, subject to various other claims, investigations, legal and administrative cases and proceedings (whether civil or criminal) or lawsuits by governmental agencies or private parties, as further described in the immediately preceding risk factor. If the results of these investigations, proceedings or suits are unfavorable to us or if we are unable to successfully defend against third-party lawsuits, we may be required to pay monetary damages or may be subject to fines, penalties, injunctions or other censure that could have a material adverse effect on our business, financial condition and results of operations. Even if we adequately address the issues raised by an investigation or proceeding or successfully defend a third-party lawsuit or counterclaim, we may have to devote significant financial and management resources to address these issues, which could harm our business, financial condition and results of operations. Refer to Item 3—Legal Proceedings for further discussion.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 8. Financial Statements（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm｜as_of：2026-02-19
<<<
Federal Trade Commission Complaint In September 2025, the United States Federal Trade Commission (the “FTC”), joined by the attorneys general of seven states, filed a lawsuit against Live Nation Entertainment, Inc. and Ticketmaster L.L.C. in the Central District of California. The plaintiffs allege that Live Nation and Ticketmaster advertised ticket prices to consumers that were deceptively lower than prices displayed at checkout, deceived consumers about the enforcement of advertised event ticket purchase limits and facilitated the sale of tickets unlawfully acquired by ticket brokers. The plaintiffs also allege that the Company violated the Better Online Ticket Sales Act and Section 5 of the FTC Act, as well as various state consumer protection statutes. The plaintiffs seek injunctive relief, statutory penalties and restitution for consumers. The Company filed a motion to dismiss the complaint in January 2026.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001335258&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。
2026-11-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-10-16 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-10-09 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-02 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-09-25 8-K Items 5.02 Departure/Election of Directors or Officers；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-06-12 8-K Items 5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-08 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-05-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-02-19 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-10-16，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1335258/000133525826000048/lyv-20261015.htm｜as_of：2026-10-16
<<<
Item 1.01 Entry into a Material Definitive Agreement.
Senior Notes Offering
On October 15, 2026, Live Nation Entertainment, Inc. (the “Company”) closed its previously announced private offering of $730.0 million in aggregate principal amount of 7.125% senior notes due 2032 (the “U.S. Dollar Notes”) and €600.0 million in aggregate principal amount of 6.125% senior notes due 2032 (the “Euro Notes” and, together with the U.S. Dollar Notes, the “Notes”), and in connection therewith, the Company, certain of the Company’s subsidiaries, as guarantors, U.S. Bank Trust Company, National Association, as trustee, U.S. Bank Europe DAC, as registrar and transfer agent for the Euro Notes, and U.S. Bank Europe DAC, UK Branch, as paying agent for the Euro Notes, entered into an indenture (the “Notes Indenture”) governing the Notes on the same date.
The Company intends to use the net proceeds from the offering to fund the redemption in full of all of the Company’s outstanding 6.500% Senior Secured Notes due 2027, to pay fees and expenses related to the offering, and for general corporate purposes, which may include the repayment or repurchase of certain of the Company’s indebtedness.
Pursuant to the Notes Indenture, the U.S.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-08，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1335258/000133525826000023/lyv-20260508.htm｜as_of：2026-05-08
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On May 8, 2026, Live Nation VenueCo, LLC (“VenueCo”), a bankruptcy-remote, special purpose vehicle owned by certain bankruptcy-remote, special purpose entities (the “Participants”), which are indirect subsidiaries of Live Nation Entertainment, Inc. (the “Company”), closed its previously announced issuance of €610 million aggregate principal amount of fixed rate senior secured notes (the “Notes”).
The Notes were issued pursuant to (1) a Note Purchase Agreement (the “Note Purchase Agreement”) dated April 30, 2026 providing for the issuance of the Notes by VenueCo on behalf of and as representative for issuers located in other jurisdictions (together with VenueCo, the “Members”) and (2) a Master Trust Indenture (the “Master Indenture”) dated April 30, 2026, and a First Supplemental Indenture (the “First Supplemental Indenture”), dated May 8, 2026, in each case with respect to such indenture and supplement, among VenueCo and the other Members, Mount Street Mortgage Servicing Limited as Master Trustee (the “Trustee”) and Master Servicer, HSBC Bank USA, N.A. (“HSBC”) as Depositary and the other parties thereto.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-10-09，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1335258/000133525826000046/lyv-20261007.htm｜as_of：2026-10-09
<<<
Item 8.01 Other Events.
On October 7, 2026, Live Nation Entertainment, Inc. (the “Company”) issued a press release announcing that it had priced a private offering of $730,000,000 aggregate principal amount of new senior notes due 2032 (the “U.S. Dollar Notes”) and €600,000,000 aggregate principal amount of new senior notes due 2032 (the “Euro Notes” and, together with the U.S. Dollar Notes, the “Notes”).
The U.S. Dollar Notes will have an interest rate of 7.125% per annum and will be issued at a price equal to 100.000% of their face value. The Euro Notes will have an interest rate of 6.125% per annum and will be issued at a price equal to 100.000% of their face value.
The closing date of the Notes offering will be October 15, 2026, subject to customary closing conditions. Obligations under the Notes will be guaranteed by the Company and the Company’s existing and future domestic restricted subsidiaries that guarantee the Company’s senior secured credit facilities. The Company intends to use the net proceeds from the offering to fund the redemption in full of all of the Company’s outstanding 6.500% Senior Secured Notes due 2027, to pay fees and expenses related to the offering, and for general corporate purposes, which may include the repayment or repurchase of certain of the Company’s indebtedness.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
