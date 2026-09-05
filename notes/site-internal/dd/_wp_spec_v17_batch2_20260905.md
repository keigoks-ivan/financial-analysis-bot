# v17 第二批派工（2026-09-05 晚；WP1／WP2 已 commit：24657e01d、ad4204a5c）

> 共同約定見 `_wp_spec_v17_20260905.md` 開頭（Python 3.9 相容、per-run 目錄、fixture 路徑、回報格式、≤40 輪、不 commit）。四件互不碰檔，並行。
> **既有可用件**：`scripts/ddreport.py`（plan／status、`spawn_list.json`、`manifest.json`）、`scripts/dd_headless.py`（`spawn`／`spawn_many`、`DD_CLAUDE_BIN` 可指假 binary、`scripts/tests/fake_claude.py`）、`scripts/dd_evidence.py finalize`、`scripts/validate_evidence.py --part`、`scripts/validate_judgment.py`（J1 需 `--evidence`；`--fix`；`--j1-warn`）、`scripts/dd_bundle.py judge|gate`、`scripts/dd_prompts/*.md.tmpl`。母稿 `_dd_pipeline_redesign_spec_20260905.md` §3（流程）、§3.4（閘）、§3.8（無頭）、§4.1（熔斷）、§8 C-5（快速版欄目）。
> **fixture 注意**：`_src/CRDO_20260904/parts/` 已於 2d42d47ed 修正為真正 Credo；`_src/SNOW_20260904_dryrun/` 是 v16.1 dry-run（無 digest、無 prose）。

---

## WP1d `ddreport.py run`：Stage 0 → 判斷 → 閘 → 快速版 串接（無頭）
**擁有**：`scripts/ddreport.py`（加 `run`、`stage0`、`judge`、`gate`、`brief` 子命令與 `judge check`）、新檔 `scripts/tests/test_ddreport_run.py`、可擴充 `scripts/tests/fake_claude.py`（加 replay 模式）。**不動** dd_headless／dd_evidence／validate_*／dd_bundle 的內部（只 import 或 subprocess 呼叫）；`dd_gate.py`／`dd_brief.py` 由 WP3／WP4a 並行交付，本 WP 只依介面呼叫、模組不存在時印警告跳過。

功能（每步寫 manifest：state、started／ended、agent usage、over_budget；任一步 FAIL 或 over_budget 即停，印一行「段／實測／目標／狀態」與 `--resume` 提示）：
1. `run TICKER [--date] [--archetype] [--peers] [--axes-per-batch 2] [--judgment-model fable|opus|sonnet] [--full] [--replay-from _src/{T}_{D}] [--until stage0|judged|gated|brief] [--resume] [--accept-over-budget]`。
2. `stage0`：plan（未 plan 時）→ 先 spawn `k_koyfin`（digest 依賴其路徑清單）→ `dd_headless.spawn_many(其餘 spawn, max_parallel=4)` → `dd_evidence.py finalize --run-dir`（run 目錄骨架含 `init` 產的 evidence.json，archetype 有來源）→ strict PASS 才進下一步；FAIL 時依 finalize 的「需重派」清單只重派那幾個（≤2 次）。
3. `judge`：`dd_bundle.py judge --run-dir` → 渲染 `prompts/b1_judge.md`（模板 `scripts/dd_prompts/judge.md.tmpl`，WP-text 交付；本 WP 先放最小占位模板，一行「讀 {bundle_path}，依規則寫 {judgment_path}／{scenario_path}，寫完跑 `python3 scripts/ddreport.py judge check {ticker} {date}`」，WP-text 交付後整檔替換）→ `dd_headless.spawn`（model＝`--judgment-model` 預設 fable、tools Read Write Bash、max_turns 8、budget 1.2M）→ `judge check TICKER DATE`：`dd_scenario.py {scenario} --html tables/e11.html --meta scenario_meta.json` → `dd_decision.py run {judgment} --html tables/audit.html --json {judgment}` → `validate_judgment.py {judgment} --evidence {evidence} --fix --report`（環境變數 `DD_J1_WARN=1` 時加 `--j1-warn`）；FAIL → 寫 `prompts/b1_fix.md`（FAIL 原文＋「只准改被點名欄位」）→ 再 spawn 一次（max_turns 4）→ 再 check；仍 FAIL 停下。
4. `gate`：`dd_bundle.py gate --run-dir` → `prompts/g_gate.md`（模板 `gate.md.tmpl`，WP-text 交付，先占位）→ spawn（model＝與判斷模型不同：fable→opus、opus→sonnet、sonnet→opus；tools Read Write；max_turns 6；budget 2.5M）→ 產物 `gate_audit.md` → `python3 scripts/dd_gate.py parse gate_audit.md --json`（介面：`{"red": N, "yellow": M, "findings":[{axis, level, path, note, fix}]}`）→ red>0 → `dd_gate.py patch-prompt --audit … --judgment … --evidence … --out prompts/b1_patch.md` → spawn 判斷模型（max_turns 6）→ `judge check`；`decision_out.verdict` 翻面才重跑 gate 一次，否則進 brief。
5. `brief`：`python3 scripts/dd_brief.py --run-dir DIR --out docs/dd/brief/BRIEF_{T}_{D}.html`（不存在時印警告）。`--full` 本輪不實作，印「WP4b 未交付」。`finish`（INDEX／update_dd_index／commit）本輪不做，留 WP4a-2。
6. `--replay-from DIR`：設 `DD_CLAUDE_BIN=scripts/tests/fake_claude.py`，fake 進入 replay 模式（環境變數 `DD_REPLAY_FROM`）：依 prompt 檔內的輸出路徑與 spawn id，把 fixture 的對應檔複製過去（`parts/batch{k}.json`／`axes_{k}.json` → 本 run 的 `parts/axes_{k}.json`：fixture 批數與新分批不同時，先把 fixture 全部 batch 的 `coverage` 合併，再依本 run 該批的軸清單挑出對應軸寫入；`numbers_*`→`parts/numbers_collect.json`；digest→`digest.json`；judgment／scenario→對應路徑；gate 用 `_audit_{T}_{D}.md` 若存在），並回一份合法的 result JSON（沿用 fake 既有樣本，`num_turns` 1）。這讓整條 `run` 在零 LLM 下跑通。

**驗收**：
```
DD_J1_WARN=1 python3 scripts/ddreport.py run CIEN --date 20260905 --offline --replay-from notes/site-internal/dd/_src/CIEN_20260905 --until judged
python3 scripts/ddreport.py status CIEN 20260905          # manifest：stage0 PASS、judged PASS（J1 WARN 列出未處置條數）
DD_J1_WARN=1 python3 scripts/ddreport.py run BE --date 20260905 --offline --replay-from notes/site-internal/dd/_src/BE_20260905 --until gated   # gate 用 _audit_BE：red=1 → 產 prompts/b1_patch.md → fake 再回同一 judgment → check → 停或過，回報實際走到哪
python3 -m pytest -q scripts/tests/test_ddreport_run.py   # 至少四測：manifest 狀態機推進；over_budget 停下；finalize FAIL 產重派清單只重派該批；--resume 從最後成功步接續
```

---

## WP3 `scripts/dd_gate.py`：閘輸出解析與修補 prompt
**擁有**：新檔 `scripts/dd_gate.py`、`scripts/tests/test_dd_gate.py`。**不動**其他檔。

功能：
1. `parse AUDIT.md [--json]`：支援兩種形狀——(a) 既有 `_audit_BE_20260905.md`／`_audit_CIEN_20260905.md`：首行 `## AUDIT: 判斷級🔴 = N`，之後 ①–⑧ 逐條散文或表格；(b) v17 模板：首行同上，接表格 `| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |`。輸出 `{"red": N, "yellow": M, "findings":[{"axis":"②","level":"🔴|🟡|🟢","path":"supply_demand_durability.findings[0] 或 judgment JSON 路徑","note":"…","fix":"…"}]}`；`red` 以首行數字為準，表內 🔴 計數不符時印警告但不改。
2. `patch-prompt --audit AUDIT.md --judgment J.json --evidence E.json --out PROMPT.md`：只取 🔴 條目；`path` 用簡單路徑解析（`a.b[2].c`）從 judgment 抽子樹（找不到就抽最近的上層物件；散文式 path 抽不到時抽 `contradictions`／`decision_inputs`／`premortem` 三塊）；從 evidence 抽被點名的 finding（`axis#n` 或 `axis.findings[n]`，或以 note 內關鍵詞在該軸 findings 比對）；組成 prompt：任務頭＋每條 🔴（依據、建議、受影響子樹原文、相關 finding 原文）＋硬規則（只准改列出的欄位；可不採納但須寫進 `evidence_dismissed[{ref, reason}]`；改完一次 Write 整檔並跑 `python3 scripts/ddreport.py judge check {T} {D}`）。若 `scripts/dd_prompts/judge_patch.md.tmpl` 存在則用它渲染 `{findings_block}`，否則內建最小模板。
3. `decide PARSED.json`：印 `BLOCK`（red>0）或 `PASS`，exit 1／0。

**驗收**：
```
python3 scripts/dd_gate.py parse notes/site-internal/dd/_audit_BE_20260905.md --json     # red=1，findings 含 ② 🔴，path 含 supply_demand_durability
python3 scripts/dd_gate.py parse notes/site-internal/dd/_audit_CIEN_20260905.md --json   # red=0，yellow=4
S=notes/site-internal/dd/_src/BE_20260905; python3 scripts/dd_gate.py patch-prompt --audit notes/site-internal/dd/_audit_BE_20260905.md --judgment $S/BE_20260905.judgment.json --evidence $S/BE_20260905.evidence.json --out /tmp/v17_be_patch.md && grep -c 'Crossroads' /tmp/v17_be_patch.md   # ≥1
python3 -m pytest -q scripts/tests/test_dd_gate.py
```

---

## WP-text（**opus**）三份 prompt 模板：判斷／閘／修補
**擁有**：新檔 `scripts/dd_prompts/judge.md.tmpl`、`scripts/dd_prompts/gate.md.tmpl`、`scripts/dd_prompts/judge_patch.md.tmpl`。**不動**其他檔（`agent-prompts.md`、`judgment-rules.md`、`critic-gates.md`、既有 `_audit_*.md` 只讀，先 grep -n 定位再讀範圍）。

要求（每檔 ≤120 行；變數只用 `{run_dir}`、`{bundle_path}`、`{judgment_path}`、`{scenario_path}`、`{ticker}`、`{date}`、`{max_turns}`、`{audit_path}`、`{findings_block}`；模板內其他大括號一律寫成 `{{`／`}}`）：
1. `judge.md.tmpl`：從 `agent-prompts.md` (b1) 段改寫成 v17——讀**只有一個檔** `{bundle_path}`（已含證據、最新一季逐字稿、摘要、規則、schema 速查）；寫 judgment.json／scenario.json 各一次 Write；一次複合 Bash `python3 scripts/ddreport.py judge check {ticker} {date}`；FAIL 只改欄位、≤1 輪。**新增規則**：bundle 內每條 `dir=-` 的 finding 必須出現在某個 `evidence_refs`（contradictions／moat.threats／premortem.blind_spots／triggers／thesis.R）或寫進 `evidence_dismissed[{ref, reason}]`，validator 硬擋。**刪除**交稿前自查①-⑦整段（改由跨模型閘承接）。保留：數字引用優先序、reasoning 每模組必填、前份漂移逐欄歸因、禁令（不上網、不讀 docs/dd、不重讀自己產物、每檔一次 Write）。輪次上限 `{max_turns}`，超過停下回報。
2. `gate.md.tmpl`：從 `agent-prompts.md` (c) 段＋`critic-gates.md` 的①–⑦改寫——讀**只有一個檔** `{bundle_path}`（gate bundle：證據緊湊版、judgment 全文、摘要、最新一季逐字稿），禁外部檢索、禁跑腳本；逐條①–⑦給 🟢／🟡／🔴＋一句依據＋**指向欄位**（judgment JSON 路徑或 `axis#n`）；🔴 只給「判斷級」（口徑沿用既有 `_audit_*`：證據包已有而判斷未接、算術或機率防線失守、裁決與自身輸入矛盾；資料級不算）；輸出**固定格式**：首行 `## AUDIT: 判斷級🔴 = N`，接表格 `| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |`，一次 Write 到 `{audit_path}`，附註 ≤200 字。
3. `judge_patch.md.tmpl`：讀 `{judgment_path}` 全文一次＋下方 `{findings_block}`；只准改被點名欄位；可不採納但須寫 `evidence_dismissed`；改完一次 Write 整檔，跑 `python3 scripts/ddreport.py judge check {ticker} {date}`；≤1 輪修正。

**驗收**：三檔存在且各 ≤120 行；`grep -c '{bundle_path}'` 前兩檔各 ≥1；`judge.md.tmpl` 不含「自查」；`gate.md.tmpl` 含 `## AUDIT: 判斷級🔴 =`；三檔各用 `python3 -c "import sys;print(open(sys.argv[1]).read().format_map({k:'X' for k in ['run_dir','bundle_path','judgment_path','scenario_path','ticker','date','max_turns','audit_path','findings_block']})[:80])" FILE` 渲染不拋 KeyError／ValueError。

---

## WP4a `scripts/dd_brief.py`：快速版渲染（零 LLM）
**擁有**：新檔 `scripts/dd_brief.py`、`scripts/dd_templates/brief.html`、`scripts/tests/test_dd_brief.py`。**不動**其他檔；`gen_dd_tables.py` 只 import（dd-meta 生成與 E11／E12 片段沿用其函式，不重寫）；`dd_gate.py` 若存在可 import 解析 audit，否則自寫簡單版。

功能：
1. CLI：`dd_brief.py --run-dir DIR --out FILE` 或 `--judgment J --scenario-meta M [--evidence E] [--audit gate_audit.md] [--decision-audit tables/audit.html] --out FILE`。
2. 版面照樣張 `/private/tmp/claude-501/-Users-ivanchang-financial-analysis-bot/34843d94-950b-4fb7-970f-bb4fe7813d02/scratchpad/tsm/BRIEF_TSM_sample.html`（先 cp 到 `scripts/dd_templates/brief.html` 再改成模板，CSS 保留；「樣張」橫幅與「v17 才有」占位移除）。欄目（母稿 §8 C-5）：頁首（裁決｜角色、oneliner、日期、現價、row_hit、前份裁決同向／翻面〔`evidence.prior_dd.prior_meta` 若有〕）、八格數字（EV／IRR／AR／Max DD／moat＋trend／估值燈／trap／runway）、H1–H3（`thesis.H[]` text／threshold／drift_rule）、R1–R3、single_thing、情境樹（scenario_meta 六欄＋機率＋Base EPS 路徑）、估值與品質、決策矩陣稽核（`decision_out.audit_rows` 或 `--decision-audit` 片段）、矛盾裁定（`contradictions[]` axis／side_a／side_b／ruling／settle_metric）、pre-mortem（failure_story／second_failure／blind_spots／max_dd）、觸發器（`triggers[]` text／metric／threshold／action／date）、催化劑、加減碼出場（`decision_out` rearm_trigger／pacing／holding_cap／exec_line）、**負向證據處置表**（evidence 內 dir=- 的 finding × judgment 的 evidence_refs／evidence_dismissed → 進了哪個欄位／不採納理由／未處置）、**閘的黃燈**（`--audit` 的 🟡 列）、reasoning 各模組原文（`<details>` 折疊）。欄位缺值一律「—」，不得炸。
3. 頁內含 `<script id="dd-meta" type="application/json">`：由 `gen_dd_tables` 既有 dd-meta 生成函式產出，另加 `"brief": true`；`<meta name="robots" content="noindex">`；`<title>{T} 速判 {D}</title>`。
4. 中文標點全形，`qc.py` 須過。

**驗收**：
```
S=notes/site-internal/dd/_src
for T in BE_20260905 CIEN_20260905 CRDO_20260904 PANW_20260904; do python3 scripts/dd_brief.py --judgment $S/$T/$T.judgment.json --scenario-meta $S/$T/$T.scenario_meta.json --evidence $S/$T/$T.evidence.json --out /tmp/v17_brief_$T.html && python3 scripts/qc.py /tmp/v17_brief_$T.html | tail -1; done
python3 - <<'PY'
import re,json
for T in ['BE_20260905','CIEN_20260905','CRDO_20260904','PANW_20260904']:
    b=open(f'/tmp/v17_brief_{T}.html').read(); d=open(f'docs/dd/DD_{T}.html').read()
    g=lambda h: json.loads(re.search(r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>',h,re.S).group(1))
    bm,dm=g(b),g(d); diff={k:(bm.get(k),dm.get(k)) for k in dm if k!='brief' and bm.get(k)!=dm.get(k)}
    print(T,'brief=',bm.get('brief'),'欄位差異數',len(diff),list(diff)[:6])
PY
python3 scripts/dd_brief.py --judgment $S/BE_20260905/BE_20260905.judgment.json --scenario-meta $S/BE_20260905/BE_20260905.scenario_meta.json --evidence $S/BE_20260905/BE_20260905.evidence.json --audit notes/site-internal/dd/_audit_BE_20260905.md --out /tmp/v17_brief_BE_audit.html && grep -c '負向證據' /tmp/v17_brief_BE_audit.html
python3 -m pytest -q scripts/tests/test_dd_brief.py
```
dd-meta 欄位差異數目標 0；若 `gen_dd_tables` 生成本就與當時 HTML 有已知差異，逐欄列出並解釋，不硬改 gen_dd_tables。
