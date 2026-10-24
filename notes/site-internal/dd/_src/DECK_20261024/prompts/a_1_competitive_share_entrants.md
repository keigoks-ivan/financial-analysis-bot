你是 stock-analyst v20 DD 的證據採集子 agent。標的：DECK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - DECK market share gaining OR losing 2026
  - new entrant OR displace threat 2026
  - DECK competitor design win 2026
  - vs peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-22）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm｜as_of：2026-05-22
<<<
We have demonstrated a history of investing in our workforce by offering competitive salaries and wages. We provide tuition reimbursement for eligible US employees up to $5 thousand per calendar year. Further, to foster a stronger sense of ownership and align the interests of management with stockholders, equity awards are granted to a substantial proportion of our leadership team. In addition, employees across the US business have the opportunity to purchase stock at a discounted price through our Employee Stock Purchase Plan. Further, we engage an independent compensation consultant, FW Cook, which provides us with information to evaluate the effectiveness of our executive compensation program, including competitive pay practices and trends in our industry, the design and structure of our executive compensation program, and the formulation of and benchmarking against our peers within our industry.

Competition The industry and markets in which we operate are highly competitive. Our competitors include fashion, casual, lifestyle, and athletic footwear companies, branded apparel companies, and retailers with their own private labels.

Although the industry is fragmented, some of our competitors are larger and have substantially greater resources, and several sell products that compete directly with our products. In particular, we face competition from domestic and international competitors selling products designed to compete directly or indirectly with products similar to those of our HOKA brand and UGG brand. In addition, access to offshore manufacturing and the growth of e- commerce have made it easier for new companies to enter the markets in which we compete, further increasing competition in the footwear, apparel, and accessories industry.

We believe our ability to successfully compete depends on numerous factors, including our ability to predict, assess, and respond quickly to changing consumer tastes and preferences, produce exceptional and innovative products that meet expectations for product craft, quality and technical performance, maintain and enhance the image and strength of our brands, price our products competitively, and manage the impacts of supply chain disruptions. In addition, we believe our key customers face intense competition from other department stores, sporting goods stores, retail specialty stores, and online retailers, among others, which could negatively impact the financial stability of their businesses and their ability to conduct business with us. Refer to Part I, Item 1A, “Risk Factors,” within this Annual Report for further discussion of the potential impact of competition on our business.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-22）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm｜as_of：2026-05-22
<<<
We face intense competition from both established companies and newer entrants into the market, and our failure to compete effectively could cause our market share to decline, which could harm our reputation and have a material adverse effect on our financial condition and results of operations.

The footwear, apparel, and accessories industry is highly competitive and subject to rapidly changing consumer preferences. If we are unable to compete effectively, we could experience a decline in market share, reduced demand for our products, pricing pressure, or damage to our reputation, which could have a material adverse effect on our financial condition and results of operations. Competition in our markets is influenced by factors such as Table of Contents 14 brand recognition, product innovation and performance, pricing, speed‑to‑market, marketing effectiveness, use of data analytics and AI, access to manufacturing capacity, and control of distribution channels.

Our competitors include both established global brands and newer market entrants, including competitors whose broader product assortments and higher sales volumes may be more important to certain customers. We believe that the growth and visibility of our HOKA brand and UGG brand have attracted competitors specifically targeting the categories in which we operate. Barriers to entry have been reduced by access to offshore manufacturing and evolving technologies, allowing competitors to develop and scale products more quickly and at lower cost.

Some of our competitors also have substantially greater financial, technological, manufacturing, marketing, and distribution resources than we do, as well as broader brand awareness, which may enable them to compete more effectively on price, accelerate product development, leverage advanced data analytics or AI, adapt to technological changes, and withstand periods of excess inventory or reduced consumer demand. As a result, we face ongoing competition for customer relationships and distribution channels, including competition for preferred access to key retail accounts, shelf space, and digital visibility.

Consistent with these dynamics, we have experienced, and expect to continue to experience, pricing and promotional pressure across our brands and channels, particularly during periods of elevated industry inventory levels or inflationary pressure. Increased discounting or promotional activity by competitors may require us to reduce prices or increase promotions to remain competitive, negatively affecting our gross margin and results of operations, and could cause consumers to shift purchases to competing products. In addition, many of our key wholesale customers face intense competitive pressures, and deterioration in their financial condition could adversely affect their ability to do business with us.

To execute our growth plan, we must continue to attract and retain highly qualified talent, including executive officers and key employees. In addition, to develop new products and successfully operate and grow our key business processes, we rely on employees with specialized expertise across design, marketing, merchandising, sourcing, technology, operations, and support functions, including talent in areas such as data analytics, digital commerce, and supply chain management. Competition for executive officers, key employees, and skilled talent is intense within our industry, and we continue to experience upward pressure on compensation costs. Changes to our Table of Contents 17 office environment or work models may not meet employees’ expectations, and many of the companies with which we compete for talent have greater name recognition and financial resources than we have. Continued strength in our results may also increase the risk that our employees are targeted by competitors. If our overall employment proposition, including compensation, benefits, culture, work model, or career development opportunities, is not perceived as favorable relative to other employers, our ability to attract, hire, and retain qualified personnel could be adversely affected. We are committed to offering competitive compensation and benefits, which may increase our selling, general, and administrative (SG&A) expenses.…

In particular, our HOKA brand maintains its competitiveness through continuous product innovation and timely introduction of new features and technologies that align with current and emerging consumer expectations, including our ability to bring such innovations to market ahead of or in line with competitors. Also, we continue to invest in research and development to increasingly incorporate recycled, renewable, regenerated, and certified/ natural materials (preferred materials) in our products as part of our sustainability efforts. We also increasingly use preferred synthetics, regenerated or synthetic cellulosic fibers, and plant fibers. Although we continue to refine our materials and develop new properties for specific applications, if we fail to introduce technical innovation in our products in a timely or commercially successful manner, or experience issues with the quality of our products or materials, consumer demand for our products could decline and we may experience reputational damage. In addition, if our competitors introduce superior or more cost-effective innovations, we may lose market share or be required to increase promotional activity to remain competitive. Further, as our brands transition to suppliers with preferred materials, we may be subject to increased costs or supply constraints, which could reduce our sales and profitability and have a material adverse effect on our financial condition and results of operations.…

Table of Contents 20 Additionally, we may not be able to successfully integrate acquired businesses into our operations or achieve the expected benefits of such acquisitions. We may also face cannibalization of existing product sales by newly acquired products unless we successfully differentiate target consumers and increase our overall market share.

Our business could be significantly harmed if we are not able to protect our intellectual property rights. We believe our competitive position is attributable to the value of our trademarks, patents, trade dress, trade names, trade secrets, copyrights, and other intellectual property rights. As a result of the success of our brands, we have become a target of counterfeiting and product imitation. Although we actively pursue legal and other actions against those who infringe on our intellectual property rights, we cannot guarantee that these actions will be adequate to protect our brands in the future, particularly because some countries’ laws do not protect these rights to the same extent as US laws. If we fail to adequately protect our intellectual property rights, it may allow competitors to sell products that are similar to and directly competitive with our products, or we could lose opportunities to sell our products to consumers who instead purchase counterfeit or imitation products, which could reduce sales of our products and adversely affect the value of our brands. In addition, any intellectual property lawsuits in which we are involved could require significant time and expense and distract management’s attention from operating our business, which may negatively affect our business and results of operations.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
