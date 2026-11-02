你是 stock-analyst v20 DD 的證據採集子 agent。標的：MSFT。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Microsoft distribution channel disruption OR shift 2026
  - MSFT Microsoft business model transition subscription OR platform 2026
  - Software - Infrastructure channel disintermediation D2C 2026
  - Microsoft go-to-market change 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2026，申報 2026-07-29）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm｜as_of：2026-07-29
<<<
Item 1 LinkedIn LinkedIn connects the world’s professionals to make them more productive and successful and transforms the way companies hire, market, sell, and learn. In addition to LinkedIn’s free services, LinkedIn offers monetized solutions designed to offer AI-enabled insights and productivity: Talent Solutions, Marketing Solutions, Premium Subscriptions, and Sales Solutions. Growth will depend on our ability to increase LinkedIn member engagement on the platform and our ability to continue offering insight and AI-enabled services that provide value for our members and customers. LinkedIn revenue is mainly affected by demand from enterprises and professionals for subscriptions to Talent Solutions, Sales Solutions, and Premium Subscriptions offerings, as well as member engagement and the quality of the sponsored content delivered to those members to drive Marketing Solutions.

More Personal Computing Our More Personal Computing segment consists of products and services that put customers at the center of the experience with our technology. This segment primarily comprises: •Windows and Devices, including Windows OEM licensing (Windows Pro and non-Pro licenses sold through the OEM channel) and Devices, comprising Surface and PC accessories.

Windows and Devices The Windows operating system is designed to deliver a more personal computing experience for users by enabling consistency of experience, applications, and information across their devices. Windows OEM revenue is impacted significantly by the number of Windows operating system licenses purchased by OEMs, which they pre-install on the devices they sell. In addition to computing device market volume, Windows OEM revenue is impacted by: •The mix of computing devices based on form factor and screen size.

•Changes in inventory levels in the OEM channel. •Pricing changes and promotions, pricing variation that occurs when the mix of devices manufactured shifts from local and regional system builders to large multinational OEMs, and different pricing of Windows versions licensed.

Item 1 DISTRIBUTION, SALES, AND MARKETING Distribution occurs through a combination of direct and indirect channels. Direct sales activities serve customers ranging from large multinational enterprises and public sector organizations to small and medium-sized businesses. Indirect sales activities serve customers through a broad network of partners that support the sale, deployment, and management of Microsoft products and services worldwide.

The indirect channel extends the reach of commercial offerings and supports customers across industries, geographies, and organization sizes. Sales and distribution models continue to evolve to support cloud-based, subscription-based, and consumption-based offerings while maintaining multiple options through which customers may acquire and manage our products and services.

OEMs license and preinstall certain Microsoft software on devices that are sold to end customers. In addition, certain products and services are available through online purchasing channels and digital marketplaces.

The information found on these websites is not part of, or incorporated by reference into, this or any other report we file with, or furnish to, the SEC. In addition to these channels, we use social media to communicate to the public. It is possible that the information we post on social media could be deemed to be material to investors. We encourage investors, the media, and others interested in Microsoft to review the information we post on the social media channels listed on our Investor Relations website.

•Competing platforms have content and application marketplaces with scale and significant installed bases. The variety and utility of content and applications available on a platform are important to device purchasing decisions. Users may incur costs to move data and buy new content and applications when switching platforms. To compete successfully, we must enlist developers to write applications for our platform and ensure that these applications have high quality, security, customer appeal, and value. Efforts to compete with competitors’ content and application marketplaces may increase our cost of revenue and lower our operating margins. Competitors’ rules governing their content and applications marketplaces may restrict our ability to distribute products and services through them in accordance with our technical and business model objectives.

Item 1A RISKS RELATING TO THE EVOLUTION OF OUR BUSINESS We make significant investments in products and services that may not achieve expected returns. We will continue to make significant investments in research, development, and marketing for existing products, services, and technologies, including AI-based products and services. We also invest in the development and acquisition of a variety of hardware for productivity, communication, and entertainment, including PCs, tablets, and gaming devices. Investments in new technology are speculative. Commercial success depends on many factors, including innovation, developer support, and effective distribution and marketing. If customers do not perceive our latest offerings as providing significant new functionality or other value, they may reduce their purchases of new software and hardware products or upgrades, unfavorably affecting revenue. We may not achieve significant revenue from new product, service, and distribution channel investments for several years, if at all. New products and services may not be profitable or may not achieve operating margins as high as we have experienced historically. We may not get engagement in certain features that drive post-sale monetization opportunities. Our data-handling practices across our products and services will continue to be under scrutiny. Perceptions of mismanagement, driven by regulatory activity or negative public reaction to our practices or product experiences, could negatively impact product and feature adoption.…

Our product distribution system relies on an extensive partner and retail network. OEMs building devices that run our software have also been a significant means of distribution. The impact of economic conditions on our partners, such as the bankruptcy of a major distributor, OEM, or retailer, could cause sales channel disruption.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSFT_20261102/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
