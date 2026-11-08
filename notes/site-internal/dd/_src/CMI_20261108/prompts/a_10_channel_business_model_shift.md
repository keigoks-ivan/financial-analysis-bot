你是 stock-analyst v20 DD 的證據採集子 agent。標的：CMI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Cummins distribution channel disruption OR shift 2026
  - CMI Cummins business model transition subscription OR platform 2026
  - Specialty Industrial Machinery channel disintermediation D2C 2026
  - Cummins go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
ITEM 1. Business OVERVIEW We were founded in 1919 as Cummins Engine Company, a corporation in Columbus, Indiana, and one of the first diesel engine manufacturers. In 2001, we changed our name to Cummins Inc. We are a global power leader committed to powering a more prosperous world. Since 1919, we have delivered innovative solutions that move people, goods and economies forward. Our five reportable segments - Engine, Components, Distribution, Power Systems and Accelera - offer a broad portfolio, including advanced diesel, electric and hybrid powertrains; integrated power generation systems; critical components such as aftertreatment, turbochargers, fuel systems, controls, transmissions, axles and brakes; and zero emissions technologies like battery and electric powertrain systems. With a global footprint, deep technical expertise and an extensive service network, we deliver dependable, cutting-edge solutions tailored to our customers' needs, supporting them through the energy transition with our Destination Zero strategy. We sell our products to original equipment manufacturers (OEMs), distributors, dealers and other customers worldwide. We serve our customers through a service network of approximately 640 wholly-owned, joint venture and independent distributor locations and more than 13,000 Cummins certified dealer locations in approximately 190 countries and territories.

REPORTABLE SEGMENTS We have five complementary reportable segments: Engine, Components, Distribution, Power Systems and Accelera. These segments share technology, customers, strategic partners, brand recognition and our distribution network in order to compete more efficiently and effectively in their respective markets. In each of our reportable segments, we compete worldwide with a number of other manufacturers and distributors that produce and sell similar products. Our products primarily compete on the basis of performance, price, total cost of ownership, fuel economy, emissions compliance, speed of delivery, quality and customer support.

The Components segment is organized around the following businesses: •Drivetrain and braking systems - We design, manufacture and supply drivetrain systems, including axles, drivelines, brakes and suspension systems primarily for commercial vehicle and industrial applications. We also market and sell on-highway, off-highway and other products principally for OEM dealers and other independent distributors and service garages within the aftermarket industry. We primarily serve markets in North America, Europe, South America, Asia Pacific, China and India.

Customers of the Components segment generally include the Engine, Distribution, Power Systems and Accelera segments, joint ventures including Tata Cummins Ltd., Dongfeng Cummins Engine Co., Ltd. and Beijing Foton Cummins Engine Co., Ltd., truck manufacturers and other OEMs, many of which are also customers of the Engine segment, such as PACCAR, Daimler, AB Volvo, Traton, Stellantis and other manufacturers that use our components in their product platforms.

7 Table of Contents Distribution Segment Distribution segment sales and EBITDA as a percentage of consolidated results were: Years ended December 31, 2025 2024 2023 Percent of consolidated net sales (1)

30 % 27 % 25 % Percent of consolidated EBITDA (1) 34 % 27 % 24 % (1) Measured before intersegment eliminations The Distribution segment is our primary sales, service and support channel. The segment serves our customers and certified dealers through a worldwide network of wholly-owned, joint venture and independent distribution locations. Wholly-owned locations operate and serve markets in the seven geographic regions noted below. Joint venture locations serve markets in South America, Southeast Asia, Middle East and India while independent distribution locations serve markets in these and other geographies.

Distribution’s mission encompasses the sale and support of a wide range of products and services, including power generation systems, high-horsepower engines, heavy-duty and medium-duty engines designed for on- and off-highway use, application engineering services, custom-designed assemblies, retail and wholesale aftermarket parts and in-shop and field-based repair services. We also provide selected sales and aftermarket support for the Accelera business. Our familiarity with a wide range of market applications allows us to tailor sales, service and support to meet customer-specific needs.

The Distribution segment is organized and managed as seven geographic regions, including North America, Europe, Asia Pacific, China, India, Latin America and Africa and Middle East. Across these regions, our locations compete with distributors or dealers that offer similar products. In many cases, these competing distributors or dealers are owned by, or affiliated with the companies that are listed as competitors of the Engine, Components or Power Systems segments. These competitors vary by geographical location and application market.

JOINT VENTURES, ALLIANCES AND NON-WHOLLY-OWNED SUBSIDIARIES We have a number of joint venture agreements and alliances with business partners around the world. Our joint ventures are either distribution or manufacturing entities. We also own controlling interests in non-wholly-owned manufacturing and distribution subsidiaries.

9 % 91 27 % Distribution entities Komatsu Cummins Chile, Ltda. 54 15 % 55 19 % 55 16 % All other distributors 25 7 % 17 6 % 16 4 % Cummins share of net income (2)

Distribution Entity Komatsu Cummins Chile, Ltda. - Komatsu Cummins Chile, Ltda. is a joint venture with Komatsu America Corporation. The joint venture is a distributor that offers the full range of our products and services to customers and end-users in Chile and Peru. See further discussion of our distribution network under the Distribution segment section above.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/26172/000002617226000009/cmi-20251231.htm｜as_of：2026-02-10
<<<
EXECUTIVE SUMMARY AND FINANCIAL HIGHLIGHTS Overview We are a global power leader committed to powering a more prosperous world. Since 1919, we have delivered innovative solutions that move people, goods and economies forward. Our five reportable segments - Engine, Components, Distribution, Power Systems and Accelera - offer a broad portfolio, including advanced diesel, electric and hybrid powertrains; integrated power generation systems; critical components such as aftertreatment, turbochargers, fuel systems, controls, transmissions, axles and brakes; and zero emissions technologies like battery and electric powertrain systems. With a global footprint, deep technical expertise and an extensive service network, we deliver dependable, cutting-edge solutions tailored to our customers' needs, supporting them through the energy transition with our Destination Zero strategy. We sell our products to original equipment manufacturers (OEMs), distributors, dealers and other customers worldwide. We have long-standing relationships with many of the leading manufacturers in the markets we serve, including PACCAR Inc., Traton Group, Daimler Trucks AG and Stellantis N.V. We serve our customers through a service network of approximately 640 wholly-owned, joint venture and independent distributor locations and more than 13,000 Cummins certified dealer locations in approximately 190 countries and territories.

Our segment reporting structure is organized according to the products and markets each segment serves. The Engine segment produces engines (15 liters and smaller) and associated parts for sale to customers in on-highway and various off-highway markets. Our engines are used in trucks of all sizes, buses and recreational vehicles, as well as in various industrial applications, including construction, agriculture, power generation systems and other off-highway applications. The Components segment sells axles, drivelines, brakes and suspension systems for commercial diesel and natural gas applications, aftertreatment systems, turbochargers, fuel systems, valvetrain technologies, automated transmissions and electronics. The Distribution segment includes wholly-owned and partially-owned distributorships engaged in wholesaling engines, generator sets and service parts, as well as performing service and repair activities on our products, maintaining relationships with various OEMs throughout the world and providing selected sales and aftermarket support for our Accelera business. The Power Systems segment is an integrated power provider, which designs, manufactures and sells standby and prime power generators, engines (16 liters and larger) for standby and prime power generator sets and industrial applications (including mining, oil and gas, marine, rail and defense), alternators and other power components. The Accelera segment designs, manufactures, sells and supports electrified power systems with innovative components and subsystems, including battery and electric powertrain technologies.…

Distribution Segment Results Financial data for the Distribution segment was as follows: Favorable/(Unfavorable) Years ended December 31, 2025 vs. 2024 2024 vs. 2023 In millions 2025 2024 2023 Amount Percent Amount Percent External sales $ 12,386 $ 11,352 $ 10,199 $ 1,034 9 % $ 1,153 11 % Intersegment sales 19 32 50 (13) (41) % (18) (36) % Total sales 12,405 11,384 10,249 1,021 9 % 1,135 11 % Research, development and engineering expenses 53 55 57 2 4 % 2 4 % Equity, royalty and interest income from investees 105 90 97 15 17 % (7) (7) % Interest income 23 37 34 (14) (38) % 3 9 % Segment EBITDA 1,808 1,378 1,209 430 31 % 169 14 % Percentage Points Percentage Points Segment EBITDA as a percentage of total sales 14.6 % 12.1 % 11.8 % 2.5 0.3 Sales for our Distribution segment by region, were as follows: Favorable/(Unfavorable)
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
