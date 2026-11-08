你是 stock-analyst v20 DD 的證據採集子 agent。標的：QCOM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - QCOM QUALCOMM market share gaining OR losing 2026
  - QUALCOMM new entrant OR displace threat Semiconductors 2026
  - QCOM competitor design win 2026
  - QUALCOMM vs Semiconductors peers market share trend 2025 2026


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
The industries in which QCT operates are intensely competitive. QCT competes worldwide with a number of U.S. and international designers and manufacturers of semiconductors, ranging from multinational companies with integrated research and development, manufacturing, sales and marketing organizations across a broad spectrum of product lines, to companies that are focused on a single application, industry or standard product, including those that produce products for industries and applications including handsets, automotive or IoT, among others. Most of these competitors compete with us with respect to some, but not all, of our product lines. Companies that provide on-device AI, high-performance and low-power computing and connectivity-based integrated circuit products and/or software are generally competitors or potential competitors. As a result of global expansion by foreign and domestic competitors, technological changes, device manufacturer concentrations, limited global supply capacity, vertical integration and the potential for further industry consolidation, we anticipate the 9 industry to remain very competitive. We believe that the principal competitive factors for our products include performance, level of integration, quality, compliance with industry standards, price, time-to-market, system cost, design, engineering and supply chain capabilities, new product innovation, growth and scaling of distribution channels, desire by certain customers to use multiple suppliers and customer support. QCT also competes in both single-mode and multimode environments against alternative communications technologies.…

QCT also faces competition, which may intensify in the future, from products internally developed by our customers, including some of our largest customers. Our competitors devote significant amounts of their financial, technical and other resources to develop and market competitive products and, in some cases, to develop and adopt competitive technologies, and those efforts may materially and adversely affect us. Although we have attained a significant position in the semiconductor industry, many of our current and potential competitors may have advantages over us. These and other risks related to competition are more fully described in “Part I, Item 1A. Risk Factors” in this Annual Report, including the Risk Factors titled “The semiconductor industry is subject to intense competition in an environment of rapid technological change. Our success depends in part on our ability to adapt to such change and compete effectively; and such change and competition could result in decreased demand for our products and technologies or declining average selling prices for our products or those of our customers or licensees” and “Our business, particularly our semiconductor business, may suffer as a result of our customers vertically integrating (i.e., developing their own integrated circuit products).”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-04）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm｜as_of：2026-11-04
<<<
•The semiconductor industry is subject to intense competition in an environment of rapid technological change. Our success depends in part on our ability to adapt to such change and compete effectively; and such change and competition could result in decreased demand for our products and technologies or declining average selling prices for our products or those of our customers or licensees.

The semiconductor industry is subject to intense competition in an environment of rapid technological change. Our success depends in part on our ability to adapt to such change and compete effectively; and such change and competition could result in decreased demand for our products and technologies or declining average selling prices for our products or those of our customers or licensees.

Our products, technologies and platform solutions face significant competition. We expect this competition to intensify as our current competitors expand their product offerings, improve their products or reduce the prices of their products as part of a strategy to maintain existing business and customers or attract new business and customers, as new opportunities develop, and as new competitors enter the industry. Competition in the semiconductor industry is affected by various factors that include, among others: customer concentrations in various segments (e.g., handsets and data center); vertical integration; competition in certain geographic regions; government intervention or support of national industries or competitors; geopolitical tensions, which may drive customer preference toward local suppliers; the ability to maintain product differentiation in light of evolving industry standards and speed of technological change (including the transition to smaller geometry process technologies, the demand for always on, always connected capabilities, the increasing use of AI and machine learning technologies and the need to run complex AI-based applications on devices and in data centers, and the need for related software and developer ecosystems); access to capacity in the supply chain; and value-added features that drive selling prices and consumer demand for new devices.

We compete with many different semiconductor companies, ranging from multinational companies with integrated research and development, manufacturing, sales and marketing organizations across a broad spectrum of product lines, to companies that are focused on a single application, industry or standard product, including those that produce products or provide services for mobile handsets, automotive, IoT or data center, among others. Most of these competitors compete with us with respect to some, but not all, of our businesses or product lines. Companies that provide on-device AI, high-performance and low-power computing and connectivity-based integrated circuit products and/or software, or that provide custom silicon solutions for data center infrastructure, are generally competitors or potential competitors.

We anticipate that additional competitors will introduce products as a result of growth opportunities in the industries in which we operate, the trend toward global expansion by foreign and domestic competitors, and technological and public policy changes. Additionally, the semiconductor industry has experienced and may continue to experience consolidation, which could result in significant changes to the competitive landscape. Certain of our largest customers have in the past used, currently use and may in the future use our competitors’ integrated circuit products in some or all of their devices, rather than our products. Further, certain of those customers have developed, are developing or may develop their own integrated circuit products (effectively making them competitors), which they have in the past used, currently use or may in the future use in some or all of their devices, rather than our products. See also the Risk Factor titled “Our business, particularly our semiconductor business, may suffer as a result of our customers vertically integrating (i.e., developing their own integrated circuit products).”

In addition, employees and former employees, in particular former employees who become employees of our competitors, customers, licensees or other third parties, including state actors, have in the past and may in the future 25 misappropriate, wrongfully use, publish or provide to our competitors, customers, licensees or other third parties, including state actors, our technology, intellectual property or other proprietary or confidential information. This risk is exacerbated as competitors for talent, particularly engineering talent, increasingly attempt to hire our employees. See also the Risk Factor titled “We may not be able to attract or retain qualified employees.” Similarly, we provide access to certain of our technology, intellectual property and other proprietary or confidential information to our direct and indirect customers and licensees and certain of our consultants, who have in the past and may in the future wrongfully use such technology, intellectual property or information, or wrongfully disclose such technology, intellectual property or information to third parties, including our competitors or state actors. We have also provided and may continue to provide access to certain of our technology, intellectual property and other proprietary or confidential information to certain joint venture partners, including those affiliated with state actors in foreign jurisdictions.…

Our future success depends upon the continued service of our executive officers and other key management and technical personnel, and on our ability to continue to identify, attract, retain and motivate them. Implementing our business strategy requires specialized engineering and other talent, as our revenues are highly dependent on technological and product innovations. In addition, in order to extend and grow our business in industries and applications beyond mobile handsets, we need to attract, retain and motivate engineering and other technical personnel with specialized skills in these areas, and these skills are in high demand among our competitors. The market for employees in our industry is extremely competitive, and competitors for talent, particularly engineering talent, increasingly attempt to hire, and to varying degrees have been successful in hiring, our employees or employment candidates, including by establishing or expanding local offices near our headquarters in San Diego, California. Further, the increased availability of remote working arrangements has expanded the pool of companies that can compete for our employees and employment candidates. A number of such competitors for talent are significantly larger than us and/or offer compensation in excess of what we offer or other benefits that we do not offer, including remote work policies that may be perceived as more favorable than ours.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
