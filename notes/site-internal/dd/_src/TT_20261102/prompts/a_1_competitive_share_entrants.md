你是 stock-analyst v20 DD 的證據採集子 agent。標的：TT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - TT Trane Technologies market share gaining OR losing 2026
  - Trane Technologies new entrant OR displace threat Building Products & Equipment 2026
  - TT competitor design win 2026
  - Trane Technologies vs Building Products & Equipment peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-05）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm｜as_of：2026-02-05
<<<
Competitive Conditions Our products and services are sold in highly competitive markets throughout the world. Due to the diversity of these products and services and the variety of markets served, we encounter a wide variety of competitors that vary by product line and services. They include well-established regional or specialized competitors, as well as larger U.S. and non-U.S. corporations or divisions of larger companies.

Competitive Pay and Benefits Trane Technologies' compensation programs and policies are designed to align the compensation of our employees with the Company's performance and strategy, to attract and retain a talented workforce and to meet the needs of employees globally. We are committed to providing competitive and equitable wages and benefits that allow our employees to thrive at work and at home. In addition, the structure of our compensation programs balance incentive earnings for both long-term and short-term performance with our annual incentive plan closely tied to our financial goals as well as progress toward our 2030 Sustainability Commitments. We further align our leadership globally, fostering collaboration to drive profitable, market-leading revenue growth.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-05）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm｜as_of：2026-02-05
<<<
We face significant competition in the markets that we serve. The markets that we serve are highly competitive. We compete worldwide with a number of other manufacturers and distributors that produce and sell similar products. There has been consolidation and new entrants (including non-traditional competitors) within our industries and there may be future consolidation and new entrants, either of which could result in increased competition and pricing pressures and significantly alter the dynamics of the competitive landscape in which we operate. Due to our global footprint we are competing worldwide with large companies and with smaller, local operators who may have customer, regulatory or economic advantages in the geographies in which they are located. In addition, some of our competitors may employ pricing and other strategies that are not traditional. While we understand our markets and competitive landscape, there is always the risk of disruptive technologies coming from companies that are not traditionally manufacturers or service providers of our products. Refer to "Item 1. Business" for additional details. As we integrate acquisitions into our portfolio of solutions, we may face new competitors in our target markets and incur increased competition from alternative solutions, which could lead to decreased demand or reduced market share for our products and services.…

We must efficiently and effectively innovate, develop and commercialize new and enhanced products and services in a rapidly changing technological and business environment in order to remain competitive in our current and future markets and in order to continue to grow our business. The timely development and commercialization of new products and services and the enhancement of existing products and services is required to meet our customer demands, market trends, and regulatory requirements. The ongoing refreshment of our product and service offerings portfolio requires strategic choices of a significant investment of resources, anticipation of the opportunity and risks of new technologies, and the ability to compete with others who may have superior resources in specific technology domains. We cannot provide any assurance that any new or enhanced product or service will be successfully commercialized in a timely manner, if ever, or, if commercialized, will result in returns greater than our investment. Investment in a product or service could divert our attention and resources from other projects that become more commercially viable in the market. We also cannot provide any assurance that any new or enhanced product or service will be accepted by our current and future markets. The accelerating pace of technological change increases the risk of shortened product lifecycles.…

Nonetheless, this intellectual property may be subject to challenge, infringement, invalidation or circumvention by third parties. Despite extensive security measures, our intellectual property may be subject to misappropriation through unauthorized access of our information technology systems, employee theft, or theft by private parties or foreign actors, including those affiliated with or controlled by state actors. Our business and competitive position could be harmed by such events. We also rely on nondisclosure and noncompetition agreements with certain employees, contractors, and other parties to protect, in part, trade secrets and other proprietary rights. There can be no assurance that these agreements will adequately protect our trade secrets and other proprietary rights and will not be breached, that we will have adequate remedies for any breach, that others will not independently develop substantially equivalent proprietary information, or that third parties will not otherwise gain access to our trade secrets or other proprietary rights. Our ability to protect our intellectual property rights by legal recourse or otherwise may be limited, particularly in countries where laws or enforcement practices are inadequate or undeveloped. Our inability to enforce our IP rights under any of these circumstances could have an impact on our competitive position and business.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-05）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm｜as_of：2026-02-05
<<<
Given our broad range of products manufactured and geographic markets served, management uses a variety of factors to predict the outlook for the Company. We monitor key competitors and customers in order to gauge relative performance and the outlook for the future. We regularly perform detailed evaluations of the different market segments we serve to proactively detect trends and to adapt our strategies accordingly, including potential triggers and actions to be taken under recessionary and other macroeconomic scenarios. In addition, we believe our backlog and order levels are indicative of future revenue and thus are a key measure of anticipated performance.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TT_20261102/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
