# Hedge fund strategy index annual returns - sources log (2026-10-04)

All numbers below come from downloaded files / fetched pages. Nothing estimated.

## 1. edhec_annual.csv  (MAIN SERIES)
- Provider / family: EDHEC-Risk Alternative Indexes (13 "pure style" composite indices; returns derived by EDHEC from a pool of hedge-fund databases via principal-component weighting; non-investable).
- Raw monthly file: `edhec_A_z4ir3.csv` (monthly returns in PERCENT, dd/mm/yyyy, 1997-01 to 2018-11, 263 rows, no blanks).
  - Original mirror URL: https://raw.githubusercontent.com/z4ir3/finance-courses/master/data/edhec-hedgefundindices.csv
  - Identical copies (byte-identical after CRLF strip; same blob SHAs as GitHub code-search results):
    - `edhec_B_McCloud77.csv` <- https://raw.githubusercontent.com/McCloud77/Portfolio-Construction-and-Analysis/master/data/edhec-hedgefundindices.csv
    - `edhec_C_salimt.csv` <- https://raw.githubusercontent.com/salimt/Finance-and-Risk-Management-Algorithms/master/portfolio-construction-and-analysis-with-python/data/edhec-hedgefundindices.csv
  - This is the EDHEC/Coursera ("Introduction to Portfolio Construction and Analysis with Python") course dataset; the official edhec-risk.com history.csv URL is dead (redirects to a "delestage" page).
- Annual file: calendar-year returns, decimal (0.123 = 12.3%), compounded from monthly: prod(1+r_m)-1. Only full years: **1997-2017 (21 years)**. 2018 omitted (data ends 2018-11).
- Strategies (13): Convertible Arbitrage, CTA Global, Distressed Securities, Emerging Markets, Equity Market Neutral, Event Driven, Fixed Income Arbitrage, Global Macro, Long/Short Equity, Merger Arbitrage, Relative Value, Short Selling, Funds Of Funds.
  - NOTE: "Relative Value", "Event Driven" and "Funds Of Funds" are broad composites that overlap the sub-strategy columns (Conv Arb, FI Arb, Merger Arb, Distressed are subsets of RV/ED). "Funds of Funds" is a composite of FoFs, not a strategy. There is NO Multi-Strategy column. Decide before averaging whether to use all 13 or only non-overlapping ones.
- Net of fees: EDHEC indices are built from fund-reported returns, which are net of fund fees (net of underlying manager fees; FoF also net of FoF layer). Not formally confirmed from the file itself.
- Caveats: backfill / survivorship biases are mitigated but not eliminated by EDHEC's method; EDHEC revises history (this file is a vintage ending Nov-2018; values may differ from other vintages). Short Selling is an extreme-beta series (e.g. 2017 -31.9%, 1999 -22.6%, 2003 -23.9%) and will dominate any equal-weight average / "best strategy" ranking in some years.
- Spot-check: no independent second-source check was possible (no overlapping verified HFRI/CS annual numbers obtained). Integrity check only: three independent GitHub mirrors are identical; first rows match the code-search fragments (1997-01: Conv Arb 1.19, CTA 3.93, ... FoF 3.17).

## 2. hfri_press_release_fy_extracts.csv  (PARTIAL, long format, NOT a clean series)
- Provider / family: HFR (Hedge Fund Research) HFRI indices, from HFR "Performance Notes" year-end press releases (non-investable HFRI Total/composite indices and investable HFRI 500).
- URLs (saved to `hfr_notes/dec_YYYY.html`): https://www.hfr.com/media/performance-notes/hfri-indices-december-{2020,2021,2022,2023}-performance-notes/
- Each row has the verbatim sentence; every quote was programmatically verified to exist in the saved HTML. Returns in PERCENT (not decimal) in this file.
- Coverage actually obtained (FY, "Total" indices only):
  - 2020: FWC 11.6, EH(Total) 17.5, ED(Total) 9.3 (Macro Total, RV Total FY not stated)
  - 2021: FWC 10.3, ED(Total) 13.1 (EH Total, Macro Total, RV Total FY not stated; only HFRI 500 EH 11.9)
  - 2022: Macro(Total) 9.3 (EH/ED/RV Total FY not stated; only HFRI 500 Macro 14.8, HFRI 500 RV 0.97)
  - 2023: FWC 7.5, ED(Total) 10.7, EH(Total) 10.4, RV(Total) 7.2 (Macro Total FY not stated)
- Caveats: these are PRELIMINARY year-end figures from press text and HFR revises (e.g. the Dec-2021 release restates 2020 FWC as +11.8 vs +11.6 in the Dec-2020 release). Strategy sets are only the 4 HFRI main strategies, not sub-strategies; not comparable 1:1 to EDHEC columns. Too sparse to use as a second family for the hypothesis test.
- Pages that returned 404 to curl AND WebFetch (not obtained): HFR year-end releases for 2018, 2019, 2024, 2025 (hfr.com/media/market-commentary/... and performance-notes Dec-2024/2025 slugs).
- Leads NOT verified from a fetched page (came only from web-search result summaries; do NOT use as data without opening the source): HFRI EH(Total) 2024 ~+12.0, RV(Total) 2024 ~+8.7, Macro(Total) 2024 ~+5.65, ED 2024 ~+11.6 (asset weighted); HFRI EH 2025 ~+17.3 (EH Total ~+17.1); HFRI FWC 2024 ~+9.8; HFRI Asset-weighted 2018 Macro +1.9, EH -5.9, ED -0.6, RV +1.2.

## Not obtained
- Credit Suisse / CS-Tremont (hedgeindex.com: SSL verify failure; no published annual table found via search or GitHub code search).
- BarclayHedge (403 Cloudflare for curl; WebFetch redirect to ionanalytics.com which also 403s).
- Eurekahedge (now behind "With Intelligence" login).
- web.archive.org snapshots (proxy tunnel closed; not worked around). archive.org availability API works but snapshots do not.
- GitHub HFRI datasets: only variable lists (diegodalvarez/SkewDrawdown data/hfri.csv has ticker metadata only); the HFR monthly return files referenced by zoonek/2026-sharpe-ratio are not committed.
- Any strategy-index data for 2018 (full) through 2025 on a consistent family with EDHEC.
