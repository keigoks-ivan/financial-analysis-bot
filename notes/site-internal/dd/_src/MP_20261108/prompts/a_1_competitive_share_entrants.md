你是 stock-analyst v20 DD 的證據採集子 agent。標的：MP。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MP MP Materials market share gaining OR losing 2026
  - MP Materials new entrant OR displace threat Rare Earth Mining + Magnet Manufacturing 2026
  - MP competitor design win 2026
  - MP Materials vs Rare Earth Mining + Magnet Manufacturing peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm｜as_of：2026-02-26
<<<
Competition The rare earth mining, processing, and magnetics manufacturing markets are capital-intensive and highly competitive. With continued state-sponsored consolidation, there remain two major rare earth groups in China. These groups and their affiliates control (and/or allocate to unaffiliated third parties) substantially all of China’s quota for concentrate production and rare earth refining. In 2025, China took additional steps to consolidate control of the industry into the two major groups through export and import limitations, as well as adjustments to the production quota system. Outside of China, there are few producers operating at scale, with only one other major integrated operator across Australia and Malaysia. China also maintains a dominant position in the supply of NdFeB permanent magnets due to its vast rare earth reserves, advanced processing capabilities, and vertically integrated production infrastructure.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm｜as_of：2026-02-26
<<<
We operate in a highly competitive industry. The rare earth mining and processing and magnet manufacturing industry is capital intensive with competitive market dynamics. Production of REE and magnet products is dominated by our Chinese competitors. These competitors may have greater financial resources, as well as other strategic advantages to operate, maintain, improve, and possibly expand their facilities. Additionally, our Chinese competitors have historically been able to produce at relatively low costs due to domestic economic and regulatory factors, including less stringent environmental and governmental regulations and lower labor and benefit costs. If we are not able to achieve consistent product quality at our anticipated costs of production, then any strategic advantages that our competitors may have over us, including, without limitation, lower labor, compliance, and production costs, could have a material adverse effect on our business.

Some of our competitors have made, or may make, acquisitions or enter into partnerships or other strategic relationships to achieve competitive advantages. In addition, new entrants not currently considered competitors may enter our market through acquisitions, partnerships, or strategic relationships. We expect these trends to continue as demand for rare earth materials increases. Industry consolidation may result in competitors with more compelling product offerings or greater pricing flexibility than we have, or business practices that make it more difficult for us to compete effectively, including on the basis of price, sales, technology or supply. For example, in 2025, China took additional steps to consolidate control of the industry into the two major groups through export and import limitations, as well as adjustments to the production quota system. Outside of China, there are few producers operating at scale, with processing capabilities located in only one other major integrated operator across Australia and Malaysia. These competitive pressures could have a material adverse effect on our business.

Much of the technology used in the markets in which we compete is protected by patents and trade secrets, and our commercial success will depend in significant part on our ability to obtain and maintain patent and trade secret protection for our products and methods. To compete in these markets, we rely on a combination of trade secret protection, nondisclosure and licensing agreements, patents and trademarks to establish and protect our proprietary intellectual property rights, including our proprietary rare earth production processes that are not patented. Our intellectual property rights may be challenged or infringed upon by third parties, or we may be unable to maintain, renew or enter into new license agreements with third-party owners of intellectual property on reasonable terms. In addition, our intellectual property may be subject to infringement or other unauthorized use outside of the U.S. In such case, our ability to protect our intellectual property rights by legal recourse or otherwise may be limited, particularly in countries where laws or enforcement practices are undeveloped or do not recognize or protect intellectual property rights to the same extent as the U.S. Unauthorized use of our intellectual property rights or our inability to preserve existing intellectual property rights could adversely impact our competitive position and results of operations.…

Proprietary trade secrets and unpatented know-how are also very important to our business. We rely on trade secrets to protect certain aspects of our technology, especially where we do not believe that patent protection is appropriate or obtainable. However, trade secrets are difficult to protect. Our employees, consultants, contractors, outside scientific collaborators and other advisors may unintentionally or willfully disclose our confidential information to competitors, and confidentiality agreements may not provide an adequate remedy in the event of unauthorized disclosure of confidential or proprietary information. It is expensive and time consuming, with no certain outcome, to pursue a claim that a third party illegally obtained and is using our trade secrets. Moreover, our competitors may independently develop equivalent knowledge, methods and know-how. Failure to obtain or maintain trade secret protection could adversely affect our competitive business position.

Our ability to obtain additional patents is uncertain and the legal protection afforded by these patents is limited and may not adequately protect our rights or permit us to gain or keep any competitive advantage. In addition, the specific content required of patents and patent applications that are necessary to support and interpret patent claims is highly uncertain due to the complex nature of the relevant legal, scientific and factual issues. Changes in either patent laws or interpretations of patent laws in the U.S. or elsewhere may diminish the value of our intellectual property or narrow the scope of our patent protection. Even if patents are issued regarding our products and processes, our competitors may challenge the validity of those patents. Patents also will not protect our products and processes if competitors devise ways of making products without infringing our patents.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
