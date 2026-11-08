你是 stock-analyst v20 DD 的證據採集子 agent。標的：LEU。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - LEU Centrus Energy tariff section 232 2026
  - Centrus Energy export control OR entity list Uranium 2026
  - LEU Centrus Energy China tariff OR trade restriction 2026
  - Uranium tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm｜as_of：2026-02-11
<<<
The war in Ukraine escalated tensions between Russia and the international community. As a result, the United States and other countries imposed, including through the United States’ enactment of the Import Ban Act discussed below, and may continue imposing, additional sanctions, tariffs, and export controls against certain Russian products, services, organizations and/or individuals, and Russia passed the Russian Decree as discussed below. Such additional restrictions, and Russian response thereto, could affect our ability to purchase, take delivery of, transport, or re-sell Russian uranium enrichment, engage in transactions with TENEX, or implement the TENEX Supply Contract, which would have a negative material impact on our business. Refer to Part I, Item 1, Business -Competition and Foreign Trade - War in Ukraine and Part I, Item 1A, Risk Factors - Economic and Industry Risks - Dependence on our largest customers or suppliers could adversely affect us, for further discussion.

19 Ukraine War The war in Ukraine escalated tensions between Russia and the international community. As a result, the United States and other countries imposed, including through the United States’ enactment of the Import Ban Act discussed below, and may continue imposing, additional sanctions, tariffs, and export controls against certain Russian products, services, organizations and/or individuals, and Russia passed the Russian Decree as discussed below. Such additional restrictions, and any Russian response thereto, could affect our ability to purchase, take delivery of, transport, or re-sell Russian uranium enrichment, engage in transactions with TENEX, or implement the TENEX Supply Contract, which would have a negative material impact on our business. Further, tariffs, sanctions or other restrictions by the United States, Russia or other countries may impact our ability and the cost to transport, export, import, deliver, take delivery, or make payments related to the LEU we purchase and may require us to increase purchases from non-Russian sources to the extent available. For example, due to restrictions imposed by Canada on the ability of Canadian persons and entities to provide ocean transportation services to Russia, a permit is required for our shipper, a Canadian company, to transport the LEU that we procure under the TENEX Supply Contract to the United States.…
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm｜as_of：2026-02-11
<<<
Risks related to the war in Ukraine factors primarily include: •the current war in Ukraine and related international sanctions and restrictions; •market and supply chain complications arising from the Import Ban Act, and the Russian Decree; and •financial losses we incur in connection with (i) the impact of government sanctions and tariffs imposed in response to the invasion of Ukraine and/or (ii) disputes with our counterparties arising from such sanctions or mitigation efforts.

Further, sanctions, tariffs or restrictions by the United States, Russia, or other countries on goods and services needed to make imports may directly or indirectly impact performance of the TENEX Supply Contract and our ability to transport, import, take delivery of or make payments or deliveries related to the LEU we purchase. For example, as a result of restrictions imposed by Canada on the ability of Canadian persons and entities to provide ocean transportation services to Russia, a permit is required for our shipper, a Canadian company, to transport the LEU that we procure under the TENEX Supply Contract to the United States. A Canadian permit issued to our shipper was extended to March 2027, but for so long as the sanctions remain in place, the shipper will require further extensions beyond the current validity of the permit for continued shipments of LEU imports. Furthermore, because sanctions also limit the types of non-nuclear cargo that the ocean carrier can ship to and from Russia, its overall business in Russia has been curtailed, so this reduced the number of ships it uses for transportation to and from Russia, making it more difficult for us to make timely deliveries of LEU.…

Additional sanctions, tariffs or other measures could be imposed by the U.S. or foreign governments (including the Russian government) in the future. For example, there is draft legislation in the U.S. Congress designed to impose potentially significant tariffs on Russian goods and/or sanctions on Rosatom that would effectively prohibit (again, subject to government-issued waivers) transactions with TENEX, a subsidiary of Rosatom. Since the enactment of the Import Ban Act, TENEX continued to implement the TENEX Supply Contract while we pursue waivers from the DOE. With the issuance of the Russian Decree, TENEX began to seek the necessary export licenses and has received three licenses to date. However, we do not know what actions TENEX might take in response to new sanctions or government actions, including the Russian Decree, but if it refused, or was unable or prohibited to make future deliveries, such refusal or its inability would likely affect our ability to meet our delivery obligations to our customers and would have a material adverse effect on the Company and its financial condition.

There have recently been significant changes to international trade policies and tariffs affecting imports and exports. The U.S. has implemented a range of new tariffs and increases to existing tariffs, and, in response to the tariffs announced by the U.S., other countries have imposed new or increased tariffs on certain exports from the United States. There is currently significant uncertainty about the future relationship between the United States and other countries with respect to trade policies, government regulations and tariffs. We cannot predict whether, and to what extent, current tariffs will continue, or trade policies will change in the future.

On September 8, 2025, the U.S. officially removed import tariffs on uranium as part of a broader executive order aimed at strengthening domestic supply chains and supporting strategic industries. However, there is draft legislation in the U.S. Congress designed to impose potentially significant tariffs on Russian goods. These developments are ongoing and are subject to change, including the imposition of additional tariffs and retaliatory measures by these and other countries. Depending on their extent, scope and duration, these tariffs and retaliatory measures may result in increased costs for any equipment and other goods we require to operate and develop our projects in accordance with our current plans. At the same time, it is possible that these tariffs and other measures may benefit certain aspects of our business, including by increasing demand for uranium produced in the U.S. Although discussions continue regarding potential economic arrangements between certain countries, there remains significant uncertainty over the scope, impact and duration of any tariffs and retaliatory measures, and they may, among other things, adversely impact general economic conditions, including the market and demand for uranium and our business financial condition and results of operations. For further discussion of these risks and uncertainties, refer to Part I, Item 1A, Risk Factors - The current war in Ukraine and related international or U.S.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-11）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1065059/000162828026007117/leu-20251231.htm｜as_of：2026-02-11
<<<
61 The war in Ukraine has escalated tensions between Russia and the international community. As a result, the United States and other countries imposed, including through the U.S.’s enactment of the Import Ban Act discussed below, and may continue imposing, additional sanctions, tariffs, and export controls against certain Russian products, services, organizations and/or individuals, and Russia passed the Russian Decree as discussed below. Such additional restrictions, and any Russian response thereto, could affect our ability to purchase, take delivery of, transport, or re-sell Russian uranium enrichment, engage in transactions with TENEX, or implement the TENEX Supply Contract, which would have a negative material impact on our business. Further, tariffs or sanctions by the United States, Russia or other countries may impact our ability and the cost to transport, export, import, take delivery, or make payments related to the LEU we purchase and may require us to increase purchases from non-Russian sources to the extent available. For example, due to restrictions imposed by Canada on the ability of Canadian persons and entities to provide ocean transportation services to Russia, a permit is required for our shipper, a Canadian company, to transport the LEU that we procure under the TENEX Supply Contract to the United States.…

62 On April 15, 2025, the President of the United States signed Executive Order 14272 initiating a U.S. Department of Commerce investigation under Section 232 of the Trade Expansion Act of 1962, to determine whether imports of processed critical minerals, including uranium, and their derivative products threaten to impair national security. Following the investigation, on January 14, 2026, the President issued Proclamation 11001, which directed the Secretary of Commerce and the United States Trade Representative (“USTR”) to pursue negotiations with trading partners over the next 180 days to ensure the United States maintains adequate supplies of critical minerals while mitigating supply-chain vulnerabilities affecting processed critical minerals and their derivative products. Proclamation 11001 indicated that, depending on the status or outcome of those negotiations, alternative remedies may be considered in the future, including the imposition of an additional sectoral tariff. The imposition of new or increased tariffs on these products or other trade restrictions from our international suppliers could significantly increase our costs and have a material adverse effect on our financial position and results of operations.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
