你是 stock-analyst v20 DD 的證據採集子 agent。標的：ABNB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - ABNB Airbnb tariff section 232 2026
  - Airbnb export control OR entity list Online Travel / Marketplace Platform 2026
  - ABNB Airbnb China tariff OR trade restriction 2026
  - Online Travel / Marketplace Platform tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm｜as_of：2026-02-12
<<<
Macroeconomic conditions, including economic downturns, inflation, tariffs, and currency fluctuations, also influence consumer discretionary spending, which is crucial for our business. Factors like unemployment, consumer debt, and financial market volatility can decrease consumer confidence and spending, particularly affecting leisure travel, which forms a substantial part of our business. Economic downturns have historically reduced travel spending, and future downturns could similarly decrease demand for our platform, leading to lower bookings, increased cancellations, and reduced revenue, thereby materially adversely affecting our business, results of operations, and financial condition.

Our payments platform is subject to various laws, rules, regulations, policies, legal interpretations, and regulatory guidance, including those governing: cross-border and domestic money transmission and funds transfers; stored value and prepaid access; foreign exchange; data privacy, data security, and cybersecurity; banking secrecy; payment services (including payment processing and settlement services); consumer protection; economic and trade sanctions; anti-corruption and anti-bribery; and anti-money laundering (“AML”) and counter-terrorist financing (“CTF”). As we expand further, we face varying and sometimes conflicting legal obligations. For example, certain transactions that may be permissible in one jurisdiction may be prohibited by sanctions, AML, CTF, or other regulations in a different jurisdiction. We regularly assess our compliance programs and may identify gaps requiring costly enhancements to our policies and controls.

We are subject to governmental economic and trade sanctions laws and regulations that limit the scope of our offerings. Additionally, failure to comply with applicable economic and trade sanctions laws and regulations could subject us to liability and negatively affect our business, results of operations, and financial condition.

We must comply with economic and trade sanctions from governments where we operate, including U.S. agencies like the U.S. Treasury Department’s Office of Foreign Assets Control (“OFAC”), the Council of the European Union, the Office of Financial Sanctions Implementation of His Majesty’s Treasury in the United Kingdom (“OFSI”), and Luxembourg's Ministry of Finance. These sanctions restrict transactions or dealings with certain countries, regions, and governments, and certain individuals or entities, such as those operating, organized, or resident in certain countries or regions or those listed on OFAC’s List of Specially Designated Nationals and Blocked Persons. Future sanctions in key business areas could materially impact our business, results of operations, and financial condition.

19 Table of Contents To comply, we maintain and regularly update internal controls and report to OFAC, OFSI, and Luxembourg authorities on blocked or rejected payments and potential violations. These controls do not guarantee that transactions inconsistent with applicable sanctions laws will not occur. Any breaches or investigations could lead to claims or actions against us, affecting our business, results of operations, and financial condition. As we grow and as regulations evolve, we may need to invest further in our internal controls or adjust our operations.

The regulatory and intellectual property frameworks governing the use and protection of AI and ML Technologies and its outputs are rapidly evolving, and we cannot predict how future legislation and regulation will impact our ability to offer and protect products or services that we develop which leverage AI and ML Technologies. Regulators (including data protection regulators) have taken, and are expected to continue to take, an increased interest in issues, such as how we and our vendors collect, maintain, process, and provide transparency on the use of personal data in this context. The increased use of AI and ML Technologies means that regulators are increasingly seeking advance engagement with businesses like ours in respect of certain types of data processing, including our lead EU data protection regulator, the Irish Data Protection Commission. In addition, certain existing legal regimes including those related to data privacy, competition, and consumer protection, may also regulate certain aspects of AI and ML Technologies, and new laws may be adopted and interpreted in ways 24 Table of Contents that would limit our ability to use AI and ML Technologies. This may affect our use of AI and ML Technologies and our ability to provide, improve or commercialize our services effectively and efficiently and result in increased costs.…

Our board of directors has authorized management to repurchase shares of our Class A common stock at management’s discretion. Share repurchases may be made through a variety of methods, which may include open market purchases, privately negotiated transactions, block trades, or accelerated share repurchase transactions or by any combination of such methods. Any such repurchases will be made from time to time subject to market and economic conditions, applicable legal requirements, and other relevant factors. The manner, timing, and amount of any share repurchases may fluctuate and will be determined by us based on a variety of factors, including the market price of our Class A common stock, our priorities for the use of cash to support our business operations and plans, general business and market conditions, tax laws, and alternative investment opportunities, all of which may be further impacted by macroeconomic conditions and factors, including rising interest rates, and inflation, tariffs, global conflicts, and public health crises. Our share repurchase program authorizations do not have an expiration date nor do they obligate us to acquire any specific number or dollar value of shares. Our share repurchase program authorizations may be modified, suspended, or terminated at any time, which may result in a decrease in the trading prices of our Class A common stock.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm｜as_of：2026-02-12
<<<
Macroeconomic and Geopolitical Conditions on our Business As we look forward, we recognize the potential impact of challenging macroeconomic and geopolitical conditions on our business, including inflation, interest rates, foreign currency fluctuations, tariffs and trade controls, and potential decreased consumer spending. To date, these conditions have not had a material impact on our business, results of operations, cash flows, and financial condition; however, the impact in the future of these macroeconomic and geopolitical conditions on our business, results of operations, cash flows, and financial condition is uncertain and will depend on future developments that we may not be able to accurately predict.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABNB_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
