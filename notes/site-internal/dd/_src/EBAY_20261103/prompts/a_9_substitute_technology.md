你是 stock-analyst v20 DD 的證據採集子 agent。標的：EBAY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - eBay product substitute technology threat 2026
  - Internet Retail alternative technology disruption 2026 2027
  - EBAY eBay technology obsolescence risk
  - Internet Retail next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-19）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm｜as_of：2026-02-19
<<<
•We may not be able to keep pace with technological changes, including emerging AI technologies, and with changes in consumer demands and expectations.

•We may not be able to match the flexibility and expertise of all specialist competitors – Competitors that are narrowly focused on specific goods may be better than we are at creating buyer and seller communities and catering to the needs of those communities. Specialist competitors may have more resources to innovate quickly and efficiently within these communities without disruption to buyers and sellers outside of those communities. Additionally, our growth strategy has increasingly emphasized our Focus Categories, such as motor parts and accessories, collectibles, refurbished goods, and authenticated luxury items. Our Focus Category buyers and sellers often have unique product and service needs. The size and complexity of our platforms can make it difficult for us to address the unique needs of our Focus Category consumers as quickly and efficiently as our specialist competitors.

15 Table of Contents We may not be able to keep pace with technological changes, including emerging AI technologies, and with changes in consumer demands and expectations.

Our industry is subject to rapid technological change, and the demands and expectations of our consumers can change quickly. Predicting the changes that our consumers want, learning new technologies and developing new products and services can be complex, time-consuming and costly, and our investments in new innovations may not yield the expected business or financial benefits. If we fail to anticipate or identify technological trends or fail to devote appropriate resources to adapt to such trends, our business could be harmed.

Any further trade policy developments, especially in key geographies such as the U.S, the U.K., and the E.U., could significantly impact the cost of items and available inventory to be bought and sold on our platforms, limit our ability and the ability of our sellers to offer and deliver products on a timely or cost-effective basis, or otherwise adversely impact our consumers’ ability to buy and sell on our platforms. Further, adapting to new and changed trade restrictions can be expensive, time-consuming and very disruptive to our buyers and sellers. For example, tariffs generally apply based on the manufacturing location, rather than the selling location, of goods. These distinctions can be confusing for our sellers and lead to platform solutions that fail to satisfy all of our customers. Our business to consumer sellers may be dissuaded from using our platforms if we do not have solutions that accurately calculate customs fees based on manufacturing location. However, those same solutions may dissuade our consumer-to-consumer sellers from using our platforms, because they serve to increase the cost of the items they are selling. The loss of sellers from one or more geographies could negatively impact the breadth and relevance of inventory available on our platforms, which could lead to decreased buyer traffic and harm our business.

Systems failures and business interruptions could harm our business. We have experienced and will continue to experience system failures that interrupt the availability or reduce the speed or functionality of our platforms and services. These events have resulted in, and will in the future result in, loss of revenue. These events can occur for many reasons, including hardware and software defects or malfunctions, cyberattacks such as denial-of-service, credential stuffing, and other types of attacks, human error, earthquakes, hurricanes, floods, fires, natural disasters, sustained drought, power losses, disruptions in telecommunications services, fraud, military or political conflicts, terrorist attacks, computer viruses, or other events. Our systems are also subject to compromise, sabotage and intentional acts of vandalism. Some of our systems are not fully redundant and our disaster recovery planning can never be sufficient to cover all eventualities.

Any actual or attempted cyberattack, breach or data incident, or even an unfounded public rumor regarding such an attack, breach or incident, could have a material adverse effect on our business, reputation, financial condition or results of operation. eBay does not need to be the direct target of such attacks, breaches or incidents for them to have a material adverse effect on our operations. For example, a cyberattack on a key service provider, or a vulnerability in software that they use, could disrupt our services or compromise user and employee data 21 Table of Contents entrusted to that service provider. We perform risk-based assessments of our service providers, but we do not control our service providers and our ability to monitor their data security is limited, so we cannot guarantee that their security measures will be adequate. In addition, we and our employees, users and service providers also may not discover a cyberattack, breach or other incident for a significant period after the incident occurs, which could amplify any adverse outcomes resulting from such incidents.

Price increases, service terminations, disruptions or interruptions, product and service changes, and any other issue that prevents these third parties from providing products or services that we or our customers rely on could materially harm our business. For example, domestic or international shipping and postal rate increases may reduce the competitiveness of certain sellers’ offerings, and postal service changes and disruptions could require certain sellers to utilize alternatives which could be more expensive, slower or inconvenient, which could in turn decrease the number of transactions on our sites, negatively impacting our results of operations. Similarly, changes in the payments and delivery options available to our buyers, or the speed or cost of shipping, may reduce buyer engagement and spending on our platforms. Additionally, if sellers are unable to access tools that automate their listings, or if the providers of these tools no longer automated eBay listings among their services, our sellers may sell their good through one of our competitors or not at all, which could reduce the breadth and relevance of our inventory and harm our business.

We have outsourced certain important functions that are critical to our operations to third-party providers, including some customer support, payments and financial services, product development functions, and certain authentication services. If our service providers do not perform satisfactorily, our operations could be disrupted and user satisfaction could decrease, which could materially harm our business. The third-party suppliers we and our customers rely on may not continue to provide their products or services on acceptable terms, or at all, and we may be unable to procure alternatives from other third parties in a timely and efficient manner and on acceptable terms, or at all.

Our use of “open source” software may subject us to certain unfavorable conditions, including conditions that: (i) we make publicly available the source code for any modifications or derivative works we create based upon, incorporating or using the open source software, (ii) we license such modifications or derivative works under the terms of the particular open source license, (iii) we waive intellectual property rights in any innovation that is derived using the open source software, or (iv) we offer our products that incorporate the open source software for low or no cost. There is little legal precedent or authoritative guidance governing the interpretation of the terms of some open-source licenses (especially as applied to new technological contexts), so the potential impact of these terms on our business is uncertain and enforcement of these terms, or other compliance actions, may result in unanticipated obligations or restrictions regarding our products or services.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EBAY_20261103/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
