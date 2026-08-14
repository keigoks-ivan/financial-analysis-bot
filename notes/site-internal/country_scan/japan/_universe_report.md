# JP Universe — Coverage & Quality Report

**As of**: 2026-08-14
**Output**: `notes/site-internal/country_scan/japan/_universe.json`
**Threshold**: market cap ≥ ¥100bn (≈ US$680M at ~147 JPY/USD)

## 1. How the ticker list was sourced

The spec called for starting from the current TOPIX 500 constituent list. That list is not freely downloadable in machine-readable form — JPX's live "TOPIX Component Stocks Weight" file sits behind their paid Index Data Service / client portal, and the JPX public index page returned HTTP 403 to automated fetch. The only fully-enumerated TOPIX 500 ticker list locatable via web search was a **2022-02 vintage** file (`topix500_202202.txt`, 500 codes, originally sourced from JPX data by a third-party site). No current (2026) TOPIX 500 list could be sourced.

**Skeleton** = that 2022-02 TOPIX 500 list (500 tickers).

**Supplemental additions** = 6 tickers manually identified as large-cap (post-2022 IPOs/spin-offs) and individually confirmed via yfinance to (a) be ≥¥100bn market cap and (b) be absent from the 2022 list:

| Ticker | Name | Reason not in 2022 list |
|---|---|---|
| 9023.T | Tokyo Metro | IPO Oct 2024 |
| 285A.T | Kioxia Holdings | IPO Dec 2024 |
| 5838.T | Rakuten Bank | IPO Apr 2023 |
| 6525.T | Kokusai Electric | IPO Oct 2023 |
| 6526.T | Socionext | IPO Oct 2022 (after the Feb-2022 skeleton snapshot) |
| 5016.T | JX Advanced Metals | IPO Mar 2025 (spin-off of ENEOS) |

**Total candidate list**: 506 tickers (500 + 6).

**Honest gap**: this is a skeleton, not an exhaustive scan. A 2022-vintage TOPIX 500 list is ~4 years stale — TOPIX itself has been undergoing periodic (semi-annual) reconstitution the whole time, and JPX is mid-way through a broader structural reform of TOPIX (Phase 2 starts Oct 2026, extending eligibility screening to Prime+Standard+Growth on free-float market cap / liquidity criteria). Likely **systematic misses** beyond the 6 manually patched: (a) any other 2023–2026 IPO/spin-off that grew past ¥100bn and isn't one of the 6 we happened to search for, (b) Standard-market names that organically appreciated past ¥100bn since 2022 without ever being TOPIX-500-eligible on liquidity grounds, (c) any name promoted into TOPIX 500 by a periodic review that a 2022 snapshot wouldn't reflect. A true zero-gap universe would require either a paid JPX data feed or a full market-cap screen of all ~3,100 Prime+Standard listed names — the latter was assessed and rejected for this run on time/rate-limit grounds (at ~1s/ticker sequential yfinance calls plus the mandated inter-batch sleeps, a full Prime+Standard sweep would run ~50–60 minutes and materially raise 429 risk for a payoff of mostly sub-threshold names). This is the deliberate "note honestly, don't chase completeness" tradeoff the task spec anticipated.

## 2. Fetch results

| Stage | Count |
|---|---|
| Candidate tickers | 506 |
| yfinance fetch — hard failure (no response at all, even after retry) | 0 |
| yfinance fetch — reproducible empty payload ("unresolved", see below) | 29 |
| Confirmed below ¥100bn threshold after fetch | 1 |
| **Final universe (confirmed ≥¥100bn)** | **476** |

No batch hit a sustained 429 wall — batching at 25 tickers/call with 3–5s inter-batch sleep and a single 30s-delayed retry-per-ticker was sufficient to clear the whole 506-ticker candidate list without any hard-missing tickers.

### 2a. The 29 "unresolved" tickers

These 29 codes returned a near-empty yfinance payload (no name, no sector, no market cap — essentially a stub) on **both** the original fetch pass and an independent re-fetch pass run afterward specifically to rule out a rate-limit artifact. Because the result was identical and reproducible on retry (not a transient 404-then-succeeds pattern), this is a real data gap, not a rate-limit issue.

Most likely explanation: the 2022-vintage skeleton contains codes for companies that have since **delisted, gone private, merged, or had their ticker code reassigned**. Spot check: `6502.T` was Toshiba Corporation, which was taken private via TOB by a Japan Industrial Partners-led consortium in December 2023 — consistent with this theory. The remaining 28 were not individually verified against corporate-action records; that would require per-name research beyond this data-engineering pass.

These 29 are **excluded from `stocks[]` and from every coverage/sector/P-B statistic below** — their true current market cap is neither confirmed ≥¥100bn nor confirmed below it, so including them either way would fabricate certainty the data doesn't support.

Excluded ticker list: `2412.T, 2427.T, 2651.T, 3141.T, 4185.T, 4530.T, 4581.T, 4739.T, 4921.T, 5486.T, 6028.T, 6201.T, 6406.T, 6502.T, 6755.T, 6967.T, 7205.T, 7518.T, 7732.T, 8279.T, 8355.T, 8369.T, 8382.T, 8385.T, 8905.T, 9086.T, 9613.T, 9719.T, 9783.T`

### 2b. Confirmed sub-threshold name

One 2022-skeleton constituent fetched cleanly but is now below ¥100bn: **JCR Pharmaceuticals (4552.T)**, market cap ¥64.3bn. Excluded from the final universe (it's a real data point, just under the bar — TOPIX 500 membership isn't a pure market-cap ranking, so a name can be in the 2022 list on liquidity/other grounds while sitting under ¥100bn).

## 3. Per-field coverage (of the 476 confirmed-in-universe names)

| Field | Coverage |
|---|---|
| name | 100.0% |
| sector | 100.0% |
| industry | 100.0% |
| market_cap | 100.0% |
| price | 100.0% |
| currency | 100.0% |
| price_to_book | 100.0% |
| payout_ratio | 100.0% |
| shares_outstanding | 100.0% |
| 52w high / low (+ derived % from high/low) | 100.0% |
| dividend_yield | 97.9% |
| forward_pe | 98.3% |
| trailing_pe | 96.4% |
| revenue_growth | 97.1% |
| total_debt | 99.8% |
| total_cash / net_cash / net_cash_to_mktcap | 99.6% |
| roe | 92.4% |
| roa | 92.2% |
| earnings_growth | 85.9% |

**Systematic gaps checked and NOT found to be significant**: the anticipated "banks/financials lack ROE via yfinance" pattern did not materialize strongly here — Financial Services is missing ROE for only 4/40 names (10%), roughly in line with the all-sector average (7.6% missing). ROA/ROE/earnings_growth gaps are mildly concentrated in Industrials (11/125 missing ROE) but not dramatically so; this looks like ordinary per-company data-vendor sparsity rather than a sector-systematic hole. `earnings_growth` is the weakest field overall (85.9%) across all sectors roughly evenly — treat it as the least reliable derived-growth field in this dataset.

## 4. P/B < 1 count at ≥¥100bn (governance lens — load-bearing stat)

- **105 of 476** confirmed-universe names (of which 476/476 have a known `price_to_book` value, so this is a clean denominator — no missing-data ambiguity) have **price_to_book < 1**.
- **105 / 476 = 22.1%** of the ≥¥100bn universe trades below book value.

By sector (count of P/B<1 names):

| Sector | P/B<1 count |
|---|---|
| Consumer Cyclical | 22 |
| Industrials | 20 |
| Basic Materials | 20 |
| Utilities | 11 |
| Healthcare | 9 |
| Financial Services | 7 |
| Consumer Defensive | 4 |
| Energy | 4 |
| Real Estate | 3 |
| Communication Services | 3 |
| Technology | 2 |

Note for the governance lens: Financial Services shows only 7/40 (17.5%) below book here — lower than the popular narrative of "Japanese banks structurally trade sub-1x P/B," though banks are a subset of Financial Services (which also includes insurers, brokers, credit-card cos) so this sector-level number will dilute a bank-specific read. The lens agent consuming this file should filter `sector == "Financial Services"` and cross-check `industry` for a bank-only cut if it needs that specific claim.

## 5. Sector distribution (476 names)

| Sector | Count | % |
|---|---|---|
| Industrials | 125 | 26.3% |
| Consumer Cyclical | 74 | 15.5% |
| Technology | 51 | 10.7% |
| Basic Materials | 46 | 9.7% |
| Consumer Defensive | 44 | 9.2% |
| Healthcare | 42 | 8.8% |
| Financial Services | 40 | 8.4% |
| Communication Services | 26 | 5.5% |
| Utilities | 13 | 2.7% |
| Real Estate | 11 | 2.3% |
| Energy | 4 | 0.8% |

Industrials being the largest single bucket (over a quarter of the universe) reflects both Japan's genuine industrial-conglomerate weight and yfinance's coarse GICS-like bucketing (auto parts, machinery, trading houses, and shipping all land in "Industrials").

## 6. Derived fields note

- `net_cash = total_cash − total_debt`; `net_cash_to_mktcap = net_cash / market_cap`. Both null wherever either input is null (4 names: coverage 99.6%).
- `pb_below_1` is a boolean computed only where `price_to_book` is non-null; all 476 names have a known P/B so this flag is fully populated.
- `pct_from_52w_high` / `pct_from_52w_low` computed as `(price − level) / level`; negative for the high-distance figure in the normal case (price below 52w high).

## 7. Bottom line for downstream lens agents

- Treat `notes/site-internal/country_scan/japan/_universe.json` `stocks[]` (476 rows) as the working universe. Every row has confirmed market cap ≥¥100bn and a known P/B.
- Do not silently backfill the 29 unresolved tickers or the 1 sub-threshold name — they're intentionally excluded, not lost.
- `roe`/`roa`/`earnings_growth` are the fields most likely to be null on any given row (85–92% coverage); build fallback logic rather than assuming presence.
- This is a **skeleton-plus-patch** universe, not a guaranteed-exhaustive ¥100bn+ Tokyo-listed screen — see §1 for the honest completeness caveat.
