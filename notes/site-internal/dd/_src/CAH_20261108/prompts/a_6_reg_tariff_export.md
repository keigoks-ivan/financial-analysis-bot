你是 stock-analyst v20 DD 的證據採集子 agent。標的：CAH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - CAH Cardinal Health tariff section 232 2026
  - Cardinal Health export control OR entity list Medical Distribution 2026
  - CAH Cardinal Health China tariff OR trade restriction 2026
  - Medical Distribution tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-11）｜章節：全文（無法依 Item 切段）｜url：https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm｜as_of：2026-08-11
<<<
6 Cardinal Health | Fiscal 2026 Form 10-K MD&A Overview Tariffs International Emergency Economic Powers Act ("IEEPA")Tariffs In February 2025, the United States imposed tariffs under the IEEPA on certain goods, materials, and products imported into the United States from countries where we do business. In February 2026, the U.S. Supreme Court ruled that the IEEPA tariffs were unlawful. Subsequent to this ruling, U.S. Customs and Border Protection (the "CBP") worked to establish a phased process to administer refunds required by the Supreme Court ruling. In April 2026 and June 2026, the U.S. Government launched its program to administer refund requests under Phase 1 and Phase 2, respectively, and additional phases are expected to be communicated in the future. The majority of our refund requests fall under Phase 2. Our refund requests under Phases 1 and 2 have been submitted and accepted by the CBP. We expect that the remainder of our refund requests will be submitted in later phases or through other established mechanics.

Since February 2025, we have paid approximately $200 million in IEEPA tariffs, related to products that we source, manufacture or distribute, primarily in our GMPD segment. After receiving refunds of IEEPA tariffs from the U.S. Government, we expect to return to customers the portion of those refunds that reflect the estimated increased prices paid related to IEEPA tariffs.

During the fourth quarter of fiscal 2026, we recorded a receivable of approximately $200 million in relation to the expected refund of IEEPA tariffs from the U.S. Government. This resulted in a net benefit to operating earnings of approximately $100 million during the three months ended June 30, 2026, primarily due to the recording of a corresponding expense related to the payments to customers. The net operating earnings impact was immaterial for fiscal 2026, due to the timing of tariff related expense recognition and the IEEPA tariff refund. The ultimate resolution of this matter could impact our results of operations in future periods, including GMPD segment profit and consolidated operating income.

Tariff Environment The tariff environment remains dynamic and we do not expect to be able to establish alternative sources of supply or otherwise mitigate the potential impact of tariffs on all of the products that we source, manufacture, or distribute. For example, in addition to the IEEPA tariffs discussed above, our GMPD segment has experienced, and expects to continue to experience increased costs as a result of tariffs imposed or expected to be imposed under different legal authority, including Sections 122, 232 and 301 of the Trade Act of 1974 and Section 308 of the Smoot-Hawley Tariff Act. Our GMPD segment continues to take action to reduce the impact of these tariffs and other potential tariffs on our financial results, including through cost optimization initiatives and by increasing prices on impacted products to customers; however, these measures have not fully offset the adverse impact. We are still incurring increased costs from tariffs, and if we are not successful at increasing prices to customers, our financial results will continue to be negatively impacted. Furthermore, if our competitors do not increase prices, or increase prices to a lesser extent than we do or are able to offset the impact of tariffs through other actions, our competitive and financial position may be adversely affected.

It is also possible that our Pharma segment could be impacted by tariffs. An April 2026 proclamation issued by the President of the United States imposed tariffs on imports of branded pharmaceutical products and associated ingredients imported into the United States. If pharmaceutical manufacturers raise their prices or stop importing certain products, we could experience increased costs or supply disruptions which may impact our financial results.

Additionally, while generic pharmaceutical products are not currently subject to U.S. tariffs, the President recently issued a statement indicating that generic pharmaceutical products will be subject to 100% tariffs beginning in 2028 and 200% tariffs beginning in 2029. There remains significant uncertainty about the ultimate implementation of this proposal; however, these potential tariffs may impact our costs or decrease available supply, which could impact Pharma segment profit and consolidated operating earnings.

Global Medical Products and Distribution GMPD segment revenue for fiscal 2026 was relatively flat at $12.7 billion due to Cardinal Health brand growth, offset by lower distribution volumes and the expected IEEPA tariff refund repayment to customers.

Global Medical Products and Distribution GMPD segment profit for fiscal 2026 increased 91 percent to $258 million from the prior year, primarily due to growth from existing customers. The net impact of tariffs to fiscal 2026 was not significant, as the adverse impact of tariff costs recognized during the year was primarily offset by the benefit of the IEEPA tariff refund.

In February 2025, the United States imposed tariffs under the International Emergency Economic Powers Act (IEEPA) on certain goods, materials, and products imported into the United States from countries where we do business.

As of the end of fiscal 2026, we have paid approximately $200 million in IEEPA tariffs, primarily related to products that we source, manufacture, or distribute in our GMPD segment. After receiving refunds of IEEPA tariffs from the CBP, we expect to return to those customers the portion of those refunds that reflect the estimated increased prices related to IEEPA tariffs.

36 Cardinal Health | Fiscal 2026 Form 10-K Risk Factors During the fourth quarter of fiscal 2026, we recorded a receivable of approximately $200 million in relation to the expected refund of IEEPA tariffs from the U.S. Government. This resulted in a net benefit to operating earnings of approximately $100 million, during the three months ended June 30, 2026, primarily due to the recording of a corresponding expense related to the payback to customers. The net operating earnings impact was immaterial for fiscal 2026, due to the timing of tariff related expense recognition and the IEEPA tariff refund. The ultimate resolution of this matter could impact our results of operations in future periods, including GMPD segment profit and consolidated operating earnings.

Following the Supreme Court IEEPA ruling, the U.S. government replaced IEEPA tariffs with tariffs imposed under Section 122 of the Trade Act of 1974. We continue to evaluate the impact of these and other tariffs, including tariffs imposed under Sections 301 and 232 of the Trade Act of 1974.

We have taken actions to reduce the impact of IEEPA and other tariffs on our financial results, including through cost optimization initiatives and by increasing prices on impacted products to customers; however, these measures have not fully offset the negative impact. Tariffs imposed or threatened to be imposed on goods, materials, and products from countries where we do business, and any retaliatory actions taken by such countries could result in us incurring substantial additional costs to source materials, directly and indirectly, from affected countries, and require us to raise prices on certain products and seek alternative sources of supply. If our competitors do not increase prices, or increase prices to a lesser extent than we do, or are able to offset the impact of tariffs through other actions, our competitive and financial position may be adversely affected. Additionally, if we are not able to find adequate alternate sources of supply, we may experience supply shortages or disruptions. Additionally, in certain circumstances, including in our other operating segments, we may not receive increased reimbursement commensurate with the increase in costs, which may negatively impact our results of operations.

Other events outside of our control also have, and will continue to, directly and indirectly adversely impact our operations and financial results. These events include those related to public health crises, including epidemics or pandemics; geopolitical events or tensions, including civil unrest, trade sanctions, tariffs and other trade restrictions, armed conflicts, or terrorism; negative or declining global economic conditions, or unstable international governments and legal systems. Among other potential affects, these events may have a disruptive and unpredictable impact on our operations and those of our suppliers and vendors, or customers, hinder manufacturing and transportation, result in significant excess costs, lead to shifts in customer demand, or have a negative impact on capital markets. For example, the recent conflict in Iran has resulted in increased fuel prices which may lead to increased costs for products that we source, manufacture, or distribute, and may also cause supply chain or manufacturing disruptions, impacting our ability to meet demand. Such events are inherently unpredictable, and our responses may involve the implementation of measures which may not be as successful as intended in mitigating adverse impacts.

During the fourth quarter of fiscal 2026, we recorded a receivable of approximately $200 million in relation to the expected refund of IEEPA tariffs from the government, which is included in prepaid expenses and other assets in the consolidated balance sheet. Upon receiving refunds of IEEPA tariffs from the government, we expect to return to those customers the portion of those refunds that reflect the estimated increased prices paid related to IEEPA tariffs.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
