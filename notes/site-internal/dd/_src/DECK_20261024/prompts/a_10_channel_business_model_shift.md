你是 stock-analyst v20 DD 的證據採集子 agent。標的：DECK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - distribution channel disruption OR shift 2026
  - DECK business model transition subscription OR platform 2026
  - channel disintermediation D2C 2026
  - go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-22）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm｜as_of：2026-05-22
<<<
Our brands compete across the fashion and casual lifestyle, performance, running, and outdoor markets. We believe our products are distinctive and appeal to a broad demographic. Our brands sell our products through quality domestic and international retailers and international distributors in our wholesale channel, and directly to global consumers through our Direct-to-Consumer (DTC) channel, which is comprised of an e‑commerce and retail store presence. We seek to differentiate our brands and products by offering diverse lines that emphasize fashion, performance, authenticity, functionality, quality, and comfort, and products tailored to a variety of activities, seasons, and demographic groups. Independent third-party contractors manufacture all of our products (independent manufacturers).

Channel Distribution We operate omnichannel global marketplaces for our brands where consumers can shop and experience our brands seamlessly across both channels outlined below.

Wholesale. Our wholesale channel sells products to a network of third-party retailers, including partner retailers, and distributors. This approach enables us to expand market reach and leverage the scale and operational capabilities of our wholesale partners to serve a broad base of end consumers.

We sell our HOKA brand products primarily through full-service specialty retailers, outdoor and sporting goods retailers, select online retailers, fashion lifestyle retailers, sports style partners, and higher-end department stores.

We continue to expand our HOKA brand wholesale distribution globally, including through additional mono-branded locations operated by partner retailers.

We sell our UGG brand products primarily through fashion lifestyle retailers, higher-end department stores, streetwear and sports style partners, online retailers and partner retailers. As the retail marketplace continues to evolve to reflect changing consumer preferences, we continually review and evaluate our UGG wholesale distribution and product segmentation approach.

We sell our Teva brand products primarily through outdoor and sporting goods retailers, fashion lifestyle retailers, large national retail chains, higher-end department stores, and online retailers.

Direct-to-Consumer. Our DTC channel is comprised of our Company-owned e-commerce websites and retail stores where products are sold at retail prices. Our e-commerce websites and retail stores are intertwined and interdependent in an omnichannel marketplace, which engenders brand loyalty while increasing product sales and improving our inventory productivity. In addition, we believe some of our consumers interact with both before making purchasing decisions in store and online. For example, consumers may feel or try on products in our retail stores and then place an order online later, or they may initially research products online and then make a purchase in store.

E-Commerce Websites. Our global e-commerce websites provide us with an opportunity to directly engage and connect with our consumers and communicate a consistent message that promotes awareness of our brands’ promises and key initiatives, offers targeted information to specific consumer demographics, and drives consumers to our retail stores. Our e‑commerce websites provide consumers with access to the broadest selection and assortment of our products. As of March 31, 2026, we operate Company-owned e-commerce websites in 54 different countries.

Retail Stores. Retail stores enable us to expose consumers to a curated selection of products and directly influence our consumers’ experience with our brands. We continue to open mono-branded retail stores in key markets to further grow the UGG brand and HOKA brand presence and appeal to a broader consumer base, while also prioritizing the revitalization and recalibration of our existing retail store fleet to enhance overall brand impact and consumer experience. As of March 31, 2026, we have a total of 203 global Company-owned retail stores (including 141 UGG brand retail stores and 62 HOKA brand retail stores), which include 105 concept stores and 98 outlet stores.

Geographic Distribution US Distribution. In our wholesale channel, we sell our products in the US through sales representatives, organized by brand and either geography or account type, as each brand generally has certain strategic customers that expect a dedicated sales team with specialized knowledge of the brand’s product offerings. In addition to our wholesale Table of Contents 6 channel, we sell products directly to consumers through our DTC channel and fulfill online orders through our warehouses and DCs, and retail stores. We currently distribute products sold in the US through our DCs in Moreno Valley, California, and Mooresville, Indiana. We also distribute products to our wholesale channel customers through a DC bypass program.

International Distribution. Collectively, our brands are sold internationally, including in Canada, Europe, Asia, and Latin America. We sell our products internationally in our wholesale channel through wholly owned subsidiaries and independent distributors, some of which operate partner retail stores. In addition, in certain countries we sell products through our DTC channel. For our wholesale and DTC channels, we distribute our products through a number of warehouses and DCs managed by 3PLs in certain international locations. We are currently transitioning one of our international 3PLs to a new partner.

We manage our inventory levels by considering existing orders, as well as forecasted sales and budgets by brand for both the wholesale and DTC channels, taking into account customer delivery requirements. Our systems and processes are designed to improve our product planning and forecasting, inventory control and supply chain management capabilities, including our Company-owned e-commerce websites. In addition, added discipline around SKU productivity, product purchasing decisions, lead time reduction, and selling excess inventory through our liquidation channels, are key areas of focus that have enhanced inventory performance, including higher inventory turnover, and partially mitigated product cost increases.

Our general practice, consistent with industry standards, is to offer customers in our wholesale channel the right to return defective or improperly shipped merchandise, and to accept returns from our consumers in the DTC channel between 30 to 90 days from the point of sale for cash or credit.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-22）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm｜as_of：2026-05-22
<<<
Our brands compete across the fashion and casual lifestyle, performance, running, and outdoor markets. We believe our products are distinctive and appeal to a broad demographic. Our brands sell our products through quality domestic and international retailers and international distributors in our wholesale channel, and directly to global consumers through our DTC channel, which is comprised of an e‑commerce and retail store presence. We seek to differentiate our brands and products by offering diverse lines that emphasize fashion, performance, authenticity, functionality, quality, and comfort, and products tailored to a variety of activities, seasons, and demographic groups. Independent third-party contractors manufacture all of our products.

▪Other brands net sales decreased 33.9% to $146,208. ◦Channel ▪Wholesale channel net sales increased 12.3% to $3,208,107.

•Our long-term strategy is to grow our DTC channel to represent a larger portion of our total net sales by differentiating the consumer experience relative to the wholesale channel and driving consumer acquisition and retention. We are investing in e-commerce platform upgrades, data analytics, consumer experience initiatives, and selective global retail store expansion. We expect growth in our DTC channel’s net sales to continue to positively impact our gross margin; however, as we also seek to expand distribution with wholesale partners to drive brand awareness and Table of Contents 34 market share, our wholesale channel may represent a larger portion of our net sales in certain periods, which could pressure gross margin in those periods.

•We continue to take actions to reposition the Teva brand, including refocusing certain wholesale channel distribution toward outdoor and premium retail partners and emphasizing brand messaging around its outdoor-adventure heritage. Our efforts to reposition the Teva brand and our future results of operations remain uncertain. In particular, macroeconomic pressure on value‑oriented domestic wholesale consumers may continue to adversely affect Teva brand performance.

Net Sales. Net sales by brand, channel, and geography were as follows: Years Ended March 31, 2026 2025 Change Amount Amount Amount % Net sales by brand HOKA brand Wholesale $1,651,794 $1,397,776 $254,018 18.2% Direct-to-Consumer 935,536 835,314 100,222 12.0 Total 2,587,330 2,233,090 354,240 15.9 UGG brand Wholesale 1,444,686 1,282,319 162,367 12.7 Direct-to-Consumer 1,294,072 1,249,032 45,040 3.6 Total 2,738,758 2,531,351 207,407 8.2 Table of Contents 37 Years Ended March 31, 2026 2025 Change Amount Amount Amount % Other brands Wholesale 111,627 175,770 (64,143)

(36.5) Direct-to-Consumer 34,581 45,401 (10,820) (23.8) Total 146,208 221,171 (74,963) (33.9) Total (1) $5,472,296 $4,985,612 $486,684 9.8% Net sales by channel Total Wholesale $3,208,107 $2,855,865 $352,242 12.3% Total Direct-to-Consumer 2,264,189 2,129,747 134,442 6.3 Total (1)

•Net sales of the UGG brand increased due to higher global net sales growth across both wholesale and DTC channels. Growth was led by international sales, with increases in domestic sales for the wholesale channel and a slight increase in the DTC channel. This collective growth was as a result of increased global demand for key franchises and further adoption of year-round product offerings.

•Net sales of the Other brands decreased primarily due to lower domestic net sales in the wholesale channel driven by the phase out of standalone operations of the Koolaburra brand and the sale of the Sanuk brand in the prior period. The decrease was also due to lower global net sales for the Teva brand across both channels, primarily driven by lower sales in the value-oriented consumer segment of the wholesale channel as the Teva brand refocuses its wholesale distribution with outdoor and premium retailers.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
