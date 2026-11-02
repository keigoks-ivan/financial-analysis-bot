你是 stock-analyst v20 DD 的證據採集子 agent。標的：NXPI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - NXPI NXP Semiconductors tariff section 232 2026
  - NXP Semiconductors export control OR entity list Semiconductors 2026
  - NXPI NXP Semiconductors China tariff OR trade restriction 2026
  - Semiconductors tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1413447/000141344726000008/nxpi-20251231.htm｜as_of：2026-02-19
<<<
Recently announced and future tariffs and other trade restrictions could materially and adversely affect our business, financial condition and results of operations.

In 2025, the U.S. government announced a series of tariffs, including tariffs targeting a broad range of imports and targeted tariffs on goods from specific countries and industries. In response, many countries imposed reciprocal tariffs and other trade restrictions on the United States. Although many of these tariffs, countermeasures and other trade restrictions have since been eased or paused, their initial announcements triggered considerable volatility in global markets and heightened economic uncertainty, and the global trade situation, particularly between the United States and China, continues to be highly dynamic. Further, throughout 2025 the U.S. government has initiated numerous investigations into products and industries under Section 232 of the Trade Expansion Act of 1962. For example, in April 2025, the Department of Commerce launched an investigation into the national security impacts of imported semiconductors and semiconductor manufacturing equipment. While the results of this investigation remain unknown, it is expected to result in additional tariffs and trade restrictions that may adversely impact our business. Similar investigations on other industries or products, including automotive, copper, steel, aluminum, critical minerals and aircraft, may also adversely impact the semiconductor industry and our business.…

21 Our manufacturing operations depend on deliveries of equipment and materials in a timely manner and, in some cases, on a just-in-time basis. From time to time, suppliers may extend lead times, limit the amounts supplied to us or increase prices due to capacity constraints or other factors. Supply disruptions may also occur due to shortages in critical materials, such as silicon wafers or specialized chemicals. In addition, the imposition of tariffs or other trade restrictions may significantly increase the costs, and otherwise adversely impact the availability of certain raw materials and supplies needed for our manufacturing operations. Because the equipment that we purchase is complex, it is frequently difficult or impossible for us to substitute one piece of equipment for another or replace one type of material with another. A failure by our suppliers to deliver our requirements could result in disruptions to our manufacturing operations. Our business, financial condition and results of operations could be harmed if we are unable to obtain adequate supplies of quality equipment or materials in a timely manner or if there are significant increases in the costs of equipment or materials due to current or expected inflation, trade restrictions or other reasons and we are not able to increase the price of our products.

As a result, we are subject to environmental, data privacy, export controls and sanctions, AI technologies, cybersecurity, disclosure and reporting (including reporting of ESG-related data), labor and health and safety laws and regulations in each jurisdiction in which we operate. We are also required to obtain environmental permits and other authorizations or licenses from governmental authorities for certain of our operations. In the jurisdictions where we operate, we need to comply with differing standards and varying practices of regulatory, tax, customs, judicial and administrative bodies.

No assurance can be given that we have been or will be at all times in complete compliance with the laws and regulations to which we are subject or that we have obtained or will obtain the permits and other authorizations or licenses that we need. If we violate or fail to comply with laws, regulations, permits and other authorizations or licenses, we could be fined or otherwise sanctioned by regulators. Furthermore, if one or more of our customers are sanctioned by regulators for non-compliance with laws and regulations, we could experience a decrease in demand for our products. For example, import and export regulations, such as the U.S. Export Administration Regulations administered by the U.S. Department of Commerce and sanctions imposed by the European Union (EU) and other jurisdictions, are complex, change frequently, have generally become more stringent over time and have intensified in recent years. Our results of operations could be negatively impacted if we are required to suspend activities with certain customers or suppliers due to the current and future changes in regulations, including as a result of executive orders or policy changes pursued by the new U.S. administration. For example, in 2020, due to regulations imposed by the U.S. government, we ceased shipments of our products to Huawei pending approval of export licenses.…

25 In the current environment, there are numerous and evolving risks to cybersecurity and privacy, including criminal hackers, state-sponsored intrusions, industrial espionage, employee malfeasance, and human or technological error. Computer hackers and others routinely attempt to breach the security of technology products, services, and systems, and those of customers, suppliers, and some of those attempts may be successful. Such breaches could result in, for example, unauthorized access to, disclosure, misuse, loss, or destruction of our, our customer, or other third party data or systems, theft of sensitive or confidential data including personal information (including personal data about our employees, customers or other third parties) and intellectual property, system disruptions, and denial of service. In the event of such breaches, we, our customers or other third parties could be exposed to potential liability, litigation, and regulatory action, as well as the loss of existing or potential customers, damage to our reputation, and other financial loss. In addition, the cost and operational consequences of responding to breaches and implementing remediation measures could be significant. We have identified instances of employee misappropriation or theft of certain proprietary technology by individuals who are no longer employed by NXP. In some cases, such misappropriation may result in the violation of applicable export control regulations, which we report to relevant authorities as appropriate.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NXPI_20261102/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
