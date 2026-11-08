你是 stock-analyst v20 DD 的證據採集子 agent。標的：HIMX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_second_source] 客戶 second-source 與 in-house
Q: 最大客戶是否正在導入第二供應商，或將此環節自製（in-house）？
  - HIMX Himax Technologies largest customer second-source OR in-house 2026
  - custom chip OR component second source agreement 2026
  - Himax Technologies single-source risk customer diversify supplier
  - in-house design OR insourcing Semiconductors 2026
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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
In order to reduce costs, Panel Manufacturers generally seek to have display drivers with higher channel counts and new panel designs to reduce the number of display drivers required for each panel. We have been developing such innovative and cost-effective display driver solutions in order to grow our market share, attract additional customers, increase our average selling prices and capture new design wins. However, we cannot assure you that we will successfully achieve these goals. If we fail to do so and the number of display drivers typically required per panel decreases thereby reducing our unit shipments, our revenues may decline. Panel Manufacturers have developed several panel designs to reduce the usage of display drivers, including gate in panel, or GIP, amorphous silicon gate, or ASG, or simply gateless designs, which integrate the gate driver function onto the glass and eliminate the need for gate drivers, as well as dual gate and triple gate panel designs, which would largely reduce the usage of source drivers. If such designs or technologies become widely adopted, demand for our display drivers may decrease significantly, which would adversely and materially affect our results of operations.…

Certain of our competitors have established or may establish strategic or strong relationships with Panel Manufacturers that are also our existing or potential customers. Marketing our display drivers to such Panel Manufacturers that have established relationships with our competitors may be difficult. Moreover, several Panel Manufacturers have in-house design capabilities and therefore may not need to source semiconductor products from us. If our customers successfully develop in-house capabilities to design and develop semiconductors that can substitute for our products, they would likely reduce or stop purchasing our products. To sell new products, we will likely need to target new market segments and new customers with whom we do not have current relationships, which may require different strategies and may present difficulties that we have not encountered before. Failure to broaden our customer base and attract new customers may limit our growth prospects.

Access to third-party tape, assembly and testing capacity is critical to our business because we do not have in-house tape, assembly and testing capabilities for commercial production and instead rely on third-party service providers. Access to these services is especially important to our business because display drivers require specialized tape, assembly and testing services. A limited number of third-party tape, assembly and testing houses tape, assemble and test substantially all of our current products. Therefore, suppliers could be in a better position to bargain for higher prices, longer contract terms, higher deposit and/or higher contract breach penalties for their services and products, which could result in an increase in our average unit cost and/or penalty expenses. If the primary tape, assembly and testing service providers that we rely upon are not able to meet our requirements in price, quality, and service, or if our business relationships with these service providers were adversely affected, we would not be able to obtain the required capacity and would have to seek alternative providers, which may not be available on commercially reasonable terms, or at all. As a result, we do not directly control our product delivery schedules, tape, assembly and testing costs, and quality assurance and control.…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
22 Table of Contents Supply Chain Management The manufacturing of display drivers is complex and requires several manufacturing stages such as wafer fabrication, gold bumping, and assembly and testing, and the availability of materials such as the processed tape used in TAB packaging. We refer to these manufacturing stages and material requirements collectively as the “supply chain”. Panel manufacturers typically operate at high levels of capacity utilization and require a reliable supply of display drivers. A shortage of display drivers, or a disruption to this supply, may disrupt panel manufacturers’ operations. As a result, a company’s ability to deliver its products on a timely basis at the quality and quantity required is critical to satisfying its existing customers and winning new ones. Such supply chain management is particularly crucial to fabless display driver companies that do not have their own in-house manufacturing capacity. In the case of display drivers, supply chain management is further complicated by the high-voltage CMOS process technology and the special assembly and testing requirements that are not standard in the semiconductor industry. Access to this capacity also depends in part on display driver companies having received assurances of demand for their products since semiconductor manufacturing service providers require credible demand forecasts before allocating capacity among customers and investing to expand their capacity to support growth.

ASIC One of the critical elements of our 3D sensing total solution is an ASIC for 3D depth map generation. We are able to develop the ASIC thanks to our unique in-house capability in developing video ASICs for customers. Equipped with the ASIC, our 3D sensing total solution can substantially reduce the power consumed while processing 3D sensing, enhance personal data security, accelerate the 3D depth map generation, and provide superior depth data output that matches with our optical component. We consider this unique capability as our competitive advantage. It has been and will continue to be one of our key drivers in the success of our 3D sensing total solution.

Concurrently, progress also been made in the WiseEye Module business. Himax WiseEye modules incorporate Himax's low-power CMOS image sensors, AI processor, and versatile AI models from either in-house or third-party partners. Meticulously engineered in compact form factors with high integration and plug-and-play capability, the modules feature user-programmable, pre-loaded AI models that enable seamless system integration, lowering development barriers and reducing overall AI deployment costs. This initiative is particularly well suited for early-stage market adoption and rapid customer engagement. WiseEye modules are seeing expanding adoption across diverse applications, including smart home appliances and various surveillance systems. Notably, our PalmVein module has built a strong design-in pipeline across multiple industries, spanning smart access control, workforce management, smart door locks, and computer monitors.

3D Technologies. Several technologies in Himax are integrated together to form our 3D solution. First, wafer level nanoimprinted technology is used to design and manufacture DOE and Waveguide. Then, our in-house capability on semiconductors enables us to design IC that particularly matches our optical component. Our expertise in precision assembly in optics also helps us to provide a more complete solution to our customers.

Customers Our customers for display drivers are primarily Panel Manufacturers and mobile device module manufacturers, who in turn design and market their products to manufacturers of end-use products such as notebook computers, desktop monitors, televisions, smartphone, tablet, automotive and consumer electronics products. We may sell our products through agents or distributors for certain products or in certain regions. As of December 31, 2025, we sold our products to around 300 customers. Our ten largest customers together accounted for approximately 74.1%, 73.6% and 71.3% of our revenues in 2023, 2024 and 2025, respectively. In 2023, 2024 and 2025, our two largest customers accounted for 10% or more of our net revenue: customer A and its affiliates accounted for 28.7%, 26.4% and 24.0% of our revenues, respectively; and customer C accounted for 11.0%, 8.3% and 7.8%, respectively.

We operate a fab under Himax Display primarily for performing manufacturing processes for our LCoS microdisplays. Moreover, we have established an in-house WLO facility under Himax Taiwan for the key process of our wafer level optics products, which started small-scale shipments from December 2009 and commenced mass shipment to anchor customer from 2017 onwards. We began construction of our new building, Fab 2, in March 2017, located nearby the current headquarters to house additional WLO capacity, the new active alignment equipment needed for our 3D sensing business and to provide extra office space. The construction of Fab 2 was completed in the first half of 2018.

For WiseEye ultralow power AI sensing, the main competition is Qualcomm with its “Glance” device. Few additional small size companies develop AI base edge devises, such as Lattice, Eta Computing, Nuvoton, Altek, etc. However, Himax is the only vendor who can offer a truly in-house vertically integrated solution comprise with all three building blocks required by customers: CMOS sensor, purposely designed MCU and the AI algorithm.

We have established an in-house WLO facility under Himax Taiwan for the key process of our products. The facility occupies 1,171 square meters of floor space in a building leased from Innolux, which was already produced and shipped over 50 million optics to Tier-1 customer since 2010. However, the building lease was terminated early at the end of January 2024, and we relocated the WLO facility to our Fab 2. We have also expanded certain facilities for LCoS and WLO products to accommodate new customers and new applications located at our headquarters in Tainan, Taiwan. To build up test program development, engineering testing, debugging capability and manufacturing support, we have established under Himax Taiwan an in-house CP test facility from 2022.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/parts/axes_2.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
