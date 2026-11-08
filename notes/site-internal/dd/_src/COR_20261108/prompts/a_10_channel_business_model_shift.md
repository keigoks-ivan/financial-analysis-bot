你是 stock-analyst v20 DD 的證據採集子 agent。標的：COR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Cencora distribution channel disruption OR shift 2026
  - COR Cencora business model transition subscription OR platform 2026
  - Medical Distribution channel disintermediation D2C 2026
  - Cencora go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm｜as_of：2025-11-25
<<<
1 Table of Contents The Company We serve our customers (healthcare providers and pharmaceutical and biotech manufacturers) through a geographically diverse network of distribution service centers and other operations in the United States and select global markets. In our pharmaceutical distribution businesses, we are typically the primary supplier of pharmaceutical and related products to our healthcare provider customers. We offer a broad range of services to our customers designed to enhance the efficiency and effectiveness of their operations, which allow them to improve the delivery of healthcare to patients and to lower overall costs in the pharmaceutical supply chain.

Strategy Our business strategy is focused on the global pharmaceutical supply chain where we provide distribution and value-added services to healthcare providers (primarily pharmacies, health systems, medical and dialysis clinics, physicians, and veterinarians) and pharmaceutical manufacturers to improve channel efficiencies and support positive patient outcomes. Our strategy is one of driving executional excellence in our core distribution solutions business in the U.S. and internationally, while also investing in higher-margin, high-growth adjacencies where we provide solutions to pharmaceutical manufacturers to support the clinical development and commercialization of their therapies and support providers in driving efficiency and effectiveness of their operations. Implementing this disciplined and focused strategy in a seamless and unified way has allowed us to significantly expand our business. We are well positioned to grow revenue and increase operating income through the execution of the following key elements of our business strategy: •Optimize and Grow U.S. Healthcare Solutions Businesses. We are well positioned in size and market breadth to continue to grow our U.S. Healthcare Solutions businesses as we make investments to improve our operating and capital efficiencies. Our U.S.…

We believe we have one of the lowest operating cost structures among pharmaceutical distributors. Our robust distribution facility network includes a national distribution center in Columbus, Ohio, which offers pharmaceutical manufacturers a single shipping destination. We continue to seek opportunities to achieve increased productivity and drive operating income gains as we invest in and continue to implement warehouse automation technology, adopt “best practices” in warehousing activities, and increase operating leverage by increasing volume per full-service distribution facility. We continue to seek opportunities to expand our offerings in our human health distribution businesses.

U.S. Healthcare Solutions Segment The U.S. Healthcare Solutions reportable segment distributes a comprehensive offering of brand-name, specialty brand-name and generic pharmaceuticals, over-the-counter healthcare products, home healthcare supplies and equipment, and related services to a wide variety of healthcare providers, including acute care hospitals and health systems, independent and chain retail pharmacies, mail order pharmacies, medical clinics, long-term care and alternate site pharmacies, and other customers. The U.S. Healthcare Solutions reportable segment also provides pharmaceutical distribution (including plasma and other blood products, injectable pharmaceuticals, vaccines, and other specialty pharmaceutical products) and additional services to physicians who specialize in a variety of disease states, especially oncology and retina, and to other healthcare providers, including hospitals, retinal practices, and dialysis clinics. The U.S. Healthcare Solutions reportable segment also provides pharmacy management, staffing and additional consulting services, and supply management software to a variety of retail and 3 Table of Contents institutional healthcare providers. Additionally, it delivers packaging solutions to institutional and retail healthcare providers. Through its animal health business, the U.S. Healthcare Solutions reportable segment sells pharmaceuticals, vaccines, parasiticides, diagnostics, micro feed ingredients, and various other products to customers in both the companion animal and production animal markets. It also offers demand-creating sales force services to manufacturers.

Customers We have a diverse customer base that includes institutional and retail healthcare providers as well as pharmaceutical manufacturers. Institutional healthcare providers include acute care hospitals, health systems, mail order pharmacies, long-term care and other alternate care pharmacies, providers of pharmacy services to such facilities, physicians, and physician group practices. Retail healthcare providers include national and regional retail drugstore chains, independent community pharmacies, pharmacy departments of supermarkets and mass merchandisers, and veterinarians. We are typically the primary source of supply for our healthcare provider customers. Our manufacturer customers include branded, generic, and biotechnology manufacturers of prescription pharmaceuticals, as well as over-the-counter product and health and beauty aid manufacturers. In addition, we offer a broad range of value-added solutions designed to enhance the operating efficiencies and competitive positions of our customers, thereby allowing them to improve the delivery of healthcare to patients and consumers.

Competition We operate in a highly competitive global environment in the distribution of pharmaceuticals and related healthcare services. Our largest competitors are McKesson Corporation (“McKesson”), Cardinal Health, Inc. (“Cardinal”), and UPS Logistics, among others. Our U.S. human health distribution businesses compete with both McKesson and Cardinal, as well as national generic distributors and regional distributors within pharmaceutical distribution. In addition, we compete with manufacturers who sell directly to customers, chain drugstores who manage their own warehousing, specialty distributors, and packaging and healthcare technology companies. Alliance Healthcare, MWI Animal Health, World Courier, and our consulting businesses also face competition from a variety of entities. In all areas, competitive factors include price, product offerings, value-added service programs, service and delivery, credit terms, and customer support.

The U.S. Drug Enforcement Administration (“DEA”), the U.S. Food and Drug Administration (“FDA”), the U.S. Department of Justice, and various other federal and state authorities regulate the purchase, storage, and/or distribution of pharmaceutical products, including controlled substances. Wholesale distributors of controlled substances must hold valid DEA licenses, meet various security and operating standards, and comply with regulations governing the sale, marketing, packaging, holding, and distribution of controlled substances.

In recent years, some states have passed or proposed laws and regulations that are intended to protect the safety of the pharmaceutical supply chain. These laws and regulations are designed to prevent the introduction of counterfeit, diverted, adulterated, or mislabeled pharmaceuticals into the distribution system. At the federal level, the supply chain security legislation known as the Drug Quality and Security Act (“DQSA”) became law in 2013. Title II of the DQSA, known as the Drug Supply Chain Security Act (“DSCSA”), establishes federal traceability standards requiring drugs to be labeled and tracked at the lot level, preempts state drug pedigree requirements, and requires all supply-chain stakeholders to participate in an electronic, interoperable prescription drug traceability system. The DSCSA also establishes requirements for drug wholesale distributors and third-party logistics providers, including licensing requirements applicable in states that had not previously licensed third-party logistics providers. The FDA issued a proposed rule on February 4, 2022, which, when finalized, will establish national standards for the licensure of wholesale drug distributors and third-party logistics providers. The standards, terms, and conditions established for licensure under this regulation would be applicable to both federal and state licenses.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-25）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm｜as_of：2025-11-25
<<<
U.S. Healthcare Solutions Segment The U.S. Healthcare Solutions reportable segment distributes a comprehensive offering of brand-name, specialty brand-name and generic pharmaceuticals, over-the-counter healthcare products, home healthcare supplies and equipment, and related services to a wide variety of healthcare providers, including acute care hospitals and health systems, independent and chain retail pharmacies, mail order pharmacies, medical clinics, long-term care and alternate site pharmacies, and other customers. The U.S. Healthcare Solutions reportable segment also provides pharmaceutical distribution (including plasma and other blood products, injectable pharmaceuticals, vaccines, and other specialty pharmaceutical products) and additional services to physicians who specialize in a variety of disease states, especially oncology and retina, and to other healthcare providers, including hospitals, specialty retinal practices, and dialysis clinics. The U.S. Healthcare Solutions reportable segment also provides pharmacy management, staffing and additional patient access and adherence support services, and supply management software to a variety of retail and institutional healthcare providers. Additionally, it delivers packaging solutions to institutional and retail healthcare providers. Through its animal health business, the U.S. Healthcare Solutions reportable segment sells pharmaceuticals, vaccines, parasiticides, diagnostics, micro feed ingredients, and various other products to customers in both the companion animal and production animal markets. It also offers demand-creating sales force services to manufacturers.

Operating Expenses Fiscal Year Ended September 30, (dollars in thousands) 2025 2024 Change Distribution, selling, and administrative $ 6,493,842 $ 5,661,106 14.7% Depreciation and amortization 1,051,075 1,091,974 (3.7)% Litigation and opioid-related expenses, net 60,671 227,070 Acquisition-related deal and integration expenses 291,044 103,001 Restructuring and other expenses 229,422 233,629 Goodwill impairment 723,884 418,000 Total operating expenses $ 8,849,938 $ 7,734,780 14.4% Distribution, selling, and administrative expenses increased by $832.7 million, or 14.7%, from the prior fiscal year primarily due to the January 2025 acquisition of RCA and to support our revenue growth. As a percentage of revenue, distribution, selling, and administrative expenses were 2.02% in the current fiscal year and represent an increase of 9 basis points compared to the prior fiscal year primarily due to the January 2025 acquisition of RCA, offset in part by our improved operating leverage from our 9.3% revenue growth from the prior fiscal year.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
