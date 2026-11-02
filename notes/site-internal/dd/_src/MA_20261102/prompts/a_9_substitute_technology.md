你是 stock-analyst v20 DD 的證據採集子 agent。標的：MA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Mastercard product substitute technology threat 2026
  - Credit Services alternative technology disruption 2026 2027
  - MA Mastercard technology obsolescence risk
  - Credit Services next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm｜as_of：2026-02-11
<<<
ITEM 1. BUSINESS Our Strategic Priorities Consumer payments. We focus on enabling consumer payments, providing consumers with choice and flexibility to transact across multiple payment rails (including cards, real-time payments and account-based transactions), while ensuring that all payments are secure and seamless. We do so by: •Capturing the significant secular opportunity of cash displacement by increasing acceptance through advancing technology and partnering with players across the payments ecosystem, as well as by opening up closed-loop and domestic networks. We also pursue incremental volume and transactions by extending our reach across under-penetrated card verticals (such as bill pay) and real-time account-based payments •Driving brand preference through compelling consumer experiences by offering relevant value propositions to consumers (including features, benefits, events and activities), providing comprehensive digital functionality (such as Digital First and One Credential), delivering enhanced security and functionality (increasing tokenization, scaling authentication and streamlining online checkout) and driving increased approval, spend and activation rates •Investing in the future and driving market transformation by extending the reach of our network to enable the tokenization of credentials, identities, assets and data and the exchange of those items between counterparties (providing security, privacy and control). We also seek to achieve this transformation by modernizing our payment network (including enabling real-time card payments) to meet evolving needs Commercial and new payment flows.…

•Real-time Account-based Payments Systems. We face competition in the ACH and real-time account-based payments space from providers of infrastructure, applications and services. As these real-time account-based propositions mature, we face a possible increase in competition for our existing domestic person-to-merchant (“P2M”) and person-to-person (“P2P”) transaction market share. Similarly, as interlinking of these infrastructures is further explored, they could disrupt our existing cross-border P2M and P2P market share. Also, several industry initiatives are experimenting with the concept of account-based global schemes, which could lead to a disruption of the clearing and settlement options utilized in various currencies.

•Digital Currencies. Stablecoins and cryptocurrencies may become more popular as they potentially become more regulated around the globe (through laws such as the GENIUS Act, which in 2025 became the first major crypto legislation in the U.S.) and are increasingly perceived to provide immediacy, 24/7 accessibility, immutability and efficiency. Some players, including payment service providers and payment facilitators, have started to enable merchant acceptance of such currencies in P2M, while some banks have started experimenting with blockchain B2B payments. Digital currencies and emerging players (such as crypto natives) have the ability to disrupt traditional financial markets. The increased prominence of digital currencies creates an opportunity for us, but could also compete with our products and services.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm｜as_of：2026-02-11
<<<
Governments in some countries have acted, or in the future may act, to provide resources, preferential treatment or other protection to selected national or domestic payment and switching providers, or have created, or may in the future create, their own national provider. These actions may displace us from, prevent us from entering into, or substantially restrict us from participating in, particular geographies, and may prevent us from competing effectively against those providers. For example: •Governments in some countries have implemented, or may implement, regulatory requirements that mandate switching of domestic payments either entirely in that country or by only domestic companies.

The payments industry is subject to rapid and significant technological changes, including new technologies and changes to existing technologies (such as digital assets and blockchain, AI, machine learning, privacy enhancement and cybersecurity). These changes could result in new technologies that may be superior to, or render obsolete, the technologies we currently use in our programs and services. They may also result in new and innovative payment methods, products and services.

Our future success will depend, in part, on our ability to anticipate, develop or adapt to technological changes and evolving industry standards. If we fail to sufficiently develop and adopt new technologies, or improve and keep pace with current technologies and reflect such technology in our payments offerings, our payments offerings could be negatively impacted and/or we could be put at a competitive disadvantage. This could impact our ability to compete with new technologies and products, as well as encourage customers that use our technology to enhance and deliver their payment-related products and services (including fintechs and technology companies) to use their own technology to compete against us. These developments could lead to a decline in the use of our technology, products and services, which could have a material adverse impact on our overall business and results of operations.

The payments markets in which we compete are characterized by rapid technological change, new product introductions, evolving industry standards and changing customer and consumer needs. In order to remain competitive and meet the needs of the payments markets, we are continually involved in developing and implementing complex multi-rail solutions and diversifying our products and services. These efforts carry the risks associated with any diversification initiative, including cost overruns, delays in delivery and performance problems. These projects also carry risks associated with working with different types of customers (such as corporations that are not financial institutions, non-governmental organizations (NGOs) and new end users). These differences may present new operational challenges, such as enhanced infrastructure and monitoring for less regulated customers.

Our transaction switching systems and other offerings may experience interruptions as a result of technology malfunctions, network degradation, updates and migrations to new technology and platforms, supply-chain attacks, fire, floods, earthquakes, weather events, power outages, telecommunications disruptions, terrorism, workplace violence, accidents or other catastrophic events (including those related to climate change). We have experienced in limited instances, and may continue to experience, some types of these interruptions. Our visibility in the global payments industry may also put us at greater risk of attack by terrorists, activists, or hackers who intend to disrupt our facilities, networks and/or systems. Inadequate infrastructure in lesser-developed markets could also result in service disruptions, which could impact our ability to do business in those markets. Additionally, we rely on third-party service providers for the timely transmission of information across our global data network. If one of our service providers fails to provide the communications capacity or services we require, as a result of natural disasters, operational disruptions, cybersecurity-related disruptions or failures, terrorism, hacking or any other reason, the failure could interrupt our services. Although we maintain an enterprise resiliency program to analyze risk, assess potential impacts, and develop effective response strategies, we cannot ensure that our business would be immune to these risks.…

While we work directly with many stakeholders in the payments system (including merchants, governments, fintechs and large digital companies and other technology companies), we are, and will continue to be, significantly dependent on our relationships with our issuers and acquirers and their respective relationships with account holders and merchants to support our programs and services. Furthermore, we depend on our issuing partners and acquirers to continue to innovate to maintain competitiveness in the market. We do not issue cards or other payment devices, extend credit to account holders or determine the interest rates or other fees charged to account holders. Each issuer determines these and most other competitive payment program features. In addition, we do not establish the discount rate that merchants are charged for acceptance, which is the responsibility of our acquiring customers. As a result, our business significantly depends on the continued success and competitiveness of our issuing and acquiring customers and the strength of our relationships with them. In turn, our customers’ success depends on a variety of factors over which we have little or no influence, including economic conditions in global financial markets or their disintermediation by competitors or emerging technologies, as well as regulation. If our customers become financially unstable, we may lose revenue or we may be exposed to settlement risk.…

Our performance largely depends on the skills, capabilities and motivation of our employees (including our people leaders), as well as the environment we create for them to enable them to perform their jobs effectively. The market for specialized skill-sets remains highly competitive, particularly in emerging technologies. To the extent we are unable to differentiate our value proposition in the market, effectively develop leaders and build robust succession pipelines, it could impact our ability to deliver for our customers. Failure to attract, hire, develop, motivate and retain highly qualified talent could leave us vulnerable to not identifying and/or acting on emerging customer or market opportunities. In addition, broader trends such as escalations in global conflict and a rise in mental health needs are impacting the well-being of our people. To the extent we are unable to communicate effectively on these issues and provide support to our employees, we could experience a significant impact on our business, reputation and culture. Further, changes in and enforcement of immigration and work permit laws and visa regulations have made it difficult for employees to work in, or transfer among, jurisdictions where we operate, potentially impairing our ability to attract and retain talent.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
