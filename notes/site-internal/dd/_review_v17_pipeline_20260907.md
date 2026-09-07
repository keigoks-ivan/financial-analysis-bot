# v17 管線全面複審與 Git 分岔解法分析

日期：2026-09-07  
檢視基準：本機 `HEAD 95f35ba54bf9e363cb54cc4f0c304a4d916f12a8`；`origin/main acd89216d0b88b05a31c225684bcfd4c2241f7a8`。

## 0．結論先行

本輪是唯讀複審，沒有執行 DD、沒有 spawn 模型、沒有碰裁決規則，也沒有做任何 Git 手術。結論如下。

1. 有三個發布級缺口應優先處理：critic gate 在解析失敗或腳本缺失時會 fail-open；brief 的 schema gate 在 pre-commit、pre-push QC、CI 三處都沒真正接上；`finish` 在研究頁同步失敗後仍會 commit／push。
2. 今天修好的 IRR 事故還有兩個同源尾巴：`gen_dd_tables.build_dd_meta()` 的 EV 仍是 `decision_inputs` 無條件優先；新版 judgment 三欄填 `null` 後，完整版頁首與 revlog 仍直接讀 judgment，會漏掉 scenario 的 EV／IRR／AR。
3. v17 brief 已進主 research index、screener、ticker hub 與 knowledge brain，但仍被 prior、搜尋、track record、kill registry、供應鏈連結及多個離線聚合器忽略。現有 13 份 brief 全部都比同 ticker 的完整版新，所以這不是理論缺口。
4. `resume` 與 archive 的來源 fallback 只補了 judgment／scenario_meta，沒有補 manifest；`finish` 也沒有自己的完成狀態。`.dd_build` 清掉後不能從存查重跑 finish，已完成的 run 又會被 `--resume` 當作要再 finish 一次。
5. Git 分岔比工作單快照又前進了：共同祖先後，本機 53 顆、遠端 56 顆；其中雙向各有 44 顆 patch-equivalent，只有本機 9 顆與遠端 12 顆沒有 patch-equivalent。最安全的解法不是在這棵髒工作樹改歷史，而是在獨立 clone 建一條以 `origin/main` 為底的 canonical 線，按檔案 blob 驗收後再切換。

以下嚴重度以「會不會讓未驗證或不同步的報告上站」排序。所有修法都只談管線完整性與資料定義，不增刪 veto／gate／門檻／critic 規則。

## 1．發現，依嚴重度排序

### P0-1．critic gate 解析失敗會被當成零個紅燈；gate 腳本缺失也會放行

**錨點**

- `scripts/ddreport.py:2089-2098`：`dd_gate.py` 不存在時把 stage 記成 `SKIPPED` 並回傳 0。
- `scripts/ddreport.py:2169-2183`：parse rc 非 0 或 JSON 解析失敗時，`parsed=None`；下一行用 `(parsed or {}).get("red", 0)` 得到 0。
- `scripts/ddreport.py:2283-2299`：`red` 為 0 的分支直接把 stage 記為 `PASS`。
- `scripts/ddreport.py:3630-3635, 3675-3679`：`run --resume` 與一般 stage loop 都把 `SKIPPED` 視為成功。

**怎麼證明**

靜態控制流已足以重現：令 parse 子行程回傳 rc 1，或回傳 rc 0 但 stdout 不是 JSON，`parsed` 都是 `None`；`red=0`，若沒有超額就走 `PASS`。目前測試只覆蓋「已有 audit 時不重派」與「沒有 audit 時回完整 gate」，沒有 parse error fail-closed 案例。反證標準是新增一個 parse rc 非 0／壞 JSON fixture，若 `_gate_finalize_from_audit()` 回非 0且 stage＝FAIL，才算本發現錯。

**影響**

四個 critic gate 的中的結果只要格式壞掉，就可能以「red=0」發布；這正是靜默失敗，且比內容誤判更難在 log 看出來。腳本缺失同樣可繞過整段 critic。

**最小修法**

parse rc 非 0、JSON 不是 dict、必要計數鍵缺失，一律 stage＝FAIL 並印原始 parser output；`dd_gate.py` 缺失也 fail closed。`SKIPPED` 只保留給明確不適用的段，不得用於 v17 必經 critic。補兩個零 LLM 單元測試即可，成本近零。

### P0-2．brief 只接到 math gate，沒有接到 schema gate；而 math gate 對無 dd-meta 會靜默略過

**錨點**

- `scripts/hooks/pre-commit:55-56, 170-180`：有抓 `STAGED_BRIEF`，但 `TARGETS_DD` 只在 `STAGED_DD` 非空時設定，schema validator 永遠收不到只改 brief 的 commit。
- `scripts/hooks/pre-commit:202-204`：brief 確實已接到 `verify_dd_math.py`，所以「算術覆蓋已修」成立。
- `scripts/verify_dd_math.py:71-90, 194-210`：dd-meta 缺失／JSON 壞掉時 `check_file()` 回 `None`，main 直接 `continue`，rc 仍可為 0。
- `scripts/qc.py:402-425`：結構檢查只認「父目錄名是 dd 且檔名 DD_ 開頭」，`docs/dd/brief/BRIEF_*.html` 不算 DD。
- `scripts/validate_dd_meta.py:447-465`：無參數全掃只 glob 根目錄 `DD_*.html`。
- `.github/workflows/validate_dd_meta.yml:15-29, 42-43`：workflow path trigger 不含 brief，執行的 validator 又採上述根目錄預設。

**怎麼證明**

目前 `python3 scripts/verify_dd_math.py --all` 實掃 48 份 v15+，其中包含 13 份 brief，結果全過，證明 math 取檔修正有效。反過來，把任一 `/tmp/BRIEF_BAD.html` 做成無 dd-meta 或壞 JSON：直接把檔案傳給 `verify_dd_math.py` 時會「驗算 0 檔，全數通過」；傳給 `validate_dd_meta.py` 才會報錯。pre-commit、qc 與 CI 的控制流沒有把後者用在 brief。反證標準是 staged-only brief 能觸發 `validate_dd_meta.py BRIEF...` 且 CI path 也會觸發。

**影響**

缺 signal、verdict、oneliner 等 schema 欄位，甚至整塊 dd-meta 壞掉的 brief，仍可能通過現有 commit／push 鏈。finish 的四欄三方檢查會擋本次正常 run 的無 meta，但人工修改後再 commit、或其他發布入口仍沒有保護。

**最小修法**

把 brief 加進 `validate_dd_meta.py` 預設 targets、pre-commit `TARGETS_DD`、`qc.is_dd_html()` 與 CI path；同時讓 `verify_dd_math.py` 對「明示傳入的 v15／BRIEF 檔卻無法解析 meta」FAIL，不讓 checked＝0 顯示全過。全是確定性檢查，零模型成本。

### P0-3．同步失敗只警告，finish 仍 commit／push；下游 cascade 也大量 fail-soft

**錨點**

- `scripts/ddreport.py:3488-3505`：先寫 INDEX，再跑 `update_dd_index.py`；rc 非 0 只印 warn，接著 archive、commit、push。
- `scripts/update_dd_index.py:3068-3077, 3103-3118`：screener 缺失或失敗不阻斷。
- `scripts/update_dd_index.py:3135-3148, 3150-3164, 3166-3187`：供應鏈、picks、consumer layer 的 subprocess 失敗都只警告。

**怎麼證明**

在單元測試 monkeypatch `subprocess.run(update_dd_index)` 回 rc 1，現行 `_do_finish()` 仍會走到 `_git(["add", ...])`。反證標準是 rc 1 時沒有 archive、git add、commit、push，且 INDEX 不留下半寫狀態。此處沒有實跑發布命令。

**影響**

commit subject 會寫 `resync research+screener`，但實際 research／screener／kill registry 等可能仍是舊資料。這與 Phase 3 的 `--sync-later` 崩潰不變量是同一類問題：報告已推、衍生頁沒同步。

**最小修法**

先定義「DD 必須同步」的最小權威集合，`update_dd_index.py` 對該集合聚合 rc；finish 收到非 0 就停止，不 commit／push。可選頁才保留 warn。INDEX 寫入需用暫存內容或在失敗時可恢復，避免半完成。這不增加 LLM 成本；可能增加少量本地聚合時間，但避免事後重跑整條鏈。

### P1-1．三個 scenario 衍生欄仍有呈現層與 meta 層的權威衝突

**錨點**

- `scripts/dd_brief.py:197-217, 220-232`：快速版 tile 已對 EV／IRR／AR 做 judgment 與 scenario 比對，這條路徑已修。
- `scripts/gen_dd_tables.py:150-185`：`ev5y_pct` 先放 `di.get("ev5y_pct")`；後面的差異迴圈只有 IRR／AR，EV 只在原值為 `None` 時才由 scenario 補。`_override_tol` 的 EV 常數實際未被使用。
- `scripts/gen_dd_tables.py:538-568`：完整版 dashboard 的 EV／IRR 直接讀 `decision_inputs`，完全沒讀傳入的 `scenario_meta`。
- `scripts/gen_dd_tables.py:703-724`：完整版 revlog 當期列的 AR／EV也直接讀 `decision_inputs`。
- `scripts/dd_prompts/judge.md.tmpl:62-64`：新主判斷明定三欄一律 `null`。

**怎麼證明**

對 WDC 存查呼叫 `build_dd_meta(judgment, scenario_meta)`：judgment EV 7.0、scenario EV 6.8，函式仍產 7.0；IRR 則會因差異過大改採 0.9。再用三欄為 null 的 judgment 呼叫 `render_dashboard_html()`，5Y EV／IRR 顯示空值，即使 scenario_meta 有值。反證標準是三個呈現與 meta 入口都只從同一個 mech-first helper 取值。

**影響**

未來新跑的 brief dd-meta 因 judgment 為 null，會正確 fallback；但 `--full` 的頁首與 revlog 會漏數字。歷史非 null 存查中，EV 仍可能由 judgment 蓋 scenario；finish 容差內甚至可讓 tile 與 dd-meta 不同而通過。

**最小修法**

抽一個不重定義容差的三欄 resolver，`build_dd_meta()`、brief tile、full dashboard、revlog 共用；新 run 以 scenario 為權威，judgment null 是 N/A。這是定義一致性，不是新增判斷規則，零 LLM 成本。

### P1-2．finish 只驗 brief PASS；可選到未 PASS 的 prose，也沒驗 stage0／judged／gated

**錨點**

- `scripts/ddreport.py:3062-3081`：只要 `stages.prose.out_path` 指向的檔存在，就優先選 prose，不看 prose state。
- `scripts/ddreport.py:3439-3457`：finish 唯一的 stage 前置條件是 brief＝PASS。
- `scripts/ddreport.py:3675-3689`：從正常 `run` 進 finish 時 stage loop 會擋失敗，所以正常首跑較安全；但公開的 `finish` 子命令可直接繞過這個序列保證。

**怎麼證明**

造 manifest：brief＝PASS、gated＝FAIL、prose＝FAIL，但 prose.out_path 指向一個存在且數學可過的 HTML；直接呼叫 `_do_finish(..., dry_run=True)`，現況會選 prose 並進一致性閘。反證標準是 finish 在任何副作用與 HTML 選擇前，逐一驗必要 stage；full 只能選 prose＝PASS 的 out_path。

**最小修法**

finish 根據輸出類型驗 prerequisite：brief 發布要求 stage0／judged／gated／brief 全 PASS；full 再要求 prose PASS。不可把 `SKIPPED` 當 v17 必經段成功。零模型成本。

### P1-3．13 份 brief 對部分主下游可見、對另一部分完全不可見

**實測影響面**

根目錄完整版 668 份、brief 13 份；13 份 brief 全部比同 ticker 最新完整版新：AVGO、BWXT、CAMT、CDNS、ETN、FIX、FN、GRAB、HPE、STRL、TXN、WDAY、WDC。換言之，任何只掃根目錄的 latest-per-ticker 消費者，對這 13 檔都讀到舊裁決。

**已涵蓋，負面結果**

- `scripts/update_dd_index.py:503-512, 1176-1192`：research 主索引同時掃 full 與 brief。
- `scripts/dd_screener_dd_loader.py:168-178, 191-210`：screener 同時掃兩種，且同日 full 優先。
- `scripts/build_ticker_hubs.py:164-188`：ticker hub 同時掃兩種。
- `knowledge/build_knowledge.py:23-26, 150` 與 `knowledge/brain_extract.py:632-634`：決策帳本與全文腦已納入 brief。

**未涵蓋，主鏈直接呼叫**

- `scripts/build_supply_chain_dd_index.py:44`。
- `scripts/build_search_index.py:86`。
- `scripts/build_track_record.py:35, 190`。
- `scripts/sync_kill_registry.py:91`。
- `scripts/inject_dd_livebar.py:29, 71`。
- 呼叫位置都在 `scripts/update_dd_index.py:3135-3187`，且失敗仍 fail-soft。

**未涵蓋，其他聚合／稽核工具**

- `scripts/dd_prior.py:97, 111-119`：只找 `DD_{ticker}_*.html`；下一輪判斷會把最新 brief 當作不存在。
- `scripts/dd_decision.py:920`：`check-all` 預設只掃根目錄。
- `scripts/aggregate_dd_stats.py:144`、`aggregate_dca_stats.py:147`、`check_dd_earnings_freshness.py:45`、`check_tier_matrix.py:227`。
- `scripts/intel/sec_filings.py:172`、`scripts/intel/calendar_ext.py:67`、`snapshot_consensus.py:322`、`list_breakout_candidates.py:86`。
- 共用 `scripts/dd_meta_reader.py:84-92` 本身只掃根目錄，且明文對壞 meta 靜默跳過；任何新 caller 都會繼承缺口。

**怎麼證明**

將 full 與 brief 以檔名日期分組後，實測 13／13 brief 都是該 ticker 最新。對每個上述 consumer 的輸入 iterator 做計數，若結果仍只含 668 個根目錄檔而不是 681 個候選，發現成立。反證標準是共用 iterator 同時產出兩種檔並有明確 same-date precedence。

**最小修法**

不要逐支再寫 glob。擴充 `dd_meta_reader` 為唯一 iterator，參數明示是否含 brief、對 parse failure 回傳 diagnostics；所有 latest consumer 共用相同的日期與 same-day full 優先規則。先修主鏈五支與 `dd_prior`，離線工具可分批。純本地 I/O，零 LLM token；track record 的外部取價成本不應因同 ticker 去重前置正確而增加。

### P1-4．archive fallback 不能在 `.dd_build` 整輪被清掉後重跑 finish

**錨點**

- `scripts/ddreport.py:3224-3238`：judgment／scenario_meta 可以由 run path fallback 到 `_src/{T}_{D}`。
- `scripts/ddreport.py:3441-3446`：但 `_do_finish()` 第一件事仍要求 run 目錄的 manifest；讀不到便立即結束。
- `scripts/ddreport.py:3113-3156`：archive 確實有複製 manifest，所以資料已存在，只是 finish 沒有讀它。

**怎麼證明**

WDC 的 run manifest 與 archive manifest 都存在且內容相同。若把 `_run_dir()` 指向一個不存在的暫存路徑、保留 WDC `_src`，finish 會在 3443-3446 結束，連 `_finish_source_path()` 都到不了。反證標準是 run manifest 缺失時能明示 fallback archive manifest，並以存查內 out-path／發布檔重新建立目標。

**最小修法**

把 manifest 也納入同一套 source resolver；archive manifest 裡的絕對 run out_path 不可直接信，應按 ticker／date 與輸出模式重新解出 docs 目標。fallback 必須明列來源。零模型成本。

### P1-5．finish 沒有完成狀態，status／resume 無法分辨「已產出」與「已發布」

**錨點與實證**

- `scripts/ddreport.py:1023-1033`：status 只印 manifest.state。
- `scripts/ddreport.py:3504-3536`：archive、commit 後沒有寫 `finish_pass`、commit SHA 或 push 狀態。
- 實際 WDC run manifest 與 archive manifest 都仍是 `state=brief_pass`，四段為 PASS；它無法表達已 commit／push。
- `scripts/ddreport.py:3628-3635, 3681-3689`：`run --resume` 見所有段 PASS 會略過段落，然後再次呼叫 finish。

**怎麼證明**

對已成功發布的 WDC 執行 status，只會看到 `brief_pass`。若再 resume，會重新走 finish；INDEX 雖可能冪等，但最後可能以 nothing-to-commit 當失敗。反證標準是 manifest 有 finish 的 prepare／commit／push 狀態與 SHA，resume 能從第一個未完成的副作用接續且不重做已完成副作用。

**最小修法**

把 finish 建模成可恢復 stage，逐步記 `validated`、`site_synced`、`archived`、`commit_sha`、`pushed_sha`；每步設冪等檢查。此修法可與 Phase 3 pending sync 共用狀態，不另造第二套旗標。零 LLM 成本。

### P2-1．同源欄位大量由 agent 重填，schema／validator 沒有一般化一致性契約

`scripts/dd_schema/judgment-to-ddmeta.md:12-25, 39-43, 59-63` 已宣告多組「＝同源」，但 `validate_judgment.py:176-297` 的 cross-field 檢查沒有一般化驗這些 pair；`gen_dd_tables.py:122-150` 直接挑其中一側寫 dd-meta。因此 agent 若兩處填不同值，結果由 renderer 的任意取邊決定。

**系統性盤點**

| dd-meta／輸出欄 | agent 重複來源 | 腳本可做的事 | 現況風險 |
|---|---|---|---|
| `signal` | `decision_inputs.signal`、`appendix_a.signal` | 單一來源後複製 | meta 選 appendix；矩陣選 decision_inputs |
| `trap` | `decision_inputs.trap`、`trap_analysis.verdict` | 複製 | meta 選 trap_analysis |
| `moat` | `decision_inputs.moat`、`moat.grade` | 複製 | meta 選 moat |
| `val`／`ma` | decision_inputs、appendix_a | 複製 | meta 選 appendix；矩陣選 decision_inputs |
| `moat_trend`／`runway_post_y5`／`capalloc_grade`／`archetype` | decision_inputs 與各權威模組 | 複製 | meta 選模組側；矩陣選 decision_inputs |
| `pct_5y`／短中期 upside／`moat_score` | appendix_a 與 valuation／moat | 複製 | meta 選 appendix |
| `decision_out.verdict`／`role`／`row_hit`／`pacing`／`holding_cap`／`audit_rows` | agent 先填 | `dd_decision.py` 完整重算覆寫 | 最終值安全，但 agent output 是純成本 |
| `requires_critic` | agent 與 `dd_decision.py` | 腳本算出的條目與人工條目聯集 | 不能整欄機械化，需保留人工增量 |
| `ev5y_pct`／`irr_base_pct`／`asym_ratio` | 原 agent decision_inputs | scenario 完整計算 | 新 prompt 已改 null；呈現尾巴見 P1-1 |
| Bull／Bear 價、機率、Base upside、scenario_tree | scenario only | scenario 完整計算 | 沒有 judgment 重存，這部分設計正確 |
| `max_dd_pct` | judgment premortem 範圍 | `min(lo,hi)` 複製 | scenario 結構性 N/A，現行 finish 特例正確 |

**實測與一個不能直接合併的契約衝突**

掃 18 份 2026-09 存查 judgment：signal、trap、moat、val、ma、moat_trend、runway、capalloc、archetype、pct、upside、moat_score 的 pair 目前都是 0 mismatch，證明 agent 多數有守約，但不是機械保證。`fpe_fy2` 有 10／18 不同，`peg_fy2` 有 8／18 不同；AVGO 的 reasoning 明確區分 FY26 30.77x／0.51 與 FY27 18.51x／0.31。這推翻 mapping 文件所寫的「appendix_a.fpe_fy2＝valuation.fwd_pe」與「peg_fy2＝valuation.peg」，不能直接用 copy 修；要先澄清 valuation 欄的財年口徑。這是資料契約問題，不是裁決規則。

**最小修法**

短期先為真正同義 pair 加 validator equality，錯就 fail；中期 Phase 5 skeleton 只讓 agent 填一次，腳本複製到重複欄。FPE／PEG 先補欄位描述或拆成帶 fiscal-year 的欄位，未定義前不要硬合併。這能減少 Fable output，且不減任何模組、表格、critic 或 sourcing。

### P2-2．dd_delta 的 prior_meta 名稱與資料來源不一致，scenario 漂移又被排除

**錨點**

- `scripts/dd_delta.py:195-220`：三個衍生欄映射回 judgment；四個 scenario-only 欄明示為 `None`。
- `scripts/dd_delta.py:524-539`：`prior_meta_diff.prior_meta` 實際從 prior judgment 抽，不是從發布 HTML dd-meta 或 prior scenario_meta 抽。
- `scripts/dd_delta.py:612-623`：check 明示略過 scenario-only 四欄。
- 對照 `scripts/validate_judgment.py:635-645`：主 validator 的 current 側會經 `gen_dd_tables.build_dd_meta()` 加 scenario，再跟真正 prior dd-meta 比；這條較接近權威。

**怎麼證明**

WDC archive judgment 的 IRR＝3.6，而已修正發布 meta／scenario_meta＝0.9；`dd_delta` 產出的 `prior_meta_diff.irr_base_pct` 會是 3.6，欄名卻叫 prior_meta。新版 judgment 三欄改 null 後，delta check 又只會看到 null，而不是 scenario 的新值。反證標準是 delta 的 prior/current 都經同一個 judgment＋scenario→dd-meta resolver，且四個 scenario-only 欄也能比較。

**影響與最小修法**

目前 `ddreport.py` 沒接 `dd_delta.py`，所以這是 dormant design debt，不影響現行 v17 首跑；一旦啟用 delta mode，就可能錯判哪些欄漂移、哪些 prose 可 carry forward。修法是讀 archive 的發布 dd-meta 或 judgment＋scenario_meta 合成，不要把 judgment subset 命名成 meta。純機械、零 LLM 成本。

### P2-3．batch 的 Max DD 摘要不走發布值解析

`scripts/ddreport.py:3760-3774` 的 batch row 直接取 `premortem.max_dd.lo`，而 finish／HTML 的契約是 `min(lo, hi)`。若 lo／hi 次序異常，batch 回報可跟上站 dd-meta 不同。最小修法是摘要直接讀本次 HTML dd-meta，或共用 max-dd resolver；不用新增門檻。

## 2．閘與靜默失敗的負面結果

以下是本輪查過但沒有發現新缺口的部分，避免只報壞消息造成錯誤印象。

1. `verify_dd_math.py --all` 現已同時掃根目錄 DD 與 brief，實跑 48 份 v15+ 全數通過；今天的取檔修復有效。
2. `finish` 的一致性閘位於 INDEX、update、archive、git 之前，且 dry-run 也會跑；四欄 source error、verifier rc 非 0都會阻斷。`--accept-mismatch` 不能繞過 verifier 或 source error，這部分實作正確。
3. judgment 三欄為 null、scenario 有值時，finish 會明列結構性 N/A；三方全空仍阻斷。Max DD 用 judgment 的 `min(lo,hi)` 對 HTML，scenario 明列 N/A，沒有永久擋死。
4. `validate_judgment.drift_checks()` 的 current meta 會共用 `gen_dd_tables.build_dd_meta()` 並帶 scenario；不是另一套完全獨立算法。殘留問題是共用 resolver 本身的 EV 與 full render，已列 P1-1。
5. `dd_decision.py:825-883` 會在 judge check 中覆寫六個機械 decision_out 欄，並保留 rearm／exec_line、聯集 requires_critic；沒有發現「agent verdict 無條件蓋機械 verdict」的下游路徑。
6. update_dd_index 主 research 表、DD screener、ticker hubs、knowledge ledger／brain 都已含 brief。缺口集中在主鏈 cascade 的旁支與其他工具，不是整站完全看不到 brief。

## 3．建議修復順序

1. 先修 P0-1 與 P0-2：這兩項能讓「PASS」重新有可信語意，都是小改動、零 token。
2. 再把 P0-3 與 Phase 3 pending sync 一起做成同一個可恢復 finish state，不要各自造旗標。
3. 修 P1-1，否則新版 null 契約一旦跑 full 就有可見回歸。
4. 統一 brief iterator，先接 `dd_prior` 與 update cascade 五支，再補離線聚合器。
5. Phase 5 skeleton 實作時同步消掉 P2-1 的真同義重複欄；FPE／PEG 先定義財年，不可直接複製。

這個順序不改任何判斷類規則。若要更動 veto／gate 的內容或閾值，需另走治理程序並登記 kill condition；本報告沒有提出這類變更。

## 4．Git 結構性分岔：只出方案，不執行

### 4.1 現況證據

- `git merge-base HEAD origin/main`＝`89e11fca6779bc9f4f7c9af445a91e2b4e463138`。
- `git rev-list --left-right --count HEAD...origin/main`＝`53 56`，已不是工作單快照的 52／51。
- `git cherry origin/main HEAD`：44 顆 local commit 有遠端 patch-equivalent，9 顆沒有。
- 反向 `git cherry HEAD origin/main`：44 顆 remote commit 有本機 patch-equivalent，12 顆沒有。
- 兩端 tree 仍差 816 檔；大宗是 `data/weekly_cache_universe/*.json`。因此不能只看 commit 數，也不能把「patch-equivalent」誤當「整棵 tree 相同」。發布與程式檔是否已推，仍應逐檔用 `git show origin/main:<path>` 或 blob hash 比對。

### 4.2 方案 A：獨立 clone 建 canonical 線，按 blob 驗收後切換，推薦

**怎麼做**

1. 等持有人宣告切換窗口，但不要求目前各 session 先丟掉工作。
2. 在 repo 外建立獨立 clone，以 `origin/main` 為底開 integration branch。
3. 先列 9 個 local-only patch，再逐顆判斷：若相關檔的 `git show origin/main:<path>` 已與本機目標 blob 相同就略過；真的缺才以 cherry-pick 或檔案 patch 移植。
4. 對 12 個 remote-only patch 做同樣檔案級審核，跑全套測試；確認 integration tree 是預期真相後再 fast-forward 推 remote。
5. 所有舊 session 收工且 working tree 乾淨後，才把本機工作目錄重新對齊 canonical 分支；未到這一步前，舊 repo 只讀不手術。

**風險**

移植 9 顆時仍可能把「內容相同但歷史不同」重複套用；大批 data cache 也會干擾 tree diff。必須以任務檔案清單與 blob hash 驗收，不能按 commit subject 猜。

**對其他 session 未 commit 工作的影響**

建立獨立 clone 與 integration branch不碰現有 `.git`、index、working tree，影響最低。真正切換舊 repo 前仍需所有 session 停寫並各自交 diff。

**失敗時回退**

integration 尚未推時直接廢棄該 clone／branch，現有 repo 完全不變；若已推 integration branch 但未替換 main，只刪 branch 即可。main 只接受可 fast-forward 且驗收完的結果，不做 force push。

### 4.3 方案 B：在獨立環境做一次真 merge，保留雙方歷史

**怎麼做**

在獨立 clone 匯入本機 HEAD，從一端開 integration branch，對另一端做非 `ours` 的真 merge；逐檔解衝突並跑測試。完成後會有一顆雙 parent merge commit，之後 `origin/main..HEAD` 又有正常祖先語意。

**風險**

53／56 顆中有 44 對 patch-equivalent，merge-base 卻很老；Git 會看到大量雙方都改過的檔。816 檔 tree 差與生成資料會製造高衝突量，最危險的是「為了讓 merge 過而整側接受」，可能抹掉另一側獨有修復。成本與人工審核量最高。

**對其他 session 未 commit 工作的影響**

只要在獨立 clone 做，對現有 session 無影響；最後切換仍需要 freeze window。若直接在目前 repo merge，則會污染 index 與 working tree，不可採。

**失敗時回退**

不推 integration branch；刪除獨立環境即可。已推分支也不動 main。這方案不需要、也不應 force push。

### 4.4 方案 C：凍結後備份 ref，再把本機 main 重新錨到 origin/main

**怎麼做**

等所有 session 完全乾淨，先建不可誤刪的備份 branch／tag 指向現有 HEAD，輸出未追蹤檔清單與逐檔 patch；再把日常工作線切到遠端 canonical，從備份只移植確認缺少的 9 顆／檔案。

**風險**

這是唯一會直接改目前 repo 分支指標與 checkout 的方案。任何仍在寫檔的 session 都可能看到基底瞬間改變，未 commit 修改可能變成衝突、誤 stage 或被後續人工操作覆蓋。即使有備份 ref，未追蹤檔也不受 ref 保護。風險最高，不建議在多 session 活躍時採用。

**對其他 session 未 commit 工作的影響**

有直接影響；必須全員停止、逐 session 交 diff、確認 `git status` 乾淨後才可考慮。不能用 stash／checkout／reset 當作清場捷徑。

**失敗時回退**

用備份 ref 在另一個乾淨 worktree 重建原 tree，再逐檔取回；不要在帶未 commit 工作的目錄直接反向 reset。未追蹤檔須在手術前另列清單並人工保全。

### 4.5 建議

採方案 A。它把「內容真相的合併」和「目前多人共用 working tree 的切換」拆成兩個可獨立驗收的事件；失敗時沒有必要碰現有 session。方案 B 只有在持有人非常重視保留雙方 commit topology 時才值得付出衝突成本；方案 C 留作最後切換手段，不應作為整併方法。

## 5．本輪檢查命令與原始輸出

### 5.1 py_compile

第一次照工作單原指令執行，語法編譯前在 macOS cache 寫入被沙箱擋下；這不是程式語法錯誤，原文如下。

```text
$ python3 -m py_compile scripts/ddreport.py
Traceback (most recent call last):
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/py_compile.py", line 215, in <module>
    sys.exit(main())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/py_compile.py", line 207, in main
    compile(filename, doraise=True)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/py_compile.py", line 172, in compile
    importlib._bootstrap_external._write_atomic(cfile, bytecode, mode)
  File "<frozen importlib._bootstrap_external>", line 186, in _write_atomic
PermissionError: [Errno 1] Operation not permitted: '/Users/ivanchang/Library/Caches/com.apple.python/Users/ivanchang/financial-analysis-bot/scripts/ddreport.cpython-39.pyc.4421214784'
```

把 bytecode cache 改指 `/tmp` 後，以同一個 Python 3.9 編譯器重跑；rc＝0，stdout／stderr 皆空。

```text
$ env PYTHONPYCACHEPREFIX=/tmp/v17-review-pycache python3 -m py_compile scripts/ddreport.py
```

### 5.2 pytest

```text
$ python3 -m pytest scripts/tests -q
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed in 37.37s
```

### 5.3 qc

完整命令 rc＝0。原始輸出首行與末行如下；中間是逐項列出的同一批 361 個既有 warning，沒有新增 error。

```text
$ python3 scripts/qc.py
⚠  361 warning(s) (non-blocking):
  …中間逐項列出 361 個既有 warning…
✅ QC passed: 529 file(s) scanned in changed mode, 0 errors, 361 warning(s).
```
