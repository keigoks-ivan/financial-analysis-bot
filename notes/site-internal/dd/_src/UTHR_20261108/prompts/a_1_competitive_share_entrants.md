你是 stock-analyst v20 DD 的證據採集子 agent。標的：UTHR。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[competitive_share_entrants] 競爭份額／新進入者
Q: 本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？
  - UTHR United Therapeutics market share gaining OR losing 2026
  - United Therapeutics new entrant OR displace threat Drug Manufacturers - Specialty & Generic 2026
  - UTHR competitor design win 2026
  - United Therapeutics vs Drug Manufacturers - Specialty & Generic peers market share trend 2025 2026


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

[1] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1. Business｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
We also face competition from manufacturers of generic versions of Remodulin in the United States and abroad. See the section below entitled Patents and Other Proprietary Rights, Strategic Licenses, and Market Exclusivity—Generic Competition and Challenges to our Intellectual Property Rights.

Generic Competition and Challenges to our Intellectual Property Rights Remodulin—Generic Competition We settled litigation with Sandoz Inc. (Sandoz) related to its abbreviated new drug application (ANDA) seeking FDA approval to market a generic version of Remodulin and in March 2019, Sandoz announced the availability of its generic product in the United States. We have also entered into similar settlement agreements with other generic companies, some of which have also launched sales of generic versions of Remodulin. Through December 31, 2025, we have seen limited erosion of Remodulin sales as a result of generic treprostinil competition in the United States. We are currently engaged in litigation with 2025 Annual Report 15 Sandoz and its marketing partner, RareGen, LLC (RareGen) (now a subsidiary of Liquidia Corporation, the parent company of Liquidia Technologies, Inc. (Liquidia)), related to the infusion devices used to administer Remodulin subcutaneously. We understand that generic treprostinil was initially launched by Sandoz/RareGen for use only by intravenous infusion. In May 2021, Sandoz/Liquidia Corporation announced that Sandoz’s generic treprostinil was made available for subcutaneous use, following FDA clearance of a cartridge that can administer the product via the MS-3 pump. In addition, Liquidia has announced it is developing a new subcutaneous infusion system for its generic treprostinil product.…

General We intend to vigorously enforce our intellectual property rights related to our products. However, we may not prevail in defending our patent rights, and additional challenges from other ANDA filers or other challengers may surface with respect to our products. Our patents could be invalidated, found unenforceable, or found not to cover one or more generic forms of our products. If any ANDA filer or filer of a 505(b)(2) NDA for a branded treprostinil product were to receive approval to sell its treprostinil product and/or prevail in any patent litigation, our affected product(s) would become subject to increased competition. Patent expiration, patent litigation, and competition from generic or other branded treprostinil manufacturers could have a significant, adverse impact on our treprostinil-based product revenues, our profits, and our stock price. These potential effects are inherently difficult to predict. For additional discussion, see the risk factor entitled, Our intellectual property rights may not effectively deter competitors from developing competing products that, if successful, could have a material adverse effect on our revenues and profits, contained in Part I, Item 1A—Risk Factors included in this Report.

Competition Many drug companies engage in research, development, and commercialization of products to treat cardiopulmonary diseases, pulmonary diseases, and cancer. For the treatment of PAH, we compete with many approved products in the United States and the rest of the world. In the U.S., these competitive therapies include oral ERAs (Letairis® (ambrisentan), Opsumit® (macitentan), Tracleer® (bosentan), generic bosentan, and generic ambrisentan); prostacyclin-class therapies Uptravi® (oral selexipag), Veletri® (intravenous epoprostenol), Ventavis® (inhaled iloprost), Yutrepia® (treprostinil inhalation powder), generic intravenous epoprostenol, and generic treprostinil injection; PDE-5 inhibitors (Revatio® (sildenafil), generic sildenafil, and generic tadalafil); an SGC stimulator Adempas® (riociguat); an activin pathway inhibitor Winrevair (sotatercept-csrk) delivered via subcutaneous injection; and an oral combination product known as Opsynvi®, comprised of tadalafil and macitentan. Some of these therapies are manufactured and marketed by large pharmaceutical companies such as Johnson & Johnson, Gilead Sciences, Inc., Bayer Schering Pharma AG, GSK plc, and Merck, as well as a variety of large generic drug manufacturers. In the fourth quarter of 2025, the manufacturer of Flolan® (intravenous epoprostenol) discontinued manufacture of the product.

Orenitram faces direct competition from Uptravi, which is indicated to delay disease progression and reduce the risk of hospitalization for PAH, and will compete with a generic version of Uptravi which is expected to launch in 2026. Orenitram’s initial indication was limited to the improvement of exercise capacity, which may have led physicians to prescribe Uptravi instead of Orenitram. However, Uptravi is an oral IP prostacyclin receptor agonist. While prostacyclin analogues such as Orenitram broadly mimic the effect of prostacyclin, IP prostacyclin receptor agonists bind selectively to the IP receptor, one of several prostacyclin receptors. Given the progressive nature of PAH, many patients initiate Orenitram or another one of our treprostinil-based therapies after their disease progresses while taking Uptravi. In August 2018, we announced the results of our FREEDOM-EV clinical study, which demonstrated that Orenitram delays time to clinical worsening, demonstrated improvement across key clinical measures, and, at study closure, indicated a positive impact on survival rates. In October 2019, the FDA approved a supplement to our Orenitram NDA expanding the Orenitram label to indicate that it also delays disease progression, in addition to improving exercise capacity. We believe that these clinical results and updated labeling have resulted in increased use of Orenitram. We are developing a next-generation IP receptor agonist called ralinepag, for PAH.…

We have faced generic competition for Adcirca since the launch of generic tadalafil in the United States in August 2018, which has significantly reduced our Adcirca revenues. We have also faced generic competition for Remodulin in the United States and certain European countries since 2019. Finally, we have entered into settlement agreements with Actavis and ANI permitting them to launch generic versions of Orenitram in the United States in June 2027 and December 2027, respectively, or earlier under certain circumstances. We have also entered into a settlement agreement with Watson permitting it to launch a generic version of Nebulized Tyvaso in the United States as early as January 2026, although to date Watson has not received FDA approval to do so. For details regarding these and other potential generic competitors, see the section above entitled Patents and Other Proprietary Rights, Strategic Licenses, and Market Exclusivity—Generic Competition and Challenges to our Intellectual Property Rights.

We compete with the developers, manufacturers, and distributors of all of the products noted above for customers, funding, access to licenses, personnel, third-party collaborators, product development, and commercialization. Some of these companies have substantially greater financial, marketing, sales, distribution and technical resources, and more experience in research and development, product development, manufacturing and marketing, clinical trials, and regulatory matters, than we have.
>>>

[2] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 1A. Risk Factors｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
Competition could negatively impact our operating results. We compete with well-established drug companies for market share, as well as, among other things, funding, licenses, expertise, personnel, clinical trial patients and investigators, consultants, and third-party collaborators. Some of these competitors have substantially greater financial, marketing, manufacturing, sales, distribution, and technical resources, and a larger number of approved products, than we do. Some of these competitors also possess greater experience in areas critical to our success, such as research and development, clinical trials, sales and marketing, and regulatory matters.

Numerous treatments compete with our commercial therapies. For example, for the treatment of PAH, we compete with over fifteen branded and generic drugs. Sales of a generic version of Adcirca launched in August 2018 have had a material adverse impact on our sales of Adcirca. The availability of generic treprostinil injection in the United States could materially impact our revenues, and generic competition materially impacted our Remodulin revenues outside the United States. Our 32 United Therapeutics, a public benefit corporation competitors are also developing numerous new products that may compete with ours, including products intended to treat PAH and/or PH-ILD. For example, Merck commercially launched Winrevair (sotatercept-csrk) in the United States in March 2024, which competes with our treprostinil-based products. In addition, in June 2025 Liquidia launched U.S. sales of Yutrepia for PAH and PH-ILD, which now competes with our treprostinil-based products. Additional treatments, such as Insmed Incorporated’s TPIP, are in late-stage clinical trials for treatment of PAH and/or PH-ILD. Each of these products could potentially materially adversely affect our revenues. There are also three therapies approved for the treatment of IPF, including Boehringer Ingelheim’s Jascayd® (nerandomilast), which was approved by FDA in October 2025 for IPF, and later for PPF. A wide variety of additional therapies are being developed by our competitors for the treatment of IPF.…
>>>

[3] 來源：SEC EDGAR｜文件：10-K（FY2025，申報 2026-02-25）｜章節：Item 7. MD&A｜url：https://www.sec.gov/Archives/edgar/data/1082554/000108255426000006/uthr-20251231.htm｜as_of：2026-02-25
<<<
We operate in a highly competitive market in which several large pharmaceutical companies control many of the available PAH therapies, including Merck, which received FDA approval for Winrevair (sotatercept-csrk) to treat PAH in March 2024. These pharmaceutical companies are well established in the market and possess greater financial, technical, and marketing resources than we do. In addition, Yutrepia was approved by the FDA in May 2025 for treatment of PAH and PH-ILD, and the product was launched commercially in June 2025. While we have not seen a material impact on our net revenues as a result of Winrevair or Yutrepia’s launch to date, our net revenues could be materially impacted if either or both of these products gain significant market share or cause material price erosion for our existing products.
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

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/parts/axes_1.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
