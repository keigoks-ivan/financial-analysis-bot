你是 stock-analyst v20 DD 的證據採集子 agent。標的：ALV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - ALV Autoliv market share gaining OR losing 2026
  - Autoliv new entrant OR displace threat Auto Tier 1 / Passive Safety 2026
  - ALV competitor design win 2026
  - Autoliv vs Auto Tier 1 / Passive Safety peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
Since 1997, the Company’s sales compound annual growth rate (CAGR) for passive safety has been around 5% compared to the market rate of around 2.8% which includes an LVP growth of around 1.9%. The Company's outperformance is a result of a steady flow of new passive safety technologies, strong focus on quality and a superior global footprint both in products and engineering. This has enabled Autoliv to increase its global market share in passive safety from 27% in 1997 to around 44% in 2025.

In seatbelts, Autoliv has a global market share of around 45%, primarily due to being the technology leader with several important innovations such as pretensioners and active seatbelts. The Company's strong market position is also a reflection of its superior global footprint. Seatbelts are the primary life-saving safety product globally and are also an important requirement in low-end vehicles in the medium- and low-income markets. This provides the Company with an excellent opportunity to benefit from the expected growth in this segment of the market.

Autoliv holds a leading position in both airbags and steering wheels, with a combined market shares of around 44%. The market for airbags and steering wheels is expected to grow primarily due to increasing installation rates of inflatable curtains, side airbags, knee airbags, and front‑center airbags, as well as rising demand for higher‑value steering wheels with leather and additional integrated functions.

The Company's competitors Autoliv is the clear market leader in passive safety components and systems for the automotive industry with an estimated global market share of around 44%.

Other competitors include Nihon Plast and Ashimori in Japan, Yanfeng and Jinheng in China, Samsong in South Korea, and Chris Cintos de Seguranca in South America. Collectively, these competitors account for the majority of the remaining market share in passive safety.

Intellectual Property The Company has developed a considerable amount of proprietary technology related to automotive safety systems and relies on many patents to protect such technology. The Company's intellectual property plays an important role in maintaining its competitive position in a number of the markets the Company serves. For information on the Company's use of intellectual property and its importance to the Company, see “Risk Factors – If our patents are declared invalid or our technology infringes on the proprietary rights of others, our ability to compete may be impaired” in Item 1A of this Annual Report.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
We operate in a highly competitive market The market for passive safety systems is highly competitive, and we face competition from a number of other companies that produce and sell similar products. Among other factors, our products compete on the basis of price, quality, manufacturing and distribution capability, design and performance, technological innovation, delivery, and service. Some of our competitors are subsidiaries (or divisions, units or similar) of larger companies with greater financial and other resources than us. Some of our competitors may also have “preferred status” as a result of special relationships or ownership interests with certain customers. Our ability to compete successfully depends, in large part, on our success in continuing to innovate and manufacture products that have commercial success with our customer and end-consumers, differentiating our products from those of our competitors, continuing to deliver quality products in the time frames required by our customers, and maintaining best-cost production. We continue to invest in technology and innovation, which we believe are critical to our long-term growth. Our ability to maintain and improve existing products, while successfully developing and introducing distinctive new and enhanced products that anticipate changing customer and consumer preferences and capitalize upon emerging technologies will be a significant factor in our ability to remain competitive.…

Our business in Asia is subject to aggressive competition and is sensitive to economic, market, and political conditions We operate in the automotive supply market throughout Asia including the highly competitive markets in China, South Korea, and India. In each of these markets we face competition from both international and smaller domestic manufacturers. Due to the significance of the Asian markets for our profit and growth, we are exposed to risks in China, South Korea, and India. We anticipate that additional competitors, both international and domestic, may seek to enter the Chinese, South Korean, and/or Indian markets resulting in increased competition. Increased competition may result in lower sales volumes, price reductions, reduced margins and our inability to gain or hold market share. There have been periods of increased market volatility and moderation in the levels of economic growth in China, which resulted in periods of lower automotive production growth rates in China than those previously experienced. Our business in Asia is sensitive to economic and market conditions that drive automotive sales volumes in China, South Korea, and India and may be impacted if there are reductions in vehicle demand in those markets.…

19 RISKS RELATED TO INTELLECTUAL PROPERTY If our patents are declared invalid or our technology infringes on the proprietary rights of others, our ability to compete may be impaired We have developed a considerable amount of proprietary technology related to automotive safety systems and rely on a number of patents to protect such technology. Our intellectual property plays an important role in maintaining our competitive position in a number of the markets we serve. At present, we hold more than 6,600 patents and patent applications covering a large number of innovations and product ideas, mainly in the fields of seatbelt and airbag technologies. In addition to our in-house research and development efforts, we seek to acquire rights to new intellectual property through corporate acquisitions, asset acquisitions, licensing and joint venture arrangements. Our patents and licenses expire on various dates during the period from 2026 to 2045. We do not expect the expiration of any single patent or license to have a material adverse effect on our business, operating results and financial condition. Developments or assertions by or against us relating to intellectual property rights could negatively impact our business. We primarily protect our innovations with patents and vigorously protect and defend our patents, trademarks and know-how against infringement and unauthorized use.…

We may not be able to respond quickly enough to changes in technology and technological risks and to develop our intellectual property into commercially viable products Changes in legislative, regulatory, or industry requirements or in competitive technologies may render certain of our products obsolete or less attractive to our customers. We currently license certain proprietary technology to third parties and, if such technology becomes obsolete or less attractive, those licensees could terminate our license agreements, which could adversely affect our operating results. Our ability to anticipate changes in technology and regulatory standards and to successfully develop and introduce new and enhanced products on a timely basis will be a significant factor in our ability to remain competitive. We cannot provide assurance that we will be able to achieve the technological advances that may be necessary for us to remain competitive or that certain of our products will not become obsolete. We are also subject to the risks generally associated with new product introductions and applications, including lack of market acceptance, delays in product development and failure of products to operate properly. As part of our business strategy, we may from time to time seek to acquire businesses or assets that provide us with additional intellectual property.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1034670/000119312526058162/alv-20251231.htm｜as_of：2026-02-19
<<<
The customer landscape is gradually changing, with a multitude of new OEMs emerging in recent years. This is especially prominent within electric vehicles and in China. In China, domestic OEMs have gained significant market shares and as a group now has larger market share than global OEMs have in China. Autoliv's sales to domestic OEMs in China has grown rapidly. In 2022, this group accounted for 22% of Autoliv's sales in China, and in 2025 their share of Autoliv sales in China was 44%. The fastest growing OEM in China in recent years has been BYD, although its growth slowed significantly in 2025. BYD has a uniquely high degree of vertical integration, with a large proportion of in-house sourcing of products and systems. This includes passive safety systems, which is supplied by its subsidiary FinDreams Technology. Autoliv supplies components, especially inflators, to FinDreams Technology.

NEW COMPETITION Increased competition may result in price reductions, reduced margins and the Company's inability to gain or hold market share. OEMs rigorously evaluate suppliers on the basis of product quality, price, reliability and delivery as well as engineering capabilities, technical expertise, product innovation, financial viability, application of lean principles, operational flexibility, customer service, and overall management. To maintain the Company's competitiveness and position as a market leader, it is important to focus on all these aspects of supplier evaluation and selection.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
