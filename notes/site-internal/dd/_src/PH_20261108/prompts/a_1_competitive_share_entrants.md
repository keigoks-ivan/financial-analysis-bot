你是 stock-analyst v20 DD 的證據採集子 agent。標的：PH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - PH Parker-Hannifin market share gaining OR losing 2026
  - Parker-Hannifin new entrant OR displace threat Specialty Industrial Machinery 2026
  - PH competitor design win 2026
  - Parker-Hannifin vs Specialty Industrial Machinery peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-21）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm｜as_of：2026-08-21
<<<
3 Table of Contents Competition Parker operates in highly competitive markets and industries. We offer our products over numerous, varied markets through our divisions operating in 44 countries. Our global scope means that we have hundreds of competitors across our various markets and product offerings. Our competitors include U.S. and non-U.S. companies. These competitors and the degree of competition vary widely by product lines, end markets, geographic scope and/or geographic locations. Although each of our segments has numerous competitors, given our market and product breadth, no single competitor competes with the Company with respect to all the products we manufacture and sell.

In the Diversified Industrial Segment, Parker competes based on product quality and innovation, customer experience, manufacturing and distribution capability, aftermarket support, and price competitiveness. We believe that we are one of the market leaders in most of the major markets for our most significant Diversified Industrial Segment products. We have comprehensive motion and control technologies allowing us to provide the broadest systems capabilities. While our primary global competitors include Bosch Rexroth AG, Copeland, Danaher Corporation, Danfoss A/S, Donaldson Company, Inc., Emerson/ASCO, Festo SE & Co., Freudenberg-NOK, Gates Corporation, IMI/Norgren, SMC Corporation, Swagelok Company, and Trelleborg AB, none of these businesses compete with every group or product in our Diversified Industrial Segment.

In the Aerospace Systems Segment, we have developed relationships with key customers based on our advanced technological and engineering capabilities, performance in quality, delivery, service, and price competitiveness. This has enabled us to obtain significant original equipment business on new aircraft programs for our systems and components, as well as the follow-on repair and replacement business for these programs. Further, the Aerospace Systems Segment utilizes design and manufacturing techniques as well as best cost region and supply chain management strategies to reduce cost. Although we believe that we are one of the market leaders in most of the major markets for our most significant Aerospace Systems Segment products, primary global competitors for these products include Crane Co., Eaton Corporation plc, Honeywell Aerospace Inc., Moog Inc., RTX Corporation, Safran S.A., Senior plc, Triumph Group, Inc., and Woodward, Inc.

Across our two segments, we believe that our broad-based portfolio of core technologies, which consist of hydraulics, pneumatics, electromechanical, filtration, fluid & gas handling, process control, engineered materials, and climate control, is a positive factor in our ability to compete effectively with both large and small competitors. We believe that the following factors also contribute to our ability to compete effectively: •Our business system, The Win Strategy •Technology powerhouse of interconnected solutions •Deep partnerships with our customers to develop innovative products •Application engineering expertise •Global distribution network •Decentralized operating structure Patents, Trademarks, Trade Names, Copyrights, Trade Secrets, Licenses We own a number of patents, trademarks, trade names, copyrights, trade secrets and licenses related to our products. We also have exclusive and non-exclusive rights to use patents, trademarks, trade names, copyrights and trade secrets owned by others. In addition, patent and trademark applications are pending, although there can be no assurance that further patents and trademarks will be issued. We do not depend on any single patent, trademark, copyright, trade secret or license or group of patents, trademarks, copyrights, trade secrets or licenses to any material extent.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-21）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm｜as_of：2026-08-21
<<<
We cannot predict changes in worldwide or regional economic conditions and government policies, as such conditions are highly volatile and beyond our control. In addition, our responses to mitigate the impact of these conditions, such as potential price increases, could negatively impact our market share or relationships with distributors or customers. If these conditions deteriorate or remain at depressed levels for extended periods, however, our business, results of operations and financial condition could be materially adversely affected.

Our operations are subject to competition from a wide variety of global, regional and local competitors, which could adversely affect our results of operations by creating downward pricing pressure and/or a decline in our margins or market shares. To compete successfully, we must excel in terms of product quality and innovation, technological and engineering capability, manufacturing and distribution capability, delivery, price competitiveness, and customer experience.

We depend on the skills, institutional knowledge, working relationships, and continued services and contributions of key personnel, including our leadership team, engineers and others at all levels of the company, as a critical part of our human capital resources. In addition, our ability to achieve our operating and strategic goals depends on our ability to identify, hire, train and retain qualified individuals. We compete with other companies both within and outside of our industry for talented personnel in a highly competitive labor market, and we may lose key personnel or fail to attract other talented personnel or otherwise identify and retain suitable replacements, and face increased 12 Table of Contents cost pressures for labor. These challenges in labor markets could have material adverse effects on our results of operations, financial condition and cash flows.

Further, our operations are subject to certain antitrust and competition laws in the jurisdictions in which we conduct our business, in particular the United States and Europe. These laws prohibit, among other things, anticompetitive agreements and practices. If any of our commercial agreements or practices are found to violate or infringe such laws, we may be subject to civil and other penalties. We may also be subject to third-party claims for damages. Further, agreements that infringe antitrust and competition laws may be void and unenforceable, in whole or in part, or require modification in order to be lawful and enforceable. Accordingly, any violation of these laws could harm our reputation and could have a material adverse effect on our earnings, cash flows and financial condition.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
