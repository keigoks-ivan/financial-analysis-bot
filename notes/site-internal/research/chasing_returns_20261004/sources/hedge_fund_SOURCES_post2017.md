# Hedge fund strategy returns AFTER 2017 - sources log #2 (2026-10-04)
Builds on ../hf/SOURCES.md. All numbers come from downloaded files or fetched pages; nothing estimated.
Wide CSVs: rows = date/year, cols = strategy, DECIMAL returns (0.05 = 5%). Annual = compounded from monthly, full calendar years only.

## A. Credit Suisse Hedge Fund Index family - BEST NEW FIND (13 series incl. 11 strategies)
- Files: `creditsuisse_monthly.csv` (1994-01..2022-04, 340 months), `creditsuisse_annual.csv` (full years 1994-2021, 28 yrs). Raw: `raw/NAVROR_sam.csv`.
- URL: https://raw.githubusercontent.com/SuperSam1995/hedge-fund-ml/main/data/raw/NAVROR_full.csv
  (byte-identical copy: https://raw.githubusercontent.com/kaiwenShen/Do-You-Really-Need-to-Pay-2-20-Hedge-Fund-Strategy-Replication-via-Machine-Learning/main/data/NAVROR_full.csv). Header carries Bloomberg tickers (HEDG, HEDG_CVARB, ... HEDG_MULTI) - a Bloomberg NAV/ROR export, percent strings, converted to decimal. Dropped the 1993-12 all-zero base-date row.
- Strategies: Broad index, Convertible Arbitrage, Emerging Markets, Equity Market Neutral, Event Driven (+ sub: Distressed, Multi-Strategy, Risk Arbitrage), Fixed Income Arbitrage, Global Macro, Long/Short Equity, Managed Futures, Multi-Strategy (3 NaN months early on). NO Dedicated Short Bias column in this file.
- Fees/investable: CS index is (from general knowledge of CS methodology, NOT verified from a fetched page) asset-weighted, net of fees, non-investable.
- Caveats: data ends 2022-04 so 2022 is not a full year; CS EMN has a -40% year in 2008 (monthly min -40.45%) - looks real (CS EMN is a small pool) but is an outlier; file is second-hand (Bloomberg export committed by students), no official CS annual table was fetched to verify it.
- COVERAGE FOR TEST: 2008-2021 all 13 series complete (14 years).

## B. EDHEC extension through 2021 (same 13 series as the first pass)
- Files: `edhec_ext_monthly.csv` (1997-01..2021-06), `edhec_ext_annual.csv` (full years 1997-2020).
- URLs: https://raw.githubusercontent.com/twn39/pyperfanalytics/master/data/edhec_v2.csv (to 2021-05) and https://raw.githubusercontent.com/Rabbidon/Combinatorial-Financial-Bandits/master/data/hedge_funds_rets.csv (to 2021-06; used as the superset). Raw copies in `raw/`.
- Integrity: the two files match each other to 1e-16 on 293 common months, and match the first-pass z4ir3 file (1997-01..2018-11, 263 months) to 1e-17. So history is NOT revised vs the first-pass vintage; the files just add 2018-12..2021-06.
- Provenance of the 2018-12+ rows is UNKNOWN (not traceable to an EDHEC page; official edhec-risk.com URL is dead). Treat post-2018-11 EDHEC as unverified-but-plausible.
- SUSPECT: Short Selling has exact 0.0000 in 7 months of 2020-2021 (2020-04, 2020-05, 2020-11, 2020-12, 2021-01, 2021-04, 2021-05; some other months only 3-decimal precision), likely placeholder/missing fill. Do not rely on Short Selling after 2019 (its 2020 annual +15.8% is partly built from those zeros). CTA Global also has one 0.
- Net of fees (fund-reported), non-investable; same caveats as first pass.

## C. HFRX (HFR investable-style indices), daily files from HFR's own download, mirrored on GitHub
- Files: `hfrx_monthly.csv` (month-end level to month-end level), `hfrx_annual.csv`, `hfrx_daily_levels.csv`. Raw in `raw/` (RL_*.csv, AS_HFRXGL.csv).
- URLs: https://raw.githubusercontent.com/RiskLabAI/Notebooks.py/main/features/SWEFI/hedgefund_data/HFRX_historical_{HFRXM,HFRXMD,HFRXMA,HFRXSDV,HFRXEMN}.csv (identical copies under dependency/ccgrf/data/) and https://raw.githubusercontent.com/ArturSepp/OptimalPortfolios/main/papers/crypto_allocation_risk_2023/replication/data/HFRX_historical_HFRXGL.csv
- Series: HFRX Global Hedge Fund (2003-03..2023-08), EH Equity Market Neutral (2003-03..2023-08), ED Merger Arbitrage (2003-03..2023-08), Macro/CTA (2003-03..2023-08), Market Directional composite (2004-07..), Macro Systematic Diversified CTA (2004-12.., month-end-only rows in 2007-08). Annual: full years 2004-2022 (SDV/MD from 2005/2005).
- ONLY 6 series, two are composites - NOT a usable strategy cross-section (no HFRX EH, ED, RVA, Convertible Arb, FI, Distressed, Multi-Strat, Short Bias files exist on GitHub; searched).
- Checks passed: daily ROR vs level change <0.0005 except SDV (47 gap days); HFRX Macro/CTA FY2022 computed +3.75% = press release "+3.75 percent"; HFRX Market Directional FY2021 computed +13.65% = press "+13.65 percent"; HFRX Global 2018 computed -6.7% vs press "loss of 7 percent" (hedgenordic).
- Investable, net of fees (per HFR; not re-verified). HFRX Global runs ~3.8%/yr below CS broad over 2004-2021 (annual corr 0.95).
- LICENCE: raw files carry HFR's data-usage notice (internal, non-commercial use only; no redistribution). The claude repo is PUBLIC - do not commit these HFRX files into it.

## D. HFRI press-release year-end figures (long format, partial) 
- File: `hfri_press_fy_extracts_2019_2025.csv` (percent, every `verbatim_fragment` programmatically confirmed present in the saved page; pages in `hfr_pages/*.txt`). Complements first-pass `../hf/hfri_press_release_fy_extracts.csv` (2020-2023).
- URLs: hedgeweek 2019 https://www.hedgeweek.com/hedge-funds-record-best-annual-returns-decade-2019-says-hfr/ ; mondovisione 2021 https://mondovisione.com/media-and-resources/news/hfri-gains-to-conclude-strong-2021-202217/ ; mondovisione 2022 https://mondovisione.com/media-and-resources/news/hfri-500-macro-gains-in-december-leads-industry-to-record-outperformance-in-202-2023110/ ; thefullfx 2024 https://thefullfx.com/hedge-funds-end-2024-on-a-mixed-note-hfr/ ; hedgeweek 2025 https://www.hedgeweek.com/hedge-funds-post-strongest-annual-gains-since-2009-says-hfr/ ; allnews.ch 2025 (French) https://allnews.ch/node/148430
- Complete 4-strategy (EH/ED/Macro/RV Total) rows exist only for 2019, 2024, 2025 (with first pass: 2023 lacks Macro; 2020-2022 are mostly missing). Combined strategy-level set from HFR press:
  2019 EH 13.9 / ED 7.4 / RV 7.6 / Macro 6.2 ; 2024 EH 12.3 / ED 8.73 / RV 8.61 / Macro 5.95 ; 2025 EH 17.3 (index, not labelled Total) / ED 11.0 / RV 7.5 (Dec estimated) / Macro 7.2 (allnews; hedgeweek says "just over 7%").
- Year-end FY figures are preliminary, HFR revises (e.g. 2020 FWC 11.6 -> 11.8). Mixed index types (Total=fund-weighted vs HFRI 500 investable vs asset-weighted) - check the label before comparing. 2025 sub-strategies verified: EH Healthcare +33.8, EH Energy/Basic Materials +23.4, RV Convertible Arb +10.5, Multi-Manager/Pod +9.7.
- 2018 not obtained: hfr.com 2018 release 404; reposts only give HFRX figures in snippets (HFRX EH -9.7, HFRX Global ~-7).

## Spot-check against EDHEC overlap (annual, mapped strategies, 1997-2020 unless noted)
- CS vs EDHEC annual correlation: Conv Arb 0.98, Emerging Mkts 0.98, Event Driven 0.96, FI Arb 0.96, Distressed 0.95, L/S Equity 0.94, CTA/Managed Futures 0.91, EMN 0.86, Merger Arb/Risk Arb 0.86, Global Macro 0.75. Monthly corr lowest for EMN 0.69 and Global Macro 0.81. CS broad vs EDHEC FoF annual corr 0.93.
- The two families agree on the best mapped strategy in only 14 of 24 years (1997-2020) - so "best strategy last year" depends on the family; flag this if the test is run on one family only.
- HFRX vs EDHEC/CS is a weak match at the strategy level (EMN corr 0.25-0.44, Macro/CTA vs Global Macro 0.02-0.17; Macro/CTA vs CTA/Managed Futures 0.64-0.66; Systematic Diversified CTA vs CTA 0.73-0.81; Global vs CS broad 0.95).

## Not obtained / dead ends this round
- HFR hfr.com index pages: login page only (no tables). hfr.com press URLs ?p=24963, ?p=24788, ?p=42652 and the 2018/2019/2025 market-commentary slugs: 404 (reposts used instead).
- SG CTA / Trend indices (wholesale.banking.societegenerale.com): 403; search snippet says data requires contact/licence via SG Markets Analytics - no public download found.
- hedgeindex.com (Credit Suisse official): 503 via WebFetch (SSL failure earlier). No official CS annual table fetched.
- GitHub: no HFRI strategy monthly files (only HFRX above and tickers-only hfri.csv); no HFRX EH/ED/RVA files; no EDHEC vintage past 2021-06; no Eurekahedge/BarclayHedge files (BarclayHedge/Eurekahedge themselves were not retried).
- NOT tried within the time box: Preqin free tables, IASG, Hedge Fund Journal year-end tables, HFRX family press releases for other years.
- Overall: no consistent strategy-level family exists for 2022-2025 except sparse HFRI press figures; CS ends 2022-04, EDHEC 2021-06, HFRX 2023-08.
