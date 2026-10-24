你是 stock-analyst v20 DD 的證據採集子 agent。標的：BX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - BX tariff section 232 2026
  - export control OR entity list 2026
  - BX China tariff OR trade restriction 2026
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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm｜as_of：2026-02-27
<<<
Geopolitical concerns and other global events outside of our control have contributed and may continue to contribute to volatile global equity and debt markets. These concerns and events include, without limitation, trade conflict, civil unrest, threats to national security, and national and international security events (including war, terrorist acts or other hostilities). Geopolitical instability has been prevalent in recent years, and 2025 was a year of significant geopolitical events, including, among others, trade tensions resulting from U.S. tariff implementation and retaliatory tariffs by other countries and ongoing armed conflicts in the Middle East and Ukraine.

37 Table of Contents We regularly are subject to requests for information, inquiries and informal or formal investigations by the SEC and other regulatory authorities, with which we routinely cooperate, and which have included review of historical practices that were previously examined. Such investigations have previously and may in the future result in penalties and other sanctions. SEC actions and initiatives can have an adverse effect on our financial results, including as a result of the imposition of a sanction, a limitation on our or our personnel’s activities, or changing our historic practices. Even if an investigation or proceeding did not result in a sanction, or the sanction imposed against us or our personnel by a regulator were small in monetary amount, the adverse publicity relating to the investigation, proceeding or imposition of these sanctions could harm our reputation and cause us to lose existing clients or fail to gain new clients. In addition, certain states and other regulatory authorities have required investment managers to register as lobbyists, and we have registered as such in a number of jurisdictions. Other states or municipalities may consider similar legislation or adopt regulations or procedures with similar effect. These registration requirements impose significant compliance obligations on registered lobbyists and their employers, which may include annual registration fees, periodic disclosure reports and internal recordkeeping.

In recent years, the U.S. government has taken substantial actions with respect to international trade policy, including seeking to renegotiate certain existing bilateral or multi-lateral trade agreements and treaties with foreign countries. The U.S. government has also imposed, and may in the future impose further, tariffs on certain foreign goods, such as steel and aluminum, from various countries, including China, Canada and Mexico. Some foreign governments, including China, Canada, and Mexico, have threatened or instituted retaliatory tariffs on certain U.S. goods. In February 2026, the U.S. Supreme Court ruled that many of the tariffs recently imposed by the U.S. government exceeded its authority, thereby invalidating many, but not all, of such tariffs. Subsequent to the U.S. Supreme Court’s ruling, the U.S. Presidential administration raised potential alternative means through which the administration could impose tariffs and subsequently imposed a global tariff under a different law. The outlook on further trade policy actions, including trade agreements and potential retaliatory tariffs is unclear. Increased tariffs on goods imported from China, Canada, Mexico and other countries could further increase, costs, decrease margins and reduce the competitiveness of products and services offered by our portfolio companies. This has and could further adversely impact the revenues and profitability of select companies that have substantial sales of physical goods in the U.S.…

The U.S. has also implemented a number of economic sanctions programs and export controls that specifically target Chinese entities and nationals on national security grounds, including, for example, with respect to China’s response to political demonstrations in Hong Kong and China’s conduct concerning the treatment of Uyghurs and other ethnic minorities in its Xinjiang province. Moreover, the U.S. has implemented additional sanctions against entities participating in China’s military industrial complex and providing support to the country’s military, intelligence, and surveillance apparatuses. These sanctions impose certain restrictions on U.S. persons and entities buying or selling publicly traded securities of these designated entities. Further escalation of the “trade war” between the U.S. and China, the countries’ inability to reach further trade agreements, or the continued use of reciprocal sanctions by each country, may negatively impact opportunities for investment as well as the rate of global growth, particularly in China, which has and continues to exhibit signs of slowing growth. Such slowing growth could adversely affect the revenues and profitability of our funds’ portfolio companies.

Furthermore, we may also be adversely affected if there is misconduct by personnel of our funds’ portfolio companies or by such companies’ service providers. For example, financial fraud or other deceptive practices at our funds’ portfolio companies, or failures by personnel at our funds’ portfolio companies to comply with anti-corruption, anti-bribery, anti-fraud, anti-money laundering, trade and economic sanctions, export controls, anti-harassment, 48 Table of Contents anti-discrimination or other legal and regulatory requirements, could subject us to, among other things, civil and criminal penalties or material fines, profit disgorgement, injunctions on future conduct and securities litigation, and could also cause significant reputational and business harm to us. Such misconduct may undermine our due diligence efforts with respect to such portfolio companies and could negatively affect the valuations of the investments by our funds in such portfolio companies. Losses to our funds and us could also result from misconduct or other actions by service providers, such as administrators, consultants or other advisors, if such service providers improperly use or disclose confidential information, misappropriate funds, or violate legal or regulatory obligations. Moreover, we may face an increased risk of such misconduct to the extent our funds’ investment in non-U.S.

The Iran Threat Reduction and Syria Human Rights Act of 2012 (“ITRA”) requires companies subject to SEC reporting obligations under Section 13 of the Exchange Act to disclose in their periodic reports specified dealings or transactions involving Iran or other individuals and entities targeted by certain OFAC sanctions, including, by way of example, the Russian Federal Security Service, engaged in by the reporting company or any of its affiliates during the period covered by the relevant periodic report. In some cases, ITRA requires companies to disclose these types of transactions even if they were permissible under U.S. law, including companies that are or may be at the time considered our affiliates. We do not independently verify or participate in the preparation of these disclosures. We have been in the past and may be in the future be required to separately file with the SEC a notice when such activities have been disclosed in our periodic reports, and the SEC is required to post such notice of disclosure on its website and send the report to the President and certain U.S. Congressional committees. The President thereafter is required to initiate an investigation and, within 180 days of initiating such an investigation, determine whether sanctions should be imposed.…

In addition, investments in companies that are based outside of the United States may be negatively impacted by restrictions on international trade or the imposition of tariffs (and any resulting reciprocal tariffs), which have been an area of focus for the current U.S. Presidential administration. See “—Trade negotiations and related government actions may create regulatory uncertainty for our funds’ portfolio companies and our investment strategies and adversely affect the profitability of our funds’ portfolio companies.”
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BX_20261024/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
