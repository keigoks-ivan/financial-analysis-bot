你是 stock-analyst v20 DD 的證據採集子 agent。標的：GLXY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - GLXY Galaxy Digital tariff section 232 2026
  - Galaxy Digital export control OR entity list Capital Markets 2026
  - GLXY Galaxy Digital China tariff OR trade restriction 2026
  - Capital Markets tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
Our investment adviser is subject to, among other things, the anti-fraud provisions of the Advisers Act and fiduciary duties derived from these provisions, which apply to our relationships with our investment banking clients. These provisions and duties impose restrictions and obligations on us with respect to our dealings with our clients and the investments we manage, including for example disclosure of conflicts of interest. Our investment adviser has in the past and will in the future be subject to periodic SEC examinations. Our investment adviser is also subject to other requirements under the Advisers Act and related regulations primarily intended to protect investment banking clients. These additional requirements include maintaining effective and comprehensive compliance programs and written policies and procedures, record-keeping, reporting and disclosure, advertising and solicitation rules, safeguards for protecting client funds and securities, limitations on agency cross and principal transactions between an adviser and its advisory clients, restrictions on advisory contract assignments, privacy protection regulations, and anti-corruption rules relating to investors associated with U.S. state or local governments. The Advisers Act generally grants the SEC broad administrative powers, including the power to limit or restrict an investment adviser from conducting advisory activities in the event it fails to comply with 13 Table of Content federal securities laws.…

Economic Sanctions We must comply with economic and trade sanctions administered by the United States and other foreign governments in jurisdictions in which we operate. These sanctions can prohibit or restrict transactions to or from certain countries, regions, governments, and specified individuals. For instance, the Office of Foreign Assets Control includes cryptocurrency addresses to the list of Specially Designated Nationals whose assets are blocked and with whom U.S. person are generally prohibited from transacting.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
We do not have experience in developing and offering AI/HPC data center infrastructure. We may experience difficulties and/or construction delays related to the infrastructure development and modification of AI/HPC campuses, including the Helios campus, due to factors beyond our control. For example, there may be difficulties related to, or construction delays caused by: integrating new equipment into our existing infrastructure; constraints on our ability to connect to or procure the expected electricity supply capacity at the campus, including delays in utility interconnection, transformer production, substation equipment availability or required utility upgrades; supply chain or construction disruption (including as a result of labor shortages, wage inflation, labor disputes, strikes or work stoppages, severe weather, tariffs or otherwise); failure of contractors or subcontractors to perform on a timely basis or at all, or other misconduct on the part of contractors or subcontractors; defects in design, construction or installed equipment; inability to procure the necessary equipment, including specialized and long-lead items such as generators, transformers, switchgear, 24 Table of Content cooling systems, substations and related electrical infrastructure, on commercially acceptable terms or at all; diversion of management resources; insufficient funding or other resource constraints; or actual costs for development exceeding our planned budget.

Governments have limited or may limit the shipment of products in and out of their jurisdictions or impose tariffs on products, which could negatively impact our ability to receive AI/HPC data center equipment from our suppliers. Our third-party manufacturers, suppliers, sub-contractors and customers have been and will continue to be disrupted by worker absenteeism, quarantines, restrictions on employees’ ability to work, office and factory closures, severe weather, disruptions to ports and other shipping infrastructure, border closures, or other travel or health-related restrictions. Depending on the magnitude of such effects on our supply chain, shipments of parts for our existing bitcoin mining and AI/HPC data center equipment, as well as any new bitcoin mining and AI/HPC data center equipment we purchase, may be delayed. As our AI/HPC data center equipment requires repair or becomes obsolete and requires replacement, our ability to obtain adequate replacements or repair parts from the third-party manufacturers may therefore be hampered. Supply chain disruptions could therefore negatively impact our operations.

Furthermore, our KYC and onboarding processes are designed to verify the identity of our customers, manage associated risks and prevent offers and sales of some digital assets and other products and services to certain persons. While we have implemented tailored AML and KYC protocols within each of our business lines, due to the nature of the digital assets industry and technology, including the pseudonymous nature of blockchain transactions, we may inadvertently or without our knowledge engage in transactions with persons named on OFAC’s Specially Designated Nationals list or other blocked or sanctioned persons in connection with our interactions with a blockchain. Further, fraudulent and illegal transactions and prohibited status could be difficult or impossible for us and our partners, suppliers and vendors to detect in some circumstances. Therefore, there can be no assurance that our AML and KYC protocols will be sufficient to prevent or detect all inappropriate practices, fraud or violations of such laws, regulations and requirements by the Company’s affiliates, employees, directors, officers, partners, agents and service providers, in connection with our operations.…

As digital assets have grown in both popularity and market size, the U.S. Congress and a number of U.S. federal and state agencies and self-regulatory organizations (including FinCEN, OFAC, SEC, CFTC, FINRA, NFA, the Consumer Financial Protection Bureau, the Department of Justice, the Department of Homeland Security, the Federal Bureau of Investigation, the IRS, the Office of the Comptroller of the Currency, the FDIC, the Federal Reserve and state financial institution and securities regulators) have been examining the operations of digital asset networks, digital asset users and the digital asset markets, with particular focus on the extent to which digital assets can be misused to launder the proceeds of illegal activities, evade sanctions, or fund criminal or terrorist enterprises, and generally the safety and soundness of digital asset trading platforms and other service providers that hold digital assets for users. Many of these regulatory bodies have issued consumer advisories regarding the risks posed by digital assets to investors. Ongoing and future regulatory actions with respect to digital assets generally or any digital asset that we hold or invest in may alter, perhaps to a materially adverse extent, the nature of an investment in us or our ability to continue to operate.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/parts/axes_4.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
