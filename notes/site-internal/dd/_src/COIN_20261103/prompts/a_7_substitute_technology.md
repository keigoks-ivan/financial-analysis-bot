你是 stock-analyst v20 DD 的證據採集子 agent。標的：COIN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Coinbase Global product substitute technology threat 2026
  - Financial Data & Stock Exchanges alternative technology disruption 2026 2027
  - COIN Coinbase Global technology obsolescence risk
  - Financial Data & Stock Exchanges next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm｜as_of：2026-02-12
<<<
Although we maintain insurance coverage, it may be insufficient to protect us against all losses and costs stemming from security breaches, cyberattacks, and other types of unlawful activity, or any resulting disruptions or data theft and loss from such events. Outages and disruptions of our platform, including any caused by cyberattacks, may harm our reputation, business, operating results, and financial condition.

Our industry has been characterized by many rapid, significant, and disruptive products and services in recent years. These include decentralized applications, DeFi, yield farming, NFTs, play-to-earn games, lending, staking and re-staking, token wrapping, network and governance tokens, innovative programs to attract customers such as transaction fee mining programs, initiatives to attract traders such as trading competitions, airdrops and giveaways, staking reward programs, “layer 2” blockchain networks, smart contract wallets, and novel cryptocurrency fundraising and distribution schemes, such as “initial exchange offerings.” We expect new services and technologies to continue to emerge and evolve, which may be superior to, or render obsolete, the products and services that we currently provide. For example, decentralized networks and other disruptive technologies such as generative AI may fundamentally alter the use of our products or services in unpredictable ways. We cannot predict the effects of new services and technologies on our business. However, our ability to grow our customer base and net revenue will depend heavily on our ability to innovate and create successful new products and services, both independently and in conjunction with third-party developers. In particular, developing and incorporating new products and services into our business may require substantial expenditures, take considerable time, and ultimately may not be successful.…

We rely on third parties in connection with many aspects of our business, including payment processors, financial institutions, and payment gateways to process transactions; cloud computing services and data centers that provide facilities, infrastructure, smart contract development, website functionality and access, components, and services, including databases and data center facilities and cloud computing; as well as third parties that provide outsourced customer service, compliance support and product development functions, which are critical to our operations. Because we rely on third parties to provide these services and to facilitate certain of our business activities, we face increased operational risks. We do not directly manage the operation of any of these third parties, including their data center facilities that we use. These third parties may be subject to financial, legal, regulatory, and labor issues, cybersecurity incidents, data theft or loss, break-ins, computer viruses or vulnerabilities in their code, denial-of-service attacks, sabotage, acts of vandalism, loss, disruption, or instability of third-party financial institution relationships, privacy breaches, service terminations, disruptions, interruptions, and other misconduct. They are also vulnerable to damage or interruption from human error, power loss, telecommunications failures, fires, floods, earthquakes, hurricanes, tornadoes, pandemics and similar events.…

We also rely on insurance carriers to insure customer losses resulting from a breach of our physical security, cybersecurity, or by employee or third party theft and hold surety bonds as required for compliance with certain of our licenses under applicable state laws. Our ability to maintain crime, specie, and cyber insurance, as well as surety bonds, is subject to the insurance carriers’ ongoing underwriting criteria and our inability to obtain and maintain appropriate insurance coverage could cause a substantial business disruption, adverse reputational impact, inability to compete with our competitors, and regulatory scrutiny, and could adversely affect our business, operating results, and financial condition.

Any significant disruption in our products and services, in our information technology systems, or in any of the blockchain networks we support, could result in a loss of customers or funds and adversely affect our brand, reputation, business, operating results, and financial condition.

If any of our systems, or those of our third-party service providers, are disrupted for any reason, our products and services may fail, resulting in unanticipated disruptions, slower response times and delays in our customers’ trade execution and processing, failed settlement of trades, incomplete or inaccurate accounting, recording or processing of trades, unauthorized trades, loss of customer information, increased demand on limited customer support resources, customer claims, complaints with regulatory organizations, lawsuits, or enforcement actions. Further, when these disruptions occur, we have in the past, and may in the future, fulfill customer transactions using inventory to prevent adverse user impact and limit detrimental impact to our operating results. A prolonged interruption in the availability or reduction in the availability, speed, or functionality of our products and services could harm our business. Significant or persistent interruptions in our services could cause current or potential customers or partners to believe that our systems are unreliable, leading them to switch to our competitors or to avoid or reduce the use of our products and services, and could permanently harm our reputation and brands.…

We deposit, transfer, and custody customer cash and crypto assets in multiple jurisdictions. In each instance, we require bank-level security encryption to store customers’ assets for our wallet and storage systems, as well as our financial management systems related to such custodial functions. Our security technology is designed to prevent, detect, and mitigate inappropriate access to our systems, by internal or external threats. We believe we have developed and maintained administrative, technical, and physical measures designed to comply with applicable legal requirements and industry standards. However, it is nevertheless possible that hackers, employees or service providers acting contrary to our policies, or others could circumvent these measures to improperly access our systems or documents, or the systems or documents of our business partners, agents, or service providers, and improperly access, obtain, or misuse customer crypto assets and funds. The methods used to obtain unauthorized access, disable, or degrade service or sabotage systems are also constantly changing and evolving and may be difficult to anticipate or detect for long periods of time.…

Any acquisitions and investments that we make could require significant management attention, disrupt our business, result in dilution to our shareholders, and could adversely affect our business, operating results, and financial condition.

Future forks may occur at any time. A fork can lead to a disruption of networks and our information technology systems, cybersecurity attacks, replay attacks, or security weaknesses, any of which can further lead to temporary or even permanent loss of our and our customers’ assets. Such disruption and loss could cause us to be exposed to liability, even in circumstances where we have no intention of supporting an asset compromised by a fork.

General Risk Factors Adverse economic conditions could adversely affect our business. Our performance is subject to general economic conditions, and their impact on the crypto asset markets and our customers. The United States and other key international economies have experienced cyclical downturns from time to time in which economic activity declined resulting in lower consumption rates, restricted credit, reduced profitability, weaknesses in financial markets, bankruptcies, and overall uncertainty with respect to the economy. Adverse general economic conditions have impacted in the past, and may impact in the future, the onchain economy, although the extent of such impacts remains uncertain and dependent on a variety of factors, including market adoption of crypto assets, global trends in the onchain economy, central bank monetary policies, instability in the global banking system, volatility and disruptions in the capital and credit markets, and other events beyond our control. Geopolitical developments, such as trade wars and foreign exchange limitations can also increase the severity and levels of unpredictability globally and increase the volatility of global financial and crypto asset markets. For example, in the past the capital and credit markets have experienced extreme volatility and disruptions, resulting in steep declines in the value of crypto assets.…

We may be adversely affected by natural disasters, pandemics, and other catastrophic events, and by man-made problems such as terrorism, that could disrupt our business operations, and our business continuity and disaster recovery plans may not adequately protect us from a serious disaster.

Natural disasters or other catastrophic events may also cause damage or disruption to our operations, international commerce, and the global economy, and could have an adverse effect on our business, operating results, and financial condition. Our business operations are subject to interruption by 76 Table of Contents natural disasters, fire, power shortages, and other events beyond our control. In addition, our global operations expose us to risks associated with public health crises, such as pandemics and epidemics, which could harm our business and cause our operating results to suffer. For example, the COVID-19 pandemic and the related precautionary measures that we adopted have in the past resulted, and could in the future result, in difficulties or changes to our customer support, or create operational or other challenges, any of which could adversely affect our business, operating results, and financial condition. Further, acts of terrorism, labor activism or unrest, and other geopolitical unrest, including ongoing regional conflicts around the world, could cause disruptions in our business or the businesses of our partners or the economy as a whole.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/parts/axes_7.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
