你是 stock-analyst v20 DD 的證據採集子 agent。標的：GILD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - GILD Gilead Sciences tariff section 232 2026
  - Gilead Sciences export control OR entity list Biotech / Specialty Pharma 2026
  - GILD Gilead Sciences China tariff OR trade restriction 2026
  - Biotech / Specialty Pharma tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm｜as_of：2026-02-24
<<<
In addition, the current U.S. Presidential administration has indicated that it plans to pursue changes to various regulatory policies from prior administrations, some of which have already started to be implemented. As a result, there is uncertainty as to how these and other potential legal and regulatory changes may impact our business. For example, the administration has taken a number of actions aimed at lowering U.S. drug prices and testing new Medicare and Medicaid payment models. President Trump also has pledged to impose tariffs on pharmaceuticals and other products, some of which have already started to be implemented. These tariffs and retaliatory measures taken by other nations in response may increase our costs and adversely impact the competitiveness of our products outside the U.S. Some of these policy changes may be subject to litigation or other challenge, increasing the uncertainty of their effects on our business. For more information, see Item 1A. Risk Factors “Our existing products are subject to pricing and reimbursement pressures from government agencies and other third parties, including required discounts and rebates.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/882095/000088209526000006/gild-20251231.htm｜as_of：2026-02-24
<<<
•U.S. Department of Commerce initiated an investigation on imports of pharmaceuticals and pharmaceutical ingredients, which may result in the current U.S. Presidential administration taking actions to impose potential tariffs or importation quotas in the pharmaceutical industry that could increase our manufacturing costs and adversely impact our supply chain resiliency and business competitiveness. For example, in September 2025, the U.S. Presidential administration announced plans to impose up to 100% tariffs on imported branded or patented pharmaceuticals, subject to certain exceptions. The specific impact remains uncertain at this time and is subject to the timing, scope and duration of any tariffs and actions imposed as well as broader tariffs and actions outside of the pharmaceutical industry.

•The current U.S. Presidential administration has indicated that it plans to pursue additional policies aimed at lowering prescription drug costs. The administration has issued multiple executive orders and statements that illustrate the intent to require pharmaceutical manufacturers to offer U.S. prices based on most favored-nation (“MFN”) lowest prices and that direct specified agency heads to take certain actions if significant progress towards such MFN prices is not achieved. In July 2025, the President sent letters to Gilead and other pharmaceutical manufacturers outlining the steps the President believes pharmaceutical manufacturers must take to bring down the prices of prescription drugs in the U.S. to match the MFN price offered in other developed nations. The administration has announced agreements with certain manufacturers, including Gilead, around these issues and has stated that it has paused the implementation of tariffs on pharmaceuticals to allow for negotiation of agreements with additional manufacturers. In December 2025, Gilead reached an agreement with the administration to (1) pause the imposition of Section 232 tariffs on Gilead for three years, (2) implement MFN prices in Medicaid for select existing and future launched products, (3) set a new direct-to-patient price for Epclusa and (4) return a portion of increased international revenues to the U.S. if the U.S. government is successful in increasing drug prices abroad.…

The healthcare industry is subject to various federal, state and international laws and regulations pertaining to drug approval, manufacturing, reimbursement, rebates, price reporting, healthcare fraud and abuse, and data privacy and security. In the U.S., these laws include anti-kickback and false claims laws, the Federal Food, Drug, and Cosmetic Act, laws and regulations relating to the Medicare and Medicaid programs and other federal and state programs, such as the Medicaid Rebate Statute and the 340B statute, laws that regulate written and verbal communications about our products, individual state laws relating to pricing and sales and marketing practices, the Health Insurance Portability and Accountability Act and other federal and state laws relating to the privacy and security of health information, including the Department of Justice Final Rule on Preventing Access to U.S. Sensitive Personal Data and Government-Related Data by Countries of Concern or Covered Persons, which impacts how and where clinical and other sensitive data is shared. Actual or alleged violations of these laws or any related regulations may be punishable by criminal and/or civil sanctions, including, in some instances, substantial fines, civil monetary penalties, exclusion from participation in federal and state healthcare programs, including Medicare, Medicaid and U.S. Department of Veterans Affairs and U.S.…

•Changes in trade policies by the U.S. or foreign governments, which may result in protectionist measures, such as new or increased sanctions, tariffs (such as the country-specific tariffs and related retaliatory actions implemented by the U.S. and other countries), embargoes, import and export licensing requirements or other trade restrictions, or the threat of such restrictions.

We are undertaking significant multi‑year capital investments to expand our U.S. manufacturing capabilities and accelerate R&D, including our initiative to invest $32 billion in the U.S. through 2030. These investments are subject to numerous risks, including construction and commissioning delays, cost inflation, supply chain constraints, contractor performance, permitting and zoning challenges and the availability of skilled labor, and we may not complete our announced investments on a timely basis or at all. New or expanded facilities must meet cGMP and other regulatory requirements, are subject to FDA and other inspections, process validation and qualification, and their construction depends on third-party suppliers and partners whose performance we do not control. Any failure, delay, observation or remediation requirement could defer or limit production, increase costs or result in enforcement actions or other liabilities. We may not realize anticipated economic, employment, productivity, scale or innovation benefits, anticipated cost savings or future growth, and our reputation may be damaged, if these projects are delayed or unable to be completed in a cost-effective manner. This could also lead to underutilized assets, inventory write‑offs or asset impairments.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GILD_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
