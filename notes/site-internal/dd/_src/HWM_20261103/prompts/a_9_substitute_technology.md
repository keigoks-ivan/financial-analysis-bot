你是 stock-analyst v20 DD 的證據採集子 agent。標的：HWM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Howmet Aerospace product substitute technology threat 2026
  - Aerospace & Defense alternative technology disruption 2026 2027
  - HWM Howmet Aerospace technology obsolescence risk
  - Aerospace & Defense next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/4281/000000428126000012/hwm-20251231.htm｜as_of：2026-02-12
<<<
9 Table of Contents Howmet is unable to predict the future course of industry variables, the strength of the U.S., regional or global economies, or the effects of government actions. Negative economic conditions, such as a major economic downturn or recession, continued inflation, changes in the global trade landscape or disruptions in the financial markets, could have a material adverse effect on Howmet’s business, financial condition, or results of operations.

A material disruption of, or manufacturing difficulties at, Howmet’s manufacturing operations could adversely affect Howmet’s business.

If Howmet’s operations, particularly at one of its key manufacturing facilities, were to be disrupted, including because of significant equipment failures, natural disasters, power outages, fires, explosions, terrorism, violence, theft, sabotage, adverse weather conditions, public health crises, labor disputes, labor shortages, or other reasons, Howmet may be unable to effectively meet its obligations to, or demand from, its customers. In addition, the manufacture of many of Howmet’s products is a complex process. Manufacturing problems arising from equipment failure or malfunction, inadvertent failure to follow regulatory or customer specifications and procedures, including those related to quality or safety, and problems with raw materials could have an adverse impact on the Company’s ability to fulfill orders or meet product quality or performance requirements, which may result in negative publicity and damage to our reputation, adversely impacting product demand and customer relationships. Interruptions in production capability could increase Howmet’s costs and reduce its sales, including causing the Company to incur costs for premium freight, make substantial capital expenditures, or purchase alternative material at higher costs to fulfill customer orders. Additionally, a delivery delay by us due to production interruptions could subject us to liability from customer claims that such delay resulted in losses to the customer.…

Howmet is dependent on a limited number of suppliers for materials and services essential to our operations, including raw materials, and supply chain disruptions could have a material adverse effect on our business.

Howmet has supply arrangements with suppliers for various materials and services, including raw materials. We maintain annual or long-term contracts for a majority of our supply requirements, and, for the remainder, we depend on spot purchases. There can be no assurance that we will be able to renew, or obtain replacements for, any of our long-term contracts when they expire on terms that are as favorable as our existing agreements, or at all. For certain raw materials and services, we depend on a number of limited source or sole source suppliers, such as for titanium sponge and specialized metal alloys. Supply constraints could impact our production or force us to purchase materials and other supplies from alternative sources, which may not be available in sufficient quantities, at prices that are favorable to us or in a timely manner. Howmet could also have exposure if a key supplier is unable to deliver sufficient quantities of a necessary material on a timely basis. Several of our suppliers have had, in the past, constraints on their ability to supply Howmet with its full requirements due to lack of capacity, labor shortages and/or material availability. If such constraints were to continue or escalate, it could result in an adverse impact on our business.…

Information technology system failures, cyberattacks, and security breaches may threaten the integrity of Howmet’s intellectual property and other sensitive information, disrupt its business operations, and result in reputational harm and other negative consequences having a material adverse effect on its financial condition and results of operations.

Howmet’s information technology systems could be subject to damage or interruption from power outages; computer network and telecommunications failures; cyberattacks; catastrophic events such as fires, floods, earthquakes, tornadoes, hurricanes, acts of war, or terrorism; and usage errors by employees. If Howmet’s information technology systems are damaged or cease to function properly, the Company may have to make a significant investment to fix or replace them, and Howmet may suffer loss of critical data and interruptions or delays in its operations. Any material disruption in the Company’s information technology systems, or delays or difficulties in implementing or integrating new systems or enhancing current systems, could have an adverse effect on Howmet’s business, financial condition, or results of operations.

While the Company continually works to safeguard its systems and mitigate potential risks, there is no assurance that such actions will be sufficient to prevent cybersecurity incidents that manipulate or improperly use the Company’s systems or networks, compromise confidential, personal or otherwise protected information, destroy or corrupt data, block access to its systems, or otherwise disrupt its operations. The occurrence of such events could negatively impact Howmet’s reputation and its competitive position and could result in litigation with third parties, regulatory action, loss of business, potential liability, and increased remediation costs, any of which could have a material adverse effect on its financial condition and results of operations.

As discussed in “Competitive Conditions” in Part I, Item 1 (Business) of this report, the markets for Howmet’s products are highly competitive. Howmet’s competitors include a variety of both U.S. and non-U.S. companies in our product markets, which could include existing customers. New entrants in our markets, new product offerings, new and/or emerging technologies in the marketplace, or new facilities may compete with or replace Howmet products. The willingness of customers to accept alternative solutions for the products sold by Howmet, pricing pressure from competitors, and technological advancements or other developments, including the use of AI, by or affecting Howmet’s competitors or customers could adversely affect Howmet’s business, financial condition, or results of operations. Howmet’s competitive position and future performance depend, in part, on the Company’s ability to develop and innovate products, deploy technology initiatives, and implement advanced manufacturing technologies, including through the use of new and evolving technologies, including AI. The Company's competitors may adopt new technological initiatives and implement technological advancements using AI to pursue new or improved products and services more quickly, profitably, successfully and effectively than the Company.…

In addition to the Proposed CAM Acquisition, Howmet may continue to pursue other acquisitions and take other strategic actions to grow or streamline its portfolio. There can be no assurance that we will be able to execute upon any such acquisitions or strategic actions, or that any anticipated benefits of such acquisitions or actions will be realized. Acquisitions, including the planned Proposed CAM Acquisition, present significant operational challenges and risks, including the effective integration of the business into the Company, which may be more difficult, time consuming or more costly than expected and may divert management attention from the Company’s existing business. Acquisitions, including the Proposed CAM Acquisition, may increase operating costs, expose the Company to potential unforeseen issues and legal liabilities, including the assumption of liabilities (including unforeseen liabilities) of acquired companies or businesses, increase cybersecurity issues or vulnerabilities or result in customer loss and business disruption (including, without limitation, difficulties in retaining or maintaining relationships with employees, customers or suppliers). Any of the foregoing may adversely affect Howmet’s business, financial condition, or results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HWM_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
