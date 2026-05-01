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

## Site composition：research.investmquest.com 由四個 repo 組成

公開站 `https://research.investmquest.com/` 的最終 `docs/` 內容並非全部來自本 repo，而是由四個獨立 repo 共同產生，各自擁有 `docs/` 子路徑的不同部分。任何「整站樣板/頁首/頁尾統一」這類任務，第一步要先判斷該頁路徑屬於哪個 repo，再去對應 repo 改 generator template，而不是只改本 repo `docs/` 內檔案（會被外部 cron 覆蓋）。

| Repo | 路徑 | 擁有的 docs/ 子路徑 |
|---|---|---|
| **financial-analysis-bot**（本 repo） | `/Users/ivanchang/financial-analysis-bot` | 首頁、`earnings/`、`research/`、`pm/`、`dd/`、`id/`、`markets.html`、`sectors.html`、`screener.html`、`screener-tw.html`、`how-to.html`、加上 `briefing/index.html` 與 `six-state/index.html`（**只有 index 落地頁**，內容報告由其他 repo 寫入） |
| **minervini-quality-backtest** | `/Users/ivanchang/minervini-quality-backtest` | `qgm/latest.html`、`qgm/archive/*`、`qgm-tw/latest.html`、`qgm-tw/archive/*`。生成器：`live/daily_screener.py`（Jinja2 內嵌 HTML），`.github/workflows/daily_screener_us.yml` / `daily_screener_tw.yml` 每日 cron，commit 訊息 `QGM US/TW screener update YYYY-MM-DD`，author `github-actions[bot]`，**直接 push 到本 repo main** |
| **morning-briefing** | `/Users/ivanchang/morning-briefing` | `briefing/YYYY-MM-DD.html`（每日簡報）、`weekly/*`（週報）、可能含 earnings 流程。workflows：`daily_briefing.yml`、`earnings_only.yml`、`weekly_report.yml` |
| **v7-backtest** | `/Users/ivanchang/v7-backtest` | `backtest/*`（GEM dual momentum、slope filter、turtle、QQQ short、Clenow trend following 等回測模組）、可能含 `six-state/` 的報告內容 |

### 判斷某個 docs/ 路徑屬於哪個 repo

- 規則速查：`qgm/`、`qgm-tw/` → minervini-quality-backtest；`briefing/YYYY-*`、`weekly/`、可能 `earnings/` → morning-briefing；`backtest/`、可能 `six-state/` 的報告檔 → v7-backtest；其餘 → 本 repo
- 不確定時：`git -C <repo> log --oneline -- docs/<path>` 看哪個 repo 有歷史
- 訊號：本 repo `git log` 顯示 commit author = `github-actions[bot]` 但 `.github/workflows/` 裡找不到對應 workflow → 該路徑由外部 repo cron push 過來

### 工作流程

- 接到「整站頁首/頁尾改 XX」「為什麼某個子頁面長得不一樣」這類任務：先判斷該路徑屬於哪個 repo，到對應 repo 改 template，再考慮要不要同時 patch 已經渲染好的檔案
- 若用戶只要立即修好渲染後的 HTML（不在意被覆蓋），可以只改本 repo `docs/` 下的檔案，但**必須提醒用戶下次外部 cron push 會覆蓋**
- 改外部 repo 是新的 commit/push 範圍，**動手前先跟用戶確認**（不在預設 git push 授權範圍內）

## Workflow: push earnings / 發布財報

When the user says **"push earnings"** or **"發布財報"** (any variant: "發佈財報", "發布新財報", "更新 earnings index"), run the following end-to-end without asking:

### Step 1 — Scan `docs/earnings/`

List every file matching `earnings_YYYY-MM-DD.html` (single-day reports). Ignore `index.html` and any `earnings_week_of_*.html` (weekly summaries — separate workflow).

### Step 2 — Parse existing index

Read `docs/earnings/index.html`. Extract every `href="earnings_YYYY-MM-DD.html"` that appears **inside a real `<li><a>` element** within `<ul class="reports">` — **not** hrefs that appear inside HTML comments like the `<!-- ADDING A NEW REPORT ... -->` template example. Those are the dates already published.

### Step 3 — Compute diff

`missing = files_in_folder − dates_in_index`. If `missing` is empty, reply **"already up to date"** and do NOT commit, do NOT push. Stop here.

### Step 4 — Extract metadata per missing report

For each missing `earnings_YYYY-MM-DD.html`:

1. **Takeaway** — read `<div class="report-lede">`. Strip HTML tags, drop the leading `<strong>核心發現：</strong>` (or similar) prefix. The lede is usually 2–4 sentences separated by `；`. **Summarize** it into **one short line (≤ 25 words Chinese)** with 2–3 key themes joined by ` · `. Example:
   - Lede: "Intel 以 $0.29 EPS + Foundry 營收 $5.42B 啟動 CPU 復活敘事；NextEra 被美國商務部選中開發 9.5 GW gas-fired generation...；ServiceNow 遭中東衝突深跌 15%，beat-but-no-raise 繼續被懲罰..."
   - Takeaway: `INTC blowout · Gas-fired AI power thesis · Beat-but-no-raise 被懲罰`

   Use the tickers/themes that actually appear in the lede. Do not invent.

2. **Company count** — prefer the number in `<div class="report-meta">N companies analyzed</div>`. Fallback: count `<div class="company-card">` occurrences.

3. **Date formatting** — convert `YYYY-MM-DD` to `Month DD, YYYY` (English full month name, no leading zero on day) and compute 3-letter English weekday (`Mon`/`Tue`/`Wed`/`Thu`/`Fri`/`Sat`/`Sun`).

### Step 5 — Build new `<li>` entries

For each missing report, produce:

```html
      <li>
        <a href="earnings_YYYY-MM-DD.html">
          <div class="date">Month DD, YYYY</div>
          <div class="meta">
            <span class="latest-tag">Latest</span>
            <span class="weekday">Day</span>
            <span class="companies">N companies</span>
          </div>
          <div class="takeaway">TAKEAWAY</div>
        </a>
      </li>
```

Rules:

- Indent the `<li>` at 6 spaces (it sits inside `<ul class="reports">` which is at 4-space indent inside `<div class="container">`).
- Include `<span class="latest-tag">Latest</span>` **only on the newest entry** (the first `<li>` after sort). When adding a report that becomes the new latest, remove `latest-tag` from the previously-first `<li>`.

### Step 6 — Merge + sort the list

Load existing `<li>` entries from `index.html`, add the new ones, then sort **descending by date** (newest first). Replace the entire contents of `<ul class="reports">` with the sorted list.

Preserve the `<!-- ADDING A NEW REPORT: ... -->` template comment (put it at the top of the `<ul>`, before the first `<li>`) so future entries have the example in place.

### Step 7 — Remove empty-state

If `<div class="empty-state">尚未發布分析報告…</div>` is still present in `index.html` and the new `<ul>` has ≥ 1 `<li>`, delete the entire `<div class="empty-state">…</div>` block.

### Step 8 — Commit and push

```bash
git add docs/earnings/
git commit -m "Add earnings analysis: YYYY-MM-DD[, YYYY-MM-DD ...]"
git push origin main
```

Commit subject lists the newly added dates (comma-separated, ascending). If the push is rejected (remote has new commits), `git pull --rebase origin main` then push again. Abort if rebase conflicts.

### Step 9 — Report back

Output a short summary:

```
Added:   YYYY-MM-DD (N companies), YYYY-MM-DD (M companies), ...
Skipped: <list any files that failed to parse, with reason> (or "none")
Index now contains: K report(s)
Live: https://research.investmquest.com/earnings/
```

### Edge cases

- **No `<div class="report-lede">`** — mark the entry with takeaway `(lede missing — review manually)` and add to the `Skipped` list in the report; still create the `<li>` so the link isn't orphaned.
- **Takeaway overflows one line** on the rendered page — the user asked for a single short line; if a lede is genuinely too sparse to condense, prefer `company ticker · theme · theme` over verbose sentences.
- **Filename doesn't match `earnings_YYYY-MM-DD.html`** — ignore silently (covers weekly summaries, drafts, .DS_Store, etc.).
- **Duplicate date in folder but index already has it** — not missing; no action.
- **Pre-existing untracked `docs/id/ID_*.html`** — never stage these; use `git add docs/earnings/` (directory-scoped) so unrelated untracked files are not pulled in.

### What NOT to do

- Do not re-style the HTML, change CSS, or touch files outside `docs/earnings/`.
- Do not edit nav on other pages (they already link to `/earnings/`).
- Do not open a PR. This is a direct push to `main`, same as existing `publish_dd.sh` flow.
- Do not amend commits once pushed. If a mistake is found, make a new commit.

## Git pre-commit hook（dd/id-meta validator）

Repo 內建 pre-commit hook 在 `scripts/hooks/pre-commit`，commit 前自動跑 `validate_dd_meta.py` + `validate_id_meta.py`，不過違反 schema 的檔案無法 push（鏡像 GitHub Actions strict gate 在本機提早攔截）。只在 staged files 觸及 `docs/dd/DD_*.html` / `docs/id/ID_*.html` / validator script 本身時才跑，其他 commit 無感。

**新機器 / 新 clone 啟用：**

```bash
bash scripts/install_hooks.sh
```

只跑這一次（會把 `core.hooksPath` 指向 `scripts/hooks/`）。Bypass：`git commit --no-verify`。Uninstall：`git config --unset core.hooksPath`。

