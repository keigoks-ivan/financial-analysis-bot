你是 stock-analyst v20 DD 的證據採集子 agent。標的：CAT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - CAT Caterpillar market share gaining OR losing 2026
  - Caterpillar new entrant OR displace threat Farm & Heavy Construction Machinery 2026
  - CAT competitor design win 2026
  - Caterpillar vs Farm & Heavy Construction Machinery peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm｜as_of：2026-02-13
<<<
1 Table of Contents The competitive environment for construction machinery is characterized by some global competitors and many regional and specialized local competitors. Examples of global competitors include CASE (part of CNH Industrial N.V.), Deere Construction & Forestry (part of Deere & Company), Doosan Bobcat (Part of Doosan Group), Hitachi Construction Machinery Co., Ltd., Hyundai Construction Equipment Co., Ltd., Hyundai Doosan Infracore Co., Ltd. (both part of Hyundai Heavy Industries Group), J.C. Bamford Excavators Ltd., Kobelco Construction Machinery (part of Kobe Steel, Ltd), Komatsu Ltd., Kubota Farm & Industrial Machinery (part of Kubota Corporation), Sany Heavy Industry Co., Ltd., and Volvo Construction Equipment (part of the Volvo Group). As an example of regional and local competitors, our competitors in China also include Guangxi LiuGong Machinery Co., Ltd., Longking Holdings Ltd., Sany Heavy Industry Co, XCMG Construction Machinery Co., Ltd., Shandong Lingong Construction Machinery Co., Ltd. (SDLG, JV with Volvo Construction Equipment) and Shantui Construction Machinery Co., Ltd., (part of Shandong Heavy Industry Group Co.). Each of these companies has varying product lines that compete with Caterpillar products, and each has varying degrees of regional focus.

The competitive environment for Resource Industries consists of a few larger global competitors that compete in several of the markets that we serve and a substantial number of smaller companies that compete in a more limited range of products, applications, and regional markets. Our global surface competitors include Deere Construction & Forestry (part of Deere & Company), Epiroc AB, Hitachi Construction Machinery Co., Ltd., Komatsu Ltd., Liebherr-International AG, Sandvik AB, and Volvo Construction Equipment. Our global underground competitors include Epiroc AB, Komatsu Ltd., and Sandvik AB.

The competitive environment for reciprocating engines in marine, oil and gas, industrial and electric power generation systems along with turbines in oil and gas and electric power generation consists of a few larger global competitors that compete in a variety of markets that Caterpillar serves, and a substantial number of smaller companies that compete in a limited-size product range, geographic region and/or application. Principal global competitors include Cummins Inc., Deutz AG, Rolls-Royce Power Systems AG and Siemens Energy AG. Other competitors, such as Volvo Penta AB, FPT Industrial SpA (Iveco Group), INNIO Group, GE Vernova Inc., Kawasaki Heavy Industries Ltd., Everllence SE (formerly MAN Energy Solutions SE), Weichai Power Co., Ltd., and other emerging market competitors compete in certain markets in which Caterpillar competes. An additional set of competitors, including Aggreko plc, Generac Holdings Inc., Discovery Energy, LLC (Rehlko, formerly Kohler Energy), Baker Hughes Co., and others, are primarily packagers who source engines and/or other components from domestic and international suppliers and market products regionally and internationally through a variety of distribution channels. In rail-related businesses, our global competitors include Wabtec Corp, Greenbrier Companies, Inc., Voestalpine AG, Vossloh AG, Alstom SA, and Siemens Mobility A/S. We also compete with other companies on a more limited range of products, services and/or geographic regions.

Cat Financial operates in a highly competitive environment, with financing for users of Caterpillar equipment and services available through a variety of sources, principally commercial banks and finance and leasing companies. Cat Financial’s competitors include Wells Fargo Equipment Finance Inc., Banc of America Leasing & Capital LLC, BNP Paribas Leasing Solutions Limited, Australia and New Zealand Banking Group Limited, Société Générale S.A. and various other banks and finance companies. In addition, many of the manufacturers that compete with Caterpillar also own financial subsidiaries, such as John Deere Capital Corporation, Komatsu Financial L.P., Volvo Financial Services and Kubota Credit Corporation, which utilize many below-market interest rate programs (funded by the manufacturer) to support machine sales. Cat Financial works with the broader Caterpillar organization to provide a broad array of financial merchandising programs to compete around the world.

Cat Financial provides financing only when certain criteria are met. Credit decisions are based on a variety of credit quality factors including prior payment experience, customer financial information, credit ratings, loan-to-value ratios and other internal metrics. Cat Financial typically maintains a security interest in retail-financed equipment and generally requires physical damage insurance coverage on financed equipment. Cat Financial finances a significant portion of Caterpillar dealers’ sales and inventory of Caterpillar equipment throughout the world. Cat Financial’s competitive position is improved by marketing programs offered in conjunction with Caterpillar and/or Caterpillar dealers. Under these programs, Caterpillar, or the dealer, funds an amount at the outset of the transaction, which Cat Financial then recognizes as revenue over the term of the financing. We believe that these marketing programs provide Cat Financial a significant competitive advantage in financing Caterpillar products.

5 Table of Contents Competitive Environment Caterpillar products and services are sold worldwide into a variety of highly competitive markets. In all markets, we compete on the basis of product performance, customer service, quality and price. From time to time, the intensity of competition results in price discounting in a particular industry or region. Such price discounting puts pressure on margins and can negatively impact operating profit. Outside the United States, certain competitors enjoy competitive advantages inherent to operating in their home countries or regions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-13）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/18230/000001823026000008/cat-20251231.htm｜as_of：2026-02-13
<<<
We operate in a highly competitive environment. We compete on the basis of a variety of factors, including product performance, customer service, quality and price. There can be no assurance that our products will be able to compete successfully with other companies’ products. Thus, our share of industry sales could be reduced due to aggressive pricing or product strategies pursued by competitors, unanticipated product or manufacturing difficulties, our failure to price our products competitively, our failure to produce our products at a competitive cost or an unexpected buildup in competitors’ new machine or dealer-owned rental fleets, which could lead to downward pressure on machine rental rates and/or used equipment prices.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAT_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
