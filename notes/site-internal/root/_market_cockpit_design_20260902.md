# 設計凍結稿 v3：市況主控台（market cockpit）＝市況分析與決策的合成層

- 日期：2026-09-02｜狀態：**持有人授權「由 orchestrator 推薦的決定執行，做完 commit & push」**（2026-09-02）。判斷在此凍結，sonnet 實作，orchestrator 整合驗收。
- 前稿：`_forecast_v2_design_20260902.md`（帳簿 v2，已 push）。視覺原型（真實數據）：Artifact「市況主控台」2026-09-02，sonnet 依原型實作。
- 憲法相容：**不是收斂面**（市場層狀態向量與 paper 規則，不產名單）；描述器紀律（公開頁只講機率與條件、不下買賣指令）；判斷類規則登 rule_ledger；成品白話依 `_plainlang_styleguide.md`。

## §0 三個拍板（orchestrator 推薦，持有人授權）

1. **六態曝險燈退役**：資料停在 2026-07-03、workflow 已停排程。頁面保留、加「已退役，由市況曝險規則（paper）接手」橫幅並連到 `/market/`；state.json 內標 `retired: true`。
2. **判讀必留命題**：monitor-read／detective-read／crowding-monitor／macro-analyst 每次判讀至少 1 條、至多 3 條帶 resolver＋p 的命題進帳簿；不留命題＝沒說話。共用機械腳本 `scripts/ledger_from_editorial.py` 驗 resolver、append、生哨兵 twin。**LLM／人的 p 由該判讀者自己給**（持有人 2026-09-02 授權不介入），不再經人工確認。
3. **市況曝險規則 v0（paper，PREREG）**：見 §4。上線即 paper 記分，SPRT 判綠前只顯示不執行；判紅即撤。

## §1 合成層：`docs/market/data/state.json`（schema `market-state-v1`，日更零 LLM）

`scripts/build_market_state.py` 只讀不算（所有數字來自既有 latest.json／帳簿／scorecard），輸出：

```json
{"schema":"market-state-v1","as_of":"<各層 as_of 最大值>","generated_at":"…",
 "components":{"monitor":{"as_of":"","stale":false},"detective":{},"flowmap":{},"statlab":{},"intel":{},"regime":{},"macro_clock":{},"crowding":{},"ledger":{},"scorecard":{},"exposure_track":{},"six_state":{"retired":true,"as_of":"2026-07-03"}},
 "environment":[{"key":"regime","label":"大類資產環境（regime）","value":"晚週期再通脹","sub":"美元見頂回落 · 六軸定性 0.63","as_of":"","cadence":"不定期","stale":false,"tone":"warn"}, "… macro_clock／detective／monitor／six_state 共 5 磚"],
 "council":[{"id":"","source":"","template":"","claim":"","p":0.66,"p_clim":0.65,"resolve_by":""}],
 "council_summary":{"spy_up_21d":{"p":0.66,"p_clim":0.65,"n_sources":2},"spy_up_63d":{},"vol_up_21d":{},"vol_spike_21d":{}},
 "flows":{"cta":[{"market":"SPX","proxy":"SPY","px":767.05,"composite":"+3/3","levels":[{"w":20,"level":757.67,"dist_pct":-1.24}],"full_flip_flow_bn":[20,40]}],
          "vol_control":{"exposure_pct":73,"rv_1m":10.3,"rv_3m":13.7,"ladder":[]},"lev_etf":{"shock_minus2_bn":{"SPX":-1.98,"NDX":-4.96,"SOX":-2.66}},
          "month_end":{"in_window":true,"direction":"sell_equity_buy_bond","bucket":"mid"},"buyback":{"peak_week":"2026-10-12"}},
 "fuses":[{"theme":"USFiscalDeficit","metric":"10Y/30Y 殖利率","now":"5.22%","threshold":"5.5%","dist_pct":4.9,"p":0.23,"resolve_by":"2026-10-08","link":""}],
 "anomalies":[{"key":"","msg":"","sev":""}],
 "stock_pulse":{"n_30d":33,"n_60d":0,"by_verdict_30d":{"進場":14,"觀望":18,"迴避":1},"since_v13":{"n":188,"進場":70,"觀望":113,"迴避":5},"fresh":true,"threshold":10},
 "exposure_rule":{"target":0.0,"factors":{"vol":1.0,"trend":1.0,"credit":1.0},"gates":{"core":"open","satellite_structural":"open","satellite_cyclical":"open"},"nav":100,"bench":{"spy":100,"b6040":100},"sprt":{}},
 "scoreboard":{"modules":{},"ledger_sources":{},"exposure_rule":{}},
 "triggers":[{"label":"SPY 收盤跌破","level":"757.7","why":"CTA 20 日窗翻空，SPX 複合體機械賣壓"},{"label":"SPY 已實現波動升破","level":"15.7","why":"波動控制基金曝險 73%→64%"},{"label":"10 年殖利率收上 · 期限溢價站上","level":"5.0% · 1.0%","why":"財政逆風被市場確認；帳上機率 30%／24%"}],
 "read_zh":{"headline":"…","bullets":["…"]},
 "freshness":[{"pipeline":"monitor 跨資產監測","as_of":"","cadence":"日更","status":"ok|warn|stale"}],
 "gaps":[]}
```

**凍結規則**：
- `council`＝forecasts.jsonl 中 status=open、source ≠ sentinel-noise、source ≠ dd-verdict 的本尊（dd 進 stock_pulse 不進議會）。`council_summary` 聚合＝同 template 各 source 的 p 簡單平均（Tetlock 議會；template 對應：spy_up_21d ← tsmom SPY＋vrp_spy_up_21d；spy_up_63d ← vrp_spy_up_63d；vol_up_21d ← rv21_higher_21d；vol_spike_21d ← rv21_touch_plus5_21d），p_clim 同法平均。
- `stock_pulse.fresh` ＝ n_60d ≥ 10（PREREG 暫定，2026-10 校準輪複審）；不新鮮時 `read_zh` 個股句改為「個股層無新資料，本期不判讀」。
- `triggers` 三條機械規則：①SPY 最近 CTA 翻轉位（flowmap cta SPX nearest_flip_level）；②vol-control 階梯下一階 rv；③帳上 p 最高的總經證偽命題（macro-falsifier open 中 p 最大者，含 p）。
- `read_zh` 為模板句（無 LLM）：headline＝「接下來一個月 SPY 收高機率 {p}%（基準 {clim}%）＝{無邊際|略偏多|略偏空}；波動升高機率 {p}%（基準 {clim}%）；下方 {dist}% 有機械賣壓；三個月 {p}%（基準 {clim}%）。」判定詞：|p−clim| < 5pp → 無邊際；≥5pp 依方向。bullets 依序：環境分歧句、流量不對稱句、引信句（p 最高者）、個股脈搏句（含新鮮度）、記分板句（幾綠幾黃幾紅、哨兵狀態）。全形標點。
- stale 判定：日更管線 as_of 落後今日 > 4 天、週更 > 10 天、月頻 > 45 天、regime > 30 天；六態固定 stale＋retired。
- 缺檔不 crash：該塊 null＋gaps 記錄。

## §2 頁面 `docs/market/index.html`＋入口

- 依 Artifact 原型（六塊：今日讀法／環境五磚／預測議會 dumbbell＋機械賣家價格梯／引信距離＋今日異常＋個股脈搏／三個觸發數字／記分板＋新鮮度），fetch `data/state.json` 渲染；樣板（nav／頁首／CSS token／字體）照抄 `docs/flowmap/index.html`；noindex **不加**（本頁是市場群正式入口）。
- 新增區塊「市況曝險規則（paper）」：目標曝險、三因子、三軌新倉閘、NAV 對兩個基準的小折線（exposure_track.json）、SPRT 狀態；標題旁標「paper · 未證明前只顯示不執行」。
- nav：`scripts/site_nav.py` 市場群加 `("market", "/market/", "市況主控台")` 置於情報監視器之前；`PREFIX_ACTIVE` 映射 `market/`。重跑 nav 注入（依 site_nav 既有流程）。
- 首頁 `docs/index.html` 「市場現況」區標題右側加連結「市況主控台 →」（一行，不改四磚）。
- `docs/six-state/index.html` 頂部加退役橫幅（一段白話＋連結 `/market/`）。
- 白話：依 styleguide 四句式；術語首現括號；描述器聲明固定在 footer。

## §3 判讀必留命題（skills，orchestrator 自改）

- editorial.json 新欄 `forecasts[]`：`[{"claim":"","p":0.3,"horizon_days":30,"resolver":{"series":"monitor:hy_oas","op":">","value":3.0,"window":"any_close"},"why":"一句白話理由"}]`（monitor-editorial-v1／detective-editorial-v1 additive）。
- `scripts/ledger_from_editorial.py --source monitor-read|detective-read|crowding-monitor --file <json> [--write]`：驗 resolver（`settle_forecasts.check_resolver`）、查重（同 source 同 claim 30 天內）、p_clim（monitor 五個 FRED key 用 `build_macro_base_rates.climatology`；pxd／price 方向命題用該價格快取近 2 年同 horizon 無條件上漲頻率；其餘 None）、episode_id=`{source}:{as_of}:{序號}`、append＋哨兵 twin。
- crowding-monitor：每期報告另存 `knowledge/editorial_drafts/crowding_{YYYYMMDD}.json`（同 schema，named trades 的 unwind 觸發器數值化），跑同一腳本。（原擬放 `docs/crowding/data/` 與該 skill「不動 pipeline 疆界」硬規則衝突，改放 knowledge/。）
- macro-analyst：發稿流程加一步 `python scripts/harvest_macro_falsifiers.py --p-mode conditional --write`（條件式歷史頻率法機械化，見 v2 §9）。
- kill（登 rule_ledger）：各判讀 source 同 SPRT 條款；正面義務：判讀無命題視為未完成。

## §4 市況曝險規則 v0（paper，PREREG 凍結至判決或 24 個月）

- 週頻：每週六 weekly-market-update 班車以週五收盤算，週一生效；inception 2026-09-07，NAV=100；`scripts/build_exposure_track.py` → `docs/market/data/exposure_track.json`（prereg 逐字＋nav_series＋factors_history）。
- 資料：SPY／AGG 日線＝`data/flowmap_prices.json`；HY OAS 21 交易日變化＝`docs/monitor/data/latest.json` hy_oas spark（百分點）。
- 因子：
  - vol＝clip(0.15 / RV_blend, 0.25, 1.0)，RV_blend＝0.5×RV21＋0.5×RV63（SPY 日對數報酬年化 %，口徑同 rv-model）；
  - trend＝1.0 若 SPY 12-1 動能（t−252 至 t−21 總報酬）> 0，否則 0.5；
  - credit＝0.5 若 HY OAS 近 21 交易日上升 > 0.50 個百分點，否則 1.0。
- 目標曝險＝clip(vol × trend × credit, 0.25, 1.0)；其餘現金 0%。基準：SPY buy-and-hold；60/40（SPY／AGG，月初再平衡）。
- 三軌新倉閘（寫進 state.json，PM 讀為輸入之一，非指令）：core 恆「open」；satellite_structural：目標曝險 ≥ 0.5 →「open」否則「caution」；satellite_cyclical：trend=1.0 且 credit=1.0 且 RV21 < 19.93（rv 表 Q5 切點）→「open」否則「closed」。
- 記分：月樣本＝當月 paper 報酬 − SPY B&H 報酬 > 0 為命中；SPRT 同 v2 參數；另列 Sharpe／MaxDD 對兩基準（資訊欄）。scorecard 加 `exposure_rule` 區。
- kill（登 rule_ledger）：SPRT accept_h0 → 規則撤下、閘回「僅顯示無規則」；期間不調參；paper only 永不連實倉。

## §5 intel 新聞 LLM 進淘汰賽（source `intel-llm`）

- `scripts/intel/prompts/brief.md` 追加輸出欄 `claims`（0–2 條）：`{claim, p, horizon_days(7–90), resolver{series, op, value, window}}`，series **白名單**：`monitor:dgs10|dgs30|hy_oas|tp10y|sofr_iorb`、`pxd:SPY|QQQ|IWM`、`vixts:SLOPE`；prompt 明講「resolver 寫不出就不要提」。`summarize.py` 解析並驗白名單，存進當日 JSON `claims[]`（壞格式丟棄不 crash）。
- `scripts/harvest_intel_claims.py --write`（掛 forecast-settle-weekly，settle 之後）：讀近 7 日 intel JSON，驗 resolver、查重（同 claim 文 30 天）、p_clim（同 §3 規則）、episode_id=`intel:{date}:{n}`、append＋twin。
- kill（登 rule_ledger）：SPRT accept_h0 → 拿掉 prompt 欄；另 180 天 claims 總數 < 20 → 儀式化認定撤下。

## §6 分包與檔案所有權

| 包 | 擁有檔案 |
|---|---|
| E1 state builder | 新 `scripts/build_market_state.py`、`docs/market/data/state.json`、新 `.github/workflows/market-state-daily.yml`（cron `30 8 * * 2-6`；另在 `forecast-settle-weekly.yml` 末尾加一步 build_market_state＋PATHS——此檔由 E5 擁有，E1 只提供 step 文字給 orchestrator 合併） |
| E2 page | 新 `docs/market/index.html`、`scripts/site_nav.py`（加一條目）、`docs/index.html`（市場現況區加一連結）、`docs/six-state/index.html`（退役橫幅） |
| E3 exposure track | 新 `scripts/build_exposure_track.py`、`docs/market/data/exposure_track.json`、`.github/workflows/weekly-market-update.yml`（加一步）、`scripts/score_flowmap.py`（加 exposure_rule 區＋讀 exposure_track）、`knowledge/rule_ledger.md`（§3／§4／§5 三組 kill 登記） |
| E5 LLM 命題 | `scripts/intel/prompts/brief.md`、`scripts/intel/summarize.py`、新 `scripts/harvest_intel_claims.py`、新 `scripts/ledger_from_editorial.py`、`scripts/harvest_macro_falsifiers.py`（`--p-mode conditional`）、`.github/workflows/forecast-settle-weekly.yml`（加 harvest_intel_claims 與 build_market_state 兩步＋PATHS） |
| orchestrator | 四個 read／macro skill 條文、memory、整合驗收、commit & push |

## §7 驗收

1. `build_market_state.py` 產出 state.json 全塊非 null（缺檔測試：暫改路徑 → gaps 記錄不 crash）；read_zh 與原型同義。
2. `/market/` 在本機 http.server 渲染六塊＋曝險區；nav 出現；首頁連結；六態橫幅。
3. `build_exposure_track.py` 產 inception 列；factors 與手算一致（RV21／RV63／12-1／HY 21d 變化）。
4. `ledger_from_editorial.py` 對一份含 2 條命題的測試 editorial dry-run／write（scratch ledger）；`harvest_intel_claims.py` 對含 claims 的假 intel JSON 同上；`harvest_macro_falsifiers.py --p-mode conditional` 六筆 p 與 v2 §9 手算一致。
5. score_flowmap 產 exposure_rule 區；qc.py；YAML 合法；py3.9 編譯。

## §8 站上資產掃描後的接線順序（2026-09-02 掃描；持有人授權依 orchestrator 推薦執行，列為 v3 之後的下一批）

掃描結論：站上已有四個「自帶 base rate 或 track record」的機械件，與一個已結構化的 kill 門檻件，全部可用既有 resolver 域接進帳簿，零新資料源。順序依「有歷史勝率、有 as_of、有唯一鍵」三條件排：

| 序 | 件 | 命題模板 | resolver | p 來源 | 阻塞 |
|---|---|---|---|---|---|
| 1 | **sop-funnel 板機訊號**（`docs/dd-screener/sop-funnel/latest.json`＋`ledger.json`，日更） | 「{ticker} 板機訊號後 91 天跑贏 SPY」 | relspy: | 自家 5 年回測 `backtest.json` charter win_rate 64.2%（n=53）→ p；p_clim 用 dd 宇宙表 | 無；每個訊號有日期＋ticker 唯一鍵 |
| 2 | **engine GRP 席位**（`docs/engine/arena.json` core_seats／sat_seats，週日更） | 「本週 GRP 核心席位 {ticker} 91 天跑贏 SPY」（衛星同） | relspy: | `scoreboard.json` by_verdict 統計 → PREREG offset；p_clim 同上 | 無；episode＝ticker×席位週 |
| 3 | **精選榜／十倍股名單**（`docs/picks/candidates.json`、`tenbagger.json`，週更） | 「本週精選榜新進 {ticker} 91 天跑贏 SPY」 | relspy: | PREREG offset（無自家勝率） | 名單覆寫無快照 → producer 落帳即是快照 |
| 4 | **kill_watch 引信**（`docs/detective/data/kill_watch.json`，12 條 macro／ID／DD 門檻，含 monitor data_source／op／current，週更） | 「{metric} 90 天內觸及 {threshold}」 | monitor: | FRED 五序列用 climatology；其餘 p_clim=None（raw Brier）；p 由 orchestrator 條件頻率法或判讀者給 | 非 monitor 序列者不落帳；市況主控台引信區同時顯示這 12 條 |
| 5 | **risk_gauge 週序列**（`docs/cache/risk_history.json`，1,345 週 score／spx／nfci／vix） | 「SPY 13 週後更高」條件於風險分數五分位 | pxd:SPY | 自建 25 年條件表（月度取樣） | 無；是最長的一條本站序列 |
| 6 | **RRG 類股象限**（`docs/rotation/data/radar.json`，日更） | 「{sector ETF} 63 天跑贏 SPY」條件於象限 | relspy: | 自 statlab 3 年 sector 價格自建象限條件表（樣本薄，標 lo） | 11 檔 × 月＝breadth 加成 |
| 7 | catalyst variance 漂移（`docs/catalyst/variance.json` drift_pct） | 「{ticker} FY+1 共識 EPS 90 天內漂移轉 🔴」 | 新域 epsdrift: | 無歷史 → raw Brier | 需先每週存快照 |

**不接／延後**：P10 動能 paper track（prereg 明文禁止被引用，NAV 已自帶記分）；long-track／turtle-sleeve 家族（已有 replay 記分，與實單系統相鄰，不進帳簿）；entry-state（資料停在 2026-07-05，先修管線）；comparisons／weekly（停更）；DD／ID 文字型 kill 門檻（由 kill_watch 已結構化者代表，其餘不機械化）。

**掃描順帶發現**：crowding 週更已併入 crossasset-weekly（週日），COT 最新 2026-08-18 為 CFTC 延遲非管線停擺；dd-screener 四個子篩（alpha-rank／breakout／bottom-out／earnings-acceleration）依 CLAUDE.md 為已封存頁，非過期；`docs/track-record` 已是 DD 裁決對 SPY 的回顧記分板，dd-verdict producer 的經驗表日後改讀它的 cohort 統計而非 settlement.json。
