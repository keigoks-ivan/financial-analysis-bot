你是 stock-analyst v20 DD 的證據採集子 agent。標的：PLTR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - PLTR Palantir Technologies market share gaining OR losing 2026
  - Palantir Technologies new entrant OR displace threat Software - Infrastructure 2026
  - PLTR competitor design win 2026
  - Palantir Technologies vs Software - Infrastructure peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm｜as_of：2026-02-17
<<<
Competition We are fundamentally competing with the internal software development efforts of our potential customers.

In addition, our competitors include large enterprise software companies, government contractors, and system integrators. We also face competition from emerging companies as well as established companies that have entered, and may continue to enter, this market.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm｜as_of：2026-02-17
<<<
We face intense competition for qualified personnel, especially engineering personnel, in major U.S. markets, where a large portion of our personnel are based, as well as in other non-U.S. markets where we have expanded or expect to expand our non-U.S. operations. We incur costs related to attracting, relocating, and retaining qualified personnel in these highly competitive markets, including leasing real estate in prime areas in these locations and compensation-related expenses. Further, many of the companies with which we compete for qualified personnel have greater resources than we have. If the perceived value of our equity awards declines, or if the mix of equity and cash compensation or the structure and terms of the compensation that we offer is less attractive than that of our competitors, it may adversely affect our ability to recruit and retain highly skilled personnel, and we may incur additional compensation-related expenses to successfully recruit and retain such personnel. Additionally, laws and regulations, such as restrictive immigration laws, may limit our ability to recruit outside of the United States. We seek to retain and motivate existing personnel through our compensation practices, company culture, and career development opportunities. If we fail to attract new personnel or to retain our current personnel, our business and operations could be harmed.

We have in the past changed, and we expect that in the future we may change, our pricing models, including as a result of competition, global economic conditions, general reductions in our customers’ spending levels, pricing studies, or changes in how our platforms are broadly consumed. Similarly, as we introduce new platforms, products, and services, such as AIP, or as a result of the evolution of our existing platforms, products, and services, we may have difficulty determining the appropriate price structure for our products and services, or customers may request or demand different pricing structures. In addition, as new and existing competitors introduce new products or services that compete with ours, or revise their pricing structures, we may be unable to attract new customers at the same price or based on the same pricing model as we have used historically. Moreover, as we continue to target selling our platforms and services to larger organizations, these larger organizations may demand different pricing structures or substantial price concessions. As we expand access to our products to increasingly broad swaths of the market, our pricing model and product and service offerings for such customers have been, and will continue to be, tailored to be attractive for such customers.…

The markets for our platforms are very competitive, and we expect such competition to continue or increase in the future. A significant number of companies are developing products that currently, or in the future may, compete with some or all aspects of our proprietary platforms. We may not be successful in convincing the management teams of our potential customers to deploy our platforms in lieu of existing software solutions or in-house software development projects often favored by internal IT departments or other competitive products and services. In addition, our competitors include large enterprise software companies, government contractors, and system integrators, and we may face competition from emerging companies as well as established companies who have not previously entered this market. Additionally, we may be required to make substantial additional investments in our research, development, services, marketing, and sales functions in order to respond to competition, and there can be no assurance that we will be able to compete successfully in the future.

In addition, some of our larger competitors have substantially broader and more diverse product and service offerings and may be able to leverage their relationships with distribution partners and customers based on other products or incorporate functionality into existing products to gain business in a manner that discourages customers from purchasing our platforms, including by selling at zero or negative margins, product bundling, or offering closed technology platforms. Potential customers may also prefer to purchase from their existing provider rather than a new provider regardless of platform performance or features. As a result, even if the features of our platforms offer advantages that others do not, customers may not purchase our platforms. These larger competitors often have broader product lines and market focus or greater resources and may therefore not be as susceptible to economic downturns or other significant reductions in capital spending by customers. If we are unable to sufficiently differentiate our platforms from the integrated or bundled products of our competitors, such as by offering enhanced functionality, performance, or value, we may see a decrease in demand for those platforms, which could adversely affect our business, financial condition, and results of operations.

Some of our competitors have made or could make acquisitions of businesses that allow them to offer more competitive and comprehensive solutions. As a result of such acquisitions, our current or potential competitors may be able to accelerate the adoption of new technologies that better address customer needs, devote greater resources to bring these products and services to market, initiate or withstand substantial price competition, or develop and expand their product and service offerings more 24 Table of Contents quickly than we do. These competitive pressures in our market, or our failure to compete effectively, may result in fewer orders, reduced revenue and margins, and loss of market share. In addition, it is possible that industry consolidation may impact customers’ perceptions of the viability of smaller or even mid-size software firms and consequently customers’ willingness to purchase from such firms.

We may not compete successfully against our current or potential competitors. If we are unable to compete successfully, or if competing successfully requires us to take costly actions in response to the actions of our competitors, our business, financial condition and results of operations could be adversely affected. In addition, companies competing with us may have an entirely different pricing or distribution model. Increased competition could result in fewer customer orders, price reductions, reduced margins, and loss of market share, any of which could harm our business and results of operations.

The market for our platforms is rapidly evolving. Our future success will depend in large part on the growth and expansion of this market, which is difficult to predict and relies on a number of factors, including customer adoption, customer demand, changing customer needs, the entry of competitive products, the success of existing competitive products, potential customers’ willingness to adopt an alternative approach to data collection, storage, and processing and their willingness to invest in new software after significant prior investments in legacy data collection, storage, and processing software. The estimates and assumptions that are used to calculate our market opportunity are subject to change over time, and there is no guarantee that any particular number or percentage of the organizations covered by our market opportunity estimates will pay for our platforms and services at all or generate any particular level of revenue for us. Even if the market in which we compete meets the size estimates and growth forecasts, our business could fail to grow at the levels we expect or at all for a variety of reasons outside our control, including competition in our industry.…

We have a culture that encourages employees to quickly develop and launch key technologies and platforms intended to solve our customers’ most important problems and prioritizes the advancement of employees to positions of significant responsibility based on merit despite, in some cases, limited prior work or industry experience. Much of our hiring into technical roles comes through our internship program or from candidates joining us directly from undergraduate or graduate engineering programs rather than industry hires. Successful entry-level hires are often quickly advanced and rewarded with significant responsibilities, 25 Table of Contents including in important customer-facing roles as project managers, development leads, and product managers. Larger competitors, such as defense contractors, system integrators, and large software and service companies that traditionally target large enterprises typically have more sizable direct sales forces staffed by individuals with significantly more industry experience than our customer-facing personnel, which may negatively impact our ability to compete with these larger competitors. We have historically operated with a relatively flat reporting and organization structure and have few formal promotions. As our business grows and becomes more complex, the staffing of customer-facing personnel, some of whom may have limited industry experience, may result in unintended outcomes or in decisions that are poorly received by customers or other stakeholders.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLTR_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
