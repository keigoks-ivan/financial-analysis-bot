你是 stock-analyst v20 DD 的證據採集子 agent。標的：FTNT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - FTNT Fortinet market share gaining OR losing 2026
  - Fortinet new entrant OR displace threat Software - Infrastructure 2026
  - FTNT competitor design win 2026
  - Fortinet vs Software - Infrastructure peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm｜as_of：2026-02-25
<<<
Competition The markets for our products are extremely competitive and are characterized by rapid technological change. The principal competitive factors in our markets include: •product security performance, throughput, features, effectiveness, interoperability and reliability; •addition and integration of new networking and security features and technological expertise; •compliance with industry standards and security and other certifications; •price of products and services and total cost of ownership; 8 Table of Contents •brand recognition; •customer service and support across varied and complex customer segments and use cases; •sales and distribution capabilities; •size and financial stability; •breadth of product line; •form factor of the solution; and •other competitive differentiators.

Among others, our competitors include Check Point Software Technologies Ltd. (“Check Point”), Cisco Systems, Inc. (“Cisco”), CrowdStrike Holdings, Inc. (“CrowdStrike”), F5 Networks, Inc. (“F5 Networks”), Hewlett-Packard Enterprise (“HPE”), Huawei Technologies Co., Ltd. (“Huawei”), Microsoft Corporation (“Microsoft”), Netskope Inc. (“Netskope”), Palo Alto Networks, Inc. (“Palo Alto Networks”), SonicWALL, Inc. (“SonicWALL”), Sophos Group Plc (“Sophos”) and Zscaler, Inc. (“Zscaler”).

We believe we compete favorably based on our products’ security performance, throughput, reliability, breadth and ability to work together, our ability to add and integrate new networking and security features and our technological expertise. Several competitors are significantly larger, have greater financial, technical, marketing, distribution, customer support and other resources, are more established than we are, and have significantly better brand recognition. Some of these larger competitors have substantially broader product offerings and leverage their relationships based on other products or incorporate functionality into existing products in a manner that discourages users from purchasing our products. Other, often smaller competitors, may intensely focus on a small group of point solutions and be positioned as a leader in discrete technologies that we compete with. Based in part on these competitive pressures, we may lower prices or attempt to add incremental features and functionalities to our products.

Conditions in our markets could change rapidly and significantly as a result of technological advancements, market consolidation or de-consolidation, supply chain constraints, price list or discount changes or inflation. The development and market acceptance of alternative technologies could decrease the demand for our products or render them obsolete. Our competitors may introduce products that are less costly, provide superior performance, are better marketed, or achieve greater market acceptance than our products. Additionally, our larger competitors often have broader product lines and are better positioned to withstand a significant reduction in capital spending by end-customers, and will therefore not be as susceptible to downturns in a particular market. The above competitive pressures are likely to continue to impact our business. We may not be able to compete successfully in the future, and competition may harm our business.

Our employees are the foundation of our innovation and cybersecurity leadership for the benefit of our customers. We understand there is a shortage of highly skilled employees for security companies like ours, and we believe that our success and competitive advantage depends largely on our ability to continue to attract and retain highly skilled employees. We believe we offer fair, competitive compensation and benefits, and we encourage a merit-based and inclusive culture. Our compensation programs for our employees include base pay, incentive compensation, opportunities for equity ownership where local statutes allow and employee benefits that promote well-being across different aspects of our employees’ lives, which may include health and welfare insurance, retirement benefits and paid time off.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm｜as_of：2026-02-25
<<<
We provide channel partners with specific programs to assist them with selling our products but there can be no assurance that these programs will be effective. In addition, our channel partners may be unsuccessful in marketing, selling and supporting our products and services and may purchase more inventory than they can sell. Our channel partners generally do not have minimum purchase requirements. Some of our channel partners may have insufficient financial resources to withstand changes and challenges in business conditions. Moreover, many of our channel partners are privately held, including some of our largest partners, and we may not have sufficient information to assess their financial condition. If our channel partners’ financial condition or operations weaken, their ability to sell our products and services could be negatively impacted. Our channel partners may also market, sell and support products and services that are competitive with ours, and may devote more resources to the marketing, sales and support of such products, or may decide to cease selling our products and services 18 Table of Contents altogether in favor of a competitor’s products and services. They may also have incentives to promote our competitors’ products to the detriment of our own, or they may cease selling our products altogether.…

The market for network security products is intensely competitive and dynamic, and we expect competition to continue to intensify. We face many competitors across the different cybersecurity markets. Our competitors include companies such as Check Point, Cisco, CrowdStrike, F5 Networks, HPE, Huawei, Microsoft, Netskope, Palo Alto Networks, SonicWALL, Sophos, and Zscaler.

In addition, certain of our larger competitors may have broader product offerings, and leverage their relationships based on other products or incorporate functionality into existing products in a manner that discourages customers from purchasing our products. These larger competitors often have broader product lines and market focus, and are in a better position to withstand any significant reduction in capital spending by end-customers in these markets. Therefore, these competitors will not be as susceptible to downturns in a particular market. Also, many of our smaller competitors that specialize 20 Table of Contents in providing protection from a single type of security threat are often able to deliver these specialized security products to the market more quickly than we can.

Conditions in our markets could change rapidly and significantly as a result of technological advancements or continuing market consolidation. Our competitors and potential competitors may also be able to develop products or services, and leverage new business models, that are equal or superior to ours, achieve greater market acceptance of their products and services, disrupt our markets, and increase sales by utilizing different distribution channels than we do. For example, certain of our competitors are focusing on delivering security services from the cloud which include cloud-based security providers, such as CrowdStrike and Zscaler. In addition, current or potential competitors may be acquired by third parties with greater available resources, and new competitors may arise pursuant to acquisitions of network security companies or divisions. As a result of such acquisitions, competition in our market may continue to increase and our current or potential competitors might be able to adapt more quickly to new technologies and customer needs, devote greater resources to the promotion or sale of their products and services, initiate or withstand substantial price competition, take advantage of acquisition or other opportunities more readily, or develop and expand their product and service offerings more quickly than we do. In addition, our competitors may bundle products and services competitive with ours with other products and services.…

Moreover, business models based on a subscription cloud-based software service have become increasingly in demand by our end-customers and adopted by other providers, including our competitors. While we have introduced additional cloud-based solutions and will continue to do so, most of our platform is currently deployed on premise, and therefore, as customers demand that solutions be provided through a subscription cloud-based business model, we are making additional investments in our infrastructure and personnel to be able to more fully provide our platform through a subscription cloud-based model in order to maintain the competitiveness of our platform. Such investments involve expanding our data centers, servers and networks, and increasing our technical operations and engineering teams and this results in added cost and risks associated with managing new business models, such as obligations to deliver certain functionality and features and to meet certain service level agreements related to cloud-based solutions. There is also a risk that we are slower to offer these solutions than competitors. The risks are compounded by the uncertainty concerning the future success of any of our particular subscription cloud-based business models and the future demand for our subscription cloud-based models by customers. Additionally, if we are unable to meet the demand to provide our services effectively through a subscription cloud-based model, we may lose customers to competitors.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTNT_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
