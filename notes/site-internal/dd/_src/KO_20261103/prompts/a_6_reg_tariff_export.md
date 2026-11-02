你是 stock-analyst v20 DD 的證據採集子 agent。標的：KO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - KO The Coca-Cola tariff section 232 2026
  - The Coca-Cola export control OR entity list Beverages - Non-Alcoholic 2026
  - KO The Coca-Cola China tariff OR trade restriction 2026
  - Beverages - Non-Alcoholic tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm｜as_of：2026-02-20
<<<
In the United States, the safety, production, storage, transportation, distribution, advertising, marketing, labeling and sale of our Company’s products and their ingredients are subject to the Federal Food, Drug, and Cosmetic Act; the Federal Trade Commission Act; the Lanham Act; state consumer protection laws; various federal and state laws and regulations governing competition and trade practices, including the Robinson-Patman Act of 1936, as amended, and the Clayton Antitrust Act of 1914, as amended; federal, state and local workplace health and safety laws; various federal and state laws and regulations governing our employment practices, including those related to equal employment opportunity and compensation; various federal, state and local environmental protection laws; privacy and personal data protection laws; trade laws and regulations, including laws regarding the import or export of our products or ingredients used in our products and tariffs; and various other federal, state and local statutes and regulations. We are also required to comply with the Foreign Corrupt Practices Act and the Trade Sanctions Reform and Export Enhancement Act. Outside the United States, our business is subject to numerous similar statutes and regulations, as well as other legal and regulatory requirements and regulatory reviews.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm｜as_of：2026-02-20
<<<
Other financial uncertainties in our major markets and unstable geopolitical conditions or events in certain markets, including international conflicts, civil unrest, acts of war, terrorism, governmental changes, or changes in international relations, could undermine global consumer confidence and reduce consumers’ purchasing power, thereby reducing demand for our products. Throughout 2025, the Company faced disruption to our operations due to international conflicts. Geopolitical instability has in the past led, and may in the future lead, to logistical, transportation and supply chain disruptions; business disruptions (including labor shortages); increased risk of cybersecurity incidents or other disruptions to our information systems; reduced availability and increased costs of transportation, energy, packaging, raw materials and other input costs; and heightened security risk, impacting employee safety and/or damage to infrastructure or our assets. At times, we have faced product boycotts resulting from political activism, which have reduced demand for our products. Restrictions on our ability to transfer earnings or capital across borders; price controls; limitations on profits; the negotiation of new trade agreements; new, expanded or retaliatory tariffs, including tariffs that increase suppliers’ sourcing costs; import authorization requirements; and other restrictions on business activities, which have been or may be imposed or expanded as a result of political and economic instability, deterioration of economic relations between countries or otherwise, could impact our profitability.…

The raw materials and other supplies, including ingredients, agricultural commodities, energy, fuel, packaging materials, transportation, labor and other supply chain inputs used for the production and distribution of our products, are subject to price volatility and fluctuations in availability caused by many factors. These factors include changes in supply and demand; supplier capacity constraints; a deterioration of our or our bottling partners’ relationships with suppliers; international conflicts; political uncertainties; acts of terrorism; governmental instability; inflation; weather conditions (including the effects of climate change); hurricanes, wildfires, floods, droughts and other natural disasters; disease or pests (including the impact of citrus greening disease on the citrus industry); agricultural uncertainty; health epidemics, pandemics or other contagious outbreaks; cattle disease outbreaks (including avian flu); labor shortages, strikes or work stoppages; changes in or the enactment of new laws and regulations; governmental actions or controls or import/export restrictions, such as new, expanded or retaliatory tariffs, including tariffs that increase suppliers’ sourcing costs, sanctions, quotas or trade barriers; port congestion or delays; transport capacity constraints; cybersecurity incidents or other disruptions; or fluctuations in foreign currency exchange rates. Many of our raw materials and supplies are purchased in the open market, and the prices for such items are subject to fluctuation.…

Increased or new indirect taxes could negatively affect our business. Our business operations are subject to numerous duties or taxes that are not based on income, sometimes referred to as “indirect taxes,” including import duties, tariffs, excise taxes, sales or value-added taxes, taxes on sweetened or aerated beverages, packaging taxes, carbon taxes, property taxes and payroll taxes, in many of the jurisdictions in which we operate. In addition, in the past, the U.S. Congress considered imposing a federal excise tax on beverages sweetened with sugar, HFCS or other nutritive sweeteners and may consider similar proposals in the future. As federal, state and local governments in the United States and throughout the world experience significant budget deficits, some lawmakers have singled out beverages among a plethora of revenue-raising items and have imposed or increased, or proposed to impose or increase, sales or similar taxes on beverages, particularly sweetened beverages and alcohol beverages, as well as packaging and/or packaging materials. Increases in or the imposition of new indirect taxes on our business operations or products would increase the cost of products or, to the extent levied directly on consumers, make our products less affordable, which may negatively impact our net operating revenues and profitability.

Our Company is subject to various laws and regulations in the countries and territories throughout the world in which we do business, including laws and regulations relating to competition, distribution and pricing, product safety and quality, product design, advertising and labeling, container deposits, recycling, recycled content, extended producer responsibility, the protection of the environment, occupational health and safety, employment and labor practices (including human rights), machine learning and artificial intelligence (including generative artificial intelligence), personal data protection and privacy, and data security. For additional information regarding laws and regulations applicable to our business, refer to the heading “Governmental Regulation” set forth in Part I, “Item 1. Business” of this report. Changes in applicable laws or regulations or evolving interpretations thereof, changes in enforcement priorities of regulators, and differing or competing regulations and standards across the markets where our products or raw materials are made, manufactured, distributed or sold, have in the past resulted in, and could continue to result in, higher compliance costs, higher capital expenditures and higher production costs, or make it necessary for us to reformulate certain of our products, resulting in adverse effects on our business.…

We earn revenues, pay expenses, own assets and incur liabilities in countries using many currencies other than the U.S. dollar. In 2025, we derived $28.8 billion of net operating revenues from operations outside the United States. Because our consolidated financial statements are presented in U.S. dollars, we must translate revenues, income and expenses, as well as assets and liabilities, into U.S. dollars at exchange rates in effect during or at the end of each reporting period. Therefore, increases or decreases in the value of the U.S. dollar against other currencies affect our net operating revenues, operating income and the value of balance sheet items denominated in foreign currencies. Global events, including political instability, international conflicts, trade disputes, tariffs, economic sanctions, inflation, increasing interest rates and emerging market volatility, and the resulting uncertainties, may cause currencies to fluctuate in relation to the U.S. dollar. Due to the geographic diversity of our operations, weakness in some currencies may be offset by strength in other currencies over time. We also use derivative financial instruments to further reduce our net exposure to foreign currency exchange rate fluctuations. However, fluctuations in foreign currency exchange rates, particularly the strengthening of the U.S. dollar against major currencies or the currencies of large developing countries, could materially affect our financial results.

There are increasing concerns among certain consumers, governments and other stakeholders about the damaging impact of the accumulation of plastic bottles and other packaging materials in the environment, particularly in the world’s waterways, lakes and oceans, as well as inefficient use of resources when packaging materials are not collected and recycled or reused. We and our bottling partners sell certain of our beverage products in plastic bottles and use other packaging materials that, while largely recyclable, may not be regularly recovered and recycled due to lack of collection and recycling infrastructure. If we and our bottling partners do not, or are perceived not to, act responsibly to address plastic materials recoverability and recycling concerns and associated waste management issues, our corporate image and brand reputation could be damaged, which may cause some consumers to reduce or discontinue consumption of some of our beverage products. In addition, from time to time we establish and publicly announce voluntary goals to reduce the Coca-Cola system’s impact on the environment by, for example, using more recycled content in our packaging materials.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KO_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
