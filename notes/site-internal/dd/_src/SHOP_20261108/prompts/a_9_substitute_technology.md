你是 stock-analyst v20 DD 的證據採集子 agent。標的：SHOP。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[substitute_technology] 替代技術
Q: 是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？
  - Shopify product substitute technology threat 2026
  - Software - Application alternative technology disruption 2026 2027
  - SHOP Shopify technology obsolescence risk
  - Software - Application next-generation technology roadmap 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm｜as_of：2026-02-11
<<<
Research and Development Shopify is building products and solutions for commerce that enable merchants of all sizes around the world to successfully start and scale their businesses on Shopify. We strive to increase the probability of a merchant's future success by finding and supporting solutions that enable merchant discovery and allow merchants to develop a commerce presence across multiple channels and geographies. We expect to continue to leverage emerging technologies including data analytics, machine learning and AI in our products, to help our merchants increase productivity, improve workflows, make smarter decisions and enhance the reach of their products. For example, Shopify provides a suite of AI-enabled features integrated across the Shopify platform, including Sidekick, our AI-enabled commerce assistant, and Agentic Storefronts, which enables agent-assisted product discovery and checkout across a number of AI platforms. Research and development at Shopify is currently focused on product management, product development and product design to accomplish these goals.

10 Table of Contents Competition Our market is transforming, competitive and highly fragmented, and we expect competition to increase in the future. We believe the principal competitive factors in our market are: •vision for commerce and product strategy; •simplicity and ease of use for merchants and their buyers; •integration of multiple sales channels; •embedding of commerce functionality across more surfaces; •interoperability across surfaces; •cost-effective solutions; •significant app ecosystem; •breadth and depth of functionality; •pace of innovation; •powerful data analytics; •ability to leverage emerging technologies, including AI; •ability to scale; •security and reliability; •support for merchant discovery and brand development; and •brand recognition and reputation.

The growth of ecommerce may attract new entrants or new offerings from existing competitors. Additionally, some merchants may select one or more integrated or standalone offerings from other providers such as: •ecommerce software vendors; •content management systems; •payment processors; •point of sale providers; •domain registrars; •shipping label providers; •fulfillment service providers; •alternative lenders; •financial services; •cross-border services providers; and •marketplaces.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm｜as_of：2026-02-11
<<<
A portion of our business consists of small and medium-sized businesses. Small and medium-sized businesses tend to be more susceptible than larger businesses to general economic conditions and other business-related risks, which has, and may continue to, contribute to merchant turnover. These businesses may be particularly susceptible to changes in economic conditions, including pressure from inflation, declines in consumer spending, international trade risks and/or the imposition of trade protection measures (such as the imposition of or an increase in tariffs or import and export licensing 14 Table of Contents and control requirements), global supply chain disruptions and shortages including events impacting shipping and fulfillment all of which may negatively impact a merchant’s business and in turn, negatively impact our business. Large merchants generally require higher service levels and have more complex needs than small and medium-sized businesses. As we look to further tailor our sales strategies to attract large volume brands, we may face elevated costs, extended onboarding cycles and decreased predictability in finalizing the sale of products and services to these merchants. If we fall short of meeting the requirements of these merchants, it could impede our ability to grow within the enterprise market.

Competition may intensify as our competitors enter into business arrangements or alliances or raise additional capital, or as established companies in other market segments or geographic markets expand into our market segments or geographic markets. For instance, certain competitors could use strong positions in one or more markets to gain a competitive advantage against us in areas where we operate by, among other things: integrating competing platforms, applications or features into products they control; making acquisitions; or making access to our platform more difficult including by changing the terms of service related to their products, which could impact our and our merchants' ability to offer services or adversely impact our results of operations and those of our merchants. For example, large technology platforms have imposed and are considering imposing, or may provide their users the ability to impose, restrictions on the ability of other parties to access or use data from their customers and users. These practices may impact our merchants' ability to market and sell their offerings, which could affect the demand for our platform and lead to the loss of current or prospective merchants or other business relationships. Competitors may also be more established in international markets with a better understanding of local customs, providing them a competitive advantage.…

Our competitors may be effective in providing incentives to third parties to favor their products or services or to prevent or reduce subscriptions to our platform. In addition, third-party service providers may not perform as expected under our agreements or under their agreements with our merchants, and we or our merchants may in the future have disagreements or disputes with such providers. If we lose access to products or services from a particular supplier, or experience a significant disruption in the supply of products or services from a current supplier, especially a single-source supplier, it could have an adverse effect on our business and operating results.

Our future success depends, in part, on our ability to continue to attract and retain highly skilled personnel. Our ability to identify, hire, develop, motivate and retain qualified personnel will directly affect our ability to maintain and grow our business, and such efforts will require significant time, expense and attention. Our inability to attract or retain qualified personnel or delays in hiring required personnel may seriously harm our business, financial condition and operating results. Our ability to continue to attract and retain highly skilled personnel, specifically employees with technical and engineering skills and skills in emerging technologies such as AI, will be critical to our future success and the demand and competition for such specialized talent may be high. Our remote-first work model may negatively impact our ability to attract, train and retain talent.

Policing unauthorized use of our intellectual property and misappropriation of our technology and trade secrets is difficult and we may not always be aware of such unauthorized use or misappropriation. Despite our efforts to protect our intellectual property rights, unauthorized third parties may attempt to use, copy or otherwise obtain and market or distribute our intellectual property rights or technology or otherwise develop services with the same or similar functionality as our platform. If our competitors infringe, misappropriate or otherwise misuse our intellectual property rights and we are not adequately protected, or if our competitors are able to develop a platform with the same or similar functionality as ours without infringing our intellectual property, our competitive advantage and results of operations could be harmed. Litigation brought to protect and enforce our intellectual property rights could be costly, time consuming and distracting to management and could result in the impairment or loss of portions of our intellectual property. As a result, we may be aware of infringement by our competitors, but may choose not to bring litigation to enforce our intellectual property rights due to the cost, time and distraction of bringing such litigation.…

Our solutions incorporate and are dependent to a significant extent on the use and development of open source software and we intend to continue our use and development of open source software in the future. Such open source software is generally licensed by its authors or other third parties under open source licenses and is typically freely accessible, usable and modifiable. Pursuant to such open source licenses, we may be subject to certain conditions, including requirements that we offer our proprietary software that incorporates the open source software for no cost, that we make available source code for modifications or derivative works we create based upon, incorporating or using the open source software and that we license such modifications or derivative works under the terms of the particular open source license.…

Although we believe that we have complied with our obligations under the various applicable licenses for open source software, it is possible that we may not be aware of all instances where open source software has been incorporated into our proprietary software or used in connection with our solutions or our corresponding obligations under open source licenses. We rely on multiple software programmers to design our proprietary software and we cannot be certain that our programmers have not incorporated open source software into our proprietary software that we intend to maintain as confidential or that they will not do so in the future. To the extent that we are required to disclose the source code of certain of our proprietary software developments to third parties, including our competitors, in order to comply with applicable open source license terms, such disclosure could harm our intellectual property position, competitive position, results of operations and financial condition. In addition, to the extent that we have failed to comply with our obligations under particular licenses for open source software, we may lose the right to continue to use and exploit such open source software in connection with our operations and solutions, which could disrupt and adversely affect our business.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/parts/axes_9.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
