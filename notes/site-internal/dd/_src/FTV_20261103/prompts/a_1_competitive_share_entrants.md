你是 stock-analyst v20 DD 的證據採集子 agent。標的：FTV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - FTV Fortive market share gaining OR losing 2026
  - Fortive new entrant OR displace threat Scientific & Technical Instruments 2026
  - FTV competitor design win 2026
  - Fortive vs Scientific & Technical Instruments peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1659166/000165916626000007/ftv-20251231.htm｜as_of：2026-02-25
<<<
Competition We believe that we are a leader in many of our served markets. Although our businesses generally operate in highly competitive markets, our competitive position cannot be determined accurately in the aggregate or by segment, since none of our competitors offer all of the same product and service lines or serve all of the same markets as we do. Because of the range of the products and services we sell and the variety of markets we serve, we encounter a wide variety of competitors, including larger companies or divisions of larger companies with substantial sales, marketing, research, and financial capabilities, as well as well-established regional competitors who are more specialized than we are in particular markets. We face increased competition in a number of our served markets as a result of the entry of competitors based in low-cost manufacturing locations, and increasing consolidation in particular markets. The number of competitors varies by product and service line. Our management believes that we have a market leadership position in most of the markets we serve.…

Competition Laws Our global operations are subject to complex and changing antitrust and competition laws and regulations, including conflicting laws and regulations in different jurisdictions that have increased the cost of conducting our global operations. We have implemented policies and procedures designed to ensure compliance with applicable global laws and regulations, but there can be no assurance of complete and consistent compliance with all laws and regulations given the complex and evolving policies implemented by governments around the world. If we are found to have violated laws and regulations, it could materially adversely affect our business, reputation, results of operations and financial condition.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1659166/000165916626000007/ftv-20251231.htm｜as_of：2026-02-25
<<<
We face intense competition and if we are unable to compete effectively, we may experience decreased demand and decreased market share. Even if we compete effectively, we may be required to reduce prices for our products and services.

Many of our businesses operate in industries that are intensely competitive and have been subject to consolidation. Because of the range of the products and services we sell and the variety of markets we serve, we encounter a wide variety of competitors. See “Business—Competition.” In order to compete effectively, we must retain longstanding relationships with major customers and continue to grow our business by establishing relationships with new customers, continually developing new or enhanced products and services to maintain and expand our brand recognition and leadership position in various product and service categories, and penetrating new markets, including high-growth markets. Our failure to compete effectively and/or pricing pressures resulting from competition may adversely impact our financial results, and our expansion into new markets may result in greater-than-expected risks, liabilities and expenses.

We generally sell our products and services in industries that are characterized by rapid technological changes, frequent new product introductions and changing industry standards. If we do not develop innovative new and enhanced products and services on a timely basis, our offerings will become obsolete over time and our competitive position and financial results will suffer. Our success will depend on several factors, including our ability to: •accurately identify customer needs and preferences and predict future needs and preferences; •allocate our research and development funding to products and services with higher growth prospects; •anticipate and respond to our competitors’ development of new products and services and technological innovations; •differentiate our offerings from our competitors’ offerings and avoid commoditization; •innovate and develop new technologies and applications, and acquire or obtain rights to third-party technologies that may have valuable applications in our served markets; •obtain adequate intellectual property rights with respect to key technologies before our competitors do; •successfully commercialize new technologies in a timely manner, price them competitively, and cost-effectively manufacture and deliver sufficient volumes of new products of appropriate quality on time; and •stimulate customer demand for and convince customers to adopt new technologies.

Our success also depends on our ability to attract, develop and retain a talented employee base. Our brand, our culture, our ability to provide competitive compensation, our locations of operations, and our reputation are important to our ability to recruit and retain key employees in these competitive markets. If we are not competitive or successful in our recruiting efforts, if we cannot attract or retain key employees, if we do not adequately ensure effective succession planning or transfer of knowledge for our key employees, or if some of our key employees are unable to enter, or choose to leave, the United States given uncertainties relating to immigration laws or immigration enforcement actions, our ability to deliver and execute on our operational, development, or portfolio strategies would be adversely affected.

Certain of our businesses sell a significant amount of their products to key distributors and other channel partners that have valuable relationships with customers and end-users. Some of these distributors and other partners also sell our competitors’ products or compete with us directly, and if they favor competing products for any reason they may fail to market our products effectively. Adverse changes in our relationships with these distributors and other partners, or adverse developments in their financial condition, performance, or purchasing patterns, could adversely affect our financial results. The levels of inventory maintained by our distributors and other channel partners, and changes in those levels, can also significantly impact our results of operations in any given period. In addition, the consolidation of distributors and customers in certain of the industries in which we operate could adversely impact our profitability.

We own numerous patents, trademarks, copyrights, trade secrets, and other intellectual property and have licenses to intellectual property owned by others, which in aggregate are important to our business. The intellectual property rights that we obtain, however, may not be sufficiently broad or otherwise may not provide us a significant competitive advantage, and patents may not be issued for pending or future patent applications owned by or licensed to us. In addition, the steps that we and our licensors have taken to maintain and protect our intellectual property may not prevent it from being challenged, invalidated, circumvented, designed-around, or becoming subject to compulsory licensing, particularly in countries where intellectual property rights are not highly developed or protected. In some circumstances, enforcement may not be available to us because an infringer has a dominant intellectual property position or for other business reasons, or countries may require compulsory licensing of our intellectual property. We also rely on nondisclosure and noncompetition agreements with employees, consultants, and other parties to protect, in part, trade secrets and other proprietary rights.…

•we are also required to comply with increasingly complex and changing data privacy regulations in multiple jurisdictions that regulate the collection, use, protection, and transfer of personal data, including the transfer of personal data between or among countries. In particular, the General Data Protection Regulation became effective in the European Union in May 2018 and the California Consumer Privacy Act became effective in January 2020. We may also face audits or investigations by one or more domestic or foreign government agencies relating to our compliance with these regulations. An adverse outcome in any such audit or investigation could subject us to fines or other penalties. That or other circumstances related to our collection, use, and transfer of personal data could cause a loss of reputation in the market and/or adversely affect our business and financial position; •certain of our products are medical devices that are subject to regulation by the U.S. FDA, by other federal and state governmental agencies, by comparable agencies of other countries and regions, and by certain accrediting bodies. To varying degrees, these regulators require us to comply with laws and regulations governing the development, testing, manufacturing, labeling, marketing, distribution, and post-marketing surveillance of our products.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1659166/000165916626000007/ftv-20251231.htm｜as_of：2026-02-25
<<<
This MD&A is designed to provide a reader of our financial statements with a narrative from the perspective of management. Our MD&A is divided into seven sections: •Basis of Presentation •Overview •Results of Operations •Financial Instruments and Risk Management •Liquidity and Capital Resources •Critical Accounting Estimates •New Accounting Standards OVERVIEW General Fortive is a multinational business with global operations with approximately 44% of our sales derived from customers outside the United States in 2025. As a company with global operations, our businesses are affected by worldwide, regional, and industry-specific economic, trade policies, fiscal policies, regulatory, and political factors. Our geographic and industry diversity, as well as the range of products, software, and services we offer, typically help limit the impact of any one industry or the economy of any single country, except for the United States, on our operating results. Given the broad range of products manufactured, software and services provided, and geographies served, we do not use any indices other than general economic trends to predict the overall outlook for the Company. Our individual businesses monitor key competitors and customers, including their sales, to the extent possible, to gauge relative performance and the outlook for the future.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTV_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
