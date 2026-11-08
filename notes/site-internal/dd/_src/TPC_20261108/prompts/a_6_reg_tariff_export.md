你是 stock-analyst v20 DD 的證據採集子 agent。標的：TPC。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - TPC Tutor Perini tariff section 232 2026
  - Tutor Perini export control OR entity list Engineering & Construction 2026
  - TPC Tutor Perini China tariff OR trade restriction 2026
  - Engineering & Construction tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm｜as_of：2026-02-26
<<<
Economic factors, such as inflation, tariffs, the timing of new awards, or the pace of project execution, have resulted and may continue to result in losses or lower than anticipated profit.

Economic factors, including inflation and tariffs, have also previously subjected us, and could in the future subject us, to higher costs, which we may not be able to fully recover in future projects that we are bidding, and may also decrease profit on our existing contracts, in particular with respect to our fixed price, unit price and guaranteed maximum price contracts. Changes in laws, policies or regulations, including tariffs and taxes, have previously impacted, and in the future could impact, the prices for materials or equipment. Further, our results of operations have historically fluctuated, and may continue to fluctuate, quarterly and annually depending on when new awards occur and the commencement and progress of work on projects already awarded.

For the year ended December 31, 2025, we derived $489.7 million, or 9%, of revenue from our work on projects in international locations, including U.S. territories. Our international operations expose us to risks inherent in doing business in regions outside the United States, including political risks; risks of loss due to acts of war; unstable economic, financial and market conditions; potential incompatibility with foreign subcontractors and vendors; foreign currency controls and fluctuations; trade restrictions; economic and trade sanctions; logistical challenges; variations in taxes; and changes in labor conditions, labor strikes and difficulties in staffing and managing international operations. Failure to successfully manage risks associated with our international operations could result in higher operating costs than anticipated or could delay or limit our ability to generate revenue and income from construction operations in key international markets.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/77543/000007754326000028/tpc-20251231.htm｜as_of：2026-02-26
<<<
With respect to potential concerns regarding the U.S. government’s scrutiny and curtailment of federal funding for certain projects, as well as concerns about recent federal government shutdowns and varying new tariff policies that have been and may continue to be implemented, the Company does not currently anticipate any significant impacts to its business related to these factors. Most of the Company’s major projects are funded at the state or local level, or with some combination of federal, state and local funding. For projects that are wholly or partially funded with federal dollars, the funding for those projects has already been committed and/or those projects are strategically important to the United States. Despite this, there have recently been, and there may in the future be, occasions where even previously authorized and committed funding is withheld by the government, which could delay the progress of certain projects or the awards of new projects. The Company does not anticipate any material adverse impacts to its financial results as the result of such temporary project delays.

Specifically related to potential tariff impacts, the Company utilizes a pre-award and post-award strategy. As part of its pre-award strategy, the Company’s detailed estimating process includes consideration of anticipated cost increases over the performance period of the contract, as well as additional contingencies to address other potential incremental costs related to unforeseen risks. Prior to its bid or proposal submission, the Company also works to negotiate favorable contract provisions that provide entitlement for certain compensable events, which may include price escalation and allowances. Once the project is awarded, the Company’s strategy shifts to entering into purchase orders or “buy-outs” of materials, such as steel and concrete, as well as large pieces of equipment at the onset of projects, which mitigate the risk of future equipment and commodity price increases by passing that risk to vendors. Also at that time, the Company enters into fixed-price contracts with its key project subcontractors whereby the risk of unforeseen escalation is transferred to the subcontractors. The Company benefits from its long-term relationships with key suppliers, vendors and subcontractors, which minimize supply chain disruptions that could arise as a result of tariffs. While the Company believes this strategy appropriately mitigates the current risk of potential tariff impacts, there could be other unforeseen future developments.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
