你是 stock-analyst v20 DD 的證據採集子 agent。標的：DECK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - DECK tariff section 232 2026
  - export control OR entity list 2026
  - DECK China tariff OR trade restriction 2026
  - tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-22）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm｜as_of：2026-05-22
<<<
Volatile economic conditions and changes in the market have affected, and may continue to affect, consumer confidence and discretionary spending. A significant portion of our HOKA brand and UGG brand products are premium, discretionary purchases, and demand for these products is sensitive to macroeconomic factors, including inflation, wages and employment, consumer debt, declines in net worth driven by market conditions, interest rates, tariffs, and public health issues such as a pandemic. During periods of economic uncertainty, consumers may reduce discretionary purchases, trade down to lower-priced alternatives, or delay buying decisions, which could require us to increase promotional activity or reduce prices, adversely affecting our sales and profitability.

The production of our finished goods is outsourced to independent manufacturers, the majority of which are in Southeast Asia. During fiscal year 2026, production of our finished goods was predominantly from Vietnam and Indonesia, while less than 5% was from China or any other individual country. As a result, we are exposed to geographic concentration risk arising from regional and global economic conditions, changes in diplomatic and trade relationships (including the imposition of new or increased tariffs), political and social instability, armed conflict, disease outbreaks, natural disasters, and other regulatory, environmental, and geopolitical developments.

The majority of raw materials and components used by our independent manufacturers are sourced from designated suppliers, and tariffs, duties, or other trade restrictions may be imposed, modified, or expanded with limited notice. These measures could require us or our independent manufacturers to seek alternative sourcing options that may not be available in sufficient quantities, at acceptable quality levels, or in a timely manner. Evolving international trade dynamics could materially increase our cost of goods sold, disrupt logistics or inventory flows, adversely affect product pricing and demand, and reduce our gross margin. Customs authorities may also challenge our tariff classifications or treatment of certain products, resulting in additional costs or penalties. In addition, certain tariffs imposed under the International Emergency Economic Powers Act have been invalidated by a recent US Supreme Court decision, and additional tariffs may be invalidated, modified, or refunded in the future. As a result, we may face uncertainty regarding the treatment of tariff-related costs, including the potential recovery or refund of tariff amounts previously paid or partially reflected in selective pricing actions or cost-sharing arrangements. These and other judicial, regulatory, or trade policy developments could increase compliance complexity, create cost volatility, impair our ability to plan sourcing, pricing, and inventory strategies, and result in disputes, claims, unrecoverable costs, and reputational harm, regardless of the ultimate outcome.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-22）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm｜as_of：2026-05-22
<<<
•Diluted earnings per share increased 10.9% to $7.02 per share. Trends And Uncertainties Impacting Our Business And Industry Our business and industry are subject to several important trends and uncertainties, including the following: Macroeconomic and Geopolitical Factors •Macroeconomic factors, including inflationary pressures, increased tariffs, rising supply chain costs, high interest rates, foreign currency exchange rate volatility, escalating global conflicts, changes in discretionary spending, and recession risks, are creating a complex and challenging environment for our business and industry that may continue to pressure our results of operations, including our gross margin. For example, prolonged or escalating conflicts in the Middle East could disrupt our supply chain and increase energy, transportation, and commodity costs, as well as cause shipping delays. While these factors did not materially impact our results of operations during the current period, they could negatively affect us in future periods.

•We are exposed to risks from evolving trade policies, including higher tariffs and restrictions affecting goods imported from certain regions where we have a concentration of sourcing and manufacturing. Recent judicial, regulatory, and administrative developments regarding tariffs imposed under the International Emergency Economic Powers Act and other authorities have increased uncertainty related to both our future duty costs and potential recovery of previously paid duties. The US Customs and Border Protection have announced a phased process for submitting refund requests; however, the availability, timing, and amount of any refunds remain uncertain. As of March 31, 2026, we have not recognized any amounts related to potential tariff refunds or other recoveries. We continue to monitor developments and pursue mitigation strategies, including selective pricing actions, inventory and sourcing management, supplier diversification, and negotiating cost-sharing arrangements; however, we may be unable to offset tariff-related cost impacts, which could materially and adversely affect our gross margin and demand for our products.

Table of Contents 38 Gross Profit. Gross margin decreased to 57.7% from 57.9%, compared to the prior period, primarily due to incremental tariffs on domestic goods and a slightly unfavorable channel mix; partially offset by cost‑sharing arrangements, strategic price increases, and favorable product mix, along with slightly favorable foreign currency exchange rate fluctuations and freight costs.

The increase in total income from operations, compared to the prior period, was primarily due to higher net sales, partially offset by higher SG&A expenses as a percentage of net sales and slightly lower gross margins driven by tariffs.

Table of Contents 39 Drivers of significant net changes in total income from operations, compared to the prior period, were as follows: •The increase in income from operations of the HOKA brand was due to higher net sales, partially offset by lower gross margins driven by tariffs, as well as higher SG&A expenses as a percentage of net sales driven by other SG&A expenses including sales commissions, as well as higher rent and occupancy, payroll and related costs, and advertising, marketing and promotional expenses.

•The increase in income from operations of the UGG brand was due to higher net sales, partially offset by slightly lower gross margins driven by tariffs, as well as higher SG&A expenses as a percentage of net sales primarily driven by advertising, marketing, and promotion expenses, as well as other SG&A expenses including sales commissions.

•The decrease in income from operations of Other brands was primarily driven by the Teva brand from lower net sales and gross margins due to tariffs, along with higher SG&A expenses as a percentage of net sales; combined with lower income from operations driven by the phase out of standalone operations of the Koolaburra brand.

Critical Accounting Estimates The preparation of our consolidated financial statements in accordance with US GAAP requires management to make estimates and assumptions that affect the amounts reported. Management bases these estimates and assumptions upon historical experience, existing and known circumstances, authoritative accounting pronouncements, and other factors it believes to be reasonable. In addition, management has considered the potential impact of macroeconomic and geopolitical factors on our financial condition, results of operations, and liquidity, including inflationary pressures, increased tariffs, rising supply chain costs, high interest rates, foreign currency exchange rate volatility, escalating global conflicts, changes in discretionary spending, and recession risks.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
