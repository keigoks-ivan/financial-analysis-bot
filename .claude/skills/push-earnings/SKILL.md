---
name: push-earnings
description: 發布財報報告（earnings）並更新 index。觸發：用戶說「push earnings」/「發布財報」/「發佈財報」/「發布新財報」/「更新 earnings index」。掃 docs/earnings/ 找新增的 earnings_YYYY-MM-DD.html，diff 對比 index.html，提取 takeaway/company count/date，建 <li> 並排序，commit & push。
version: v1.0
date: 2026-05-03
---

# Workflow: push earnings / 發布財報

When the user says **"push earnings"** or **"發布財報"** (any variant: "發佈財報", "發布新財報", "更新 earnings index"), run the following end-to-end without asking:

## Step 1 — Scan `docs/earnings/`

List every file matching `earnings_YYYY-MM-DD.html` (single-day reports). Ignore `index.html` and any `earnings_week_of_*.html` (weekly summaries — separate workflow).

## Step 2 — Parse existing index

Read `docs/earnings/index.html`. Extract every `href="earnings_YYYY-MM-DD.html"` that appears **inside a real `<li><a>` element** within `<ul class="reports">` — **not** hrefs that appear inside HTML comments like the `<!-- ADDING A NEW REPORT ... -->` template example. Those are the dates already published.

## Step 3 — Compute diff

`missing = files_in_folder − dates_in_index`. If `missing` is empty, reply **"already up to date"** and do NOT commit, do NOT push. Stop here.

## Step 4 — Extract metadata per missing report

For each missing `earnings_YYYY-MM-DD.html`:

1. **Takeaway** — read `<div class="report-lede">`. Strip HTML tags, drop the leading `<strong>核心發現：</strong>` (or similar) prefix. The lede is usually 2–4 sentences separated by `；`. **Summarize** it into **one short line (≤ 25 words Chinese)** with 2–3 key themes joined by ` · `. Example:
   - Lede: "Intel 以 $0.29 EPS + Foundry 營收 $5.42B 啟動 CPU 復活敘事；NextEra 被美國商務部選中開發 9.5 GW gas-fired generation...；ServiceNow 遭中東衝突深跌 15%，beat-but-no-raise 繼續被懲罰..."
   - Takeaway: `INTC blowout · Gas-fired AI power thesis · Beat-but-no-raise 被懲罰`

   Use the tickers/themes that actually appear in the lede. Do not invent.

2. **Company count** — prefer the number in `<div class="report-meta">N companies analyzed</div>`. Fallback: count `<div class="company-card">` occurrences.

3. **Date formatting** — convert `YYYY-MM-DD` to `Month DD, YYYY` (English full month name, no leading zero on day) and compute 3-letter English weekday (`Mon`/`Tue`/`Wed`/`Thu`/`Fri`/`Sat`/`Sun`).

## Step 5 — Build new `<li>` entries

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

## Step 6 — Merge + sort the list

Load existing `<li>` entries from `index.html`, add the new ones, then sort **descending by date** (newest first). Replace the entire contents of `<ul class="reports">` with the sorted list.

Preserve the `<!-- ADDING A NEW REPORT: ... -->` template comment (put it at the top of the `<ul>`, before the first `<li>`) so future entries have the example in place.

## Step 7 — Remove empty-state

If `<div class="empty-state">尚未發布分析報告…</div>` is still present in `index.html` and the new `<ul>` has ≥ 1 `<li>`, delete the entire `<div class="empty-state">…</div>` block.

## Step 8 — Commit and push

```bash
git add docs/earnings/
git commit -m "Add earnings analysis: YYYY-MM-DD[, YYYY-MM-DD ...]"
git push origin main
```

Commit subject lists the newly added dates (comma-separated, ascending). If the push is rejected (remote has new commits), `git pull --rebase origin main` then push again. Abort if rebase conflicts.

## Step 9 — Report back

Output a short summary:

```
Added:   YYYY-MM-DD (N companies), YYYY-MM-DD (M companies), ...
Skipped: <list any files that failed to parse, with reason> (or "none")
Index now contains: K report(s)
Live: https://research.investmquest.com/earnings/
```

## Edge cases

- **No `<div class="report-lede">`** — mark the entry with takeaway `(lede missing — review manually)` and add to the `Skipped` list in the report; still create the `<li>` so the link isn't orphaned.
- **Takeaway overflows one line** on the rendered page — the user asked for a single short line; if a lede is genuinely too sparse to condense, prefer `company ticker · theme · theme` over verbose sentences.
- **Filename doesn't match `earnings_YYYY-MM-DD.html`** — ignore silently (covers weekly summaries, drafts, .DS_Store, etc.).
- **Duplicate date in folder but index already has it** — not missing; no action.
- **Pre-existing untracked `docs/id/ID_*.html`** — never stage these; use `git add docs/earnings/` (directory-scoped) so unrelated untracked files are not pulled in.

## What NOT to do

- Do not re-style the HTML, change CSS, or touch files outside `docs/earnings/`.
- Do not edit nav on other pages (they already link to `/earnings/`).
- Do not open a PR. This is a direct push to `main`, same as existing `publish_dd.sh` flow.
- Do not amend commits once pushed. If a mistake is found, make a new commit.
