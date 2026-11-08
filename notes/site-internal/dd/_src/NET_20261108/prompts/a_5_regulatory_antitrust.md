你是 stock-analyst v20 DD 的證據採集子 agent。標的：NET。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - NET Cloudflare antitrust OR monopoly investigation 2026
  - Cloudflare regulation OR regulatory scrutiny Software - Infrastructure 2026
  - NET Cloudflare DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
Item 3. Legal Proceedings
From time to time we are subject to legal proceedings and claims arising in the ordinary course of business. We are not presently a party to any legal proceeding that we believe is likely to have a material impact on our business, results of operations, or financial condition.
Future litigation may be necessary, among other things, to defend ourselves or our customers by determining the scope, enforceability, and validity of third-party proprietary rights or to establish our proprietary rights. The results of any litigation cannot be predicted with certainty, particularly in the areas of unsettled and evolving law in which we operate, and an unfavorable resolution in any legal proceedings could materially affect our future business, results of operations, or financial condition. Regardless of the outcome, litigation can have an adverse impact on us because of defense and settlement costs, diversion of management resources, and other factors. For additional information, see "Risk Factors - Activities of our paying and free customers or the content of their websites and other Internet properties may violate applicable laws and/or our terms of service and could subject us to lawsuits, regulatory enforcement actions, and/or liability in various jurisdictions" and "We are currently, and may be in the future, party to intellectual property rights claims and other litigation matters that, if resolved adversely, could have a material impact on our business, results of operations, or financial condition" and Note 8 to the consolidated financial statements included in this Annual Report on Form 10-K.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1477333/000147733326000016/cloud-20251231.htm｜as_of：2026-02-26
<<<
In addition, we must comply with laws and regulations relating to the formation, administration, and performance of contracts with the public sector, including U.S. federal, state, and local governmental organizations, as well as 33 Table of contents foreign governmental organizations, which affect how we and our channel partners do business with governmental agencies. Selling our products to the U.S. government, whether directly or through channel partners, also subjects us to certain regulatory and contractual requirements, including expanded compliance obligations under the Federal Acquisition Regulations. Failure to comply with these laws, regulations, and requirements by either us or our channel partners could subject us to investigations, fines, and other penalties, which could have an adverse effect on our business, results of operations, and financial condition. For example, the U.S. Department of Justice (DOJ) and the General Services Administration (GSA) have in the past pursued claims against and financial settlements with vendors under the False Claims Act and other statutes related to misrepresenting cybersecurity practices or protocols, pricing and discount practices and compliance with certain provisions of GSA contracts. The DOJ and GSA continue to actively pursue such claims. Violations of certain regulatory and contractual requirements could also result in us being suspended or debarred from future government contracting.…

In addition, we may not be able to find suitable acquisition candidates and we may not be able to complete acquisitions on favorable terms, if at all. If we identify companies that we would like to buy, we may also face antitrust, competition, and other regulatory scrutiny that may limit our ability to complete such acquisitions. If we do complete acquisitions, we may not ultimately strengthen our competitive position or achieve our goals, and any acquisitions we complete could be viewed negatively by customers, developers, or investors. In addition, we may not be able to integrate acquired businesses successfully or effectively manage the combined company following an acquisition. If we fail to successfully integrate our acquisitions, or integrate and retain the people, technologies, business partners, or customers associated with those acquisitions, into our company, the results of operations of the combined company could be adversely affected. Any integration process in connection with an acquisition will require significant time and resources, require significant attention from management, and disrupt the ordinary functioning of our business, and we may not be able to manage the process successfully, which could adversely affect our business, results of operations, and financial condition.…

This is especially true regarding the cross-border transfer of personal data. For example, in July 2023, the European Commission adopted an adequacy decision for the EU-U.S. Data Privacy Framework, which generally allows the free flow of EU personal data to the United States for participating entities. While this framework currently serves as a means for cloud service providers like our company to freely transfer EU personal data to the United States, it may be subject to future legal challenges, suspension, amendment, repeal, or limitations to its scope by the 51 Table of contents European Commission. In addition, some customers and vendors may be unwilling to rely on this framework due to these and other uncertainties, including perceived uncertainty about the U.S. stance on the existing legal framework. In addition, in January 2023, the European Data Protection Board issued its 2022 Coordinated Enforcement Action on the use of cloud-based services by the public sector, in which it expressed concerns that EU public sector entities may not be able to use U.S.-based cloud service providers consistently with GDPR due to their concerns about the ability of U.S. government agencies to access EU personal data.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
