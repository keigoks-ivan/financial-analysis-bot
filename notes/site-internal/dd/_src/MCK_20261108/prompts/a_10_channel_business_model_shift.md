你是 stock-analyst v20 DD 的證據採集子 agent。標的：MCK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - McKesson distribution channel disruption OR shift 2026
  - MCK McKesson business model transition subscription OR platform 2026
  - Pharmaceutical Distribution + Specialty Solutions channel disintermediation D2C 2026
  - McKesson go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
Our Oncology & Multispecialty segment includes provider solutions that encompass specialty drug distribution, group purchasing organizations, infusion services, direct to patient pharmacy capabilities, InspiroGene™ cell and gene therapy services, technology solutions, practice consulting services, and vaccine distribution. In addition, the segment supports the U.S. Oncology Network, one of the largest networks of physician-led, integrated, community-based oncology practices dedicated to advancing high-quality, evidence-based cancer care in the U.S. The segment also includes PRISM Vision Holdings, LLC (“PRISM Vision”); which drives patient outcomes in a retina and ophthalmology setting. Combined with Sarah Cannon Research Institute (“SCRI”) and our technology business, Ontada, this segment provides research, insights, technologies, and services that address and improve cancer and specialty care. This segment was previously reflected in the former U.S. Pharmaceutical reportable segment.

Our Medical-Surgical Solutions segment is a leading provider of medical-surgical supplies, laboratory equipment, and pharmaceutical distribution, logistics, and other services to non-acute settings in the U.S. These include healthcare providers operating in ambulatory care environments, such as physician offices, surgery centers, and hospital reference labs, as well as extended care settings, including nursing homes, hospice and home health care agencies, government markets, and online marketplaces and retailers. This segment offers more than 270,000 national brand medical-surgical products as well as its own line of more than 4,000 high-quality products through a network of distribution centers in the U.S. During fiscal 2026, we announced our intention to separate this segment into an independent company. As a part of the separation strategy, on April 20, 2026, we announced a definitive agreement under which funds managed by affiliates of Apollo Global Management, Inc. (“Apollo Funds”) will acquire approximately 13% minority ownership interest in our Medical‑Surgical Solutions segment through an investment of approximately $1.25 billion in the segment’s convertible preferred equity. This transaction is subject to regulatory approvals and customary closing conditions.

Our former Norwegian operations, which provided distribution and services to wholesale and retail customers in Norway where we owned, partnered, or franchised with retail pharmacies, were included in Other. During fiscal 2026, we completed the sale of our businesses in Norway. Refer to Financial Note 2, “Business Acquisitions and Divestitures,” to the consolidated financial statements included in this Annual Report for more information.

Item 1 Index McKESSON CORPORATION U.S. Pharmaceutical Our U.S. Pharmaceutical business operates and serves customers through a network of 27 distribution centers in the U.S., including two strategic redistribution centers. We invest in technology and other systems at all of our distribution centers to enhance safety, reliability, and product availability. For example, we offer McKesson ConnectSM, an internet-based ordering system that provides item look-up and real-time inventory availability as well as ordering, purchasing, third-party reconciliation, and account management functionality. We make extensive use of technology as an enabler to ensure customers have the right products at the right time in the right place.

Within U.S. Pharmaceutical, we have three primary pharmaceutical distribution customer channels: (i) retail national accounts, which include national and regional retail chains, food and drug combinations, mail order pharmacies, and mass merchandisers, (ii) community pharmacy and health, and (iii) institutional healthcare providers such as hospitals, health systems, integrated delivery networks, and long-term care providers.

•Strategic Redistribution Centers – Two facilities totaling over 740,000 square feet that offer access to inventory for single source warehouse purchasing, including pharmaceuticals and biologics. These distribution centers also provide the foundation for a two-tiered distribution network that supports best-in-class direct store delivery.

•McKesson Plasma and Biologics – Specialty and plasma drug distributor that leads in market exclusive drug access; partner to health systems customers in navigating the complexities of limited distribution drug; and optimization of McKesson Distribution benefits.

McKesson Canada Our Canadian pharmaceutical business is one of the largest pharmaceutical wholesale and retail distributors in Canada. The wholesale business delivers products to retail pharmacies, hospitals, long-term care centers, clinics, and institutions in Canada through a national network of distribution centers and provides logistics and distribution services for manufacturers.

Oncology & Multispecialty: The Oncology & Multispecialty segment provides a range of solutions to oncology and other specialty practices and offers community physician specialists (oncologists, rheumatologists, ophthalmologists, urologists, neurologists, and other specialists) an extensive set of customizable solutions and services designed to strengthen core practice operations, enhance value-based care delivery, and expand their service offering to patients. Community-based physicians supported by this business have broad flexibility and discretion to select the products and commitment levels that best meet their practice needs. Services in provider solutions include specialty drug distribution, group purchasing organizations (“GPOs”) like Onmark®, technology solutions, practice consulting services, and vaccine distribution.

Medical-Surgical Solutions Segment: Our Medical-Surgical Solutions segment is a leading provider of medical-surgical supplies, laboratory equipment, and pharmaceutical distribution, logistics, biomedical maintenance, and other services to U.S. healthcare providers across the non-acute and alternate-site spectrum. Our more than 336,000 customers include physician offices, surgery centers, post-acute care facilities, hospital reference labs, and home health agencies. We partner with manufacturers and channel partners to support our key markets, including ambulatory care, extended care, government, and other online marketplaces, and retailers. We distribute medical-surgical supplies (such as gloves, needles, syringes, and wound care products), infusion pumps, laboratory equipment and supplies, and pharmaceuticals. Through a network of distribution centers in the U.S., we offer more than 270,000 products from national brand manufacturers and our own brand of more than 4,000 high-quality products. Through the right mix of products and services, we help improve efficiencies, profitability, and compliance. Our focus is to help customers improve patient and business outcomes. We develop customized plans to address the product, operational, and clinical support needs of our customers, including inventory management, reducing administrative burdens, and training and educating clinical staff. We deliver for our customers, so they can deliver and care for their patients. During fiscal 2026, we announced our intention to separate this segment into an independent company.…

Competition We operate in highly competitive markets across North America, and the healthcare industry has experienced significant consolidation in recent years. Within the pharmaceutical distribution landscape in which our North American Pharmaceutical segment operates, we face strong competition from international, national, regional, and local full-line, short-line, and specialty distributors; service merchandisers; self-warehousing chain drugstores; manufacturers engaged in direct distribution; third-party logistics companies; and large payer organizations. Our primary competitors in distribution, wholesaling, and logistics are Cencora, Inc. and Cardinal Health, Inc.

Federal and state laws regulate the pharmaceutical drug supply chain in order to prevent the distribution of counterfeit, stolen, contaminated, or otherwise harmful prescription drugs in interstate commerce. At the federal level, the Drug Supply Chain Security Act (“DSCSA”), among other things, requires standardized, unit-level traceability of pharmaceutical products along the entire drug supply chain and requires all trading partners to cooperate in an electronic, interoperable prescription drug traceability system. The DSCSA also sets forth national standards for the licensure of wholesale drug distributors and third-party logistic providers and other requirements applicable to these entities and the FDA has issued a proposed rule with respect to these requirements. These federal and state regulatory requirements have increased, and may further increase, our compliance burden and distribution costs.

Available Information We routinely post on our company website, and via our social media channels, information that may be material to investors, including details and updates to information disclosed elsewhere, which may include business developments, earnings and financial performance, sustainability matters, details regarding upcoming events, and materials for presentations to investors and financial analysts. Investors are encouraged to monitor our website, www.mckesson.com. Interested parties can sign up on our website, including our Investor Relations site, to receive automated e-mail alerts, such as via RSS newsfeed, when we post certain information. Interested parties can also follow our social media feed @McKesson on X. The content on any website or social media channel is not incorporated by reference into this report, unless expressly noted otherwise.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
•Medical-Surgical Solutions segment provides medical-surgical, laboratory, and pharmaceutical distribution, logistics, and other services to U.S. healthcare providers operating in the non-acute settings. These include ambulatory care environments, such as physician offices, surgery centers, and hospital reference labs, as well as extended care settings, including nursing homes, hospice and home health care agencies, government facilities, and online marketplaces and retailers. This segment offers national brand medical-surgical products as well as our own line of more than 4,000 high-quality products through a network of distribution centers within the U.S. During fiscal 2026, we announced our intention to separate this segment into an independent company. As a part of the separation strategy, on April 20, 2026, we announced a definitive agreement under which funds managed by affiliates of Apollo Global Management, Inc. (“Apollo Funds”) will acquire approximately 13% minority ownership interest in our Medical‑Surgical Solutions segment through an investment of approximately $1.25 billion in the segment’s convertible preferred equity. The transaction is subject to regulatory approvals and customary closing conditions.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
