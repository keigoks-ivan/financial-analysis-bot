你是 stock-analyst v20 DD 的證據採集子 agent。標的：H。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Hyatt Hotels distribution channel disruption OR shift 2026
  - H Hyatt Hotels business model transition subscription OR platform 2026
  - Lodging channel disintermediation D2C 2026
  - Hyatt Hotels go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm｜as_of：2026-02-13
<<<
Hyatt's portfolio of properties consists of full service hotels and resorts, select service hotels, all-inclusive resorts, and other properties, including timeshare, fractional, and other forms of residential and vacation units. We also offer distribution and destination management services through ALG Vacations and distribution services through Mr & Mrs Smith, a boutique and luxury global travel platform. On June 17, 2025, we completed the acquisition of Playa Hotels & Resorts N.V. ("Playa Hotels" or the "Playa Hotels Acquisition"), a leading owner, operator, and developer of all-inclusive resorts in Mexico, the Dominican Republic, and Jamaica. At December 31, 2025, our hotel portfolio consisted of 1,528 hotels and all-inclusive resorts (372,763 rooms). See Part II, Item 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations—Overview" for a breakdown of our portfolio. Our colleagues and hotel general managers are supported by our regional management teams, located in cities around the world, and our executive management team, headquartered in Chicago.

Marketing We are focused on the high-end traveler, positioning our offerings at the top of each segment in which our brands operate. Our marketing strategy is designed to drive incremental bookings, loyalty, and community through global, regional, field, and digital marketing efforts. Building and differentiating each of our brands is critical to increasing Hyatt's brand preference. We are focused on targeting the distinct guest segments that each of our brands serve and supporting the needs of the hotels by thorough analysis and application of data and analytics. We also evaluate, experiment with, and implement various artificial intelligence ("AI") tools or solutions to assist in these efforts and drive greater personalization for guests, members, and customers. The World of Hyatt loyalty program and our digital platforms are also key components of building loyalty and driving revenue. The loyalty program focuses on deepening relationships with members, driving repeat stays, guest satisfaction, recognition, and differentiated services and experiences for our most loyal guests. Our digital platforms are our primary distribution channels providing guests, customers, and members with an efficient source of information about our hotels, distinct brand experiences, and a seamless booking experience.…

Competition There is intense competition in all areas of the hospitality industry. Competition exists for hotel and resort guests, vacation membership customers, management and hotel services agreements and franchise agreements, sales of vacation and branded residential units, and online travel customers, including leisure and business travelers as well as travel agencies and tour operators. Our principal competitors are other operators of full service, select service, extended-stay, all-inclusive, and wellness properties, including other major hospitality chains with well-established and recognized brands, as well as cruise line operators. We also compete against smaller hotel chains and independent and local owners and operators and face competition from new distribution channels in the travel industry, including potential AI platforms. Additional sources of competition include large companies that offer online travel services as part of their business model, such as Alibaba, financial services providers such as credit card issuers, search engines such as Google, and peer-to-peer inventory sources that allow travelers to book stays on websites that facilitate the short-term rental of homes and apartments from owners, thereby providing an alternative to hotel rooms, such as Airbnb and Vrbo.

We compete for management and hotel services agreements based primarily on the value and quality of our management and hotel services, brand name recognition and reputation, loyalty program penetration, the level of our management fees, room rate expectations, costs associated with system-wide services, including without limitation, sales and revenue management, marketing, global care centers (including reservation and customer support), digital and technology, and digital media (collectively, "system-wide services"), the terms of our management and hotel services agreements, including compared to the terms our competitors offer, and the economic advantages to the property owner of retaining our management and hotel services and using our brand name. We compete for franchise agreements based primarily on brand name recognition and reputation, loyalty program penetration, the room rate that can be realized, costs associated with system-wide services, and the royalty fees charged.…

The number of branded lodging operators with a global reach and depth of products and offerings similar to us is limited. We believe our strong customer base, prominent brand recognition, strategic property locations, and global development team enable us to compete effectively. For additional information, see Part I, Item 1A, "Risk Factors—Risks Related to Our Business." Because we operate in a highly competitive industry, our revenues, profits, or market share could be harmed if we are unable to compete effectively, and new distribution channels, including potential AI platforms, alternatives to traditional hotels, and industry consolidation among our competitors may negatively impact our business.

Investors and others should note that we routinely announce material information to investors and the marketplace using SEC filings, press releases, public conference calls, webcasts, and the Hyatt Investor Relations website. Additionally, certain information we may disclose, particularly in the corporate responsibility context, is informed by the expectations of various 24 Table of Contents stakeholders or third-party frameworks and, as such, may not necessarily be material for purposes of our filings under U.S. federal securities laws, even if we use "material" or similar language in discussing such matters. We use these channels as well as social media channels (e.g., the Hyatt Facebook account (facebook.com/hyatt); the Hyatt Instagram account (instagram.com/hyatt); the Hyatt LinkedIn account (linkedin.com/company/hyatt); the Hyatt TikTok account (tiktok.com/@hyatt); the Hyatt X account (x.com/hyatt); and the Hyatt YouTube account (youtube.com/user/hyatt)) as a means of disclosing information about our business to our guests, customers, colleagues, investors, and the public. While not all of the information that we post to the Hyatt Investor Relations website or on our social media channels is of a material nature, some information could be deemed to be material.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm｜as_of：2026-02-13
<<<
Competition. The hospitality industry is highly competitive. Increased supply can put significant pressure on ADR at our properties as well as those of our competitors. We face competition from new distribution channels in the travel industry, including potential AI platforms; large companies that offer travel services as part of their business model; financial services providers such as credit card issuers; search engines; peer-to-peer inventory sources; and industry consolidation. We believe our brand strength and ability to manage our operations in an efficient manner will help us to continue competing successfully within the hospitality industry.

Distribution segment revenues and Adjusted EBITDA. Year Ended December 31, 2025 2024 Better / (Worse) Distribution revenues (1) $ 946 $ 1,023 $ (77) (7.5) % Other revenues (1) — 26 (26) (100.0) % Segment revenues $ 946 $ 1,049 $ (103) (9.8) % (1) See "—Results of Operations" for further discussion regarding the decrease in distribution revenues and other revenues.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
