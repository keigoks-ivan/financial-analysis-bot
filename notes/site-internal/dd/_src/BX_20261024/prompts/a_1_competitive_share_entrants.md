你是 stock-analyst v20 DD 的證據採集子 agent。標的：BX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - BX market share gaining OR losing 2026
  - new entrant OR displace threat 2026
  - BX competitor design win 2026
  - vs peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm｜as_of：2026-02-27
<<<
Competition The asset management industry is intensely competitive, and we expect it to remain so. We compete both globally and on a regional, industry and sector basis. We compete on the basis of a number of factors, including investment performance, transaction execution skills, access to capital, access to and retention of qualified personnel, reputation, range of products and services, innovation and price.

We face competition in the pursuit of institutional and individual investors for our investment funds. Although over time many institutional and individual investors have increased the amount of capital they commit to alternative investment funds, such increases may create increased competition with respect to fees charged by our funds. In the private wealth and insurance channels, the market for capital is highly competitive, requires significant investment and is highly regulated, which could create competitive challenges for us. In addition, competition for fundraising in the private wealth and insurance channels is also driven by the willingness of certain of our competitors to charge lower fees or pay higher or different types of distributors fees.

We also face competition in the pursuit of attractive investment opportunities for our funds. Depending on the investment, we face competition primarily from sponsors managing other funds, investment vehicles and other pools of capital, other financial institutions and institutional investors (including sovereign wealth and pension funds), corporate buyers and other parties. Several of these competitors have significant amounts of capital and many of them have investment objectives similar to ours, which may create additional competition for investment opportunities. Some of these competitors may also have a lower cost of capital and access to funding sources or other resources that are not available to us, which may create competitive disadvantages for us with respect to investment opportunities. In addition, some of these competitors may have higher risk tolerances, different risk assessments or lower return thresholds, which could allow them to consider a wider variety of investments and to bid more aggressively than us for investments. Corporate buyers may be able to achieve synergistic cost savings with regard to an investment or be perceived by sellers as otherwise being more desirable bidders, which may provide them with a competitive advantage in bidding for an investment.

In all of our businesses, competition is also intense for the attraction and retention of qualified employees. Our ability to continue to compete effectively in our businesses will depend upon our ability to attract new employees and retain and motivate our existing employees.

For additional information concerning the competitive risks that we face, see “—Item 1A. Risk Factors — Risks Related to Our Business — The asset management business is intensely competitive.”

As discussed below, we seek to retain and incentivize the performance of our employees through our compensation structure. We also enter into non-competition and non-solicitation agreements with certain employees. See “Part III. Item 11. Executive Compensation — Non-Competition and Non-Solicitation Agreements” for a description of the material terms of such agreements.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm｜as_of：2026-02-27
<<<
The asset management business is intensely competitive. Our asset management business competes with a number of private funds, specialized investment funds, funds structured for individual investors, hedge funds, funds of hedge funds and other sponsors managing pools of capital, as well as corporate buyers, traditional asset managers, commercial banks, investment banks and other financial institutions (including sovereign wealth funds). We expect that competition will continue to increase. For example, certain traditional asset managers have developed their own private equity and private wealth platforms and are marketing other asset allocation strategies as alternatives to hedge fund investments. A number of factors serve to increase our competitive risks: • a number of our competitors have greater financial, technical, research, marketing and other resources and more personnel than we do, • some of our funds may not perform as well as competitors’ funds or other available investment products, 28 Table of Contents • several of our competitors have significant amounts of capital, and many of them have similar investment objectives to ours, which may create additional competition for investment opportunities and may reduce the size and duration of pricing inefficiencies that many alternative investment strategies seek to exploit, • some of our competitors, particularly strategic competitors, may have a lower cost of capital, which may be exacerbated by limits on the deductibility of interest expense, • some of…

We may lose investment opportunities if we do not match investment prices, structures and terms offered by competitors. Alternatively, we may experience decreased rates of return and increased risks of loss if we match investment prices, structures and terms offered by competitors. Moreover, if we are forced to compete with other 29 Table of Contents alternative asset managers on the basis of price, we may not be able to maintain our current fund fee and carried interest terms. We have historically competed primarily on the performance of our funds, and not on the level of our fees or carried interest relative to those of our competitors. However, there is a risk that fees and carried interest in the alternative investment management industry will decline, without regard to the historical performance of a manager. Further, as part of a shift in the distribution arrangements in the private wealth industry, certain third-party intermediaries have sought to revise existing or implement new fee arrangements that align their fees with the initial amount or ongoing net asset value of capital invested through the intermediary in the applicable vehicle.…

There is no guarantee that the non-competition and non-solicitation agreements to which our senior managing directors and other key personnel are subject, together with our other arrangements with them, will prevent them from leaving, joining our competitors or otherwise competing with us. Such agreements also expire after a certain period of time, at which point such personnel would be free to compete against us and solicit our clients and employees. In addition, such agreements may not be enforceable in all cases, particularly as legislatures or regulators enact legislation or adopt rules aimed at effectively prohibiting non-competition agreements. For example, legislation that would prohibit post-employment non-competition agreements except in limited circumstances has been introduced in New York.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BX_20261024/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
