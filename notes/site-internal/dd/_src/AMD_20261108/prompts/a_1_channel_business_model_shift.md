你是 stock-analyst v20 DD 的證據採集子 agent。標的：AMD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Advanced Micro Devices distribution channel disruption OR shift 2026
  - AMD Advanced Micro Devices business model transition subscription OR platform 2026
  - Semiconductors channel disintermediation D2C 2026
  - Advanced Micro Devices go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-04）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm｜as_of：2026-02-04
<<<
Client and Gaming Segment Client Business Client Market Our CPUs and APUs power PCs that are an integral part of how customers work, learn and play. The Client market encompasses the global personal computing ecosystem, including desktop and notebook PCs sold primarily through OEMs, distributors and select direct customers. Our products consist mainly of x86 CPUs and APUs marketed under the AMD Ryzen™ and AMD Ryzen™ AI brands for consumer, commercial and enthusiast segments. Our customers focus on a combination of performance, efficiency, reliability, and value that aligns with their specific use cases. We built a leadership roadmap across these areas and are continuing to further differentiate end user experiences by infusing AI across our portfolio.

Sales and Marketing We sell our products via a direct sales force, our OEMs (as described in detail below) and through independent distributors and sales representatives in both domestic and international markets. Our sales arrangements generally operate on the basis of product forecasts provided by the particular customer, but do not typically include any commitment or requirement for minimum product purchases. We use purchase orders and related documents, and contractual agreements as evidence of our sales arrangements. Our agreements typically contain standard terms and conditions covering matters such as payment terms, warranties and indemnities for issues specific to our products.

Customers Our Data Center Segment customers consist primarily of hyperscale data centers, original equipment manufacturers (OEMs), original design manufacturers (ODMs), system integrators and independent distributors in both domestic and international markets. ODMs provide design and/or manufacturing services to branded and unbranded private label resellers, OEMs and system builders.

Our Client and Gaming Segment customers consist primarily of PC OEMs, a network of independent distributors and, for chipset products, ODMs that manufacture motherboards. PC OEMs and independent distributors as well as add-in-board manufacturers (AIBs), independent game console and portable gaming devices manufacturers and contract manufacturers for AMD branded graphics cards.

Our Embedded Segment products are sold to customers in a very wide range of markets such as aerospace and defense, automotive, industrial, vision and healthcare, communications infrastructure, test and measurement, emulation and prototyping, audio, video and broadcasting and data center. For these products, we either sell directly to our customers or through a network of distributors and OEM partners. We are also developing a network of Value Added Resellers (VARs) and Integrated Solution Vendors (ISVs) for our Alveo products.

Original Equipment Manufacturers We focus on three types of OEM partners: multi-nationals, selected regional accounts and selected global and local system integrators, who target commercial and consumer end customers of all sizes. Large multi-nationals and regional accounts are the core of our OEM partners’ business; however, we are increasingly focused on the VAR channel, which resells OEM systems to the mid-market and the small and medium business (SMB) segments. Additionally, we have increased our focus on global system integrators, which resell OEM systems, coupled with their software and services solutions into Enterprise, High Performance Computing (HPC) and Cloud Service Provider customers. Our OEM customers include numerous foreign and domestic manufacturers of servers and workstations, desktops, notebooks, PC motherboards and game consoles.

Third-Party Distributors Our authorized channel distributors resell to sub-distributors, OEMs, ODMs and other customers. Typically, distributors handle a wide variety of products, and may include products from other manufacturers that compete with our products. Distributors typically maintain an inventory of our products. In most instances, our agreements with distributors protect their inventory of our products against price reductions and provide certain return rights with respect to any product that we have removed from our price book or are otherwise subject to discontinuation. In addition, some agreements with our distributors may contain standard stock rotation provisions permitting limited product returns.

Add-in-Board (AIB) Manufacturers and System Integrators We offer component-level graphics and chipset products to AIB manufacturers who in turn build and sell board-level products using our technology to system integrators (SIs), retailers and sub distributors. In most instances, our agreements with AIBs protect their inventory of our products against price reductions. We also sell directly to some SI customers. SIs typically sell from positions of regional or product-based strength in the market. They usually operate on short design cycles and can respond quickly with new technologies. SIs often use discrete graphics solutions as a means to differentiate their products and add value to their customers.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-04）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm｜as_of：2026-02-04
<<<
Our estimates of necessary adjustments for distributor price incentives and price protection on unsold products held by distributors are based on actual historical incentives provided to distributor customers and known future price movements based on our internal and external market data analysis.

We also provide limited product return rights to certain OEMs and to most distribution customers. These return rights are generally limited to a contractual percentage of the customer’s prior quarter shipments, although, from time to time we may approve additional product returns beyond the contractual arrangements based on the applicable facts and circumstances. In order to estimate adjustments to revenue to account for these returns, including product restocking rights provided to distributor and OEM customers, we utilize relevant, trended actual historical product return rate information gathered, adjusted for actual known information or events, as applicable.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
