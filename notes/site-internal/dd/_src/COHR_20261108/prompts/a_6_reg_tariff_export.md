你是 stock-analyst v20 DD 的證據採集子 agent。標的：COHR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - COHR Coherent tariff section 232 2026
  - Coherent export control OR entity list Scientific & Technical Instruments 2026
  - COHR Coherent China tariff OR trade restriction 2026
  - Scientific & Technical Instruments tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-14）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm｜as_of：2026-08-14
<<<
Import and Export Compliance We are required to comply with all relevant import/export and economic sanctions laws and regulations, including: •The import regulations administered by U.S. Customs and Border Protection; •The International Traffic in Arms Regulations (ITAR) administered by the U.S. Department of State, Directorate of Defense Trade Controls, which among other things impose licensing requirements on the export from the United States of certain defense articles and defense services, generally including items that are specially designed or adapted for a military application and/or listed on the United States Munitions List; •The Export Administration Regulations (EAR) administered by the U.S. Department of Commerce, Bureau of Industry and Security, which among other things impose licensing requirements on certain dual-use goods, technology, and software; and •The regulations administered by the U.S. Department of the Treasury, Office of Foreign Assets Control, implementing economic sanctions against designated countries, governments, and persons based on U.S. foreign policy and national security considerations.

Foreign governments also have similar import and export controls, sanctions, laws, and regulations. For additional discussion regarding our import, export, and sanctions compliance, see the discussion in Item 1A. Risk Factors of this Annual Report on Form 10-K.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-14）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm｜as_of：2026-08-14
<<<
We have made and are planning to make significant investments to satisfy increased customer demand, including expansion of our production capacity in the United States and in other regions where we operate. These projects are highly dependent on available sources of materials, and specialized equipment, as well as labor, skilled sub-contractors and other service providers. Increasing demand, supply constraints, inflation, tariffs, trade restrictions, and other market conditions could result in shortages and higher costs. Additionally, difficulties in obtaining labor, skilled sub-contractors and other service providers or other resources could result in delays in completion of our construction projects and cost increases, including costs to operate these facilities. Our ability to increase production is also subject to regulatory approvals, environmental and operational permits, clean-room and tool availability, hiring and training of qualified personnel, implementation of highly complex manufacturing processes, and the pace of bringing equipment and processes online with the capability to manufacture high-quality products at acceptable yields.

Similarly, changes in U.S. federal policy that affect the geopolitical landscape could give rise to circumstances outside our control that could have negative impacts on our business operations. For example, in early 2025, the United States implemented significant new tariffs on foreign imports impacting multiple countries, commodities and industries, and those new tariffs and export restrictions also prompted retaliatory tariffs and export restrictions from certain countries. A number of these tariffs remain in effect, including significant tariffs and trade sanctions between the United States and China. Historically, tariffs have led to increased trade and political tensions and, to date, the outcome of the negotiations between the United States and the various countries is not yet clear.

The legal landscape governing these measures also remains unsettled. On February 20, 2026, the U.S. Supreme Court rendered a decision invalidating tariffs imposed under the International Emergency Economic Powers Act (“IEEPA”), which introduces uncertainty regarding potential refund processes and future trade-policy actions. In addition, the U.S. government has initiated investigations under Section 232 of the Trade Expansion Act of 1962 to evaluate whether additional tariffs may be necessary on certain commodities, including semiconductors, critical minerals, and derivative electronics products, on national-security grounds, and upon completion of these investigations the President may direct the imposition of additional tariffs on these or other commodities. Because we manufacture and source products both in the United States and internationally, and derive a portion of our revenue from foreign customers, we may be more susceptible to negative impacts from these measures than less internationally focused enterprises, and such measures could trigger further retaliatory actions by affected countries.

We cannot predict what actions may be taken with respect to export regulations, tariffs, or other trade regulations between the United States and other countries, what products or companies may be subject to such actions, or what actions may be taken by other countries in retaliation. Further changes in trade policy, tariffs, restrictions on exports or other trade barriers, or restrictions on supplies, equipment, and raw materials including rare earth minerals, may limit our ability to produce products, increase our selling and/or manufacturing costs, decrease margins, reduce the competitiveness of our products, or inhibit our ability to sell products or purchase necessary equipment and supplies. For example, increasing geopolitical tensions could result in new export controls associated with products that support or enable AI or data center infrastructure applications which could, in turn, restrict future sales of certain products to certain markets in which we operate. Such changes may also result in reputational harm to us, the development or adoption of technologies that compete with our products, long-term changes in global trade and technology supply chains, or negative impacts on our customers’ products which incorporate our solutions. Any of the effects described in this risk factor could have a material adverse effect on our business, results of operations, or financial condition.

Our business is subject to various domestic and international laws and other legal requirements, including anti-corruption regulations, such as the Foreign Corrupt Practices Act of 1977, anti-money laundering regulations, anti-competition and import/export regulations, such as the U.S. Export Administration Regulations (“EAR”), and applicable executive orders. We are subject to the passage of and changes in the interpretation of import/export regulation by U.S. and other government entities at the federal, state, and local levels and by non-U.S. agencies, including, but not limited to, the following: •We are required to comply with import laws and export control and economic sanctions laws, which may affect our ability to enter into or complete transactions with certain customers, business partners, and other persons. In certain circumstances, export control and economic sanctions laws may prohibit the export of certain products, services, and technologies. We may be required to obtain an export license before exporting a controlled item, and granting of a required license cannot be assured. Compliance with the import laws that apply to our businesses may restrict our access to, and may increase the cost of obtaining, certain products and could interrupt our supply of imported inventory.

Obtaining export licenses can be difficult, time-consuming and require interpretation of complex regulations. Failure to obtain and/or retain export licenses for these shipments could significantly reduce our revenue and materially adversely affect our business, financial condition, results of operations and relationships with our customers.

The U.S. government may continue to add companies to its restricted entity list and/or technologies to its list of prohibited exports to specific countries, which have had and may in the future have an adverse effect on our revenue and our ability to sell our products. If export controls are imposed or tightened after we have committed to manufacturing capacity or placed orders with our suppliers to address anticipated demand, the resulting reduction in demand for affected products could require us to record substantial charges for excess or obsolete inventory and for noncancellable purchase obligations. Any such charges could have a material adverse effect on our business, results of operations, or financial condition.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-14）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/820318/000082031826000020/iivi-20260630.htm｜as_of：2026-08-14
<<<
See Note 7. Assets Held-for-Sale and Sale of Businesses for further information. Macroeconomic Conditions - Tariffs and Export Controls In early 2025, the United States implemented significant new tariffs and export restrictions affecting a broad range of countries, commodities and industries. These actions have prompted retaliatory measures from certain foreign governments, including the imposition of tariffs and export controls. On February 20, 2026, the U.S. Supreme Court ruled that tariffs imposed under the International Emergency Economic Powers Act (“IEEPA”) were not authorized by the statute. The Company is the importer of 37 Table of Contents record for certain raw materials and products that were previously subject to such tariffs under IEEPA. During the fourth quarter of fiscal 2026, following the orders of the U.S. Court of International Trade directing U.S. Customs and Border Protection to refund such duties, the Company concluded that recovery of a portion of previously paid tariffs was probable. As a result, the Company recorded the receipt of tariff refunds received and recognized a net receivable for additional refunds expected to be recovered. The amounts recorded were not material to the Company. The receivable represents the Company’s estimate of recoverable tariffs associated with eligible import entries based on information available as of June 30, 2026, including shipment‑level data and applicable court rulings guidance.…

As a global company with a substantial and diversified manufacturing footprint, we have some ability to mitigate the effects of tariffs, trade sanctions, and other geopolitical challenges. Our global supply chain and internal production capabilities for many critical components provides flexibility in sourcing and manufacturing, which helps support costumer demand and business continuity. However, sustained disruption in global trade conditions could increase costs, disrupt operations, reduce demand or delay production, adversely affecting our business, financial condition, results of operations and cash flows.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
