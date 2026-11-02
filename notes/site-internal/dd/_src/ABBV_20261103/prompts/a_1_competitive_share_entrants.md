你是 stock-analyst v20 DD 的證據採集子 agent。標的：ABBV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - ABBV AbbVie market share gaining OR losing 2026
  - AbbVie new entrant OR displace threat Drug Manufacturers - General 2026
  - ABBV competitor design win 2026
  - AbbVie vs Drug Manufacturers - General peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm｜as_of：2026-02-20
<<<
5 | 2025 Form 10-K Competition The markets for AbbVie's products are highly competitive. AbbVie competes with other research-based pharmaceuticals and biotechnology companies that discover, manufacture, market and sell proprietary pharmaceutical products, therapies and biologics. For example, AbbVie's immunology products compete with IL-23 inhibitors, IL-17 inhibitors, JAK inhibitors, biosimilars and other competitive products intended to treat a number of disease states, and AbbVie's oncology products compete with targeted therapies including BTK inhibitors, ADCs, cell therapies and other competitive products intended to treat certain cancers. In addition, a number of other companies have successfully developed and market products that are being positioned as competitors to Botox. The search for technological innovations in pharmaceutical products is a significant aspect of competition. The introduction of new products by competitors and changes in medical practices and procedures can result in product obsolescence. Price is also a competitive factor. In addition, the substitution of generic and biosimilar pharmaceutical products for branded pharmaceutical products creates competitive pressures on AbbVie's products that do not have patent protection. New products or treatments brought to market by AbbVie’s competitors could cause revenues for AbbVie’s products to decrease due to price reductions and sales volume decreases.

Humira faces direct biosimilar competition globally and AbbVie will continue to face competitive pressure from these biologics and from orally administered products.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm｜as_of：2026-02-20
<<<
As patents for certain of its products expire, AbbVie could face competition from lower priced generic or biosimilar products. The expiration or loss of patent protection for a product typically is followed promptly by substitutes that may significantly reduce sales for that product in a short amount of time. If AbbVie's competitive position is compromised because of generics, biosimilars or otherwise, it could have a material adverse effect on AbbVie's business and results of operations. In addition, proposals emerge from time to time for legislation to further encourage the early and rapid approval of generic drugs or biosimilars. Any such proposals that are enacted into law could increase the impact of generic or biosimilar competition.

Large pharmaceutical companies and generics manufacturers of pharmaceutical products continue to expand into the biotechnology field and form partnerships to pursue biosimilars. Companies have developed and are developing biosimilars that compete with AbbVie’s biologic products. As competitors obtain marketing approval for biosimilars referencing AbbVie’s biologic products, AbbVie’s products may become subject to competition from such biosimilars, with the attendant competitive pressure and consequences. Expiration of or successful challenges to AbbVie’s applicable patent rights could also trigger competition from other products, assuming any relevant exclusivity period has expired. As a result, AbbVie could face increased litigation and administrative proceedings with respect to the validity and/or scope of patents relating to its biologic products.

To remain competitive, AbbVie must continue to launch new products and new indications and/or brand extensions for existing products. Such launches must generate revenue sufficient both to cover its substantial research and development costs and to replace revenues of profitable products that are lost to or displaced by competing products or therapies. Failure to do so would have a material adverse effect on AbbVie's revenue and profitability. Accordingly, AbbVie commits substantial effort, funds and other resources to research and development and must make ongoing substantial expenditures without any assurance that its efforts will be commercially successful. A high rate of failure in the biopharmaceutical industry is inherent in the research and development of new products, and failure can occur at any point in the research and development process, including after significant resources have been invested.…

AbbVie competes with other research-based pharmaceutical and biotechnology companies that research, develop, manufacture, market and sell proprietary pharmaceutical products and biologics. All of these competitors may introduce new products or develop technological advances that compete with AbbVie’s products in therapeutic areas such as immunology, neuroscience, oncology and aesthetics. In addition, as AbbVie products lose exclusivity, competition surrounding such products will increase and generic and biosimilar products will increasingly penetrate the markets. Furthermore, consolidation 2025 Form 10-K | 18 among certain pharmaceutical and biotechnology companies can enhance such advantages. These advantages may make it difficult for us to compete with them successfully to discover, develop and market new products and for our current products to compete with new products or indications they may bring to market. AbbVie cannot predict with certainty the timing or impact of the introduction by competitors of new products or technological advances. Such competing products may be safer, more effective, more effectively marketed or sold, have lower prices or better insurance coverage or reimbursement levels, or have superior performance features than AbbVie’s products, and this may negatively impact AbbVie’s business and results of operations.

In the ordinary course of business, AbbVie is the subject of product liability claims and lawsuits alleging that AbbVie's current or historical products or the products of other companies that it promotes have resulted or could result in an unsafe condition for or injury to patients. Product liability claims and lawsuits and safety alerts or product recalls, regardless of their ultimate outcome, may have a material adverse effect on AbbVie's business, results of operations and reputation and on its ability to attract and retain customers. Consequences may also include additional costs, a decrease in market share for the product in question, lower revenue and exposure to other claims. Additionally, some of these matters involve numerous plaintiffs and parties seeking large or indeterminate financial claims and may remain unresolved for several years. AbbVie evaluates its risks and has determined that the cost of obtaining product liability insurance outweighs the likely benefits of the coverage that is available and, as such, AbbVie's product liability losses are self-insured.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABBV_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
