# 設計凍結稿 P2：預測帳簿第二批 producer＋Kelly paper 組合＋resolver 擴充（2026-09-02）

- 日期：2026-09-02 深夜｜狀態：**orchestrator 凍結，持有人複審中；sonnet 分包實作、全部不 commit**（持有人說 push 才 commit）。
- 前稿：`_forecast_v2_design_20260902.md`（帳簿 v2）、`_market_cockpit_design_20260902.md`（市況主控台 v3；§11 為選股 v2 整合，與本稿同批實作）。本稿只寫差異與新增；v2／v3 未被改動的條文仍有效。
- 憲法相容：不是收斂面（全部是「給既有東西記分」或市場層 paper 規則）；描述器紀律；判斷類規則登 rule_ledger 並附 kill；成品白話依 `_plainlang_styleguide.md`；Python 3.9、stdlib（yfinance 只在 builder 抓資料時允許）；所有 producer dry-run 預設、`--write` 落帳、`--ledger` 可覆寫測試路徑、stdout 只印 JSONL、訊息進 stderr；哨兵 twin 由 `forecast_lib.append` 自動生成。

---

## §0 現況與本批範圍（判斷紀錄）

**9/3 首次日更預檢（本機 `build_market_state.py --out scratch`）**：11 條管線 0 gap；stale 只有 regime（2026-07-06，已提名候刪）與 COT（2026-08-18，CFTC 延遲）；總經時鐘 warn（月頻）。**唯一缺口**：第五磚（實單執行層）`as_of` 讀 long-track 的 `data_date`，該欄是**週線 bar 標籤（本週五）**，9/2 顯示 2026-09-04，讀者看到未來日期；stale 判定也因此晚 4 天。修法見 §7(a)，不動 long-track 產線。

**資料事實（決定本批口徑）**：
- FRED 對 ICE BofA HY／IG／CCC OAS 只給約 3 年（2023-09 起，實測 794 列）；monitor 自己的長史錨是 `baa10y`（1986 起）與 `hyg_lqd`（2008 起），但 `baa10y` 不在 latest.json 顯示項。→ 信用領先用 **HYG／LQD 比值**（monitor 已顯示、spark 日頻 30 點、yfinance `auto_adjust=True` 收盤），不用 OAS。
- `docs/monitor/data/internals.json`＋`internals_history.json` 已有 `bei10y`（450 日）、`core_pce_yoy`／`payems_3m`（月頻、日填）、`auct_dealer`（242 場，2012 起）。kill_watch 四條 internals 型引信中三條有 FRED 全史可算 climatology（T10YIE／PCEPILFE／PAYEMS），auct_dealer 無。→ 新增 `internals:` resolver 域即可落帳三條（原待辦「等 monitor 補 bei10y」改此路，不動 monitor 管線）。
- 市場內部結構：internals 的廣度序列多數只有 34～450 點，不夠建 20 年 base rate；11 檔 SPDR 類股 ETF 站上 50 日線比例可用 yfinance 自建 25 年，且 `data/statlab_prices.json` 已有這 11 檔＋SPY 供產生端同公式計算。→ 市場廣度 producer 用類股 ETF 廣度。
- 日曆效應：FOMC／CPI 歷史日期無現成資料源，本批只做**純由價格序列可推導**的兩種——月末四日窗（turn-of-month）與假日前一日；FOMC／CPI 列下一批（`docs/intel/data/ff_calendar.json` 只有未來事件）。
- `docs/catalyst/variance.json` 週更（intel-2-daily 週日段）但無歷史快照；`docs/catalyst/snapshots/` 放的是財報前瞻凍結檔，非 variance。
- 選股 v2 已併入 main，整合規格在 v3 稿 §11；`data/weekly_cache_universe/` 由 weekly-engine.yml 首次 CI 週跑後才有檔。

**本批做**：G1 信用領先／G2 市場廣度／G3 日曆效應三個 producer；G4 resolver 擴充（`vs_base_date` 窗、`internals:` 域、relspy 退路加 universe 快取、macro 月頻 climatology、kill_watch 收 internals 型）；G5 Kelly 傾斜 paper 組合；G6 variance 週快照；H1 選股三名單 producer（v3 稿 §11.1）；G7 整合（state builder／兩頁面／記分板／workflow／rule_ledger）。**不做**：FOMC／CPI 日曆、epsdrift resolver、CTA 尺規換 TFF、dealer gamma（P3）。

---

## §1 G1 信用領先 producer（source `credit-lead`）

**命題**：`credit_spy_up_21d`／`credit_spy_up_63d`——「{resolve_by} 前（約 21／63 個交易日）SPY 收盤高於 {date} 收盤 {close}」，條件＝信用領先訊號。與 vrp 同型，故進議會 `spy_up_21d`／`spy_up_63d` 聚合（§7）。

**訊號**：R_t＝HYG 收盤 ÷ LQD 收盤（同日、yfinance `auto_adjust=True` Close，與 monitor 口徑一致）；x_t＝100 × ln(R_t ／ R_{t−21})（21 個交易日對數變化，%）。x 為負＝HYG 相對 LQD 下跌＝高收益利差走闊。

**Builder `scripts/build_credit_base_rates.py`**（慣例照抄 `build_vrp_base_rates.py`）：
- raw cache `data/credit_base_rates_raw_cache.json`：HYG／LQD／SPY 各 20 年日收盤（yfinance；失敗沿用既有快取並 warn，**不做 stooq fallback**——stooq 未還原股利，口徑不同）。
- 取樣點＝三序列共同交易日中每月首個交易日 t，需 t−21 存在；21d 結果需 t＋21 存在、63d 需 t＋63（各自獨立計數，尾端不足者不計）。結果＝SPY 收盤(t＋H) > SPY 收盤(t)。
- 桶＝x 的三分位（取樣點 in-sample 切點 q33／q67，JSON 內誠實註記）：`low`（利差走闊快）／`mid`／`high`（利差收斂快）。每桶 `freq_up_21d`／`freq_up_63d`／`n_21d`／`n_63d`；`pooled` 同欄；`p_clim`＝{`credit_spy_up_21d`: pooled freq_up_21d, `credit_spy_up_63d`: pooled freq_up_63d}。cell n < 30 → producer 用 pooled。
- 輸出 `data/credit_base_rates.json`：`{built_at, data_start, data_end, n_samples, cuts:{q33,q67}, buckets:{low,mid,high}, pooled, p_clim, definition, note}`。`--if-due` 85 天、`--skip-fetch`。

**Generator `scripts/generate_credit_forecasts.py`**：
- 資料＝`docs/monitor/data/latest.json` credit 類 `hyg_lqd` item：`spark`（須 ≥ 22 點）與 `date`；x＝100 × ln(spark[−1] ／ spark[−22])。SPY 今收＝`data/flowmap_prices.json` SPY 於 item.date 當日的 bar（無此日 → 跳過，reason `date_mismatch`，下週再試）。
- 節奏＝每月首次班車（查重：同 source 同 YYYY-MM 已有 → 整批拒）；兩筆同 `episode_id=credit:{YYYY-MM}`；resolver `{"series":"pxd:SPY","op":">","value":<今收>,"window":"at_expiry"}`；horizon 30／91 曆日；p＝桶頻率（n<30 用 pooled）；p_clim／p_clim_ref／p_table_built_at 由表；note 記 x、桶、切點。
- claim 白話：「{resolve_by} 前（約 21 個交易日）：SPY 收盤高於 {date} 的 {close}｜信用領先條件：HYG／LQD 比值 21 日變化 {x:+.2f}%（{桶白話}）」；桶白話 low→「高收益利差走闊，風險偏好轉弱」、mid→「利差持平」、high→「高收益利差收斂，風險偏好轉強」。63d 版本改「約 63 個交易日」。

## §2 G2 市場廣度 producer（source `breadth`）

**命題**：`breadth_spy_up_21d`／`breadth_spy_up_63d`（同 §1 型，進議會聚合）。

**訊號**：b_t＝100 × (站上 50 日簡單均線的類股 ETF 檔數) ÷ (當日有 ≥ 50 根 bar 的類股 ETF 檔數)，母體 11 檔 SPDR：XLK XLF XLE XLV XLI XLY XLP XLU XLB XLRE XLC；可用檔數 < 9 的日子不取樣。

**Builder `scripts/build_breadth_base_rates.py`**：raw cache `data/breadth_base_rates_raw_cache.json`（SPY＋11 檔，25 年，yfinance auto_adjust Close；失敗沿用快取）；取樣＝SPY 每月首個交易日；結果＝SPY 收盤(t＋21／63) > 收盤(t)；**桶固定（PREREG）**：`low` b < 30／`mid` 30 ≤ b ≤ 80／`high` b > 80；每桶 freq／n、pooled、`p_clim`（無條件）；cell n < 30 → pooled。輸出 `data/breadth_base_rates.json` 結構同 §1（cuts 換成固定門檻）。`--if-due` 85 天。

**Generator `scripts/generate_breadth_forecasts.py`**：資料＝`data/statlab_prices.json`（series 為 [date, close]，11 檔＋SPY）；t＝SPY 最後一根 bar；b_t 同公式；SPY 今收＝flowmap_prices 於 t 的 bar（缺 → `date_mismatch` 跳過）；月查重；`episode_id=breadth:{YYYY-MM}`；resolver pxd:SPY at_expiry；claim 白話：「…｜市場廣度條件：11 個類股 ETF 站上 50 日均線比例 {b:.0f}%（{桶白話}）」，low→「參與度低（洗盤區）」、mid→「參與度中性」、high→「參與度高（廣度強）」。

## §3 G3 日曆效應 producer（source `calendar`）

**命題**：
- `tom_spy_up_4d`「月末四日窗：{resolve_by}（次月第三個交易日）SPY 收盤高於 {base_date} 收盤」——L＝月最後交易日，base_date＝L 的前一交易日，resolve_by＝次月第三個交易日（窗＝L−1 收盤 → L＋3 收盤，4 個交易日）。
- `preholiday_spy_up_1d`「假日前一日：{P} SPY 收盤高於前一交易日收盤（{假日名} 前）」——P＝假日前最後一個交易日，base_date＝P 的前一交易日，resolve_by＝P。

**Resolver（G4 實作）**：pxd:／ttp: 域新增 `window: "vs_base_date"`：`{"series":"pxd:SPY","op":">","value":0,"window":"vs_base_date","base_date":"YYYY-MM-DD"}`；outcome＝(close_end ／ close_base − 1) {op} value，close_base＝base_date 當日或之前最近收盤（該收盤日期須 ≥ base_date − 4 曆日，否則 void `vs_base_stale_base`），close_end＝resolve_by 當日或之前最近收盤，只在 today ≥ resolve_by 時結算（同 at_expiry）；base_date ≥ resolve_by → void `vs_base_bad_dates`；缺價 → void `pxd_no_bar_vs_base:{ticker}`；`--check-resolver` 印實際取到的 base／end 日期。

**Builder `scripts/build_calendar_base_rates.py`**：raw cache `data/calendar_base_rates_raw_cache.json`（SPY 25 年，yfinance auto_adjust Close）。TOM：每月 L，需 L−1 與 L＋3 存在，命中＝close(L＋3)／close(L−1) − 1 > 0；p_clim＝全部 t 的 close(t＋4)／close(t) − 1 > 0 頻率。Pre-holiday：假日＝資料期間內（首尾各去 5 個交易日）不在交易日序列中的週一至週五；連續缺口只算一次；P＝缺口前最後交易日；命中＝close(P)／close(P−1) − 1 > 0；p_clim＝全部 t 的單日上漲頻率。輸出 `data/calendar_base_rates.json`：`{built_at, data_start, data_end, tom:{p, n}, preholiday:{p, n}, p_clim:{tom_spy_up_4d, preholiday_spy_up_1d}, definitions}`。`--if-due` 85 天。

**Generator `scripts/generate_calendar_forecasts.py`**（每週班車都跑）：
- 未來交易日曆＝週一至週五 − `NYSE_HOLIDAYS`（**逐字寫入**）：2026：01-01 元旦、01-19 馬丁路德金恩日、02-16 總統日、04-03 耶穌受難日、05-25 陣亡將士紀念日、06-19 六月節、07-03 獨立紀念日（補假）、09-07 勞動節、11-26 感恩節、12-25 聖誕節；2027：01-01 元旦、01-18 馬丁路德金恩日、02-15 總統日、03-26 耶穌受難日、05-31 陣亡將士紀念日、06-18 六月節（補假）、07-05 獨立紀念日（補假）、09-06 勞動節、11-25 感恩節、12-24 聖誕節（補假）。所需日期超出表 → 跳過並 stderr `holiday_table_exhausted`（逼維護，不猜）。
- 事件枚舉：ts_date 起 60 天內的每個月末 L 與每個假日 H；**落帳條件 base_date ∈ [ts_date, ts_date＋7 天)**（班車週一 02:00 UTC 在美股收盤前，base_date＝當週一亦合法）。
- 查重鍵＝(source, claim_template, resolve_by)；`episode_id`＝`cal:tom:{L 所在 YYYY-MM}`／`cal:pre:{H}`；block_key＝resolve_by 的 YYYY-MM；horizon＝(resolve_by − ts_date).days；p／p_clim 由表；note 記 L／H／P。
- 首張預期：TOM 2026-09-30（base 09-29、resolve_by 10-05，於 09-28 班車落帳）；假日前一日首張＝感恩節（P 11-25，於 11-23 班車落帳；勞動節 09-04 已過）。

## §4 G5 Kelly 傾斜 paper 組合（`kelly_rule`，PREREG 凍結至判決或 24 個月）

**定位**：v2 §0 承諾的「以機率建 Kelly 縮放 paper 組合對 buy-and-hold」。它回答「議會的 p 有沒有錢的價值」，與市況曝險規則（描述環境的三因子）並列、不合併。paper only，永不連實倉。

**Builder `scripts/build_kelly_track.py`** → `docs/market/data/kelly_track.json`（schema `kelly-track-v1`：prereg 逐字、inception_date、exposure_history、nav_series、bench、sprt、stats、data_gaps、built_at），掛 `weekly-market-update.yml` 於 `build_exposure_track.py` 之後（週六班車以週五收盤算、週一生效）。

**輸入**：`docs/market/data/state.json` `council_summary.spy_up_21d`（p、p_clim、n_sources）；`docs/market/data/exposure_track.json` `factors_history[−1].rv_blend`（缺 → 自算，公式逐字同 build_exposure_track）；`docs/monitor/data/latest.json` rates `dgs3mo` val（%）；SPY 日線＝`data/flowmap_prices.json`。

**規則**：edge＝p − p_clim。若 |edge| < 0.05、或 n_sources < 2、或任一輸入缺 → E＝1.0（記 reason：`no_edge`／`thin_council`／`missing_input`）。否則 z＝Φ⁻¹(p) − Φ⁻¹(p_clim)（`statistics.NormalDist().inv_cdf`），σ21＝(rv_blend ／ 100) × √(21／252)，**E＝clip(1 ＋ 0.25 × z ／ σ21, 0.5, 1.5)**（四分之一 Kelly，相對 100% 基準的傾斜）。5pp 門檻與 read_zh 的「無邊際」同一把尺。

**帳**：inception＝首次執行的效力週一，NAV＝100；日 NAV_t＝NAV_{t−1} × (1 ＋ E × r_SPY,t − fin_t)，fin_t＝max(E − 1, 0) × (dgs3mo ＋ 1.5)／100／252（槓桿部分付 3 個月國庫券＋1.5% 年息，同 long-track 慣例）；E < 1 的現金不計息（同曝險規則慣例，對本規則偏保守，寫進 prereg）。基準＝SPY buy-and-hold。

**記分**：月樣本＝當月 paper 報酬 − SPY 報酬 > 0 為命中；SPRT 同 v2 §3.3、鎖存（實作照抄 build_exposure_track 的 sprt_with_latch）；Sharpe／MaxDD ≥ 3 個月才列（資訊欄）。`score_flowmap.py` 加 `kelly_rule` 區（讀法同 exposure_rule），`n_sprt_modules` 3 → 4。

**kill（rule_ledger）**：SPRT accept_h0 → 撤下；資料層：連續 8 週因 `missing_input` E＝1.0 → gaps 標紅（非 kill）。

## §5 G6 財務 variance 週快照

`scripts/snapshot_variance.py`：讀 `docs/catalyst/variance.json`，as_of＝`generated_at` 前 10 碼；寫 `docs/catalyst/variance_history.json`：`{schema:"variance-history-v1", snapshots:[{as_of, generated_at, n, rows:{TICKER:{fy_label, base_eps, consensus_eps, drift_pct, flag}}}]}`，同 as_of 覆寫（冪等）、as_of 升冪、不裁舊、缺檔不 crash（exit 0＋stderr）。掛 `intel-2-daily.yml` 週日 catalyst 步 `build_variance_tracker.py` 之後一行（`|| echo "::warning::variance snapshot failed"`）；該工作流 PATHS 已含 `docs/catalyst`（實作時確認）。下一批再做 `epsdrift:` resolver。

## §6 G4 resolver 擴充包

1. **`window: "vs_base_date"`**（§3）於 pxd:／ttp: 域。
2. **`internals:<key>` 域**：現值＝`docs/monitor/data/internals.json` categories[].items[] 中 key 的 `val`（parse 同 monitor 域）；序列＝`docs/monitor/data/internals_history.json` `series[key]`（[date, value] 升冪）；單位 scale 偵測逐字同 monitor 域（v2 §4.1）；any_close／at_expiry 語義同 monitor 域；key 缺 → void `internals_key_missing:{key}`；`--check-resolver internals:bei10y` 可用。
3. **relspy px_T 退路鏈**加 `data/weekly_cache_universe/`（在 weekly_cache 之後、statlab 之前；schema 同 weekly_cache）。
4. **`scripts/build_macro_base_rates.py`**：FRED_SERIES 加 `PCEPILFE`、`PAYEMS`（月頻）；衍生序列 `core_pce_yoy`＝(PCEPILFE_t ／ PCEPILFE_{t−12} − 1) × 100、`payems_3m`＝最近 3 個月 ΔPAYEMS 平均（千人）——口徑同 `build_monitor_internals.py`；`MONITOR_KEY_SERIES` 加 `core_pce_yoy`→("core_pce_yoy","%")、`payems_3m`→("payems_3m","K")；新增 `MONTHLY_SERIES={core_pce_yoy, payems_3m}`：climatology 對月頻序列 H＝max(1, round(horizon_days／30.44)) 個觀測、20 年窗＝240 個觀測，回傳 dict 加 `freq: "monthly"|"daily"`。
5. **`scripts/harvest_macro_falsifiers.py` `conditional_p`**：月頻 key 用 PREREG 月頻常數 LVL_WINDOW 12 個觀測／MOM_WINDOW 3 個觀測／SHRINK_PRIOR_N 12（P_FLOOR 0.01 不變）；`LVL_BUCKET` 顯式登記 `core_pce_yoy: (">=", 90)`、`payems_3m: ("<=", 10)`、`bei10y: (">=", 90)`（取代 harvest_kill_watch 的 setdefault 猜法）。
6. **`scripts/harvest_kill_watch.py`**：`data_source.type == "internals"` 且 key ∈ MONITOR_KEY_SERIES → 收案；resolver `internals:<key>`；current 取 internals.json；delta 單位 core_pce_yoy %／payems_3m K／bei10y %；`auct_dealer` → 跳過 `no_climatology_series`；檔頭「只處理 monitor 型」段落改寫為現況。預期新落帳三張：bei10y ≥ 2.6（現 2.35）、core_pce_yoy ≥ 3.5（現 3.34）、payems_3m < 0（現 20K）。
7. `knowledge/README.md` 域清單與 window 清單同步。

## §7 G7 整合（G1–G6、H1 dry-run 全過後才做）

- **`scripts/build_market_state.py`**：(a) 第五磚 `as_of`＝max(history_us[−1].date, history_tw[−1].date)，sub 末尾加「週線 bar {data_date}」，freshness 列同；(b) 議會映射：`spy_up_21d` ← tsmom SPY＋`vrp_spy_up_21d`＋`credit_spy_up_21d`＋`breadth_spy_up_21d`；`spy_up_63d` ← `vrp_spy_up_63d`＋`credit_spy_up_63d`＋`breadth_spy_up_63d`；calendar 兩模板進 council 清單但不進 summary（窗長不同）；(c) 新增頂層 `kelly_rule` 區（exposure、edge、z、sigma21、reason、n_sources、nav、bench、sprt；缺檔 null＋gap）與 freshness 列「Kelly 傾斜組合（paper）」週更；(d) `STOCK_LEVEL_SOURCES` 加 `own-board`／`picks-late`／`mech-nodd`；(e) 記分板句計數自動含新模組。
- **`docs/market/index.html`**：來源名稱表加 credit-lead「信用領先模型」、breadth「市場廣度模型」、calendar「日曆效應模型」；`LIST_LABEL` 加 own-board「擁有層前十五」、picks-late「爆發榜晚段（守門擋下）」、mech-nodd「無 DD 機械過閘」，個股脈搏名單計數改可點連結（v3 稿 §11.2 對照表）；`SCORE_MODULE_LABEL` 加 kelly_rule「Kelly 傾斜組合（paper）」；曝險區加第二條 NAV 線與小卡（E、edge、z、σ21、reason）；方法論折疊補一段白話講 Kelly 傾斜。
- **`docs/flowmap/index.html`** 來源名稱表加六個（三個模型＋三個名單）。
- **`.github/workflows/forecast-settle-weekly.yml`**：settle 之後加 `generate_credit_forecasts.py --write`、`generate_breadth_forecasts.py --write`、`generate_calendar_forecasts.py --write`（皆 `|| echo … continuing`）與三個 builder `--if-due`；PATHS 加 `data/credit_base_rates*.json`、`data/breadth_base_rates*.json`、`data/calendar_base_rates*.json`；`generate_list_forecasts.py --list all` 既有步驟自動含三個新名單。
- **`knowledge/rule_ledger.md`**：新增 7 條（credit-lead／breadth／calendar／kelly_rule／own-board／picks-late／mech-nodd；kill 皆＝SPRT accept_h0 → 砍；own-board／picks-late／mech-nodd 附 v3 稿 §11.3 註記）；**加一提刪一候刪提名：flowmap CTA 複合體尺規**（AUM 錨 $250bn 為自估、翻轉位無公開對帳；P3 換 CFTC TFF leveraged funds 前，先審其 flip level 事後命中）。

## §8 分包與檔案所有權（sonnet，並行、互不觸碰他人檔案；全部不 commit、不對真帳簿 `--write`）

| 包 | 擁有檔案 |
|---|---|
| G1 信用領先 | `scripts/build_credit_base_rates.py`、`scripts/generate_credit_forecasts.py`、`data/credit_base_rates*.json` |
| G2 市場廣度 | `scripts/build_breadth_base_rates.py`、`scripts/generate_breadth_forecasts.py`、`data/breadth_base_rates*.json` |
| G3 日曆效應 | `scripts/build_calendar_base_rates.py`、`scripts/generate_calendar_forecasts.py`、`data/calendar_base_rates*.json` |
| G4 resolver 擴充 | `knowledge/settle_forecasts.py`、`knowledge/README.md`、`scripts/build_macro_base_rates.py`、`scripts/harvest_macro_falsifiers.py`（僅 conditional_p 月頻分支＋LVL_BUCKET）、`scripts/harvest_kill_watch.py`、`data/macro_base_rates*.json`（--skip-fetch 不重建亦可） |
| G5 Kelly | `scripts/build_kelly_track.py`、`docs/market/data/kelly_track.json`、`.github/workflows/weekly-market-update.yml`、`scripts/score_flowmap.py`（kelly_rule 區） |
| G6 variance 快照 | `scripts/snapshot_variance.py`、`docs/catalyst/variance_history.json`、`.github/workflows/intel-2-daily.yml`（一行） |
| H1 選股名單 | `scripts/generate_list_forecasts.py`（v3 稿 §11.1） |
| G7 整合（後跑） | `scripts/build_market_state.py`、`docs/market/data/state.json`、`docs/market/index.html`、`docs/flowmap/index.html`、`.github/workflows/forecast-settle-weekly.yml`、`knowledge/rule_ledger.md` |

## §9 驗收（orchestrator）

1. 三個 builder 各產表，`p_clim` 非 null、桶 n 合理（信用／廣度 ≥ 200 取樣點；TOM n ≥ 240、假日前 n ≥ 180）；手算抽查一個桶。
2. 三個 generator dry-run 輸出合法 JSONL（`forecast_lib.finalize` 驗欄位）；calendar 以 `--as-of 2026-09-28` 應產 TOM 09-30 一張、以 `--as-of 2026-11-23` 應產感恩節一張。
3. `settle_forecasts.py --check-resolver internals:bei10y` 印 scale 與現值；對 scratch 帳簿放一張 `vs_base_date` 命題（過去日期）結算正確。
4. `harvest_kill_watch.py --p-mode conditional` dry-run 多出三張 internals 命題，p 與 p_clim 皆非 null。
5. `build_kelly_track.py` 以今日 state.json（edge 1.2pp）應得 E＝1.0、reason `no_edge`；手改 p 為 0.75 應得 E＞1 且 ≤ 1.5。
6. `snapshot_variance.py` 兩次執行檔案不變（冪等）。
7. `generate_list_forecasts.py --list all` dry-run：ownboard 15 候選（扣既有 open 者）、late ≥ 4（SIMO／HIMX／COHR／ALAB…）、nodd 0（誠實）。
8. G7 後：`build_market_state.py` 0 gap、第五磚 as_of＝2026-08-31（非 09-04）、council_summary spy_up_21d n_sources 隨新 producer 落帳後增加；本機 http.server 開 `/market/` 檢查曝險區與名單連結；`python3 scripts/qc.py`；三個 YAML 語法；`python3.9 -m py_compile` 全部新檔。

## §10 明確不做／待決

- **十倍股 5 席價格**：仍等 `data/weekly_cache_universe/` 首次 CI 落地；若仍不覆蓋（十倍母體為 $10–200 億小型股，多半不在 engine 母體），選項＝帳簿自有 `data/ledger_prices.json`（settle 班車對「relspy 命題引用但所有快取皆無」的 ticker 抓週線；新增資料層與 yfinance 依賴於 settle 班車，**需持有人核准**）。
- **選股側兩件待決**（對方交接，轉達持有人）：見 v3 稿 §11 開頭。
- **P3**：CTA 尺規換 CFTC TFF leveraged funds（本批已提名候刪審查）、dealer gamma、FOMC／CPI 日曆效應（需歷史事件日期源）、`epsdrift:` resolver。
- **macro 報告 refresh** 2026-10-08～10 到期（writer sonnet、orchestrator review）。
