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

## Git pre-commit hook

Repo 有 dd/id meta validator pre-commit hook。新 clone 啟用方式與 bypass 細節：見 `scripts/README.md`。
