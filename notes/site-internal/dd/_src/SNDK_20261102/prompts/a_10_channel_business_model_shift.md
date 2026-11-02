你是 stock-analyst v20 DD 的證據採集子 agent。標的：SNDK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Sandisk distribution channel disruption OR shift 2026
  - SNDK Sandisk business model transition subscription OR platform 2026
  - Computer Hardware channel disintermediation D2C 2026
  - Sandisk go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
The Datacenter end market is comprised primarily of products for datacenters, cloud service providers, and private cloud customers. Through the Edge end market, we provide our original equipment manufacturer (“OEM”) and channel customers a broad array of high-performance flash solutions across personal computer, mobile, gaming, automotive, physical AI, at-home entertainment, and industrial spaces. The Consumer end market is highlighted by our broad range of retail and other end-user products, which capitalize on the strength of our product brand recognition and vast presence around the world.

We serve the Consumer end market with a portfolio of SSDs and removable flash products, including cards and universal serial bus flash drives, through our retail and channel routes to market. We offer client portable SSDs with a range of capacities and performance characteristics to address a broad spectrum of the client storage market. Our removable cards are designed primarily for use in consumer devices, such as mobile phones, tablets, imaging systems, gaming devices, cameras and smart video systems. Our universal serial bus flash drives are used in the computing and consumer markets and are designed for high performance and reliability.

Sales and Distribution We sell our products to computer manufacturers and OEMs, cloud service providers, resellers, distributors and retailers throughout the world. We maintain sales offices in selected parts of the world including the major geographies of the Americas, Asia Pacific, Europe and the Middle East. Our international sales, which include sales to foreign subsidiaries of U.S. companies but do not include sales to U.S. subsidiaries of foreign companies, represented 82%, 80% and 86% of our net revenue for 2026, 2025 and 2024, respectively. Sales to international customers are subject to certain risks not normally encountered in domestic operations, including exposure to tariffs and various trade and other regulations. For a discussion of associated risks, see Part I, Item 1A., Risk Factors of this Annual Report on Form 10-K.

9 Table of Contents We perform our marketing and advertising functions both internally and through outside firms utilizing both consumer media and trade publications targeting various reseller and end-user markets. We also maintain customer relationships through direct communication and by providing information and support through our website. In accordance with standard storage industry practice, we provide distributors and retailers with limited price protection and programs under which we reimburse certain marketing expenditures. We also provide distributors, resellers and OEMs with other sales incentive programs.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-17）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/2023554/000162828026057406/sndk-20260703.htm｜as_of：2026-08-17
<<<
The Datacenter end market is comprised primarily of products for datacenters, cloud service providers, and private cloud customers. Through the Edge end market, we provide our original equipment manufacturer (“OEM”) and channel customers a broad array of high-performance flash solutions across personal computer, mobile, gaming, automotive, physical AI, at-home entertainment, and industrial spaces. The Consumer end market is highlighted by our broad range of retail and other end-user products, which capitalize on the strength of our product brand recognition and vast presence around the world.

On February 21, 2025, WDC executed the spin-off of the Company through WDC’s pro rata distribution of 116,035,464, or 80.1%, of the Company’s outstanding shares of common stock to holders of WDC’s common stock. Each WDC stockholder received one-third (1/3) of one share of the Company’s common stock for each share of WDC’s common stock held by such WDC stockholder as of February 12, 2025, the record date of the distribution. Upon completion of the separation, WDC owned 28,827,787, or 19.9%, of the outstanding shares of the Company’s common stock. Following the distribution, the Company became an independent publicly listed company, and on February 24, 2025, the Company began trading as an independent publicly traded company under the stock symbol “SNDK” on Nasdaq.

Revenue by end market: Datacenter $ 5,153 $ 960 $ 325 Edge 12,160 4,127 4,069 Consumer 2,935 2,268 2,269 Total revenue $ 20,248 $ 7,355 $ 6,663 Revenue by geography: Asia $ 14,241 $ 4,457 $ 4,510 Americas 4,275 1,618 1,095 Europe, Middle East and Africa 1,732 1,280 1,058 Total revenue $ 20,248 $ 7,355 $ 6,663 46 Table of Contents Our broad portfolio of technology and products addresses multiple end markets. Datacenter represents a large and growing end market comprised primarily of products for public or private cloud environments and enterprise customers. Through the Edge end market, we provide our OEM and channel customers a broad array of high-performance flash solutions across personal computer, mobile, gaming, automotive, physical AI, at-home entertainment, and industrial spaces. The Consumer end market is highlighted by our broad range of retail and other end-user products, which capitalize on the strength of our product brand recognition and vast presence around the world.

Revenue We provide distributors and retailers (collectively referred to as “resellers”) with limited price protection for inventories held by resellers at the time of published list price reductions. We also provide resellers and OEMs with other sales incentive programs. We record estimates of variable consideration related to these items as a reduction of revenue at the time of revenue recognition. We use judgment in our assessment of variable consideration in contracts to be included in the transaction price. We use the expected value method to arrive at the amount of variable consideration. We constrain variable consideration until the likelihood of a significant revenue reversal is not probable and believe that the expected value method is the appropriate estimate of the amount of variable consideration based on the fact that we have a large number of contracts with similar characteristics.

For sales to OEMs, the methodology for estimating variable consideration is based on the amount of consideration expected to be earned based on the OEMs’ volume of purchases under agreed-upon sales incentive programs. For sales to resellers, the methodology for estimating variable consideration is based on the amount of consideration expected to be earned from sell-through activity under agreed-upon sales incentive programs. The amount of consideration expected to be earned by the reseller is based on historical pricing information, current pricing trends and channel inventory levels. Estimating the impact of these factors requires judgment and differences between estimated and actual amounts of variable consideration can occur.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
