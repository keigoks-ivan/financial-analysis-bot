你是 stock-analyst v20 DD 的證據採集子 agent。標的：TMDX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - TMDX TransMedics Group antitrust OR monopoly investigation 2026
  - TransMedics Group regulation OR regulatory scrutiny Medical Devices / Organ Transplant Logistics 2026
  - TMDX TransMedics Group DOJ OR FTC OR EU competition 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm｜as_of：2026-02-24
<<<
Item 3. Legal Proceedings.
On February 14, 2025, a class action captioned Jewik v. TransMedics Group, Inc., et al., Case No. 1:25-cv-10385, was filed against the Company and certain of its current and former officers in the U.S. District Court for the District of Massachusetts. The complaint purported to assert claims pursuant to Sections 10(b) and 20(a) of the Exchange Act and SEC Rule 10b-5 promulgated thereunder, seeking unspecified damages on behalf of a putative class of investors who purchased or otherwise acquired the Company’s shares between the Class Period, February 28, 2023 and January 10, 2025.
On April 2, 2025, another purported stockholder filed a putative class action lawsuit against the Company and certain of its current and former officers, also in the U.S. District Court for the District of Massachusetts (Collins v. TransMedics Group, Inc., et al., Case No. 1:25-cv-10778). The Collins complaint alleged claims substantially similar to those alleged in the Jewik action and also sought unspecified damages. On May 22, 2025, the court consolidated the Jewik and Collins actions and appointed the Peace Officers’ Annuity and Benefit Fund of Georgia and Oguzhan Altun as lead plaintiffs, or the Lead Plaintiffs.
On August 8, 2025, Lead Plaintiffs filed a consolidated amended complaint. Like the earlier-filed complaints, the amended complaint purports to assert claims pursuant to Sections 10(b) and 20(a) of the Exchange Act and Rule 10b-5, on behalf of a putative class of investors who purchased or otherwise acquired the Company’s shares during the Class Period. Lead Plaintiffs seek unspecified damages allegedly caused by purported misstatements and omissions contained in our 2022 Annual Report, certain earnings calls, and other public statements. The amended complaint claims these alleged statements and omissions operated to artificially inflate the price paid for our common stock during the Class Period. On October 7, 2025, defendants filed a motion to dismiss the amended complaint for failure to state a claim.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm｜as_of：2026-02-24
<<<
The national competent authorities in each member state oversee and enforce compliance with the standards set out in the MDR against relevant economic operators (including device manufacturers, importers, authorized representatives and distributors). Under the MDR, national competent authorities can inform other national competent authorities, the European Commission and Notified Bodies, as applicable, of certain non-compliances.

Under the MDR, a medical device placed on the market in the European Union must meet the applicable General Safety and Performance Requirements, or GSPRs, laid down in Annex I of the MDR. Similar to the U.S. system, medical devices are classified into one of four classes based on risk: I, IIa, IIb and III, with class I representing the lowest risk products and class III the highest risk products. One of the most fundamental GSPRs is that a medical device must be designed and manufactured in such a way that it will not compromise the clinical condition or safety of patients, or the safety and health of users and others (provided that any risks posed are acceptable when weighted against the benefits). In addition, the GSPRs include (but are not limited to) that the device must achieve the performances intended by the manufacturer, be designed, manufactured and packaged in a suitable manner and the manufacturer must establish, implement, document and maintain a risk management plan. The European Commission has adopted various standards applicable to medical devices, referred to as harmonized standards. While not mandatory, compliance with these harmonized standards is often viewed as the easiest way to satisfy the GSPRs as a practical matter.…

If such an investigation is necessary, and will be conducted in the UK, the manufacturer must submit a notification to the MHRA before the investigation is due to begin, and such a clinical investigation may only proceed provided no grounds for objection are raised by the MHRA within the statutory review time constraint. The manufacturer must also obtain ethics committee approval for the investigation.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1756262/000119312526067032/tmdx-20251231.htm｜as_of：2026-02-24
<<<
Internationally, the regulatory requirements relating to product defects may vary. A regulatory authority in a specific country may request or require a product recall while others may not. Within the European Union, competent authorities are required without delay to take corrective action against a device (including withdrawal/recall of a device) and notify other national competent authorities, the European Commission and notified bodies (as applicable) of any devices that present an unacceptable risk to the health or safety of patients, users or other persons, or other aspects of the protection of public health. Other non-compliance with the MDR may also lead to corrective action being taken and notifications being sent if the non-compliance is not rectified within a given time period (as determined by the competent authority). Therefore, a recall in one EU member state may lead to recalls in the rest of the European Union.

To enforce compliance with the healthcare regulatory laws, certain enforcement bodies have recently increased their scrutiny of interactions between healthcare companies and healthcare providers, which has led to a number of investigations, prosecutions, convictions and settlements in the healthcare industry. For example, the member states of the European Union closely monitor perceived unlawful marketing activity by companies, including inducement to prescribe and the encouragement of off-label use of devices. Responding to investigations can be time-and resource-consuming and can divert management’s attention from the business. Additionally, as a result of these investigations, healthcare companies and healthcare providers may have to agree to additional compliance and reporting requirements as part of a consent decree or corporate integrity agreement. Any such investigation or settlement could increase our costs or otherwise have an adverse effect on our business. Even an unsuccessful challenge or investigation into our practices could cause adverse publicity and be costly to respond to.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
