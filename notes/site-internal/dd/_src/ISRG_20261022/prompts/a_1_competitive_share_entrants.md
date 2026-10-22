你是 stock-analyst v20 DD 的證據採集子 agent。標的：ISRG。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - ISRG Intuitive Surgical market share gaining OR losing 2026
  - Intuitive Surgical new entrant OR displace threat Medical Instruments & Supplies 2026
  - ISRG competitor design win 2026
  - Intuitive Surgical vs Medical Instruments & Supplies peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm｜as_of：2026-02-03
<<<
Competition We face competition in the forms of existing open surgery, conventional MIS (laparoscopy), drug therapies, radiation treatment, and other emerging diagnostic and interventional surgical approaches. Some of these procedures are widely accepted in the medical community and, in many cases, have a long history of use. Our success depends on continued clinical and technical innovation, quality, and reliability, as well as educating hospitals, surgeons, and patients on the demonstrated results associated with robotic-assisted medical procedures using da Vinci surgical systems or Ion endoluminal systems and their value 14 Table of Contents relative to other techniques. We also face competition from several companies that have introduced or are developing new approaches and MIS products. We believe that the entrance or emergence of competition validates MIS and robotic-assisted surgery or robotic-assisted bronchoscopy.

Moreover, as we add new robotically controlled products (e.g., da Vinci stapling and da Vinci energy products) that compete with product offerings traditionally within the domains of open surgery and/or conventional MIS, we face greater competition from larger and well-established companies, such as Johnson & Johnson and Medtronic plc.

Additionally, we currently face, or anticipate facing, competition from companies with products used in open or MIS surgeries, including laparoscopy and alternative multi-port, single-port, or endoluminal systems. We also compete with companies providing other therapeutic approaches for addressing target clinical conditions, as well as companies developing diagnostic solutions that could serve as alternatives to current or planned Intuitive offerings. Companies that have introduced products in the field of robotic-assisted medical procedures, or have made explicit statements about their efforts to enter the field, include, but are not limited to, the following: Beijing Surgerii Robotics Company Limited; CMR Surgical Ltd.; Distalmotion SA; Harbin Sizhe Rui Intelligent Medical Equipment Co., Ltd.; Johnson & Johnson; Karl Storz SE & Co. KG; Medicaroid Corporation; Medtronic plc; meerecompany Inc.; Noah Medical Corporation; Shandong Weigao Group Medical Polymer Company Ltd.; Shanghai Microport Medbot (Group) Co., Ltd.; Shenzhen Edge Medical Co., Ltd.; and SS Innovations International, Inc. Other companies with substantial experience in industrial robotics could potentially expand into the field of medical robotics and become competitors. Additionally, we expect increasing competition within China for robotic-assisted systems. Our revenues may be reduced due to pricing pressure if our competitors develop and market products that are more effective or less expensive than our products.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1035267/000103526726000010/isrg-20251231.htm｜as_of：2026-02-03
<<<
Robotic-assisted medical procedures with a da Vinci surgical system or Ion endoluminal system are technologies that compete with established and emerging treatment options in reconstructive medical procedures or disease management. These competitive treatment options include open surgery, conventional MIS (laparoscopy), drug therapies, radiation treatment, and other emerging diagnostic and interventional surgical approaches. Some of these procedures are widely accepted in the medical community and, in many cases, have a long history of use. Technological advances could make such treatment options more effective or less expensive than using our products, which could render our products obsolete or unmarketable. Also, studies could be published that show that other treatment options are more beneficial and/or cost-effective than robotic-assisted medical procedures. We cannot be certain that physicians, or their patients, will choose our products to replace or supplement established treatment options or that our products will continue to be competitive with current or future technologies. For example, in 2023, certain drugs initially approved for use in diabetes patients gained acceptance for use in weight loss treatment following FDA approvals for weight loss indications. The availability and effectiveness of weight loss drugs have reduced the number of bariatric procedures performed, including those bariatric procedures performed using our da Vinci surgical system, as some patients reconsider the surgical treatment option.…

Additionally, we currently face, or anticipate facing, competition from companies with products used in open or MIS surgeries, including laparoscopy and alternative multi-port, single-port, or endoluminal systems. We also compete with companies providing other therapeutic approaches for addressing target clinical conditions, as well as companies developing diagnostic solutions that could serve as alternatives to current or planned Intuitive offerings. Companies that have introduced products in the field of robotic-assisted medical procedures, or have made explicit statements about their efforts to enter the field, include, but are not limited to, the following: Beijing Surgerii Robotics Company Limited; CMR Surgical Ltd.; Distalmotion SA; Harbin Sizhe Rui Intelligent Medical Equipment Co., Ltd.; Johnson & Johnson; Karl Storz SE & Co. KG; Medicaroid Corporation; Medtronic plc; meerecompany Inc.; Noah Medical Corporation; Shandong Weigao Group Medical Polymer Company Ltd.; Shanghai Microport Medbot (Group) Co., Ltd.; Shenzhen Edge Medical Co., Ltd.; and SS Innovations International, Inc. Other companies with substantial experience in industrial robotics could potentially expand into the field of medical robotics and become competitors. Additionally, we expect increasing competition within China for robotic-assisted systems. We may not be able to maintain or improve our commercial position against current or potential competitors.…

28 Table of Contents In China, we have seen increasing competition in the robotic-assisted surgical system industry from domestic companies as well as a sustained broader central government focus on anti-corruption and systematic governance. For example, in July 2023, the Chinese government launched an anti-corruption and systematic governance campaign targeting the healthcare sector. This campaign resulted in heightened scrutiny by medical institutions with respect to initiating tenders, with some tenders being canceled or delayed without a timeline. The extent and impact of this campaign on our business remains uncertain. In 2025, the effects of this campaign, combined with the competitive dynamics in China and various measures related to industrial policy, contributed to fewer systems being placed in China than we anticipated. Currently, the extent and impact of this campaign and the competitive dynamics in China on our business remains uncertain.

We are highly dependent on the principal members of our management and scientific staff. For example, our product development plans depend, in part, on our ability to attract and retain software, mechanical, electrical, manufacturing, and robotics engineers. Attracting and retaining qualified personnel is critical to our success, and competition for qualified personnel is intense. We may not be able to attract and retain personnel on acceptable terms given the constrained labor market and competition for such personnel. Furthermore, as competition intensifies, there is an increased risk that our current or emerging competitors may attempt to hire our key personnel, which could be achieved through offers of substantial financial incentives or strategic opportunities, aiming to capitalize on their knowledge to accelerate their own product development initiatives. In addition, many of our tenured employees are retirement eligible and have significant historical knowledge or expertise that must be transferred to other employees. If we are unable to effectively safeguard our human capital or mitigate the risks associated with knowledge transfer, our business, financial condition, or results of operations could be adversely impacted, and there could be a detrimental effect on our competitive position.

The healthcare industry has been consolidating, and organizations continue to consolidate purchasing decisions for many of our healthcare provider customers. Numerous initiatives and reforms by legislators, regulators, and third-party payers to curb the rising cost of healthcare have catalyzed a consolidation of aggregate purchasing power within the markets in which we sell our products. As the healthcare industry consolidates, competition to provide products and services is expected to continue to intensify, resulting in pricing pressures and decreased average selling prices. In addition, for smaller hospitals or groups that do not consolidate with larger networks, these entities may face increasing cost and/or competitive pressures, which could impact their ability to purchase additional products and services from us or make contractual payments over time. We expect that market demand, government regulation, third-party payor coverage and reimbursement policies, government contracting requirements, new entrants, technology, and societal pressures will continue to change the worldwide healthcare industry, resulting in further consolidation, which may exert further downward pressure on prices of our products and services and may have a material adverse impact on our business, financial condition, or results of operations.

Our operations are subject to certain antitrust and competition laws in the jurisdictions in which we conduct our business, in particular the U.S. and the EU. These laws prohibit, among other things, anticompetitive agreements and practices. If any of our commercial agreements or practices are found to violate or infringe such laws, we may be subject to civil and other penalties. We may also be subject to third-party claims for damages. Further, agreements that infringe upon these antitrust and competition laws may be void and unenforceable, in whole or in part, or require modification in order to be lawful and enforceable. If we are unable to enforce our commercial agreements, whether at all or in material part, our business, financial condition, or results of operations could be adversely affected.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
