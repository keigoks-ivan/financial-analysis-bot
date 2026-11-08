你是 stock-analyst v20 DD 的證據採集子 agent。標的：QCOM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - QUALCOMM product substitute technology threat 2026
  - Semiconductors alternative technology disruption 2026 2027
  - QCOM QUALCOMM technology obsolescence risk
  - Semiconductors next-generation technology roadmap 2026


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

Research and Development We compete in industries that are characterized by rapid technological change, evolving industry standards and frequent new product introductions, requiring a continuous effort to enhance existing products and technologies and to develop new 11 products and technologies. We have significant engineering resources, including engineers with substantial expertise in modem, advanced SoC (which includes specialized engines such as CPU, GPU and NPU to enable high-performance and low-power computing and other optimization techniques), AI, radio-frequency integrated circuit, RFFE, multimedia (camera, video, display and computer vision), sensor perception and drive policy, packaging, data center infrastructure and networking and a broad range of other technologies. We expect to continue to invest in research and development in a variety of ways in an effort to extend the demand for our products and technologies and to utilize that research and development in industries and applications from mobile handsets to automotive, IoT and data center, including continuing the development of new computing, AI, connectivity and multimedia technologies and other technologies (such as ADAS/AD and XR), developing alternative technologies for certain specialized applications, participating in the formulation of new wireless communication standards and technologies and assisting in deploying digital wireless communications networks around the world. We support Android, Windows, Linux and other client software environments in our chipsets.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-04）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm｜as_of：2026-11-04
<<<
•The semiconductor industry is subject to intense competition in an environment of rapid technological change. Our success depends in part on our ability to adapt to such change and compete effectively; and such change and competition could result in decreased demand for our products and technologies or declining average selling prices for our products or those of our customers or licensees.

The semiconductor industry is subject to intense competition in an environment of rapid technological change. Our success depends in part on our ability to adapt to such change and compete effectively; and such change and competition could result in decreased demand for our products and technologies or declining average selling prices for our products or those of our customers or licensees.

Climate change concerns and the potential resulting environmental impact may result in new environmental, health and safety laws and regulations that may affect us, our suppliers and our customers. Such laws or regulations could cause us to incur additional direct costs for compliance, including costs associated with changes to manufacturing processes or the procurement of raw materials used in manufacturing processes, as well as increased indirect costs resulting from our customers, suppliers or both incurring additional compliance costs that are passed on to us. These costs may adversely impact our results of operations and financial condition. In addition, climate change could cause certain natural disasters, such as drought, wildfires, storms, flooding or rising sea levels, to occur more frequently or with greater intensity, which could pose physical risks to our manufacturing facilities or our suppliers’ facilities, could disrupt the availability of water necessary for the operation of such facilities, and could increase or decrease temperatures resulting in increased operating costs and/or business disruption.

We have manufacturing facilities in Asia and Europe, and the primary warehouses where we store finished goods are located in Asia. If tsunamis, flooding, earthquakes, volcanic eruptions, drought or other natural disasters, effects of climate change, acts of war or other geopolitical conflicts were to damage, destroy or disrupt any of these facilities, it could disrupt our operations, cease or delay production and shipments of inventory and result in costly repairs, replacements or other costs and lost business. In addition, natural disasters, effects of climate change, acts of war or other geopolitical conflicts may result in disruptions in transportation, distribution channels and supply chains and significant increases in the prices of raw materials. Further, health crises, including epidemics or pandemics, and government and business responses thereto, could affect our manufacturing facilities, including by resulting in quarantines and/or closures, which could result in disruptions to and potential closures of our manufacturing operations. Our manufacturing operations could also be disrupted by cyber-attacks on our IT systems, as described in the Risk Factor titled “Our business and operations could suffer in the event of security breaches of our IT systems, or other misappropriation of our technology, intellectual property or other proprietary or confidential information.”

Our manufacturing operations depend on securing raw materials, equipment and other supplies in adequate quality and quantity in a timely manner from multiple suppliers, and in some cases, we rely on a limited number of suppliers, including in some cases sole suppliers, particularly in Asia. There may be cases where supplies of raw materials, equipment and other products are interrupted or limited by natural disaster, geopolitical conflict, accident or some other event affecting a supplier 24 or source of raw materials; supply is suspended due to quality or other issues; there is a shortage of supply due to a rapid increase in demand; and/or we or our suppliers are prohibited from utilizing certain raw materials, or products or components that incorporate such raw materials, due to government restrictions related to the countries from which such raw materials originate, and acceptable alternative suppliers, raw materials or raw materials sources are not available or not available in acceptable time frames or upon acceptable terms, among others, which could impact production and prevent us from supplying our products to our customers. If the supply-demand balance is disrupted, it may considerably increase costs of manufacturing due to increased prices we pay for raw materials.…

The successful operation of various functions within our business, as well as the protection of our intellectual property and other proprietary or confidential information, depend in part on the security and functionality of our IT systems. Third parties regularly attempt to gain unauthorized access to our IT systems, and many such attacks are increasingly more sophisticated. These attacks, which might be related to industrial, corporate or other espionage, criminal hackers or state-sponsored intrusions, include trying to covertly introduce malware to our computers and networks, including those in our manufacturing operations, exploiting vulnerabilities in hardware, software or other IT infrastructure and impersonating authorized users, among others. We are also subject to ransom-style cyber-attacks, which could expose our confidential or proprietary information, demand payment of money and/or impact our IT systems and cause widespread disruption to our business, including our manufacturing operations. Third parties that store and/or process our confidential information, or that provide products, software or services used in our IT infrastructure, are subject to similar attacks, which could also result in malware being introduced into our IT infrastructure, e.g., through the third parties’ software and/or software updates.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
