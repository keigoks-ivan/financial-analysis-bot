你是 stock-analyst v20 DD 的證據採集子 agent。標的：QCOM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - QCOM QUALCOMM top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - QUALCOMM customer concentration risk disclosure
  - bankruptcy OR downgrade OR guidance cut 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-04）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm｜as_of：2026-11-04
<<<
QCT also faces competition, which may intensify in the future, from products internally developed by our customers, including some of our largest customers. Our competitors devote significant amounts of their financial, technical and other resources to develop and market competitive products and, in some cases, to develop and adopt competitive technologies, and those efforts may materially and adversely affect us. Although we have attained a significant position in the semiconductor industry, many of our current and potential competitors may have advantages over us. These and other risks related to competition are more fully described in “Part I, Item 1A. Risk Factors” in this Annual Report, including the Risk Factors titled “The semiconductor industry is subject to intense competition in an environment of rapid technological change. Our success depends in part on our ability to adapt to such change and compete effectively; and such change and competition could result in decreased demand for our products and technologies or declining average selling prices for our products or those of our customers or licensees” and “Our business, particularly our semiconductor business, may suffer as a result of our customers vertically integrating (i.e., developing their own integrated circuit products).”

Revenue Concentrations and Significant Customers A small number of customers/licensees historically have accounted for a significant portion of our consolidated revenues. In fiscal 2026, revenues from Apple and Samsung each comprised 10% or more of our consolidated revenues. Additional information regarding revenue concentrations is provided in this Annual Report in “Notes to Consolidated Financial Statements, Note 2. Composition of Certain Financial Statement Items” and “Notes to Consolidated Financial Statements, Note 8. Segment Information.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-04）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm｜as_of：2026-11-04
<<<
Risk Factors Summary: RISKS RELATED TO REVENUE AND CUSTOMER CONCENTRATION •We derive a significant portion of our revenues from a small number of mobile handset customers and licensees, and particularly from their sale of premium-tier handset devices. If revenues derived from these customers or licensees decrease or the timing of such revenues fluctuates, our business and results of operations could be negatively affected.

Risk Factors: RISKS RELATED TO REVENUE AND CUSTOMER CONCENTRATION We derive a significant portion of our revenues from a small number of mobile handset customers and licensees, and particularly from their sale of premium-tier handset devices. If revenues derived from these customers or licensees decrease or the timing of such revenues fluctuates, our business and results of operations could be negatively affected.

Although we expect to derive an increasing portion of our revenues from areas outside of mobile handsets, such as automotive, IoT and data center, we continue to derive a significant portion of our revenues from a small number of mobile handset customers and licensees, and particularly from their sale of premium-tier handset devices. Device share in the mobile industry, particularly at the premium tier, is concentrated among a few companies, including Apple, Samsung and certain Chinese original equipment manufacturers (OEMs), many of whom are or have in the past been our largest customers. This concentration means that the loss of any one of our key mobile handset customers, or a significant reduction in purchases from any such customer, whether due to such customer’s use of their own integrated circuit products (i.e., vertical integration) or our competitors’ integrated circuit products, government restrictions, a decline in global, regional or local economic conditions, a decline in consumer demand or any other reason, would have a significant negative impact on our business. For example, Apple has historically purchased our modem products for use in its devices and has historically been one of our largest customers, but we expect that Apple will primarily use its own internally developed modem products, rather than our products, in its devices going forward.…

Certain of our largest mobile handset customers (for example, Samsung and Xiaomi) have developed their own integrated circuit products, which they have in the past used, and/or currently use, in certain of their devices. We expect such customers will in the future use their own integrated circuit products in some or all of their devices, rather than our products, and additional customers may also develop and use their own integrated circuit products. In addition, although Apple has historically purchased our modem products for use in its devices and has historically been one of our largest customers, we expect that Apple will primarily use its own internally developed modem products, rather than our products, in its devices going forward, which will have a significant negative impact on our QCT revenues, results of operations and cash flows.

Our products, technologies and platform solutions face significant competition. We expect this competition to intensify as our current competitors expand their product offerings, improve their products or reduce the prices of their products as part of a strategy to maintain existing business and customers or attract new business and customers, as new opportunities develop, and as new competitors enter the industry. Competition in the semiconductor industry is affected by various factors that include, among others: customer concentrations in various segments (e.g., handsets and data center); vertical integration; competition in certain geographic regions; government intervention or support of national industries or competitors; geopolitical tensions, which may drive customer preference toward local suppliers; the ability to maintain product differentiation in light of evolving industry standards and speed of technological change (including the transition to smaller geometry process technologies, the demand for always on, always connected capabilities, the increasing use of AI and machine learning technologies and the need to run complex AI-based applications on devices and in data centers, and the need for related software and developer ecosystems); access to capacity in the supply chain; and value-added features that drive selling prices and consumer demand for new devices.

We anticipate that additional competitors will introduce products as a result of growth opportunities in the industries in which we operate, the trend toward global expansion by foreign and domestic competitors, and technological and public policy changes. Additionally, the semiconductor industry has experienced and may continue to experience consolidation, which could result in significant changes to the competitive landscape. Certain of our largest customers have in the past used, currently use and may in the future use our competitors’ integrated circuit products in some or all of their devices, rather than our products. Further, certain of those customers have developed, are developing or may develop their own integrated circuit products (effectively making them competitors), which they have in the past used, currently use or may in the future use in some or all of their devices, rather than our products. See also the Risk Factor titled “Our business, particularly our semiconductor business, may suffer as a result of our customers vertically integrating (i.e., developing their own integrated circuit products).”
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
