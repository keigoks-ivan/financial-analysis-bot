你是 stock-analyst v20 DD 的證據採集子 agent。標的：SNDK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Sandisk product substitute technology threat 2026
  - Computer Hardware alternative technology disruption 2026 2027
  - SNDK Sandisk technology obsolescence risk
  - Computer Hardware next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
•Disruption in our supply chain, other inability to source our supply requirements, or an increase in the costs of materials or components could negatively affect our business.

•Our operations are subject to a substantial risk of damage or disruption. •Our inability to attract, retain and develop highly skilled management and technical talent could negatively impact our business prospects.

•Competitive conditions, including declining average selling prices, volatile demand, technological change, industry consolidation, lengthy product qualifications, and supply constraints, in our industry can negatively impact our business.

We are subject to risks and regulatory obligations associated with our global manufacturing operations and global sales efforts, as well as risks and regulatory obligations associated with our utilization of global suppliers, including: •obtaining governmental approvals and compliance with evolving domestic and foreign regulations; •the need to comply with regulations on international business, including the Foreign Corrupt Practices Act, the United Kingdom Bribery Act 2010, the anti-bribery laws of other countries and rules regarding conflict minerals; •the impacts of social, political, immigration, and tax and trade policies in the U.S. and abroad; •exchange, currency and tax controls and reallocations; •the continued evolution and implementation of complex global and local tax regimes; •varying levels of protection of intellectual property rights; •policies and financial incentives by governments in China, the U.S. and countries in Europe and Asia designed to reduce dependence on foreign semiconductor manufacturing capabilities; •trade barriers, such as export controls, export bans, import restrictions, embargoes, sanctions, license and certification requirements (including semiconductor, encryption and other technology), tariffs and complex customs regulations; 14 Table of Contents •difficulties in managing international operations, including appropriate internal controls; and •financial volatility and disruptions to supply chain resulting from public health crises.

As a result of these risks, our business could be harmed. We are dependent on a limited number of qualified suppliers who provide critical services, materials or components, and a disruption in our supply chain or other inability to source our supply requirements, or an increase in the costs of materials or components, could negatively affect our business.

We do not have long-term contracts with some of our existing suppliers, nor do we always have guaranteed manufacturing capacity with many of our suppliers, so we cannot guarantee that they will devote sufficient resources or capacity to manufacturing our products. Any significant problems that occur at our suppliers could lead to product shortages or quality assurance problems. When we do have contractual commitments with suppliers in an effort to stabilize the supply of our components, those commitments may require us to buy a substantial number of components or make significant cash advances to the supplier and may not result in a satisfactory supply of our components. Additionally, if such suppliers were to experience operational or financial difficulties, be acquired by a competitor, or fail to perform required obligations under our supply agreements, our ability to source critical components could be impaired, potentially disrupting our product manufacturing and harming our business. We may also cancel or defer outstanding purchase commitments with certain suppliers due to changes in actual and forecasted demand, which may result in fees, penalties and other associated charges.…

Our operations, and those of certain of our suppliers and customers, are subject to substantial risk of damage or disruption.

Constraints on global talent mobility and hiring, including changes in immigration laws and policies, travel restrictions, work permits regulation and administration, government restrictions to contain the spread of infectious disease, and limitations on the ability of employees to enter, leave, or return to jurisdictions in which we operate, may also affect our ability to attract and retain the specialized skills needed to support our business and may disrupt our operations.

16 Table of Contents While we continue to invest in employee development, workforce planning, and structural agility, the speed and complexity of technological change and market demands create ongoing people-related risks that may impact our ability to sustain long-term innovation and operational performance.

In addition, the use of AI in the development of our products could potentially lead to ambiguities in intellectual property ownership, infringement or misappropriation risks, which could impact our competitive position and expose us to litigation, monetary penalties, or operational disruptions. The unauthorized or unapproved use of generative AI tools by our employees, contractors, or other third parties, as well as overreliance on AI automation or agentic AI without appropriate human oversight, may lead to the inadvertent disclosure of confidential, proprietary, or personal information, flawed or unauthorized actions, or other adverse consequences, including disruptions to business operations, exposing us to data security, privacy, legal, regulatory, and reputational risks. Misuse of such tools can also result in violations of applicable laws and regulations, including data protection and intellectual property laws. As legal and regulatory frameworks surrounding AI continue to evolve, we may be required to adapt our practices, policies, or systems, which could increase operational costs, limit innovation, or expose us to liability. This could materially affect our operations, financial condition, and ability to achieve our strategic objectives.

We participate in a highly competitive industry that has been, and may continue to be, subject to declining average selling prices, volatile demand, rapid technological change and industry consolidation, as well as lengthy product qualifications, all of which can negatively impact our business.

Further, our average selling prices and gross margins tend to decline when there is a meaningful shift in the mix of product sales to lower priced products. We have faced declining gross margins relating to our business in the past, and may face potential gross margin pressures in the future, resulting from our average selling prices declining more rapidly than our cost of revenue. Rapid technological changes have reduced, and may reduce in the future, the volume and profitability of sales of existing products and increase the risk of inventory obsolescence and write-downs. Finally, the semiconductor memory chip and data storage industries have experienced consolidation over the past several years, which could enhance the resources and lower the cost structure of some competitors. These factors could result in a substantial decrease in our market share and harm our business.

Additionally, new technologies could impact demand for our products in unforeseen or unexpected ways that could harm our business. For example, new products could substitute for our current products and make them obsolete, or new technologies could reduce the importance of and demand for our technology. In particular, demand for our products depends increasingly on the use of NAND flash memory in AI infrastructure, and new or alternative technologies could emerge that perform these functions more efficiently or reduce the storage required per unit of AI compute. If adopted at scale, such technologies could rapidly reduce or eliminate the importance of, and demand for, our technology in the AI infrastructure. We also develop products to meet certain industry and technical standards, which may change and cause us to incur substantial costs as we adapt to new standards or invest in different manufacturing processes to remain competitive.

For 2026, 2025, and 2024, 44%, 40% and 41%, respectively, of our total revenue came from sales to our top ten customers. These customers have a variety of suppliers to choose from and therefore can make substantial demands on us, including demands on product pricing, contractual terms and the environmental impact and attributes of our products, often resulting in the allocation of risk or increased costs to us as the supplier. Our ability to maintain strong relationships with our principal customers is essential to our future performance. We may experience events such as the loss of a key customer, prohibition or restriction of sales to a key customer by law, regulation or other government action, reductions in sales to or orders by a key customer, reductions in customer demand due to technological changes, or customer requirements to reduce our prices before we are able to reduce costs or the acquisition of a key customer by one of our competitors. These events may impact our operating results and financial condition. Further, government authorities may implement laws or regulations or take other actions that could result in significant changes to the business or operating models of our customers. Such changes could negatively impact our operating results.

The changes in our personnel, systems, and processes associated with operating independently have resulted, and may continue to result, in a loss of institutional knowledge, gaps in continuity, disruptions to our operations, and inefficiencies as our standalone organizations and systems mature. If we fail to effectively implement these initiatives—including integrating our governance structures, establishing and maintaining sufficient internal controls and corporate policies, fully developing our standalone teams and capabilities, and aligning stakeholder expectations—we may experience operational disruptions, material weaknesses or other deficiencies in our internal control over financial reporting, regulatory non-compliance, weakened stakeholder relationships, reputational harm, loss of business opportunities, and an inability to realize the anticipated benefits of the separation.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
