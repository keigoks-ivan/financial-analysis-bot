你是 stock-analyst v20 DD 的證據採集子 agent。標的：LEA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - LEA Lear market share gaining OR losing 2026
  - Lear new entrant OR displace threat Auto Parts 2026
  - LEA competitor design win 2026
  - Lear vs Auto Parts peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
6 Table of Contents Automotive sales and production can also be affected by the age of the vehicle fleet and related scrappage rates, labor relations issues, unforeseen operational disruptions, labor shortages, fuel prices, regulatory requirements, government initiatives and incentives, trade agreements, tariffs and other non-tariff trade barriers (including recent U.S. tariffs imposed or threatened to be imposed on Mexico, Canada and China, as well as other countries and any retaliatory actions taken by such countries), the availability and cost of raw materials and critical components, logistics issues, cybersecurity incidents, and the availability and cost of credit, as well as vehicle affordability and consumer preferences regarding vehicle powertrains (including preferences regarding electric and hybrid vehicles), size, configuration and features, among other factors. The impact of potential tariffs on our business and financial condition, if any, is subject to a number of factors that are not yet known or are subject to change, including the effective date and duration of such tariffs, the scope and nature of any tariffs, the amount of any tariffs, any countermeasures that the target countries may take in response to such tariffs.…

In 2026, the battery electric vehicle market is expected to represent 19% of global light vehicle production (based on January 2026 S&P Global Mobility projections), as compared to 16% in 2025 and 13% in 2024. Battery electric vehicle production increased to 14.5 million units in 2025 from 11.3 million units in 2024, primarily driven by growth in China and Europe. Increasing demand for electrified vehicles is driven by numerous product offerings from traditional automotive manufacturers as well as new entrants to the market, government requirements and incentives, automotive manufacturers' internal targets and a growing segment of end consumers who are seeking alternatives to vehicles with traditional ICE architectures. Meeting this demand requires further use of electronically controlled and assisted powertrains and related components to improve fuel efficiency; the adoption of alternative energy powertrains, such as 48-volt mild hybrid, full hybrid, plug-in hybrid and pure battery electric powertrains that facilitate electrification of the vehicle; and the use of lighter weight materials throughout the vehicle.

In our Seating business, our unique product offerings are providing us with an opportunity to offer value added solutions to our customers and to use our leading market position to capture additional market share. Our key seat component products include seat trim covers; surface materials such as leather and fabric; seat mechanisms; seat cushioning; headrests; and thermal comfort systems such as seat heating, ventilation, active cooling, pneumatic lumbar and massage products. Further, we are leveraging our distinct combination of complete seat system, seat component and thermal comfort expertise and capabilities with our ComfortFlex by LearTM module, an architecture of modular designs combining two or more thermal comfort functions, and our ComfortMax Seat by LearTM module, the integration of one or more thermal comfort features into the seat trim cover. These ComfortFlex by LearTM and ComfortMax Seat by LearTM modules can reduce sub-components by up to 50% and increase airflow directly to the occupant by up to 40%, as compared to currently available designs. With our thermal comfort systems expertise, we are poised to capitalize on the market trends in electric vehicles, second and third row comfort, and ride sharing, while also providing greater design, cost, production and energy efficiency for our customers.

8 Table of Contents Seating Segment Lear is a recognized global leader in complete seat systems. Based on independent market studies and management estimates, we believe we are one of the two largest suppliers of complete seat systems globally on the basis of revenue with strong positions in all major markets and a 26% global market share in 2025. We are also a recognized leader in key individual seat components produced for complete seat systems.

Our seat cover operations have continued to expand in low-cost markets, including precision cutting, assembly, sewing and lamination. Our acquisition of Eagle Ottawa provided us an industry-leading market share in automotive leather globally. Our capabilities in leather design, development and manufacturing allow us to deliver the most luxurious, durable and performance-tested leathers to our customers. Our acquisition of Guilford Mills provided us with Guilford Performance Textiles, a line of automotive seat and interior fabrics. On a global basis, we can provide a full range of seat cover capabilities, including design and surface coating solutions, as well as unique leather and fabric applications. We believe that the combination of these capabilities in seat surface materials differentiates us and provides us with a competitive advantage facilitating our leadership position in the industry.

Advanced Seating Craftsmanship and Innovation We believe that our broad capabilities, including advanced design and material integration skills, provide us with a competitive advantage. Our team has developed a portfolio of technologies that deliver sustainable products, differentiated design, craftsmanship and comfort. We are leveraging our unique position to be an industry leader in design and facilitating customer interactions with designers and engineers working collaboratively to create innovative solutions early in the design process. The breadth of our portfolio and depth of our design expertise allows us to better integrate all seat components and bring innovative designs into production with the highest level of craftsmanship, providing differentiated design comfort, quality and overall value to the end consumer. We believe that our unmatched component capabilities, design expertise, global manufacturing presence, and portfolio of enabling and sustainable technologies provide a unique value proposition to our customers and will drive market share gains for our business.

Competition Key competitors in the Seating segment globally include Adient plc, Forvia SE, Magna International Inc., Ningbo Jifeng Auto Parts Co., Ltd. / Grammer AG, Toyota Boshoku Corporation, TS Tech Co., Ltd. and Yanfeng Automotive Systems Co., Ltd., which have varying market presence depending on the region, country or automotive manufacturer. Toyota Motor Corporation and Honda Motor Co. Ltd. hold equity ownership positions in Toyota Boshoku Corporation and TS Tech Co., Ltd., respectively. A limited number of other automotive manufacturers maintain a presence in the seat system market through wholly-owned subsidiaries, joint ventures or in-house operations, such as FinDreams Technology Co., Ltd. and Nobo Automotive Systems Co., Ltd. In seat components, we compete with the seat system suppliers identified above, as well as certain suppliers that specialize in particular components.

14 Table of Contents Competition Key competitors in electrical distribution and connection systems include Aptiv PLC, Leoni AG, Molex Incorporated (a subsidiary of Koch Industries Inc.), Sumitomo Corporation, TE Connectivity and Yazaki Corporation. Key competitors in BDUs include Delta Electronics, Inc., LS E-Mobility, Panasonic Holdings Corporation and Yazaki Corporation. Key competitors in electronic controllers include Aumovio SE, Aptiv PLC, Denso Corporation, Harman International Industries, Incorporated (a subsidiary of Samsung Electronics Co. Ltd.), Hella (a subsidiary of Forvia SE), Motherson Group, Robert Bosch GmbH, Valeo S.A. and Visteon Corporation.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm｜as_of：2026-02-13
<<<
Our sales and production may be further affected by new entrants to the industry, as well as various automakers entering or expanding in certain regions, and the restructuring actions, including facility closures, of our customers. Chinese domestic automakers, in particular, continue to expand their market share in China (through electric vehicles) and outside of China with both innovative designs and attractive pricing. As a result, several traditional automakers have experienced declines in revenue and market share. As these traditional automakers are among our largest customers, our business and financial results may be adversely affected by decreases in their businesses or market share.

•We operate in a highly competitive industry and efforts by our competitors, as well as new entrants to the industry, to gain market share could adversely affect our financial performance.

We operate in a highly competitive industry. We and most of our competitors are seeking to expand market share with new and existing customers, including in high growth regions. Our customers award business based on, among other things, price, quality, service and technology. Our competitors' efforts to grow market share could exert downward pressure on our product pricing and margins. In addition, the automotive industry has attracted, and will continue to attract, new entrants as a result of the evolving nature of the automotive vehicle market, including the increasing adoption of electric and hybrid vehicles. Certain of these automakers and suppliers are also expanding their operations into regions in which they previously did not have a presence. Traditional automakers are experiencing increased competitive pressures as Chinese domestic automakers continue to expand their market share both in and beyond China. Chinese domestic suppliers that may have lower financial return expectations are also challenging traditional automotive suppliers for market share. Further, the global automotive industry is experiencing a period of significant technological change, including in the areas of electrification and digitization. If we are unable to differentiate our products, maintain a low-cost footprint or compete effectively to win business with newer/emerging automakers, we may lose market share or be forced to reduce prices, thereby lowering our margins.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
