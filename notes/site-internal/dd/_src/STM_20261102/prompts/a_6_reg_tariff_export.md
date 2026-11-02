你是 stock-analyst v20 DD 的證據採集子 agent。標的：STM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - STM STMicroelectronics tariff section 232 2026
  - STMicroelectronics export control OR entity list Semiconductors 2026
  - STM STMicroelectronics China tariff OR trade restriction 2026
  - Semiconductors tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
•We, and the semiconductor industry, operate at a global scale. Our global asset base and market footprint expose us to negative impacts of tariffs and /or trade barriers that may inhibit our ability to place products across regions.

Geopolitical conflicts have additionally resulted in certain countries imposing sanctions. Further consequences of such conflicts could include a risk of further sanctions, embargoes, regional instability, geopolitical shifts and adverse effects on macro-economic conditions, currency exchange rates and financial markets. This could lead to disruption to international commerce and the global economy, and could have a negative effect on our ability to sell to, ship products to, collect payments from, and support customers in certain regions based on trade restrictions, embargoes, logistics restrictions and export control law restrictions.

We, and the semiconductor industry, operate at a global scale. Our global asset base and market footprint expose us to negative impacts of tariffs and /or trade barriers that may inhibit our ability to place products across regions.

Our global asset base and diversified market footprint expose us to adverse impacts from tariffs, trade restrictions, and protectionist policies. These barriers can limit our ability to efficiently place products across key regions, disrupt established supply chains, increase input costs, and reduce market access particularly in jurisdictions where we operate manufacturing hubs or export our products. These risks may be particularly acute in the semiconductor industry, where cyclical demand patterns and rapid technological changes can amplify economic headwinds.

The institution of trade tariffs globally, including the institution of any sector-specific tariffs, as well as the threat thereof, could negatively impact economic conditions, which could have negative repercussions for our business. In particular, trade protection and national security policies of the U.S. and Chinese governments, including tariffs, trade restrictions, export restrictions and the placing of companies on restricted entity lists, have and may continue to limit or prevent us from transacting business with certain of our Chinese customers or suppliers; limit, prevent or discourage certain of our Chinese customers or suppliers from transacting business with us; or make it more expensive to do so. If disputes were to arise under any of our agreements with other parties conducting business in China, the resolution of such dispute may be subject to the exercise of discretion by the Chinese government, or agencies of the Chinese government, which may have a material adverse effect on our business. In addition, we could face increased competition as a result of China's programs to promote a domestic semiconductor industry and supply chains (such as its 5-year plans, the China Standards 2035 campaign and related large scale national and local public funding schemes).…

In addition, we may be subject to the imposition of sector-specific tariffs, such as the 100% tariff on imported, foreign-produced semi-conductor chips threatened by the current U.S. administration, or China’s related export controls. Any or all of these measures or restrictions may limit our ability to sell products in certain markets or source components from specific suppliers, potentially disrupting our supply chain and manufacturing capabilities and limiting our ability to service our customer base in a cost-effective manner.

Further, throughout 2025 the current U.S. administration initiated numerous investigations into products and industries under section 232 of the Trade Expansion Act of 1962. For example, in April 2025, the Department of Commerce launched an investigation into the national security impacts of imported semiconductors and semiconductor manufacturing equipment. This investigation may result in additional tariffs and trade restrictions that may adversely impact the semiconductor industry and our business. Similar investigations on other industries or products, including automotive, copper, steel, aluminium, critical minerals and aircraft, may also adversely impact the semiconductor industry and our business.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
56 Other claims. We are subject to the possibility of loss contingencies arising in the ordinary course of business. These include but are not limited to: product liability claims and/or warranty costs on our products, contractual disputes, indemnification claims, employee grievances, tax claims beyond assessed uncertain tax positions as well as claims for environmental damages. We are also exposed to numerous legal risks which until now have not resulted in legal disputes and proceedings. These include risks related to product recalls, environment, shareholder rights, tariffs and export control regulations, anti-trust, anti-corruption, competition as well as other compliance regulations. We may also face claims in the event of breaches of law committed by individual employees or third parties. In determining loss contingencies, we consider the likelihood of a loss of an asset or the occurrence of a liability, as well as our ability to reasonably estimate the amount of such loss or liability. An estimated loss is recorded when we believe that it is probable that a liability has been incurred and the amount of the loss can be reasonably estimated. We regularly re-evaluate any potential losses and claims and determine whether our provisions need to be adjusted based on the current information available to us.…

This outlook is based on an assumed effective currency exchange rate of approximately $1.16 = €1.00 for the 2026 first quarter and includes the impact of existing hedging contracts. The first quarter will close on March 28, 2026. This business outlook does not include any impact from potential further changes to global trade tariffs compared to the current situation, as well as any impact related to the acquisition of NXP's MEMS business, which was completed on February 2, 2026.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
