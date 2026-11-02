你是 stock-analyst v20 DD 的證據採集子 agent。標的：SOFI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - SOFI SoFi Technologies market share gaining OR losing 2026
  - SoFi Technologies new entrant OR displace threat Credit Services 2026
  - SOFI competitor design win 2026
  - SoFi Technologies vs Credit Services peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm｜as_of：2026-02-17
<<<
Competition to fund prime loans. The prime lending market is highly fragmented and competitive. We face competition from a diverse landscape of consumer lenders, including other banks, credit unions and specialty finance lenders, as well as alternative technology-enabled lenders.

Competition to acquire deposits. Although we now operate a bank, many other banks are larger, have been in business longer and often have greater brand awareness than us. Some large technology and retail companies have large consumer bases and strong balance sheets, which could enhance their competitive ability.

11 SoFi Technologies, Inc. TABLE OF CONTENTS Competition to acquire investment brokerage and crypto trading accounts. We face competition from brokerage platforms that provide some of the same features as us, such as a mobile brokerage experience, robo-investing, fractional share investing, crypto investing and options trading. In addition, the leading incumbent brokerage firms are larger, have been in business longer and generally have greater brand awareness than us. Technology and other companies have begun to offer some basic investing features and the ability to buy and sell digital and other assets.

Competition for technology products and solutions. Generally, these arrangements are multi-year contracts, which require us to spend the necessary resources on implementation and interconnecting new clients onto our platform. We face competition from larger institutions that could make investments into an integrated platform as a service solution or to a cloud-native digital and core banking solution, and also undercut our pricing, preventing our current clients from renewing, while also impeding our attempts to acquire new clients.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm｜as_of：2026-02-17
<<<
Our results of operations and future prospects depend on our ability to retain existing members and attract new members. We face intense and increasing competition and, if we do not compete effectively, our competitive positioning and our operating results will be harmed.

TABLE OF CONTENTS and other resources, and a larger customer base than we do. This allows them to potentially offer more competitive pricing or other terms or features, a broader range of financial products, or a more specialized set of specific products or services, as well as respond more quickly than we can to new or emerging technologies and changes in member preferences. In addition to established enterprises, we may also face competition from early-stage companies, or companies in industries not typically associated with financial services, such as social media and other commerce platforms, attempting to capitalize on the same, or similar, opportunities as we are. Our existing or future competitors may develop products or services that are similar to our products and services or that achieve greater market acceptance than our products and services. This could attract current or potential members away from our services and reduce our market share in the future. Additionally, when new competitors seek to enter our markets, or when existing market participants seek to increase their market share, these competitors sometimes undercut, or otherwise exert pressure on, the pricing terms prevalent in that market, which could adversely affect our market share and/or our ability to capitalize on market opportunities.

Our business is sensitive to interest rates and interest rates are highly sensitive to many factors that are beyond our control, including global, domestic and local economic conditions and the policies of various governmental and regulatory agencies and, in particular, the Federal Reserve. The Federal Reserve increased interest rates throughout 2022 and 2023 before lowering interest rates in 2024 and 2025, and we are unable to predict whether interest rates will increase or decrease in the future. Further changes to prevailing interest rates could influence not only the interest we receive on loans and investments and the amount of interest we pay on deposits and borrowings, but such changes have in the past and could in the future also affect (i) our ability to originate loans at competitive rates; (ii) our ability to pay a competitive variable annual percentage yield for deposits; (iii) the fair value of our financial assets and liabilities; (iv) the average duration of our loan portfolios and other interest-earning assets; (v) the mix of lending products we originate which is influenced by demand for refinancing products; and (vi) the competition faced by our SoFi Money deposit product from other investment products which may become more attractive as interest rates rise.…

We expect that checking and savings, a deposit account product, will continue to provide us with an important source of deposits to use for cost-effective funding of loan originations and other activities. However, revenue growth for checking and savings is dependent on increasing the volume of members who open an account and on growing balances in those accounts. Although our checking and savings account product has grown since its introduction in the first quarter of 2022, there is no guarantee that account openings and the amount on deposit in those accounts will continue to grow. In addition, although we have invested in a number of initiatives to attract new checking and savings account holders and capture a greater share of our members’ savings, including offering a competitive annual percentage yield on deposits and offering SoFi Plus membership benefits to certain deposit holders, there can be no assurance that these investments to acquire and retain members, provide differentiated features and services and spur usage of our deposit account product will be effective or cost effective. There are also no assurances that we will be able to maintain a competitive annual percentage yield on deposits, and members can easily transfer checking and savings account balances to our competitors.…

SoFi Bank accepts deposits and uses the proceeds as a source of funding, with our direct retail deposits becoming a larger proportion of our funding over time. Our deposit product has several features designed to attract consumers, including competitive interest rates, the availability of the SoFi Insured Deposit Program, whereby funds (up to $3 million) are deposited into deposit accounts at banks which are insured by the FDIC up to the applicable limits, and SoFi Plus rewards opportunities. Despite these features, we continue to face strong competition with regard to deposits, and our ability to accept and maintain deposit funding and offer competitive interest rates on deposits is dependent on, among other things, SoFi Bank’s capital levels. The FDIA’s brokered deposit provisions and related FDIC rules in certain circumstances prohibit banks from accepting or renewing brokered deposits and apply other restrictions, such as a cap on interest rates that can be paid. For example, while SoFi Bank met the definition of “well-capitalized” as of December 31, 2025 and currently has no restrictions regarding acceptance of brokered deposits or setting of interest rates, there can be no assurance that we will continue to meet this definition. Additionally, our regulators can adjust applicable capital requirements at any time and have authority to place limitations on our deposit business.…

Competition for certain of our employees, including highly skilled technology and product professionals responsible for the design, engineering and operation of systems, is competitive, which can present a risk as we compete for experienced candidates, especially if the competition is able to offer more attractive financial terms of employment. This risk extends to our current employee population. We also invest significant time and expense in engaging and developing our employees, which 76 SoFi Technologies, Inc.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
