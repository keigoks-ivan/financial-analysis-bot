你是 stock-analyst v20 DD 的證據採集子 agent。標的：MSTR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - MSTR Strategy acquisition merger 2025 2026
  - MSTR Strategy class action lawsuit securities fraud
  - MSTR Strategy clinical trial FDA approval 2025 2026
  - MSTR Strategy product launch recall warning letter
  - MSTR Strategy SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm｜as_of：2026-02-19
<<<
Item 3. Legal Proceedings
For information regarding material pending legal proceedings in which we are involved, see “Commitments and Contingencies – Shareholder Action” in Note 9 of the Notes to Consolidated Financial Statements contained in Part II, Item 8 of this Annual Report, which is incorporated herein by reference.
We are involved in various legal proceedings arising in the normal course of business. Although the outcomes of these legal proceedings are inherently difficult to predict, we do not expect the resolution of these legal proceedings to have a material adverse effect on our financial position, results of operations, or cash flows.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm｜as_of：2026-02-19
<<<
40 We are currently subject to a class action lawsuit and other proceedings and may be subject to additional proceedings in the future, which could distract our management, harm our reputation and result in substantial costs or judgments against us We are subject to a putative class action lawsuit (related to the certificate of amendment we filed on July 7, 2025 with the Secretary of State of Delaware to the STRK Stock certificate of designations) in which our board of directors are also defendants (the “Dodge Class Action”). See “Commitments and Contingencies – Shareholder Action” in Note 9 and Note 12, “Redeemable Preferred Stock”, of the Notes to Consolidated Financial Statements contained in Part II, Item 8 of this Annual Report for additional information. If the Dodge Class Action is concluded in a manner adverse to us and we ultimately incur substantial costs or damages not covered by our directors’ and officers’ liability insurance, such an outcome could have a material adverse effect on our financial condition and business.…

The choice of forum provision may limit a stockholder’s ability to bring a claim in a judicial forum that it finds favorable for disputes with us or our directors, officers or other employees, which may discourage such lawsuits against us and our directors, officers and other employees. Alternatively, if a court were to find the choice of forum provision contained in our amended and restated by-laws to be inapplicable or unenforceable in an action, we may incur additional costs associated with resolving such action in other jurisdictions.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：其他章節（財報附註等）（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm｜as_of：2026-02-19
<<<
Shareholder Action On July 21, 2025, David Dodge filed a purported class action lawsuit in the Court of Chancery of the State of Delaware against the Company and the Company’s Board alleging violations of the Delaware General Corporation Law (the “DGCL”), and asserting a claim against the Company’s Board for breach of fiduciary duty in connection with the purported DGCL violation. Plaintiff Dodge purports to assert claims on behalf of himself and similarly situated holders of the Company’s common stock alleging that pursuant to Section 242 of the DGCL (“Section 242”), the holders of the Company’s common stock were entitled to vote on the STRK Amendment (as defined in Note 12, Redeemable Preferred Stock) the Company filed on July 7, 2025 with the Secretary of State of the State of Delaware. Refer to Note 12, Redeemable Preferred Stock, for additional information on the STRK Amendment.…
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001050446&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 76 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 70 份。
2026-11-02 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-10-29 8-K Items 3.03 Material Modification to Rights of Security Holders；5.03 Amendments to Articles or Bylaws；5.07 Submission of Matters to a Vote of Security Holders；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-10-28 8-K Items 8.01 Other Events
2026-10-26 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-10-19 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-10-16 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-10-13 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-10-05 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-10-01 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-09-28 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-09-25 8-K Items 8.01 Other Events
2026-09-21 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-09-14 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-09-08 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-09-01 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-08-31 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-08-24 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-08-17 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-08-10 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-08-03 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-07-31 8-K/A Items 9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-27 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-07-20 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-07-13 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-07-06 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；8.01 Other Events
2026-06-29 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-06-22 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-06-15 8-K Items 3.03 Material Modification to Rights of Security Holders；5.03 Amendments to Articles or Bylaws；7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-06-15 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-06-10 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-06-08 8-K Items 8.01 Other Events
2026-06-08 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-06-01 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-05-26 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-18 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-05-15 8-K Items 8.01 Other Events
2026-05-11 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-05-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-04 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-05-01 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-04-27 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-04-20 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-04-13 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-04-06 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-04-01 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-03-30 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-03-23 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；5.03 Amendments to Articles or Bylaws；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-03-23 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events
2026-03-16 8-K Items 7.01 Regulation FD Disclosure；…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-03-23，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1050446/000119312526118810/d93392d8k.htm｜as_of：2026-03-23
<<<
Item 1.01.
Entry into a Material Definitive Agreement.
The information set forth in Item 8.01 of this Current Report on Form 8-K related to the Common Stock Sales Agreement Addendum, STRC Sales Agreement Addendum and STRK Sales Agreement Addendum is incorporated herein by reference.
Item 1.02.
Termination of a Material Definitive Agreement.
The information set forth in Item 8.01 of this Current Report on Form 8-K related to the termination of the prior offering of shares of STRK Preferred Stock under the Prior STRK Preferred Stock Prospectus is incorporated herein by reference.
Item 5.03.
Amendments to Articles of Incorporation or Bylaws.
On March 23, 2026, the Company filed a Certificate of Increase of STRC Preferred Stock (the “Certificate of Increase”) to certify the authorization to increase the number of authorized shares of its STRC Preferred Stock from 70,435,353 to 282,556,565 shares. A copy of the Certificate of Increase is attached as Exhibit 3.1 hereto and is incorporated herein by reference. The foregoing description of the Certificate of Increase does not purport to be complete and is qualified in its entirety by reference to such exhibit.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-11-07，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1050446/000119312525271105/d78313d8k.htm｜as_of：2025-11-07
<<<
Item 1.01
Entry into a Material Definitive Agreement.
On November 6, 2025, Strategy Inc (the “Company”) entered into an underwriting agreement (the “Underwriting Agreement”) with Barclays Bank PLC, Morgan Stanley & Co. International plc, Moelis & Company LLC, SG Americas Securities, LLC, TD Securities (USA) LLC, Canaccord Genuity LLC and StoneX Financial Inc. (the “Underwriters”), relating to the issuance and sale in an underwritten offering (the “Offering”) of 7,750,000 shares (the “Shares”) of the Company’s 10.00% Series A Perpetual Stream Preferred Stock, $0.001 par value per share (the “STRE Stock”), at a public offering price of €80.00 per share. The issuance and sale of the STRE Stock is scheduled to settle on November 13, 2025, subject to customary closing conditions. Certain terms of the STRE Stock are described in more detail in the Company’s press release announcing the pricing of the Offering, which is filed herewith as Exhibit 99.1 and incorporated herein by reference.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSTR_20261103/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
