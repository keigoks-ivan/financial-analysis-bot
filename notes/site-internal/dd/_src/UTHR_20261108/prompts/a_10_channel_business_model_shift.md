你是 stock-analyst v20 DD 的證據採集子 agent。標的：UTHR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - United Therapeutics distribution channel disruption OR shift 2026
  - UTHR United Therapeutics business model transition subscription OR platform 2026
  - Drug Manufacturers - Specialty & Generic channel disintermediation D2C 2026
  - United Therapeutics go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
2025 Annual Report 5 Remodulin Remodulin was approved by the FDA for subcutaneous and intravenous administration in 2002 and 2004, respectively, and has been sold commercially in the United States since 2002. We sell Remodulin to specialty pharmaceutical distributors in the United States and to pharmaceutical distributors internationally. We recognized $526.8 million, $538.1 million, and $494.8 million in Remodulin net product sales, representing 17 percent, 19 percent, and 21 percent of our total revenues for the years ended December 31, 2025, 2024, and 2023, respectively. Remodulin is indicated to treat patients with PAH to diminish symptoms associated with exercise. Studies establishing effectiveness included patients with functional class II-IV (moderate to severe) symptoms. Outside of the United States, Remodulin is approved and commercialized for the treatment of PAH in most of Europe, Canada, Japan, and various other countries in Asia, the Middle East, and Latin America.

12 United Therapeutics, a public benefit corporation Distribution of Commercial Products United States Distribution of Tyvaso DPI, Nebulized Tyvaso, Remodulin, Remunity and RemunityPRO Pumps, Orenitram, and Unituxin We distribute Tyvaso DPI, Nebulized Tyvaso, Remodulin, the Remunity and RemunityPRO Pumps, and Orenitram in the United States through two contracted specialty pharmaceutical distributors: Accredo Health Group, Inc. and its affiliates (Accredo) and Caremark, L.L.C. (CVS Specialty). These distributors are required to maintain certain minimum inventory levels to facilitate an uninterrupted supply to patients who are prescribed our therapies. We compensate Accredo and CVS Specialty on a fee-for-service basis for certain ancillary services in connection with the distribution of these products. If any of our distribution agreements expire or terminate, we may, under certain circumstances, be required to repurchase any unsold inventory held by our distributors.

These specialty pharmaceutical distributors are responsible for assisting patients with obtaining reimbursement for the cost of our treprostinil-based products and providing other support services. Under our distribution agreements, we sell each of our treprostinil-based products to these distributors at a transfer price that we establish. We have also established patient assistance programs in the United States, which provide our treprostinil-based products to eligible uninsured or under-insured patients at no charge. Accredo and CVS Specialty assist us with the administration of these programs.

We distribute Unituxin in the United States through an exclusive distribution agreement with Cencora Global Procurement Ltd (Cencora). Under this agreement, we sell Unituxin to Cencora at a transfer price that we establish, and we pay Cencora fees for services provided in connection with the distribution and support of Unituxin.

International Distribution of Tyvaso DPI, Nebulized Tyvaso, Remodulin, Orenitram, and Unituxin We currently sell Remodulin outside the United States to various distributors, each of which has exclusive distribution rights in one or more countries within Europe, the Middle East, Asia, and South and Central America. Our primary distributor outside the United States is Grupo Ferrer Internacional, S.A. (Ferrer), which holds Remodulin marketing authorization rights in many of these territories. We also sell Nebulized Tyvaso exclusively through Mochida Pharmaceutical Co., Ltd. (Mochida), in Japan, where the product was approved to treat PAH in late 2022, and to treat PH-ILD in 2024. In addition, we sell Nebulized Tyvaso commercially to distributors that have exclusive distribution rights in various countries in Asia, the Middle East, and Latin America, where it is approved for PAH and/or PH-ILD. We also distribute Remodulin and Unituxin in Canada through a specialty pharmaceutical wholesaler. In some of the markets where we are not licensed to market Remodulin, Remodulin is available, but not marketed, on a named patient basis in which therapies are approved for individual patients by a national medical review board, hospital, or health plan on a case-by-case basis. Similar named-patient programs are also available for Nebulized Tyvaso in certain countries.…

18 United Therapeutics, a public benefit corporation We rely entirely on third parties to supply pumps and other supplies necessary to administer Remodulin. ICU Medical discontinued manufacturing the MS-3 system used to administer subcutaneous Remodulin, and specialty pharmacy distributors informed us that supplies of MS-3 pumps are exhausted, although a limited number of refurbished pumps may be available for use with generic treprostinil. ICU Medical has also discontinued manufacturing and distribution of the CADD-Legacy system used to administer intravenous Remodulin. Historically, these were the pumps primarily used to administer Remodulin to patients in the United States. In 2021, we launched the Remunity Pump to administer subcutaneous Remodulin, and in 2022 ICU Medical made an alternative pump, the CADD-Solis, available for intravenous Remodulin. We rely entirely on DEKA and its affiliates to manufacture the Remunity and RemunityPRO Pumps for us. In June 2023, our third-party contract manufacturer obtained FDA clearance for a cartridge to be used with the MS-3 pump for subcutaneous infusion of Remodulin. This clearance enables us to help ensure continuity of cartridge supplies to existing patients using the MS-3 pump. We are also engaged in further efforts to develop alternative pumps to administer Remodulin. There are additional ancillary supplies used with these pumps, and there are a limited number of manufacturers that supply them.

We compete with the developers, manufacturers, and distributors of all of the products noted above for customers, funding, access to licenses, personnel, third-party collaborators, product development, and commercialization. Some of these companies have substantially greater financial, marketing, sales, distribution and technical resources, and more experience in research and development, product development, manufacturing and marketing, clinical trials, and regulatory matters, than we have.

Governmental Regulation Pharmaceutical Product Approval Process The research, development, testing, manufacture, promotion, marketing, distribution, sampling, storage, approval, labeling, record keeping, post-approval monitoring and reporting, and import and export of pharmaceutical products are extensively regulated by governmental agencies in the United States and in other countries. In the United States, failure to comply with requirements under the Federal Food, Drug, and Cosmetic Act (FDC Act), the Public Health Service Act (PHSA), and other federal statutes and regulations, may subject a company to a variety of administrative or judicial sanctions, such as FDA refusal to approve pending NDAs or BLAs, warning letters, product recalls, product seizures, total or partial suspension of manufacturing or distribution, injunctions, fines, civil penalties, and criminal prosecution.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
Revenues Our total revenues consist primarily of sales of the commercial products noted above, including the delivery devices (in the case of Tyvaso DPI, Nebulized Tyvaso, and Remodulin). We have entered into separate, non-exclusive distribution agreements with Accredo and CVS Specialty to distribute Tyvaso DPI, Nebulized Tyvaso, Remodulin, the Remunity and RemunityPRO Pumps, and Orenitram in the United States, and we have entered into an exclusive distribution agreement with Cencora Global Procurement Ltd. to distribute Unituxin in the United States. We also sell Nebulized Tyvaso, Remodulin, and Unituxin to distributors internationally. We sell Adcirca through Lilly’s pharmaceutical wholesale network. To the extent we have increased the price of any of these products, increases have typically been in the single-digit percentages per year, except for Adcirca, the price of which is set solely by Lilly. We also derive revenues from the sale of commercial ex vivo lung perfusion services, which are presented under Other within Note 13—Segment Information to our consolidated financial statements included in this Report.

We require our specialty pharmaceutical distributors to maintain reasonable levels of inventory reserves for our treprostinil-based therapies because the interruption of these therapies can be life threatening. Our specialty pharmaceutical distributors typically place monthly or semi-monthly orders based on current utilization trends and contractual minimum and maximum inventory requirements. As a result, sales of our treprostinil-based therapies can vary depending on the timing and magnitude of these orders and do not precisely reflect changes in patient demand. The information we have about patient demand, the number of patients using our products, and inventory held by our distributors, is based upon our review of patient utilization and inventory data provided to us by our specialty pharmaceutical distributors.

Gross-to-Net Deductions We recognize revenues net of: (1) rebates and chargebacks; (2) prompt pay discounts; (3) allowance for sales returns; and (4) distributor fees. These are referred to as gross-to-net deductions and are primarily based on estimates reflecting historical experiences as well as contractual and statutory requirements. We currently estimate our allowance for sales returns using reports from our distributors. The tables below present a reconciliation of the liability accounts associated with these deductions (in millions): Year Ended December 31, 2025 Rebates & Chargebacks Prompt Pay Discounts Allowance for Sales Returns Distributor Fees Total Balance, January 1, 2025 $ 140.8 $ 5.1 $ 2.2 $ 11.6 $ 159.7 Provisions attributed to sales in: Current period 521.6 74.0 0.9 41.7 638.2 Prior periods 0.7 0.1 — (0.5) 0.3 Payments or credits attributed to sales in: Current period (296.6) (67.7) — (30.1) (394.4)
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
