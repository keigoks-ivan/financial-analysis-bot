你是 stock-analyst v20 DD 的證據採集子 agent。標的：META。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
  - META Meta Platforms antitrust OR monopoly investigation 2026
  - Meta Platforms regulation OR regulatory scrutiny Internet Content & Information 2026
  - META Meta Platforms DOJ OR FTC OR EU competition 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
Item 3.Legal Proceedings
As a multinational company with a complex and evolving business, we are, and expect to continue to be, subject to numerous claims, litigation, regulatory, tax, and government inquiries and investigations, and other legal proceedings in jurisdictions around the world. Although we believe many of these matters are without merit and are vigorously defending them, we may not be successful. Any litigation to which we are a party may be resolved adversely or we may be subject to an unfavorable judgment that may not be reversed upon appeal. We may also decide to settle litigation, disputes, or other legal proceedings in some instances on terms that are unfavorable to us. In addition, we may become subject to orders or consent decrees imposed by government or regulatory authorities. Any such developments could cause us to incur substantial costs, expose us to civil and criminal liability (including liability for our personnel) or penalties (including substantial monetary remedies), interrupt or require us to change our business practices in a manner materially adverse to our business (including changes to our products and services or user data practices), result in negative publicity and reputational harm, divert resources and the time and attention of management from our business, or subject us to other structural or behavioral remedies that adversely affect our business. We have experienced such outcomes to varying degrees in the past, and we expect to continue to face a challenging litigation and regulatory environment, including in light of complex and evolving laws and regulations, as well as the scale of our business and the size of our user and advertiser base.
Over the last several years, the number and potential significance of the litigation and investigations involving the company have increased, and there can be no assurance that this trend will not continue.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
We receive formal and informal inquiries from government authorities and regulators regarding our compliance with laws and regulations, many of which are evolving and subject to interpretation. We are and expect to continue to be the subject of investigations, inquiries, data requests, requests for information, actions, and audits in the United States, Europe, and around the world, particularly in the areas of privacy, data use, data combination, and data protection, including with respect to processing of sensitive data, data from third parties, data for advertising purposes, data security, minors, data subject rights, safety, law enforcement, consumer protection, civil rights, content and content moderation, use of our platform for illegal, illicit, or otherwise objectionable activity, competition, consumer hardware and software, including virtual reality technology and products, AI, generative AI, and machine learning. In addition, we are currently, and may in the future be, subject to regulatory orders or consent decrees. For example, data protection, competition, content, and consumer protection authorities in the European Union, United States, and other jurisdictions have initiated actions, investigations, or administrative orders seeking to restrict the ways in which we collect and use information, or impose sanctions, and other 39 Table of Contents authorities may do the same.…

We are also subject to various litigation and formal and informal inquiries and investigations by competition authorities in the United States, Europe, and other jurisdictions, which relate to many aspects of our business, including with respect to users and advertisers. Such inquiries, investigations, and lawsuits concern, among other things, our business practices in the areas of social networking or social media services, messaging services, digital advertising, and/or mobile or online applications, as well as our acquisitions. For example, beginning in 2019, we became the subject of antitrust inquiries and investigations by the FTC and the U.S. Department of Justice. Beginning in 2020, we became subject to a lawsuit by the FTC alleging that we violated antitrust laws, including by acquiring Instagram in 2012 and WhatsApp in 2014. The complaint seeks a permanent injunction against our company's alleged violations of the antitrust laws, and other equitable relief, including divestiture or reconstruction of Instagram and WhatsApp. In addition, in November 2024, the European Commission issued a fine as a result of its finding that we tied Facebook Marketplace to Facebook and use data in a manner that infringes European Union competition rules. We are also subject to other government inquiries and investigations relating to our business activities and disclosure practices.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 3. Legal Proceedings｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
53 Table of Contents Competition We are subject to various litigation and government inquiries and investigations, formal or informal, by competition authorities in the United States, Europe, and other jurisdictions. Such investigations, inquiries, and lawsuits concern, among other things, our business practices in the areas of social networking or social media services, digital advertising, and/or mobile or online applications, as well as our acquisitions. For example, in 2019 we became the subject of antitrust investigations by the FTC and U.S. Department of Justice. On December 9, 2020, the FTC filed a complaint (FTC v. Meta Platforms, Inc.) against us in the U.S. District Court for the District of Columbia alleging that we engaged in anticompetitive conduct and unfair methods of competition in violation of Section 5 of the Federal Trade Commission Act and Section 2 of the Sherman Act, including by acquiring Instagram in 2012 and WhatsApp in 2014 and by maintaining conditions on access to our platform. The FTC sought a permanent injunction against our company's alleged violations of the antitrust laws, and other equitable relief, including divestiture or reconstruction of Instagram and WhatsApp. On June 28, 2021, the court granted our motion to dismiss the complaint filed by the FTC with leave to amend.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/parts/axes_5.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
