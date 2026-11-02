你是 stock-analyst v20 DD 的證據採集子 agent。標的：SIMO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - SIMO Silicon Motion Technology market share gaining OR losing 2026
  - Silicon Motion Technology new entrant OR displace threat Semiconductors 2026
  - SIMO competitor design win 2026
  - Silicon Motion Technology vs Semiconductors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-04-30）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm｜as_of：2026-04-30
<<<
To ensure the availability of our products for our customers, we generally instruct our foundries to begin manufacturing our products based on forecasts provided by these customers in advance of receiving purchase orders and procure NAND for our SSD solutions products. However, these forecasts do not represent binding purchase commitments, and sales of our products are only recognized when they are shipped with ownership transferred to the customer. As a result, we incur inventory and manufacturing costs in advance of anticipated revenue. Because demand for our products may not materialize, manufacturing based on forecasts subjects us to risks of high inventory carrying costs and increased obsolescence and may increase our costs. If we overestimate customer demand for our products or if purchase orders are cancelled or shipments delayed, we may end up with excess or obsolete inventory, which could have a material and adverse effect on our financial results. The risk of obsolescence and/or excess inventory is heightened for devices designed for consumer electronics due to short product lifecycles for these types of products. Conversely, if we underestimate demand or if insufficient 7 Table of Contents manufacturing capacity is available, we may not have sufficient product inventory, which could lead to missed revenue opportunities, loss of market share, damages to our customer relationships and other harm to our business.…

The market for storage devices using NAND flash components has experienced rapid technological changes, could be subject to industry consolidation and could face competition from new technologies. NAND flash technology will continue to evolve rapidly with continued cost reductions, which could lead to new types of solid-state storage devices, new applications and new categories of customers and market segments where we could be comparatively disadvantaged. The market for solid-state storage devices is relatively fragmented with 8 Table of Contents many suppliers that include NAND flash makers, module makers and OEMs, and if the market were to consolidate, a trend experienced by other parts of the semiconductor and storage industries, we could face changing demand for our products, replacement of our products by those of our competitors or internal captive sources and reduced market opportunities. If solid state storage devices were to use other types of non-volatile memory technologies other than NAND flash and we do not have relevant and competitive controller technology, our addressable market for controllers could shrink.

Our success depends to a significant extent on the development, qualification, implementation and acceptance of new product designs and improvements that provide value to our customers. Our ability to develop, qualify and distribute, and have manufactured, new products and related technologies to meet evolving industry requirements, at prices acceptable to our customers and on a timely basis are significant factors in determining our competitiveness in our target markets. For example, for our products addressing the SSD market, we must successfully identify customer requirements and design, develop and produce products on time that compete effectively as to price, functionality and performance. We sell products in markets that are characterized by rapid technological change, evolving industry standards, frequent new product introductions, smaller process geometries and other factors. We cannot assure you that our efforts to execute our product roadmap will result in innovative products and technologies that provide value to our customers. If we fail to or are delayed in developing, qualifying or shipping new products or technologies that provide value to our customers, and address these new trends and adjust our business accordingly, we may lose competitive positioning, which could cause us to lose market share and require us to discount the selling prices of our products.…

The controllers we develop and sell are used for high volume applications and their average selling prices have historically decreased over time, and we believe that it is possible they may also fall in the future. We may experience period-to-period fluctuations in future operating results if our average selling prices decline. We may be forced to reduce the average unit price of our products in response to new product introductions by our competitors, competitive pricing pressures and other factors. Also, we often provide large customers with volume-related, price-discount incentives relating to their orders of specific products; if customer procurements that benefit from these incentives scale significantly, they could lead to downward pressure on our gross margins. The mobile and computing devices markets are extremely competitive, which may result in rapidly declining average selling prices of electronic devices and components, such as those made by us, and create downward pressure on our average selling prices and operating results. To maintain acceptable operating results, we will need to develop and introduce new products and product enhancements on a timely basis and continue to reduce our costs.…

Because the markets in which we operate are highly competitive and many of our competitors have greater resources than we have, we cannot be certain that our products will compete favorably in the marketplace.

We face competition from several competitors, including Microchip and Phison, our flash memory customers and smaller merchant suppliers in China. We expect to face competition in the future from our current and potential competitors. In addition, some of our flash memory customers could develop products and technologies that replace their need for our products or otherwise reduce their demand for our products.

Some of our current and potential competitors have longer operating histories, greater name recognition, access to larger customer bases and significantly greater financial, sales and marketing, manufacturing, distribution, technical and other resources than we have. As a result, they may be able to respond more quickly to changing customer demands or to devote greater resources to the development, promotion and sales of their products than we can. Our current and potential competitors may develop and introduce new products that will be 16 Table of Contents priced lower, provide superior performance or achieve greater market acceptance than our products. For our SSD solutions, if we are unable to procure sufficient supplies of NAND flash components and at terms that enable our products to be competitive in terms of price or develop technologically competitive products, our customers may seek to purchase SSD solutions from other suppliers.

We rely heavily on the services of our key employees, including Wallace C. Kou, our President and Chief Executive Officer. In addition, our engineers and other highly skilled personnel are a significant asset and are the source of our technological and product innovations. We believe our future success will depend upon our ability to attract and retain skilled managerial, engineering and sales and marketing personnel. The competition for such personnel, particularly engineering personnel, is intense in our industry. We may not be successful in attracting and retaining engineering personnel to support our anticipated growth. These personnel are required to design and develop ICs, including firmware, and to introduce product enhancements for use in future applications. Despite the incentives we provide, our current employees may not continue to work for us, and if additional personnel are required for our operations, we may not be able to obtain the services of additional personnel necessary for our growth. In addition, we do not maintain “key person” life insurance for any of our senior executives or other key employees.…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-04-30）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm｜as_of：2026-04-30
<<<
Competition We face competition from multiple competitors, including Microchip and Phison, our flash memory customers’ internal captive developments and small Chinese merchant controller suppliers.

The markets for our products are intensely competitive, and are characterized by rapid technological change, evolving industry standards, frequent new product introductions and pricing pressures. Competition has intensified due to the increasing demand for higher levels of performance at competitive prices. We expect competition to intensify further as current competitors continue to strengthen the depth and breadth of their product offerings and additionally, our competitors in China have benefited from the government’s semiconductor localization policies. We believe that our ability to compete successfully in the rapidly evolving markets for our products depends on several factors, including, but not limited to: • the performance, features, quality and price of our products; • the timing and success of new product introductions by us, our customers and our competitors; • emergence, rate of adoption and acceptance of new industry standards; • our ability to obtain adequate foundry capacity at competitive prices; and • the number and nature of our competitors in specific market sub-segments.

While our ability to effectively compete depends in large part on our ability to protect our intellectual property, we believe that our technical expertise, customer support capabilities, and ability to introduce new products in a timely and cost-effective manner will be important factors in maintaining our competitive position.

We expect increased competition in the future from emerging or established companies, customers or other third parties, any of which could acquire significant market share. See “Risk Factors — Because the markets in which we operate are highly competitive and many of our competitors have greater resources than we have, we cannot be certain that our products will compete favorably in the marketplace” in Item 3 above.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
