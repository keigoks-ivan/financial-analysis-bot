你是 stock-analyst v20 DD 的證據採集子 agent。標的：MSI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - MSI Motorola Solutions acquisition merger 2025 2026
  - MSI Motorola Solutions class action lawsuit securities fraud
  - MSI Motorola Solutions clinical trial FDA approval 2025 2026
  - MSI Motorola Solutions product launch recall warning letter
  - MSI Motorola Solutions SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/68505/000006850526000010/msi-20251231.htm｜as_of：2026-02-12
<<<
Item 3: Legal Proceedings
In addition to the matter referenced below, we are subject to legal proceedings and claims that have not been fully resolved and which have arisen in the ordinary course of business. In the opinion of management, the ultimate disposition of these matters will not have a material adverse effect on our consolidated financial position, liquidity or results of operations. However, an unfavorable resolution could have a material adverse effect on our consolidated financial position, liquidity or results of operations in the periods in which the matters are ultimately resolved, or in the periods in which more information is obtained that changes management's opinion of the ultimate disposition.
Refer to the description of "Hytera Civil Litigation" in "Note 12: Commitments and Contingencies” to our consolidated financial statements included in "Part II. Item 8. Financial Statements and Supplementary Data" of this Form 10-K for information regarding our legal proceedings.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/68505/000006850526000010/msi-20251231.htm｜as_of：2026-02-12
<<<
Material Dispositions None. 11 Available Information We make available free of charge through the Investor Relations section of our website, www.motorolasolutions.com/investors, our annual reports on Form 10-K, quarterly reports on Form 10-Q, current reports on Form 8-K, proxy statements, other reports filed under the Securities Exchange Act of 1934, as amended (“Exchange Act”), and all other reports and amendments filed with, or furnished to, the SEC simultaneously or as soon as reasonably practicable after such material is electronically filed with, or furnished to, the SEC. Our reports are also available free of charge on the SEC’s website, www.sec.gov. Also available free of charge on our website, as provided above, are the following corporate governance documents: •Motorola Solutions, Inc. Restated Certificate of Incorporation •Motorola Solutions, Inc. Amended and Restated Bylaws •Board Governance Guidelines •Director Independence Guidelines •Principles of Conduct for Members of the Motorola Solutions, Inc. Board of Directors •Motorola Solutions Code of Business Conduct, which is applicable to all Motorola Solutions employees, including the principal executive officers, the principal financial officer and the controller (principal accounting officer)
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 7. MD&A（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/68505/000006850526000010/msi-20251231.htm｜as_of：2026-02-12
<<<
39 Other Charges Years ended December 31 (In millions) 2025 2024 Other charges from Products and Systems Integration $ 78 $ 25 Other charges from Software and Services 129 $ 130 Other charges $ 207 $ 155 Other charges increased $52 million, or 34% in 2025 compared to 2024 due to a $53 million, or 212% increase in Products and System Integration and a $1 million, or 1% decrease in Software and Services. The increase was primarily driven by: •$234 million of intangible asset amortization expense in 2025 compared to $152 million of intangible asset amortization expense in 2024, an increase primarily due to amortization of intangible assets from the acquisition of Silvus; •$66 million of acquisition-related transaction fees in 2025, primarily due to the acquisition of Silvus, compared to $20 million of acquisition-related transaction fees in 2024; •$44 million of reorganization of business expenses in 2025 compared to $26 million of reorganization of business expenses in 2024; and •$15 million of legal settlements in 2025 compared to $7 million of legal settlements in 2024; partially offset by •$157 million of gains on the Hytera litigation in 2025 compared to $61 million of gains in 2024 for the amounts recovered through legal proceedings due to theft of our trade secrets (see "Hytera Civil Litigation" within "Note 12: Commitments and Contingencies" to our consolidated financial statements…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000068505&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。
2026-11-04 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-09-09 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-17 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-20 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-07 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-03-12 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-11 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2025-11-18 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-09-09，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/68505/000119312526386490/d492220d8k.htm｜as_of：2026-09-09
<<<
Item 8.01.
Other Events.
On September 9, 2026, Motorola Solutions, Inc. (the “Company”) issued a press release announcing that its Board of Directors has authorized an increase in its share repurchase program to permit the Company to purchase up to an additional $2.0 billion of its outstanding common shares, bringing the total share repurchase program up to $20 billion, with no expiration date for the program. Through July 4, 2026, the Company repurchased approximately $17.4 billion shares of common stock under the existing share repurchase program. The Company may repurchase shares from time to time in the open market or in other privately negotiated transactions, subject to market conditions.
A copy of the press release is attached hereto as Exhibit 99.1 and incorporated herein by reference.
Item 9.01.
Financial Statements and Exhibits.
(d)
Exhibits
Exhibit No.
Description
99.1
Press Release by Motorola Solutions, Inc. dated September 9, 2026 announcing increase to share repurchase program.
104
Cover Page Interactive Data File (embedded within the Inline XBRL document).
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-08-17，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/68505/000119312526354035/d143399d8k.htm｜as_of：2026-08-17
<<<
Item 8.01.
Other Events.
On August 17, 2026, Motorola Solutions, Inc. (the “Company”) closed the underwritten public offering (the “Offering”) of $350,000,000 in aggregate principal amount of 4.850% senior notes due 2029 (the “2029 Notes”), and $600,000,000 in aggregate principal amount of 5.650% senior notes due 2036 (the “2036 Notes” and, together with the 2029 Notes, the “Notes”) pursuant to the Underwriting Agreement, dated August 6, 2026, by and among the Company and the several underwriters named therein (the “Underwriting Agreement”). The Notes were issued pursuant to an Indenture dated as of August 19, 2014 between the Company and The Bank of New York Mellon Trust Company, N.A., as trustee (the “Indenture”), as supplemented by an Officers’ Certificate, dated August 17, 2026 (the “Officers’ Certificate”). The Notes were offered and sold pursuant to a registration statement on Form S-3 (File No. 333-277316) under the Securities Act of 1933, as amended.
The Underwriting Agreement is filed as Exhibit 1.1, the Indenture is included as Exhibit 4.1, the Officers’ Certificate is filed as Exhibit 4.2, and specimen copies of the 2029 Notes and the 2036 Notes are filed as Exhibit 4.3 and Exhibit 4.4, respectively, to this current report on Form 8-K. Each of these exhibits is incorporated herein by reference.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
