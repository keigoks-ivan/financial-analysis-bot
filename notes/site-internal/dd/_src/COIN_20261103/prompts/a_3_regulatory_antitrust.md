你是 stock-analyst v20 DD 的證據採集子 agent。標的：COIN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - COIN Coinbase Global antitrust OR monopoly investigation 2026
  - Coinbase Global regulation OR regulatory scrutiny Financial Data & Stock Exchanges 2026
  - COIN Coinbase Global DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm｜as_of：2026-02-12
<<<
ITEM 3. LEGAL PROCEEDINGS
For a description of material legal proceedings in which we are involved, see Note 21. Commitments and Contingencies of the Notes to our Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K, which is incorporated herein by reference.
We are not presently a party to any other legal or regulatory proceedings that in the opinion of our management, if determined adversely to us, would individually or taken together have a material adverse effect on our business, operating results, financial condition, or cash flows. However, we are subject to regulatory oversight by numerous state, federal, and foreign regulators and we are and we may become subject to various legal proceedings, inquiries, investigations, and demand letters that arise in the course of our business. For example, we have received investigative subpoenas and other inquiries from various state agencies and attorneys general for documents and information pertaining to our business practices and policies, customer complaints, asset launches, certain ongoing litigation, and certain transfers of crypto assets. In addition, we have received investigative subpoenas and demand letters from various regulators for documents and information, including about certain customer programs, operations, and existing and intended future products, including our processes for listing assets, the classification of certain listed assets, our staking programs, and our stablecoin and yield-generating products. We intend to cooperate fully with such investigations. These examples are not exhaustive.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm｜as_of：2026-02-12
<<<
Consumer protection The Federal Trade Commission (“FTC”), the Consumer Financial Protection Bureau (“CFPB”), and other U.S. federal, state, and local and foreign regulatory agencies regulate financial products, including money transfer services related to remittance or peer-to-peer transfers. These agencies, as well as certain other governmental bodies, including state attorneys general, have broad consumer protection mandates and discretion in enforcing consumer protection laws, including matters related to unfair or deceptive, and, in the case of the CFPB, abusive acts or practices (“UDAAPs”), and they promulgate, interpret, and enforce rules and regulations that affect our business. The CFPB has enforcement authority to prevent an entity that offers or provides consumer financial services or products in the United States from committing or engaging in UDAAPs or violating other federal consumer financial laws, including the ability to engage in joint investigations with other agencies, issue subpoenas and civil investigative demands, conduct hearings and adjudication proceedings, commence a civil action, grant relief (e.g., limit activities or functions; rescission of contracts), and refer matters for criminal proceedings. Market disruptions have led to certain attempts by consumer protection focused agencies, including the CFPB, to directly regulate the crypto industry.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm｜as_of：2026-02-12
<<<
From time to time we have been, and may in the future be, subject to claims and disputes with our customers with respect to our products and services, such as regarding the execution and settlement of crypto asset trades, fraudulent or unauthorized transactions, account takeovers, deposits and withdrawals of crypto assets, failures or malfunctions of our systems and services, or other issues relating to our products and services. For example, during periods of heavy Trading Volumes, we have received increased customer complaints. Additionally, the ingenuity of criminal fraudsters, combined with many consumer users’ susceptibility to fraud, may cause our customers to be subject to ongoing account takeovers and identity fraud issues. While we have taken measures to detect and reduce the risk of fraud, there is no guarantee that they will be successful and, in any case, require continuous improvement and optimization for continually evolving forms of fraud to be effective. There can be no guarantee that we will be successful in detecting and resolving these disputes or defending ourselves in any of these matters, and any failure may result in impaired relationships with our customers, damage to our brand and reputation, and substantial fines and damages.…

Moreover, while fiat currencies can be used to facilitate illegal activities, crypto assets are relatively new and, in many jurisdictions, may be lightly regulated or largely unregulated. Many types of crypto assets have characteristics, such as the speed with which digital currency transactions can be conducted, the ability to conduct transactions without the involvement of regulated intermediaries, the ability to engage in transactions across multiple jurisdictions, the irreversible nature of certain crypto asset transactions, and encryption technology that anonymizes these transactions, that make crypto assets susceptible to use in illegal activity. U.S. federal regulatory authorities and law enforcement agencies, such as the Department of Justice, the Department of the Treasury, SEC, CFTC, FTC, FinCEN or the Internal Revenue Service (“IRS”), various state securities and financial regulators, such as the NYDFS, and similar foreign regulatory authorities, have taken and continue to take legal actions against persons and entities alleged to be engaged in fraudulent schemes or other illicit activity involving crypto assets. We also support crypto assets that incorporate privacy-enhancing features, and may from time to time support additional crypto assets with similar functionalities. These privacy-enhancing crypto assets obscure the identities of sender and receiver, and may prevent law enforcement officials from tracing the source of funds on the blockchain.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
