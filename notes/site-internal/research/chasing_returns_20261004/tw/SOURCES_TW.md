# SOURCES_TW — Taiwan market history (data gathering only, no analysis)

Built 2026-10-04 in the session scratchpad. Nothing was written inside the repo and nothing was committed.

## Access situation (read first)
- **TWSE endpoints are WAF-blocked from this sandbox when fetched with curl.** Almost every `www.twse.com.tw` URL (`/rwd/zh/...`, legacy `/exchangeReport/...`, `/indicesReport/...`, `/downloads/...factbook...`, `?response=open_data`) returned a 307 to the "因為安全性考量，您所執行的頁面無法呈現" page. A few `FMTQIK` URLs passed at random and the same URL behaved the same on every retry. I did not try to get around the block with URL variations or mass retries.
- **TWSE data was obtained through the WebFetch tool**, which reaches the same TWSE JSON endpoints from a different network path. WebFetch passes the page through a small summarising model, so every TWSE number reached me as model-transcribed text, not as a raw file. Mitigations:
  - the prompt asked for verbatim rows or "last row only";
  - every series was cross-checked against an independent source (see Spot-checks);
  - where my own transcription mattered (the raw `twse_*_raw.txt` and `twse_ind/*.csv` files), those files are kept.
  - Residual risk: a transcription slip in a non-cross-checked cell, e.g. a single sector value in 2009–2020.
- Raw intermediate files in this folder: `twse_fmtqik_monthend_raw.txt` (ROC date|close), `twse_mfi94u_monthend_raw.txt`, `twse_ind/YYYY.csv`, `twii_yahoo_*.csv/json`, `tip/*.json`, `tip_indexes.json`.

## Providers and endpoints used
| Provider | Endpoint | Used for |
|---|---|---|
| TWSE (via WebFetch) | `https://www.twse.com.tw/rwd/zh/afterTrading/FMTQIK?date=YYYYMM01&response=json` (market daily TAIEX close; data exists from 1990-01) | TAIEX month-end closes 1990-01..1997-06; corrections/verifications for later months |
| TWSE (via WebFetch) | `https://www.twse.com.tw/rwd/zh/TAIEX/MFI94U?date=YYYYMM01&response=json` (發行量加權股價報酬指數 daily; starts 2003-01-02) | TR index month-end 2003-01..2020-12 |
| TWSE (via WebFetch) | `https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date=YYYYMMDD&type=IND&response=json` | sector (類股) price index year-end closes 2009..2020; 2025-12-31 full table used to verify TIP |
| Yahoo Finance | `https://query1.finance.yahoo.com/v8/finance/chart/%5ETWII?range=max&interval=1mo` and `period1=0&interval=1d` (history starts 1997-07-02) | TAIEX month-end 1997-07..2020-12 |
| Wikipedia | `https://en.wikipedia.org/wiki/TAIEX` ("Annual Returns" table, 1966–2025; cites TWSE) | annual closes 1967–1989; cross-check elsewhere |
| TIP 臺灣指數公司 (runs the TWSE indices) | `https://backend.taiwanindex.com.tw/api/indexes` (catalogue) and `.../api/indexes/{code}/records?start=YYYY-MM-DD&end=YYYY-MM-DD` (daily price + total-return series) | everything 2021-01-04..2026-10-02: TAIEX price and TR, all sector price indices; index metadata (base/launch dates). The API only holds data from 2021-01-04 (earlier windows return empty) |
| DGBAS / FRED / IMF / data.gov.tw | see "What failed" | CPI: not obtained |

## Files
- `taiex_monthly.csv` — month, close, last_session_date, source, note. **1990-01..2026-09 (441 months), price index.** 1990-01..1997-06 TWSE; 1997-07..2020-12 Yahoo monthly bars with TWSE overrides; 2021-01..2026-09 TIP/TWSE.
- `taiex_annual.csv` — year, close, price_return, source, note. 1966 (base)..2025 year-end + 2026 (Sep-30, YTD).
- `taiex_tr_monthly.csv` — TAIEX total return index (發行量加權股價報酬指數) month-end 2003-01..2026-09, plus the same-month price close. A 2002-12 base row is **inferred** and flagged.
- `taiex_tr_annual.csv` — TR and price year-end returns 2003–2025 and `implied_income_uplift` = (1+TR)/(1+price)−1.
- `tw_sector_yearend.csv` — rows = year (2009..2025, plus 2026 at 09-30), columns = TWSE sector index names in Chinese (renamed to current names, see below). `tw_sector_yearend_long.csv` keeps the original names, source and exact date per cell. `tw_sector_index_meta.csv` has TIP code, English name, base date and first publish date.
- `tw_cpi.csv` — **not created** (CPI not obtained).

## Spot-checks
- **1990** year-end: Wikipedia 4,530.16 = TWSE FMTQIK final session 1990-12-27 4,530.16. OK
- **2025** year-end: Wikipedia 28,963.60 = Yahoo = TIP = TWSE MI_INDEX 2025-12-31 28,963.60. OK
- **2000** year-end: Wikipedia and Yahoo 4,743.94 but TWSE final session (Saturday 2000-12-30) is **4,739.09**, so the Wikipedia/Yahoo value does not match TWSE. The file uses TWSE.
- 2009–2020: headline TAIEX in the 12 TWSE sector files equals Wikipedia/Yahoo year-end in all 12 years.
- 2021-01..2026-09: all 69 TIP month-ends equal the Yahoo month-ends (0 mismatches). 16 sector values at 2025-12-31 from TIP equal the TWSE MI_INDEX values.
- 1997-12, 1998-12, 1999-12, 2001-12: TWSE FMTQIK equals Yahoo/Wikipedia.

## Findings on data quality (important for replication)
1. **Saturday trading sessions.** TWSE held half-day Saturday sessions until 2000-12-30, plus occasional make-up Saturdays later. Yahoo daily omits them, and the Wikipedia annual table appears to use the last weekday close in some years. Differences found against TWSE:

   | Series | Period | Wikipedia/Yahoo vs TWSE |
   |---|---|---|
   | Year-end | 1991 | 4,540.55 vs **4,600.67** |
   | Year-end | 1994 | 7,111.10 vs **7,124.66** |
   | Year-end | 1995 | 5,158.65 vs **5,173.73** |
   | Year-end | 2000 | 4,743.94 vs **4,739.09** |
   | Month-end (Yahoo) | 1997-08 | 9,827.49 vs 9,756.47 |
   | Month-end (Yahoo) | 2000-04 | 8,824.36 vs 8,777.35 |
   | Month-end (Yahoo) | 2000-09 | 6,432.36 vs 6,185.14 |
   | Month-end (Yahoo) | 2007-09 | 9,411.95 vs 9,476.52 |
   | Month-end (Yahoo) | 2016-01 | 8,080.60 vs 8,145.21 |
   | Month-end (Yahoo) | 2017-09 | 10,329.94 vs 10,383.94 |
   | Month-end (Yahoo) | 2018-03 | 10,906.22 vs 10,919.49 |

   `taiex_annual.csv` and `taiex_monthly.csv` use the TWSE values and record the override in `source`/`note`. Yahoo's daily series is also wrong for 1998-10, 1999-01, 1999-07 and 1999-10 (Saturday month-ends), but the Yahoo monthly bars used here match TWSE for those months.
2. **1967–1989 annual closes are Wikipedia only and unverified.** TWSE API history starts in 1990. Years that ended on a Saturday (1977, 1978, 1983, 1988, 1989) may carry the same Friday-vs-Saturday error seen in 1991/1994/1995/2000. The 1967 "return" is measured against the 1966 **average** (base 100), not a 1966 year-end close.
3. **Yahoo 1997-08..2020-12 was only partially verified.**
   - Months whose last calendar day was a Sat/Sun were checked against TWSE for 1997-07..2002-12.
   - 2003–2020 was checked by comparing Yahoo's last valid daily date with TWSE's last session date from the TR file; the only mismatches were the four months overridden above.
   - Other 1997–2002 months are Yahoo values without a TWSE cross-check.
4. **Index rebasing:** TAIEX is not rebased (base 1966 average = 100, published from 1970-11-02). TR index base: first TR observation 2003-01-02 = 4,524.92 vs price 4,524.87 (price +72.42 on the day), so the base is the 2002-12-31 price level 4,452.45. This is an inference from data, not read from a TWSE document, and TIP's own metadata for IR0001 is inconsistent ("base 100").
5. **Price vs total return.**
   - Everything in `taiex_monthly.csv`, `taiex_annual.csv` and `tw_sector_yearend.csv` is **price index only** (no dividends).
   - TWSE TR starts 2003 (cash dividends reinvested).
   - Derived uplift, TR vs price: mean +3.7% per year over 2004–2025 (`taiex_tr_annual.csv`). Year-by-year it ranges from about 2.5% to 4.8% in recent years. Use the file, not the mean.
6. **Dividend yield for pre-2003 gross-up: not obtained.** The TWSE market-wide PER/dividend-yield statistic is in the Fact Book ("Market PER and Dividend Yield (2015-2024)", plus a by-industry year-end table), but those pages are tables I could not extract, and the per-stock BWIBBU endpoints were not pulled. The only dividend information in the files is the implied TR-minus-price uplift from 2003.

## Sector indices (類股) notes
- **Coverage: year-end closes 2009–2025 plus 2026-09-30, 40 series.** TWSE `MI_INDEX type=IND` returned **empty data tables for 2006-12-29 and 2008-12-31** and had data for 2009-12-31. The first date with data was not bisected. The 2003-12-31 query was rejected as earlier than the supported date. **Year-end sector history before 2009 is missing**, so 1987/1995–2008 was not obtained. TIP only holds 2021+.
- Last trading day of December used (per-cell date is in `tw_sector_yearend_long.csv`): 2011-12-30, 2012-12-28, 2016-12-30, 2017-12-29, 2018-12-28, 2021-12-30, 2022-12-30, 2023-12-29. Other years use 12-31.
- **Index launch bases (TIP metadata):**

  | Index group | Base date | First published |
  |---|---|---|
  | Food, Textiles, Paper, Building Materials, Finance | 1986-12-29 | 1987-01-06 |
  | Cement-ceramic (水泥窯製), Plastic-chemical (塑膠化工), Electrical (機電) composites | 1986-12-29 | 1987-01-06 |
  | Cement, Plastic, Electric Machinery, Electrical & Cable, Chem/Biotech/Medical, Glass & Ceramic, Iron & Steel, Rubber, Automobile, Electronics, Shipping, Tourism, Trading, Others | 1994-12-31 | 1995-08-01 |
  | Semiconductors, Computer & Peripheral, Optoelectronics, Communications, Electronic Components, Electronic Distribution, Information Services, Other Electronics, **Chemical, Biotech & Medical, Oil/Gas/Electricity** | 2007-06-29 | 2007-07-02 |
  | Green Energy & Environment, Digital & Cloud, Sports & Leisure, Household | 2023-06-30 | 2023-07-03 |

  So sub-sector electronics indices exist only from 2007 (the 2009+ file is therefore fully covered for them), and the four 2023 sectors have only 2023, 2024, 2025 and 2026-09 values. The 2007 and 2023 launches reclassified part of the market (化學生技醫療 split into 化學 + 生技醫療; 2023 added four industries). I did not verify membership changes or index continuity across those dates, and I did not verify a 2016 reclassification at all.
- **Renames harmonised in `tw_sector_yearend.csv`** (originals kept in the long file):
  - 電子類指數 (through 2018) → 電子工業類指數
  - 觀光類指數 → 觀光餐旅類指數
  - 未含金融保險股指數 → 未含金融指數
  - 未含電子股指數 → 未含電子指數
  - 未含金融電子股指數 → 未含金融電子指數
- Both old and new composite sectors appear: 化學生技醫療 together with 化學 and 生技醫療; and 水泥窯製/塑膠化工/機電 composites together with their components. Do not double count.
- Not included: TWSE sector total-return indices (TIP has them from 2021, TWSE from the 1987/1995/2007 bases; not pulled). The TWSE sector TR tables for 2009–2020 are also available in the same MI_INDEX response but were not extracted.

## What failed / missing
- TAIEX **monthly before 1990**: no accessible source (TWSE API starts 1990). Only annual 1967–1989 (Wikipedia).
- TR index monthly before 2003: does not exist at TWSE.
- **CPI (`tw_cpi.csv`) not obtained.** Tried:
  - DGBAS nstatdb (`nstatdb.dgbas.gov.tw`, JS-rendered; CSV URL guesses returned an error page);
  - stat.gov.tw CPI page (no direct download link);
  - FRED (`fred.stlouisfed.org`: HTTP/2 INTERNAL_ERROR/timeout through the proxy);
  - IMF DataMapper (403, Akamai);
  - data.gov.tw (only Taipei City CPI, annual from ROC 87 = 1998, not national).
- TWSE direct curl: blocked as described above.
