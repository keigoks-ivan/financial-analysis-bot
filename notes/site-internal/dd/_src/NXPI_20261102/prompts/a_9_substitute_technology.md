你是 stock-analyst v20 DD 的證據採集子 agent。標的：NXPI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - NXP Semiconductors product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - NXPI NXP Semiconductors technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1413447/000141344726000008/nxpi-20251231.htm｜as_of：2026-02-19
<<<
NXP has not experienced any material labor disruptions. In addition, employee-led works councils operate in certain countries and provide input on topics relevant to employees, consistent with local regulations and governance frameworks.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1413447/000141344726000008/nxpi-20251231.htm｜as_of：2026-02-19
<<<
The semiconductor industry is highly competitive and characterized by constant and rapid technological change, short product lifecycles, significant price erosion and evolving standards. Accordingly, the success of our business depends to a significant extent on our ability to develop new technologies and products that are ultimately successful in the market. The costs related to the research and development necessary to develop new technologies and products are significant and subject to increase due to current and expected inflation and any reduction of our research and development budget could harm our competitiveness. Meeting evolving industry requirements, including the increasing use of AI and machine learning technologies (including the need to run complex AI-based applications on devices), and introducing new products to the market in a timely manner and at prices that are acceptable to our customers are significant factors in determining our competitiveness and success.

We are a party to collective bargaining agreements and social plans with our labor unions. We are also required to consult with our employee representatives, such as works councils, on items such as restructurings, acquisitions and divestitures. Although we believe that our relations with our employees, employee representatives and unions are satisfactory, no assurance can be given that we will be able to successfully extend or renegotiate these agreements as they expire from time to time or to conclude the consultation processes in a timely and favorable way. The impact of future negotiations and consultation processes with employee representatives could have a material impact on our financial results. Also, if we fail to extend or renegotiate our labor agreements and social plans, if significant disputes with our unions arise, or if our unionized workers engage in a strike or other work stoppage, we could incur higher ongoing labor costs or experience a significant disruption of operations, which could have a material adverse effect on our business.

We manufacture, in our own factories as well as with third parties, our products using processes that are highly complex, require advanced and costly equipment and must continuously be modified to improve yields and performance. Difficulties in the production process can reduce yields or interrupt production, and, as a result of such problems, we may on occasion not be able to deliver products or do so in a timely or cost-effective or competitive manner. Such difficulties may include rationing, or other forced disruption of utility supplies such as electricity, gas or water by governments or regulators which could lead to disruptions of our operation resulting in high costs and global supply chain disruptions. As the complexity of both our products and our fabrication processes has become more advanced, manufacturing tolerances have been reduced and requirements for precision have become more demanding. As is common in the semiconductor industry, we have in the past experienced manufacturing difficulties that have given rise to delays in delivery and quality control problems. There can be no assurance that any such occurrence in the future would not materially harm our results of operations.…

21 Our manufacturing operations depend on deliveries of equipment and materials in a timely manner and, in some cases, on a just-in-time basis. From time to time, suppliers may extend lead times, limit the amounts supplied to us or increase prices due to capacity constraints or other factors. Supply disruptions may also occur due to shortages in critical materials, such as silicon wafers or specialized chemicals. In addition, the imposition of tariffs or other trade restrictions may significantly increase the costs, and otherwise adversely impact the availability of certain raw materials and supplies needed for our manufacturing operations. Because the equipment that we purchase is complex, it is frequently difficult or impossible for us to substitute one piece of equipment for another or replace one type of material with another. A failure by our suppliers to deliver our requirements could result in disruptions to our manufacturing operations. Our business, financial condition and results of operations could be harmed if we are unable to obtain adequate supplies of quality equipment or materials in a timely manner or if there are significant increases in the costs of equipment or materials due to current or expected inflation, trade restrictions or other reasons and we are not able to increase the price of our products.

Disruptions in our relationships with any one of our key customers could adversely affect our business.

Environmental and other disasters, such as flooding, heavy precipitation large earthquakes, volcanic eruptions or nuclear or other disasters, or a combination thereof may negatively impact our business. If flooding, heavy precipitation, a large earthquake, volcanic eruption or, extreme weather event or other natural disaster were to 22 directly damage, destroy or disrupt our manufacturing facilities, it could disrupt our operations, delay new production and shipments of existing inventory or result in costly repairs, replacements or other costs, all of which would negatively impact our business. Even if our manufacturing facilities are not directly damaged, a large natural disaster may result in disruptions in distribution channels, supply chains, movement of goods and significant increases in the prices of raw materials used for our manufacturing process. For instance, the nuclear incident following the tsunami in Japan in 2011 impacted the supply chains of our customers and suppliers. Furthermore, any disaster affecting our customers (or their respective customers) may significantly negatively impact the demand for our products and our revenues. In addition, climate change could cause certain natural disasters, such as drought, wildfires, storms, flooding or rising sea levels, to occur more frequently or with greater intensity.…

25 In the current environment, there are numerous and evolving risks to cybersecurity and privacy, including criminal hackers, state-sponsored intrusions, industrial espionage, employee malfeasance, and human or technological error. Computer hackers and others routinely attempt to breach the security of technology products, services, and systems, and those of customers, suppliers, and some of those attempts may be successful. Such breaches could result in, for example, unauthorized access to, disclosure, misuse, loss, or destruction of our, our customer, or other third party data or systems, theft of sensitive or confidential data including personal information (including personal data about our employees, customers or other third parties) and intellectual property, system disruptions, and denial of service. In the event of such breaches, we, our customers or other third parties could be exposed to potential liability, litigation, and regulatory action, as well as the loss of existing or potential customers, damage to our reputation, and other financial loss. In addition, the cost and operational consequences of responding to breaches and implementing remediation measures could be significant. We have identified instances of employee misappropriation or theft of certain proprietary technology by individuals who are no longer employed by NXP. In some cases, such misappropriation may result in the violation of applicable export control regulations, which we report to relevant authorities as appropriate.…

Effective October 28, 2025, Kurt Sievers voluntarily retired as our CEO and executive director and Rafael Sotomayor succeeded Mr. Sievers as President and CEO and temporary executive director of the Company. Any significant leadership change involves inherent risk, including potential disruptions to our operations or relationships with customers, suppliers and key employees, and can be inherently difficult to implement. If our CEO transition is not successful for any reason, it could have an adverse impact on our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NXPI_20261102/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
