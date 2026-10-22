你是 stock-analyst v20 DD 的證據採集子 agent。標的：COF。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Capital One Financial product substitute technology threat 2026
  - Credit Services alternative technology disruption 2026 2027
  - COF Capital One Financial technology obsolescence risk
  - Credit Services next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm｜as_of：2026-02-19
<<<
Table of Contents •Geopolitical conflicts or instabilities, such as the war in Ukraine, the ongoing conflict in the Middle East and the political instability in Venezuela and increased geopolitical tensions between the U.S. and China; •Trade wars, trade barriers, tariffs, economic sanctions, labor shortages and disruptions of global supply chains, including their impacts on the auto industry; •The effects of stalemates in the U.S. government, including government shutdowns whether recurring, prolonged or otherwise, developments related to the U.S. federal debt ceiling, default by the U.S. government on its debt obligations, or related credit-rating downgrades; •Inflation and deflation, including the effects of related governmental responses; •Concerns over a potential recession, which may lead to adjustments in spending patterns; •Technology-driven disruption of certain industries, such as those due to advances in AI, robotics and cryptocurrency; •Adverse developments impacting the U.S.…

Similar to other large corporations in our industry, we are exposed to operational risk that can manifest itself in many ways, such as errors in execution, inadequate processes, inaccurate models, faulty or disabled technological infrastructure, malicious disruption and fraud by employees or persons outside of our company, whether through attacks on Capital One directly, or on our third-party service providers or customers. In addition, the increased use of near real-time money movement solutions and the use of AI, as well as other emerging technologies, increases the complexity of preventing, detecting and recovering fraudulent transactions. We are also heavily dependent on the security, capability, integrity and continuous availability of the technology systems and networks that we use to manage our internal financial and other systems, monitor risk and compliance with regulatory requirements, provide services to our customers, develop and offer new products and communicate with stakeholders. In addition, our employees, service providers, partners and other third parties with whom we interact may expose us to certain risks as a result of human error or misconduct. For example, errors in processing wire transfers may result in the inadvertent release of funds in incorrect amounts or to incorrect recipients, and we may be unable to recover such funds.…

We also face the risk of adverse customer impacts and business disruption arising from the execution of strategic initiatives and operational plans we may pursue across our operations. For example, when we launch a new product, service or platform for the delivery or distribution of products or services, acquire or invest in a business or make changes to an existing product, service or delivery platform, there is the risk of execution issues related to changes to technology, operations or processes. These issues could be driven by insufficient mitigation of operational risks associated with the change implementation, inadequate training, failure to account for new or changed requirements, or failure to identify or address impacted downstream processes. Furthermore, ineffective change management oversight and governance over the execution of our key projects and initiatives could expose us to operational, strategic and reputational risk and could negatively impact customers or our financial performance. In addition, we may experience increased costs, compliance issues, and/or disruptions due to our hybrid work model, which could also affect our ability to operate effectively.

If we do not maintain the necessary operational, technological and organizational infrastructure to operate our business, including to maintain the resiliency and security of that infrastructure, our business and reputation could be materially adversely affected. We also are subject to disruptions to our systems or networks arising from events that are wholly or partially beyond our control, which may include computer viruses; computer, telecommunications, network, utility, electronic or physical infrastructure outages; bugs, errors, insider threats, design flaws in systems, networks or platforms; availability and quality of vulnerability patches from key vendors, cyber-attacks and other security incidents, natural disasters, other damage to property or physical assets, or events arising from local or larger scale politics, including civil unrest, terrorist acts and military conflict. Any failure to maintain our infrastructure or prevent disruption of our systems, networks and applications could diminish our ability to operate our businesses, service customer accounts and protect customers’ information, or pay our debts in a timely manner (which could limit our access to future funding), or result in potential liability to customers and business partners, reputational damage, regulatory intervention and customers’ loss of confidence in our businesses, any of which could result in a material adverse effect.

We also rely on the business infrastructure and systems of third-party service providers (and their supply chains) with which we do business and/or to whom we outsource the operation, maintenance and development of our information technology and communications systems. Other than the ongoing integration of Discover, we have substantially migrated primarily all aspects of our core information technology infrastructure and systems and customer-facing applications to third-party cloud infrastructure platforms, principally AWS. If we fail to architect, administer or oversee these environments in a well-managed, secure and effective manner, or if such platforms become unavailable, are disrupted, fail to scale, do not operate as designed or do not meet their service level agreements for any reason, we may experience unplanned service disruption or unforeseen costs which could result in material harm to our business and operations. We must successfully develop and maintain information, financial reporting, disclosure, privacy, data protection, data security and other controls adapted to our reliance on outside platforms and providers. Weakness in our third-party service providers’ processes or controls could impact our ability to deliver 32 Capital One Financial Corporation (COF)

Any disruptions, failures or inaccuracies of our operational processes, technology systems, networks and models, including those associated with improvements or modifications to such technology systems, networks and models, or failure to identify or effectively respond to operational risks in a timely manner and continue to deliver our services through an operational disruption, could cause us to be unable to market, deliver and manage our products and services, manage our risk, meet our regulatory obligations, report our financial results in a timely and accurate manner, or pay our debts in a timely manner (which could limit our access to future funding), all of which could have a negative impact on our results of operations. In addition, our ongoing investments in technology may increase our expenses. As our business develops, changes or expands, additional expenses can arise as a result of a reevaluation of business strategies or risks, management of outsourced services, asset purchases or other acquisitions, structural reorganization, compliance with new laws or regulations, the integration of newly acquired businesses or the prevention or occurrence of cyber-attacks and other security incidents. If we are unable to successfully manage our expenses, our financial results will be negatively affected.…

An actual, suspected, threatened or alleged disruption or breach, including as a result of a cyber-attack, or media (including social media) reports of alleged or perceived security vulnerabilities or incidents at Capital One or at our service providers, could result in significant legal and financial exposure, regulatory intervention, litigation, enforcement actions, remediation costs, card reissuance, inability to timely pay our debts (and consequently limit our access to future funding), operational disruptions, supervisory liability, damage to our reputation or loss of confidence in the security of our systems, products and services that could adversely affect our business. Moreover, we are subject to varied cybersecurity laws and regulations and incident reporting requirements, and may in the future be subject to new cybersecurity laws and regulations and incident reporting requirements, which could require us to publicly disclose certain information about certain cybersecurity incidents before they have been resolved or fully investigated, and any delays in receiving timely information from impacted service providers and business partners can affect our ability to fully meet applicable disclosure requirements for a given incident. There can be no assurance that unauthorized access or cyber incidents will not occur or that we will not suffer material losses in the future.…

We face risks from catastrophic events. Natural disasters, geopolitical events, supply chain issues and other catastrophic events can have widespread and unpredictable impacts on global society, economic conditions and consumer and business behavior, which may reoccur or occur over an extended duration. These events could harm our employees, business and infrastructure, including our information technology systems and third-party platforms. Our ability to conduct business may be adversely affected by a disruption in the infrastructure that supports our business and the communities where we are located, which are concentrated in the Northern Virginia, New York and Chicago metropolitan areas, Richmond, Virginia, Plano, Texas and the Philippines. This may include a disruption involving damage or loss of access to a physical site, cyber-attacks and other security incidents, terrorist activities, the occurrence or worsening of disease outbreaks or pandemics, natural disasters, extreme weather events, electrical outage, environmental hazards, disruption to technological infrastructure, communications or other services we use, our employees or third parties with whom we conduct business. Our business, financial condition and results of operations may be impacted by any such disruption and our ability to implement corresponding response measures quickly.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/parts/axes_7.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
