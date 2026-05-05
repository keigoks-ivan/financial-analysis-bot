# Header Consistency Audit — 2026-05-03

## Canonical header

- Source: `financial-analysis-bot/docs/mental-models/index.html` lines 265–306
- Key features:
  - `<header class="imq-nav-root">` with dark-gradient CSS (`linear-gradient(135deg,#0f172a 0%,#1e293b 100%)`)
  - Logo: `InvestMQuest<span>.</span> Research` (blue dot), href `/`
  - Menu items in order: 首頁 / 研究▾ / 市場▾ / 工具▾ / 🧠 心智模型 / 📘 使用說明
  - 研究 dropdown: 個股 DD → PM 複盤 → 產業深度 ID → ⭐ 九大非共識 → 🎯 Tier Matrix
  - 市場 dropdown: 每日簡報 → 週報 → 財報分析 → Markets → Sectors → 六狀態機
  - 工具 dropdown: 量化回測 → QGM 美股 → QGM 台股 → Screener 美股 → Screener 台股
  - Inline dropdown JS (click-to-toggle + outside-click-to-close)
  - Active highlight: `.active` class on current page link and parent `.imq-dd.active`

---

## Per-page status

| URL | Repo | File | Status | Type | Issues |
|---|---|---|---|---|---|
| `/` | fab | docs/index.html | **OK** | — | — |
| `/research/` | fab | docs/research/index.html | **OK** | — | — |
| `/pm/` | fab | docs/pm/index.html | **OK** | — | — |
| `/id/` | fab | docs/id/index.html | **OK** | — | — |
| `/id/theses.html` | fab | docs/id/theses.html | **OLD_NAV** | Missing Tier Matrix; research dropdown order wrong (個股DD→產業深度ID→⭐九大非共識→PM複盤); 市場 dropdown missing 財報分析 | Fix: add `🎯 Tier Matrix` link; fix research dropdown order to match canonical |
| `/markets.html` | fab | docs/markets.html | **OLD_NAV** | Missing Tier Matrix; research dropdown order wrong (個股DD→PM複盤→產業深度ID→⭐九大非共識, no Tier Matrix); active class on 研究 dropdown (wrong — this is a 市場 page) | Fix: full nav refresh |
| `/sectors.html` | fab | docs/sectors.html | **OLD_NAV** | Missing Tier Matrix in research dropdown | Fix: add `🎯 Tier Matrix` to research dropdown |
| `/earnings/` | fab | docs/earnings/index.html | **OLD_NAV** | Missing Tier Matrix in research dropdown | Fix: add `🎯 Tier Matrix` to research dropdown |
| `/screener.html` | fab | docs/screener.html | **OLD_NAV** | Missing Tier Matrix in research dropdown | Fix: add `🎯 Tier Matrix` to research dropdown |
| `/screener-tw.html` | fab | docs/screener-tw.html | **OLD_NAV** | Missing Tier Matrix in research dropdown | Fix: add `🎯 Tier Matrix` to research dropdown |
| `/how-to.html` | fab | docs/how-to.html | **OLD_NAV** | Missing Tier Matrix in research dropdown | Fix: add `🎯 Tier Matrix` to research dropdown |
| `/mental-models/` | fab | docs/mental-models/index.html | **OK (canonical)** | — | — |
| `/briefing/` | fab (landing only) | docs/briefing/index.html | **DIFFERENT_STYLE** | No `imq-nav-root`; uses old inline div nav with only 5 flat links (首頁/每日簡報/週報/回測/六狀態機); missing all dropdowns, 心智模型, 使用說明, Tier Matrix | Full nav replacement needed |
| `/briefing/YYYY-MM-DD.html` | morning-briefing | template: briefing/html_template.py ~line 2108 | **DIFFERENT_STYLE** | Same old inline 5-link nav as briefing/index.html; ~39 existing HTML files affected; template generates all daily pages | Fix template at `html_template.py` line 2108–2116 |
| `/weekly/` (index) | morning-briefing | docs/weekly/index.html | **DIFFERENT_STYLE** | Same old inline 5-link nav; generated from weekly_template.py ~line 1160 | Fix template |
| `/weekly/YYYY-*.html` | morning-briefing | template: briefing/weekly_template.py ~line 1160 + 1221 | **DIFFERENT_STYLE** | Old inline 5-link nav (two nav blocks: line 1160 and line 1221); ~81 existing HTML files; template generates all weekly pages | Fix both nav blocks in weekly_template.py |
| `/six-state/` | fab | docs/six-state/index.html | **DIFFERENT_STYLE** | Uses plain `<header>` (not imq-nav-root); flat nav: 首頁/每日簡報/週報/回測/六狀態機 — no dropdowns, no 心智模型, no 使用說明 | Full nav replacement needed |
| `/backtest/` | fab | docs/backtest/index.html | **OLD_NAV** | Has imq-nav-root; missing 🧠 心智模型; research dropdown missing Tier Matrix; research dropdown order wrong (個股DD→PM複盤→產業深度ID→⭐九大非共識, no Tier Matrix) | Fix research dropdown + add 心智模型 |
| `/backtest/dual_track/` | fab | docs/backtest/dual_track/index.html | **OLD_NAV** | Has imq-nav-root; missing 🧠 心智模型; research dropdown missing Tier Matrix, wrong order (個股DD→產業深度ID→⭐九大非共識→PM複盤); 市場 dropdown missing 財報分析 | Fix: full nav resync |
| `/backtest/10y/` | fab | docs/backtest/10y/index.html | **OLD_NAV** | Same as dual_track above | Fix: full nav resync |
| `/backtest/long_track/` | fab | docs/backtest/long_track/index.html | **OLD_NAV** | Same as dual_track above | Fix: full nav resync |
| `/backtest/long_track_qqq/` | fab | docs/backtest/long_track_qqq/index.html | **OLD_NAV** | Same as dual_track above | Fix: full nav resync |
| `/backtest/six_state/` | fab | docs/backtest/six_state/index.html | **OLD_NAV** | Same as dual_track above | Fix: full nav resync |
| `/backtest/gem/` | fab | docs/backtest/gem/index.html | **OLD_NAV** | Same as dual_track above | Fix: full nav resync |
| `/backtest/clenow/` | fab | docs/backtest/clenow/index.html | **OLD_NAV** | Same as dual_track above | Fix: full nav resync |
| `/backtest/short_system/` | fab | docs/backtest/short_system/index.html | **OLD_NAV** | Same as dual_track above | Fix: full nav resync |
| `/backtest/slope_filter/` | fab | docs/backtest/slope_filter/index.html | **OLD_NAV** | Has imq-nav-root; missing 🧠 心智模型; research dropdown wrong order + missing Tier Matrix; 市場 dropdown missing 財報分析 | Fix: full nav resync |
| `/backtest/turtle/` | fab | docs/backtest/turtle/index.html | **OLD_NAV** | Same as slope_filter above | Fix: full nav resync |
| `/backtest/criteria/` | fab | docs/backtest/criteria/index.html | **OLD_NAV** | Same as dual_track above | Fix: full nav resync |
| `/qgm/latest.html` | minervini-quality-backtest (generator) | docs/qgm/latest.html | **DIFFERENT_STYLE** | Latest.html uses plain `<header>` with 8-link flat nav (old style); archive files correctly use imq-nav-root; generator already has imq-nav-root but latest.html hasn't been regenerated yet | latest.html is a stale copy; will auto-fix on next cron run |
| `/qgm-tw/latest.html` | minervini-quality-backtest (generator) | docs/qgm-tw/latest.html | **DIFFERENT_STYLE** | Same issue as qgm/latest.html — old flat nav | Will auto-fix on next cron run |
| `/qgm/archive/*.html` | minervini-quality-backtest (generator) | docs/qgm/archive/ | **OLD_NAV** | Has imq-nav-root (correct!); but research dropdown has wrong order (個股DD→產業深度ID→⭐九大非共識→PM複盤) and missing Tier Matrix; 市場 dropdown has wrong order (每日簡報→財報→週報→六狀態機→Markets→Sectors); 心智模型 NOT present | Generator fix needed at daily_screener.py line 393–432 |
| `/qgm-tw/archive/*.html` | minervini-quality-backtest (generator) | docs/qgm-tw/archive/ | **OLD_NAV** | Same issues as qgm/archive | Generator fix needed |
| `/backtest/slope_filter/` (v7) | v7-backtest (generator only, static file in fab) | src/slope_filter_backtest/report.py line 131 | **DIFFERENT_STYLE in generator** | Generator uses plain `<header>` flat nav; the actual file in fab/docs/ has imq-nav-root (was manually fixed); generator is out of date | Fix generator at report.py line 131–134 |

---

## Inconsistencies grouped by repo

### Repo: financial-analysis-bot (this repo, direct push)

**Files with OLD_NAV (imq-nav-root present but items missing/wrong order):**

| File | Issues |
|---|---|
| `docs/id/theses.html` | Missing Tier Matrix link; research dropdown wrong order; 市場 dropdown missing 財報分析 |
| `docs/markets.html` | Missing Tier Matrix; wrong research dropdown order; wrong active class (shows 研究.active instead of 市場.active) |
| `docs/sectors.html` | Missing Tier Matrix in research dropdown |
| `docs/earnings/index.html` | Missing Tier Matrix in research dropdown |
| `docs/screener.html` | Missing Tier Matrix in research dropdown |
| `docs/screener-tw.html` | Missing Tier Matrix in research dropdown |
| `docs/how-to.html` | Missing Tier Matrix in research dropdown |
| `docs/backtest/index.html` | Missing 🧠 心智模型 link; research dropdown missing Tier Matrix |
| `docs/backtest/dual_track/index.html` | Missing 🧠 心智模型; research dropdown missing Tier Matrix + wrong order; 市場 missing 財報分析 |
| `docs/backtest/10y/index.html` | Same as dual_track |
| `docs/backtest/long_track/index.html` | Same as dual_track |
| `docs/backtest/long_track_qqq/index.html` | Same as dual_track |
| `docs/backtest/six_state/index.html` | Same as dual_track |
| `docs/backtest/gem/index.html` | Same as dual_track |
| `docs/backtest/clenow/index.html` | Same as dual_track |
| `docs/backtest/short_system/index.html` | Same as dual_track |
| `docs/backtest/slope_filter/index.html` | Same as dual_track |
| `docs/backtest/turtle/index.html` | Same as dual_track |
| `docs/backtest/criteria/index.html` | Same as dual_track |

**Total: 19 files with OLD_NAV**

**Files with DIFFERENT_STYLE:**

| File | Issues |
|---|---|
| `docs/briefing/index.html` | No imq-nav-root; inline-div flat nav, 5 links only, no dropdowns |
| `docs/six-state/index.html` | Plain `<header>` (not imq-nav-root); flat nav, 5 links only, no dropdowns |

**Total: 2 files with DIFFERENT_STYLE**

**Note on DD/ID individual reports:**
- `docs/dd/DD_*.html` (243 files): Use old inline-div flat nav with 5 links (首頁/每日簡報/週報/回測/六狀態機). These are DIFFERENT_STYLE but were out of scope of the original user report, as individual DD reports have their own internal nav pattern.
- `docs/id/ID_*.html` (93 files): Most have imq-nav-root. 73/93 are missing 心智模型; 3/93 missing Tier Matrix. Mixed state.

**Generator in this repo:**
- `docs/backtest/_build_system_pages.py` line 486: uses old `<header>` flat nav. If re-run, it will regenerate all backtest subpages with the old nav style. Needs updating before re-running.

---

### Repo: morning-briefing (external — needs separate commit/push)

- Template files:
  - **Daily briefing nav**: `/Users/ivanchang/morning-briefing/briefing/html_template.py` lines **2108–2116**
  - **Weekly index + report nav (block 1)**: `/Users/ivanchang/morning-briefing/briefing/weekly_template.py` lines **1160–1168**
  - **Weekly report nav (block 2)**: `/Users/ivanchang/morning-briefing/briefing/weekly_template.py` lines **1221–1229**
- Pages affected by template fix:
  - **~39** daily briefing HTML files in `financial-analysis-bot/docs/briefing/YYYY-MM-DD.html`
  - **~81** weekly HTML files in `financial-analysis-bot/docs/weekly/`
  - **1** weekly index `financial-analysis-bot/docs/weekly/index.html`
- What's wrong: Both templates use old-style inline `<div>` nav with only 5 flat links. No `imq-nav-root` class, no dropdowns, no 🧠 心智模型, no 📘 使用說明, no Tier Matrix.
- Fix: Replace the inline `<div style="background:linear-gradient(...)">` nav block in each template function with the canonical imq-nav-root `<header>` block. There are **3 template locations** total (html_template.py ×1, weekly_template.py ×2).
- Template fix is single-file-per-function: **one edit per template file fixes all generated pages going forward, but existing HTML files in financial-analysis-bot/docs/ will need to be regenerated** (or batch-patched separately, since the cron will regenerate new files but not retroactively fix old ones).

---

### Repo: minervini-quality-backtest (external — needs separate commit/push)

- Generator file: `/Users/ivanchang/minervini-quality-backtest/live/daily_screener.py` lines **393–432**
- Current state of generator: Already has `imq-nav-root` style — this is good. But the nav content has defects:
  - Research dropdown **wrong order**: `個股DD → 產業深度ID → ⭐九大非共識 → PM複盤` (canonical is `個股DD → PM複盤 → 產業深度ID → ⭐九大非共識 → 🎯Tier Matrix`)
  - Research dropdown **missing Tier Matrix** link
  - 市場 dropdown **wrong order**: `每日簡報 → 財報分析 → 週報 → 六狀態機 → Markets → Sectors` (canonical is `每日簡報 → 週報 → 財報分析 → Markets → Sectors → 六狀態機`)
  - **Missing 🧠 心智模型** top-level link (only has `📘 使用說明`)
- Pages affected: **~30** archive files (`docs/qgm/archive/*.html`, `docs/qgm-tw/archive/*.html`); plus `latest.html` files (which additionally have a completely different old nav — they will auto-fix once the cron re-runs with the corrected generator).
- Fix: Single-file edit to `daily_screener.py` lines 393–432. Correct the research/市場 dropdown order, add Tier Matrix, add 🧠 心智模型 link.

---

### Repo: v7-backtest (external — needs separate commit/push)

- Generator files with stale nav:
  1. `/Users/ivanchang/v7-backtest/src/slope_filter_backtest/report.py` lines **131–134**: uses plain `<header>` with 4-link flat nav (首頁/每日簡報/週報/回測). No dropdowns, no 心智模型, no 使用說明.
  2. `/Users/ivanchang/financial-analysis-bot/docs/backtest/_build_system_pages.py` line **486**: same old `<header>` flat nav — **this file lives in financial-analysis-bot repo** but functions as a generator. Currently its generated output (backtest subpages) has imq-nav-root via manual edits, but if this script is re-run it will overwrite with old nav.
- Pages affected: `slope_filter/index.html` (currently manually fixed in docs/; generator is stale). Other backtest pages generated by `_build_system_pages.py` are also manually fixed in docs/ but the generator needs updating.
- Fix: Update both generator files to use canonical imq-nav-root block.
- Note: `six_state_backtest/backtest_six_state.py` outputs to a local `results/` directory, not to docs/, so it does not affect the live site.

---

## Summary of divergence types found

| Type | Definition | Count |
|---|---|---|
| **OK** | Matches canonical exactly (ignoring active class specific to page) | 4 pages |
| **OLD_NAV** | Has `imq-nav-root` but missing items or wrong order | 19 pages (fab) + 30 QGM archive files |
| **DIFFERENT_STYLE** | Completely different nav structure (inline div or plain `<header>`, no dropdowns) | 2 pages (fab) + ~39 briefing + ~81 weekly + 2 QGM latest.html |
| **MISSING_NAV** | No nav at all | 0 |

**Most common specific defects:**
1. **Missing `🎯 Tier Matrix`** in research dropdown — affects most pages that have imq-nav-root (predates Tier Matrix feature addition)
2. **Missing `🧠 心智模型`** top-level link — affects all backtest subpages and all morning-briefing generated pages
3. **Wrong research dropdown order** — affects backtest subpages, QGM generator, theses.html, markets.html
4. **Old inline div nav** — affects briefing/index.html, six-state/index.html, all morning-briefing generated pages, and DD/weekly individual reports

---

## Recommended fix order

1. **[morning-briefing] Template fix** (3 locations in 2 files) — fixes all ~120 briefing/weekly pages in one shot, highest user-visible impact since these are daily-viewed pages. Template paths: `html_template.py:2108`, `weekly_template.py:1160`, `weekly_template.py:1221`.

2. **[financial-analysis-bot] fab main repo direct-edit pages** (19 files) — direct push, no external dep. Priority sub-order:
   - `docs/briefing/index.html` and `docs/six-state/index.html` (DIFFERENT_STYLE → full replacement)
   - `docs/backtest/*/index.html` (11 files — all missing 心智模型 + Tier Matrix + wrong order)
   - `docs/id/theses.html` and `docs/markets.html` (wrong active + wrong order)
   - `docs/sectors.html`, `docs/earnings/index.html`, `docs/screener.html`, `docs/screener-tw.html`, `docs/how-to.html` (just missing Tier Matrix in research dropdown)

3. **[minervini-quality-backtest] Generator fix** — single file `daily_screener.py`. Fix research + 市場 dropdown order, add Tier Matrix + 心智模型. Next cron run will propagate to all new QGM pages; existing archive files need either re-generation or a separate batch patch.

4. **[v7-backtest / fab] Generator fix** — `src/slope_filter_backtest/report.py` and `docs/backtest/_build_system_pages.py`. Prevent regression if these scripts are ever re-run.

---

## Active class audit (correct vs incorrect)

| Page | Expected active | Actual active | Correct? |
|---|---|---|---|
| `/` | `<a href="/" class="active">首頁</a>` | ✓ | OK |
| `/research/` | research dropdown + 個股DD | ✓ | OK |
| `/pm/` | research dropdown + PM複盤 | ✓ | OK |
| `/id/` | research dropdown + 產業深度ID | ✓ | OK |
| `/id/theses.html` | research dropdown + ⭐九大非共識 | ✓ | OK |
| `/markets.html` | 市場 dropdown + Markets | **研究.active + theses.html.active** | WRONG |
| `/sectors.html` | 市場 dropdown + Sectors | ✓ | OK |
| `/earnings/` | 市場 dropdown + 財報分析 | **earnings.active on wrong page (sectors)** | WRONG |
| `/screener.html` | 工具 dropdown + Screener美股 | 市場.active + earnings.active | WRONG |
| `/screener-tw.html` | 工具 dropdown + Screener台股 | None | MINOR_DIFF |
| `/how-to.html` | `📘 使用說明.active` | ✓ | OK |
| `/mental-models/` | `🧠 心智模型.active` | ✓ | OK |
| `/backtest/*/` | 工具 dropdown + 量化回測 | ✓ | OK |
