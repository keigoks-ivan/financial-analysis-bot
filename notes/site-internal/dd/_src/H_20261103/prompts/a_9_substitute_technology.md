你是 stock-analyst v20 DD 的證據採集子 agent。標的：H。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Hyatt Hotels product substitute technology threat 2026
  - Lodging alternative technology disruption 2026 2027
  - H Hyatt Hotels technology obsolescence risk
  - Lodging next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm｜as_of：2026-02-13
<<<
•The success of our business depends on complex internal and third-party information technology, cloud, and AI systems, and any failures, security incidents, data issues, regulatory challenges, integration difficulties, or inability to effectively develop, govern, or access these technologies could disrupt operations, reduce revenues, and harm our reputation and competitiveness.

Operational Risks The risks of doing business internationally, or in a particular country or region, could lower our revenues, increase our costs, reduce our profits, or disrupt our business.

While these factors and the impact of these factors are difficult to predict, any one or more of them could lower our revenues, affect our operations, increase our costs, reduce our profits, or disrupt our business.

The continued expansion in the use and influence of social media has compounded the potential scope of negative publicity that could be generated, which may lead to litigation or governmental investigations or the damage of our reputation. Adverse incidents have occurred at our properties in the past and may occur in the future. Negative incidents could lead to tangible adverse effects on our business, including lost sales, boycotts, reduced enrollment and/or participation in the loyalty program, or paid membership program that we manage, disruption of access to our digital platforms, loss of development opportunities, or reduced colleague retention and increased recruiting difficulties. In addition, the increasing prevalence and adoption of generative AI tools and LLMs, including ChatGPT, Claude, Gemini, Grok, and others, means that information about Hyatt, our brands, and our properties can be accessed quickly and easily. The manner in which these AI tools decide what information to provide in response to a given user query may also result in our properties receiving less attention by users of these tools. In cases where the information provided is inaccurate, incomplete, misguided, or misleading, the reputation of Hyatt and our brands could be impacted based on the contents of information provided, and there is no guarantee that our efforts to correct such issues will be successful.…

The availability of capital or the conditions under which we or our third-party owners, franchisees, or development partners can obtain capital can have a significant impact on the overall level, cost, and pace of future development and therefore, the ability to grow our revenues. Credit markets have, and may continue, to experience significant disruption severely reducing liquidity and credit availability which has in the past, and could continue to, result in difficulties for certain third-party owners and franchisees to obtain commercially viable financing. Such disruptions may diminish the ability and desire of existing and potential development partners to access capital necessary to develop properties. Our ability to access additional capital could also be limited by the terms of our revolving credit facility, our outstanding notes, bonds, or other indebtedness we may incur, which restricts or may restrict our ability to incur debt under certain circumstances. Additionally, if one or more of the financial institutions that support our revolving credit facility fail, we may not be able to find a replacement, which would reduce the availability of funds that we can borrow under the facility.

The regulations and contractual obligations applicable to security and privacy are increasingly demanding, both in the United States and in other jurisdictions where we operate, and cyber threat actors regularly target the hospitality industry, including our business. In addition, the scope and complexity of the cyber threat landscape could affect our ability to adapt to and comply with changing regulatory obligations and expectations. Because of the scope and complexity of our information technology structure, our reliance on third-party hardware, software, and services to support and protect our structure and data, and the constantly evolving cyber threat landscape, our systems are vulnerable to cybersecurity risks that threaten the confidentiality, integrity, and availability of our information technology systems and confidential information, including from diverse threat actors and diverse attack vectors, including cyberterrorists, state actors, opportunistic hackers and hacktivists, malware (including ransomware), third-party disruptions, failures, or unauthorized access, as well as malfeasance by insiders, human or technological error, negligence, fraud, and as a result of bugs, misconfigurations, or exploited vulnerabilities in software or hardware. Moreover, our systems, colleagues, and customers have been, and we expect will continue to be, targeted by social engineering/phishing attacks or account takeover tactics that may, among other things, aim to obtain funds or information fraudulently.…

The success of our business depends on complex internal and third-party information technology, cloud, and AI systems, and any failures, security incidents, data issues, regulatory challenges, integration difficulties, or inability to effectively develop, govern, or access these technologies could disrupt operations, reduce revenues, and harm our reputation and competitiveness.

In addition to our proprietary AI technologies, we use AI technologies licensed from third parties in our technologies and our ability to continue to use such technologies at the scale we need may be dependent on access to specific third-party software and infrastructure. We cannot control the availability or pricing of such third-party AI technologies, especially in a highly competitive environment, and we may be unable to negotiate favorable economic terms with the applicable providers. If any such third-party AI technologies become incompatible with our solutions or unavailable for use, or if the providers of such models unfavorably change the terms on which their AI technologies are offered or terminate their relationship with us, our solutions may become less appealing to our customers and our business will be harmed. In addition, to the extent any third-party AI technologies are used as a hosted service, any disruption, outage, or loss of information through such hosted services could disrupt our operations or solutions, damage our reputation, cause a loss of confidence in our solutions, or result in legal claims or proceedings, for which we may be unable to recover damages from the affected provider.…

Negotiations of collective bargaining agreements, attempts by labor organizations to organize additional groups of our colleagues, or changes in labor laws could disrupt our operations, increase our labor costs, or interfere with the ability of our management to focus on executing our business strategies.

Certain of our properties are subject to collective bargaining agreements, similar agreements, or regulations enforced by governmental authorities. If relationships with our colleagues, other field personnel, or the unions that represent them become adverse, the properties we manage, own, or lease could experience labor disruptions such as strikes, lockouts, and public demonstrations. Labor disruptions, which are generally more likely when collective bargaining agreements are being 44 Table of Contents renegotiated, could harm our relationship with our colleagues or cause us to lose guests. Further, adverse publicity in the marketplace related to union messaging could further harm our reputation and reduce customer demand for our services. Labor regulation, including minimum wage legislation, could lead to higher wage and benefit costs, changes in work rules that raise operating expenses, legal costs, and limitations on our ability or the ability of our third-party owners and franchisees to take cost saving measures during economic downturns. Collective bargaining agreements may also limit our ability to make timely staffing or labor changes in response to declining revenues.

We and our third-party owners and franchisees may also become subject to additional collective bargaining agreements in the future. Potential changes in the federal regulatory scheme could make it easier for unions to organize groups of our colleagues. If such changes take effect, more of our colleagues or other field personnel could be subject to increased organizational efforts, which could potentially lead to disruptions or require more of our management's time to address unionization issues. These or similar agreements, legislation, or changes in regulations could disrupt our operations, hinder our ability to cross-train and cross-promote our colleagues due to prescribed work rules and job classifications, reduce our profitability, or interfere with the ability of our management to focus on executing our business strategies.

Our franchisees and their hotel operators also currently may be or may become subject to collective bargaining agreements. Labor disruptions, labor regulation, and negotiation of labor agreements may be disruptive to a franchisee's operations which could impact our franchise fee revenues or harm our reputation. We do not participate in the negotiations of collective bargaining agreements covering unionized labor employed by third-party owners and franchisees.

In addition, existing environmental laws and regulations may be revised or reinterpreted or new more stringent laws and regulations related to global climate change, air quality, or other environmental, health, and safety concerns may be adopted or become applicable to us. For example, compliance with future corporate responsibility and other climate-related legislation and regulation, and our efforts to achieve science-based emissions reduction and other targets, could be difficult and costly. As a result, we may experience significant increased operating and compliance costs, and operating disruptions or limitations, which could adversely affect our results of operations, financial condition, and business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
