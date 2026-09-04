# judgment.json → dd-meta 欄位對映表（WP1c）

> 本檔是 `scripts/gen_dd_tables.py` 產 `dd-meta.html` 的權威對照表，也是 `scripts/validate_judgment.py` 與 `scripts/dd_judgment_from_meta.py`（反推）共用的欄名依據。dd-meta schema 本身（v15.0）不動，本檔只記錄「這個 dd-meta 欄，在 judgment.json 裡唯一住在哪裡」。

## 一、v12 必填 22 欄

| dd-meta 欄 | judgment.json 路徑 | 備註 |
|---|---|---|
| `ticker` | `meta.ticker` | |
| `schema` | `meta.schema` | 固定 `v15.0`（判斷機器凍結） |
| `date` | `meta.date` | |
| `price_at_dd` | `decision_inputs.price_at_dd` | 與 `meta` 不重複儲存；`meta` 只留 ticker/date/schema |
| `signal` | `appendix_a.signal`（＝`decision_inputs.signal`，兩處同源） | 附錄 A 機械評等 |
| `trap` | `trap_analysis.verdict`（＝`decision_inputs.trap`） | |
| `trap_label` | `trap_analysis.label` | |
| `moat` | `moat.grade`（＝`decision_inputs.moat`） | 字母，非數字 |
| `val` | `appendix_a.val`（＝`decision_inputs.val`） | |
| `ma` | `appendix_a.ma`（＝`decision_inputs.ma`） | |
| `fpe_fy2` | `appendix_a.fpe_fy2`（＝`valuation.fwd_pe`） | |
| `pct_5y` | `appendix_a.pct_5y`（＝`valuation.percentile_5y`） | |
| `peg_fy2` | `appendix_a.peg_fy2`（＝`valuation.peg`） | |
| `upside_short_pct` | `appendix_a.upside_short_pct`（＝`valuation.upside_short_pct`） | |
| `upside_mid_pct` | `appendix_a.upside_mid_pct`（＝`valuation.upside_mid_pct`） | |
| `stress` | `appendix_a.stress`（`{pass,total}`） | |
| `moat_score` | `moat.score`（＝`appendix_a.moat_score`） | 1-10 |
| `growth_durability` | `appendix_a.growth_durability` | 1-10 |
| `quality_score` | `appendix_a.quality_score` | 1-10 |
| `ai_risk` | `appendix_a.ai_risk` | |
| `long_term_confidence` | `appendix_a.long_term_confidence` | |
| `verdict` | `appendix_a.verdict` | 與 `signal` 常同值 |
| `oneliner` | 頂層 `oneliner` | ≤200 字 |

**`scenario_ref` 的落地形狀（WP1c 判斷）**：草案 §3.2 只寫 `"scenario_ref":"{T}_{D}.scenario.json"`，未定形狀。WP1c 落地為指向 `scripts/dd_scenario.py --meta` 的**輸出**檔（不是它的輸入檔）——即已含 `bull_5y_price`／`bear_5y_price`／`p_bull_pct`／`p_bear_pct`／`upside_5y_pct`／`ev5y_pct`／`irr_base_pct`／`asym_ratio`／`scenario_tree` 的 JSON，這樣 `gen_dd_tables.py` 與 `validate_judgment.py`（重用 `dd_scenario.check_meta()`）都能直接消費，不必重新跑一次情境樹輸入格式的 schema。`gen_dd_tables.py` 也接受 `--scenario-meta FILE` 明示覆蓋（優先於 `scenario_ref`）。

## 二、v13 必填 5 欄（決策層）

| dd-meta 欄 | judgment.json 路徑 |
|---|---|
| `dca_verdict` | `decision_out.verdict` |
| `dca_role` | `decision_out.role` |
| `moat_trend` | `moat.trend`（＝`decision_inputs.moat_trend`） |
| `runway_post_y5` | `growth.runway_post_y5`（＝`decision_inputs.runway_post_y5`） |
| `ev5y_pct` | `decision_inputs.ev5y_pct`（來源＝`scenario_ref` 產物 `ev5y_pct`，寫入時已同步） |

## 三、v13 選填欄

| dd-meta 欄 | judgment.json 路徑 | 備註 |
|---|---|---|
| `irr_base_pct` | `decision_inputs.irr_base_pct` | scenario 產物 |
| `max_dd_pct` | `premortem.max_dd.lo` | 範圍下界（較深的負值） |
| `asym_ratio` | `decision_inputs.asym_ratio` | scenario 產物 |
| `bull_5y_price` / `bear_5y_price` | scenario 產物直接貼（judgment.json 本身不重存，`gen_dd_tables.py` 讀 `--scenario-meta` 檔） | AR Live 掛單輸入 |
| `p_bull_pct` / `p_bear_pct` | 同上，scenario 產物直接貼 | |
| `catalysts` | 頂層 `catalysts[]` | 逐項同形狀直接貼 |
| `base_eps_path` | `eps_meta.base_eps_path` | |
| `fy_end_month` | `eps_meta.fy_end_month` | |
| `eps_basis` | `eps_meta.eps_basis` | |
| `endo_growth_ceiling` | `moat.roic_durability.endo_ceiling` | |
| `capalloc_grade` | `governance.capalloc_grade`（＝`decision_inputs.capalloc_grade`） | |
| `moat_execution` | `moat.execution` | |
| `moat_pricing_power` | `moat.pricing` | |
| `upside_5y_pct` | scenario 產物 `upside_5y_pct`（＝Base 案 5Y%） | |
| `archetype` | `archetype.primary`（＝`decision_inputs.archetype`） | |
| `rearm_trigger` | `decision_out.rearm_trigger` | ≤120 字 |
| `cycle_position` | `decision_inputs.cycle_position` | 僅循環 archetype 填 |
| `cycle_verdict` | `decision_inputs.cycle_verdict` | 僅循環 archetype 填 |
| `industry_clock_phase` | `industry.clock_phase` | |
| `kill_metrics` | 優先讀頂層 `kill_metrics[]`（若存在，逐項直接貼，無損）；不存在時退回從 `triggers[]` 減碼／清倉／風險列機械轉譯（見下方§四） | 見下方「kill_metrics 兩種居所」 |
| `scenario_tree` | scenario 產物直接貼（`--scenario-meta` 輸出的 `scenario_tree` 欄） | |

### kill_metrics 兩種居所（WP1c 對草案的落地判斷，非規則變動）

設計稿 §3.2 只寫「dd-meta `kill_metrics[]`＝triggers 的減碼／清倉／風險列」（同源規則）。這是**寫新報告**時的紀律（Stage 1 agent 從 triggers 表机械推導）。但 `dd_judgment_from_meta.py`（回溯反推既有 v15 DD）發現：既有 dd-meta 的 `kill_metrics[]` 本身就是獨立欄位，且無法從既有 triggers 表無損還原（triggers 表的「指標與門檻」欄是 `metric`+`threshold` 合併顯示，反解會丟失 `metric` 短標籤）。故 `gen_dd_tables.py` 採**雙居所＋優先序**：頂層 `kill_metrics[]`（若 judgment.json 提供）優先、無損直貼；只有在該欄缺席時才退回從 `triggers[]` 機械轉譯（可能產生 `metric` 為空字串——見 `validate_judgment.py` 不對此欄硬性擋）。新報告（Stage 1 產出）建議只餵 `triggers[]`、不重複填頂層 `kill_metrics[]`，讓機械轉譯生效；回溯反推的 judgment.json 兩者都會填（頂層 `kill_metrics[]` 為權威、`triggers[]` 中的減碼/清倉/風險列可能是 dd_judgment_from_meta.py 無法百分之百切回原 8 欄 E12 表的近似值）。

## 四、同源規則的機械轉譯（`gen_dd_tables.py` 實作依據）

- **`kill_metrics[]`** ＝ `triggers[]` 中 `type` ∈ {`風險`, `減碼`, `清倉`} 的列，逐列轉譯：`metric`←`triggers[i].metric`、`bear_threshold`←`triggers[i].threshold`、`window`←`triggers[i].source_freq`（找不到頻率格式時留空字串）、`source`←`triggers[i].maps_to`、`last_status` 不機械推導（judgment.json 未提供欄位時省略，not fabricated）。
- **`rearm_trigger`** ＝ `decision_out.rearm_trigger`（若空，退回 `triggers[]` 中 `type`＝`估值rearm` 或 `action` 含「進場首倉」的那一列 `action` 文字）。
- **`catalysts[]`** ＝ 頂層 `catalysts[]` 直接貼（judgment.json 已是 dd-meta 同形狀，不再從 `triggers[]` 二次轉譯——與 SKILL.md 條文「⏰ 有日期列」的散文版本不同，實測（SNOW/DELL/AVGO）顯示 catalysts 常含 triggers 表沒有的事件，故 v16 把兩者列為**獨立居所**，此為 WP1c 對草案的落地判斷，非規則變動）。

## 五、E2／E12 表與 judgment.json 的對應

- **E2（§2.B 三假設表）** ＝ `thesis.H[]`（3 列，欄位＝`text`/`2y`/`5y`/`10y`/`threshold`/`source`/`drift_rule`）。
- **E12（§13 末監測與觸發器表）** ＝ 頂層 `triggers[]`（欄＝`n`/`text`/`type`/`maps_to`/`metric`/`threshold`/`action`/`source_freq`/`date`）。**「類型」欄渲染時優先用選填的 `type_display`**（逐字保留原「類型」儲存格文字）——實測（SNOW／DELL／AVGO 2026-09-03）證實「類型」欄的括號附註是 writer 自由發揮（SNOW 把 H/R 編號塞進括號、DELL/AVGO 留純 enum、AVGO 甚至出現「假設驗證（上行）」這種與 H/R 編號無關的自訂標籤），不是 `maps_to` 的機械函數；`type` 本身維持乾淨 enum（供 `dd_decision.py` 等矩陣腳本讀取），`type_display` 缺席時才退回「`type` ＋ 從 `maps_to` 解析出的 H/R token」的盡力重建。
- **附錄 A 表（`appA-table.html`）** ＝ `appendix_a.*`（品質分／估值燈／MA／trap 一列式）。
- **`audit.html`（`<details class="audit">`）** ＝ `decision_out.audit_rows[]`（若為空陣列則整段略過，不渲染空殼）。

## 五之二、七表來源（`gen_dd_tables.py` WP1c 修法1，E3/E5/E6/E7/E8/E9/E10）

`gen_dd_tables.py` 從 judgment.json 機械生成 QC-38「可見表格清單」中商業本質七表，各表輸出 `{out}/e{N}.html`（`<table id="e{N}">…`），由 `render_dd.py --assemble` 注入對應 prose 段（見 render_dd.py 內 `_ASSEMBLE_ORDER` 旁的 marker 對照）。欄名為 WP1c 落地判斷，schema `required`/`minItems` 已鎖定：

| 表 | 來源路徑 | items 欄位 | 注入段 |
|---|---|---|---|
| E3（逐段TAM/SAM＋利潤池） | `industry.tam_table[]`（minItems 1） | `segment`／`tam_now`／`tam_5y`／`penetration_pct`／`cagr_pct`／`value_chain_position`／`profit_pool_shift` | s3（`<!-- E3 -->`） |
| E5（二維評分＋Moat-to-Numbers） | `moat.{execution,pricing,combined,grade}` 摘要列＋`moat.spread_table[]`（minItems 1） | spread_table：`driver`／`metric_now`／`metric_hist_avg`／`spread`／`moat_linkage` | s5（`<!-- E5 -->`） |
| E6（對手P&L對照） | `moat.competitors[]`（minItems 1，schema 必填 8 欄） | `name`／`rev_growth`／`gm`／`om`／`rd_intensity`／`fcf_margin`／`net_cash`／`strategy_note` | s5（`<!-- E6 -->`） |
| E7（§5.R四檢查點） | `moat.roic_durability.checkpoints[]`（minItems 4）＋同物件 `quadrant`/`roiic`/`reinvest_rate`/`endo_ceiling`/`formula_note` 摘要列 | checkpoints：`n`／`question`／`status`／`evidence` | s5（`<!-- E7 -->`） |
| E8（分部前瞻build） | `growth.segments[]`（minItems 1） | `segment`／`fy0_rev`／`fy1e_rev`／`fy2e_rev`／`om_fy0`／`om_fy1e`／`om_fy2e`／`eps_contribution_pct` | s6（`<!-- E8 -->`） |
| E9（DuPont＋CCC合一） | `quality.dupont[]`（minItems 1）與 `quality.ccc[]`（minItems 1），依 `year` 合併 | dupont：`year`／`net_margin`／`asset_turnover`／`leverage`／`roe`；ccc：`year`／`dso`／`dio`／`dpo`／`ccc` | s7（`<!-- E9 -->`） |
| E10（資本配置track） | `governance.capital_returns[]`（minItems 1，逐年）＋`governance.scorecard[]`（minItems 1，附於表後列點） | capital_returns：`year`／`buyback`／`dividend`／`capex`／`rd`（選填）；scorecard：`year`／`action`／`rationale`／`grade` | s9（`<!-- E10 -->`） |

E3/E5/E6/E7/E8/E9/E10 缺對應 judgment 子物件或子物件為空陣列 → `validate_judgment.py`（schema `required`＋`minItems`）FAIL；`verify_dd_math.py` 對 v16 產出（dd-meta `"pipeline":"v16"`）另外檢查渲染後 HTML 是否真的有 `<table id="e3">`…`id="e10">`（防止 judgment 有資料但呈現層漏注入）。

## 六、v16 新增、dd-meta 沒有的 `decision_inputs` 七欄

`thesis_irreconcilable`／`valuation_dependent`／`market_wrong_reason_given`／`week26_return_pct`／`momentum_overheated`／`cycle_gates_pass`／`consensus_rev_3m_pct` 是決策矩陣（`dd_decision.py`，WP1b）需要但 dd-meta 從未落欄的中間變數，**不進 dd-meta**，只在 `judgment.json` 內供矩陣腳本讀取；反推工具（`dd_judgment_from_meta.py`）一律填 `null`（回溯反推，無法從既有 dd-meta 取得）。
