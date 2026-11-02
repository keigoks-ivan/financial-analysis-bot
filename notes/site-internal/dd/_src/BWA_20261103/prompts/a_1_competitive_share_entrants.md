你是 stock-analyst v20 DD 的證據採集子 agent。標的：BWA。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - BWA BorgWarner market share gaining OR losing 2026
  - BorgWarner new entrant OR displace threat Auto Tier 1 / Propulsion + eProducts 2026
  - BWA competitor design win 2026
  - BorgWarner vs Auto Tier 1 / Propulsion + eProducts peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm｜as_of：2026-02-11
<<<
Competition The Company’s reportable segments compete worldwide with a number of other manufacturers and distributors that produce and sell similar products. Many of these competitors are larger and have greater resources than the Company. Technological innovation, application engineering development, quality, price, delivery and program launch support are the primary methods of competition.

The Company’s major non-OEM competitors are Robert Bosch GmbH, Denso Corporation, Garrett Motion, Hitachi, Ltd., Magna Powertrain (an operating unit of Magna International Inc.), Valeo, Schaeffler Group and Contemporary Amperex Technology Co., Limited. The Company also competes with certain start-ups in electrification.

In addition, a number of the Company’s major OEM customers manufacture, for their own use and for others, products that compete with the Company's products. Other current OEM customers could elect to manufacture products to meet their own requirements or to compete with the Company. We cannot 11 Table of Contents guarantee that the Company’s business will not be adversely affected by increased competition in the markets in which it operates.

For many of its products, the Company’s competitors include suppliers in parts of the world that enjoy economic advantages such as lower labor costs, lower health care costs, lower tax rates and, in some cases, export subsidies and/or raw materials subsidies. Also, see Item 1A, “Risk Factors.”
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/908255/000090825526000011/bwa-20251231.htm｜as_of：2026-02-11
<<<
We face strong competition. We compete globally with a number of other manufacturers and distributors that produce and sell similar products. Price, quality, delivery, technological innovation, engineering development and program launch support are the primary elements of competition. Our competitors include vertically integrated units of our major OEM customers, as well as a large number of independent domestic and international suppliers. Additionally, our competitors include start-ups that may be well funded, with the result that they could have more operational and financial flexibility than we have. A number of our competitors are larger than we are, and some competitors have greater financial and other resources than we do. Although many OEMs have indicated that they will continue to rely on outside suppliers, a number of major OEM customers have indicated their intent to insource certain components that we produce, and many do manufacture products for their own uses that directly compete with our products. These OEMs have elected and could elect to manufacture such products for their own uses in place of the products we currently supply. Our traditional OEM customers, faced with intense international competition, have continued to expand their global sourcing of components.…

The automotive industry is increasingly focused on improved vehicle efficiency and reduced emissions, including the development of hybrid and electric vehicles, largely as a result of changing consumer preferences and increasingly stringent global regulatory requirements related to climate change, and of advanced driver-assistance technologies, with the goal of developing and introducing a commercially viable, fully automated driving experience. There has also been an increase in consumer preferences for mobility-on-demand services, such as car and ride sharing, as opposed to automobile ownership, which may result in a long-term reduction in the number of vehicles per capita. In addition, some industry participants are exploring transportation through alternatives to automobiles. These evolving areas have also attracted increased competition from entrants outside the traditional automotive industry. While we are focused on driving growth through our ability to capitalize on certain potential trends, such as the move toward hybrid and electric vehicles, some of the focuses and trends are not part of our product line or strategy. If we do not continue to innovate and develop, or acquire, new and compelling products that capitalize upon new technologies, including artificial intelligence (“AI”) and machine learning, or improve in response to OEM and consumer preferences, this could have an adverse impact on our results of operations.

We own important intellectual property, including patents, trademarks, copyrights, and trade secrets and are involved in numerous licensing arrangements. Our intellectual property plays an important role in maintaining our competitive position in a number of the markets that we serve. Our competitors may develop technologies that are similar or superior to our proprietary technologies or design around the patents we own or license. Further, as we expand our operations in jurisdictions where the enforcement of intellectual property rights is less robust, the risk of others duplicating our proprietary technologies increases, despite efforts we undertake to protect them. Our inability to protect or enforce our intellectual property rights or claims that we are infringing intellectual property rights of others could adversely affect our business and our competitive position.

Further, we continually update and expand our information technology systems to enable us to run our business more efficiently, including the potential incorporation of AI solutions into our information systems and processes. The increasing use and evolution of advanced technology solutions creates potential risks for loss or misuse of Company data that forms part of any data set that was collected, used, stored or transferred to run our business. Any unintentional dissemination or intentional destruction of confidential information stored in our or our third-party providers' systems, portable media or storage devices may result in significantly increased business and security recovery costs, a damaged reputation, administrative penalties, or costs related to defending legal claims. The use of AI in the development of our products and services could also cause loss or theft of intellectual property as well as subject us to risks related to intellectual property infringement or misappropriation, data privacy and cybersecurity. In addition, if the content, analyses, or recommendations that AI programs assist in producing are or are alleged to be deficient, inaccurate, or biased, then our business, financial condition, and results of operations and our reputation may be adversely affected.…

To the extent we are not able to successfully launch new business, vehicle production at our customers could be significantly delayed or shut down. Such situations could result in loss of customers, significant financial penalties to us or a diversion of personnel and financial resources to improving launches rather than investment in continuous process improvement or other growth initiatives and could result in our customers shifting work away from us to a competitor, all of which could result in loss of revenue or loss of market share and could have an adverse effect on our profitability and cash flows.

Maintaining a strong position in the Chinese market is a key component of our global growth strategy. The automotive supply market in China is highly competitive, with competition from many of the largest global manufacturers and numerous smaller domestic manufacturers. As the Chinese market evolves, market participants have acted, and we anticipate will continue to act aggressively to increase or maintain their market share. Increased competition may result in price reductions, reduced margins and our inability to gain or hold market share. Domestic Chinese OEMs continue to expand their market share in and outside of China, and are increasingly insourcing certain components once sourced from Tier 1 suppliers. In addition, our business in China is sensitive to economic, political, social and market conditions that drive sales volumes in China. If we are unable to maintain our position in the Chinese market or if vehicle sales in China decrease, our business and financial results could be adversely affected.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
