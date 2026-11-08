你是 stock-analyst v20 DD 的證據採集子 agent。標的：NET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - NET Cloudflare acquisition merger 2025 2026
  - NET Cloudflare class action lawsuit securities fraud
  - NET Cloudflare clinical trial FDA approval 2025 2026
  - NET Cloudflare product launch recall warning letter
  - NET Cloudflare SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
Item 3. Legal Proceedings
From time to time we are subject to legal proceedings and claims arising in the ordinary course of business. We are not presently a party to any legal proceeding that we believe is likely to have a material impact on our business, results of operations, or financial condition.
Future litigation may be necessary, among other things, to defend ourselves or our customers by determining the scope, enforceability, and validity of third-party proprietary rights or to establish our proprietary rights. The results of any litigation cannot be predicted with certainty, particularly in the areas of unsettled and evolving law in which we operate, and an unfavorable resolution in any legal proceedings could materially affect our future business, results of operations, or financial condition. Regardless of the outcome, litigation can have an adverse impact on us because of defense and settlement costs, diversion of management resources, and other factors. For additional information, see "Risk Factors - Activities of our paying and free customers or the content of their websites and other Internet properties may violate applicable laws and/or our terms of service and could subject us to lawsuits, regulatory enforcement actions, and/or liability in various jurisdictions" and "We are currently, and may be in the future, party to intellectual property rights claims and other litigation matters that, if resolved adversely, could have a material impact on our business, results of operations, or financial condition" and Note 8 to the consolidated financial statements included in this Annual Report on Form 10-K.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
Through our network, we provide a wide variety of products that enable our customers and our customers' users to exchange information, conduct business, and engage in various online activities both domestically and internationally. Our customers and our customers' users may use our network and products in violation of applicable law or in violation of our terms of service or the customer’s own policies. The existing laws relating to the liability of providers of online products and services for activities of their users are highly unsettled and in flux both within the United States and internationally. We are currently, and in the future may be, subject to lawsuits and/or liability arising from the conduct of our customers and our customers' users. Additionally, the conduct of our customers and our customers' users may subject us to regulatory enforcement actions and/or liability. We are a defendant in lawsuits, both in the United States and abroad, seeking injunctive relief and/or damages against us based on content that is made available through our customers’ websites and other Internet properties.…

We own a large number of patents, copyrights, trademarks, domain names, and trade secrets and, from time to time, are subject to litigation based on allegations of infringement, misappropriation, or other violations of intellectual property or other rights. As we face increasing competition and gain an increasingly high profile, the possibility of intellectual property rights claims, commercial claims, and other assertions against us grows. In addition, a number of companies in our industry hold a large number of patents and also protect their copyright, trade secret, trademark, and other intellectual property rights, and companies in the networking and security industry frequently enter into litigation based on allegations of patent infringement or other violations of intellectual property rights. We have in the past been, are currently, and may from time to time in the future become, a party to litigation and disputes related to intellectual property, our business practices, and our products. For example, we are a defendant in lawsuits, both in the United States and abroad, seeking injunctive relief and/or damages against us based on claims of alleged patent infringement and claims of alleged copyright infringement through content on our customers’ websites.…

Delaware law and provisions in our amended and restated certificate of incorporation and amended and restated bylaws could make a merger, tender offer, or proxy contest difficult, thereby depressing the market price of our Class A common stock.
>>>

[3] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001477333&type=8-K｜as_of：2026-11-08
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。
2026-11-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-08-13 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；3.02 Unregistered Sales of Equity Securities；8.01 Other Events；9.01 Financial Statements and Exhibits
2026-08-06 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-01 8-K/A Items 5.02 Departure/Election of Directors or Officers；5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-06-30 8-K Items 5.02 Departure/Election of Directors or Officers；5.07 Submission of Matters to a Vote of Security Holders；9.01 Financial Statements and Exhibits
2026-05-07 8-K/A Items 2.02 Results of Operations and Financial Condition；2.05 Costs Associated with Exit or Disposal Activities；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-05-07 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-10 8-K Items 5.02 Departure/Election of Directors or Officers；9.01 Financial Statements and Exhibits
2026-02-10 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
>>>

[4] 來源：SEC EDGAR｜文件：8-K（2026-05-07，Item 2.05）｜章節：8-K Item 2.05 Costs Associated with Exit or Disposal Activities｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000035/cloud-20260507.htm｜as_of：2026-05-07
<<<
Item 2.05) in the EDGAR submission header of the Original Form 8-K. No other changes have been made to the Original Form 8-K, which is restated herein.
Item 2.02 Results of Operations and Financial Condition.
On May 7, 2026, Cloudflare, Inc. (the "Company") reported financial results for the fiscal quarter ended March 31, 2026. A copy of the press release is furnished as Exhibit 99.1 to this report and incorporated by reference.
The information contained in Items 2.02 and 7.01 of this report, including Exhibit 99.1 attached hereto, is furnished and shall not be deemed “filed” for purposes of Section 18 of the Securities Exchange Act of 1934, as amended, or subject to the liabilities of that section. The information shall not be deemed incorporated by reference into any other filing with the Securities and Exchange Commission made by the Company regardless of any general incorporation language in such filing, except as shall be expressly set forth by specific reference in such filing.
Item 2.05 Costs Associated with Exit or Disposal Activities.
On May 7, 2026, the Company announced a plan (the “Plan”) designed to further accelerate its evolution to an agentic AI-first operating model. As part of the Plan, the Company expects to reduce its current workforce by approximately 20%.…
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-08-13，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1477333/000095010326012340/dp251721_8k.htm｜as_of：2026-08-13
<<<
Item 1.01. Entry into a Material Definitive Agreement.
Convertible Notes and the Indenture
On August 13, 2026, Cloudflare, Inc. (the “Company”)
issued $2.50 billion aggregate principal amount of 0% Convertible Senior Notes due 2031 (the “Notes”) pursuant to an indenture,
dated August 13, 2026 (the “Indenture”), between the Company and U.S. Bank Trust Company, National Association, as trustee.
The Notes will not bear regular interest and the
principal amount of the Notes will not accrete. The Notes may bear special interest under specified circumstances relating to the Company’s
failure to comply with its reporting obligations under the Indenture or if the Notes are not freely tradable as required by the Indenture.
The Notes will mature on August 15, 2031, unless earlier redeemed, repurchased or converted in accordance with their terms.
The conversion rate for the Notes will initially
be 2.0123 shares of the Company’s Class A common stock, par value $0.001 per share (the “Class A Common Stock”), per
$1,000 principal amount of Notes, which is equivalent to an initial conversion price of approximately $496.94 per share of the Class A
Common Stock. The initial conversion price of the Notes represents a premium of approximately 60% to the last reported sale price of $310.59…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
