你是 stock-analyst v20 DD 的證據採集子 agent。標的：NVT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - nVent Electric product substitute technology threat 2026
  - Electrical Equipment & Parts alternative technology disruption 2026 2027
  - NVT nVent Electric technology obsolescence risk
  - Electrical Equipment & Parts next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1720635/000162828026008608/nvt-20251231.htm｜as_of：2026-02-17
<<<
We compete in various geographic regions and product markets around the world. Among these, the most significant are global infrastructure, industrial, and commercial and residential markets. We expect to experience fluctuations in revenues and results of operations due to economic and business cycles. Important factors for our business and the businesses of our customers include the overall strength of the global economy and our customers’ confidence in the economy, industrial and governmental capital spending, the strength of infrastructure and commercial and residential markets, unemployment rates, availability of commercial financing, interest rates, inflation rates, and energy and commodity prices. Recessions, economic downturns, inflation, slowing economic growth and social and political instability in the industries and/or markets where we compete could negatively affect our revenues and financial performance in future periods, result in future restructuring charges, and adversely impact our ability to grow or sustain our business. Macroeconomic and political instability caused by global supply chain disruptions, inflation and the strength of the U.S. dollar could adversely impact our results of operations. In addition, military conflicts and their impact on economies may adversely impact our results of operations. The businesses of many of our industrial customers are to varying degrees cyclical and have experienced periodic downturns.…

The markets for our products and services are geographically diverse and highly competitive. We compete against large and well-established national and global companies, as well as regional and local companies and lower-cost manufacturers. Competition may also result from new entrants into the markets we serve offering products and/or services that compete with ours. We compete based on technical expertise, reputation for quality and reliability, timeliness of delivery, previous installation history, contractual terms and price. Some of our competitors attempt to compete based primarily on price, localized expertise and local relationships. In addition, economic downturns could adversely affect pricing as market participants compete more aggressively on price. If we are unable to continue to differentiate our products, services and solutions, or if our pricing is adversely impacted or we incur additional costs to remain competitive, it could have a material adverse effect on our business, financial condition, results of operations and cash flows.

We operate in global markets that are characterized by customer demand that is often global in scope but localized in delivery. We compete with thousands of smaller regional and local companies that may be positioned to offer products produced at lower cost than ours, or to capitalize on highly localized relationships. Also, in several emerging markets potential customers prefer local suppliers, in some cases because of existing relationships and in other cases because of local legal restrictions or incentives that favor local businesses. In addition, we need to be flexible to adapt our products to ever changing customer preferences, including those relating to regulatory, sustainability and social responsibility matters. Accordingly, our future 5 success depends upon a number of factors, including our ability to adapt our products, services, organization, workforce and sales strategies to fit localities throughout the world, particularly in high-growth emerging markets; identify emerging technological and other trends in our target end markets; and develop or acquire competitive products and services and bring them to market quickly and cost-effectively. The failure to effectively adapt our products or services could have a material adverse effect on our business, financial condition, results of operations and cash flows.

A disruption in the availability, price or quality of products or materials that we manufacture and source from various countries throughout the world could have a material adverse effect on our results of operations.

Our business is subject to risks associated with global manufacturing and sourcing. We use a variety of raw materials in the production of our products including steel, copper, aluminum and paints. We also purchase certain electronic components, electrical and packaging materials from a number of suppliers. Although we regularly monitor the financial health and operations of companies in our supply chain, and use alternative suppliers when necessary and available, supply chain constraints could cause a disruption in our ability to obtain raw materials or components required to manufacture our products and adversely affect our operations. Significant shortages in the availability of these materials or price increases could increase our operating costs and adversely impact the competitive positions of our products. We rely on materials, components and finished goods that are sourced from or manufactured in locations outside the U.S., including Mexico, China and other countries, and these countries may experience political or trade instability, which could disrupt our supply of products or 6 materials. We rely on our suppliers to produce high quality materials, components and finished goods according to our specifications. Although we have quality control procedures in place, there is a risk that products may not meet our specifications which could impact our ability to ship quality products to our customers on a timely basis.

Cybersecurity threats from user error to attacks designed to gain unauthorized access to our systems, networks and data are increasing in frequency and sophistication, including the risk that threat actors will leverage emerging technology, such as artificial intelligence, to exploit vulnerabilities. These threats pose a risk to the security of our systems and networks and the confidentiality, availability and integrity of the data we process and maintain and pose a risk of theft to our assets. The risk of cybersecurity attacks may increase as artificial intelligence capabilities improve and are increasingly used to identify vulnerabilities and construct increasingly sophisticated cybersecurity attacks, with the possibility of additional vulnerabilities being introduced through our own use of artificial intelligence and its use by our stakeholders, including vendors and customers. Establishing systems and processes to address these threats and changes in legal requirements relating to data collection and storage may increase our costs. Previous cybersecurity incidents have not materially affected us, including our business strategy, results of operations or financial condition. There can be no assurance of similar results in the future.…

The rapid evolution of artificial intelligence technologies, together with emerging and potentially divergent governmental regulations and industry standards, may require ongoing investment in governance, monitoring, data security, training and compliance. Failure to appropriately develop, manage, secure and oversee our artificial intelligence activities could expose us to legal liability, operational disruptions, reputational harm and other adverse effects on our business and results of operations.

Disruptions in the financial markets could adversely affect us, our customers and our suppliers by increasing funding costs or reducing availability of credit.

In the normal course of our business, we may access credit markets for general corporate purposes, which may include repayment of indebtedness, acquisitions, additions to working capital, repurchase of shares and capital expenditures. Although we expect to have sufficient liquidity to meet our foreseeable needs, our access to and the cost of capital could be negatively impacted by disruptions in the credit markets, which have occurred in the past and made financing terms for borrowers unattractive or unavailable. These factors may make it more difficult or expensive for us to access credit markets if the need arises. In addition, these factors may make it more difficult for our suppliers to meet demand for their products or for prospective customers to commence new projects, as customers and suppliers may experience increased costs of debt financing or difficulties in obtaining debt financing. Disruptions in the financial markets in the past have had adverse effects on other areas of the economy and have led to a slowdown in general economic activity that may adversely affect our businesses. One or more of these factors could adversely affect our business, financial condition, results of operations and cash flows.

Catastrophic and other events beyond our control may disrupt operations at our manufacturing facilities and those of our suppliers, which could cause us to be unable to meet customer demands or increase our costs or reduce customer spending.

If operations at any of our manufacturing facilities or those of our suppliers were to be disrupted as a result of significant equipment failures, natural disasters, earthquakes, power outages, fires, explosions, terrorism, military conflicts, international hostilities, cybersecurity incidents, adverse weather conditions, labor disputes, public health epidemics or other catastrophic events or events outside of our control, we may be unable to fill customer orders and otherwise meet customer demand for our products. In addition, these types of events may negatively impact consumer, commercial and industrial spending in impacted regions or, depending on the severity, globally. As a result, any of such events could have a material adverse effect on our business, financial condition, results of operations and cash flows. Interruptions in production, in particular at our manufacturing facilities, could increase our costs and reduce our sales. Any interruption in production capability could require us to make substantial capital expenditures to fill customer orders. We maintain property damage insurance that we believe to be adequate to provide for reconstruction of facilities and equipment, as well as business interruption insurance to mitigate losses resulting from any production interruption or shutdown caused by an insured loss.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
