你是 stock-analyst v20 DD 的證據採集子 agent。標的：H。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - H Hyatt Hotels acquisition merger 2025 2026
  - H Hyatt Hotels class action lawsuit securities fraud
  - H Hyatt Hotels clinical trial FDA approval 2025 2026
  - H Hyatt Hotels product launch recall warning letter
  - H Hyatt Hotels SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm｜as_of：2026-02-13
<<<
Item 3. Legal Proceedings.
We are involved in various claims and lawsuits arising in the normal course of business, including proceedings involving tort and other general liability claims, workers' compensation and other employee claims, intellectual property claims, and claims related to our management of certain hotel properties. Most occurrences involving liability, claims of negligence, and employees are covered by insurance, in each case, with solvent insurance carriers. We record a liability when we believe the loss is probable and reasonably estimable. We currently believe that the ultimate outcome of such lawsuits and proceedings will not, individually or in the aggregate, have a material effect on our consolidated financial position, results of operations, or liquidity.
See Part IV, Item 15, "Exhibits and Financial Statement Schedule—Note 14 and Note 15 to our Consolidated Financial Statements" for additional information related to tax and legal contingencies, respectively.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm｜as_of：2026-02-13
<<<
Disputes that relate to the subject matter of the Amended and Restated Global Hyatt Agreement are subject to arbitration pursuant to the terms of the agreement. The exclusive requirement to arbitrate under the Amended and Restated Global Hyatt Agreement shall not apply with respect to the manner in which Hyatt's operations are conducted to the extent the parties (in their capacities as stockholders) and non-Pritzker public stockholders are affected comparably; provided, however, that a party 21 Table of Contents may participate in and benefit from any shareholder litigation initiated by a non-party to the agreement. A party to the agreement may not solicit others to initiate or be a named plaintiff in such litigation (i) unless two thirds of the independent directors (excluding for such purposes any Pritzker) of a board of directors having at least three independent directors (excluding for such purposes any Pritzker) do not vote in favor of the matter that is the subject of the litigation or (ii) in the case of affiliated transactions reviewed by our board of directors, unless at least one independent director (excluding for such purposes any Pritzker) did not approve the transaction.

Disputes that relate to the subject matter of the Amended and Restated Foreign Global Hyatt Agreement are subject to arbitration pursuant to the terms of the agreement. The exclusive requirement to arbitrate under the Amended and Restated Foreign Global Hyatt Agreement shall not apply with respect to the manner in which Hyatt's operations are conducted to the extent the parties (in their capacities as stockholders) and non-Pritzker public stockholders are affected comparably; provided, however, that a party may participate in and benefit from any shareholder litigation initiated by a non-party to the agreement. A party to the agreement may not solicit others to initiate or be a named plaintiff in such litigation (i) unless two thirds of the independent directors (excluding for such purposes any Pritzker) of a board of directors having at least three independent directors (excluding for such purposes any Pritzker) do not vote in favor of the matter that is the subject of the litigation or (ii)
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm｜as_of：2026-02-13
<<<
We generally seek to resolve any disagreements with our third-party owners or franchisees amicably. Formal dispute resolution occurs through arbitration, if provided under the applicable management and hotel services agreement or franchise agreement, or through litigation. We cannot predict the outcome of any such arbitration or litigation, the effect of any adverse judgment of a court or arbitrator against us, or the amount of any settlement we may enter into with any third party.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001468174&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。
2026-10-29 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-07-30 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-05-28 8-K Items 7.01 Regulation FD Disclosure；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-05-22 8-K Items 5.02 Departure/Election of Directors or Officers；5.07 Submission of Matters to a Vote of Security Holders
2026-04-30 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-03-27 8-K Items 5.02 Departure/Election of Directors or Officers
2026-02-17 8-K Items 5.02 Departure/Election of Directors or Officers；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-12 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-12-30 8-K Items 2.01 Completion of Acquisition or Disposition of Assets；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-26 8-K Items 1.01 Entry into a Material Definitive Agreement；8.01 Other Events；9.01 Financial Statements and Exhibits
2025-11-17 8-K Items 9.01 Financial Statements and Exhibits
2025-11-07 8-K Items 7.01 Regulation FD Disclosure
2025-11-06 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2025-12-30，Item 2.01）｜章節：8-K Item 2.01 Completion of Acquisition or Disposition of Assets｜url：https://www.sec.gov/Archives/edgar/data/1468174/000110465925125229/tm2534420d1_8k.htm｜as_of：2025-12-30
<<<
Item 2.01. Completion of
Acquisition or Disposition of Assets.
As previously disclosed by Hyatt Hotels Corporation
(“Hyatt” or the “Company”), on June 29, 2025, HI Holdings Playa B.V., a private limited liability
company (besloten vennootschap met beperkte aansprakelijkheid) organized under the laws of the Netherlands and an indirect wholly
owned subsidiary of Hyatt (“HI Holdings”), and Hyatt Corporation entered into a Share Purchase Agreement (the “Share
Purchase Agreement”) with Turquoise Topco Limited (“Original Buyer”), a joint venture between an affiliate
of KSL Capital Partners, LLC and Rodina, which provides for the sale of Playa Resorts Holding B.V. which, following certain internal restructurings,
would indirectly hold all of the subsidiaries of Playa that own hotels and real property in exchange for an all-cash purchase price of
$2.0 billion, subject to customary adjustments (the “Asset Sale Transaction”). Original Buyer subsequently assigned
the Share Purchase Agreement and its rights thereunder to TRQ TORTUGA B.V., a Dutch private limited liability company (“Buyer”).
On December
30, 2025, the Asset Sale Transaction closed for an all-cash purchase price of $1,977.5 billion. Buyer financed the acquisition
with equity financing from an affiliate of KSL Capital Partners, LLC and Rodina, committed debt financing from third party sources, and
a $200 million preferred equity investment provided by Hyatt.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2025-11-26，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1468174/000110465925116442/tm2532262d1_8k.htm｜as_of：2025-11-26
<<<
Item 1.01. Entry into a Material Definitive Agreement.
Offering of the Notes
On November 26, 2025, Hyatt Hotels Corporation (the “Company”)
issued and sold $400,000,000 of its 5.400% Senior Notes due 2035 (the “Notes”) in a public offering (the “Offering”)
pursuant to an effective Registration Statement on Form S-3 (Registration No. 333-274272) (the “Registration Statement”).
The Company received net proceeds from the Offering of approximately $396.2 million, after deducting underwriters’ discounts and
estimated offering expenses payable by the Company.
The Company intends to use the net proceeds from the Offering to repay
all of the 4.850% notes due 2026 (the “2026 Notes”). The Company will use any remaining net proceeds for general corporate
purposes the Company may deem necessary or advisable, and to pay fees and expenses related to the Offering.
Indenture
The Notes were issued pursuant to an indenture, dated August 30,
2023 (the “Base Indenture”), between the Company and Computershare Trust Company, N.A., as trustee (the “Trustee”),
as supplemented by a fourth supplemental indenture, dated November 26, 2025 (the “Fourth Supplemental Indenture”
and, together with the Base Indenture, the “Indenture”), between the Company and the Trustee, setting forth the terms
of the Notes.
The Base Indenture was included as Exhibit 4.5 to the Company’s
Registration Statement on Form S-3 (No.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-05-28，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1468174/000110465926067209/tm2615108d1_8k.htm｜as_of：2026-05-28
<<<
Item 8.01. Other Events.
On May 28, 2026, the Company announced that its Board of Directors
has authorized the repurchase of up to an additional $1.0 billion of the Company’s common stock. These repurchases may be made
from time to time in the open market, in privately negotiated transactions, or otherwise, including pursuant to a Rule 10b5-1 plan or
an accelerated share repurchase transaction, at prices that the Company deems appropriate and subject to market conditions, applicable
law and other factors deemed relevant in the Company’s sole discretion. The common stock repurchase authorization applies to the
Company’s Class A common stock and/or the Company’s Class B common stock. The common stock repurchase authorization
does not obligate the Company to repurchase any dollar amount or number of shares of common stock and the authorization may be suspended
or discontinued at any time.
Item 9.01. Financial Statements and Exhibits.
(d) Exhibits.
Exhibit
No.
Document Description
99.1
Investor Day Slide Presentation, dated May 28, 2026 (furnished pursuant to Item 7.01)
99.2
Hyatt Hotels Corporation Press Release, dated May 28, 2026 (furnished pursuant to Item 7.01)
104
Cover Page Interactive Data File (embedded within the Inline XBRL document)
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
