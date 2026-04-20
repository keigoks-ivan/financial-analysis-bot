# Claude Skills — 研究三套

本目錄存放 3 套 Claude Code user skill，搭配 InvestMQuest Research 研究工作流使用。

| Skill | 用途 | 觸發 |
|:---|:---|:---|
| `stock-analyst/` | 個股深度 DD（quality tier / gate / trap / entry / targets）| 「研究 NVDA」「幫我跑 2330 的 DD」 |
| `industry-analyst/` | 產業深度 ID（14 章 schema，跨多檔共用產業研究） | 「研究 AI ASIC 產業」「sector 分析」 |
| `portfolio-manager/` | PM 週度複盤（core / satellite / cash sizing + 4 級 override） | 「幫我複盤組合」「portfolio rebalance」 |

## 在新電腦上安裝

Claude Code 會從 `~/.claude/skills/` 讀 user skill。直接把這三個資料夾 symlink 或 copy 過去：

```bash
# 方法 A：symlink（建議，同步更新）
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/stock-analyst"     ~/.claude/skills/stock-analyst
ln -s "$(pwd)/skills/industry-analyst"  ~/.claude/skills/industry-analyst
ln -s "$(pwd)/skills/portfolio-manager" ~/.claude/skills/portfolio-manager

# 方法 B：copy（skill 與 repo 脫鉤）
cp -r skills/* ~/.claude/skills/
```

安裝完在 Claude Code 內 `/` 面板應該看到這 3 個 skill。

## 版本現況（2026-04-20）

- **stock-analyst v12.0** — 14 章 DD 框架 + Bollinger MA 狀態機 + trap 🟡🔴 偵測
- **industry-analyst v1.4** — 14 章 ID schema + 7 Pre-Publish Gates + Reference Card
- **portfolio-manager v1.1** — 3 層架構（DD → 中性訊號 → PM 決策）+ 4 級 override

## 輸出資料夾

三套 skill 的輸出都寫入 `docs/`：
- `docs/dd/DD_{ticker}_{date}.html` — 個股 DD
- `docs/id/ID_{Theme}_{date}.html` — 產業 ID
- `docs/pm/PM_{date}.html` — PM 週複盤

## 來源

這些 skill 是開發過程中逐步長出來的。SKILL.md 是權威文件，其他 `*.md`（references / templates / policies / compat）是配套。
