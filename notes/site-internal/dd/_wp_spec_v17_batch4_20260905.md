# v17 第四批派工（2026-09-05 晚；持有人「把它做完」）

> 共同約定見 `_wp_spec_v17_20260905.md` 開頭。三件互不碰檔，並行。不 commit（orchestrator 統一 commit 並打 tag）。
> 既有可用件：`scripts/ddreport.py`（plan／stage0／judge／gate／brief／run／status；replay 模式）、`scripts/dd_brief.py`（`--run-dir DIR --out FILE`，產 `docs/dd/brief/BRIEF_{T}_{D}.html`，內含 dd-meta＋`"brief": true`）、`scripts/dd_headless.py`（每個 spawn 的 usage 已寫 `{run}/agents/*.json`、manifest 有各段 usage）。
> 母稿 `_dd_pipeline_redesign_spec_20260905.md` §3.6（finish）、§7（版本收斂）、§7.3（CLAUDE.md）、§6（規則帳本）、§8 C-5（快速版位置與「速判」）。

---

## WP6a `ddreport.py finish`（sonnet）
**擁有**：`scripts/ddreport.py`（加 `finish`、`index-row` 子命令；`run` 在 brief 之後接 finish，`--no-finish` 可停）、`scripts/tests/test_ddreport_finish.py`。**不動**其他檔（`update_dd_index.py` 只 subprocess 呼叫）。

功能：
1. `index-row --html FILE`：從 HTML 的 dd-meta 生成 `docs/dd/INDEX.md` 一列，八欄取值照 `.claude/skills/ddreport/SKILL.v3.draft.md` 步驟 5 的表（日期／Ticker／Schema／裁決＝`dca_verdict`＋`dca_role`＋`rearm_trigger`／陷阱定性＝`trap_label`／第 6 欄＝`moat_grade`（或 `moat`）＋`moat_trend`／`val`／`trap` 同既有「B↑/🔴/🟡」格式／檔案／備註）。**檔案欄**：完整版 `DD_{T}_{D}.html`；快速版 `brief/BRIEF_{T}_{D}.html`。**備註欄**：`judgment.plain.verdict_sub`（有）或 `oneliner`（無）＋三個決策數字（EV5y／IRR／Max DD）＋固定尾註「**v17 快速版（sonnet 收證據→Fable 判斷→opus 閘→零 LLM 渲染）**」或「**v17 完整版**」。印出該列，`--append` 時 append 到 INDEX.md 末尾（冪等：同檔名已存在則不重複）。
2. `finish TICKER DATE [--dry-run] [--no-push] [--skip-dd-screener]`：
   - 前置：manifest 的 brief 段 PASS。
   - `index-row --append`。
   - `python3 scripts/update_dd_index.py`（`--skip-dd-screener` 透傳；失敗只 warn）。
   - 存查：把 run 目錄的 `evidence.json`、`digest.json`、`judgment.json`、`scenario.json`、`scenario_meta.json`、`parts/`、`gate_audit.md`（有）、`prompts/`、`manifest.json`、`agents/*.json` 複製到 `notes/site-internal/dd/_src/{T}_{D}/`（檔名照 `_src` 既有慣例 `{T}_{D}.evidence.json` 等；parts／prompts／agents 各自成子目錄）。
   - `token.json`：從 manifest／agents 彙總三欄（fable／opus／sonnet 各 cache_read／cache_creation／output）＋每段輪次，寫進 `_src/{T}_{D}/token.json`，並印一行「全帳 X.XM（fable a／opus b／sonnet c）」。
   - **DD commit 檔案集**（白名單，只 stage 這些）：`docs/dd/brief/BRIEF_{T}_{D}.html`（或 `docs/dd/DD_{T}_{D}.html`）、`docs/dd/INDEX.md`、`docs/research/_body.html`、`docs/dd-screener/latest.json`、`docs/picks/candidates.json`、`notes/site-internal/dd/_src/{T}_{D}/`。其他被 update_dd_index 動到的檔（`data/weekly_cache/*`、rss、search-index、track-record、site_nav self-heal）**不 stage**，印出略過檔數。
   - commit 訊息固定：`Add {T} DD 快速版 {D}（{verdict}｜{role}；v17 全帳 {X.X}M）; resync research+screener`，尾附既有 Co-Authored-By 與 Claude-Session 兩行（從環境變數 `DD_COMMIT_TRAILER` 讀，沒有就省略）。
   - push：`git fetch`，遠端領先時**不 rebase、不 autostash**（2026-09-05 教訓：殘留 autostash 吞掉未 commit 編輯），改印「HOLD：遠端領先 N，請 orchestrator 用 worktree cherry-pick 推」並 exit 2；不領先才 `git push origin main`。`--dry-run` 時不寫 INDEX、不跑 update_dd_index、不 commit，只印會做的事與檔案集。
3. `run` 預設接 finish；`--dry-run`／`--until brief` 不接。

**驗收**：
```
DD_J1_WARN=1 python3 scripts/ddreport.py run CIEN --date 20260905 --offline --replay-from notes/site-internal/dd/_src/CIEN_20260905 --until brief
python3 scripts/ddreport.py index-row --html docs/dd/brief/BRIEF_CIEN_20260905.html          # 印一列，檔案欄為 brief/BRIEF_CIEN_20260905.html
python3 scripts/ddreport.py finish CIEN 20260905 --dry-run                                   # 印檔案集（含 brief 與 _src），不改任何檔
git status --short docs/dd/INDEX.md notes/site-internal/dd/_src/CIEN_20260905 | wc -l         # 0（dry-run 未動）
python3 -m pytest -q scripts/tests/test_ddreport_finish.py                                   # 至少：index-row 八欄、冪等 append、commit 檔案集白名單、遠端領先時 exit 2（用假 git 或 monkeypatch）
rm -rf docs/dd/brief                                                                          # 驗收後清掉重放產物（docs/ 不得留 fixture）
```

---

## WP6b 下游載入器收快速版（sonnet）
**擁有**：`scripts/update_dd_index.py`、`scripts/dd_screener_dd_loader.py`、`scripts/engine/grp.py`（若它自己讀 DD 檔；若只讀 dd-screener latest.json 則不動）、`knowledge/build_knowledge.py`、`knowledge/brain_extract.py`。**不動**其他檔；每處改動最小化，不重構。

原則：快速版 `docs/dd/brief/BRIEF_{T}_{D}.html` 的 dd-meta 與完整版同欄位（多 `"brief": true`），**對所有下游就是一份 DD**；同 ticker 取日期最新的一份（不論完整或快速）。

1. `update_dd_index.py`：`DD_DIR.glob("DD_*.html")` 之處（約第 503、1175 行與 `_find_latest_*`）同時納入 `DD_DIR/"brief"` 下的 `BRIEF_*.html`；INDEX.md 檔案欄 `brief/BRIEF_…` 能解析；研究頁列對 `brief:true` 的條目在裁決欄加一個小標 `<span class="brief-tag" title="快速版：判斷同完整版，未寫散文">速判</span>`（樣式 inline 或沿用既有 badge class；先查 `notes/site-internal/root/_plainlang_styleguide.md` 有無「速判」定案字樣，沒有才用此字）。
2. `dd_screener_dd_loader.py`：`_DD_FILENAME_DATE_RE` 與 glob 同時接受 `brief/BRIEF_{STEM}_{YYYYMMDD}.html`；`_latest_per_ticker_with_paths` 跨兩種檔取最新；輸出記錄加 `brief: bool`。
3. `engine/grp.py`：只在它直接讀 DD 檔時改；讀 latest.json 則確認 `dca_verdict`／日期欄對快速版同樣生效（寫一句註解即可）。
4. `knowledge/build_knowledge.py`、`brain_extract.py`：`DD_GLOB` 加 `docs/dd/brief/BRIEF_*.html`；日期解析同時支援 `BRIEF_` 前綴；來源型別仍記 `dd`（帳本不分快慢）。

**驗收**（用 CIEN 重放產物當臨時檔，驗完刪除）：
```
DD_J1_WARN=1 python3 scripts/ddreport.py run CIEN --date 20260905 --offline --replay-from notes/site-internal/dd/_src/CIEN_20260905 --until brief   # 若 docs/dd/brief/BRIEF_CIEN_20260905.html 已存在可略
python3 scripts/update_dd_index.py --dry-run --skip-dd-screener 2>&1 | grep -i -E 'BRIEF_CIEN|速判' | head -3      # 有命中
python3 - <<'PY'
import sys; sys.path.insert(0,'scripts'); import dd_screener_dd_loader as L
# 依實際 API 呼叫「最新一份 per ticker」，確認 CIEN 取到 brief（日期 2026-09-05 與完整版同日時，任一皆可，但 brief 旗標須存在）
PY
python3 -c "import re,glob;print([p for p in glob.glob('docs/dd/brief/*.html')])"
python3 knowledge/build_knowledge.py --help >/dev/null 2>&1 && echo help-ok   # 若有 dry/limit 旗標則跑一次確認 BRIEF 被掃到；沒有就只跑 import 與 glob 單元
rm -rf docs/dd/brief; git status --short docs/ | grep -v '^ M docs/t/' | head   # 不得留下 docs/ 變動（除其他 session 既有）
```

---

## WP6c skill 合併、v15.2 歸檔、CLAUDE.md 與規則帳本（**opus**）
**擁有**：`.claude/skills/ddreport/SKILL.md`（整檔重寫）、`.claude/skills/stock-analyst/SKILL.md`（整檔改 redirect stub）、`_archived/skills/stock-analyst-v15.2/`（新目錄，`git mv` 進去：原 `stock-analyst/SKILL.md`→`SKILL.md`、`stock-analyst/SKILL.v16.draft.md`、`stock-analyst/references/html-output.md`、`stock-analyst/references/data-collection.md`、`ddreport/SKILL.v3.draft.md`，加一份 `README.md` 說明歸檔理由與 tag 名）、`.claude/skills/stock-analyst/references/v16/judgment-rules.md`（**只改 §16「自查觸發」一段**：改為指向 Stage 1G 跨模型閘與 J1 validator，門檻條文一字不動）、`CLAUDE.md`（只改模型路由表那一列與「註記」段、「DD writer 路由」與「writer↔critic 對調」兩段各加一句 v17 註）、`knowledge/rule_ledger.md`（新增／改寫三條）。**不動**其他檔。

1. **`ddreport/SKILL.md`（≤2.5KB）**：frontmatter `version: v4.0`；描述＝「任何 DD 觸發語 → `python3 scripts/ddreport.py run {T} [--full] [--judgment-model]`，無頭三段（sonnet 收證據→Fable 判斷→opus 閘→零 LLM 快速版；`--full` 才加 sonnet 散文），完成自動 finish＋commit＋push；exit 2 表示遠端領先，orchestrator 用 worktree cherry-pick 推」；觸發語清單（含原 stock-analyst 全部觸發語，裸 ticker 仍走 stock-screen-v1）；回報格式（路徑、裁決、三個數字、全帳三欄、閘 🔴🟡 數、fallback 段數）；「不做的事」三行；回退＝`git checkout dd-v16.2-final -- .claude/skills scripts`。
2. **`stock-analyst/SKILL.md`（≤1.5KB）**：deprecation stub，比照 `deep-conviction-analyst` 寫法：所有觸發語轉 `ddreport`；`references/` 仍是規則權威（judgment-rules／render-rules／gate-checklist 與條件載入檔）；歸檔位置與 tag。
3. **歸檔**：用 `git mv`；`_archived/skills/stock-analyst-v15.2/README.md` 寫：歸檔日、原因（v17 無頭三段取代單體 writer；設計稿路徑）、tag `dd-v15.2-final`＝歸檔前最後一個 commit、`dd-v16.2-final`＝v16.2 最後上站（CIEN）當日 commit（tag 由 orchestrator 打，README 只寫名稱）。
4. **`judgment-rules.md` §16**：標題改「16｜驗收（v17：J1 validator＋Stage 1G 跨模型閘）」，內文改為三句：判斷 agent 不自查；負向證據由 validator 硬擋；判斷級 🔴 由不同模型的閘擋。QC-41／48／50／row 8b 的**觸發條件與 fail-safe 方向原文保留**，只改「由誰執行」。
5. **CLAUDE.md**：路由表「v16.2 DD（試點中）」列改「**v17 DD（現行）** | Stage 0／0e sonnet／判斷 Fable／閘 opus／快速版零 LLM／散文（`--full`）sonnet；orchestrator 只跑一條指令」；註記段的「2026-09-05 持有人拍板」句後加「同日拍板 v17：預設產物快速版，完整版 `--full`；入口 `scripts/ddreport.py`；skill 合併為 `ddreport` v4.0」；「DD writer 路由」與「DD 層 writer↔critic 對調」兩段開頭各加一行「**v17 起本段僅適用 `--full` 散文段；判斷層＝Fable、閘＝opus，kill condition 見 rule_ledger「v17 Stage 1G」列。**」。其餘一字不動。
6. **`rule_ledger.md`**：(a) 新增「J1 負向證據可追溯」列（規則、版本 v17 2026-09-05、依據＝BE 抽查 🔴 根因與 J1 重放基線 BE 18／CIEN 15／CRDO 14、kill condition＝母稿 §6 第 1 條原文、加一提刪一＝提名 QC-17／QC-18）；(b) 第 21 列「v16.1 移除流程內 critic gate」改寫為「v17 Stage 1G 判斷層閘（上站前、跨模型、只擋判斷級 🔴）」，kill condition＝母稿 §6 第 2 條原文，舊文以「PREREG 破例已結案（SNOW dry-run／BE 兩度命中）」註記保留；(c) 退役執行提名列：QC-7／14／36、QC-17／18、QC-8、QC-2／10／24／25 警語，狀態「2026-10 校準輪前先降級為腳本註解，條文保留」。

**驗收**：`wc -c` 兩份 SKILL.md 在上限內；`grep -rn -E 'v15\.2 .*唯一生產|--v16 旗標|預設.*v2\.3' .claude/skills CLAUDE.md` 無命中；`ls _archived/skills/stock-analyst-v15.2/` 五檔＋README；`python3 scripts/qc.py CLAUDE.md knowledge/rule_ledger.md .claude/skills/ddreport/SKILL.md .claude/skills/stock-analyst/SKILL.md .claude/skills/stock-analyst/references/v16/judgment-rules.md` 過；`git status --short` 只列上述檔與 rename。上限 30 輪。
