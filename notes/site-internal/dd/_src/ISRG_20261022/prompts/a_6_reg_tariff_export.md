你是 stock-analyst v20 DD 的證據採集子 agent。標的：ISRG。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - ISRG Intuitive Surgical tariff section 232 2026
  - Intuitive Surgical export control OR entity list Medical Instruments & Supplies 2026
  - ISRG Intuitive Surgical China tariff OR trade restriction 2026
  - Medical Instruments & Supplies tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm｜as_of：2026-02-03
<<<
We perform research and development activities, manufacture, and distribute our products in OUS markets. Revenue from OUS markets accounted for approximately 32%, 33%, and 34% of our revenue for the years ended December 31, 2025, 2024, and 2023, respectively. Our OUS operations are, and will continue to be, subject to a number of risks including: •the failure to obtain or maintain the same degree of protection against infringement of our intellectual property rights due to differing intellectual property protection laws in OUS countries from those in the U.S.; •multiple OUS regulatory requirements that are subject to change and that could impact our ability to manufacture and sell our products; •changes in tariffs, trade barriers, and regulatory requirements, such as the enactment of tariffs on goods imported into the U.S. including, but not limited to, potential tariffs on goods imported from Mexico where we manufacture a significant majority of our instruments and accessories that we sell; •protectionist laws, policies, and business practices that favor local competitors or lead non-U.S. customers to favor domestic technology solutions over imports, which could slow our growth, increase our costs, or make our products less competitive in OUS markets; •local or national regulations that make it difficult or impractical to market or use our products; •U.S.…

We have increased, and will continue to increase, our operations in China. There is inherent risk, based on the complex and changing dynamic between China and the U.S., that political, diplomatic, military, or other events could result in business disruptions, including, but not limited to, increased policy or regulatory enforcement against companies, tariffs, trade embargoes, or export restrictions. Tariffs increase the cost of our products and the components and raw materials that go into making them. These increased costs adversely impact the gross margin that we earn on our products. Tariffs can also make our products more expensive for customers, which could make our products less competitive when compared to those products offered by domestic companies and reduce consumer demand. Countries may also adopt other measures, such as controls on imports or exports of goods, technology, or data, which could adversely impact our operations and supply chain and limit our ability to offer our products and services as designed. These measures can require us to take various actions, including changing suppliers and restructuring business relationships. Changing our operations in accordance with new or changed trade restrictions can be expensive, time-consuming, disruptive to our operations and distracting to management.…

The U.S. federal government has made changes to the U.S. trade policy, including entering into a successor to the North American Free Trade Agreement (“NAFTA”), known as the United States-Mexico-Canada Agreement (“USMCA”), effective as of July 1, 2020. In addition, during 2025, the U.S. federal government imposed new tariffs on imports from various countries including Mexico, Germany, and China, among others. Such tariffs and, if enacted, any further legislation or actions taken by the U.S. federal government that restrict trade, such as additional tariffs, trade barriers, and other protectionist or retaliatory measures taken by governments in other countries, including reciprocal tariffs, limitations on government procurement, or technology export restrictions, could adversely impact our global operations and our ability to sell products and services in our OUS markets. Tariffs could increase the cost of our products and the components and raw materials that go into making them. These increased costs could adversely impact the gross margin that we earn on our products, which could make our products less competitive and reduce consumer demand. Countries may also adopt other protectionist measures that could limit our ability to offer our products and services, which could increase uncertainties and associated risks relating to our global operations.…

In addition, our ability to meet customers’ demands depends, in part, on our ability to timely obtain an adequate delivery of quality materials, parts, and components from our suppliers. An information technology systems interruption, including cyberattacks, could adversely affect the ordering, distribution, and manufacturing processes of our suppliers. Furthermore, the prices of commodities and other materials used in our products, which are often volatile and outside of our control, and may be subject to tariffs, could adversely impact our supply. Current supply chain constraints include difficulties in obtaining a sufficient supply of specific component materials impacted by evolving trade requirements and certain subcontract suppliers being operationally challenged to meet our production requirements. For example, in 2025, the Chinese government announced export controls and licensing requirements applicable to certain products containing Chinese-origin rare earth elements and may implement additional controls in the future. Rare earth elements are critical to certain components contained in our products, and China is a predominant producer of these materials. If implemented in their current or a similar form, these measures may require us to obtain export licenses for certain of our products, and we may further experience supply chain disruptions as a result of limited availability of critical materials and minerals due to the restrictions.…

Additionally, in February 2022, armed conflict escalated between Russia and Ukraine. Russia’s military actions against Ukraine have resulted in substantial expansion of sanction programs imposed by the United States, the EU, and other countries against Russia, Belarus, the Crimea Region of Ukraine, the so-called Donetsk People’s Republic, and the so-called Luhansk People’s Republic. In response, the Russian authorities imposed significant currency control measures, restrictions on transacting with non-Russian parties, export controls, and other economic and financial restrictions. Related sanctions, export controls, or other actions that may be initiated by countries including the U.S., the EU, or Russia (e.g., potential cyberattacks, 41 Table of Contents disruption of energy flows, etc.) could adversely affect the global economy, financial markets, energy supply and prices, certain critical materials and metals, supply chains, and global logistics and could adversely affect our business, financial condition and liquidity, or results of operations.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm｜as_of：2026-02-03
<<<
Trade and Tariffs Update Beginning in 2025, the U.S. implemented a baseline tariff framework on most imports with higher country- and product-specific rates for certain trading partners, including Mexico, Germany, and China, among others, alongside reciprocal measures announced by other jurisdictions. Our disclosure reflects tariffs currently in effect or announced as of the date of this report and assumes such tariffs remain in place, consistent with how we reflect tariff impacts in our financial outlook. We currently manufacture a significant majority of our instruments and accessories in Mexicali, Mexico. Most of these products qualify as originating under the USMCA and, therefore, have not been subject to U.S. import tariffs to date. We also import certain raw materials and finished goods from outside of the U.S. that are subject to tariffs, including our endoscopes, a majority of which are manufactured in Germany. In addition, our operations involve importing certain raw materials from China, importing sub-assemblies to support our local da Vinci Xi surgical system manufacturing in China, and selling U.S.-manufactured da Vinci Xi 63 Table of Contents surgical systems into China. These imports into the U.S. and China are subject to tariffs, which we expect to continue to have an adverse impact on the product cost of our da Vinci Xi surgical system in China.

Some of our suppliers have also incurred incremental tariffs and have passed or may pass on those additional costs to us. These pass-through tariffs and other specific tariff actions against steel and aluminum, critical minerals, semiconductors, and other products have not had a material direct impact on our operations to date, but the long-term effect of these and other existing and future tariff actions is difficult to predict.

In 2025, tariffs and other trade measures have increased our cost of revenues by approximately $63.0 million. Based on the announced and implemented global tariffs as of the date of this report, and assuming such tariffs remain in place, we expect our cost of revenues driven by tariffs and other trade measures to continue to increase in 2026. Future changes to tariff rates and the imposition of new tariffs by the U.S. and/or other countries could result in a material impact to our results of operations. The ultimate impact of changes to tariffs and trade barriers will depend on various factors, including the timing, amount, scope, and nature of any tariffs or trade barriers that are implemented, all of which could have a material adverse effect on our business, financial condition, or results of operations.

During the fourth quarter of 2025, we continued to experience isolated stresses to supply, particularly for specific component materials impacted by evolving trade requirements and at certain subcontract suppliers that were operationally challenged to meet our production requirements. These isolated instances did not have a material impact on our business during the fourth quarter of 2025. As a result of the escalation in tariffs and country-specific trade requirements, including export license controls between major economies, we may experience tariff-related inflation in raw materials costs as well as supply shortages based on shipment delays and the availability of alternative sources of supply for critical materials used in the manufacture of finished products.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
