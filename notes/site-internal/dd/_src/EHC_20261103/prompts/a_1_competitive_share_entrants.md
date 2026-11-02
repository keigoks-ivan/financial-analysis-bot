你是 stock-analyst v20 DD 的證據採集子 agent。標的：EHC。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - EHC Encompass Health market share gaining OR losing 2026
  - Encompass Health new entrant OR displace threat Medical Care Facilities 2026
  - EHC competitor design win 2026
  - Encompass Health vs Medical Care Facilities peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm｜as_of：2026-02-26
<<<
•Growth. We actively pursue capacity expansions through the development of new inpatient rehabilitation hospitals and additions to existing hospitals each year. In addition, our same store hospitals have other organic growth opportunities, including secular shifts in aging demographic populations, the ability to capture market share, and the maturation of newly opened locations.

Given the significant number of stroke patients in need of post-acute care, we will continue working to build our stroke market share. As of December 31, 2025, 148 of our 173 hospitals held stroke-specific certifications that required us to demonstrate effective use of evidence-based clinical practice guidelines to manage and optimize stroke care and an organized approach to performance measurement and evaluation of clinical outcomes.

Competitive Strengths We believe we differentiate ourselves from our competitors based on, among other things, the quality of our clinical outcomes, our cost-effectiveness, our financial strength, and our extensive application of technology. We also believe our competitive strengths discussed below give us the ability to adapt and succeed in a healthcare industry facing regulatory uncertainty around attempts to improve outcomes and reduce costs.

Competition The inpatient rehabilitation industry, outside of our leading position, is highly fragmented. Our inpatient rehabilitation hospitals compete primarily with rehabilitation units, most of which are within acute-care hospitals, in the markets we serve. An acute-care hospital operating its own unit, particularly one owned or operated by a large public company or not-for-profit that has a dominant position in the local market, can be a formidable competitor because 92% of our patients come from acute-care 3 hospitals. There are several privately held companies offering post-acute rehabilitation services that compete with us in select geographic markets. In addition, there is a public company that is primarily focused on other post-acute care services but also operates 38 inpatient rehabilitation hospitals across the country. Other providers of post-acute care services compete for some rehabilitation patients. For example, nursing homes may market themselves as offering certain rehabilitation services, particularly to patients not in need of intensive rehabilitation therapy, even though those nursing homes are not required to offer the same level of care and are not licensed as hospitals.…

Fostering a Strong Culture Inclusion and Cultural Education For 2025, we focused on centralizing inclusion and cultural programming and providing education our employees need to care for our patients. Our cultural awareness programs are centered around quality and clinical excellence to ensure our employees are supported and trained to meet the culturally unique needs of our patients. As a result of this training and other initiatives, the organization improved on the employee engagement survey score relating to culturally competent patient care. This engagement measure is significant from a company perspective because we see a positive correlation around the question of “Our company equips me/staff with the resources to deliver Culturally Competent Care to our patients” and our net promotor score which measures patient satisfaction.

We potentially face opposition any time we initiate a project requiring a new or amended CON or seek to acquire an existing CON. This opposition may arise either from competing national or regional companies or from local hospitals or other providers which file competing applications or oppose the proposed CON project. Opposition to our applications may delay or prevent our future addition of beds or hospitals in given markets or increase our costs in seeking those additions. The necessity for these approvals serves as a barrier to entry and has the potential to limit competition for us (in markets where we hold a CON) and for other providers (in markets where we are seeking a CON). We have generally been successful in obtaining CONs or similar approvals, although there can be no assurance we will achieve similar success in the future, and the likelihood of success varies by locality and state.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm｜as_of：2026-02-26
<<<
We face intense competition for patients from other healthcare providers. We operate in the competitive, fragmented inpatient rehabilitation industry. Although we are the nation’s largest owner and operator of inpatient rehabilitation hospitals in terms of patients treated, revenues, and number of hospitals, in any particular market we may encounter competition from local or national entities with longer operating histories or other competitive advantages. For example, acute-care hospitals, including those owned and operated by large public companies, may choose to expand or begin offering post-acute rehabilitation services. Given that approximately 92% of our hospitals’ admissions come from acute-care hospitals, that increase in competition could materially and adversely affect our admission 34 referrals in the related markets. There are also large acute-care systems that may have more resources available to compete than we have. Other providers of post-acute care services may attempt to become competitors in the future. For example, nursing homes frequently market themselves as offering certain rehabilitation services, even though nursing homes are not required to offer the same level of care, and are not licensed, as hospitals.

There can be no assurance this competition, or other competition which we may encounter in the future, will not adversely affect our business, financial position, results of operations, or cash flows. In addition, from time to time, there are efforts in states with certificate of need (“CON”) laws to weaken those laws, which could potentially increase competition in those states. For example, in 2023, South Carolina enacted legislation to repeal CON regulations for several provider types, including IRFs. Conversely, competition and statutory procedural requirements in some CON states may inhibit our ability to expand our operations in those states. For a breakdown of the CON status of the states and territories in which we have operations, see Item 2, Properties.

Our operations are dependent on the efforts, abilities, and experience of our medical personnel, such as physical therapists, occupational therapists, speech pathologists, nurses, and other healthcare professionals. We compete with other healthcare providers in recruiting and retaining qualified personnel responsible for the daily operations of each of our locations. The lack of availability of clinical personnel is a significant ongoing operating issue facing healthcare providers and unexpected labor market disruptions, like the COVID-19 pandemic, can exacerbate the issue. The operating conditions associated with the pandemic significantly affected the availability and turnover of clinical staff and, in turn, increased staffing costs. Availability of clinical staff, elevated turnover and staffing costs continue to be a challenge for us and other healthcare providers. The availability of staff may be exacerbated if immigration is significantly limited in the future. Staffing shortages or retention concerns in one or more markets in which we operate have required and may again require us to enhance wages and benefits to recruit and retain qualified personnel or to contract for more expensive temporary personnel. We also depend on the available labor pool of semi-skilled and unskilled employees in each of the markets in which we operate. While we do not employ physicians, we do rely on the availability of physicians to treat patients in our hospitals.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
