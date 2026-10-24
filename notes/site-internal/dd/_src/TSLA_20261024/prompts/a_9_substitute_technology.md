你是 stock-analyst v20 DD 的證據採集子 agent。標的：TSLA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - product substitute technology threat 2026
  - alternative technology disruption 2026 2027
  - TSLA technology obsolescence risk
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm｜as_of：2026-01-29
<<<
As is the case for some OEM companies, some of our procured components and systems are sourced from single suppliers. Where multiple sources are available for certain key components, we work to qualify multiple suppliers for them where it is sensible to do so in order to minimize potential production risks due to disruptions in their supply. We also mitigate risk by maintaining safety stock for key parts and assemblies and die banks for components with lengthy procurement lead times.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm｜as_of：2026-01-29
<<<
Our products contain thousands of parts purchased globally from hundreds of suppliers, including single-source direct suppliers, which exposes us to multiple potential sources of component shortages. Unexpected changes in business conditions, materials pricing, including inflation of raw material costs, labor issues, wars, trade policies, natural disasters, health epidemics, trade and shipping disruptions, port congestions, cyberattacks and other factors beyond our or our suppliers’ control could also affect these suppliers’ ability to deliver technologies or components to us or to remain solvent and operational. U.S. trade policy alterations in 2025, including heightened import tariffs and subsequent retaliatory measures, have impacted our supply chain costs, and may impact the availability of certain technologies or components, depending on the exact scope of the tariffs ultimately implemented and retaliatory export controls. Additionally, if our suppliers do not accurately forecast and effectively allocate production or if they are not willing to allocate sufficient production to us, or face other challenges such as insolvency, it may reduce our access to components and require us to search for new suppliers.…

As the scale and variants of our production increases, we will also need to accurately forecast, purchase, warehouse and transport components at high volumes to our manufacturing facilities and servicing locations internationally. If we are unable to accurately match the timing and quantities of component purchases to our actual needs or successfully implement automation, inventory management and other systems to accommodate the increased complexity in our supply chain and parts management, we may incur unexpected production disruption, storage, transportation and write-off costs, which may harm our business and operating results.

We are dependent on the continued supply of lithium-ion battery cells for our vehicles and energy storage products, and we will require substantially more cells to grow our business according to our plans. Currently, we rely on suppliers such as Panasonic and Contemporary Amperex Technology Co. Limited (CATL) for these cells. We have to date fully qualified only a very limited number of such suppliers and have limited flexibility in changing suppliers. Any disruption in the supply of battery cells from our suppliers could limit production of our vehicles and energy storage products. In the long term, we intend to supplement cells from our suppliers with cells manufactured by us, which we believe will be more efficient, manufacturable at greater volumes and more cost-effective than currently available cells. However, our efforts to develop and manufacture such battery cells have required, and may continue to require, significant investments, and there can be no assurance that we will be able to achieve these targets in the timeframes that we have planned or at all. If we are unable to do so, we may have to curtail our planned vehicle and energy storage product production or procure additional cells from suppliers at potentially greater costs, either of which may harm our business and operating results.

Finally, the high volumes of lithium-ion cells and battery modules and packs manufactured by us and by our suppliers are stored and recycled at our various facilities. Any mishandling of these products may cause disruption to the operation of such facilities. While we have implemented safety procedures related to the handling of the cells, there can be no assurance that a safety issue or fire related to the cells would not disrupt our operations. Any such disruptions or issues may harm our brand and business.

The loss of the services of any of our key employees or any significant portion of our workforce could disrupt our operations or delay the development, introduction and ramp of our products and services. In particular, we are highly dependent on the services of Elon Musk, Technoking of Tesla and our Chief Executive Officer. None of our key employees is bound by an employment agreement for any specific term and we may not be able to successfully attract and retain senior leadership necessary to grow our business. Our future success also depends upon our ability to attract, hire and retain a large number of engineering, manufacturing, marketing, sales and delivery, service, installation, technology and support personnel, especially to support our planned high-volume product sales, market and geographical expansion and technological innovations. If we are not successful in managing these risks, our business, financial condition and operating results may be harmed.

To the extent any security incident results in unauthorized access or damage to or acquisition, use, corruption, loss, destruction, alteration or dissemination of our data, including intellectual property and personal information, or our products, vehicles or service offerings, or for it to be believed or reported that any of these occurred, it could disrupt our business, harm our reputation, compel us to comply with applicable data breach notification laws, subject us to time consuming, distracting and expensive litigation, regulatory investigation and oversight, mandatory corrective action, require us to verify the correctness of database contents, or otherwise subject us to liability under laws, regulations and contractual obligations, including those that protect the privacy and security of personal information. This could result in increased costs to us and result in significant legal and financial exposure and/or reputational harm.

We also rely on service providers, and similar incidents relating to their information technology systems could also have a material adverse effect on our business. There have been and may continue to be significant supply chain attacks. Our service providers, including our workforce management software provider, have been subject to ransomware and other security incidents, and we cannot guarantee that our or our service providers’ systems have not been breached or that they do not contain exploitable defects, bugs, or vulnerabilities that could result in a security incident, or other disruption to, our or our service providers’ systems. Our ability to monitor our service providers’ security measures is limited, and, in any event, malicious third parties may be able to circumvent those security measures.

Further, the implementation, maintenance, segregation and improvement of these systems require significant management time, support and cost, and there are inherent risks associated with developing, improving and expanding our core systems as well as implementing new systems and updating current systems, including disruptions to the related areas of business operation. These risks may affect our ability to manage our data and inventory, procure parts or supplies or manufacture, sell, deliver and service products, adequately protect our intellectual property or achieve and maintain compliance with, or realize available benefits under, tax laws and other applicable regulations.

Moreover, if we do not successfully implement, maintain or expand these systems as planned, our operations may be disrupted, our ability to accurately and/or timely report our financial results could be impaired and deficiencies may arise in our internal control over financial reporting, which may impact our ability to certify our financial results. Moreover, our proprietary information, including intellectual property and personal information, could be compromised or misappropriated and our reputation may be adversely affected. If these systems or their functionality do not operate as we expect them to, we may be required to expend significant resources to make corrections or find alternative sources for performing these functions.

Our business may be adversely affected by any disruptions caused by union activities.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
