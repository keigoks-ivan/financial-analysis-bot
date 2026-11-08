你是 stock-analyst v20 DD 的證據採集子 agent。標的：RL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - RL Ralph Lauren tariff section 232 2026
  - Ralph Lauren export control OR entity list Apparel Manufacturing 2026
  - RL Ralph Lauren China tariff OR trade restriction 2026
  - Apparel Manufacturing tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-21）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm｜as_of：2026-05-21
<<<
Import Restrictions and Other Government Regulations Virtually all of our merchandise imported into the Americas, Europe, Asia, Australia, and New Zealand is subject to duties. In addition, most of the countries to which we ship could impose safeguard quotas and duties to protect their local industries from import surges that threaten to create market disruption. In addition, each of the countries in which our products are sold has laws and regulations covering imports. Because the U.S. and the other countries in which our products are manufactured and sold may, from time to time, impose new duties, tariffs, surcharges, or other import controls or restrictions, or adjust presently prevailing duty or tariff rates or levels, we maintain a program of intensive monitoring of import restrictions and opportunities. We seek to minimize our potential exposure to import-related risks through, among other measures, adjustments in product design and fabrication, shifts of production among countries and manufacturers, and through geographical diversification of our sources of supply.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-21）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm｜as_of：2026-05-21
<<<
Risks Related to Macroeconomic Conditions Economic, political, and other conditions, including the imposition of significant new tariffs or other changes to existing trade policies and agreements, may adversely affect the global economy and/or the level of consumer purchases of discretionary items and luxury retail products, including our products.

In April 2025, the U.S. announced significant changes to its trade policies under the authority of the International Emergency Economic Powers Act ("IEEPA"), including widespread tariff increases on imported goods and the potential for additional tariffs and further increases to existing tariffs, and revisions or terminations of existing trade agreements. In response, many countries announced retaliatory tariffs on U.S. exports and other trade restrictions. In February 2026, the U.S. Supreme Court invalidated the IEEPA tariffs previously applied to our imports, after which the current administration announced a new round of tariffs under an alternative U.S. Trade Act authority. In March 2026, the U.S. Court of International Trade issued an order directing U.S. Customs and Border Protection to refund IEEPA tariffs that were previously collected, and in April 2026, U.S. Customs and Border Protection announced the refund process leveraging the Consolidated Administration and Processing of Entries Claim Portal through a phased rollout. Although we have taken steps to preserve our rights with respect to potential refunds, there can be no assurance that we will receive any refunds, in whole or in part. These developments have increased uncertainty regarding the future relationship between the U.S.…

Although we believe that our growth strategy will lead to long-term growth in revenue and profitability, there can be no assurance regarding the timing of or extent to which we will realize the anticipated benefits, if at all. Our failure to realize the anticipated benefits, which may be due to our inability to execute the various elements of our growth strategy, changes in consumer preferences, competition, economic conditions (including potential changes to existing trade policies and agreements, including higher tariffs on U.S. imports, as well as inflationary pressures), and other risks described herein, such as those related to pandemic diseases, supply chain disruptions, and military conflicts or other hostilities, could have a material adverse effect on our business. Such a failure could also result in the implementation of new restructuring-related activities, which may be dilutive to our earnings in the short term.

We do not own or operate any manufacturing facilities and depend exclusively on independent third parties for the manufacture of our products. Our products are manufactured to our specifications through arrangements with approximately 300 foreign manufacturers in various countries. In Fiscal 2026, the vast majority of our products (by dollar value) were produced outside of the U.S., primarily in Asia, Europe, and Latin America, with approximately 21% of our products sourced from Vietnam, 16% from Cambodia, and 11% from India. Risks inherent in importing our products include (i) the imposition of additional tariffs, duties, taxes, and other charges on imports or exports, such as those announced by the U.S. as discussed below; (ii) changes in diplomatic and trade relationships, including sanctions, trade restrictions, and other retaliatory measures; (iii) the imposition of additional regulations, quotas, trade sanctions, or safeguards or sourcing and reporting requirements that could increase compliance costs or lead to the detention, exclusion, or seizure of goods and imposition of monetary penalties and fines; (iv) adverse changes in local economic conditions, such as prolonged periods of economic weakness, high inflation and/or interest rates, or other factors described herein; (v) changes in social or political conditions, including those resulting from military conflicts, terrorist acts, or other hostilities, that could result in the disruption of trade from the countries in which…

As previously discussed, recent changes in U.S. trade policies, including tariff-related developments surrounding the IEEPA and other authorities, have increased uncertainty regarding the future relationship between the U.S. and other countries, as well as the potential for an ensuing global trade war and economic slowdown. The imposition of new tariffs could result in potential retaliatory tariffs from other countries and could continue to impact our supply chain costs. As approximately 96% of our products are currently produced outside of the U.S., any material change in tariffs or other trade restrictions could result in a significant increase to our product costs. There can be no assurance that we will be able to offset potential increased product costs through higher sales prices to our consumers, supply chain diversification, or other mitigating measures, which in turn could have a material adverse effect on our business due to lower profitability.

Our ability to capitalize on growth in new international markets and to maintain our current level of operations in our existing markets is subject to certain risks associated with operating in various locations around the globe. These include, but are not limited to (i) complying with a variety of U.S. and foreign laws and regulations, including, but not limited to, trade, product labeling, and product safety restrictions, as well as forced labor regulations such as the Uyghur Forced Labor Prevention Act ("UFLPA") and the Countering America's Adversaries Through Sanctions Act ("CAATSA"), both of which prohibit the importation of goods made in whole or in part in certain territories, or by certain identified entities, and grants U.S. Customs & Border Protection the authority to detain, exclude, or seize goods and assess monetary penalties and fines, the Foreign Corrupt Practices Act, which prohibits U.S. companies from making improper payments to foreign officials for the purpose of obtaining or retaining business, and similar foreign country laws, such as the U.K. Bribery Act, which prohibits U.K.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-21）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm｜as_of：2026-05-21
<<<
Global Economic Conditions and Industry Trends The global economy and retail industry are impacted by many factors beyond our control. In April 2025, the U.S. announced significant changes to its trade policies under the authority of the International Emergency Economic Powers Act ("IEEPA"), including widespread tariff increases on imported goods, with potential for new tariffs and further increases on existing tariffs in the future, as well as revisions or terminations to existing trade agreements. In response, many countries announced retaliatory tariffs on U.S. exports and other trade restrictions. In February 2026, the U.S. Supreme Court invalidated the IEEPA tariffs previously applied to our imports, after which a new round of tariffs was announced by the current administration under an alternative U.S. Trade Act authority. In March 2026, the U.S. Court of International Trade issued an order directing U.S. Customs and Border Protection to refund IEEPA tariffs that were previously collected, and in April 2026, U.S. Customs and Border Protection announced the refund process, leveraging the Consolidated Administration and Processing of Entries Claim Portal through a phased rollout. Although we have taken steps to preserve our rights with respect to the potential refunds, there can be no assurance that we will receive any refunds, in whole or in part.…

We have implemented various global strategies to address many of these challenges and continue to build a foundation for long-term profitable growth by strengthening our consumer-facing areas and driving a more efficient operating model. We continue to monitor the current geopolitical landscape, including the potential impact of changes to tariffs. We have taken proactive measures in recent years to diversify our supply chain from a geographic perspective and believe we can further mitigate potential cost pressures associated with new tariffs through a combination of our disciplined inventory management, leveraging our relationships with suppliers to reduce product costs, our ability to change country of origin, and pricing actions. However, our profitability will be negatively impacted should tariffs increase significantly across our supply chain. Regarding mitigating inflationary pressures, our strategy includes numerous levers, including our ability to effectively increase prices, leveraging our diversified supply chain and strong supplier relationships, and leveraging our in-house quality control to reduce time and cost from the manufacturing process, among other efforts. Despite the competitive environment, we plan to continue driving our broader long-term strategy of brand elevation, which includes multiple levers to continue driving average unit retail growth and brand equity.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
