# v19 判斷檔契約：誰填、誰投影（WP-H1，2026-09-11）

> 契約本體在 `scripts/dd_schema/judgment.schema.json` 的頂層 `v19_contract` 區塊；轉接程式是 `scripts/dd_project.py`（唯一一處）。**舊形狀（`meta.contract` 沒標 `v19`）一律照舊驗、照舊渲染**，本檔不適用。

## 一、判別與流程

`meta.contract` ＝ `"v19"` 是唯一判別。流程：

1. 判斷者寫 v19 判斷檔（judge-owned 欄，見第二節）。
2. `dd_project.project()` 投影成**舊形狀視圖**（第三節的 P-01…P-25）。
3. 既有檢查與渲染全部讀那個視圖：`validate_judgment`（J1／J2／J6／同源／leak／展開區塊／反證三視角）、`gen_dd_tables`（dd-meta ＋ 七表）、`dd_brief`、`dd_bundle` 的 `gate_view`、`dd_delta` 的 DRIFT_WATCH 對帳、`dd_decision`（對 `dd_project.py view` 的輸出跑矩陣）。

保留的是**檢查語義**，不是原讀檔路徑。不靠模型再寫一份舊格式。

## 二、欄位歸屬表

### 2.1 judge-owned（判斷者必須明示）

| 區塊 | 內容 | 為什麼不能由程式算 |
|---|---|---|
| `meta`／`oneliner`／`facts_ref`／`scenario_ref` | 標頭與兩個輸入檔指標 | — |
| `thesis` | H1–H3、R1–Rn、Single Thing | 出手點①：假設、門檻、漂移觸發 |
| `answers.q1_business` | 結論句＋短理由＋`fact_refs`＋`revenue_quality`／`unit_econ_note`／`archetype`／`industry`／`single_thing` | 出手點①：商模門檻與唯一致命數字 |
| `answers.q2_moat` | ＋`moat.mechanism`／`trend`／`trend_evidence`／`grade`／子評分／`competitor_notes`／`spread_notes`（選填）／`peer_na_reason`（查無或不適用時必填）／`threats`／`roic_durability` | 出手點②：優勢機制、持續性、子評分與重要性。**等級不可由分數推**——實檔 8.5 分同時對應 A 與 B。2026-09-11（WP-H2-1）：同業的**數字、期間、口徑、來源搬進 `facts.peer_comparison`**，判斷者只寫每家一句 `strategy_note`（有沒有本錢打價格戰、策略定位）與口徑判讀 `spread_notes` |
| `answers.q3_growth` | ＋`growth.driver_mix`／`runway_post_y5`／`endo_ceiling_basis`／`segments` | 出手點②：未來滲透率、第二曲線是否可信、缺口歸因 |
| `answers.q4_capital` | ＋`capalloc.items[]`（逐項適用性與輸入）／`governance`／`quality` | Codex 表：併購 NOPAT 歸屬、ROIIC 代理、不可比資料與不適用項的處理由判斷者決定 |
| `answers.q5_valuation` | ＋`valuation.basis`（正常化口徑）／`val_light`／`peg`／`percentile_5y`／`denominator_disputed`＋`denominator_note` | 盈餘是否正常化、一次性因素、分母爭議 |
| `answers.q6_how_wrong` | ＋`trap.verdict`／`label` | 陷阱定性 |
| `scenario_inputs` | 三支 EPS 路徑、終端倍數、機率、`terminal_label`、`max_dd.lo/hi/basis`、`basis`、`endo_ceiling_exceeded` | EV／IRR／AR 是算術，但路徑、倍數、機率、Max DD 範圍與理由是判斷 |
| `counter_evidence` | 三視角反證、矛盾裁定（含 `cause`）、`triggers[]`、`kill_metrics[]`、`action_conditions.rearm_trigger`／`exec_line` | 反證與行動條件的唯一居所 |
| `decision_inputs` 九欄 | `signal`／`ma`／`cycle_position`／`cycle_verdict`／`thesis_irreconcilable`／`valuation_dependent`／`market_wrong_reason_given`／`momentum_overheated`／`cycle_gates_pass` | 判斷密集欄；`signal` 的 QC-31 六步、`ma` 的週線六態都要讀圖判斷 |
| `appendix_a` 七欄 | `growth_durability`／`quality_score`／`ai_risk`／`long_term_confidence`／`fpe_fy2`／`peg_fy2`／`stress` | 品質分含正常化判斷；`fpe_fy2`／`peg_fy2` 財年口徑未定義不得同源投影 |
| `eps_meta` | 共識三年錨 | 口徑與家數要人看 |
| `catalysts`（選填） | 行事曆事件 | 影響度是判斷；缺席時才由程式從帶日期的 triggers 投影 |

### 2.2 由程式投影（判斷者**不要填**）

| 舊形狀欄 | 來源 | 規則 |
|---|---|---|
| `archetype`／`industry` | `answers.q1.verdict_values` | P-04／P-05 |
| `moat`（含 `roic_durability`） | `answers.q2.verdict_values.moat` | P-06（`combined`／`score` 可由平均補） |
| `growth` | `answers.q3.verdict_values.growth` | P-07 |
| `quality`／`governance` | `answers.q4.verdict_values` | P-08／P-09（`capalloc_grade` 由計分卡加總，P-22） |
| `valuation` | `answers.q5.verdict_values.valuation` | P-10（分母爭議兩欄搬去 `decision_inputs`） |
| `trap_analysis` | `answers.q6.verdict_values.trap` | P-11 |
| `premortem` | `counter_evidence.blind_spots` ＋ `scenario_inputs.max_dd` | P-12（`path_risk` 由 `lo` 算，P-21） |
| `contradictions`／`triggers`／`kill_metrics`／`evidence_dismissed` | `counter_evidence` | P-13…P-16 |
| `decision_out.rearm_trigger`／`exec_line` | `counter_evidence.action_conditions` | P-17；其餘矩陣欄由 `dd_decision.py` 寫 |
| `reasoning.{industry,moat,growth,governance,valuation,premortem}` | 六問的 `reasoning` | P-18 |
| `plain.six.*` | 六問的 `verdict`（結論句只寫一次） | P-19 |
| `decision_inputs` 十三欄＋分母兩欄 | 見下表 | P-20；判斷者填了非 null → `validate_judgment` FAIL |
| `catalysts`（判斷者未給時） | 帶日期的 `triggers[]` | P-23（`impact` 留空，不捏造） |
| `scenario.json`（`dd_scenario.py` 的輸入檔） | `scenario_inputs` ＋ facts 的價格與共識 | P-25，`dd_project.py scenario` |

`decision_inputs` 的十三個機械欄與其來源：

| 欄 | 來源 |
|---|---|
| `trap` | `answers.q6.verdict_values.trap.verdict` |
| `val` | `answers.q5.…valuation.val_light` |
| `moat` | `answers.q2.…moat.grade` |
| `moat_trend` | `answers.q2.…moat.trend` |
| `runway_post_y5` | `answers.q3.…growth.runway_post_y5` |
| `capalloc_grade` | `answers.q4.…capalloc.items[]` 加總（P-22） |
| `archetype` | `answers.q1.…archetype.primary` |
| `price_at_dd` | facts `f_price_at_dd` |
| `week26_return_pct` | facts `f_week26_return_pct` |
| `consensus_rev_3m_pct` | facts `f_consensus_rev_3m_fy1_pct` |
| `asym_ratio`／`irr_base_pct`／`ev5y_pct` | 一律 null，由 scenario 權威重算（既有契約） |
| `val_denominator_disputed`／`val_denominator_note` | `answers.q5.…valuation.denominator_disputed`／`denominator_note` |

## 三、投影規則清單（`dd_project.py`）

| 編號 | 規則 | 只做算術／映射的界線 |
|---|---|---|
| P-01 | `meta.contract` 不是 `v19` → 原物件回傳（identity） | 舊形狀零改動 |
| P-02 | `meta` 原樣搬（保留 `contract` 標記） | dd-meta 只取 ticker／date／schema |
| P-03 | `oneliner`／`thesis`／`appendix_a`／`eps_meta`／`scenario_ref` 原樣搬 | — |
| P-04 | `archetype` ← 問一 | — |
| P-05 | `industry` ← 問一 | — |
| P-06 | `moat` ← 問二；`combined` 缺時取 execution／pricing 平均、`score` 缺時取 `combined` | **`grade` 不推**（實檔反例） |
| P-26 | `moat.spread_table`（度量為列）／`moat.competitors`（對手為列）← `facts.peer_comparison` ＋ 判斷者的 `competitor_notes`／`spread_notes`。對名先精確比對、再比對前綴（判斷者寫 `EME（EMCOR）`、facts 是 `EME`）。**facts 沒有同業資料時兩張表都不生**（不放空表假裝比過） | 只搬數字、不換算、不補缺的度量；對不上名就留空 note，由必要項目檢查報缺 |
| P-07 | `growth` ← 問三（`driver_mix`／`endo_ceiling_basis` 原樣留著供散文引用） | — |
| P-08 | `quality` ← 問四 | 缺就空物件，E9 顯示未提供 |
| P-09 | `governance` ← 問四；`scorecard` 缺時由計分卡逐項生成 | 逐項文字照抄判斷者的 `input` |
| P-10 | `valuation` ← 問五（分母兩欄移出） | — |
| P-11 | `trap_analysis` ← 問六（只 verdict＋label） | — |
| P-12 | `premortem` ← 反證紀錄 ＋ `scenario_inputs.max_dd` | — |
| P-13…P-16 | `contradictions`／`triggers`／`kill_metrics`／`evidence_dismissed` ← `counter_evidence` | — |
| P-17 | `decision_out` ＝ 矩陣欄 ＋ `action_conditions` 的 rearm／exec_line | 矩陣欄由 `dd_decision.py` 寫 |
| P-18 | `reasoning` ← 六問 `reasoning` | 缺就缺，不生成理由 |
| P-19 | `plain.six` ← 六問 `verdict` | 不改寫、不潤飾 |
| P-20 | `decision_inputs` ＝ judge-owned 九欄 ＋ 覆寫層 ＋ 十三個投影欄 | 事實欄取 facts，facts 缺時退回判斷檔自帶值 |
| P-21 | `path_risk` ← `max_dd.lo`（🟢 ≥−30／🟡 −30～−50／🔴 <−50） | 切點是既有規則，不是新判準 |
| P-22 | `capalloc_grade` ← 計分卡（適用項 ≥2 過＝A、1＝B、0＝C） | 一項都不適用 → 留空；判斷者給 `grade` 就以判斷者為準 |
| P-23 | `catalysts` 缺席時 ← 帶日期的 `triggers[]` | `impact` 留 null |
| P-24 | 視圖加 `_projected_from`＝`v19` 供辨識 | 不進 dd-meta（白名單欄） |
| P-25 | `scenario.json` ← `scenario_inputs` ＋ facts | 判斷者沒給的欄不寫 |

**鐵律**：缺的判斷值就留空，讓對應檢查 FAIL／WARN，不填預設。評分與燈號（moat 合併分、`capalloc_grade`、`path_risk`）只在判斷者給了子輸入時才算；`moat.grade`、`val_light`、品質分、`signal` 一律由判斷者明示。

## 四、v19 專屬檢查（`validate_judgment.py::v19_contract_checks`）

1. `v19_contract` 形狀（schema 子集直譯器）。
2. **事實檔擋門（WP-H2-1，2026-09-11）**：`facts_ref` 解析不到、不是合法 JSON、或事實檔自身過不了 `dd_facts.check` → **FAIL**。H1 時期這裡只 WARN，Codex 用 fixture 重現「事實檔不存在仍 0 FAIL」，本輪升為硬擋——沒有事實表就沒有可追溯性，不得組頁。
3. `answers[].fact_refs[]` 的 id 必須在 `facts.json` 找得到（斷鏈＝FAIL）。
4. `decision_inputs` 的十三個投影欄不得被填成非 null（同一件事不准兩邊都填）。
5. **必要項目是否有回答（`v19_required_items_checks`，取代 `minItems`）**：§5.R 四檢查點（需求基礎值／決策層級／價值鏈分配／社會容忍度）各要一個回答——判讀句 `text` 或不適用理由 `not_applicable_reason`，**空物件不算**；同業對照要嘛 `moat.competitor_notes` 每家一句 `strategy_note`、要嘛 `moat.peer_na_reason` 寫明為何查無或不適用。
6. **J2 必須真的執行（WP-H2-1）**：`scenario_meta` sidecar 找不到、或 Max DD 恆等式因缺 `price_at_dd`／`bear_5y_price`／`max_dd.lo` 而沒算 → **FAIL**（舊形狀維持 WARN）。「沒算」與「算過通過」不可同樣算過關。
7. J2 終端年檢查升 FAIL（見 `decision_inputs.md` §7）。

## 四之二、格式正規化（`dd_project.py normalize`，WP-H2-1）

判斷段改一回合交卷後，剩下的失敗多半是形狀。`normalize` 只准修三類：**①路徑**（`facts_ref`／`scenario_ref` 相對 → 絕對）**②確定的欄名映射**（`answers.q1`→`q1_business`、`facts`→`fact_refs`、頂層 `triggers`／`contradictions`／`kill_metrics`／`evidence_dismissed` → `counter_evidence.*`、`scenario`→`scenario_inputs` 等一對一無歧義項）**③單物件包陣列**（依 `v19_contract` 宣告為 array 的路徑，給了單一物件就包起來）。

**一律不補**：理由、評級、`false`、門檻、機率，以及任何缺值。修不掉 → 讓 validate FAIL → 一輪 patch map（**上限 1**）→ 仍 FAIL 就停下印「交指揮者」、**不回退 loop、不發布**（`ddreport.py::_judge_finalize_after_check`）。

## 五、required 條目數

| 形狀 | required 條目 | 說明 |
|---|---|---|
| 舊形狀（v18 基準） | 137 | `judgment.schema.json` 主體 |
| v19 judge-owned | 145 | 其中 **17 條是 `scenario_inputs`**——那批假設 v18 時代寫在另一個檔（`scenario.json`）、沒算進 137。扣掉後同尺為 **128**（−9）。真正省下的不是 required 條目數，是**不用重填**的東西：13 個 decision_inputs 機械欄、7 個 appendix_a 同源欄、`plain.*`、`reasoning` 六鍵的另一份抄寫、`trap_analysis`／`premortem`／`contradictions`／`triggers` 的第二居所，以及整份 `scenario.json`。 |
