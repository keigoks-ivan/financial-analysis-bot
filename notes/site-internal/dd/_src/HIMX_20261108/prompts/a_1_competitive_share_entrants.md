你是 stock-analyst v20 DD 的證據採集子 agent。標的：HIMX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - HIMX Himax Technologies market share gaining OR losing 2026
  - Himax Technologies new entrant OR displace threat Semiconductors 2026
  - HIMX competitor design win 2026
  - Himax Technologies vs Semiconductors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
We depend on sales of display drivers used in TFT-LCD and OLED panels, and the limited potential for further growth in both the market size of display drivers and the market share of our display drivers or the absence of continued market acceptance of our display drivers could limit our growth in revenues or harm our business.

Technological innovation may reduce the number of display drivers typically required for each panel, thereby reducing the number of display drivers we are able to sell per panel. If such a reduction in demand is not offset by the general growth of the industry, our market share or average selling prices, or our revenues may decline.

In order to reduce costs, Panel Manufacturers generally seek to have display drivers with higher channel counts and new panel designs to reduce the number of display drivers required for each panel. We have been developing such innovative and cost-effective display driver solutions in order to grow our market share, attract additional customers, increase our average selling prices and capture new design wins. However, we cannot assure you that we will successfully achieve these goals. If we fail to do so and the number of display drivers typically required per panel decreases thereby reducing our unit shipments, our revenues may decline. Panel Manufacturers have developed several panel designs to reduce the usage of display drivers, including gate in panel, or GIP, amorphous silicon gate, or ASG, or simply gateless designs, which integrate the gate driver function onto the glass and eliminate the need for gate drivers, as well as dual gate and triple gate panel designs, which would largely reduce the usage of source drivers. If such designs or technologies become widely adopted, demand for our display drivers may decrease significantly, which would adversely and materially affect our results of operations.…

Increased competition in the semiconductor industry may result in pricing pressure, reduced profitability and loss of market share, any of which could seriously harm our revenues and results of operations. We continually face intense competition from fabless display driver companies and integrated device manufacturers. Also in recent years, policies adopted by Chinese mainland panel manufacturers to actively introduce domestic IC suppliers have posed significant challenges to our business and may continue to intensify competition in the markets in which we operate. In addition, some of our competitors have substantially greater financial and other resources to pursue engineering, manufacturing, marketing and distribution of their products. As a result, they may be able to respond more quickly to changing customer demands or devote greater resources to the development, promotion and sales of their products. Some of our competitors are affiliated with, or are subsidiaries of, our panel manufacturer customers. These relationships may also give our competitors significant advantages such as early access to product roadmaps and design-in priorities, which would allow them to respond more quickly to changing customer demands and achieve more design-wins than we can. We cannot assure you that we will be able to increase or maintain our revenues and market share or compete successfully against our competitors in the semiconductor industry.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
4.B. Business Overview We are a leading global fabless semiconductor solution provider dedicated to display imaging processing technologies. Our display driver ICs and timing controllers have been adopted at scale across multiple industries worldwide including TVs, PC monitors, laptops, mobile phones, tablets, automotive, ePaper devices, industrial displays, among others. As the global market share leader in automotive display technology, we offer innovative and comprehensive automotive IC solutions, including traditional driver ICs, advanced in-cell Touch and Display Driver Integration (TDDI), local dimming timing controllers (Local Dimming TCON), Large Touch and Display Driver Integration (LTDI) and OLED technologies. Our industry-leading WiseEye Ultralow Power AI Sensing technology which incorporates Himax proprietary ultralow power AI processor, always-on CMOS image sensor, and CNN-based AI algorithm has been widely deployed in consumer electronics and AIoT applications. Himax optics technologies, such as wafer level optics (WLO), LCoS microdisplays and 3D sensing solutions, are critical enablers of emerging AR/VR and other next-generation applications.

For automotive TCONs, Himax has a dominant market share and offers a comprehensive product offerings featuring local dimming functionality, image enhancement, HDR, OSD, de-warping, to meet customers’ various needs of automotive displays We also provide gaming TCON for the new FHD 1000Hz, QHD 480Hz and UHD 240Hz gaming monitor and notebook. For high-end gaming -oriented applications, we have developed eDP 8.1G TCON to increase bandwidth. We are also developing eDP1.5 for notebooks.

26 Table of Contents The automotive display drivers can support various display resolutions to meet the customized needs of automotive display, including GIP panel and non-GIP panel, a-Si TFT panel, IGZO panel and LTPS panel. Meanwhile, the automotive display drivers can support higher output driving voltage for higher contrast ratio and faster liquid crystal response in automotive display applications. The automotive Timing Controller can support Local Dimming function for the goal of higher contrast ratio and thermal reduction in automotive display applications. We launched the world’s first TDDI design for automotive displays technology which started shipping in 2019 with meaningful mass production shipment to industrial leading automotive panel house, Tier1 and car brands starting 2021. Himax is the market leader in automotive display driver business covering the entire spectrum of products and technologies, including the industry’s most comprehensive traditional DDIC product offerings as well as TDDI, local dimming TCON, LTDI and OLED. Our automotive TDDI is already broadly adopted across the board and continue to expand, with a market share well over half. To date, Himax also has cumulatively shipped well over 100 million units of automotive TDDI, underscoring the strong market adoption of our technologies.…

● CRC/Communication loss ● LED open & short protection ​ 36 Table of Contents CMOS Image Sensor Products The CMOS image sensor products are developed by our subsidiary, Himax Imaging. The products were designed firstly for camera-equipped mobile devices, such as mobile phones, tablets and notebook computers, with a focus on low light image and video quality. Although it seems relatively challenging for us to gain significant market share in conventional RGB camera, we do think there are various interesting and different applications in imaging. Based on the technologies and IP we developed, on top of legacy products for laptop and multimedia we have been supplying, our product lines have been expanded to cover three domains: ultralow power computer vision- Always-On Sensor (“AoS”), Near Infrared (“NIR”) sensor, and big pixel BSI sensors in automotive and surveillance. In 2019, we further prioritized our focus on ultralow power computer vision- Always-On Sensor (“AoS”) as the demand for battery-powered smart device with AI intelligent sensing is rapidly growing. Together with the technologies we already developed, such as Near Infrared (“NIR”) sensor, we can provide our customers the best integrated solutions for several specific domains. In May 2024, we announced a strategic investment in Obsidian Sensors, Inc. ("Obsidian"), a San Diego-based thermal imaging sensor solution manufacturer.…

Competition The market characteristics for our products are, in general, intensely competitive, characterized by continuous technological change, evolving industry standards, and declining average selling prices. We believe key factors that differentiate the competition in our industry include: ● customer relations; ● product performance; ● design customization; ● development time / product release; ● product integration; ● technical services; ● manufacturing costs; ● supply chain management; ● timely delivery; ● economies of scale; and ● broad product portfolio.

For In-cell TDDI, we compete with Novatek Microelectronics Cop., Synaptics Incorporated, FocalTech Systems Co., Ltd., ESWIN, Chipone, OmniVision and Ilitek Corp., etc.

For 3D sensing, Himax is one of the few companies that can provide the one-stop solution though there are more companies attempting to jump into the game. ams AG and Orbbec will be the main competitors we face in the worldwide.
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
Small and Medium-Sized Display Driver IC Sector Himax continues to lead the global automotive display driver IC market, holding approximately 40% market share in DDIC, well over half of market share in TDDI, and an even higher share in local dimming TCON. We offer a comprehensive portfolio spanning both mainstream LCD and emerging OLED technologies. With hundreds of design-wins secured across TDDI, DDIC, TCON, and our expanding OLED portfolio, along with a steady influx of new projects, most of which are scheduled for mass production in the coming quarters, our market leadership remains firmly established. Meanwhile, Himax continues to lead automotive display IC innovation by delivering advanced solutions across a broad spectrum of panel technologies, while addressing diverse design requirements and cost targets. For ultra-large touch displays, we introduced the industry’s first LTDI solution in 2023, which has since entered mass production in multiple vehicle models. Designed for pillar-to-pillar displays, our LTDI architecture supports multi-chip cascading to enable ultra-high resolution, fast data transmission, and precise touch performance across expansive panels. For smaller displays with form factor and budget constraints, we provide highly integrated single-chip solutions that combine TDDI and local dimming TCON. This approach is an attractive choice for customers, as it can significantly reduce system cost while improving overall power efficiency.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
