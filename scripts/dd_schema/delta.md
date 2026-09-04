# dd_delta.py — delta.json 欄位與規則表

零 LLM 重跑差異引擎；比對 prior 來源包（`{T}_{PRIOR_D}.evidence.json`＋`.judgment.json`＋`prose/`）與新
`evidence.json`，輸出下一輪 Stage 1/2 該重看哪些欄位／段落，而非整份重寫。

## delta.json 欄位

| 欄位 | 內容 |
|---|---|
| `prior` | `{dir, date, judgment_path, evidence_path}`，指回輸入的 prior 包 |
| `numbers_changed[]` | `numbers` 逐鍵扁平化 diff：`{path, old, new, pct_change?}`；新增鍵 `added:true`（無 `old`）；list-of-dict 依 `metric`/`id`/`name`/`year`... 等共同鍵對齊後遞迴（`latest_quarter_kpis.items` 即依此對齊，非特例硬寫） |
| `coverage_changed{axis: {...}}` | 只含有變動的軸；`new_findings[]`＝舊檔沒有的 claim（正規化去空白比對）；`status_change`＝`{old,new}` |
| `events_changed{category: {...}}` | 同 `coverage_changed` 形狀，套用在 `events` 五類 |
| `prior_meta_diff` | `{prior_meta: {drift_watch欄->值}, drift_watch: [...]}`——沿用 `dd_prior.DRIFT_WATCH`；純陳列 prior 值供 Stage 1 比對，不是真正的新舊 diff（新 judgment 此時尚未存在） |
| `judgment_fields_to_review[]` | 聚合自 numbers 規則表、coverage/events 各 finding 的 `affects[]`、恆含 `contradictions` |
| `sections_to_rewrite[]` | 由上列路徑經 `JUDGMENT_PATH_TO_SID` 對映得到，聯集 `{s1,decision,revlog,s14,appA}`（永遠重寫） |
| `carry_forward[]` | prior `prose/` 實際存在的 sid 扣掉 `sections_to_rewrite` |
| `full_rewrite_required` | `{required, reasons[]}`：price_at_dd 變動 >40%／prior 報告 >180 天／`archetype_hint` 與 prior 判斷 archetype 不同 |

## 規則表（腳本頂部常數）

- `NUMBERS_FIELD_RULES`：`numbers.<subkey>` 變動 → 需重看的 judgment 路徑。coverage/events 不用表，直接吃 evidence 裡每條 finding 自帶的 `affects[]`（找不到才用 `EVENTS_CATEGORY_FALLBACK`）。
- `JUDGMENT_PATH_TO_SID`／`NUMBERS_SID_OVERRIDES`／`always_rewrite_sids`：**單一權威在 `scripts/dd_schema/section_map.json`**（散文 agent 與 `dd_delta.py` 同源讀此檔；改對映只改該檔，見 render-rules.md §2 末）。`dd_delta.py` 內建同名常數只作 fallback（檔案讀不到／壞掉才用）。`judgment_path_to_sid` 非 render-rules.md 明文（render-rules §2 只講 5 個表格注入標記），是依 `html-output.md`「章節顯示順序」內容描述反推，`_note` 欄已標記需持有人審；`ALWAYS_ALLOWED_JUDGMENT_PATHS`（`check` 用）由 `judgment_path_to_sid ∩ always_rewrite_sids` 動態算出，不再另存一份。
- `DRIFT_FIELD_JUDGMENT_PATH`：20 個 DRIFT_WATCH 欄的 judgment.json 唯一路徑，權威來源 `judgment-to-ddmeta.md`；`bull_5y_price`/`bear_5y_price`/`p_bull_pct`/`p_bear_pct` 只存在 scenario_meta.json，此欄留 `None`（`check` 略過，非猜測而是已知範圍缺口）。

## `check` 子命令

`dd_delta.py check DELTA.json --judgment NEW.json --prior-judgment PRIOR.json`：

1. 對 `judgment.json` 全樹做 `deep_diff(prior, new)`；每個改動路徑須落在 `judgment_fields_to_review ∪ ALWAYS_ALLOWED_JUDGMENT_PATHS`（`decision_inputs`/`decision_out`/`triggers`/`meta`/`oneliner`/`trap_analysis`/`catalysts`/`appendix_a`——因其段落本就永遠重寫）之下，否則列入 violations → FAIL。
2. 對每個有 judgment 路徑的 DRIFT_WATCH 欄，若新舊值不同，`contradictions[]` 必須有一筆 `prior_field` 等於該欄名，否則 FAIL。

PASS/FAIL 皆印出具體路徑與新舊值；exit code 0/1。
