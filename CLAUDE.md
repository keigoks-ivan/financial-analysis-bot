# Repo-wide instructions

## Decision-time critic：思考產業 thesis 動部位前必先 spawn

當用戶討論以下任一情境，**必須先 spawn `industry-thesis-critic` sub-agent** 對相關 ID 跑冷讀，再給投資建議。這是 Boris verify-app pattern 在投資決策的翻譯 — 寫 ID 的 agent 與驗 thesis 的 agent 不同。

**觸發情境**（任一即觸發）：
- 「考慮加倉 / 減倉 / 新進 / 退出 X 產業 theme」
- 「{theme} thesis 還活著嗎」
- 「該不該對 {industry} 增加 / 降低曝險」
- 「{ID 主題} 現在還能 act 嗎」
- 用戶提及具體 ID 主題並表達決策意圖（不是純資訊查詢）

**Spawn 方式**：
```
Agent({
  description: "Cold review {theme} thesis",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "You are operating as the industry-thesis-critic sub-agent. Read spec at /Users/ivanchang/.claude/agents/industry-thesis-critic.md. ID: {path}. Intent: {user 意圖}. Save report to docs/id/_critic_{Theme}_{YYYYMMDD}.md."
})
```

**不觸發**（僅資訊查詢）：
- 「ID_X 寫了什麼」/「{theme} 是什麼」/「介紹一下 {industry}」 — 純解釋型問題，直接回答即可
- 寫稿過程中（that's a separate write-time critic, P2 未實作）

**例外**：用戶明確說「不用跑 critic」/「我自己看就好」可跳過。

## Site composition：4 repos 共同產生 docs/

公開站 `https://research.investmquest.com/` 由 4 個 repo 共同生成 `docs/` 內容。任何「整站樣板/頁首/頁尾」這類任務，第一步要先判斷該頁路徑屬於哪個 repo，再去對應 repo 改 generator template。

**速查**：
- `qgm/`、`qgm-tw/` → minervini-quality-backtest
- `briefing/YYYY-*`、`weekly/`、可能 `earnings/` 流程 → morning-briefing
- `backtest/`、可能 `six-state/` 報告檔 → v7-backtest
- 其餘（首頁、`earnings/`、`research/`、`pm/`、`dd/`、`id/`、`markets.html`、`sectors.html`、`screener*.html`、`how-to.html`、`briefing/index.html`、`six-state/index.html`）→ 本 repo

不確定時：`git -C <repo> log --oneline -- docs/<path>` 看哪個 repo 有歷史。改外部 repo 是新的 commit/push 範圍，**動手前先跟用戶確認**。

詳細 4-repo 表格 + 每個 repo 的 generator/workflow/commit author：見 `.claude/notes/site-composition.md`。

## Workflow: push earnings / 發布財報

當用戶說「push earnings」/「發布財報」/「發佈財報」/「發布新財報」/「更新 earnings index」時，自動觸發 `push-earnings` skill（`.claude/skills/push-earnings/`），照其 9 個 steps 執行。

## Workflow: DCA 深度定見分析

當用戶說「幫我跑 {ticker} dca」/「{ticker} 定見」/「{ticker} dca」/「conviction analysis {ticker}」/「最終判斷 {ticker}」時，自動觸發 `deep-conviction-analyst` skill（`.claude/skills/deep-conviction-analyst/`）。

**定位**：DD 之上的「投資決策層」 — Phase A 三軸獨立搜尋（護城河 / 產業趨勢 / 業務財務） + Phase B 矛盾辨識與強制裁決 + Phase C PM 決策框架（§2 thesis、§7 倉位+opportunity cost、§5 single-thing、§6 pre-mortem）。

**輸出**：
- HTML：`docs/dca/DCA_{TICKER}_{YYYYMMDD}.html`（不放 `docs/dd/`，避免被 `validate_dd_meta.py` 鎖規則）
- 索引：`docs/dca/INDEX.md`（skill 自動 append）
- Research 頁同步：跑 `python scripts/update_dd_index.py` 後，「定見」欄會自動連到該 ticker 最新的 DCA 報告

## Workflow: 產業 DS（敘述型產業研究）

當用戶說「{主題} ds」/「ds {主題}」/「{產業} 敘述報告」/「分析 {產業} 的供需循環」/「{產業} 歷史與未來」/「discourse {industry}」時，自動觸發 `industry-ds` skill（`.claude/skills/industry-ds/`）。

**定位**：與 `industry-analyst`（產業 ID）並列的姊妹 skill — ID 給 PM 表格 dashboard 快速決策、DS 給供需循環敘事深度準備。同 theme 可並存（DS `ds-meta.related_ids[]` 指向同主題 ID，§0 顯示 cross-link callout）。

**章節骨架（不可動）**：§0 TL;DR → §1 歷史 → §2 現供 → §3 未供 → §4 現需 → §5 未需（含 TAM） → §6 短中長期推估 → §7 投資時鐘 → §8 Non-Consensus → §9 Kill Scenario → §10 Catalyst → §11 關聯個股。

**硬性比例**：文字 ≥ 80%、表格 ≤ 20%（與 ID 的 ≥ 70% 表格反過來）。表格上限 4 張，每張 ≤ 8 行。

**輸出**：
- HTML：`docs/ds/DS_{Theme}_{YYYYMMDD}.html`
- 索引：`docs/ds/INDEX.md` + `docs/ds/index.html`（skill 插入卡片到 subgroup-anchor 之後）
- 分類頁：跑 `python3 scripts/build_ds_category_pages.py` 重新生成 15 個 `docs/ds/cat-{mega}.html`
- 上站路徑：`https://research.investmquest.com/ds/`（與 `/id/` 並列）

**Plumbing**：
- `scripts/validate_ds_meta.py`：驗 `<script id="ds-meta">` 欄位（pre-commit hook 會跑）
- `scripts/build_ds_category_pages.py`：mirror `build_id_category_pages.py`，從 `docs/ds/index.html` 產 cat-*.html
- `scripts/init_ds_index.py`：一次性 bootstrap（從 `docs/id/index.html` 轉換出 `docs/ds/index.html`）
- Taxonomy：完全共用 ID（`docs/id/taxonomy.md` 是單一資料源；`validate_ds_meta.py` import `validate_id_meta.TAXONOMY`）

**Critic gate**：Step 8.7 強制 spawn `id-review` skill `--mode ds`（reuse 既有 id-review，加 6 條 DS-specific 檢查：表格比 / history-future causality / 供需平衡 / §6 三情境 / §10 雙路徑 / §11 一致性）。Critic report 放 `docs/ds/_critic_{Theme}_{YYYYMMDD}.md`。

## Git pre-commit hook

Repo 有 dd/id meta validator pre-commit hook。新 clone 啟用方式與 bypass 細節：見 `scripts/README.md`。
