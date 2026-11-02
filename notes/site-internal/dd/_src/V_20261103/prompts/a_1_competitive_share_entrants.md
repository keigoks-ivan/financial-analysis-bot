你是 stock-analyst v20 DD 的證據採集子 agent。標的：V。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - V Visa market share gaining OR losing 2026
  - Visa new entrant OR displace threat Credit Services 2026
  - V competitor design win 2026
  - Visa vs Credit Services peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-06）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm｜as_of：2025-11-06
<<<
COMPETITION The global payments industry continues to undergo dynamic and rapid change. Existing and emerging competitors compete with Visa’s network and payment solutions for consumers and for participation by financial institutions and sellers. Technology and innovation are shifting consumer habits and driving growth opportunities in ecommerce, GenAI agent-based commerce, mobile payments, blockchain technology and digital currencies, including stablecoins. These advances are enabling new entrants, many of which depart from traditional network payment models. In certain countries, the evolving regulatory landscape is creating local networks or enabling additional processing competition.

We compete against all forms of payment. These include paper-based payments, primarily cash and checks, and all forms of electronic payments. Our electronic payment competitors principally include the ones listed below.

Global or Multi-regional Networks: These networks typically offer a range of branded, general purpose card payment products that consumers can use at millions of merchant locations around the world. Examples include American Express, Diners Club/Discover (now owned by Capital One), JCB, Mastercard and UnionPay. These competitors may be more concentrated in specific geographic regions, such as Discover in the U.S. and JCB in Japan, or have a leading position in certain countries, such as UnionPay in China. See Item 1A—Regulatory Risks—Government-imposed obligations and/or restrictions on international payments systems may prevent us from competing against providers in certain countries, including significant markets such as China and India. Based on available data, Visa is one of the largest retail electronic funds transfer networks used throughout the world.

RTP Networks: RTP networks have launched in at least 80 countries and continue to be driven by strong government sponsorship and regulatory initiatives to enable and drive adoption (e.g., FedNow in the U.S., PIX in Brazil and United Payments Interface (UPI) in India), increasing their position as an alternative to payment card schemes. These networks primarily focus on domestic transactions, with adoption varying by use cases and geographies. However, with linkages such as PayNow in Singapore and UPI in India, cross-border RTP networks are advancing and will compete with our cross-border business. RTP networks can compete with Visa on consumer payments and other payment flows (e.g., B2B and P2P) but can also be customers for value-added services, such as risk management.

Payment Processors: Payment processors may perform processing services on third-party payments networks on behalf of issuers or acquirers. We compete with payment processors for the processing of Visa transactions. These processors may benefit from mandates requiring them to handle processing under local regulation. For example, as a result of the Interchange Fee Regulation (IFR) in Europe, we may face competition from other networks, processors and other third parties who could process Visa transactions directly with issuers and acquirers.

CMS Providers: We compete with alternative solutions to our CMS (e.g., Visa Direct) such as ACH, RTP and wires. We compete with other global and local card networks for commercial card portfolios. Additionally, we may face competition from industry players who are experimenting with B2B blockchain payments, including stablecoins, which are gaining regulatory clarity, can operate globally 24/7, and have the capability to support cross-border transactions.

Value-Added Service Providers: We face competition from companies that provide alternatives to our value-added services. These include a wide range of players, such as technology companies, information services and consulting firms, governments and merchant services companies. The integration of technology like GenAI can create new and better offerings that compete with our value-added services, such as strengthened risk monitoring and managing digital identification. Regulatory initiatives could also lead to increased competition in these areas.

19 Table of Contents There are several EU regulations that impact our business. As discussed above, the IFR regulates interchange rates within the EEA, requires Visa Europe to separate its payment card scheme activities from processing activities for accounting, organization and decision-making purposes within the EEA, and imposes limitations on network exclusivity and routing. National competent authorities in the EEA are responsible for monitoring and enforcing the IFR in their markets. We are also subject to regulations governing areas such as privacy and data protection, anti-bribery, anti-money laundering, anti-terrorism and sanctions. Other regulations in Europe, such as the second Payment Services Directive (PSD2), require, among other things, that our financial institution clients provide certain customer account access rights to emerging non-financial institution players. PSD2 also includes strong customer authentication requirements for certain transactions that could impose both operational complexity on Visa and impact consumer payment experiences. Visa Europe is also subject to supervisory oversight by the European Central Bank and certain competent authorities in Europe.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2025-11-06）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm｜as_of：2025-11-06
<<<
Regulators around the world have been establishing or increasing their authority to regulate various aspects of the payments industry. See Item 1—Government Regulation for more information. In the U.S. and many other jurisdictions, we have historically set default IRFs. Even though we generally do not receive any revenue related to IRFs in a payment transaction (in the context of credit and debit transactions, those fees are paid by the acquirers to the issuers; the reverse is true for certain transactions like ATM transactions), IRFs are a factor on which we compete with other payments providers and are therefore an important determinant of the volume of transactions we process. Consequently, changes to these fees, whether voluntarily or by mandate, can substantially affect our overall payments volume and net revenue.

Governments in a number of jurisdictions shield domestic payments providers, including card networks, brands, and processors, from international competition by imposing market access barriers and preferential domestic regulations. To varying degrees, these policies and regulations affect the terms of competition in the marketplace and impair the ability of international payments networks to compete. Public authorities may also impose regulatory requirements that favor domestic providers or mandate that domestic payments or data processing be performed entirely within that country, which could prevent us from managing the end-to-end processing of certain transactions.

UnionPay has grown rapidly in China and is actively pursuing international expansion plans, which could potentially lead to regulatory pressures on our international routing rule (which requires that international transactions on Visa cards be routed over VisaNet). Furthermore, although regulatory barriers shield UnionPay from competition in China, alternative payments providers such as Alipay and WeChat Pay have rapidly expanded into ecommerce, offline and cross-border payments, which could make it difficult for us to compete even if our license is approved in China. NetsUnion Clearing Corp, a Chinese digital transaction routing system, and other such systems could have a competitive advantage in comparison with international payments networks.

Business Risks We face intense competition in our industry. The global payments space is intensely competitive. As technology evolves and consumer expectations change, new competitors or methods of payment emerge, and existing clients and competitors assume different roles. Our products compete with cash, checks, electronic payments, virtual currency payments, global or multi-regional networks, other domestic and closed-loop payments systems, digital wallets and alternative payments providers primarily focused on enabling payments through ecommerce and mobile channels. As the global payments space becomes more complex, we face increasing competition from our clients, other emerging payment providers such as fintechs, other digital payments, technology companies that have developed payments systems enabled through online activity in ecommerce, social media, and mobile channels, other providers of CMS and VAS offerings, as well as governments in a number of jurisdictions (e.g., U.S., Brazil and India), that are developing, supporting and/or operating national schemes, RTP networks and other payment platforms. For more information, please see Item 1—Competition above.

Our competitors may acquire, develop or make better use of substantially better technology, have more widely adopted delivery channels, or have greater financial resources. They may offer more effective, innovative or a wider range of programs, products and services. They may use more effective advertising and marketing strategies that result in broader brand recognition and greater use, including with respect to issuance and seller acceptance. They may also develop better solutions or offer more favorable pricing. Moreover, even if we successfully adapt to technological change and the proliferation of alternative types of payment services by developing and offering our own services in these areas, such services may provide less favorable financial terms for us, which could hurt our financial results. We expect to face more competition as AI continues to advance and GenAI and agentic AI capabilities become integrated into payments and related services in two main ways: first, by competitors successfully enhancing their products, services and external offerings with AI to achieve greater and faster product adoption; and second, by competitors providing internal AI tools to upskill their employees for greater operational efficiencies and impact.…
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/V_20261103/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
