你是 stock-analyst v20 DD 的證據採集子 agent。標的：ARM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Arm Holdings product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - ARM Arm Holdings technology obsolescence risk
  - Semiconductors next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
Our IP business relies on our customers to design, manufacture and sell chips incorporating our products in order to generate royalty revenue. A substantial portion of our revenue depends upon the commencement of new design projects by semiconductor companies, OEMs, and CSPs, and their ability to provide complete chips based on our products to meet the specific application needs of their customers. However, our customers are not contractually obligated to design, manufacture, sell or deploy chips using our products on an exclusive basis or at all. Some of our existing customers design, manufacture, sell and deploy chips based on competing technology, including their own, and other existing or potential customers may do so in the future. To the extent that our customers elect to license technology from competitors, our competitive position could be adversely affected and we could lose market share. Furthermore, under many of our arrangements with customers, there is generally no minimum purchase obligation or guaranteed revenue stream.

Other microprocessor architectures such as x86 and RISC-V may already exist across all of these markets, or may be developed for applications within these markets. For applications in markets such as computing, data centers, networking and servers, competing microprocessor architectures, such as x86, already have a large, well-established customer base and are supported by a broad base of related software and development tools. These markets represent a significant portion of our revenue growth opportunity, and they also introduce new sources of competition, including, in some cases, incumbent competitors with established technologies, ecosystems, and customer bases, lower prices or costs, and greater brand recognition. These new markets may not grow as projected or at all, and we may not realize an adequate return on our investments. Due to the interdependence of various components in the products in which our architecture and our competitors’ architectures are used, customers are unlikely to change to another product, once adopted, until the next generation of a technology.…

Our business, reputation and relationships with our third-party partners could be adversely affected if we cannot develop technological improvements or adapt our products to technological changes on a timely basis. Whether we will be able to compete in the future will substantially depend on our ability to advance our products to meet these changing market and end-user needs and to anticipate successfully or respond to technological changes in hardware, software and architecture standards on a cost-effective and timely basis. If our products do not conform to, or are not compatible with, existing or emerging industry standards, demand for our products may decrease. Further, as a result of the rapidly changing technology and end-user needs in the semiconductor industry, our customers expect rapid development of new or enhanced products and solutions. The demand and expected timeline for development of our products and solutions, in the aggregate, often exceeds our available resources, requiring us to prioritize certain products and solutions. These resource constraints may be exacerbated when developing and distributing new products and solutions, particularly if those proposed products and solutions require greater resources than we anticipated.…

Economic conditions could continue to deteriorate in the future, including as a result of fluctuating inflation and interest rates, a sustained global semiconductor shortage, supply chain disruptions and any disruptions of international trade relationships, such as tariffs, export licenses or other government trade restrictions or new or continued conflicts. In particular, the semiconductor and electronics industries could fail to grow and sustained or increasing inflation could increase our operating expenses, increase costs for our customers and reduce demand for our products or our customers’ products. In addition, adverse economic conditions affect demand for devices that our products help create, such as smartphones, automobiles and servers. Longer-term reduced demand for these or other devices could result in reduced demand for our products and significant decreases in our licensing fees and royalty revenues over time. In addition, if our customers, distributors or other companies in the value-chain build elevated inventory levels, we could experience a decrease in short-term and/or long-term demand for our products. If any of these events or disruptions were to occur, the demand for our products could be materially adversely affected along with our business, results of operations, financial condition and prospects.

Our business and operating results are also vulnerable to interruption by other events outside of our control, such as earthquakes, fire, extreme weather events, power loss, telecommunications failures, epidemics, pandemics or other public health crises, political instability, geopolitical turmoil, such as the war in Ukraine and conflicts in the Middle East, including Iran, and any sanctions, export controls or restrictions on doing business with Russia and Belarus, or with other countries (including the PRC), as well as any resulting disruption, instability or volatility in the global markets and industries resulting from such conflict, pandemics, military conflict and uncertainties arising out of terrorist attacks, including a global economic slowdown, the economic consequences of the recent resurgence and escalation of trade conflicts between the U.S. and the PRC as well as other major U.S. trade partners, the potential for deteriorating relations between the PRC and Taiwan and the associated disruptions to, or effects on, the semiconductor industry, military action or terrorist activities and associated political instability. Economic or political instability may undermine consumer confidence and/or cause current or potential customers, including the end customers of our customers or potential customers, to reduce 22 or delay their technology purchases and investments.…

Any escalation in geopolitical tensions in Asia, particularly between the PRC and Taiwan, could significantly disrupt semiconductor chip manufacturing and interrupt the global semiconductor chip supply chain. A significant portion of the world’s semiconductor manufacturing is in Taiwan, and increased geopolitical tensions there could exacerbate supply chain disruptions. In addition, geopolitical conflicts, such as the war in Ukraine and conflicts in the Middle East, including Iran, could lead to market disruptions and exacerbate current supply chain constraints, including with respect to certain materials and metals, which are essential in semiconductor manufacturing.

Competition for highly skilled talent, and particularly engineers, can be intense. Other companies may be successful in recruiting and hiring members of our management team or other key employees, and it may be difficult for us to find suitable replacements on a timely basis, on competitive terms or at all. We experience voluntary attrition on an ongoing basis. If we lose the services of any of our senior management, other key talent or a significant number of our engineers or sales and marketing talent, our development efforts or business relationships could be disrupted, which could have a material adverse effect on our business, results of operations, financial condition and prospects. Our future success significantly depends on our ability to identify, attract, motivate and retain qualified engineers and consultants with the requisite educational background and industry experience. Competition for such qualified engineers is intense and the cost of attracting and retaining qualified employees and consultants may increase without a corresponding increase in the prices we charge our customers, which could materially and adversely affect our profitability. In certain geographic regions, there is also intense competition for sales and marketing talent, which may adversely affect our ability to expand into new markets.…

Cyberattacks, security breaches or other similar incidents with respect to our information technology systems or those of our third-party partners could result in unauthorized access to, or misappropriation, loss of availability or integrity, disclosure, modification, misuse, loss, destruction or theft of, personal, confidential and proprietary information belonging to us or our employees, third-party partners, customers or suppliers, requiring us to notify individuals, regulators, customers, or other persons under applicable laws or contractual obligations. Such incidents could also cause a significant disruptive effect on our services, which could result in us, our third-party partners or our customers suffering significant financial or reputational damage and potential third-party legal action. If our security measures are, or are believed to be, inadequate or breached as a result of third-party action, including third-party partners that have access to our internal network and environment, employee negligence, error or malfeasance, fraud, product defects, accidental technological failure, social engineering techniques, improper user configuration or otherwise, and this results in, or is believed to result in, compromise of the confidentiality, integrity or availability of our data or our third-party partners’ and customers’ data, or otherwise causes a significant disruptive effect on our services, we could incur significant liability to various parties, including our third-party partners and customers, and to individuals or organizations whose information is being processed by us,…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
The markets for our products are intensely competitive and some of them are characterized by rapid technological change. These changes result in frequent product introductions, short product life cycles and increased product capabilities typically representing significant price and performance improvements. We face significant competition from established technologies such as the x86 architecture, as well as from free, open-source technologies, including the RISC-V architecture. Some of our customers are also major supporters of the RISC-V architecture and related technologies.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
