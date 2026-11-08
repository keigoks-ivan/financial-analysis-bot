你是 stock-analyst v20 DD 的證據採集子 agent。標的：NET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - NET Cloudflare market share gaining OR losing 2026
  - Cloudflare new entrant OR displace threat Software - Infrastructure 2026
  - NET competitor design win 2026
  - Cloudflare vs Software - Infrastructure peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
Competition We compete in the market for network services primarily across three categories: •On-premises network hardware vendors. We compete with companies in this category to provide security, performance, and reliability services. We believe we are positioned favorably against these vendors with our cloud-based, multitenant approach that is better suited to an increasingly cloud-based world and that allows customers to treat our services as operational as opposed to capital costs.

In addition, we believe we are increasingly competing with public cloud vendors for storage and compute workloads as more third-party developers utilize our serverless platform. Because of the efficiency of our Cloudflare Workers product, we are able to offer it at prices that are highly competitive with public cloud vendors, and because it is distributed across our entire network, it enables the development of applications that were not previously possible on the traditional public cloud.

We believe that we are positioned favorably against our competitors based on these principal competitive factors.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
The markets for our network and products are intensely competitive and characterized by rapid changes in technology, customer requirements, industry standards, and frequent introductions of new, and improvements of, existing products. Our broad portfolio of products exposes us to competition from a large number of competitors in a number of different markets, including companies and their product and services offerings in, among others, virtual private networks, internal and external firewalls, web security (including web application firewalls and content filtering), distributed denial-of-service (DDoS) prevention, intrusion detection and prevention, application delivery controls, content delivery networks, domain name systems, email security vendors, advanced threat prevention, and wide area network (WAN) technology.

Our competitors provide both on-premises, appliance-based solutions, and cloud-based services that have functionality similar to our network and products. We expect competition to increase as other established and emerging companies and start-ups enter the markets for products and solutions for security, performance, and reliability, in particular with respect to cloud-based solutions, as customer requirements evolve and as new products, services, and technologies, including those that leverage artificial intelligence (AI) and machine learning, are introduced. If we are unable to anticipate or effectively react to these competitive challenges, our competitive position could weaken, and we could experience a decline in revenue or our growth rate that could materially and adversely affect our business and results of operations.

Our potential competitors include large companies with substantial infrastructure, such as global telecommunications services provider partners and public cloud providers. These companies could choose to enter the markets for products and solutions for security, performance, and reliability, including by acquiring existing companies, developing their own internal solutions, or establishing cooperative relationships with businesses that may allow them to offer more comprehensive solutions or to offer solutions for lower prices or to adapt more quickly than us to new technologies and customer needs. As our business continues to grow and we increase our market share for various products and services, these larger companies may increase their focus on us as a competitor and the actions they undertake to compete with our business and products. Additionally, if an increasing portion of web content is housed on another company’s network or portions of the Internet are otherwise privatized, it could reduce the demand for our products and increase competitive pressure on us. These competitive pressures in our markets or our failure to compete effectively may result in price reductions, fewer subscriptions, reduced revenue and gross margin, increased net losses, and loss of market share.

Our current competitors include a number of different types of companies, including: •on-premises network hardware vendors; •point solution vendors, which provide cloud-based products and services to address a single use case or challenge, in various categories including cloud security vendors, content delivery network (CDN) vendors, domain name system (DNS) services vendors, email security vendors, and cloud SD-WAN vendors; and •traditional public cloud vendors.

In addition, some of our larger competitors have substantially broader and more diverse product and services offerings, which may allow them to leverage existing commercial relationships, incorporate functionality into existing products, sell products and services with which we compete at zero or negative margins, offer fee waivers and reductions or other economic and non-economic concessions, bundle products and solutions, maintain closed technology platforms, or render our products unable to interoperate with such platforms. If they were to engage in predatory competitive practices, it could harm our existing product offerings or prevent us from creating viable products in other segments of the markets in which we participate. If our competitors are able to exploit their advantages or are able to persuade our customers or potential customers that their products are superior to ours, we may not be able to compete effectively and our business, financial condition, and results of operations may be materially affected.

To execute our growth plan, we must also attract and retain large numbers of highly qualified personnel in a number of job markets globally. In particular, it is critical for us to attract and retain sales and engineering talent in our fast growing industry. Competition for these personnel in the San Francisco Bay Area, where our headquarters is located, and in Lisbon, London, Singapore, and Austin, Texas, as well as other locations where we employ personnel, is intense, especially for experienced sales professionals and for engineers experienced in designing and developing cloud applications. We have from time to time experienced, and we may continue to experience, difficulty in hiring and retaining employees with appropriate qualifications or level of experience. For example, we have experienced, and may continue to experience, difficulty recruiting, hiring, and retaining sales personnel with the appropriate level of experience and knowledge necessary to effectively sell our products to large customers. Additionally, in recent years, recruiting, hiring, and retaining employees with expertise in the cybersecurity industry has become increasingly difficult as the demand for cybersecurity professionals has increased as a result of high-profile cybersecurity attacks on global corporations and governments.…

Independent industry and financial analysts often provide reviews of our products, as well as those of our competitors. Perception of our offerings in the marketplace may be significantly influenced by these expert reviews. In addition, the difficulty or inability of us to periodically provide certain types of financial information about our business and products requested by industry analysts could adversely impact these analysts’ reviews of our products. If reviews of our products are negative, or less positive than those of our competitors’, our brand may be adversely affected. The performance of our channel partners also may affect our brand and reputation, particularly if customers do not have a positive experience with our channel partners. The promotion of our brand requires us to make substantial expenditures, and we anticipate that the expenditures will increase as our markets become more competitive and we expand into new markets and products. Expenditures intended to maintain and enhance our brand may not be cost-effective or effective at all. If we do not successfully maintain and enhance our brand, we may have reduced pricing power relative to our competitors, we could lose customers, or we could fail to attract potential new customers or expand sales to our existing customers, all of which could materially and adversely affect our business, results of operations, and financial condition.

Our network and products incorporate software licensed under open source licenses, including open source software included in software we receive from third-party commercial software vendors. Use of open source software may entail greater risks than use of third-party commercial software, as open source licensors generally do not provide support, updates, or warranties, or other contractual protections regarding infringement claims or the quality of the software. In addition, the wide availability of source code incorporated in our products could allow hostile parties to more easily identify security vulnerabilities in our network and products. The terms of some open source licenses may provide that under certain conditions we could be required to release the source code of our 62 Table of contents proprietary software, and to make our proprietary software available under open source licenses, including authorizing further modification and redistribution.…

Any unanticipated disclosure of, or litigation regarding, our source code and any open source software incorporated into our source code could result in adverse judgments and liabilities, require us to reengineer all or a portion of our network and products, limit the marketing of our products, provide an advantage to our competitors or other entrants to the market, create new security vulnerabilities or highlight existing security vulnerabilities in our network and products, and reduce or eliminate the value of our network and products. We cannot assure you that our processes for controlling our use of open source software in our network and products will be effective.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
