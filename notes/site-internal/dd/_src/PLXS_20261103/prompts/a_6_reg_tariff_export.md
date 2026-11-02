你是 stock-analyst v20 DD 的證據採集子 agent。標的：PLXS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - PLXS Plexus tariff section 232 2026
  - Plexus export control OR entity list Electronics Manufacturing Services / Healthcare / Defense 2026
  - PLXS Plexus China tariff OR trade restriction 2026
  - Electronics Manufacturing Services / Healthcare / Defense tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/785786/000078578625000064/plxs-20250927.htm｜as_of：2025-11-14
<<<
In addition, we focus our sales efforts on customers in only a few market sectors, as identified in Part I, Item 1, herein. Each of these sectors is subject to macroeconomic conditions as well as trends and conditions that are sector specific. Any weakness in our customers’ end markets, or new entrants in those markets that compete with our customers, could affect our business and results of operations. Economic, business or regulatory conditions that affect the sector, or our failure to choose to do business in appropriate sectors or subsectors, can particularly impact us. For instance, sales in the Healthcare/Life Sciences sector are substantially affected by trends in the healthcare industry, such as government reimbursement rates and uncertainties relating to the U.S. healthcare sector generally. In addition, the Healthcare/Life Sciences sector is affected by health crises and trends. The semiconductor industry has historically been subject to significant cyclicality and volatility. Changing export regulations, increasing sanctions or other trade barriers may limit our ability to use or produce certain technologies or products in China or sell certain components or products that are ultimately destined to China. Further, potential reductions in government agency spending, including those due to budget cuts or other political developments or issues, could affect opportunities in all of our market sectors.

We and our customers are subject to extensive government regulation, legal requirements and industry standards (as well as customer-specific standards) relating to the products we design, manufacture and service as well as how we conduct our business. This includes regulations and standards relating to labor and employment practices, workplace health and safety, operating practices and quality systems, the environment, sourcing and global trade practices including tariffs, usage of emerging technologies, data privacy and protection, ethics, financial reporting, the market sectors we support and many other facets of our operations. The regulatory climate in the U.S. and other countries has become increasingly complex and dynamic, and regulatory enforcement activity has increased in recent periods. Rulings of the U.S. Supreme Court and other courts may affect the regulatory environment. Regulatory changes and restrictions can be announced with little or no advance notice. A failure to comply with laws, regulations or standards applicable to our business can result in, among other consequences, enforcement actions, fines, injunctions, civil penalties, criminal prosecution, recall or seizure of devices, total or partial suspension of production, including debarment, and could have an adverse effect on our reputation, customer relationships, profitability and results of operations.

•changes in labor markets, such as government-mandated wage increases, increases to minimum wage requirements, changes in union-related laws, regulations or practices, limitations on immigration or the free movement of labor or restrictions on the use of migrant workers, and difficulties in appropriately staffing and managing personnel in diverse cultures and increased public scrutiny on labor practices •customers shifting parts of their manufacturing and supply chains to different countries, including re-shoring, which may impact footprint needs and create operational disruption due to transition efforts •compliance with laws, such as the U.S. Foreign Corrupt Practices Act, the U.K. Bribery Act and the European Union’s (EU's) General Data Protection Regulation (the “GDPR”), applicable to companies with global operations •changing global trade regulations, particularly relating to advanced semiconductors and chip-manufacturing equipment, which may limit the ability to ship certain components or product to customers in China, support certain programs in our China operations, and source the components necessary to manufacture customer product in China •changes in the taxation of earnings in the U.S.…

Changes in policies or trade agreements by or changes in elected officials of the U.S. or other governments could negatively affect our operating results due to trade wars, changes in duties, tariffs or taxes, currency exchange rate fluctuations, higher costs of compliance, or limitations on currency or fund transfers, as well as government-imposed restrictions on producing certain products in, or shipping them to, specific countries. Our current facilities in Mexico operate under the Mexican Maquiladora (“IMMEX”) program. This program provides for reduced tariffs and eased import regulations. We could be adversely affected by changes in the IMMEX program or our failure to comply with its requirements.

Additionally, continued uncertainty regarding commercial dealings, tariffs, export regulations and other trade protection measures between the U.S. and countries globally, heightened by escalating geopolitical tensions, may affect our ability to do 13 Table of Contents business in certain countries, may impact the cost of our services and products originating from certain countries, and may impact the demand for our services. These actions could also affect the cost and/or availability of materials or components that we procure from suppliers, as well as create disruptions, delays, shortages or increased costs within our global supply chain. Government-imposed restrictions on where we or our customers can produce certain types of products or source components or with whom we can conduct business, outbound investment restrictions, and trade regulations limiting advanced semiconductors and chip-manufacturing equipment, could limit our ability to sell or manufacture products or services, or source components from certain companies or geographies. These factors can negatively affect our operating results and financial position, including reducing our revenues and profitability as a result of having to minimize engagements in certain countries, requiring us to shift such production to other potentially higher-cost locations, increasing the cost of sourcing components, or the loss of business.…

We generally do not have long-term supply agreements. We have experienced from time to time, and may in the future experience, significant component shortages and longer lead-times due to supplier capacity constraints. Supply chain constraints and delays can be caused by world events, such as government policies, tariffs, trade wars, trade disputes and trade protection measures, terrorism, armed conflict, natural disasters, natural resource availability, economic recession, increased demand due to economic growth or technological advancements, preferential allocations, transportation challenges, and other localized events. Further, we rely on a limited number of suppliers for many of the components used in the assembly process and, in some cases, may be required to use suppliers that are the sole provider of a particular component. Such suppliers may encounter quality problems, labor disputes or shortages, financial difficulties or business continuity issues that could preclude them from delivering components timely or at all. Supply shortages and delays in deliveries of components may result in delayed manufacturing or servicing of products, which reduces our revenue and operating profit for the periods affected. Additionally, a delay in obtaining a particular component may result in other components for the related program being held for longer periods of time, increasing working capital, risking inventory obsolescence and negatively impacting our cash flow.

Component supply shortages and delays in deliveries, along with other factors such as tariffs, trade disputes or embargoes, inflation, and rising energy and transportation costs, can also result in increased pricing. While many of our customers permit quarterly or other periodic adjustments to pricing based on changes in component prices and other factors, we have in the past and may continue to bear the risk of price increases that occur between any such repricing or, if such repricing is not permitted, during the balance of the term of the particular customer contract. In addition, these repricing or pricing recoveries have been and may continue to be dilutive to our operating margin. Conversely, as a result of our pricing strategies and practices, component price reductions have contributed positively to our operating results in the past. Our inability to continue to benefit from such reductions in the future could adversely affect our operating results, cash flows and inventory levels, which could increase as a result of higher component prices or the negative effects of inflation on customer end-market demand.

Moreover, we are subject to increasing data privacy, handling, and protection requirements and customer expectations due to the nature of their end products, including those related to the Export Administration Regulations, International Traffic in Arms Regulation, Federal Acquisition Regulation, Defense Federal Acquisition Regulation Supplement and Cybersecurity Maturity Model Certification. Any operational failure or breach of security from increasingly sophisticated cyber threats could lead to the loss or disclosure of our or our customers’ financial, product or other confidential information, result in adverse regulatory or other legal actions and have a material adverse effect on our business and reputation, which could include the loss of programs or customers. In addition, we must comply with increasingly complex and rigorous regulatory standards enacted to protect business and personal data, globally. GDPR and similar legislation in jurisdictions in which we operate continue to evolve imposing additional obligations on companies regarding the handling and protection of personal data and provide certain individual privacy rights to persons whose data is processed and stored. Compliance with existing, proposed and recently enacted laws and regulations can be costly. Failure to comply with these regulatory standards could subject us to legal and reputational risks.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
