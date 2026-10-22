你是 stock-analyst v20 DD 的證據採集子 agent。標的：MMM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - 3M product substitute technology threat 2026
  - Conglomerates alternative technology disruption 2026 2027
  - MMM 3M technology obsolescence risk
  - Conglomerates next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/66740/000006674026000014/mmm-20251231.htm｜as_of：2026-02-03
<<<
During 2025, the Company derived approximately 56 percent of its revenues from outside the United States. Accordingly, the Company’s operations and the execution of its business strategies and plans are subject to global competition and economic and geopolitical risks that are beyond its control, such as, among other things, disruptions in financial markets, economic downturns, military conflicts, terrorism, public health emergencies, political changes and trends such as protectionism, economic nationalism resulting in government actions impacting international trade agreements or imposing trade restrictions such as tariffs and retaliatory counter measures, and government deficit reduction and other austerity measures in locations or industries in which the Company operates. Further escalation of specific trade tensions, including those between the U.S. and China, or more broadly in global trade conflict, could have a material adverse effect on the Company's business and operations around the world. The Company's business is also impacted by social, political, and labor conditions in locations in which the Company or its suppliers or customers operate; adverse changes in the availability and cost of capital; monetary policy; interest rates; inflation; recession; commodity prices; currency volatility or exchange control; ability to expatriate earnings; and other laws and regulations in the jurisdictions in which the Company or its suppliers or customers operate.…

The global economy has been impacted by geopolitical tensions. The U.S. and other governments have imposed, and propose to impose additional, export controls and tariffs on certain products, and financial and economic sanctions on certain industry sectors and parties. These geopolitical tensions could result in, among other things, cyberattacks, supply chain disruptions (including limitations on access to rare earth minerals and other raw materials), higher energy and other commodity costs, lower consumer demand, and changes to foreign exchange rates and financial markets, and tariffs and trade restrictions may result in increased production costs and product pricing, further supply chain disruptions, limited access to end markets, lower profitability, and uncertainty related to planning long-term investments and strategies, and may have other competitive effects. Compliance with rapidly changing tariffs and trade restrictions may require significant time and resources, and in turn increase our cost of doing business, and could result in fines and penalties or reputational harm if we are found to not be in compliance. Any of the foregoing could have a material adverse effect on the Company’s business, financial condition, and results of operations.

3M announced in December 2022 it would take two further actions with respect to PFAS (2022 PFAS Announcement): exiting all PFAS manufacturing by the end of 2025, and working to discontinue the use of PFAS across its product portfolio by the end of 2025. 3M completed its exit of PFAS manufacturing at the end of 2025. 3M will continue to take actions to address PFAS manufactured prior to the exit. For example, the Company's water treatment assets at facilities that manufactured PFAS will continue to treat PFAS from historical manufacturing activities and remediate residual PFAS in waste streams from the Company's operations. 3M also will continue to work through the disposition of its assets and its interests in manufacturing facilities, which may include dismantling, cleaning and repurposing, and other dispositions of facilities or equipment. 3M remains in ongoing discussions with customers, government authorities, and other stakeholders and interested parties about customer agreements and the Company's interests in assets and facilities, which may be owned or leased from other parties that have interests and rights related to those facilities. The Company recognized a $0.8 billion pre-tax charge in the fourth quarter of 2022 associated with the 2022 PFAS Announcement related to asset impairments, and will incur additional expenses in connection with the 2022 PFAS Announcement.…

Demand for the Company’s products, which impacts revenue and profit margins, is affected by, among other things: (i) the development and timing of the introduction of competitive products; (ii) the Company’s pricing strategies; (iii) changes in customer order patterns, such as changes in the levels of inventory maintained by customers, vendors, or channel partners; (iv) changes in customers’ preferences for our products, including preferences for products that do not contain third-party manufactured PFAS, the success of products offered by our competitors, and changes in customer designs for their products that can affect the demand for some of the Company’s products; and (v) changes in the business environment related to disruptive technologies, such as artificial intelligence and machine learning technologies, block-chain, expanded analytics, and other enhanced learnings from increasing volume of available data.…

* The Company’s future results are subject to vulnerability with respect to materials and fluctuations in the costs and availability of purchased components, compounds, raw materials, energy, and labor due to shortages, increased demand and wages, strikes or other labor disruptions, logistics, supply chain interruptions, manufacturing site disruptions, regulatory developments, natural disasters, and other disruptive factors.

The Company depends on various components, compounds, raw materials, and energy (including oil and natural gas and their derivatives) supplied by others for the manufacturing of its products. Supplier relationships have been and could be interrupted or terminated in the future due to events such as supplier material shortages, climate impacts and severe weather events, natural and other disasters, and other disruptive events such as those noted in the first risk factor above. In addition, some of our suppliers are limited- or sole-source suppliers, and our ability to meet our obligations to customers depends on the performance, product quality, and stability of such suppliers and the Company's ability to source adequate alternatives in a cost-effective manner. Any sustained interruption in the Company’s receipt of adequate supplies, supply chain disruptions impacting the distribution of products, or disruption to key manufacturing sites’ operations due to natural and other disasters or events, such as government actions relating to discharge or emission permits, strikes or other labor disruptions, or other legal or regulatory requirements, could have a material adverse effect on the Company and its ability to fulfill supply obligations to its customers.…

14 Table of Contents Risks Related to Our Business * The Company employs information including operational technology systems to support its business and to collect, store, and/or use proprietary and confidential information, including ongoing phased implementation of an enterprise resource planning (ERP) system as part of its business transformation on a worldwide basis over the next several years. Network disruptions, security and data breaches, cyberattacks, and other cybersecurity incidents involving the Company’s information technology systems, networks and infrastructure could: disrupt or interfere with the Company’s operations; result in the compromise and misappropriation of proprietary and confidential information belonging to the Company or its customers, suppliers, and employees; and expose the Company to numerous expenses, liabilities, and other negative consequences, any or all of which could have a material adverse effect on the Company’s business, reputation, and results of operations.

In the ordinary course of business, the Company relies on centralized and local information technology networks and systems, some of which are provided, hosted, or managed by vendors and other third parties, to process, transmit, and store electronic information, and to manage or support a variety of businesses. Additionally, the Company collects and stores certain data, including proprietary business information, and has access to confidential or personal information in certain of our businesses that is subject to artificial intelligence, privacy and cybersecurity laws, regulations, and customer-imposed controls. Third parties and threat actors, including organized criminals, nation-state entities, and/or nation-state supported actors, regularly attempt to gain unauthorized access to the Company’s information and operational technology networks and infrastructure, data, and other information, and many such attempts are becoming increasingly sophisticated. Despite our cybersecurity and business continuity counter measures (including employee and third-party training, monitoring of networks and systems, patching, maintenance, and backup of systems and data), the Company’s information and operational technology systems, networks and infrastructure have experienced and are expected to experience cyberattacks of various degrees of sophistication, and are susceptible to insider threat, compromise, damage, disruption, or shutdown, including as a result of the exploitation of known or unknown hardware or software vulnerabilities, or zero day attacks, in our systems or the systems of our vendors and third-party service…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MMM_20261022/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
