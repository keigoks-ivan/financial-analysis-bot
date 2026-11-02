你是 stock-analyst v20 DD 的證據採集子 agent。標的：CMG。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - CMG Chipotle Mexican Grill market share gaining OR losing 2026
  - Chipotle Mexican Grill new entrant OR displace threat Restaurants 2026
  - CMG competitor design win 2026
  - Chipotle Mexican Grill vs Restaurants peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-04）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm｜as_of：2026-02-04
<<<
Competition The fast-casual, quick-service, and casual dining segments of the restaurant industry are highly competitive with respect to, among other things, taste, price, food quality and presentation, customer service, location, convenience, brand reputation, and cleanliness and ambience of each restaurant. Our competition includes a variety of restaurants in each of these segments, including locally-owned restaurants, as well as national and regional chains. Competition from food delivery services, which offer meals from a wide variety of restaurants, also has increased in recent years and is expected to continue to increase. Many of our competitors also offer dine-in, carry-out, online, catering, and delivery services. Among our main competitors are restaurant formats that claim to serve higher quality ingredients without artificial flavors, colors and preservatives, and that serve food quickly and at a reasonable price.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-04）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1058090/000105809026000009/cmg-20251231.htm｜as_of：2026-02-04
<<<
The restaurant industry is highly competitive on factors such as taste, price, food quality and selection, customer service, brand reputation, digital engagement, advertising and promotional initiatives, and the location, attractiveness and maintenance of restaurants. We also compete with non-traditional market participants, such as “convenience meals” in the form of entrées, side dishes or meal preparation kits from grocery stores, meal kit delivery services, and “ghost” or “dark” kitchens, where meals are prepared at separate takeaway premises rather than a restaurant. Delivery aggregators and food delivery services, which provide consumers with convenient access to a broad range of competing restaurant chains and food retailers, particularly in urbanized areas, may direct potential customers to other restaurants based on paid placements, online reviews and other factors, and may form a closer relationship with our guests. Increased competition could have an adverse effect on our sales, profitability and development plans. If guest tastes or dietary preferences change, if our marketing efforts are unsuccessful, or if we are unable to compete successfully with other restaurant concepts, our business could be adversely affected.

We continue to believe our commitment to higher-quality and responsibly sourced ingredients resonates with guests and gives us a competitive advantage; however, many of our competitors also make claims related to the quality of their ingredients and lack of artificial flavors, colors and preservatives. The use of these claims by competitors, even if such claims are not accurate or comparable, may lessen our differentiation and make it more difficult for us to compete. If we are unable to continue to maintain our distinctiveness and compete effectively, our business, financial condition and results of operations could be adversely affected.

Our profitability has been and could continue to be adversely impacted by increases in labor costs, including wages and health benefits, which are some of our most significant costs. Increases could be triggered by federal, state and local laws governing matters such as minimum wages, meal and rest breaks and changes to eligibility for overtime pay; regulations regarding scheduling and benefits; increased health care and workers’ compensation insurance costs; and higher wages and benefit costs necessary to attract, hire and retain high-quality employees with the right skill sets in a highly competitive job market. In addition, state and local laws may require wage increases, restrictions on working hours and other factors that would restrict our flexibility to respond to market conditions and increase our costs without corresponding benefits. Our ability to offset higher labor costs by increasing menu prices depends on the willingness of our guests to pay the higher prices and the perceived value of our meals relative to competitors. If competitive or inflationary pressures or other factors prevent us from offsetting higher labor costs by increased menu prices, our profitability may decline.

16 Table of Contents Our ability to open and profitably operate new restaurants also is subject to risks, such as the identification and availability of desirable locations; the negotiation of acceptable lease terms; the need to obtain required governmental permits (including zoning approvals and liquor licenses) and comply with other regulatory requirements; the availability of capable contractors and subcontractors; increases in the cost and decreases in the availability of labor and building material; changes in weather, natural disasters, pandemics or other acts of God that could delay construction and adversely affect guest traffic; our ability to hire and train qualified management and restaurant employees; and general economic and business conditions. At each potential location, we compete with other restaurants and retail businesses for desirable development sites, construction contractors, management personnel, hourly employees and other resources. If we are unable to successfully manage these risks, we could face increased costs and lower than anticipated sales and earnings in future periods. Our timeline for completing construction also has gotten longer, due to landlord reluctance to commit to building in light of fluctuating interest rates, tight money supply and general economic conditions, and due to backlogs and long wait times for us to obtain required permits and utility hookups.

In addition, we purchase ingredients, packaging and equipment from both U.S. and international suppliers and we may need to increase our menu prices in response to increased inflation, higher taxes, new tariffs on imported goods, wage increases due to a tighter job market and other macro-economic factors. Higher menu prices or the perceived value of our meals relative to competitors may lead consumers to reduce their spending in our restaurants or switch to competitors’ value or lower-priced meals. If competitive or other factors prevent us from offsetting these higher costs through menu price increases, our profitability may decline.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMG_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
