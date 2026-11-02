你是 stock-analyst v20 DD 的證據採集子 agent。標的：FLEX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - FLEX Flex market share gaining OR losing 2026
  - Flex new entrant OR displace threat Electronic Components (EMS) 2026
  - FLEX competitor design win 2026
  - Flex vs Electronic Components (EMS) peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
Power, thermal, and compute infrastructure capabilities. As part of our service offerings, we support the design, manufacture, and lifecycle management of a range of power, thermal, and compute infrastructure products used for AI data centers and mission-critical applications. These offerings are delivered through our integrated design and engineering, supply chain, manufacturing, and aftermarket services. Our capabilities in this area include: •Critical power products •Embedded power products •Thermal management products •Compute and rack‑level infrastructure COMPETITION The contract manufacturing services market is competitive. Flex competes against numerous domestic and foreign manufacturing service providers, as well as current and prospective customers.

In each of the countries where we have operations, our comprehensive benefit plans offer a locally competitive mix of some or all of the following: medical, dental and vision insurance, short and long-term disability, flexible spending accounts, various types of voluntary coverage, and other benefit programs. We routinely benchmark our salaries and benefits against market peers to ensure our total rewards package remains competitive.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm｜as_of：2026-05-20
<<<
Sales to our ten largest customers represent a significant percentage of our net sales. Our ten largest customers accounted for 45%, 44% and 37% of net sales in fiscal years 2026, 2025 and 2024, respectively. No customer accounted for more than 10% of net sales in fiscal year 2026, 2025 or 2024. Our principal customers have varied from year to year. Customers have in the past experienced, and could in the future experience, dramatic declines in their market shares, competitive position, or demand for their products and services, due to economic or other forces, that may cause them to reduce their purchases from us or, in some cases, result in the termination of their relationship with us. Significant reductions in sales to any of our largest customers, or the loss of major customers, have in the past harmed, and could in the future materially harm, our business, results of operations, cash flows, and financial condition. If we are not able to replace expired, canceled or reduced contracts with new business in a timely manner, including due to qualification, ramp‑up or customer approval requirements, our revenues and profitability would be harmed.…

Our success depends on our ability to attract, develop, motivate and retain a workforce with the skills necessary for our business, including qualified executives, management, engineering, manufacturing, information technology, cybersecurity, supply chain, and business development personnel. The market for such talent is highly competitive, and we may incur higher labor, recruiting and training costs in order to attract and retain employees with the requisite skills. If our compensation, benefits and overall employee value proposition are not viewed as competitive, our ability to attract, motivate and retain key employees could be weakened. Generally, our employees are not bound by employment or non-competition agreements, and where such agreements exist, they may be difficult to enforce. We cannot assure you that we will retain our executive officers and key employees.

Industry Risks We depend on industries that produce products that are subject to rapid technological change and short product lifecycles, and our business has in the past been, and could in the future be, adversely affected if our customers' products are not successful or if our customers lose market share.

We derive our revenue from customers in a number of end markets and factors affecting any of these industries in general, or our customers in particular, could adversely impact us. These factors include rapid changes in technology, including as a result of AI, evolving industry standards, and requirements for continuous improvement in products and services that result in short product lifecycles; the failure of our customers to successfully market their products or for our customers' products to gain widespread commercial acceptance; and dramatic market share shifts that may cause our customers to lose market share or exit businesses.

We compete with a number of different companies, depending on the type of service we provide or the location of our operations. For example, we compete with major global EMS providers, other smaller EMS companies that have a regional or product-specific focus and Original Design Manufacturers ("ODMs") with respect to some of the services that we provide. We also compete with our current and prospective customers, who evaluate our capabilities in light of their own capabilities, cost structures and strategic priorities. In the past, some of our customers moved a portion of their manufacturing away from us in order to more fully utilize their excess internal manufacturing capacity, and customers could in the future decide to in-source, dual‑source, regionalize, or otherwise reallocate manufacturing volumes among suppliers. Any of these developments could cause a decline in our sales, loss of market acceptance of our products or services, decreases of our profits, or loss of our market share. Our industry is extremely competitive, many of our competitors have achieved substantial market share, and some may have lower cost structures or greater design, manufacturing, financial or other resources than we do, including the ability to deploy capital at greater scale to support capacity expansion, advanced manufacturing technologies, or significant upfront investments required by certain power and components programs.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
