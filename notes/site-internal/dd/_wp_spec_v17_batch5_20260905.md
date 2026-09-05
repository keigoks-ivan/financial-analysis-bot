# v17 第五批派工：AVGO 第一次真跑暴露的流程缺陷（2026-09-05 晚）

> 共同約定見 `_wp_spec_v17_20260905.md` 開頭。**等 AVGO 真跑結束後才動 `scripts/ddreport.py`**（判斷／閘步驟以子程序重呼叫它）。實測數字見本檔末。

## WP7a `ddreport.py` Stage 0 機械化補洞（sonnet）
**擁有**：`scripts/ddreport.py`、`scripts/tests/test_ddreport_run.py`（加測試）。不動其他檔。
1. **Koyfin 步改零 LLM**：`plan` 內直接 subprocess 跑 `~/scripts/koyfin-downloader/.venv/bin/python koyfin_downloader.py --tickers {T}`（失敗只 warn，標 `koyfin_session_status`）與 `python3 ~/scripts/koyfin-downloader/transcripts_for_dd.py {T} --full --n 4`，解析 stdout 最後一個 JSON 物件的 `must_read`／`optional_read`（檔名），與 Drive 資料夾 `~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/{T}/` 組成絕對路徑（找不到的檔跳過並 warn），寫 `parts/transcripts.json`（形狀同 `dd_prompts/koyfin.md.tmpl` 契約，另含 `must_read_all`）；**立刻** `dd_evidence.py merge evidence.json parts/transcripts.json`。`spawn_list.json` 不再含 `k_koyfin`；`koyfin.md.tmpl` 保留但不使用（檔頭註明）。
2. **摘要子 agent 在派工前有清單**：`a2_digest` 的 spawn 在 1. 之後；prompt 改讀 `parts/transcripts.json`（不再讀 evidence.json）。`max_turns` 16、`budget_cache_read` 1.5M。
3. **peers 來源**：優先順序 `--peers` → 前份 `_src/{T}_*/` 最新一份 `evidence.json` 的 `numbers.peer_financials` 鍵（去自身與 `_` 開頭）→ `docs/id/ID_*.html` id-meta `related_tickers[]` 含 {T} 的那份取前 4 檔 → 都沒有則印錯誤退出並提示 `--peers`（strict 會擋 `<2` 對手，早停比晚停省）。
4. **重派真的重派**：`stage0` 在 finalize FAIL 時，依 `dd_evidence.py finalize` 印出的「需重派」清單（part 檔名→spawn id 對映）重新 `spawn`；`--resume` 進到 stage0 時同樣走這條，不是只重跑 finalize。`over_budget` 只在該段全部 spawn 結束後判一次；`--accept-over-budget` 對已標 over_budget 的段放行且**不再重判**。
5. **預算重校**（實測）：覆蓋子 agent 0.9M／12 輪、數字包 1.2M／15 輪、摘要 1.5M／16 輪；Stage 0 段總目標 ≤6M（母稿 §4 表同步改）。
6. `--dry-run` 時 brief 輸出到 `{run}/brief.html`，不寫 `docs/dd/brief/`。

**驗收**：`plan AVGO --offline`（Koyfin 可跑）→ `parts/transcripts.json` 四篇絕對路徑且 evidence.json 已含 `transcripts.selected`；`spawn_list.json` 無 `k_koyfin`；peers 三種來源各一測（monkeypatch）；replay CIEN 全鏈仍過；`pytest scripts/tests` 全綠。

## 實測（AVGO 2026-09-05，去重尺 cache_read，headless 回傳）
| 段 | agent | 輪 | cache_read | 備註 |
|---|---|---|---|---|
| Stage 0 | 覆蓋 a_1–a_7 | 9–16 | 0.43–0.68M（合計 3.8M） | 全部 success，part check 過 |
| Stage 0 | a1_numbers | 13 | 0.88M | 超 0.7M 預算 → 熔斷停下（設計內） |
| Stage 0 | a2_digest 首次 | 11 | 0.61M | max_turns 10 撞頂：evidence.json 當時無逐字稿清單，agent 找不到檔 |
| Stage 0 | k_koyfin | 11 | 0.59M | max_turns 10 撞頂；同指令零 LLM 幾秒完成 → 改機械 |
| Stage 0 | a2_digest 重派 | 11 | 1.00M | 清單 merge 後一次過，validate_digest 0 FAIL |
| Stage 0 合計 | | | ≈6.9M（含兩次失敗 1.2M） | 目標原 3.5M 過於樂觀；無浪費時約 5.7M |

## WP7b 判斷段修正（AVGO 判斷實測，sonnet 腳本＋opus 模板句）
**擁有**：`scripts/ddreport.py`（judge／gate 的 prompt 組裝）、`scripts/dd_headless.py`（若需 stdin 大 prompt 支援）、`scripts/dd_prompts/judge.md.tmpl`（只加一句）、`scripts/gen_dd_tables.py`（已由 orchestrator 修：`resolve_scenario_meta` 在 scenario_ref 指向輸入檔時退回同目錄 `scenario_meta.json`；本 WP 補測試）。
1. **bundle 內嵌進 prompt，不再讓 agent Read**：judge bundle 240KB 超過 Read 工具單次 2000 行上限，Fable 為讀完 bundle 花了多輪（判斷 agent 9 輪撞 8 輪上限，仍寫完判斷物）。改法：`judge`／`gate` 組 prompt 時把 bundle 全文接在模板之後（`claude -p` 由 stdin 吃 prompt，無長度問題），模板的「讀 {bundle_path}」改成「bundle 全文附於本訊息之後，不要再 Read 任何檔」。判斷 agent 目標輪次降為 ≤5（Write judgment、Write scenario、judge check、修一次、回報）；`max_turns` 設 8 維持、`judge_fix` 設 6（實測 fix agent 4 輪不夠：讀 77KB 判斷物＋改＋寫＋check 至少 4 輪）。
2. **判斷 agent 洩漏規則代號**：judgment-rules 的段名含「QC-52 DD↔ID 對帳」「QC-51 同形狀 peer 對帳」，agent 直接抄進 `contradictions[].axis` 被洩漏詞檢查擋。改法：`judge.md.tmpl` 加一句「`axis`／`ruling` 等讀者面欄位不得出現 QC 代號、欄位名、dd-meta 等機器詞；規則段名只當索引」；`validate_judgment --fix` 的 J3 加一項：`contradictions[].axis` 內 `（QC-\d+）` 直接刪除（純代號去除，不改語意）。
3. **漂移歸因對「前份無此欄」的情況**：前份 v15 dd-meta 沒有 `rearm_trigger` 欄，本次有 → 被判漂移未歸因。改法：`validate_judgment` 漂移檢查對「前份值為 None／缺欄」的欄位降為 WARN 並提示「前份格式無此欄，可不歸因」；judge prompt 不必改。
4. **scenario_meta 解析**（已修）：補 `scripts/tests/test_gen_dd_tables_meta.py` 一測：judgment.scenario_ref 指向 scenario.json 且同目錄有 scenario_meta.json 時 build_dd_meta 取得 bull_5y_price。
5. **resume 語意**：`judged_fail` 狀態下 `--resume` 應先重跑 judge check（判斷物可能已被 orchestrator 機械修正）而非直接重派判斷 agent。

**驗收**：CIEN／BE replay 全鏈仍過；`pytest scripts/tests` 全綠；用 AVGO run 目錄（`.dd_build/runs/AVGO_20260905/`，保留）跑 `judge check` → 0 FAIL；`grep -c "不要再 Read" scripts/dd_prompts/judge.md.tmpl` ≥1。

## 實測補記（判斷段）
| agent | 輪 | Fable cache_read | 輸出 token | cache_create | 費用 | 備註 |
|---|---|---|---|---|---|---|
| judge_1 | 9（上限 8）| 0.61M | 58.9K | 142K | $5.95 | 寫完 judgment.json 77KB（含 plain、6 條不採納、負向引用）與 scenario.json；未跑到 judge check |
| judge_fix_1 | 5（上限 4）| — | — | — | — | 未產出；4 輪不夠讀 77KB＋改＋寫＋check |
| orchestrator 機械修正 | 0 | 0 | 0 | 0 | 0 | 去 QC 代號、補 rearm 方法論歸因、修 gen_dd_tables 誤判 → 0 FAIL |

## WP7d 摘要子 agent 拆成一篇一個（HPE 第二次真跑實測，sonnet）
**擁有**：`scripts/ddreport.py`（plan 的 a2 派工改為 `a2_{k}` 每篇一個 spawn，各 max_turns 8、budget 0.7M；finalize 前用零 LLM 腳本把各篇 digest 片段合併成 `digest.json`，再跑 `validate_digest.py`）、`scripts/dd_prompts/digest.md.tmpl`（改單篇契約：輸入一篇路徑，輸出 `parts/digest_{k}.json` 片段）。
**依據**：HPE a2_digest 一人讀三篇：17 輪（上限 16）、cache_read 2.54M（預算 1.5M）、$1.79；AVGO 重派 14 輪 1.42M。context 隨每篇累積是主因；三個小 agent 各約 0.5M 合計 1.5M 且可平行。
**驗收**：CIEN replay 仍過（fake 需支援 a2_{k}）；HPE parts 可重放合併；`validate_digest.py` 對合併檔 0 FAIL。

## HPE 第二次真跑 Stage 0 實測（2026-09-05，帶 --peers DELL,SMCI,NTAP,CSCO）
| agent | 輪 | cache_read | 備註 |
|---|---|---|---|
| a_1–a_7 | 9–13 | 0.44–0.85M（合計 4.27M） | a_2／a_5 撞 12 輪上限但 part 已寫、finalize 過 |
| a1_numbers | 15 | 1.09M | 預算 1.2M 內 |
| a2_digest | 17 | 2.54M | 超 1.5M → 熔斷停下，`--accept-over-budget` 放行 |
| Stage 0 合計 | | 7.9M | Koyfin 零 LLM、清單先 merge、peers 早停三項修正皆生效；無重派 |
