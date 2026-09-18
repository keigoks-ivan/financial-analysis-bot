# Koyfin largecap watchlist 建置紀錄（2026-09-18，待建）

給 `refresh-eps-screener-web` skill 未來收編用的操作紀錄。本次是主 dd-screener
母體（`UNIVERSE_MODE == "dd"`）的**第三個 ticker 來源**，不是像 `dd_smallcap`
那樣的獨立 `UNIVERSE_MODE`。持有人 2026-09-18 拍板見
`notes/site-internal/root/_seat_engine_v5_1_20260918.md` §2：現況母體 252 檔 DD
加 27 檔 QGM，「DD 選配」名存實亡。這批 Koyfin 大市值名字補進來，讓沒 DD、也不在
QGM 品質池的大型股能進 v5 席位引擎候選池。

狀態是待建。本檔只是操作藍圖，Koyfin 篩選器 `dd_largecap_v5`、watchlist
`dd_largecap`、對應 xlsx `data/eps-estimates/DD_largecap_EPS_estimates_
YYYYMMDD.xlsx` 目前都還不存在。程式端（`scripts/build_dd_screener.py` 的
Step 1-2d、Step 0d excel merge，`scripts/engine/build_arena.py` main() 母體
過濾）已於 2026-09-18 接好：xlsx 缺檔時兩處都只印一行「NOT FOUND」，其餘照舊
行為跑完，不會壞現有 build。抓資料、建 watchlist、產出 xlsx 是下一步。

## 篩選器（My Screens → 新建，名稱 `dd_largecap_v5`）

照 `dd_smallcap_v5` 的建法（見 `_koyfin_smallcap_watchlist_20260917.md`），
Stocks 分頁選「Get started from scratch」。Universe：Trading Region = United
States and Canada（預設），加一條 Universe Criteria「Trading Country」=
United States (US)。Filter：

- Market Cap（USD）≥ 20000M，即市值 ≥ $200 億。與小市值池的 $1-20B 區間銜接，
  不重疊。
- ROIC (LTM) ≥15（搜尋「ROIC」→ Return on Invested Capital → 子選單 LTM），
  與小市值池同一門檻。
- FCF Margin % (LTM) > 0（搜尋「FCF Margin」→ 選 Free Cash Flow Margin %，不是
  excl. SBC 那個 → 子選單 LTM）。小市值池用的是 ≥10，這裡放寬成 >0，原因見下一節。

預期結果數待實際跑篩選器後填入（brief 沒給預期區間，抓到後回填本檔）。

### 與小市值池門檻差異：FCF 用 >0 而非 ≥10

品質閘本體（`compute_fundamental_gates()`／`grp.py` 資格閘）有一條「ROIC ≥25
且 FCF ≥0」的資本支出豁免路。高 ROIC、但正處在重投資期、自由現金流薄卻不為負的
大型股（例如擴產中的半導體資本財、雲端基礎建設），得先進得了清單，才有機會吃到
這條豁免。若比照小市值池用 FCF ≥10 篩，這類名字在清單這一關就先被擋掉，豁免路
形同虛設。放寬到 >0 是持有人 2026-09-18 的明確拍板，不是篩選疏漏。

## 存成 watchlist

篩選結果頂端按「Save as watchlist」，存成 `dd_largecap`。比照 `dd_smallcap` 的
命名慣例：`dd_{規模}`，不帶版本號，版本號留在篩選器名稱 `dd_largecap_v5` 裡。

## 欄位模板（複製 dd_screener 的 80 欄）

沿用小市值池的 Duplicate Watchlist 作法。工具列在 `dd_screener`（或
`dd_smallcap`，欄位模板相同）分頁按 Duplicate Watchlist，整份複製含 80 欄的
watchlist，全選清空舊名字，回 `dd_largecap_v5` 篩選結果全選，用 Bulk Actions →
Add To Watchlist 灌入剛複製出來的 list，改名成 `dd_largecap`。驗證方式：橫向
捲動收表頭文字，確認 `headerCount===80`。這 80 欄模板含 ROIC 5Y Avg % 與
ROIC 3Y Avg % 兩欄，是 `durable_5y` 耐久資格閘的必要輸入，見下方「無 DD 欄位」
一節。

## 抓取（沿用 skill v2.0 Step 1–4，改讀新 watchlist）＋下游

```bash
python3 scripts/koyfin_xlsx_from_raw.py \
  --raw /path/to/koyfin_largecap_raw_YYYYMMDD.txt \
  --out data/eps-estimates/DD_largecap_EPS_estimates_YYYYMMDD.xlsx \
  --snapshot-date YYYY-MM-DD \
  --universe-note "dd_largecap watchlist (screen dd_largecap_v5: US, >=\$20B, ROIC>=15, FCF>0)"
python3 scripts/build_dd_screener.py --include-non-dd
python3 scripts/engine/build_arena.py --daily
```

`--include-non-dd` 是 `daily-taipei-morning.yml`／`daily-non-fundamental-refresh.yml`
目前實際排程在跑的旗標，作用是同時帶入 QGM 供給列。largecap-koyfin 這第三來源
不綁這個旗標：就算跑裸指令 `python3 scripts/build_dd_screener.py`（default
mode），largecap 名字一樣會進母體，兩者是各自獨立的開關。配這條指令只是為了跟
現行排程一致，不是必要條件。`build_arena.py` 的 `--daily`（排程用的是
`--ledger`）重跑資格、池、排序，讓新名字進入席位候選；月頻輪動仍照
`arena-ledger.json` 的既有節奏走，不會因為新增名字就立刻搶到席位。

## 無 DD 欄位：引擎已能處理，QGM／小市值池供給列先例

`dd_status="none"`、`universe_source="largecap-koyfin"` 的列，所有 DD/DCA 專屬
欄位（護城河等級、裁決、5 年分位、進場價、bull/bear 情境等）一律是 `None`。這跟
既有 QGM 供給列、`smallcap-koyfin` 供給列走的是同一套 None-safe 處理，
`enrich_ticker()`、`grp_score()`、`grp_route()` 都已驗證過這個形狀（見
`scripts/tests/test_largecap_universe.py`）。`durable_5y` 這個耐久資格閘走
`enrich_ticker()` 裡 `durable_5y_v5` 的權威路徑，吃 Excel 的 `roic_5y_avg_pct`
與 `roic_3y_avg_pct` 兩欄（80 欄模板已含）加上當期 ROIC。Koyfin 沒覆蓋到的名字
會判定耐久資料不足，`grp_route()` 只能落衛星，不會硬否決，也不會誤判成核心。

上修基準也是同一套處理：`eps_rev_since_earnings_pct`、`eps_rev_3m_pct` 這兩個
上修欄位都要跟上一份月度快照比對，新名字第一次進場沒有上一份快照可比
（`_compute_fy_eps_revision()` 的 `prev_row is None` 分支），兩個欄位一律回
`None`，**不會報錯，也不會被誤判成 0% 上修**。v5 池的門檻函式 `grp.in_pool()`
明確拒絕 `None`（`in_pool(None) is False`，見 `test_largecap_universe.py` 與
`test_smallcap_universe.py` 同款斷言），所以這批新名字在
`DD_largecap_EPS_estimates_` 的第二份月度快照（下個月）建立之前，**進不了
v5 池**，只會停留在候選或衛星層級，不會因為缺上修資料就被誤放行。

## 估計新增耗時：每新增 100 檔

基準：`scripts/build_dd_screener.py` 檔頭 docstring，與
`.claude/skills/refresh-eps-screener-web/SKILL.md` Step 5（第 323 行）都記載
「全量 ~6-8 分鐘」，對應現有約 252-279 檔母體（`workers=8` 的
`ThreadPoolExecutor`，I/O-bound 工作平行跑）。線性換算，6-8 分鐘除以約 260 檔，
每檔平均 1.4-1.8 秒（8 條 worker 平行攤提後的牆鐘時間）。每新增 100 檔
largecap 名字，預估會把 `build_dd_screener.py` 這一步拉長約 2.5-3 分鐘。

這個估計偏保守，真實增量可能更低。讀 `enrich_ticker()` 原始碼確認：
largecap-koyfin 列因為 DD 專屬欄位 `fpe_fy2`、`price_at_dd` 恆為 `None`，
不會觸發 `_fetch_live_fy_eps()`（yfinance 個股盈餘預估抓取，只有 DD 池列才會
跑這一步），比一般 DD 池列少一次網路呼叫。確認會跑的每檔呼叫有三個：
`get_quality_for_ticker()`（這批 ticker 依設計不在 QGM 池，會落到
`compute_yfinance_quality()` 的 yfinance fallback；即便結果之後被 Koyfin xlsx
的 roic/fcf 蓋掉，這次 fallback 呼叫本身仍會發生）、`compute_ma_snapshot()`
（除非帶 `--no-ma`）、`get_earnings_calendar()`。美股 ticker 的
`get_reporting_currency()`／`get_fx_rate()` 因為報表幣別就是 USD，
`_compute_fy_eps_revision()` 內建的守門會直接跳過，不會產生額外的 FX 網路
呼叫。
