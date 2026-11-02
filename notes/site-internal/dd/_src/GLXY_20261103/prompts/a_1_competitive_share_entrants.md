你是 stock-analyst v20 DD 的證據採集子 agent。標的：GLXY。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - GLXY Galaxy Digital market share gaining OR losing 2026
  - Galaxy Digital new entrant OR displace threat Capital Markets 2026
  - GLXY competitor design win 2026
  - Galaxy Digital vs Capital Markets peers market share trend 2025 2026


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
Competition We operate in highly competitive and rapidly evolving industries and face competition from both established financial institutions and emerging crypto-native entities, as well as other AI/HPC hyperscalers. Our competitive landscape is varied across two operating business segments: Digital Assets, which includes our Global Markets and Asset Management & Infrastructure Solutions businesses, and Data Centers, which includes our scalable HPC infrastructure. See “Risk Factors—Risks Related to Our Operations—We operate in highly competitive industries and we compete against unregulated or less regulated companies and companies with greater financial and other resources, and our business, operating results, and financial condition may be adversely affected if we are unable to respond to our competitors effectively” for more information on our competitive landscape and related risks.

•Galaxy’s trading business competes against OTC brokers, derivatives platforms, and prime brokerage firms that offer digital asset trading and financing to institutional clients. These include both traditional financial institutions expanding into digital assets and crypto-native trading platforms. Leveraging advanced technology, Galaxy’s trading business also competes with decentralized finance platforms, where protocol-based solutions for lending, trading, and staking operate without traditional intermediaries.

Our investment banking business faces competition from boutique advisory firms specializing in blockchain and fintech, as well as global investment banks that provide cross-sector M&A, restructuring, and capital-raising services. These competitors range from niche players with deep digital assets expertise to large institutions with broad sectoral reach.

Data Centers Galaxy’s Data Centers operating business segment competes with a range of infrastructure providers that are building or repurposing facilities to support the rapidly growing demand for AI and compute-intensive workloads. This includes traditional data center operators expanding into HPC, cloud infrastructure providers scaling capacity, and former crypto mining operators pivoting to meet the needs of AI workloads. Competition centers around access to reliable, large-scale power, high-speed connectivity, cooling solutions, and strategically located real estate—all critical factors in delivering the performance and efficiency required by AI and HPC clients.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-26）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm｜as_of：2026-02-26
<<<
•We operate in highly competitive industries; and we compete against unregulated or less regulated companies and companies with greater financial and other resources; and our business, operating results, and financial condition may be adversely affected if we are unable to respond to our competitors effectively.

Our ability to grow our AI/HPC data center business in the future is also dependent on the overall market for AI/HPC data centers. The broader adoption, use, and commercialization of AI technology, and the continued rapid pace of developments in the AI industry, are inherently uncertain. For example, certain AI technology is under public scrutiny for creating inaccurate, incomplete or misleading content, unintended biases and other discriminatory or unexpected results, errors or inadequacies and may be, or be perceived to be, deficient, inaccurate, biased, unethical or otherwise flawed. Consumer and societal attitudes toward AI are evolving and there is a risk that regulators or the public may perceive AI technologies negatively. Concerns about automation, automated decision making, privacy, security, transparency, or other ethical considerations could deter adoption. Therefore, it is difficult to predict the demand for AI/HPC data center capacity, the size and growth rate for this market, the entry of competitive products, or the success of any existing or future products that may compete with any AI/HPC data centers we may develop. In addition, we cannot assure you that we will be able to keep up with the changing AI landscape or in developing services or infrastructure that can meet our customers’ evolving needs in a timely manner, if at all.…

We operate in highly competitive industries and we compete against unregulated or less regulated companies and companies with greater financial and other resources, and our business, operating results, and financial condition may be adversely affected if we are unable to respond to our competitors effectively.

The industries and markets in which we compete are evolving and highly competitive, with multiple participants competing for the same customers. Our current and potential future competition comes from traditional financial services providers, financial technology companies, asset management firms, consumer financial service providers and technology platforms and providers of crypto-based services, as well as traditional data center operators expanding into HPC, existing AI/HPC data center operators, cloud infrastructure providers, and former crypto mining operators pivoting to meet the needs of AI workloads.

Some of our current and potential future competitors have longer operating histories and greater capital resources than we have and may offer a wider range of products and services. Some of our competitors, particularly new and emerging technology companies and those located outside the United States, are not subject to the same regulatory requirements or scrutiny we are subject to, which could allow them to innovate more quickly or take more risks, placing us at a competitive 28 Table of Content disadvantage. In addition, some of our competitors might also be able to respond more quickly to new or changing opportunities and demands and withstand changing market conditions better than we can, especially larger competitors that might benefit from more diversified product and customer bases.

Many innovative start-up companies and larger companies have made, and continue to make, significant investments in research and development, and we expect these companies to continue to develop similar or superior products and technologies that compete with our products. Further, more traditional financial and non-financial services businesses may choose to offer crypto-based services in the future as the digital assets industry grows and as greater legal and regulatory certainty emerges. Our current and potential competitors may establish cooperative relationships among themselves or with third parties that may further enhance their resources, or may otherwise have certain competitive advantages over us. The impact of competitors with superior name recognition, greater market acceptance, larger customer bases, lower compliance costs, or stronger capital positions could adversely affect our results of operations and customer acquisition and retention.

If we are unable to compete successfully, or if competing successfully requires us to take costly actions in response to the actions of our competitors, our business, operating results, and financial condition could be adversely affected.

The industries in which we operate have been characterized by many rapid, significant, and disruptive products and services in recent years. These include decentralized applications, which allow yield farming, staking and liquid staking, token wrapping, governance tokens, innovative programs to attract customers such as transaction fee mining programs, initiatives to attract traders such as trading competitions, airdrops and giveaways, staking reward programs, and novel cryptocurrency fundraising and distribution schemes. We expect new services and technologies to continue to emerge and evolve, which may be superior to, or render obsolete, the products and services that we currently provide. Because these services and technologies are novel and may present risks, we cannot predict the effects of new services and technologies on our business. However, our ability to grow our customer base and revenue will depend in part on our ability to innovate and create successful new products and services, both independently and in conjunction with third parties. In particular, developing and incorporating new products and services into our business may require substantial expenditures, take considerable time, and ultimately may not be successful. Any new products or services could fail to attract customers, generate revenue, or perform or integrate well with third-party applications and platforms.…

The asset management industry is highly competitive and has relatively low barriers to entry. As digital assets become more mainstream, additional competitors, potentially in large numbers, have and may begin providing asset management services with respect to digital assets. We compete based on a number of factors including: investment performance, the level of fees charged, the quality and diversity of services and products provided, name recognition and reputation, and the ability to develop new investment strategies and products to meet the changing needs of investors. In addition, the introduction of new technologies, as well as regulatory changes, may significantly alter the competitive landscape for investment managers in digital assets. This could lead to fee compression or require us to spend more to modify or adapt our product offerings to attract and retain customers and remain competitive with products and services offered by new 37 Table of Content competitors in the industry. Increased competition on the basis of any of these factors, including competition leading to fee reductions, may cause our AUM, revenue and earnings to decline and materially and negatively impact the success of our asset management business and affect our overall business, results of operations and financial condition.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
