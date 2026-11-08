你是 stock-analyst v20 DD 的證據採集子 agent。標的：MAR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MAR Marriott International market share gaining OR losing 2026
  - Marriott International new entrant OR displace threat Lodging 2026
  - MAR competitor design win 2026
  - Marriott International vs Lodging peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm｜as_of：2026-02-10
<<<
Competition There is robust competition within the hospitality industry, including as relates to brand recognition and reputation, location, guest satisfaction, room rates, quality of service and accommodations, property amenities and offerings, and guest loyalty programs and offerings (including co-branded credit cards). We encounter strong competition in the short-term lodging market from regional, national, and international chains that operate lodging properties or franchise their brands, lodging properties that are not affiliated with a chain, and online platforms, including Airbnb and Vrbo, that allow travelers to book short-term rentals of homes and apartments as an alternative to hotel rooms. Although we believe that our strong brand recognition assists us in attracting and retaining guests and hotel owners, we compete against many other companies with strong brands and guest appeal, including Hilton, IHG Hotels & Resorts, Hyatt, Wyndham Hotels & Resorts, Accor, Choice Hotels, Best Western Hotels & Resorts, and others. Our direct digital channels also compete for guests with online travel 8 Table of Contents services platforms, such as Expedia.com, Priceline.com, Booking.com, Travelocity.com, Orbitz.com, and Trip.com, and search engines such as Google, Bing, Yahoo, and Baidu.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm｜as_of：2026-02-10
<<<
Risks Relating to Our Industry Our industry is highly competitive, which may impact our ability to compete successfully for guests. We operate in markets that contain many competitors. Our hotel brands and other lodging offerings generally compete with regional, national, and international chains that operate lodging properties or franchise their brands, lodging properties that are not affiliated with a chain, and online platforms that allow travelers to book short-term rentals of homes and apartments. Our ability to remain competitive and attract and retain business, group, and leisure travelers depends on our success in distinguishing and driving preference for our lodging products and services, including our Loyalty Program, direct digital channels, consumer-facing technology platforms and services, our co-branded credit cards, and other offerings. If we cannot compete successfully in these areas, our business, liquidity, financial condition, and results of operations could be materially adversely affected. Further, new lodging supply in individual markets could have a negative impact on the hotel industry and hamper our ability to maintain or increase room rates or occupancy in those markets.

Our business depends on the quality and reputation of our Company and our brands, and any deterioration could adversely impact our market share, reputation, business, financial condition, or results of operations. Many factors can affect the reputation and value of our Company or one or more of our brands, hotels in our system, or other offerings, including adherence to service and other brand standards; matters related to, or incidents involving, food quality and safety, guest and associate safety, health and cleanliness, sustainability, supply chain management, access to opportunity, human rights, and support for local communities; actions perceived as relating to political or social matters; and compliance with applicable laws. Reputational value is also based on perceptions, and broad access to social media makes it easy for anyone to provide public feedback that can influence perceptions of us, our brands, hotels in our system, or other offerings, and it may be difficult to control or effectively manage negative publicity, regardless of whether it is accurate. While reputations may take decades to build, negative incidents can quickly erode trust and confidence, particularly if they result in adverse mainstream and social media publicity, governmental investigations, proceedings or penalties, or litigation.…

Our business could suffer if we or the hotels in our system cannot attract and retain associates or as the result of the loss of the services of our senior executives. We and the hotels in our system compete with other companies both within and outside of our industry for personnel. We and the hotels in our system have in the past experienced, and could in the future experience, challenges hiring for certain positions due to various factors, such as increasing wage expectations or competition for labor from other industries, and these circumstances could continue or worsen in the future to an extent and for durations that we are not able to predict. If we or the hotels in our system cannot recruit, train, develop, and retain sufficient numbers of associates, we could experience significant negative impacts on operations, associate morale and turnover, guest satisfaction, or our internal control environment. Insufficient numbers of associates could also limit our ability to grow and expand our business. Labor shortages have in the past resulted, and could in the future result, in higher wages and initial hiring costs, increasing our labor costs and labor costs at hotels in our system, which could reduce our revenues and profits.…

Our Loyalty Program plays a significant role in our business, and unfavorable developments affecting the program could adversely affect our business and results of operations. Our Loyalty Program is an important aspect of our business. Our Loyalty Program faces significant competition from the loyalty programs offered by other hospitality companies, banks, airlines, and others. There is significant competition among loyalty programs in terms of the value and utility of program currency, rewards ranges and values, other program terms and conditions, and other program features, including co-branded credit card affiliations and offerings. If we are not able to maintain a competitive and attractive loyalty program or if we make changes to our Loyalty Program, including as a result of legal or regulatory requirements or considerations, we could experience significant adverse effects on our reputation, business, financial condition, or results of operations, including our ability to acquire, engage, and retain members in our Loyalty Program and our ability to operate other programs (including our co-branded credit card program).…

A failure to keep pace with developments in technology could impair our operations or competitive position. The lodging industry continues to demand the use of sophisticated technology and systems, including those used for our reservation, customer relationship management, finance, analytics, revenue management, property management, human resources and payroll systems, our Loyalty Program, and technologies we make available to our guests and for associates, and these and other technologies and systems must be refined, updated, and/or replaced with more advanced systems on a regular basis. Our business could suffer if we cannot refine, update, and/or replace technologies and systems as quickly or effectively as our competitors, sufficiently in advance of obsolescence or performance failure or degradation, or within budgeted costs and time frames. We also may not achieve the benefits that we anticipate from any new or upgraded technology or system, and a failure to do so could result in higher than anticipated costs or lower guest satisfaction or could impair our operating results. We are undertaking a multi-year transformation of our reservations, property management, and loyalty systems. The development and deployment of our new systems could involve delays, system interruptions, compromises of data security, or other operational impacts, including impacts on our financial reporting or internal control environment.…

Additional cybersecurity incidents could have adverse effects on our business. We have enhanced our security measures to safeguard our information systems and data, and we intend to continue implementing additional measures in the future, but, as we have seen in the past, our measures may not be sufficient to maintain the confidentiality, security, or availability of the data we collect, store, and use to operate our business. Security measures implemented by our hotel owners, service providers, and other third parties with whom we or they do business also may not be sufficient, as we have seen in the past. Efforts to hack or circumvent security measures, efforts to gain unauthorized access to, exploit or disrupt the operation or integrity of our data or information systems, failures of information systems or software to operate as designed or intended, viruses, “ransomware” or other malware, “supply chain” attacks, “phishing” or other types of business communications compromises, operator error, or inadvertent releases of data have impacted, and may in the future impact, our information systems and records or those of our hotel owners, service providers, or other third parties with whom we or they do business.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MAR_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
