你是 stock-analyst v20 DD 的證據採集子 agent。標的：GLXY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - GLXY Galaxy Digital antitrust OR monopoly investigation 2026
  - Galaxy Digital regulation OR regulatory scrutiny Capital Markets 2026
  - GLXY Galaxy Digital DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
Item 3. Legal Proceedings
In the ordinary course of business, the Company and its subsidiaries and affiliates may be threatened with, named as defendants in, or made parties to pending and potential legal actions, including class actions, arbitrations and other disputes. The Company and its subsidiaries and affiliates are also subject to oversight by numerous regulatory and other governmental agencies and may receive inspection requests, investigative subpoenas and requests from regulators for documents and information, which could lead to enforcement investigations and actions.
The Company reviews any lawsuits, regulatory investigations, and other legal proceedings on an ongoing basis and provides disclosure and records loss contingencies in accordance with its accounting policies. Except as discussed below, the Company does not believe that the ultimate resolution of existing legal and regulatory outstanding matters will have a material effect upon our financial condition or liquidity. However, in light of the uncertainties inherent in these matters, it is possible that the ultimate resolution of one or more of these matters may have a material adverse effect on the Company’s results of operations for a particular period, and future changes in circumstances or additional information could result in additional accruals or resolution in excess of established accruals, which could adversely affect the Company’s results of operations, potentially materially.
LUNA matters: On March 27, 2025, Galaxy reached an agreement with the New York State Attorney General to resolve civil claims related to certain investments, trading, and public statements made in connection with the LUNA digital asset from late 2020 to 2022. As of December 31, 2025 and December 31, 2024, the Company had accrued a legal provision of $151 million and $182 million, respectively. The accrued amounts include the impact of discounting the estimated cash flows at a rate of approximately 4.3%. The undiscounted settlement was $200 million and payable between 2025 and 2028, with a payment of $40 million in each of 2025 and 2026, and a payment of $60 million in each of 2027 and 2028.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
AI and related industries are under increasing scrutiny from regulators due to their concerns about market concentration, anti-competitive practices, and the pace of partnerships and acquisitions involving generative AI startups. As the AI industry continues to grow, transactions and business conduct will likely continue to draw scrutiny from regulators. Therefore, our investments in developing and offering AI/HPC data centers may also result in new or enhanced governmental or regulatory scrutiny, litigation, confidentiality or security risks, ethical concerns or other complications that could adversely affect our business, reputation, results of operations or financial condition.

We or our subsidiaries and affiliates have been and could be the subject of any number of inquiries, investigations, lawsuits and proceedings by counterparties, clients, other third parties and regulatory and other governmental agencies in the United States and abroad, which could lead to increased expenses and harm to our reputation, business, financial condition and the market price of our Class A common stock. Responding to inquiries, investigations, lawsuits and proceedings, regardless of the ultimate outcome of the matter, is time-consuming and expensive and can divert the attention of senior management. Adverse outcomes with respect to allegations, lawsuits, regulatory inquiries, audits, or investigations may result in significant settlement costs or judgments, penalties and fines, or require us to modify our services or require us to stop serving certain customers or geographies, any of which could negatively impact our business. The outcome of such proceedings, and the related expenses, may be difficult to predict or estimate until late in the proceedings, which may last a number of years and be costly for us to maintain.

As digital assets have grown in both popularity and market size, the U.S. Congress and a number of U.S. federal and state agencies and self-regulatory organizations (including FinCEN, OFAC, SEC, CFTC, FINRA, NFA, the Consumer Financial Protection Bureau, the Department of Justice, the Department of Homeland Security, the Federal Bureau of Investigation, the IRS, the Office of the Comptroller of the Currency, the FDIC, the Federal Reserve and state financial institution and securities regulators) have been examining the operations of digital asset networks, digital asset users and the digital asset markets, with particular focus on the extent to which digital assets can be misused to launder the proceeds of illegal activities, evade sanctions, or fund criminal or terrorist enterprises, and generally the safety and soundness of digital asset trading platforms and other service providers that hold digital assets for users. Many of these regulatory bodies have issued consumer advisories regarding the risks posed by digital assets to investors. Ongoing and future regulatory actions with respect to digital assets generally or any digital asset that we hold or invest in may alter, perhaps to a materially adverse extent, the nature of an investment in us or our ability to continue to operate.

Law enforcement agencies have often relied on the transparency of blockchains to facilitate investigations. However, certain privacy-enhancing features have been, or are expected to be, introduced to a number of digital asset networks, and these features may provide law enforcement agencies with less visibility into transaction-level data. Europol, the European Union’s law enforcement agency, and the U.S. Department of Treasury have each noted the increased use of privacy-enhancing digital assets like Zcash and Monero in criminal activity on the internet. Other U.S. regulators and agencies, including OFAC, FinCEN and the DOJ have taken regulatory or enforcement actions to attempt to limit the ability of bad actors in blockchain transactions, up to and including criminal charges. Additional regulatory action with respect to privacy-enhancing digital assets is possible in the future.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
