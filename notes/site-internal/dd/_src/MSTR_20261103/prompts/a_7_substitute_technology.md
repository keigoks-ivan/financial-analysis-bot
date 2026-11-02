你是 stock-analyst v20 DD 的證據採集子 agent。標的：MSTR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Strategy product substitute technology threat 2026
  - Software - Application alternative technology disruption 2026 2027
  - MSTR Strategy technology obsolescence risk
  - Software - Application next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm｜as_of：2026-02-19
<<<
•Bitcoin holdings are subject to risks inherent in digital systems and electronic data, including cyberattacks, power failures, data corruption, software vulnerabilities, communication disruptions, and human error. These risks may make bitcoin more susceptible to theft, destruction, or loss of value than traditional fiat currencies or conventional financial assets.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1050446/000105044626000020/mstr-20251231.htm｜as_of：2026-02-19
<<<
Negative perception, a lack of stability in the broader bitcoin markets and the closure, temporary shutdown or operational disruption of bitcoin trading venues, lending institutions, institutional investors, institutional miners, custodians, or other 29 major participants in the bitcoin ecosystem, due to fraud, business failure, cybersecurity events, government-mandated regulation, bankruptcy, or for any other reason, may result in a decline in confidence in bitcoin and the broader bitcoin ecosystem and greater volatility in the price of bitcoin. For example, in 2022, each of Celsius Network, Voyager Digital, Three Arrows Capital, FTX, and BlockFi filed for bankruptcy, following which the market prices of bitcoin and other digital assets significantly declined. In addition, in June 2023, the SEC announced enforcement actions against Coinbase, Inc., and Binance Holdings Ltd., two providers of large trading venues for digital assets, which similarly was followed by a decrease in the market price of bitcoin and other digital assets. These were followed in November 2023, by an SEC enforcement action against Payward Inc. and Payward Ventures Inc., together known as Kraken, another large trading venue for digital assets. Although these complaints were ultimately dismissed, the SEC or other regulatory agencies may initiate similar actions in the future.…

Attacks upon systems across a variety of industries, including industries related to bitcoin, are increasing in frequency, persistence, and sophistication, and, in many cases, are being conducted by sophisticated, well-funded and organized groups and individuals, including state actors. Emerging technologies, such as AI-driven cyberattacks and the potential for quantum computing, could introduce new vulnerabilities in our systems, potentially rendering traditional cryptographic techniques less effective and exposing us to more sophisticated forms of cyberattacks. The techniques used to obtain unauthorized, improper or illegal access to systems and information (including personal data and digital assets), disable or degrade services, or sabotage systems are constantly evolving, may be difficult to detect quickly, and often are not recognized or detected until after they have been launched against a target. Novel methods, such as those utilizing AI or quantum computing, may be even more difficult to detect and defend against. These attacks may occur on our systems or those of our third-party service providers or partners. We may experience breaches of our security measures due to human 31 error, malfeasance, insider threats, system errors or vulnerabilities or other irregularities.…

If a successful infringement claim is made against us and we fail to develop or license a substitute technology or brand name, as applicable, our business, results of operations, financial condition, or cash flows could be materially adversely affected.

If we or our third-party service providers experience a disruption due to a cybersecurity attack or security breach and unauthorized parties obtain access to our customers’, prospects’, vendors’, or channel partners’ data, our data, our networks or other systems, or the cloud environments we manage, our offerings may be perceived as not being secure, our reputation may be harmed, demand for our offerings may be reduced, our operations may be disrupted, we may incur significant legal and financial liabilities, and our business could be materially adversely affected As part of our business, we process, store, and transmit our customers’, prospects’, vendors’, and channel partners’ data as well as our own, including in our networks and other systems and the cloud environments we manage. Security breaches may occur due to technological error, computer viruses, or third-party action, including intentional misconduct by computer hackers or state actors, physical break-ins, industrial espionage, fraudulent inducement of employees, customers, or channel partners to disclose sensitive information such as usernames or passwords, and employee, customer, or channel partner error or malfeasance.…

Any security breach, ransomware attack, or successful denial of service attack could result in a loss of customer confidence in the security of our offerings and damage to our brand, reduce the demand for our offerings, disrupt our normal business operations, require us to spend material resources to investigate or correct the breach, require us to notify affected customers or individuals and/or applicable regulators and others, provide identity theft protection services to individuals, expose us to legal liabilities, including litigation, regulatory enforcement actions, and indemnity obligations, and materially adversely affect our revenues and operating results. Our software operates in conjunction with and is dependent on third-party products and components across a broad ecosystem. If there is a security vulnerability in one of these products or components, and if there is a security exploit targeting it, we could face increased costs, liability claims, customer dissatisfaction, reduced revenue, or harm to our reputation or competitive position. Our insurance policies may not be adequate to compensate us for the potential losses arising from any cybersecurity breach or incident. In addition, such insurance may not be available to us in the future on economically reasonable terms, or at all.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSTR_20261103/parts/axes_7.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
