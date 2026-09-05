# DD skill 重新設計交接（2026-09-05，BE v16.2 第二份上站後）

> 給下一個對話的起點。本檔只記「現況、技術債、持有人拍板、設計約束」，不預設解法。

## 0. 持有人本輪拍板（不可推翻）
- 任何 DD 觸發語（「跑 X dd report」「ddreport X」「X DD」「X 全套」）**預設走 repo 內最新版管線**（現 v16.2），不需旗標；skill 文字落後時以此為準（已寫進 CLAUDE.md 路由表註記）。
- 完成即 commit＋push（不停下複審）。
- Koyfin 增量下載交 sonnet 子 agent，orchestrator 不跑。
- writer／判斷 與 critic／抽查 永不同模型（Fable 判斷 → opus 抽查）。

## 1. 現況（2026-09-05）
- **生產鏈＝v16.2 三步制**：Stage 0（sonnet fan-out 收資料＋0e 逐字稿摘要）→ `validate_evidence.py --strict` → 判斷 agent（Fable，只寫 `judgment.json`／`scenario.json`）→ 散文 agent（sonnet，只讀 judgment 鋪陳）→ `dd_gates.sh` 六支閘 → INDEX.md → `update_dd_index.py` → commit。流程內無 critic；前三份上站後另跑 opus 事後抽查（只計數）。
- 已上站：PANW（v16.1）、CRDO（v16.2 首份）、BE（v16.2 第二份）。設計稿 `notes/site-internal/dd/_v16_design_spec_20260903.md` §13／§16。
- **退場訊號②已命中**：BE 抽查判斷級 🔴＝1（`_audit_BE_20260905.md`：Crossroads 1,500 噸／年鈧口徑在證據包卻未接進判斷、Bull 6GW 未壓測）。依設計稿應把判斷層驗收放回流程內，**是否恢復流程內 critic 待持有人裁定**。
- Token（去重尺 `dd_token_report.py`）：BE Fable 判斷 4.8M（目標 ≤3M ✗）、sonnet 散文 2.4M（✓）、Stage 0＋0e 5.5M、合計 ≈13.0M（≤15M ✓）。CRDO：Fable 2.4M／散文 6.8M／合計 17.6M。

## 2. 檔案地圖（技術債的物理位置）
| 位置 | 內容 | 狀態 |
|---|---|---|
| `.claude/skills/stock-analyst/SKILL.md` | v15.2，125.8KB，QC-1～QC-54，紙面上「唯一生產版本」 | 實際已不是預設鏈 |
| `.claude/skills/stock-analyst/SKILL.v16.draft.md` | v16.2 四段制契約骨架，25KB | 「草稿、不生效」但實際在跑 |
| `references/`（14 檔）＋`references/v16/`（6 檔：agent-prompts／judgment-rules 41KB／render-rules 16KB／validators／rule-migration-map／retire-candidates） | 條件載入規則 | v15 與 v16 兩套並存、部分重複 |
| `.claude/skills/ddreport/SKILL.md`（v2.3）＋`SKILL.v3.draft.md`（v3.1） | orchestrator 步驟散文 | v2.3 仍寫「預設」，與拍板衝突（本輪誤啟 v15.2 writer 的直接原因） |
| `scripts/dd_*.py`（evidence／numbers_extra／prior／scenario／decision／prose_budget／sections／delta／gates.sh／token_report）＋`validate_{evidence,digest,judgment,prose,dd_meta}.py`＋`verify_dd_math.py`＋`gen_dd_tables.py`＋`render_dd.py` | 機械層 | 功能齊，但沒有單一入口把它們串起來 |
| `scripts/dd_schema/`（judgment.schema.json、decision_inputs.md、judgment-to-ddmeta.md） | 交接物契約 | 權威在此，但 prompt 內仍重述 |
| `.dd_build/`（共用工作目錄）＋`notes/site-internal/dd/_src/{T}_{D}/` | 中間產物／來源檔存查 | 見 3.3 |

## 3. 本輪實測到的技術債（按痛度排序）
1. **路由與版本靠散文，不靠程式**：三份 skill 文字對「預設走哪條」說法不一（SKILL.md v15.2＝唯一生產版；ddreport v2.3＝預設；CLAUDE.md＝v16.2 試點；持有人＝最新版）。orchestrator 讀到哪份就走哪條 → 誤啟 v15.2 writer 燒 0.3M 後 kill。**應收斂為單一入口＋單一版本號**。
2. **orchestrator 在手工執行本該是腳本的流程**：Stage 0 的 init／axes／numbers_extra／prior／merge×N／digest_path merge／validate 全是零 LLM 的固定順序，本輪由 opus orchestrator 逐條敲 Bash，並先讀了 agent-prompts.md（25KB）、evidence-pack.md、data-collection.md（v15 格式，需手工改成 JSON 派工）、SKILL.v16.draft、ddreport v3 draft 才知道怎麼跑。**Stage 0 應是一支 `dd_stage0.py`（或 `ddreport.py --stage 0`）只回報 validator 結果**；LLM 只該出現在三處：覆蓋軸搜尋、判斷、散文。
3. **共用工作目錄跨 ticker 污染**：`.dd_build/evidence_parts/` 殘留前一天 CRDO 的 batch1-4.json，與本次同名 → 本輪先隔離才敢 merge。路徑慣例也不一致（v3 draft 寫 `.dd_build/parts/`，SKILL.v16 寫 `evidence_parts/`）。**應改 per-run 目錄 `.dd_build/{T}_{D}/`**。
4. **驗證器分工缺口造成跨 agent 往返**：
   - `validate_judgment.py` 不驗「Max DD 下限 ≥ Bear 終點跌幅」，只在 HTML 階段被 `verify_dd_math.py` 攔 → 散文 agent 交回 → orchestrator → 判斷 agent 修一欄 → 散文 agent 重產表重寫 s12 重跑閘（多兩個 agent 往返）。判斷層算得出的恆等式應全在判斷層驗。
   - `validate_evidence.py --strict` 對 findings 的 `as_of` 只在 merge 後才擋，採集子 agent 寫自由文字（「2023-2027（多年期）」）→ orchestrator 手工補日期；KPI items 缺 `as_of/source` 也是事後手剪。**part 檔應在子 agent 交稿時就驗**（給子 agent 一支 `validate_part.py`）。
   - 判斷 agent 首輪 3 FAIL 全是瑣碎 schema（oneliner >200 字、scenario_ref 相對路徑、矩陣注入文字含 `QC-48` 洩漏詞）→ 可自動修正或在 schema 層說清楚，不值得 Fable 一輪。
5. **抽查制的品質缺口是可機械化的**：BE 的 🔴 是「證據包有 direction=− 的 finding 未被 judgment 任何欄位引用」。這是可以寫成 validator 的（每條負向 finding 須在 contradictions／premortem／triggers／threats 至少被引用一次，否則列缺口要判斷 agent 明寫「不採納＋理由」）。**先做這個再決定要不要把 LLM critic 放回流程**。
6. **派工模板與資料格式錯代**：`data-collection.md` 的採集模板仍是 v15 的 Markdown ≤6KB 回傳，v16 需要 JSON 片段；本輪由 orchestrator 臨場改寫。Python 環境也含混（`dd_gates.sh` 預設 `/tmp/ddvenv/bin/python`，該 venv 現無 yfinance；`numbers_extra` 用系統 python3 可跑）。
7. **INDEX.md 與 dd-meta 雙軌**：INDEX 行由 orchestrator 從 dd-meta 手寫（第 6 欄語意歷史不一致），研究頁又只收 INDEX 有的 DD。**應由腳本從 dd-meta 生成 INDEX 行**（或研究頁直接讀 dd-meta，INDEX 退為 view）。
8. **commit 噪音**：一份 DD 的 `update_dd_index.py` 連鎖改 260 檔（weekly_cache 229 檔、track-record、kill_registry、rss、search-index、site_nav self-heal），且 `build_rss`／search-index 會撿到其他 session 的未 commit 檔（本輪 `ID_AdvancedPackaging` 被撿進 rss/search-index，只能不 commit 那三檔）。**DD commit 應只含 DD 直接產物；快取類走排程 commit**。
9. **規則體膨脹**：QC-1～QC-54 含多條「已退役 → 併入」的殼；v16 `rule-migration-map.md` 已做三分法（判斷／呈現／驗證器）但 v15.2 SKILL.md 全文仍是 always-on 讀本（judgment agent 只讀 judgment-rules 41KB 是對的方向）。`retire-candidates.md` 已列候刪清單，未執行。
10. **Fable 用量目標未達的結構原因**：判斷 agent 讀 evidence.json 116KB＋逐字稿 46KB＋規則 41KB＋schema ≈ 85K token context 起跳，再加 3 輪驗證與 1 次修補；要壓到 ≤3M 需要更少輪次（見 4、5）與更薄的 evidence（coverage findings 可先機械去重／依 direction 排序）。

## 4. 重新設計時的約束（來自 rule_ledger／CLAUDE.md，不得順手改）
- 判斷機器語意（QC 門檻、決策矩陣 rows 1–10、fail-safe 方向、dd-meta v15.0 欄位語意、篇幅帶 75–105KB、E1–E12 表格收斂、三詞統一裁決）**零變動**，除非持有人明示。
- 判斷類規則加刪走 `knowledge/rule_ledger.md` 三條治理（無 kill condition 不准加、加一提刪一、校準輪審計）；2026-10 校準輪前門檻凍結。
- 下游聚合器（`update_dd_index.py`／dd-screener／picks／engine）讀 dd-meta 不變，不新建收斂面。
- 4-repo 共站；只動本 repo。

## 5. 建議下個對話的第一步（不是解法，是問題定義）
1. 先讀本檔＋設計稿 §13／§16＋`_audit_BE_20260905.md`＋`references/v16/rule-migration-map.md`＋`retire-candidates.md`。
2. 決定三個裁定：①退場訊號②命中後，是恢復流程內 LLM critic，還是先補「負向 finding 覆蓋」validator；②v15.2 是退役還是留旗標 fallback；③單一入口是 Python 腳本（`scripts/ddreport.py`）還是薄 skill＋腳本。
3. 產出一份新的設計稿（不動現行檔），列 WP 與驗收（回溯考卷：既有 v16 三份 `_src/` 可當 fixture 重放）。
