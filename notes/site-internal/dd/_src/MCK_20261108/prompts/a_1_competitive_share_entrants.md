你是 stock-analyst v20 DD 的證據採集子 agent。標的：MCK。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - MCK McKesson market share gaining OR losing 2026
  - McKesson new entrant OR displace threat Pharmaceutical Distribution + Specialty Solutions 2026
  - MCK competitor design win 2026
  - McKesson vs Pharmaceutical Distribution + Specialty Solutions peers market share trend 2025 2026


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
Competition We operate in highly competitive markets across North America, and the healthcare industry has experienced significant consolidation in recent years. Within the pharmaceutical distribution landscape in which our North American Pharmaceutical segment operates, we face strong competition from international, national, regional, and local full-line, short-line, and specialty distributors; service merchandisers; self-warehousing chain drugstores; manufacturers engaged in direct distribution; third-party logistics companies; and large payer organizations. Our primary competitors in distribution, wholesaling, and logistics are Cencora, Inc. and Cardinal Health, Inc.

Item 1 Index McKESSON CORPORATION In our Oncology & Multispecialty segment, we compete with other specialty distributors; GPOs; specialty pharmacies; oncology networks and platforms; ophthalmology and retina management services providers; and healthcare information technology and data and analytics companies. Certain competitors also offer combinations of distribution, GPO, and provider services capabilities, including Cencora, Inc. and Cardinal Health, Inc. In addition, our clinical research offerings compete with contract research organizations, site management organizations, academic medical centers, and health systems that support clinical trials.

Our Prescription Technology Solutions business experiences substantial competition from variety of organizations, including other biopharma services providers, software and technology service firms, consulting firms, shared services vendors, and internet-based companies offering healthcare-focused technology solutions. Competition in this space ranges widely in size, geographic reach, and the scope and depth of products and services offered.

Additionally, we compete with other service providers and healthcare manufacturers, as well as potential customers who may choose to build internal supply management capabilities rather than rely on external partners like us. We believe that our scale and the breadth of our product and service portfolio are key competitive advantages. In all areas, primary competitive factors include price, quality of service, product assortment, innovation, adoption of emerging technologies, and, in some cases, customer convenience.

Competition and Related Laws: Antitrust and competition laws (“competition laws”) in the U.S. and elsewhere prohibit types of conduct, practices, or arrangements deemed to be anti-competitive. Enforcement of competition laws in the healthcare industry remains a focus of the FTC and the U.S. Department of Justice. Some of our strategic transactions may require review by competition regulators, with potential delays or other unfavorable outcomes. Violations of competition laws can result in sanctions and other adverse actions, including criminal and civil penalties. Private plaintiffs also may bring civil lawsuits for alleged violations of competition laws, including claims for treble damages. Additionally, laws may be proposed to restrict certain healthcare ownership structures or arrangements, such as vertical integration involving physician practice administrative or management services and pharmaceutical distribution services, where traditional antitrust standards might not be implicated. Competition and related laws contribute to our compliance efforts and expense, and the enforcement, enactment, expansion, or application of any of the foregoing types of laws might materially adversely affect our operations and growth strategy.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-05-08）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm｜as_of：2026-05-08
<<<
We may be unsuccessful in achieving our strategic growth objectives. Our business strategy as a diversified healthcare services company includes investing, organically and inorganically, to further build an integrated oncology and multispecialty care platform and expand our biopharma services business. Our ability to grow those businesses will depend, among other things, on our: hiring and retaining talented individuals with necessary knowledge and skills; acquiring, developing, and implementing new technologies and capabilities, including AI; establishing new offerings and pivoting or enhancing existing ones; successfully identifying, completing, and realizing the anticipated benefits of strategic transactions; forming and expanding business relationships; anticipating the needs of our customers; and successfully competing against providers of similar services. New technologies, such as AI, may not result in the benefits we anticipate, may not enable us to keep pace with our competitors and the rapidly evolving technological landscape, and may require us to expend significant resources, including to maintain our capabilities. We have increased, and expect to continue to increase, our use of AI technology, which could heighten these risks. Additionally, some of our historical competitors and a growing number of new competitive entrants have more experience than we do in enabling technologies such as data analytics, machine learning, or AI.…

Our ability to attract, engage, develop, and retain qualified and experienced employees, including key executives and other talent, is essential for us to meet our objectives. We compete with many other businesses to attract and retain employees. Competition among potential employers results in increased salaries, benefits, or other employee-related costs, or in our failure to recruit and retain employees. We may experience loss of key personnel, including unexpectedly. Although we must adequately plan for timely succession of key management roles, our succession plans might not be effective, and employees might not successfully transition into new roles. Any of these risks might have a materially adverse impact on our business operations and our financial position or results of operations.

We are adversely impacted by competition and industry consolidation. Our businesses face a highly competitive global environment with strong competition from international, national, regional, and local full-line, short-line, and specialty distributors, service merchandisers, self-warehousing chain drug stores, manufacturers engaged in direct distribution, third-party logistics companies, and large payer organizations. In addition, our businesses face competition from various other service providers and from pharmaceutical and other healthcare manufacturers as well as other potential customers, which may from time to time decide to develop, for their own internal needs, supply management capabilities that might otherwise be provided by our businesses. We also may face competition from companies that move faster to adopt emerging technologies. Due to consolidation, a few large suppliers control a significant share of the pharmaceuticals market. This concentration reduces our ability to negotiate favorable terms with suppliers and causes us to depend on a smaller number of suppliers. Many of our customers, including healthcare organizations, have consolidated or joined group purchasing organizations and have greater power to negotiate favorable prices. Consolidation by our customers, suppliers, and competitors might reduce the number of market participants and give the remaining enterprises greater bargaining power, which might lead to erosion in our profit margin. Consolidation might increase counterparty credit risk because credit purchases increase for fewer market participants.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
