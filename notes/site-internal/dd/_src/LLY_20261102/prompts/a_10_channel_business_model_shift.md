你是 stock-analyst v20 DD 的證據採集子 agent。標的：LLY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Eli Lilly and distribution channel disruption OR shift 2026
  - LLY Eli Lilly and business model transition subscription OR platform 2026
  - Drug Manufacturers - General channel disintermediation D2C 2026
  - Eli Lilly and go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm｜as_of：2026-02-12
<<<
The products we market and their distribution vary from country to country depending on the market and applicable regulations. As applicable, we educate healthcare providers about our products in various ways, including via promotion in online and other channels, distributing information and samples of certain products to physicians, and exhibiting at medical meetings. In addition, we advertise certain products directly to consumers in the U.S., and we maintain websites and other media channels (e.g., social media) with information about our major products. Promotion of our major products in the U.S. includes engagement by employee or contracted sales representatives with physicians and other healthcare professionals.

Outside the U.S., we promote our products to healthcare providers through sales representatives and other channels. We maintain our own sales organizations in many countries. We also often utilize third parties for commercial sales operations, some of which are engaged through distribution and promotion arrangements. We provide disease-state information directly to consumers via websites, social channels, and local activations.

9 Unfavorable formulary placement can lead to reduced usage of a product for the relevant patient population due to coverage restrictions, such as prior authorizations and formulary exclusions, or due to reimbursement limitations that result in higher consumer out-of-pocket cost, such as non-preferred co-pay tiers, increased co-insurance levels, and higher deductibles. Consequently, pharmaceutical companies face increased pressure in negotiations, and compete fiercely for formulary placement, not only on the basis of product attributes such as efficacy, safety profile, or patient ease of use, but also by providing rebates or other concessions. As payers and pharmaceutical companies continue to negotiate formulary placement and rebates, value-based agreements, where rebates may be based on achievement (or not) of specified outcomes, are another prevalent tool. Rebates and net cost are important factors in formulary decisions, particularly in treatment areas in which the payer has taken the position that multiple branded products are therapeutically comparable. These pressures have negatively affected, and could continue to negatively affect, our consolidated results of operations. In addition to formulary placement, changes in insurance designs continue to drive greater consumer cost-sharing through high deductible plans, higher co-insurance, or co-pays, including increased utilization of co-pay accumulator adjustment or maximization programs.…

We have implemented a Contract Pharmacy Limited Distribution System applicable to sales through the 340B program, which generally limits distribution of 340B-priced product to: (i) covered entities and their child sites; or (ii) if a covered entity lacks an in-house outpatient pharmacy, a single contract pharmacy designated by a covered entity to establish a 340B bill to/ship to arrangement. Claims-level data is ordinarily required for any contract pharmacy. Our Contract Pharmacy Limited Distribution System contains certain exceptions that permit broader contract pharmacy usage, including for "penny priced" insulin products, provided that the covered entity passes through all discounts to eligible patients at the point of sale and meets other conditions. We believe our Contract Pharmacy Limited Distribution System complies with the 340B statute, but it remains subject to ongoing inquiries and litigation that could have a material impact on our business, as discussed in Item 8, "Financial Statements and Supplementary Data—Note 16: Contingencies."

However, pharmaceutical production processes are complex, highly regulated, and vary widely from product to product. Shifting or adding manufacturing capacity is a very lengthy process requiring significant capital expenditures, process modifications, and regulatory approvals. Accordingly, developments such as unanticipated demand, unplanned plant shutdowns, manufacturing or quality assurance difficulties at one of our facilities or contracted facilities, failure or refusal of a supplier or contract manufacturer to supply contracted quantities in a timely manner or at all, increases in demand on a supplier, or difficulties in predicting or variability in demand for or supply of our products or those of our competitors have led, and may in the future lead, to interruption or higher costs in the supply of certain products, product shortages, or pauses or discontinuations of product sales in one or more markets. Supply and channel dynamics in some cases also contribute to variability in financial results for our products from period to period.…

We routinely post important information for investors in the “Investors” section of our website, www.lilly.com. We may use our website as a means of disclosing material, non-public information and for complying with our disclosure obligations under Regulation FD. Accordingly, investors should monitor the “Investors” section of our website, in addition to following our press releases, filings with the SEC, public conference calls, presentations, and webcasts. We and our executive officers may also use social media channels to communicate with investors and the public about our business, products and other matters, and those communications could be deemed to be material information. The information contained on, or that may be accessed through, our website or our or our executive officers' social media channels, is not incorporated by reference into, and is not a part of, this Annual Report on Form 10-K.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm｜as_of：2026-02-12
<<<
We expect our near-term financial performance will be impacted by, among other factors, the timing of potential regulatory approvals for orforglipron and U.S. Medicare access for Zepbound (and, if approved, orforglipron), as well as the demand and pace of uptake in new incretin channels and markets. More generally, incretin volume fluctuations due to channel dynamics or demand can have a disproportionate impact on our results of operations in any given period. Longer term, the durability of our cardiometabolic health product offerings and sustainability of our growth and prospects will depend on our ability to maintain or strengthen our competitive position as the therapeutic landscape evolves and to deliver further innovations that provide sufficient value to sustain our growth momentum.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LLY_20261102/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
