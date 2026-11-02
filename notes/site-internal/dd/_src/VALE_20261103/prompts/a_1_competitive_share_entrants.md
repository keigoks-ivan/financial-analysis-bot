你是 stock-analyst v20 DD 的證據採集子 agent。標的：VALE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - VALE Vale market share gaining OR losing 2026
  - Vale new entrant OR displace threat Other Industrial Metals & Mining 2026
  - VALE competitor design win 2026
  - Vale vs Other Industrial Metals & Mining peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：全文（無法依 Item 切段）｜url：https://www.sec.gov/Archives/edgar/data/917851/000129281426001844/valeform20f_2025.htm｜as_of：2026-03-27
<<<
VALE ANNUAL REPORT FORM 20-F | 40 Table of Contents II. INFORMATION ON THE COMPANY Lines of Business Our principal lines of business consist of mining and related logistics. This section presents information about operations, production, sales and competition and is organized as follows: 1. Iron Ore Solutions 1.1. Iron ore and iron ore agglomerates 1.1.1 Iron ore properties 1.1.2 Iron ore production 1.1.3 Individual property disclosure 1.1.3.1 Serra Norte 1.1.3.2 Serra Sul 1.1.4 Iron ore agglomerates operations 1.1.4.1 Iron ore pellets operations 1.1.4.2 Iron ore pellets production 1.1.4.3 Iron ore briquette operations 1.1.5 Iron ore strategy 1.1.6 Customers, sales and marketing 1.1.7 Competition 1.2. Logistics and energy assets to support Iron Solutions operations 1.2.1 Railroads 1.2.2 Ports and maritime terminals 1.2.3 Energy 2. Vale Base Metals 2.1 Nickel 2.1.1 Properties 2.1.2 Production 2.1.3 Individual property disclosure 2.1.3.1 Sudbury 2.1.4 Nickel Strategy 2.1.5 Customers and sales 2.1.6 Competition 2.2 Copper 2.2.1 Properties 2.2.2 Production 2.2.3 Individual property disclosure 2.2.3.1 Salobo 2.2.4 Copper Strategy 2.2.5 Customers and sales 2.2.6 Competition 2.3 PGMs and other precious metals 2.4 Cobalt 2.5 Logistics and energy assets to support Vale Base Metals operations 2.5.1 Ports 2.5.2 Energy 3. Other Investments 3.1 Anglo American Minério de Ferro Brasil 3.2 PT Vale Indonesia Tbk (PTVI)

We invest in customer service in order to improve our competitiveness. We work with our customers to understand their objectives and to provide them with Iron Ore Solutions to meet specific customer needs. Using our expertise in mining, agglomeration and iron-making processes, we search for technical solutions that will balance the best use of our world-class mining assets and the satisfaction of our customers. We believe that our ability to provide customers with a total Iron Ore Solutions and the quality of our products are both very important advantages helping us improve our competitiveness in relation to competitors that may be more conveniently located geographically. In addition to offering technical assistance to our customers, we have offices in St. Prex (Switzerland), Tokyo (Japan), Singapore, Dubai (UAE), Shanghai, Beijing and Qingdao (China), which support global sales by Vale International. These offices also allow us to stay in close contact with our customers, monitor their requirements and our contract performance, and ensure that our customers receive timely deliveries.

1.1.7 Competition The global iron ore and iron ore pellet markets are highly competitive. The main factors affecting competition are price, quality and range of products offered, reliability, operating costs and shipping costs.

Asia. Our main competitors in the Asian market are located in Australia and include subsidiaries and affiliates of BHP Group Limited (BHP), Rio Tinto Ltd (Rio Tinto) and Fortescue Metals Group Ltd.

Europe. Our main competitors in the European market are Luossavaara Kiirunavaara AB (LKAB), ArcelorMittal Mines Canada Inc., Iron Ore Company of Canada, a subsidiary of Rio Tinto, Kumba Iron Ore Limited and Société Nationale Industrielle et Miniére. We are competitive in the European market for the same reasons as in Asia, and due to the proximity of our port facilities to European customers.

Although pricing is relevant, quality and reliability are important competitive factors as well. We believe that our integrated transportation systems, high quality ore and technical services make us a strong competitor in the Brazilian market. With respect to pellets, our major competitors are LKAB, Iron Ore Company of Canada, Ferrexp Plc, Arcelor-Mittal Mines Canada, Samarco and Bahrain Steel.

2.1.6 Competition The global nickel market is highly competitive. Our key competitive strengths include our long-life mines, sophisticated exploration and processing technologies, and a diversified portfolio of products. Our global marketing reach, diverse product mix, and customer technical support direct our products into applications and geographic regions that offer the highest margins for our products.

2.2.6 Competition The global refined copper market is highly competitive. Producers are integrated mining companies and custom smelters, covering all regions of the world, while consumers are principally wire rod and copper alloy producers. Competition occurs mainly on a regional level and is based primarily on production costs, quality, reliability of supply and logistics costs. The world’s largest copper cathode producers are Jiangxi Copper Corporation, Tongling Non-Ferrous Metals Group Co., Jinchuan, Aurubis, Corporación Nacional del Cobre de Chile (Codelco), and Freeport McMoRan, each operating at the parent company level or through subsidiaries. Our participation in the global refined copper cathodes market is marginal as we position ourselves more competitively in the copper concentrate market.

Our market share in 2025 was about 2.8% of the total custom copper concentrate market.

Sustainability Committee. Responsible for advising on the sustainability strategy and the integration thereof into our strategic planning, aiming the creation of value, competitivity, and socio-economic and environmental sustainability; our corporate sustainability policies related to safety, environment, health, education and relationship with communities, Indigenous Peoples and other stakeholders, human rights, communication and institutional relations; the direction of our strategic sustainability indicators and the communication and disclosure thereof, also through our Annual Report on ESG matters; the guidelines for our adhesion to or permanence in initiatives, technical standards or agreements, in the national or international sphere, regarding sustainability matters, that may be under competence of the Board of Directors; guidelines for long-term social and environmental commitments that are under the competence of the Board of Directors; among other responsibilities. Its current members are Rachel de Oliveira Maia (Coordinator), Manuel Lino Silva de Sousa Oliveira, André Viana Madeira, Franklin Lee Feder, Marcio Antonio Chiumento and Wagner Vasconcelos Xavier.

Defined benefit plan (“Plano BD”) - The Plano BD is closed to new entrants since 2000, when the Vale Mais plan was implemented. It is a plan that has defined benefit characteristics, covering almost exclusively retirees and their beneficiaries.

The foreign plans are managed in accordance with their region. They are divided between plans in Canada, USA and UK. Pension plans in Canada are composed of a defined benefit and defined contribution component. Currently the defined benefit plans do not allow new entrants. The majority of foreign defined benefit plans are underfunded as of December 31, 2025 and 2024 and just two overfunded plans as of December 31, 2025 and 2024.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
