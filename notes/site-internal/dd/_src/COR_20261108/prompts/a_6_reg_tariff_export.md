你是 stock-analyst v20 DD 的證據採集子 agent。標的：COR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[reg_tariff_export] 關稅／出口管制
Q: 本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？
  - COR Cencora tariff section 232 2026
  - Cencora export control OR entity list Medical Distribution 2026
  - COR Cencora China tariff OR trade restriction 2026
  - Medical Distribution tariff exposure supply chain 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm｜as_of：2025-11-25
<<<
Furthermore, geopolitical dynamics caused by changes or uncertainty in U.S. policies or the political, economic, social or other conditions or policies in foreign countries and regions in which we do business may impact or disrupt our business, as well as the operations of our customers, suppliers, service providers, or other third-party business partners. During fiscal 2025, we continued to experience increased costs, including for fuel, and it is possible that we could experience supply disruptions, shortages, or additional costs (including with respect to packaging, materials, and other equipment) resulting from U.S. tariffs or other protective measures. These tariffs and protective measures may include (i) the existing fentanyl tariffs, reciprocal tariffs, or secondary tariffs imposed on Indian or Brazilian-origin goods; (ii) the threatened tariffs on imports of pharmaceuticals and pharmaceutical ingredients under Section 232 of the Trade Expansion Act of 1962 (as amended); or (iii) additional tariffs imposed by the U.S. Executive Branch or Congress. We cannot predict how or when these tariffs may be implemented or modified. Moreover, other countries may impose counter-tariffs or measures that could impact our operations and pricing. The current environment relating to tariffs is highly dynamic, and tariff policies may be interrelated with other regulatory and foreign policy initiatives of the Executive Branch and/or Congress.

Significantly higher and sustained rates of inflation, with subsequent increases in operational costs, could have a material adverse effect on our business. The continued threat of terrorism and heightened security and military action in response thereto, or any other current or future acts of terrorism, war or other geopolitical developments (such as rising nationalism, the conflict in Ukraine, and evolving conditions in the Middle East), and other events (such as economic sanctions and trade restrictions) may cause further disruptions to the economies of the U.S. and other countries and create further uncertainties. Any disruption may inhibit our access to, or require us to spend more money to source, certain products that we use in our operations. Any of these factors could adversely affect our business.

The pharmaceutical products that we purchase are also subject to price inflation and deflation, as well as the threatened and enacted tariffs described above. Additionally, certain distribution service agreements that we have entered into with brand-name and generic pharmaceutical manufacturers have a price appreciation component to them. As a result, our gross profit from brand-name and generic pharmaceuticals continues to be subject to fluctuation based upon the timing and extent of manufacturer price increases, which we do not control. If the frequency or rate of brand-name and generic pharmaceutical price increases slows, whether due to regulatory mandates, the implementation of legislative proposals, policy initiatives or voluntary manufacturer actions, our results of operations could be adversely affected. In addition, generic pharmaceuticals are also subject to price deflation. If the frequency or rate of generic pharmaceutical price deflation accelerates, the negative impact on our results of operations would increase.

Statutory and/or regulatory violations could also form the basis for qui tam complaints. The qui tam provisions of the federal and various state civil False Claims Acts authorize a private person, known as a relator, to file civil actions under these statutes on behalf of the federal and state governments. Under False Claims Acts, the filing of a qui tam complaint by a relator imposes obligations on government authorities to investigate the allegations and determine whether to intervene in the action. Such cases may involve allegations around the marketing, sale, purchase, and/or dispensing of brand-name and/or generic pharmaceutical products, the provision of services to the pharmaceutical industry, or misrepresentations on documents filed with U.S. Customs and Border Protection that results in the underpayment of duties and tariffs. Qui tam complaints are filed under seal and remain sealed until the applicable court orders otherwise. Our business and results of operations could be adversely affected if qui tam complaints are filed against us for alleged violations of any health or customs laws and regulations and damages arising from resultant false claims, if the litigation proceeds whether government authorities decide to intervene in any such matters, and/or if we are found liable for all or any portion of violations alleged in any such matters.

We are subject to laws concerning our business operations and marketing activities in foreign countries where we conduct business. For example, we are subject to the U.S. Foreign Corrupt Practices Act (the “FCPA”), U.S. export control and trade sanction laws, and similar anti-corruption and international trade laws in certain foreign countries, such as the U.K. Bribery Act, any violation of which could create substantial liability for us and also cause a loss of reputation in the market. We may also have substantial liability if a third party acting on our behalf or on the behalf of our subsidiaries (including our joint venture partners) is in violation of these laws. In connection with our acquisitions, our results of operations and financial position may be adversely affected if we are not able to put in place effective financial controls and compliance policies to safeguard against risks of violating the FCPA or other anti-corruption and international trade laws as part of our integration of acquired businesses. If we are found to have violated the FCPA, we may face sanctions including civil and criminal fines, disgorgement of profits, and suspension or debarment of our ability to contract with government agencies or receive export licenses.…

We have been and may in the future be adversely affected by events outside of our control, including: widespread public health issues, such as infectious diseases; natural disasters and other catastrophic events such as earthquakes, floods, or severe weather, including as a result of climate change; government policy changes; and political events such as terrorism, political tensions, military conflicts, civil unrest, sanctions, tariffs or other trade restrictions, and trade wars. These events can disrupt operations for us, our suppliers, our service providers, and our customers, as well as impair product manufacturing, supply, and transport availability and cost in unpredictable ways that depend on highly uncertain future developments. They might affect consumer confidence levels and spending or the availability of certain goods or commodities. In response to these types of events, we might suspend operations, implement extraordinary procedures, incur increased costs, or seek alternate sources for product supply, or suffer consequences that are unexpected and difficult to mitigate. Any of these risks might have a material adverse impact on the Company.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/parts/axes_6.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
