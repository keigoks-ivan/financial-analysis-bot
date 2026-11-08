你是 stock-analyst v20 DD 的證據採集子 agent。標的：CAMT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - CAMT Camtek tariff section 232 2026
  - Camtek export control OR entity list Semiconductor Equipment & Materials 2026
  - CAMT Camtek China tariff OR trade restriction 2026
  - Semiconductor Equipment & Materials tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-19）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1109138/000117891326001561/zk2634678.htm｜as_of：2026-03-19
<<<
Geopolitical tensions may result in export control restrictions, trade sanctions, and more generally international trade regulations which may impact our ability to sell and deliver our systems, technology, and services. Changes in applicable social, political, regulatory and economic conditions or in laws and policies governing foreign trade, manufacturing, development and investment in the territories and countries, where our customers are located, could adversely affect our business, financial condition, operating results and cash flows. Among other things, such factors may affect our ability to sell our products and services in certain countries, such as China. Our business involves the sale of systems and services to customers in a number of countries, including U.S., Europe, Korea, Taiwan and China, and includes technologies that may be the subject of increased export regulations or policies.

The abovementioned measures can create legal and/or contractual exposure not only for U.S. companies or U.S. people, but also for non-U.S. companies like us. In some cases, the abovementioned export restrictions might also be applicable to the products or services which we export from countries other than the United States, should there be a U.S. nexus to our activities, should the products contain certain U.S. origin items above the applicable threshold, or should they be produced using certain U.S.-controlled technology, software, or production equipment.

Even where U.S. and other global export controls do not apply to our products, they may impact the demand for our products. For example, certain additional export administration regulations issued by the U.S. Department of Commerce since October 2022, and which have increased in 2025, may have an adverse effect on the entire semiconductor manufacturing sector in China and reduce the demand for semiconductors equipment and therefore indirectly affect our sales in China.

It has been and may continue to be increasingly difficult to keep up with the pace, complexity and scope of these changes. While we continue to carefully monitor new sanctions and trade restrictions that could arise and conduct ongoing detailed assessments of applicable law, any alleged or actual violations of such laws whether U.S. or other jurisdictions, whether or not directly applicable to us, could have an adverse impact on our reputation, business, results of operations and financials.

In 2025, our sales in the Asia Pacific region (mainly China, Taiwan and South Korea) accounted for approximately 91% of our total revenues with sales to China being 49% of our total revenues. A number of Asian countries have experienced or could experience political and economic instability. For instance, Taiwan and China encountered a number of continuous disputes, as have North and South Korea. Additionally, the Asia-Pacific region is susceptible to the occurrence of natural disasters, such as earthquakes, cyclones, tsunamis and flooding. Changes in local legislation, changes in governmental policies, controls and regulations, trade restrictions, a downturn in economic or financial conditions, an outbreak of hostilities or other political upheaval, as well as any further extraordinary events having an adverse effect on the economy or business environment in this region, would likely harm the operations of our customers in these countries, may cause a significant decline in our future revenues and may have an adverse effect on our results of operations and cash flow. These general risks are heightened in China, which is our largest territory, where the nature of the economy, local legislation, governmental policies and regulatory environment are rapidly evolving and where foreign companies may face the negative effects of changed governmental policies, regulatory, business and cultural obstacles.…

Tariffs could have an adverse effect on economic conditions and financial markets. The international environment in which we operate is affected by inter-country trade agreements and tariffs. As a result of recent revisions in the U.S. administrative policy there are, and may be additional, changes to existing trade agreements, greater restrictions on free trade and significant increases in tariffs on goods imported into the United States. Over the course of 2025, the U.S. has continued to impose tariffs on imports from foreign countries, including China. These additional tariffs or any future tariffs or retaliation by another government against such tariffs or policies affects may affect global trade in our markets and have introduced significant uncertainty into our markets.

The application of increased tariffs or continuing uncertainty also may result in an increase to our costs of operation or otherwise limit our commercial opportunities. Any of these events could adversely affect our business, results of operations and financial condition.

Due to our global operations, we must comply with certain international and domestic laws, disclosure requirements, export control regulations and restrictions which may expose our business to risks. In addition, our business is subject to numerous domestic laws and regulations designed to protect the environment, including with respect to discharges and management of hazardous substances, wastes and emissions and soil and ground water contamination. The failure to comply with current or future environmental requirements could expose us to criminal, civil and administrative charges and monetary liability. We believe that we have complied with these requirements and that such compliance has not had a material adverse effect on our results of operations, financial condition or cash flows. Although we are not presently aware of any liability that could be material to our business, financial condition or operating results, due to the nature of our business and environmental risks, we cannot provide assurance that any such material liability will not arise in the future. A number of our customers have adopted, or may adopt, procurement policies that include environmental, social and governance responsibility provisions or requirements that their suppliers should comply with, or they may seek to include such provisions or requirements in their procurement terms and conditions.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
