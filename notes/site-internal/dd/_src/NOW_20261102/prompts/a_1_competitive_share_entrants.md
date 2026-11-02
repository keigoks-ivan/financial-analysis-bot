你是 stock-analyst v20 DD 的證據採集子 agent。標的：NOW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - NOW ServiceNow market share gaining OR losing 2026
  - ServiceNow new entrant OR displace threat Software - Application 2026
  - NOW competitor design win 2026
  - ServiceNow vs Software - Application peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm｜as_of：2026-01-29
<<<
While competitors are actively developing AI capabilities and several entrants have emerged with point solutions focused on data analysis and information generation, we believe many face challenges in delivering the comprehensive integration, workflow orchestration, governance frameworks, and enterprise-grade reliability that our customers require to operationalize AI insights. The AI era has not eliminated—and has arguably intensified—the fundamental need for platforms that can unify disparate systems, maintain data integrity, ensure regulatory compliance, enforce business logic, and provide consistent execution across complex organizational processes.

Competition We operate in a highly competitive and rapidly evolving market characterized by fragmentation, low barriers to entry, shifting customer needs and frequent introductions of new products and services. As our business expands and the industries in which we operate continue to evolve, we compete with a broad range of solutions and alternative approaches, including: •enterprise application software vendors, both cloud-based and on-premises, such as Microsoft, Oracle, SAP, Salesforce and Workday; •new technologies and entrants, including point-solutions and platform solutions, particularly those related to AI; •custom-developed and in-house solutions; •technology consulting firms; •systems integrators; and •software resellers.

For additional information about competition, see “Risk Factors—A failure to innovate and adapt how we offer our products in response to rapidly evolving technological changes and in the midst of an intensely competitive market may harm our competitive position and business prospects.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm｜as_of：2026-01-29
<<<
We compete in markets that evolve rapidly. The pace of innovation will continue to accelerate as customers recognize the advantages of acquiring leading digital technologies and adopting AI native solutions and modern cloud-based infrastructure. Cutting-edge capabilities such as AI, machine learning, hyper automation, low-code/no-code application development, system observability and predictive insights become increasingly relevant to the customer’s evolving needs. With this rapid evolution, we are increasingly competing with alternative solutions and approaches to solve customer needs, and we expect additional competition as we shift our products and services to compete with providers in new and adjacent markets.

Competitors, regardless of their size, may be able to respond more quickly and effectively to new or changing opportunities, technologies, standards, customer requirements and buying practices. They may introduce new technology, solve similar problems in different ways or more effectively utilize existing technology that reduces demand for our services. They may utilize acquisitions, integrations or consolidations to offer integrated or bundled products, enhanced functionality or other advantages. Some of our existing competitors and potential competitors are larger and have greater name recognition, the ability to more efficiently scale their business, more established operations and customer relationships and greater financial and technical resources than we do. “Systems of record” operators may attempt to create technology solutions or other mechanisms that would prevent our systems from integrating with theirs. They may create pricing pressures by reducing the price of competing products, services or subscriptions or bundling their offerings, causing our offerings to appear relatively more expensive. Companies whose products are integrated with our Platform could also seek to compete with us by blocking, limiting or imposing fees on particular integrations or data access. Cloud-based and AI native vendors may build more business applications or AI powered automation solutions that compete with our products and services. We may also encounter customer reluctance or unwillingness to migrate away from their current solutions.

AI technology is evolving quickly. To remain competitive, we must make significant investments to continue to successfully develop and incorporate this technology into our products. Our ability to incorporate AI technology into our products depends on the availability, performance and pricing of third-party hardware and software equipment and technical infrastructure. Our competitors or other third parties may develop or incorporate AI into their products more quickly or successfully than us. They may also have or in the future obtain IP rights that would prevent, limit or interfere with our ability to make, use or sell our AI products. For these reasons, among others, we may not be able to compete effectively in the evolving AI market.

In the highly competitive technology industry, we face ongoing challenges in attracting and retaining top talent across various roles, such as product development and engineering (particularly with AI and machine learning backgrounds), sales, operations and cybersecurity. These key individual contributors are critical to our success, can command very significant compensation in the market and are actively recruited by our key competitors. Our ability to achieve significant revenue growth may depend on our success in recruiting, training and retaining sufficient qualified personnel to support our growth. We have faced and may continue to face difficulties attracting, hiring and retaining highly-skilled, qualified personnel and may not be able to fill positions in desired geographic areas or at all. Further, as we continue to grow and expand our workforce globally, we may face operational and workplace culture challenges that could negatively impact our ability to maintain the effectiveness of our business execution and the beneficial aspects of our corporate culture. While our work model, where a substantial portion of our employees work partially or fully remote, increased our access to talent, we may not be able to take advantage of a broader talent pool if our competitors offer the same work model or if we continue to rely on our primary operating locations for talent.…

Third parties may challenge or invalidate our IP rights through administrative proceedings, litigation or allowing contractual rights to expire. There is considerable patent and other IP development activity and claims and related litigation regarding patent and IP rights in our industry. Our competitors, other third parties, including practicing entities and non-practicing entities, own large numbers of patents, copyrights, trademarks and trade secrets, which they may use and have used to assert claims of infringement, misappropriation or other violations of IP rights against us. Moreover, the patent portfolios of many of our competitors and other third parties may be larger than ours. This disparity may increase the risk that our competitors or other third parties may sue us for patent infringement and may limit our ability to counterclaim for patent infringement or settle through patent cross-licenses. We have recorded material charges for legal settlements of such claims in the past. Further, upon expiration of any agreements that allow us to use third-party IP, we may be unable to renew such agreements on favorable terms, if at all, in which case we may face IP litigation or may need to cease offering or to modify our products and services to remove such components.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
