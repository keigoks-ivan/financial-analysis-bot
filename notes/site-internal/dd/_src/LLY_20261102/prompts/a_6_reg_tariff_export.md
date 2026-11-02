你是 stock-analyst v20 DD 的證據採集子 agent。標的：LLY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - LLY Eli Lilly and tariff section 232 2026
  - Eli Lilly and export control OR entity list Drug Manufacturers - General 2026
  - LLY Eli Lilly and China tariff OR trade restriction 2026
  - Drug Manufacturers - General tariff exposure supply chain 2026


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
In November 2025, we announced preliminary voluntary agreements with the U.S. government in which, among other arrangements, we agreed to implement measures to lower Medicaid and certain other drug prices for U.S. patients and to launch new medicines with a more balanced pricing approach across developed nations. As part of these agreements, we expect Medicare beneficiaries will have access to discounted Lilly obesity medicines by July 1, 2026, and States will have the option to expand access to these discounted medicines through Medicaid. We will also participate in a government direct-to-patient purchasing platform that will direct people in the U.S. to offerings to purchase certain medicines from us at significant discounts to current list prices. The preliminary agreements also provide a three-year grace period during which time our products under a Section 232 investigation will not face tariffs, provided that we meet U.S. manufacturing investment commitments. We are currently in the process of negotiating definitive agreements to implement these arrangements.

Governments in many emerging markets are also focused on limiting health care costs and have enacted price controls and measures impacting intellectual property. Reforms, initiatives, and other actions in our product markets, including those that may stem from political initiatives, periods of uneven economic growth or downturns or uncertainty, or as a result of inflation or deflation, trade and other global disputes and interruptions including related to tariffs, trade protection measures, and similar restrictions, the emergence, or escalation of, and responses to, international tension and conflicts, or government budgeting priorities, are expected to continue to result in added pressure on pricing, access, and reimbursement for our products.

Our active ingredient manufacturing and finishing operations, including formulation, filling, assembling, delivery device manufacturing, and packaging, take place at sites in the U.S., including Puerto Rico, Ireland and a number of other sites throughout the world. To support anticipated demand for our current and prospective products, we have undertaken significant manufacturing expansion initiatives. Investments to increase our manufacturing capacity include new sites in North Carolina, Wisconsin, Indiana, Virginia, Texas, Alabama, Pennsylvania, Ireland, Germany, and the Netherlands. We also utilize third parties for certain active ingredient manufacturing, filling, finishing operations, and for device or component production and assembly. Among other third-party providers, we, and the pharmaceutical industry generally, depend on China-based suppliers for portions of our supply chain. U.S. officials have enacted and continue to consider legislation or other actions that are intended to limit supply chain reliance on China, including the BIOSECURE Act. In addition, historically, geopolitical tensions between the U.S. and China have led to the imposition of tariffs, sanctions, and certain 21 other business restrictions between the U.S. and China. In 2025, the U.S. government imposed new tariffs on Chinese goods, and China responded with tariffs on select U.S. goods.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm｜as_of：2026-02-12
<<<
Regional or single-source dependencies may in some cases accentuate risks and costs (e.g., tariffs) related to manufacturing and supply. For example, we, and the pharmaceutical industry generally, depend on China-based suppliers for portions of our supply chain, including integral chemical synthesis, reagents, starting materials, and ingredients. Finding alternative suppliers if and as necessary due to geopolitical developments or otherwise may not be feasible or could require significant time and expense due to the nature of our products and the need to obtain regulatory approvals, which would cause disruptions to patients and detrimentally impact our business. See, Item 1A, "Risk Factors—Risks Related to Our Operations—Reliance on third-party relationships and outsourcing arrangements could adversely affect our business," and "Risk Factors—Risks Related to Doing Business Internationally—Our global operations subject us to risks, including as related to uneven economic growth or downturns, international trade, and other global disruptions, geopolitical tensions, or disputes" for more details.

External environmental factors have also caused, and in the future may cause, delays in, and/or increase costs related to, distribution of our medicines, the construction or other acquisition of additional manufacturing capacity, procurement activity, and supplier or contract manufacturer arrangements. Relevant external environmental factors include (i) tariffs, (ii) cost inflation and global transportation and logistics challenges; (iii) labor market dynamics; (iv) natural disasters (including increased instances or severity of natural disasters or other events that may be due to climate change); (v) public health outbreaks, epidemics, or pandemics; (vi) periods of uneven economic growth or downturns; and (vii) the emergence or escalation of, or responses to international tension and conflicts.

Outsourcing involves many risks, including the risk that third parties may not perform to our standards or legal requirements; may not produce reliable results; may not perform in a timely manner; may misuse or not maintain the confidentiality, integrity, and availability of confidential and proprietary information relating to us, our clinical trial subjects, or patients; may experience disruption or fail to perform due to IT system vulnerabilities, such as inadequacies, inadequate controls or procedures, operating failures, unauthorized access, service interruptions or failures, security breaches, malicious intrusions, fraud, theft, exfiltration, ransomware or other cyber-attacks; may be unable to satisfy their commitments to us in which case we may not be able to achieve acceptable alternative sourcing; or may fail to perform at all. The foregoing risks may be heightened in jurisdictions outside the U.S., where we may have fewer alternative providers as well as face additional costs, uncertainties, and risks. Among other third-party providers, we, and the pharmaceutical industry generally, depend on China-based suppliers for portions of our supply chain. U.S. officials have enacted and continue to consider legislation or other actions that are intended to limit supply chain reliance on China, including the BIOSECURE Act. In addition, historically, geopolitical tensions between the U.S.…

Significant portions of our business are conducted in Europe, Asia, and other international geographies. Our global operations and complex supply chain expose us to legislation and regulatory action in or regarding foreign jurisdictions as well as geopolitical and other cross-border risks. Trade and other global disputes, interruptions, and developments, including those related to tariffs, trade protection measures, import or export licensing requirements or disagreements with authorities regarding tariff classifications, transfer pricing, or valuations, the imposition of trade sanctions or similar restrictions by the U.S. or other governments, international tension and conflicts, as well as economic stagnation, cost inflation, strains on global transportation, manufacturing, and labor markets, and public health outbreaks, epidemics, or pandemics affect our ability to do business and, in some cases, result in financial, operational, legal, business, or reputational harm. Among other risks, the use of tariffs and other trade restrictions may increase costs, impact clinical trials or sales of our products, result in supply disruptions or delays, or otherwise complicate aspects of our business. In 2025, the U.S. and other countries imposed or reached alignment on new tariffs. In some cases, imposed tariffs have been paused but may come into effect quickly and unpredictably. While pharmaceuticals are exempt from certain of these tariffs, such exemptions may be terminated or may not apply to any future tariffs.

35 Moreover, tensions between the U.S. and China, which have already led to a series of tariffs and sanctions, as well as other business restrictions, could further escalate based on additional trade restrictions, retaliation thereto, or otherwise, which could significantly impact our business, including by increasing scrutiny of, or restrictions on, market access, operations, and business development transactions. See Item 1A, "Risk Factors—Risks Related to Our Operations—Reliance on third-party relationships and outsourcing arrangements could adversely affect our business," for additional information. The precise impact of tariffs, trade protection measures, and other restrictions may depend on their ultimate scope, timing, and other factors. If enacted, additional restrictions could result in supply disruptions or delays, further increase costs, or otherwise have a negative impact on our business. Given the nature of pharmaceutical regulation and commercialization, we may not be able to offset the burden of increased costs from tariffs and related impacts to any meaningful degree.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm｜as_of：2026-02-12
<<<
46 The U.S. and other countries have recently imposed or reached alignment on new tariffs. In some cases, imposed tariffs have been paused but may come into effect quickly and unpredictably. While pharmaceuticals are exempt from certain of these tariffs, such exemptions may be terminated or may not apply to any future tariffs. The precise impact of tariffs, trade protection measures, and other restrictions depend on their ultimate scope, timing, and other factors. If enacted, additional restrictions could result in supply disruptions or delays, further increase costs, or otherwise have a negative impact on our business. Given the nature of pharmaceutical regulation and commercialization, we may not be able to share the burden of increased costs from tariffs and related impacts to any meaningful degree.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LLY_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
