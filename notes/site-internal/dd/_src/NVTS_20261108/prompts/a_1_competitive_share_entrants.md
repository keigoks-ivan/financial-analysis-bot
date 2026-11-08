你是 stock-analyst v20 DD 的證據採集子 agent。標的：NVTS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - NVTS Navitas Semiconductor market share gaining OR losing 2026
  - Navitas Semiconductor new entrant OR displace threat Semiconductors 2026
  - NVTS competitor design win 2026
  - Navitas Semiconductor vs Semiconductors peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm｜as_of：2026-02-27
<<<
Competitive Advantages Our status as one of the only pure-play next-generation high-power semiconductor companies positioned at the intersection of AI data center growth and grid modernization provides us with significant competitive advantages as we pursue emerging high-power markets.

Navitas is one of the very few suppliers offering a full spectrum of GaN and high-voltage SiC products and solutions to support impending shifts in power architecture driven by AI computing and grid modernization. This dual-capability is strategically and competitively significant because it allows us to address the full range of high-power use cases and challenges. GaN excels in medium-voltage, high-frequency, high-density power conversion while SiC dominates in high- and ultra-high-voltage, high-power systems. Whereas many of our competitors specialize in one or the other, we are a full-stack next-generation power semiconductor provider of both GaN and high-voltage SiC devices, allowing system-level optimization across voltage tiers.

We believe that Navitas has one of the broadest intellectual property portfolios in the power semiconductor industry, giving us a competitive advantage against both incumbent competitors and new market entrants. We possess a patent portfolio consisting of over 300 patents, issued or pending worldwide, that encompass fundamental aspects of both GaN 8 TABLE OF CONTENTS and SiC technology. The competitive value of our patent portfolio was validated in October 2024 when we entered into a broad patent cross-license with Infineon Technologies AG.

Finally, we believe that our capital efficiency and financial strength gives us a competitive advantage in our markets. By adopting a fabless manufacturing model, we are able to scale faster with a lower fixed-cost burden than our vertically integrated peers. Similarly, with no debt and a strong balance sheet, we have the ability and optionality to quickly allocate capital towards new opportunities and high-value programs. At Navitas, “speed of execution” is a core value and we believe it gives us a competitive advantage.

Competition Our competitors include suppliers of silicon-based as well as GaN-based and SiC-based power semiconductors. Our competitors include both global semiconductor companies with diversified product portfolios and smaller semiconductor companies with a narrow product or market focus. Similarly, our competitors include companies that outsource manufacturing and foundry services like we do, as well as those that are vertically integrated. Many of our competitors have significantly greater financial resources than we do, meaning they are better positioned to weather adverse market conditions or make opportunistic acquisitions. Most suppliers of GaN-based devices today offer discrete (i.e., non-integrated) GaN solutions, which require silicon-based and other components for drive, control and protection. These solutions, even though they offer some benefits compared to silicon, still do not capture all the advantages of a GaN integrated power IC that Navitas provides. Our primary GaN competitors include Infineon Technologies AG, Power Integrations, Inc., Texas Instruments Incorporated, Innoscience (Suzhou) Semiconductor Co., Ltd., Renesas Electronics Corp., and Efficient Power Conversion Corporation (EPC). Our primary SiC competitors include Infineon, Wolfspeed, Inc., ON Semiconductor Corporation, ROHM Co., Ltd., Qorvo, Inc., and STMicroelectronics International N.V. Our primary silicon-based power semiconductor competitors include Infineon, STMicroelectronics, ON Semiconductor and 10 TABLE OF CONTENTS Power Integrations, among others.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm｜as_of：2026-02-27
<<<
Our products are based on novel design technology and our future success depends on the successful development of high-voltage power switching components and systems based on design technology. In addition, as we prioritize high-power markets and applications, the importance of reliability and safety will add complexity to our product development process. There can be no assurance that any development problems we experience in the future related to our products will not cause significant delays or unanticipated costs, or that such development problems can be solved. In addition, we compete in a dynamic environment characterized by rapid technology and product evolution and robust competition. Our end customers are constantly seeking new products with more features and functionality at lower cost and with greater reliability, and our success relies heavily on our ability to continue to develop and market to our end customers new and 17 TABLE OF CONTENTS innovative products and improvements of existing products. Our failure to timely develop new technologies or to react quickly to changes in new or existing technologies could materially delay our development of new products, which could result in product obsolescence, decreased revenue, and/or a loss of market share to competitors.…

As we prioritize high-power markets and applications, it becomes crucial that we accurately anticipate and respond to technological shifts and market demands, and to timely develop new or enhanced products or technologies in response to the same. Our failure to do so could result in decreased revenue and the loss of our design wins to our competitors. Due to the interdependence of various components in the systems within which our products and the products of our competitors operate, end customers are unlikely to change to another design, once adopted, until the next generation of a technology. As a result, if we fail to introduce new or enhanced products that meet the needs of our end customers or penetrate new markets in a timely fashion, and our designs do not gain acceptance, we will lose market share and our competitive position.

•Unpredictable Competitive Dynamics: To the extent new and emerging products and technologies reshape or create new market landscapes, the competitive environment may evolve in unexpected ways. For example, new competitors may emerge, or traditional competitors with established R&D and manufacturing resources, and long-standing customer relationships, may choose to offer competitive GaN or high-voltage SiC solutions.

For example, historically, we have relied on TSMC as our sole supplier of GaN wafers, a key component in our product offerings. On July 1, 2025, TSMC announced its intention to cease GaN production in July 2027. We have taken proactive steps to mitigate this risk, including committing to purchase buffer inventory from TSMC, expanding our collaboration 20 TABLE OF CONTENTS with Powerchip Semiconductor Manufacturing Corporation and in November 2025, we announced a long-term strategic partnership with GlobalFoundries to develop and deliver advanced GaN solutions for critical applications in high power markets, including AI datacenters, energy and grid infrastructure, performance computing and industrial electrification. Despite these mitigation steps, there is no assurance that we will be able to successfully source sufficient quality or volume of GaN wafers at a cost or on a timeline that meets our requirements. We may not be able to purchase a sufficient quantity of buffer inventory from TSMC, or we may incur substantial costs in doing so and end with excess inventory that must be scrapped. Any delays or disruptions in qualifying or ramping production with Powerchip or GlobalFoundries, or other alternative suppliers, could negatively impact our ability to fulfill customer orders, lead to increased costs, or cause a loss of revenue and market share.…

Proprietary trade secrets and unpatented know-how are also very important to our business. We rely on trade secrets to protect certain aspects of our technology, especially where we do not believe that patent protection is appropriate or obtainable. However, trade secrets can be difficult to protect. Our employees, consultants, contractors, outside collaborators and other advisors may unintentionally or willfully disclose our confidential information to competitors, and confidentiality agreements may not provide an adequate remedy in the event of unauthorized disclosure of confidential or proprietary information. Enforcing a claim that a third party illegally obtained and is using our trade secrets may be expensive and time consuming. Moreover, our competitors may independently develop equivalent knowledge, methods and know-how. Failure to obtain or maintain trade secret protection could adversely affect our competitive business position.
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-27）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm｜as_of：2026-02-27
<<<
Our revenues fluctuate in response to a combination of factors. In addition, our revenues may fluctuate in response to the Company’s announced transition to high-power markets. Some of the factors that may cause these revenue fluctuations include the following: •our overall product mix and sales volumes; •gains and losses in market share and design win traction, including the Company’s ability to ramp new high-power products; •pace at which technology is adopted in our end markets; •the stage of our products in their respective life cycles; •the effects of competition and competitive pricing strategies, particularly in the mobile and consumer markets impacted by our announced transition to high-power markets; •availability of specialized field application engineering resources supporting demand creation and end customer adoption of new products; •achieving acceptable yields and obtaining adequate production capacity from our wafer foundries and assembly and test subcontractors; •market acceptance of our end customers’ products; governmental regulations influencing our markets; and •the global and regional economic cycles; •declines in average selling prices due product advances and market competition; •the availability, and fluctuations in the price of, the raw materials required for our products •changes in customer and distributor relationships including the Company’s announced consolidation of its distribution network in connection with its transition to high-power markets; and 38 TABLE OF CONTENTS •seasonal demand patterns in certain…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVTS_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
