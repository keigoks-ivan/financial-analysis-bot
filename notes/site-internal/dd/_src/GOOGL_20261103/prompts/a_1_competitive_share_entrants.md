你是 stock-analyst v20 DD 的證據採集子 agent。標的：GOOGL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - GOOGL Alphabet market share gaining OR losing 2026
  - Alphabet new entrant OR displace threat Internet Content & Information 2026
  - GOOGL competitor design win 2026
  - Alphabet vs Internet Content & Information peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-05）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm｜as_of：2026-02-05
<<<
Competition Our business is characterized by rapid change as well as new and disruptive technologies. We face formidable competition in every aspect of our business, including but not limited to, from: •general purpose search engines and information services; •vertical search engines and e-commerce providers for queries on topics such as those related to travel, jobs, and health, which users may navigate directly to rather than go through Google; •online advertising platforms and networks, including online shopping and streaming services; •other forms of advertising, such as billboards, magazines, newspapers, radio, and television, as our advertisers typically advertise in multiple media, both online and offline; •digital content and application platform providers; •providers of enterprise cloud services; •AI model developers and providers of AI products and services; •companies that design, manufacture, and market consumer hardware products, including businesses that have developed proprietary platforms; •providers of digital video services; •social networks, which users may rely on for product or service referrals, rather than seeking information through traditional search engines; and •providers of workspace communication and connectivity products.

6. Table of Contents Alphabet Inc. Competing successfully depends heavily on our ability to continually develop and distribute innovative products and technologies to the marketplace across our businesses. For example, for advertising, competing successfully depends on attracting and retaining: •users, for whom other products and services are literally one click away, on the basis of the relevance of our advertising, as well as the general usefulness, security, and availability of our products and services; •advertisers, primarily based on our ability to generate sales leads, and ultimately customers, and to deliver their advertisements in an efficient and effective manner across a variety of distribution channels even as trends in advertising mediums and user preferences change; and •content providers, primarily based on the quality of our advertiser base, our ability to help these partners generate revenues from advertising, and the terms of our agreements with them.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-05）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm｜as_of：2026-02-05
<<<
9. Table of Contents Alphabet Inc. Within Google Services, we continue to invest heavily in devices, including our smartphones, home devices, and wearables, which is a highly competitive market with frequent introduction of new products and services, rapid adoption of technological advancements by competitors, increased market saturation in developed countries, short product life cycles, evolving industry standards, continual improvement in performance characteristics, and price and feature sensitivity on the part of consumers and businesses. There can be no assurance we will be able to provide devices that compete effectively.

Within Other Bets, we are investing significantly in areas such as life sciences and transportation, among others. These investment areas face intense competition from large, experienced, and well-funded competitors, and our offerings, many of which involve the development of new and emerging technologies, may not be successful, or be able to compete effectively or operate at sufficient levels of profitability.

Our business environment is rapidly evolving and intensely competitive. Our businesses face changing technologies, shifting user needs, and frequent introductions of rival products and services. To compete successfully, we must accurately anticipate technology developments and deliver innovative, relevant, and useful products, services, and technologies in a timely manner. For example, with the rise of AI in recent years, we have increasingly focused our investments in building powerful AI tools and AI enhancements to our existing products and services to better cater to our users, customers, and other partners. As our businesses evolve, the competitive pressure to innovate will encompass a wider range of products and services. We must continue to invest significant resources in technical infrastructure, including the development of our custom TPUs, and research and development, including through acquisitions, in order to enhance our technology, products, and services.

We have many competitors in different industries. Our current and potential domestic and international competitors range from large and established companies to emerging start-ups. Some competitors have longer operating histories and well-established relationships in various sectors. They can use their experience and resources in ways that could affect our competitive position, including by making acquisitions and entering into other strategic arrangements; continuing to invest heavily in technical infrastructure, research and development, and in talent; initiating intellectual property and competition claims (whether or not meritorious); and continuing to compete for users, advertisers, customers, and content providers. Further, discrepancies in enforcement of existing laws may enable our lesser known competitors to aggressively interpret those laws without commensurate scrutiny, thereby affording them competitive advantages. Our competitors may also be able to innovate and provide products and services faster or more cost effectively than we can or may foresee the need for products and services before we do.

Our financial condition and operating results may also suffer if our products and services are not responsive in a timely manner to the evolving needs and desires of our users, advertisers, publishers, customers, and content providers, or if we miscalculate those needs and desires and invest significantly in areas that fail to gain sufficient market traction. As new and existing technologies continue to develop, competitors and new entrants may be able to offer experiences that are, or that are perceived to be, substantially similar to or better than ours, and the consumers may change how they obtain information online, potentially reducing the utility of our existing products and services. These technologies could reduce usage of our products and services, and force us to compete in different ways and expend significant resources to develop and operate equal or better products and services. Competitors' success in providing compelling products and services or in attracting and retaining users, advertisers, publishers, customers, and content providers could harm our financial condition and operating results.

We may enter into long-term contracts for materials and products that commit us to significant terms and conditions. We may face costs for materials and products that are not consumed due to market demand, technological change, excess or obsolete inventory, changed consumer preferences, quality, product recalls, and warranty issues. Certain of our competitors may negotiate more favorable contractual terms based on volume and other commitments that may provide them with competitive advantages and may affect our supply. For example, industry supply capacity for AI accelerators, including GPUs as well as our custom-built TPUs, is highly competitive and rapidly evolving. If we are unable to negotiate favorable contractual terms or our competitors claim the supply or capacity first, we may face increased costs and supply constraints, which could harm our business, financial condition, and operating results.

Our ability to compete effectively and our future success depend on our continuing to identify, hire, develop, motivate, and retain highly skilled personnel for all areas of our organization. Competition in our industry for qualified employees, particularly AI talent, is intense, and certain of our competitors have directly targeted, and may continue to target, our employees. In addition, our compensation arrangements, such as our equity award programs, may not always be successful in attracting new employees and retaining and motivating our existing employees. Immigration policy and regulatory changes, and uncertainty regarding such policies and regulations, may also affect our ability to hire, mobilize, or retain some of our global talent. All of our executive officers and key employees are at-will employees, and we do not maintain any key-person life insurance policies.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GOOGL_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
