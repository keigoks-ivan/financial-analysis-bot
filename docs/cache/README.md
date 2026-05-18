# Ticker Data Cache

This directory holds 4 cache files that consolidate cross-market ticker data, refreshed on two cadences:

| File | Cadence | Cron | Source |
|---|---|---|---|
| `fundamentals-us.json` | **Monthly** (1st of month) | `0 22 1 * *` UTC = 1st 06:00 TPE next day | QGM-US passthrough + yfinance fetch |
| `fundamentals-tw.json` | **Monthly** (1st of month) | `0 7 1 * *` UTC = 1st 15:00 TPE | QGM-TW passthrough + yfinance fetch |
| `prices-us.json` | **Daily** (Tue–Sat) | `30 22 * * 1-5` UTC = Tue–Sat 06:30 TPE | Mirror `docs/screener/latest.json` + yfinance fallback |
| `prices-tw.json` | **Daily** (Mon–Fri) | `30 8 * * 1-5` UTC = Mon–Fri 16:30 TPE | Mirror `docs/screener/tw_latest.json` + yfinance fallback |

Producer scripts:
- `scripts/build_fundamentals_cache.py --region {us,tw}`
- `scripts/build_prices_cache.py --region {us,tw}`

Schema validator:
- `scripts/validate_cache_schema.py` (also wired into pre-commit hook)

Viewer page:
- `https://research.investmquest.com/cache/`

---

## Universe

Each region's universe is the **union** of DD tickers + that region's market index list:

- **US (`fundamentals-us.json` / `prices-us.json`)**: DD non-TW ∪ S&P 500 + NQ 100 extras = ~545 tickers
- **TW (`fundamentals-tw.json` / `prices-tw.json`)**: DD TW ∪ TWSE 0050 + 0051 + 00714 = ~197 tickers

**Bucket rule**: ticker ending `.TW` / `.TWO` OR bare 4-digit numeric (e.g. `2330`) → TW. Everything else (US, EU `.PA/.MC/.AS/.DE`, JP `.T`, HK `.HK`) → US.

---

## Schema v1.0

### Fundamentals (monthly)

Top-level:
```json
{
  "schema_version": "1.0",
  "region": "us" | "tw",
  "as_of": "YYYY-MM-DD",
  "run_timestamp": "ISO 8601",
  "next_refresh_due": "YYYY-MM-DD",
  "stale_after_days": 35,
  "universe_size": 545,
  "source_breakdown": {"qgm-us": 59, "yfinance": 470, "failed": 16, ...},
  "health": {
    "status": "ok | partial-warn | partial-error",
    "success_count": 530,
    "failed_count": 15,
    "failure_ratio": 0.027,
    "runtime_seconds": 1234
  },
  "failed_tickers": ["BRK.A", ...],
  "tickers": { TICKER: {...} }
}
```

Per ticker (`tickers[TICKER]`):
```json
{
  "currency": "USD" | "TWD" | "EUR" | "JPY" | "GBP" | "HKD" | "CNY",
  "quality": {
    "fcf":   26.92,    // FCF margin %, 0-100
    "roic":  62.14,    // ROIC %, 0-100
    "eps2y": 52.73,    // 2Y forward EPS CAGR %, 0-100
    "peg":   0.37,     // PEG ratio, decimal
    "de":    0.073     // Debt/Equity, decimal
  },
  "eps_estimate": {
    "fy0": 8.38,       // current FY EPS in native currency
    "fy1": 11.43       // next FY EPS in native currency
  },
  "info": {
    "forwardEps":  11.43,  // native currency
    "trailingEps": 5.21,   // native currency
    "bookValue":   4.50    // native currency
  },
  "growth": {
    "rev_growth_yoy": 67.8,  // %, 0-100+
    "rev_cagr_3y":    null   // %, optional
  },
  "margins": {
    "gross":     72.3,     // %, 0-100
    "operating": 53.5,     // %, 0-100
    "net":       50.1      // %, 0-100
  },
  "trends": {
    "gm_5y_trend":         5,      // QGM direction score (int); null for non-QGM tickers
    "roic_5y_stability":   0.92,   // 0-1, fraction of 5Y above 15%
    "fcf_5y_normalized":   0.265,  // 0-1, 5Y avg FCF margin
    "quality_score":       92      // 0-100 QGM aggregate; null for non-QGM
  },
  "quarterly": {
    "eps_yoy_neg_streak":         0,  // consecutive quarters EPS YoY negative
    "fcf_margin_decline_streak":  0   // consecutive quarters FCF margin declining
  },
  "quality_source": "qgm-us" | "qgm-tw" | "yfinance" | "yfinance-eu" | "yfinance-jp" | "yfinance-hk",
  "fetched_at": "ISO 8601"
}
```

### Prices (daily)

Top-level adds `indices` block:
```json
{
  ...top-level same as fundamentals...
  "indices": {
    "SPY": {...}, "QQQ": {...},     // US file
    "TWII": {...}                   // TW file
  },
  "tickers": { TICKER: {...} }
}
```

Per ticker (`tickers[TICKER]`):
```json
{
  "currency": "USD" | "TWD" | ...,
  "price":             190.12,
  "close_change_pct":  1.23,
  "high_52w":          192.40,    // (only in yfinance-fallback rows; mirrored rows use screener fields)
  "low_52w":           98.20,
  "dist_52w_high_pct": -1.2,      // % below 52w high (signed)
  "ma21_pct":          5.2,       // % above MA21 (signed)
  "ma50_pct":          12.3,
  "vs_200ma_pct":      31.5,
  "rs_score":          92.3,      // 0-100 percentile vs reference universe
  "rs_rating":         89,        // alternate 0-100 score (screener field)
  "rs_1w":             88,
  "rs_4w":             92,
  "rs_13w":            95,
  "rsi14":             58.4,      // 0-100
  "atr_pct":           1.85,      // ATR as % of price
  "trend_ok":          true,      // 200ma rising over last ~21d
  "source":            "screener-us-mirror" | "screener-tw-mirror" | "yfinance-fallback"
}
```

---

## Unit / currency conventions

Every numeric field follows ONE of these patterns:

| Pattern | Unit | Examples |
|---|---|---|
| **Percentage** (0-100) | scaled by 100 (NOT 0.0-1.0) | `quality.fcf: 26.92`, `margins.gross: 72.3`, `rs_score: 92.3`, `ma50_pct: 12.3` |
| **Ratio** (0-1 or 0-x) | decimal | `quality.de: 0.073`, `quality.peg: 0.37`, `trends.roic_5y_stability: 0.92` |
| **Price** | **native currency** | `price: 190.12` (USD), `2330.TW.price: 1245` (TWD) |
| **EPS** | native currency | `eps_estimate.fy0: 8.38` (USD), `2330.TW.eps_estimate.fy0: 35.2` (TWD) |
| **Signed %** | `+`/`-` percent | `dist_52w_high_pct: -1.2`, `close_change_pct: 1.23`, `vs_200ma_pct: 31.5` |
| **Counts** | int | `quarterly.eps_yoy_neg_streak: 2`, `health.success_count: 530` |

Cross-currency calculations (e.g. comparing `marketCap` across regions) require converting via FX rate — consumer's responsibility.

---

## NOT stored — derived at consumer side

These fields can drift mid-month if cached, so consumer code computes them on demand from `daily.price × monthly.eps`:

- `peg = price / fy1_eps / (eps2y/100)` — though QGM's snapshot peg is included in `quality.peg`
- `fy1_per = price / fy1_eps`, `fy2_per = price / fy2_eps`
- `priceToSales = price / sales_per_share`
- `marketCapB = price × shares_outstanding`
- `live_fpe_est = price / fy_eps` (replaces v1.6 build_dd_screener heuristic when consumer wires up)

---

## Health & failure handling

Each file's `health` block:
- `status: "ok"` — failure_ratio < 5%
- `status: "partial-warn"` — 5–20%, viewer shows yellow badge
- `status: "partial-error"` — 20–80%, viewer shows red badge
- **`status: "abort"`** — if a build hits ≥ 80% failure, the script EXITS with code 1 BEFORE overwriting cache. Prior cache stays intact. Run again later or manually via `workflow_dispatch`.

`failed_tickers[]` lists tickers the build couldn't resolve. Common reasons:
- yfinance has no data for the ticker (delisted, class-A only, etc)
- yfinance rate-limited (transient)
- Symbol mismatch (e.g. BRK.A vs BRK-A)

---

## Manual operations

```bash
# Build US fundamentals
python3 scripts/build_fundamentals_cache.py --region us

# Build TW fundamentals
python3 scripts/build_fundamentals_cache.py --region tw

# Build prices
python3 scripts/build_prices_cache.py --region us
python3 scripts/build_prices_cache.py --region tw

# Smoke test (first 10 tickers, no write)
python3 scripts/build_fundamentals_cache.py --region us --top 10 --dry-run

# Force rebuild ignoring checkpoint (e.g. if previous run got stuck)
python3 scripts/build_fundamentals_cache.py --region us --no-resume

# Validate all cache files
python3 scripts/validate_cache_schema.py
```

Checkpoint files live in `.cache/` (gitignored).

---

## Consumer wiring status

**As of 2026-05-18: cache layer is producer-only. No consumer reads these files yet.**

Future plans (separate from cache build plan):
- `build_dd_screener.py` may read `fundamentals-us.json` / `fundamentals-tw.json` instead of QGM JSON directly
- `/flow/` page may read `prices-us.json` for indices instead of `market_state.json`
- `quality-entry` page may read both

When wired, consumer fallback chain should be: cache → existing source (QGM JSON / screener / yfinance live) → null.

---

## Cross-references

- Plan: `~/.claude/plans/https-research-investmquest-com-yfinance-cuddly-wreath.md`
- Producer scripts: `scripts/build_fundamentals_cache.py`, `scripts/build_prices_cache.py`
- Validator: `scripts/validate_cache_schema.py`
- Workflows: `.github/workflows/{monthly,daily}-{fundamentals,prices-cache}-{us,tw}.yml`
- Viewer: `docs/cache/index.html`
