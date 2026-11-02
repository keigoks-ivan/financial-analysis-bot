你是 stock-analyst v20 DD 的證據採集子 agent。標的：LLY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - LLY Eli Lilly and market share gaining OR losing 2026
  - Eli Lilly and new entrant OR displace threat Drug Manufacturers - General 2026
  - LLY competitor design win 2026
  - Eli Lilly and vs Drug Manufacturers - General peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm｜as_of：2026-02-12
<<<
Competition Our products compete globally with many other pharmaceutical products in highly competitive markets.

We believe our long-term competitive success depends on discovering and developing or acquiring and further developing innovative, cost-effective products that provide improved outcomes for patients and deliver value to payers, and continuously improving the productivity of our operations in a highly competitive and global environment. We face intensifying competition worldwide, including from China and other markets that have significantly expanded and accelerated research and development capabilities. Companies in these markets are increasingly licensing products to multinational pharmaceutical companies, entering into strategic partnerships, and competing directly in major markets. Our ability to compete effectively depends on our capacity to innovate at the pace of global scientific advancement, to access innovation through strategic partnerships and licensing arrangements across geographies, and to efficiently bring differentiated products to market. There can be no assurance that our efforts will result in commercially successful products, and it is possible that our products or indications will be, or will become, uncompetitive from time to time. See also "—Competition—U.S. Private Sector Dynamics."

8 Generic Pharmaceuticals and Biosimilars Generic pharmaceuticals and biosimilars can pose major competitive challenges to our business. In most major jurisdictions, the regulatory approval process for pharmaceuticals (other than biological products (biologics)) exempts generics from costly and time-consuming clinical trials to demonstrate their safety and efficacy, allowing generic manufacturers to rely on the safety and efficacy of the innovator product. As a result, generic manufacturers generally invest far fewer resources in research and development than we do for our branded products and can price their products significantly lower than branded products. Accordingly, when a branded non-biologic pharmaceutical loses its market exclusivity, it normally faces intense price competition from generic forms of the product, which can result in the loss of a significant portion of the branded product's revenue in a very short period of time. Loss of market exclusivity for competitive products may also shift market conditions for other branded products in the same therapeutic class. Moreover, governments in some countries leverage generic entrants to drive price concessions through the utilization of volume-based procurement bidding and other measures.

The IRA has, and will continue to, meaningfully influence our business strategies and those of our competitors. In particular, the nine-year timeline to set prices for medicines approved under a New Drug Application reduces the attractiveness of investment in small molecule innovation. The IRA can cause changes to development approach and timing and investments at-risk. The full impact of the IRA on our business and the pharmaceutical industry, including the implications to us of a competitor's product being selected for price setting, remains uncertain.

Rebates are also negotiated in the private sector. We pay rebates to private payers that provide prescription drug benefits to seniors covered by Medicare and to private payers that provide prescription drug benefits to their customers. These rebates are affected by the introduction of competitive products and generics in the same class and ongoing competitive dynamics.

The outcome of our preliminary agreements with the U.S. government and broader U.S. policy efforts to align domestic pharmaceutical pricing with international benchmarks from countries with competing healthcare cost containment priorities is uncertain and could impact our pricing strategies, product demand or access, or competitive positioning across global markets, and may result in reduced revenue in certain markets.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm｜as_of：2026-02-12
<<<
25 We engage in various forms of business development activities to enhance or refine our product pipeline and development capabilities, including licensing arrangements, co-development agreements, co-promotion arrangements, distribution and promotion agreements, joint ventures, acquisitions, equity investments, and divestitures. There are substantial risks associated with identifying and competing for successful business development targets and consummating related transactions. Continued regulatory focus on business combinations in our industry, including by the Federal Trade Commission and competition authorities in Europe and other jurisdictions, and heightened competition for attractive targets has and could continue to delay, jeopardize, or increase the costs or risks of our business development activities. In addition, failures or difficulties in integrating or retaining new personnel or the operations of the businesses, products, or assets we acquire (including related technology, commercial operations, compliance programs, information security, manufacturing, distribution, and general business operations and procedures) may affect our ability to realize the potential benefits of business development transactions and may result in our incurrence of substantial asset impairment or restructuring charges. We also may fail to generate the expected revenue and pipeline enhancement from business development activities due to diligence that fails to identify risks or adequately anticipate their magnitude, unsuccessful clinical trials, issues related to the quality, integrity, or broad applicability of data, regulatory impediments, and manufacturing or commercialization challenges.…

We compete with a large number of multinational pharmaceutical companies, biotechnology companies, and generic pharmaceutical companies and face intensifying competition worldwide, including from China and other markets where research and development capabilities have expanded and accelerated significantly. In many cases, our products compete against the leading products of one or more of our competitors. To compete successfully in a highly competitive and increasingly fast-paced global environment, we must deliver innovative, cost-effective products through internal innovation or business development that meet important medical needs, provide improved outcomes and a positive consumer experience for patients, and deliver value to payers. Our product revenues and prospects are adversely affected by patient access issues, the introduction by competitors of branded products that are first to market, have better marketplace access, have greater brand recognition, or are perceived as superior by the marketplace, by price competition, by generic or biosimilar versions of our branded products, and by generic or biosimilar versions of other products in the same therapeutic class as our branded products. Our revenues are also adversely affected by treatment innovations, including new or superior modalities, that eliminate or minimize the need for treatment with our existing products, and our existing products could be subject to decreased sales volumes, realized price reductions, or both.…

Regulation of generic and biosimilar products varies around the world and such regulation is complex and subject to ongoing interpretation and implementation by regulatory agencies and courts. Particularly for biosimilars, health authority guidelines and legislative actions could continue to make it less burdensome for competitor products to enter the market and further incentivize uptake of biosimilars. Given the importance to us of marketed biologic products and those in our clinical-stage pipeline, such regulation could have a material adverse effect on our business. See Item 1, "Business—Competition" and "Business—Research and Development," for more details. Alternatively, actual or perceived failure of robust generic and biosimilar competition could propel governments to adopt additional policies and legislation that threaten our intellectual property, pricing of our products, or other aspects of our business.

In addition, we rely on our ability to attract and retain highly qualified and skilled scientific, technical, management, and other personnel in order to compete effectively. To capitalize on the rapid development of next-generation technologies and otherwise effectively compete, we must continue to enhance skill sets and develop our workforce, both in and outside the U.S. We face intense competition for qualified individuals from numerous multinational companies, academic and other research institutions, as well as employers near our manufacturing and other facilities, which has increased and may continue to increase our labor costs. Our failure to compete effectively for talent could negatively affect our ability to discover, develop, manufacture, and sell our medicines, resulting in material financial, legal, commercial, or reputational harm to our business.

Difficulties related to supply chain activities have resulted and may in the future result in delays and disruptions in the manufacturing, distribution, and sale of our products and/or product shortages, leading to lost revenue, increased costs, reduced market opportunities, and the possibility of additional market entrants. In select cases, supply constraints may also lead to pauses, discontinuations, or other product availability issues in one or more markets, which could have a material adverse effect on our consolidated results of operations, cash flows, and reputation. Challenges and disruptions may include (i) actual or perceived quality, oversight, or regulatory compliance problems; (ii) equipment, mechanical, data, or IT system vulnerabilities, such as system inadequacies, inadequate controls or procedures, operating failures, unauthorized access, service interruptions or failures, security breaches, malicious intrusions, theft, exfiltration, ransomware or other cyber-attacks from a variety of sources; (iii) labor deficiencies; (iv) inability to obtain single-source or other raw or intermediate materials; or (v) issues related to contractors and suppliers, including the failure, inability, or refusal of a supplier or contract manufacturer to supply contracted quantities in a timely or compliant manner or at all, increases in demand on a supplier with constrained capacity, contractual disputes with our suppliers and contract manufacturers, and vertical integration by competitors within our supply chain.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LLY_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
