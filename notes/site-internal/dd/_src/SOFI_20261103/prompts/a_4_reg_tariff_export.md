你是 stock-analyst v20 DD 的證據採集子 agent。標的：SOFI。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - SOFI SoFi Technologies tariff section 232 2026
  - SoFi Technologies export control OR entity list Credit Services 2026
  - SOFI SoFi Technologies China tariff OR trade restriction 2026
  - Credit Services tariff exposure supply chain 2026


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
Bank Secrecy Act. We have implemented various anti-money laundering policies and procedures to comply with applicable federal anti-money laundering laws, regulations and requirements, such as designating a BSA officer, conducting an annual risk assessment, developing internal controls, independent testing, training, and suspicious activity monitoring and reporting. We apply the customer identification and verification program rules pursuant to the USA PATRIOT Act amendments to the BSA and its implementing regulations and screen certain customer information against the list of specially designated nationals and other lists of sanctioned countries, persons, and entities maintained by the U.S. Treasury Department’s OFAC. Additionally, SoFi Bank is a financial institution under the BSA that is required to implement a risk-based anti-money laundering program, including customer identification procedures, currency transaction reporting, suspicious activity monitoring and reporting and other recordkeeping requirements. Furthermore, the Federal Reserve expects non-bank subsidiaries of bank holding companies to comply with certain BSA reporting requirements. In addition, our contracts with financial institution partners and other third parties may contractually require us to maintain an anti-money laundering program.

Office of Foreign Assets Control. The U.S. has imposed economic sanctions that affect transactions with designated foreign countries, nationals and others. These sanctions, which are administered by OFAC, take many different forms. Generally, however, they contain one or more of the following elements: (i) restrictions on trade with or investment in a sanctioned country, including prohibitions against direct or indirect imports from and exports to a sanctioned country and prohibitions on “U.S. persons” engaging in financial or other transactions relating to a sanctioned country or with certain designated persons and entities; (ii) a blocking of assets in which the government or specially designated nationals of the sanctioned country have an interest, by prohibiting transfers of property subject to U.S. jurisdiction (including property in the possession or control of U.S. persons); and (iii) restrictions on transactions with or involving certain persons or entities. Blocked assets (for example, property and bank deposits) cannot be paid out, withdrawn, set off or transferred in any manner without a license from OFAC. Failure to comply with these sanctions could have serious legal and reputational consequences for the Company.

Our Investment Adviser and our broker-dealer have in the past been, and will in the future be, subject to periodic SEC examinations. Our Investment Adviser and our broker-dealer are also subject to other requirements under the Advisers Act and the Exchange Act, respectively, and related regulations. These additional requirements relate to matters including maintaining effective and comprehensive compliance programs, record-keeping and reporting and disclosure requirements. The Advisers Act and the Exchange Act generally grant the SEC broad administrative powers, including the power to limit or restrict an investment adviser or broker-dealer from conducting advisory or brokerage activities, respectively, in the event they fail to comply with federal securities laws. Additional sanctions that may be imposed for failure to comply with applicable requirements include the prohibition of individuals from associating with an investment adviser or broker-dealer, the revocation of registrations and other censures and fines. Even if an investigation or proceeding did not result in a sanction or the sanction imposed against us or our personnel by a regulator was small in monetary amount, the adverse publicity relating to the investigation, proceeding or imposition of these sanctions could harm our reputation and cause us to lose existing members or fail to gain new members.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-17）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1818874/000181887426000013/sofi-20251231.htm｜as_of：2026-02-17
<<<
Changes or uncertainty with respect to existing laws, regulations and policies, including changes in guidance and interpretation by regulatory authorities, and evolving priorities, including those related to financial regulation, taxation, international trade, fiscal policy, cybersecurity and privacy, digital assets, climate change (including any required reduction of greenhouse gas emissions) and healthcare, may adversely impact U.S. or global economic activity and our members, our technology platform clients, our counterparties and our earnings and operations. For example, changes, or proposed changes, to certain U.S. trade and international investment policies, particularly with important trading partners (including China and the European Union (the “EU”)) have in recent years negatively impacted financial markets. Actions taken by other countries, particularly China, to restrict the activities of businesses, could also negatively affect financial markets. An escalation of tensions, such as a trade war between certain countries or a further escalation in conflict in the Middle East or Eastern Europe or new conflict in Latin America, could lead to further measures that adversely affect financial markets, disrupt world trade and commerce and lead to trade retaliation, including through the use of duties and tariffs, foreign exchange measures or the large-scale sale of U.S. Treasury Bonds.

Additionally, global remittance services are subject to higher operational risks, including delays, transaction errors, and fraudulent activities, particularly in regions with less developed financial infrastructure, including settlement timing differences, and exposure to local liquidity constraints which may impact the predictability and profitability of our global remittance services. Political instability, trade restrictions, current or new tax laws, or economic sanctions imposed on certain countries may further restrict our ability to provide global remittance services in specific markets.

Furthermore, guidance from regulators of the Company and SoFi Bank can subject its non-bank affiliates to increased governance. For example, the OCC’s guidance on retail non-deposit investment products, or RNDIPs, applies to referral arrangements that SoFi Bank may have with an affiliate, including SoFi Securities. This guidance, which was further updated in June 2024 to align with the SEC’s Regulation BI, requires that banks implement and maintain effective oversight and monitoring of relevant RNDIP arrangements to ensure that, among other things, sales transactions and recommendations to retail investors comply with SEC regulations. In addition, our platform as a service activities engaged in through our Technology Platform, are subject to increased regulatory governance by the Federal Reserve, including related to anti-money laundering and sanctions compliance obligations, because Galileo and Technisys are non-bank subsidiaries of a bank holding company. Changes in laws, rules, regulations and supervisory guidance and policies could, among other things, subject us to additional costs, including costs of compliance; limit the types of financial services and products we may offer; and/or increase the ability of non-banks to offer competing financial services and products.…

The Investment Adviser operates in a highly regulated environment and is subject to, among other things, the anti-fraud provisions of the Advisers Act and to fiduciary duties derived from these provisions that apply to its relationships with our members who are its advisory clients. These provisions and duties also impose certain restrictions and obligations on us with respect to our dealings with our members and our investments, including for example restrictions on transactions with our affiliates. Our Investment Adviser is also subject to other requirements under the Advisers Act and related regulations. These additional requirements relate to matters including, among others, maintaining an effective and comprehensive compliance programs and record-keeping and reporting and disclosure requirements. In recent years, the SEC proposed and, in certain cases, adopted amendments to the Advisers Act rules, which present a number of additional significant and burdensome compliance challenges for registered investment advisers. In addition, our Investment Adviser has been in the past, and will be in the future, subject to SEC examination. Moreover, the Advisers Act generally grants the SEC broad administrative powers, including the power to limit or restrict an investment adviser from conducting advisory activities in the event it fails to comply with federal securities laws. The Investment Adviser is also subject to applicable state securities laws.…

From time to time, SoFi Securities and the Investment Adviser may be threatened with or named as a defendant in lawsuits, arbitrations and administrative claims. As previously noted, these entities are also subject to regulatory examinations and inspections by regulators (including the SEC and FINRA, as applicable). Compliance and trading problems or other deficiencies or weaknesses that are reported to regulators, such as the SEC and FINRA, by dissatisfied members or others, or that are identified by regulators themselves are investigated by such regulators, and may, if pursued, result in formal claims being filed against SoFi Securities and the Investment Adviser by members or disciplinary action being taken by regulators against us or our personnel. Our failure to comply with applicable laws or regulations or our own policies and procedures could result in fines, litigation, suspensions of personnel or other sanctions, which could have a material effect on our overall financial results. For example, in December 2023, FINRA found that SoFi Securities failed to establish, maintain, and enforce a supervisory system reasonably designed to supervise its fully paid securities lending offerings.…

We are also subject to economic and trade sanctions programs administered by OFAC, which prohibit or restrict transactions to or from or dealings with specified countries, their governments, and in certain circumstances, their nationals, and with individuals and entities that are specially-designated nationals of those countries, narcotics traffickers, terrorists or terrorist organizations, and other sanctioned persons and entities.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/parts/axes_4.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
