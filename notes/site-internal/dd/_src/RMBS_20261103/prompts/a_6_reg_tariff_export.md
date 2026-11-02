你是 stock-analyst v20 DD 的證據採集子 agent。標的：RMBS。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - RMBS Rambus tariff section 232 2026
  - Rambus export control OR entity list Semiconductors 2026
  - RMBS Rambus China tariff OR trade restriction 2026
  - Semiconductors tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-18）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/917273/000119312526057101/rmbs-20251231.htm｜as_of：2026-02-18
<<<
•Weak global economic conditions, including as a result of tariffs or trade restrictions and relationships, may adversely affect demand for the products and services of our customers and could otherwise harm our business.

•We are subject to various government restrictions and regulations, including on the sale of products and services that use encryption and other technology, those related to privacy, other consumer protection matters, other import/export controls and national security matters.

As a fabless semiconductor company, we purchase our inventory from third-party manufacturers in advance of selling our products. We place orders with our manufacturers based on existing and expected orders from our customers and distributors for particular products. We are also subject to increased inventory risks and costs because we build our products based on forecasts provided by our customers and distributors before receiving purchase orders for the product. While most of our contracts with our customers and distributors include lead time requirements and cancellation penalties that are designed to protect us from misalignment between orders and inventory levels, we must nonetheless make some predictions when we place orders with our manufacturers and we are not always able to make adjustments to align with our inventory needs. Our customers and distributors may also fail to place orders or cancel orders for many reasons, including but not limited to trends in the global economy, including as a result of tariffs or trade restrictions or relationships, business challenges, supply chain constraints, longer than expected inventory digestion or other changes in their business requirements. In the event that our predictions are inaccurate due to unexpected increases in orders or our manufacturers are unable to provide the inventory that we require, we may have insufficient inventory to meet our customers’ and distributors’ demands.…

Our business is dependent on distributors to service our end customers. We utilize distributors to sell our memory interface chips to certain customers. We do not have long-term purchase commitments from our distributors. If a key distributor were to experience financial difficulties, including bankruptcy, this could materially impact our financial results due to potential losses from uncollectible receivables. Additionally, any oversupply of inventory at our distributors, whether due to an industry or economic downturn or other causes, could result in reduced sales in a given period, increased order push-outs, increased inventory returns and cause us to carry higher levels of inventory. This could result in us incurring charges for obsolete or excess inventory, or we may not fully recover our costs, which would reduce our gross margin. Violations of the Foreign Corrupt Practices Act of 1977, as amended (the “FCPA”), export controls and sanction laws, or similar laws, by our distributors could also have a material adverse impact on our business.

Trade-related government actions, including changes in trade restrictions or relationships, tariffs and exchange controls, and potential retaliatory tariffs or actions by other countries, whether implemented by the United States, China, the European Union or other countries, that impose barriers or restrictions impacting our ability to sell or ship products to certain customers may have a negative impact on our financial condition and results of operations. We cannot predict the actions government entities 18 Table of Contents may take in this context and may be unable to quickly offset or effectively react to government actions that restrict our ability to sell to certain customers or in certain jurisdictions. Government actions that affect our customers’ ability to sell products or access critical elements of their supply chains may result in a decreased demand for their products, which may consequently reduce their demand for our products.

In addition, the U.S. government has implemented controls affecting the ability to send certain products and technology related to semiconductors, semiconductor manufacturing and supercomputing to China without an export license and added additional entities to restricted party lists in addition to other import/export and national security laws and regulations. We may be impacted by any of these current or new restrictions in the future if such controls are expanded to cover our key products/markets.

Our operations and performance depend significantly on worldwide economic conditions. Current and future uncertainty in the worldwide economy due to inflation, geopolitics, major central bank policies, including interest rate changes, public health crises or other global factors, could adversely affect our business. Additionally, there is ongoing uncertainty regarding the current U.S. presidential administration’s economic and other policies, priorities and actions, such as potential changes in trade restrictions or relationships, tariffs and exchange controls, and potential retaliatory tariffs or actions by other countries, which could impact our business and the cost and/or sale of our products in any countries that are impacted. Adverse economic conditions could also affect demand for our products and our customers’ products. If our customers experience reduced demand or excess inventory as a result of global or regional economic conditions or otherwise, including as a result of changes in tariffs or trade restrictions and relationships, this could result in reduced royalties revenue and/or product sales and our business and results of operations could be harmed.…

Semiconductor supply chain disruptions have been well publicized in the recent past. We believe that we could experience various supply constraints related to our memory interface chip business in the future. For example, to the extent we do not have sufficient wafer and packaging substrate firm commitments from our third-party suppliers or they are otherwise unable to provide such services and materials, we may not obtain the materials needed on our desired timelines or at reasonable prices. Large swings in demand could exceed our contracted supply and/or our suppliers’ capacity to meet those demand changes resulting in a shortage of parts, materials or capacity needed to manufacture our products. While we continually work with our suppliers to mitigate the impact of the supply constraints to our customer deliveries, in the event of a shortage or supply interruption from suppliers of our components, we may not be able to develop alternate sources quickly, cost-effectively or at all. An extended period of global supply chain and economic disruption, including as a result of tariffs or trade restrictions, could have a material negative impact on our business, results of operations, access to sources of liquidity and financial condition, though the full extent and duration is uncertain.

Additionally, various sources of supply-chain risk, including strikes or shutdowns at delivery ports or loss of or damage to our products while they are in transit or storage, IP theft, losses due to tampering, third-party vendor issues with quality or sourcing control, failure by our suppliers to comply with applicable laws and regulations, potential tariffs or other trade restrictions, geopolitical uncertainty and related military actions or other similar problems could limit or delay the supply of our products. Any interruption or delay in manufacturing or component supply, any increases in manufacturing or component costs, or the inability to obtain these services or components from alternate sources at acceptable prices and within a reasonable amount of time would harm our ability to provide our products to customers on a timely basis. This could harm our relationships with our customers, prevent us from acquiring new customers and materially and adversely affect our business.

Risks Associated with Litigation, Regulation and Our Intellectual Property We are subject to various government restrictions and regulations, including on the sale of products and services that use encryption and other technology, those related to privacy, other consumer protection matters, other import/export controls and national security matters.

Various countries have adopted controls, license requirements and restrictions on the export, import and use of products or services that contain encryption technology. In addition, governmental agencies have proposed additional requirements for encryption technology, such as requiring the escrow and governmental recovery of private encryption keys. Restrictions on the sale or distribution of products or services containing encryption technology may impact our ability to license data security technologies to the manufacturers and providers of such products and services in certain markets or may require us or our customers to make changes to the licensed data security technology that is embedded in such products to comply with such restrictions. Government restrictions, or changes to the products or services of our customers to comply with such restrictions, could delay or prevent the acceptance and use of such customers’ products and services. In addition, the United States and other countries have imposed export controls that prohibit the export of encryption and other technology to certain countries, entities and individuals. Our failure to comply with export and use regulations concerning encryption and other technology could subject us to sanctions and penalties, including fines, and suspension or revocation of export or import privileges.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
