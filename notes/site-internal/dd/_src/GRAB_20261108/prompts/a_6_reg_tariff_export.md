你是 stock-analyst v20 DD 的證據採集子 agent。標的：GRAB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - GRAB Grab Holdings tariff section 232 2026
  - Grab Holdings export control OR entity list Software - Application 2026
  - GRAB Grab Holdings China tariff OR trade restriction 2026
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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 3. Key Information (含 3.D Risk Factors)｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
22 Table of Contents Our business is subject to evolving laws governing payments, banking, insurance and other financial services. We may face challenges in maintaining necessary licenses or adapting to additional regulatory requirements imposed on these services. For example, in Indonesia, PT Indonusa Bara Sejahtera, trading as OVO Finansial, our P2P lending company, is required to cap any funding provided by a single funding provider and its affiliates at 25% of its total funding position at the end of each month. This 25% cap does not apply where the funding provider is a financial institution (e.g., banks, finance companies), in which case a higher cap of 75% applies. Following the enforcement of this requirement, we have taken measures to comply with the funding cap. However, Indonesian regulatory authorities may deem these measures to be insufficient and impose administrative sanctions on OVO Finansial. Regulators in Singapore and Malaysia are monitoring and/or reviewing “buy now, pay later” offerings, which could lead to future curbs. We are subject to regulatory examinations in applicable markets, where regulators could allege violations or view our continued participation in the markets as an overseas company undesirable, and impose sanctions or withdraw our licenses.

Our payment and financial services activities may be governed by complex and evolving laws in various jurisdictions, including those relating to banking, privacy, money transmission, AML, counter-terrorist financing, electronic funds transfers, systemic integrity risk assessments, cybersecurity of payment processes, proliferation financing, import and export restrictions, and consumer protection. These activities may be susceptible to illegal uses, such as money laundering, terrorist financing, fraudulent sales, and payments to sanctioned parties. Furthermore, jurisdictions where we allow cash payments raise additional legal and operational concerns and may increase our compliance risks.

We are subject to economic and trade sanctions relating to Myanmar administered by various governments and international organizations, including the United States, the European Union, the United Kingdom, and the United Nations. In response to the military coup in February 2021, these bodies implemented sanctions and other restrictions targeting specific individuals and entities associated with the military and security services, government officials, and those supporting the military or repressing pro-democracy movements. These measures include prohibitions on transactions, asset freezes, travel bans, and restrictions on the export, re-export, or in-country transfer of sensitive items.

Existing and potential future sanctions, coupled with ongoing geopolitical tensions, could result in a material adverse impact on Myanmar’s economy. While our operations in Myanmar represent less than one percent of our revenue, our future prospects there could be adversely affected, potentially necessitating a market exit involving significant costs and the loss of our investment. Furthermore, despite our internal controls, there remains a risk that we have engaged or could engage in dealings with sanctioned persons. Any non-compliance with these laws or related investigations could result in claims or actions against us, materially and adversely affecting our business, financial condition, results of operations and prospects.

Indonesia Our payment system services business is conducted through PT Bumi Cakrawala Perkasa (“BCP”), an Indonesian entity which owns OVO. OVO is subject to an 85% foreign investment limit (based on ultimate beneficial ownership of shares) pursuant to the Indonesian payment system regulation. Under the prevailing Bank Indonesia regulations, a voting power limitation of 49% applies to foreign shareholders, and foreign shareholders are prohibited from holding (i) the right to nominate the majority of directors and commissioners, and (ii) veto rights with respect to certain strategic decisions that have a significant impact on the company to be adopted at a general meeting of shareholders. We own 82.8% of BCP, which, due to a dual-class structure, represents a 38.9% voting interest, and we also have contractual rights to (a) control the appointment of the Chief Executive Officer, and the Chief Financial Officer (including the right to nominate any such officers as directors or as president director), (b) approve the budget and business plan of BCP and its subsidiaries; (c) approve future funding of BCP and its subsidiaries, whether through debt, equity or otherwise, and (d) certain economic rights with respect to the remaining shareholding of BCP.…

We derive substantially all of our revenue from our operations in Southeast Asia and intend to continue expanding our penetration in the region. Consequently, we are exposed to various risks inherent in the economic, political, and social conditions of the countries in which we operate, including risks related to the following: •inconsistent and evolving regulations, licensing, and legal requirements; •currency devaluations, depreciation, or restrictions on the transfer of funds; •inflation and interest rate hikes that increase our cost of operations; •new or more burdensome regulations, taxes, or tariffs; •political changes affecting the business, legal and regulatory environments; •economic downturns, political instability, civil disturbances, war, military conflict, religious or ethnic strife, terrorism, and general security concerns; •increased enforcement of laws regarding personal data protection, localization, cybersecurity, and ESG, particularly where interpretation or applicability is uncertain; •health epidemics, pandemics, or disease outbreaks; and 41 Table of Contents •natural disasters, such as volcanic eruptions, floods, typhoons, and earthquakes.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
66 Table of Contents MOT Reg. 118/2018 and subsequent regulations mandate that service tariffs (which may be evaluated periodically, at least every six months) must be set within minimum and maximum per-kilometer limits determined by the MOT or the local governor, depending on the operational area. Furthermore, vehicles used must comply with minimum service standards, including a maximum age limit of five years to ensure passenger safety and comfort. Failure to comply with either the tariff rules or vehicle standards can subject the licensee to administrative sanctions, including fines, and temporary suspension or revocation of the license.

For two-wheel ride-hailing, MOT Regulation No. 12 of 2019 stipulates the obligations of, among others, the platform company (the technology application provider). The platform company must implement measures to ensure the physical safety of drivers and passengers, including measures to equip the platform with a panic button for both drivers and passengers. It must also have standard operating procedures in place for drivers that govern how orders are handled and how a driver-partner’s conduct is managed. These required SOPs must explicitly detail the violations that lead to sanctions (including temporary suspension or termination), outline the gradual stages for imposing these sanctions, and specify the steps for both implementing and later revoking any temporary suspensions.

The platform company must also comply with service fee and tariff requirements, as set by the Ministry of Transportation (“MOT”) Decree No. 667 of 2022, as amended, sets mandatory floor and ceiling tariffs and limits the maximum commission a platform company may take from the total tariff to 15%. An additional optional supporting fee of up to 5% may be charged, provided these funds are reinvested into specific components for driver-partner welfare, such as extra insurance and operational assistance.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
