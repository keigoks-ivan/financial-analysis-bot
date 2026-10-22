你是 stock-analyst v20 DD 的證據採集子 agent。標的：TDY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - TDY Teledyne Technologies tariff section 232 2026
  - Teledyne Technologies export control OR entity list Scientific & Technical Instruments 2026
  - TDY Teledyne Technologies China tariff OR trade restriction 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm｜as_of：2026-02-20
<<<
8 Table of Contents Risks associated with international sales and operations include, but are not limited to: •political and economic instability; •additional deterioration in United States - China and United States - Russia relations; •existing and intensifying global economic sanctions and export controls, including export controls related to China and sanctions related to Russia; •our ability to obtain export licenses in a timely manner; •unauthorized release of export-controlled or otherwise protected information; •compliance with anti-corruption laws, including the U.S. Foreign Corrupt Practices Act and the UK Bribery Act; •changes in tax laws and tariff rates; •protection and enforcement of intellectual property rights; •compliance with non-U.S. data protection laws; •existing and emerging non-U.S. regulations relating to ESG and CSR matters, which could be costly to comply with; •international terrorism; •transportation, including piracy in international waters; •currency exchange rate fluctuations; and •challenges relating to managing a global workforce with diverse cultures, backgrounds and labor laws.

Escalating global trade tensions and the adoption or expansion of tariffs and trade restrictions could negatively impact us.

The U.S. Presidential administration has announced significant new tariffs on foreign imports into the United States, particularly with respect to imports from China, and has proposed additional new tariffs that may be implemented in the future, including on member states of the European Union (“EU”) and on Canada and Mexico. High tariffs generally increase the cost of materials for our products, which could result in our products becoming less competitive or generating lower margins. The extent and duration of increased tariffs and the resulting impact on general economic conditions and on our business are uncertain and depend on various factors, such as negotiations between the United States and affected countries, the responses of other countries or regions, exemptions or exclusions that may be granted, availability and cost of alternative sources of supply, and demand for our products in affected markets. Uncertainty about whether and the extent to which new tariffs will be imposed could also impact our supply chain and the cost of our products. We have significant operations in Canada and in member states of the EU, which could be negatively impacted by a trade war with the United States. With high tariffs imposed on our products, we may also need to find new suppliers and components for our products, which could result in production delays.…

New and expanding economic sanctions and export restrictions could impact our ability to sell our products.

Recent export restrictions have had a significant impact on our business. A number of well-established customers and suppliers have become listed on government restricted party lists. In particular, U.S. export enforcement agencies have placed several Chinese companies and many of their international subsidiaries on such lists, prohibiting the export to them of most commercial and dual-use items subject to the Export Administration Regulations. Furthermore, the United States has imposed certain sectoral sanctions to limit Chinese development and manufacturing of semiconductor and supercomputer technology and have imposed comprehensive restrictions of both U.S.-origin items as well as non-U.S. items manufactured from U.S.-origin equipment. In response, China has unveiled restrictions on exports from China of certain materials and components, including gallium and germanium and which are used in semiconductor manufacturing and permanent magnets and which have impacted 9 Table of Contents the production and pricing of some of our digital imaging and aerospace and defense products. China has also increased sanctions on certain specific U.S. companies, including two Teledyne legal entities, by adding them to its Unreliable Entity List or Export Control List, which has impacted the ability of some Teledyne subsidiaries (including those not so listed) to conduct business in China. Chinese airlines and other manufacturers are under pressure to decrease their dependence on U.S.…

10 Table of Contents Government lasted 43 days and resulted in delays in contract awards, issuances of export licenses, shipments and payments of invoices for several of our businesses; any new shutdown or increase in the frequency of shutdowns could have similar or worse effects. Any renewed emphasis on Federal deficit and debt reduction could lead to a further decrease in overall defense spending.

14 Table of Contents Risks related to Legal and Compliance Matters Adverse findings in matters related to export control practices, including FLIR’s historical practices, could materially impact us.

We have made other voluntary disclosures to the U.S. Department of State and the U.S. Department of Commerce, including to the Bureau of Industry and Security (“BIS”) with respect to Teledyne FLIR shipments of products from non-U.S. jurisdictions which were not licensed due to incorrect de minimis calculation methodology under the Export Administration Regulations. We have made voluntary disclosures to export authorities in jurisdictions outside the United States for certain potential violations of local export laws.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1094285/000109428526000017/tdy-20251228.htm｜as_of：2026-02-20
<<<
Trends and Other Matters Affecting Our Business The global trade environment continues to be highly dynamic, including new potential tariffs and retaliatory tariffs, and a number of the tariffs remain in effect. There have been continuing significant tariffs and trade sanctions between the United States and China. China has also restricted the export of certain rare earth minerals that we use in our products, which could disrupt the supply chain for these minerals and components made from these materials. Tariffs, trade restrictions and retaliatory measures could result in revenue reductions, cost increases on material used in our products or significant production delays, which could adversely affect our business, financial condition, operational results and cash flows. Our manufacturing facilities span across many countries which helps us mitigate the impact of certain tariffs and trade restrictions. Also, consistent with our strategy, we continually optimize our operations and take measures to contain costs to reduce the impact from tariffs. We may also implement additional pricing actions to mitigate the impact of these tariffs. We have been working to minimize potential delivery delays and shortages of components and raw materials needed for certain products we manufacture. To date, we believe our strategies have helped minimize our exposure to these conditions. It is unclear how the recent U.S.…

U.S. Government shutdowns could negatively impact our businesses. Previous U.S. Government shutdowns have resulted in delays in anticipated contract awards, issuances of export licenses, shipments and payments of invoices for several of our businesses.

Many factors could change anticipated results, including: the impact of policies of the U.S. Presidential Administration, especially with respect to new and higher tariffs, cutbacks in the funding of government agencies and programs, and the scaling back of environmental and green energy policies; escalating economic and diplomatic tension between China and the United States, including a “trade war” resulting in higher tariffs and restrictions on sales of goods and services; reciprocal tariffs from other countries, especially from members of the EU; existing and new restrictions on the supply of rare earth minerals and permanent magnets from China; U.S. Government shutdowns, which in the past have resulted in delays in anticipated contract awards, delayed payments of invoices and delays in the issuance of export and other licenses; the inability to develop and market new competitive products; changes in relevant tax and other laws; foreign currency exchange risks; rising interest rates; risks associated with indebtedness, as well as our ability to reduce indebtedness and the timing thereof; the impact of semiconductor and other supply chain shortages; higher inflation, including wage competition and higher shipping costs; labor shortages and competition for skilled personnel; inherent uncertainties involved in the estimates and judgments used in the preparation of financial statements and the providing of estimates of financial measures, in accordance with U.S.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TDY_20261022/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
