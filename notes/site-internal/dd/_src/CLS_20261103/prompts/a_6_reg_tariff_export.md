你是 stock-analyst v20 DD 的證據採集子 agent。標的：CLS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - CLS Celestica tariff section 232 2026
  - Celestica export control OR entity list Electronic Components 2026
  - CLS Celestica China tariff OR trade restriction 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
Our customers typically do not commit to long-term production schedules in advance, and we may experience volatility in customer orders and inventory levels. Customers have and may in the future terminate their agreements with us prior to scheduled expiration, fail to renew such agreements upon expiration, or significantly change, reduce or delay the volume of manufacturing or other services they order from us, any of which may adversely affect our operating results when they occur. Customers have and may also shift business to our competitors, implement in-source and second-source programs, or adjust the concentration of their supplier base. The global economic environment, adverse market conditions, "buy local" movements, political and geopolitical pressures, negative sentiment from our customers' customers, regulatory changes or changes made by local governments (such as tax benefits, tariffs or export controls) have and may continue to impact our customers' business decisions. See "Our operations have been and could continue to be adversely affected by events outside our control" and "Adoption, integration and use of AI in manufacturing and service offerings and in certain of our internal processes may present regulatory, ethical, data and cybersecurity risks and result in reputational harm or liabilities." These and other factors could adversely affect the rate of outsourcing to EMS and/or ODM providers generally or to us in particular.…

The competitive environment in our industry is intense and aggressive pricing is a common business dynamic. Some of our competitors have greater scale and offer a broader range of services. Additionally, our current and/or future competitors may: be more effective than we are in increasing or shifting their presence in new lower-cost, lower-tariff or tariff-free regions to try to offset continuous competitive pressure and increasing labor costs or to secure new business; develop or acquire services comparable or superior to ours; consolidate to form larger competitors; have greater name recognition, critical mass and/or geographic market presence; have greater manufacturing, R&D and/or marketing resources; be better able to take advantage of acquisition opportunities; be willing to, or able to make sales or provide services at lower margins than we do; or adapt more quickly than we do to new technologies, evolving industry trends and changing customer requirements. In addition, our competitors may be more effective than we are in investing in IT solutions to differentiate their offerings. Some of our 27 competitors have increased their vertical capabilities by manufacturing modules or components used in the products they assemble. Although we have also expanded our capabilities, including through acquisitions and "operate-in-place" arrangements, our competitors' expansion efforts may be more successful than ours.…

•global currency fluctuations. Any of the foregoing risks could disrupt the supply of our components or materials, slow or stop our production, and/or increase our costs. Although in the past we have incurred some increased shipping expenses and delays in connection with geopolitical conflicts, such increases and delays have not been significant to date. However, there can be no assurance that this will continue to be the case. Compliance with trade and foreign tax laws may increase our costs and actual or alleged violations of such laws could result in enforcement actions or financial penalties that could result in substantial costs. Furthermore, U.S. export control laws and economic sanctions prohibit the shipment of certain products to U.S. embargoed or sanctioned countries, governments, and persons. Even though we take precautions to ensure that our channel partners comply with all relevant regulations, any failure by our channel partners to comply with such regulations could have negative consequences for us, including reputational harm, government investigations, and penalties. In addition, the introduction or expansion of certain social programs in foreign jurisdictions may increase our costs, and certain supplier's costs, of doing business.

In addition, international trade disputes with China have resulted in increased tariffs and other measures that have, and may continue to, adversely affect the Company's business. Our Capital Equipment business and our CCS segment have been in prior periods and may continue to be negatively impacted by U.S. technology/data export controls, including controls on cross-border technology/data access, with respect to China and other countries, and China's policy supporting its private sector businesses. More generally, changes to, among other things, laws or policies in the U.S. regarding foreign trade, import/export duties and controls, tariffs or taxes, manufacturing and/or investments, or other events outside of our control, could materially adversely affect our U.S. and foreign operations. See "U.S. policies or legislation could have a material adverse effect on our business, results of operations and financial condition," and "Our operations have been and could continue to be adversely affected by events outside our control."

The policies and legislation of the U.S. administration have created, and may continue to create, uncertainty regarding trade agreements and free trade generally, and have resulted in and may result in further significant new increases in country‑specific "reciprocal" tariffs on goods imported into the U.S. from specified countries, certain of which have imposed, and may continue to impose, retaliatory tariffs and non‑tariff measures. These actions, and/or other governmental actions related to tariffs or international trade agreements, have in the past increased (and could further increase) the cost to our U.S. customers who use our non-U.S. manufacturing sites and components, and vice versa, which may materially and adversely impact demand for our services, our results of operations or our financial condition.

In addition, the U.S. government has imposed and may continue to impose additional export controls, including on certain advanced computing semiconductor chips, integrated circuits, semiconductor manufacturing items and related transactions and controls on cross-border technology/data access with respect to China and other countries. The implementation, interpretation, timing and impact on our business of these rules and other regulatory actions taken by the U.S. government is uncertain and evolving. These actions have adversely impacted and continue to adversely impact our Capital Equipment business and our CCS segment. The future adverse impact of these and/or other actions taken by the governments of either the U.S. or China, or both, or other governments (including in response to continuing tensions), could be material.

Given the uncertainty regarding the scope and duration of these (or further) trade and export actions, whether trade tensions will escalate further, and whether our customers will continue to bear the cost of the tariffs and/or avoid such costs by insourcing or shifting business to other providers, their impact on the demand for our services, our operations and results for future periods cannot be currently quantified, but may be material.

We provide engineering and manufacturing related services to our customers in the A&D business. As part of these services, we are subject to substantial regulation from government agencies including the U.S. Department of Defense (DOD) and the U.S. Federal Aviation Administration. Our A&D sites are certified in quality management standards applicable to the A&D industry. Failure to comply with these regulations or the loss of any of our quality management certifications may result in fines, penalties and injunctions, and could prevent us from executing on current or winning future contracts, any of which may materially adversely affect our financial condition and operating results. In addition to quality management standards, there are several other U.S. regulations with which we are required to comply, including the Federal Acquisition Regulations, which provides uniform policies and procedures for acquisition; the Defense Federal Acquisition Regulation Supplement, a DOD agency supplement to the FAR that provides DOD-specific acquisition regulations that DOD government acquisition officials, and those contractors doing business with DOD, must comply with in the procurement process for goods and services; and the Truth in Negotiations Act, which requires full and fair disclosure by contractors in the conduct of negotiations with the government and its prime contractors.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1030894/000103089426000011/cls-20251231.htm｜as_of：2026-02-27
<<<
Governmental actions related to international trade agreements have increased (and could further increase) the cost to our U.S. customers who use our non-U.S. manufacturing sites and components, and vice versa, which may materially and adversely impact demand for our services, our results of operations or our financial condition. Changes in policies by the U.S. or other governments could negatively affect our operating results due to changes in duties, tariffs, or taxes, or limitations on currency or fund transfers, as well as government-imposed restrictions on producing certain products in, or shipping them to, specific countries, or as the result of other similar actions by other countries or citizens affected by such changes in policies. Our Capital Equipment business and our CCS segment have been in prior periods and may continue to be negatively impacted by U.S. technology/data export controls, including controls on cross-border technology/data access, with respect to China and other countries, and China's policy supporting its private sector businesses. We have increased the resilience of our global network to manage this dynamic. However, given the uncertainty regarding the scope and duration of these or further trade actions and whether trade tensions will escalate further, their impact on the demand for our services, our operations and results for future periods cannot be currently quantified, but may be material.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
