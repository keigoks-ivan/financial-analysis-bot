# DD Screener — `latest.json` Schema (locked)

Produced by `scripts/build_dd_screener.py`, consumed by `docs/dd-screener/index.html`.
Path: `docs/dd-screener/latest.json`

This schema is the integration contract between the build pipeline and the
front-end. **Do not change field names / types without updating both sides
and bumping `schema_version`.**

v1.1 (additive, backward-compatible): adds `timing` block per stock — joined
from `docs/screener/latest.json` daily snapshot. Same source as
`flow/ath-hunter.html` consumes, so DD Screener's 起漲點 chip and Flow's ATH
classification stay in lock-step (zero data drift). null for non-US (TW/JP/EU).

v1.2 (additive, backward-compatible): propagates 6 extra dd-meta fields per
stock — `pct_5y`, `growth_durability`, `quality_score`, `ai_risk`,
`moat_execution`, `moat_pricing_power` — to power the quality-entry screener
(`docs/dd-screener/quality-entry.html`). All nullable; v12.3+ DDs carry the
two moat sub-scores, older DDs leave them `null`.

v1.3 (additive, backward-compatible): **FunnelRank (漏斗綜合排序分)**. Adds a
0–1 server-computed sort key per stock — `funnel_rank` = `0.40·quality_gate +
0.30·moat_score_adj + 0.30·revision_score` (基本面三層；時機不進分). New per-stock
fields: `funnel_rank`, `quality_gate`, `moat_score_adj`, `revision_score`,
`veto_all_downgrade`, `funnel_cap_moat_down`, `quality_gate_partial`,
`moat_no_data`, `revision_no_baseline`, `peg_fallback`. New top-level
`funnel_config` block (weights/mapping for the FE methodology panel + audit).
**`stocks[]` default sort is now `funnel_rank` DESC** (was `pass_count` DESC).
Two hard vetoes: FY1/FY2/FY3 all-downgrade → `funnel_rank=0` (+`veto_all_downgrade`);
moat trend ↓ & pass_count ≤ 4 → cap 0.50. FE adds a `回調帶` (pullback) timing
preset alongside `起漲點`. All fields additive — pre-v1.3 consumers ignore them.

## Top-level shape

```json
{
  "schema_version": "1.2",
  "run_timestamp": "2026-05-15T08:00:00+08:00",
  "as_of": "2026-05-15",
  "universe_size": 98,
  "default_preset": "MLB",

  "criteria": [
    {"key": "fcf",   "label": "FCF≥10%",  "threshold": 10.0, "invert": false, "unit": "%"},
    {"key": "roic",  "label": "ROIC≥15%", "threshold": 15.0, "invert": false, "unit": "%"},
    {"key": "eps2y", "label": "EPS≥15%",  "threshold": 15.0, "invert": false, "unit": "%"},
    {"key": "peg",   "label": "PEG≤2.0",  "threshold": 2.0,  "invert": true,  "unit": "x"},
    {"key": "de",    "label": "D/E≤0.7",  "threshold": 0.7,  "invert": true,  "unit": "x", "advisory": true}
  ],
  // 2026-07-03 (Task 1): `de` carries "advisory": true — it is DISPLAYED but does
  // NOT enter pass_count / fail_criteria / FunnelRank QualityGate. pass_count now
  // scores over the 4 non-advisory criteria (FCF / ROIC / EPS CAGR / PEG), max 4.
  // Per-stock `de_advisory` (bool) = D/E present and > 0.7 (FE renders ⚠ badge).
  // summary.pass_5 is therefore always 0 (kept for backward-compat key stability);
  // "fully passing" is now pass_4. 第五條「護城河」veto 由 sop_funnel 板機層把守。

  "presets": {
    "MLB": {"fcf": 10.0, "roic": 15.0, "eps2y": 15.0, "peg": 2.0, "de": 0.7}
  },

  "default_filter": {
    "moat_min": 9.5,
    "directions": ["↑", "→"]
  },

  "summary": {
    "pass_5": 12,
    "pass_4": 18,
    "pass_3": 9,
    "pass_lt3": 47,
    "no_data": 12
  },

  "stocks": [ /* see below */ ]
}
```

## Stock entry shape

Each entry in `stocks[]`:

```json
{
  "ticker": "NVDA",
  "name": "NVIDIA",
  "sector": "半導體",

  "moat_score": 10,
  "moat_grade": "S",
  "moat_trend": "↑",
  "signal": "A",
  "trap": "🟢",
  "val": "🟡",

  "fcf":    44.8,
  "roic":   62.1,
  "eps2y":  54.3,
  "peg":     0.38,
  "de":      0.07,
  "de_advisory": false,   // 2026-07-03: D/E > 0.7 → true（FE ⚠ badge）；advisory only, 不進 pass_count

  "pass_count": 5,
  "fail_criteria": [],

  "upside_mid_pct": 8.3,
  "upside_5y_pct": null,
  "ev5y_pct": 9.50,

  "dd_path":  "/dd/DD_NVDA_20260418.html",
  "dd_date":  "2026-04-18",
  "dca_path": "/dca/DCA_NVDA_20260418.html",
  "dca_date": "2026-04-18",

  "quality_source": "yfinance",

  "ma": {
    "price": 152.3,
    "w52": 145.2,
    "w104": 132.1,
    "w250": 110.5,
    "slope_w250_pct": 12.3,
    "drift_4w_pct": 3.2,
    "above_w52": true,
    "above_w250": true
  },

  "timing": {
    "dist_52w_high_pct": -3.2,
    "ma50_pct": 4.1,
    "vs_200ma_pct": 18.5,
    "rs_score": 87.4
  }
}
```

## Field reference

### Identity (always present)
| Field | Type | Notes |
|---|---|---|
| `ticker` | string | Canonical form: `NVDA`, `2330.TW`, `RMS`, `6857.T` — matches DD filename stem |
| `name`   | string | Company name from dd-meta `company`/`name` (fallback to ticker) |
| `sector` | string | `industry` from dd-meta (fallback `""`) |

### DD-meta sourced (always present from dd-meta JSON)
| Field | Type | Default if missing |
|---|---|---|
| `moat_score` | number 1-10 | required (skip ticker if absent) |
| `moat_grade` | "S"/"A"/"B"/"C"/"X" | required |
| `moat_trend` | "↑"/"→"/"↓" | Overridden by DCA Phase A1 arrow at build time (94/98 coverage); fallback **"→"** when no DCA arrow (conservative — assume stable, not strengthening) |
| `moat_execution` | number 1-10 \| null | v12.3+ optional moat sub-score (execution moat); null for legacy DDs |
| `moat_pricing_power` | number 1-10 \| null | v12.3+ optional moat sub-score (pricing power moat); null for legacy DDs |
| `signal` | "A+"/"A"/"B"/"C"/"X" | required |
| `trap` | emoji | required |
| `val` | emoji | required |
| `ai_risk` | "🟢"/"🟡"/"🔴" \| null | disrupt-risk light from dd-meta; used as quality-entry veto (🔴 excluded) |
| `upside_mid_pct` | number | null if missing (retained for legacy/fallback; FE no longer displays) |
| `upside_5y_pct` | number | null if missing (rarely populated in dd-meta) |
| `fpe_fy2` | number | FY+2 Forward P/E from dd-meta. Displayed in the screener's 2Y P/E column (right of PEG); mirrors `/research/` `data-pe2y`. |
| `pct_5y` | number 0-100 \| null | 5Y FwdPE historical percentile (lower = cheaper); main Entry-pillar anchor for quality-entry screener |
| `growth_durability` | number 1-10 \| null | DD §1 analyst score for growth durability |
| `quality_score` | number 1-10 \| null | DD §1 holistic quality score (distinct from `quality_source` which is a string tag) |
| `ev5y_pct` | number | DCA §4 機率加權 5Y EV → annualized IRR (%); **primary 5Y IRR column source**, mirrors `/research/` table. null if no DCA or §4 unparseable. |
| `dd_path` | "/dd/DD_*.html" | absolute path from site root |
| `dd_date` | "YYYY-MM-DD" | from dd-meta `date` |
| `dca_path` | "/dca/DCA_*.html" or null | latest DCA in `docs/dca/` matching ticker |
| `dca_date` | "YYYY-MM-DD" or null | from DCA filename |

### Quality (Step 3 — Opus task)
All 5 quality fields are **percent** units except `peg` and `de`:
- `fcf` = FCF / Revenue, **percent** (e.g. 44.8 means 44.8%)
- `roic` = NOPAT / Invested Capital, **percent** (e.g. 62.1 means 62.1%)
- `eps2y` = forward 2Y EPS CAGR, **percent**
- `peg` = forward PEG, **decimal** (e.g. 0.38)
- `de` = total debt / equity, **decimal** (e.g. 0.07)

Any field can be `null` (insufficient yfinance data, new IPO, etc).

| Field | Type | Notes |
|---|---|---|
| `quality_source` | string | One of: `"qgm-us"`, `"qgm-tw"`, `"yfinance"`, `"yfinance-eu"` |
| `pass_count` | int 0-5 | Number of criteria passed |
| `fail_criteria` | array<string> | Subset of `["fcf","roic","eps2y","peg","de"]` (criteria failed). `null` field counts as fail. |

### MA snapshot (Step 4 — Sonnet B task)
All MA values in price units. `null` for any field when history < required.
- `w52` requires ≥ 52 weeks of weekly closes
- `w104` requires ≥ 104 weeks
- `w250` requires ≥ 250 weeks
- `slope_w250_pct` = (W250_now / W250_4w_ago - 1) × 100, **percent**
- `drift_4w_pct` = (price_now / price_4w_ago - 1) × 100, **percent**
- `above_w52` / `above_w250` = bool; null if w52/w250 null

### Timing snapshot (v1.1 — joined from `docs/screener/latest.json`)
US-only daily-cron snapshot. `null` (the whole `timing` block) when ticker is
non-US (TW/JP/EU) or screener `latest.json` missing. Same source consumed by
`flow/ath-hunter.html` — zero data drift across pages.

| Field | Type | Notes |
|---|---|---|
| `dist_52w_high_pct` | number | % distance from 52-week high (adjusted close). 0 = at high; negative = below. 起漲點 sweet spot: `[-7, 0]`. |
| `ma50_pct` | number | % distance from 50-day MA. 起漲點 sweet spot: `[0, +5]` (just reclaimed, not extended). |
| `vs_200ma_pct` | number | % distance from 200-day MA. Long-term trend gauge. |
| `rs_score` | number 0-100 | Percentile RS rating vs SPY (multi-timeframe weighted). 起漲點 threshold: ≥ 80. |

### FunnelRank (v1.3 — 漏斗綜合排序分)

Server-computed 0–1 sort key composed from three fundamental layers (timing is
**not** included — it stays a filter). Constants live in `build_dd_screener.py`
header (`FUNNEL_*`) and are mirrored into the top-level `funnel_config` block.

`funnel_rank = 0.40·quality_gate + 0.30·moat_score_adj + 0.30·revision_score`

| Field | Type | Notes |
|---|---|---|
| `funnel_rank` | number 0-1 | Primary default sort key (DESC). 0 for all-downgrade veto rows. |
| `quality_gate` | number 0-1 | 5/5→1.00; 4/5 forgivable (only D/E or PEG fail)→0.85; 4/5 core fail→0.50; 3/5→0.30; ≤2/5→0.10. Partial (null criterion) → ratio-scaled through same anchors. |
| `moat_score_adj` | number 0-1 | `moat_score/10` × trend mult (↑1.10 / →1.00 / ↓0.80), cap 1.0. 0.50 if no moat data. |
| `revision_score` | number 0-1 | FY1/FY2/FY3 signal (±0.5% → ±1, else 0) weighted 0.2/0.3/0.5; `(raw+1)/2`; +0.05 if FY3 upgrade magnitude > FY1's. 0.50 if no baseline. |
| `veto_all_downgrade` | bool | True → `funnel_rank` forced to 0 (FY1/FY2/FY3 all ≤ -0.5%). FE: ⛔ + dim row + sinks. |
| `funnel_cap_moat_down` | bool | True → `funnel_rank` capped at 0.50 (moat ↓ & pass_count ≤ 4). |
| `quality_gate_partial` | bool | True → at least one of the 5 criteria was null (gate computed on present ratio). |
| `moat_no_data` | bool | True → moat_score absent, `moat_score_adj` defaulted to 0.50. |
| `revision_no_baseline` | bool | True → no prior snapshot for any FY, `revision_score` defaulted to 0.50. |
| `peg_fallback` | bool | True → frozen `peg` came from yfinance manual forwardPE/CAGR fallback (denominator not comparable to mainstream forward consensus). Does **not** alter `quality_gate`. |

### Output sort order

`stocks[]` sorted by (v1.3):
1. `funnel_rank` DESC (漏斗綜合分; veto rows = 0 sink to bottom)
2. `pass_count` DESC (tie-break)
3. `moat_score` DESC
4. `ev5y_pct` DESC (nulls last)
5. `ticker` ASC

## Front-end render rules

- Tab grouping: `tab-5` = `pass_count===5`, `tab-4` = `===4`, `tab-3` = `===3`, `tab-all` = all sorted
- Cell coloring: green if criterion pass, red if fail, gray if `null`
- 5Y IRR column shows `ev5y_pct` with color band mirroring `/research/`:
  - ≥12 → strong green (#166534)
  - 8-12 → mid green (#15803D, beats SPX)
  - 0-8 → amber (#92400E)
  - <0 → red (#991B1B)
  - null → "—" (no DCA or §4 unparseable)
- DD link: `dd_path`; DCA link: `dca_path` (hide if null)
- Source badge mapping: `qgm-us` → blue, `qgm-tw` → green, `yfinance` → gray, `yfinance-eu` → orange
- MA badge:
  - Both `above_w52` and `above_w250` null → "— n/a" (no data at all)
  - `above_w250` null only (newer IPO, < 5y history; e.g. ARM / NU / VIK / SNDK) → "🟢 W52↑ · W250 N/A" or "🔴 W52↓ · W250 N/A" depending on W52
  - `above_w52 && above_w250 && slope_w250_pct > 0` → "🟢 healthy"
  - `above_w52 && above_w250` (slope flat/down) → "🟡 mixed"
  - below either MA → "🔴 weak"
- Filter chips:
  - Moat: `[S]` (≥9.5) / `[A]` (≥8) / `[B]` (≥6) / `[All]`
  - Direction: `[↑+→]` (default) / `[↑ only]` / `[Any]`
  - Preset: `[MLB]` (default) / `[Custom]`
  - 時機 (v1.1): `[Any]` (default, no timing filter) / `[起漲點]` (requires `dist_52w_high_pct ∈ [-7, 0]` ∩ `ma50_pct ∈ [0, +5]` ∩ `rs_score ≥ 80`; rows with null `timing` block are filtered out)
  - 時機 (v1.3): `[回調帶]` (pullback — requires `dist_52w_high_pct ∈ [-15, -7]` ∩ MA badge 🟢 [`above_w52 && above_w250 && slope_w250_pct>0`, or `<5y` listing with `above_w52`] ∩ `ma50_pct ∈ [-3, +5]`; rows with null `timing` filtered out). 日線版 `PULLBACK_WATCH` (週線版見 entry-state.html)
  - Custom mode reveals 5 sliders + S-tier toggle, recomputes `pass_count` client-side using either `presets.MLB` thresholds or user-mutated Custom values

## dd-meta `kill_metrics[]` (optional, P2 · 2026-07-19)

Structured falsification table carried in the DD's `<script id="dd-meta">` JSON.
**Not** propagated into `latest.json` (the screener does not render it); documented
here because this file is the DD-meta field reference and downstream consumers key
off it. Enforced by `scripts/validate_dd_meta.py`; mirrors the ID schema's
`kill_metrics[]` (`scripts/validate_id_meta.py`) byte-for-byte so a single
backfill/parse path serves both corpora.

**Always optional** for DDs — unlike the ID (v2.5+ requires ≥ 3 items), a DD may
omit the field entirely and no minimum count applies. The frozen v13/v14 corpus is
unaffected. New DDs (especially 裁決＝進場) SHOULD carry 3–5 rows so the market
detector's kill-watch (`docs/detective/data/kill_registry.json` →
`scripts/build_kill_watch.py`) can monitor the thesis.

Each item:

| Key | Type | Required | Notes |
|---|---|---|---|
| `metric` | string ≤120 | ✅ | Short label of the watched quantity (e.g. `"AI 加速器訓練份額"`) |
| `bear_threshold` | string ≤120 | ✅ | Falsification level + direction + current value (e.g. `"跌破 65%（當前 ~73%）→ 減半"`) |
| `window` | string ≤60 | ✅ | Timeframe the DD attaches (e.g. `"下次財報 ~2026-08-26"`); `""` if none |
| `source` | string ≤120 | optional | Provenance / series hint |
| `last_status` | enum | optional | one of `ok` / `warning` / `triggered` / `unknown` |

```json
"kill_metrics": [
  {"metric": "AI 加速器訓練份額", "bear_threshold": "跌破 65%（當前 ~73%）→ 減半", "window": "", "last_status": "ok"},
  {"metric": "CUDA 護城河", "bear_threshold": "被 custom ASIC 結構繞過（training 崩）→ 清倉", "window": ""}
]
```

The 32 existing 進場 DDs were backfilled into the kill registry as `llm_only`
entries (`source: "dd_backfill_2026-07-19"`) without touching the published HTML —
future DDs emit the field natively.

## File location

```
docs/dd-screener/
├── index.html       # consumes latest.json
└── latest.json      # produced by build_dd_screener.py
```
