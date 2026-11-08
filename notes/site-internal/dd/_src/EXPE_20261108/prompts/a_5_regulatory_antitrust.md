你是 stock-analyst v20 DD 的證據採集子 agent。標的：EXPE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - EXPE Expedia Group antitrust OR monopoly investigation 2026
  - Expedia Group regulation OR regulatory scrutiny Travel Services 2026
  - EXPE Expedia Group DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1324424/000132442426000008/expe-20251231.htm｜as_of：2026-02-13
<<<
Part I. Item 3. Legal Proceedings
In the ordinary course of business, Expedia Group and its subsidiaries are parties to legal proceedings and claims involving property, personal injury, contract, alleged infringement of third-party intellectual property rights and other statutory and common law claims. The amounts that may be recovered in such matters may be subject to insurance coverage.
Rules of the SEC require the description of material pending legal proceedings, other than ordinary, routine litigation incident to the registrant’s business, and advise that proceedings ordinarily need not be described if they primarily involve damages claims for amounts (exclusive of interest and costs) not individually exceeding 10% of the current assets of the registrant and its subsidiaries on a consolidated basis. In the judgment of management, none of the pending litigation matters that the Company and its subsidiaries are defending, including those described below, involves or is likely to involve amounts of that magnitude. The litigation matters described below involve issues or claims that may be of particular interest to our stockholders, regardless of whether any of these matters may be material to our financial position or results of operations based upon the standard set forth in the SEC’s rules.
Litigation Relating to Occupancy and Other Taxes
A number of jurisdictions in the United States have filed lawsuits against online travel companies, including Expedia Group companies such as Hotels.com, Expedia, Hotwire, Orbitz and HomeAway, claiming that such travel companies have failed to collect and/or pay taxes (e.g., occupancy taxes, business privilege taxes, excise taxes, sales taxes, etc.), as well as related claims such as unjust enrichment, restitution, conversion and violation of consumer protection statutes, and seeking monetary (including tax, interest, and penalties), injunctive and/or declaratory relief. In addition, we may file complaints contesting tax assessments made by states, counties and municipalities seeking to obligate online travel companies, including certain Expedia Group companies, to collect and remit certain taxes, either retroactively or prospectively, or both. Moreover, certain jurisdictions may require us to pay tax assessments prior to contesting any such assessments.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1324424/000132442426000008/expe-20251231.htm｜as_of：2026-02-13
<<<
12 Table of Contents Our international operations are also subject to a number of other risks, including: • exposure to local economic or political instability and threatened or actual acts of terrorism; • compliance with U.S. and non-U.S. regulatory laws and requirements relating to anti-corruption, antitrust or competition, economic sanctions, data content and privacy, consumer protection, employment and labor laws, health and safety, information reporting and advertising and promotions; • weaker enforcement of our contractual and intellectual property rights; • lower levels of credit card usage and increased payment and fraud risk; • longer payment cycles, and difficulties in collecting accounts receivable; • preferences by local populations for local providers; • restrictions on, or adverse tax and other consequences related to the repatriation of cash, the withdrawal of non-U.S. investments, cash balances and earnings, as well as restrictions on our ability to invest in our operations in certain countries; • changes to trade policy or agreements that limit our ability to offer, or adversely affect demand for, our products and services; • our ability to support technologies or marketing channels that may be prevalent in a particular international market and used by local competitors, but are not scalable for an international company offering services in many markets around the world; and • uncertainty regarding liability for services and content, including uncertainty as a result of local laws and lack of…

Our global operations are subject to complex and changing laws and regulations. Our business and financial performance could be adversely affected by changes in or interpretations of existing laws, rules and regulations or the promulgation of new laws, rules and regulations applicable to us and our businesses, including those relating to travel, tourism services, and alternative accommodation licensing and listing requirements, the provision of travel packages, the internet and online commerce, internet advertising and price display, consumer protection, licensing and regulations relating to the offer of travel insurance and related products, anti-corruption, anti-trust and competition (including our contractual provisions regarding pricing and travel suppliers), economic and trade sanctions, tax, banking, machine learning and AI, data security, the provision of payment services and privacy.

Likewise, the SEC, Department of Justice (“DOJ”) and Office of Foreign Assets Controls (“OFAC”), as well as foreign regulatory authorities, have continued to enforce economic sanctions and trade regulations, anti-money laundering, and anti-corruption laws.

We also have been subject, and we will likely be subject in the future, to inquiries or legal proceedings from time to time from regulatory bodies concerning compliance with economic sanctions, consumer protection, competition, tax, payments and travel industry-specific laws and regulations. For example, in 2020, the Australian Competition and Consumer Commission held that aspects of the way that our trivago subsidiary had offered accommodation on its Australian website breached Australian Consumer Law. Expedia Group companies have also historically been involved in a number of investigations by national competition authorities related to whether certain parity clauses in contracts between Expedia Group entities and accommodation providers are anti-competitive, as well as market studies, inquiries or investigations by regulatory authorities relating to the presentation of information on certain of our consumer-facing websites. We have worked collaboratively with such authorities and in some cases have offered voluntary undertakings or commitments in order to address the regulatory authorities' concerns. However, we are unable to predict what, if any, future actions by regulatory authorities will have on our business, industry practices or online commerce more generally.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EXPE_20261108/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
