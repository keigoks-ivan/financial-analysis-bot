你是 stock-analyst v20 DD 的證據採集子 agent。標的：SBUX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - SBUX Starbucks market share gaining OR losing 2026
  - Starbucks new entrant OR displace threat Restaurants 2026
  - SBUX competitor design win 2026
  - Starbucks vs Restaurants peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
Starbucks programs and benefits are open to every partner and designed to strengthen a culture of inclusion that values diverse perspectives and experiences – from strong partner networks to a focus on hiring internally for 90% of retail leadership roles. Our hiring and recruiting practices are competitive, fair and inclusive. They help us hire the strongest candidate for every job, every time. We offer industry-leading benefits, competitive pay, and opportunities for learning and development. When our partners feel good about their future – at Starbucks or beyond – they take care of our customers. Investing in them and prioritizing their experience creates value for everyone.

Total Rewards We have demonstrated a history of investing in our workforce by offering competitive salaries and wages by continuously assessing the current business environment and labor market. We have consistently made enhancements in wages in order to attract talent to support our growth strategy and to elevate the customer experience. To foster a stronger sense of ownership and align the interests of partners with shareholders, restricted stock units are provided to eligible non-executive partners under our broad-based stock incentive programs. Furthermore, we offer competitive pay and a collection of benefits that are best in class. Partners in the U.S., which is our largest and most mature market, can: •Grow their careers with us. We established a goal to fill 90% of retail leadership roles internally, creating a way for our hourly partners to build a career at Starbucks.

Competition Our primary competitors for coffee beverage sales are specialty coffee retailers and shops. We believe that our customers choose among specialty coffee retailers and shops primarily on the basis of product quality, brand reputation, service, and convenience, as well as price. We continue to experience direct competition from large competitors in the quick-service restaurant sector and the ready-to-drink coffee beverage market, in addition to both well-established and start-up companies in many international markets. We also compete with restaurants and other specialty retailers for prime retail locations and qualified personnel to operate both new and existing stores.

Our coffee and tea products sold through our Channel Development segment compete directly against specialty coffees and teas sold through grocery stores, warehouse clubs, specialty retailers, convenience stores, and foodservice accounts and also compete indirectly against all other coffees and teas on the market.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/829224/000082922425000114/sbux-20250928.htm｜as_of：2025-11-14
<<<
Our continued success depends on our ability to adapt brand, marketing, promotional, advertising, and pricing strategies to shifting economic conditions, competitive pressures, and evolving customer preferences. We operate in a complex and costly 11 Table of Contents marketing environment. Decisions to collaborate or refrain from collaborating with certain parties may impact our brand image and, consequently, our financial performance. Our programs may not always reach consumers as intended, particularly given the wide range of generational, geographical, cultural, and socioeconomic characteristics and channels of communication used by our customers, and effective resource allocation across channels, including digital, is critical. Additionally, factors such as operating costs, competitor strategies, and inflation may affect our pricing decisions, which could impact demand. For example, there is no guarantee future cost increases will be absorbed by customers. If our marketing or pricing strategies underperform relative to competitors, our sales and market share could decline. Likewise, if we do not continuously strengthen our capabilities in marketing, data analytics (including artificial intelligence and machine learning) and innovation to understand and maintain or grow consumer interest, brand loyalty, and market share while strategically expanding into other profitable categories of the commercial beverage industry, our business could be negatively affected.

Operating in 89 global markets, we face diverse cultural, regulatory, geopolitical, and economic environments. Our success depends on navigating these differences effectively and leveraging operational strengths across markets. However, planned initiatives may not resonate uniformly with customers and could lead to unexpected shifts in perception or market share. Our international operations are also subject to additional inherent risks of conducting business abroad, such as: •Uncertainty in economic, legal, regulatory, social, and political conditions, including rising anti-American sentiment in certain markets; •Governmental trade and investment restrictions, such as tariffs, export duties, ownership limits, and favoritism toward local competitors; •Economic or trade sanctions limiting product sourcing or business operations; •Delays in store openings due to external factors, competition, or limited access to affordable real estate, potentially impacting financial performance; •Operational and supply chain challenges abroad, including staffing, logistics, product consistency, and cultural or language barriers; •Slower-than-expected growth in disposable income in developing economies; •Complex and varying interpretations of laws and regulations, including those related to taxes, labor, privacy, and responsible business matters; •Local employment laws increasing the cost and complexity of hiring and termination; •Labor disruptions due to geopolitical instability or social unrest; •Health and safety regulations affecting store operations; •Challenges in enforcing intellectual property and contract rights; •Foreign currency fluctuations and restrictions on currency use or fund repatriation; and •Licensing and…

The specialty coffee market is highly competitive across product quality, innovation, service, convenience (e.g., delivery and mobile ordering), and price. We face increasing competition in all channels and markets and do not hold leadership positions in every segment. In the U.S., large quick-service competitors offering coffee, tea, and other competitive products may reduce customer traffic and transaction value. Globally, competition from established brands, new entrants, and smaller specialty operators may hinder growth and impact sales. Furthermore, our competitors may attempt to gain market share by offering products at prices at or below those typically offered by our company, which may require us to increase spending on advertising and promotions and/or reduce prices.

Our ability to compete depends on product improvement and innovation, pricing, customer experience, and strategic investments in store development, technology, and digital engagement. If we are unable to respond to consumer demand for healthy beverages and foods, or our competitors respond more effectively, this could have a negative effect on our business. However, our competitive strategies may not always succeed and could have unintended consequences. Declines in consumer demand—due to shifting preferences, economic pressures, or changes in routines—could also negatively affect our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
