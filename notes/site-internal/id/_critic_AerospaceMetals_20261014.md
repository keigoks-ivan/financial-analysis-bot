# Cold review：ID_AerospaceMetals_20261014（skill v4.1，id2 管線）

審稿日 2026-10-14。依 id-review 【ID v4 Mode】J1–J10，只讀 excerpt、check_report，以及 evidence.json、dd-screener latest.json、姊妹 ID 的 id-meta 做定點查證。WebSearch 共用 7 輪。

## 裁決

**需改後再發布。** 「短缺 × 第二階段、等回調、盯積壓」這個方向撐得住。但是支撐「已定價高」與「信心低」的核心數字，用的是過期快照。另有一個領先指標的現值落後一季，且第一頁的財報日期寫錯。三項都在第一頁或 id-meta 上。

| 級別 | 數量 | 項目 |
|---|---|---|
| 🔴 | 3 | A 估值倍數與分位過期（J3/J6）；B Airbus 交付現值落後一季（J3/J6/J7）；C ATI 財報日錯（J3） |
| 🟡 | 7 | 見下 |
| 🟢 | 2 | J1、J4 |

## 🔴

### A. HWM、CRS 的倍數與 5Y 分位是 DD 日快照，與文中現價不同期（J3、J6）

錯誤文字：
- 第一頁與 id-meta：「不追 HWM（Fwd P/E 45.5、5Y 分位 88）」「已定價 高｜HWM 分位 88、CRS 40」。
- 信心段：「HWM 分位仍 88，不足以抵銷 7/24 的勝率」。
- 分歧 2：「45.5 倍、5Y 分位 88」。敏感度「倍數每降 5 倍約 −11%」「EPS −10% 疊加 30 倍約 −41%」「3 年後回 30 倍 EPS 需年增約 15%」，都由 45.5 推出。
- valuation 表：CRS「30.0／分位 40」，並歸為「中檔」。

正確值（`docs/dd-screener/latest.json`，as_of 2026-10-14；這個檔和 priced_block 同源）：
- HWM 的 `fpe_fy2`=45.5、`pct_5y`=88 是 `price_at_dd`=$273.77（DD 日 2026-07-10）的讀值。本文自己的現價是 $220.81，約低 19%。同檔的 live 欄位：`live_fpe_est`=33.18，`live_pct_5y_est`=42.9。我用 eps_fy_next 6.46 反算，$220.81÷6.46≈34.2 倍，與 live 欄位同量級。
- CRS 的 `fpe_fy2`=30.0、`pct_5y`=40 是 `price_at_dd`=$476.42（DD 日 2026-09-01）的讀值。本文現價 $377.25，live：`live_fpe_est`=23.61，`live_pct_5y_est`=4.5。算式 $377.25÷15.88≈23.8 倍。
- ATI 沒有此問題：`price_at_dd`=$187.98 與現價相同。

影響：
- HWM 實際約 33 倍、約第 43 百分位，落在文中自訂的「中檔」，不是「高檔」。
- CRS 約第 5 百分位，符合文中「低檔：分位低於 40」。文中卻寫「本輪無標的符合」。
- 文中的 −41%、15% 與 −11% 三個敏感度數字全部作廢。以 33 倍重算：EPS −10% 疊加 30 倍約 −19%。
- id-meta `priced_in: "high"` 沒有依據。三檔中只有 ATI（26 週 +14.2%、無分位）仍被追。
- 信心由中降低的理由，有一半寫在「HWM 分位仍 88」上，要重寫。
- 三次獨立判斷一致不能當佐證。三次吃同一份過期的 priced_block，失誤是共同的。

來源：`/docs/dd-screener/latest.json` 的 HWM、CRS 列（`fpe_fy2` 對 `live_fpe_est`、`pct_5y` 對 `live_pct_5y_est`）。可能欄位：`priced_block.md`（組裝端取了 `fpe_fy2`／`pct_5y`，沒取 `live_*`）→ judgment `priced_in`、`valuation.rows`、debates[2]、`action`。要正本清源，得在組 priced_block 時偵測 `price_at_dd` 與週線最新收盤是否偏離過大。

### B. Airbus 交付：現值停在 H1，證據包裡已有 9 月累計（J3、J6、J7）

錯誤文字：
- kill 表第 1 列「Airbus 季交付 YoY｜H1 351 架（+15%）；9 月 72 架」。
- 分歧 3 與核心判斷：「Airbus 上半年交付才 +15%」，用來證明引擎件與備品脫鉤。

正確值：
- evidence.json 的 D16 與 S3（2026-10-08）：9 月 72 架，年初至今 547 架（+8% YoY）。
- 547−351=196 架為 Q3。2025 年同期累計約 507（547÷1.08），Q3 2025 約 201。所以 Q3 YoY 約 −2%（推算值）。
- 9 月單月 72 架，去年同月 73 架，持平。
- 來源：https://www.airdatanews.com/airbus-delivers-72-jets-in-september-as-order-backlog-falls-by-58-aircraft/（2026-10-08）、https://mrobusinesstoday.com/airbus-delivers-547-aircraft-in-2026-as-september-deliveries-reach-72/。

影響：
- 本文把「季交付連 2 季 ≤0%」設為論點作廢線，窗口從 2026Q4 起算。Q3 實際已近 0 或略負，Q4 只要再 ≤0%，這條只剩一季就破線。表上看不出來。
- Q4 要達 870 架，需約 323 架（月均約 108）。Q4 2025 約 286 架，所以需要 +13% YoY。市場說法與現況落差很大，本文只引了 108 這個數，沒有把 Q3 的減速放進 12M 情境權重。
- 「備品脫鉤」要靠交付與引擎件增速的差距證明，最新一季差距的分母是 Q3 約 −2%，不是 +15%。HWM 的 Q3 引擎件要 10-29 才出，這個差距本期無法驗，但文中應如實寫。
- 這條不一定推翻 Phase II。換相第二訊號（ATI 積壓）未亮，但文中應寫「領先指標已走弱一季」。

可能欄位：`kill_metrics[0]` 現值、debates[2]、mechanics 3.1 的 OE 段。

### C. ATI Q3 財報日寫 10-27，公司公告為 10-29（J3）

錯誤文字：第一頁 action、PM 行動 ③、「2026-10 ATI Q3 財報（10-27）」、mechanics 觸發指標欄、id-meta `action`。全文把「等 10-27 ATI、10-29 HWM」當成兩個前後日期。

正確值：ATI 於 2026-10-13 公告 Q3 財報 10-29 美東 7:30 前發布，電話會議 8:30 ET，與 HWM 同日。來源：https://www.stocktitan.net/news/ATI/ati-announces-webcast-for-third-quarter-2026-6omk8busfrps.html。

來源判斷：evidence.json 沒有 10-27 的任何出處（HWM 的 10-29 有 C3、D9、S1、S2 四條）。10-27 吻合 latest.json 裡 ATI 的 `next_earnings_date` 估算值，公告晚一天出，估算沒更新。這等於把估算日當事實寫進第一頁。

影響：「ATI 積壓 YoY 跌破 +5% 即改判 Phase III」是整份報告唯一的換相板機，日期錯了會讓讀者提早兩天找不到資料。

## 🟡

**1. 第二訊號的措辭把 CRS 也算進「已亮」（J5、J9）。** 3.4 末段寫「充分條件＝龍頭股價 26 週下跌而同期指引上修（已亮：HWM −13.6%、CRS −15.3%）」。第一頁與核心判斷則寫「①僅 HWM 證實」，CRS 是首次給指引、無前次可比。閘雖已修過一次，這一段漏改。建議改為「已亮：僅 HWM（−13.6%）；CRS −15.3% 但 FY27 指引為首次給出，無法判定上修」。

**2. 商品價現值過期、且標成現值（J3）。**
- 摘要「鎳約 $16,790/t」。證據日為 2026-08-12，evidence 的 NF-D 已寫「查不到 10 月現值」。
- 實際：LME 現貨 2026-10-07 約 $15,645（https://thevaultreport.com/lme/nickel），2026-10-02 三月期約 $15,626。已低約 7%。第一頁沒有標日期，應改為「8 月 $16,790，10 月初約 $15,600」或拿掉。
- 中國 0 級海綿鈦 RMB 48–49k 是 2026-07-01，距今 3.5 個月，是 kill 表第 5 列現值。我也查不到更新的報價，這點屬「未及查證」，但表中要寫「最新可得 7 月初」並標過期。

**3. 海綿鈦 kill 與本文自己的論述矛盾（J7、J5）。** 本文反覆說商品級海綿鈦與航太級隔著 3–5 年認證牆，「中國的過剩短期進不了航太級」。kill 表第 5 列卻把商品價跌破 RMB 45,000 連 2 個月列為風險控制，第一頁又寫「破 → 論點作廢」。同一條在第一頁（論點作廢）和 kill 表（風險控制：威脅卡升一階）姿態不同。CRS 那條同樣：第一頁寫「論點作廢」，表上寫「降級」。建議第一頁姿態與表一致。「領先西方鈦定價 ≥4 季」只是推論，沒有數據。

**4. 近期催化劑漏列 CRS 10-22（J3、J8）。** 日曆只有「2027Q1 CRS FY27 Q2 財報（日期未載）」。CRS FY27 Q1 財報為 2026-10-22，公司指引營業利益 $195–200M（https://www.mychesco.com/a/news/regional/carpenter-technology-sets-oct-22-earnings-update/）。它早於 ATI、HWM，CRS 又被列「優先觀察」，並承載 kill 第 4 條（SAO 利益率）。應補上。

**5. 姊妹 ID 沒對帳，但資料在庫內（J2）。** 報告寫 CommercialAerospace、DefenseModernization「本輪輸入未附其裁決欄，無法逐項對帳」。實際 id-meta 可讀：
- ID_CommercialAerospace_20260427：shortage／II，conviction high。
- ID_DefenseModernization_20260430：shortage／**IV**，conviction high。
- 本文：shortage／II，conviction low。
航太金屬與商航、國防的需求端相位或信心不同，不一定是錯，但屬可調和的口徑差異，應各用一句交代（商航今日正在改寫，改寫完成後也要並排）。另外 `tam_usd_2030` 由 95 改為 16（窄口徑，已說明），下游若直接比欄位會看到 −83%，建議在 id-meta 欄位註記口徑，或確認聚合端會讀。

**6. 敗局劇本缺時序（J8，playbook #4）。** 12M／3Y 的 Bear 只有一句「Q4 交付落空，2027 上半年去庫存」「重演 2009 縮小版」。沒有寫誰先被砍、傳導幾季、各環節的前例。手冊命中「寫 bear 情境」，答得不夠具體。去庫存是本文宣稱的最早風險，這是缺口。其餘命中條目（#1 資本湧入、#2 撮合價、#11 分母、#14 純度稀釋、#18 雙閘）實答都有數字。

**7. 白話與內部代號（J10）。**
- 「SAO」「PEP」「VIM」「PQ billet」「A&D」「AA&S」在第一頁或表中未加白話。「SAO 調整後利益率」出現在第一頁否證指標。
- 玩家矩陣出現「（T4）」，是來源層級代號外漏到正文。
- 「充分訊號亮 1/2」「①」對讀者不直觀。

## 🟢 通過項

- **J1。** 抽查 cornerstone：ATI 2009 營收 $5.31B→$3.05B（−43%）、鈦價 $33.83→$19.37（−43%）、CRS SAO 37.8%／34.7%、HWM 引擎件 $1,373M（+32%）、結構件 −13%、ATI 積壓 $4.4B（+18%）、2006 年 ATI 與 Boeing 長約 $2.5B（https://www.asminternational.org/ati-extends-aerospace-titanium-products-supply-agreement-with-boeing/ 一類，ATI 2006-10-16 公告 2007–2015 預估 $2.5B）、CRS FY27 營業利益指引 $850–880M（FY26 $702.0M，+23% 吻合），都與證據包一致。737 速率 52 尚無核准，2026-05 後我也未見更新，吻合。
- **J4。** 四張分歧卡的「市場最強版本」都帶數字與出處，威脅卡（中國海綿）附判別訊號與 ≥1,000 噸門檻。
- **三情境算式。** HWM 10.05×68%≈6.8、ATI 1,160÷22.6%×68%≈3.5、CRS 1,658×(3,124÷2,528)≈2.0，合計 12.3。Base 16.1、Bull 18.0、Bear 12.2、加權 15.5，我重算吻合。5 年倍數 1.5、CAGR 9% 吻合。雙路徑差 6–7%，唯兩法共用同一基期，獨立性弱，文中已自白。
- **CRS capex／營收 7.8%：** $242.7M÷$3,124M＝7.77%，前年 $154.3M 吻合 5.4%。

## J6 壓力測試：留在「短缺 × 第二階段」是否成立

1. **相位有基本面證據？** 有。ATI 積壓 $4.4B（+18%）且 CEO 稱需求超過供給、CRS SAO 37.8% 創高、HWM 引擎件 +32%、換相第二訊號（ATI 積壓 <+5%）未亮。依本文雙閘，不能判 III。判定留在 II 站得住。
2. **26 週漲幅是否指向更晚相位？** HWM −13.6%、CRS −15.3% 在指引上修下下跌，是晚期特徵，文中已處理。但（B）Q3 Airbus 交付約 −2% 是未納入的減速證據，會把「後段」的語氣拉重。建議維持 II，把「後段」寫實，並把 Q4 交付落空的機率放進 12M 權重，而不是只寫情境。
3. **`priced_in` 誠實嗎？** 不誠實，原因是 A。以 live 值，HWM 約 33 倍、第 43 百分位，CRS 約 24 倍、第 5 百分位，ATI 無分位。三檔裡只有 ATI 被追，「已定價 高」應降為「中」或「分歧」。

結論：維持 shortage × II 站得住，但 base-rate 義務的第二段（為什麼這次不同）要換證據。過期的「分位 88」不能用，應改用：①龍頭已先修正（HWM 自 7/30 約 −22%，CRS 自 9/1 約 −21%，皆來自 latest.json 的 price_at_dd 對照現價）；②供給反應有實體時滯；③但 Airbus Q3 減速與去庫存風險是這格歷史失效（91 天超額中位 −7.5%）的可能路徑。信心維持「低」仍合理，只是理由要換。

## 未及查證 / 限制

- Airbus 2025 年 9 月累計 507 架為推算（547÷1.08，並與我記憶相符），未直接取得 2025 年原始表。
- CRS 與海綿鈦 10 月最新報價查不到。
- HWM 2026 capex 逾 $500M 引自 10-Q 搜尋摘要，未讀原文。
- RS 航太 9% 為二手轉述，本文已標示。
- 市場級 TAM（前版 $95B）無從重建，本文改窄口徑，我無法判斷何者較準。

## 處置（2026-10-14，局部修，不重判）

只改有錯的欄位，裁決（shortage × II）、conviction（low）、base_rate.action、交界欄位都沒動。votes.json 是中斷重跑後依原 3:0 重建的，未碰。改前檔留在 run 目錄的 `judgment.pre_local.json`、`evidence.pre_local.json`、`plan.pre_local.json`。

### 估值輸入（🔴A）

priced_block 改用 dd-screener 現價估算值（`live_fpe_est`／`live_pct_5y_est`，as_of 2026-10-14）。5Y 分位是程式按 DD 日分位推估的，不是實測序列，文中一律標「現價估算」。

| 欄位 | 改前 | 改後 | 來源 |
|---|---|---|---|
| valuation.priced_rows HWM | 45.5 倍／分位 88.0 | 33.18 倍／42.9（現價估算） | priced_block（latest.json live 欄） |
| valuation.priced_rows CRS | 30.0 倍／分位 40 | 23.61 倍／4.5（現價估算） | 同上 |
| valuation.priced_rows ATI | 29.51 倍／None | 29.47 倍／無 | 同上 |
| valuation.sensitivity | 每降 5 倍 −11%；EPS −10% 疊加 30 倍 −41% | −15%（5÷33.18）；−19%（0.9×30÷33.18≈0.81） | 重算 |
| valuation.implied_growth、derivations[1] | 回 30 倍需 EPS 年增約 15%（CRS 的 30 倍） | 回 30 倍只需年增約 3.4%（33.18÷30≈1.106，開三次方≈1.034）；「CRS 的」拿掉，CRS 已不在 30 倍 | 重算 |
| valuation.derivations[0] | 220.81÷45.5≈$4.85，口徑差未解 | 33.18÷45.5≈0.73，倍數已收斂約 27%；FY2 用 FY27 EPS，故低於以 FY26 指引算的 41.9 倍 | 重算 |
| valuation.derivations[2] | 雙殺約 −41% | 約 −19% | 重算 |
| valuation.derivations[3]、implied_growth（ATI） | 187.98÷29.51，隱含 FY27 EPS +26% | 187.98÷29.47≈$6.38，÷$5.04≈1.27，約 +27% | 重算 |
| valuation.derivations[4] | 只有營業利益指引 | 補 CRS 現價估算 23.61 倍、分位約 5（9/1 為 30.0／40） | priced_block |
| valuation.low／mid／high | low 無標的；mid＝CRS（分位 40）；high＝HWM（45.5／88） | low＝CRS（23.6 倍、分位約 5；FY27 營業利益指引中位 +23%，股價 26 週仍跌 15.3%）；mid＝HWM（33.2 倍、分位約 43）；high 無標的（HWM 7/10 曾屬此檔） | 依原 rubric 重分 |
| debates[1] 標題、our_view、priced_in、neg_read、falsifier | 45 倍／分位 88／−41%／仍 ≥45 倍 | 33 倍／分位約 43／−19%／仍 ≥33 倍；our_view 改寫為「倍數已由 45.5 降到 33.2，收斂已走了一大段」 | 重算 |
| base_rate.differences[1] | 只有股價跌幅 | 補「倍數由 7/10 的 45.5 倍降到 33.2 倍」 | priced_block |
| base_rate.differences[2] | 「HWM 分位仍 88」 | 理由換成「Airbus Q3 交付已年減約 2.5%，去庫存正是這格歷史失效的可能路徑」；cite 由 D8 改 S3、X3、C9 | 見 🔴B |
| summary.priced_in_note | HWM 分位 88、CRS 40 | HWM 分位約 43、CRS 約 5（現價估算） | priced_block |
| id_meta.action、summary.pm_actions[0–1] | 不追 HWM（45.5、88）；CRS 分位 40 | 不追 HWM：倍數已由 45.5 降到 33.2（分位約 43），仍等 10-29 財報與回調；CRS 23.6 倍、分位約 5，列優先觀察，先看 10-22 財報 | 同上 |

**priced_in：high → mid。** 依報告自己的 rubric，HWM 落在 mid、CRS 按分位落在 low、ATI 無分位但 26 週 +14.2% 是唯一仍被追的，合起來是 mid。action 方向不變（不追 HWM、等財報與回調、CRS 優先觀察），只換數字與措辭。

### 審稿發現

| 項 | 欄位 | 改前 → 改後 | 來源 |
|---|---|---|---|
| 🔴B | risks.kill_table[0].now | 「H1 351 架（+15%）；9 月 72 架」→「1–9 月 547 架（+8%）；Q3 196 架，年減約 2.5%（累計數相減）；9 月 72 架。Q4 再 ≤0% 即連 2 季」 | S3（547）、C9（H1 2025 306）、X3（9M 2025 507，Airbus 新聞稿）。2025 年同期基期是公司公布值，不是推估；Q3 2025＝507−306＝201，Q3 2026＝547−351＝196，196÷201≈0.975 |
| 🔴B | thesis.points[1]、debates[3].our_view | 「Airbus 上半年交付僅／才 +15%」→ 標明 +15% 是上半年、與 HWM Q2 同期；補「Airbus Q3 交付年減約 2.5%，領先指標已走弱一季，脫鉤要等 HWM 10-29 的 Q3 驗證」 | 同上 |
| 🔴B | debates[3].market_view | 「Q4 需月均約 108 架」→ 補「1–9 月 547 架，Q4 需月均約 108 架、年增約 13%」 | X4（2025 全年 793）：Q4 2025＝793−507＝286；(870−547)÷286≈1.13 |
| 🔴B | mechanics.demand.current_points[0] | H1 351 架（+15%）→ 1–9 月 547 架（+8%），Q3 196 架、年減約 2.5% | S3、X3 |
| 🔴B | id_meta.now_state | 補「Airbus Q3 交付年減約 2.5%」 | 同上 |
| 🔴C | id_meta.action、summary.pm_actions[2]、risks.catalysts（ATI）、mechanics.verdict.horizons[0].trigger | ATI Q3 財報 10-27 → 10-29（與 HWM 同日） | X1：ATI 2026-10-13 公告（PRNewswire，StockTitan 轉載），10-29 美東 7:30 前發布 |
| 🟡1 | mechanics.verdict.gate_sufficient[0] | 「已亮：HWM −13.6%、CRS −15.3%」→「已亮：僅 HWM −13.6%；CRS −15.3%，但 FY27 指引為首次給出，無法判定上修」 | 措辭與 thesis.derivation 對齊 |
| 🟡2 | id_meta.now_state、thesis.exhibit 鎳列 | 鎳約 $16,790/t（8 月）→ LME 鎳 10-13 現貨約 $15,445/t（較 8 月低約 8%），表列日期改 2026-10-13 | X5（The Vault Report 轉載 LME 官方結算，T3-B） |
| 🟡2 | risks.kill_table[4].now、summary.kill_brief[2].now | 海綿鈦 RMB 48–49k → 加註「最新可得，已逾 3 個月」 | 再查一輪仍無 7 月後報價 |
| 🟡4 | risks.catalysts | 原「2027Q1 CRS FY27 Q2 財報（日期未載）」改為「2026-10 CRS FY27 Q1 財報（10-22 盤前）」，移到第一列；正反情境與 kill 4 計數照舊 | X2（MyChesCo 2026-10-06）。審稿提到的單季營業利益 $195–200M 原文未載，沒寫入 |
| 🟡5 | thesis.sister_reconcile[1–2] | 「本輪輸入未附其裁決欄」→ 商航 shortage／II、conviction high，差在本報告另計同格勝率與資本湧入；國防 shortage／IV（v2.3 自訂時鐘，IV＝國防預算結構性超級週期），與本報告上游資本週期相位口徑不同 | docs/id 兩份 id-meta |
| 🟡7 | summary.clock_note、thesis.points[5] | 「訊號亮 1/2（①…）」→「兩個換相訊號亮一個，只有 HWM 證實」 | 白話 |
| 🟡7 | 玩家矩陣兩格 | 「（T4）」→「（單一二手來源）」 | 白話 |
| 🟡7 | kill_brief[1]、id_meta.kill_metrics[3]、PQ／AA&S／A&D／PEP／VIM 首次出現處 | 加中文全稱：特殊合金事業（SAO）、航太級（PQ）鈦胚料、航太國防事業（AA&S）、航太國防（A&D）、加工事業 PEP、真空感應熔爐（VIM） | 白話 |

新證據 X1–X5 已寫入 evidence.json（note 標「審稿補入」）。被引用來源的 T1 占比由 69% 變為 67%，仍高於 60% 下限。

### 跳過

- 🟡3 第一頁「破 → 論點作廢」與 kill 表姿態不一致：這句是 `report_template.md` 寫死的模板文字，改要動 skill 模板，本次不動。「領先西方鈦定價 ≥4 季」已標「（推論）」，維持。
- 🟡5 `tam_usd_2030` 口徑註記：id-meta 沒有口徑欄，加欄要動 schema，本次不動。
- 🟡6 敗局時序：mechanics.verdict.bear_narrative 已有逐季傳導與 2009 前例，補寫屬判斷內容，不在局部修範圍。
- 🔴B 延伸建議「把 Q4 落空的機率放進 12M 權重」：屬判斷，不改，列交持有人。
- 海綿鈦 10 月現值：查不到。

### 交持有人

1. Airbus Q3 已年減約 2.5%，Q4 要達指引需年增約 13%。12M 情境是否要把「Q4 交付落空」寫成明確機率或調整視野權重，屬判斷，未改。kill 表第 1 列窗口從 2026Q4 起算，Q3 已 ≤0%，Q4 再 ≤0% 算不算「連 2 季」，要擁有者定。
2. CRS 歸 low 檔只靠程式推估的 5Y 分位（4.5，按 DD 日分位與 60% 區間寬度推算），不是實測序列，是否要等實測分位再確認。
3. 頁首「破 → 論點作廢」是模板寫死的字樣，與 kill 表「風險控制／降級」姿態不一致，要改 skill 模板。
4. 重跑閘的黃燈（未修，皆不擋）：J5 一句話「最好賺的一段已被定價」與 priced_in=mid 語氣是否一致（本次依指示只改 priced_in、估值段與 action；mid 的定義是「反映 2026–27 年短缺」，字面不衝突，但語氣偏強）；J9 HWM 財報催化劑的「引擎件 <+15%」與 kill 2 門檻 <+10% 不同步；D12 美國海綿歸零年份（B18 寫 2020、A8 寫 2024 最後一座廠關閉）；D4 三角對帳兩法共用基期、差距應為 6–7%；J2 商航 20261014 版若發布，sister_ids 要換新版重對。

### 重跑結果

gate 第一輪紅 0、黃 8，未進 patch；prose 兩半皆交；check PASS（check_id rc=0、validate rc=0、76KB）。程式列出的 8 個「疑似新增數字」是章節號、來源表裡的 Section 232、Ex.99.1 與 URL 片段，不是新資料。HTML 已逐項確認：33.18、23.61、42.9、4.5、29.47、−15%、−19%、3.4%、10-29、10-22、547／196／2.5%／13%、15,445、「僅 HWM」、姊妹對帳兩句都在；10-27、−41%、「（T4）」已不在頁面。45.5 與分位 88 只剩標明「7/10」的對照句。
