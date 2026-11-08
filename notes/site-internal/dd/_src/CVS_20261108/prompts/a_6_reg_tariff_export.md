你是 stock-analyst v20 DD 的證據採集子 agent。標的：CVS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - CVS CVS Health tariff section 232 2026
  - CVS Health export control OR entity list Healthcare Plans 2026
  - CVS CVS Health China tariff OR trade restriction 2026
  - Healthcare Plans tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/64803/000006480326000010/cvs-20251231.htm｜as_of：2026-02-10
<<<
International Regulation - The Company’s international operations are subject to different, and sometimes more stringent, legal and regulatory requirements, which vary widely by jurisdiction, including anti-corruption laws; economic sanctions laws; various privacy, insurance, tax, tariff and trade laws and regulations; corporate governance, privacy, data protection (including the European Union’s (“EU’s”) General Data Protection Regulation which began to apply across the EU during 2018), data mining, data transfer, labor and employment, intellectual property, consumer protection and investment laws and regulations; discriminatory licensing procedures; compulsory cessions of reinsurance; required localization of records and funds; higher premium and income taxes; limitations on dividends and repatriation of capital; and requirements for local participation in an insurer’s ownership. In addition, the presence of operations in foreign countries potentially increases the Company’s exposure to the anti-bribery, anti-corruption and anti-money laundering provisions of U.S. law, including the Foreign Corrupt Practices Act of 1977 (the “FCPA”), and corresponding foreign laws, including the U.K. Bribery Act 2010 (the “UK Bribery Act”).

Office of Foreign Assets Control - The Company also is subject to regulation by the Office of Foreign Assets Control of the U.S. Department of Treasury (“OFAC”). OFAC administers and enforces economic and trade sanctions based on U.S. foreign policy and national security goals against targeted foreign countries and regimes, terrorists, international narcotics traffickers, those engaged in activities related to the proliferation of weapons of mass destruction, and other threats to the national security, foreign policy or economy of the U.S. In addition, the Company is subject to similar regulations in the non-U.S. jurisdictions in which it operates.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/64803/000006480326000010/cvs-20251231.htm｜as_of：2026-02-10
<<<
The political environment in which we operate remains uncertain. It is reasonably possible that our business operations and operating results could be materially adversely affected by legislative, enforcement, regulatory and public policy changes at the federal or state level, including, but not limited to: changes to the regulatory environment for health care and related benefits, including Medicare, Medicare Advantage, the ACA, and related regulations; changes in the 340B program, including the resumption of the Pilot and any expansion thereof; efforts to amend the ACA and related regulations, including through litigation aimed at challenging the ability to enforce portions of the ACA, such as the preventative services mandate; changes to laws or regulations governing drug reimbursement, pricing, purchasing and/or importation; changes to or adoption of laws or regulations governing PBMs, including those related to prohibiting pharmacy licensure for pharmacies affiliated with a PBM, network restrictions, formulary management, affiliate reimbursement, contractual guarantees and reconciliations, reimbursement mandates, required reporting, compensation, purchase discount and/or rebate arrangements with drug manufacturers and/or other PBM services; changes to the laws and regulations governing PBMs’, PDPs’ and/or Managed Medicaid organizations’ interactions with government funded health care programs; changes to or adoption of laws and/or regulations relating to claims processing and billing; changes to immigration policies; changes to patent laws; changes with respect to tax and trade policies, tariffs…

Much of the branded and generic drug product that we sell in our pharmacies, and much of the other merchandise we sell, is manufactured in whole or in substantial part outside of the U.S. In most cases, the products or merchandise are imported by others and sold to us. As a result, significant changes in tax or trade policies, tariffs or trade relations between the U.S. and other countries, such as the imposition of unilateral tariffs on imported products, could result in significant increases in our costs, restrict our access to suppliers, depress economic activity, and have a material adverse effect on our businesses, operating results and cash flows. The current administration has imposed and may further impose, or significantly increase, tariffs on imports to the United States, which could exacerbate many of these issues. In addition, other countries may change their business and trade policies and such changes, as well as any negative sentiments towards the U.S. in response to increased import tariffs and other changes in U.S. trade regulations, including those that are imposed or threatened by the new administration, could adversely affect our businesses.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-10）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/64803/000006480326000010/cvs-20251231.htm｜as_of：2026-02-10
<<<
•Changes in the economic environment, including inflation, the implementation of new tariffs or changes in tariffs, including the impact of tariffs on trade relations between the U.S. and foreign countries, and labor and other market dynamics could create exposure for increased costs and supply chain disruptions that can adversely impact consumer demand, the ability to deliver client savings or the Company’s financial results.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVS_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
