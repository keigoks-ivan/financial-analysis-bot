你是 stock-analyst v20 DD 的證據採集子 agent。標的：PH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Parker-Hannifin product substitute technology threat 2026
  - Specialty Industrial Machinery alternative technology disruption 2026 2027
  - PH Parker-Hannifin technology obsolescence risk
  - Specialty Industrial Machinery next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-21）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm｜as_of：2026-08-21
<<<
Energy Matters and Sources and Availability of Raw Materials Our primary energy source for both of our business segments is electric power. While we cannot predict future costs of electric power, we manage this cost through aggregation in deregulated markets and leveraging contracts with established pricing on portions of our energy load. We are subject to governmental regulations in regard to energy supplies in the United States and elsewhere. To date, we have not experienced any significant disruptions of our operations due to energy curtailments.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-21）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm｜as_of：2026-08-21
<<<
Our net sales attributable to selling locations outside of the United States were approximately 36% in each of 2026, 2025 and 2024. In addition, many of our customers, manufacturing operations and suppliers are located outside the United States. The Company expects net sales from non-U.S. markets to continue to represent a significant portion of its total net sales. Furthermore, completed and pending acquisitions may increase our international exposure and the complexity of managing operations across multiple jurisdictions. Our non-U.S. operations are subject to risks in addition to those facing our domestic operations, including: •fluctuations in currency exchange rates and/or changes in monetary policy; •limitations on ownership and on repatriation of earnings; •transportation delays and other supply chain disruptions; •political, social and economic instability and disruptions, including armed conflicts; •the imposition of duties and tariffs and other trade barriers; •government import and export controls, embargoes, sanctions or trade restrictions, including possible restrictions on trade and/or obstacles to conducting business in China; •labor unrest and current and changing regulatory environments; •difficulties in implementing restructuring actions on a timely basis; •difficulties in staffing and managing multi-national operations; •limitations on our ability to enforce legal rights and remedies; •public health crises, including pandemics; •the potential for nationalization of enterprises; and •potentially adverse tax consequences.

Increased cybersecurity threats and more sophisticated and targeted computer crime have posed and could continue to pose a risk to our information technology systems, and a disruption to or breach in the security of such systems, if material, could have adverse effects on our results of operations and financial condition.

We rely on a limited number of suppliers for certain critical components, such as specialty electronics, rare earths, specialty chemicals, aerospace super alloys and filtration media, and recent and planned acquisitions may increase our exposure to supply concentration risk. Any disruption in supply from these sources could require us to seek alternative suppliers, potentially at higher cost or with delays that could impact production schedules. Furthermore, our suppliers of component parts may significantly and quickly increase their prices in response to increases in 10 Table of Contents costs of raw materials that they use to manufacture the component parts. As a result, we may not be able to increase our prices commensurately with our increased costs. Consequently, our results of operations or financial condition could be materially adversely affected.

The occurrence of one or more unexpected events, including war, acts of terrorism or violence, civil unrest, fires, tornadoes, hurricanes, earthquakes, floods and other forms of severe weather in the United States or in other countries in which we operate or in which our suppliers are located could adversely affect our operations and financial performance. Natural disasters, pandemics, equipment failures, power outages or other unexpected events could result in physical damage to and complete or partial closure of one or more of our manufacturing facilities or distribution centers, temporary or long-term disruption in the supply of component products from some local and international suppliers, and disruption and delay in the transport of our products to dealers, end-users and distribution centers. Existing insurance coverage may not provide protection for all of the costs that may arise from such events. The impacts of these unexpected events are difficult to predict but could have a material adverse effect on our business, results of operations or financial condition.

The markets we serve are characterized by rapidly changing technologies and frequent introductions of new products and services. Our ability to develop new products based on technological innovation and to position our existing products in new markets can affect our competitive position and often requires the investment of significant resources. For example, artificial intelligence technologies are rapidly developing and our business may be adversely affected if we cannot successfully integrate such technologies into our internal business processes and product and service offerings, or if we cannot effectively position our products to serve the needs of artificial intelligence technology providers, including data center infrastructure, in a timely, cost-effective, compliant and responsible manner. To advance our innovation and position us to meet our customers’ expectations, we make investments in emerging technologies that we believe are needed to keep pace with rapid industry innovation. If we cannot develop, or have difficulties or delays developing new and enhanced products and services, or if we fail to gain market or regulatory acceptance of new products and technologies, our revenues may be materially reduced and our competitive position could be materially adversely affected. In addition, we may invest in research and development of products and services, or in acquisitions or other investments, that do not lead to significant revenue, which could adversely affect our profitability.

In addition, we may not be able to integrate successfully any businesses that we purchase into our existing business, including FGC and Curtis, and it is possible that any acquired businesses or joint ventures may not be profitable. We may encounter, or have encountered, the following difficulties during the integration process: •the consequences of a change in tax treatment, including the cost of integration and compliance and the possibility that the full benefits anticipated to result from the acquisitions may not be realized; •delays in the integration of management teams, strategies, operations, products, and services; •differences in business backgrounds, corporate cultures, and management philosophies that may delay successful integration; •the ability to retain key employees; •the ability to create and enforce uniform standards, controls, procedures, policies, and information systems; •challenges of integrating complex systems, technologies, networks, and other assets of the acquired companies in a manner that minimizes any adverse impact or disruptions to customers, suppliers, employees, and other constituencies; and •unknown liabilities and unforeseen increased expenses or delays associated with the integration beyond current estimates.

We continually assess the strategic fit of our existing businesses and may divest or otherwise dispose of businesses that are deemed not to fit within our strategic plan or are not achieving the desired return on investment. These transactions pose risks and challenges that could negatively impact our business. For example, when we decide to sell or otherwise dispose of a business or assets, we may be unable to do so on satisfactory terms within our anticipated timeframe or at all, and even after reaching a definitive agreement to sell or dispose of a business, the sale is typically subject to satisfaction of pre-closing conditions which may not become satisfied. The divestiture process may also result in the disclosure of proprietary or competitively sensitive information to potential buyers, the incurrence of stranded costs that are not fully absorbed by the divested business, or the need to provide transition services that divert management attention and resources. Any strategic divestiture of a product line or business or exit of a product line or product category may reduce our revenue and earnings, result in material costs and expenses, create potential indemnification or retained liability obligations and cause disruption to our employees, customers, vendors and communities in which we operate.

We are subject to national and international laws and regulations, such as the anti-corruption laws of the U.S. Foreign Corrupt Practices Act and the U.K. Bribery Act, relating to our business and our employees. Despite our 15 Table of Contents policies, procedures and compliance programs, our internal controls and compliance systems may not be able to protect the Company from prohibited acts willfully committed by our employees, agents or business partners that would violate such applicable laws and regulations. Any such improper acts could damage the Company's reputation, subject us to civil or criminal judgments, fines or penalties, and could otherwise disrupt the Company's business, and as a result, could materially adversely impact our business, financial condition and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
