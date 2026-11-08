你是 stock-analyst v20 DD 的證據採集子 agent。標的：BKNG。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - BKNG Booking Holdings market share gaining OR losing 2026
  - Booking Holdings new entrant OR displace threat Travel Services 2026
  - BKNG competitor design win 2026
  - Booking Holdings vs Travel Services peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm｜as_of：2026-02-18
<<<
Competition We compete globally with both online and traditional travel and restaurant reservation and related services. The markets for the services we offer are intensely competitive and constantly evolving. Competing offerings can be launched at a relatively low cost, with the pace of innovation increasing and the cost to do so decreasing as a result of Gen AI. Our current and potential competitors include the largest global technology companies, which have significantly more consumers, consumer data, and resources than we do, and may be able to leverage other aspects of their businesses to compete more effectively with us.

3 For more information regarding current and potential competitors and the competitive nature of the markets in which we operate, see Part I, Item 1A, Risk Factors - "Intense competition could reduce our market share and harm our financial performance."
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm｜as_of：2026-02-18
<<<
Intense competition could reduce our market share and harm our financial performance.

We operate in highly competitive and rapidly evolving global markets for travel and restaurant reservation services. Barriers to entry are low, and we compete with online travel companies ("OTCs"), travel service providers offering direct booking (such as airlines, hotels, and rental car companies), traditional travel agencies and operators, companies offering travel-related software, payments, or technology solutions, financial services and credit card companies, and global technology companies with significantly greater scale, data, and financial resources. For example, Google links travel search to its dominant search engine and has integrated travel products into Google Maps and its Gemini generative AI ("Gen AI") offering. Other large technology platforms and AI-native competitors are developing Gen AI-powered assistants and agents that can search, compare, recommend, and facilitate travel and dining reservations directly within their search engines, operating systems, messaging platforms, or "super-apps." These offerings may reduce consumers choosing to visit dedicated online travel platforms, reducing direct traffic, bookings, and customer relationships. Gen AI also lowers barriers to entry and enables competitors to potentially replicate or improve core functionality, personalize recommendations and pricing, and acquire customers more efficiently through non-travel consumer interactions. AI agents may further evolve into full-service booking platforms, increasing competitive pressure and disintermediating OTCs.…

6 For many consumers, the price of a travel service is the primary factor determining whether to book a reservation. Some competitors may operate at minimal or negative margins to gain market share. Travel service providers may offer lower prices through direct or AI-enabled channels, OTC and other competitors may more effectively invest in online marketing channels, and in certain markets we may need to provide discounts or other incentives in order to be competitive, any of which may make it difficult for us to maintain or grow our competitive position or profit margins, and may also result in lower revenues as a percentage of gross bookings. Consolidation among travel service providers or AI-enabled alternative travel offerings could result in lower OTC commission rates, increased discounting, and greater incentives for consumers to join closed-user groups. If we are unable to effectively offer competitive prices, our revenues, competitive position, business, and results of operations could be materially adversely affected.

Many markets may have strong local competitors with an established brand and travel service provider or restaurant relationships making expansion in that market difficult or costly. Certain markets in which we operate have unique localized preferences or lower operating margins, or from time to time have experienced declining or no growth. Some of our current and potential competitors may have greater resources or stronger competitive positions in certain regions than we do, or may be domiciled in different countries and subject to political, legal, and regulatory regimes that enable them to compete more effectively than us. Growing our business in such markets could require significant investment, which could have a negative impact on our profit margins. In some markets such as China, local requirements may restrict participation by foreign businesses, making entry into and expansion in those markets costly, difficult, or impossible. If we are unsuccessful in expanding in new and existing markets and managing that expansion, our business and results of operations could be adversely affected.

Our marketing efficiency, expressed as marketing expense as a percentage of gross bookings, and performance marketing return on investment ("ROIs") are impacted by a number of factors that are subject to variability and are in some cases outside of our control, including ADRs, costs per click, cancellation rates, foreign currency exchange rates, our ability to convert traffic to booking consumers, and the timing and effectiveness of our brand marketing campaigns. Marketing efficiency can also be impacted by the extent to which consumers come directly to our platforms for bookings and the economics of distribution channels. If our marketing efforts are less effective at generating new bookings, our marketing efficiency could decrease and our margins, revenues, and earnings growth could be adversely affected. For example, competition for desired placement in search results including among AI-generated or AI-impacted (i.e., by bot or agent activity) results could increase our costs-per-click and negatively impact our marketing efficiency. At times we may pursue a strategy of increasing marketing ROIs, which could negatively affect our gross bookings and revenue growth rates.…

Competition for well-qualified employees, especially software engineers, professionals supporting our Gen AI initiatives, and other technology professionals, is intense and costly. Our customer service resources (including outsource arrangements) may be unable to provide adequate customer service support. Additionally, our Gen AI initiatives could alter our infrastructure and workforce. Our success has led to increased efforts by our competitors and others to hire our employees. These difficulties may be amplified by increased ability to work remotely, evolving restrictions on immigration or availability of visas or work permits for skilled technology workers, requirements of applicable collective bargaining agreements, and laws in certain jurisdictions that make recruiting senior talent more difficult, such as the reductions in the partial tax exemption that benefits certain non-Dutch citizens working in the Netherlands. These factors combined with inflationary pressure on compensation has caused our personnel expenses to attract and retain key talent to increase, which may adversely affect our results of operations. If we do not 9 succeed in attracting, and retaining well-qualified employees, our business, ability to grow and innovate, competitive position, reputation, and results of operations would be adversely affected.

We are subject to competition and consumer protection laws and regulations around the world. These laws and regulations evolve, and their interpretation, application, and enforcement can also change, be unpredictable, or be affected by changing political or social pressures. As we expand our business into new areas, including building the Connected Trip vision and integrating Gen AI into our offerings, we may become subject to additional laws and regulations. We have been the subject of investigations or inquiries by national competition authorities ("Competition Authorities") and other governmental authorities regarding competition law matters, consumer protection issues, and other areas. For example, we are involved in investigations related to whether certain of Booking.com's arrangements with accommodation providers are anti-competitive, including with respect to issues like contractual parity, pricing tools or programs offered to partners, or the ranking criteria used in displaying results to consumers. See Note 16 to our Consolidated Financial Statements for information regarding certain legal proceedings in which we are involved. To resolve certain of the proceedings or investigations we have been or are involved in, we have made commitments regarding future business practices or activities including related to our parity arrangements, the information we provide about our search results ranking, and how we display prices, discounts, and popularity and availability statements.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1075531/000107553126000009/bkng-20251231.htm｜as_of：2026-02-18
<<<
Although we believe that providing an extensive collection of properties, excellent customer service, and an intuitive, easy-to-use platform are important factors influencing a consumer's decision to make a reservation, for many consumers the price of the travel service is the primary factor determining whether to book. Discounting and couponing (i.e., merchandising) occurs across the major regions in which we operate, particularly in Asia. In some cases, our competitors are willing to make little or no profit on a transaction or offer travel services at a loss in order to gain market share. As a result, it is important to offer travel services at a competitive price, whether through discounts, coupons, closed-user group rates or loyalty programs, increased flexibility in cancellation policies, or otherwise. Some of these initiatives, such as discounts, may result in lower ADRs and lower revenues as a percentage of gross bookings as they can reduce the daily room rate and are recognized as contra-revenue.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
