你是 stock-analyst v20 DD 的證據採集子 agent。標的：AMKR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Amkor Technology product substitute technology threat 2026
  - Semiconductor Equipment & Materials alternative technology disruption 2026 2027
  - AMKR Amkor Technology technology obsolescence risk
  - Semiconductor Equipment & Materials next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-20）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm｜as_of：2026-02-20
<<<
General Risk Factors •natural disasters and other calamities, health conditions or pandemics, political instability, hostilities or other disruptions.

Since our business is, and will continue to be, dependent on the requirements of semiconductor companies for outsourced packaging and test services, any downturn in the semiconductor industry or any other industry that uses a significant number of semiconductor devices, such as communications, computing, automotive and industrial or consumer electronics, could have a material adverse effect on our business and operating results. During downturns, we have experienced, among other things, reduced demand, excess capacity and reduced sales. For example, the Covid-19 pandemic disrupted demand in the automotive and industrial end market in 2020, and during 2019, there was weakness in the general market and an inventory correction in the smartphone market.

We obtain the materials and equipment required for the packaging and test services performed by our factories from various vendors. We source most of our materials, including critical materials such as leadframes, laminate substrates and gold wire, from a limited group of suppliers. A disruption to the operations of one or more of our suppliers could extend lead times for materials and equipment and have a negative impact on our business. For example, the Covid-19 pandemic and resulting supply chain disruptions and economic turbulence created extended lead times for some materials and equipment, and furthermore, fire, severe weather, earthquakes, flooding and tsunamis in the past have impacted the supply of specialty chemicals, substrates, silicon wafers, equipment and other supplies to the electronics industry.

In addition, we purchase the majority of our materials on a purchase order basis. Our business may be harmed if we cannot obtain materials and other supplies from our vendors in a timely manner, in sufficient quantities, at acceptable quality or at competitive prices or are unable to increase our prices sufficiently to recover inflationary price increases in materials or supplies. Some of our customers are also dependent on a limited number of suppliers for certain materials and silicon wafers. Shortages or disruptions in our customers’ supply channels, including any disruptions arising out of the conflicts in Ukraine and Israel or other future conflicts, could have a material adverse effect on our business, financial condition, results of operations and cash flows.

•the payment of dividends and other payments by non-U.S. subsidiaries may be subject to prohibitions, limitations or taxes in local jurisdictions; •fluctuations in currency exchange rates, particularly the U.S. dollar to Japanese yen exchange rate for our operations in Japan; •political and social conditions, and the potential for civil unrest, terrorism or other hostilities (such as the ongoing conflicts in Ukraine and Israel); •disruptions or delays in shipments caused by customs brokers or government agencies; •difficulties in attracting and retaining qualified personnel and managing foreign operations, including foreign labor disruptions; •difficulty in enforcing contractual rights and protecting our intellectual property rights; •potentially adverse tax consequences resulting from tax laws in the United States and in other jurisdictions; and •local business and cultural factors that differ from our normal standards and practices, including business practices that we are prohibited from engaging in by the U.S. Foreign Corrupt Practices Act and other anti-corruption laws and regulations.

We depend on our information technology systems for many aspects of our business. Our systems may be susceptible to damage, disruptions or shutdowns due to failures during the process of upgrading, replacing or maintaining software, databases or components thereof, power outages, hardware failures, interruption, failures or vulnerabilities in the systems of third-parties (including those with access to our systems or data, such as customers or vendors), computer viruses, attacks by computer hackers, ransomware, phishing or other cybersecurity attacks, telecommunication failures, user errors, malfeasance or catastrophic events. Threat actors may utilize emerging technologies, such as AI and machine learning. Such events have occurred in the past and may occur in the future. Cybersecurity breaches could result in unauthorized disclosure of confidential information, disruptions to our operations and/or impacts to a third party with which we have a relationship, such as a customer or vendor, which could result in reputational, competitive, operational or other business harms as well as financial costs and regulatory action. While we have not experienced a material information security breach, we cannot be sure that such a breach will not occur in the future. The information technology systems in our factories are at varying levels of sophistication and maturity as the factories have different sets of products, processes and customer expectations.…

•delays in the design and implementation of the system; •costs may exceed our plans and expectations; and •disruptions resulting from the implementation, integration or cybersecurity breach of the systems may impact our ability to process transactions and delay shipments to customers, impact our results of operations or financial condition or harm our control environment.

Our business could be materially and adversely affected if our information technology systems are disrupted or if we are unable to successfully install new systems or improve, upgrade, integrate or expand upon our existing systems. We maintain insurance policies for various types of information security risks, including network security and privacy liability for third party claims, and business interruption and system failure reimbursement coverage, but we do not carry insurance for all the above referred risks. With regard to the insurance we do maintain, we cannot assure you that it would be sufficient to cover all of our potential losses. As a result, our business, financial condition, results of operations and cash flows could be materially and adversely affected by a disruption, failure or breach of our information technology systems.

There has also been an increase in regulatory and public attention and industry and customer focus on the materials contained in semiconductor products, the environmental impact of semiconductor operations and the risk of chemical releases from such operations, climate change, sustainability and related environmental concerns. Increased regulation of and restriction on the use of hazardous substances may impact our supply chain due to decreased availability, necessitate changes in our packaging processes, require us to seek substitutes that may not be readily available in the marketplace or eliminate the use of such hazardous substances although there may not be a technically feasible alternative. This increased focus on sustainability and the environmental impact of semiconductor operations and products has caused industry groups and customers to impose additional requirements on us and our suppliers, sometimes exceeding regulatory standards. These industry and customer requirements include increased tracking and reporting of GHG emissions, reductions in waste and wastewater from operations, additional reporting on the materials and components used in the products for which we perform our services, and the use of renewable energy sources in our factory operations.…

General Risk Factors Our business and financial condition has been adversely affected, and could be adversely affected in the future, by natural disasters and other calamities, health conditions or pandemics, political instability, hostilities or other disruptions.

We have significant packaging and test services and other operations in China, Japan, Korea, Malaysia, the Philippines, Portugal, Singapore, Taiwan and Vietnam, and the Arizona Facility is a new factory under construction in the United States. Such operations are or could be subject to: natural disasters, such as earthquakes, tsunamis, typhoons, floods, droughts, extreme heat, volcanoes and other severe weather and geological events, and other calamities, such as fire; the outbreak of infectious diseases (such as Covid-19 and other coronaviruses, Ebola or flu); industrial strikes; government-imposed travel restrictions or quarantines; breakdowns of equipment; difficulties or delays in obtaining materials, equipment, utilities and services, including electricity and water; political events or instability; acts of war or armed conflict (such as ongoing conflicts in Ukraine and Israel); terrorist incidents and other hostilities in regions where we 31 Table of Contents have facilities; and industrial accidents and other events, that could disrupt or even shut down our operations. While our global manufacturing footprint may allow us to shift production to other factories without substantial cost or production delays, certain of our services are currently performed using equipment located in one or only a subset of our factories.…

For example, in April 2016, our Kumamoto factory was damaged by earthquakes in Japan. As a result of these earthquakes, our sales were reduced due to the temporary disruption in operations, and we incurred earthquake-related costs for damaged inventory, buildings and equipment. Our suppliers and customers also have significant operations in such locations, and this could compound the effect of any such disruption. In the event of such a disruption or shutdown, we may be unable to reallocate production to other facilities in a timely or cost-effective manner (if at all), and we may not have sufficient capacity, or customer approval, to service customer demands in our other facilities. A natural disaster or other calamity, political instability, the occurrence of hostilities or other event that results in a prolonged disruption to our operations, or the operations of our customers or suppliers, could have a material adverse effect on our business, financial condition, results of operations and cash flows.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
