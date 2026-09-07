# 委託書：v17 複審 P1／P2 清理（給 Codex）

> 用法：在 Codex 開 `~/financial-analysis-bot`，第一句「先讀 AGENTS.md 的『角色分工』與『寫程式 agent 的改動紀律』兩節，再讀本檔全文」。本檔是唯一任務來源。
> 日期：2026-09-07。委託人：持有人。指揮者：Claude Code 主 session（放行與 push 的決定權在指揮者）。
> 前置：P0 三件與批 A 補件五件已放行並 commit（`f5e57eba1`／`fccc0fe20`），git 分岔已依方案 A 整併成一顆（`09a72ebe73`）。
> 依據報告：`notes/site-internal/dd/_review_v17_pipeline_20260907.md` §1 的 P1-1 到 P2-3，錨點行號以該檔為準。

## 〇、交件方式

**一批交完，中途不要回來問。** 下列七項連續做完再交件；順序照本檔（那就是複審 §3 的建議修復順序，有相依性）。全部是零 LLM 成本的機械層。

上一份委託書（`_codex_brief_gate_and_git_20260907.md`）的**第一節禁區、第六節「什麼時候自己決定／什麼時候停」、第七節基準自測快照，全部原文適用**，不再重述。特別重申兩條：**你只交 diff，不 commit 不 push**；**不得跑 `ddreport.py run／finish／batch`、不得 spawn 模型**。

## 一、P1-1 三欄權威衝突（先做這件，否則 `--full` 一跑就有可見回歸）

**現況**：`ev5y_pct`／`irr_base_pct`／`asym_ratio` 三欄，新 judge prompt 已一律填 `null` 交由 `dd_scenario.py` 算回，但呈現層還沒跟上——

- `scripts/gen_dd_tables.py:150-185`：`build_dd_meta()` 的 EV 先取 `di.get("ev5y_pct")`，差異迴圈只涵蓋 IRR／AR，EV 只在原值為 `None` 才由 scenario 補；`_override_tol` 的 EV 常數實際沒被用到。
- `scripts/gen_dd_tables.py:538-568`（完整版 dashboard）與 `:703-724`（revlog 當期列）：直接讀 `decision_inputs`，**完全沒讀傳入的 `scenario_meta`** → 三欄為 null 時顯示空值。
- `scripts/dd_brief.py:197-217, 220-232`：快速版 tile 這條路徑已修，可當正確樣板。

**要做到**：抽一個共用的三欄 resolver，`build_dd_meta()`、brief tile、full dashboard、revlog 四個入口全部改走它。**新 run 以 scenario 為權威，judgment null 即 N/A**；歷史非 null 存查沿用既有容差邏輯，容差常數不得改動（改容差＝改判準，屬禁區）。

**驗收**：①用三欄為 null 的 judgment ＋ 有值的 scenario_meta 呼叫 `render_dashboard_html()` 與 revlog，兩處都要顯示 scenario 的值；②對 WDC 存查呼叫 `build_dd_meta(judgment, scenario_meta)`，EV 不得再由 judgment 的 7.0 蓋掉 scenario 的 6.8；③四個入口對同一組輸入回相同值的單元測試。

## 二、P1-3 統一 latest 迭代器（影響面最大）

**現況**：13 份 brief **全部**比同 ticker 最新完整版新（AVGO／BWXT／CAMT／CDNS／ETN／FIX／FN／GRAB／HPE／STRL／TXN／WDAY／WDC）。任何只掃根目錄的 latest-per-ticker 消費者，對這 13 檔一律讀到**舊裁決**。

已涵蓋（不用動）：`update_dd_index.py`、`dd_screener_dd_loader.py`、`build_ticker_hubs.py`、`knowledge/build_knowledge.py`、`knowledge/brain_extract.py`。

**未涵蓋，主鏈直接呼叫（本批必修）**：`build_supply_chain_dd_index.py:44`、`build_search_index.py:86`、`build_track_record.py:35,190`、`sync_kill_registry.py:91`、`inject_dd_livebar.py:29,71`，加上 `dd_prior.py:97,111-119`（**這支最要緊——下一輪判斷會把最新 brief 當作不存在**）。

**未涵蓋，離線工具（本批做到能收就收，收不完在報告列清單）**：`dd_decision.py:920` 的 `check-all`、`aggregate_dd_stats.py:144`、`aggregate_dca_stats.py:147`、`check_dd_earnings_freshness.py:45`、`check_tier_matrix.py:227`、`intel/sec_filings.py:172`、`intel/calendar_ext.py:67`、`snapshot_consensus.py:322`、`list_breakout_candidates.py:86`。

**要做到**：**不要逐支再寫一個 glob。** 擴充 `scripts/dd_meta_reader.py:84-92` 成唯一 iterator——參數明示是否含 brief、**同日期時完整版優先**、對 parse failure 回傳 diagnostics 而不是靜默跳過；上述 consumer 全部改用它。`dd_meta_reader` 目前對壞 meta 靜默跳過，任何新 caller 都會繼承這個缺口，一併修掉。

**驗收**：對每支改過的 consumer 計數其輸入候選，應為 681（668 完整版＋13 brief）而不是 668；同 ticker 同日兩種都在時，取完整版。track record 的外部取價成本不得因此增加（去重要在取價之前）。

## 三、P1-2 finish 的 stage 前置條件

**現況**：`ddreport.py:3062-3081` 只要 `stages.prose.out_path` 指向的檔存在就優先選 prose，**不看 prose state**；`:3439-3457` finish 唯一的前置條件是 brief＝PASS。從正常 `run` 進 finish 有 stage loop 擋著，但公開的 `finish` 子命令可直接繞過。

**要做到**：finish 在**任何副作用與 HTML 選擇之前**，依輸出型態逐一驗必要 stage——brief 發布要求 `stage0`／`judged`／`gated`／`brief` 全 PASS；`--full` 再加 `prose` PASS，且只能選 prose＝PASS 的 out_path。`SKIPPED` 不得當作 v17 必經段的成功（比照已放行的 gated／brief 處置）。

**驗收**：造一個 brief=PASS、gated=FAIL、prose=FAIL 但 prose.out_path 存在且數學可過的 manifest，`_do_finish(..., dry_run=True)` 必須在選檔前就擋下，且不得選中 prose。

## 四、P1-4 archive fallback 讓 finish 能重跑

**現況**：`ddreport.py:3224-3238` 的 judgment／scenario_meta 已能 fallback 到 `_src/{T}_{D}`，但 `:3441-3446` 仍硬要 run 目錄的 manifest，讀不到就結束——即使 archive 裡明明有一份（`:3113-3156` 有複製）。

**要做到**：manifest 納入同一套 source resolver；**archive manifest 裡的絕對 run out_path 不可直接信**，要按 ticker／date 與輸出模式重新解出 docs 目標。fallback 生效時必須明列來源。

**驗收**：把 `_run_dir()` 指向不存在的暫存路徑、保留某 ticker 的 `_src`，finish 能由 archive manifest 續行而不是立刻結束。

## 五、P1-5 收尾確認（多半已由批 A 完成，請驗證而不是重做）

批 A 已加 `finish.site_sync` 狀態機、`report_commit_sha`／`report_pushed_sha`／`archived`，`status` 也已顯示 finish 與 deferred，且你回報「已完成 finish 的 `--resume` 是 no-op」。**請逐條對照複審 P1-5 的四個要求**（`validated`／`site_synced`／`archived`／`commit_sha`／`pushed_sha` 皆可恢復、resume 從第一個未完成副作用接續且不重做已完成副作用），缺什麼補什麼；**已滿足的直接在報告寫「已由批 A 覆蓋」並附證據，不要重寫一套**。

## 六、P2-2 與 P2-3（順手做，都是小改）

- **P2-2**：`dd_delta.py:524-539` 的 `prior_meta_diff.prior_meta` 實際是從 prior **judgment** 抽的，不是 prior 發布 dd-meta；`:612-623` 又把四個 scenario-only 欄整個略過。三欄改 null 後，delta check 只會看到 null。修法：prior／current 都經**同一個 judgment＋scenario→dd-meta resolver**（就是第一節那支），四個 scenario-only 欄也要能比。目前 `ddreport.py` 沒接 `dd_delta.py`，所以這是 dormant debt，**不要為它擴大改動範圍**。
- **P2-3**：`ddreport.py:3760-3774` 的 batch 摘要直接取 `premortem.max_dd.lo`，但發布契約是 `min(lo, hi)`。改成讀本次 HTML dd-meta 或共用同一個 max-dd resolver。不新增任何門檻。

## 七、P2-1 只做「短期」那一半，不要碰 FPE／PEG

**要做**：`validate_judgment.py` 為**真正同義**的 pair 加 equality 檢查，不一致就 fail。名單（複審實測 18 份 2026-09 存查全部 0 mismatch，代表加了不會誤傷）：`signal`、`trap`、`moat`、`val`、`ma`、`moat_trend`、`runway_post_y5`、`capalloc_grade`、`archetype`、`pct_5y`、短中期 upside、`moat_score`。

**明確不要做**：①`fpe_fy2`（18 份中 10 份不同）與 `peg_fy2`（8／18 不同）**不是** bug——AVGO 的 reasoning 明確區分 FY26 30.77x／0.51 與 FY27 18.51x／0.31，推翻了 mapping 文件寫的等式。這是**財年口徑未定義**的資料契約問題，要先澄清才能談合併，本批只在 `judgment-to-ddmeta.md` 補一行「口徑待定義，不得視為同義」，不要動程式。②Phase 5 的 skeleton／「只讓 agent 填一次」屬另一件委託，本批不做。

## 八、驗收總表（全部跑完貼原始輸出）

| 命令 | 判定 |
|---|---|
| `python3 -m pytest scripts/tests -q` | 不得有 fail；passed 只增不減（開工時 153） |
| `python3 scripts/qc.py` 與 `--all` | errors 必須 0 |
| `python3 scripts/verify_dd_math.py --all` | 不得有 FAIL（開工時 48 檔全過） |
| `python3 scripts/validate_dd_meta.py` | rc 0（開工時 681 檔／ok 540／warnings 173） |

開工先自測一次取當下快照，收工再比對；warnings 與檔數變動記錄即可，只有粗體級失敗才停。
