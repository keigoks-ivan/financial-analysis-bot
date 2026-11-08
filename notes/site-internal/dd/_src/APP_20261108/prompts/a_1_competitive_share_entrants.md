你是 stock-analyst v20 DD 的證據採集子 agent。標的：APP。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - APP AppLovin market share gaining OR losing 2026
  - AppLovin new entrant OR displace threat Advertising Agencies 2026
  - APP competitor design win 2026
  - AppLovin vs Advertising Agencies peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm｜as_of：2026-02-19
<<<
•MAX is our monetization solution, utilizing an advanced in-app bidding technology that optimizes the value of a publisher’s advertising inventory by running a real-time competitive auction, driving more competition, and higher returns for publishers.

MAX MAX is our in-app bidding solution that optimizes the value of publishers' advertising inventory by running a single unbiased, real-time competitive auction, driving more competition and higher returns for publishers. MAX auctions are more effective than historical tools and approaches because MAX yields more targeted users for advertisers and enables publishers to achieve better competitive prices for each impression. Many developers who integrate MAX have experienced a measurable increase in their average revenue per daily active user over traditional monetization tools and save countless hours because they are able to automate manual monetization work through its advanced feature set. As a result, MAX has become the preferred in-app bidding solution for many publishers worldwide, helping drive meaningful growth and momentum for AppLovin.

MAX includes the following features: •Advanced in-app bidding technology: MAX’s competitive auctions happen in real time with most bidding platforms in the industry bidding simultaneously for developers’ inventory at high volume. The competitive global demand helps maximize average revenue per user on each impression with many developers experiencing a measurable increase when moving to MAX.

We intend to pursue additional intellectual property protection to the extent we believe it would advance our business objectives and maintain our competitive position. Notwithstanding these efforts, there can be no assurance that we will adequately protect our intellectual property or that it will provide any competitive advantage. We take steps to protect our proprietary information, in part, by entering into confidentiality agreements with our employees, consultants, developers, and 5 Table of Contents vendors, and generally limiting access to and distribution of our proprietary information. However, we cannot assure you that the steps taken by us will prevent misappropriation of our proprietary rights. Despite our efforts to protect our intellectual property rights, unauthorized parties may attempt to copy aspects of our advertising solutions or obtain and use information that we regard as proprietary. Policing unauthorized use of our proprietary rights is difficult and time consuming. Further, our intellectual property rights may be invalidated, circumvented, or challenged. In addition, the laws of some foreign countries do not protect our proprietary rights to the same extent as the laws of the United States, and many foreign countries do not enforce these laws as diligently as government agencies and private parties in the United States.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm｜as_of：2026-02-19
<<<
In addition, our ability to execute our strategy depends in part on our continued ability to identify, hire, develop, motivate, and retain highly skilled employees, particularly in the competitive fields of AI development, machine learning, product management, engineering and data science. We believe that our corporate culture has been an important factor in our ability to hire and retain key employees, and if we are unable to maintain our corporate culture as we grow, we may be unable to foster the innovation, creativity, and teamwork we believe we need to support our growth. While we believe we compete favorably, competition for highly skilled employees is intense, particularly in Silicon Valley, where our headquarters is located. Interviewing, hiring, and integrating new employees has been and will continue to be challenging as we continue to navigate the global working environment. If we are unable to identify, hire, and retain highly skilled employees, our business, financial condition, and results of operations could be adversely affected.

We face significant competition in the advertising ecosystem. Advertisers often engage with numerous advertising platforms and networks to purchase advertisements and developers often engage with numerous tools to market and monetize their apps. Accordingly, we face significant competition from traditional, online, and mobile businesses that provide ad networks and platforms, and other services for advertisers to reach relevant audiences. We also face competition from providers of developer tools that enable developers to reach their audiences or manage or optimize their advertising campaigns. These companies vary in size and include Meta, Google, Amazon, and Unity Software as well as various private companies, several of which are also our partners and clients. Clients who are also competitors may decide to invest in their own offerings rather than continue to use our advertising solutions.

We also face competition for advertising spending from game platforms such as personal computer and console games, and other leisure time activities, such as television, movies, music, sports, and the internet. During periods of macroeconomic uncertainty, levels of advertising spending have historically decreased and are likely to decrease and therefore this competition may intensify, which has at times harmed and may in the future harm our revenue. To the extent we explore entering into new markets or new business opportunities in the advertising ecosystem, or otherwise, we may also compete with established businesses with more experience in such areas.

Some of our current and potential competitors may be domiciled in different countries and subject to political, legal, and regulatory regimes that enable them to compete more effectively than us, particularly outside of the United States. Some of our current and potential competitors may have greater resources, more diversified revenue streams, better technological or data analytics capabilities, or stronger brands or competitive positions in certain product segments, geographic regions, or user demographics than we do. If clients prefer our competitors’ products or services over our own, or if our competitors are better able to adapt to changes in the preferences of advertisers or users, regulations, or other developments, our business, financial condition, and results of operations could be adversely affected.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
