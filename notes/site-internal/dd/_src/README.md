# `_src/{TICKER}_{DATE}/` 來源檔存查

每份 v16+ DD 上站後的中間產物，供差異模式基底、事後抽查與流程重放（回溯考卷）。

| 檔 | 內容 |
|---|---|
| `{T}_{D}.evidence.json` | Stage 0 merge 後、`validate_evidence --strict` 通過的證據包 |
| `{T}_{D}.transcript_digest.json` | 0e 逐字稿摘要（PANW 為 v16.1，無此檔） |
| `{T}_{D}.judgment.json`／`.scenario.json`／`.scenario_meta.json` | 判斷 agent 產物與 `dd_scenario.py` 輸出 |
| `prose/` | 散文 agent 每段一檔 |
| `parts/` | **WP0（2026-09-05）搶救**：Stage 0 各子 agent 交回的 part 檔（`batch{n}.json` 覆蓋軸、`numbers_extra.json` 零 LLM 數字包、`numbers_agent.json`／`numbers_collect.json` 採集 agent 補值、`prior.json` 前份三區塊、`digest_path.json`），原存於 gitignored 的 `.dd_build/evidence_parts*`；有了它 Stage 0 的 merge／validate 才能重放，不只判斷→散文 |

**2026-09-05 修正**：WP0 首版把 `.dd_build/evidence_parts_crdo_20260904/` 當成 CRDO，經 WP1b 重放比對發現內容是 SNOW 2026-09-04 v16.1 dry-run 的證據（Snowflake 240 處、Credo 0 處）。已改正：`CRDO_20260904/parts/`＝真正的 Credo part 檔（原 `.dd_build/evidence_parts_crdo/`）；SNOW 那組移到 `SNOW_20260904_dryrun/`（含 evidence／judgment／scenario／scenario_meta，對應 `_audit_SNOW_20260904.md`；dry-run 未上站，無 prose）。
