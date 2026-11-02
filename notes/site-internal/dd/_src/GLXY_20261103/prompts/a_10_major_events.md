你是 stock-analyst v20 DD 的證據採集子 agent。標的：GLXY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
  - GLXY Galaxy Digital acquisition merger 2025 2026
  - GLXY Galaxy Digital class action lawsuit securities fraud
  - GLXY Galaxy Digital clinical trial FDA approval 2025 2026
  - GLXY Galaxy Digital product launch recall warning letter
  - GLXY Galaxy Digital SEC investigation restatement


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
Item 3. Legal Proceedings
In the ordinary course of business, the Company and its subsidiaries and affiliates may be threatened with, named as defendants in, or made parties to pending and potential legal actions, including class actions, arbitrations and other disputes. The Company and its subsidiaries and affiliates are also subject to oversight by numerous regulatory and other governmental agencies and may receive inspection requests, investigative subpoenas and requests from regulators for documents and information, which could lead to enforcement investigations and actions.
The Company reviews any lawsuits, regulatory investigations, and other legal proceedings on an ongoing basis and provides disclosure and records loss contingencies in accordance with its accounting policies. Except as discussed below, the Company does not believe that the ultimate resolution of existing legal and regulatory outstanding matters will have a material effect upon our financial condition or liquidity. However, in light of the uncertainties inherent in these matters, it is possible that the ultimate resolution of one or more of these matters may have a material adverse effect on the Company’s results of operations for a particular period, and future changes in circumstances or additional information could result in additional accruals or resolution in excess of established accruals, which could adversely affect the Company’s results of operations, potentially materially.
LUNA matters: On March 27, 2025, Galaxy reached an agreement with the New York State Attorney General to resolve civil claims related to certain investments, trading, and public statements made in connection with the LUNA digital asset from late 2020 to 2022. As of December 31, 2025 and December 31, 2024, the Company had accrued a legal provision of $151 million and $182 million, respectively. The accrued amounts include the impact of discounting the estimated cash flows at a rate of approximately 4.3%. The undiscounted settlement was $200 million and payable between 2025 and 2028, with a payment of $40 million in each of 2025 and 2026, and a payment of $60 million in each of 2027 and 2028.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
We or our subsidiaries and affiliates have been and could be the subject of any number of inquiries, investigations, lawsuits and proceedings by counterparties, clients, other third parties and regulatory and other governmental agencies in the United States and abroad, which could lead to increased expenses and harm to our reputation, business, financial condition and the market price of our Class A common stock. Responding to inquiries, investigations, lawsuits and proceedings, regardless of the ultimate outcome of the matter, is time-consuming and expensive and can divert the attention of senior management. Adverse outcomes with respect to allegations, lawsuits, regulatory inquiries, audits, or investigations may result in significant settlement costs or judgments, penalties and fines, or require us to modify our services or require us to stop serving certain customers or geographies, any of which could negatively impact our business. The outcome of such proceedings, and the related expenses, may be difficult to predict or estimate until late in the proceedings, which may last a number of years and be costly for us to maintain.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 3. Legal Proceedings（訴訟／重大事項段落）｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
Item 3. Legal Proceedings In the ordinary course of business, the Company and its subsidiaries and affiliates may be threatened with, named as defendants in, or made parties to pending and potential legal actions, including class actions, arbitrations and other disputes. The Company and its subsidiaries and affiliates are also subject to oversight by numerous regulatory and other governmental agencies and may receive inspection requests, investigative subpoenas and requests from regulators for documents and information, which could lead to enforcement investigations and actions.

In December 2022, a proposed class action was filed in the Ontario Superior Court of Justice against GDH Ltd., our Chief Executive Officer and our former Chief Financial Officer asserting various claims including alleged misrepresentations relating to our public disclosure regarding investments and trading in the LUNA digital asset. The class action purports to be brought on behalf of a proposed class of persons and entities who acquired our securities on the secondary market from May 17, 2021 to and including May 6, 2022. The class action seeks unspecified damages and various declaratory relief, including leave to proceed with the right of action for misrepresentation under statutory securities provisions. These proceedings are still in early stages and have not been certified to proceed as a class action. The plaintiff’s motion for leave and certification is scheduled to be heard in June 2026. Based on the stage of the case, the outcome remains uncertain, and the Company cannot estimate the potential impact, if any, on its business or financial statements at this time.
>>>

[4] 來源：SEC EDGAR｜文件：8-K 申報清單（近12個月）｜章節：8-K 清單｜url：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001859392&type=8-K｜as_of：2026-11-03
<<<
【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 15 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。
2026-10-27 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-09-23 8-K Items 5.02 Departure/Election of Directors or Officers
2026-08-05 8-K Items 5.02 Departure/Election of Directors or Officers
2026-08-05 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-28 8-K Items 1.01 Entry into a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits
2026-07-24 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2026-07-22 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-07-13 8-K Items 5.02 Departure/Election of Directors or Officers
2026-05-28 8-K Items 5.07 Submission of Matters to a Vote of Security Holders
2026-05-08 8-K Items 1.01 Entry into a Material Definitive Agreement；9.01 Financial Statements and Exhibits
2026-04-28 8-K Items 2.02 Results of Operations and Financial Condition；7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2026-02-03 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
2026-01-15 8-K Items 8.01 Other Events；9.01 Financial Statements and Exhibits
2025-12-11 8-K Items 7.01 Regulation FD Disclosure；9.01 Financial Statements and Exhibits
2025-11-10 8-K Items 2.02 Results of Operations and Financial Condition；9.01 Financial Statements and Exhibits
>>>

[5] 來源：SEC EDGAR｜文件：8-K（2026-07-28，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000079/glxy-20260728.htm｜as_of：2026-07-28
<<<
Item 1.01 Entry into a Material Definitive Agreement.
Senior Secured Notes Offering
General
On July 28, 2026, Galaxy Helios Data Centers II LLC (“Issuer”), an indirect wholly owned subsidiary of Galaxy Digital Inc. (the “Company”), completed its previously announced private offering (the “Offering”) of 9.875% Senior Secured Notes due 2031(the “Notes”). The Notes were sold under a purchase agreement, dated as of July 23, 2026, entered into by and among the Issuer, Galaxy Helios II LLC, a wholly owned direct subsidiary of the Issuer (the “Guarantor”), and Morgan Stanley & Co. LLC as the representative of the several initial purchasers, for resale to persons reasonably believed to be qualified institutional buyers in reliance on Rule 144A under the Securities Act of 1933, as amended (the “Securities Act”), and outside the United States to non-U.S. persons in reliance on Regulation S under the Securities Act. The aggregate principal amount of Notes sold in the Offering was $3,507,000,000.
The Notes were issued at a price equal to 99.500% of their principal amount.…
>>>

[6] 來源：SEC EDGAR｜文件：8-K（2026-05-08，Item 1.01）｜章節：8-K Item 1.01 Entry into a Material Definitive Agreement｜url：https://www.sec.gov/Archives/edgar/data/1859392/000162828026032991/glxy-20260508.htm｜as_of：2026-05-08
<<<
Item 1.01 Entry into a Material Definitive Agreement.
On May 8, 2026, Galaxy Digital Inc. (the “Company”) entered into an Open Market Sale AgreementSM (the “Sales Agreement”) with Jefferies LLC, BNY Mellon Capital Markets, LLC and UBS Securities LLC (each, an “Agent” and together, the “Agents”), pursuant to which the Company may sell, from time to time, at its option, shares of the Company’s Class A common stock, $0.001 par value per share (the “Common Shares”), through the Agents, as sales agents (the “ATM Offering”). The issuance and sale, if any, of the Common Shares under the Sales Agreement will be made pursuant to the automatic shelf registration statement on Form S-3ASR (Registration No. 333-[ l ]) filed with the Securities and Exchange Commission (the “SEC”) on May 8, 2026, which became effective immediately upon filing, and the related prospectus supplement dated May 8, 2026 (the “ATM Prospectus Supplement”), pursuant to which the Company may sell up to an aggregate of $500,000,000 of Common Shares.…
>>>

[7] 來源：SEC EDGAR｜文件：8-K（2026-07-24，Item 8.01）｜章節：8-K Item 8.01 Other Events｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000074/glxy-20260723.htm｜as_of：2026-07-24
<<<
Item 8.01 Other Events.
On July 23, 2026, Galaxy Digital Inc. (the “Company”) issued a press release announcing that Galaxy Helios Data Centers II LLC (the “Issuer”), an indirect wholly owned subsidiary of the Company, priced its offering (the “Offering”) of $3.507 billion aggregate principal amount of 9.875% Senior Secured Notes due 2031 (the “Notes”). The Offering is expected to close on July 28, 2026, subject to market and customary closing conditions.
The Notes will only be offered and sold to persons reasonably believed to be qualified institutional buyers in reliance on Rule 144A under the Securities Act of 1933, as amended (the “Securities Act”), and outside the United States to non-U.S. persons in reliance on Regulation S under the Securities Act.
A copy of the press release announcing the pricing of the Offering is filed as Exhibit 99.1 to this Current Report on Form 8-K and is incorporated herein by reference.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
