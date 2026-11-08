你是 stock-analyst v20 DD 的證據採集子 agent。標的：TMDX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - TMDX TransMedics Group market share gaining OR losing 2026
  - TransMedics Group new entrant OR displace threat Medical Devices / Organ Transplant Logistics 2026
  - TMDX competitor design win 2026
  - TransMedics Group vs Medical Devices / Organ Transplant Logistics peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm｜as_of：2026-02-24
<<<
Our Competitive Strengths We believe the continued growth of our company will be driven by the following competitive strengths: •Only FDA approved, portable, multi-organ, warm perfusion platform Our Organ Care System is the only FDA approved portable, multi-organ, warm perfusion device on the market. Portability is a critical aspect in reducing the ischemic injury to the organ before transplantation, thereby reducing post-transplant complications and allowing the utilization of more organs for transplant. The multi-organ platform allows for the standardization of use across transplant programs.

12 Competition Competition in organ preservation for transplantation can be classified into two main segments: (1) cold storage and cold perfusion technologies and (2) warm perfusion technologies. In both cold storage and cold perfusion, the organs are not functioning and are metabolically inactive. The characteristics of cold storage and cold perfusion described above significantly limit donor organ utilization and are a primary driver of post-transplant complications. Supply of cold storage and cold perfusion products is fragmented with a number of companies mainly providing undifferentiated flush and perfusion solutions or temperature controlled cold storage devices.

The national competent authorities in each member state oversee and enforce compliance with the standards set out in the MDR against relevant economic operators (including device manufacturers, importers, authorized representatives and distributors). Under the MDR, national competent authorities can inform other national competent authorities, the European Commission and Notified Bodies, as applicable, of certain non-compliances.

Clinical Investigations Clinical evidence is required for the conformity assessment of most medium and high risk devices. In some cases, a clinical investigation may be required to support the CE marking of a device. All clinical investigations involving medical devices must comply with the relevant requirements of the MDR, EU member state requirements, and current good clinical practices defined in harmonized standards and guidance documents. Clinical investigations for medical devices cannot proceed without a positive opinion of an ethics committee and notification to the relevant national competent authorities. Both national competent authorities and ethics committees also require the submission of serious adverse event reports during a study and may request a copy of the final study report.

In the European Union the consequences for failing to comply with advertising and promotional laws might lead to reputational damage, fines, exclusions from public tenders and actions for damages from competitors for unfair competition.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm｜as_of：2026-02-24
<<<
Other companies may develop technologies and products that result in improved patient outcomes or are safer, easier to use, less expensive or more readily accepted than the OCS. These products or technologies could make the OCS obsolete or noncompetitive and reduce demand for our OCS products. Many of these providers of alternative products, procedures and therapies have greater name recognition, significantly greater financial resources and expertise in research and development, manufacturing, preclinical testing, conducting clinical trials, obtaining regulatory approvals and clearances and marketing and selling products than we do. Smaller and other early stage companies may also prove to be significant competitors, particularly through collaborative arrangements with large and established companies. Third parties may also compete with us in recruiting and retaining qualified medical, engineering and management personnel, establishing clinical trial sites and patient registration for clinical trials, as well as in acquiring technologies complementary to or necessary for our products or development programs or otherwise advantageous to our business. Our failure to compete effectively will harm our business and operating results.

If any third-party patents were asserted against us, even if we believe such claims are without merit, a court may not find in our favor on questions of infringement, validity, enforceability, or priority. A court of competent jurisdiction could hold that the asserted third-party patents are valid, enforceable, and infringed, which could materially and adversely affect our ability to commercialize our products. In order to successfully challenge the validity of any U.S. patent in federal court, we would need to overcome a presumption of validity. As this burden is a high one requiring us to present clear and convincing evidence as to the invalidity of any such U.S. patent claim, a court of competent jurisdiction may not invalidate the claims of any such U.S. patent. We may choose or, if we are found to infringe a third party’s patent rights and we are unsuccessful in demonstrating that such patents are invalid or unenforceable, we could be required to obtain a license from such third party to continue developing, manufacturing, and marketing any of our products. However, we may not be able to obtain any required license on commercially reasonable terms or at all.…

However, our patents or pending patent applications that mature into issued patents may not include claims with a scope sufficient to protect our OCS technology, any additional features we develop for our OCS technology or any new products. Other parties may have developed technologies that may be related to or competitive with our system, may have filed or may file patent applications and may have received or may receive patents that overlap or conflict with our patent applications, either by claiming the same methods or devices or by claiming subject matter that could dominate our patent position. The patent positions of medical device companies, including our patent position, may involve complex legal and factual questions, and, therefore, the scope, validity and enforceability of any patent claims that we may obtain cannot be predicted with certainty. Our pending and future patent applications may not issue as patents or, if issued, may not issue in a form that will be advantageous to us.…

Depending upon the timing, duration and specifics of FDA marketing approval of our products, one or more of the U.S. patents we own or license may be eligible for patent term restoration (also referred to as patent term extension) under the Drug Price Competition and Patent Term Restoration Act of 1984, referred to as the Hatch-Waxman Act. The Hatch-Waxman Act permits a patent restoration term of up to five years for a patent covering an approved product as compensation for effective patent term lost as a result of product development and the FDA regulatory review process. However, even if, at the relevant time, we have an issued patent covering our product, we may not be granted an extension if we were, for example, to fail to apply within applicable deadlines or prior to expiration of relevant patents or otherwise fail to satisfy applicable requirements. Moreover, the time period of the extension could be less than we request, for example, if we are found to have failed to exercise due diligence during the testing phase or regulatory review process.…

In addition to patent protection, we also rely upon trade secret protection, as well as non-disclosure agreements and invention assignment agreements with our employees, consultants and third parties, to protect our confidential and proprietary information. In addition to contractual measures, we try to protect the confidential nature of our proprietary information using commonly accepted physical and technological security measures. Such measures may not, for example, in the case of misappropriation of a trade secret by an employee or third party with authorized access, provide adequate protection for our proprietary information. Our security measures may not prevent an employee or consultant from misappropriating our trade secrets and providing them to a competitor, and recourse we take against such misconduct may not provide an adequate remedy to protect our interests fully. Unauthorized parties may also attempt to copy or reverse engineer certain aspects of our products that we consider proprietary. Enforcing a claim that a party illegally disclosed or misappropriated a trade secret can be difficult, expensive and time-consuming, and the outcome is unpredictable. Even though we use commonly accepted security measures, trade secret violations are often a matter of state law, and the criteria for protection of trade secrets can vary among different jurisdictions.…

Many of our employees and consultants were previously employed at or engaged by other medical device, biotechnology or pharmaceutical companies, including our competitors or potential competitors, hospitals or other third parties. Some of these employees, consultants and contractors may have executed proprietary rights, non-disclosure and non-competition agreements in connection with such previous employment. Although we try to ensure that our employees and consultants do not use the intellectual property, proprietary information, know-how or trade secrets of others in their work for us, we may be subject to claims that we or these individuals have, inadvertently or otherwise, misappropriated the intellectual property or disclosed the alleged trade secrets or other proprietary information, of these former employers, competitors or other third parties. Additionally, we may be subject to claims from third parties challenging our ownership interest in or inventorship of intellectual property we regard as our own, based on claims that our agreements with employees or consultants obligating them to assign intellectual property to us are ineffective or in conflict with prior or competing contractual obligations to assign inventions to another employer, to a former employer, or to another person or entity.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
