你是 stock-analyst v20 DD 的證據採集子 agent。標的：FICO。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - FICO Fair Isaac tariff section 232 2026
  - Fair Isaac export control OR entity list Software - Application 2026
  - FICO Fair Isaac China tariff OR trade restriction 2026
  - Software - Application tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-06）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm｜as_of：2026-11-06
<<<
•Laws and regulations restricting transactions with sanctioned parties and regarding export controls as they apply to FICO products delivered in non-U.S. countries or to foreign nationals (e.g., Office of Foreign Asset Control sanctions and Export Administration Regulations).
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-06）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/814547/000081454726000042/fico-20260930.htm｜as_of：2026-11-06
<<<
In addition, the U.S. and other key international economies periodically experience economic downturns and periods of heightened uncertainty, which may result in reduced demand for goods and services, increased volatility of interest rates, fluctuating rates of inflation, geopolitical tensions, restricted credit, poor liquidity, reduced corporate profitability, volatility in credit, trade policies and tariffs, equity and foreign exchange markets, bankruptcies, and overall uncertainty with respect to the economy. The potential for economic disruption presents considerable risks to our business, including potential bankruptcies or credit deterioration of financial institutions with which we have substantial relationships. Economic disruption could adversely affect demand for our products and services, resulting in a decline in the sales of new products to our customers and a reduction in transaction volumes from existing customers. In addition, the volume of our Scores sales depends heavily on macroeconomic conditions in the markets in which our customers operate. For example, the volume of transactions in the U.S. mortgage and credit card markets, which account for a significant portion of the revenues in our Scores segment, may be adversely affected by economic conditions.

During fiscal 2026, 92% of our revenues were derived from sales of products and services to the banking industry. Periods of global economic uncertainty historically have produced substantial stress, volatility, illiquidity, and disruption of global credit and other financial markets, including the bankruptcy, acquisition, or government assistance related to certain major domestic and international financial institutions. The potential for future stress and disruptions, including in connection with geopolitical tensions, military conflicts, trade policies and tariffs, inflationary pressures, and interest rate volatility, presents considerable risks to our businesses and operations. These risks include potential bankruptcies or credit deterioration of financial institutions, many of which are our customers. Such disruption would result in a decline in the revenue we receive from financial and other institutions. In addition, if consumer demand for financial services and products and the number of credit applications decrease, including due to interest rate changes or other factors, the demand for our products and services could also be materially reduced. These types of disruptions could lead to a decline in the volumes of products and services we provide our customers and could negatively impact our revenue and results of operations.

•Laws and regulations restricting transactions with sanctioned parties and regarding export controls as they apply to FICO products delivered in non-U.S. countries or to foreign nationals (e.g., Office of Foreign Asset Control sanctions and Export Administration Regulations); •Anti-bribery and corruption laws and regulations (e.g., the Foreign Corrupt Practices Act and the UK Bribery Act 2010); •Financial regulatory standards (e.g., Sarbanes-Oxley Act requirements to maintain and verify internal process controls, including controls for material event awareness and notification); •Laws and regulations that apply to the management or oversight of third parties (e.g., vendors, contractors, suppliers, and distributors); and •Laws and regulations relating to the environmental, social, and sustainability practices of companies, including enhanced climate-related disclosure requirements from regulators, such as California’s climate disclosure rules and the E.U.’s Corporate Sustainability Reporting Directive.

A large portion of our revenues is derived from international sales. During fiscal 2026, 20% of our revenues was derived from business outside the U.S. As part of our growth strategy, we plan to continue to pursue opportunities outside the U.S., including opportunities in countries with economic systems that are in early stages of development and that may not mature sufficiently to result in growth for our business. Accordingly, our future operating results could be negatively affected by a variety of factors arising out of international commerce, some of which are beyond our control. These factors include: •general economic and political conditions in countries where we sell our products and services; •difficulty in staffing and efficiently managing our operations in multiple geographic locations and in various countries; •effects of a variety of foreign laws and regulations, including restrictions on access to personal information; •data privacy, consumer protection, and AI laws and regulations; •import and export licensing requirements; •longer payment cycles; •difficulties in enforcing contracts and collecting accounts receivable; •reduced protection for intellectual property rights; •currency fluctuations; •unfavorable tax rules or rulings; •changes in tariffs and other trade barriers; •the presence and acceptance of varying levels of business corruption in international markets; •geopolitical tensions, instability, terrorism, and military conflicts; •natural disasters and pandemics, including individual countries’ reactions to them; and •difficulties…

Purchases of technology products and services and decisioning solutions are subject to adverse economic conditions. During periods of economic weakness, companies across many industries delay or reduce technology purchases, and we may experience softened demand for our decisioning solutions and other products and services. Global economic uncertainty has resulted in, and continues to contribute to, substantial stress, volatility, illiquidity, and disruption of global credit and other financial markets. Various factors contribute to the uncertain economic environment, including geopolitical tensions, military conflicts, interest rate levels and volatility, inflation, actual or anticipated recessions, trade policies and tariffs, and political and governmental instability.

30 Table of Contents Economic uncertainty has and could continue to negatively affect the businesses and purchasing decisions of companies in the industries we serve. Such disruptions present considerable risks to our businesses and operations. As global economic conditions experience stress and negative volatility, including any stress or negative volatility related to the imposition of, or threatened imposition of, tariffs and retaliatory tariffs, economic sanctions, and increased trade tensions or if there is an escalation in regional or global conflicts, or terrorism, we may experience reductions in the number of available customers and in capital expenditures by our remaining customers, longer sales cycles, deferral or delay of purchase commitments for our products, and increased price competition. These factors may adversely affect our business, results of operations, and liquidity.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FICO_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
