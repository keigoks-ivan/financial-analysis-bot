你是 stock-analyst v20 DD 的證據採集子 agent。標的：COF。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - COF Capital One Financial market share gaining OR losing 2026
  - Capital One Financial new entrant OR displace threat Credit Services 2026
  - COF competitor design win 2026
  - Capital One Financial vs Credit Services peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm｜as_of：2026-02-19
<<<
7 Capital One Financial Corporation (COF) Table of Contents COMPETITION Each of our business segments operates in a highly competitive environment, and we face competition in all aspects of our business from numerous bank and non-bank providers of financial services.

Our Consumer Banking and Commercial Banking businesses compete with national, state and direct banks as well as with savings and loan associations and credit unions for loans and deposits. Our competitors also include automotive finance companies, commercial banking companies and other financial services providers that provide loans, deposits, and other similar services and products. In addition, we compete against non-bank institutions that are able to offer these products and services. As a result of our recent acquisition of the Global Payment Network, we now compete in the global payments industry, both with traditional competitors and new, emerging alternative payment providers.

We also consider new and emerging companies in digital and mobile payments and other financial technology providers among our competitors. We compete with many forms of payment mechanisms, including a variety of new and evolving alternative payment mechanisms, systems and products, offered by both bank and non-bank providers.

Our businesses generally compete on the basis of the quality and range of their products and services, transaction execution, innovation and price, and, with respect to our payment network businesses, the strength, reach, pricing and capabilities of our network offerings to merchants, acquirers and issuers. Competition varies based on the types of clients, customers, industries and geographies served. Our ability to compete depends, in part, on our ability to attract and retain our associates and on our reputation as well as our ability to keep pace with innovation, in particular in the development of new technology platforms. There can be no assurance, however, that our ability to market products and services successfully or to obtain adequate returns on our products and services will not be impacted by the nature of the competition that now exists or may later develop, or by the broader economic environment. For a discussion of the risks related to our competitive environment, see “Item 1A. Risk Factors.”

Compensation and Wellness We appreciate the importance of a competitive total compensation package to attract and retain great talent. Our benefits, including competitive parental leave, on-site health centers, company contributions to associates’ 401(k) plans, educational assistance and other health, wellness and financial benefits are designed to support our associates’ wellbeing inside and outside of the workplace. Furthermore, pay equity is an important element of our pay philosophy. We evaluate base pay and incentive pay for all of our associates globally, at least annually. We review groups of associates in similar roles, adjusting for factors that appropriately explain differences in pay such as job location and experience.

Intellectual Property and Other Proprietary Information As part of our overall and ongoing strategy to protect and enhance our intellectual property rights, we rely on a variety of protections, including copyrights, trademarks, trade secrets, patents and certain restrictions on disclosure, solicitation and competition. We also undertake other measures to control access to, or distribution of, our other proprietary and confidential information. Any patents we may obtain may increase our competitive advantage, protect our investments in commercializing our technology, preserve our freedom to operate, and allow us to enter into licensing (e.g., cross-licenses) or other arrangements with third parties. For a discussion of risks associated with intellectual property, see “Item 1A. Risk Factors” under the heading “If we are not able to protect our intellectual property rights, or we violate third-party intellectual property rights, our revenue and profitability could be negatively affected.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm｜as_of：2026-02-19
<<<
We operate in a highly competitive environment across all of our lines of business, whether in making loans, attracting deposits or in the global payments industry, and we expect competitive conditions to continue to intensify with respect to most of our products, particularly in our card, payment network and consumer banking businesses. We compete on the basis of the rates we pay on deposits and the rates and other terms we charge on the loans we originate or purchase, as well as the quality and range of our customer service, products, innovation and experience, and, with respect to our payment network businesses, the strength, reach, pricing and capabilities of our network offerings to merchants, acquirers and issuers. This competitive environment is a result of changes in technology, product delivery systems and regulation, as well as the emergence of new or significantly larger financial services providers, all of which may affect our customers’ expectations and demands. In addition to offering competitive products and services, we invest in and conduct marketing campaigns to attract and inform customers. If our marketing campaigns are unsuccessful, it may adversely impact our ability to attract new customers and grow our business.

Some of our competitors, including new and emerging competitors in the digital and mobile payments space and other financial technology providers and payment networks, are not subject to the same regulatory requirements or scrutiny to which we are subject, which also could place us at a competitive disadvantage, in particular in the development of new technology platforms or the ability to rapidly innovate. We compete with many forms of payments offered by both bank and non-bank providers, including a variety of new and evolving alternative payment mechanisms, systems and products, such as aggregators and web-based and wireless payment platforms or technologies, digital currencies or cryptocurrencies (including stablecoins and tokenized deposits), prepaid systems and payment services targeting users of social networks, communications platforms and online gaming. If we are unable to continue to keep pace with innovation and fail to reflect such technology in our payments offerings, do not effectively market our products and services, are unable to deliver them effectively and securely to our customers or are prohibited from or unwilling to enter emerging areas of competition, our business and results of operations could be adversely affected.…

Some of our competitors are substantially larger than we are, which may give those competitors advantages, including a more diversified product and customer base, the ability to reach more customers and potential customers, operational efficiencies, broad-based local distribution capabilities, lower-cost funding and larger existing branch networks. Many of our competitors are also focusing on cross-selling their products and developing new products or technologies, which could affect our ability to maintain or grow existing customer relationships or require us to offer lower interest rates or fees on our lending products or higher interest rates on deposits. Competition for loans could result in origination of fewer loans, earning less on our loans or an increase in loans that perform below expectations.

We face strong and increasing competition in the direct banking market. Aggressive pricing throughout the industry may adversely affect the retention of existing balances and the cost-efficient acquisition of new deposit funds and may affect our growth and profitability. Customers could also close their online accounts or reduce balances or deposits in favor of products and services offered by competitors for other reasons. These shifts, which could be rapid, could result from general dissatisfaction with our products or services, including concerns over pricing, online security or our reputation. The potential consequences of this competitive environment are exacerbated by the flexibility of direct banking and the financial and technological sophistication of our online customer base.

As a result of our recent acquisition of the Global Payment Network, we now face substantial and increasingly intense competition in the payments industry, both from traditional players and new, emerging alternative payment providers. For example, we now compete with other payment networks to attract Network Partners to issue credit and debit cards and other card products on the Global Payment Network. In addition, increased competition with certain network operators, such as Visa and Mastercard, could affect our existing partnerships and business relationships with these networks, which have historically played a significant role in facilitating our card-issuing and transaction processing services. Competition with other operators of payment networks is generally based on issuer fees, fees paid to networks (including switch fees), merchant acceptance and functionality, technological capabilities and other economic terms. Competition is also based on customer perception of service quality, merchant acceptance, brand image, reputation and market share. Further, we are now facing ongoing competition from emerging alternative payment providers who may create innovative networks or other arrangements with our primary competitors, large merchants or other industry participants, or provide stablecoins, other digital currencies or tokenized deposits, which could adversely impact our costs, transaction volume and ability to grow our business.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
