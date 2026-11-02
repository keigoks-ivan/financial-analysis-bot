你是 stock-analyst v20 DD 的證據採集子 agent。標的：GLXY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Galaxy Digital product substitute technology threat 2026
  - Capital Markets alternative technology disruption 2026 2027
  - GLXY Galaxy Digital technology obsolescence risk
  - Capital Markets next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
Our ability to grow our AI/HPC data center business in the future is also dependent on the overall market for AI/HPC data centers. The broader adoption, use, and commercialization of AI technology, and the continued rapid pace of developments in the AI industry, are inherently uncertain. For example, certain AI technology is under public scrutiny for creating inaccurate, incomplete or misleading content, unintended biases and other discriminatory or unexpected results, errors or inadequacies and may be, or be perceived to be, deficient, inaccurate, biased, unethical or otherwise flawed. Consumer and societal attitudes toward AI are evolving and there is a risk that regulators or the public may perceive AI technologies negatively. Concerns about automation, automated decision making, privacy, security, transparency, or other ethical considerations could deter adoption. Therefore, it is difficult to predict the demand for AI/HPC data center capacity, the size and growth rate for this market, the entry of competitive products, or the success of any existing or future products that may compete with any AI/HPC data centers we may develop. In addition, we cannot assure you that we will be able to keep up with the changing AI landscape or in developing services or infrastructure that can meet our customers’ evolving needs in a timely manner, if at all.…

Governments have limited or may limit the shipment of products in and out of their jurisdictions or impose tariffs on products, which could negatively impact our ability to receive AI/HPC data center equipment from our suppliers. Our third-party manufacturers, suppliers, sub-contractors and customers have been and will continue to be disrupted by worker absenteeism, quarantines, restrictions on employees’ ability to work, office and factory closures, severe weather, disruptions to ports and other shipping infrastructure, border closures, or other travel or health-related restrictions. Depending on the magnitude of such effects on our supply chain, shipments of parts for our existing bitcoin mining and AI/HPC data center equipment, as well as any new bitcoin mining and AI/HPC data center equipment we purchase, may be delayed. As our AI/HPC data center equipment requires repair or becomes obsolete and requires replacement, our ability to obtain adequate replacements or repair parts from the third-party manufacturers may therefore be hampered. Supply chain disruptions could therefore negatively impact our operations.

Some of our current and potential future competitors have longer operating histories and greater capital resources than we have and may offer a wider range of products and services. Some of our competitors, particularly new and emerging technology companies and those located outside the United States, are not subject to the same regulatory requirements or scrutiny we are subject to, which could allow them to innovate more quickly or take more risks, placing us at a competitive 28 Table of Content disadvantage. In addition, some of our competitors might also be able to respond more quickly to new or changing opportunities and demands and withstand changing market conditions better than we can, especially larger competitors that might benefit from more diversified product and customer bases.

Furthermore, forks can lead to disruptions of networks and our information technology systems, cybersecurity attacks, replay attacks, or security weaknesses, any of which can further lead to temporary or even permanent loss of customer cryptocurrencies. For instance, when the Ethereum and Ethereum Classic networks split in July 2016, replay attacks, in which transactions from one network were rebroadcast on the other network to achieve “double-spending,” plagued platforms that traded Ethereum through at least October 2016, resulting in significant losses to some cryptocurrency platforms. Another possible result of a fork is an inherent decrease in the level of security due to the splitting of some mining power across networks, making it easier for a malicious actor to exceed 50% of the mining power of that network. Such disruption and loss could cause our company to be exposed to liability, even in circumstances where we have no intention of supporting a cryptocurrency compromised by a fork.

The cryptocurrency market operates 24 hours a day, seven days a week. The cryptocurrency market does not have a centralized clearinghouse, and transactions in cryptocurrencies rely on direct settlements between third parties after trades are executed. Accordingly, we rely on our affiliates and third-party banks to facilitate cash settlements between customers and us and rely on the ability of our trading venues to complete cryptocurrency settlements. In addition, we must maintain cash assets in our bank accounts sufficient to meet the working capital needs of our business, which includes deploying available working capital to facilitate cash settlements between us and our customers or us and our trading venues. If our affiliates, third-party banks or trading venues have operational failures and cannot perform and facilitate our routine cash and cryptocurrency settlement transactions, we will be unable to support normal cryptocurrency trading operations and these disruptions could have an adverse impact on our business, financial condition and results of operations. Similarly, if we fail to maintain cash assets in our bank accounts sufficient to meet the working capital needs of our business and necessary to complete routine cash settlements related to our trading activity, such failure could impair our ability to support normal trading operations and these disruptions could have an adverse impact on our business, financial condition and results of operations.

Our business is highly dependent on maintaining effective information technology systems as well as the integrity and timeliness of the data we use to serve our customers, support our partners, and operate our business. It is possible that hardware failures or errors in our systems could result in data loss or corruption or cause the information we collect to be incomplete, or contain inaccuracies that our customers regard as significant. Because of the large amount of data that we collect and manage, if our data were found to be inaccurate or unreliable, or became inaccessible, whether due to failures, errors, or other reasons, or if we or any of our third-party service providers, especially our third-party dialing and routing software systems, were to fail to effectively maintain such information systems and data integrity, we could experience operational disruptions. Such disruptions may impact our customers, individuals and partner teams, and hinder our ability to provide services, establish appropriate pricing, retain and attract customers, establish reserves, report financial results timely and accurately and maintain regulatory compliance.

Disruptions of the information technology systems or infrastructure of certain of our third-party vendors and service providers could also disrupt our businesses, damage our reputation, increase our costs, and have a material adverse effect on our business, financial condition and results of operations.

Our performance is subject to general economic conditions, and their impact on the cryptoeconomy, markets and our customers. The United States and other key international economies have experienced cyclical downturns from time to time in which economic activity declined resulting in lower consumption rates, restricted credit, reduced profitability, weaknesses in financial markets, bankruptcies, and overall uncertainty with respect to the economy. Adverse general economic conditions have impacted in the past, and may impact in the future, the cryptoeconomy, although the extent of such impacts remains uncertain and dependent on a variety of factors, including market adoption of digital assets, global trends in the cryptoeconomy, central bank monetary policies, instability in the global banking system, volatility and disruptions in the capital and credit markets, and other events beyond our control. Geopolitical developments, such as trade wars and foreign exchange limitations can also increase the severity and levels of unpredictability globally and increase the volatility of global financial and digital asset markets. For example, in the past, the capital and credit markets have experienced extreme volatility and disruptions, resulting in steep declines in the value of digital assets.…

Natural disasters or other catastrophic events may also cause damage or disruption to our operations, international commerce, and the global economy, and could have an adverse effect on our business, operating results, and financial condition. Our business operations are subject to interruption by natural disasters, severe weather, fire, power shortages, and other events beyond our control. Further, acts of terrorism, labor activism or unrest, global conflict and other geo-political unrest could cause disruptions in our business or the businesses of our partners or the economy as a whole. For example, the continued conflict between Ukraine and Russia and the evolving conflict in the Middle East is likely to continue to create, impacts on global economic markets that are unpredictable. Furthermore, certain Galaxy operations are headquartered in Israel, with primary offices located in Tel Aviv. Approximately 75 Galaxy employees are physically located in Israel, a number of whom have military reserve service obligations. There has been no material impact from the ongoing conflict in the Middle East on our operations in the region. Galaxy management is monitoring the situation including implementing business continuity plans to mitigate future potential risk.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/parts/axes_7.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
