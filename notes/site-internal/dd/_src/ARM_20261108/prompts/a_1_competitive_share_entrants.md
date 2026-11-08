你是 stock-analyst v20 DD 的證據採集子 agent。標的：ARM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - ARM Arm Holdings market share gaining OR losing 2026
  - Arm Holdings new entrant OR displace threat Semiconductors 2026
  - ARM competitor design win 2026
  - Arm Holdings vs Semiconductors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
•We face intense competition and could lose market share to our competitors. •Our development of production silicon products, such as the Arm AGI CPU, compute subsystems (“CSS”), chiplets, complete chip solutions, and other more integrated compute products may subject us to new or enhanced competitive, brand, technological, regulatory, operational and financial risks.

We face intense competition and could lose market share to our competitors. The market for our products is intensely competitive and characterized by rapid changes in design and manufacturing technologies, software development efficiencies, end-user requirements, industry standards, and frequent new product introductions and improvements. We anticipate continued challenges from current and new competitors, including established technologies such as the x86 architecture, a family of instruction set architectures (“ISAs”), as well as by free, open-source technologies, including the RISC-V architecture. Many of our customers are also major supporters of the RISC-V architecture and related technologies. If RISC-V-related technology continues to be developed and market support for RISC-V increases, our customers may choose to utilize this free, open-source architecture instead of our products. Additionally, many of our direct and indirect competitors, including some of our semiconductor customers, are major corporations with substantially greater technical, financial and marketing resources and name recognition than we have. Some of these competitors have a much larger application software base and a much larger installed customer base than we do, and there can be no assurance that we will have the financial resources, technical expertise, and marketing, distribution and support capabilities to compete successfully with them in the future.

In markets where we are established already and new markets we have entered, intend to enter or may in the future enter, our primary competitors may have, among other things, greater financial, technical, marketing, distribution, support or other resources and capabilities, greater brand recognition, lower labor and development costs, different regulatory restrictions or a larger customer base than we do. In certain of these markets, we may have to invest substantial resources into developing an ecosystem of software and tools to create a competitive ecosystem that allows us to compete with alternative architectures. Further, several of our customers are creating their own bespoke accelerators for artificial intelligence (“AI”) workloads that are intended to sit alongside the Arm core. If, over time, more of the workloads move to accelerators away from the CPU, the CPU market size may decrease, resulting in a decrease of our license fees and royalties. While we have implemented a number of strategies to address this risk, such as introducing the Arm AGI CPU, creating dedicated neural processing units ("NPUs"), adding dedicated AI acceleration features to our CPUs and graphics processing units (“GPUs”), and maintaining dialogues with partners in the AI software ecosystem to ensure that our products and solutions are appropriate for AI workloads, there can be no assurances that our strategies will be successful.…

While our customers likely would incur significant costs in switching to competitors’ architecture, our competitors (including new market entrants) may offer greater incentives to customers through rebates, bundling, marketing funds, similar programs and other commercial arrangements to induce them to use their architecture in lieu of our products.

In order to remain competitive in the highly competitive markets in which we do business, we may need to reduce the prices of our products or services or otherwise change the structure and terms of our customer relationships or our business model. If our competitors offer significant discounts on certain products in an effort to recapture or gain market share or to sell other software or hardware products, we may need to lower our prices or offer other favorable terms to compete successfully. Any such changes would likely reduce our profits and could have a material adverse effect on our business, results of operations, financial condition and prospects. Any substantial changes to our other commercial arrangements with our customers or our business model could cause revenues to decline or be delayed as our sales force implements and our customers adjust to the commercial arrangements or business model. Changes to our business model could also necessitate changes in our product mix, which could cause revenues or profitability to decline, particularly if such changes in our product mix result in an increased reliance on lower margin offerings.…

Our IP business relies on our customers to design, manufacture and sell chips incorporating our products in order to generate royalty revenue. A substantial portion of our revenue depends upon the commencement of new design projects by semiconductor companies, OEMs, and CSPs, and their ability to provide complete chips based on our products to meet the specific application needs of their customers. However, our customers are not contractually obligated to design, manufacture, sell or deploy chips using our products on an exclusive basis or at all. Some of our existing customers design, manufacture, sell and deploy chips based on competing technology, including their own, and other existing or potential customers may do so in the future. To the extent that our customers elect to license technology from competitors, our competitive position could be adversely affected and we could lose market share. Furthermore, under many of our arrangements with customers, there is generally no minimum purchase obligation or guaranteed revenue stream.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
Cloud AI •Cloud Compute. The cloud compute market includes the main server chips, data processing units, and smart network interface cards used by CSPs to run their operations. Arm-based chips have been gaining market share as CSPs have started to deploy Arm products in their own in-house designed chips used in their data centers, and as other CSPs start to deploy chips designed by Arm licensees.

Competition We compete based on a variety of factors, including price, performance, energy-efficiency, ease of product customization, product quality, software availability, marketing and distribution capability, customer support, name recognition and financial strength. Given our reliance on our partners and customers, our competitive position is dependent on our partners’ and customers’ competitive positions. In addition, our partners and customers do not license our products exclusively; rather, several of our partners and customers also design, develop, manufacture and market processors based on non-Arm based architectures as well as develop their own Physical IP in-house. Our partners and customers compete with each other and with us in various markets. The level of competition and the nature of the competitor generally varies based on the end market. For established markets where there is an incumbent architecture with a supporting ecosystem, it can be difficult for a new architecture to displace existing architectures and, therefore, to gain market share. For example, we have made significant progress and have established a large market share in markets such as smartphones, consumer electronics and IoT. We face competition primarily from other architectures like x86 and RISC-V in many of these markets.…

Additionally, because our resources must be allocated amongst developing and maintaining our existing IP portfolio and developing and commercializing any new, more integrated compute products or solutions, companies that focus their efforts on a single product or solution or a limited number of products or solutions may have significantly greater financial, technical, manufacturing, marketing, sales and distribution resources dedicated to such markets and solutions than we do. Such companies may also have a more developed IP portfolio for the applicable markets and solutions and may be able to leverage these resources and competitive factors to gain or maintain market share. Furthermore, many of our customers who have historically licensed our IP may face direct competition from us in certain market segments, which could impact our existing commercial relationships. For example, some of our customers may face direct competition from us in silicon production products, such as with the Arm AGI CPU. See “Item 3. Key Information—D. Risk Factors—Risks Relating to Our Business and Industry—Our development of production silicon products, such as the Arm AGI CPU, CSS, chiplets, complete chip solutions, and other more integrated compute products may subject us to new or enhanced competitive, brand, technological, regulatory, operational and financial risks.”
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2026，申報 2026-05-26）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/1973239/000197323926000097/arm-20260331.htm｜as_of：2026-05-26
<<<
Our Market Share Across End Markets Arm CPUs are the world’s most widely licensed and deployed processors. Our products are used in almost all smartphones, the majority of tablets and digital TVs, and a significant proportion of all chips with embedded processors, including for both consumer and enterprise applications. As new high-growth markets for electronics emerge, our customers require our more advanced processor designs. For example, AI demand is driving strong momentum for the Arm ecosystem. AI growth requires significantly more compute across all of our end markets from smartphones with better chat features, to automobiles with better driving and parking assist, to IoT microprocessors with embedded NPUs. Our operating and financial performance is dependent, in large part, upon maintaining our market share in the smartphone and consumer electronics markets and maintaining or growing market share in our other target markets, such as cloud and AI data centers.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
