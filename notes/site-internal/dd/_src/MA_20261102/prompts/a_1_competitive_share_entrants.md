你是 stock-analyst v20 DD 的證據採集子 agent。標的：MA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MA Mastercard market share gaining OR losing 2026
  - Mastercard new entrant OR displace threat Credit Services 2026
  - MA competitor design win 2026
  - Mastercard vs Credit Services peers market share trend 2025 2026


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
Competition We face a number of competitors both within and outside of the global payments industry. We compete in all categories of payments (including paper-based payments and all forms of electronic payments) as well as in all categories in which we provide services and solutions: •General Purpose Payments Networks. We compete worldwide with payments networks such as Visa, American Express, JCB, China UnionPay and Discover, among others. These competitors tend to offer a range of card-based payment products. Some competitors have more market share than we do in certain jurisdictions. Some also have different business models that may provide an advantage in pricing, technology, regulatory compliance burdens or otherwise. Globally, financial institutions may issue both Mastercard-branded and competitor payment products, and we compete for business on the basis of individual portfolios or programs. In addition, a number of our customers issue American Express-, China UnionPay- and/or Discover-branded payment cards in a manner consistent with a four-party system. We continue to face intense competitive pressure on MASTERCARD 2025 FORM 10-K 21

•Debit and Local Networks. We compete with ATM and point-of-sale debit networks. In various countries, local debit brands serve as the main domestic brands, while our brands are used mostly to enable cross-border transactions (typically representing a small portion of overall transaction volume). In addition, several governments are promoting, or considering promoting, local networks for domestic switching. See “Risk Factors” in Part I, Item 1A for a more detailed discussion of the risks related to payments system regulation and government actions that may prevent us from competing effectively.

•Real-time Account-based Payments Systems. We face competition in the ACH and real-time account-based payments space from providers of infrastructure, applications and services. As these real-time account-based propositions mature, we face a possible increase in competition for our existing domestic person-to-merchant (“P2M”) and person-to-person (“P2P”) transaction market share. Similarly, as interlinking of these infrastructures is further explored, they could disrupt our existing cross-border P2M and P2P market share. Also, several industry initiatives are experimenting with the concept of account-based global schemes, which could lead to a disruption of the clearing and settlement options utilized in various currencies.

•Services and Solutions Providers. We face competition from companies that provide alternatives to our services and solutions. These companies include information services and consulting firms that provide consulting services and insights to financial institutions, merchants and governments, technology companies that provide cyber and fraud solutions (including AI-based solutions), and companies that compete against us as providers of loyalty and program management solutions. We also face competition from companies that provide alternatives to our other solutions, including open finance. Regulatory initiatives could also lead to increased competition in this space.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm｜as_of：2026-02-11
<<<
The global payments industry is highly competitive. Our payment programs compete against competitors both within and outside of the global payments industry and compete in all payment categories, including paper-based payments and all forms of electronic payments. We compete against general purpose payments networks, debit and local networks, ACH and real-time account-based payments systems, digital wallets and other fintechs (focused on online activity across various channels and processing payments using in-house capabilities), digital public infrastructure and other government-backed solutions and digital currencies. We also face competition from companies that provide alternatives to our services and other solutions.

Certain of our competitors to our payment network operate three-party payments systems with direct connections to both merchants and consumers, potentially providing competitive advantages. If we continue to attract more regulatory scrutiny than these competitors because we operate a four-party system, or we are regulated because of the system we operate in a way in which our competitors are not, we could lose business to these competitors. See “Business - Competition” in Part I, Item 1.

Certain of our competitors have developed alternative, e-commerce and/or mobile device payments systems, as well as physical store locations. A number of these competitors rely principally on technology to support their services that provides cost advantages, and as a result may benefit from lower costs than we do. Many of these competitors are also able to use existing payment networks without being subject to many of the associated costs. Moreover, these competitors also occupy various roles in the payments ecosystem that enable them to influence payment choice of other participants. With respect to government-backed solutions, including those involving DPI, government participation in structures could prevent us from entering into, or substantially restrict us from participating in, particular geographies. Any of these factors could put us at a competitive disadvantage.

If we are not able to differentiate ourselves from our competitors, drive value for our customers and/or effectively align our resources with our goals and objectives, we may not be able to compete effectively against these threats. Our failure to compete effectively against any of the foregoing threats could materially and adversely affect our overall business and results of operations.

•Payments industry participants may develop their own products and services to support our switched transaction and payments offerings, forcing us to change our pricing or practices for our own offerings in order to compete. Participants may also withhold rights to data we use to power our solutions in order to support their own potential future solutions, potentially impacting the effectiveness of our solutions. In addition, governments may promote their own national or international payments platforms, potentially putting us at a competitive disadvantage in those markets, or requiring us to compete differently. Moreover, as central banks experiment with CBDCs, policies and design considerations that governments adopt could impact the extent of our role in facilitating CBDC-based payment transactions, potentially impacting the transactions that we may process over our network.

In the future, we may not be able to enter into agreements with our customers if they require terms that we are unable or unwilling to offer, and we may be required to modify existing agreements in order to maintain relationships and compete with others in the industry. Some of our competitors are larger with greater financial resources and accordingly may be able to charge lower prices. In addition, to the extent that we offer discounts or incentives under such agreements, we will need to further increase transaction volumes or the amount of services provided in order to benefit from such agreements and to increase revenue and profit, and we may not be successful in doing so, particularly in the current regulatory environment. Our customers also may implement cost reduction initiatives that reduce or eliminate payment product marketing or increase requests for greater incentives or greater cost stability. In addition to decisions made by competitors and customers, we also face pressure from pricing regulation and litigation.

Our future success will depend, in part, on our ability to anticipate, develop or adapt to technological changes and evolving industry standards. If we fail to sufficiently develop and adopt new technologies, or improve and keep pace with current technologies and reflect such technology in our payments offerings, our payments offerings could be negatively impacted and/or we could be put at a competitive disadvantage. This could impact our ability to compete with new technologies and products, as well as encourage customers that use our technology to enhance and deliver their payment-related products and services (including fintechs and technology companies) to use their own technology to compete against us. These developments could lead to a decline in the use of our technology, products and services, which could have a material adverse impact on our overall business and results of operations.

While we have exclusive, or nearly-exclusive, relationships with certain of our customers to issue payment products, other customers have similar exclusive, or nearly-exclusive, relationships with our competitors. These relationships may make it difficult or cost-prohibitive for us to do significant amounts of business with these customers to increase our revenues. In addition, these customers may be more successful and may grow faster than the customers that primarily issue our payment products, which could put us at a competitive disadvantage. Furthermore, we earn substantial revenue from customers with nearly-exclusive relationships with our competitors. Such relationships could provide advantages to the customers to shift business from us to the competitors with which they are principally aligned. A significant loss of our existing revenue or transaction volumes from these customers could have a material adverse impact on our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
