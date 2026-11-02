你是 stock-analyst v20 DD 的證據採集子 agent。標的：INCY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - INCY Incyte market share gaining OR losing 2026
  - Incyte new entrant OR displace threat Biotechnology 2026
  - INCY competitor design win 2026
  - Incyte vs Biotechnology peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm｜as_of：2026-02-10
<<<
18 Table of Contents Although we believe our rights under patents and patent applications provide a competitive advantage, the patent positions of pharmaceutical and biotechnology companies are highly uncertain and involve complex legal and factual questions. We may not be able to develop patentable products or processes and may not be able to obtain patents in the United States or elsewhere from pending applications. Even if patent claims are allowed, the claims may not issue, or in the event of issuance, may not be valid or enforceable or may not be sufficient to protect the technology owned by or licensed to us or provide us with a competitive advantage. Any patent or other intellectual property rights that we own or obtain may be circumvented, challenged or invalidated by our competitors. Others may have patents that relate to our business or technology, and that may prevent us from marketing our drug candidates unless we are able to obtain a license to those patents. In addition, litigation or other proceedings may be necessary to defend against claims of infringement, to enforce patents, to protect our other intellectual property rights, to determine the scope and validity of the proprietary rights of third parties, or to defend ourselves in patent or other intellectual property right suits brought by third parties.…

Competition Our drug discovery, development and commercialization activities face, and will continue to face, intense competition from organizations such as pharmaceutical and biotechnology companies, as well as academic and research institutions and government agencies. We face significant competition from organizations, particularly fully integrated pharmaceutical companies, that are pursuing pharmaceuticals that are competitive with our drug products and our drug candidates.

Accordingly, our competitors may succeed in obtaining patent protection, receiving FDA and other regulatory approval or commercializing products that compete with our drug products or our drug candidates.

In addition, any drug candidate that we successfully develop may compete with existing therapies that have long histories of safe and effective use. Competition may also arise from: •other drug development technologies and methods of preventing or reducing the incidence of disease; •new compounds; or •other classes of therapeutic agents.

19 Table of Contents We face and will continue to face intense competition from other companies for collaborative arrangements with pharmaceutical and biotechnology companies, for establishing relationships with academic and research institutions and for licenses to drug candidates or proprietary technology. These competitors, either alone or with their collaborative partners, may succeed in developing products that are more effective or commercially successful than ours.

In a number of countries, including in particular developing countries, government officials and other groups have suggested that pharmaceutical companies should make drugs available at a low cost. In some cases, governmental authorities have indicated that where pharmaceutical companies do not do so, their patents might not be enforceable to prevent generic competition. Some major pharmaceutical companies have greatly reduced prices for their drugs in certain developing countries. If certain countries do not permit enforcement of any of our patents, sales of our products in those countries, and in other countries by importation from low-price countries, could be reduced by generic competition or by parallel importation of our product. Alternatively, governments in those countries could require that we grant compulsory licenses to allow competitors to manufacture and sell their own versions of our products in those countries, thereby reducing our product sales, or we could respond to governmental concerns by reducing prices for our products. In all of these situations, our results of operations could be adversely affected.

We offer what we believe is a competitive compensation and benefits package, which allows 100% of global Incyte employees to participate in our annual incentive compensation plan, annual equity-based grants, health benefits and tuition reimbursement. We seek to ensure our compensation package remains competitive by conducting benchmark reviews annually. We support our colleagues in their professional development, offering opportunities for growth through challenging job assignments, development plans, and training opportunities.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm｜as_of：2026-02-10
<<<
Our products compete, and our product candidates may in the future compete, with currently existing therapies, including generic drugs, product candidates currently under development by us and others, or future product candidates, including new chemical entities that may be safer or more effective or more convenient than our products. Any products that we develop may be commercialized in competitive markets, and our competitors, which include large global pharmaceutical and biopharmaceutical companies and smaller research-based biotechnology companies, may succeed in developing products that render our products obsolete or noncompetitive. Many of our competitors, particularly large pharmaceutical and biopharmaceutical companies, have substantially greater financial, operational and human resources than we do. Smaller or earlier stage companies may also prove to be significant competitors, particularly through focused development programs and collaborative arrangements with large, established companies. In addition, many of our competitors deploy more personnel to market and sell their products than we do, and we compete with other companies to recruit, hire, train and retain pharmaceutical sales and marketing personnel. If our sales force and sales support organization are not appropriately resourced and sized to adequately promote our products, the commercial potential of our current and any future products may be diminished.…

34 Table of Contents Present and potential competitors for JAKAFI include major pharmaceutical and biotechnology companies, as well as specialty pharmaceutical firms. In addition, JAKAFI could face competition from generic products. As a result of the Drug Price Competition and Patent Term Restoration Act of 1984, commonly known as the Hatch-Waxman Act, in the United States, generic manufacturers may seek approval of a generic or other version of an innovative pharmaceutical by filing with the FDA an Abbreviated New Drug Application (“ANDA”) or a New Drug Application (“NDA”) pursuant to section 505(b)(2) of the Federal Food, Drug, and Cosmetic Act (the “FDCA”). The Hatch-Waxman Act provides significant incentives to generic manufacturers to challenge U.S. patents on successful innovative pharmaceutical products. We have received a notice letter from each of Apotex, Inc., Hikma Pharmaceuticals USA Inc., Sun Pharmaceutical Industries Inc., Granules India Ltd., Dr.…

MONJUVI/MINJUVI currently competes with existing therapies that are approved for the treatment of patients with diffuse large B-cell lymphoma on the basis of, among other things, efficacy, cost, breadth of approved use and the safety and side-effect profile. These existing therapies are offered by major pharmaceutical and biotechnology companies, as well as specialty pharmaceutical firms. Competitors and potential competitors for PEMAZYRE, ZYNYZ and NIKTIMVO include major pharmaceutical and biotechnology companies, as well as specialty pharmaceutical firms.

The biotechnology and pharmaceutical industries are intensely competitive and subject to rapid and significant technological change. Despite investing significant resources, we may not be successful in discovering, developing, or commercializing additional drug products or our existing drug products in new indications. Discovery and development of drug candidates are expensive, uncertain and time-consuming, and we do not know if our efforts will lead to discovery of any drug candidates that can be successfully developed and marketed. We, or our collaborators or licensees, may decide to discontinue development of any or all of our drug candidates at any time for commercial, scientific or other reasons. Even if a drug candidate receives marketing approval, it may not be able to achieve market acceptance or compete successfully with our competitors’ products and we may never realize a return on the significant amount of time and money invested in the drug candidate, which could adversely affect our operating results and financial condition as well as our business plans. Of the compounds or biologics that we identify as potential drug products or that we in-license from other companies, including potential products for which we are conducting clinical trials, only a few, if any, are likely to lead to successful drug development programs and commercialized drug products.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
