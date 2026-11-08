你是 stock-analyst v20 DD 的證據採集子 agent。標的：ABNB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Airbnb product substitute technology threat 2026
  - Online Travel / Marketplace Platform alternative technology disruption 2026 2027
  - ABNB Airbnb technology obsolescence risk
  - Online Travel / Marketplace Platform next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm｜as_of：2026-02-12
<<<
Industry, Financial, and Insurance Risks Any decline or disruption in the travel and hospitality industries or economic downturn could materially adversely affect our business, results of operations, and financial condition.

We rely on a number of third-party payment service providers, including payment card networks, banks, payment processors, and payment gateways, to link us to payment card and bank clearing networks to process payments made by our guests and to remit payments to hosts on our platform. If these providers, some of whom are the sole providers of their particular service, become unable or unwilling to offer services on acceptable terms or at all, our business could be disrupted, requiring us to find alternatives providers and they may not be able to be replaced in a timely manner, or at all, or on favorable terms. Transitioning to new providers would demand significant resources and might not be well-received by users, potentially leading to losses and necessitating payments to hosts from our funds, which could materially adversely affect our business, results of operations, and financial condition.

Compliance Costs Compliance with diverse and evolving laws across jurisdictions is costly and complex, increasing our operational expenses and potential liabilities (including potential criminal or other penalties). For example, we incur significant operational costs to comply with requirements of jurisdictions and cities that have disparate requirements around tax collection, tax reporting, data sharing, host registration, limits on lengths of stays, and other regulations, each of which may require us to dedicate significant resources to provide the infrastructure and tools needed on our platform for our hosts to meet these legal requirements and for us to fulfill any obligations we may have. Environmental, health, and safety requirements have also become increasingly stringent, and our costs, and our hosts’ costs, to comply with such requirements may increase as a result. The complexity of our platform and changes required to comply with the large number of varying requirements can lead to constraints on supply as well as compliance gaps. Additionally, unclear and changing laws can deter hosts and 16 Table of Contents guests from using our platform, reduce supply and demand, and increase litigation risks, adversely affecting our business. Failure or delays in complying with laws, even if unclear or in dispute, could subject us to penalties, including fines, business disruption, and site blocking.

Non-compliance with PCI DSS or payment network rules could breach our contracts with payment processors, leading to fines, penalties, and potential loss of card processing capabilities. Payment networks may also change rules, causing operational disruptions and compliance challenges. We cannot guarantee the maintenance of our card acceptance privileges or the prevention of data or security breaches, illegal or improper use of our payments platform, or the theft, loss, or misuse of card data or the maintenance of card acceptance privileges.

Intellectual property disputes could lead to significant liabilities, force us to cease using certain technologies or branding, or require us to obtain costly licenses or develop alternative solutions. These outcomes could increase our expenses and reduce our competitiveness, adversely affecting our business, results of operations, and financial condition.

Since our founding, we have experienced rapid growth in consumer traffic to our platform. We rely on computer systems, hardware, software, technology infrastructure, and online sites and networks for both internal and external operations that are critical to our business (collectively, “IT Systems”). We own and manage some of these IT Systems but also rely on third-party IT Systems for certain operations, including payment processing and accounting. Significant consumer growth or third-party failures may require costly upgrades, potentially affecting our business, and if our systems and network infrastructure cannot be expanded or are not scaled to cope with increased demand or fail to perform, we could experience significant operational interruptions, including poor performance, incorrect payments, search ranking issues, unanticipated disruptions in service, slower response times, and delays in the introduction of new offerings, decreased customer satisfaction, and loss of users. Our reliance on the Internet and mobile networks could also lead to disruptions in access. Our IT Systems, including those from third-party providers, are also vulnerable to damage or interruption from natural disasters. For example, our San Francisco operations are at risk from earthquakes and power outages, which could disrupt business operations. Such disruptions could materially adversely impact our business, results of operations, and financial condition. We have experienced IT System failures from time to time.…

In addition to our proprietary technologies, we use AI and ML Technologies licensed from third parties. Our ability to continue to adopt, integrate, and use such technologies at the scale we may need may be dependent on access to specific third-party software, and infrastructure, such as processing hardware or third-party AI models, and we cannot control the quality, availability, or pricing of such third-party software and infrastructure, especially in a highly competitive environment. If any such third-party models, software, or infrastructure becomes incompatible with our offerings or unavailable for use or has degradations in performance, or if the providers of such services unfavorably change the terms on which their services are offered or terminate their relationship with us, our offerings may become less appealing to our customers. In addition, to the extent any third-party infrastructure or software is used as a vendor hosted service, any disruption, outage, or loss of information through such hosted services could disrupt our operations or offerings, damage our reputation, cause a loss of confidence in our offerings, or result in legal claims or proceedings, for which we may be unable to recover damages from the affected provider.

Inadvertent use of open source software can occur in software development in the Internet and technology industries. Such inadvertent use of open source software could expose us to claims of non-compliance with the applicable terms of the underlying licenses, which could lead to unforeseen business disruptions, including being restricted from offering parts of our platform which incorporate the software, being required to publicly release proprietary source code, being required to re-engineer parts of our code base to comply with license terms, or being required to extract the open source software at issue. Our exposure to these risks may be increased as a result of evolving our core source code base, introducing new offerings, integrating acquired-company technologies, or making other business changes, including in areas where we do not currently compete. Any of the foregoing could adversely impact the value or enforceability of our intellectual property, and materially adversely affect our business, results of operations, and financial condition.

We own and manage some IT Systems but also rely on third parties for a range of IT Systems, which include our infrastructure, and related products and services, including, among others, cloud computing services and other third parties for the provision of our community support and other critical operations. We face evolving cybersecurity risks that could impact the confidentiality, integrity, and availability of our and our third-party providers’ IT Systems and confidential information, including personal data and proprietary information if exposed. As we expand our technology use, enhance our AI and ML capabilities, and collaborate with third parties, managing these threats becomes more challenging. These risks come from diverse threat actors, such as state-sponsored organizations, opportunistic hackers and hacktivists, as well as through diverse attack vectors, such as social engineering/phishing, malware (including ransomware), malfeasance by company insiders, suppliers or providers, and human or technological error, and as a result of malicious code embedded in open source software, or misconfigurations, bugs, or other vulnerabilities in software and hardware that is integrated into our or our providers’ IT Systems, products, or services.…

We do not control the operation, physical security, or data security of any of these third-party providers, or their use of AI, ML, or other technologies in their products and services. Despite our efforts to use commercially reasonable diligence in the selection and retention of such third-party providers, such efforts may be insufficient or inadequate to prevent or remediate such risks. Some of our third-party providers, including our cloud computing providers and our payment processing partners, have been and may be subject to further intrusions, computer viruses, malicious software (such as ransomware), denial-of-service attacks, phishing attacks, sabotage, acts of vandalism, terrorism, or other misconduct, and incidents due to inadvertent error or malfeasance by employees, contractors, or other parties. There can be no assurance that our service providers will anticipate or prevent all types of attacks or that any security measures will be effective against all types of cybersecurity threats and risks. Our service providers are vulnerable to damage or interruption from power loss, telecommunications failures, fires, floods, earthquakes, hurricanes, tornadoes, and similar events, and they may be subject to financial, legal, regulatory, and labor issues, each of which may impose additional costs or requirements on us or prevent these third parties from providing services to us or our customers on our behalf.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABNB_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
