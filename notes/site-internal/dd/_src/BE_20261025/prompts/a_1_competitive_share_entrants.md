你是 stock-analyst v20 DD 的證據採集子 agent。標的：BE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - BE market share gaining OR losing 2026
  - new entrant OR displace threat 2026
  - BE competitor design win 2026
  - vs peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
Energy Server Systems Competition We primarily compete against alternative sources of electricity generation which provide firm, always on power. In addition to power provided by centralized utility grids, and other utility and non-utility owned generation sources, we primarily compete against OEMs providing onsite firm resources which are: •Gas reciprocating engines. Reciprocating internal combustion engines that are powered by natural gas to generate electricity directly onsite, often for backup power, load balancing, or CHP applications. The Bloom Energy Server system has a higher efficiency, lower emissions, higher reliability, and better flexibility to adapt to load fluctuations.

We believe our Energy Server systems compete favorably against these products, with our systems capability to adapt to variable oscillating workloads. Furthermore, due to its relative ease in permitting and installation compared to the above mentioned products, the Energy Server can be deployed rapidly, giving us a competitive advantage when customers have an urgent need for power. The Energy Server system has a negligible impact on air quality, no noise pollution, minimal water 10 Table of Contents Index to Financial Statements usage and the ability to produce more megawatts for the same amount of fuel. The Energy Server system’s modular design provides superior reliability compared to these products as the system can be serviced with no downtime. Finally, the Energy Server system has a high efficiency that allows for a low operating cost and emissions profile.

As a publicly traded company in the U.S., we are subject to laws and regulations of the SEC as well as the rules of the New York Stock Exchange, on which our company is listed. As a global enterprise operating in multiple countries, we must abide by laws and regulations applicable to entities across many jurisdictions, including those governing antitrust and competition, cybersecurity, data privacy, artificial intelligence, anti-bribery and anti-competition.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-09）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm｜as_of：2026-02-09
<<<
We face significant competition. We compete for customers, financing partners and incentive dollars from other electric power providers. Our Bloom Energy Server systems compete with a broad range of companies and technologies, including traditional energy suppliers, such as public utilities, and other energy providers utilizing traditional co-generation systems, nuclear, hydro, coal or geothermal power, companies utilizing intermittent solar or wind power paired with storage, and other commercially available fuel cell companies. We also compete with traditional backup energy equipment such as diesel generators.

Many of our competitors, such as traditional utilities and other companies offering distributed generation products, have longer operating histories, customer incumbency advantages, access to and influence with local and state governments, and access to more capital resources than us. Despite advantages offered by our products, prospective customers may still select such competitors to fulfill their energy needs after weighing all of the foregoing and any other applicable considerations. Significant developments in alternative technologies, such as energy storage, wind, solar or hydro power generation, or improvements in the efficiency or cost of traditional energy sources, including coal, oil, natural gas used in combustion, or nuclear power, may materially and adversely affect our business and prospects in ways we cannot anticipate. We may also face new competitors with better technologies, products, or resources. If we fail to adapt to changing market conditions and to compete successfully with grid electricity or new competitors, our growth will be limited, which would adversely affect our business results.

U.S. tax equity investors typically derive a significant portion of their economic returns through tax benefits when they finance a product. Tax equity investors are generally entitled to substantially all of the project’s tax benefits, such as those provided by the ITC and Modified Accelerated Cost Recovery System (“MACRS”) or bonus depreciation. The number of and available capital from potential tax equity investors is limited, we compete with other energy companies eligible for these tax benefits to access such investors, and the availability of capital from Equity Investors is subject to fluctuations based on factors outside of our control such as macroeconomic trends and changes in applicable taxation regimes. Concerns regarding our limited operating history at a large scale, historical lack of profitability and that we are the only party who can manufacture our products have made it difficult to attract tax equity investors in the past. Our ability to obtain additional financing depends on the continued confidence of banks and other financing sources in our business model, the market for our solutions, and the continued availability of tax benefits applicable to our solutions, regardless of whether we arrange the financing, or our customers finance the products themselves.…

Policing unauthorized use of proprietary technology can be difficult and expensive, and the measures we have taken to protect our intellectual property rights, including our trade secrets, may not be sufficient to prevent such use. For example, many of our engineers reside in California where it is not legally permissible to prevent them from leaving employment with us 36 Table of Contents Index to Financial Statements and working for a competitor. Similarly, the FTC has been active with regard to non-compete provisions which may impact our ability to prevent our employees from leaving employment with us and working for a competitor. Also, litigation may be necessary to enforce our intellectual property rights, including protecting our trade secrets, or to determine the validity and scope of the proprietary rights of others. Such litigation may result in our intellectual property rights being challenged, limited in scope, or declared invalid or unenforceable. We cannot be certain that the outcome of any litigation will be in our favor, and adverse determination in any such litigation could impair our intellectual property rights, business, prospects, brand, and reputation.

We rely primarily on patents, trade secrets, copyrights, and trademarks, and non-disclosure, confidentiality, and other types of contractual restrictions to establish, maintain, and enforce our intellectual property and proprietary rights. However, our rights under these intellectual property laws and agreements afford us only limited protection and the actions we take to establish, maintain, and enforce our intellectual property rights may not be adequate. For example, our trade secrets and other confidential information could be discovered by or disclosed in an unauthorized manner to third parties. Additionally, intellectual property rights owned or licensed to us could be challenged, invalidated, or declared unenforceable in judicial or administrative proceedings, or circumvented, designed around by our competitors, infringed, or misappropriated. Competitors could copy or reverse engineer our products or develop and market products that are substantially equivalent to or superior to our own. Any of these possibilities, including the unauthorized use of our intellectual property by others, could reduce our competitive advantage and have a material adverse effect on our business, financial condition, or operating results. In addition, the laws of some countries do not protect intellectual property rights as fully as do the laws of the U.S. Many U.S.-based companies have encountered substantial intellectual property infringement in foreign countries, including countries where we sell products.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
