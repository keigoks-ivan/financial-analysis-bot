# 已退役 workflow 歸檔

從 `CLAUDE.md` 移出的退役段落全文保留於此。CLAUDE.md 原位只留一行指標，避免 always-on context 一直背這些死規則。

---

## Workflow: 產業 DS（敘述型產業研究）— 【DEPRECATED 2026-06-11，已併入 industry-analyst v2.0】

`industry-ds`（DS 敘述報告）已於 2026-06-11 停用，**併入 `industry-analyst` v2.0**。v2.0 走「敘事為骨、表格為窗」單一架構，用 DS 的因果敘事弧當骨架、ID 的決策資產當器官嵌入，吸收了 DS 的敘事弧 / 因果閉合 / 推導鏈 / §末 aside 來源系統。

**觸發語轉向**：原 DS 觸發語（「{主題} ds」/「ds {主題}」/「{產業} 敘述報告」/「分析 {產業} 的供需循環」/「{產業} 歷史與未來」/「discourse {industry}」）現在一律觸發 `industry-analyst`（v2.0），輸出寫 `docs/id/`（不再寫 `docs/ds/`）。

**Legacy DS 報告**：既有 8 份 `docs/ds/DS_*.html` 凍結為 legacy，檔案不動、不 retrofit、不遷移，仍在 `https://research.investmquest.com/ds/` 上站。需 review / patch / 驗證 legacy DS 時走 `id-review --mode ds`（DS-mode 8 條檢查清單仍在）；**不要用 industry-ds 生新 DS**。

**Plumbing（僅供 legacy DS 維護參考）**：`scripts/validate_ds_meta.py`（驗 `ds-meta`，pre-commit hook 仍跑）、`scripts/build_ds_category_pages.py`（重生 `docs/ds/cat-*.html`）、`scripts/init_ds_index.py`（一次性 bootstrap）。Taxonomy 與 ID 共用（`docs/id/taxonomy.md`）。

---

## deep-conviction-analyst（DCA）— 【DEPRECATED 2026-06-22，已併入 stock-analyst v13】

舊架構是「DD（基本面）+ DCA（決策層）兩份報告」。v13 起把兩者整併成**單一報告 `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`**：Part I 基本面深度（§1-§11，骨幹 ≥60%）+ Part II 決策層（§12 矛盾裁決 / §13 pre-mortem+Max DD / §14 統一裁決 / §15 複審），收斂為一個統一裁決：進場 / 觀望 / 迴避（+ 倉位角色）。

原 DCA 觸發語（「{ticker} dca」/「{ticker} 定見」/「conviction analysis {ticker}」/「最終判斷 {ticker}」/「該不該進場 {ticker}」/「買不買 {ticker}」）現在一律改觸發 `stock-analyst`（現 v14.x）。skill stub `.claude/skills/deep-conviction-analyst/SKILL.md` 僅作 deprecation 重導向，不再產獨立 `docs/dca/DCA_*.html`。

既有 343 份 legacy `docs/dca/DCA_*.html` 凍結保留、仍在站上，下游聚合器以 dual-read 支援（v13 dd-meta 決策層欄位優先，讀不到才 fall back legacy DCA）。設計細節見 `docs/_handoff_v13_dd_design_20260621.md`。

---

## stock-analyst 舊版部署筆記 tmp_v8.1.2 / tmp_v9.0 — 【已移除 2026-07-11】

`tmp_v8.1.2_deploy.md`（v8.1→v8.1.2 品質管控補丁）與 `tmp_v9.0_deploy.md`（v8.1.2→v9.0 護城河驅動 + 綜合品質分）是 stock-analyst 早期版本的一次性部署 prompt（step-by-step Edit 指令），部署早已完成。stock-analyst 現為 v14.12，完整制度沿革（v12.6→v14.12 每條規則的 WHY 與歷版摘要）見 `.claude/skills/stock-analyst/references/changelog.md`。這兩份 tmp 檔於 2026-07-11 repo 清理時 `git rm`；此處僅留一行歷史指標，內容不再保留（設計已被更新的 changelog 取代）。
