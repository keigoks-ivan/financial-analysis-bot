你是 stock-analyst v20 DD 的證據採集子 agent。標的：CRS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Carpenter Technology product substitute technology threat 2026
  - Metal Fabrication alternative technology disruption 2026 2027
  - CRS Carpenter Technology technology obsolescence risk
  - Metal Fabrication next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-12）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm｜as_of：2026-08-12
<<<
For other products, there are several dozen smaller producing companies and converting companies that are also competitors, as well as several hundred independent distributors of products similar to those distributed by us. Additionally, numerous foreign companies produce various specialty metal products similar to those produced by us. Furthermore, a number of different products may, in certain instances, be substituted for our finished products.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-08-12）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/17843/000001784326000034/crs-20260630.htm｜as_of：2026-08-12
<<<
Periods of reduced demand and excess supply as well as the availability of substitute lower cost materials can adversely affect our ability to price and sell our products at the profitability levels we require to be successful.

Additional worldwide capacity and reduced demand for our products could significantly impact future worldwide pricing which would adversely impact our results of operations and financial condition. In addition, continued availability of lower cost, substitute materials may cause significant fluctuations in future results as our customers opt for a lower cost alternative.

It is possible that we could experience prolonged periods of reduced production due to unplanned equipment failures, and we could incur significant repair or replacement costs in the event of those failures. It is also possible that operations could be disrupted due to other unforeseen circumstances such as power outages, explosions, fires, floods, accidents and severe weather conditions. We must make regular, substantial capital investments and changes to our manufacturing processes to lower production costs, improve productivity, manufacture new or improved products and remain competitive. We may not be in a position to take advantage of business opportunities or respond to competitive pressures if we fail to update, replace or make additions to our equipment or our manufacturing processes in a timely manner. The cost to repair or replace much of our equipment or facilities would be significant. We cannot be certain that we will have sufficient internally generated cash or acceptable external financing to make necessary capital expenditures in the future.

A significant portion of our manufacturing and production facilities are located in Reading and Latrobe, Pennsylvania and Athens, Alabama, which increases our exposure to significant disruption to our business as a result of unforeseeable developments in these geographic areas.

The prices for and availability of electricity, natural gas, oil and other energy resources are subject to volatile market conditions. These market conditions often are affected by political and economic factors beyond our control. Disruptions or lack of availability in the supply of energy resources could temporarily impair the ability to operate our production facilities. Further, increases in energy costs, or changes in costs relative to energy costs paid by competitors, have affected and may continue to adversely affect our profitability. To the extent that these uncertainties cause suppliers and customers to be more cost sensitive, increased energy prices may have an adverse effect on our results of operations, financial condition and cash flows.

War (such as the war in Iran, the war in Ukraine, the war between Israel and HAMAS, the war between Israel and Hezbollah and the Houthi attacks on commercial shipping vessels and other naval vessels), civil conflict, terrorism, other geopolitical and diplomatic tensions, natural disasters, climate change and public health issues including domestic or international pandemics, other outbreaks of contagious diseases and other adverse public health developments have caused or could cause damage or disruption to domestic or international commerce by creating economic or political uncertainties. Additionally, the volatility in the financial markets could negatively impact our business. These events could result in a decrease in demand for our products, affect the availability of credit facilities to us, our customers or other members of the supply chain necessary to transact business, make it difficult or impossible to deliver orders to customers or receive materials from suppliers, affect the availability or pricing of energy sources or result in other severe consequences that may or may not be predictable. As a result, our business, financial condition and results of operations could be materially adversely affected.

Much of our future success depends on the continued service and availability of skilled personnel, including members of our executive management team, management, metallurgists and production positions. Failure to attract, hire, develop, motivate, and retain highly qualified employee talent, or failure to develop and implement an adequate succession plan for the management team, could disrupt our operations and adversely affect our business and our future success.

We are regularly the target of attempted cyber and other security threats and must continuously monitor and develop our IT networks and infrastructure to prevent, detect, address and mitigate the risk of unauthorized access, misuse, computer viruses and other events that could have a security impact. Cybersecurity attacks are evolving in both frequency and sophistication and could be made by both internal and external individuals or groups with an extensive range of motives. If we are unable to prevent cybersecurity attacks and other information security breaches, we may encounter significant disruptions in our operations which could adversely impact our business, financial condition and results of operations or result in the unauthorized disclosure of confidential information. Such breaches may also harm our reputation, result in financial losses or subject us to litigation or other costs or penalties.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
