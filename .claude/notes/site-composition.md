# Site composition：research.investmquest.com 由四個 repo 組成

公開站 `https://research.investmquest.com/` 的最終 `docs/` 內容並非全部來自本 repo，而是由四個獨立 repo 共同產生，各自擁有 `docs/` 子路徑的不同部分。任何「整站樣板/頁首/頁尾統一」這類任務，第一步要先判斷該頁路徑屬於哪個 repo，再去對應 repo 改 generator template，而不是只改本 repo `docs/` 內檔案（會被外部 cron 覆蓋）。

| Repo | 路徑 | 擁有的 docs/ 子路徑 |
|---|---|---|
| **financial-analysis-bot**（本 repo） | `/Users/ivanchang/financial-analysis-bot` | 首頁、`earnings/`、`research/`、`pm/`、`dd/`、`id/`、`markets.html`、`sectors.html`、`screener.html`、`screener-tw.html`、`how-to.html`、加上 `briefing/index.html` 與 `six-state/index.html`（**只有 index 落地頁**，內容報告由其他 repo 寫入） |
| **minervini-quality-backtest** | `/Users/ivanchang/minervini-quality-backtest` | `qgm/latest.html`、`qgm/archive/*`、`qgm-tw/latest.html`、`qgm-tw/archive/*`。生成器：`live/daily_screener.py`（Jinja2 內嵌 HTML），`.github/workflows/daily_screener_us.yml` / `daily_screener_tw.yml` 每日 cron，commit 訊息 `QGM US/TW screener update YYYY-MM-DD`，author `github-actions[bot]`，**直接 push 到本 repo main** |
| **morning-briefing** | `/Users/ivanchang/morning-briefing` | `briefing/YYYY-MM-DD.html`（每日簡報）、`weekly/*`（週報）、可能含 earnings 流程。workflows：`daily_briefing.yml`、`earnings_only.yml`、`weekly_report.yml` |
| **v7-backtest** | `/Users/ivanchang/v7-backtest` | `backtest/*`（GEM dual momentum、slope filter、turtle、QQQ short、Clenow trend following 等回測模組）、可能含 `six-state/` 的報告內容 |

## 判斷某個 docs/ 路徑屬於哪個 repo

- 規則速查：`qgm/`、`qgm-tw/` → minervini-quality-backtest；`briefing/YYYY-*`、`weekly/`、可能 `earnings/` → morning-briefing；`backtest/`、可能 `six-state/` 的報告檔 → v7-backtest；其餘 → 本 repo
- 不確定時：`git -C <repo> log --oneline -- docs/<path>` 看哪個 repo 有歷史
- 訊號：本 repo `git log` 顯示 commit author = `github-actions[bot]` 但 `.github/workflows/` 裡找不到對應 workflow → 該路徑由外部 repo cron push 過來

## 工作流程

- 接到「整站頁首/頁尾改 XX」「為什麼某個子頁面長得不一樣」這類任務：先判斷該路徑屬於哪個 repo，到對應 repo 改 template，再考慮要不要同時 patch 已經渲染好的檔案
- 若用戶只要立即修好渲染後的 HTML（不在意被覆蓋），可以只改本 repo `docs/` 下的檔案，但**必須提醒用戶下次外部 cron push 會覆蓋**
- 改外部 repo 是新的 commit/push 範圍，**動手前先跟用戶確認**（不在預設 git push 授權範圍內）
