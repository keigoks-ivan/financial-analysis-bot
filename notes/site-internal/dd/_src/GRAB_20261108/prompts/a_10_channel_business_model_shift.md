你是 stock-analyst v20 DD 的證據採集子 agent。標的：GRAB。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Grab Holdings distribution channel disruption OR shift 2026
  - GRAB Grab Holdings business model transition subscription OR platform 2026
  - Software - Application channel disintermediation D2C 2026
  - Grab Holdings go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-06）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1855612/000185561226000020/ck0001855612-20251231.htm｜as_of：2026-03-06
<<<
•In Indonesia, our GrabKios offering enables a network of GrabKios agents to act as an offline channel to sell digital goods including mobile airtime credits, bill payment services and e-commerce purchasing services.

Regulations on Our Online Platform The E-Commerce Regulations (Government Regulation No. 80 of 2019 and Minister of Trade Regulation No. 31 of 2023) require any business actor that provides Electronic Communication facilities for trading transactions, such as an online platform or marketplace, to obtain an E-Commerce Trade Business License (SIUPMSE). Since our platform acts as an electronic communication medium supporting e-commerce transactions, we must obtain and maintain this license to operate legally. Specifically, these regulations mandate that we, as the platform operator, ensure certain consumer protection information, such as the contact details of the Directorate-General of Consumer Protection and Trade Order, is easily accessible to consumers on the app interface. As of the date of this annual report, we have obtained an effective SIUPMSE for our Indonesia platform entity. Further, a Drug and Food Authority regulation effective July 2024 governs the online distribution of over-the-counter medicine and prescription drugs. We are in the process of obtaining the required license to facilitate sales of medicines via our platform.

Insurance Products The implementation and marketing of insurance products through bank and non-bank business entities utilizing an electronic system (such as an online platform) requires prior approval from the OJK. In this context, “marketing” means that the entire insurance process (from product selection, risk assessment, premium/contribution payment, to policy issuance) is done through electronic systems without any face-to-face interactions. In addition, an entity marketing insurance products via an electronic system, whether an insurance company conducting direct marketing or a marketing channel entity (such as an insurance agent, a bank or a non-bank entity), must hold an Electronic System Provider Certificate (“TDPSE”) issued by the MOCD. These regulations ensure that all electronic distribution activities adhere to OJK and MOCD's technology risk management standards and are subject to regulatory oversight over their electronic system administration.

Malaysia Regulations on Our Online Platform The Consumer Protection (Electronic Trade Transaction) Regulations 2024 apply to our operation as an online marketplace where goods and services are traded or advertised. These Regulations impose obligations on us, as the online marketplace operator, to protect consumer interests. Our key compliance obligations include ensuring that required goods and services information provided by suppliers is displayed on the online marketplace, maintaining proper transaction records, and establishing adequate grievance-handling procedures for consumers using our platform.

The PSA Amendment, which became effective in 2022, provides an exclusive enumeration of what constitutes a “public utility.” Only those specifically classified as a public utility (e.g., electricity distribution and transmission, water pipeline distribution systems, seaports, and certain public utility vehicles) are subject to the 60% foreign ownership restriction. Public services not classified as a public utility (such as transport vehicles accredited with and operating through technology-based application companies (“TNCs”) are generally open to full foreign ownership. However, other public services may later on be classified as public utilities by congressional act.

Regulations on Our Online Platform The first applicable regulation is the Direct Sales and Direct Marketing Act, B.E. 2545 (2002), as amended. This Act regulates business operators who offer goods or services to consumers at a distance with the anticipation that the consumer will respond and purchase those goods or services, which can include online platforms. Such business operators could be viewed as a "direct marketing business," requiring a Direct Marketing Certificate from the Office of the Consumer Protection Board. While the competent authority historically interpreted this as applying only to tangible goods sold through online channels, recent changes in interpretation permit the registration of intangible services, such as the Grab platform services. We have obtained this certificate for our GrabGift e-voucher offerings and have also obtained a Direct Marketing Certificate for the Grab platform services.

Regulations on Deliveries Business Our GrabFood, GrabMart, GrabGifts, and Dine Out offerings are subject to e-commerce regulations, including Decree No. 52/2013/ND-CP and Circular 59/2015/TT-BCT (as amended), which require us to register or notify our mobile application with the Ministry of Industry and Trade (MOIT) to avoid administrative fines. The Law on E-Commerce 2026 (“2026 E-Commerce Law”), effective July 1, 2026, introduces stricter obligations for e-commerce platform operators, potentially classifying Grab as a direct, intermediary, and/or integrated platform. Key obligations include publicly disclosing compliance documents and product information, pre-screening seller content for illegal or counterfeit goods, assuming joint liability for buyer damages, and maintaining data storage for at least three years. Existing registrations remain valid until June 30, 2027, by which time Grab must secure re-notification or re-registration under forthcoming implementing regulations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
