你是 stock-analyst v20 DD 的證據採集子 agent。標的：TWLO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - TWLO Twilio market share gaining OR losing 2026
  - Twilio new entrant OR displace threat Software - Infrastructure 2026
  - TWLO competitor design win 2026
  - Twilio vs Software - Infrastructure peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm｜as_of：2026-02-24
<<<
•Efficient Go-to-Market Execution. We are focused on improving profitability and growing our market share. To achieve this, we are focused on bolstering our independent software vendor (“ISV”) and other partner relationships, improving our self-service capabilities, cross-selling our products, and expanding internationally.

Competition The markets for our products are rapidly evolving and are increasingly competitive. Our competitors are primarily (i) communications platform-as-a-service (“CPaaS”) companies that offer communications products and applications, (ii) regional network service providers that offer limited developer functionality on top of their own physical infrastructure, (iii) customer relationship management and customer experience vendors, (iv) standalone customer data platform vendors and (v) other software companies that compete with portions of our product line.

The principal competitive factors in these markets include completeness of offering, credibility with customers, ability to differentiate our products against competing offerings, global reach, ease of integration and programmability, product features, platform scalability, reliability, deliverability, security and performance, brand awareness and reputation, the strength of sales and marketing efforts, customer support, and the cost of deploying and using products.

We believe that we compete favorably on the basis of the factors listed above and that none of our competitors currently compete directly with us across all of our product offerings. With the introduction of new products and services and new market entrants, we expect competition to intensify in the future.

We are committed to delivering a comprehensive compensation and benefits program that provides support for all of our employees’ well-being. We provide competitive compensation to attract and retain talented employees, including market-competitive pay, incentive compensation in the form of bonuses or sales commissions, and equity compensation for certain employees. In addition, we offer competitive benefits packages to our full-time employees, subject to the satisfaction of certain eligibility requirements, that are aligned with industry standards and local market practices in each of the countries in which we operate. We ensure that our compensation is fair for all employees, regardless of background. We routinely run a rigorous statistical analysis to ensure compensation is fair, taking into account factors that should impact pay, like role, level, location, and performance. Twilio is an equal opportunity employer, and we are committed to ensuring that Twilio is an inclusive workplace where everyone, regardless of background, is treated fairly and has access to the opportunities, systems, and resources to do their best work.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm｜as_of：2026-02-24
<<<
The current and prospective markets for our products are rapidly evolving, significantly fragmented and highly competitive, in some cases with relatively low barriers to entry, and may fail to grow as expected or decline over time. The principal competitive factors of these markets include completeness of offering, credibility with customers, ability to differentiate our products against competing offerings, global reach, ease of integration and programmability, product features, platform scalability, reliability, deliverability, security and performance, brand awareness and reputation, the strength of sales and marketing efforts, customer support, and the cost of deploying and using products, as well as our customers’ perception of the value and necessity of our products and platform. Our competitors are primarily (i) CPaaS companies that offer communications products and applications, (ii) regional network service providers that offer limited developer functionality on top of their own physical infrastructure, (iii) customer relationship management and customer experience vendors, (iv) standalone customer data platform vendors and (v) other software companies that compete with portions of our product line.

Some of our competitors and potential competitors are larger and have greater name recognition, longer operating histories, more established customer relationships, larger budgets, lower operating costs, and significantly greater resources than we do. As a result, our competitors may be able to respond more quickly and effectively than we can to new or changing opportunities, technologies, standards, customer requirements or changing economic conditions. Our competitors may also offer products or services that address one or a limited number of functions at lower prices, with greater depth than our products or in different geographies. Our current and potential competitors have in the past and may in the future develop and market products and services with comparable functionality to our products, and this could lead us to decrease prices in order to remain competitive. In addition, customers may reduce or delay spending on our products or substitute alternative solutions in response to pricing pressures, budget constraints or changing business priorities.

With the introduction of new products and services and new market entrants, we expect competition to intensify in the future. Industry developments and evolving technology, such as AI, may also impact our competitive landscape and the factors required to compete effectively in current or prospective markets. Our ability to grow will depend in part on our success in expanding the scope of our products and entering new markets, and there can be no assurance that the markets will grow or that our products will achieve meaningful adoption within them. As we expand the scope of our products, we may face additional competition and, in some cases, may find our products in competition with those of our customers, which could cause them to replace our products with competitive offerings. If one or more of our competitors were to merge or partner with another of our competitors or our suppliers, the change in the competitive landscape could also adversely affect our ability to compete effectively. For example, certain of our competitors have engaged in acquisition activity, and we expect that our competitors will continue to evaluate the acquisition of companies and technologies that could increase competition with our products in the future.…

We believe that maintaining and enhancing our brand identity and increasing market awareness of our company and products, particularly among developers and enterprises, is critical to achieving widespread acceptance of our platform, to strengthening our relationships with our existing customers and to our ability to attract new customers. The successful promotion of our brand will depend largely on our continued marketing efforts, our ability to continue to offer high-quality products, and our ability to successfully differentiate our products and platform from competing products and services. Our brand promotion and thought leadership activities may not be successful or yield increased revenue. In addition, independent industry analysts often provide reviews of our products and competing products and services, which may significantly influence the perception of our products in the marketplace. If these reviews are negative or not as strong as reviews of our competitors’ products and services, then our brand may be harmed.

We have deployed, and continue to develop and incorporate, AI solutions and features in our platform and our business, and these solutions and features may become more important to our operations, future growth or competitiveness over time. We expect to rely on AI solutions and features to help drive future growth and efficiency in our business, but there can be no assurance that we will realize the desired or anticipated benefits from AI in a timely or cost-effective manner. For example, we 26 Table of Contents are focused on continued product innovations to combine our communications products with contextual data and AI. We are also building out new AI capabilities internally, including AI automation and agents in our self-service platform and in our internal operations. We may also fail to properly implement or market our AI solutions and features. Our competitors or other third parties may incorporate AI into their products, offerings, and solutions more quickly or more successfully than us, which could impair our ability to compete effectively and adversely affect our results of operations.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TWLO_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
