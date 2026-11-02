你是 stock-analyst v20 DD 的證據採集子 agent。標的：PYPL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - PYPL PayPal Holdings tariff section 232 2026
  - PayPal Holdings export control OR entity list Credit Services 2026
  - PYPL PayPal Holdings China tariff OR trade restriction 2026
  - Credit Services tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm｜as_of：2026-02-03
<<<
Anti-money laundering, counter-terrorist financing, and sanctions. PayPal is subject to anti-money laundering (“AML”) laws and regulations in the U.S. and other jurisdictions, as well as laws designed to prevent the use of the financial systems to facilitate terrorist activities. Our AML program is designed to prevent our payments platform from being used to facilitate money laundering, terrorist financing, and other illicit activities, or to do business in countries or with persons and entities included on designated country or person lists promulgated by the U.S. Department of the Treasury’s Office of Foreign Assets Control and equivalent authorities in other countries. Our AML and sanctions compliance programs, which are overseen by our AML/Bank Secrecy Act Officer, are composed of policies, procedures, and internal controls, and are designed to address these legal and regulatory requirements and assist in managing money laundering and terrorist financing risks.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm｜as_of：2026-02-03
<<<
Anti-Money Laundering and Counter-Terrorist Financing; Economic and Trade Sanctions Regulators globally continue to increase standards and expectations regarding anti-money laundering and counter-terrorist financing, and to expand the scope of existing laws and regulations to emerging products and markets, which may require us to revise or expand our compliance program globally and/or in specific jurisdictions, including the procedures we use to verify the identity of our customers and to monitor international and domestic transactions. Such changes could increase the costs and complexity of compliance, lead to increased friction for customers, and result in a decrease in business. Regulators regularly re-examine the transaction volume thresholds at which we must obtain and keep applicable records or the circumstances in which we must verify identities of customers, and any change to such obligations could result in greater compliance costs and negatively impact our business. We are also required to comply with economic and trade sanctions administered by the U.S., the European Union (“EU”) and its member states, the U.K., and other jurisdictions in which we operate. Non-compliance with anti-money laundering laws and regulations or economic and trade sanctions may subject us to significant fines, penalties, lawsuits, and enforcement actions, result in regulatory sanctions and additional compliance requirements, increase regulatory scrutiny of our business, restrict our operations, and damage our reputation and brands.…

We are regularly subject to claims, individual and class action lawsuits, arbitration proceedings, government and regulatory investigations, inquiries, actions or requests, and other proceedings alleging violations of laws, rules, and regulations with respect to competition, antitrust, intellectual property, privacy, data protection, information security, anti-money laundering, counter-terrorist financing, sanctions, anti-bribery, anti-corruption, consumer protection (including unfair, deceptive, or abusive acts or practices), the terms of our customer agreements, fraud, accessibility, securities, tax, labor and employment, commercial disputes, services, charitable fundraising, contract disputes, escheatment of unclaimed or abandoned property, product liability, use of our services for illegal purposes, the matters described in “Note 13—Commitments and Contingencies—Litigation and Regulatory Matters—General Matters” to our consolidated financial statements, and other matters. We expect that the number and significance of these disputes and inquiries will continue to increase as our products, services, and business expand in complexity, scale, scope, and geographic reach, including through acquisitions of businesses and technology, and as a result of expanded enforcement of certain existing laws and regulations by federal, state and local agencies. For example, there continues to be enforcement activity in connection with federal and state consumer protection laws, including suits which seek civil penalties.…

Cross-border trade (i.e., transactions where the merchant and consumer are in different countries) is an important source of our revenues and profits. Cross-border transactions generally provide higher revenues and operating income than similar transactions that take place within a single country or market. In certain markets, cross-border trade may represent our primary or sole offering. Cross-border trade has been and may be negatively impacted by various factors including foreign exchange rate fluctuations; changes in or new tariffs, trade disputes, barriers or restrictions threats of such actions, and the related uncertainty thereof; sanctions; import or export controls; and the interpretation and application of laws of multiple jurisdictions in the context of cross-border trade and foreign exchange. Any factors that increase the costs or uncertainty of cross-border trade for us or our customers or that restrict, delay, or make cross-border trade more expensive, difficult or impractical could reduce our cross-border transactions and volume, negatively impact our revenues and profits, and harm our business.

Our international operations generate a significant portion of our net revenues and subject us to significant challenges, uncertainties, and risks, including, but not limited to, local regulatory, licensing, reporting, and legal obligations; costs and challenges associated with operating in markets in which we may have limited or no experience, including adapting our products and services to local requirements and customer preferences; difficulties in developing, staffing, and simultaneously managing a large number of varying foreign operations as a result of distance, language, and cultural differences and varying laws, regulations, and customs; differing employment practices and the existence of works councils; difficulties in hiring, retaining and integrating qualified employees and maintaining our company culture; fluctuations in foreign exchange rates; exchange control regulations; profit repatriation restrictions; changes in or new tariffs, sanctions, fines, or other trade barriers or restrictions and the related uncertainty thereof; import or export regulations; compliance with U.S. and foreign anti-bribery, anti-corruption, sanctions, anti-money laundering and counter-terrorist financing laws and regulations; the interpretation and application of laws of multiple jurisdictions; and national or regional political, economic, or social instability. In addition, some countries have enacted or are considering data localization or residency laws, which require that certain data be maintained, stored and/or processed within their country of origin.…

Global and regional economic conditions could harm our business. Adverse global and regional economic conditions such as political unrest and turmoil affecting the banking system or financial markets, including, but not limited to, tightening in the credit markets, extreme volatility or distress in the financial markets (including the fixed income, credit, currency, equity, and commodity markets), unemployment, consumer debt levels, recessionary or inflationary pressures, supply chain issues, reduced consumer confidence or economic activity, government fiscal, monetary and tax policies, U.S. and international trade relationships, agreements, treaties, changes in or new tariffs and restrictive actions or threats of such actions, including an escalation of trade tensions between the U.S. and its trading partners, the inability of a government to enact a budget in a fiscal year, government shutdowns, government austerity programs, geopolitical conditions or events, and other negative financial news or macroeconomic developments could have a material adverse impact on the demand for our products and services, including a reduction in the volume and size of transactions on our platform. In particular, recent tariffs and reciprocal trade measures enacted or threatened to be enacted by the U.S. and other countries have led to increased volatility and uncertainty in certain parts of the global economy.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm｜as_of：2026-02-03
<<<
MACROECONOMIC ENVIRONMENT A deterioration in macroeconomic conditions resulting from uncertainties and effects from tariffs, inflation, international conflicts, and interest rates could continue to increase the risk of lower consumer spending, merchant and consumer bankruptcy, insolvency, business failure, higher credit losses, foreign exchange fluctuations, or other business interruption, which may adversely impact our business. We are unable to reasonably estimate the total potential impact on our financial results that may ultimately result from such changes in the macroeconomic environment.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
