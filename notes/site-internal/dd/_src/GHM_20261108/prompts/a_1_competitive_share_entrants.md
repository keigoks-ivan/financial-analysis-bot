你是 stock-analyst v20 DD 的證據採集子 agent。標的：GHM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - GHM Graham market share gaining OR losing 2026
  - Graham new entrant OR displace threat Specialty Industrial Machinery 2026
  - GHM competitor design win 2026
  - Graham vs Specialty Industrial Machinery peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-06-08）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm｜as_of：2026-06-08
<<<
Our Strengths Our core strengths include: •We have a value-enhancing engineering sales and product development platform. We believe our customer-facing platform of technical sales, project estimating and application engineering are competitive advantages. We have tools and capabilities that we believe allow us to move quickly and comprehensively to meet the unique needs of our customers. We believe that our early and deep involvement in our customers' projects adds significant value and is an important competitive differentiator in the industries we serve. We believe customers need our engineering and fabrication expertise early in a project life cycle to understand how best to utilize our equipment in the optimization of their systems.

Fiscal 2023 through 2026 were characterized by continual improvement and increasing profitability, and formed the initial steps along our path to achieve our fiscal 2027 goals through investments in our business. We remain focused on disciplined execution and strategic investments that enhance our capabilities and support long-term profitable growth. Our priorities are our targeted markets, operational excellence, leveraging the investments we have made, and serving our stakeholders. We will maintain strong capital discipline with smart capital deployment. We plan to: •Pursue clearly defined markets with significant barriers to entry •Optimize processes and tools to deliver superior performance •Engage all stakeholders to multiply our efforts •Prioritize capital investments that fuel growth and maximize shareholder value •Supplement our organic growth opportunities with strategic acquisitions Competition Our business is highly competitive. The principal bases on which we compete include technology, price, performance, reputation, delivery, and quality. Our competitors listed in alphabetical order by market include: North America Market Principal Competitors Defense DC Fabricators; PCC; Triumph Aerospace; Xylem Energy & Process Croll Reynolds Company, Inc.; Gardner Denver, Inc.; GEA Wiegand GmbH; Korting Hannover AG; Schutte & Koerting Turbomachinery OEM – Defense and Space Ametek, Inc.; Collins Aerospace; Concepts NREC; Curtiss Wright; Honeywell; Kratos Defense & Security Solutions; L3Harris Technologies, Inc.

Advanced Mixing Systems Hauschild SpeedMixer; Mazerustar Planetary Mixers; Thinky Corporation; Resodyn Acoustic Mixers international Market Principal Competitors Energy & Process Croll Reynolds Company, Inc.; Edwards, Ltd.; Gardner Denver, Inc.; GEA Wiegand GmbH; Korting Hannover AG; Schutte & Koerting; Westlake 6 Turbomachinery OEM – Energy & Process Chem Process Systems; Donghwa Entec Co., Ltd.; Hangzhou Turbine Equipment Co., Ltd.; KEMCO; Mazda (India); Oeltechnik GmbH Turbomachinery OEM – power and power producer Chem Process Systems; Holtec; KEMCO; Mazda (India); SPX Heat Transfer; Thermal Engineering International Advanced Mixing Systems Hauschild SpeedMixer; Mazerustar Planetary Mixers; Thinky Corporation Intellectual Property Our success depends in part on our ability to protect our proprietary technologies. We rely on a combination of patent, copyright, trademark, trade secret laws, and contractual confidentiality provisions to establish and protect our proprietary rights. We also depend heavily on the brand recognition of the Graham, Barber-Nichols, and FlackTek names in the marketplace.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-06-08）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm｜as_of：2026-06-08
<<<
In addition, our increased market share has caused an adverse share position for some of our competitors for these products. Competitor response to our market penetration is possible. Our customers may also raise concerns about their supplier concentration issues and the risk exposure related to this concentration. As the U.S. Navy is looking to expand its fleet, there is also a risk that their facilities, their supply chain, or our supply chain may not be able to support this expansion. This could adversely impact our ability to grow this portion of our business. Further, the bidding process related to these Defense projects requires us to devote a certain amount of time and resources to prepare bids and proposals and there is no assurance that we will recoup those investments.

The bladeless mixer industry is characterized by ongoing innovation and technological change. Competitors may develop new technologies or enhanced product features that outperform or otherwise diminish the attractiveness of our current offerings. Our ability to remain competitive depends on successfully anticipating technological trends, investing in research and development and introducing new or improved products in a timely manner. If we fail to keep pace with emerging technologies or shifting customer expectations, our products may become outdated, leading to reduced demand, loss of market share, or pricing pressure, any of which could materially adversely affect our business, financial condition and results of operations.

Our business is highly competitive. If we are unable to successfully implement our business strategy and compete against entities with greater resources than we have or against competitors who have a relative cost advantage, we risk losing market share to current and future competitors.

We encounter competition in all of our markets. Some of our present and potential competitors may have greater financial, marketing, technical or manufacturing resources. Our competitors may also be able to respond more quickly to new technologies or processes and changes in customer demands and they may be able to devote greater resources towards the development, promotion and sale of their products. Certain competitors may also have a cost advantage compared to us due to their geography or changes in relative currency values and may compete against us based on price. This may affect our ability to secure new business and maintain our level of profitability. As our markets continue to grow, and new market opportunities expand, we could see a shift in pricing as a result of facing competitors with lower production costs, which may have a material adverse impact on our results of operations and financial results. In addition, our current and potential competitors may make strategic acquisitions or establish cooperative relationships among themselves or with third parties that increase their ability to address the needs of our customers. Moreover, customer buying patterns can change if customers become more price sensitive and accepting of lower cost suppliers. If we cannot compete successfully against current or future competitors, our business will be materially adversely affected.

We are exposed to the risk of currency fluctuations between the U.S. dollar and the currencies of the countries in which we sell our products to the extent that such sales are not based in U.S. dollars - primarily the Chinese RMB and India INR. Currency movements can affect sales in several ways, the foremost being our ability to compete for orders against foreign competitors that base their prices on relatively weaker currencies. Strength of the U.S. dollar compared with the Euro, India, or Asian currencies may put us in a less competitive position. Business lost due to competition for orders against competitors using a relatively weaker currency cannot be quantified. In addition, cash can be adversely impacted by the conversion of sales made by us in a foreign currency to U.S. dollars. While we may enter into currency exchange rate hedges from time to time to mitigate these types of fluctuations, we cannot remove all fluctuations or hedge all exposures and our earnings could be adversely impacted by changes in currency exchange rates. In addition, if the counter-parties to such exchange contracts do not fulfill their obligations to deliver the contractual foreign currencies, we could be at risk for fluctuations, if any, required to settle the obligation.…

During weaker market periods, we may choose to be more aggressive in pricing certain competitive projects to protect or gain market share or to maintain or increase the utilization of our facilities. In these situations, it is possible that an incrementally profitable order, while increasing contribution, may be unprofitable from an accounting perspective when including fixed manufacturing costs. In these situations, we are required to recognize the financial loss at the time of order acceptance, or as soon as our cost estimates are updated, whichever occurs first. It is possible we may accumulate losses either on a large project or more than one project such that, in a short time period, for example a reporting quarter, these losses may have a meaningful impact on the earnings for that period.

Competition for qualified management, including our executive management, and key technical and sales personnel in our industry is intense. Moreover, our technology is highly specialized, and it may be difficult to replace the loss of any of our key technical and sales personnel. Many of the companies with which we compete for management and key technical and sales personnel have greater financial and other resources than we do or are located in geographic areas which may be considered by some to be more desirable places to live. If we are not able to retain any of our key management, including our executive management, technical or sales personnel, due to competition, retirement or any other reason for leaving, it could have a material adverse effect on our business and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
