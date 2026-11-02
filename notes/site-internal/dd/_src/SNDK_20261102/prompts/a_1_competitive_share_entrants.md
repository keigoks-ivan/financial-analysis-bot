你是 stock-analyst v20 DD 的證據採集子 agent。標的：SNDK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - SNDK Sandisk market share gaining OR losing 2026
  - Sandisk new entrant OR displace threat Computer Hardware 2026
  - SNDK competitor design win 2026
  - Sandisk vs Computer Hardware peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
Competition Our industry is highly competitive. We believe we are well positioned with our leading flash product portfolio, premium consumer brand, differentiated semiconductor innovation engine and leadership in driving cost efficiency. Nevertheless, we face strong competition from other manufacturers of flash in the Datacenter, Edge and Consumer end markets. We compete with vertically-integrated suppliers such as Kioxia, Micron Technology, Inc., Samsung Electronics Co., Ltd., SK Hynix, Inc., Yangtze Memory Technologies Co., Ltd. and numerous smaller companies that assemble flash into products.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
We provide warranties on the majority of our products for periods of one to five years. We test our products in our manufacturing facilities through a variety of means. However, our testing may fail to reveal defects in our products that may not become apparent until after the products have been sold into the market. In addition, our products may be used in a manner that is not intended or anticipated by us, resulting in potential liability. Accordingly, there is a risk that product defects will occur, including as a result of third-party components or applications that we incorporate in our products, which could require a product recall. Product recalls can be expensive to implement. As part of a product recall, we may be required or choose to replace the defective product. Moreover, there is a risk that product defects may trigger an epidemic failure clause in a customer agreement. If an epidemic failure occurs, we may face termination of long-term sales agreements and may be required to replace or refund the value of the defective product and to cover certain other costs associated with the consequences of the epidemic failure.…

The terms of our agreements with Kioxia with respect to Flash Ventures require that substantially all of our flash-based memory be obtained from Flash Ventures, which limits our ability to respond to market demand and supply changes and makes our financial results particularly susceptible to variations from our forecasts and expectations. For example, we are contractually obligated to pay for 50% of the fixed costs of Flash Ventures regardless of whether we order any flash-based memory, and our orders placed with Flash Ventures on a rolling basis are binding. As a result, a failure to accurately forecast supply and demand could cause us to over-invest or under-invest in inventory, technology transitions or the expansion of Flash Ventures’ capacity. Over-investment by us or our competitors can result in excess supply and lead to significant decreases in 18 Table of Contents our product prices, significant excess, obsolete inventory or inventory write-downs or underutilization charges, and the potential impairment of our investments in Flash Ventures. For example, in 2023, WDC incurred $296 million in charges for unabsorbed manufacturing overhead costs as a result of reduced utilization of its manufacturing capacity and $108 million in charges to write down its inventory as a result of decreases in market pricing.…

Further, our average selling prices and gross margins tend to decline when there is a meaningful shift in the mix of product sales to lower priced products. We have faced declining gross margins relating to our business in the past, and may face potential gross margin pressures in the future, resulting from our average selling prices declining more rapidly than our cost of revenue. Rapid technological changes have reduced, and may reduce in the future, the volume and profitability of sales of existing products and increase the risk of inventory obsolescence and write-downs. Finally, the semiconductor memory chip and data storage industries have experienced consolidation over the past several years, which could enhance the resources and lower the cost structure of some competitors. These factors could result in a substantial decrease in our market share and harm our business.

As we compete in new product areas, the overall complexity of our business may increase and may result in increases in research and development expenses and substantial investments in manufacturing capability, technology enhancements and go-to-market capability. We must also qualify our products with customers through potentially lengthy testing processes with uncertain results. Some of our competitors offer products that we do not offer (including DRAM), which may allow them to win sales from us or to more efficiently maintain product availability, pricing, and margins on products that incorporate DRAM, such as enterprise-grade SSDs. Some of our customers may also be developing storage solutions internally, which may reduce their demand for our products or shift their demand to potentially lower-margin component products. We expect that competition will continue to be intense, and our competitors may be able to gain a product offering or cost structure advantage over us, which would harm our business. Further, our competitors may utilize pricing strategies, including through aggressive expansion of their output capacities, which may allow them to offer products at prices at levels that we may be unable to competitively match.

The variety and volume of products we manufacture are based in part on accurately forecasting market and customer demand for our products. While multi-year agreements with certain customers provide increased visibility into future demand and may reduce forecasting uncertainty for portions of our business, our ability, as well as our customers’ and suppliers’ ability, to accurately forecast demand, remains difficult due to volatility in global economic conditions, evolving end market dynamics, customer deployment schedules, and industry consolidation. Further, for many of our OEM customers utilizing just-in-time inventory, we do not generally require firm order commitments and instead receive a periodic forecast of requirements, which may prove to be inaccurate. In addition, because our products are designed to be largely interchangeable with competitors’ products, our demand forecasts may be impacted significantly by the strategic actions of our competitors. Inaccurate demand forecasts could result in periods of product oversupply or undersupply, with the consequences described above under the “We rely substantially on strategic relationships with various partners, including Kioxia” and “We participate in a highly competitive industry” risk factors.…

Also, the storage ecosystem is constantly evolving, and our traditional customer base is changing. Fewer companies now hold greater market share for certain applications and services, such as cloud storage and computing platforms, mobile, social media, shopping and streaming media. As a result, the competitive landscape is changing, giving these companies increased leverage in negotiating prices and other terms of sale, which could negatively impact our profitability. In addition, the changes in our evolving customer base create new selling and distribution patterns to which we must adapt. To remain competitive, we must respond to these changes by ensuring we have proper scale in this evolving market, as well as offer products that meet the technological requirements of this customer base at competitive pricing points. To the extent we are not successful in adequately responding to these changes, our operating results and financial condition could be harmed.

Our success depends, in significant part, on the proprietary nature of our technology, including non-patentable intellectual property such as our process technology. If we fail to protect our technology, intellectual property or contract rights, our customers and others may seek to use our technology and intellectual property without the payment of license fees and royalties, which could weaken our competitive position, reduce our operating results and increase the likelihood of costly litigation. We primarily rely on patent, copyright, trademark and trade secret laws, as well as non-disclosure agreements and other methods, to protect our proprietary technologies and processes. There can be no assurance that our existing patents will continue to be held valid, if challenged, or that they will have sufficient scope or strength to protect us. It is also possible that competitors or other unauthorized third parties may obtain, copy, use or disclose, illegally or otherwise, our proprietary technologies and processes, despite our efforts to protect our proprietary technologies and processes. If a competitor is able to reproduce or otherwise capitalize on our technology despite the safeguards we have in place, it may be difficult, expensive or impossible for us to obtain necessary legal protection. There are entities whom we believe may infringe our IP. Enforcement of our rights often requires litigation.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
