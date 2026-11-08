你是 stock-analyst v20 DD 的證據採集子 agent。標的：TMDX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - TransMedics Group product substitute technology threat 2026
  - Medical Devices / Organ Transplant Logistics alternative technology disruption 2026 2027
  - TMDX TransMedics Group technology obsolescence risk
  - Medical Devices / Organ Transplant Logistics next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm｜as_of：2026-02-24
<<<
Our insurance may not cover our losses in any particular case, or insurance may not be available on commercially reasonable terms to cover certain of these catastrophic events. In addition, regardless of the level of insurance coverage, damage to our facilities or any disruption that impedes our ability to manufacture the OCS in a timely manner could materially and adversely affect our business, financial condition, operating results, cash flows and prospects.

We must continue to educate surgeons, transplant centers and private and public payors and demonstrate the merits of the OCS compared with cold storage or new competing technologies.

The supply of raw materials to our component parts suppliers could be interrupted for a variety of reasons, including availability and pricing. We may experience supply chain disruptions due to general impacts of inflation and labor shortages and these disruptions to the supply chain could adversely affect our ability to meet commitments to customers. Significant price increases could adversely affect our results of operations and operating margins. In particular, inflation, changes in trade policies, the imposition of duties and tariffs and public health crises could adversely impact the price or availability of raw materials and the components of our products. The U.S. continues to implement certain trade actions, including imposing tariffs on certain goods imported from China and other countries. Significant tariffs have been proposed by the new administration, although it is not possible to predict the extent or focus of any such tariffs at this time. Additional tariffs, trade restrictions and export controls imposed by the U.S. on a broader range of imports, or further retaliatory trade measures taken by China or other countries in response, may impact our suppliers and the price of our components for our OCS products or our aircraft.…

Other companies may develop technologies and products that result in improved patient outcomes or are safer, easier to use, less expensive or more readily accepted than the OCS. These products or technologies could make the OCS obsolete or noncompetitive and reduce demand for our OCS products. Many of these providers of alternative products, procedures and therapies have greater name recognition, significantly greater financial resources and expertise in research and development, manufacturing, preclinical testing, conducting clinical trials, obtaining regulatory approvals and clearances and marketing and selling products than we do. Smaller and other early stage companies may also prove to be significant competitors, particularly through collaborative arrangements with large and established companies. Third parties may also compete with us in recruiting and retaining qualified medical, engineering and management personnel, establishing clinical trial sites and patient registration for clinical trials, as well as in acquiring technologies complementary to or necessary for our products or development programs or otherwise advantageous to our business. Our failure to compete effectively will harm our business and operating results.

As part of our services offered under our NOP, we have acquired a fleet of fixed-wing aircraft. All of the aircraft we currently operate are standardized variants of a certificated model produced by a single manufacturer. Parts and services from this manufacturer 36 are subject to their product and workmanship warranties and capacity to service aircraft. If this manufacturer fails to adequately fulfill its obligations towards us or experiences interruptions or disruptions in production or provision of services due to, for example, bankruptcy, natural disasters, labor strikes or disruption of its supply chain we may experience a significant delay in the delivery of or fail to receive previously ordered parts, which would adversely affect our revenue and results of operations and could jeopardize our ability to meet the demands of our customers. If there is a shortage of replacement parts that are compatible with the model of aircraft we operate, our entire fleet may be impacted and we would not be able to rely on other model aircraft during replacement part shortages or outages. Our operation of a single model of aircraft may therefore limit flexible use of our fleet.…

We rely on Pratt & Whitney aircraft engines to power our owned aircraft, and we may enter into program agreements covering certain of our aircraft related to engine maintenance and overhauls for certain aircraft in our fleet. If Pratt & Whitney fails to adequately fulfill its obligations towards us or experiences interruptions or disruptions in production or provision of parts or services due to, for example, bankruptcy, natural disasters, labor strikes, increased FAA, oversight of the production process, or disruption of its supply chain, we may experience a significant delay in the delivery of or fail to receive previously ordered aircraft engines and parts, which could result in grounded aircraft. These disruptions would adversely affect our revenue and profitability and could jeopardize our ability to meet the demands of our customers. In addition, if we fail to meet our obligations or are otherwise in default under the program agreements, our access to aircraft engines and parts may become limited, which could adversely impact our business, operations, cash flow, financial condition and liquidity.

Our aircraft fleet requires regular maintenance work, which may cause operational disruption. Failure to perform timely maintenance and repairs results in aircraft being underutilized which could have an adverse impact on our business, financial condition and results of operations. On occasion, airframe manufacturers and/or regulatory authorities require mandatory or 37 recommended modifications across a particular fleet which may ground a particular type of aircraft. This may cause operational disruption to, and impose significant costs on us. Furthermore, our operations in remote locations, where delivery of components and parts or transportation of maintenance personnel could take a significant period of time, could result in delays in our ability to maintain and repair our aircraft. Any such delays may pose a risk to our business, financial condition and results of operations. Moreover, as our aircraft base increases and our fleet ages, our maintenance costs could potentially increase and we may be unable to manage the composition of our fleet in a manner that reduces costs due to the availability and prices for replacement aircraft and parts. When our aircraft are grounded for maintenance, we are required to rely on third-party logistics service providers to transport organs for our NOP, which increases the cost of operating our NOP.

We rely on shipping providers to deliver products to our customers globally. Labor, tariff or World Trade Organization-related disputes, piracy, physical damage to shipping facilities or equipment caused by severe weather or terrorist incidents, congestion at shipping facilities, inadequate equipment to load, dock and offload our products, energy-related tie-ups or other factors could disrupt or delay shipping or off-loading of our products domestically and internationally. Such disruptions or delays could materially and adversely affect our business, financial condition, operating results, cash flows and prospects.

We may experience disruptions as we continue to expand our operations and facilities and execute on our growth strategy. In January 2026, we entered into a lease agreement with the intent to move our headquarters to a larger space in Somerville, Massachusetts. We intend to renovate the facility before moving our operations, including manufacturing, to this facility. The process of moving our business, opening new facilities and bringing operations online at this new site is inherently complex and is not part of our day-to-day operations. The relocation and expansion of our headquarters and the opening of any additional new facilities, including our planned expansion in Italy, may cause significant disruption to our operations, divert management attention and resources and involve significant costs, all of which could have a material adverse effect on our business, financial condition and results of operations. The relocation of our headquarters and any additional facilities that we seek to open may take longer than anticipated or may not proceed as planned, and the expected benefits may be less than anticipated.

We currently make limited use of AI technologies in our operations, and we may continue to explore further use cases. The rapid advancement of these technologies presents opportunities for us in research, manufacturing, commercialization, and other business endeavors, but also entails risks, including that AI-generated content, analyses, or recommendations we utilize could be deficient, that our competitors may more quickly or effectively adopt AI capabilities, or that our use of AI or other emerging technologies increases regulatory, privacy, cybersecurity and other significant risks. In addition, any disruption or failure in the AI functionality we incorporate into our business activities, products or services could adversely impact our business or result in delays or errors in our product offerings. The legal and regulatory landscape surrounding AI technologies is rapidly evolving and uncertain, including in the areas of intellectual property, cybersecurity and privacy and data protection. Compliance with new or changing laws, regulations or industry standards relating to AI may impose significant costs on us and limit our ability to effectively develop, deploy or use AI technologies. Furthermore, if we are unable to effectively manage the use of AI technologies by our employees and service providers, our confidential information, intellectual property and reputation could be put at risk.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
