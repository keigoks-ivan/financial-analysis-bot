你是 stock-analyst v20 DD 的證據採集子 agent。標的：STM。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - STM STMicroelectronics antitrust OR monopoly investigation 2026
  - STMicroelectronics regulation OR regulatory scrutiny Semiconductors 2026
  - STM STMicroelectronics DOJ OR FTC OR EU competition 2026
  (na_allowed=true)


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 8. Financial Information（含 8.A.7 Legal Proceedings）｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
Item 8. Financial Information
Consolidated Statements and Other Financial Information
Please see “Item 18. Financial Statements” for a list of the financial statements filed with this Form 20-F.
Legal Proceedings
For a description of our material pending legal proceedings, please see Note 26 “Commitments, Contingencies, Claims and Legal Proceedings” to our Consolidated Financial Statements, which is incorporated herein by reference.
Dividend Policy
Our dividend policy reads as follows: “STMicroelectronics seeks to use its available cash in order to develop and enhance its position in a competitive semiconductor market while at the same time managing its cash resources to reward its shareholders for their investment and trust in STMicroelectronics. Based on its results, projected capital requirements as well as business conditions and prospects, the Managing Board proposes on an annual basis to the Supervisory Board, whenever deemed possible and desirable in line with STMicroelectronics’ objectives and financial situation, the distribution of a quarterly cash dividend, if any. The Supervisory Board, upon the proposal of the Managing Board, decides or proposes on an annual basis, in accordance with this policy, which portion of the profits or distributable reserves shall not be retained in reserves to fund future growth or for other purposes and makes a proposal concerning the amount, if any, of the quarterly cash dividend”.
On May 28, 2025, our shareholders approved a cash dividend of US$0.36 per outstanding share of our common stock, which was distributed in quarterly installments of US$0.09 in each of the second, third and fourth quarters of 2025 and will also be distributed in the first quarter of 2026. Future dividends, if any, and their timing and amounts may be affected by our accumulated profits, our capacity to generate cash flow, our financial situation, the general economic situation and prospects and any other factors that the Supervisory Board, upon the recommendation of our Managing Board, shall deem important. For a history of dividends paid by us to our shareholders in the past three years, see Note 18 to our Consolidated Financial Statements “Shareholders’ Equity – Dividends”.
Item 9. Listing
Market Information…
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
Further, throughout 2025 the current U.S. administration initiated numerous investigations into products and industries under section 232 of the Trade Expansion Act of 1962. For example, in April 2025, the Department of Commerce launched an investigation into the national security impacts of imported semiconductors and semiconductor manufacturing equipment. This investigation may result in additional tariffs and trade restrictions that may adversely impact the semiconductor industry and our business. Similar investigations on other industries or products, including automotive, copper, steel, aluminium, critical minerals and aircraft, may also adversely impact the semiconductor industry and our business.

Pillar II enforces a global minimum corporate income tax at an effective rate of 15% for large multinationals. On December 20, 2021 the OECD published the Global Anti-Base Erosion Model Rules ("GloBe Rules") for Pillar II. On December 22, 2021, the European Commission published a legislative proposal for Pillar II (the "EU Pillar II Directive" or "Pillar II").
>>>

[3] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
(3) Fab 3 is currently shared between the Company and Tower Semiconductor. (4) The joint 300mm semiconductor manufacturing facility with GlobalFoundries Inc in Crolles, France, which has received European Commission approval, has a projected cost of €7.5 billion of capital expenditure, maintenance and ancillary costs and will benefit from financial support of up to roughly €2.9 billion from the State of France in line with the European Chips Act.

In December 2018, the European Commission announced the approval of the IPCEI on Microelectronics ("IPCEI ME"), a pan-European project initiated to foster research and innovation in microelectronics to be funded by Germany, France, Italy, the U.K. and Austria.

On October 4, 2022, the European Commission approved, under EU State Aid rules, a support up to €292.5 million through the Italian Recovery and Resilience Plan for the construction of a new integrated SiC substrate manufacturing facility in Catania, Italy. In 2025 we recognized grants of €9.2 million related to this project.

On May 31, 2024, the European Commission approved, under the EU State Aid rules, an Italian aid measure to support the Company in the construction and operation of an integrated chip manufacturing plant for SiC power devices in Catania, Italy. The aid will take the form of a €2 billion direct grant to ST to support its planned investment of €5 billion in capital expenditure. The measure will strengthen Europe's security of supply, resilience and digital sovereignty in semiconductor technologies. The measure will also contribute to achieving the digital and green transitions. On October 13, 2025, the European Commission formally granted ST the status of Integrated Production Facility ("IPF") as referenced in the European Chips Act.
>>>

[4] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-02-26）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm｜as_of：2026-02-26
<<<
56 Other claims. We are subject to the possibility of loss contingencies arising in the ordinary course of business. These include but are not limited to: product liability claims and/or warranty costs on our products, contractual disputes, indemnification claims, employee grievances, tax claims beyond assessed uncertain tax positions as well as claims for environmental damages. We are also exposed to numerous legal risks which until now have not resulted in legal disputes and proceedings. These include risks related to product recalls, environment, shareholder rights, tariffs and export control regulations, anti-trust, anti-corruption, competition as well as other compliance regulations. We may also face claims in the event of breaches of law committed by individual employees or third parties. In determining loss contingencies, we consider the likelihood of a loss of an asset or the occurrence of a liability, as well as our ability to reasonably estimate the amount of such loss or liability. An estimated loss is recorded when we believe that it is probable that a liability has been incurred and the amount of the loss can be reasonably estimated. We regularly re-evaluate any potential losses and claims and determine whether our provisions need to be adjusted based on the current information available to us.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
