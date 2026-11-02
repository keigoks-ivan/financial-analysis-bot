你是 stock-analyst v20 DD 的證據採集子 agent。標的：PWR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Quanta Services product substitute technology threat 2026
  - Engineering & Construction alternative technology disruption 2026 2027
  - PWR Quanta Services technology obsolescence risk
  - Engineering & Construction next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm｜as_of：2026-02-19
<<<
Business Environment With respect to our electric infrastructure service offerings, utility and other customers are continuing to invest significant capital in their infrastructure systems and programs. Our utility customers continue to face increased demand for electricity, including as a result of electrification trends and increased demand for data center and other technology infrastructure and advanced manufacturing facilities. To accommodate this growth, we expect continued demand for new or expanded transmission, substation and distribution infrastructure to reliably transport power to meet demand driven by electrification, data centers and manufacturing reshoring, as well as the modification and reengineering of existing infrastructure with increasing penetration of renewable generation and battery storage and the increased investment in new gas-powered generation. Furthermore, in order to reliably and efficiently deliver power and in preparation for emerging technologies, utility customers are also integrating smart grid technologies into distribution systems to improve grid management and create efficiencies, and a number of utility customers continue to implement system upgrades and hardening programs in response to recurring severe weather events, including, among other things, initiatives to underground critical infrastructure.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm｜as_of：2026-02-19
<<<
•Disruptions or failure to adequately protect our information technology systems could materially affect our business and reputation.

•The loss of, or our inability to attract or keep, key personnel could disrupt our business.

Changes in climate have caused, and are expected to continue to cause, among other things, changes to meteorological and hydrological patterns, as well as impacts to the frequency and intensity of wildfires, hurricanes, floods, droughts, extreme heat, other storms and severe weather-related events and natural disasters. These changes have and may in the future impact our future operating results and may have a long-term impact on our business, results of operation, financial condition and cash flows. While we seek to mitigate these risks, we recognize that certain risks are inherent given how and where we conduct our operations. For example, catastrophic natural disasters can negatively impact projects we are working on, our facilities and other physical locations, portions of our equipment, or the locations and service regions of our customers. Accordingly, a natural disaster has the potential to disrupt our and our customers’ businesses and may cause us to experience work stoppages, project delays, financial losses and additional costs to resume operations, including increased insurance costs or loss of coverage, legal liability and reputational losses, and we expect that increasing physical climate-related impacts may result in further changes to the cost or availability of insurance in the future.

Disruptions to our information technology systems or our failure to adequately protect critical data, sensitive information and technology systems could materially affect our business and reputation.

We rely on information technology systems to manage our operations and other business processes and to protect sensitive company information. We also collect and retain information about our customers, stockholders, vendors, employees, contractors, business partners and other parties, all of whom expect that we will adequately protect such information. We face numerous and evolving cybersecurity risks that threaten the confidentiality, integrity and availability of our information technology systems and confidential information as well as the systems and information of key third parties and information technology vendors upon whom we rely. Certain of our vendors have experienced cyber-attacks that exploited vulnerabilities in their systems and have resulted in disruptions to their systems. While these events have not resulted in any known material impacts to our systems, we expect such attacks will continue in the future. Furthermore, the infrastructure systems and facilities on which we work are strategic targets that are at greater risk of cyber-attacks or acts of terrorism than other targets. Additionally, an intrusion into the information systems of a business we acquire may also ultimately compromise our systems. Our operations are decentralized with operating companies maintaining some of their own information systems, data and service providers, including some of their own security controls and processes.…

We have experienced and addressed cyber-attacks, breaches and disruptions of our information systems, and systems of key third parties and information technology vendors that we rely upon, in the past, and we expect such events to continue to arise in the future. While to date we have not experienced any material impact as a result of these events, the ultimate impact of future and similar events remains unknown, and we expect additional vulnerabilities to arise. Cyber-attacks can result in compromises of our payment systems, monetary losses, inability to access or operate our systems (e.g., ransomware), delays in processing transactions or reporting financial results, the disclosure or misappropriation of confidential, personal or proprietary company information (including for the purpose of transacting in our stock), or the release of customer, stockholder, vendor or employee information. An attack could also cause material service disruptions to our internal systems or to our operating companies’ systems, or in extreme circumstances, infiltration into, damage to or loss of control of our customers’ energy infrastructure systems.…

We cannot be sure that we will be able to successfully complete the integration process without substantial costs, delays, disruptions or other operational or financial problems. Failure to successfully integrate acquired businesses could adversely impact our business, financial condition, results of operations and cash flows.

The loss of, or our inability to attract or keep, key personnel could disrupt our business.

Most government contracts are awarded through a regulated competitive bidding process, which can often include more cumbersome compliance requirements and be more time consuming than the bidding process for non-governmental projects. This could require us to incur substantial costs, subject us to increased liability for our disclosures, and influence our business strategy in ways other than we might prefer. Additionally, involvement with government contracts could require a significant amount of costs to be incurred before any revenues are realized. We are also subject to numerous procurement rules and other public sector regulations when we contract with certain governmental agencies, any deemed violation of which could lead to fines or penalties or a loss of business. Government agencies routinely audit and investigate government contractors and may review a contractor’s performance under its contracts, cost structure and compliance with applicable laws, regulations and standards. If a government agency determines that costs were improperly allocated to specific contracts, such costs will not be reimbursed or a refund of previously reimbursed costs may be required. If a government agency alleges or proves improper activity, civil and criminal penalties could be imposed and serious reputational harm could result. Many government contracts must be appropriated each year, and without re-appropriation we would not realize all of the potential revenues from any awarded contracts.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
