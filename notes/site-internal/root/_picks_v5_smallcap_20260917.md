# 精選榜改版：爆發組退役、十倍組改 v5 小市值池（2026-09-17）

## 為什麼要改

爆發（循環拐點型）追循環股價格動能，跟 v5 席位引擎 thesis「品質派資格 ∩ 獲利上修
排序 ∩ 突破還原歷史新高、價格動能整個退出排序」正面矛盾；記分板顯示循環轉折形狀
（n=20）中位報酬 −2.8%、虧損率 55%，是輸家形狀。十倍組原 gate-set（逐檔 yfinance
掃六條件，全數標「未調參」、從未回溯驗證）是與 GRP 席位獨立的一把尺，兩尺並存徒
增認知成本，統一為同一套已校準的規則、只換市值帶，風險更低。

## 改了什麼

1. **爆發退役**：比照長熬（2026-07-29）先例。`build_picks.py` 移除 `build_baofa()`
   及整條 cyclical-track/sop-funnel/radar/arena/ID 產業趨勢 pipeline，`candidates.json`
   的 `official_baofa[]`／`baofa[]` 寫死空陣列＋`retired_groups.baofa`。`picks.json`
   changelog 新增一筆、`rules.retired_baofa` 留痕。
2. **十倍組全面重寫**：`build_tenbagger.py` 不再自建 gate-set，改逐字重用 GRP 席位
   v5 資格閘（`grp.quality_gate`／`durable_5y_v5`／成長閘含基期效應／`grp_score`／
   `pool_sort_key`／`in_pool`／`timing_lamp`，經 `build_arena.row_dict`／`_flat_view`）
   跑在 $10億–$200億市值帶。母體＝`data/engine/universe.json`（972 檔）∪
   `docs/dd-screener/latest.json` ticker，查不到 v5 欄位或市值未知者計入「資料
   不足」，不用 QGM 原始池回推湊數（缺 revision/timing 欄位會讓資格閘失真）。市值
   來源：`qgm_seed.market_cap_b` → `mktcap.json` 快取 → QGM 原始池 → 網路補。
3. **無核心席、無月頻輪動**：`official`＝池（依上修排序，無上限）、`buyable`＝綠/
   橘燈、`waiting.{yellow,red}`＝其餘依燈號分組、`not_in_pool`＝資格過但上修未達
   5% 收合複審；無 `seat_cap`（舊 schema 遺留鍵，v5 不消費）。
4. **排程改每日**：`daily-taipei-morning.yml` Step 2b（Arena `--daily` 之後），鏡射
   進 `daily-non-fundamental-refresh.yml`；`weekly-market-update.yml` 移除舊兩步。
5. **頁面**：`_embed.html` 改「①可買②等待池③收合」單表，欄位對齊 GRP 席位表
   （代號／上修%／距歷史新高%／下次財報／耐久／時機／倉位／DD／備註）；cockpit
   picks 分頁摘要句同步改寫。
6. `generate_list_forecasts.py` 的 `picks`／`late` producer 降 dormant（讀空陣列
   時印明「來源已退役」），PREREG claim_template 不刪。

## 實跑結果（2026-09-17，`python3.12 scripts/build_tenbagger.py`）

universe 980 檔（扣 .TW）→ 池覆蓋 263 → 市值可判定 250 → 落在 $10億–$200億帶 56 →
資格閘全過 **0**（47/56 卡耐久、30/56 卡站上 52 週線、29/56 卡三年成長多數缺
Koyfin 三年期預估、13/56 卡融券 >10%，卡點重疊、分散在多閘，非單一閘全滅——誠實
掛零非 bug）。資料不足：未在池覆蓋 717、市值未知 13；帶外 194。

## 證偽條件

見 `knowledge/rule_ledger.md`「精選榜改版：爆發組退役、十倍組改 v5 小市值池」列。

## 沒做/未驗證

小市值池目前掛零，無「可買」實例可供 UI 視覺驗算（表格渲染以合成 fixture 在
`scripts/tests/test_picks_v5.py` 驗證）。市值網路補抓對 .KL/.T/.AX/.SW 等非 .TW
外國掛牌會打 404（`grp.fetch_caps()` 既有行為，非本次新增，僅警告不影響輸出）。
