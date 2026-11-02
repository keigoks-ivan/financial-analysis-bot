你是 stock-analyst v20 DD 的證據採集子 agent。標的：HOOD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - HOOD Robinhood Markets tariff section 232 2026
  - Robinhood Markets export control OR entity list Capital Markets / Online Brokerage / Fintech Platform 2026
  - HOOD Robinhood Markets China tariff OR trade restriction 2026
  - Capital Markets / Online Brokerage / Fintech Platform tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm｜as_of：2026-02-18
<<<
As required by the USA Patriot Act and other rules, we have established comprehensive AML, customer identification and transaction surveillance designed to prevent our financial services from being used to facilitate money laundering, terrorist financing, and other illicit activity. Our program is also designed to prevent our products and services from being used to facilitate business in countries, or with persons or entities, included on designated government sanctions lists, including lists promulgated by OFAC, Specially Designated Nationals and Blocked Persons lists, and equivalent foreign lists. Additionally, we have designed and implemented restrictions to prevent certain types of high-risk activity, including account opening fraud, and systems to identify potentially manipulative patterns of trading or higher risk patterns of money movements, and report such activities and transactions, where appropriate. Our AML compliance program includes policies, procedures, reporting protocols, and internal controls, including the designation of AML compliance officers. This program is designed to address these legal and regulatory requirements, while managing risk associated with money laundering and terrorist financing. Anti-money laundering regulations are constantly evolving, thus we actively monitor our compliance with AML rules and regulations and industry standards, and continuously implement policies, procedures, and internal controls in light of current legal requirements.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1783879/000178387926000023/hood-20251231.htm｜as_of：2026-02-18
<<<
Our results of operations are heavily reliant on the level of trading activity on our platforms and Net Deposits. In the past, our results of operations and other operating metrics have fluctuated from quarter to quarter, including due to movements and trends in the underlying markets, changes in general economic conditions, interest in investing, and fluctuations in trading levels generally, each of which is outside our control and will continue to be outside of our control. As a result, period-to-period comparisons of our results of operations might not be meaningful, and our past results of operations should not be relied on as indicators of future performance. Further, we are subject to additional risks and uncertainties that are frequently encountered by companies in rapidly evolving markets. Our financial condition and results of operations in any given quarter can be influenced by numerous factors, including the occurrence of any of the risks described elsewhere in this Risk Factors section, many of which we are unable to predict or are outside of our control.…

A reduction in our liquidity position could reduce our customers’ confidence in us, which could result in the withdrawal of customer assets and loss of customers, or could cause us to fail to satisfy broker-dealer or other regulatory capital guidelines, which may result in immediate suspension of securities activities, regulatory prohibitions against certain business practices, increased regulatory inquiries and reporting requirements, increased costs, fines, penalties or other sanctions, including suspension or expulsion by the SEC, FINRA or other SROs or state regulators, and could ultimately lead to the liquidation of our broker-dealers or other regulated entities. Factors which might adversely affect our liquidity positions include temporary liquidity demands due to timing differences between brokerage transaction settlements and the availability of segregated cash balances, timing differences between cryptocurrency transaction settlements between us and our cryptocurrency Liquidity Providers and between us and our cryptocurrency customers, fluctuations in cash held in customer accounts, a significant increase in our margin lending activities, increased regulatory capital requirements, changes in regulatory guidance or interpretations, other regulatory changes, or a loss of market or customer confidence resulting in unanticipated and/or excessive withdrawals or redemptions, or a suspension of redemptions or withdrawals of customer assets.…

As we are a financial services company, our business, results of operations, and reputation are directly and indirectly affected by elements beyond our control, such as financial market volatility (such as we previously experienced during the COVID-19 pandemic or have experienced and may experience in the future due to trade policy shifts and the imposition or escalation of tariffs implemented by the U.S. and other countries or blocs, including China, Canada, and the EU, and those countries’ or blocs’ responses to such shifts and tariffs), economic and political conditions including unemployment rates, inflation, tax and interest rates, geopolitical conflicts, such as the Russian invasion of Ukraine and ongoing events in the Middle East, significant increases in the volatility or trading volume of particular securities, cryptocurrencies, or Futures (such as we experienced during the meme stock events of early 2021 and the Dogecoin surge of mid-2021), broad trends in business and finance, actual events or concerns involving liquidity, defaults, or non-performance by third-party financial institutions or transactional counterparties (such as the 2023 Banking Events), changes in volume of securities, cryptocurrencies, or Futures trading generally and changes in the markets in which such transactions occur, and changes in how such transactions are processed.…

•the need to offer customer support and other aspects of our offering (including websites, articles, blog posts, and customer support documentation) in various languages or locations; •compliance with anti-bribery and anti-corruption laws, such as the FCPA and equivalent AML and sanctions rules and requirements in local markets, by us, our employees, and our business partners; •the need to recruit and manage staff in new countries and regions to support international operations, and comply with employment law, tax, payroll, and benefits requirements in multiple countries; 44 Table of Contents •the need to enter into new business partnerships with third-party service providers in order to provide products and services in the local market, or to meet regulatory obligations; •varying levels of internet technology adoption and infrastructure, and increased or varying network and hosting service provider costs and differences in technology service delivery in different countries; •fluctuations in currency exchange rates, inflation, and tariffs and trade policy shifts could limit our ability to operate efficiently across or within borders, and the requirements of currency control regulations, which might restrict or prohibit conversion of other currencies into U.S. dollars; •double taxation of our international earnings and potentially adverse tax consequences due to requirements of or changes in the income and other tax laws of the U.S.…

We are subject to a wide variety of local, state, federal, and international laws, regulations, licensing schemes, and industry standards in the U.S., the U.K., the EU, the United Arab Emirates, Singapore, the British Virgin Islands, and in other countries and regions in which we operate. These laws, regulations, and standards govern numerous areas that are important to our business, and include, or might in the future include, those relating to all aspects of financial services, the securities and futures markets, investment advisory, investment companies, money transmission, the origination, marketing, servicing, and collection of consumer debt, foreign exchange, payments services and products (such as payment processing, settlement services, and credit cards), cryptocurrency (including crypto-asset perpetuals), derivatives, trading in shares and fractional shares, fraud detection, consumer protection, AML, escheatment, sanctions regimes and export controls, data privacy, data protection, data security, as well as climate risk and environmental impact, including with respect to disclosure of GHG emissions and other metrics related to climate change.

51 Table of Contents We are required to comply with U.S. economic and trade sanctions administered by OFAC and we have processes in place to facilitate compliance with OFAC regulations. As part of our customer onboarding process, in accordance with the CIP rules under Section 326 of the USA Patriot Act, we screen all potential customers against OFAC watchlists and continue to screen all customers, vendors and employees daily against OFAC watchlists. Although our application includes features designed to block access to our services from sanctioned countries, if our services are accessed from a sanctioned country in violation of trade and economic sanctions, we could be subject to enforcement actions.

Additionally, allowing customers to deposit and withdraw cryptocurrencies to and from our platforms increases the risk that our platforms might be exploited to facilitate illegal activity such as fraud, gambling, money laundering, tax evasion, and scams. Crypto Transfers, Robinhood Wallet, and Robinhood Connect also expose us to heightened risks related to potential violations of trade sanctions, including OFAC regulations, and AML and counter-terrorist financing laws, which among other things impose strict liability 79 Table of Contents for transacting with prohibited persons. We engage blockchain analytics vendors to help determine whether the external wallets involved in Crypto Transfers are controlled by persons on prohibited lists or involved in fraudulent or illegal activity. However, fraudulent and illegal transactions and prohibited status could be difficult or impossible for us and our vendors to detect in some circumstances. The use of our platforms for illegal or improper purposes could subject us to claims, individual and class action lawsuits, and government and regulatory investigations, prosecutions, enforcement actions, inquiries, or requests that could result in significant liabilities and reputational harm for us and could cause cryptocurrency trading volumes and transaction-based revenues to decline.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/parts/axes_4.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
