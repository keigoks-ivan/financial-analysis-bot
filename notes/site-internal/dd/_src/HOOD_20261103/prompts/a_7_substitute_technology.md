你是 stock-analyst v20 DD 的證據採集子 agent。標的：HOOD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Robinhood Markets product substitute technology threat 2026
  - Capital Markets / Online Brokerage / Fintech Platform alternative technology disruption 2026 2027
  - HOOD Robinhood Markets technology obsolescence risk
  - Capital Markets / Online Brokerage / Fintech Platform next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm｜as_of：2026-02-18
<<<
Our mission is to democratize finance for all. We use technology to provide access to the financial system in a way that is simple and convenient for our customers. We believe the financial system should be built to work for everyone. That’s why we create products that let our customers start investing at their own pace, on their own terms. We believe investing should be familiar and welcoming, with a simple design and an intuitive interface, so that customers are empowered to achieve their goals. We started with a revolutionary, bold brand and design in the Robinhood app which makes investing approachable for millions. Over the last decade, we have disrupted and changed the industry, becoming the first U.S. retail broker to offer commission-free stock trading with no account minimums, which was subsequently adopted by the rest of the industry. In recent years, we have continued to build relationships with our customers by introducing new products and diversifying our services that further expand access to the financial system, including focusing on products and tools for more seasoned investors. Through these efforts, we believe we have made investing culturally relevant and understandable, and that our platforms enable our customers to become long-term investors and take greater control of their finances.

The sanctions for FCPA and Bribery Act violations can be significant. The SEC may bring civil enforcement actions against issuers and their officers, directors, employees, stockholders, and agents for violations of the anti-bribery or accounting provisions of the FCPA. Companies and individuals that have committed violations of the FCPA may have to disgorge their ill-gotten gains plus pay prejudgment interest and substantial civil penalties. Companies may also be subject to oversight by an independent consultant. In the U.K., the Serious Fraud Office has also published various policies and internal guidance 28 Table of Contents documents for investigators and prosecutors considering bribery offenses. The consequences for individuals and organizations found guilty of an offense under the Bribery Act can be serious. The maximum sentence is 10 years for individuals who commit such offenses. Organizations are liable for an unlimited fine; removal of tainted proceeds; debarment from public sector contracts/tenders, as well as the disruption and cost of a law enforcement investigation; and directors may be disqualified from acting as a director for up to fifteen years.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm｜as_of：2026-02-18
<<<
The markets in which we compete are evolving and highly competitive, with multiple participants competing for the same customers. Our current and potential future competition principally comes from incumbent brokerages, established financial technology companies, venture-backed financial technology firms, banks, cryptocurrency exchanges, asset management firms, financial institutions, consumer financial service providers and technology platforms. The majority of our competitors have longer operating histories and greater capital resources than we have and offer a wider range of products and services. Some of our competitors, particularly new and emerging technology companies, are not subject to the same regulatory requirements or scrutiny to which we are subject, which could allow them to innovate more quickly or take more risks, placing us at a competitive disadvantage. The impact of competitors with superior name recognition, greater market acceptance, larger customer bases, or stronger capital positions could adversely affect our results of operations and customer acquisition and retention. Our competitors might also be able to respond more quickly to new or changing opportunities and demands and withstand changing market conditions better than we can, especially larger competitors that might benefit from more diversified product and customer bases.…

56 Table of Contents Our ability to attract, engage, and retain our customers and to increase our revenue depends heavily on our ability to evolve our existing products and services and to create and monetize new products and services that are adopted by customers. Rapid and significant technological changes continue to confront the financial services industry, including developments in the methods in which securities are traded and developments in cryptocurrencies. To keep pace or to innovate we have introduced and might continue to introduce significant changes to our existing products and services or acquire or introduce new and unproven products and services, including using technologies with which we have little or no prior development or operating experience (for instance, event contracts). Our efforts have been and might continue to be inhibited by industry-wide standards, legal restrictions, incompatible customer expectations, demands, and preferences, or third-party intellectual property rights. Our efforts to innovate have been and might continue to also be delayed or blocked by new or enhanced regulatory scrutiny or technical complications.…

We rely on technology, including the internet and mobile services, to conduct much of our business activity and allow our customers to conduct financial transactions on our platforms. Our systems and operations, including our cloud-based operations and disaster recovery operations, those of the third parties on which we rely to conduct certain key functions, and those of companies we have acquired or may seek to acquire in the future, are vulnerable to disruptions from natural disasters, power and service outages, interruptions or losses, computer and telecommunications failures, software bugs, cybersecurity attacks, computer viruses, malware, distributed denial of service attacks, spam attacks, phishing or other social engineering, ransomware, security breaches, credential stuffing, technological failure, vulnerabilities, human error, terrorism, improper operation, unauthorized entry, data loss, intentional bad actions, and other similar events and we have experienced such disruptions in the past. For example, on October 20, 2025, Amazon Web Services (AWS) experienced a major disruption in its US-EAST-1 region due to a failure in an internal system. This affected certain of our operations, resulting in service instability and interruption.…

In addition, surges in trading volume on our platforms have in the past and might in the future cause our systems to operate at diminished speed or even fail, temporarily or for a more prolonged period of time, which would affect our ability to process transactions and potentially result in some customers’ orders being executed at prices they did not anticipate, executed incorrectly, or not executed at all. For example, we experienced (i) the March 2020 Outages, which resulted in some of our customers being unable to buy and sell securities and other financial products on our U.S. trading platform for a period of time, and (ii) the partial service outages and degraded service on our RHC cryptocurrency platform from time to time in mid-April and early May 2021 caused by a surging demand for cryptocurrency trading (the “April-May 2021 Disruptions”), which resulted in some of our customers being unable to buy and sell cryptocurrencies for a period of time. Our platforms have otherwise in the past and might in the future experience outages. The March 2020 Outages resulted in putative class action lawsuits, arbitrations, and regulatory examinations and investigations, as well as cash remediation payments.…

We currently use machine learning and AI to improve our products and processes in certain circumstances, such as to increase the efficiency of our in-app chat support, customer support workflows, fraud detection systems, and software coding optimization, as well as to improve the customer experience in our newsfeed, and we have plans to continue to expand our use of AI in the future. Our research and development of such technology also remains ongoing. As with many new and emerging technologies, AI presents numerous risks and challenges that could adversely affect our business. If we fail to keep pace with rapidly evolving AI technological developments, especially in the financial technology sector, our competitive position and business results may suffer. At the same time, use of AI has recently become the source of significant media attention and political debate. The introduction and use of AI technologies, particularly generative AI, into new or existing offerings may result in new or expanded risks and liabilities, including due to enhanced governmental or regulatory scrutiny, litigation, compliance issues, ethical concerns, confidentiality or security risks, as well as other factors that could adversely affect our business, reputation, and financial results.…

Furthermore, forks can lead to disruptions of networks and our information technology systems, cybersecurity attacks, replay attacks, or security weaknesses, any of which can further lead to temporary or even permanent loss of customer cryptocurrencies. For instance, when the Ethereum and Ethereum Classic networks split in July 2016, replay attacks, in which transactions from one network were rebroadcast on the other network to achieve “double-spending,” plagued platforms that traded Ethereum through at least October 2016, resulting in significant losses to some cryptocurrency platforms. Another possible result of a fork is an inherent decrease in the level of security due to the splitting of some mining power across networks, making it easier for a malicious actor to gain the majority of the mining power of that network. Such disruption and loss could cause our company to be exposed to liability, even in circumstances where we have no intention of supporting a cryptocurrency compromised by a fork.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/parts/axes_7.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
