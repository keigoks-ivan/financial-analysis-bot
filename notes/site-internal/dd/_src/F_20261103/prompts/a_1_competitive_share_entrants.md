你是 stock-analyst v20 DD 的證據採集子 agent。標的：F。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - F Ford Motor market share gaining OR losing 2026
  - Ford Motor new entrant OR displace threat Auto Manufacturers 2026
  - F competitor design win 2026
  - Ford Motor vs Auto Manufacturers peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
◦Costs of components and raw materials necessary for production of vehicles ◦Costs for customer warranty claims and additional service actions ◦Costs for safety, emissions, and fuel economy technology and equipment •A high proportion of relatively fixed structural costs, so that small changes in wholesale unit volumes can significantly affect overall profitability Although supply disruptions have resulted in a higher level of new vehicle prices, our industry has historically had a very competitive pricing environment, driven in part by excess capacity. For the past several decades, manufacturers typically have offered price discounts and other marketing incentives to provide value for customers and maintain market share and production levels, and we saw some of these actions resume as industry production and inventories increased in recent quarters, especially with waning policy support for EVs leading to excess supply in that market segment. The decline in value of foreign currencies can also contribute significantly to competitive pressures in many of our markets.

Item 1. Business (Continued) Sales, Industry Volume, and Market Share Sales, industry volume, and market share in certain key markets during the past three years were as follows: Sales (a) Industry Volume (b) Market Share (c)

(c)Market share represents reported retail sales of our brands as a percent of total industry volume in the relevant market or region.

(d)China includes Taiwan; China market share includes Ford and Lincoln brand and JMC brand vehicles produced and sold by our unconsolidated affiliates.

Competitive Benefit Programs We provide employees with a competitive, comprehensive, and flexible set of benefits and resources to support their financial, social, mental/emotional, physical, and professional health. Our comprehensive global benefits programs are designed to attract and retain top talent worldwide. These programs include a wide range of resources and solutions to educate, empower, and support individual and organizational goals while being tailored to local regulations and employee needs across our diverse global workforce. This comprehensive approach is integral to our total rewards strategy, addressing business and employee challenges through a multi-channel approach that provides diverse populations and global regions with flexible options to meet their specific goals.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm｜as_of：2026-02-11
<<<
Operational Risks Ford’s long-term success depends on delivering the Ford+ plan, including improving cost competitiveness. We previously announced our plan for growth and value creation – Ford+. Ford+ is our plan to thrive at the intersection of great vehicles, iconic brands, and innovative software and service, building Ford into a higher growth, higher margin, more capital efficient, and more durable company. Our Ford+ plan is designed to leverage our foundational strengths with enhanced capabilities – enriching customer experiences and deepening loyalty. As we progress this transformation of our business, we must integrate our strategic initiatives into a cohesive business model, modernize our systems, processes, and technologies, and balance competing priorities, or we will not be successful. To facilitate this transformation, we are making substantial investments, recruiting new talent, and modernizing and optimizing our business model, management and IT systems, and organization. Our strategy involves providing customers freedom of choice to select the powertrain that best suits their needs and maintaining manufacturing flexibility at Ford to meet shifting customer demand. Accordingly, maintaining discipline in our capital allocation continues to be important, as a strong core business and a balance sheet that provides the flexibility to invest in these opportunities are critical to the success of our Ford+ plan.…

Ford may not realize the anticipated benefits of restructuring actions and such actions may cause Ford to incur significant charges, disrupt our operations, or harm our reputation. We continually review and evaluate our business to find opportunities to make our operations more efficient and reduce costs. In doing so, we have taken, and may in the future take, restructuring actions, such as strategic divestitures, unwinding an existing venture or relationship, or ceasing operations in a market, particularly for those businesses where a path to sustained profitability is not feasible in light of the capital allocation requirements or for other reasons. Our plans for implementing such actions may be accelerated by shifting industry dynamics and new entrants to our industries with which we must compete. These actions may include employee separations, a reduced footprint (e.g., plant closures or smaller operations at existing plants or plants that are not yet on-line), operating our plants at less than full capacity (e.g., reducing shifts), cancelling products or programs, or shifting our strategy for the deployment of technologies. Such restructuring actions have caused us and may in the future cause us to incur significant costs; record impairments or other charges; subject us to potential claims from employees, suppliers, dealers, other counterparties, or governmental authorities (including a reduction or clawback of 21

Ford’s new and existing products and digital, software, and physical services are subject to market acceptance and face significant competition from existing and new entrants in the automotive and digital and software services industries, and Ford’s reputation may be harmed based on positions it takes or if it is unable to achieve the initiatives it has announced. Although we conduct extensive market research before launching new or refreshed products and introducing new services, many factors both within and outside our control affect the success of new or existing products and services in the marketplace, and we may not be able to accurately predict or identify emerging trends or preferences or the success of new products or services in the market. It takes years to design and develop a new vehicle or change an existing vehicle. Because customers’ preferences may change quickly, our new and existing products may not generate sales in sufficient quantities and at costs low enough to be profitable and recoup investment costs. Offering products and services that customers want and value can mitigate the risks of increasing price competition, price sensitive customers, and declining demand, but products and services that are perceived to be less desirable (whether in terms of price, quality, styling, safety, overall value, fuel efficiency, or other attributes) can exacerbate these risks.…

With increased consumer interconnectedness through the internet, social media, and other media, mere allegations relating to quality, safety, reliability, fuel efficiency, sustainability, corporate social responsibility, or other key attributes can negatively impact our reputation or market acceptance of our products or services, even where such allegations prove to be inaccurate or unfounded. Further, our ability to successfully grow through capacity expansion and investments in the areas of electrification, connectivity, digital and physical services, and software services depends on many factors, including advancements in technology, regulatory changes (e.g., new or revised government mandates and incentives), infrastructure development (e.g., a widespread vehicle charging network), and other factors that are difficult to predict, that have affected and may continue to affect significantly the future of electrified vehicles, autonomous and driver assistance technologies, digital and physical services, and software services. The automotive, software, and digital service businesses are very competitive and change rapidly.…

Ford may face increased price competition for its products and services, including pricing pressure resulting from industry excess capacity, currency fluctuations, competitive actions, legal and policy changes, or economic or other factors, particularly for electrified vehicles. The global automotive industry is intensely competitive, with installed manufacturing capacity generally exceeding current demand. Historically, industry overcapacity has resulted in many manufacturers offering marketing incentives on vehicles in an attempt to maintain and grow market share; these incentives historically have included a combination of subsidized financing or leasing programs, price rebates and reductions, and other incentives. As a result, we are not necessarily able to set our prices to offset higher marketing incentives, commodity or other cost increases, tariffs, or the impact of adverse currency fluctuations. This risk includes cost advantages foreign competitors may have because of their weaker home market currencies, which may, in turn, enable those competitors to offer their products at lower prices. Further, higher inventory levels put downward pressure on pricing, which may have an adverse effect on our financial condition and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
