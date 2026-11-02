你是 stock-analyst v20 DD 的證據採集子 agent。標的：EHC。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Encompass Health product substitute technology threat 2026
  - Medical Care Facilities alternative technology disruption 2026 2027
  - EHC Encompass Health technology obsolescence risk
  - Medical Care Facilities next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm｜as_of：2026-02-26
<<<
In some cases, we believe the reviewing party is not merely challenging the sufficiency of the medical record but is substituting its judgment of medical necessity for that of the attending physician or imposing documentation or other requirements that are not set out in the regulations. We argue that doing so is inappropriate and has no basis in law. When the government or its contractors reject the medical judgment of physicians or impose documentation and other requirements beyond the language of the statutes and regulations, patient access to inpatient rehabilitation as well as our Medicare reimbursement from the related claims may be adversely affected.

We expend significant capital to protect against cybersecurity threats, including denial of service attacks, email phishing schemes, hacking, advanced persistent threats, malware, and ransomware. Substantial additional expenditures may be required to respond to and remediate any problems caused by breaches, including the unauthorized access to or theft of patient data and protected health information stored in our information systems and the introduction of computer malware or ransomware to our systems. We also provide our employees annual training and regular reminders on important measures they can take to prevent breaches and other cyber threats, including phishing schemes. We routinely identify attempts to gain unauthorized access to our systems. However, given the rapidly evolving nature and proliferation of cyber threats, there can be no assurance our training and network security measures or other controls will detect, prevent or remediate security or data breaches in a timely manner or otherwise prevent unauthorized access to, damage to, or interruption of our systems and operations. For example, it has been widely reported that many well-organized international interests, in certain cases with the backing of sovereign governments, are targeting the theft of patient information and the disruption of healthcare services through the use of advanced persistent threats and ransomware attacks.…

ACE-IT, our enterprise-level clinical information system, is subject to a licensing, implementation, technology hosting, and support agreement with Oracle Health. In addition, we have a number of partners and non-software vendors with whom we share data in order to provide patient care and otherwise operate our business. Our inability, or the inability of our partners or vendors, to continue to secure, maintain and upgrade information systems, software, and hardware could disrupt or reduce the efficiency of our operations, including affecting patient care. On February 21, 2024, Change Healthcare, a subsidiary of UnitedHealth Group that acts as an intermediary for processing of our payment claims for all payors, notified us of a cybersecurity incident affecting some of its systems. In response to the incident, both we and Change Healthcare severed those business service connections between our systems and Change Healthcare’s. We promptly conducted forensics on our systems based on the shared information regarding this Change Healthcare incident and did not identify any compromise or unauthorized access of our systems or networks. However, the incident did affect our ability to submit any claims for payment for a period of time until we implemented alternative modes for submissions.…

The financial and operational strength, access to credit, and general liquidity of a joint venture partner may affect the growth or performance for the associated inpatient rehabilitation hospital, and in a few instances in the past has done so. Our joint venture partners may be, and in the past some have been, unable or unwilling, at the time of our request, to make capital contributions to fund their proportional shares of operating or capital expenditures that we believe are in the best interest of the joint ventures. The delay or inability of a joint venture to undertake a funding expenditure could affect the growth or performance of that hospital. Should a joint venture partner close its acute-care hospital operating in the market with the joint venture inpatient rehabilitation hospital, we would likely suffer a significant referral disruption or decrease in that market, particularly in smaller markets where the acute-care hospital that is closing is the primary or only hospital.

We may undertake strategic acquisitions from time to time. Prior to consummation of any acquisition, the acquired business will have operated independently of us, with its own procedures, corporate culture, locations, employees and systems. We expect to integrate acquired businesses into our existing business utilizing certain common information systems, operating procedures, administrative functions, financial and internal controls and human resources practices to the extent practicable. There may be substantial difficulties, costs and delays involved in the integration of an acquired business with our business. Additionally, an acquisition could cause disruption to our business and operations and our relationships with customers, employees and other parties. In some cases, the acquired business has itself grown through acquisitions, and there may be legacy systems, operating policies and procedures, and financial and administrative practices yet to be fully integrated. To the extent we are attempting to integrate multiple businesses at the same time, we may not be able to do so as efficiently or effectively as we initially anticipate. The failure to successfully integrate on a timely basis any acquired business with our existing business could have an adverse effect on our business, financial position, results of operations, and cash flows.

Our operations are dependent on the efforts, abilities, and experience of our medical personnel, such as physical therapists, occupational therapists, speech pathologists, nurses, and other healthcare professionals. We compete with other healthcare providers in recruiting and retaining qualified personnel responsible for the daily operations of each of our locations. The lack of availability of clinical personnel is a significant ongoing operating issue facing healthcare providers and unexpected labor market disruptions, like the COVID-19 pandemic, can exacerbate the issue. The operating conditions associated with the pandemic significantly affected the availability and turnover of clinical staff and, in turn, increased staffing costs. Availability of clinical staff, elevated turnover and staffing costs continue to be a challenge for us and other healthcare providers. The availability of staff may be exacerbated if immigration is significantly limited in the future. Staffing shortages or retention concerns in one or more markets in which we operate have required and may again require us to enhance wages and benefits to recruit and retain qualified personnel or to contract for more expensive temporary personnel. We also depend on the available labor pool of semi-skilled and unskilled employees in each of the markets in which we operate. While we do not employ physicians, we do rely on the availability of physicians to treat patients in our hospitals.…

We may be more vulnerable to the effects of a public health emergency than other businesses due to the nature of our patients, and a regional or global socio-political, weather or other catastrophic event could severely disrupt our business.

The majority of our patients are elderly individuals with complex medical challenges, many of whom may be more vulnerable than the general public during a contagious disease outbreak or other public health catastrophe. Our employees also may be at greater risk of contracting contagious diseases due to their exposure to vulnerable patients. For example, if another pandemic were to occur, we could suffer significant losses to our patient population or a reduction in the availability of our employees and, at a high cost, be required to replace affected workers. Local, regional or national governments might limit or ban public interactions to halt or delay the spread of diseases causing business disruptions and the temporary suspension of our services. Accordingly, certain public health catastrophes could have a material adverse effect on our financial condition and results of operations.

Legislators and regulators at the international, national, regional and local levels have adopted and are expected to continue to adopt legal requirements ultimately designed to reduce greenhouse gas emissions and to promote a transition to a lower-carbon economy. For instance, a number of recently enacted laws and regulations impose on companies broad climate-related disclosure requirements, such as California’s suite of statutes adopted in 2023 known as the “climate accountability package,” to track and report matters associated with greenhouse gas emissions, alternative energy usage, energy conservation, and the transition to a lower-carbon economy. Additionally, a number of states and localities have passed building energy performance standards that impose reporting and energy use reduction obligations on commercial buildings, including our hospitals. These types of laws and regulations have proliferated in recent years and are likely to continue to do so in the future. These climate-related laws and regulations have increased our costs associated with compliance and are likely to continue to do so in the future. Additionally, the costs that other companies incur to comply with these types of laws and regulations are likely to be passed on to us, which would increase the cost of the goods and services that we purchase from vendors and suppliers.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
