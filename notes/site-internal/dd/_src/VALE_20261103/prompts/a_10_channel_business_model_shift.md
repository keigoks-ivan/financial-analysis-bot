你是 stock-analyst v20 DD 的證據採集子 agent。標的：VALE。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Vale distribution channel disruption OR shift 2026
  - VALE Vale business model transition subscription OR platform 2026
  - Other Industrial Metals & Mining channel disintermediation D2C 2026
  - Vale go-to-market change 2026


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
Substantially all of our iron ore production from the Northern System is transported from Carajás, in the Brazilian state of Pará, to the port of Ponta da Madeira, in the Brazilian state of Maranhão, through the Carajás railroad (EFC). Any interruption of the Carajás railroad or of the port of Ponta da Madeira could significantly impact our ability to sell our production from the Northern System. With respect to the Carajás railroad, there is particular risk of interruption at the bridge over the Tocantins River, in which the trains run on a single line railway. In the port of Ponta da Madeira, there is particular risk of interruption at the São Marcos access channel, a deep-water channel that provides access to the port. Also, any failure or interruption of our long-distance conveyor belt used to transport our iron ore production from the S11D mine to the beneficiation plant, could adversely impact our operations at the S11D mine.

Electrical power for the Sudbury operations is primarily sourced from grid supply approximately 70%, considering that a portion of the demand is met by our hydroelectric power facilities. In Sudbury, all incoming grid-connected power and hydroelectric generation is distributed to mines and processing plants through our electrical distribution network, consisting of 69 kV distribution power lines, substations, transformers, breakers, disconnects and other electrical equipment. This distribution system is owned, operated, and maintained by us. We consume 100% of our self-generated hydro generation. The hydroelectric facilities have a nameplate capacity of 55 MWh.

We make cash distributions on the common shares underlying the ADSs in reais to the custodian on behalf of the depositary. The custodian then converts such proceeds into U.S. dollars and transfers such U.S. dollars to be delivered to the depositary for distribution to holders of ADRs net of the depositary’s fees. For information on taxation of dividend distributions, see Additional Information—Taxation—Brazilian Tax Considerations.

VALE ANNUAL REPORT FORM 20-F | 185 Table of Contents BYLAWS Distributions classified as interest on equity Brazilian companies are permitted to pay limited amounts to shareholders and treat such payments as an expense for Brazilian income tax purposes. Our bylaws provide for the distribution of interest on shareholders’ equity as an alternative form of payment to shareholders. The interest rate applied is limited to the Brazilian long-term interest rate, or TJLP, for the applicable period. The deduction of the amount of interest paid cannot exceed the greater of (1) 50% of net income (after the deduction of the provision of social contribution on net profits and before the deduction of the provision of the corporate income tax) before taking into account any such distribution for the period in respect of which the payment is made or (2) 50% of the sum of retained earnings and profit reserves. Any payment of interest on shareholders’ equity is subject to Brazilian withholding income tax. See Additional Information—Taxation—Brazilian Tax Considerations. Under our bylaws, the amount paid to shareholders as interest on shareholders’ equity (net of any withholding tax) may be included as part of any mandatory and minimum dividend.…

generally will be taxable to you as foreign source dividend income and generally will not be eligible for the dividends-received deduction allowed to corporate shareholders under U.S. federal income tax law. The amount of any such distribution will include the amount of Brazilian withholding taxes, if any, withheld on the amount distributed. To the extent that a distribution exceeds our current and accumulated earnings and profits, such distribution will be treated as a nontaxable return of capital to the extent of your basis in the ADSs or common shares, as the case may be, with respect to which such distribution is made, and thereafter as a capital gain.

Whistleblower Channel Any breaches of our policies and standards can be reported by anyone, including employees, contractors, suppliers, members of affected communities and other stakeholders, via our Whistleblower Channel, which is available in 8 languages. Our Whistleblower Channel is managed by our Audit and Compliance Department, an independent department that reports directly to the Board of Directors. Our Whistleblower Channel is structured to guarantee confidentiality and to protect whistleblower anonymity and the rights of the investigated party.

Our employees and contractors in Brazil and Canada also have access to our Respect Channel (Canal de Acolhimento), which is a channel operated by a specialized and independent team to listen, understand and guide anyone reporting harassment or discrimination. By calling this line, the person may decide whether or not to register an allegation, which is then investigated by our Whistleblower Channel team.

In 2025, our Whistleblower Channel received 10,151 reports and closed 10,079 cases, of which (i) 14% referred to queries and reports that were not investigated due to lack of information or pertinence to the scope of the Whistleblower Channel, (ii) 29% were complaints, which were answered by the Whistleblower Channel, but did not lead to an investigation, and (iii) 57% were allegations that led to investigations, which confirmed violations of Vale’s Code of Conduct in 54% of these cases.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
