你是 stock-analyst v20 DD 的證據採集子 agent。標的：UTHR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - United Therapeutics product substitute technology threat 2026
  - Drug Manufacturers - Specialty & Generic alternative technology disruption 2026 2027
  - UTHR United Therapeutics technology obsolescence risk
  - Drug Manufacturers - Specialty & Generic next-generation technology roadmap 2026


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
Patients must use external pumps manufactured by third parties to deliver Remodulin. Historically, Smiths Medical, Inc. (Smiths Medical, which was acquired by ICU Medical, Inc., or ICU Medical) manufactured the pumps used by most patients in the United States to administer Remodulin, including the CADD-MS®3 (MS-3) pump used to deliver subcutaneous Remodulin, and the CADD-Legacy® pump to deliver intravenous Remodulin. In 2015, Smiths Medical notified us that it was planning to discontinue the manufacture of the MS-3 pumps and associated cartridges. In response, we funded Smiths Medical’s manufacture of several thousand additional MS-3 pumps and, in parallel, pursued development of the Remunity Pump so that PAH patients would not experience a delay or disruption in their Remodulin therapy. Our specialty pharmacy distributors informed us that supplies of new MS-3 pumps are fully exhausted, although a limited number of refurbished pumps may be available for use with generic treprostinil. In June 2023, our third-party contract manufacturer, Gilero LLC, which was later acquired by Sanner GmbH, obtained FDA clearance for a cartridge to be used with the MS-3 pump for subcutaneous infusion of Remodulin. As discussed below under Remunity and RemunityPRO Pumps, our Remunity and RemunityPRO Pumps are now the primary infusion systems used to deliver Remodulin subcutaneously.…

Regenerative Medicine •Miromatrix. In December 2023, we acquired Miromatrix Medical Inc. (Miromatrix), a company based in Minnesota focused on the development of new technologies for generating manufactured kidneys and liver alternatives composed of human primary cells. The development-stage Miromatrix external liver assist product, called miroliverELAP®, uses a decellularized porcine liver matrix that has been seeded with human-derived cells and an extracorporeal blood circuit to maintain liver support in patients experiencing acute liver failure. Miromatrix first used its decellularization technology to successfully develop two acellular products, MiroMesh® and MiroDerm®, which received FDA 510(k) clearance for hernia repair and wound care applications, respectively, and which were later spun off by Miromatrix. In January 2026 we announced that Miromatrix completed a phase 1 study of miroliverELAP in patients with acute liver failure. This study, which was the first human clinical trial of a manufactured organ alternative, met its primary endpoint. Miromatrix is planning to commence a phase 2 study. Miromatrix is also developing miroliver®, a fully implantable manufactured liver alternative product, and mirokidney®, a fully implantable manufactured kidney alternative product, both of which are based on decellularized porcine organ scaffolds that have been reseeded with human-derived cells.…

•IVIVA. In October 2023, we completed the acquisition of IVIVA Medical, Inc. (IVIVA), a preclinical stage company based in Massachusetts, focused on bio-artificial manufactured kidney alternative products. IVIVA’s preclinical implantable kidney alternative product uses autologous cells to mimic important physiological functions of native kidneys in recipients to support their native kidney function without the need for immunosuppression. The product is designed to replace the need for external kidney dialysis.

Manufactured Organ and Organ Alternative Proprietary Rights We have a large portfolio of pending patent applications and issued patents that could protect our proprietary rights in our manufactured organs and organ alternative products. We own patents, and have licensed rights under third-party patents, covering various aspects of these products; we do not view any one patent or group of patents as critical. For example, we have over 150 pending patent applications and multiple issued patents covering various aspects of our 3D organ alternative bioprinting program, and we have exclusively licensed an extensive 3D printing patent portfolio from 3D Systems for use in the field of manufacturing solid organ alternatives. Our xenotransplantation patent portfolio includes over 150 pending applications and issued patents, including nearly one hundred issued patents in the U.S. and abroad. Our regenerative medicine patent portfolio includes over 300 pending applications and issued patents.

Patent Term and Regulatory Exclusivity In 1984, the Hatch-Waxman Act created a faster approval process for generic drugs, called the ANDA. Generally, an ANDA provides for marketing of a drug product that has the same active ingredients in the same strength(s), route of administration, and dosage form as an approved drug and has been shown through bioequivalence testing to be therapeutically equivalent to the approved drug, which is known as the reference listed drug (RLD). ANDA applicants are not required to conduct or submit results of preclinical or clinical tests to prove the safety or effectiveness of their drug product, other than the requirement for bioequivalence testing. Drugs approved in this way are commonly referred to as “generic equivalents” to the approved drug, and can often be substituted by pharmacists under prescriptions written for the original approved drug.

We believe our 3D printed, regenerative medicine, and bio-artificial organ alternative products will be subject to similar regulatory requirements as the Miromatrix products, and will necessitate BLA approvals in the U.S.

In many cases, our manufactured organ and organ alternative products will involve seeking regulatory approval for categories of products that have never been approved by the FDA before, and therefore, our anticipated regulatory approach is subject to change as regulators issue new guidance, and as our discussions with the FDA and other agencies progress.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
The commercial success of our products depends, in significant part, on coverage by governmental payers such as Medicare and Medicaid, and private insurance companies. A reduction in the availability or extent of reimbursement from domestic or foreign government health care programs could have a material adverse effect on our business and results of our operations. Government and commercial payers are increasingly attempting to limit the price of medicinal products and frequently challenge the pricing of new or expensive drugs. In many markets outside the United States, governments control the prices of prescription pharmaceuticals through the implementation of reference pricing, price cuts, rebates, revenue-related taxes, and profit control. Financial pressures may cause United States government payers and/or private health insurers to implement policies that would reduce reimbursement rates for our products, limit future price increases, cap reimbursement rates for pharmaceuticals to rates paid internationally, require the automatic substitution of generic products, demand more rigorous requirements for initial coverage for new products, implement step therapy policies that require patients to try other medicines, including generic products, before using our products, or take other similar steps that could make it more difficult for patients to access our products.…

•Natural and man-made disasters (such as fires, contamination, power loss, hurricanes and other forms of severe weather, earthquakes, flooding, terrorist attacks, and acts of war), some of which could be exacerbated by climate change, disease outbreaks, and pandemics such as COVID-19 impacting our internal and third-party manufacturing and warehousing sites could cause a supply disruption.

•The supply of materials and components necessary to manufacture and package our products may become scarce or unavailable, which in the past has delayed, and in the future could delay, the manufacturing and subsequent sale of such products. Products manufactured with substituted materials or components must be approved by the FDA and applicable international regulatory agencies before they can be sold.

Any of these factors could disrupt sales of our commercial products, delay clinical trials or commercialization of new products, result in product liability claims and product recalls, and entail higher costs or lost revenues. Interruptions in our manufacturing process could be significant given the length of time and complexity involved in obtaining necessary regulatory approvals for alternative arrangements, through either third parties or internal manufacturing processes.

Lilly manufactures and supplies Adcirca for us. We use Lilly’s pharmaceutical wholesaler network to distribute Adcirca. If Lilly is unable to manufacture or supply Adcirca or its distribution network is disrupted, it could delay, disrupt, or prevent us from selling Adcirca.

Risks Related to Legal Compliance We must comply with extensive laws and regulations in the United States and other countries. Failure to obtain approvals on a timely basis or to comply with these requirements could delay, disrupt, or prevent commercialization of our products.

We are increasingly dependent on information technology systems and infrastructure, much of which is outsourced to third parties including in cloud-based platforms. We collect, store, and use sensitive or confidential data, including intellectual property, our proprietary business information and that of our suppliers, patients, healthcare providers, and business partners, and personally identifiable information. We recently launched a new patient relations program, United Therapeutics Cares, which has increased our access to sensitive information about our patients. Actual or alleged cybersecurity incidents, including those caused by employee error, malfeasance, system failures, malware, ransomware, viruses, distributed denial of services attacks, credential harvesting, social engineering, and other forms of unauthorized access or disclosure to, or disrupting the operation of, our networks and systems or those of our customers, suppliers, vendors, and other service providers, can cause the loss, destruction, or unauthorized access or disclosure of data, including personal information of employees or confidential or proprietary information, disruption of our manufacturing and other operations, and damage to our reputation and competitive position, any of which could be costly to address and remediate and adversely affect our business, financial condition, or results of operations.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
