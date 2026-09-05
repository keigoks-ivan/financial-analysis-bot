# ID v4 裁決級 refresh 批次 — 續跑說明（2026-09-05）

本目錄是 session f38855d4 的工作副本（原在 session scratchpad，新 session 看不到）。**未追蹤、不要 commit**；用完可刪。

- `playbook_id_v4.md`：每份 ID 的派工鏈（含並行發布鎖 §8a）。新 session 的 SP 路徑要改成自己的 scratchpad；或直接把 SP 指到本目錄。
- `queue.md`／`results.md`：進度與結果表（以 `git log --oneline -- docs/id/` 為準）。
- `queue_meta.md`：各主題 mega／sub_group／ticker 清單；`prior_brief_*.md` 已全部產好。
- `scripts/`：prior_brief.py／returns.py（26W／52W vs QQQ）／tok.py（jsonl token 加總）。
- `AINetworking/`：失敗那份的 Phase 1 sketch、三輪證據包、dd-meta、returns——可從 Phase 2 重跑。

**停下原因**：WebSearch 每 session 上限 200 次、所有子 agent 共用，4 份並行約一份半就耗盡。續跑前在新 session 啟動時設 `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`（建議 ≥1500 給 18 份），並把並行數降到 2–3。
**資料警訊**：APH 2026-08-06 宣布 2:1 分割（9/2 生效），`data/weekly_cache/APH.json` 未調整，26W 報酬顯示 −57%（實約 +9%）；NVDA 自 FY27 Q1 起不再單獨揭露 Networking 營收，相關 kill metric 需改設計。
