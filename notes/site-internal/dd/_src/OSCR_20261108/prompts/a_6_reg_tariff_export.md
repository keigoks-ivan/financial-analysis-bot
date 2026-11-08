你是 stock-analyst v20 DD 的證據採集子 agent。標的：OSCR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - OSCR Oscar Health tariff section 232 2026
  - Oscar Health export control OR entity list Healthcare Plans 2026
  - OSCR Oscar Health China tariff OR trade restriction 2026
  - Healthcare Plans tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm｜as_of：2026-02-13
<<<
26 Table of Contents We also incur substantial administrative costs, particularly distribution costs, the costs of scaling and improving our operations, and the costs of hiring and retaining personnel. External factors, including general economic conditions such as inflation, tariffs, and unemployment levels and federal and state legislative and regulatory actions, are generally beyond our control and could further reduce our ability to accurately estimate and effectively control our administrative expenses, including the cost of our third-party vendors. Furthermore, regulatory changes or developments may require us to change our existing practices with respect to broker commissions and could potentially result in a substantial increase in related costs or limit our ability to manage those costs in the future. Any such increase in costs could cause our actual results to differ, potentially materially, from our prior expectations. As a result of our market expansion, expansion of our plan offerings and growth of our membership, our anticipated medical expenses and administrative costs are subject to additional uncertainty.

Changes in laws, regulations or rules relating to taxes or tariffs could adversely affect us.

Changes in laws relating to taxes and tariffs could adversely impact our business, results of operations, financial condition and cash flows. On July 4, 2025, the OBBBA was signed into law. In addition to the changes to the ACA discussed above, OBBBA included business tax provisions such as the reinstatement of rules related to the deductibility of research and experimental (“R&E”) expenditures and the reinstatement of bonus depreciation deductions for qualified property and modifications to EBITDA-based business interest expense limitations. Pursuant to the OBBBA’s transition rules, the Company elected to expense all unamortized, domestic R&E costs previously capitalized between 2022 and 2024. As the Company maintains a valuation allowance against its net deferred tax assets, including NOLs, this election resulted in no change to tax expense for the year ended December 31, 2025.

The Trump administration has indicated that tariffs may be imposed on a variety of products relevant to our business, including certain pharmaceutical products and ingredients and medical devices and supplies imported into the United States. Any such tariffs could result in higher costs for medical providers and facilities, higher pharmaceutical prices, higher costs of medical devices, and shortages of certain medicines and medical supplies. Shortages in medicines and supplies may also impact the health of our members, which in turn may result in higher medical costs. The substantial uncertainty regarding the potential imposition and implementation of tariffs could adversely impact our ability to accurately estimate and manage medical costs and expenses and adversely affect our results of operations and financial position.

40 Table of Contents The regulations and contractual requirements applicable to us and other market participants are complex and subject to change, making it necessary for us to invest significant resources in complying with our regulatory and contractual requirements. Ongoing vigorous legal enforcement and the highly technical regulatory scheme mean that our compliance efforts in this area will continue to require significant resources, and we may not always be successful in ensuring appropriate compliance by our employees, consultants, or vendors, for whose compliance or lack thereof we may be held responsible and liable. Regulatory audits, investigations, and reviews could result in significant or material changes to our business practices, including increased capital requirements, and also could result in significant or material premium refunds, fines, penalties, civil liabilities, criminal liabilities, or other sanctions, including marketing and enrollment sanctions, suspension or exclusion from participation in government programs, imposition of heightened monitoring by our federal or state regulators, and suspension or loss of licensure if we are determined to be in violation of applicable laws or regulations. Any of these audits, reviews, or investigations could have a material adverse effect on our financial position, results of operations, or business, or could result in significant liabilities and negative publicity for the Company.

Our vendor and service provider arrangements could be adversely impacted by changes in vendors’ or service providers’ operations or financial condition, or other matters outside of our control. Violations of, or noncompliance with, laws and/or regulations governing our business or noncompliance with contract terms by third-party vendors and service providers could increase our exposure to liability to our members, providers, or other third parties, or could result in sanctions and/or fines from the regulators that oversee our business. In turn, this could increase the costs associated with the operation of our business or have an adverse impact on our business and reputation. Moreover, if these vendor and service provider relationships are terminated for any reason, we may not be able to find alternative partners in a timely manner or on acceptable financial terms, and may incur significant costs and/or experience significant disruption to our operations in connection with any such vendor or service provider transition. As a result, we may not be able to meet the full demands of our members or customers and, in turn, our business, financial condition, and results of operations may be harmed, and we could be subject to regulatory sanctions and fines and penalties.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1568651/000156865126000011/oscr-20251231.htm｜as_of：2026-02-13
<<<
66 Table of Contents Proposed Tariffs The Trump administration has indicated that new tariffs may be imposed on a variety of products relevant to our business, including certain pharmaceutical products and ingredients and medical devices and supplies imported into the United States. If such tariffs are imposed, the potential impact could include, among other things, higher costs for medical providers and facilities, higher pharmaceutical prices, higher costs of medical devices, and supplies and shortages of certain medicines and medical supplies. Shortages in medicines and supplies may also impact the health of our members, which in turn may result in higher medical costs. The unprecedented nature of these types of tariffs, as well as uncertainty around their implementation, could impact our ability to accurately estimate and effectively manage the impact on our medical expenses, which in turn could adversely affect our results of operations and financial position. For additional details, see Part I, Item 1A. “Risk Factors-Most Material Risks to Us-Failure to accurately estimate our incurred medical expenses or overall market morbidity, or effectively manage our medical costs or related administrative costs could negatively affect our financial position, results of operations, and cash flows” and “Risk Factors-Risks Related to the Regulatory Framework That Governs Us-Changes in laws, regulations or rules relating to taxes or tariffs could adversely affect us.”
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
