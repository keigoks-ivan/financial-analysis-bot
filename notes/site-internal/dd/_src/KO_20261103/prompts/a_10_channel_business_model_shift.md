你是 stock-analyst v20 DD 的證據採集子 agent。標的：KO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - The Coca-Cola distribution channel disruption OR shift 2026
  - KO The Coca-Cola business model transition subscription OR platform 2026
  - Beverages - Non-Alcoholic channel disintermediation D2C 2026
  - The Coca-Cola go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm｜as_of：2026-02-20
<<<
We make our branded beverage products available to consumers throughout the world through our network of independent bottling partners, distributors, wholesalers and retailers as well as our consolidated bottling and distribution operations. Beverages bearing trademarks owned by or licensed to the Company account for 2.2 billion of the estimated 65 billion servings of all beverages consumed worldwide every day.

Our concentrate operations typically generate net operating revenues by selling beverage concentrates, sometimes referred to as “beverage bases,” syrups, including fountain syrups, and certain finished beverages to authorized bottling operations (to which we typically refer as our “bottlers” or our “bottling partners”). Our bottling partners combine concentrates with still or sparkling water and sweeteners (depending on the product), or combine syrups with still or sparkling water, to produce finished 3 beverages. The finished beverages are packaged in authorized containers, such as cans and refillable and nonrefillable glass and plastic bottles, bearing our trademarks or trademarks licensed to us and are then sold to retailers directly or, in some cases, through wholesalers or other bottlers. In addition, outside the United States, our bottling partners are typically authorized to manufacture fountain syrups, using our concentrates, which they sell to fountain retailers for use in producing beverages for immediate consumption, or to authorized fountain wholesalers who in turn sell and distribute the fountain syrups to fountain retailers. Our concentrate operations are included in our geographic operating segments.

Our finished product operations generate net operating revenues by selling sparkling soft drinks and a variety of other finished beverages to retailers, or to distributors and wholesalers who in turn sell the beverages to retailers. Generally, finished product operations generate higher net operating revenues but lower gross profit margins than concentrate operations. These operations consist primarily of our consolidated bottling and distribution operations, which are included in our Bottling Investments operating segment. In certain markets, the Company also operates non-bottling finished product operations in which we sell finished beverages to distributors and wholesalers that are generally not one of the Company’s bottling partners. These operations are generally included in our geographic operating segments. Additionally, we sell directly to consumers through retail stores operated by Costa. These sales are included in our EMEA operating segment, regardless of the physical location of the retail stores. In the United States, we manufacture fountain syrups and sell them to fountain retailers, who use the fountain syrups to produce beverages for immediate consumption, or to authorized fountain wholesalers or bottling partners who in turn sell and distribute the fountain syrups to fountain retailers. These fountain syrup sales are included in our North America operating segment.

In addition to the beverage brands we own, we also provide marketing support and otherwise participate in the sales of other beverage brands through licenses, joint ventures and strategic relationships. For example, certain Coca-Cola system bottlers distribute certain brands of Monster, primarily Monster Energy, in designated territories in the United States, Canada and other international territories pursuant to distribution coordination agreements between the Company and Monster and related distribution agreements between Monster and Coca-Cola system bottlers.

4 Distribution System We make our branded beverage products available to consumers in more than 200 countries and territories through our network of independent bottling partners, distributors, wholesalers and retailers as well as our consolidated bottling and distribution operations. For information about geographic and customer data, refer to Note 20 of Notes to Consolidated Financial Statements set forth in Part II, “Item 8. Financial Statements and Supplementary Data” of this report.

Our five largest independent bottling partners based on unit case volume in 2025 were as follows: •Coca-Cola FEMSA, S.A.B. de C.V. (“Coca-Cola FEMSA”), which has bottling and distribution operations in Mexico (a substantial part of central Mexico, as well as southeast and northeast Mexico), Guatemala, Colombia (most of the country), Nicaragua, Costa Rica, Panama, Venezuela, Uruguay, Brazil (a major part of the states of São Paulo and Minas Gerais; the states of Mato Grosso do Sul, Paraná, Rio Grande do Sul, and Santa Catarina; and part of the states of Goiás and Rio de Janeiro), and Argentina (federal capital of Buenos Aires and surrounding areas); •Coca-Cola Europacific Partners plc (“CCEP”), which has bottling and distribution operations in Andorra, Australia, Belgium, continental France, Germany, Great Britain, Iceland, Indonesia, Luxembourg, Monaco, the Netherlands, New Zealand and the Pacific Islands, Norway, Papua New Guinea, the Philippines, Portugal, Spain and Sweden; •Coca-Cola HBC AG (“CCHBC”), which has bottling and distribution operations in Armenia, Austria, Belarus, Bosnia and Herzegovina, Bulgaria, Croatia, Cyprus, the Czech Republic, Egypt, Estonia, Greece, Hungary, Italy, Latvia, Lithuania, Moldova, Montenegro, Nigeria, North Macedonia, Northern Ireland, Poland, the Republic of Ireland, Romania, Russia, Serbia, Slovakia, Slovenia, Switzerland and Ukraine; •Arca Continental, S.A.B.…

In certain parts of the world outside the United States, we have not granted comprehensive beverage production and distribution rights to the bottlers. In such instances, we have authorized certain bottlers to (1) prepare and package Company Trademark Beverages for sale to other bottlers, or (2) purchase Company Trademark Beverages from other bottlers for sale and distribution throughout their respective designated territories, often on a nonexclusive basis.

Competition The commercial beverage industry is highly competitive and consists of numerous companies, ranging from small or emerging to very large and well established. These include companies that, like our Company, compete globally in multiple geographic areas, as well as businesses that are primarily regional or local in operation. Competitive products include numerous nonalcoholic sparkling soft drinks; water products, including flavored and enhanced waters; juices, juice drinks and nectars; dilutables (including syrups and powders); coffees; teas; energy drinks; sports drinks; milk and other dairy-based drinks; plant-based beverages; functional beverages, including vitamin-based products and relaxation beverages; and various other nonalcoholic beverages. These competitive products are sold to consumers in both ready-to-drink and non-ready-to-drink form. The Company has directly entered the alcohol beverage category in numerous markets outside the United States. In the United States, the Company has established a wholly owned, indirect, firewalled subsidiary, which uses third-party manufacturers and distributors to produce, distribute and sell alcohol products in the United States and also authorizes alcohol-licensed third parties to use certain of our trademarks and related intellectual property on alcohol beverages that contain Company beverage bases. Competitive products include all alcohol ready-to-drink beverages containing various alcohol bases. In many of the countries in which we do business, PepsiCo, Inc. is a primary competitor.…

7 Our competitive strengths include leading brands with high levels of consumer recognition and loyalty; a worldwide network of bottlers and distributors of Company products; sophisticated marketing capabilities; and a talented group of dedicated employees. Our competitive challenges include strong competitors in all geographic regions; in many countries, a concentrated retail sector with powerful buyers able to freely choose among Company products, products of competitive beverage suppliers and individual retailers’ own store or private-label beverage brands; new industry entrants; and dramatic shifts in consumer shopping methods and patterns due to a rapidly evolving digital landscape.

We also own numerous trademarks that are very important to our business. Depending upon the jurisdiction, trademarks are valid as long as they are in use and/or their registrations are properly maintained. Pursuant to our bottler’s agreements, we authorize our bottlers to use applicable Company trademarks in connection with their preparation, packaging, distribution and sale of Company products. In addition, we authorize certain third parties to use applicable Company trademarks in connection with their preparation, packaging, distribution and sale of beverages bearing Company trademarks in certain territories. We also grant licenses to third parties from time to time to use certain of our trademarks in conjunction with certain merchandise and food products.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm｜as_of：2026-02-20
<<<
Our finished product operations generate net operating revenues by selling sparkling soft drinks and a variety of other finished beverages to retailers, or to distributors and wholesalers who in turn sell the beverages to retailers. Generally, finished product operations generate higher net operating revenues but lower gross profit margins than concentrate operations. These operations consist primarily of our consolidated bottling and distribution operations, which are included in our Bottling Investments operating segment. In certain markets, the Company also operates non-bottling finished product operations in which we sell finished beverages to distributors and wholesalers that are generally not one of the Company’s bottling partners. These operations are generally included in our geographic operating segments. Additionally, we sell directly to consumers through retail stores operated by Costa. These sales are included in our EMEA operating segment, regardless of the physical location of the retail stores. In the United States, we manufacture fountain syrups and sell them to fountain retailers, who use the fountain syrups to produce beverages for immediate consumption, or to authorized fountain wholesalers or bottling partners who in turn sell and distribute the fountain syrups to fountain retailers. These fountain syrup sales are included in our North America operating segment.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KO_20261103/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
