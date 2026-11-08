你是 stock-analyst v20 DD 的證據採集子 agent。標的：NET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - NET Cloudflare tariff section 232 2026
  - Cloudflare export control OR entity list Software - Infrastructure 2026
  - NET Cloudflare China tariff OR trade restriction 2026
  - Software - Infrastructure tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
The United States government has implemented, or threatened to implement, tariffs on some or all of the goods imported into the United States from a number of other countries around the world. In response, many of the countries subject to these tariffs have themselves implemented or threatened to implement tariffs, taxes, or other retaliatory measures on U.S. goods or services or U.S. companies, or have restricted or threatened to restrict the operations of certain U.S. companies in those countries. The implementation, or threatened implementation, of tariffs, taxes, and other restrictions on goods, services, or businesses by the United States and other countries and the resulting additional costs and uncertainties may cause the costs of our products to increase. Additionally, future tariffs could cause the costs of the equipment we use to operate our global network to increase, corporate spending to become delayed or curtailed, increase rates of inflation, reduce economic growth rates, create an economic downturn or recession, or result in other similar or unexpected adverse effects on our business, financial condition, or results of operations.

Our future financial performance also depends in part on our ability to continue to upgrade paying customers to higher-tier subscriptions, expand the number of products we sell to paying customers and, for certain of our products, expand our paying customers' usage of such products, and, to a lesser extent, convert free customers into paying customers. Conversely, our paying customers may convert to lower-cost or free plans or reduce the number of products they purchase from us or the amount they use our products if they do not see the marginal value in paying for our higher-cost plans or for our specific products, or due to challenging macroeconomic conditions and/or reduced operating budgets, thereby impacting our ability to increase revenue. For example, we periodically have experienced a higher level of churn in our paying customer base (which is when any of our paying customers cease to be a paying customer for any reason, including any pay-as-you-go customer converting to a free subscription plan). Moreover, our free customers have no obligation to transition to paying customers at any point.…

We rely on a limited number of suppliers for several components of the equipment we use to operate our network and provide products to our customers. Our reliance on these suppliers exposes us to risks, including reduced control over production costs, increased prices due to tariffs (such as the tariffs the United States and other countries recently implemented or threatened to implement), increased prices and constraints based on the then-current availability with an increased demand, terms, and pricing of these components. For example, we generally rely on a limited number of suppliers for the servers that we use in our network and we ordinarily purchase these components on a purchase-order basis, without any long-term contracts guaranteeing supply. We may also be subject to price increases from these suppliers should they be negatively impacted by tariffs or other regulations, such as the tariffs the United States and other countries recently implemented or threatened to implement. While the network equipment and servers we purchase generally are commodity equipment and we believe an alternative supply source or location for servers on substantially similar terms could be identified quickly, our business could be adversely affected until those efforts are completed.

Geopolitical events, including conflicts and geopolitical tension around the world, or any worsening or expansion of those conflicts or tensions, may increase the likelihood of certain of these risks materializing or heighten their impact on us in affected regions. In addition, heightened use of trade restrictions and sanctions, including tariffs or prohibitions on technology transfers to achieve diplomatic ends could impact our ability to conduct our business as planned.

Our business activities are subject to various economic and trade sanctions regulations administered by the U.S. Department of the Treasury’s Office of Foreign Assets Control (OFAC) and U.S. export control and similar foreign laws and regulations, including the U.S. Department of Commerce’s Export Administration Regulations (EAR). We incorporate encryption technology into certain of our products, and the encryption products and the underlying technology may be exported outside the United States only with the required export authorizations, including by license, a license exception, or other appropriate government authorizations, including the filing of classification requests or self-classification reports. Further, the U.S. economic sanctions laws and export control laws include restrictions or prohibitions on the sale or supply of most products and services to U.S. embargoed or sanctioned countries, governments, persons, and entities.

On September 29, 2025, the U.S. Department of Commerce’s Bureau of Industry and Security (BIS) released an interim final rule that expanded export control restrictions and licensing requirements under the EAR Entity List and Military End-User List to foreign entities that are 50% or more owned by one or more parties on those lists, which BIS has labeled the “Affiliates rule.” Although the Affiliates rule was suspended for a period of one year on November 10, 2025, the Affiliates rule, if implemented, would significantly raise the bar for compliance with EAR by imposing an affirmative responsibility to know the ownership of the foreign companies that are parties to any transactions. Even though we take precautions and have implemented policies and practices to assist in compliance, there is a risk that we may not be in full compliance with these laws.

In 2019, we learned that we may have failed to comply with certain U.S. export-related filing and reporting requirements and may have submitted incorrect information to the U.S. government in connection with certain hardware exports. Upon learning of these potential violations and associated export control requirements, we promptly initiated a voluntary internal review and are taking remedial measures to prevent similar export control anomalies from occurring in the future. In May 2019, we submitted an initial voluntary self-disclosure to BIS regarding potential violations of EAR and a voluntary self-disclosure to the Census Bureau regarding potential violations of the Foreign Trade Regulations. In July 2019, we filed the full and complete voluntary self-disclosures. The voluntary self-disclosure to the Census Bureau was completed with no penalties in November 2019. The voluntary self-disclosure to BIS was completed with no penalties in June 2020.

In May 2019, we submitted an initial voluntary self-disclosure to OFAC related to our non-compliance with certain economic and trade sanctions programs, and we filed the full and complete voluntary self-disclosure to OFAC in July 2019. Specifically, we identified that our products were used by, or for the benefit of, certain individuals and entities included in OFAC’s Specially Designated Nationals and Blocked Persons List, including entities identified in 59 Table of contents OFAC’s counter-terrorism and counter-narcotics trafficking sanctions programs and individuals or entities affiliated with governments currently subject to comprehensive U.S. sanctions or located in regions subject to comprehensive sanctions. A small number of these parties made payments to us in connection with their use of our products. The voluntary self-disclosure, which we may supplement as appropriate, remains under an ongoing review by OFAC.

These efforts related to export controls and OFAC sanctions could result in negative consequences for us, including costs related to government investigations, financial penalties and harm to our reputation. The impact on us related to these matters could be substantial.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
Impact of Macroeconomic Developments The United States government has implemented, or threatened to implement, tariffs on some or all of the goods imported into the United States from a number of other countries around the world. We purchase a portion of the equipment that we use to operate our network from suppliers located outside the United States and we also purchase this equipment from United States suppliers that themselves purchase components from suppliers located outside the United States. As a result of these actual and potential U.S. tariffs, we work with our suppliers to assess the potential impact of tariffs on our equipment purchases and take actions when practical to adjust where we source the equipment we use to operate our network in the United States and in locations outside of the United States.

In addition, in response to the tariffs implemented or threatened by the United States, many of the countries subject to these tariffs have themselves implemented or threatened to implement tariffs, taxes, or other retaliatory measures on U.S. goods or services or U.S. companies, or have restricted or threatened to restrict the operations of certain U.S. companies in those countries. The implementation, or threatened implementation, of tariffs, taxes, and other restrictions on goods, services, or businesses by the United States and other countries and the resulting additional costs and uncertainties may cause the costs of our products to increase. Additionally, future tariffs could cause the costs of the equipment we use to operate our global network to increase, corporate spending to become delayed or curtailed, increase rates of inflation, reduce economic growth rates, create an economic downturn or recession, or result in other similar or unexpected adverse effects on our business, financial condition, or results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
