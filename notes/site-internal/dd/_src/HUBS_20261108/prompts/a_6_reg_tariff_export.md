你是 stock-analyst v20 DD 的證據採集子 agent。標的：HUBS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - HUBS HubSpot tariff section 232 2026
  - HubSpot export control OR entity list Software - Application 2026
  - HUBS HubSpot China tariff OR trade restriction 2026
  - Software - Application tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm｜as_of：2026-02-11
<<<
A component of our growth strategy involves the further expansion of our operations and customer base internationally. We have formed several international entities and may plan to form additional entities in the future. These international operations focus primarily on sales, professional services and support, and select international locations have development teams. Our current international operations and future initiatives will involve a variety of risks, including: •difficulties in maintaining our company culture with a dispersed and distant workforce; •more stringent regulations relating to data security and the unauthorized use of, or access to, commercial and personal data, particularly in the European Union; •unexpected changes in regulatory requirements, taxes or trade laws, including tariffs or other trade restrictions; •differing labor regulations, especially in the European Union, where labor laws are generally more advantageous to employees as compared to the United States, including deemed hourly wage and overtime regulations in these locations; •challenges inherent in efficiently managing an increased number of employees over large geographic distances, including the need to implement appropriate systems, policies, benefits and compliance programs; •difficulties in managing a business in new markets with diverse cultures, languages, customs, legal systems, alternative dispute systems and regulatory systems; •currency exchange rate fluctuations and the resulting effect on our revenue and expenses, and the cost and risk of entering into hedging transactions; 21 •…

•limited or insufficient intellectual property protection; •perceptions of U.S.-based companies in the regions where we operate or plan to operate; •perceptions of regions or governments in the regions where we operate or plan to operate, resulting in negative publicity or reputational harm; •international disputes, wars, political instability or terrorist activities and resulting economic instability; •likelihood of potential or actual violations of domestic and international anticorruption laws, such as the U.S. Foreign Corrupt Practices Act and the U.K. Bribery Act, or of U.S. and international export control and sanctions regulations, which likelihood may increase with an increase of sales or operations in foreign jurisdictions and operations in certain industries; and •adverse tax burdens and foreign exchange controls that could make it difficult to repatriate earnings and cash.

Our overall performance depends in part on worldwide economic conditions. Global financial developments and downturns seemingly unrelated to us or the software industry may harm us. The United States and other key international economies have been affected from time to time by falling demand for a variety of goods and services, restricted credit, poor liquidity, reduced corporate profitability, volatility in credit, equity and foreign exchange markets, volatility in the banking sector, changes in the labor market, 23 supply chain disruptions, bankruptcies, inflation and overall uncertainty with respect to the economy, including with respect to trade issues, such as trade wars, tariffs or other trade restrictions or the threat of such actions. For example, on October 1, 2025, the U.S. federal government shut down through November 12, 2025, suspending services deemed non-essential as a result of the failure by Congress to enact regular appropriations for the 2026 fiscal year. If we experience another government shutdown , it could result in increased uncertainty and volatility in the global economy and financial markets which could have an adverse effect on our business.…

Further, the economies of countries in Europe have been experiencing weakness associated with high sovereign debt levels, weakness in the banking sector, uncertainty over the future of the Eurozone and volatility in the value of the pound sterling and the Euro and instability resulting from the ongoing conflicts between Russia and Ukraine and in Israel, Gaza, Iran, and in Venezuela. The effects of such conflicts, including any resulting sanctions, export controls or other restrictive actions that may be imposed against governmental or other entities in, for example, Russia, have in the past contributed and may in the future contribute to disruption, instability and volatility in the global markets. We have operations, as well as current and potential new customers, throughout Europe. If economic conditions in Europe and other key markets for our platform continue to remain uncertain or deteriorate further, it could adversely affect our customers’ ability or willingness to subscribe to our platform, delay prospective customers’ purchasing decisions, reduce the value or duration of their subscriptions or affect renewal rates, all of which could harm our operating results.

The landscape of privacy and cybersecurity regulation in the U.S. is increasingly complex. Numerous states have passed comprehensive privacy and data security laws, which impose obligations on covered businesses similar – but not identical – to those under the CCPA, and some states have passed privacy and cybersecurity laws governing specific sectors, technologies, or categories of personal data, such as laws regulating health data, children’s data, and online chatbots. Many of those states have also passed – or proposed to pass – laws and regulations that amend the standard of protection required by such laws. A number of other states have proposed similar privacy legislation, and the U.S. Congress has considered – and may reintroduce – federal privacy and cybersecurity legislation that may or may not preempt some or all of such U.S. state privacy laws, and may provide a private right of action. Through executive and legislative action, the federal government has also taken steps to restrict data transactions involving persons affiliated with China, Russia, Venezuela, and other countries of concern. For example, the Department of Justice January 8, 2025 rule on "Preventing Access to U.S. Sensitive Personal Data and Government-Related Data by Countries of Concern or Covered Persons,” prohibits the sharing of certain sensitive personal data categories to countries of concern.…

35 We are subject to governmental export controls and economic sanctions laws that could impair our ability to compete in international markets and subject us to liability if we are not in full compliance with applicable laws.

Our business activities are subject to various restrictions under U.S. and other global export controls and trade and economic sanctions laws, including the U.S. Commerce Department’s Export Administration Regulations and economic and trade sanctions regulations maintained by the U.S. Treasury Department’s Office of Foreign Assets Control. If we fail to comply with these laws and regulations, we, and certain of our employees, could be subject to civil or criminal penalties and reputational harm. Obtaining the necessary authorizations, including any required license(s), for a particular transaction may be time-consuming, is not guaranteed, and may result in the delay or loss of sales opportunities. Furthermore, export control laws and economic sanctions laws prohibit certain transactions with embargoed or sanctioned countries, governments, persons and entities. These sanctions laws with which we must comply may also change rapidly from time to time as a result of geopolitical events, such as the imposition of sanctions on Russia as a result of the conflict between Russia and Ukraine. Although we take precautions to prevent unlawful transactions and business relationships with sanction targets, the possibility exists that we could inadvertently provide our products and services to persons or entities prohibited by U.S. and other global sanctions regimes.…

•unforeseen costs and expenses related to the expansion of our business, operations and infrastructure, including disruptions in our hosting network infrastructure and privacy and data security; •foreign currency exchange rate fluctuations; •rising inflation in the economies in which we operate and our ability to control costs, including operating expenses; and •general economic and political conditions in our domestic and international markets, including economic sanctions, trade policy changes and restrictions, trade wars, tariffs, or the threat posed by such actions.

General Risks Failure to comply with laws and regulations could harm our business. Our business is subject to regulation by various federal, state, local and foreign governmental agencies, including agencies responsible for monitoring and enforcing employment and labor laws, workplace safety, environmental laws, consumer protection laws, anti-bribery laws, import/export controls, federal securities laws and tax laws and regulations. In certain jurisdictions, these regulatory requirements may be more stringent than those in the United States. Noncompliance with applicable regulations or requirements could subject us to investigations, sanctions, mandatory recalls, enforcement actions, disgorgement of profits, fines, damages, civil and criminal penalties or injunctions.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1404655/000119312526046646/hubs-20251231.htm｜as_of：2026-02-11
<<<
Global Economic Conditions Our results of operations may be significantly influenced by general macroeconomic conditions, including, but not limited to, the impact of pandemics, geo-political conflicts, foreign currency fluctuations, interest rates, inflation, recession risks, tariffs or other trade restrictions, and existing and new domestic and foreign laws and regulations, all of which are beyond our control. Fluctuations in foreign exchange rates and inflation have had, and may continue to have an adverse impact on our financial condition and operating results in future periods. As we continue to monitor the direct and indirect impacts of these circumstances, the broader implications of these macroeconomic events on our business, results of operations and overall financial position, particularly in the long term, remain uncertain. See Part I, Item 1A. "Risk Factors" for further discussion of the impact of these general macroeconomic factors and risks on our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
