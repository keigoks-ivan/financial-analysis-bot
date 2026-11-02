你是 stock-analyst v20 DD 的證據採集子 agent。標的：HLT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - HLT Hilton Worldwide Holdings market share gaining OR losing 2026
  - Hilton Worldwide Holdings new entrant OR displace threat Lodging 2026
  - HLT competitor design win 2026
  - Hilton Worldwide Holdings vs Lodging peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm｜as_of：2026-02-11
<<<
(2)These selected competitors exclude lesser-known regional competitors. 5 Our Guest Loyalty Program Hilton Honors is our award-winning guest loyalty program that supports our portfolio of brands. The program generates significant repeat business by rewarding guests with points for each stay at our leased, managed, franchised and timeshare properties, as well as each stay at strategic partner hotels when the stay is reserved through our booking channels, which are then redeemable for free or discounted room nights at our properties and other goods and services. Hilton Honors members can also use points earned to transact with strategic partner hotels as well as many strategic partners, including credit card providers, such as American Express, airlines, rail and car rental companies, Amazon, Lyft and others. Hilton Honors members who book through preferred Hilton channels also have access to instant benefits, including a flexible payment slider that allows members to choose nearly any combination of points and money to book a stay, an exclusive member discount and free standard Wi-Fi. Members also have access to contactless technology exclusively through the Hilton Honors app, where members can check in, choose their room and access their room using Digital Key. The program provides targeted marketing, promotions and customized guest experiences to 243 million members.…

Competition We encounter active and robust competition as a hotel and resort manager, franchisor and lessee. Competition in the hospitality industry is based on several criteria, generally including: the attractiveness of the facility; location; level of service; quality of accommodations; amenities; food and beverage options and outlets; public and meeting spaces and other guest services; consistency of service; room rate; brand reputation; and the ability to earn and redeem loyalty program points through a global system. Our properties and brands compete with other hotels, resorts, motels, inns and other accommodation rental services in their respective geographic markets or customer segments, including facilities owned by local interests, individuals, national and international chains, institutions, investment and pension funds and real estate investment trusts ("REITs"). We believe that our capabilities as a multi-branded manager, franchisor and lessee of hotels with an associated global, system-wide guest loyalty program and commercial platform help us continue to maintain our position as one of the largest and most geographically diverse hospitality companies in the world.

Our principal competitors include other branded and independent hotel operating companies, national and international hotel brands and ownership companies. While local and independent brand competitors vary, on a global scale, our primary competitors are Accor S.A., Choice Hotels International, Hyatt Hotels Corporation, Intercontinental Hotel Group, Marriott International and Wyndham Hotels & Resorts.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm｜as_of：2026-02-11
<<<
The segments of the hospitality industry in which we operate are subject to intense competition. Our principal competitors are other operators of luxury, full-service and focused-service hotels, including other major hospitality chains with well-established and recognized brands. We also compete against smaller hotel chains, independent and local hotel owners and operators, home and apartment sharing services and timeshare operators. If we are unable to compete successfully, our revenues or profits may decline.

Competition for hotel guests We face competition for individual guests, group reservations and conference business at our hotels. We compete for these customers based primarily on brand name recognition and reputation, as well as location, rates for hotel rooms, food and beverage and other services, property size and availability of guest rooms and conference and meeting space, quality of the accommodations and technology provided, previous customer experience and satisfaction, amenities and the ability to earn and redeem loyalty program points. Our competitors may have greater commercial, financial and marketing resources and more efficient technology platforms, which could allow them to improve their properties and expand and improve their marketing efforts in ways that could affect our ability to compete for guests effectively, or they could offer a type of lodging product that customers find attractive but that we do not offer.

Competition for management and franchise contracts We compete to enter into management and franchise contracts. Our ability to compete effectively is based primarily on the value and quality of our management services, brand name recognition and reputation, our access to and willingness to invest capital or provide other incentives or inducements, availability of suitable properties to maintain brand variety across geographic areas, the overall economic terms of our contracts and the economic advantages to the third-party hotel owner of retaining our management services and/or using our brands. If the properties that we manage or franchise perform less successfully than those of our competitors, if we are unable to offer terms as favorable as those offered by our competitors or if the availability of suitable properties is limited, we may not be able to compete effectively for new management or franchise contracts.

The hospitality industry demands the use of sophisticated technology and systems for property management, brand assurance and compliance, procurement, finance, human resources, reservation systems, distribution of hotel resources to current and future customers and guest amenities and the operation of the Hilton Honors guest loyalty program. These technologies may require maintenance or refinements and upgrades, and third parties may cease support of systems that are currently in use. The development and maintenance of these technologies has required and may further require significant investment by us. As various systems and technologies become outdated or new technology is required, we may not be able to replace or introduce them as quickly as needed or in a cost-effective and timely manner. If we fail to keep pace with rapidly evolving technological developments in AI, our competitive position and business results may suffer. Our competitors or other third parties may incorporate AI into their operations more quickly or successfully than us, or develop superior offerings with the aid of AI, which could impair our ability to compete effectively and adversely affect our results of operations. In some cases, hotel owners may refuse to upgrade systems or deploy new technology to replace aging or end-of-life software and/or hardware.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HLT_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
