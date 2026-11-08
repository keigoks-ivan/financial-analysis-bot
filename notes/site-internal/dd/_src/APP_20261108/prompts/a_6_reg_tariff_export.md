你是 stock-analyst v20 DD 的證據採集子 agent。標的：APP。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - APP AppLovin tariff section 232 2026
  - AppLovin export control OR entity list Advertising Agencies 2026
  - APP AppLovin China tariff OR trade restriction 2026
  - Advertising Agencies tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1751008/000175100826000010/app-20251231.htm｜as_of：2026-02-19
<<<
•changes that limit our ability to deliver, target, or measure the effectiveness of advertising, including changes to policies by mobile operating system and third-party platform providers, and the degree to which users opt in or opt out of certain types of ad targeting as a result of changes and controls implemented in connection with such policy changes and with the E.U. General Data Protection Regulation (the "GDPR"), ePrivacy Directive, the California Consumer Privacy Act (the "CCPA") as amended by the California Privacy Rights Act (the "CPRA"), other U.S. state and international privacy laws, data broker laws, and the Children’s Online Privacy Protection Act (the "COPPA"); •decisions by clients to reduce their advertising due to concerns about legal liability or uncertainty regarding their own legal and compliance obligations, or due to negative publicity, regardless of its accuracy, involving us, our data practices, advertising metrics or tools, our advertising solutions, or other companies in our industry; and •the impact of macroeconomic conditions, including tariffs, trade wars, inflation, and high interest rates, political uncertainty and international conflicts around the world, such as in Ukraine and the Middle East, as well as friction between the United States and China, and responses thereto, and seasonality, whether in the advertising industry in general, or among specific types of advertisers or within particular geographies.

A deterioration in macroeconomic conditions, whether in the United States, internationally, or globally, could create uncertainty and adversely affect advertising spending or costs related to our operations. Historically, consumer purchasing and advertising spending have each declined during economic downturns and periods of uncertainty regarding future economic prospects or when disposable income or consumer lending is lower. Uncertain economic conditions may impact advertiser spending in future periods and may also adversely affect our clients, which in turn may harm our business, financial condition, and results of operations. Economic and political relations between the U.S. and other countries continue to evolve rapidly, including with respect to tariff and other policies, and changing policies may adversely affect our business by harming advertising spending or increasing our costs.

Further, we have operations in China and the continuing tension between the U.S. and China may impact our business and results of operations in the future. The U.S. government has restricted the ability to send certain products and technology to China without an export license. In many cases, these licenses are subject to a policy of denial and will not be issued. While our current products are not restricted by these controls, such controls or future restrictions could impact our business in the future. Additionally, the U.S. government also continues to add additional entities in China and other countries to restricted party lists impacting the ability of U.S. companies to engage with these entities. In addition, the Chinese government has retaliated, and may continue to retaliate, to recent changes in U.S. tariffs and export controls in ways that could indirectly impact our business. If 16 Table of Contents we are unable to promptly or properly react to new developments in these and other international regions, our business, financial condition, and results of operations could be adversely affected.

•public health crises, such as the COVID-19 pandemic, which can result in varying impacts to our employees, clients, advertisers, app developers, and business partners internationally; •higher costs associated with doing business internationally, including costs related to local advisors; •export or import regulations; and •trade and tariff restrictions.

Any allegations or violations of the FCPA or other applicable anti-corruption laws could result in whistleblower complaints, adverse media coverage, investigations, loss of export privileges, severe criminal or civil sanctions, suspension or disbarment from U.S. government contracts, substantial diversion of management’s attention, significant legal fees and fines, severe criminal or civil sanctions against us, our officers, or our employees, disgorgement of profits, other sanctions and remedial measures, and prohibitions on the conduct of our business, any of which could adversely affect our reputation, business, financial condition, and results of operations. Responding to any investigation or action will likely result in a significant diversion of management’s attention and resources and significant defense costs and other professional fees.

We are subject to governmental export controls and economic sanctions laws that could impair our ability to compete in global markets or subject us to liability if we violate the controls.

Our advertising solutions may be subject to U.S. export controls, including the Export Administration Regulations. Under these regulations, exports of our products and services as well as the underlying technology may require export authorizations, including by license, a license exception, or other appropriate government authorizations, and the filing of a classification request or self-classification report to use a license exception, as applicable.

Furthermore, our activities are subject to U.S. economic sanctions laws and regulations administered by the U.S. Department of Treasury’s Office of Foreign Assets Control that prohibit transactions with sanctioned parties, including the provision of services and the export of hardware, software, and technology to embargoed jurisdictions or sanctioned parties without the required authorizations. These laws and regulations are rapidly evolving and may be in conflict across international jurisdictions, leading to uncertainty and difficulty in achieving full compliance. Should we violate such existing or similar future laws or regulations, we may be subject to substantial monetary fines or suffer reputational damage and other penalties that could negatively impact our business. If we need to obtain any necessary export licenses or other authorizations for a particular sale, the process may be time-consuming and may result in the delay or loss of opportunities to sell our products.

We take precautions to prevent our products and services and the underlying technology from being provided, deployed or used in violation of export control and sanctions laws and regulations, including implementation of IP address blocking and sanctioned person screening, and continue to evaluate further enhancements to our policies and procedures relating to export control and sanctions compliance. However, we cannot assure you that our policies and procedures relating to export control and sanctions compliance will prevent violations in the future by us or our partners or agents. If we are found to be in violation of sanctions or export control regulations, including failure to obtain appropriate import, export, or re-export licenses or permits, it can result in significant penalties and government investigations, as well as reputational harm and loss of business. Knowing and willful violations can result in possible incarcerations for responsible employees and managers.

In addition to the United States, various other countries regulate the import and export of certain encryption and other technology, including import and export licensing requirements, and have enacted laws that could limit our ability to distribute our products or could limit our clients’ ability to implement our products in those countries. Changes in our advertising solutions, or future changes in export and import regulations may create delays in the introduction of our products and the underlying technology in international markets, prevent our clients with global operations from deploying our products globally, or, in some cases, prevent the export or import of our products to certain countries, governments, or persons altogether. For example, the Chinese government has retaliated, and may continue to retaliate, to recent changes in U.S. tariffs and export controls in ways that could indirectly impact our business. If we are unable to promptly or properly react to new developments in these and other international regions, our business, financial condition, and results of operations could be adversely affected.

Our growth strategy includes further expanding our operations and client base in international markets and acquiring companies that may operate in countries where we do not already do business. Such acquisitions may subject us to additional or expanded export and sanctions regulations. Further, any change in export or import regulations or controls, economic sanctions or related legislation, or change in the countries, governments, persons, or technologies targeted by such regulations, could result in decreased use of our products by, or in our decreased ability to export or sell our products to, existing or potential clients with global operations. Any decreased use of our products or limitation on our ability to export or sell our products in major international markets could adversely affect our business, financial condition, and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
