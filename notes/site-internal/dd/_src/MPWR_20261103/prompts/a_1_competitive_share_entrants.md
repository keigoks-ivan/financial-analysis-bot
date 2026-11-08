你是 stock-analyst v20 DD 的證據採集子 agent。標的：MPWR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MPWR Monolithic Power Systems market share gaining OR losing 2026
  - Monolithic Power Systems new entrant OR displace threat Semiconductors 2026
  - MPWR competitor design win 2026
  - Monolithic Power Systems vs Semiconductors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm｜as_of：2026-02-27
<<<
Our product families are differentiated from those of our competitors with respect to their high degree of integration and strong levels of accuracy, power efficiency, quality and longevity, making them cost-effective and more sustainable relative to many competing solutions. For example, DC to DC solutions are used to convert and control voltages within a broad range of electronic systems, such as cloud-based and on-premises CPU servers and workstations, AI systems, memory, storage solutions, notebooks, infotainment, power sources, home appliances, network infrastructure and satellite communications. We believe our DC to DC products are differentiated in the market, particularly with respect to their high degree of integration, high voltage operation, high load current, high switching speed, small footprint, and high energy efficiency. These features are important to our customers as they are designed to result in fewer components that need to be produced and consumed, a smaller form factor, more accurate regulation of voltages, lower power consumption and, ultimately, lower system cost, increased reliability and lower carbon emissions through the elimination of many discrete components and power devices.

Competition The analog and mixed-signal semiconductor industry is highly competitive, and we expect competitive pressures to continue. Our ability to compete effectively and to expand our business will depend on our ability to continue to recruit both applications engineering and design engineering personnel, our ability to introduce new products, our ability to maintain the rate at which we introduce these new products, and our ability to meet our end customers’ energy efficiency goals. Our industry is characterized by decreasing average selling prices over the life of a product. We compete with domestic and international semiconductor companies, many of which have substantially greater financial and other resources with which to pursue engineering, manufacturing, marketing, and distribution of their products. In some cases, our competitors have a broader number of product offerings that may enable them to more effectively market and sell to customers and engage sales partners.

We are in direct and active competition, with respect to one or more of our product lines, with several manufacturers of such products. We consider our primary competitors to include Analog Devices, Infineon Technologies, NXP Semiconductors, ON Semiconductor, Power Integrations, Renesas Electronics, ROHM Semiconductor, Semtech, STMicroelectronics and Texas Instruments.

9 Table of Contents We expect continued competition from existing competitors as well as competition from new entrants into the semiconductor market. We believe that we are competitive in the markets in which we sell because our ICs and solutions are typically smaller in size, are highly integrated with lower energy consumption, and achieve higher performance specifications than most of our competitors. However, there is no assurance that our products will continue to compete favorably or that we will be successful in the face of increasing competition from new products introduced by existing competitors or new companies entering our markets. In addition, there has historically been a high level of consolidation in the semiconductor industry. If these or future acquisitions are successful, competition may intensify, as our competitors add resources with which to compete against us.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm｜as_of：2026-02-27
<<<
Our competitiveness and future success depend on our ability to design, develop, manufacture, assemble, test, market, and support new products and enhancements on a timely and cost-effective basis. A fundamental shift in technologies in any of our product markets could have a material adverse effect on our competitive position within these markets. Our failure to timely develop new technologies or to react quickly to changes in existing technologies could materially delay our development of new products, which could result in product obsolescence, decreased revenue, and/or a loss of market share to competitors.

The semiconductor industry has a history of consolidation as companies attempt to improve the leverage of growing research and development costs, strengthen or hold their market positions in an evolving industry, or become unable to continue operations unless they find an acquirer or consolidate with another company. In addition, companies that are strategic alliance partners in some areas of our business may acquire or form alliances with our competitors, thereby reducing their business with us. We believe that semiconductor industry consolidation may result in stronger competitors that are better able to compete as sole-source suppliers of multiple products for customers. This could harm our operating results and could have a material adverse effect on our business, financial condition and results of operations.

We compete against many companies with substantially greater financial and other resources, and our market share may decline if we are unable to respond to our competitors effectively.

The analog and mixed-signal semiconductor industry is highly competitive, and we expect competitive pressures to continue. Our ability to compete effectively and to expand our business will depend on our ability to continue to recruit application and design engineers, introduce new products, and maintain the rate at which we introduce new products. We compete with domestic and foreign semiconductor companies, many of which have substantially greater financial and other resources with which to pursue engineering, manufacturing, marketing, and distribution of their products, and, in some cases, may have broader product offerings that enable them to more effectively market and sell to customers and engage sales partners. We are in direct and active competition with many manufacturers of varying size and financial strength. The number of our competitors has grown due to the expansion of the market segments in which we participate.

We cannot guarantee that our products will continue to compete favorably, or that we will be successful in the face of increasing competition from new products and enhancements introduced by existing competitors or new companies entering our markets, which would materially and adversely affect our results of operations and our financial condition.

In addition, from time to time, governments may provide subsidies or make other investments that could give competitive advantages to competing semiconductor companies. For example, in August 2022, the U.S. enacted the CHIPS Act, which, among other things, provides funding to increase domestic production and research and development in the semiconductor industry. Because we operate a fabless business model, we are not eligible for such investments. Many of our competitors benefit from these and other investments, which helps increase their production capacities, shorten their lead times and gain market share. These competitive pressures could materially and adversely affect our business, financial condition and results of operations.

In addition, if new competitors, technological advances by existing competitors, our entry into new markets, or other competitive factors require us to invest significantly greater resources than anticipated in our research and development efforts, our operating expenses would increase further. If we are required to invest significantly greater resources than anticipated in research and development efforts without a corresponding increase in revenue, our operating results could be harmed. Many of our competitors have significantly greater resources than we have and are able to invest substantially greater amounts into research and development initiatives than we are, which could reduce the technological advances that we may be able to achieve and may harm our ability to compete. In order to remain competitive, we anticipate that we will continue to devote substantial resources to research and development, and we expect these expenses to increase in the foreseeable future due to the increased complexity and the greater number of products under development.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MPWR_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
