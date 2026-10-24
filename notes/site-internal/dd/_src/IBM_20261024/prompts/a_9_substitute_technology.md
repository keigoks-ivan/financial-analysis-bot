你是 stock-analyst v20 DD 的證據採集子 agent。標的：IBM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - product substitute technology threat 2026
  - alternative technology disruption 2026 2027
  - IBM technology obsolescence risk
  - next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-24）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/51143/000005114326000010/ibm-20251231.htm｜as_of：2026-02-24
<<<
Failure of Innovation Initiatives Could Impact the Long-Term Success of the Company: IBM has moved into areas, including those that incorporate or utilize hybrid cloud, AI, quantum and other disruptive technologies, in which it can differentiate itself through responsible innovation, by leveraging its investments in R&D and attracting a successful developer ecosystem. If IBM is unable to continue its cutting-edge innovation in a highly competitive and rapidly evolving environment or is unable to commercialize such innovations, expand and scale them with sufficient speed and versatility or is unable to attract a successful developer ecosystem, the company could fail in its ongoing efforts to maintain and increase its market share and its profit margins.

Risks from Investing in Growth Opportunities Could Impact the Company’s Business: The company continues to invest significantly in key strategic areas, including AI, to drive revenue growth and market share gains. Client adoption rates and viable economic models are less certain in the high-value, highly competitive, and rapidly-growing segments. Additionally, emerging business and delivery models may unfavorably impact demand and profitability for our other products or services. If the company does not adequately and timely anticipate and respond to changes in customer and market preferences, competitive actions, disruptive technologies, emerging business models and ecosystems, the client demand for our products or services may decline or IBM’s costs may increase.

Risks to the Company from Acquisitions, Alliances and Divestitures Include Integration Challenges, Failure to Achieve Objectives, the Assumption or Retention of Liabilities and Higher Debt Levels: The company has made and expects to continue to make acquisitions, alliances and divestitures. Such transactions present significant challenges and risks and there can be no assurances that the company will manage such transactions successfully, that strategic objectives will be achieved or that strategic opportunities will be available to the company on acceptable terms or at all. With respect to acquisitions and alliances, the related risks include the company failing to achieve anticipated revenue improvements and cost savings, the failure to retain key personnel or strategic relationships of acquired companies, the assumption of liabilities related to litigation or other legal proceedings involving the businesses in such transactions, and delays in obtaining, or the failure to obtain, necessary governmental or regulatory approvals, as well as the failure to close planned transactions. Such transactions may require the company to secure financing and any significant disruption or turmoil in the capital markets could have an adverse effect on IBM’s ability to access the capital markets at favorable terms. From time to time, the company divests or attempts to divest assets that are no longer central to its strategic objectives.…

Product and Service Quality Issues Could Impact the Company’s Business and Operating Results: The company has rigorous quality control standards and governance processes intended to prevent, detect and correct errors, malfunctions and other defects in its products and services. If errors, malfunctions, defects or disruptions in service are experienced by customers or in the company’s operations there could be negative consequences that could impact customers’ business operations and harm the company’s business’s operating results.

The company regularly addresses cybersecurity attacks and vulnerabilities. Cybersecurity attacks or other security incidents, including industry-wide incidents, have or could result in, for example, one or more of the following: unauthorized access to, disclosure, modification, misuse, loss, or destruction of company, customer, or other third-party data or systems; theft or import or export of sensitive, regulated, or confidential data including personal information and intellectual property, including key innovations in AI, quantum, or other disruptive technologies; the loss of access to critical data or systems through ransomware, crypto mining, destructive attacks or other means; and business delays, service or system disruptions or denials of service.

Cybersecurity attacks or other catastrophic events resulting in disruptions to or failures in power, information technology, communication systems or other critical infrastructure could result in interruptions or delays to company, customer, or other third-party operations or services, financial loss, injury or death to persons or property, potential liability, and damage to brand and reputation. Although the company continuously takes significant steps to mitigate 7 Table of Contents cybersecurity risk across a range of functions, such measures can never eliminate the risk entirely or provide absolute security.

As a global enterprise, the regulatory environment with regard to cybersecurity and data protection issues is increasingly complex and will continue to impact the company’s business, including through increased risk, increased costs, and expanded or otherwise altered compliance obligations, including with respect to the increased regulatory activity around the security of critical infrastructure, connected devices, customer industries (e.g., financial services) and various customer and government supply chain security programs. As the reliance on data grows for the company and our clients, the potential impact of regulations on the company’s business, risks, and reputation will grow accordingly. The enactment and expansion of cybersecurity and data protection laws, regulations and standards around the globe will continue to result in increased compliance costs, including due to an increased focus on international data transfer mechanisms and data location; increased cybersecurity requirements and reporting obligations; the lack of harmonization of such laws and regulations; the increase in associated litigation and enforcement activity by governments and private parties; the potential for damages, fines and penalties and debarment; and the potential regulation of new and emerging technologies. Any additional costs and penalties associated with increased compliance, enforcement, and risk reduction could make certain offerings less profitable or increase the difficulty of bringing certain offerings to market or maintaining certain offerings.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
