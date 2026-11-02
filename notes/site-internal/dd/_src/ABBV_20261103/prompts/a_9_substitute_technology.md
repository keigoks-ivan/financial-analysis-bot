你是 stock-analyst v20 DD 的證據採集子 agent。標的：ABBV。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - AbbVie product substitute technology threat 2026
  - Drug Manufacturers - General alternative technology disruption 2026 2027
  - ABBV AbbVie technology obsolescence risk
  - Drug Manufacturers - General next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm｜as_of：2026-02-20
<<<
5 | 2025 Form 10-K Competition The markets for AbbVie's products are highly competitive. AbbVie competes with other research-based pharmaceuticals and biotechnology companies that discover, manufacture, market and sell proprietary pharmaceutical products, therapies and biologics. For example, AbbVie's immunology products compete with IL-23 inhibitors, IL-17 inhibitors, JAK inhibitors, biosimilars and other competitive products intended to treat a number of disease states, and AbbVie's oncology products compete with targeted therapies including BTK inhibitors, ADCs, cell therapies and other competitive products intended to treat certain cancers. In addition, a number of other companies have successfully developed and market products that are being positioned as competitors to Botox. The search for technological innovations in pharmaceutical products is a significant aspect of competition. The introduction of new products by competitors and changes in medical practices and procedures can result in product obsolescence. Price is also a competitive factor. In addition, the substitution of generic and biosimilar pharmaceutical products for branded pharmaceutical products creates competitive pressures on AbbVie's products that do not have patent protection. New products or treatments brought to market by AbbVie’s competitors could cause revenues for AbbVie’s products to decrease due to price reductions and sales volume decreases.

Furthermore, the law provides that only a biosimilar product that is determined to be "interchangeable" will be considered by the FDA as substitutable for the original biologic product without the intervention of the health care provider who prescribed the original biologic product. To prove that a biosimilar product is interchangeable, the applicant must demonstrate that the product can be expected to produce the same clinical results as the original biologic product in any given patient, and if the product is administered more than once in a patient, that safety risks and potential for diminished efficacy of alternating or switching between the use of the interchangeable biosimilar biologic product and the original biologic product is no greater than the risk of using the original biologic product without switching. The law continues to be interpreted and implemented by the FDA. As a result, its full ultimate impact, implementation and meaning remains subject to uncertainty.

Third Party Agreements AbbVie has agreements with third parties for process development, product distribution, analytical services and manufacturing of certain products. AbbVie procures certain products and services from a limited number of suppliers and, in some cases, a single supply source. In addition, AbbVie has agreements with third parties for active pharmaceutical ingredient and product manufacturing, formulation and development services, fill, finish and packaging services, transportation and distribution and logistics services for certain products. AbbVie does not believe that these manufacturing-related agreements are material because AbbVie's business is not substantially dependent on any individual agreement. In most cases, AbbVie maintains alternate supply relationships that it can utilize without undue disruption of its manufacturing processes if a third party fails to perform its contractual obligations. AbbVie seeks to maintain sufficient inventory of product to minimize the impact of any supply disruption.

In the United States, most states also have generic substitution legislation requiring or permitting a dispensing pharmacist to substitute a different manufacturer's generic version of a pharmaceutical product for the one prescribed. In addition, the federal government follows a diagnosis-related group (DRG) payment system for certain institutional services provided under Medicare or Medicaid and has implemented a prospective payment system (PPS) for services delivered in hospital outpatient, nursing home and home health settings. DRG and PPS entitle a health care facility to a fixed 2025 Form 10-K | 10 reimbursement based on the diagnosis and/or procedure rather than actual costs incurred in patient treatment, thereby increasing the incentive for the facility to limit or control expenditures for many health care products. Medicare reimburses Part B drugs based on average sales price plus a certain percentage to account for physician administration costs, which have been reduced in the hospital outpatient setting. Medicare enters into contracts with private plans to negotiate prices for most patient-administered medicine delivered under Part D.

Most governments also promote generic substitution by mandating or permitting a pharmacist to substitute a different manufacturer's generic version of a pharmaceutical product for the one prescribed and by permitting or mandating that health care professionals prescribe generic versions in certain circumstances. Many governments are also following a similar path for biosimilar therapies. In addition, governments use reimbursement lists to limit the pharmaceutical products that are eligible for reimbursement by national health care systems.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm｜as_of：2026-02-20
<<<
As patents for certain of its products expire, AbbVie could face competition from lower priced generic or biosimilar products. The expiration or loss of patent protection for a product typically is followed promptly by substitutes that may significantly reduce sales for that product in a short amount of time. If AbbVie's competitive position is compromised because of generics, biosimilars or otherwise, it could have a material adverse effect on AbbVie's business and results of operations. In addition, proposals emerge from time to time for legislation to further encourage the early and rapid approval of generic drugs or biosimilars. Any such proposals that are enacted into law could increase the impact of generic or biosimilar competition.

To remain competitive, AbbVie must continue to launch new products and new indications and/or brand extensions for existing products. Such launches must generate revenue sufficient both to cover its substantial research and development costs and to replace revenues of profitable products that are lost to or displaced by competing products or therapies. Failure to do so would have a material adverse effect on AbbVie's revenue and profitability. Accordingly, AbbVie commits substantial effort, funds and other resources to research and development and must make ongoing substantial expenditures without any assurance that its efforts will be commercially successful. A high rate of failure in the biopharmaceutical industry is inherent in the research and development of new products, and failure can occur at any point in the research and development process, including after significant resources have been invested.…

Trade restrictions, tariffs, and other changes in global trade policy could increase costs, disrupt supply chains, and adversely affect AbbVie’s business and results of operations.

AbbVie operates in a global environment and relies on complex international supply chains for the development, manufacture, and distribution of its products, including the sourcing of active pharmaceutical ingredients and key materials. Changes in global trade policy, including the potential imposition of import or export tariffs, trade restrictions, or other measures affecting pharmaceutical products or related inputs, could increase manufacturing and procurement costs, reduce margins or disrupt supply continuity. If AbbVie is unable to substantially mitigate or offset increased costs or disruptions resulting from such measures through pricing adjustments, operational changes, or alternative sourcing arrangements, it may have an adverse effect on AbbVie’s business and results of operations.

AbbVie uses raw materials and components in its pharmaceutical and biologic manufacturing processes that may be sourced from single suppliers. The failure of AbbVie's suppliers, and particularly its single-source suppliers, to fulfill their contractual obligations in a timely manner or as a result of regulatory noncompliance or physical disruption at a manufacturing site may impair AbbVie's ability to deliver its products to customers on a timely and competitive basis, which could adversely affect AbbVie's business and results of operations. Increases in demand on any of AbbVie's suppliers could result in delays and disruptions in the manufacturing, distribution and sale of its products and/or product shortages, leading to lost revenue. Finding an alternative supplier could take a significant amount of time and involve significant expense due to the nature of the products and the need to obtain regulatory approvals. AbbVie cannot guarantee that it will be able to reach agreement with alternative providers or that regulatory authorities would approve AbbVie's use of such alternatives. Business interruption insurance may not provide adequate compensation in the case of a failure by a supplier.

Possible regulatory actions could result in substantial modifications to AbbVie's business practices and operations; refunds, recalls or seizures of AbbVie's products; a total or partial shutdown of production in one or more of AbbVie's or its suppliers' facilities while AbbVie or its supplier remedies the alleged violation; the inability to obtain future approvals; and withdrawals or suspensions of current products from the market. Any of these events could disrupt AbbVie's business and have a material adverse effect on its business and results of operations.

AbbVie depends on information technology and a failure of, or significant disruption to, those systems, or a failure to adequately adopt emerging technologies such as artificial intelligence, could have a material adverse effect on AbbVie's business.

Additionally, AbbVie utilizes AI and other emerging technologies in select applications to support its operations. These technologies may present opportunities for AbbVie's business but may also entail risks, including that AI-generated analyses utilized by AbbVie could be deficient or exacerbate regulatory, cybersecurity or other significant risks. Further, our failure to effectively implement these technologies could hinder our ability to compete, as competitors' advancements in AI may lead to more efficient operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABBV_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
