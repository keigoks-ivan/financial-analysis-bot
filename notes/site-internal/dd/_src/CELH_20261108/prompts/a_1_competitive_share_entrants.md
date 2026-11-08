你是 stock-analyst v20 DD 的證據採集子 agent。標的：CELH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - CELH Celsius Holdings market share gaining OR losing 2026
  - Celsius Holdings new entrant OR displace threat Beverages - Non-Alcoholic 2026
  - CELH competitor design win 2026
  - Celsius Holdings vs Beverages - Non-Alcoholic peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm｜as_of：2026-03-02
<<<
Competition Our products compete broadly with not only functional energy drinks, but all categories of non-alcoholic liquid refreshments. The functional energy drink and liquid refreshment sectors are highly competitive and include international, national, regional and local producers and distributors. Our direct competitors in the functional energy drink sector include but are not limited to Monster Beverage Corporation, Red Bull GmbH, The Coca-Cola Company, Pepsi, Keurig Dr Pepper Inc., Nestlé S.A., BlueTriton Brands, Starbucks Corporation, Congo Brands and Molson Coors.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm｜as_of：2026-03-02
<<<
Our advertising, labeling and promotional activities are subject to a wide range of laws and regulations in the jurisdictions in which our products are sold. In the U.S. our advertising activities are subject to regulation by the FTC under the Federal Trade Commission Act. In addition, our advertising and promotional activities are subject to state consumer protection and unfair competition laws, including laws such as California’s Consumer Legal Remedies Act and Unfair Competition Law. Outside the U.S., our advertising and promotional activities are subject to comparable consumer protection, unfair competition and misleading or deceptive conduct laws administered by governmental authorities in the jurisdictions in which we operate. Any actions or investigations initiated against our business by governmental authorities or private litigants could have a material adverse effect on our business, financial condition, results of operations and cash flows.

We rely on our management team and other key personnel. We depend on the skills, experience, relationships and continued services of key personnel, including our experienced management team. In addition, our ability to achieve our operating goals also depends on our ability to recruit, train and retain qualified individuals. We compete with other companies both within and outside of our industry for talented personnel and we may lose key personnel or fail to attract and retain additional talented personnel. Any such loss or failure could have a material adverse effect on our business, financial condition, results of operations and cash flows.

Our business requires that we attract, develop and maintain a highly skilled and diverse workforce. Our employees are highly sought after by our competitors and other companies and competition for existing and prospective personnel has increased. Our continued ability to compete effectively depends on our ability to attract, retain, develop and motivate highly skilled personnel for all areas of our organization. Moreover, the broader labor market continues to be impacted by numerous factors, including, but not limited to, wage inflation, labor shortages, increased employee turnover, changes in availability and a shift toward remote work, which, in turn, has created a shortage of qualified workers, thereby further increasing the competitive landscape of attracting and retaining qualified workers.

The functional beverage product industry is highly competitive. The principal areas of competition are pricing, packaging, distribution channel penetration, development of new products and flavors and marketing campaigns. Our products compete with a wide range of beverages produced by a relatively large number of manufacturers, some of which have substantially greater financial, marketing and distribution resources and name recognition than we do.

Due to competition in the functional beverage product industry, we may encounter difficulties in maintaining our current revenues, market share or position within this industry, any of which could have a material adverse effect on our business, financial condition, results of operations and cash flows.

Following termination, a former distributor may have increased capacity, shelf space, sales focus and operational resources available to support other brands, including our competitors. As a result, such distributors may choose to scale, prioritize, or expand distribution of competing products, including brands that directly compete with ours, within the same markets or channels. This could strengthen competitors’ market positions and intensify competitive pressures against us, which may adversely affect our sales, market share, and relationships with other distributors or retail partners. Any of these factors could have a material adverse effect on our business, results of operations and financial condition.

Our ability to compete in the highly competitive functional beverage product industry and to achieve our business growth objectives depends, in part, on our ability to develop new flavors, products and packaging. The success of our innovation, in turn, depends on our ability to identify consumer trends and cater to consumer preferences. In addition, if we fail to adequately differentiate our products from those of our competitors, we may lose market share and pricing power and fail to attract or retain loyal customers. The increasing number of competing products and limited shelf space in retail outlets may further limit our ability to establish and maintain a distinctive market position. If we are not successful in our innovation activities, we could experience a material adverse effect on our business, financial condition, results of operations and cash flows.

Consumers are seeking greater variety in their functional beverage products. Our future success will depend, in part, upon our continued ability to develop and introduce different and innovative functional beverage products that appeal to consumers. In order to retain and expand our market share, we must continue to develop and introduce different and innovative products and be competitive in the areas of efficacy, taste, quality and price, although there can be no assurance of our ability to do so. There is no assurance that consumers will continue to purchase our products in the future. Product lifecycles for some functional beverage brands, products or packages may be limited to a few years before consumers’ preferences change. The functional beverage products that we currently market are in varying stages of their product lifecycles and there can be no assurance that such products will become or remain profitable for us. We may be unable to achieve volume growth through product and packaging initiatives. We may also be unable to penetrate new markets. Additionally, as shopping patterns are being affected by the digital evolution, with consumers embracing shopping by way of mobile device applications, e-commerce retailers and e-commerce websites or platforms, we may be unable to address or anticipate changes in consumer shopping preferences or engage with our consumers on their preferred platforms.…

Our portfolio, which includes Celsius®, Alani Nu®, and Rockstar®, competes in the highly competitive functional beverage product category. This category is subject to shifting consumer preferences, new product introductions, aggressive pricing and significant promotional activity by established and emerging brands. Any decline in sales of our functional beverage products or loss of market share in these categories, could materially adversely affect our future revenues and profitability.

18 The increasing number of competitive products and limited availability of shelf and cooler space in retail outlets may limit our ability to maintain or expand our market presence. Competitors may engage in aggressive marketing, offer price discounts or pursue false or misleading advertising claims that could impact our brand reputation and sales. In addition, competition from private-label and other wellness or performance brands could intensify. These competitive pressures may result in price erosion, reduced market share or increased promotional expenses, any of which could have a material adverse effect on our business, financial condition, results of operations and cash flows.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-02）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1341766/000134176626000024/celh-20251231.htm｜as_of：2026-03-02
<<<
Key Drivers of our Financial Success and Market Presence - Much of our financial success is dependent on our ability to market and connect with a diverse consumer base, including wellness-focused consumers, fitness enthusiasts and consumers looking for more functionality in their beverage consumption. We believe that our strategic marketing initiatives, aimed at different demographics and lifestyle segments, contribute to revenue growth and market share expansion. We continually adapt our marketing mix to align with changing consumer preferences, leveraging digital and social media channels for broader reach and engagement. Furthermore, we have designed our focus on product innovation to meet the evolving demands of health-conscious consumers, while maintaining appeal to a general consumer base seeking quality and convenience, thereby enhancing our competitive position and financial performance. Our approach is to create a brand experience that is both inclusive and appealing to a wide range of consumers, fostering loyalty and driving sustainable growth. We believe that our multifaceted approach is crucial for driving enduring revenue growth and maintaining a strong market presence in the energy drink industry.

Market Competition Risks The energy drink industry is characterized by intense competition, involving a diverse array of competitors with varying market strategies and product offerings. This includes well-established companies with strong brand recognition, as well as emerging competitors that may introduce innovative approaches or specialized products. The entry of new or strengthening competitors who employ aggressive pricing strategies can significantly impact our market share and profitability. Additionally, continuing shifts in consumer preferences towards healthier alternatives or different beverage categories could intensify competition as new entrants expand into our categories.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
