你是 stock-analyst v20 DD 的證據採集子 agent。標的：PLTR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - PLTR Palantir Technologies tariff section 232 2026
  - Palantir Technologies export control OR entity list Software - Infrastructure 2026
  - PLTR Palantir Technologies China tariff OR trade restriction 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm｜as_of：2026-02-17
<<<
Our results of operations depend on sales to enterprise customers, which make product purchasing decisions based in part or entirely on factors, or perceived factors, not directly related to the features of the platforms, including, among others, that customer’s projections of business growth, uncertainty about macroeconomic conditions (including as a result of the ongoing Russia-Ukraine conflict and related economic sanctions, the conflict resulting from Hamas’ attack on Israel and the ongoing conflict in the Middle East, fluctuating interest rates, monetary policy changes, foreign currency fluctuations, or the potential or actual imposition of tariffs or other impacts on trade relations), capital budgets, anticipated cost savings from the implementation of our platforms, potential preference for such customer’s internally-developed software solutions, perceptions about our business and platforms, more favorable terms offered by potential competitors, and previous technology investments. In addition, certain decision makers and other stakeholders within our potential customers tend to have vested interests in the continued use of internally developed or existing software, which may make it more difficult for us to sell our platforms and services.…

The market for our platforms is rapidly evolving. Our future success will depend in large part on the growth and expansion of this market, which is difficult to predict and relies on a number of factors, including customer adoption, customer demand, changing customer needs, the entry of competitive products, the success of existing competitive products, potential customers’ willingness to adopt an alternative approach to data collection, storage, and processing and their willingness to invest in new software after significant prior investments in legacy data collection, storage, and processing software. The estimates and assumptions that are used to calculate our market opportunity are subject to change over time, and there is no guarantee that any particular number or percentage of the organizations covered by our market opportunity estimates will pay for our platforms and services at all or generate any particular level of revenue for us. Even if the market in which we compete meets the size estimates and growth forecasts, our business could fail to grow at the levels we expect or at all for a variety of reasons outside our control, including competition in our industry.…

Compliance with laws and regulations applicable to our non-U.S. operations increases our cost of doing business in foreign jurisdictions. We may be unable to keep current with changes in foreign government requirements and laws as they change from time to time. Failure to comply with these regulations could subject us to investigations, sanctions, enforcement actions, disgorgement of profits, fines, damages, civil and criminal penalties, injunctions, or other collateral consequences. In many foreign countries, it is common for others to engage in business practices that are prohibited by our internal policies and procedures or U.S. regulations applicable to us. In addition, although we have implemented policies and procedures designed to ensure compliance with these laws and policies, there can be no assurance that all of our employees, contractors, partners, and agents will comply with these laws and policies. Violations of laws or key control policies by our employees, contractors, partners, or agents could result in delays in revenue recognition, financial reporting misstatements, governmental sanctions, fines, penalties, or the prohibition of the importation or exportation of our platforms. In addition, responding to any action may result in a significant diversion of management’s attention and resources and an increase in professional fees.…

Our offerings are subject to U.S. export controls, and we incorporate encryption technology into certain of our offerings. Our controlled software offerings and the underlying technology may be exported outside of the United States only with the required export authorizations, which may include license requirements in some circumstances. Additionally, our current or future products may be classified under the Commerce Department Export Administration Regulations (“EAR”) or as defense articles subject to the United States International Traffic in Arms Regulations (“ITAR”). Most of our products, including our core software platforms, have been classified under the EAR and are generally exportable without needing a specific license, under an EAR exception for encrypted software. If a product, or component of a product, is classified under the ITAR, or is ineligible for the EAR encryption exception, then those products could be exported outside the United States only if we obtain the applicable export license or qualify for a different license exemption or exception. In certain contexts, the services we 44 Table of Contents provide might be classified as defense services subject to the ITAR separately from the products we provide.…

Furthermore, our activities are subject to the economic sanctions, laws and regulations of the United States and other jurisdictions. Such controls prohibit the shipment or transfer of certain products and services without the required export authorizations or export to countries, governments, and persons targeted by applicable sanctions. We take precautions to prevent our offerings from being exported in violation of these laws, including: (i) seeking to proactively classify our platforms and obtain authorizations for the export and/or import of our platforms where appropriate, (ii) implementing certain technical controls and screening practices to reduce the risk of violations, and (iii) requiring compliance with U.S. export control and sanctions obligations in customer and vendor contracts. However, we cannot guarantee the precautions we take will prevent violations of export control and sanctions laws.

As discussed above, if we misclassify a product or service, export or provide access to a product or service in violation of applicable restrictions, or otherwise fail to comply with export regulations, we may be denied export privileges or subjected to significant per violation fines or other penalties, and our platforms may be denied entry into other countries. Any decreased use of our platforms or limitation on our ability to export or sell our platforms would likely adversely affect our business, results of operations and financial condition. Violations of U.S. sanctions or export control laws can result in fines or penalties, including civil penalties of over $300,000 or twice the value of the transaction, whichever is greater, per EAR violation and a civil penalty of over $1,000,000 or twice the value of the transaction, whichever is greater, per ITAR violation. In the event of criminal knowing and willful violations of these laws, fines of up to $1,000,000 per violation and possible incarceration for responsible employees and managers could be imposed.

We also note that if we or our business partners or counterparties, including licensors and licensees, prime contractors, subcontractors, sublicensors, vendors, customers, shipping partners, or contractors, fail to obtain appropriate import, export, or re-export licenses or permits, notwithstanding regulatory requirements or contractual commitments to do so, or if we fail to secure such contractual commitments where necessary, we may also be adversely affected, through reputational harm as well as other negative consequences, including government investigations and penalties. For instance, violations of U.S. sanctions or export control laws can result in fines or penalties, including significant civil and criminal penalties per violation, depending on the circumstances of the violation or violations.

Negative consequences for violations or apparent violations of trade control requirements may include the absolute loss of the right to sell our platforms or services to the government of the United States, or to other public bodies, or a reduction in our ability to compete for such sales opportunities. Further, complying with export control and sanctions regulations for a particular sale may be time-consuming and may result in the delay or loss of sales opportunities.

Also, various countries, in addition to the United States, regulate the import and export of certain encryption and other technology, including import and export permitting and licensing requirements, and have enacted laws that could limit our ability to distribute our platforms or could limit our customers’ abilities to implement our platforms in those countries. For example, following Russia’s invasion of Ukraine, and as the conflict has continued, the United States and other countries have imposed economic sanctions and severe export control restrictions against Russia, Belarus, and certain regions of Ukraine, and the United States and other countries could continue to impose wider sanctions and export restrictions and take other actions should the conflict further escalate. Any new export restrictions, new legislation, changes in economic sanctions, or shifting approaches in the enforcement or scope of existing regulations, or in the countries, persons, or technologies targeted by such regulations, could result in decreased use of our platforms by existing customers with non-U.S. operations, declining adoption of our platforms by new customers with non-U.S. operations, limitation of our expansion into new markets, and decreased revenue.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLTR_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
