# dd2：DD 管線 v20 原型（實作契約）

設計稿：`notes/site-internal/dd/_dd_v20_clean_design_20260916.md`。本檔是給實作者看的模組契約。
原則：**舊鏈 `scripts/ddreport.py` 與 `dd_*.py` 一字不改**，dd2 只重寫「指揮流程」，零 LLM 工具全部沿用。

## 0｜三個先講清楚的決定

1. **判斷物形狀＝v19 契約**（`scripts/dd_schema/judgment.schema.json` 頂層 `v19_contract`，`meta.contract="v19"`）。不另立 v20 schema。理由：v19 契約已經只剩判斷者該填的欄，`dd_project.py`／`validate_judgment.py`／`gen_dd_tables.py`／`dd_brief.py` 全部認它。卡裡的欄名（`moat.trend`、`counter_evidence.blind_spots` 等）就是 v19 契約的欄名。
2. **判斷 JSON 本體約 33K 到 40K 字**（TXN／FIX v19 實測），不是設計稿寫的 5 到 8KB。判斷通省的是：單輪（不再 4 輪重讀 640K cache）、零修補輪、思考設上限。輸出目標改為：JSON ≤ 30K 字、思考 ≤ 32K token。
3. **散文由 sonnet 寫**（設計稿 §4.4）。v19 於 2026-09-11 曾改成判斷者直接寫給讀者的文字、取消散文通；v20 反向，理由是 Fable 輸出貴、sonnet 便宜。TXN 對照時要比這兩種的總價。

## 1｜run dir 與 manifest（與舊鏈同布局，讓 finish／brief／gates 直接可用）

```
.dd_build/runs/{T}_{D}/
  evidence.json  axes.json  facts.json  judgment.json  scenario.json  scenario_meta.json
  gate_result.json  gate_audit.md
  parts/  prompts/  agents/  bundles/  tables/  prose/  prose_A.html  prose_B.html
  manifest.json
```

manifest 沿用舊鏈鍵：`ticker`／`date`／`state`／`stages`。`stages` 用 `ddreport.STAGE_ORDER` 的名字
`stage0`／`judged`／`gated`／`brief`／`prose`，每段 `{"state": "PASS|FAIL|RUNNING", "agent_usage": [...], "started", "finished"}`。
v20 多一段 `facts`（零 LLM）。`ddreport.py finish` 要求 stage0／judged／gated／brief 為 PASS（有 prose 段時也要 PASS），見 `_finish_required_stages`。

`state` 字串沿用舊鏈：`planned`／`stage0_pass`／`judged_pass`／`judged_fail`／`gated_pass`／`gated_fail`／`brief_pass`／`prose_pass`／`prose_fail`。

## 2｜證據庫 `facts/{T}/`（新，`facts_store.py`）

```
facts/{T}/
  axes/{axis_id}.json     {"axis": id, "fetched_at": "YYYY-MM-DD", "run": "T_D", "status", "queries_run", "findings": [...], "note"}
  numbers.json            {"fetched_at", "run", "quarter": "...", "latest_quarter_kpis": {...}}
  transcripts.json        {"fetched_at", "files": [...], "latest_quarter": "..."}
```

保存期限（設計稿 §5，2026-09-16 拍板）：

| 軸 id | 期限（天） | 強制刷新 |
|---|---|---|
| numbers（latest_quarter_kpis） | 到下一次財報 | evidence.earnings_recency 出現新一季 |
| competitive_share_entrants、customer_second_source、customer_concentration_credit、supply_demand_durability、end_markets、channel_business_model_shift | 90 | 新一季逐字稿出現 |
| regulatory_antitrust、reg_tariff_export、geo_supply_chain、substitute_technology | 180 | 無 |
| capital_markets_pricing | 30 | 股價相對上次 fetch 變動 > 20% |
| major_events | 14 | 無 |

API：
```python
store = FactsStore(repo_root, ticker)
plan = store.plan_refresh(axis_ids, today, *, new_quarter: bool, price_move_pct: float|None)
#  -> {"stale": [axis_id...], "fresh": {axis_id: axis_obj_with_reused_from_and_age_days}}
store.put_axis(axis_id, axis_obj, fetched_at, run_id)      # gather 後回存
store.put_numbers(obj, fetched_at, run_id, quarter)
store.numbers_fresh(new_quarter: bool) -> obj | None
store.seed_from_evidence(evidence_dict, fetched_at, run_id)  # 一次性從舊 run 的 evidence.json 灌入
```
規則表放檔頂常數 `TTL_DAYS`／`FORCE_REFRESH`；未知軸 id 預設 90 天。

## 3｜LLM 通（`spawn.py`）

包一層 `scripts/dd_headless.spawn`。**只有兩種呼叫**：
```python
oneshot(prompt_path, model, out_json, cwd, *, thinking_cap=None)  # 無工具、max_turns=1；回 result_text
agentic(prompt_path, model, out_json, cwd, tools, max_turns, budget_cache_read)  # 查／寫兩通用
```
`oneshot` 回傳 dict 同 dd_headless（`ok`／`result_text`／`output_tokens`／`cache_read`／`cost_usd`／`by_model`），另加 `thinking_tokens`（從 raw JSON `modelUsage.*.thinkingTokens` 取）。
`thinking_cap` 以環境變數 `MAX_THINKING_TOKENS` 傳給子行程（**未經驗證**，實作時先用 sonnet 小 prompt 實測是否生效，把結果寫進本檔 §7）。
另實測：每個 `claude -p` 子行程的 `modelUsage` 都出現一筆 haiku 約 100K input（TXN 09-10 judge_1 實錄，$0.10／通）。找出來源（slim 旗標下仍有？`--tools ""` 下仍有？），能關就關，關不掉就記錄。

## 4｜prompt 組裝（`bundle.py` ＋ `prompts/*.md.tmpl`）

沿用 `scripts/dd_bundle.py` 的段落函式，不重寫：
- 判斷：`_task_header_v19` 不用（改用 `prompts/judge.md.tmpl`）＋ `_schema_cheatsheet("v19")` ＋ `_facts_section(facts_path)` ＋ `_transcript_section(evidence, None)` ＋ `cards/judge_card.md` ＋ 常載附卡 roic／playbook ＋ 條件附卡（讀 `evidence.archetype_hint`／`judgment` 未有時用 evidence 的 archetype，命中 `cards/judge_addendum_*.md` 檔頭 `load-when`）＋ 前份判斷摘要（從 `parts/prior.json` 的 `prior_dd` 取 verdict／role／H／R／Single Thing／kill_metrics／rearm_trigger，≤ 5KB）。**不放** `_evidence_compact`、`_digest_section`、`judgment-rules-v19.md` 全文。
  尾段沿用 `scripts/dd_prompts/judge_oneshot_tail.md.tmpl` 的 `scenario_inputs` 形狀範本與「緊湊 JSON」條款，但改寫成「回覆全文即 JSON，陣列外不得有文字」，刪掉「Write」「下一次呼叫」「只准改被點名欄位」等字句。
- 閘：`prompts/gate.md.tmpl`（任務頭一段）＋ `cards/gate_card.md` ＋ `_gate_referenced_facts_section(raw_judgment, facts)` ＋ `_gate_scenario_meta_section(judgment_path)` ＋ judgment.json 全文（緊湊）。輸出契約：JSON 陣列 `[{"item","light","judgment_path","reason"}]`。
- 散文：`_prose_task_header(judgment, evidence)` ＋ `_table_listing_section(tables_dir)` ＋ `_prose_budget_section(judgment_path, tables_dir)` ＋ `_numbers_whitelist_section(judgment)` ＋ `_mechanical_sids_section(prose_dir)` ＋ `cards/prose_card.md` ＋ judgment 投影視圖（`dd_project.view_for`，緊湊）。輸出：`prose_A.html`（s1–s7）、`prose_B.html`（s8–s12＋decision）寫在 run_dir，SID 標記格式見 prose_card §6。

每個 builder 回傳寫好的 prompt 路徑與 bytes 數，並把各段 bytes 記進 manifest（`bundle_bytes`）。

## 5｜主流程（`run.py`，orchestrator 自寫）

```
plan     python3 scripts/ddreport.py plan T --date D --reuse-days 0 [--archetype][--peers]   （零 LLM 準備：evidence init、axes、prior、numbers_extra、Koyfin、a1_numbers prompt）
stage0   facts_store.plan_refresh → 過期軸每軸一通 sonnet（coverage.md.tmpl，_axis_block([axis])）＋ numbers 一通（沿用 plan 產的 prompts/a1_numbers.md，若 store 有新鮮 numbers 則跳過）
         → 每 part `validate_evidence.py --part` → `dd_evidence.py merge` → 新鮮軸從 store 注入（帶 reused_from／age_days）→ `dd_evidence.py finalize --run-dir`
         → store.put_axis／put_numbers 回存
facts    dd_facts.py extract --run-dir → facts.json；dd_facts.py check（零 LLM，不開 sonnet 補題）
judged   bundle.build_judge → oneshot(fable, thinking_cap=32000) → 剝 code fence → json.loads → 寫 judgment.json（縮排）
         → ddreport._judge_check(T, D)；FAIL → `dd_project.py normalize --write` 一次 → 再 check；仍 FAIL → stage FAIL，停
gated    bundle.build_gate → oneshot(opus) → json.loads 陣列 → gate_result.json ＋ gate_audit.md（人讀版）；任一 🔴 → FAIL，停
brief    ddreport._do_brief(T, D, do_full=True, manifest)
prose    ddreport._do_prose_prepare(T, D) → bundle.build_prose → agentic(sonnet, tools=["Write"], max_turns=6)
         → ddreport._do_prose_split(T, D) → ddreport._run_gates(run_dir, T, D) ＋ _prose_depth_findings；FAIL → 停
finish   python3 scripts/ddreport.py finish T D [--no-push]
```
每段結束把 usage 加進 manifest；結尾印設計稿「回報格式」那六項。exit code：0 成功、2 遠端領先、其餘 FAIL。

## 6｜測試

`scripts/tests/test_dd2_*.py`，pytest。facts_store 用 tmp_path；bundle 用 `.dd_build/runs/FIX_20260911/`（有 facts.json／judgment.json／evidence.json）當 fixture 只讀；spawn 只測參數組裝（monkeypatch subprocess）。

## 7｜實測紀錄（實作者填）

- **MAX_THINKING_TOKENS 是否生效：單獨設 env 無效，須搭配 Claude Code 既有的 thinking 觸發詞**。
  指令：`s.oneshot(prompt_path=P, model="sonnet", out_json=O, cwd=".", thinking_cap=1024)`（`s`＝`dd2.spawn`，`P`＝23 人握手推理題 `thinking_prompt.md`）。
  無觸發詞：env 無設定、`thinking_cap=1024` 兩次，raw JSON `modelUsage.claude-sonnet-5.thinkingTokens` 皆為 0。
  改用帶 Claude Code 觸發詞「ultrathink：」的同題（`thinking_prompt_ultrathink.md`）：不設 env 仍 0；`thinking_cap=1024` 時變 **48**（`usage.output_tokens_details.thinking_tokens` 同步 48）；另試 `--effort low`（無觸發詞、無 env）也是 0，非替代解法。
  結論：env 真的傳到子行程且設了思考上限，但只有 prompt 同時帶觸發詞才會被用到——只設 `thinking_cap` 不改 prompt 措辭沒有效果。

- **haiku 開銷來源與能否關閉：關不掉，且與 slim／`--tools` 設定無關，只看 prompt 內容**。
  指令：同一支 `thinking_prompt.md` 分別在 (a) 預設（`DD_HEADLESS_SLIM` 未設，slim 開）、(b) `DD_HEADLESS_SLIM=0`、(c) `dd_headless.spawn(..., extra_args=["--tools", "default"])`（拿掉工具限制）下各跑一次。
  三次 raw JSON 的 `modelUsage.claude-haiku-4-5-20251001.inputTokens` 都是 **1042**，完全不隨設定變動；換成近乎空白的 `只回 OK` 提示測同三種設定，三次都**沒有** haiku 項。
  （原題「加 `--tools \"\"`」已用假 binary＋`FAKE_CLAUDE_LOG` 零成本驗證：argv 與預設逐字相同——`dd_headless.py` L178-183 對無工具呼叫本就自動補 `--tools ""`，故第三組改測「移除限制」才有鑑別力。）
  結論：haiku 呼叫觸發與否、輸入量大小只看 prompt 內容長短，與 slim／`--tools` 無關，現有旗標關不掉；raw JSON 無欄位標明用途，維持 `dd_headless.py` 註解「可能是 Claude Code 內部分類／摘要呼叫」的推測，只能如實記錄進 manifest。

## 8｜TXN 2026-09-16 首次端到端（dry-run，證據庫先由 TXN_20260910 灌入）

| 段 | 通數 | 花費 | 時間 | 結果 |
|---|---|---|---|---|
| plan | 0 | $0 | 5 分（Koyfin 逾時 300s 後改讀磁碟） | PASS |
| stage0 | 0（12 軸＋numbers 全沿用） | $0 | 秒級 | PASS |
| facts | 0 | $0 | 秒級 | PASS（36 條機械事實／53 條 findings_digest） |
| judged | 1（Fable 單輪） | $3.52 | 11 分 | 第 3 跑 PASS（第 1 跑 23 FAIL、第 2 跑 2 FAIL，見下） |
| gated | 1（opus 單輪） | $0.96 | 2.7 分 | 🔴 3 🟡 3 → 照設計停下 |

對照舊鏈 TXN_20260910（同樣沿用證據）：stage0 $1.25／judged $6.67（1 主＋3 修補）／gated $1.32，合計 $9.24。v20 到閘為止 $4.48。

判斷三跑的 FAIL 演變（全部靠「把規則餵進 bundle」解決，未開修補輪）：
1. 23 FAIL：enum 欄填自由文字（v19 速查沒列 archetype／cycle_* enum）→ 加 `enum_sheet()`；前份 20 欄漂移看不到（evidence 原文已拿掉）→ prior_summary 加 `drift_watch_prior`；scenario_ref 沒填 → run.py 機械填。
2. 2 FAIL：禁用詞「估值燈」→ 加 `leak_words_section()`（機械抽 dd_sections.LEAK_PATTERNS）；Single Thing 門檻變動條目措辭 → drift_rule 補句。
3. 1 FAIL：q1.single_thing 寫成指標字串 → `run.normalize_v20` 複製物件（純形狀）。

判斷三跑裁決各異：進場·條件式｜衛星 → 觀望｜追蹤 → 進場｜核心（舊鏈＝進場｜核心）。單輪 Fable 的裁決有跑間變異，驗收 §10 條件 1 要用多跑或閘後結果比，不能只比一跑。

閘三紅：⑤ `decision_inputs.ma` 無均線資料卻填 ✅（決定 row 10 vs 9b）；⑥ ROIIC 25% 無算式、再投資率取值無理由；⑧ 情境路徑變動誤歸「價格變動」。三項都是判斷級，不是形狀。閘另指出同業組（2308.TW／VRT／ETN／SU.PA）是電源系統廠不是類比 IC 廠，屬 plan 沿用 archive peers 的資料問題。

待持有人決定：閘紅燈後是否允許一通 patch map（Fable 單輪只回被點名欄位，約 $1）再重閘一次；或維持停下交人。
