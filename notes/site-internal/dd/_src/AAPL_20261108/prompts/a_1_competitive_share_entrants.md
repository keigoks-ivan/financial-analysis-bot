你是 stock-analyst v20 DD 的證據採集子 agent。標的：AAPL。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - AAPL Apple market share gaining OR losing 2026
  - Apple new entrant OR displace threat Consumer Electronics 2026
  - AAPL competitor design win 2026
  - Apple vs Consumer Electronics peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-03）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm｜as_of：2026-11-03
<<<
Competition The markets for the Company’s products and services are highly competitive and are characterized by aggressive price competition, downward pressure on gross margins, continual improvement in product performance, and price sensitivity on the part of consumers and businesses. The markets in which the Company competes are further defined by frequent introduction of new products, services and technologies, including artificial intelligence technologies, short product life cycles, evolving industry standards, and rapid adoption of technological advancements. Many of the Company’s competitors seek to compete primarily through aggressive pricing and very low cost structures, and by imitating the Company’s products and infringing on its intellectual property.

Apple Inc. | 2026 Form 10-K | 2 The Company’s ability to compete successfully depends heavily on ensuring the continuing and timely introduction of innovative new products, services and technologies. The Company designs and develops nearly the entire solution for its products, including the hardware, operating system, numerous software applications and related services. Principal competitive factors important to the Company include price, product and service features, including security features, relative price and performance, product and service quality and reliability, design and technology innovation, a strong third-party software and accessories ecosystem, marketing and distribution capability, service and support, corporate reputation, and the ability to effectively protect and enforce the Company’s intellectual property rights.

The Company is focused on expanding its market opportunities related to smartphones, personal computers, tablets, wearables and accessories, and services. The Company’s products, services and technologies face substantial competition from companies that have significant technical, marketing, distribution and other resources, as well as established hardware, software, and service offerings with large customer bases. In addition, the Company faces significant competition as competitors imitate the Company’s product features and applications to offer more competitive solutions. The Company also expects competition to intensify as competitors imitate the Company’s approach to providing components seamlessly within their offerings or work collaboratively to offer integrated solutions. Some of the Company’s competitors have broad product lines, low-priced products, large installed bases of active devices, and large customer bases. Competition has been particularly intense as competitors have aggressively cut prices and lowered product margins. Certain competitors have the resources, experience or cost structures to provide products and services at little or no profit or even at a loss. The Company has a minority market share in the global smartphone, personal computer, tablet and wearables markets, and some of the markets in which the Company competes have from time to time experienced little to no growth or contracted overall.…

Research and Development Because the industries in which the Company competes are characterized by rapid technological advances, the Company’s ability to compete successfully depends heavily upon its ability to successfully manage frequent introductions and transitions of competitive products, services and technologies, including artificial intelligence technologies, to the marketplace. The Company continues to develop new technologies to enhance existing hardware, software and services, and to expand the range of its offerings through research and development (“R&D”), licensing of intellectual property and technology, and acquisition of third-party businesses and technology.

In addition to Company-owned intellectual property, many of the Company’s hardware, software and services include technology or intellectual property that must be licensed from third parties. It may be necessary in the future to seek or renew licenses relating to various aspects of the Company’s hardware, software and services. While the Company has generally been able to obtain such licenses on commercially reasonable terms in the past, there is no guarantee that such licenses could be obtained in the future on commercially reasonable terms or at all. In addition, the Company’s products and services have been, and may in the future be, alleged to infringe the intellectual property rights of others due to extensive existing intellectual property coverage, the rapid pace of new intellectual property rights generation, and technological changes in the industries in which the Company currently competes or may compete in the future. This risk may be exacerbated by the use of new and emerging technologies, including machine learning and artificial intelligence, which can involve, among other things, the acquisition and use of copyrighted materials for training as well as the potential reproduction of copyrighted materials in their outputs.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-11-03）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm｜as_of：2026-11-03
<<<
The Company’s ability to compete successfully also depends on the effective protection and enforcement of its intellectual property rights. Regulatory requirements, government investigations and litigation can force the Company to withdraw from, or modify its products, services and technologies for, certain countries and limit its ability to derive value from, or to enjoin others from using, its intellectual property rights. Additionally, they may require the Company to share its innovations with competitors. Any of these outcomes can adversely affect the Company’s competitive advantage.

The Company currently holds a significant number of patents, trademarks and copyrights and has registered, and applied to register, additional patents, trademarks and copyrights. In contrast, many of the Company’s competitors seek to compete primarily through aggressive pricing and very low cost structures, and by imitating the Company’s products and infringing on its intellectual property. Effective intellectual property protection is not consistently available in every country in which the Company operates. If the Company is unable to continue to develop and sell innovative new products with attractive margins or if competitors infringe on the Company’s intellectual property, the Company’s ability to maintain a competitive advantage could be materially adversely affected.

Apple Inc. | 2026 Form 10-K | 7 The Company’s products, services and technologies face substantial competition from companies that have significant technical, marketing, distribution and other resources, as well as established hardware, software and service offerings. In addition, the Company faces significant competition as competitors imitate the Company’s product features and applications to offer more competitive solutions. The Company also expects competition to intensify as competitors imitate the Company’s approach to providing components seamlessly within their offerings or work collaboratively to offer integrated solutions. Some of the Company’s competitors have broad product lines, low-priced products, large installed bases of active devices, and large customer bases. Competition has been particularly intense as competitors have aggressively cut prices and lowered product margins. Certain competitors have the resources, experience or cost structures to provide products and services at little or no profit or even at a loss. The Company has a minority market share in the global smartphone, personal computer, tablet and wearables markets, and some of the markets in which the Company competes have from time to time experienced little to no growth or contracted overall.

The Company competes with a number of companies in the development and deployment of artificial intelligence and has made significant investments in building artificial intelligence features and related infrastructure across its products and services. Failure to successfully develop, deploy or differentiate artificial intelligence capabilities, or to do so as quickly or cost-effectively as competitors, could result in loss of market share, erosion of competitive positioning, and inability to attract or retain customers and talent.

Due to the highly volatile and competitive nature of the markets and industries in which the Company competes, the Company must continually introduce new products, services and technologies, enhance existing products and services, effectively stimulate customer demand for new and upgraded products, services and technologies, navigate global regulatory requirements and barriers to market access, and successfully manage the transition to or adoption of these new and upgraded products, services and technologies. The success of new product, service and technology introductions depends on a number of factors, including the Company’s ability to recruit and retain highly skilled personnel, and the timely and successful development, introduction and market acceptance of new products, services and technologies. Success also relies on the Company’s ability to manage the risks associated with new technologies and production ramp-up issues, the effective integration of third-party services and technologies into the Company’s products and services, the availability, delivery and performance of application software or other third-party support for the Company’s products and services, the ability of the Company to accurately predict demand across markets, the effective management of manufacturing and other purchase commitments and inventory levels in line with anticipated product demand, and the availability of products in appropriate quantities and at expected costs.…

The Company’s minority market share in the global smartphone, personal computer, tablet and wearables markets can make developers less inclined to develop or upgrade software for the Company’s products and more inclined to devote their resources to developing and upgrading software for competitors’ products with larger market share. When developers focus their efforts on these competing platforms, the availability and quality of applications for the Company’s devices can suffer.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
