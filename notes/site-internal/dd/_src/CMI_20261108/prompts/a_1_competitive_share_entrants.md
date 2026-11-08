你是 stock-analyst v20 DD 的證據採集子 agent。標的：CMI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - CMI Cummins market share gaining OR losing 2026
  - Cummins new entrant OR displace threat Specialty Industrial Machinery 2026
  - CMI competitor design win 2026
  - Cummins vs Specialty Industrial Machinery peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
REPORTABLE SEGMENTS We have five complementary reportable segments: Engine, Components, Distribution, Power Systems and Accelera. These segments share technology, customers, strategic partners, brand recognition and our distribution network in order to compete more efficiently and effectively in their respective markets. In each of our reportable segments, we compete worldwide with a number of other manufacturers and distributors that produce and sell similar products. Our products primarily compete on the basis of performance, price, total cost of ownership, fuel economy, emissions compliance, speed of delivery, quality and customer support.

In the Engine segment, our competitors vary from country to country, with local manufacturers generally predominant in each geography. Other independent engine manufacturers include Weichai Power Co., Ltd., Yuchai and Deutz AG. Truck OEMs may also elect to produce their own engines, and we must provide competitive products to win and keep their business. Truck OEMs that currently produce some or all of their own engines include Daimler, PACCAR, Traton, Volvo Powertrain, Ford Motor Company, China First Auto Works, Dongfeng Motor Corporation, CNH Industrial and Isuzu.

The Components segment competes with other manufacturers of aftertreatment systems, turbochargers, fuel systems, drivetrain systems and transmissions. Our primary competitors in these markets include Robert Bosch GmbH, Garrett Motion, Inc., Borg-Warner Inc., Tenneco Inc., Eberspacher Holding GmbH & Co. KG, Allison Transmission, Knorr-Bremse AG and ZF Friedrichshafen AG.

The Distribution segment is organized and managed as seven geographic regions, including North America, Europe, Asia Pacific, China, India, Latin America and Africa and Middle East. Across these regions, our locations compete with distributors or dealers that offer similar products. In many cases, these competing distributors or dealers are owned by, or affiliated with the companies that are listed as competitors of the Engine, Components or Power Systems segments. These competitors vary by geographical location and application market.

8 Table of Contents In the markets served by the Power Systems segment, we compete with a variety of independent engine manufacturers and generator set assemblers as well as OEMs who manufacture engines for their own products around the world. Our primary competitors are Caterpillar, Inc., MTU (Rolls Royce Power Systems Group) and Kohler/SDMO (Kohler Group), but we also compete with INNIO, Generac, Mitsubishi Heavy Industries and numerous regional generator set assemblers. Our alternator business competes globally with Leroy Somer, Marathon Electric and Meccalte, among others.

In the markets served by the Accelera segment, we compete with battery companies, powertrain component manufacturers and vertically integrated OEMs. Our primary competitors include Daimler, PACCAR, Traton, BYD Company Limited, Dana Incorporated and BorgWarner Inc.

Competitive Pay, Benefits and Well-Being To attract and retain the best talent, we focus on providing progressive, market-competitive pay, benefits and rewards. Our programs are designed to remain sustainable and responsive to the market while still honoring our core values. We provide benefit programs with the goal of supporting the emotional, financial, physical and social health of our employees throughout their career at Cummins. Some examples include base and variable pay, healthcare programs, global mental health support, paid time off, flexible work, retirement saving plans and employee stock purchase plans.

When designing our base pay ranges, we conduct market analyses to ensure our ranges are competitive and our employees are advancing their earning potential. We also perform annual compensation studies to assess market movement, pay equity and living wages. We review wages globally as we continuously work to ensure we are fair, equitable, competitive and can attract and retain the best talent.

Our strong focus on cultivating an inclusive culture underscores our belief that a diverse and inclusive workforce is a core value and competitive advantage for us. This focus dates back to the early 1970s as reflected in a public statement made by our former Chairman, J. Irwin Miller: “Character, ability and intelligence are not concentrated in one sex over the other, nor in persons with certain accents or in certain races or in persons holding degrees from universities over others. When we indulge ourselves in such irrational prejudices, we damage ourselves most of all and ultimately assure ourselves of failure in competition with those more open and less biased.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
Concerns regarding climate change may lead to additional international, national, regional and local legislative and regulatory responses, accords and mitigation efforts. Various stakeholders, including legislators and regulators, shareholders and non-governmental organizations, are continuing to look for ways to reduce GHG emissions, and consumers are increasingly demanding products and services resulting in lower GHG emissions. We could face risks to our brand reputation, investor confidence and market share due to an inability to innovate and develop new products that decrease GHG emissions. Increased input costs, such as fuel, utility, transportation and compliance-related costs, could increase our operating costs and negatively impact customer operations and demand for our products. As the impact of any additional future climate related legislative or regulatory requirements on our global businesses and products is dependent on the timing, scope and design of the mandates or standards, we are currently unable to predict its potential impact, which could have a material adverse effect on our results of operations, financial condition and cash flows.

We depend on the skills, institutional knowledge, working relationships, and continued services and contributions of key personnel, including our leadership team and others at all levels of the company, as a critical part of our human capital resources. In addition, our ability to achieve our operating and strategic goals depends on our ability to identify, hire, train and retain qualified individuals. We compete with other companies both within and outside of our industry for talented personnel in a highly competitive labor market, and we may lose key personnel or fail to attract other talented personnel. Any such loss or failure could have material adverse effects on our results of operations, financial condition and cash flows.

If we fail to keep pace with rapidly evolving technological developments in AI, our competitive position and business results may suffer. Our competitors or other third parties may incorporate AI into their products or operational processes more quickly or more successfully than us, which could have a material adverse effect on our competitive position, reputation and results of operations.

We face significant competition in the regions we serve. The markets in which we operate are highly competitive. We compete worldwide with a number of other manufacturers and distributors that produce and sell similar products. We primarily compete with diesel engines and related diesel products; however, new technologies continue to be developed for gasoline, natural gas, hydrogen, electrification and other technologies, and we will continue to face new competition from these expanding technologies. Our products primarily compete on the basis of performance, price, total cost of ownership, fuel economy, emissions compliance, speed of delivery, quality and customer support. We also face competitors in some emerging regions who have established local practices and long standing relationships with participants in these 25 Table of Contents markets. Additionally, we face increasing competition to develop innovative products that result in lower emissions. There can be no assurance that our products will be able to compete successfully with the products of other companies and in other markets.

As our customers in emerging markets continue to grow in size and scope, they are increasingly seeking to export their products to other countries. This has meant greater demand for our advanced engine technologies to help these customers meet the more stringent emissions requirements of developed markets, as well as greater demand for access to our distribution systems for purposes of equipment servicing. As these emerging market customers enter into, and begin to compete in more developed markets, they may increasingly begin to compete with our existing customers in these markets. Our further aid to emerging market customers could adversely affect our relationships with developed market customers. In addition, to the extent the competition does not correspond to overall growth in demand, we may see little or no benefit from this type of expansion by our emerging market customers.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
