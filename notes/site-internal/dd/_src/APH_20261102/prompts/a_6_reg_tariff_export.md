你是 stock-analyst v20 DD 的證據採集子 agent。標的：APH。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - APH Amphenol tariff section 232 2026
  - Amphenol export control OR entity list Electronic Components 2026
  - APH Amphenol China tariff OR trade restriction 2026
  - Electronic Components tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926013549/aph-20251231x10k.htm｜as_of：2026-02-11
<<<
​ Raw Materials ​ The Company purchases a wide variety of raw materials for the manufacture of its products, including (i) precious metals such as gold, silver and palladium, (ii) aluminum, steel, copper, titanium and metal alloy products (iii) copper wire and optical fiber, and (iv) plastic materials. The Company also purchases a wide variety of mechanical and electronic components for the manufacturing of its products. Such raw materials and components are generally available throughout the world and are purchased locally from a variety of suppliers. The Company is generally not dependent upon any one source for raw materials or components or, if one source is used, the Company generally attempts to protect itself through long-term supply agreements. From time to time, the Company has encountered, and in the future may encounter, difficulties in obtaining certain raw materials or components necessary for production at reasonable costs due to supply chain constraints and logistical challenges, which may include regulatory restrictions and the imposition of additional tariffs. These difficulties may also negatively impact the pricing of materials and components sourced or used by the Company.…

​ Government Regulation ​ As a global company, we are subject to various laws and regulations applicable to parties doing business with the U.S. and other governments, including laws and regulations governing reporting obligations, interactions with government officials, performance of government contracts, the use and treatment of government furnished property and the nature of materials used in our products. In addition, the Company and its products are subject to import and export regulations present in each of the various jurisdictions in which we operate around the world. Certain of our products, including purchased components of such products, are subject to U.S. and non-U.S. export control laws and regulations, and may be exported only with the required export license or through an export license exception. The issuances of such licenses, in particular within the defense market, are subject to complex laws and regulations that could change frequently and with limited notice, depending on the jurisdiction, geopolitical events or other factors. The Company has systems in place to apply for licenses and to maintain compliance with any such regulations. Separately, we are required to comply with certain U.S. and non-U.S. economic sanctions and trade embargoes, as well as the terms of any preferential duty and/or tariff programs in which we participate.

​ For a discussion of certain risks related to government regulation, including export and import controls and sanctions, refer to the risk factors titled “The Company is exposed to political, economic, military and other risks related to operating in countries outside the United States, and changes in general economic conditions, geopolitical conditions, U.S. and other countries’ trade policies and other factors beyond the Company’s control may adversely impact its business and operating results,” “The Company must comply with complex export and import controls as well as economic sanctions and trade embargoes imposed by the United States government and other countries,” “Our business and financial results may be adversely affected by government contracting risks,” and “Our international operations require us to comply with anti-corruption laws and regulations of the U.S. government and various foreign jurisdictions, and our business reputation and financial results may be impaired by improper conduct by any of our employees, customers, suppliers, distributors or any other business partners,” in Part I, Item 1A. Risk Factors herein.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/820313/000110465926013549/aph-20251231x10k.htm｜as_of：2026-02-11
<<<
​ During the last few years, there have been significant changes to U.S. and other countries’ trade policies, export control laws, sanctions, legislation, treaties and tariffs, including U.S. trade policies and tariffs affecting several of the countries in which we operate. The U.S. continued to impose new tariffs on imports to the U.S. throughout 2025, and in response, several countries have imposed, or threatened to impose, reciprocal tariffs on imports from the U.S. and other retaliatory measures. These changes have, in certain cases, increased our costs of doing business. There is significant uncertainty about the future of trade relationships around the world, including potential changes to trade laws and regulations, trade policies, and tariffs. We cannot predict what additional actions may ultimately be taken by the U.S. or other governments with respect to tariffs or trade relations, what products may be subject to such actions (including subject to U.S. export control restrictions), what actions may be taken by the other countries in retaliation or whether we would be able to fully mitigate the impact of any such actions by pricing or other measures.…

​ The Company purchases a wide variety of raw materials for the manufacture of its products, including (i) precious metals such as gold, silver and palladium, (ii) aluminum, steel, copper, titanium and metal alloy products, (iii) copper wire and optical fiber and (iv) plastic materials. In the past, prices for these and certain other basic materials have experienced significant volatility. While the Company does not currently anticipate significant, broad-based difficulties in obtaining raw materials or components necessary for production, it has, from time to time, experienced certain difficulties, and inflationary pressures, increased commodity prices and regulatory restrictions may impact the cost and availability of certain raw materials and components used by the Company and result in supply shortages for discrete raw materials or components. Moreover, the Company may not be able to pass along any increased raw material or component prices to its customers and may not be able to procure and obtain sufficient quantities of raw materials and components in a timely manner and at acceptable prices from our suppliers.…

​ We, as well as some of our customers, are subject to various laws and regulations applicable to parties doing business with the U.S. and other governments, including laws and regulations governing reporting, cybersecurity and procurement obligations, interactions with government officials, performance of government contracts, the use and treatment of government furnished property and the nature of materials used in our products, many of which are complex, frequently changing, and subject to varying interpretations. We may be unilaterally suspended or barred from conducting business with the U.S. and other foreign governments or their suppliers (both directly and indirectly), become subject to fines or other sanctions or prohibited from taking certain actions if we are found to have violated such laws or regulations. For example, under the executive order titled “Prioritizing the Warfighter in Defense Contracting” issued in January 2026, defense contractors designated as underperforming by the Secretary of War are prohibited from conducting stock buybacks and issuing dividends until their performance improves. As a result of the need to comply with these numerous laws and regulations, we are subject to increased risks of governmental investigations, civil fraud actions, criminal prosecutions, whistleblower lawsuits and other enforcement actions. The U.S.…

​ Certain of our products, including purchased components of such products, are subject to U.S. and non-U.S. export control laws and regulations, and may be exported only with the required export license or through an export license exception. In addition, we are required to comply with certain U.S. and non-U.S. economic sanctions and trade embargoes that restrict our ability to transact or deal with certain persons, countries, regions, and governments. These laws and regulations are complex, may change frequently and without prior notice, have generally become more stringent over time and have intensified under recent U.S. administrations, especially in light of ongoing tensions between the U.S. and China, as well as other countries. For example, in 2019, the U.S. government added certain companies based in China to the “Entity List” maintained by the U.S. Department of Commerce, which imposes additional restrictions on sales to such companies. Since 2019, numerous other companies have been added to that list. Further, in 2022, the U.S. Commerce Department’s Bureau of Industry and Security (“BIS”) released new export control regulations that restrict the provision to China of certain technology, software, manufacturing equipment and commodities that are used to make certain advanced computing integrated circuits (“ICs”) and supercomputers. These changes include new restrictions on the ability of U.S.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APH_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
