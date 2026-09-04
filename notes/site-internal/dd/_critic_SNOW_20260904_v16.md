# SNOW 判斷層 critic（v16 Stage 1 · 跨模型冷讀）｜2026-09-04

> 載具：QC-41（四軸＋⑤⑥）＋QC-50 合併。判斷層 sonnet → critic opus。查證 10 輪（8 WebSearch＋2 WebFetch，預算 14）。
> 讀入：`SNOW_20260904.evidence.json`／`.judgment.json`／`.scenario.json`＋`scenario_meta`／`e11.html`；規則原文只讀 timing-appendix QC-45 段與 judgment-rules QC-49 段。未讀任何 HTML／散文。

## FINDINGS

| # | 嚴重度 | JSON 路徑 | 一句話 | 最小修法 |
|---|---|---|---|---|
| F1 | 🔴 | `industry.bargaining.down`／`moat.trend_evidence`／`moat.roic_durability.checkpoints[0].evidence` | 「733 家客戶近 12 個月 product revenue 超 100 萬美元」是舊期數字，Q2 FY27 官方為 **828 家（+27% YoY）** | 三處 733→828，補「+27% YoY」；並註明 828 的 +27% 低於 product revenue 的 +37%＝擴張來自既有大戶加購而非新大戶增加，「占約 68% 營收」需一併重驗 |
| F2 | 🔴 | `valuation.upside_short_pct`／`upside_mid_pct`／`appendix_a` 同名欄 | 短中期 upside 悄悄由規則法（FY+1 EPS × 合理 P/E）換成分析師目標價，且用的是**財報前**舊共識（−15.0% 恰為 302.29 對 355.50），前份 −61.9%→本份 −15.0% 共 47pp 漂移零歸因 | 依規則重算（FY28E 3.02 × 合理 PE 48 ≈ $145 → 約 −59%）；若堅持錨分析師，須改用證據包自己記載的**財報後**目標 $390–450；兩者皆須開 `contradictions[]` 條目 |
| F3 | 🔴 | `decision_inputs.consensus_rev_3m_pct` | 2.2% 是 yfinance 財報前快照（2.7071 vs d90 2.65025），證據包已警告未反映 9/2 財報；判斷物自己用 **+11.65% guide 上調倍率**建 Base 路徑＝自承共識該上修逾 10%，直接壓低 QC-50 gate② 的觸發判定 | 欄位標「財報前快照，post-earnings 未反映」或改填 guide 隱含 +11.65%，並在 QC-50 論述中承認 gate② 以財報後基礎成立 |
| F4 | 🔴 | `governance.sbc`／`decision_inputs.valuation_dependent`／`premortem` | Q2 FY27 股權薪酬 **$456.4M > 非GAAP 營業利益 $237.0M**（年化約 $1.8B ≈ FY27 營收 29%）——整棵情境樹、終端 48x、輔助 PE 全建立在「扣掉一個比營業利益還大的項目」之後的非GAAP EPS 上，判斷物全文未出現此量級對照 | `governance.sbc.note` 補此對照；`premortem` 增列「非GAAP 口徑失效」失敗路徑；並明寫為何 `valuation_dependent` 仍為 False（或翻 True） |
| F5 | 🔴 | `moat.roic_durability.endo_ceiling` | 欄位填 26.0，但 `formula_note` 自承「此 26% 為五年後**非GAAP營益率**之估計上限，非傳統報酬率數值」＝把利潤率填進成長天花板欄；實際做 sanity check 用的是營收 CAGR 20.3%；前份同欄 25.0 是成長率，下游 dd-meta 會把兩者當同單位比較 | `endo_ceiling` 改填 20.3（實際用於交叉檢核的營收成長上限），26% 營益率移入 `formula_note` |
| F6 | 🔴 | `contradictions[]` | 情境六欄 `bull_5y_price` 767.6→750.0、`bear_5y_price` 50.6→43.2、`ev5y_pct` 6.4→6.6、`irr_base_pct` 2.3→2.2、`asym_ratio` 1.0→1.1，及 `rearm_trigger` 第二肢改寫（AI run-rate 揭露→Databricks 連四季），六項對 `prior_meta` 有異但**無獨立條目**（§12 3b 要求逐欄本次值／前份值／三元歸因）；`validate_judgment.py` 竟 PASS＝機械閘未實作此檢查 | 補 6 條獨立條目；歸因主因皆為「方法論變了（情境參數同向收緊）」，須寫明方向是**收緊非放寬**（Bull PE 65→60、Base PE 50→48、Bear 終端 EPS 2.81→2.40、二段 CAGR 26/20→20/15） |
| F7 | 🟡 | `valuation.val_light_derivation` | QC-45 要求**雙尺取較嚴者**，只算了尺①（growth-adj EV/S 0.62），尺②（自身上市以來 fwd EV/S 分位）標「證據包未涵蓋」——SNOW 2020-09 上市已逾 3 年，尺② 是全權重尺非輔助 | 我已代查：GuruFocus SNOW EV/Revenue 10Y 最低 8.58／**中位 20.92**／最高 182.54，2026-08-03 現值 21.14 ≈ 中位 → 30/70/85 切點下為 🟡。**取較嚴 = 🟡，燈色成立**；把此尺與來源補進推導文字 |
| F8 | 🟡 | `moat.spread_table[1]` | 毛利率列用 FY26 年度 67.3% vs 四年均 66.7%＝「+0.6pp」，並稱 AI 稀釋「尚未顯著發生」；實際 Q2 FY27 **非GAAP product 毛利率 74.7%，較去年同期約 76% 已下滑**，當季口徑 spread 為負 | 改用非GAAP product GM 口徑（74.7% vs ~76%，−1.3pp），「尚未顯著發生」→「已開始發生，FY27 guide 74% 為進一步下探」 |
| F9 | 🟡 | `trap_analysis.evidence_against` | 「RPO 年增 30%…（領先指標未虛胖）」隱去了 **RPO $9.00B 未達共識 $9.37B（−3.9%）**——那是本季唯一走反方向的數字 | 補上 vs 共識落差；刪除或改寫「領先指標未虛胖」這句（現況該句被證據直接證偽） |
| F10 | 🟡 | `moat.competitors[]`／`quality.three_year[].peer_median`／`governance.capital_returns[].rd`／`valuation.peers[2]` | 大量可公開取得欄位掛「數據缺口」：MongoDB 6 欄中 5 欄、Datadog 4 欄、peer_median 5/5、R&D 4/4、Confluent 整列 null；DDOG fwd PE 兩來源互斥（96 vs 79.26）且 EV/EBITDA 873x 明顯是 EBITDA≈0 的假象仍留在表上 | 從 MDB/DDOG 最近一季 10-Q 補 GM/OM/FCF margin；刪 873x；CFLT 改標「本輪排除」而非 null 列 |
| F11 | 🟡 | `moat.competitors[]`／`moat.threats[]` | **Microsoft Fabric 在整個證據包 0 次提及**；競爭軸只用單一低階來源（repvue）排出 Databricks#1／BigQuery#2／Redshift#3，漏掉 Azure/M365 生態內公認在 14 項比較中贏 9 項的 Fabric。`moat_trend`「→」建立在雙雄框架上 | 增一列 Fabric 競爭者／或一條 🟡 threat；裁決方向不受影響（本已 觀望），故列 🟡 |
| F12 | 🟡 | `decision_inputs.momentum_overheated`／`week26_return_pct`（源：`evidence.numbers.rsi14`） | 股價創 52 週新高、單日 +16.55%，`rsi14` 卻是 36.06——日線 RSI 不可能如此；`momentum_overheated=False` 與 audit row 5 直接建在這個讀數上。`week26_return_pct=None`，但 2026-01 約 $211、其後至 4 月初腰斬、現 $355.5，26 週漲幅極可能逾 +100% | RSI 重算或標為不可用並改由 4 週漂移＋26 週漲幅推導；補 26 週基期價。**註**：即使 overheated 翻 True，row 5 也是指向 ≥觀望，裁決不變，此為路徑誠實性問題 |
| F13 | 🟡 | `reasoning.valuation` | 寫「裁決依**分母爭議檢查**以側重絕對報酬與情境樹經濟性為主」，但 `val_denominator_disputed=False`、audit row 11.4b-denom hit=false；`contradictions[3]` 其實已正確執行 §11 4b.1 並判定分母**非**爭點 | 改寫為「4b.1 分母爭議檢查通過（營收成長率非爭點，側A 論證有效），裁決另以絕對報酬與情境樹經濟性為主」 |
| F14 | 🟡 | `decision_out.rearm_trigger`／`triggers[3]` | 進場 re-arm 門檻寫成「非GAAP 遠期本益比回落至 70 倍以下（≈$211）」——正是本報告宣告**非權威**（QC-45：GAAP 未轉正前 PE/PEG undefined）的那把尺；等於要 🟡 時用 EV/S、要 觀望 時用 PE | re-arm 改以 growth-adj EV/S（如 ≤0.5 轉 🟢）或絕對報酬門檻（Base IRR ≥ X%）表述，$211 只留作對照；並增一條**非價格**的論點增強觸發（見 QC-50 建議） |

## GATE: FAIL

理由：裁決方向（觀望｜追蹤）我認同且獨立驗證後仍站得住，但六條 🔴 中，F1 是重複三處的事實錯誤、F2/F3/F5 會把錯值寫進下游 dd-meta 欄位、F6 是 `judgment-rules.md` §12 3b 明文「無歸因＝validate FAIL」卻被機械閘漏放行。此檔在修完 F1–F6 前不可進 Stage 2。**re-gate 只需覆核六條 🔴 的落點，不需重跑四軸。**

---

## ① 競爭惡化 — 🟡 判斷低估

- Databricks 核心事實**我獨立查證通過**：2026-08-13 官方公告 total run-rate 破 $7B、YoY >80%、$5B 融資 $190B 估值（Coatue 領投）；Lakehouse 資料倉儲 run-rate 破 $1.5B、YoY >100%。判斷物引用無誤，`thesis.R1`／`triggers[2]` 門檻設定合理。
- **缺 Microsoft Fabric（F11）**。整份證據包 Fabric 0 命中，而 Snowflake 的競爭敘事若只有 Databricks，會系統性低估 Azure/M365 生態內的替代——這條與 Databricks 的路徑不同（Databricks 打 AI/ML 與 lakehouse，Fabric 打「已經買了 M365 就順便用」的採購慣性），對 NRR 的侵蝕形態也不同（前者搶新 workload，後者搶中型帳戶整包）。`moat_trend`「→」的證據基礎因此偏窄。
- 中小客戶底部（ClickHouse／Tinybird，TCO 低 60-70%）與 win-loss 勝率兩條，證據包自己標為低階聚合部落格、方法論不明——判斷物已正確降級為「方向性色彩」，處理得當。
- **828 vs 733（F1）** 落在本軸：828 家 $1M+ 客戶 YoY +27%，慢於 product revenue +37%，代表本季加速是既有大戶加購驅動而非大戶家數擴張。這對 H3（「份額此消彼長非整組遷移」）其實是**支持**的觀察，但也意味著成長更集中在少數帳戶——判斷物兩面都沒寫。

## ② 供需 durability — 🟢 判讀無虞（一項附註）

- NRR 126%、RPO $9.0B +30%、product revenue $1.4919B +37%、total $1.5468B +35%、non-GAAP EPS $0.62、GAAP 淨損 $191.7M：逐項與 8-K 一手核對**全部吻合**。連三季加速（30%→37%）為真，非敘事。
- 判斷物把「AI／agentic 需求是結構性非週期」判為結構性，我同意：三年 FCF margin 穩定 23-27%、capex/營收僅約 2%，沒有循環商品的供給可逆性問題。`archetype=未獲利高成長` 判定正確，不需走循環鏡頭。
- **附註（F9）**：RPO 未達共識 $9.37B。判斷物把 RPO +30% 單向寫成 trap 的反證，這是本軸唯一的證據挑選瑕疵。修正後 durability 判讀不變（consumption 模式下 RPO 本就不是好的領先指標，公司自己在 8-K 這樣講）。

## ③ 其他結構變數（開放軸）— 🟡 判斷低估

- **毛利率稀釋已開始，不是「將至」（F8）**。非GAAP product GM 74.7%，較去年同期約 76% 下滑，公司歸因 AI 基礎設施成本。判斷物用 FY26 年度 GAAP 口徑 67.3% 講「稀釋尚未顯著發生」，是拿較粗且較舊的尺看一個已經在動的變數。這條對 `moat.spread_table`（護城河價差的唯一量化窗）尤其重要。
- **SBC 量級（F4）是本輪最被低估的結構變數**。$456.4M/季 > 非GAAP 營業利益 $237.0M。判斷物的 `governance.sbc` 只講「占營收比重 41.5%→34.2%→guide 27%，方向改善」，這是對的但避開了絕對量級；而整份估值與情境樹用的都是非GAAP EPS。這同時也是 QC-45 為何要 GAAP-負→不用 PE/PEG 的實質理由（見下方核心裁定題）。另有 $23 億可轉債（2027／2029 到期）的轉換稀釋，判斷物有記但未進任何情境。
- **通路集中度未接線**：證據包 `channel_business_model_shift` 記載 AWS Marketplace 2025 曆年銷售破 $2B、約當 FY26 營收近 45%，且 SNOW 對 AWS 有五年 $6B 承諾——單一通路近半營收＋對該通路的巨額 take-or-pay 承諾，是實打實的結構性依賴。這條在 coverage 是 found，但完全沒進 `moat.threats[]`／`thesis.R`／`triggers[]`。屬證據採到卻沒接線。
- **歐盟資料主權／CLOUD Act — 🟢**。判斷物在 `industry.bargaining.geo` 與 checkpoint#4 有質性處理。我另查一輪，命中的多是賣「Snowflake 歐盟替代品」的廠商行銷文（sota.io、iomete），無獨立硬證據可加碼；`not_applicable` 未被濫用，本子軸判讀充分。
- 證券集體訴訟（2026-02-24 提起，爭點正是 Iceberg Tables 與分層儲存定價對消耗量的影響）已在 `thesis.R3` 與 `catalysts[2]` 落檔，處理得當。

## ④ priced-in — 🔴 判斷錯

判斷物的 priced-in 論證（「現價已把加速動能大部分計入」）在數字層錨錯邊：

- `valuation.targets` 用 `analyst_avg_12m` 317.29／alt 302.29、`vs_current_pct` −8.53%，而其 `note` 自己承認「多數目標價疑似仍為財報前設定（TD Cowen 08-20、Cantor 08-31，皆早於 09-02 財報）」。
- 同一份證據包的 `coverage.capital_markets_pricing` 明載**財報後**上修：Mizuho $355→$425、BTIG $340→$424、Needham $330→$450、Rosenblatt 上調，並總結「財報後目標價分布約 $350–450，多數主要券商落在 $390–450」。
- 亦即：以財報後賣方為錨，$355.5 是折價 10–27%，不是溢價 8.5%。判斷物在同一包證據內選了已被自己註記為過期的那一半，並讓它流進 `upside_short_pct`／`upside_mid_pct`（F2）。

這**不改變裁決**（裁決真正的承重腳是情境樹絕對報酬 2.2%／AR 1.1，不是賣方目標價），但 priced-in 這一軸目前的書面論證是站不住的，且錯值已寫進兩個 dd-meta 欄位。另一處單向解讀：法說會分析師零人追問 Databricks，判斷物讀成「風險未定價」（利空）；同一事實也可讀成「賣方已判定該風險不重要」。`premortem.blind_spots[0]` 有並列兩種解讀後選了前者，屬合理裁量，不扣分，但 `trap_analysis.evidence_for` 直接把它當成硬證據用，兩處口徑不一致。

## ⑤ 覆蓋面掃描 — 🟢

`evidence.coverage` 16 軸**全數 status=found，零 none、零 not_applicable**，無理由品質可審。抽查密度：`capital_markets_pricing` 4 查 10 發現、`substitute_technology` 3 查 7 發現、`major_events` 5 查 4 發現，皆非敷衍。唯一薄的是 `end_markets__專業服務`（1 查 2 發現），但該分部占營收約 5%，投入與重要性相稱，不扣分。本軸無 finding。

（覆蓋的**廣度**問題見 F11：Fabric 缺口不是「某軸沒查」，而是 `competitive_share_entrants` 這一軸查了但查漏了，故計在 ① 不計在 ⑤。）

## ⑥ 量化模組完整性抽查

**(a) `moat.roic_durability` — 🔴（F5）**
- `roiic`／`reinvest_rate` 皆填「無法乾淨計算」＋理由（GAAP 營業利益為負、稅後淨營業利潤為負時公式無意義），並在 `formula_note` 給出替代推導（營收 CAGR 20.3% ＋非GAAP 營益率五年由 14.5%→約 26% 貢獻約 10pp/yr ⇒ EPS CAGR 約 30.8%）。這是**合格的**——不是「估計約 X%」的敷衍，換尺理由成立。
- 但 `endo_ceiling=26.0` 是營益率不是成長天花板（`formula_note` 自承），而真正拿去做交叉檢核的是營收 CAGR 20.3%。單位錯置，下游 dd-meta 會與前份的 25.0（成長率）直接比較。
- **內生天花板 vs 共識 CAGR 的 sanity check 有做且結論正確**：EPS CAGR 30.8% > 營收上限 20.3%，缺口已標記為「內生上限已超出」，並以「提高 Bear 機率至 30%」處置。這正是規則要的動作，給分。

**(b) 情境樹 EPS 價差 — 🟢**
- Bull 終端 12.50 vs Base 8.27＝**+51% EPS 價差**，非「只有倍數差」的退化型；Bull PE 60 vs Base 48 亦有實質差異。
- 與前份逐項對照，本輪**全面收緊**：Bull PE 65→60、Base PE 50→48、Bear 終端 EPS 2.81→2.40、二段 CAGR bull 26→20／base 20→15、Bull 5Y 價 767.6→750.0、Bear 5Y 價 50.6→43.2。**核心裁定題 (4) 的答案：Bear 路徑相對前份是收緊不是放寬**（與 DELL 修 $14 終端 EPS 的方向一致，未出現「為了讓 EV 好看而放寬 Bear」的形態）。唯一放寬處是 Bull EPS 路徑（前份 11.81→本份 12.50），但被 Bull PE 下調抵銷有餘。
- 反向意見一則（不列 finding，屬判斷裁量）：Bear 終端 $43.2 隱含 FY32 EV/S 約 1.5x，遠低於 SNOW 上市以來 EV/Revenue 最低值 8.58x。此 Bear 對一家 67% 毛利、23% FCF margin 的公司而言近乎清算價。我做了敏感度：把 Bear 5Y 價放寬到 $140（−60%），EV 由 +6.6% 只升到 **+15.0%**、5Y IRR 由 2.2% 升到約 2.8%。**即使把最誇張的 Bear 整個換掉，裁決仍不變**——這反而是本份裁決最強的穩健性證明，建議 patch 時把這句敏感度寫進 `reasoning.scenario`。

**(c) 內部對帳 — 🟢**
- `decision_inputs.irr_base_pct` 2.2 ＝ `scenario_meta.irr_base_pct` 2.2；`ev5y_pct` 6.6 ＝ 6.6；`asym_ratio` 1.1 ＝ 1.1。三處一致。
- e11 機率加權我重算：0.25×111.0 ＋ 0.45×11.7 ＋ 0.30×(−87.8) ＝ **+6.68% ≈ EV +6.6%** ✓。`upside_5y_pct` 11.7 ＝ Base 5Y%，非 EV，欄位語意正確。
- `eps_meta.base_eps_path`（FY28 3.02／FY29 4.14／FY30 5.38）與 `scenario.eps.base` 前三年一致 ✓。
- Base 起始 FY27E 2.16 ＝ 財報前共識 1.93632 × 1.1165（guide 上調倍率）＝ 2.162 ✓，推導透明。

**⑦ 白話呈現核** — 依 v16 改法不在本輪，未評。

---

## 核心裁定題

### (1) QC-45「EPS 轉正」＝哪個口徑？— **GAAP。今天的 EV/S 主錨對規則；昨天 critic 認可 PE/PEG 為主尺是誤判。**

三個理由，由弱到強：

1. **文法／同主語**。QC-45 觸發句寫「**GAAP 負 EPS 時** PE 分位與 PEG 全 undefined」，退出句「EPS 轉正（FY+1 > 0）後改回 PE/PEG 尺」承接同一主語與同一問題（什麼時候 PE/PEG 才重新有意義）。同一條文的進出兩端讀成兩種口徑，需要外部理由，條文沒給。
2. **自相矛盾檢驗**。若「轉正」讀非GAAP，SNOW 會**同時**滿足觸發（GAAP 負）與退出（非GAAP FY+1 正 = FY28E 2.71–3.02），規則對同一標的同時要求「改用 EV/S」與「改回 PE/PEG」。這不是模糊，是矛盾。
3. **死條文 reductio（決定性）**。QC-45 的目標母體是「未獲利高成長」——這類公司幾乎全數非GAAP EPS 為正（正是因為把 SBC 加回去）。非GAAP 讀法會讓 QC-45 對其設計對象**永不可達**，成為裝飾條文。這違反本 repo 判斷類規則須可證偽／可觸發的治理原則（「0 命中的閘是裝飾不是紀律」）。

**實質面亦支持 GAAP 讀法**：SNOW 本季 SBC $456.4M > 非GAAP 營業利益 $237.0M（F4）。QC-45 之所以在 GAAP 負時封掉 PE/PEG，正是因為此時的非GAAP EPS 分母把一個大於營業利益本身的股東成本排除在外——用它算 PE 再乘終端倍數，等於對一個未經證實的口徑做五年複利。SNOW 是這條規則的教科書適用對象，不是例外。

**但 val 🟡 目前只是「補完後仍成立」，不是「已成立」**：agent 只跑了尺①（0.62 → 🟡），尺②被標「證據包未涵蓋」而跳過，違反 QC-45「雙尺取較嚴者」（F7）。我代查補齊：SNOW 上市以來 EV/Revenue 最低 8.58／中位 20.92／最高 182.54，2026-08-03 現值 21.14 ≈ 中位，於 30/70/85 切點落 🟡。**尺① 🟡 ∩ 尺② 🟡 → 取較嚴仍 🟡。** 另我用 FY1 分母覆核尺①：EV 121.99B ÷ FY27 營收共識 6.104B ＝ 20.0x ÷ 30.31% ＝ 0.66，同樣 🟡——agent 宣稱的「多組替代分母測試皆落合理區間」屬實。毛利率 67-75% > 50%，不觸發 EV/gross-profit 對照要求。

**故：val 🟡 成立，矩陣機械落 row 9b 也是正確輸出。前份的 val 🔴 是對 QC-45 適用範圍的誤用，不是「取嚴」。**

### (1b) 那 QC-49 承繼是否合規？— **合規，且揭露方式已正確，不需改標為進場·條件式。**

- **條文層**：QC-49 對「翻面的成因」不設任何條件，只問「引不引得出前次已發火的具體觸發器」。我逐條核 `prior_dd.triggers` 五列：#1 成長率（現 37%，門檻連 2 季 <30%）未發火；#2 NRR（現 126%，門檻連 2 季 <118%）未發火；#3 Databricks 相對速度（現約 2.7x，倍數已達但季數未滿 4）**未滿足完整門檻**；#4 估值 rearm（PE ≤70x／$212，現 164.6x）未發火；#5 複審日期 2026-11-25 未到。判斷物的「五項皆未發火」屬實。**一個保留**：前份 `rearm_trigger` 的第二肢是「AI/agentic 層（CoCo/CoWork）貢獻 run rate 具體揭露且達門檻」，本季法說僅揭露帳戶數與「貢獻約半數加速」的質性說法，未揭露 run-rate 絕對金額——我判定未發火，但判斷物只數了 E12 五列、沒有明文檢核這一肢，應在 `contradictions[4]` 補一句。
- **目的層**：QC-49 的標題就是「防方法論 churn 誤當資訊」。**方法論驅動的機械翻面正是本規則的核心適用情境，而非規避情境。** 主張「因為是方法論改變所以不該承繼」等於把規則讀反。
- **邊界④ 不適用**：例外口是「前次 binding constraint 已**退役或降級**」。前次的 binding constraint 是 val 🔴 → row 8；QC-45 這條規則本身沒有退役，退役的是前份對它的錯誤適用。QC-49 沒有「前份誤用規則」的例外口——這是規則設計的真實缺口（**建議登記下輪校準**：是否為 QC-49 增設「前份經 critic 認定為規則誤用所致之 binding constraint，不受承繼保護」的第五款；但**本輪不得據此重裁**，因為那等於 critic 在裁決當下自造例外）。
- **揭露層 — 已達標**：`decision_out.row_hit` 寫「9b→翻面前置條件未達成，承繼(觀望)」，`audit_rows` 同時列 row 9b `hit=true` 與 QC-49 `hit=true`，`exec_line` 完整交代機械輸出與承繼理由。不存在「矩陣算出 9b 卻藏起來」的情形，故**無須改標為進場·條件式**。
- **實質層**：Base IRR 2.2%、AR 1.1、EV +6.6%，且如 ⑥(b) 敏感度所示，即使整個換掉最苛的 Bear，IRR 也只到約 2.8%。承繼的方向與經濟性一致——這是「規則與常識同時指向同一答案」的情形，而非靠規則硬壓。

**唯一不誠實之處在別處，且已列為 F14**：報告宣告 PE/PEG 非權威（才有 🟡），卻把進場 re-arm 門檻寫成「PE 回落至 70x（≈$211，−41%）」。要 🟡 時用 EV/S、要 觀望 時用 PE。這才是應修的「標示誠實性」問題，不是裁決標籤。

### (2) 漂移三元歸因完整性 — **不完整，見 F6。**

`drift_watch` 20 欄逐欄比對結果：

| 欄 | 前份 | 本份 | 狀態 |
|---|---|---|---|
| dca_verdict／dca_role／signal／ma／trap／moat_trend／runway_post_y5／p_bull_pct／p_bear_pct／archetype／cycle_position | — | — | 相同，無需條目 ✓ |
| `val` | 🔴 | 🟡 | ✅ `contradictions[1]` 完整三元歸因，方法論明標 |
| `price_at_dd` | 369.89 | 355.50 | △ 併在 `contradictions[1]` 作次因處理，未開獨立條目（可接受但非嚴格合規） |
| `asym_ratio` | 1.0 | 1.1 | ❌ 無條目 |
| `ev5y_pct` | 6.4 | 6.6 | ❌ 無條目 |
| `irr_base_pct` | 2.3 | 2.2 | ❌ 無條目 |
| `bull_5y_price` | 767.6 | 750.0 | ❌ 無條目 |
| `bear_5y_price` | 50.6 | 43.2 | ❌ 無條目 |
| `rearm_trigger` | PE 70x｜AI run-rate 揭露 | PE 70x｜Databricks 連四季 | ❌ 無條目（第二肢實質改寫） |
| `max_dd_pct` | −86.0 | lo −80／hi −55 | ❌ 無條目（口徑亦由單值改區間） |

另 `long_term_confidence` 中→低雖不在 20 欄內，判斷物仍主動開了 `contradictions[2]`，歸因為「前份規則適用落差」——這條做得好，應保留。已寫的 5 條 contradictions 品質高（三元歸因、evidence_level、settle_metric、if_then 齊備），問題純在覆蓋數量。**另回報 orchestrator：`validate_judgment.py` 對此檔 PASS（0 FAIL／1 soft WARN），代表 §12 3b 的逐欄漂移檢查在 v16 機械閘中尚未實作，屬工具缺口而非本 agent 疏失範圍。**

### (3) 七表是否 sourced — **五表實、兩表半空、一表有假象。**

| 表 | 判定 |
|---|---|
| `industry.tam_table`（3 列） | 🟢 實 — Mordor $149B(2026)→$491B(2031) CAGR 26.9% 具名來源；代理層窄口徑引自站內 ID 並標明「僅事實引用非決策層結論」，合 DD↔ID 規範 |
| `moat.spread_table`（3 列） | 🟡 — 三列皆有數字，但毛利率列口徑過舊且方向判錯（F8）；NRR 與非GAAP 營益率兩列扎實（126% 持平、+450bp） |
| `moat.competitors`（3 列） | 🔴 半空 — MDB 6 欄缺 5、DDOG 缺 4、Databricks 因未上市缺 5（此列合理）；等於整表只有 `strategy_note` 有內容（F10） |
| `moat.roic_durability.checkpoints`（4 題） | 🟢 實 — 四題皆有具名證據（97% 既有客戶續約、五年 $6B AWS 承諾、FY27 guide GM 74%、歐盟主權），第 4 題社會容忍度未偷懶帶過。唯客戶數 733 需改 828（F1） |
| `growth.segments`（2 列） | 🟡 — FY0/FY1 為實際與公司 guide（46.8B/60.7B 皆一手），FY2/FY3 明標「估計」且寫出遞減假設；`om_fy2e` 的「約 18%」無推導，屬全表唯一無錨數字 |
| `quality.dupont`（4 年） | 🟢 實且可驗 — 我逐年重算：−38.6×0.268×1.41＝−14.6 ✓／−29.9×0.342×1.59＝−16.3 ✓／−35.5×0.402×3.01＝−43.0 ✓／−28.4×0.513×4.76＝−69.3 ✓。四年恆等式全對，且 ROE 惡化歸因（權益因累虧＋買回萎縮 54.6→19.2 億）正確 |
| `quality.ccc`（4 年） | 🟢 實且可驗 — 127−0−10.1＝116.9 ✓／120.8−20.3＝100.5 ✓／92.5−50.8＝41.7 ✓／101.4−35.8＝65.6 ✓ |
| `governance.scorecard`（3 列） | 🟢 實 — Observe 收購 $5.962 億具日期、買回均價 $177.37 具口徑、買回收益率測試明寫未通過及門檻，且誠實標「資料不足無法評估」而非硬給等級 |
| `governance.capital_returns`（4 年） | 🟡 — buyback／dividend／capex 逐年有值，R&D 整欄 4/4 缺口（10-K 可得，屬採集懶） |
| `valuation.peers`（3 列） | 🔴 有假象 — CFLT 整列 null；DDOG EV/EBITDA 873x 明知是 EBITDA≈0 的假象仍留表；DDOG fwd PE 兩來源 96 vs 79.26 未裁決；MDB 快照為 2026-05-06（4 個月前） |

結論：**dupont／ccc／tam／checkpoints／scorecard 是真 sourced 且可驗算**（我實際重算了 dupont 與 ccc 全部 8 條恆等式，無誤）；**competitors 與 peers 兩表接近佔位**，capital_returns 與 segments 各有一欄空洞。

### (4) Bear 是否放寬 — **否，全面收緊。** 見 ⑥(b) 表列六項參數逐項對照。反而是我認為 Bear 偏苛（隱含 FY32 EV/S 1.5x < 上市以來最低 8.58x），但敏感度顯示放寬 Bear 也不改裁決。

### (5) 覆蓋矩陣 16 軸 — 見 ⑤，全 found、零 none／零 not_applicable，本軸 🟢 無 finding。

---

## QC-50 錯過成本反向 critic

**觸發確認**：裁決落觀望 ✓；gate①：前次同 ticker 觀望（2026-05-24 inception、2026-07-05、2026-09-03 連三份皆觀望），to-date 自 5/24 起約 +106%（>+30% 門檻）✓。gate②：`consensus_rev_3m_pct=2.2` 名目未達 +10%，**但該數字是財報前快照（F3）**，判斷物自身採用 +11.65% 的 guide 上調倍率建 Base 路徑，以財報後基礎 gate② 亦成立。**兩條 gate 實質全開。**

### 反駁「觀望」最強的兩點

**第一：兩個承重的「已充分定價」證據，用的都是被自己註記為過期的數字。**
`vs_current_pct=−8.53%` 與 `upside_short_pct=−15.0%` 全部錨在財報前的 $302–317 賣方均值；同一份證據包記載財報後目標價群聚 **$390–450**（Mizuho 425、BTIG 424、Needham 450、Rosenblatt 上調）。以財報後賣方為錨，現價是折價 10–27%。同理，`consensus_rev_3m_pct=2.2%` 讓「共識沒在上修」看起來像事實，但 Q2 non-GAAP EPS $0.62 vs 共識 $0.45（beat 38%）、product revenue guide $5.84B→$6.07B、非GAAP 營益率 guide 13.5%→14.5%——這是教科書級的共識上修前夜。**歷史上觀望最容易錯過的形態，正是「基本面連續加速 ＋ 共識大幅上修 ＋ 估值燈紅」三件同時發生**，而本份把其中兩件用過期數字壓成了中性。

**第二：三次觀望的 binding constraint 都是估值燈，而估值燈這次自己承認前兩次算錯。**
5/24（PEG 2.03、估值🟠）、7/5（Fwd PE ~97x、IRR 2.6%）、9/3（PEG 3.20、val🔴）——三次否決 SNOW 的都不是基本面惡化（每一份的 signal 都是 B、moat_trend 都是 →、runway 都是 🟢），而是估值尺。本份確認了那把尺在 GAAP-負公司身上**根本不該用**（核心裁定題 (1)）。也就是說：**一個三次都由同一把後來被判定為用錯的尺所產生的「觀望」，現在被 QC-49 用來壓住那把尺修正後的機械輸出。** 這是 QC-49 邊界④ 想處理卻沒涵蓋到的形態（誤用 ≠ 退役），是本輪最尖銳的錯過成本論證。期間股價自 inception 翻一倍。

### 這兩點的弱點（為何我仍不建議翻面）

1. **絕對報酬經濟性完全不隨估值燈改色而移動。** val 由 🔴 變 🟡 只是換了衡量「相對成長貴不貴」的尺，沒有改變任何一個現金流輸入。Base IRR 2.2%、AR 1.1、EV +6.6% 三個數字在兩份報告之間幾乎不動（2.3→2.2、1.0→1.1、6.4→6.6）。我做的 Bear 敏感度更關鍵：把最苛的 Bear（$43.2，隱含 EV/S 1.5x）整個換成 $140（−60%），EV 只由 +6.6% 升到 +15.0%、IRR 由 2.2% 到約 2.8%。**錯過成本論證要成立，必須在情境樹裡找到報酬，而不是在估值燈的顏色裡找。** 目前找不到——起始 164.6x 非GAAP PE 要求 re-rate 每年 −21.8% 才能讓 Base 走到 +11.7%。
2. **第二點的力道被 SBC 反噬。** 「那把尺用錯了」的正確結論是「SNOW 不該用 PE/PEG 衡量」，但同一個理由（SBC $456.4M > 非GAAP 營業利益 $237.0M）也意味著**情境樹裡那條非GAAP EPS 路徑本身就是被美化過的分子**。修正估值尺會讓相對估值變好看，同時應該讓人對絕對 EPS 路徑更懷疑，兩者方向相反。判斷物只做了前半。
3. **升級的載體不存在，且技術輸入是壞的。** row 8a（爆發候選）硬性要求 val∈{🟠,🔴}——val 一旦 🟡 反而失去 8a 資格；唯一路徑 row 9b 的節奏閘依賴 MA／RSI／26 週漲幅三個輸入，其中 `rsi14=36.06` 在 52 週新高當日不可能為真（F12）、`week26_return_pct` 為 None、且 9/3 當日同時留下 shooting star 與 gap-up-closed-red 兩個反轉燭型（證據包明載、判斷物完全未接線）。**在節奏輸入壞掉的當下升級，比在節奏輸入壞掉的當下承繼更危險。**
4. QC-50 依規則只能建議、不能強制翻面，fail-safe 方向為維持觀望。

### QC-50 結論與要求

**不建議翻面，維持 觀望｜追蹤。** 但要求兩件落檔，否則下一輪的錯過成本仍會建立在髒數字上：

- **(a) 修 F2／F3。** `upside_short_pct`／`upside_mid_pct`／`consensus_rev_3m_pct` 三個欄位目前被財報前快照污染，且都是 QC-50 下一輪的計分輸入。不修，下一份 DD 會再一次「看起來共識沒上修、賣方沒空間」。
- **(b) rearm 增列非價格觸發（連動 F14）。** 現行 re-arm 兩肢皆為壞形態：一肢是「PE 回落 70x（−41%）」——用了本報告宣告非權威的尺，且對一支剛創新高的股票近乎不可能；另一肢是 Databricks 相對優勢**未達**兩倍門檻（等於等壞消息）。**兩肢都成立的世界裡，SNOW 只會因為變糟才進場，不會因為變好而進場——那不是紀律，是永久觀望的保證。** 應增一條論點增強型觸發，例如：CoCo/CoWork 帳戶連兩季淨增 ≥2,000 **且**公司首度揭露 AI 相關 run-rate 絕對金額 ≥$1.0B（H1 的 5Y 驗證點提前兌現），或 non-GAAP 營益率連兩季超 guide 且 GM 止跌回 76%。

---

## 未及查證清單（查證預算 10/14 用畢，餘 4 輪保留）

1. **財報後 FY28／FY29 共識 EPS 實際數字** — stockanalysis 該欄為付費牆，證據包亦記為缺口。故 F3 的「共識應上修逾 10%」是以判斷物自身 guide 倍率＋Q2 beat 幅度推得，非直接觀測到的共識序列。**這是本報告 QC-50 gate② 判定的唯一軟肋。**
2. **SNOW 26 週前（約 2026-03-05）實際收盤價** — 搜尋回傳 2025/2026 資料混雜、不可用。26 週漲幅是否逾 100%（影響 row 8a 邊界與 F12）未能定案。
3. **828 家 $1M+ 客戶所對應的營收占比** — 8-K 給了家數與 +27% YoY，但未給「占約 68% 營收」的更新值；判斷物沿用的 68% 可能與 733 同期。
4. **Microsoft Fabric 的量化份額**（F11）— 只查到質性比較與 Gartner 引述（SNOW 40% 資料倉儲份額），未取得 Fabric 對 SNOW 的實際 win-loss 或帳戶流失數據。故 F11 列 🟡 而非 🔴。
5. **可轉債 $23 億（2027／2029 到期）的轉換價與潛在稀釋股數** — 未查，故無法評估其對情境樹每股數的影響。
6. **前份 `rearm_trigger` 第二肢「AI/agentic run rate 具體揭露且達門檻」的門檻原文** — `prior_meta` 只存了摘要句，未存門檻數字；我依「公司僅揭露帳戶數未揭露金額」判為未發火，若前份門檻其實是帳戶數口徑，此判定需重驗（影響 QC-49 承繼的第 6 條檢核）。

---

# R2 re-gate

> 2026-09-04 第二輪。範圍依協調者指定：①逐條核六條 🔴 落點＋抽核 F12／F14；②patch 有無引入新矛盾（decision_inputs↔decision_out、triggers↔kill_metrics／rearm、contradictions 歸因方向）。查證 1 輪 WebSearch（26 週基期價，未果），累計 11/14。未重跑 QC-41 四軸。

## R2 已確認修好

| R1 | 狀態 | 落點核對 |
|---|---|---|
| F1 | ✅（有殘留，見 R2-4） | `industry.bargaining.down`／`moat.trend_evidence`／`checkpoints[0]` 三處 828 已入，並補「+27% YoY」 |
| F2 | ✅ 並重算通過 | `upside_short_pct=-59.2`：FY28E 3.02 × 合理PE 48 ＝ 145.0 →(145.0−355.5)/355.5＝−59.2% ✓；`upside_mid_pct=-44.1`：4.14 × 48 ＝ 198.7 →−44.1% ✓。兩欄同 PE 基準、`appendix_a` 同步 ✓ |
| F3 | ✅ 數值 | 11.65（口徑註記缺，見 R2-5） |
| F4 | ✅ **（R1 誤判為未修，特此更正）** | 我第一次以「456.4／237.0」阿拉伯數字 grep 未命中，實際檔內以中文單位書寫。`governance.sbc.q2_fy27_sbc_vs_opinc` 已載「Q2 FY27 單季股權薪酬 4.564 億美元，超過同季非GAAP營業利益 2.370 億美元（年化約當營收比重近三成）」並點出非GAAP營益率改善很大程度來自 SBC 未計入；`premortem.blind_spots[4]` 新增「非GAAP 口徑失效路徑」。修得比我要求的更完整。（`valuation_dependent` 未連動，見 R2-6） |
| F5 | ✅ | `endo_ceiling` 20.3 |
| F6 | ✅（一條方向標錯，見 R2-3） | contradictions 5→12，補齊 bull/bear_5y_price、ev5y、irr_base、asym、max_dd、rearm 七條；`ev5y_pct` 與 `asym_ratio` 兩條誠實標「本欄微幅改善非收緊」而非硬套收緊，此處判斷品質好 |
| F7 | ✅ | 20.92／21.14 已入推導 |
| F8 | ✅ | 改季度非GAAP product GM 口徑 74.7% vs 約 76%＝−1.3pp，並寫明「年度數字滯後、季度更即時」的換尺理由 |
| F9 | ✅ | RPO 90.0 億 vs 共識 93.7 億（−3.9%）已補，且明說「本輪領先指標中唯一未達共識」 |
| F10 | ✅（合法部分不採納） | 873x 降為註解說明並將 `ev_ebitda` 置 null、CFLT 標排除。MDB／DDOG 毛利率等欄未填數而改標「證據包未涵蓋」——patch agent 禁搜，屬規則允許的不採納；**留給下輪 Stage 0 補採集** |
| F11 | ✅ | `moat.threats[3]` Fabric，level 🟡，並自承「本輪全文先前對此競爭者零提及、證據包未涵蓋其份額數據，僅方向性標記」——揭露誠實 |
| F13 | ✅ | `reasoning.valuation` 改為「4b.1 分母爭議檢查已通過（val_denominator_disputed=false，側A 論證所依賴的營收成長率分母本身非爭議數字），故裁決另以絕對報酬與情境樹經濟性為主要依歸」 |
| F14 | ✅（一項門檻仍虛，見 R2-8） | `rearm_trigger` 與 `triggers[3]` 一致改為「成長調整後 EV/Rev ≤0.45（現 0.62）或 Base 5Y IRR ≥8%（現 2.2%）為權威門檻，PE 70x／$211 僅供對照」——F14 的核心（把 re-arm 從已宣告非權威的尺搬到權威尺）達成 |

## 新矛盾掃描

- `triggers[] ↔ kill_metrics[] ↔ rearm_trigger`：**無矛盾** ✓。triggers#1/#2/#3 門檻與 kill_metrics 三條逐字對齊；triggers[3] 與 `decision_out.rearm_trigger` 文字一致。
- `scenario_meta ↔ decision_inputs`：**無矛盾** ✓。irr_base 2.2／ev5y 6.6／asym 1.1 三處仍三方一致，patch 未動情境輸入。
- `decision_inputs ↔ decision_out`：**有重大新矛盾**，見 R2-1／R2-2。
- `contradictions[]` 歸因方向：一條標錯，見 R2-3。

## FINDINGS-R2

| # | 嚴重度 | JSON 路徑 | 一句話 | 最小修法 |
|---|---|---|---|---|
| R2-1 | 🔴 | `decision_inputs.momentum_overheated` | 由 False 改為 **True，但規則兩條判準皆未成立**——附錄 A 過熱定義為「RSI 14d > 70 **或** 4 週漂移 > +10%」，實測 `drift_4w_pct=7.86`（<10）、`rsi14=36.06` 為壞讀數（不可用 ≠ >70）；26 週 +106.4% 不屬過熱定義（那是 row 8a 的獨立條件）。F12 要的是「壞讀數標為不可用」，patch 卻讀成「所以過熱成立」 | 回填 `null`（bool 三態，禁 "unknown"）或 False，並在 `reasoning` 註明「4 週漂移 7.86% < 10% 未達門檻；RSI 讀數與 52 週新高互斥故第一條件無法檢核」 |
| R2-2 | 🔴 | `decision_out.audit_rows`（row 5／row 9b）＋`row_hit`＋`exec_line`＋`decision_inputs.qc49_inherit_prior` | R2-1 的連鎖：**row 5 `hit=true` 與 row 9b `hit=true` 同時成立**，但 row 9b 的前提是「無 Veto」，row 5（動能過熱→≥觀望）正是 Soft Veto，兩者互斥。若 row 5 真命中，觀望是**機械直出**、QC-49 承繼根本不需動用，而 `row_hit`「9b→承繼前次裁決(觀望)」、`exec_line`「矩陣原始輸出…指向可分批建倉之路徑」、`qc49_inherit_prior=true`、`contradictions[4]` 整段承繼論述全數失效 | **解(A)（推薦，變動最小且規則有據）**：修 R2-1 → row 5 回 false → row 9b 維持 true → `row_hit`／`exec_line`／QC-49 全段沿用 R1 已認可版本。**解(B)（若堅持 True）**：row 9b 改 false（basis 註「row 5 Soft Veto 阻斷」）、`row_hit` 改「row 5（動能過熱）→觀望」、`qc49_inherit_prior` 改 false、`exec_line` 與 `contradictions[4]` 整段重寫。**不得維持現狀**。另回報：`validate_judgment.py` 對此互斥組合亦 PASS，與 F6 同屬 v16 機械閘缺口 |
| R2-3 | 🟡 | `contradictions[10]`（max_dd_pct 對帳條目） | 歸因方向標反：前份 −86.0% → 本次 lo −80／hi −55，回撤**變淺＝放寬**，條目卻寫「方向為收緊」，同一句又自承「數字上收斂」，前後打架。§12 3b 要防的正是這種標示 | 改標「方向為放寬（回撤深度收斂，且口徑由單值改為區間），惟 `path_risk` 維持 🔴，本輪不據此下修風險評等」 |
| R2-4 | 🟡 | `reasoning.moat` | F1 只修了三個資料欄位，推導文字仍寫「733家客戶百萬美元以上營收穩定」；`reasoning` 會被呈現層原樣鋪進 `<div class="reasoning">`，等於錯數字仍會上站 | 733→828 |
| R2-5 | 🟡 | `decision_inputs.consensus_rev_3m_pct` | 值改 11.65 但**全檔無任何口徑註記**（"11.65" 僅出現該欄一次，無「guide 隱含」「非實測共識」字樣，亦無 contradictions 條目）。此欄是 QC-50 gate② 的機械輸入，而 11.65 是由 guide 上調倍率反推的**估算**非觀測值 | 在 `reasoning.valuation` 或新增 contradictions 條目寫明「11.65% 係 guide 上調倍率（product revenue +3.9% × 非GAAP營益率 +7.4%）隱含之估算，財報後實際共識序列證據包未涵蓋」 |
| R2-6 | 🟡 | `decision_inputs.valuation_dependent`／`reasoning.premortem` | F4 的證據落在描述層，未回到決策欄。`valuation_dependent` 仍為 False，`reasoning.premortem` 仍以「非估值依賴型」作為不強制砍倉的三理由之一——但新入檔的事實是「非GAAP營益率改善很大程度來自 SBC 未計入」，這正是估值依賴的典型形態。F4 原文要求「明寫為何仍 False（或翻 True）」，此問未答 | 於 `reasoning.premortem` 補一句正面作答（例：SBC 占比軌跡下行且 FCF margin 23-27% 為真現金，故不判估值依賴型），或翻 True 並連動 row 7a |
| R2-7 | 🟡 | `decision_inputs.week26_return_pct`／`premortem.blind_spots[3]` | 填入 106.4（現承重：row 8a basis 明載 week26=106.4），但 `blind_spots[3]` 原文未動、仍寫「26 週前實際收盤價證據包未涵蓋…本輪無法驗證」——一邊宣稱查不到、一邊填了一位小數。我兩輪 WebSearch 亦未能外部驗證此值 | 改寫 blind_spots[3] 說明 106.4 的推導來源（週線快取／自算），或將該值標為估算；二者擇一，不可並存 |
| R2-8 | 🟡 | `decision_out.rearm_trigger`（第四肢） | 新增的非價格觸發「AI run rate 揭露達門檻」**沒有門檻數字**，正是 QC-50(b) 要避免的形態（前份同一肢即因無數字而無法判定是否發火，見 R1 未及查證#6） | 補具體數字，例：AI 相關 run-rate 絕對金額首度揭露且 ≥$1.0B，或 CoCo／CoWork 帳戶連兩季淨增 ≥2,000 戶 |

## GATE-R2: FAIL

- **裁決不變**：觀望｜追蹤 仍是正確終局，R2 全部 findings 皆不改變方向；F1–F14 的實質修補品質高（F4／F8／F9／F14 修得到位，F6 的七條新條目歸因紮實）。
- **但不可上站**：R2-1／R2-2 是 patch 引入的**新**矛盾，且是最不能留的一種——決策矩陣同時宣稱一條 Soft Veto 命中與一條「無 Veto」路徑命中，而 `row_hit`／`exec_line`／QC-49 整段敘述建立在其中一半上。兩者互為因果，**單欄回填 `momentum_overheated`（解 A）即同時解掉**。
- **re-gate 範圍**：只核 `decision_inputs.momentum_overheated`、`audit_rows` row 5／row 9b、`decision_out.row_hit`／`exec_line` 四處是否自洽；R2-3～R2-8 六條 🟡 可併同一輪修完但不需我逐條複核。**不需重跑 QC-41 四軸，不需重跑 QC-50。**

## R2 未及查證

1. **SNOW 2026-03-05 前後收盤價**（R2-7）——第二輪再查一次仍無果（搜尋結果混入 2025 年資料）。106.4% 目前無外部錨。
2. 財報後 FY28／FY29 實際共識 EPS 序列（R1 未及查證#1 延續）——`consensus_rev_3m_pct=11.65` 因此仍是估算（R2-5）。
