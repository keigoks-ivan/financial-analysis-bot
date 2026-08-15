> ⚠ STALE（2026-08-15）：本檔為 hub／子頁組裝前研究素材，opus critic 修正未回填；數字以已發布的 docs/backtest/country_scan/us*.html 為準。

# 美股國家掃描 Phase 0c —— 站內 DD 存量對帳表

**產出日期**：2026-08-15（複審窗基準日）　**掃描範圍**：`docs/dd/DD_*.html` 全部 649 份檔案

**用途**：本表是九鏡頭 writer 的直接素材，writer 不必自行掃 `docs/dd/`；同時是 hub §11「DD 對帳與複審隊列」的來源。裁決欄位一律逐字抄 dd-meta JSON，不改寫不總結。

## 0. 總計統計

- **站內 DD 檔案總數**：649 份（含歷史版本、含非美股）
- **美股掛牌唯一標的**（同 ticker 取最新日期為權威，已排除 .TW/.TWO/.T/.KL/.MC/.AS/.HK 後綴或純數字台股代號）：**229 檔**
  - 歸入九鏡頭母體：**203 檔**
  - 外國公司 ADR／外國主要上市旗標（`foreign_adr`，保留在表中供引用但不入九鏡頭母體）：**26 檔**
- **非美股掛牌**（台/日/馬，判準即排除，不列入本表）：22 檔唯一標的（48 份檔案），不展開
- **複審窗**（≤90 天 = 窗內；以 2026-08-15 為基準日）：窗內 **216** 檔／逾窗 **13** 檔（窗內比例 94.3%）

### 九鏡頭分布

| 鏡頭 | 檔數 | 窗內（≤90天） | 逾窗 |
|---|---|---|---|
| 鏡頭一・巨型平台與 AI 資本週期 | 15 | 14 | 1 |
| 鏡頭二・半導體與 AI 基礎設施 | 56 | 52 | 4 |
| 鏡頭三・軟體與訂閱經濟 | 18 | 17 | 1 |
| 鏡頭四・複利機器 | 10 | 10 | 0 |
| 鏡頭五・醫療保健 | 16 | 16 | 0 |
| 鏡頭六・金融 | 13 | 13 | 0 |
| 鏡頭七・消費特許經營 | 31 | 29 | 2 |
| 鏡頭八・能源電力與再工業化 | 35 | 31 | 4 |
| 鏡頭九・中小型隱形冠軍 | 9 | 9 | 0 |
| **鏡頭外／foreign_adr（不入母體，僅參考）** | 26 | — | — |

## 1. 判準與方法說明

- **美股判準**：檔名 ticker 無 `.TW`／`TW`／`.TWO`／純數字台股代號／`T` 後綴（日股）／`KL` 後綴（馬股）＝美股掛牌。純數字（如 2330、2454）視同台股本地代號排除，不需額外 `.TW`。
- **同 ticker 多版本**：取檔名日期最新者為權威，逐字抄其 dd-meta；舊版列於「歷史版本」欄（僅計數，不展開）。
- **foreign_adr 旗標**：檔名無上述後綴、但公司主要業務/主要上市地在美國以外（如 TSM、ASML、荷比法瑞星等地公司之 ADR 或美股次要掛牌），保留在表中供引用，但**不計入九鏡頭母體**（呼應 `_PLAN.md` §2 母體排除規則）。判定依 dd-meta `oneliner`／HTML `<title>` 內公司全名與掛牌地線索逐檔查證，非純字串規則，可能有邊界案例（見文末「拿不準清單」）。
- **裁決欄**：v13 起有獨立 `verdict`（短碼）+ `dca_verdict`/`dca_role`/`moat_trend` 欄；v12.x 舊檔僅有 `signal`（短碼）+ `verdict`（長句，內嵌方向與觸發價），無 dca_* 欄——標記為 **legacy**，`dca_verdict`/`dca_role`/`moat_trend` 三欄留空以示不存在，不得杜撰。
- **複審窗**：`days_since` = 2026-08-15 − 權威檔日期，取自檔名日期（非 INDEX.md，依 repo CLAUDE.md 教訓）。≤90 天記窗內，>90 天記逾窗。
- **九鏡頭歸類**：依 `_PLAN.md` §4 定義與典型獵場逐檔判斷「最能解釋其長期報酬來源」的鏡頭；重疊名字只在該鏡頭收編一次，他頁應標切線（切線文字不在本表展開，由 writer 依 §4 切線規則自行處理）。部分名字不在 plan 原始獵場清單內（如网路市集平台、汽車供應鏈、航太製造），本表以最佳判斷歸類並在「拿不準清單」註記，供 writer／critic 複核。

## 鏡頭一・巨型平台與 AI 資本週期（15 檔）

> **判斷call 註記**：判斷call：網路市集/訂閱平台（ABNB/BKNG/UBER/DASH/EBAY/SPOT/MELI）歸屬鏡頭一而非鏡頭七消費特許經營或鏡頭三軟體，非 plan 原始獵場名單，屬本表擴充判斷；ORCL 歸鏡頭一因近期 thesis 主軸已轉為 OCI 雲端資本週期/AI capex，非傳統企業軟體訂閱敘事，亦屬擴充判斷

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EBAY | EBAY 深度盡職調查｜DD v12.3｜2026-05-16 | `DD_EBAY_20260516.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260516 | 91 | 逾窗 | B |  |  |  | 0 |
| DASH | DASH 深度研究報告 v12.3｜2026-05-18 | `DD_DASH_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| ABNB | DD｜Airbnb (ABNB) 個股深度報告 — 2026-07-03 | `DD_ABNB_20260703.html` | v14.4 | 20260703 | 43 | 窗內 | B | 進場 | 條件式核心持倉 | → | 1 |
| ORCL | DD｜Oracle (ORCL) v14.3 個股深度報告 2026-07-03 | `DD_ORCL_20260703.html` | v14.3 | 20260703 | 43 | 窗內 | B | 觀望 | 條件式衛星持倉 | → | 3 |
| TSLA | DD_TSLA_20260705 ｜ Tesla, Inc. 深度研究報告 v14.5 | `DD_TSLA_20260705.html` | v14.5 | 20260705 | 41 | 窗內 | B | 迴避 | 不持有/迴避 | ↓ | 2 |
| SPOT | DD SPOT｜Spotify Technology — 2026-07-11（v14.12） | `DD_SPOT_20260711.html` | v14.12 | 20260711 | 35 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| NFLX | DD_NFLX_20260717 — Netflix 個股深度報告 v14.12 | `DD_NFLX_20260717.html` | v14.12 | 20260717 | 29 | 窗內 | B | 進場 | 衛星 | → | 7 |
| GOOGL | DD · GOOGL 深度報告 v14.12 · 2026-07-23 | `DD_GOOGL_20260723.html` | v14.12 | 20260723 | 23 | 窗內 | A | 進場 | 核心 | → | 9 |
| MSFT | DD — MSFT Microsoft Corporation｜2026-07-30｜v14.12 | `DD_MSFT_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 進場 | 核心 | → | 9 |
| META | DD｜META Meta Platforms — 2026-07-30（統一裁決：進場）v14.12 | `DD_META_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 進場 | 核心 | → | 6 |
| AAPL | DD Report — AAPL (Apple Inc.) v14.12 ｜ 2026-07-31 | `DD_AAPL_20260731.html` | v14.12 | 20260731 | 15 | 窗內 | B | 觀望 | 追蹤 | → | 3 |
| AMZN | DD_AMZN_20260731 — Amazon.com 買側深度研究 v14.12 | `DD_AMZN_20260731.html` | v14.12 | 20260731 | 15 | 窗內 | A | 進場 | 核心 | → | 8 |
| BKNG | DD — Booking Holdings (BKNG) — 2026-08-05 | `DD_BKNG_20260805.html` | v14.12 | 20260805 | 10 | 窗內 | B | 進場 | 衛星 | → | 1 |
| MELI | MELI 深度研究與投資裁決 ｜ 2026-08-07 | `DD_MELI_20260807.html` | v15.0 | 20260807 | 8 | 窗內 | B | 觀望 | 追蹤 | → | 3 |
| UBER | DD UBER Uber Technologies — 2026-08-08（統一裁決：進場） | `DD_UBER_20260808.html` | v15.0 | 20260808 | 7 | 窗內 | B | 進場 | 衛星 | → | 3 |

## 鏡頭二・半導體與 AI 基礎設施（56 檔）

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CDNS | DD｜CDNS Cadence Design Systems｜2026-05-04 | `DD_CDNS_20260504.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260504 | 103 | 逾窗 | A |  |  |  | 0 |
| FN | DD｜Fabrinet (FN) — 2026-05-05 | `DD_FN_20260505.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260505 | 102 | 逾窗 | B |  |  |  | 2 |
| CAMT | DD｜CAMT｜2026-05-14 | `DD_CAMT_20260514.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260514 | 93 | 逾窗 | B |  |  |  | 2 |
| NVMI | NVMI Nova Ltd — DD v12.3｜2026-05-15 | `DD_NVMI_20260515.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260515 | 92 | 逾窗 | B |  |  |  | 1 |
| WDC | WDC｜Western Digital｜深度研究 DD｜v12.3｜2026-05-18 | `DD_WDC_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| FLEX | DD｜FLEX (Flex Ltd.)｜2026-05-18 | `DD_FLEX_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| NTAP | NTAP NetApp 深度研究 DD v12.3 — 2026-05-18 | `DD_NTAP_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| KEYS | DD｜KEYS · Keysight Technologies｜2026-05-21 | `DD_KEYS_20260521.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260521 | 86 | 窗內 | A |  |  |  | 5 |
| ALAB | ALAB｜Astera Labs｜DD v12.4｜2026-05-22 | `DD_ALAB_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | B |  |  |  | 2 |
| TEL | DD｜TEL TE Connectivity｜2026-05-22 | `DD_TEL_20260522.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | A |  |  |  | 0 |
| CRWV | DD｜CRWV CoreWeave, Inc. — v12.4 (2026-05-23) | `DD_CRWV_20260523.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260523 | 84 | 窗內 | B |  |  |  | 0 |
| ARW | Arrow Electronics (ARW) — DD v12.4 ｜ 2026-05-23 | `DD_ARW_20260523.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260523 | 84 | 窗內 | B |  |  |  | 0 |
| AMKR | AMKR Amkor Technology — DD v12.4（2026-05-24） | `DD_AMKR_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| MTSI | DD MTSI v12.4 — MACOM Technology Solutions（2026-05-24） | `DD_MTSI_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| NVTS | NVTS Navitas Semiconductor — DD v12.4（2026-05-24） | `DD_NVTS_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | X |  |  |  | 0 |
| AXTI | DD AXTI v12.4 — AXT, Inc.（2026-05-24） | `DD_AXTI_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| VICR | VICR｜Vicor Corporation 深度報告 DD v12.4｜2026-05-24 | `DD_VICR_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| SANM | DD_SANM_20260524 — Sanmina Corp 深度研究 (v12.4) | `DD_SANM_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| NVT | NVT nVent Electric — DD v12.4（2026-05-24） | `DD_NVT_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| HPE | DD｜HPE Hewlett Packard Enterprise — v12.4（2026-06-02） | `DD_HPE_20260602.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260602 | 74 | 窗內 | B |  |  |  | 1 |
| CIEN | DD · CIEN · Ciena · v12.7 · 2026-06-12 | `DD_CIEN_20260612.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260612 | 64 | 窗內 | B |  |  |  | 2 |
| ADI | DD｜Analog Devices (ADI) — v12.7 深度研究報告 2026-06-20 | `DD_ADI_20260620.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260620 | 56 | 窗內 | B |  |  |  | 2 |
| ON | DD｜ON Semiconductor (ON) — v12.7 深度研究報告 2026-06-20 | `DD_ON_20260620.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260620 | 56 | 窗內 | B |  |  |  | 2 |
| RMBS | RMBS 深度研究報告 DD v12.7 — 2026-06-20 | `DD_RMBS_20260620.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260620 | 56 | 窗內 | B |  |  |  | 1 |
| AVGO | DD AVGO Broadcom — 2026-06-23（統一裁決：進場） | `DD_AVGO_20260623.html` | v14.2 | 20260623 | 53 | 窗內 | A | 進場 | 核心持倉 | → | 9 |
| MRVL | DD — Marvell Technology (MRVL) v14.2｜2026-06-23 | `DD_MRVL_20260623.html` | v14.2 | 20260623 | 53 | 窗內 | B | 觀望 | 條件式核心持倉 | → | 7 |
| CRDO | DD · CRDO 深度報告 v14.2 · 2026-06-23 | `DD_CRDO_20260623.html` | v14.2 | 20260623 | 53 | 窗內 | B | 觀望 | 條件式核心持倉 | → | 6 |
| NVDA | DD — NVIDIA (NVDA) v14.2｜2026-06-24 | `DD_NVDA_20260624.html` | v14.2 | 20260624 | 52 | 窗內 | A+ | 進場 | 核心持倉 | → | 7 |
| AMAT | DD AMAT｜Applied Materials v14.2 深度報告（2026-06-26） | `DD_AMAT_20260626.html` | v14.2 | 20260626 | 50 | 窗內 | B | 觀望 | 條件式核心持倉 | → | 4 |
| TER | DD｜Teradyne (TER) v14.2 — 2026-06-26 | `DD_TER_20260626.html` | v14.2 | 20260626 | 50 | 窗內 | B | 觀望 | 條件式衛星持倉 | → | 6 |
| ONTO | DD ONTO｜Onto Innovation v14.2 深度報告（2026-06-26） | `DD_ONTO_20260626.html` | v14.2 | 20260626 | 50 | 窗內 | B | 觀望 | 條件式衛星持倉 | ↑ | 4 |
| COHR | COHR 深度研究 DD — Coherent Corp.（2026-06-27） | `DD_COHR_20260627.html` | v14.2 | 20260627 | 49 | 窗內 | B | 進場 | 條件式核心持倉 | ↑ | 4 |
| FORM | DD｜FORM｜2026-06-29 | `DD_FORM_20260629.html` | v14.2 | 20260629 | 47 | 窗內 | B | 觀望 | 條件式衛星持倉 | → | 1 |
| JBL | DD｜Jabil (JBL) v14.3 個股深度報告 2026-07-03 | `DD_JBL_20260703.html` | v14.3 | 20260703 | 43 | 窗內 | B | 觀望 | 條件式衛星持倉 | → | 3 |
| MU | DD｜Micron Technology (MU) v14.5 — 2026-07-05 | `DD_MU_20260705.html` | v14.5 | 20260705 | 41 | 窗內 | B | 觀望 | 條件式衛星持倉 | → | 8 |
| CSCO | CSCO ｜ Cisco Systems ｜ 買側 DD v14.5 ｜ 2026-07-06 | `DD_CSCO_20260706.html` | v14.5 | 20260706 | 40 | 窗內 | B | 觀望 | 條件式核心持倉 | → | 1 |
| VRT | DD VRT — Vertiv Holdings ｜ 2026-07-10 ｜ v14.11 | `DD_VRT_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 進場 | 衛星 | → | 6 |
| GFS | DD GFS — GlobalFoundries（2026-07-10） | `DD_GFS_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 觀望 | 衛星 | → | 1 |
| DELL | DD｜Dell Technologies (DELL) v14.11 — 2026-07-10 | `DD_DELL_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 觀望 | 衛星 | → | 4 |
| CLS | DD｜Celestica (CLS)｜v14.12｜2026-07-11 | `DD_CLS_20260711.html` | v14.12 | 20260711 | 35 | 窗內 | B | 觀望 | 追蹤 | → | 3 |
| TXN | DD TXN — Texas Instruments 深度研究（v14.12）｜2026-07-23 | `DD_TXN_20260723.html` | v14.12 | 20260723 | 23 | 窗內 | A | 進場 | 核心 | ↑ | 3 |
| INTC | DD · INTC · Intel Corporation · 2026-07-24 · v14.12 | `DD_INTC_20260724.html` | v14.12 | 20260724 | 22 | 窗內 | 觀望 | 觀望 | 追蹤 | → | 2 |
| KLAC | DD｜KLAC KLA Corporation｜2026-07-29｜v14.12 | `DD_KLAC_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | B | 觀望 | 追蹤 | ↑ | 5 |
| NXPI | DD｜NXP Semiconductors (NXPI) — v14.12 深度研究報告 2026-07-29 | `DD_NXPI_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | B | 進場 | 衛星 | → | 4 |
| STX | DD — STX Seagate Technology Holdings｜2026-07-29｜v14.12 | `DD_STX_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | B | 觀望 | 追蹤 | → | 7 |
| GLW | DD｜GLW Corning Incorporated｜2026-07-29｜v14.12 | `DD_GLW_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | B | 觀望 | 追蹤 | → | 4 |
| LRCX | DD — Lam Research (LRCX) — 2026-07-30 — v14.12 | `DD_LRCX_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 進場 | 衛星 | ↑ | 6 |
| QCOM | DD_QCOM_20260730 — Qualcomm 個股深度研究（v14.12） | `DD_QCOM_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 進場 | 衛星 | → | 2 |
| ARM | ARM 深度研究 DD v14.12 · 2026-07-30 | `DD_ARM_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 觀望 | 追蹤 | → | 2 |
| APH | DD · Amphenol (APH) · v14.12 · 2026-07-30 | `DD_APH_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | A | 進場 | 核心 | ↑ | 8 |
| MPWR | DD · MPWR Monolithic Power Systems · v14.12 · 2026-07-31 | `DD_MPWR_20260731.html` | v14.12 | 20260731 | 15 | 窗內 | A | 進場 | 衛星 | → | 3 |
| AMD | AMD 深度研究 DD v14.12 · 2026-08-05 | `DD_AMD_20260805.html` | v14.12 | 20260805 | 10 | 窗內 | B | 進場 | 衛星 | → | 8 |
| ANET | DD｜ANET Arista Networks｜2026-08-05｜v14.12 | `DD_ANET_20260805.html` | v14.12 | 20260805 | 10 | 窗內 | B | 觀望 | 追蹤 | → | 6 |
| KLIC | KLIC 深度研究報告 — Kulicke &amp; Soffa Industries（DD Schema v15.0） | `DD_KLIC_20260806.html` | v15.0 | 20260806 | 9 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| SNDK | DD SNDK SanDisk — 2026-08-06（統一裁決：觀望） | `DD_SNDK_20260806.html` | v15.0 | 20260806 | 9 | 窗內 | C | 觀望 | 追蹤 | → | 4 |
| LITE | LITE 深度研究 DD — Lumentum Holdings（2026-08-12） | `DD_LITE_20260812.html` | v15.0 | 20260812 | 3 | 窗內 | B | 觀望 | 候選/追蹤池 | → | 6 |

## 鏡頭三・軟體與訂閱經濟（18 檔）

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DDOG | DD｜DDOG Datadog 2026-05-16 | `DD_DDOG_20260516.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260516 | 91 | 逾窗 | B |  |  |  | 0 |
| HUBS | DD｜HUBS HubSpot Inc｜2026-05-22｜v12.4 | `DD_HUBS_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | B |  |  |  | 0 |
| WDAY | DD｜WDAY Workday｜2026-05-22｜v12.4 | `DD_WDAY_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | B |  |  |  | 0 |
| TWLO | DD｜TWLO Twilio Inc｜v12.4 ｜ 2026-05-22 | `DD_TWLO_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | B |  |  |  | 0 |
| MDB | DD｜MDB MongoDB｜2026-05-24｜v12.4 | `DD_MDB_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| VEEV | DD｜Veeva Systems (VEEV) v12.7 — 2026-06-15 | `DD_VEEV_20260615.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260615 | 61 | 窗內 | B |  |  |  | 0 |
| PANW | PANW 深度研究 DD｜v14.2｜2026-06-29 | `DD_PANW_20260629.html` | v14.2 | 20260629 | 47 | 窗內 | B | 觀望 | 條件式核心持倉 | ↑ | 2 |
| ADBE | ADBE 深度研究 DD｜v14.4｜2026-07-03 | `DD_ADBE_20260703.html` | v14.4 | 20260703 | 43 | 窗內 | B | 觀望 | 條件式核心持倉 | ↓ | 1 |
| CRWD | DD｜CrowdStrike (CRWD) — v14.4 深度研究報告（含決策層） | `DD_CRWD_20260703.html` | v14.4 | 20260703 | 43 | 窗內 | B | 觀望 | 條件式核心持倉 | ↑ | 5 |
| CRM | DD｜Salesforce (CRM) 個股深度研究 + 決策層｜2026-07-05｜v14.5 | `DD_CRM_20260705.html` | v14.5 | 20260705 | 41 | 窗內 | B | 進場 | 條件式衛星持倉 | → | 3 |
| SNOW | DD — Snowflake (SNOW) 2026-07-05 | `DD_SNOW_20260705.html` | v14.5 | 20260705 | 41 | 窗內 | 觀望（thesis 全面確認、前次加碼觸發器已發火、moat A→、runway 🟢，但 $260 貼近 ATH、non-GAAP fwd PE ~97x、5Y Base IRR ~2.6%/yr、AR 1.6 無不對稱；估值 🟠 已把 AI 拐點 price in，等回檔重進） | 觀望 | 條件式衛星持倉 | → | 1 |
| APP | DD — AppLovin（APP）v14.11 深度報告（2026-07-10） | `DD_APP_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 進場 | 衛星 | → | 2 |
| NOW | DD — ServiceNow (NOW) v14.12 — 2026-07-23 | `DD_NOW_20260723.html` | v14.12 | 20260723 | 23 | 窗內 | B | 進場 | 核心 | → | 2 |
| IBM | DD — IBM 國際商業機器 v14.12（隨附 Q2 2026 逐字稿 read-through） | `DD_IBM_20260723.html` | v14.12 | 20260723 | 23 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| FTNT | DD · FTNT · Fortinet, Inc. · 2026-07-30 · v14.12 | `DD_FTNT_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 觀望 | 追蹤 | → | 2 |
| PLTR | PLTR 深度研究報告 DD v15.0 — 2026-08-05 | `DD_PLTR_20260805.html` | v15.0 | 20260805 | 10 | 窗內 | B | 進場 | 衛星 | → | 4 |
| NET | DD NET Cloudflare — 2026-08-07（統一裁決：觀望） | `DD_NET_20260807.html` | v15.0 | 20260807 | 8 | 窗內 | B | 觀望 | 追蹤 | ↑ | 5 |
| SHOP | SHOP 深度研究與投資裁決 ｜ 2026-08-08 | `DD_SHOP_20260808.html` | v15.0 | 20260808 | 7 | 窗內 | B | 觀望 | 追蹤 | ↑ | 0 |

## 鏡頭四・複利機器（10 檔）

> **判斷call 註記**：V/MA 依 plan §4 判斷call 歸鏡頭四（網路效應複利機），鏡頭六財務章節須標切線；GE/HWM/TDY 為航太售後市場複利股；CSX 為鐵路護城河複利股

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DE | DD｜DE Deere & Company｜v12.4 ｜ 2026-05-22 | `DD_DE_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | A |  |  |  | 0 |
| MSI | Motorola Solutions (MSI) — Deep Due Diligence v12.4 — 2026-05-24 | `DD_MSI_20260524.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| MA | DD｜Mastercard (MA) v14.4 個股深度報告 2026-07-03 | `DD_MA_20260703.html` | v14.4 | 20260703 | 43 | 窗內 | A | 進場 | 核心持倉 | ↑ | 1 |
| ROP | DD ROP Roper Technologies v14.11 — 2026-07-10 | `DD_ROP_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 進場 | 核心 | → | 1 |
| HWM | DD — HWM Howmet Aerospace v14.11（2026-07-10） | `DD_HWM_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 觀望 | 核心 | ↑ | 2 |
| GE | DD｜GE — GE Aerospace（v14.12）2026-07-17 | `DD_GE_20260717.html` | v14.12 | 20260717 | 29 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| TDY | DD TDY Teledyne Technologies — v14.12（2026-07-23，隨附 Q2 2026 逐字稿 read-through） | `DD_TDY_20260723.html` | v14.12 | 20260723 | 23 | 窗內 | B | 觀望 | 追蹤 | → | 2 |
| CSX | DD · CSX 深度報告 v14.12 · 2026-07-23 | `DD_CSX_20260723.html` | v14.12 | 20260723 | 23 | 窗內 | B | 觀望 | 追蹤 | → | 2 |
| V | DD｜Visa Inc. (V) — 2026-07-29 · v14.12 | `DD_V_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | A | 進場 | 核心 | ↑ | 1 |
| FTV | Fortive Corporation (FTV) — Deep DD v14.12 — 2026-07-30 | `DD_FTV_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 觀望 | 追蹤 | → | 1 |

## 鏡頭五・醫療保健（16 檔）

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MDT | DD｜MDT Medtronic plc｜2026-05-18 | `DD_MDT_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| CVS | DD｜CVS Health (CVS)｜v12.3｜2026-05-18 | `DD_CVS_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| OSCR | DD｜Oscar Health（OSCR）｜v12.3｜2026-05-18 | `DD_OSCR_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | C |  |  |  | 0 |
| ABBV | AbbVie (ABBV) DD v12.4 — 2026-05-25 | `DD_ABBV_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| UNH | UNH｜UnitedHealth Group — 買側 DD｜2026-05-25 | `DD_UNH_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| MRK | Merck (MRK) DD v12.4 — 2026-05-25 | `DD_MRK_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| GILD | DD｜GILD（Gilead Sciences）｜2026-05-25｜v12.4 | `DD_GILD_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | A+ |  |  |  | 0 |
| MCK | MCK｜McKesson Corporation — 買側 DD｜2026-05-25 | `DD_MCK_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | A |  |  |  | 0 |
| COR | DD｜COR Cencora｜2026-05-25 v12.4 | `DD_COR_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| CAH | DD｜CAH Cardinal Health｜2026-05-25 v12.4 | `DD_CAH_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| TMDX | DD｜TMDX（TransMedics Group）｜2026-05-25｜v12.4 | `DD_TMDX_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| EHC | Encompass Health (EHC) DD v12.4 — 2026-05-25 | `DD_EHC_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| BSX | DD｜Boston Scientific (BSX) v14.11 個股深度報告 2026-07-10 | `DD_BSX_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | C | 迴避 | 不持有 | ↓ | 5 |
| JNJ | DD｜JNJ Johnson &amp; Johnson｜2026-07-16｜v14.12 | `DD_JNJ_20260716.html` | v14.12 | 20260716 | 30 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| ISRG | DD_ISRG_20260717 — Intuitive Surgical 深度研究（v14.12） | `DD_ISRG_20260717.html` | v14.12 | 20260717 | 29 | 窗內 | B | 觀望 | 追蹤 | → | 4 |
| LLY | DD — Eli Lilly (LLY) v15.0｜2026-08-06 | `DD_LLY_20260806.html` | v15.0 | 20260806 | 9 | 窗內 | A+ | 進場 | 核心 | → | 8 |

## 鏡頭六・金融（13 檔）

> **判斷call 註記**：FICO 歸財務（信用評分基礎設施，非軟體）；GLXY 前開曼籍 2025 傳聞已遷至 Delaware 便於 Nasdaq/指數資格，本表暫列一般美股不掛 foreign_adr 但保留註記

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| COIN | COIN｜Coinbase Global｜v12.4 DD｜2026-05-25 | `DD_COIN_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| GLXY | GLXY｜Galaxy Digital Inc.｜v12.4 DD｜2026-05-25 | `DD_GLXY_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| GS | DD · The Goldman Sachs Group (GS) · 2026-06-15 | `DD_GS_20260615.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260615 | 61 | 窗內 | B |  |  |  | 1 |
| FICO | DD — Fair Isaac (FICO) — 2026-07-10 | `DD_FICO_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 進場 | 核心 | → | 2 |
| PYPL | DD PYPL — PayPal Holdings｜v14.11 深度研究報告 | `DD_PYPL_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | C | 觀望 | 追蹤 | → | 1 |
| SEZL | DD SEZL — Sezzle Inc.（v14.11，2026-07-10） | `DD_SEZL_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 觀望 | 核心 | → | 1 |
| HOOD | DD｜HOOD Robinhood Markets｜2026-07-14｜v14.12 | `DD_HOOD_20260714.html` | v14.12 | 20260714 | 32 | 窗內 | B | 觀望 | 追蹤 | ↑ | 1 |
| MS | DD — Morgan Stanley (MS) — 2026-07-16 | `DD_MS_20260716.html` | v14.12 | 20260716 | 30 | 窗內 | B | 觀望 | 核心 | ↑ | 2 |
| BLK | DD_BLK_20260716 — BlackRock 深度研究報告 v14.12 | `DD_BLK_20260716.html` | v14.12 | 20260716 | 30 | 窗內 | A | 進場 | 核心 | → | 0 |
| COF | Capital One (COF) 深度研究 DD · v14.12 · 2026-07-22 | `DD_COF_20260722.html` | v14.12 | 20260722 | 24 | 窗內 | B | 進場 | 衛星 | → | 2 |
| IBKR | Interactive Brokers (IBKR) 深度研究 DD · v14.12 · 2026-07-22 | `DD_IBKR_20260722.html` | v14.12 | 20260722 | 24 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| BX | DD — Blackstone (BX) v14.12 — 2026-07-24 | `DD_BX_20260724.html` | v14.12 | 20260724 | 22 | 窗內 | B | 進場 | 核心 | → | 0 |
| SOFI | DD｜SoFi Technologies (SOFI) — v14.12｜2026-07-30 | `DD_SOFI_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 觀望 | 追蹤 | → | 1 |

## 鏡頭七・消費特許經營（31 檔）

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LULU | LULU lululemon athletica — 買側 DD v12.3 — 2026-05-16 | `DD_LULU_20260516.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260516 | 91 | 逾窗 | B |  |  |  | 0 |
| DIS | DIS｜The Walt Disney Company｜DD v12.3 Inception｜2026-05-16 | `DD_DIS_20260516.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260516 | 91 | 逾窗 | B |  |  |  | 0 |
| LYV | DD｜LYV Live Nation Entertainment｜2026-05-18 | `DD_LYV_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| MNST | MNST Monster Beverage ｜ DD v12.3 ｜ 2026-05-18 | `DD_MNST_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| CELH | CELH Celsius Holdings ｜ DD v12.3 ｜ 2026-05-18 | `DD_CELH_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| H | DD｜H Hyatt Hotels Corporation｜v12.3 ｜ 2026-05-20 | `DD_H_20260520.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260520 | 87 | 窗內 | B |  |  |  | 0 |
| HD | HD｜The Home Depot — v12.4 DD + Q1 FY26 重評估 (2026-05-21) | `DD_HD_20260521.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260521 | 86 | 窗內 | B |  |  |  | 1 |
| LOW | LOW｜Lowe's — v12.4 DD + Q1 FY26 重評估 (2026-05-21) | `DD_LOW_20260521.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260521 | 86 | 窗內 | B |  |  |  | 1 |
| TJX | TJX · The TJX Companies — 買側深度研究（DD v12.4）2026-05-21 | `DD_TJX_20260521.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260521 | 86 | 窗內 | B |  |  |  | 0 |
| WMT | WMT｜Walmart Inc. - 買側深度研究報告 v12.4 | `DD_WMT_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | B |  |  |  | 1 |
| ROST | DD｜Ross Stores (ROST) — 2026-05-22 | `DD_ROST_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | A |  |  |  | 0 |
| LEVI | DD｜LEVI Levi Strauss & Co.｜2026-05-22 | `DD_LEVI_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | B |  |  |  | 0 |
| RL | RL｜Ralph Lauren｜深度研究 DD｜v12.4｜2026-05-22 | `DD_RL_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | B |  |  |  | 1 |
| URBN | URBN｜Urban Outfitters Inc｜深度研究 DD｜v12.4｜2026-05-22 | `DD_URBN_20260522.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260522 | 85 | 窗內 | B |  |  |  | 0 |
| M | DD｜M Macy's, Inc. — v12.7（2026-06-15） | `DD_M_20260615.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260615 | 61 | 窗內 | C |  |  |  | 0 |
| CHWY | DD｜CHWY Chewy, Inc. — v12.7（2026-06-15） | `DD_CHWY_20260615.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260615 | 61 | 窗內 | X |  |  |  | 0 |
| KR | DD｜KR The Kroger Co. — 2026-06-19 | `DD_KR_20260619.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260619 | 57 | 窗內 | C |  |  |  | 0 |
| SN | DD · SN · SharkNinja · v12.7 · 2026-06-19 | `DD_SN_20260619.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260619 | 57 | 窗內 | B |  |  |  | 0 |
| NKE | DD · NKE 耐吉 · 2026-07-01 · v14.2 統一裁決 | `DD_NKE_20260701.html` | v14.2 | 20260701 | 45 | 窗內 | B 觀望 | 觀望 | 條件式核心持倉 | → | 1 |
| STZ | DD · STZ Constellation Brands · 2026-07-01 · v14.2 統一裁決 | `DD_STZ_20260701.html` | v14.2 | 20260701 | 45 | 窗內 | B 觀望 | 觀望 | 條件式核心持倉 | → | 0 |
| HLT | HLT 深度研究 DD｜v14.4｜2026-07-03 | `DD_HLT_20260703.html` | v14.4 | 20260703 | 43 | 窗內 | B | 觀望 | 條件式核心持倉 | ↑ | 1 |
| DECK | DD · DECK Deckers · 2026-07-06 · v14.5 統一裁決 | `DD_DECK_20260706.html` | v14.5 | 20260706 | 40 | 窗內 | B 進場·條件式（衛星：逢回分批） | 進場 | 衛星持倉 | → | 1 |
| MAR | DD — Marriott International (MAR) v14.11 · 2026-07-10 | `DD_MAR_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 觀望 | 核心 | → | 1 |
| COST | Costco Wholesale (COST) 深度研究 ｜ 2026-07-11（DD Schema v14.12） | `DD_COST_20260711.html` | v14.12 | 20260711 | 35 | 窗內 | B | 觀望 | 追蹤 | ↑ | 1 |
| EAT | DD｜EAT Brinker International｜2026-07-11｜v14.12 | `DD_EAT_20260711.html` | v14.12 | 20260711 | 35 | 窗內 | B | 進場 | 衛星 | → | 1 |
| KO | DD｜The Coca-Cola Company (KO) — 2026-07-29 · v14.12 | `DD_KO_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | B | 觀望 | 追蹤 | ↑ | 0 |
| RCL | DD｜Royal Caribbean Cruises (RCL) — 2026-07-29 · v14.12 | `DD_RCL_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | B | 觀望 | 追蹤 | ↑ | 2 |
| CMG | DD｜Chipotle Mexican Grill (CMG) — 買側深度研究 v14.12 — 2026-07-30 | `DD_CMG_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | C | 觀望 | 追蹤 | → | 1 |
| SBUX | DD｜Starbucks (SBUX) — 2026-07-30 · v14.12 | `DD_SBUX_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 進場 | 衛星 | → | 2 |
| GRMN | DD GRMN Garmin Ltd. — 買側標的研究 v14.12（2026-07-30） | `DD_GRMN_20260730.html` | v14.12 | 20260730 | 16 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| TPR | TPR｜Tapestry, Inc. 深度研究報告 v15.0（2026-08-06） | `DD_TPR_20260806.html` | v15.0 | 20260806 | 9 | 窗內 | B | 觀望 | 衛星 | ↑ | 2 |

## 鏡頭八・能源電力與再工業化（35 檔）

> **判斷call 註記**：汽車供應鏈(MGA/LEA/BWA/F/GM/ALV)、航太製造(RKLB/SPCX)非 plan 原始獵場，歸類理由=再工業化/國防太空製造

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BWXT | DD_BWXT_20260505 — BWX Technologies 深度研究 v12.3 | `DD_BWXT_20260505.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260505 | 102 | 逾窗 | B |  |  |  | 1 |
| STRL | DD_STRL_20260505 — Sterling Infrastructure 深度研究 v12.3 | `DD_STRL_20260505.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260505 | 102 | 逾窗 | B |  |  |  | 0 |
| ETN | DD｜ETN Eaton Corporation｜2026-05-06｜v12.3 | `DD_ETN_20260506.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260506 | 101 | 逾窗 | B |  |  |  | 4 |
| FIX | DD｜FIX Comfort Systems USA 2026-05-16 | `DD_FIX_20260516.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260516 | 91 | 逾窗 | B |  |  |  | 1 |
| PH | PH 深度研究 DD｜2026-05-18｜Parker-Hannifin v12.3 | `DD_PH_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| JCI | JCI Johnson Controls v12.3 Inception DD — Post-Q2 FY26 Data Center 重評 | `DD_JCI_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | A |  |  |  | 0 |
| EME | DD_EME｜EMCOR Group, Inc.｜2026-05-18 | `DD_EME_20260518.html` | v12.2 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| HUBB | DD｜HUBB Hubbell Inc｜v12.3 ｜ 2026-05-18 | `DD_HUBB_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | A |  |  |  | 0 |
| CMI | CMI 深度研究報告 v12.3｜2026-05-18 | `DD_CMI_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| MGA | DD｜MGA Magna International — v12.4 (2026-05-24) | `DD_MGA_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| LEA | DD｜LEA Lear Corporation — v12.4 (2026-05-24) | `DD_LEA_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| BWA | DD｜BorgWarner（BWA）｜2026-05-24｜v12.4 | `DD_BWA_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| F | DD｜F Ford Motor Company — v12.4 (2026-05-24) | `DD_F_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| GM | DD｜GM General Motors — v12.4 (2026-05-24) | `DD_GM_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| ALV | DD｜Autoliv（ALV）｜2026-05-24｜v12.4 | `DD_ALV_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| LEU | DD｜LEU Centrus Energy — 2026-05-25 | `DD_LEU_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| NUE | DD｜NUE Nucor Corporation — 2026-05-25 | `DD_NUE_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| MP | MP Materials — DD v12.4 — 2026-05-25 | `DD_MP_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| TPC | DD｜Tutor Perini (TPC) — v12.4 | `DD_TPC_20260525.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260525 | 82 | 窗內 | B |  |  |  | 0 |
| FSLR | DD｜First Solar (FSLR) — v12.4 深度研究報告 | `DD_FSLR_20260608.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260608 | 68 | 窗內 | B |  |  |  | 0 |
| TLN | DD · TLN · Talen Energy · v12.7 · 2026-06-12 | `DD_TLN_20260612.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260612 | 64 | 窗內 | B |  |  |  | 0 |
| ROK | DD · Rockwell Automation (ROK) · v12.7 · 2026-06-20 | `DD_ROK_20260620.html` | v12.7 _(legacy，無 dca_* 欄)_ | 20260620 | 56 | 窗內 | B |  |  |  | 2 |
| RKLB | DD RKLB Rocket Lab 2026-07-02｜v14.3 統一裁決報告 | `DD_RKLB_20260702.html` | v14.3 | 20260702 | 44 | 窗內 | B | 觀望 | 候選/追蹤池 | ↑ | 2 |
| J | DD — Jacobs Solutions (J) v14.4 深度報告 | `DD_J_20260703.html` | v14.4 | 20260703 | 43 | 窗內 | B | 進場 | 衛星持倉 | → | 1 |
| MOD | DD — Modine Manufacturing (MOD) v14.11 · 2026-07-10 | `DD_MOD_20260710.html` | v14.11 | 20260710 | 36 | 窗內 | B | 進場 | 衛星 | → | 2 |
| MMM | 3M Company (MMM) 深度研究 DD · v14.12 · 2026-07-22 | `DD_MMM_20260722.html` | v14.12 | 20260722 | 24 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| GEV | DD GEV — GE Vernova｜v14.12｜2026-07-23 | `DD_GEV_20260723.html` | v14.12 | 20260723 | 23 | 窗內 | B | 觀望 | 追蹤 | → | 6 |
| URI | DD — URI 聯合租賃 v14.12 | `DD_URI_20260723.html` | v14.12 | 20260723 | 23 | 窗內 | B | 觀望 | 追蹤 | → | 0 |
| HON | HON (Honeywell Technologies) v14.12 DD — 2026-07-24 | `DD_HON_20260724.html` | v14.12 | 20260724 | 22 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| BE | DD — BE Bloom Energy Corporation｜2026-07-29｜v14.12 | `DD_BE_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | B | 進場 | 衛星 | ↑ | 2 |
| CARR | DD｜Carrier Global (CARR) — v14.12 深度研究報告 2026-07-29 | `DD_CARR_20260729.html` | v14.12 | 20260729 | 17 | 窗內 | B | 進場 | 衛星 | → | 0 |
| PWR | DD｜Quanta Services (PWR)｜v14.12｜2026-07-31 | `DD_PWR_20260731.html` | v14.12 | 20260731 | 15 | 窗內 | B | 觀望 | 追蹤 | ↑ | 1 |
| TT | DD — Trane Technologies (TT) v14.12 · 2026-07-31 | `DD_TT_20260731.html` | v14.12 | 20260731 | 15 | 窗內 | A | 進場 | 核心 | → | 2 |
| CAT | DD_CAT_20260805 ｜ Caterpillar v14.12 | `DD_CAT_20260805.html` | v14.12 | 20260805 | 10 | 窗內 | B | 觀望 | 追蹤 | → | 1 |
| SPCX | DD_SPCX_20260805 — Space Exploration Technologies Corp.（v14.12） | `DD_SPCX_20260805.html` | v14.12 | 20260805 | 10 | 窗內 | B | 觀望 | 追蹤 | → | 1 |

## 鏡頭九・中小型隱形冠軍（9 檔）

| Ticker | 公司（來源：DD title） | 權威檔 | schema | 報告日 | 距今天數 | 窗內/逾窗 | verdict/signal | dca_verdict | dca_role | moat_trend | 歷史版本數 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CRS | CRS｜Carpenter Technology｜深度研究 DD｜v12.3｜2026-05-18 | `DD_CRS_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | A |  |  |  | 0 |
| ATI | ATI｜ATI Inc.｜深度研究 DD｜v12.3｜2026-05-18 | `DD_ATI_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| TTMI | DD_TTMI｜TTM Technologies, Inc.｜2026-05-18 | `DD_TTMI_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| CHEF | DD｜CHEF The Chefs' Warehouse｜v12.3 Inception | `DD_CHEF_20260518.html` | v12.3 _(legacy，無 dca_* 欄)_ | 20260518 | 89 | 窗內 | B |  |  |  | 0 |
| MWA | MWA｜Mueller Water Products 深度報告 DD v12.4｜2026-05-24 | `DD_MWA_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | A |  |  |  | 0 |
| PLXS | DD_PLXS_20260524 — Plexus Corp 深度研究 (v12.4) | `DD_PLXS_20260524.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260524 | 83 | 窗內 | B |  |  |  | 0 |
| CW | DD｜Curtiss-Wright (CW) — v12.4 | `DD_CW_20260529.html` | v12.4 _(legacy，無 dca_* 欄)_ | 20260529 | 78 | 窗內 | B |  |  |  | 1 |
| WLDN | WLDN 深度研究 DD｜v14.4｜2026-07-03 | `DD_WLDN_20260703.html` | v14.4 | 20260703 | 43 | 窗內 | A | 進場 | 衛星持倉 | ↑ | 1 |
| GHM | DD — Graham Corporation (GHM) — 2026-07-14 v14.12 | `DD_GHM_20260714.html` | v14.12 | 20260714 | 32 | 窗內 | B | 觀望 | 追蹤 | → | 1 |

## 鏡頭外／foreign_adr 區（不入九鏡頭母體，供引用）

依 `_PLAN.md` §2：外國公司 ADR（如 TSM、ASML、BABA 類）判準＝S&P 1500 成員資格優先，指數外的外國掛牌公司不入母體，但 hub／子頁對帳章可引用站內既有 DD。以下 26 檔逐字抄裁決供引用，**不計入任何鏡頭統計**。

| Ticker | 公司（來源：DD title） | 掛牌地/身分 | 權威檔 | schema | 報告日 | 距今天數 | verdict/signal | dca_verdict | dca_role |
|---|---|---|---|---|---|---|---|---|---|
| GRAB | DD_GRAB_20260505 — Grab Holdings 深度研究 v12.3 | 新加坡/開曼，Grab Holdings，Nasdaq 主要上市（FPI） | `DD_GRAB_20260505.html` | v12.3 | 20260505 | 102 | B |  |  |
| LVMH | LVMH (MC.PA)｜LVMH Moët Hennessy Louis Vuitton｜深度研究 DD｜v12.3｜2026-05-20 | 法國，Euronext Paris 主要上市（美股僅 OTC LVMUY） | `DD_LVMH_20260520.html` | v12.3 | 20260520 | 87 | B |  |  |
| VACN | DD｜VAT Group AG（VACN.SW）— v12.4 深度研究報告 | 瑞士，VAT Group AG（VACN.SW），SIX Swiss Exchange | `DD_VACN_20260522.html` | v12.4 | 20260522 | 85 | B |  |  |
| NBIS | DD｜NBIS Nebius Group N.V. — v12.4 (2026-05-23) | 荷蘭，Nebius Group N.V.（前 Yandex 國際業務），Nasdaq 上市 | `DD_NBIS_20260523.html` | v12.4 | 20260523 | 84 | B |  |  |
| ABB | DD｜ABB Ltd（ABB / ABBNY）— v12.4 | Switzerland/Sweden，ABB Ltd，NYSE ADR | `DD_ABB_20260525.html` | v12.4 | 20260525 | 82 | B |  |  |
| BHP | DD｜BHP Group (BHP) — 2026-05-25 — v12.4 | 澳洲/英國，BHP Group，NYSE ADR | `DD_BHP_20260525.html` | v12.4 | 20260525 | 82 | B |  |  |
| ESLT | DD - Elbit Systems Ltd (ESLT) - 2026-05-25 - v12.4 | 以色列，Elbit Systems，Nasdaq 普通股（FPI） | `DD_ESLT_20260525.html` | v12.4 | 20260525 | 82 | B |  |  |
| LYCAU | Lynas Rare Earths (LYC.AX) — DD v12.4 — 2026-05-25 | 澳洲，Lynas Rare Earths（LYC.AX），ASX 主要上市 | `DD_LYCAU_20260525.html` | v12.4 | 20260525 | 82 | B |  |  |
| RACE | DD｜RACE Ferrari N.V. — v12.4 (2026-05-25) | 荷蘭籍控股/義大利業務，Ferrari N.V.，NYSE 主要+Milan 次要（FPI） | `DD_RACE_20260525.html` | v12.4 | 20260525 | 82 | B |  |  |
| RIO | DD｜Rio Tinto (RIO) — 2026-05-25 — v12.4 | 英國/澳洲，Rio Tinto，NYSE ADR | `DD_RIO_20260525.html` | v12.4 | 20260525 | 82 | B |  |  |
| SU | DD｜Schneider Electric SE（SU / SU.PA）— v12.4 | 法國，Schneider Electric SE（SU/SU.PA），Euronext Paris 主要上市 | `DD_SU_20260525.html` | v12.4 | 20260525 | 82 | A |  |  |
| VALE | DD｜Vale S.A. (VALE) — 2026-05-25 — v12.4 | 巴西，Vale S.A.，NYSE ADR | `DD_VALE_20260525.html` | v12.4 | 20260525 | 82 | B |  |  |
| BMO | DD｜Bank of Montreal (BMO) v12.7 — 2026-06-15 | 加拿大，Bank of Montreal，NYSE+TSX 雙掛牌 | `DD_BMO_20260615.html` | v12.7 | 20260615 | 61 | B |  |  |
| TD | DD｜TD The Toronto-Dominion Bank（多倫多道明銀行）— v12.7 | 加拿大，Toronto-Dominion Bank，NYSE+TSX 雙掛牌 | `DD_TD_20260615.html` | v12.7 | 20260615 | 61 | B |  |  |
| VIK | DD｜Viking Holdings (VIK) v14.2 — 2026-06-29 | 百慕達籍/挪威創辦，Viking Holdings Ltd，NYSE 主要上市（FPI） | `DD_VIK_20260629.html` | v14.2 | 20260629 | 47 | B | 觀望 | 條件式衛星持倉 |
| HIMX | DD｜Himax Technologies (HIMX) v14.4 個股深度報告 2026-07-03 | 台灣，Himax Technologies，Nasdaq ADR（FPI） | `DD_HIMX_20260703.html` | v14.4 | 20260703 | 43 | B | 觀望 | 候選/追蹤池 |
| NU | DD Report — NU (Nu Holdings) ｜ v14.4 ｜ 2026-07-03 | 開曼/巴西，Nu Holdings，NYSE 主要上市（FPI） | `DD_NU_20260703.html` | v14.4 | 20260703 | 43 | A | 進場 | 衛星持倉 |
| ONON | DD｜On Holding AG (ONON) v14.4 — 2026-07-03 | 瑞士，On Holding AG，NYSE 上市（FPI） | `DD_ONON_20260703.html` | v14.4 | 20260703 | 43 | B | 進場 | 衛星持倉 |
| SE | DD｜Sea Limited (SE) v14.4 個股深度報告 2026-07-03 | 新加坡/開曼，Sea Limited，NYSE 主要上市（FPI） | `DD_SE_20260703.html` | v14.4 | 20260703 | 43 | B | 觀望 | 條件式核心持倉 |
| BESI | DD｜BE Semiconductor Industries (BESI)｜2026-07-10｜v14.11 | 荷蘭，BE Semiconductor，Euronext Amsterdam 主要上市 | `DD_BESI_20260710.html` | v14.11 | 20260710 | 36 | B | 觀望 | 核心 |
| SIMO | SIMO｜Silicon Motion Technology 深度研究報告 v14.11 | 台灣，Silicon Motion Technology，Nasdaq ADR-like ordinary shares（FPI） | `DD_SIMO_20260710.html` | v14.11 | 20260710 | 36 | B | 觀望 | 衛星 |
| AENA | DD｜Aena S.M.E. (AENA.MC) v14.12 — 2026-07-11 | 西班牙，Aena S.M.E.，Madrid 上市（美股僅 OTC AENAY） | `DD_AENA_20260711.html` | v14.12 | 20260711 | 35 | B | 觀望 | 追蹤 |
| ASML | DD ASML｜艾司摩爾 v14.12 深度報告（2026-07-16） | 荷蘭，Euronext Amsterdam + Nasdaq 雙主要上市 | `DD_ASML_20260716.html` | v14.12 | 20260716 | 30 | B | 進場 | 核心 |
| STM | DD STM｜STMicroelectronics — v14.12（2026-07-24） | 瑞士籍/法義業務，STMicroelectronics N.V.，NYSE+Euronext Paris+Borsa Italiana | `DD_STM_20260724.html` | v14.12 | 20260724 | 22 | 觀望 | 觀望 | 追蹤 |
| RMS | DD_RMS_20260730 — Hermès International（RMS.PA）v14.12 深度研究報告 | 法國，Hermès International（RMS.PA），Euronext Paris（美股僅 OTC HESAY） | `DD_RMS_20260730.html` | v14.12 | 20260730 | 16 | B | 觀望 | 追蹤 |
| TSM | TSM 台積電（ADR）深度盡職調查 — 2026-08-08 | 台灣，台積電 ADR，NYSE | `DD_TSM_20260808.html` | v15.0 | 20260808 | 7 | A | 進場 | 核心 |

## 非美股掛牌（台/日/馬，判準即排除，僅計數不展開）

22 檔唯一標的（48 份檔案，含歷史版本），涵蓋台股（2308/2317/2327/2330/2345/2368/2383/2454/3017/3037/3231/3443/3653/3661/5274/8299）、日股（6146/6857）、馬股（5246/5326/5398/6139）。依 `_PLAN.md` §0 鐵律「獨立成立」，美股國家掃描不得展開跨市場對照，本表不逐檔列出。

## 拿不準清單（歸類/旗標判斷 call，建議 writer／critic 複核）

以下歸類非 `_PLAN.md` §4 原始獵場名單明文列出，屬本表擴充判斷，信心度中等，供下游 writer／opus critic 複核調整：


1. **網路市集/訂閱平台歸鏡頭一而非鏡頭七或三**：ABNB、BKNG、UBER、DASH、EBAY、SPOT、MELI——判斷依據是報酬驅動機制（雙邊網路效應/平台經濟）而非產業表面分類（旅遊/零售/串流）。若 writer 認為應留在消費特許經營或另立子類，屬合理異議。
2. **ORCL 歸鏡頭一（平台）而非鏡頭三（軟體）**：近期 DD thesis 主軸已轉向 OCI 雲端資本週期/AI capex 敘事，判斷偏向與 Mag7 資本週期同組；傳統上 Oracle 仍是企業軟體/資料庫公司，另一種合理歸類是鏡頭三。
3. **V／MA 歸鏡頭四（複利機器）而非鏡頭六（金融）**：依 `_PLAN.md` §4 明文「V/MA 若判為網路效應複利機歸鏡頭四，本頁標切線」，本表採複利機判斷，鏡頭六財務頁應標切線帶回。
4. **FICO 歸鏡頭六（金融）而非鏡頭三（軟體）或鏡頭四（複利）**：核心業務為信用評分基礎設施授權（收費模式近網路型金融基礎設施），非典型 SaaS，也是合理複利股候選，三選一皆有論述空間。
5. **CSX 歸鏡頭四（複利機器）**：鐵路護城河型複利股判斷；亦可能因缺乏 plan 原始獵場對應鏡頭而應獨立於任一鏡頭外。
6. **GE／HWM／TDY 歸鏡頭四；CRS／ATI／CW／GHM 歸鏡頭九**：航太售後市場供應鏈按市值/複利品質切成兩群（大型=複利機、中小型=隱形冠軍），切分點主觀，建議 writer 覆核市值門檻是否一致。
7. **汽車供應鏈（MGA、LEA、BWA、F、GM、ALV）與航太/太空製造（RKLB、SPCX）歸鏡頭八（能源電力與再工業化）**：plan 原始獵場未列這兩群，本表以「再工業化/國防太空製造」廣義理由塞入鏡頭八；若 writer 認為應設「鏡頭外」處理，也是合理選項（尤其 SPCX 若為私募股權間接曝險而非公開市場可交易 ticker，可能需要在 hub 額外註記其獨特流動性狀態）。
8. **CDNS（Cadence）歸鏡頭二（半導體）而非鏡頭三（軟體）**：EDA 設計工具與晶片產業高度耦合，但本質是軟體授權商業模式，另一種合理歸類是鏡頭三。
9. **GLXY（Galaxy Digital）未掛 foreign_adr**：傳聞已於 2025 完成開曼→Delaware 遷籍以符合 Nasdaq/指數資格，本表暫列一般美股（鏡頭六金融），但遷籍真實性與生效時點未逐一查證來源，建議 writer 二次確認。
10. **GFS（GlobalFoundries）未掛 foreign_adr**：Mubadala（阿布達比）為大股東，且可能以外國私人發行人身分申報，但主要晶圓廠與營運重心在美國/德國/新加坡，本表暫不掛旗標僅留註記，建議 writer 複核申報身分（10-K vs 20-F）。
11. **CRDO（Credo Technology）未掛 foreign_adr**：法律上開曼群島註冊（常見 fabless 稅務結構），但總部與營運實質在美國矽谷，本表依「業務實質而非法律籍屬」判準不掛旗標，若 writer 採更嚴格的申報身分判準（20-F）則應改列 foreign_adr。

## 歷史版本補充說明

部分標的歷史版本數為 0（僅一份 DD，無歷史對照），部分達 9 版（如 AMZN、AVGO、GOOGL、MSFT 等高關注度大型股，反映 2026-03 至今多輪重跑）。歷史版本檔名未逐一列出，如需回溯特定標的歷次裁決演進，請直接 `ls docs/dd/DD_{TICKER}_*.html` 或跑 `python knowledge/q.py <TICKER>`。
