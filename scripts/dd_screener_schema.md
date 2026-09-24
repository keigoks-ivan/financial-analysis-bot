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

v1.4 (2026-09-22, additive): **FunnelRank v2 — 四層側寫逐層排序法**, replacing
v1.3's weighted-sum `funnel_rank` as the default sort key. v1 fields (`funnel_
rank`, `quality_gate`, `moat_score_adj`, `revision_score`, and the veto/cap
flags above) are unchanged and kept computed for one version ("v1 legacy,
removed next version"). See §"FunnelRank v2" below and design doc
`notes/site-internal/root/_funnel_v2_design_20260922.md`. New per-stock fields:
`funnel_v2_rank`, `funnel_v2_tiers`, `funnel_v2_profile`, `funnel_v2_median`,
`funnel_v2_top_tier_count`, `funnel_v2_veto`, `funnel_v2_note`. New top-level
`funnel_v2_config` (layer field lists + min-layers threshold) and
`funnel_v2_summary` (ranked/veto/insufficient counts). **`stocks[]` default
sort is now `funnel_v2_rank` ASC** (rank 1 = best; None sinks, tie-broken by
the v1.3 chain — see "Output sort order" below).

**護城河不進排序（2026-09-22 最終定案）**：launch day 前後試了三版護城河層
設計——3-chain percentile + 80%-coverage gate、single-source absolute-tier +
`FUNNEL_V2_MOAT_JUDGMENT_ENABLED` transition switch、最後是純顯示連結
（`moat_questions_url`/`moat_review_due`，連到已放棄的「護城河三題」版
面）——三版皆已從程式碼與 `latest.json` 整段刪除。護城河是判斷不是可排序
的分數，`FUNNEL_V2_LAYER_ORDER` 只有四個成員（`quality`/`engine`/`gap`/
`price`），`stocks[]` 條目不再有任何 `moat_*` 欄位屬於 FunnelRank v2（v1
legacy 的 `moat_score`/`moat_grade`/`moat_trend`/`moat_score_adj` 不受影
響，見上方 FunnelRank v1.3 一節）。個股儀表板（`/stock-dash/?t={T}`）取代
原本規劃的站內顯示連結，dd-screener 每列直接連出，不經 `latest.json` 傳
遞任何護城河判斷資料。

v1.5 (2026-09-23, corrective — same-day follow-up, not a new layer/field
shape): fixes three FunnelRank v2 implementation bugs found against the
design doc + adds one new field. (1) **Sort method** was implemented as a
fixed-order tuple comparison (quality→engine→gap→price); the design doc's
own prose always said "compare the weakest layer first" — now actually
leximin (see "Sort method" below). (2) **Price layer** drops `pct_5y` (stale,
copied from the DD report at write time; also missing for all 87 non-DD
stocks) — three fields now, not four. (3) **Quality layer**'s `fcf_ni_ratio`
input is capped at `FUNNEL_V2_FCF_NI_CAP=0.8` before entering the percentile
average (previously uncapped, so GAAP-NI-is-tiny names like CRWD/PANW/MDB
topped this field on an accounting artifact, not real quality). (4) New field
`target_upside_source` (`"koyfin"` \| `"yfinance"` \| `null`) — `target_upside_
pct` now falls back to a yfinance `Ticker.info` lookup (`targetMeanPrice` /
`currentPrice`) when Koyfin's own `target_avg`/`last_price_local` pair is
split across an ADR/local-listing pair (e.g. TSM/2330.TW), only when Koyfin's
own calc came back `null`. See `knowledge/rule_ledger.md` FunnelRank v2 row
(2026-09-23 append) and design doc §2.2/§2.5/§3.

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
| `dd_status` | "dd" \| "none" | 選股系統 v2 (2026-09, `--include-non-dd`): "dd" = real DD report (all fields above populated); "none" = QGM-sourced non-DD row (`dd_screener_dd_loader.load_non_dd_universe`) — every field above is null. `universe_source` ("qgm-us"/"qgm-tw"/null) tags which QGM file a "none" row came from, and `qgm_seed` (object \| null) carries that row's raw QGM numbers (price/market_cap_b/fy1_eps/fy2_eps/fy1_per/quality_score/pool_tier/hard_filter_details/roic_5y_stability_pct_above/trend_template_conditions) as fallback input for the quality/EPS stages. |

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

**v1.4 note**: `funnel_rank` and the four fields above are kept exactly as
computed pre-v1.4 ("v1 legacy, removed next version") — they are no longer the
default sort key (see FunnelRank v2 below) but remain available for the FE's
legacy-methodology collapsed panel and for `scripts/build_stock_dash.py`'s T4
trigger (which reads `funnel_rank` directly and is out of scope for this
change).

### FunnelRank v2 (v1.4 — 四層側寫逐層排序法)

Server-computed **rank** (not a 0–1 score) built from four independent
layers instead of one weighted sum. Constants/field lists live in
`build_dd_screener.py`'s `FUNNEL_V2_*` header and `compute_funnel_v2()`, and
are mirrored into the top-level `funnel_v2_config` block. Full rationale
(motivation, per-layer field list, sort method, veto rules, boundary vs. the
seat engine / sop-funnel) is in the design doc
`notes/site-internal/root/_funnel_v2_design_20260922.md` — this section is
the field reference only.

The four layers (`quality`, `engine`, `gap`, `price`) are 0–100 rank-based
percentiles of the stock within the **full build population** (all of
`stocks[]`, not just `dd_status=="dd"` rows): `quality`
(`roic_5y_avg_pct`, `fcf`, `fcf_ni_ratio` capped at `FUNNEL_V2_FCF_NI_CAP=0.8`
before entering the average — see below, `fund.ni_margin_ltm_pct`), `engine`
(`implied_growth_pct`, `incremental_roic_pct` [excluded when
`incremental_roic_clamped` or `incremental_roic_note=="資本縮減"`],
`eps_fy1_fy3_cagr_pct`), `gap` (`eps_rev_3m_pct`, `eps_rev_since_earnings_pct`,
`implied_growth_pct − fund.est_eps_cagr_3y_pct`), `price` (reverse layer —
`pe_vs_5y_x`, `live_peg` inverted so cheaper ranks higher; `target_upside_pct`
not inverted — 3 fields; `pct_5y` was dropped 2026-09-23, see v1.5 note
above). A layer is `null` for a stock when none of its fields have data for
that stock (it simply doesn't participate in that layer's ranking — never
defaults to a neutral value the way v1's 0.50 fallbacks did).

**`fcf_ni_ratio` cap (2026-09-23, "penalize low, don't reward high")** — the
raw ratio is uncapped everywhere else (output field, both existing veto
checks); only the value fed into this one percentile average is
`min(fcf_ni_ratio, FUNNEL_V2_FCF_NI_CAP)`. Without the cap, names whose GAAP
net income is tiny relative to FCF (CRWD 35.9, PANW 13.4, MDB 11.2) topped
this field purely on a denominator artifact, not superior quality. At/above
0.8 all tie (cash conversion is fine, further multiples don't mean more);
below 0.8 still ranks on the uncapped value.

**`target_upside_pct` / `target_upside_source` (2026-09-23)** — Koyfin's
export is split for ~20 names (e.g. TSM/ADR has `fund.last_price_local` but
no `fund.target_avg`; 2330.TW is the reverse), so `compute_fundamental_
gates()`'s own calc is `null` for them. `enrich_ticker()` then falls back to
a yfinance `Ticker.info` lookup (`targetMeanPrice` over `currentPrice`,
falling back to `regularMarketPrice`) — same API call, same quote source,
same currency on both sides — only when Koyfin's value is `null`.
`target_upside_source` records which path won: `"koyfin"`, `"yfinance"`, or
`null` when neither produced a value. `compute_fundamental_gates()` itself
stays network-free (only ever sets `"koyfin"` or `null`); the fallback lives
in `enrich_ticker()`.

v1.6 (2026-09-25, additive): new per-stock field `eps_year_ago` — the prior
fiscal year's actual EPS (yfinance `Ticker.earnings_estimate` row `0y`'s
`yearAgoEps`, same-basis companion to `eps_fy_curr`/`eps_fy_next`; already
computed internally by `_fetch_live_fy_eps()`/used for `eps2y_live_method=
"yearago"`, just not previously surfaced). Added so `build_stock_dash.py` can
read it from `latest.json` instead of calling `Ticker.earnings_estimate`
itself per-ticker (that call gets 429/401'd from the GitHub Actions runner
IP). `null` when yfinance had no `0y` row or no `yearAgoEps`.

**護城河不進排序（2026-09-22 最終定案）**：launch day 前後試了三版護城河層
設計——3-chain percentile + 80%-coverage gate、single-source absolute-tier +
`FUNNEL_V2_MOAT_JUDGMENT_ENABLED` transition switch、最後是純顯示連結
（`moat_questions_url`/`moat_review_due`）——三版皆已從程式碼整段刪除。護
城河是判斷不是可排序的分數，`FUNNEL_V2_LAYER_ORDER` 只有四個成員，
`latest.json` 的 `stocks[]` 條目不再有任何 `moat_*` 欄位屬於 FunnelRank
v2。個股儀表板（`/stock-dash/?t={T}`）取代原本規劃的站內顯示連結，由
dd-screener 每列直接連出，不經 `latest.json` 傳遞任何護城河判斷資料。

| Field | Type | Notes |
|---|---|---|
| `funnel_v2_rank` | int 1..N \| null | Primary default sort key (ASC, 1 = best). `null` for hard-veto or insufficient-data rows (sink to bottom). |
| `funnel_v2_tiers` | array<int>[4] | Per-layer five-bucket tier, order `[quality, engine, gap, price]`. `[80,100]→4` … `[0,20)→0`. `null`/missing layer → `-1`. |
| `funnel_v2_profile` | array<number\|null>[4] | Per-layer 0–100 percentile, same order as `funnel_v2_tiers`. |
| `funnel_v2_median` | number \| null | Median of the non-null quality/engine/gap/price percentiles. Tie-break after the 4 tiers, before ticker. |
| `funnel_v2_top_tier_count` | int 0-4 | Count of layers at tier 4 (top quintile). Display-only. |
| `funnel_v2_veto` | array<string> | Hard-veto reasons hit (`quality_veto_level=拒絕`, `decline_signal_light=⛔`, `veto_all_downgrade` — same three judgments v1 already used to zero/force-sink a row). Non-empty → `funnel_v2_rank=null`. |
| `funnel_v2_note` | string \| null | `"資料不足（N/4 層）"` when fewer than 3 of 4 layers have a non-`-1` tier (and no veto fired) → `funnel_v2_rank=null`. `null` otherwise. |

**Sort method (corrected 2026-09-23)** — leximin, not a weighted sum and not
a fixed-order tuple comparison: take the 4 tiers, substitute
`FUNNEL_V2_MISSING_TIER_AS=2` for any `-1` (missing layer treated as
neutral — neither rewarded nor punished), sort the 4 values ascending, then
compare rows weakest-vs-weakest first, then second-weakest, and so on;
descending on that comparison (bigger weakest layer wins). Ties across all 4
positions fall through to `funnel_v2_median` descending, then `ticker`
ascending. (The previous implementation compared
`(quality_tier, engine_tier, gap_tier, price_tier)` in that fixed order —
this contradicted the design doc's own "compare the weakest layer first"
prose and let the quality layer alone decide most of the ranking; see
`knowledge/rule_ledger.md` FunnelRank v2 row, 2026-09-23 append.) v1's two
soft caps (`funnel_cap_moat_down`, and the "降一級" branch of
`funnel_cap_quality`) remain **retired** in v2 (see prior revision /
`knowledge/rule_ledger.md` for rationale and kill condition) — unaffected by
this section.

**Data-sufficiency gate**: a row needs ≥3 of the 4 layers with a non-`-1`
tier to receive a rank at all; otherwise `funnel_v2_rank=null` +
`funnel_v2_note` (see above).

### Output sort order

`stocks[]` sorted by (v1.4):
1. `funnel_v2_rank` ASC (rank 1 = best; `null` — veto'd or insufficient data — sinks to the bottom)
2. `funnel_rank` DESC (v1 legacy tie-break, for the `null`-rank rows above)
3. `pass_count` DESC
4. `moat_score` DESC
5. `ev5y_pct` DESC (nulls last)
6. `ticker` ASC

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
