你是 stock-analyst v20 DD 的證據採集子 agent。標的：LYV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - LYV Live Nation Entertainment market share gaining OR losing 2026
  - Live Nation Entertainment new entrant OR displace threat Entertainment 2026
  - LYV competitor design win 2026
  - Live Nation Entertainment vs Entertainment peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm｜as_of：2026-02-19
<<<
7 Competition Competition in the live entertainment industry is intense. We believe that we compete primarily on the basis of our ability to deliver quality music events, sell tickets and provide enhanced fan and artist experiences. We believe that our primary strengths include: •the quality of service delivered to our artists, fans, ticketing clients and corporate sponsors; •our track record and reputation in promoting and producing live music events and tours both domestically and internationally; •our artist relationships; •our global footprint; •the quality of our ticketing software and services; •our ecommerce site and effective marketing capabilities; •our diverse distribution platform of venues; •the scope, effectiveness and expertise of our advertising and sponsorship programs; and •our financial stability.

Although we believe that our products and services currently compete favorably with respect to such factors, we cannot provide any assurance that we can maintain our competitive position against current and potential competitors, especially those with significantly greater brand recognition, or greater financial, marketing, technical and other resources.

Some of our competitors in the live music promotion industry are Anschutz Entertainment Group, or AEG, Another Planet Entertainment, CTS Eventim, Jam Productions, Ltd., I.M.P., Outback Presents and TEG Dainty in addition to numerous smaller regional companies and various casinos and venues in North America, Europe, Asia and Australia. AEG operates under a number of different names including AEG Presents, Concerts West, Frontier Touring, Goldenvoice and Messina Touring Group. Some of our competitors in the live music industry have a stronger presence in certain markets, have access to other sports and entertainment venues and may have greater financial resources in those markets, which may enable them to gain a greater competitive advantage in relation to us.

In markets where we own or operate a venue, we compete with other venues to serve artists likely to perform in that general region. Consequently, touring artists have various alternatives to our venues when scheduling tours. Our main competitors in venue management include Legends Global, Madison Square Garden Entertainment Corp., The Nederlander Organization and Bowery Presents, in addition to numerous smaller regional companies in North America, Europe, Australia and New Zealand. Some of our competitors in venue management may have more attractive or a greater number of venues in certain markets, and may have greater financial resources in those markets.

The ticketing services industry includes the sale of tickets primarily through online and mobile channels, but also through telephone and ticket outlets. The transition to online and mobile ticket purchases has made it easier for technology-based companies to offer primary ticketing services and standalone, automated ticketing systems that enable venues to perform their own ticketing services or utilize self-ticketing systems. In the online environment, we compete with other websites, online event sites and ticketing companies to provide event information, sell tickets and provide other online services such as fan clubs and artist websites.

8 We also face significant and increasing competition from companies that sell self-ticketing systems, as well as from venues that choose to integrate self-ticketing systems into their existing operations or acquire primary ticketing service providers. Our competitors include primary ticketing companies such as Tickets.com, AXS, Paciolan, Inc., CTS Eventim AG, Eventbrite, eTix, SeatGeek, Ticketek and Fever; secondary ticketing companies such as StubHub, Vivid Seats, Viagogo and SeatGeek; and many others, including large technology and ecommerce companies that could enter these markets.

Our main competitors at the local market level for sponsorships and advertising dollars include local sports teams, which often offer state-of-the-art venues, strong brand association and attractive local media packages, as well as festivals, theme parks and other local events. On the national level, our competitors include the major sports leagues that sell sponsorships combined with significant national media packages.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1335258/000133525826000009/lyv-20251231.htm｜as_of：2026-02-19
<<<
Our businesses are in highly competitive industries, and we may not be able to maintain or increase our current revenue due to such competition. The live music industry competes with other forms of entertainment for consumers’ discretionary spending and within this industry we compete with other venues to book artists, and, in the markets in which we promote music concerts, we face competition from other promoters and venue operators. Our competitors compete with us for key employees who have relationships with popular music artists and who have a history of being able to book such artists for concerts and tours. These competitors may engage in more extensive development efforts, undertake more far-reaching marketing campaigns, adopt more aggressive pricing policies and make more attractive offers to existing and potential artists. Due to increasing artist influence and competition to attract and maintain artist clients, we may enter into agreements on terms that are less favorable to us, which could negatively impact our financial results. Our competitors may develop services, advertising options or music venues that are equal or superior to those we provide or that achieve greater market acceptance and brand recognition than we achieve.…

Our ticketing business faces significant competition from other national, regional and local primary ticketing service providers to secure new and retain existing clients on a continuous basis. Additionally, we face significant and increasing challenges from companies that sell self-ticketing systems and from clients who choose to self-ticket, through the integration of such systems into their existing operations or the acquisition of primary ticket services providers or by increasing sales through venue box offices and season and subscription sales. We also face competition in the resale of tickets from resale marketplaces and from other ticket resellers with online distribution capabilities. The advent of new technology, particularly as it relates to online ticketing, has amplified this competition. The intense competition that we face in the ticketing industry could cause the volume of our ticketing services business to decline. As we are also a content provider and venue operator we may face direct 14 competition with our prospective or current primary ticketing clients, who primarily include live event content providers. This direct competition with our prospective or current primary ticketing clients could result in a decline in the number of ticketing clients we have and a decline in the volume of our ticketing business, which could adversely affect our business, financial condition and results of operations.

Additionally, the market potential of live music venue sites cannot be precisely determined, and our live music venues may face competition in markets from unexpected sources. Newly constructed live music venues may not perform up to our expectations. We face significant competition for potential live music venue locations and for opportunities to acquire existing live music venues. Because of this competition, we may be unable to add to or maintain the number of our live music venues on terms we consider acceptable.

From time to time, federal, state and local authorities and/or consumers commence investigations, inquiries or litigation with respect to our compliance with applicable consumer protection, advertising, unfair business practice, antitrust (and similar or related laws) and other laws. Our businesses have historically cooperated with authorities in connection with these investigations. We are currently subject to agreements with the States of New Jersey, Maryland, Nevada, Illinois, and North Carolina and the FTC which govern, and in certain cases place limitations on, our ticketing resale practices. Our competitors in the secondary ticket sales market are not, to our knowledge, bound by such limitations (other than as a result of laws that apply equally to all secondary ticket sellers) and as a result, we may be at a competitive disadvantage. From time to time, other states, Canadian provinces and the federal government have commenced investigations or inquiries related to other aspects of our ticketing business, including a now-settled suit brought by the Canadian Competition Bureau relating to alleged deceptive marketing practices. In addition, until recently, we were bound by the terms of a consent decree with the United States Department of Justice entered into in connection with our merger with Ticketmaster Entertainment LLC, which placed certain restraints on our business.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
