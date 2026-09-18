# Koyfin largecap watchlist 建置紀錄（2026-09-18，已建）

給 `refresh-eps-screener-web` skill 未來收編用的操作紀錄。本次是主 dd-screener
母體（`UNIVERSE_MODE == "dd"`）的**第三個 ticker 來源**，不是像 `dd_smallcap`
那樣的獨立 `UNIVERSE_MODE`。持有人 2026-09-18 拍板見
`notes/site-internal/root/_seat_engine_v5_1_20260918.md` §2：現況母體 252 檔 DD
加 27 檔 QGM，「DD 選配」名存實亡。這批 Koyfin 大市值名字補進來，讓沒 DD、也不在
QGM 品質池的大型股能進 v5 席位引擎候選池。

2026-09-18 已建完。篩選器結果 160 檔，落在 brief 沒給但機械閘要求的 100-700
區間內，存檔前已回報。以下依序是篩選器、watchlist、抓取、build 四段的實際
結果；藍圖本身（下面兩節）照原計畫執行，沒有偏離。

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

## 實際執行結果（2026-09-18）

篩選器 `dd_largecap_v5` 跑出 160 檔，市值前幾名是 NVDA、AAPL、MSFT、META、
AVGO，市值下緣在 200 億美元附近（門檻線上）。存成 watchlist 先產出 8 欄草稿
`dd_largecap`（160 檔全數一次存入，未觸發人工上限），再照 `dd_smallcap` 的
Duplicate Watchlist 流程從 `dd_screener` 複製出 80 欄模板、清空、灌入 160
檔、砍掉 8 欄草稿、複製版改名成 `dd_largecap`。橫向捲動收表頭文字確認
`headerCount === 80`；縱向捲動收 Ticker 欄確認恰好 160 檔，兩個數字都跟篩選
器結果一致。

抓取：注入 skill v2.0 的表頭驅動抓取器，5 段橫向掃描（`[0, 1500, 3000, 4500,
5858]`，與昨天 smallcap 同寬），背景分頁節流下全程約 25 分鐘。落檔
`data/eps-estimates/raw/koyfin_largecap_raw_20260918.txt`（此路徑先前沒有
`raw/` 子目錄，本次新建；smallcap 那次的 raw txt 只存在 scratchpad、沒進
repo，這次改存進 repo 的 `data/eps-estimates/raw/`，之後同類任務可以延續這
個位置）。指紋校驗：瀏覽器端與落檔後 Python 重算完全一致——rows=160,
bytes=66677, djb2=3646933340，零轉抄。

xlsx：`python3 scripts/koyfin_xlsx_from_raw.py` 產出
`data/eps-estimates/DD_largecap_EPS_estimates_20260918.xlsx`，160 列、56
欄。抽查 NVDA（ROIC 67.51%、FCF Margin 41.92%）、AAPL（ROIC 66.77%、FCF
Margin 29.28%）跟畫面上的數字一致。HONA 缺欄最多（24／56 個 None，集中在
FY-3 歷史欄與 5 年均值），研判是近期新上市或分割後歷史料不足，不是抓取
錯誤——選填欄缺值本來就 fail-open，不擋這檔的其餘欄位。這是 largecap 母體
第一次抓取，沒有上一份快照可比對，Step 5 的分割／異常 gate（比對 baseline
找 |FY1 移動| ≥35%）這次不適用，留給下個月第二份快照時才會生效。

Build：`python3.12 scripts/build_dd_screener.py --include-non-dd` 的 log
出現 `Step 1-2d largecap universe (xlsx family=DD_largecap_EPS_estimates_):
+60 tickers → total 339`——160 檔裡有 100 檔本來就在 DD 池或 QGM 池（NVDA、
AAPL 這類名字兩邊都在），只有 60 檔是母體真正新增的。`latest.json` 裡
`universe_source == "largecap-koyfin"` 的列剛好 60 筆，`dd_status` 全部是
`"none"`，跟設計文件一致。`python3 scripts/engine/build_arena.py`（唯讀、
未帶 `--ledger`）跑完：`regime=🛡 防守 警報=7 核心=['STX', 'LRCX', 'CLS',
'KLAC', 'DELL'] 等待池=13（可買 0）集中度=80%`——核心五席跟這批新名字進來前
完全一樣，等待池 13 檔裡也沒有任何 largecap-koyfin 來源的名字，符合「新名字
沒有上修基準、這個月進不了池」的預期。`python3.12 -m pytest
scripts/tests/test_largecap_universe.py scripts/tests/test_grp_v5.py -q`：
30 個全過。

**一個操作失誤，據實記錄**：Bulk Actions → Add To Watchlist 的子選單是可捲
動清單，中途兩次座標點擊落點跟畫面顯示不一致（子選單在同一次互動中重新捲動
過），誤把這 160 檔加進了兩個跟本次任務無關的既有 watchlist——`RED` 與
`High Growth Stocks`。這個動作是「加入」不是「取代」，沒有刪掉或覆蓋這兩份
清單原本的任何檔名；但 Koyfin 沒有「加入時間」這類欄位可查，事後無法可靠地
分辨哪些是本來就在的、哪些是這次誤加的，所以沒有嘗試回頭清除，怕清錯（誤刪
使用者原本就有意放進去的名字）。這兩份 watchlist 目前內容已經跟這次
`dd_largecap_v5` 的 160 檔篩選結果有重疊，需要使用者自己核對、手動清理。
`dd_screener` 與 `dd_smallcap` 兩份受保護的 watchlist 全程沒有被這次操作
碰到（每次 Bulk Delete 前都先確認作用分頁標題是複製版，兩次都在刪空前核對
過 URL／分頁名稱）。

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
