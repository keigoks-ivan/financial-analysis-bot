你是 stock-analyst v20 DD 的證據採集子 agent。標的：ANET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - ANET Arista Networks market share gaining OR losing 2026
  - Arista Networks new entrant OR displace threat Computer Hardware 2026
  - ANET competitor design win 2026
  - Arista Networks vs Computer Hardware peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
Our Market Drivers and Products Centers of Data Drive the World 1 Table of Contents In the modern competitive landscape, the ability to access, manipulate, and leverage data is fundamental to an organization’s growth and viability. This is especially true in the era of Large Language Models (LLMs), agentic AI, and physical AI, where data has evolved from a byproduct of operations into the primary engine of intelligence and autonomy. Consequently, the network has matured beyond traditional "IT infrastructure" to become the spine or central nervous system. It serves as the critical conduit through which data flows from cloud and edge environments to the AI models that drive decision-making. This heightened dependency on real-time data movement underscores the necessity for a network architecture defined by unprecedented scale, availability, predictable performance, and open programmability. Operational simplicity and robust security are essential to ensure the business can compete in a world of massive, networked transactions.

Competition The markets in which we participate are highly competitive and characterized by rapidly transforming technology, changing end-customer needs, evolving industry standards, frequent introductions of new products and services and industry consolidation. We expect competition to intensify in the future as the market for cloud and AI networking expands and existing competitors and new market entrants introduce new products or enhance existing products.

The data center and campus networking markets have historically been dominated by Cisco, with competition also coming from other large network equipment and system vendors, including Dell/EMC, Extreme Networks, Hewlett Packard Enterprise, Huawei, Juniper Networks, Nvidia, and white box networking vendors that utilize open-source operating systems. Most of our competitors and some strategic alliance partners have made acquisitions and/or have entered into or extended partnerships or other strategic relationships to offer more comprehensive product lines, including cloud networking solutions. For example, Broadcom has acquired VMware, Hewlett Packard Enterprise has acquired Juniper Networks and Nvidia has made significant investments in several AI Neoclouds. We often see that these types of acquisitions and strategic investments are used to influence buying decisions rather than allowing for the selection of a best-of-breed vendor.

We also face competition from other companies and new market entrants, current technology partners, and customers who may acquire or develop network switches and cloud service solutions for internal use and/or broaden their product portfolios to market and sell to customers. Some of these entities are developing white box networking products based on open-source network operating systems that may be provided for free using off-the-shelf or commoditized hardware technology 8 Table of Contents (“white box” hardware). Others may adopt a disaggregated approach to the procurement of hardware and leverage their own proprietary software. The arrival of new market entrants and the rapid adoption of alternative technologies may create downward pricing pressure. Such shifts could result in lost sales and materially harm our operating results and financial condition.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1596532/000159653226000013/anet-20251231.htm｜as_of：2026-02-17
<<<
We have made substantial investments to develop new products and services, make enhancements to existing products, and expand our product offerings through our acquisitions and internal research and development efforts. If we are unable to anticipate technological changes in our industry by introducing new, enhanced or expanded products and services in a timely and cost-effective manner or if we fail to introduce products and services that meet market demand or gain market share, we may lose our competitive position, our products may become obsolete, and our business, financial condition or results of operations could be adversely affected. For example, with our most recently introduced 800 GbE, AI focused Ethernet products and AI-Driven Campus and Branch Networking Offerings, our ability to maintain our competitive position with our customers will depend on our ability to deliver these new products in a timely manner, our customers' acceptance of these products and the growth of the markets that these products serve. In addition, the evaluation, testing and qualification of our new products by our customers may be lengthy and may require increased customer trials and contracts with acceptance clauses, which delay revenue recognition and may negatively impact our revenue.

Additionally, from time to time, we invest in expansion into adjacent markets, including campus and Wi-Fi networking, AI networking, cloud and enterprise routing markets, network security markets and SD-WAN markets. Although we believe these solutions are complementary to our current offerings, we have less experience and a more limited operating history in these markets, and our efforts in this area may not be successful. Expanding our services in existing and new markets and increasing the depth and breadth of our presence imposes significant burdens on our marketing, compliance, and other 20 administrative and managerial resources. In addition, the markets for our products, particularly the AI Ethernet segment, are characterized by rapid evolution and volatility; consequently, these markets may experience significant fluctuations, including prolonged slowdowns, cyclical contractions, or the correction of speculative bubbles that could adversely affect demand. Our plan to expand and deepen our market share in our existing markets and possibly expand into additional markets is subject to a variety of risks and challenges.…

The markets in which we compete, including the markets for data center, campus networking, network visibility and security and AI, are intensely competitive, and we expect competition to increase in the future from established competitors, industry consolidation and new market entrants. This competition has resulted in increased pricing pressure, which could result in reduced profit margins, increased sales and marketing expenses and the loss of market share, any of which would likely harm our business, financial condition, results of operations and prospects.

We also face competition from other companies and new market entrants, including current technology partners, suppliers and customers or other cloud service providers who may acquire or develop network switches and cloud service solutions for internal use and/or to broaden their portfolio of products to market and sell to customers. Some of these competitors are developing "white box" networking products based on open-source network operating systems that may be provided for free and off-the-shelf or commoditized hardware technology, or “white box” hardware, while other competitors may adopt a disaggregated approach to the procurement of hardware and their proprietary software. Customers may also increase their adoption of networking solutions based upon open-source network operating systems that may be provided for free and used either on “white box” or proprietary hardware. As new markets emerge like AI, we expect the field to remain intensely competitive as our competitors have made significant investments in such new markets. In addition, we have not established broad market awareness or acceptance of our AI Ethernet products that will compete against more established InfiniBand products or against the AI Ethernet products of other competitors.…

Detecting and protecting against the unauthorized use of our products, technology and proprietary rights is expensive, difficult and, in some cases, impossible. Litigation may be necessary in the future to enforce or defend our intellectual property rights, to protect our trade secrets or to determine the validity and scope of the proprietary rights of others. Such litigation could result in substantial costs and diversion of management resources, either of which could harm our business, financial condition, results of operations and prospects, and there is no guarantee that we would be successful. Furthermore, many of our current and potential competitors have the ability to dedicate substantially greater resources to protecting their technology or intellectual property rights than we do. Accordingly, despite our efforts, we may not be able to prevent third parties from infringing or misappropriating our intellectual property rights, which could result in a substantial loss of our market share.

Our future success depends, in part, on our ability to continue to attract and retain highly skilled personnel, particularly software engineering and sales personnel. In addition, we are expanding internationally and into adjacent markets including the enterprise and AI market, which requires a significant investment of time, effort and financial resources into hiring and training our sales force to address these markets. If we do not effectively train our direct sales force, we may be unable to add new customers, increase sales to our existing customers, or successfully expand into new markets. Competition for highly skilled personnel is often intense, especially in the San Francisco Bay Area where we have a substantial presence and need for highly skilled personnel, especially with certain types of technical skills like in AI. Many of the companies with which we compete against for experienced personnel may have greater resources and be able to provide more attractive compensation packages and other amenities. Research and development personnel are aggressively recruited by startup and growth companies, which are especially active in many of the technical areas and geographic regions in which we conduct product development. In addition, in making employment decisions, particularly in the high-technology industry, job candidates often consider the value of the stock-based compensation they are to receive in connection with their employment.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
