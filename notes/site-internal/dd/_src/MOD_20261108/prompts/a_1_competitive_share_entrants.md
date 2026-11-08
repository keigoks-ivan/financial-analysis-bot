你是 stock-analyst v20 DD 的證據採集子 agent。標的：MOD。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MOD Modine Manufacturing market share gaining OR losing 2026
  - Modine Manufacturing new entrant OR displace threat Building Products & Equipment 2026
  - MOD competitor design win 2026
  - Modine Manufacturing vs Building Products & Equipment peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
The following is a summary of our primary product groups, categorized as a percentage of our net sales: ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ Fiscal 2026 ​ ​ ​ Fiscal 2025 Data Centers 35 % 25 % Heat Transfer Solutions 18 % 21 % HVAC Technologies 11 % 10 % On-Highway Applications 23 % 28 % Heavy-Duty Equipment 13 % 16 % ​ Competitive Position We compete with many manufacturers of heat transfer and HVAC&R solutions, some of which are divisions of larger companies. The markets for our products continue to be very dynamic. For example, our data center customers are expanding globally, driving us to invest in geographic and capacity expansion to meet their needs. Additionally, our global power generation customers are looking for new technologies and global manufacturing capacity to meet their growth demands, driven by new data center construction and demand for backup power for these data centers, as well as for hospitals, mining and airports. Our HVAC&R OEM customers are faced with significant international competition and maintain global manufacturing footprints to compete in local markets. In addition, consolidation within the supply base and vertical integration may introduce new or restructured competitors to our markets. We are investing in geographic and capacity expansion to meet these customer needs, particularly as we experience competition from companies positioned in different geographies that enjoy economic advantages such as lower labor costs and tax rates.…

Competitive compensation and benefits We offer our employees competitive compensation and comprehensive benefit packages. We regularly benchmark our compensation practices and benefits programs against those of comparable industries and in the geographic areas where our facilities are located. We believe that our compensation and employee benefits are competitive and allow us to attract and retain talent throughout our organization.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/67347/000110465926066795/mod-20260331x10k.htm｜as_of：2026-05-27
<<<
Most of our products are sold in competitive markets. Our sales levels and margins could be adversely affected by pricing pressures from our customers and pricing actions of our competitors. Such pricing pressures may require us to adjust the prices of products to stay competitive. If we are unable to offset any price concessions through improved operating efficiencies and manufacturing processes, sourcing alternatives, technology enhancements and other cost reduction initiatives, our results of operations and cash flows could be adversely affected.

We experience competition from companies in other parts of the world that enjoy economic advantages, such as lower labor costs, lower health care costs, lower tariff or tax rates, lower costs associated with legal compliance, and, in some cases, export or raw materials subsidies. In addition, consolidation and vertical integration within the supply base have introduced new or restructured competitors to our markets. Increased competition could adversely affect our business and results of operations.

Our leading-edge technologies, product quality, and the history of our product performance in each of our markets has created our competitive value with our customers. If we fail to be at the forefront of technological advances and cannot differentiate ourselves from our competitors with our technology or fail to provide high quality, innovative and advanced performance products and services that both meet or exceed customer expectations and address their ever-evolving needs, we may experience price erosion, lower sales, and lower profit margins. Significant technological developments by our competitors or others also could adversely affect our business and results of operations.

We design technologically advanced products and systems, and the processes and time required to develop, design and produce these products and systems can be lengthy, difficult and complex. We spend significant time and financial resources to ensure the successful launch of new products and programs. Due to our high level of launch activity, we must appropriately manage these activities and deploy our capital and operational and administrative resources to take advantage of the resulting increase in our business. If we do not successfully or timely launch new products, systems and programs, we may lose market share or damage relationships with our customers, which could negatively affect our business and results of operations. In addition, any failure in our manufacturing strategy for these new products or programs could result in operating inefficiencies or asset impairment charges, which could adversely affect our results of operations and cash flows.

Under our strategy based on 80/20 principles, we are focused on acquiring businesses and investing in technologies that we expect to accelerate our strategic growth in select markets. If we are unable to successfully execute on further organic growth opportunities or complete acquisitions in the future, our growth may be limited. There can be no assurance we will be able to identify and complete the purchase of attractive acquisition targets, including obtaining financing, if necessary, to facilitate such transactions. Future acquisitions will require integration of operations, sales and marketing, information technology, finance, and administrative functions. If we are unable to successfully integrate future acquisitions into our existing operations, capitalize on expected market share or revenue gains, realize anticipated cost or revenue synergies, or operate any acquired businesses profitably, we may not achieve the financial or operational success expected. In addition, future acquisitions could include the issuance of shares of our common stock as all or a portion of the consideration paid to the sellers. Any such issuance of shares would be dilutive to the interests of our existing shareholders and may adversely affect the market price of our shares.

Our ability to sustain and grow our business requires us to hire, develop, and retain skilled and diverse personnel throughout our organization. We depend significantly on the engagement of our employees and their skills, experience and industry knowledge to support our objectives and initiatives, and have attracted a leadership team executing on strategic initiatives informed by our 80/20 mindset. Our ability to achieve our operating and strategic goals depends on our ability to identify, hire, train and retain talented personnel, including our leadership team. We compete with other companies for talented personnel in the locations and labor markets in which we operate, all of which are very competitive, and we may lose key personnel or fail to attract other talented personnel, including at our manufacturing locations. Any prolonged labor shortages or significant employee turnover could negatively impact productivity and result in increased labor costs, such as increased overtime to meet demand or increased wage rates necessary to attract and retain employees. Overall, difficulty in attracting, developing, and retaining qualified personnel could adversely affect our business and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
