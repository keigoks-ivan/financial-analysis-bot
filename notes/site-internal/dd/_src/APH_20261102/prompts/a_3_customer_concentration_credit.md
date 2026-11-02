你是 stock-analyst v20 DD 的證據採集子 agent。標的：APH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[customer_concentration_credit] 客戶集中度與客戶信用
Q: 前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？
  - APH Amphenol top customer revenue concentration 10-K 2026
  - credit rating OR balance sheet stress 2026
  - Amphenol customer concentration risk disclosure
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926013549/aph-20251231x10k.htm｜as_of：2026-02-11
<<<
​ Automotive - Amphenol is a leading supplier of advanced interconnect systems, sensors and antennas for a growing array of automotive applications. In addition, Amphenol has developed advanced technology solutions for hybrid and electric vehicles and is working with leading global customers to proliferate these advanced interconnect products into next-generation automobiles. Sales into the automotive market represented approximately 15% of the Company’s net sales in 2025, with sales into the following primary end applications: ​ ​ ​ ​ ● ​ ​antennas ​ ​ ​ ● ​ ​lighting ● ​ ​charging stations ​ ● ​ ​passenger connectivity ● ​ ​climate control ​ ● ​ ​power management ● ​ ​electric vehicles ​ ● ​ ​safety and security systems ● ​ ​engine management and control ​ ● ​ ​sensing systems ● ​ ​exhaust monitoring and cleaning ​ ● ​ ​telematics systems ● ​ ​hybrid vehicles ​ ● ​ ​transmission systems ● ​ ​infotainment and communications ​ ​ ​ ​ 5 Table of Contents Commercial Aerospace - Amphenol is a leading provider of high-performance interconnect systems and components to the commercial aerospace market. In addition to connector and interconnect assembly products, the Company also provides rigid and flexible printed circuits, specialty cable, high-technology cable management products as well as sensors. Our products are specifically designed to operate in the harsh environments of commercial aerospace, while also providing substantial weight reduction, simplified installation and/or minimal maintenance. Sales into the commercial aerospace market represented approximately 5% of the Company’s net sales in 2025, with sales into the following primary end applications: ​ ​ ​ ​ ● ​ ​aircraft and airframe power distribution ​ ​ ​ ● ​ ​in-flight entertainment ● ​ ​avionics ​ ● ​ ​in-flight internet connectivity

● ​ ​controls and instrumentation ​ ● ​ ​lighting and control systems ● ​ ​engines ​ ● ​ ​wire bundling and cable management ​ ​ ​ ​ ​ ​ ​ ​ Communications Networks - Amphenol is a leading global provider to the communications networks market and offers a wide product portfolio to support wireline and wireless service providers. The Company’s products include antennas, cables, connectors and interconnect systems that are used in current and next-generation wireline and wireless communications standards, including 5G networks. Sales into the communications networks market represented approximately 10% of the Company’s net sales in 2025, with sales into the following primary end applications: ​ ​ ​ ​ ​ ​ ● ​ ​antenna systems ​ ​ ​ ● ​ ​fiber management systems ● ​ ​base stations ​ ​ ​ ● ​ ​mobile switches ● ​ ​cable, satellite & telecommunications networks ​ ● ​ ​network switching equipment ● ​ ​customer premises equipment ​ ● ​ ​satellite interface devices ● ​ ​distributed antenna systems (DAS)

​ ​ ​ ● ​ ​agricultural equipment ​ ​ ​ ● ​ ​marine ● ​ ​alternative and traditional energy generation ​ ● ​ ​medical equipment ● ​ ​batteries and hybrid drive systems ​ ● ​ ​oil and gas ● ​ ​entertainment ​ ● ​ ​power distribution ● ​ ​factory and machine tool automation ​ ● ​ ​public safety ● ​ ​heavy equipment ​ ● ​ ​rail mass transit ● ​ ​instrumentation ​ ● ​ ​semiconductor manufacturing equipment ● ​ ​internet of things ​ ● ​ ​smart manufacturing ● ​ ​LED lighting ​ ● ​ ​transportation 6 Table of Contents ​ Information Technology and Data Communications - Amphenol is a global provider of interconnect solutions to designers, manufacturers and operators of internet and artificial intelligence (“AI”)-enabling systems. With our industry-leading high-speed, power and active and passive fiber optic interconnect technologies, together with superior simulation and testing capability and cost effectiveness, Amphenol is a market leader in interconnect development for the information technology and data communications (“IT datacom”) market. Our products enable a broad array of IT datacom systems and applications, including a growing range of systems to power AI and machine learning. Whether industry standard or application-specific designs are required, Amphenol provides customers with products that enable performance at the leading edge of next-generation, high-speed, power and fiber optic technologies.…

​ The Company’s products are sold to thousands of original equipment manufacturers (or OEMs) in numerous countries throughout the world. The Company’s products are also sold to electronic manufacturing services (EMS) companies, to original design manufacturers (or ODMs) and to service providers, including telecommunications network service providers and web service providers. No single customer accounted for 10% or more of the Company’s net sales during the years ended December 31, 2025, 2024 and 2023.

​ The Company sells its products through its own global sales force, independent representatives and a global network of electronics distributors. The Company’s sales to distributors represented approximately 19% and 18% of the Company’s net sales in 2025 and 2024, respectively. In addition to product design teams and collaborative initiatives 7 Table of Contents with customers, the Company uses key account managers to manage certain customer relationships on a global basis so that it can bring to bear its total resources to meet the worldwide needs of its multinational customers.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 8. Financial Statements｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926013549/aph-20251231x10k.htm｜as_of：2026-02-11
<<<
Interconnect and Sensor Systems ​ ​ 2,636.5 ​ ​ 2,190.2 ​ ​ 2,028.6 ​ ​ ​ 11,433.9 ​ ​ 6,550.5 ​ ​ 5,265.3 ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ Total Net sales ​ $ 23,094.7 ​ $ 15,222.7 ​ $ 12,554.7 ​ 99 Table of Contents Net sales by geographic area are based on the customer location to which the product is shipped. No single customer accounted for 10% or more of the Company’s net sales during the years ended December 31, 2025, 2024 and 2023. As the Company is not organized by product or group of products, it is impracticable to disclose net sales by product or group of products. For further discussion related to the Company’s policies surrounding revenue recognition, refer to Note 1 herein.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APH_20261102/parts/axes_3.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
