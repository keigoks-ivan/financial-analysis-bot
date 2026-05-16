# DD v12.3 Upgrade Manifest

**Live work tracker.** Each window: pull → claim 3 `pending` (or `dca_only`) → mark `in_progress` + window-id → push manifest → do work → commit batch (DD + DCA + manifest `done`) → push.

Trigger skill: `/dd-v12-3-upgrade 3`  (or natural: `跑 v12.3 升級 3 檔`)

## Counts

- **pending** (legacy → full body upgrade + DCA cascade): 93
- **dca_only** (already v12.3, just DCA cascade audit): 17
- **skip** (META/CRDO/DIS in flight elsewhere): 3
- **total tickers**: 113

Schema breakdown (latest DD per ticker):
- v12.3: 20
- v12.2: 34
- v12.1: 16
- v12.0: 37
- pre-v12: 6

## Hard gates (per upgrade)

- DD post-upgrade size **≥ 80 KB**
- DCA post-cascade size **≥ 50 KB**
- No-fabricate: every number in §8.H / §11 / §12 / §10 peer / §13.4 needs inline source citation
- Pre-flight WebSearch ≥ 3 (customer concentration / SBC / M&A 5Y)
- Cold-review every 5 batch (sonnet sub-agent on random ticker)

## Manifest

| ticker | latest_dd | schema | size_kb | status | claimed_by | notes |
|---|---|---|---|---|---|---|
| 2308 | DD_2308_20260325.html | pre-v12 | 53.4 | pending | – | pre-v12-heavy; under-80kb (53.4kb) |
| 2308TW | DD_2308TW_20260514.html | v12.2 | 84.0 | pending | – | – |
| 2330 | DD_2330_20260409.html | pre-v12 | 53.0 | pending | – | pre-v12-heavy; under-80kb (53.0kb) |
| 2330TW | DD_2330TW_20260514.html | v12.3 | 82.4 | done | win-20260516-1349-cd3c | dca-only: 3 files audited, 0 broken anchor; DCA_2330TW_20260506 (49.8KB) pre-existing under-floor, unedited |
| 2383TW | DD_2383TW_20260418.html | v12.0 | 73.2 | pending | – | under-80kb (73.2kb) |
| 2454 | DD_2454_20260504.html | v12.2 | 59.8 | pending | – | under-80kb (59.8kb) |
| 3017 | DD_3017_20260504.html | v12.2 | 80.5 | pending | – | – |
| 3661TW | DD_3661TW_20260514.html | v12.2 | 84.3 | pending | – | – |
| 6146T | DD_6146T_20260420.html | v12.0 | 23.5 | pending | – | under-80kb (23.5kb) |
| 6857T | DD_6857T_20260420.html | v12.0 | 24.5 | pending | – | under-80kb (24.5kb) |
| AAPL | DD_AAPL_20260504.html | v12.3 | 83.1 | done | win-20260516-1549-eeec | legacy_full v12.2→v12.3 (sonnet sub-agent): §2 D R:R QC-29 砍 + §7 砍低估值 + §13 砍 13.0/13.3/13.5 + §5.F iPhone 18 AI adoption ≥ 50% (2026-09 trigger) + §5.B sourced floor (iPhone ASP ≥ $950 / Services ≥ $130B / FPE floor 24x) + §5.C ⚡🔥🐢 + §8.H data-gap reframe (10-K no customer ≥ 10%, geographic Americas 42%/China 16%/Europe 25%, product iPhone 52%/Services 24%) + §9 F 二維 execution 9 / pricing 9 + QC-23 ⛔ Apple Intelligence vs Gemini 架構 (15%/24M) + §12 M&A 5Y (Pixelmator 2024 / DarwinAI 2024 / 7 AI startups 2025, organic-first) + SBC FY24 2.99% / FY25 2.88% (低於警示) ex-EPS gap ~10% 由 16.5B share count 主導 + §13.4 mega-cap platform tier (MSFT/GOOGL/META/AMZN, excluded chip-only); verdict 不變 B; DCA cascade 2 files (57.4/64.9 KB) QC-29 + MA60/200/104w label fixed |
| ADI | DD_ADI_20260427.html | v12.1 | 62.6 | pending | – | under-80kb (62.6kb) |
| AENA | DD_AENA_20260428.html | v12.1 | 80.1 | pending | – | – |
| ALAB | DD_ALAB_20260506.html | v12.3 | 100.3 | done | win-20260516-1403-6a45 | legacy_full v12.2→v12.3: §2 D R:R 瘦身 + §7 砍低估值四問 + §13 砍 13.0/13.3/13.5 + §5.F single thing 新增 (FY27 Q3 新 hyperscaler 量產 binary event) + §8.H 客戶結構 (top-1 >70% / top-3 ~86% 引 FY25 10-K) + §9 F 二維 moat (execution 9 + pricing 9 → A) + §12 M&A 5Y track (aiXscale Photonics 2026-01 $74M) + SBC ex-EPS ⚠️ (FY24 59% IPO 後常態) + dd-meta moat_execution/pricing sub-scores; verdict 不變 B; DCA cascade 2 files (QC-29/0/4 + MA60/200/104w stress label 修正) |
| AMAT | DD_AMAT_20260515.html | v12.3 | 104.2 | done | win-20260516-1349-cd3c | dca-only: 3 files audited, 1 anchor fix in DCA_AMAT_20260511 (§13.5 → v12.0 source attribution + v12.3 §13.4 peer cross-ref) |
| AMD | DD_AMD_20260506.html | v12.3 | 84.9 | done | win-20260516-1549-eeec | legacy_full v12.2→v12.3 (sonnet sub-agent): §2 D QC-29 砍 + §7 砍低估值/便宜理由 + §13 砍 13.0/13.3/13.5 + §5.F MI355X/MI450 Helios H2 2026 量產 + 3 家 hyperscaler design-win binary + §5.B sourced floor (DC YoY ≥ 30% / server CPU 市佔 ≥ 38% / FPE ≥ 20x) + §8.B price/vol 30%/70% + 5Y M&A (Xilinx $35B / Pensando $1.9B / Silo $665M / ZT $4.9B / Enosemi) + §8.H top-1 MSFT ~12-15% (10-K data-gap explicit, hyperscaler ASIC 四大 in-house risk 分析) + §9 二維 execution 8 / pricing 6 + QC-23 (🟡 INTC / 🔴 NVDA Rubin / ⛔ ASIC) + §12 M&A integration table + SBC FY25 4.1%, Non-GAAP vs GAAP gap 38.5% ⚠️ (主因 Xilinx amortization $2B+/yr) + §13.4 NVDA/INTC direct peer, AVGO 列參考非 anchor; verdict 不變 B; DCA cascade 1 file (69.5 KB) §5 cross-ref note |
| AMZN | DD_AMZN_20260430.html | v12.3 | 102.0 | done | win-20260516-1549-eeec | legacy_full v12.1→v12.3 (sonnet sub-agent): §2 E QC-29 砍 + §7 砍低估值 + §13 砍 13.0/13.3/13.5 + §5.F AWS YoY ≥ 25% × 4 季 + margin ≥ 35% binary (Q4 2026 trigger) + §5.B sourced floor (10-K 2025 / 2026-04-29 法說 / CNBC 2026-04-20) + §5.C 🐢🔥⚡ + §8.B price/vol AWS 5%/23%, Ads 8%/16%, NA Retail 2%/11% + 5Y M&A (MGM $8.45B 2022 ✓ / One Medical $3.9B 2023 ⚠ / iRobot $1.7B 2024 terminated ✗ / Anthropic $4B→$25B 2023-26 ✓) + §8.H data-gap (no customer ≥10%; NA 61.5% / Intl 20.5% / AWS 18%; Anthropic 44% Trainium concentration) + §9 二維 execution 10 / pricing 8 (composite 9 → S) + QC-23 (🟡 GOOGL/Walmart/NVDA / 🔴 MSFT Azure + GOOGL shopping agent / ⛔ decentralized AI inference ~5%) + §12 SBC ex-EPS $7.17 GAAP → $8.61 ex-SBC +20% gap ⚠️ + §13.4 mega-cap cloud+retail tier (MSFT/GOOGL/META/WMT, AAPL labeled non-ideal); verdict 不變 B; DCA cascade 1 file (68.0 KB) |
| ANET | DD_ANET_20260506.html | v12.2 | 79.1 | pending | – | under-80kb (79.1kb) |
| APH | DD_APH_20260504.html | v12.3 | 107.9 | done | win-20260516-1413-083f | legacy_full v12.2→v12.3 (pilot): §2 9→7 子節 + §7 砍低估值/便宜理由四問 + §13 砍 13.0/13.3/13.5 + §5.F NVDA cable-free binary event + §8.B price/vol split + §8.H top-1 <10% (10-K FY2024) + top-5 25-30% data-gap aside + §9 二維 execution 9 / pricing 8 + §10 peer compare + ex-buyback EPS CAGR + FCF lumpiness 非 lumpy + §11 議價權三段 (上/下/地緣) + §12 M&A 5Y track (CIT $2.025B / CCS $10.5B etc) + SBC ex-EPS 3.0% < 5pp 無⚠️ + §13.4 connector tier (TEL/Sensata/Aptiv/Molex 避 AVGO/MRVL 錯 tier); verdict 不變 A; DCA cascade clean 2 files (56.4 + 59.4 KB) 0 broken anchors |
| APP | DD_APP_20260418.html | v12.0 | 61.7 | pending | – | under-80kb (61.7kb) |
| ARM | DD_ARM_20260427.html | v12.1 | 78.4 | pending | – | under-80kb (78.4kb) |
| ASML | DD_ASML_20260515.html | v12.3 | 100.6 | done | win-20260516-1349-cd3c | dca-only: 2 files audited, 0 broken anchor |
| AVGO | DD_AVGO_20260418.html | v12.0 | 56.3 | pending | – | under-80kb (56.3kb) |
| BE | DD_BE_20260429.html | v12.1 | 88.1 | in_progress | win-20260516-1610-9762 | – |
| BESI | DD_BESI_20260420.html | v12.0 | 30.4 | pending | – | under-80kb (30.4kb) |
| BSX | DD_BSX_20260418.html | v12.0 | 102.2 | in_progress | win-20260516-1558-ceca | – |
| BWXT | DD_BWXT_20260505.html | v12.2 | 61.9 | pending | – | under-80kb (61.9kb) |
| CAMT | DD_CAMT_20260514.html | v12.2 | 69.7 | pending | – | under-80kb (69.7kb) |
| CAT | DD_CAT_20260504.html | v12.2 | 60.3 | pending | – | under-80kb (60.3kb) |
| CDNS | DD_CDNS_20260504.html | v12.2 | 50.1 | pending | – | under-80kb (50.1kb) |
| CIEN | DD_CIEN_20260427.html | v12.0 | 68.2 | pending | – | under-80kb (68.2kb) |
| CLS | DD_CLS_20260428.html | v12.1 | 73.4 | pending | – | under-80kb (73.4kb) |
| CMG | DD_CMG_20260516.html | v12.3 | 78.2 | done | win-20260516-1355-78dc | dca-cascade clean (0 broken anchors); 2 dcas ≥ 50kb |
| COHR | DD_COHR_20260418.html | v12.0 | 63.9 | pending | – | under-80kb (63.9kb) |
| COST | DD_COST_20260427.html | v12.1 | 57.0 | pending | – | under-80kb (57.0kb) |
| CRDO | DD_CRDO_20260516.html | v12.3 | 79.7 | skip | – | in flight (other window) |
| CRM | DD_CRM_20260418.html | v12.0 | 65.4 | pending | – | under-80kb (65.4kb) |
| CRWD | DD_CRWD_20260418.html | v12.0 | 60.2 | pending | – | under-80kb (60.2kb) |
| CSCO | DD_CSCO_20260427.html | v12.0 | 54.8 | pending | – | under-80kb (54.8kb) |
| DDOG | DD_DDOG_20260516.html | v12.3 | 78.4 | done | win-20260516-1355-78dc | dca-cascade clean (0 broken anchors); 2 dcas ≥ 50kb |
| DELL | DD_DELL_20260418.html | v12.0 | 49.4 | pending | – | under-80kb (49.4kb) |
| DIS | DD_DIS_20260516.html | v12.3 | 102.2 | skip | – | in flight (other window) |
| EAT | DD_EAT_20260428.html | v12.1 | 81.7 | in_progress | win-20260516-1420-1db7 | – |
| EBAY | DD_EBAY_20260516.html | v12.3 | 105.7 | done | win-20260516-1350-2107 | dca-cascade clean (0 broken anchors); dca-under-50kb (49.1kb) pre-existing |
| ETN | DD_ETN_20260506.html | v12.2 | 79.4 | pending | – | under-80kb (79.4kb) |
| FICO | DD_FICO_20260418.html | v12.0 | 68.9 | pending | – | under-80kb (68.9kb) |
| FIX | DD_FIX_20260516.html | v12.3 | 87.8 | done | win-20260516-1350-2107 | dca-cascade clean (0 broken anchors); dca 55.6kb |
| FN | DD_FN_20260505.html | v12.2 | 73.2 | pending | – | under-80kb (73.2kb) |
| FORM | DD_FORM_20260427.html | v12.0 | 70.9 | pending | – | under-80kb (70.9kb) |
| FTNT | DD_FTNT_20260427.html | v12.0 | 65.8 | pending | – | under-80kb (65.8kb) |
| GEV | DD_GEV_20260504.html | v12.2 | 71.8 | pending | – | under-80kb (71.8kb) |
| GFS | DD_GFS_20260427.html | v12.1 | 75.7 | pending | – | under-80kb (75.7kb) |
| GLW | DD_GLW_20260429.html | v12.1 | 70.5 | pending | – | under-80kb (70.5kb) |
| GOOGL | DD_GOOGL_20260504.html | v12.2 | 99.2 | pending | – | released by win-20260516-1441-1e69 (sub-agent stream timeout before patch applied; file unchanged) |
| GRAB | DD_GRAB_20260505.html | v12.2 | 65.7 | pending | – | under-80kb (65.7kb) |
| HWM | DD_HWM_20260418.html | v12.0 | 76.6 | pending | – | under-80kb (76.6kb) |
| INTC | DD_INTC_20260427.html | v12.0 | 82.4 | in_progress | win-20260516-1620-67d3 | legacy_full v12.0→v12.3 |
| ISRG | DD_ISRG_20260418.html | v12.0 | 62.2 | pending | – | under-80kb (62.2kb) |
| JBL | DD_JBL_20260418.html | v12.0 | 53.7 | pending | – | under-80kb (53.7kb) |
| KEYS | DD_KEYS_20260418.html | v12.0 | 59.9 | pending | – | under-80kb (59.9kb) |
| KLAC | DD_KLAC_20260516.html | v12.3 | 82.3 | done | win-20260516-1349-e2c6 | dca-only: 2 files audited, 4 anchor fixes (QC-29/0/4 stress→v12.3 2/2; MA60/200/104w→短期/中期) + v12.3 reconciliation block in DCA_KLAC_20260507 (under-floor remediation 49.8→51.7 KB) |
| LITE | DD_LITE_20260506.html | v12.2 | 82.6 | in_progress | win-20260516-1420-1db7 | – |
| LLY | DD_LLY_20260504.html | v12.3 | 103.8 | done | win-20260516-1441-1e69 | legacy_full v12.2→v12.3: §2/§7/§13 砍 + §5.F retatrutide TRIUMPH-1/2 binary event + §8.B 5Y M&A + §8.H 3 wholesaler distributors >10% (10-K Note 2; specific % data-gap aside) + §9 二維 execution 10 + pricing 9 (S; QC-23 ⛔-1 = retatrutide failure 10%) + §10 ex-buyback EPS CAGR ~92% + FCF U-shape lumpy + §11 議價權三段 (上 contract mfg / 下 McKesson+Cencora+Cardinal+PBM / 地緣 US 50%+) + §12 M&A track (Loxo/Versanis/Akouos/Point/Morphic etc) + §13.4 big-pharma GLP-1 tier (NVO/MRK/PFE/JNJ/ABBV); verdict 不變 A+; DCA cascade 2 files (53.6 + 57.6 KB), 3 §13.5 anchor fixes in DCA_LLY_20260511 |
| LRCX | DD_LRCX_20260425.html | v12.0 | 67.7 | pending | – | under-80kb (67.7kb) |
| LULU | DD_LULU_20260516.html | v12.3 | 78.2 | done | win-20260516-1355-78dc | dca-cascade clean (0 broken anchors); 2 dcas ≥ 50kb |
| MA | DD_MA_20260516.html | v12.3 | 85.3 | done | win-20260516-1350-2107 | dca-cascade clean (0 broken anchors); dca 51.0kb |
| MAR | DD_MAR_20260414.html | pre-v12 | 70.4 | pending | – | pre-v12-heavy; under-80kb (70.4kb) |
| MELI | DD_MELI_20260513.html | v12.2 | 86.4 | in_progress | win-20260516-1420-1db7 | – |
| META | DD_META_20260516.html | v12.3 | 75.6 | skip | – | in flight (other window) |
| MOD | DD_MOD_20260427.html | v12.0 | 65.8 | pending | – | under-80kb (65.8kb) |
| MPWR | DD_MPWR_20260418.html | v12.0 | 67.5 | pending | – | under-80kb (67.5kb) |
| MRVL | DD_MRVL_20260418.html | v12.0 | 73.8 | pending | – | under-80kb (73.8kb) |
| MSFT | DD_MSFT_20260515.html | v12.3 | 86.7 | done | win-20260516-1349-e2c6 | dca-only: 2 files audited, 1 anchor fix in DCA_MSFT_20260507 (QC-29 3/3 stress→v12.3 stress 2/2) + v12.3 reconciliation block (under-floor remediation 47.2→50.0 KB) |
| MU | DD_MU_20260418.html | v12.0 | 71.3 | pending | – | under-80kb (71.3kb) |
| NET | DD_NET_20260515.html | v12.3 | 77.5 | done | win-20260516-1400-1792 | dca-only: 2 files audited, 0 broken anchor; DCA_NET_20260508 (49.1KB) pre-existing under-floor, unedited |
| NFLX | DD_NFLX_20260516.html | v12.3 | 86.2 | done | win-20260516-1349-e2c6 | dca-only: 2 files audited, 1 anchor fix in DCA_NFLX_20260511 (QC-29 0/4 stress→v12.3 stress 2/2) |
| NKE | DD_NKE_20260516.html | v12.3 | 80.7 | done | win-20260516-1358-e570 | dca-cascade clean (2 DCAs, 0 broken anchor) |
| NOW | DD_NOW_20260427.html | v12.0 | 80.4 | in_progress | win-20260516-1620-67d3 | legacy_full v12.0→v12.3 |
| NU | DD_NU_20260515.html | v12.3 | 78.0 | done | win-20260516-1400-1792 | dca-only: 1 file audited, 1 anchor fix in DCA_NU_20260515 (QC-29 label removed; substantive 2/4 stress data preserved as it matches DD dd-meta) |
| NVDA | DD_NVDA_20260418.html | v12.0 | 55.1 | pending | – | under-80kb (55.1kb) |
| NVMI | DD_NVMI_20260515.html | v12.2 | 73.8 | pending | – | under-80kb (73.8kb) |
| NXPI | DD_NXPI_20260504.html | v12.3 | 104.4 | done | win-20260516-1441-1e69 | legacy_full v12.2→v12.3: §2/§7/§13 砍 + §5.F Q2 GM ≥ 57.5% binary + §8.B price/vol split + §8.H top-1 <10% / Avnet distributor 22% (10-K) / top-5/10 data-gap aside + §9 二維 execution 9 + pricing 8 (A; QC-23 🟡 Renesas+Infineon, 🔴 China local 40%, ⛔ Tesla SoC + RISC-V) + §10 peer compare (Infineon/Renesas/STM/ON) + §11 議價權三段 (上 TSMC/Samsung/ASE+Amkor / 下 Tier-1 named + Apple ~8-10% / 地緣 EU+China 35%) + §12 M&A 5Y (TTTech $625M / Kinara $307M / Aviva Links $243M / Marvell auto $1.78B cancelled) + SBC FY24 3.65% + §13.4 auto/industrial analog+MCU IDM tier (避 AVGO/MRVL 錯 tier); verdict 不變 B; DCA cascade 2 files clean (44.6 + 60.5 KB; DCA_NXPI_20260507 pre-existing under-floor, unedited) |
| ON | DD_ON_20260505.html | v12.3 | 111.3 | done | win-20260516-1414-59b1 | legacy_full v12.2→v12.3: §2 9→7 子節 + §7 砍低估值/便宜理由四問 + §13 砍 13.0/13.3/13.5 + §5.F (Q2 26 GAAP GM ≥ 39% binary) + §8.B M&A 5Y (GT 2021 ✅ / Quantenna 2019 ⚠️ / Allegro 2025 ❌) + §8.H top-1 distributor ~10-12% (10-K FY24) + §9 二維 execution 7 / pricing 6 → B + §10 ex-buyback EPS CAGR 22.2% + FCF lumpiness FY23 trough + §11 議價權三段 (上/下/地緣) + §12 SBC FY25 2.40% Rev + §13.4 peer tier mid-tier power semi (STM/IFX/MCHP/NXP 17-19x); verdict 不變 B; 22 inline source URLs; DCA cascade 2 files (07: 46.3KB pre-existing under-floor; 11: 58.0KB) |
| ONTO | DD_ONTO_20260506.html | v12.3 | 118.0 | done | win-20260516-1555-c02c | legacy_full v12.2→v12.3 (sub-agent): §2 9→7 子節 + §7 砍低估值/便宜理由四問 + §13 砍 13.0/13.3/13.5 + §5.F HBM4 reference binary (2026Q4-2027Q2, +57%/-34%) + §5.B sourced floor + §5.C ⚡🔥🐢 + §8.B M&A 5Y 4 deals $1.34B + 定價/量 3Y 20%→30% + §8.H top-1 SK Hynix 12-15% + top-5 ~50-55% + dual-track HBM5 re-tender + §9 二維 execution 7 / pricing 8 (NOT single-axis) + QC-23 三級 (🟡 40%+30% / 🔴 20% / ⛔ 10%) + §10 ex-buyback EPS CAGR 31.5% vs 32% (gap <5pp) + FCF lumpiness FY23 trough cv=0.49 🟡 + §11 議價權三段 + §12 M&A 5Y + SBC ex-EPS dilution 22% ⚠️ + §13.4 metrology peer tier (CAMT/Lasertec/NVMI, ban KLAC/AMAT/ASML cross-tier); verdict 不變 B; DCA cascade 2 files (07: 57.2KB + 11: 54.6KB) 3 QC-29 anchor 修正 |
| ORCL | DD_ORCL_20260418.html | v12.0 | 60.3 | pending | – | under-80kb (60.3kb) |
| PANW | DD_PANW_20260427.html | v12.0 | 70.4 | pending | – | under-80kb (70.4kb) |
| PLTR | DD_PLTR_20260505.html | v12.2 | 82.6 | pending | – | – |
| PYPL | DD_PYPL_20260323.html | pre-v12 | 54.4 | pending | – | pre-v12-heavy; under-80kb (54.4kb) |
| QCOM | DD_QCOM_20260504.html | v12.2 | 81.6 | pending | – | – |
| RCL | DD_RCL_20260508.html | v12.3 | 121.9 | done | win-20260516-1555-c02c | legacy_full v12.2→v12.3 (sub-agent): §2 9→7 子節 + §7 砍低估值/便宜理由 + §13 砍 13.0/13.3/13.5 + §5.F FY26 Adj EPS guide floor binary + §5.B sourced floor + §5.C ⚡🔥🐢 + §8.B 5Y M&A (Silversea 2018→2020 only) + 定價/量 3Y + §8.H B2C reframe (NA 64% / EU 22% / Asia 8%, Royal 70% / Celebrity 22% / Silversea 5%, Icon-class Meyer Turku single-source, customer deposits ~$6B refund 壓力) + §9 二維 execution 8.5 ↑ widening / pricing 8.0 → stable (composite 8/10) + QC-23 (🟡×3 / 🔴×2 / ⛔×1) + §10 3Y trend + peer (CCL/NCLH) + ex-buyback EPS CAGR 12% vs 13% (<5pp) + FCF lumpiness capex cycle 2025-2028 + §11 議價權三段 (上游 shipyard duopoly Meyer Turku/Chantiers/Fincantieri + 下游 B2C 95% Q4 26 pricing power + 地緣 Caribbean/Med/EU ETS/China) + §12 M&A 5Y near-zero + SBC FY24 $363M (+75% YoY MacroTrends, 2.0% Rev not 0.5%) + §13.4 cruise tier (CCL/NCLH/VIK, exclude DIS/MAR/HLT); verdict 不變 A (sub-agent §1 "原 A+ 降為 A" 為 hypothetical baseline 而非 v12.2 實際 verdict shift); DCA cascade 2 files (DCA_RCL_20260507 clean 57.9KB + DCA_RCL_20260511 QC-29 anchor 修正 59.7KB) |
| RMBS | DD_RMBS_20260427.html | v12.0 | 73.4 | pending | – | under-80kb (73.4kb) |
| RMS | DD_RMS_20260418.html | v12.0 | 99.2 | in_progress | win-20260516-1558-ceca | – |
| ROK | DD_ROK_20260418.html | v12.0 | 68.9 | pending | – | under-80kb (68.9kb) |
| ROP | DD_ROP_20260330.html | pre-v12 | 91.4 | pending | – | pre-v12-heavy |
| SBUX | DD_SBUX_20260429.html | v12.1 | 90.2 | in_progress | win-20260516-1620-67d3 | legacy_full v12.1→v12.3 |
| SE | DD_SE_20260513.html | v12.2 | 87.2 | in_progress | win-20260516-1610-9762 | – |
| SIMO | DD_SIMO_20260427.html | v12.1 | 69.2 | pending | – | under-80kb (69.2kb) |
| SNDK | DD_SNDK_20260504.html | v12.3 | 107.4 | done | win-20260516-1555-c02c | legacy_full v12.2→v12.3 (sub-agent): §2 9→7 子節 + §7 砍低估值/便宜理由 + §13 砍 13.0/13.3/13.5 + §5.F NAND ASP ≥ +30% Q3 FY27 + BiCS10 量產 hyperscaler 認證 binary + §5.B sourced floor + §8.B 5Y M&A near-zero (post-spin Feb 2025, WDC era separate) + Kioxia 合併概率 25% + §8.H top-1 < 10% (10-K) + top-10 40% Q1 FY26 vs 53% YoY (10-Q 2025-11-07) diversifying + dual-track hyperscaler + cyclical risk + §9 二維 execution 6 / pricing 2 (NAND commodity, pricing power LOW) → composite ~5 + QC-23 (🟡 Micron/Samsung / 🔴 China YMTC / ⛔ MRAM tech transition) + §10 FCF lumpiness FY23 trough -$932M peak-trough $11B (商品 cycle natural lumpy not red flag) + ex-buyback EPS CAGR gap <5pp + §12 SBC GAAP $23.03 vs Non-GAAP $23.41 gap 1.6% < 5pp + §13.4 NAND pure-play tier (Kioxia ideal peer, exclude WDC/NTAP cross-tier); verdict 不變 B; stress 0/4 → 2/2 框架更新; DCA_SNDK_20260511 line 430 已被 win-1447-0ce8 註記 §13.5 reference TODO |
| SPOT | DD_SPOT_20260429.html | v12.1 | 87.8 | in_progress | win-20260516-1610-9762 | – |
| STM | DD_STM_20260504.html | v12.2 | 70.3 | pending | – | under-80kb (70.3kb) |
| STRL | DD_STRL_20260505.html | v12.2 | 79.9 | pending | – | under-80kb (79.9kb) |
| STX | DD_STX_20260429.html | v12.1 | 63.1 | pending | – | under-80kb (63.1kb) |
| TDY | DD_TDY_20260427.html | v12.0 | 41.6 | pending | – | under-80kb (41.6kb) |
| TER | DD_TER_20260504.html | v12.2 | 67.4 | pending | – | under-80kb (67.4kb) |
| TPR | DD_TPR_20260427.html | v12.1 | 69.8 | pending | – | under-80kb (69.8kb) |
| TSLA | DD_TSLA_20260418.html | v12.0 | 75.4 | pending | – | under-80kb (75.4kb) |
| TSM | DD_TSM_20260323.html | pre-v12 | 48.4 | pending | – | pre-v12-heavy; under-80kb (48.4kb) |
| TXN | DD_TXN_20260504.html | v12.2 | 78.7 | pending | – | under-80kb (78.7kb) |
| UBER | DD_UBER_20260418.html | v12.0 | 63.1 | pending | – | under-80kb (63.1kb) |
| V | DD_V_20260516.html | v12.3 | 98.5 | done | win-20260516-1358-e570 | dca-cascade clean (1 DCA, 0 broken anchor); dca 51.9kb |
| VIK | DD_VIK_20260515.html | v12.3 | 73.8 | done | win-20260516-1358-e570 | under-80kb (73.8kb); dca-cascade 3 DCAs, 1 anchor fix in 20260515 (QC-29 4 情境 → v12.3 base+bear 2 情境); dca-under-50kb (48.96kb) pre-existing |
| VRT | DD_VRT_20260425.html | v12.0 | 96.7 | in_progress | win-20260516-1558-ceca | – |
| WMT | DD_WMT_20260427.html | v12.1 | 56.2 | pending | – | under-80kb (56.2kb) |
