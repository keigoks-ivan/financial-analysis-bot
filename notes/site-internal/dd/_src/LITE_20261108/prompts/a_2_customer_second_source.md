你是 stock-analyst v20 DD 的證據採集子 agent。標的：LITE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_second_source] 客戶 second-source 與 in-house
Q: 最大客戶是否正在導入第二供應商，或將此環節自製（in-house）？
  - LITE Lumentum Holdings largest customer second-source OR in-house 2026
  - custom chip OR component second source agreement 2026
  - Lumentum Holdings single-source risk customer diversify supplier
  - in-house design OR insourcing Communication Equipment 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm｜as_of：2026-08-17
<<<
We purchase raw materials, packages and components from a limited number of suppliers, who are often small and specialized. Additionally, some of our suppliers are our sole sources for certain materials, equipment and components. We depend on the timely and continued supply and quality of the materials, packages and components that our suppliers supply to us. While we have entered into advanced payments to secure orders from some of these suppliers, we have not entered into long-term agreements with many of these suppliers. We do not have a guarantee of supply from many of these suppliers and, as a result, there is no assurance that we would be able to secure the equipment or components that we require, in sufficient quantity, quality and on reasonable terms. Our business and results of operations have been, and could continue to be, adversely affected by this dependency. Alternative sources to mitigate the risk that the failure of any sole supplier will adversely affect our business are not feasible in all circumstances.…

In addition, changes in the business requirements, vendor selection, project prioritization, financial prospects, capital resources, and expenditures, or purchasing behavior (including product mix purchased or timing of purchases) of our key customers, or any real or perceived quality issues related to the products that we sell to such customers, have led to decreased sales to such customers or delays or cancellations of planned purchases of our products or services, which has unfavorably impacted our revenues and operating results, and may continue to impact our business and results of operations. We may also experience pricing pressure with certain of our customers that may adversely affect our revenue and margins, or, if the ongoing relationship no longer benefits us, we may decide to suspend or terminate our relationship with such customers. There are also continuing trade tensions, including an uncertain regulatory environment, in the U.S. and countries in Asia, and in particular, China, which have impacted and could continue to materially impact our sales to key customers in these regions. Further, we may be required to purchase raw materials, increase production capacity or make other changes to our business to accommodate certain large customers.…

The end markets for optical products have experienced significant industry consolidation during the past few years. We expect this trend to continue as companies attempt to strengthen or hold their market positions in an evolving industry and as companies are acquired or are unable to continue operations. As a result, the markets for optical subsystems, components and laser diodes are highly competitive and the intensity of such competition is increasing. Our current competitors include a number of domestic and international public and private companies, many of which may have substantially greater financial, technical, marketing and distribution resources and brand name recognition than we have. As we expand into new markets, we face competition not only from our existing competitors, but also from new competitors, including existing companies with strong technological and sales positions in those markets. We may not be able to compete successfully against either current or future competitors, particularly, in light of increasing consolidation. Our competitors may continue to enter markets or gain or retain market share through introduction of new or improved products or with aggressive low pricing strategies that may impact the efficacy of our approach. These competitors may be able to devote greater resources than we can to the development, promotion, sale and support of their products.…

We also rely on several independent contract manufacturers to supply us with certain products. For many products, a particular contract manufacturer may be the sole source of the finished good products. We depend on these manufacturers to meet our production and capacity requirements and to provide quality products to our customers. There are a number of risks associated with our reliance on contract manufacturers including: •reduced control over delivery schedules and planning; •availability of manufacturing capability and capacity, particularly during periods of high demand; •reliance on the quality assurance procedures of third parties; •risks associated with data security breaches or cyber-attacks targeting our contract manufacturers, including manufacturing disruptions or unauthorized access to information; and •potential misappropriation of our intellectual property.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/parts/axes_2.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
