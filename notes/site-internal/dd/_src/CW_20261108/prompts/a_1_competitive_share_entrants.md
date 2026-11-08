你是 stock-analyst v20 DD 的證據採集子 agent。標的：CW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - CW Curtiss-Wright market share gaining OR losing 2026
  - Curtiss-Wright new entrant OR displace threat Specialty Defense + Commercial Nuclear 2026
  - CW competitor design win 2026
  - Curtiss-Wright vs Specialty Defense + Commercial Nuclear peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm｜as_of：2026-02-12
<<<
Curtiss-Wright maintains a unique presence on high-performance platforms and critical applications that require our technical sophistication, and we benefit from decades of engineering expertise and knowledge transfer. Curtiss-Wright has been involved in numerous “firsts” in the industry, and since the origin of many of our markets, including commercial aerospace (our history dates back to the Wright Brothers and their historical first manned flight), naval nuclear power (presence on the first nuclear naval vessel), commercial power (our products were utilized in the first commercial nuclear power plant), and defense electronics (use of commercial off-the-shelf ("COTS") electronics in military applications). Today, we maintain competitive positions in the majority of our key A&D and commercial end markets through engineering and technological leadership, precision manufacturing, and long-standing customer relationships where we are deeply embedded in our customers' workflows. We are committed to continuously driving innovation and investment in technologies, while also aligning our core competencies with new applications and evolving market trends. Our investments typically target the fastest growth vectors and secular trends that align with our strengths in attractive end markets.

4 Our portfolio of highly competitive technologies is relied upon to improve safety, operating efficiency, and reliability, while meeting performance requirements in the most demanding environments. Our products are often in must-not-fail safety-critical applications. Our ability to provide mission critical, niche products and services on a cost-effective basis is fundamental to our strategy to drive increased value to our customers, which include defense prime contractors, commercial aerospace original equipment manufacturers ("OEMs"), and numerous energy and manufacturing companies. We compete globally, primarily based on technology and pricing.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/26324/000162828026007587/cw-20251231.htm｜as_of：2026-02-12
<<<
The commercial and government markets in which we operate are characterized by rapidly changing technologies. In addition, product and program needs of our government and commercial customers change and evolve regularly. Accordingly, to remain competitive in the future, we will need to continue to invest financial resources, including through internal research and development, acquisitions, or other teaming arrangements, to: (a) identify emerging technological trends in our current and target markets; (b) develop and manufacture competitive products, systems, and services; (c) enhance our offerings by adding technological innovations that differentiate our products, systems, and services from those of our competitors; and (d) develop, manufacture, and bring those products, systems, and service to market quickly at cost-effective prices. These expenditures could divert our attention and resources from other projects, and we cannot be sure that these expenditures will ultimately lead to the timely development of new offerings and technologies or identification of and expansion into new markets. Due to the design complexity of our products, we may, in the future, experience delays in completing the development and introduction of new products. Any delays could result in increased costs of development or deflect resources from other projects.…

We operate in highly competitive markets. Many of our products and services are sold in highly competitive markets, and are affected by varying degrees of competition, including competition for hiring and retaining skilled labor. We compete against companies that often have higher sales volumes and greater financial, technological, research and development, human, and marketing resources, and larger customer bases than we have. These companies may also price their products and services below our selling prices, which could exert downward pressure on our product pricing and margins. As a result, they may be better able to withstand the effects of periodic economic downturns. In addition, some of our largest customers could develop the capability to manufacture products or provide services similar to products that we manufacture or services that we provide. This would result in these customers supplying their own products or services and competing directly with us for sales of these products or services, all of which could significantly reduce our revenues. Furthermore, we are facing increased international competition and cross-border consolidation of competition. If consolidation of our competition continues to occur, we would expect the competitive pressures we face to increase.…

As of December 31, 2025, we had approximately $1.0 billion of debt outstanding. Our level of debt and debt servicing costs associated with that indebtedness, in part because of increases in interest rates on variable rate indebtedness under our revolving credit facility, could have significant consequences for our business. For example, our indebtedness could require us to use a substantial portion of our cash flows from operations to pay the principal and interest on our debt, thereby reducing funds available for working capital, acquisitions, dividends, capital expenditures, and other investments in our business, including investments in technology and research and development; make us vulnerable to economic downturns and increases in interest rates; limit us from obtaining additional debt; limit our flexibility in planning for, or reacting to, changes in the industries in which we compete; and place us at a competitive disadvantage compared to our competitors, some of whom have lower debt service obligations and greater financial resource than we do. In addition, most of our debt arrangements require us to maintain certain debt and interest coverage ratios and limit our ability to incur debt, make investments or undertake certain other business activities. These requirements could limit our ability to obtain future financing and may prevent us from taking advantage of attractive business opportunities.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
