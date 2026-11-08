你是 stock-analyst v20 DD 的證據採集子 agent。標的：LEU。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Centrus Energy product substitute technology threat 2026
  - Uranium alternative technology disruption 2026 2027
  - LEU Centrus Energy technology obsolescence risk
  - Uranium next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm｜as_of：2026-02-11
<<<
Our LEU segment backlog includes medium and long-term sales contracts and contingent sales commitments with major utilities through 2040. We have secured cost-competitive supplies of SWU under long-term contracts through the end of this decade designed to allow us to fill our existing customer orders and make new sales. However, supply chain disruptions may impact our ability to fill existing customer orders. A market-related price reset provision in the TENEX Supply Contract, which is our largest supply contract, became effective in 2019 – when market prices for SWU were near historic lows – which has significantly lowered our cost of sales and contributed to improved margins since 2019.

The DOE continues to pursue the availability of HALEU for the ARDP and for the advanced reactor market and the availability of domestically enriched uranium in a quantity that would be sufficient to address a supply disruption and gaps in domestic production and enrichment. Congress appropriated a total of approximately $3.4 billion to the DOE to jumpstart U.S. nuclear fuel production, including both LEU and HALEU enrichment. Based on this funding, the DOE issued a series of three RFPs covering HALEU production, HALEU deconversion, and LEU production. In late 2024, the DOE made initial selections under each of the RFPs. Centrus was among the awardees for all three RFPs under IDIQ structures (the HALEU Deconversion Contract, HALEU Production Contract, and the LEU Production Contract).

In addition to limitations targeted specifically at imports of LEU or exports of natural uranium back to Russia, the evolving sanctions imposed by the United States and foreign governments on the mechanisms used to make payments to Russia and to obtain services, including transportation, have increased the risk that implementation of the TENEX Supply Contract may be disrupted frequently. If the U.S. government were to prohibit companies and individuals from engaging in transactions with Rosatom and its subsidiaries, including TENEX, the Company and its suppliers could not implement the TENEX Supply Contract absent a license or other authorization from the sanctioning government.

The actual size of the annual quotas allocated to Centrus for the TENEX Supply Contract are confidential, but a public version of the quotas shows that they represent a significant portion of the total quotas provided under the RSA in 2021 through 2028. The quotas provided for the TENEX Supply Contract are expected to be adequate to support the Company’s long-term strategic goals and to permit enriched uranium procured from TENEX during the remaining term of the TENEX Supply Contract to be imported to supply U.S. utilities subject to potential supply chain disruptions as a result of the Import Ban Act, the Russian Decree and other impacting restrictions.

In addition to limitations targeted specifically at imports of LEU into the U.S. or export of LEU out of Russia, the evolving sanctions or restrictions imposed by the United States and foreign governments on the mechanisms used to make payments to Russia and to obtain services, including transportation, have increased the risk that implementation of the TENEX Supply Contract may be disrupted frequently. If the U.S. government were to prohibit companies and individuals from engaging in transactions with Rosatom and its subsidiaries, including TENEX, the Company and its suppliers could not implement the TENEX Supply Contract absent a license or other authorization from the sanctioning government.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm｜as_of：2026-02-11
<<<
Risks related to operational factors primarily include: •our inability to successfully perform our U.S. government contracts, including any task orders we may be awarded; •our ability to successfully implement our planned expansion projects in Piketon, Ohio and Oak Ridge, Tennessee; •disruptions arising from the Import Ban Act or the Russian Decree restricting imports, exports or sales of SWU or uranium that we buy from our Russian supplier and our other sources of supply; •the inability to sell all of the LEU we are required to purchase under supply agreements for prices that cover our costs.

29 These events could adversely affect us to the extent they result in a reduction or elimination of customers’ contractual requirements to purchase from us; the suspension or reduction of nuclear reactor operations; the reduction or blocking of supplies of raw materials, natural or enriched uranium or SWU; lower demand; burdensome regulation, disruptions of shipments, production importation or payment (including the blocking or restriction of transportation services or hardware); increased competition from third parties; increased costs or difficulties; or increased liability for actual or threatened property damage or personal injury. Additionally, customers may face financial difficulties, including from factors unrelated to the nuclear industry, that could affect their willingness or ability to make purchases. We cannot provide any assurance that events will not prevent or delay us from making deliveries to our customers or increase our costs or that our customers, suppliers, or contractors will not default on their obligations to us or file for bankruptcy protection. If a customer files for bankruptcy protection, for example, we likely would be unable to collect all, or even a significant portion, of amounts that are owed to us.…

The global outbreak of COVID-19 was declared a pandemic by the World Health Organization and a national emergency by the U.S. government, and negatively affected the U.S. and global economies, disrupted supply chains, and resulted in significant travel, transport, and other restrictions. Although the COVID-19 pandemic has ended, other national or global health related outbreaks could further disrupt the supply chains and day-to-day operations of the Company, our suppliers, our contractors, and our customers, which could materially adversely affect our operations, including increasing our costs. In this regard, global supply chains and the timely availability of products or product components sourced domestically or imported from other nations, including SWU contained in LEU we purchase, could be materially disrupted by quarantines, slowdowns or shutdowns, border closings, and travel restrictions resulting from a global pandemic or health crisis. Further, impacts of such health crises on our management and workforce, or our suppliers, contractors, or customers, could adversely impact our business and we may be unable to mitigate such impacts.

As described in further detail in Part II, Item 7, Management’s Discussion and Analysis of Financial Condition and Results of Operations, we are pursuing several expansion initiatives, including the expansion of the manufacturing capacity at our facility in Oak Ridge, Tennessee and a major expansion of our uranium capacity in Piketon, Ohio. ACO was awarded a $900.0 million task order from the DOE to expand its uranium enrichment facility in Piketon, Ohio, which is subject to negotiation of a definitive agreement. These projects are complex, costly, and subject to significant uncertainties. Delays, cost overruns, or operational disruptions could materially impact our ability to achieve the anticipated benefits of these initiatives. Our ability to complete expansion projects on time and within budget depends on a variety of factors, many of which are outside our control. These include challenges related to DOE funding, permitting, zoning, environmental reviews, supply chain constraints, and the availability and performance of contractors, subcontractors, and construction materials. Adverse weather, labor disputes, supply chain disruptions or delays, changing market conditions, unexpected engineering issues, or changes in regulatory requirements could further delay or disrupt construction activities.

The DOE continues to pursue the availability of HALEU for the ARDP and for the advanced reactor market and the availability of domestically enriched uranium in a quantity that would be sufficient to address a supply disruption and gaps in domestic production and enrichment and issued separate RFPs for the deconversion of HALEU, the production of HALEU and domestic production of LEU. The DOE awarded ACO the HALEU Production Contract, the HALEU Deconversion Contract and the LEU Production Contract. These IDIQ contracts were awarded to multiple successful bidders, after which the awardees compete for individual task orders. The ultimate dollar amount under each contract and the potential scale of the expansion supported will depend upon the scope of task orders that DOE may subsequently issue under each of the contracts for which we will compete. On January 5, 2026, the DOE announced that ACO was awarded a $900.0 million task order to expand its uranium enrichment facility in Piketon, Ohio, to include commercial-scale production of HALEU under the HALEU Production Contract. The task order is subject to negotiation of a definitive agreement and there are no guarantees about whether or when funding by the DOE for such expansion would be awarded.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
