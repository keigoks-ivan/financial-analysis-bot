你是 stock-analyst v20 DD 的證據採集子 agent。標的：COIN。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - COIN Coinbase Global tariff section 232 2026
  - Coinbase Global export control OR entity list Financial Data & Stock Exchanges 2026
  - COIN Coinbase Global China tariff OR trade restriction 2026
  - Financial Data & Stock Exchanges tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm｜as_of：2026-02-12
<<<
Anti-money laundering and counter-terrorist financing We are subject to various anti-money laundering and counter-terrorist financing laws, including the Bank Secrecy Act (the “BSA”) in the United States, and similar laws and regulations abroad. In the United States, as a money services business registered with the Financial Crimes Enforcement Network (“FinCEN”), we are required under the BSA to among other things, develop, implement, and maintain a risk-based anti-money laundering program, provide an anti-money laundering-related training program, report suspicious activities and transactions to FinCEN, comply with certain reporting and recordkeeping requirements, and collect and maintain information about our customers. In addition, the BSA requires us to comply with certain customer due diligence requirements as part of our anti-money laundering obligations, including developing risk-based policies, procedures, and internal controls reasonably designed to verify a customer’s identity. Many states and other countries impose similar and, in some 15 Table of Contents cases, more stringent requirements related to anti-money laundering and counter-terrorist financing. Our compliance program is designed to prevent and detect instances of money laundering, terrorist financing, and other illicit activity on our platform. It is also designed to prohibit the use of Coinbase in sanctioned jurisdictions, or by sanctioned persons or entities, as determined by the Office of Foreign Assets Control (“OFAC”), and equivalent foreign authorities.…

For a description of the risks we may face from (i) unauthorized or impermissible customer access to our products and services outside of jurisdictions where we have determined to make such products and services available or (ii) an assertion of jurisdiction over our operations or the crypto assets we offer by U.S. and foreign regulators and other government entities, see the following risk factors in the section titled “Risk Factors” in Part I, Item 1A of this Annual Report on Form 10-K: (i) “We are subject to an extensive, highly-evolving and uncertain regulatory landscape and any adverse changes to, or our failure to comply with, any laws and regulations could adversely affect our brand, reputation, business, operating results, and financial condition”; (ii) “As we continue to expand and localize our international activities, our obligations to comply with the laws, rules, regulations, and policies of a variety of jurisdictions will increase and we may be subject to inquiries, investigations, and enforcement actions by U.S. and non-U.S.…

Anti-corruption, economic and trade sanctions and export controls We are subject to anti-corruption and economic and trade sanctions laws and regulations in the United States and other jurisdictions in which we operate. Anti-corruption laws, such as the Foreign Corrupt Practices Act in the United States and the Bribery Act 2010 in the United Kingdom (the “Bribery Act”), generally prohibit companies and those acting on their behalf from making improper payments to foreign government officials and political figures for the purpose of obtaining or retaining business or to gain an unfair business advantage. Some of these laws, such as the Bribery Act, also prohibit improper payments between private entities and persons. Economic and trade sanctions programs that are administered by the U.S. Department of the Treasury’s OFAC and equivalent applicable foreign authorities prohibit or restrict transactions to or from, or dealings with or involving, certain countries, regions, governments, and in certain circumstances, specified individuals and entities such as narcotics traffickers, terrorists, and terrorist organizations, as well as certain digital currency addresses owned by the foregoing. We are also required to comply with export control laws and regulations administered by the United States and other applicable jurisdictions, including those administered by the U.S. Department of Commerce’s Bureau of Industry and Security.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm｜as_of：2026-02-12
<<<
Due to the highly volatile nature of prices of crypto assets, our operating results have, and will continue to, fluctuate significantly from quarter to quarter in accordance with market sentiments and movements in the broader onchain economy. Our operating results will continue to fluctuate significantly as a result of a variety of factors, many of which are unpredictable and in certain instances are outside of our control, including: •crypto asset trading activity, including trading volume and the prevailing trading prices for crypto assets, which can be highly volatile; •our ability to attract, maintain, grow, and engage our customer and developer base; •changes in the legislative or regulatory environment, or actions by U.S. or foreign governments or regulators, including fines, orders, or consent decrees; •regulatory changes or scrutiny that impact our ability to offer certain products or services; •our ability to continue to diversify and grow our subscription and services revenue, including our stablecoin revenue; •our mix of revenue between transaction and subscription and services; •pricing for, or temporary suspensions of, our products and services; •adding crypto assets to, or removing from, our platform; •our ability to establish and maintain partnerships, collaborations, joint ventures, or strategic alliances with third parties; •fluctuations in the market values of our marketable and strategic investments; •market conditions of, and overall sentiment towards, crypto; •macroeconomic conditions,…

As we continue to expand and localize our international activities, our obligations to comply with the laws, rules, regulations, and policies of a variety of jurisdictions will increase and we may be subject to inquiries, investigations, and enforcement actions by U.S. and non-U.S. regulators and governmental authorities, including those related to sanctions, export control, and anti-money laundering.

As we expand and localize our international activities, we have become increasingly obligated to comply with the laws, rules, regulations, policies, and legal interpretations of both the jurisdictions in which we operate and those into which we offer services on a cross-border basis. For instance, financial regulators outside the United States have increased their scrutiny of crypto asset exchanges over time, 33 Table of Contents such as by requiring crypto asset exchanges operating in their local jurisdictions to be regulated and licensed under local laws. Moreover, laws regulating financial services, the internet, mobile technologies, crypto, AI, and related technologies outside of the United States are highly evolving, extensive and often impose different, more specific, or even conflicting obligations on us, as well as broader liability. In addition, we are required to comply with laws and regulations related to economic sanctions and export controls enforced by the U.S. Department of the Treasury’s Office of Foreign Assets Control (“OFAC”) and the U.S. Department of Commerce’s Bureau of Industry and Security, and U.S. anti-money laundering and counter-terrorist financing laws and regulations, enforced by FinCEN and certain state financial services regulators. U.S. sanctions and export control laws and regulations generally restrict dealings by persons subject to U.S.…

If an applicable regulatory authority or a court, in either case having final determinative authority on the topic, were to determine that a supported crypto asset, product or service currently offered, sold, or traded on our platform is a security, we would not be able to offer such crypto asset for trading, or product or service on our platform, until we are able to do so in a compliant manner. A determination by the SEC, a state or foreign regulatory authority, or a court that an asset that we currently support for trading on our platform, or product or service that we offer on our platform, constitutes a security may result in us removing that crypto asset from or ceasing to offer that product or service on our platform, and may also result in us determining that it is advisable to remove assets from our platform, or to cease offering products and services on our platform, that have similar characteristics to the asset, product or service that was alleged or determined to be a security.…

We have and may in the future experience employee or service provider misconduct. Employee or service provider misconduct or error could subject us to legal liability, financial losses, and regulatory sanctions and could seriously harm our reputation and negatively affect our business. Such misconduct could include engaging in improper or unauthorized transactions or activities, misappropriation of customer funds, insider trading and misappropriation of information, failing to supervise other employees or service providers, improperly using confidential information, as well as improper trading activity such as spoofing, layering, wash trading, manipulation and front-running. Employee or service provider errors, including mistakes in executing, recording, or processing transactions for customers, could expose us to the risk of material losses even if the errors are detected. Although we have implemented processes and procedures and provide trainings to our employees and service providers to reduce the likelihood of misconduct and error, these efforts may not be successful. Moreover, the risk of employee or service provider error or misconduct may be even greater for novel products and services and is compounded by the fact that many of our employees and service providers are accustomed to working at tech companies which generally do not maintain the same compliance customs and rules as financial services firms.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/parts/axes_4.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
