你是 stock-analyst v20 DD 的證據採集子 agent。標的：IBM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - IBM market share gaining OR losing 2026
  - new entrant OR displace threat 2026
  - IBM competitor design win 2026
  - vs peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231.htm｜as_of：2026-02-24
<<<
Competition IBM is a globally integrated enterprise that participates in a highly competitive environment. Our competitors vary by industry segment, and range from large multinational enterprises to smaller, more narrowly focused entities. Across our business segments, we recognize hundreds of competitors worldwide and as we execute our hybrid cloud and AI strategy, we are regularly exposed to new competitors.

1 Table of Contents Overall, the company is the leader or among the leaders in each of our business segments. A summary of the competitive environment for each business segment is included below: Software: The depth, breadth, and innovation of our software offerings, coupled with our global reach, deep industry expertise and research capabilities help differentiate our offerings from our competitors. Our hybrid cloud and AI platforms allow clients to realize their digital and AI transformations across the applications, data, and environments in which they operate. The principal competitors in this segment include: Alphabet (Google), Amazon, BMC, Broadcom, Microsoft, Oracle, Salesforce, SAP and Splunk, a CISCO Company. We also compete with smaller, niche competitors in specific geographic regions or product segments.

Consulting: Consulting integrates strategy, experience design, technology and operations expertise by domain across industries to deliver transformation for clients. Consulting operates in a highly competitive, dynamic market that spans business consulting, systems integration, application development and management, and business process outsourcing services. Our competitors include global firms such as Accenture, Capgemini, India-based service providers, management consulting firms, the consulting practices of public accounting firms, engineering service providers, and niche specialists. Our competitive position is supported by industry expertise; hybrid cloud, data, and AI capabilities; and the use of IBM technology and ecosystem partners to deliver solutions aligned to clients’ strategic priorities.

Infrastructure: IBM is well positioned in the growing hybrid cloud infrastructure market, providing on-premises and cloud-based server and storage solutions. We gain advantage and differentiation through investments in higher-value capabilities, including security, scalability, and reliability, designed especially for mission-critical and AI workloads. In addition, we offer a portfolio of life-cycle services for hybrid cloud infrastructure deployment. Our principal competitors include: Dell Technologies, Hewlett-Packard Enterprise (HPE), Intel, NetApp and Pure Storage as well as original device manufacturers (ODMs) who provide systems that are re-branded. Further, cloud service providers are leveraging innovation in technology and service delivery to compete with traditional providers and to offer additional routes to market for server and storage systems.

Financing: Financing provides client and commercial financing, facilitating IBM clients’ acquisition of hardware, software and services. Financing’s ability to manage credit and residual value risk generates a competitive advantage for the company. The key competitive factors include: interest rates charged, IT product experience, client service, contract flexibility, ease of doing business, global capabilities and residual values. In client and commercial financing, Financing primarily competes with non-captive financing entities and financial institutions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231.htm｜as_of：2026-02-24
<<<
Failure of Innovation Initiatives Could Impact the Long-Term Success of the Company: IBM has moved into areas, including those that incorporate or utilize hybrid cloud, AI, quantum and other disruptive technologies, in which it can differentiate itself through responsible innovation, by leveraging its investments in R&D and attracting a successful developer ecosystem. If IBM is unable to continue its cutting-edge innovation in a highly competitive and rapidly evolving environment or is unable to commercialize such innovations, expand and scale them with sufficient speed and versatility or is unable to attract a successful developer ecosystem, the company could fail in its ongoing efforts to maintain and increase its market share and its profit margins.

Risks from Investing in Growth Opportunities Could Impact the Company’s Business: The company continues to invest significantly in key strategic areas, including AI, to drive revenue growth and market share gains. Client adoption rates and viable economic models are less certain in the high-value, highly competitive, and rapidly-growing segments. Additionally, emerging business and delivery models may unfavorably impact demand and profitability for our other products or services. If the company does not adequately and timely anticipate and respond to changes in customer and market preferences, competitive actions, disruptive technologies, emerging business models and ecosystems, the client demand for our products or services may decline or IBM’s costs may increase.

The Company’s Financial Results for Particular Periods Are Difficult to Predict: IBM’s revenues and profitability are affected by such factors as the introduction of new products and services, the ability to compete effectively in increasingly competitive marketplaces, the length of the sales cycles and the seasonality of technology purchases. In addition, certain of the company’s growth areas involve new products, new customers, new and evolving competitors, and new markets, all of which contribute to the difficulty of predicting the company’s financial results. The company’s financial results may also be impacted by the structure of products and services contracts and the nature of its customers’ businesses; for example, certain of the company’s services contracts with commercial customers in regulated industries are subject to periodic review by regulators with respect to controls and processes. Further, general economic conditions, including sudden shifts in regional or global economic activity may impact the company’s financial results in any particular period. As a result of the above-mentioned factors, the company’s financial results are difficult to predict. Historically, the company has had lower revenue in the first quarter than in the immediately preceding fourth quarter.…

The Company Depends on Skilled Employees and Could Be Impacted by a Shortage of Critical Skills: Much of the future success of the company depends on the continued service, availability and integrity of skilled employees, including technical, marketing and staff resources. Skilled and experienced personnel in the areas where the company competes are in high demand, and competition for their talents is intense. Changing demographics and labor work force trends may result in a shortage of or insufficient knowledge and skills. In addition, as global opportunities and industry demand shifts, realignment, training and scaling of skilled resources may not be sufficiently rapid or successful. Further, many of IBM’s 5 Table of Contents key employees receive a total compensation package that includes equity awards. Any new regulations, volatility in the stock market and other factors could diminish the company’s use or the value of the company’s equity awards, putting the company at a competitive disadvantage.

The Development and Use of AI, including the Company’s Increased AI Solutions and Use of AI Technologies, Could Impact the Long-Term Success of the Company and its Reputation or Give Rise to Legal or Regulatory Action: IBM is increasingly applying AI technologies to its services and products, to how it delivers solutions to IBM clients, and to its own internal operations. Additionally, IBM is investing in and offering new products and services associated with AI development, deployment, governance, and management. As stated more comprehensively and in context of several risk factors throughout this Item 1A., if the company does not continue to be recognized as an AI leader with strong governance processes or if our AI technologies do not work as intended or produce unexpected outcomes, IBM’s ongoing efforts to maintain and increase its market share and its profit margins, its reputation, and its competitiveness could be harmed. Further, IBM’s drive for greater agility, productivity, flexibility and cost savings by continuously transforming with the use of AI may not yield intended gains in speed, quality, productivity and enablement of rapid scaling. The evolving global AI regulatory and legal environment may affect the company’s business and the company’s overall results of operations.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
