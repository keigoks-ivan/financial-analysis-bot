你是 stock-analyst v20 DD 的證據採集子 agent。標的：AXTI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - AXTI AXT market share gaining OR losing 2026
  - AXT new entrant OR displace threat 半導體基板 / InP / GaAs 2026
  - AXTI competitor design win 2026
  - AXT vs 半導體基板 / InP / GaAs peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
Silicon substrates dominate the semiconductor substrate market. Silicon wafers are larger in diameter and significantly lower in cost. AXT and our competitors exist because the laws of physics prevent certain functions from performing properly, or at all, if silicon material is used as the wafer substrate. Our substrate wafers are used when a typical silicon substrate wafer cannot meet the performance requirements of a semiconductor chip or optoelectronic device. Demand for higher performance non-silicon-based wafer substrates, such as the substrates in which AXT specializes, is expected to increase as new applications are adopted. In contrast to the ever-more complex electronic circuit designs and the skill sets required to accomplish such designs, the knowledge base and skill sets required for AXT and our competitors are material science-based. We do not design or manufacture the semiconductor chips and other electronic circuits. Instead, we apply our deep knowledge in material science to grow single crystal ingots that are then sliced into individual wafer substrates. We add value by researching, developing and producing the specialty material wafers. This places us at the beginning of the semiconductor “food chain”.

We promote our product diversity as a way to differentiate ourselves in the market. Some competitors provide only gallium arsenide substrates. We provide gallium arsenide and also indium phosphide and germanium substrates. Some competitors limit their wafer diameters to only a few sizes. Our wafers range from one inch to up to eight inches in diameter. We also produce substrates with customer defined specifications, which may range in thickness, smoothness or flatness and may include adding special additional materials, such as iron or sulfur. In addition to our wafers or substrates, we also generate revenue from our two consolidated subsidiaries that sell raw materials. Product diversity can mitigate some of the down cycles in our market because we are not dependent on a single product or application for revenue.

As a manufacturing company, we must constantly improve our manufacturing processes to remain competitive, and our research and development programs must be integrated into our manufacturing lines. All of our research and development is conducted at our manufacturing facilities in China and the process technology developed by the China teams over the last 20 years enables us to remain competitive and to provide high-quality wafer substrates to our customers. Our China research and development teams must continue to stay close to the manufacturing sites and develop new process steps, features and benefits. We believe our teams are fully capable of moving the process technology forward. We also engage third party firms or individuals on specific projects.

Competition The semiconductor substrate industry is characterized by narrow technological boundaries, price erosion and generally intense competition. Certain wafer substrates, such as low-quality wafer substrates for consumer products using LED lighting, compete almost entirely on price. Other products, such as InP and low EPD GaAs wafers, have fewer competitors and quality is a key competitive factor in addition to price. We face actual and potential competition from a number of established companies who have the advantages of greater name recognition and more established relationships in the industry. In some cases, our competitors have substantially greater financial, technical and marketing resources as they are divisions of much larger companies. They may utilize these advantages to expand their product offerings more quickly, adapt to new or emerging technologies and changes in customer requirements more quickly, and devote greater resources to the marketing and sale of their products. We believe a critical factor in our business is the level of technical support we provide to the customer or prospective customer and we attempt to counter possible advantages of name recognition or size with superior technical support through our team of technical sales support professionals, the majority of whom hold PhDs in physics or materials science.

15 Table of Contents We believe that the primary competitive factors in the markets in which our substrate products compete are: ● quality; ● low EPD; ● price; ● customer technical support; ● ability to quickly add InP capacity; ● product performance; and ● meeting customer specifications.

A majority of our customers specialize in epitaxial growth, a complex series of chemical layers grown on top of our wafers. Our wafers cannot be used to make chips until the epitaxial layers are grown. Typically, our customer or prospective customer has at least two qualified substrate suppliers. Qualified suppliers must meet industry-standard specifications for quality, on-time delivery and customer support. Once a substrate supplier has qualified with a customer, then price, consistent quality and current and future product delivery lead times become the most important competitive factors. A supplier that cannot meet a customer’s current lead times or that a customer perceives will not be able to meet future demand and provide consistent quality can lose market share. Our primary competition in the market for compound and single element semiconductor substrates includes Sumitomo Electric Industries (“Sumitomo”), Japan Energy (“JX”), Freiberger Compound Materials (“Freiberger”), Umicore, China Crystal Technology Corp. (“CCTC”) and Vital Materials. We believe that at least two of our competitors are shipping high volumes of GaAs substrates manufactured using a process similar to our VGF technology. In addition, we also face competition from semiconductor device manufacturers that may use other specialty material substrates that are not GaAs, InP or Ge based materials and that are actively exploring alternative materials.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
● Difficulties in accurately estimating market demand could result in over-investing in inventory, equipment and capacity expansion or losing market share if we do not invest sufficiently.

​ The Chinese government has in the past imposed temporary restrictions on manufacturing facilities, such as the restrictions imposed on polluting factories for the 2008 Olympics and the 2014 Asian Pacific Economic Cooperation event. These restrictions included a shutdown of the transportation of materials and power plants to reduce air pollution. To reduce air pollution in Beijing, the Chinese government has sometimes limited the construction of new, or expansion of existing, facilities by manufacturing companies in the Beijing area or required mandatory factory shutdowns. For example, in the first quarter of 2018, over 300 manufacturing companies, including Tongmei, were intermittently shut down by the local government for a total of ten days from February 27 to March 31 due to severe air pollution. If the government applies restrictions to us or requires mandatory factory shutdowns in the future, then such restrictions or shutdowns could have an adverse impact on our results of operations and our financial condition. Our ability to supply current or new orders could be significantly impacted. Customers could then be required to purchase products from our competitors, causing our competitors to take market share from us.

The markets for our products are intensely competitive. We face competition for our wafer substrate products from other manufacturers of substrates, such as Sumitomo, JX, Freiberger, Umicore, Vital and CCTC, and from companies, such as Qorvo and Skyworks, that are actively considering alternative materials to GaAs and marketing semiconductor devices using these alternative materials. If we are unable to compete effectively, our revenue may decrease and we may not maintain profitability. We face many competitors that have a number of significant advantages over us, including: ● greater name recognition and market share in the business; ● more manufacturing experience; ● extensive intellectual property; and ● significantly greater financial, technical and marketing resources.

The level and intensity of competition has increased over the past years and we expect competition to continue to increase in the future. Competitive pressures have resulted in reductions in the prices of our products, and continued or increased competition could reduce our market share, require us to further reduce the prices of our products, affect our ability to recover costs and result in reduced gross margins and profitability.

We manufacture all of our products in China, and source most of our raw materials in China. We have in the past experienced quality problems with our products. Our previous quality problems caused us to lose market share to our competitors as some of our customers reduced their orders until our wafer surface quality was as good and as consistent as that offered by our competitors. If we are unable to continue to achieve customer qualifications for our products, or if we are unable to control product quality, customers may not increase purchases of our products, our China facilities will become underutilized, and we will be unable to achieve revenue growth.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-03-17）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1051627/000143774926008612/axti20251231_10k.htm｜as_of：2026-03-17
<<<
(77.8 )% $ 1,555 82.5 % % of total revenue 0.9 % 3.5 % 2.5 % Equity in income of unconsolidated joint ventures is the aggregate net income (loss) from our minority-owned supply chain joint venture companies that are not consolidated. Equity in income of unconsolidated joint ventures decreased $2.7 million to an income of $0.8 million in 2025 from an income of $3.4 million in 2024. The decrease is the result of export restrictions from China on gallium resulting in lower revenue and profit from international sales. Further, gallium suppliers in China reduced their pricing as they competed for market share within their domestic market.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
