你是 stock-analyst v20 DD 的證據採集子 agent。標的：META。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - META Meta Platforms market share gaining OR losing 2026
  - Meta Platforms new entrant OR displace threat Internet Content & Information 2026
  - META competitor design win 2026
  - Meta Platforms vs Internet Content & Information peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
Competition Our business is characterized by innovation, rapid change, and disruptive technologies. We compete with companies providing connection, sharing, discovery, and communication products and services to users online, as well as companies that sell advertising to businesses looking to reach consumers and/or develop tools and systems for managing and optimizing advertising campaigns. We face significant competition in every aspect of our business, including, but not limited to, companies that facilitate the ability of users to create, share, communicate, and discover content and information online or enable marketers to reach their existing or prospective audiences. We compete to attract, engage, and retain people who use our products, to attract and retain businesses that use our free or paid business and advertising services, and to attract and retain developers who build compelling applications that integrate with our products. We also compete with companies in the development and application of AI, particularly with respect to the development of frontier AI models, as well as the development and delivery of consumer hardware and augmented and virtual reality products and services.…

Compensation, Benefits, Health, and Well-being We offer competitive compensation to attract and retain the best people, and we help care for our people so they can focus on our mission. Our employees' total compensation package includes market-competitive salary, bonuses or sales incentives, and equity. We generally offer full-time employees equity at the time of hire and through annual equity grants because we want them to be owners of the company and committed to our long-term success.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-01-29）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm｜as_of：2026-01-29
<<<
Further, we face significant competition from other companies that are developing their own AI features and technologies, including competition from AI features and technologies that may be similar or superior to our technologies or more cost-effective to develop and deploy, or that otherwise achieve more timely or successful market acceptance. Given the long history of development in the AI sector, other parties may have (or in the future may obtain) patents or other proprietary rights that would prevent, limit, or interfere with our ability to make, use, or sell our own AI features. Our AI initiatives also depend on our access to data to effectively train our models, which is subject to risks related to the availability or costs of data, regulatory or other legal developments, or other factors, as well as our ability to attract and retain specialized personnel in a limited and competitive talent market. Further, our ability to continue to develop and effectively deploy AI technologies is dependent on access to specific third-party equipment, technology, and other technical and physical infrastructure, such as processing hardware, network capacity, models, computing power, and related energy requirements, as to which we cannot control the availability or pricing, especially in a highly competitive environment.

We believe the metaverse, an embodied internet where people have immersive experiences beyond two-dimensional screens, is the next evolution in social technology. In 2021, we announced a shift in our business and product strategy to focus on helping to bring the metaverse to life, and we are directing our efforts toward innovations in AI, wearables, and devices to help build next-generation interfaces. We expect this will be a complex, evolving, and long-term initiative that will involve the development of new and emerging technologies, continued investment in infrastructure as well as privacy, safety, and security efforts, and collaboration with other companies, developers, partners, and other participants. However, the metaverse may not develop in accordance with our expectations, and market acceptance of features, products, or services we build is uncertain. We regularly evaluate our product roadmaps and make significant changes as our understanding of the technological challenges and market landscape and our product ideas and designs evolve. In addition, we have relatively limited experience with consumer hardware products and virtual and augmented reality technology, which may enable other companies to compete more effectively than us.…

We compete with companies providing connection, sharing, discovery, and communication products and services to users online, as well as companies that sell advertising to businesses looking to reach consumers and/or develop tools and systems for managing and optimizing advertising campaigns. We face significant competition in every aspect of our business, including, but not limited to, companies that facilitate the ability of users to create, share, communicate, and discover content and information online or enable marketers to reach their existing or prospective audiences. We compete to attract, engage, and retain people who use our products, to attract and retain businesses that use our free or paid business and advertising services, and to attract and retain developers who build compelling applications that integrate with our products. We also compete with companies in the development and application of AI, particularly with respect to the development of frontier AI models, as well as the development and delivery of consumer hardware and augmented and virtual reality products and services. We also expect to face additional competition as we introduce or acquire new products, as our existing products evolve, or as other companies introduce new products and services, including as part of efforts to innovate through the development and application of AI and other new technologies, as well as efforts to develop the metaverse.

Some of our current and potential competitors may have greater resources, experience, or stronger competitive positions in certain product segments, geographic regions, or user demographics than we do. For example, some of our competitors may be domiciled in different countries and subject to political, legal, and regulatory regimes that enable them to compete more effectively than us. These factors may allow our competitors to respond more effectively than us to new or emerging technologies and changes in market conditions. We believe that some users, particularly younger users, are aware of and actively engaging with other products and services similar to, or as a substitute for, our products and services, and we believe that some users have reduced their use of and engagement with our products and services in favor of these other products and services. In addition, from time to time we make updates to our products and services to improve the user experience (including to help provide users with safe, positive, age-appropriate experiences), and these changes have had, and may in the future have, the effect of reducing time spent and some measures of user engagement with our products and services.…

Our competitors may develop products, features, or services that are similar to ours or that achieve greater acceptance, may undertake more far-reaching and successful product development efforts or marketing campaigns, or may adopt more aggressive pricing policies. Some competitors may gain a competitive advantage against us in areas where we operate, including: by making acquisitions; by limiting our ability to deliver, target, or measure the effectiveness of ads; by imposing fees or other charges related to our applications or our delivery of ads; by making access to our products more difficult or impossible; by making it more difficult to communicate with our users; by limiting the ability of our devices or products to interoperate with their popular platforms or products; or by integrating competing platforms, applications, or features into products they control such as mobile device operating systems, search engines, browsers, or e-commerce platforms. For example, each of Apple and Google have integrated competitive products with iOS and Android, respectively. In addition, Apple has released changes to iOS that limit our ability, and the ability of others in the digital advertising industry, to target and measure ads effectively.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
