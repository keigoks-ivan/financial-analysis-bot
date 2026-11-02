你是 stock-analyst v20 DD 的證據採集子 agent。標的：CLS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - CLS Celestica market share gaining OR losing 2026
  - Celestica new entrant OR displace threat Electronic Components 2026
  - CLS competitor design win 2026
  - Celestica vs Electronic Components peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
Our end market revenue as a percentage of total revenue is as follows: 2025 2024 2023 ATS 26 % 33 % 42 % Communications 57 % 41 % 33 % Enterprise 17 % 26 % 25 % Industry overview Celestica operates in the contract design and manufacturing industry and competes with a variety of providers from EMS companies to ODMs. The EMS companies that Celestica competes with, typically manage global manufacturing and logistics networks that are capable of delivering customized solutions, and may offer, depending on the extent of their capabilities, end-to-end services covering the full product lifecycle, which can include assembly, supply chain management, testing, system integration, fulfillment and other services. ODMs offer a similar range of services, and also typically support the design and development of products they manufacture for their customers.

Enhance our Capabilities in R&D, New Technology Development, Quality Products and Design to support our HPS Business. We continually invest in our internal R&D capabilities to support the development of new technologies, products and IP, which support the offering within our HPS business. As an ODM, we believe it is critical for our competitive positioning to be competent in working with leading edge technologies for IT hardware products across networking, server and storage categories. Investment in our design and engineering capabilities and product roadmaps is required in order to maintain our technology leadership throughout upgrade cycles and to support our customers in their deployments of their critical IT products and infrastructure. We also invest in software engineering capabilities in order to support our customers on enablement of open-sourced solutions.

12 Competition The contract design and manufacturing industry is highly competitive with multiple global EMS and ODM providers competing for customers and programs. Our competitors in the EMS industry include Benchmark Electronics, Inc., Flex Ltd., Hon Hai Precision Industry Co., Ltd., Jabil Inc., Plexus Corp., and Sanmina Corporation, as well as smaller EMS companies that often have a regional, product, service or industry-specific focus. Our ODM competitors provide product design capabilities and manufacturing services and include Quanta Computer Inc., Wiwynn Corporation, and Accton Technology Corp. In some markets, particularly in data center switching, we also face competition from OEMs (including Arista Networks, Inc., Cisco Systems, Inc. and others), where customers may decide between the use of customized (ODM) and off-the-shelf (OEM) solutions, which may include considerations of cost, software, after-market services, and the degree of customization necessary, among others.

We also face indirect competition from current and prospective customers who evaluate our capabilities and commercial models against the merits of manufacturing products internally, and from distribution and logistics providers expanding their services across the supply chain, including assembly, fulfillment, logistics and in some cases, engineering services. There may be instances where our HPS offerings compete with a customer's hardware offerings. We compete with different companies depending on the type of service or geographic area.

Some of our competitors have greater scale and provide a broader range of services than we provide. We believe our competitive advantage is our track record in advanced manufacturing capabilities, design and engineering, quality, delivery, managing complexity and responsiveness enabling cost-effective solutions and speed-to-market, as well as value-added services, including engineering and supply chain services.

The landscape in our CCS segment remains very competitive. The IT hardware industry we serve has been characterized by rapid demand growth in recent years, with spending increasingly concentrated amongst large data center customers, primarily cloud-based and AI service providers, including hyperscalers, resulting in aggressive bidding from EMS providers and increased competition from ODMs as they attempt to gain greater share in this market.

To remain competitive, we believe we must continue to provide advanced manufacturing services and solutions, lead design capabilities in the technologies we support in our HPS business, maintain high quality levels, deliver finished products and services on time and compete favorably on price.

Compensation, Benefits and Recognition Our compensation and benefits programs are designed to attract, retain, and motivate top talent. We offer a comprehensive package that includes competitive salaries, variable performance-based compensation, health benefits, retirement savings plans, vacation, and other paid time off. We provide opportunities for employees to share in the Company's success through short-term incentive programs available to almost all employees. These programs reward achievement of key business objectives and reinforce our commitment to a performance-driven culture. Furthermore, we offer a variety of recognition programs to acknowledge employees who are achieving business results by living our brand and values, and embracing the characteristics of our leadership imperatives. We encourage business and people leaders to acknowledge individual and team success in quarterly town halls, and in more formal ways through our global recognition programs, including Bravo! and Ignition Awards. We regularly review our compensation and benefits programs to ensure they remain competitive and aligned with our business strategy and meet the needs of our employees.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
Our operating results are highly dependent upon the ability of our customers (both our traditional OEM and hyperscaler customers) to compete and succeed in the marketplace using products we manufacture and services we provide. Factors that may adversely affect our customers include: rapid changes in technology (including evolving AI technologies); evolving industry standards; seasonal demand; their failure to successfully market, and/or a lack of widespread commercial acceptance of, their products and services; supply chain issues; the emergence of substitutes for products and services; dramatic shifts in demand which may cause them to lose market share or exit businesses; recessionary periods in our customers' markets; short product lifecycles resulting from continuous improvements in products and services, commoditization of certain products, changes in preferences by end customers, and the emergence of new entrants or competitors with disruptive products, services, or new business models. For example, competition from lower‑cost and open‑source AI models, together with rapid advances in model efficiency, may reduce user switching costs, increase price sensitivity, and limit our customers' ability to maintain or improve pricing for their AI‑related products and services.…

The recruitment of personnel in the EMS and ODM industries is highly competitive. We believe that our future success depends, in part, on our ability to attract and retain highly skilled executive, technical and management talent in the various geographies in which we operate and within desired timeframes. Competitive dynamics, as well as the time required to replace or redistribute responsibilities related to the loss of the services of certain executive, management and technical employees, individually or in the aggregate, could have a material adverse effect on our operations, and there can be no assurance that we will be able to retain their services. Regional competitive dynamics may also impact our ability to retain and acquire talent. Organizational changes may impact our relationships with customers, vendors, and employees, potentially resulting in loss of business, loss of vendor relationships, and the loss of key employees or declines in employee productivity. Uncertainties associated with any senior management transitions could lead to concerns from current and potential third parties with whom we do business, any of which could hurt our business prospects.…

We operate in a highly competitive industry. Our competitors include large global EMS companies, ODMs that specialize in providing internally-designed products and manufacturing services, smaller EMS companies that often have a regional, product, service or industry-specific focus, as well as component and sub-system suppliers, distributors and/or systems integrators. In addition, our HPS offering may compete with our traditional OEM customers' hardware offerings. Offering products or services that compete with the offerings of our customers may negatively impact our relationship with, or result in a loss of business from, such customers. We face indirect competition from current and prospective customers who decide to manufacture products internally, or in-source previously outsourced business. In addition to the foregoing, we face competition from distribution and logistics providers expanding their services across the supply chain.

The competitive environment in our industry is intense and aggressive pricing is a common business dynamic. Some of our competitors have greater scale and offer a broader range of services. Additionally, our current and/or future competitors may: be more effective than we are in increasing or shifting their presence in new lower-cost, lower-tariff or tariff-free regions to try to offset continuous competitive pressure and increasing labor costs or to secure new business; develop or acquire services comparable or superior to ours; consolidate to form larger competitors; have greater name recognition, critical mass and/or geographic market presence; have greater manufacturing, R&D and/or marketing resources; be better able to take advantage of acquisition opportunities; be willing to, or able to make sales or provide services at lower margins than we do; or adapt more quickly than we do to new technologies, evolving industry trends and changing customer requirements. In addition, our competitors may be more effective than we are in investing in IT solutions to differentiate their offerings. Some of our 27 competitors have increased their vertical capabilities by manufacturing modules or components used in the products they assemble. Although we have also expanded our capabilities, including through acquisitions and "operate-in-place" arrangements, our competitors' expansion efforts may be more successful than ours.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
