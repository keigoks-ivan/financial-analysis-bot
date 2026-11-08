你是 stock-analyst v20 DD 的證據採集子 agent。標的：MNST。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Monster Beverage distribution channel disruption OR shift 2026
  - MNST Monster Beverage business model transition subscription OR platform 2026
  - Beverages - Non-Alcoholic channel disintermediation D2C 2026
  - Monster Beverage go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm｜as_of：2026-02-27
<<<
Our Monster Energy® Drinks segment primarily generates net operating revenues by selling ready-to-drink packaged drinks primarily to bottlers and full service beverage distributors (“bottlers/distributors”). In some cases, we sell ready-to-drink packaged drinks 3 Table of Contents directly to retail grocery and specialty chains, wholesalers, club stores, mass merchandisers, convenience and gas chains, drug stores, foodservice customers, value stores, e-commerce retailers and the military.

Our Strategic Brands segment primarily generates net operating revenues by selling “concentrates” and/or “beverage bases” to authorized bottling and canning operations. Such bottlers generally combine the concentrates and/or beverage bases with sweeteners, water and other ingredients to produce ready-to-drink packaged energy drinks. The ready-to-drink packaged energy drinks are then sold by such bottlers to other bottlers/distributors and to retail grocery and specialty chains, wholesalers, club stores, mass merchandisers, convenience and gas chains, foodservice customers, drug stores, value stores, e-commerce retailers and the military. To a lesser extent, our Strategic Brands segment generates net operating revenues by selling certain ready-to-drink packaged energy drinks to bottlers/distributors.

Distribution Agreements During 2025, we continued to expand distribution of our products in both our domestic and international markets.

Monster Energy® Distribution Agreements We have entered into agreements with various bottlers/distributors providing for the distribution of certain of our energy drinks during initial terms of up to twenty years, which may be extended thereafter, subject to certain terms and conditions, which may vary depending on the form of the agreement. Such agreements remain in effect for their then-current term as long as our products are being distributed, but are subject to specified termination rights held by each party, which may include by way of example, and depending on the form of agreement, termination upon: mutual agreement; material breach of the agreement by, or an insolvency of, either party; deadlock; change of control; changes in legal or regulatory conditions and termination of certain related agreements. Additionally, we are entitled to terminate certain distribution agreements at any time without cause upon payment of a termination fee, including a limited number of distribution agreements with TCCC network bottlers that were entered into prior to 2015.

All distribution territories in the United States, and substantially all distribution territories internationally have been transitioned to TCCC network bottlers/distributors.

9 Table of Contents Strategic Brands Distribution Agreements We have entered into distribution coordination agreements with TCCC pursuant to which we have designated, and in the future may designate, subject to TCCC’s approval, territories in which TCCC network bottlers will distribute our Strategic Brands energy drinks. We have entered into agreements with various TCCC network bottlers, both in the United States and internationally, providing for the distribution and sale of our Strategic Brands energy drinks.

Alcohol Brands Distribution Agreements Monster Brewing Company has entered into agreements with various beer distributors, both in the United States and, to a limited extent, internationally, providing for the distribution of our alcohol products. Such agreements have varying terms and durations. Monster Brewing Company has also entered into distribution agreements with licensed beer distributors for the exclusive distribution of certain beverages in agreed upon territories.

We compete not only for consumer preference, but also for maximum marketing, sales efforts and attention from our multi-brand licensed bottlers and distributors, many of which have a principal affiliation with competing companies and brands. Our products compete with all liquid refreshments, including TCCC, PepsiCo, Inc. (“PepsiCo”), Keurig Dr. Pepper Inc. (“KDP”) and Red Bull GmbH. From time to time, competitors have entered into distribution or acquisition agreements with certain other competitors. For example, KDP, which distributes C4 and Bloom, entered into a long-term sales and distribution agreement with Black Rifle Coffee Company as well as a definitive agreement to acquire GHOST Lifestyle LLC and GHOST Beverages LLC. In addition, Celsius Holdings, Inc. (“CELSIUS”) acquired Alani Nutrition LLC (“Alani Nu”). We also compete with companies that are smaller or primarily local in operation. Our products also compete with private-label brands such as those carried by grocery store chains, convenience store chains and club stores.

Where appropriate, we partner with our bottlers/distributors and/or retailers to assist our marketing efforts.

Customers Our non-alcohol customers are primarily full service beverage bottlers/distributors, retail grocery and specialty chains, wholesalers, club stores, mass merchandisers, convenience and gas chains, drug stores, foodservice customers, value stores, e-commerce retailers and the military. Our alcohol customers are primarily beer distributors who in turn sell to retailers within the alcohol distribution system. Percentages of our gross billings to various customer types for the years ended December 31, 2025, 2024 and 2023 are reflected below. Such information includes sales made by us directly to the customer types concerned, which include our full service beverage bottlers/distributors in the United States. Such full service beverage bottlers/distributors in turn sell certain of our products to some of the same customer types listed below. We limit our description of our customer types to include only our sales to our full service bottlers/distributors without reference to such bottlers/distributors’ sales to their own customers.

​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ 2025 ​ ​ ​ 2024 ​ ​ ​ 2023 U.S. full service bottlers/distributors 45% ​ 46% ​ 47% International full service bottlers/distributors 43% ​ 41% ​ 40% Club stores and e-commerce retailers 8% ​ 8% ​ 8% Retail grocery, direct convenience, specialty chains and wholesalers 2% ​ 2% ​ 2% Alcohol, value stores and other 2% ​ 3% ​ 3% ​ Our non-alcohol customers include Coca-Cola Canada Bottling Limited, Coca-Cola Consolidated, Inc., Coca-Cola Bottling Company United, Inc., Reyes Holdings, LLC, Coca-Cola Southwest Beverages LLC, The Coca-Cola Bottling Company of Northern 12 Table of Contents New England, Inc., Swire Pacific Holdings, Inc. (USA), Liberty Coca-Cola Beverages, LLC, Coca-Cola Europacific Partners, Coca-Cola Hellenic, Coca-Cola FEMSA, Swire Coca-Cola (China), COFCO Coca-Cola, Coca-Cola Beverages Africa, Coca-Cola İçecek and certain other TCCC network bottlers, Asahi Soft Drinks, Co., Ltd., Wal-Mart, Inc. (including Sam’s Club), Costco Wholesale Corporation and Amazon.com, Inc.

Government Regulation The production, distribution and sale in the United States of many of our products are subject to various U.S. regulations, including but not limited to: the Federal Food, Drug and Cosmetic Act (“FD&C Act”); the Occupational Safety and Health Act and various state laws and regulations governing ingredient safety and labeling and workplace health and safety; various environmental statutes; the Safe Drinking Water and Toxic Enforcement Act of 1986 (“California Proposition 65”); various state and federal laws and regulations pertaining to the sale and distribution of alcohol beverages; data privacy, cybersecurity and personal data protection laws and regulations, including the California Consumer Privacy Act of 2018 (as modified by the California Privacy Rights Act) and a number of other federal, state and local statutes and regulations applicable to the production, transportation, sale, safety, advertising, marketing, labeling, packaging, and ingredients of such products. Outside the United States, the production, distribution and sale of many of our products are also subject to numerous statutes and regulations.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/865752/000110465926020831/mnst-20251231x10k.htm｜as_of：2026-02-27
<<<
Our non-alcohol customers are primarily full service beverage bottlers/distributors, retail grocery and specialty chains, wholesalers, club stores, mass merchandisers, convenience and gas chains, drug stores, foodservice customers, value stores, e-commerce retailers and the military. Our alcohol customers are primarily beer distributors who in turn sell to retailers within the alcohol distribution system. Percentages of our gross billings to our various customer types for the years ended December 31, 2025, 2024 and 2023 are reflected below. Such information includes sales made by us directly to the customer types concerned, which include our full service beverage bottlers/distributors in the United States. Such full service beverage bottlers/distributors in turn sell certain of our products to some of the same customer types listed below. We limit our description of our customer types to include only our sales to our full service bottlers/distributors without reference to such bottlers/distributors’ sales to their own customers.

% Less: Promotional allowances, commissions and other expenses*** ​ (1,573,343) ​ (1,282,887) ​ (1,129,637) 22.6 % 13.6 % Net Sales ​ $ 8,294,343 ​ $ 7,492,709 ​ $ 7,140,027 10.7 % 4.9 % ​ ***Although the expenditures described in this line item are determined in accordance with GAAP and meet GAAP requirements, the presentation thereof does not conform to GAAP presentation requirements. Additionally, our definition of promotional and other allowances may not be comparable to similar items presented by other companies. Promotional and other allowances for our energy drink products primarily include consideration given to our non-alcohol bottlers/distributors or retail customers including, but not limited to the following: (i) discounts granted off list prices to support price promotions to end-consumers by retailers; (ii) reimbursements given to our bottlers/distributors for agreed portions of their promotional spend with retailers, including slotting, shelf space allowances and other fees for both new and existing products; (iii) our agreed share of fees given to bottlers/distributors and/or directly to retailers for advertising, in-store marketing and promotional activities; (iv) our agreed share of slotting, shelf space allowances and other fees given directly to retailers, club stores and/or wholesalers; (v) incentives given to our bottlers/distributors and/or retailers for achieving or exceeding certain predetermined sales goals; (vi) discounted or free products; (vii) contractual fees given to our bottlers/distributors related to sales made by us direct to certain customers that fall within the bottlers’/distributors’ sales…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
