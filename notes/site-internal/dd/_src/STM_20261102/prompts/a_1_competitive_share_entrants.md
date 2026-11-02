你是 stock-analyst v20 DD 的證據採集子 agent。標的：STM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - STM STMicroelectronics market share gaining OR losing 2026
  - STMicroelectronics new entrant OR displace threat Semiconductors 2026
  - STM competitor design win 2026
  - STMicroelectronics vs Semiconductors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
•We may not be able to match our production capacity to demand. •Competition in the semiconductor industry is intense, and we may not be able to compete successfully if our product design technologies, process technologies and products do not meet market requirements. Furthermore, the competitive environment of the industry has resulted, and is expected to continue to result, in vertical and horizontal consolidation among our suppliers, competitors and customers, which may lead to erosion of our market share, impact our ability to compete and require us to restructure our operations.

Competition in the semiconductor industry is intense, and we may not be able to compete successfully if our product design technologies, process technologies and products do not meet market requirements. Furthermore, the competitive environment of the industry has resulted, and is expected to continue to result, in vertical and horizontal consolidation among our suppliers, competitors and customers, which may lead to erosion of our market share, impact our ability to compete and require us to restructure our operations.

We compete in different product lines to various degrees on certain characteristics, for example, price, technical performance, product features, product design, product availability, process technology, manufacturing capabilities and sales and technical support. Given the intense competition in the semiconductor industry, if our products do not meet market requirements based on any of these characteristics, our business, financial condition and results of operations could be materially adversely affected. Our competitors may, among others, have a stronger presence in key markets and geographic regions, greater name recognition, larger customer bases, greater government support and greater financial, R&D, sales and marketing, manufacturing, distribution and technical resources 16 than us. These competitors may be able to adapt more quickly to changes in the business environment, to new or emerging technologies and to changes in customer requirements.

The semiconductor industry is intensely competitive and characterized by the high costs associated with developing marketable products and manufacturing technologies as well as high levels of investment in production capabilities. As a result, the semiconductor industry has experienced, and is expected to continue to experience, significant vertical and horizontal consolidation among our suppliers, competitors and customers. Market consolidation initiatives, planned restructurings, and any other such actions in the semiconductor industry may be subject to stricter regulations in the jurisdictions in which we operate, which could erode our market share, negatively impact our ability to compete and require us to increase our R&D effort, engage in mergers and acquisitions and/or restructure our operations.

In recent years, some of our customers have vertically integrated their businesses. Such vertical integrations may impact our business. Our relationships with the newly formed entities could be either reinforced or jeopardized by the integration. If we are unable to maintain or increase our market share with our key customers or distributors, or if they were to increase product returns or fail to meet payment obligations, our results of operations could be materially adversely affected.

Our industry adapts to technological advancements and it is likely that new products, equipment, processes and service methods, including transformation initiatives related to digitalization, are in the process of being implemented. Any failure by us to manage our data governance processes could undermine our digitalization initiatives, and any failure by us to react to changes or advances in existing technologies and processes as we develop and invest in our product, technology and transformation roadmaps could materially delay the introduction of new solutions. If we are not able to execute on these roadmaps, including our digitalization strategies, on a timely basis or at an acceptable cost this could result in loss of competitiveness of our solutions, decreased revenue and a loss of market share.

Such collaboration provides us with a number of important benefits, including the sharing of costs, reductions in our own capital requirements, acquisitions of technical know-how and access to additional production capacities. However, there can be no assurance that our collaboration efforts will be successful and allow us to develop and access new technologies in due time, in a cost-effective manner and/or to meet customer demands. If a particular collaboration terminates before our intended goals are accomplished we may incur additional unforeseen costs, and our business and prospects could be adversely affected. Furthermore, if we are unable to develop or otherwise access new technologies, whether independently or in collaboration with another industry participant, we may fail to keep pace with the rapid technology advances in the semiconductor industry, our participation in the overall semiconductor industry may decrease and we may also lose market share.

We depend on patents and other IP rights to protect our products and our manufacturing processes against misappropriation by others. The process of seeking patent protection can be long and expensive, and there can be no assurance that we will receive patents from currently pending or future applications. Even if patents are issued, they may not be of sufficient scope or strength to provide meaningful protection or any commercial advantage. In addition, effective IP protection may be unavailable or limited in some countries. Our ability to enforce one or more of our patents could be adversely affected by changes in patent laws, laws in certain foreign jurisdictions that may not effectively protect our IP rights or by ineffective enforcement of laws in such jurisdictions. Competitors may also develop technologies that are protected by patents and other IP and therefore either be unavailable to us or be made available to us subject to adverse terms and conditions. We have in the past used our patent portfolio to negotiate broad patent cross-licenses with many of our competitors enabling us to design, manufacture and sell semiconductor products, without concern of infringing patents held by such competitors.…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
Sales, Marketing and Distribution Our sales and marketing is organized by a combination of key accounts and regional sales units organized by market segment with the primary objective of accelerating sales growth and gaining market share. Emphasis is placed on strengthening the development of our global and major local accounts; boosting demand creation through an enhanced focus on geographical and key accounts coverage with strong technical and application expertise, supported application labs and competence centers. The mass market is covered through a joint effort with our distribution partners and local initiatives; establishing regional sales and marketing teams that are fully aligned with our end-markets and products strategies across our focused market segments: Automotive, Industrial Power and Energy, Industrial Smart industrials, Personal Electronics and Communications Equipment, Computers and Peripherals.

We have four regional sales organizations reporting to a global head of sales & marketing: Americas, Asia Pacific excluding China ("APeC"), China, and Europe, Middle-East and Africa ("EMEA"). Our regional sales organizations have a similar structure to enhance global coordination and go-to-market activities. The sales and marketing teams are strongly focused on profitable revenue growth and business performance as well as on fostering demand creation, expanding the customer base, expanding products usage in customer applications (cross selling) and maximizing market share, anticipating new products needs and providing the best technical and application support in the field for our customers. The sales and marketing activities are supported by sales engineers, system marketing, product and technical marketing, application labs, competence centers, field application engineers and quality engineers.

Competition Markets for our products are intensely competitive. We compete with major international semiconductor companies and while only a few companies compete with us in all of our product lines, we face significant competition from each of them. Smaller niche companies are also increasing their participation in the semiconductor market, and semiconductor foundry companies have expanded significantly, particularly in Asia. Competitors include manufacturers of standard semiconductor devices, ASICs and fully customized ICs, including both chip and board-level products, as well as customers who develop their own IC products and foundry operations. Some of our competitors are also our customers or suppliers. We compete in different product lines to various degrees on the basis of price, technical performance, product features, product system compatibility, customized design, availability, quality and sales and technical support. In particular, standard products may involve greater risk of competitive pricing, inventory imbalances and severe market fluctuations than differentiated products. Our ability to compete successfully depends on factors both within and outside our control, including successful and timely development of new products and manufacturing processes, product performance and quality, manufacturing yields and product availability, customer service, pricing, industry trends and general economic trends.

The semiconductor industry is characterized by the high costs associated with developing marketable products and manufacturing technologies as well as high levels of investment in production capabilities. As a result, the semiconductor industry has experienced, and is expected to continue to experience, significant vertical and horizontal consolidation among our suppliers, competitors and customers, which could lead to erosion of our market share, impact our capacity to compete and require us to restructure our operations. See “Item 3. Key Information — Risk Factors”.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
