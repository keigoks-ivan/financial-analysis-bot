# 設計凍結稿 v2：預測系統從「可預測物件」轉向「方向命中率」

- 日期：2026-09-02｜狀態：**持有人已核准方向（2026-09-02），本稿為逐項凍結，發包 sonnet 實作**
- 前稿：`_flowmap_forecast_ledger_design_20260901.md`（v1，全部上線）。本稿只寫「差異與新增」，v1 未被本稿改動的條文仍有效。
- 憲法相容性不變：不是收斂面、描述器紀律、判斷類規則登 rule_ledger、成品白話（`_plainlang_styleguide.md`）。
- 發包規則：實作＝sonnet；本稿凍結的門檻／公式／kill 條款 sonnet 不得改；驗收＝orchestrator。

---

## §0 審視結論（判斷紀錄，供追溯；持有人 2026-09-02 核准）

終極目標＝提高「預測股市走勢」的成功率。v1 系統對此目標的問題，一句話：**它預測的東西（流量／波動／期限結構）與方向命中率之間沒有任何一條被量測的連接線**。五項裁決：

1. **目標函數**：方向命題的 Brier skill score，基準＝該命題型別的無條件歷史頻率（p_clim），附 block-bootstrap 信賴區間；另以機率建 Kelly 縮放 paper 組合對 buy-and-hold（本批只落 BSS，paper 組合列下一批）。
2. **breadth**：trend-track 每月 9 檔、VRP、DD 裁決全部轉成機率命題進帳簿。Grinold 的 IR = IC × √breadth 判死的是「單一指數點位」，不是「方向」；breadth 是唯一免費槓桿。
3. **kill 機制**：固定 n 二項檢定改為 SPRT 序貫檢定（處理反覆偷看），自相關樣本以 episode 計有效樣本。
4. **flowmap**：降為條件層與解讀層；vol-control 改描述器（無可對帳的公開流量資料）；CTA 尺規換 TFF leveraged funds 列下一批。
5. **macro 草案**：先擱置到記分修完；帳簿內 macro 層本批升級（p_clim 自 FRED 歷史、單位正規化、p 由 orchestrator 依 base rate＋stance 賦值後持有人確認）。macro 報告本身不重寫（refresh_due 2026-10-08～10 到期時走 refresh，見 §10）。

**一項自我更正**：審視稿曾指「p 表 in-sample 且季度重建納入新資料，前 20 筆是自己對自己打分」。實際上每筆 forecast 的 p 來自落帳當時的表，表的 data_end ≤ ts，結果在表之外，屬樣本外。真正需要的只是把表版本戳進 forecast（`p_table_built_at`），本稿照此處理，不再誇大。

**具體 bug（審視時實測）**：monitor `sofr_iorb` 的 `val` 顯示 `3bps` 而 `spark` 值為 `0.03`（百分點），settle 讀 spark，故 macro 草案門檻 5.0 永不成立。本稿 §4 以單位正規化根治。

---

## §1 目標函數（凍結）

- **主指標**：每個 source 的 BSS = 1 − mean(Brier_i) / mean(Brier_clim_i)，其中 Brier_i = (p_i − y_i)²、Brier_clim_i = (p_clim_i − y_i)²。**p_clim 是逐筆的**，不是該 source 的 in-sample 結果頻率（v1 的做法廢除）。
- **有效樣本 n_eff**＝resolved 集合中 distinct `episode_id` 數；所有「≥20 筆」門檻一律改讀 n_eff。
- **決策指標**＝SPRT（§3.3）；BSS 與其 90% block-bootstrap CI 為資訊欄，不做決策。
- 無 p_clim 的筆（p_clim=null）只計 raw Brier，不進 BSS／SPRT。

## §2 帳簿 schema v2（`knowledge/forecasts.jsonl`，additive）

每筆新增欄位（既有 13 欄不動）：

| 欄位 | 型別 | 定義 |
|---|---|---|
| `schema` | str | `"fc-v2"`（舊筆 migration 時補） |
| `claim_template` | str | 命題型別 id，見各 producer 段；人工落帳為 `manual`／`macro_threshold` |
| `p_clim` | float\|null | 該命題型別的無條件歷史頻率（定義見各 producer 段） |
| `p_clim_ref` | str\|null | p_clim 來源描述（表檔＋built_at＋窗口） |
| `p_table_built_at` | str\|null | 賦 p 所用 base-rate 表的 built_at（人工賦 p 為 null） |
| `episode_id` | str | 有效樣本計數單位（定義見各 producer 段） |
| `block_key` | str | block-bootstrap 分塊鍵＝`YYYY-MM`（預設 ts 所在月；producer 可自帶，dd-verdict 用裁決月，`finalize` 不覆寫已設定值——2026-09-02 整合定案） |
| `twin_of` | str\|null | 哨兵筆指向本尊 id；本尊為 null |

Migration：既有 2 筆 rv-model 補齊上表（p_clim 自重建後的 rv_base_rates.json pooled 頻率；episode_id=`rv:2026-09`；block_key=`2026-09`）；並為其產生哨兵 twin（§3.4）。migration 由 `knowledge/forecast_lib.py --migrate` 一次性執行，冪等。

結算回寫（settle）新增每筆：`brier_clim`（float\|null）、`beat_clim`（bool\|null；Brier_i < Brier_clim_i；相等為 null）。

## §3 記分方法（凍結）

### 3.1 p_clim 定義原則
「同一命題、把條件拿掉之後的歷史頻率」。同一 producer 的表檔必須同時輸出條件頻率（p 來源）與無條件頻率（p_clim 來源），兩者用**同一窗口、同一取樣點**算。

### 3.2 forecast_settlement.json 新增 `sources` 摘要（A2 只讀不算）
```json
"sources": { "<source>": {
  "n_resolved": 0, "n_eff": 0, "n_with_clim": 0,
  "mean_brier": null, "mean_brier_clim": null, "bss": null, "bss_ci90": [null, null],
  "sprt": { "p0": 0.5, "p1": 0.65, "alpha": 0.05, "beta": 0.10, "A": 2.8904, "B": -2.2513,
            "llr": 0.0, "n_used": 0, "state": "continue|accept_h1|accept_h0", "decided_at": null, "decided_n": null },
  "status": "yellow|green|red", "status_label": "…（白話）",
  "calibration_buckets": [ {"bucket":"[0-10%]","n":0,"avg_p":null,"freq":null} ]
} }
```
哨兵 source（`sentinel-noise`）同樣一筆摘要。

### 3.3 SPRT 序貫檢定（所有 kill 決策的唯一機制；PREREG 凍結）
- 樣本序列：producer source＝每筆 resolved 且 `beat_clim` 非 null 的 `beat_clim`（依 resolved_ts 升冪）；hit-rate 模組（flowmap CTA／月末）＝每筆 `hit`（依樣本日期升冪）。
- 參數：H0 命中率 p0 = 0.50；H1 p1 = 0.65；α = 0.05；β = 0.10。上界 A = ln((1−β)/α) = ln(18) = 2.8904；下界 B = ln(β/(1−α)) = ln(0.1/0.95) = −2.2513。
- 每樣本 LLR 增量：命中 +ln(0.65/0.50) = +0.26236；未命中 +ln(0.35/0.50) = −0.35667。
- 決策：n_eff < 20 一律 `continue`（🟡）；n_eff ≥ 20 且累積 LLR ≥ A → `accept_h1`（🟢）；≤ B → `accept_h0`（🔴＝kill 門檻觸發，舉旗待校準輪處決）；否則 `continue`（🟡）。
- 決策一旦落定即**鎖存**（記 decided_at／decided_n），之後樣本繼續累計顯示但狀態不變；只有校準輪可重設（rule_ledger 註記）。
- 揭露義務：每次輸出附「在 p 為真值 0.60 時預期需約 200 樣本才會判綠、無技巧時約 50 樣本判紅」的白話說明；並附同時受檢 source／模組數與預期假綠數（= 數目 × α）。不做 BH 校正（序貫檢定不適用），以哨兵為經驗對照。

### 3.4 哨兵 source（`sentinel-noise`）
- 每一筆 producer 落帳（rv／vix／cot／tsmom／vrp／dd-verdict／macro-falsifier）同時 append 一筆 twin：`id = {id}_sn`、`source = "sentinel-noise"`、`twin_of = id`、claim／resolver／resolve_by／horizon／episode_id／block_key／claim_template／p_clim 全同本尊，**p = clip(p_clim + ε, 0.05, 0.95)**，ε ~ N(0, 0.15)，seed = int(sha256(id).hexdigest()[:8], 16)，用 `random.Random(seed).gauss(0, 0.15)`。p_clim 為 null 時不生 twin。
- 期望性質：真技巧為零且帶雜訊，期望 BSS < 0。**哨兵判綠＝記分壞掉；哨兵遲遲不判紅＝淘汰機制無力**。兩個方向都要看。
- 哨兵不計入任何「本站預測」數字、不進其他 source 的 n_eff；成績單獨立一列。

### 3.5 block-bootstrap CI（資訊欄）
以 `block_key` 分塊整塊重抽，2000 次，seed 20260902，取 5／95 百分位為 `bss_ci90`。n_eff < 20 不算（null）。

### 3.6 q.py --forecasts 輸出
沿用現有版面，每 source 段改列：n_resolved／n_eff／mean Brier／mean Brier_clim／BSS [CI]／SPRT 狀態（LLR、n_used、state）／校準 10 桶；哨兵段獨立。旧「climatology＝in-sample 結果頻率」文字刪除。

## §4 resolver 新域與單位正規化（`knowledge/settle_forecasts.py`）

### 4.1 monitor 域單位正規化（根治 sofr_iorb）
- scale = parse(item.val) / spark[-1]（兩者皆非 0 時）；若 scale 落在 {0.01, 0.1, 1, 10, 100, 1000} 任一值的 ±5% 內取該值，否則 void，reason=`unit_ambiguous:{key}`。
- 比較時 threshold_spark = resolver.value / scale。resolver.value 維持「顯示單位」（人讀得懂：5 = 5bp）。
- `--check-resolver monitor:<key>` 印出：顯示值、spark 尺度、scale、以及「value 若寫 X 會被換成 X/scale 比對」。
- 兩者皆為 0 或 spark 空 → 沿用舊行為（不換算）並在 note 標 `unit_scale_unknown`。

### 4.2 `ttp:<TICKER>`（trend-track 價格快取）
讀 `data/trend_track_prices.json`（與 flowmap_prices 同構）日線收盤；語義與 `pxd:` 完全相同（at_expiry＝resolve_by 當日或之前最近收盤；any_close＝區間內任一收盤）。

### 4.3 `relspy:<TICKER>`（相對 SPY）
resolver 形態：`{"series":"relspy:NVDA","op":">","value":0,"window":"at_expiry","base_date":"YYYY-MM-DD","base_px":123.4,"base_spy":567.8}`。
結算：px_T＝`data/weekly_cache/<ALIAS(TICKER)>.json` resolve_by 當日或之前最近收盤（照 settle_outcomes.py 的 `_close_at_or_before`）；spy_T＝`data/flowmap_prices.json` SPY 同規則；outcome = 1 若 (px_T/base_px − spy_T/base_spy) > value。只支援 at_expiry。缺任一價 → void，reason=`relspy_missing_price:{TICKER}`。

### 4.4 結算輸出
每筆回寫 `brier_clim`／`beat_clim`；`forecast_settlement.json` 加 §3.2 `sources`；schema 升 `forecast-settlement-v2`。

## §5 producers

### 5.0 共用：`knowledge/forecast_lib.py`（A1 交付；B/C/D/M 依此 API 寫）
```python
# 由 scripts/*.py 這樣載入（knowledge/ 無 __init__）：
#   sys.path.insert(0, str(ROOT / "knowledge")); import forecast_lib as fl
fl.next_ids(ts_str, prefix, n, path)        # 沿用各 producer 既有規則：fc_{YYYYMMDD}_{prefix}_{NN}
fl.finalize(drafts)                          # 補 schema="fc-v2"、block_key、驗欄位齊、回傳 drafts（不寫檔）
fl.make_sentinel_twin(draft) -> dict|None    # §3.4
fl.append(drafts, path=FORECASTS, write=False) -> (n_written, n_twins)   # write=False 只印 JSONL 到 stdout；write=True append 本尊＋twin
fl.existing(path) -> list[dict]
fl.migrate(path)                             # 一次性補舊筆欄位＋twin；冪等
```
所有 producer：dry-run 預設、`--write` 落帳、查重規則各自沿用、stdout 只印 JSONL、訊息進 stderr。

### 5.1 既有三 producer retrofit（A1）
- `build_rv_base_rates.py`：每模板加 pooled 無條件頻率 → JSON 頂層 `p_clim: {"rv21_higher_21d": x, "rv21_touch_plus5_21d": y}`；`--skip-fetch` 重建。
- `build_vixts_base_rates.py`：加 `p_clim: {"vixts_recover_21d": 任一交易日起 21 交易日內 slope>0 的無條件頻率（全樣本日取樣）, "spy_up_63d": 任一交易日起 63 交易日後 SPY 更高的無條件頻率}`。
- `build_cot_base_rates.py`：加 `p_clim: {"px_up_20d": {"SPY":..,"QQQ":..,"IWM":..}, "px_down_20d": {...}}`（自建 6 年快取全日取樣）。
- 三個 generate_*：改用 forecast_lib；填 `claim_template`（rv：`rv21_higher_21d`／`rv21_touch_plus5_21d`；vix：`vixts_recover_21d`／`spy_up_63d_after_onset`；cot：`cot_reversal_20d`）、`p_clim`（cot 依方向取 up／down）、`p_clim_ref`、`p_table_built_at`、`episode_id`（rv：`rv:{YYYY-MM}`；vix：onset 日，但若距前一筆 vix-model onset ≤ 63 交易日則沿用前一筆 episode_id；cot：`cot:{code}:{run_start_week}`，run＝連續極端週的第一週，需回看 cot_history 判 run 起點）。

### 5.2 tsmom producer（B）— `claim_template = "tsmom_up_21d"`
- `scripts/build_tsmom_base_rates.py`：自建 `data/tsmom_base_rates_raw_cache.json`（9 檔＋PDBC，各抓 20 年日線，yfinance→stooq，慣例照抄 build_rv_base_rates）。取樣點＝每月首個交易日；訊號＝t−252 至 t−21 總報酬 > 0（與 build_trend_track.py 定義逐字一致）；結果＝t 後第 21 個交易日收盤 > t 收盤。輸出 `data/tsmom_base_rates.json`：per ticker × state(in_trend/not) 的 freq_up、n；pooled（全 9 檔）同表；`p_clim` per ticker＝該 ticker 全取樣點無條件 freq_up。cell n < 30 → producer 用 pooled 同 state。`--if-due` 85 天。
- `scripts/generate_tsmom_forecasts.py`：每月首個交易日（查重：同 ticker 同 YYYY-MM 拒）；資料＝`data/trend_track_prices.json`（現價與 12-1 訊號自算，不讀 track.json 的簿記）；DBC 不足時 PDBC（照 build_trend_track 規則）。每檔一筆：claim「{resolve_by} 前（21 個交易日後）：{ticker} 收盤高於今日 {close}」；resolver `ttp:{ticker}` `>` value=今收 at_expiry；horizon 30 曆日；p＝表；episode_id=`tsmom:{YYYY-MM}:{ticker}`。

### 5.3 VRP producer（C）— `claim_template = "vrp_spy_up_21d"`／`"vrp_spy_up_63d"`
- 定義：VRP_t = VIX_t² − RV21_t²，VIX 為 ^VIX 收盤（年化隱含波動 %），RV21 為 SPY 對數報酬 21 交易日年化 %（口徑逐字同 build_rv_base_rates）。
- `scripts/build_vrp_base_rates.py`：自建 `data/vrp_base_rates_raw_cache.json`（^VIX、SPY 各 10 年）；取樣點＝每月首個交易日；三分位切點＝取樣點 VRP 的 33.3／66.7 百分位（in-sample，誠實註記）；輸出 per tercile：freq_up_21d、freq_up_63d、n；`p_clim`＝無條件 freq_up_21d／freq_up_63d。`--if-due` 85 天。
- `scripts/generate_vrp_forecasts.py`：每月首個交易日兩筆（查重同月拒）；當前 VRP 自 `data/statlab_prices.json`（^VIX、SPY）算；resolver `pxd:SPY` `>` value=今收 at_expiry；horizon 30／91 曆日；episode_id=`vrp:{YYYY-MM}`（兩筆共用）。

### 5.4 DD 裁決 producer（D）— `claim_template = "dd_beat_spy_91d"`／`"dd_beat_spy_365d"`
- 來源：`knowledge/decisions.jsonl`，`kind=decision`、`entity_type=company`、`verdict ∈ {進場, 觀望, 迴避}`、`date ≥ 2026-06-22`。命題一律為「跑贏 SPY」（觀望／迴避的 p 較低即可）。
- p（PREREG，假設本身就是受測命題）：p = clip(p_clim + offset, 0.05, 0.95)，offset 進場 +0.08／觀望 −0.04／迴避 −0.10，兩個 horizon 同 offset。
- `scripts/build_dd_verdict_base_rates.py`：(a) `p_clim`：對 `data/weekly_cache/` 全部 ticker × 每月首個週線日（近 5 年），算「91 曆日後／365 曆日後跑贏 SPY」pooled 頻率（SPY 自建 `data/dd_verdict_base_rates_raw_cache.json` 10 年日線）；(b) 經驗表：自 `knowledge/settlement.json` 對已到期 h91／h365 的 verdict 筆算 per verdict 跑贏 SPY 頻率與 n（現在 n=0，隨時間自填）。輸出 `data/dd_verdict_base_rates.json`。producer 只用 (a)＋PREREG offset；CONFIG `USE_EMPIRICAL_TABLE = False`，只有校準輪可翻（進化只在校準輪）。`--if-due` 85 天。
- `scripts/generate_dd_verdict_forecasts.py`：掃 decisions.jsonl 未落帳者（查重鍵＝decision id × template）；每筆兩個 horizon；resolver §4.3（base_px＝`price_at_decision`；base_spy＝flowmap_prices SPY 於 decision date 當日或之前收盤）；resolve_by ＝ date + 91／365 曆日，已過期者不落帳（只落 resolve_by ≥ today）；ts＝落帳當日（非 decision date），note 記 decision date；episode_id=`dd:{ticker}:{decision YYYY-MM}`；block_key＝decision YYYY-MM。ticker 不在 weekly_cache（含 ALIAS）→ 跳過並印原因。

### 5.5 macro 證偽表 producer 升級（M）— `claim_template = "macro_threshold"`
- `scripts/build_macro_base_rates.py`：維護 `data/macro_base_rates_raw_cache.json`（FRED 全史：DGS10、DGS30、BAMLH0A0HYM2、THREEFYTP10、SOFR、IORB；sofr_iorb ＝ (SOFR − IORB) × 100 bp，自 2021-07-29 起；抓法照 build_monitor.fetch_fred 但不切 400 筆）。提供函式 `climatology(key, op, delta, horizon_days) -> {"p": float, "n": int, "window": "..."}`：以近 20 年（不足取全部）每個交易日 t 為起點，H_td = round(horizon_days × 252/365)，any_close：">" 看 max_{1..H_td}(x) − x_t ≥ delta；"<" 看 min − x_t ≤ delta（delta 帶號＝門檻 − 現值）。輸出 `data/macro_base_rates.json` 只存 meta（各序列起訖、n），climatology 由 harvest 即時呼叫。`--if-due` 85 天。
- `scripts/harvest_macro_falsifiers.py`：每筆草案填 `p_clim`（climatology，delta＝門檻 − monitor 現值，單位換算成 FRED 序列單位：dgs10/dgs30/hy_oas/tp10y 為 %、sofr_iorb 為 bp）、`p_clim_ref`、`claim_template`、`episode_id=macro:{slug}:{metric}`、`block_key`；resolver.value 維持顯示單位（settle §4.1 正規化）；note 對 tp10y 加註「monitor tp10y＝FRED THREEFYTP10（Kim–Wright 口徑），非 NY Fed ACM」。新增 `--p-file p.json`（`{source_ref: p}`），`--write` 只落有 p 的草案（其餘仍 need_human_p 跳過）。
- p 賦值程序：orchestrator 依 p_clim＋報告 stance 提案並附推理，持有人確認後 `--write --p-file`。

## §6 flowmap 成績單與治理（A2）

- `scripts/score_flowmap.py`：CTA／月末改 SPRT（§3.3，hit 序列；沿用既有樣本定義不動）；移除 α=0.10 二項檢定；`rv_model` 段改為 `ledger_sources`＝逐字複製 `forecast_settlement.json.sources`（含哨兵）；新增 `vol_control: {"status":"descriptor","status_label":"描述器，不評分（無可對帳的公開流量資料）"}`；meta 加 `multiplicity: {"n_tested": N, "alpha": 0.05, "expected_false_green": N×0.05}`；schema 升 `flowmap-scorecard-v2`。
- `docs/flowmap/index.html` 成績單段：渲染 SPRT 三態＋ledger_sources 卡片。白話名（首現括號原名）：rv-model→「波動率模型」、vix-model→「VIX 期限結構模型」、cot-model→「COT 極端部位模型」、tsmom→「趨勢方向模型」、vrp→「波動風險溢酬模型」、dd-verdict→「個股裁決」、macro-falsifier→「總經證偽表」、sentinel-noise→「哨兵（無技巧對照組）」。狀態白話：🟢「已證實優於基準」🟡「證據累積中（有效樣本 n／決策需累積 LLR）」🔴「已證實不優於基準，等校準輪處決」。方法論折疊補一段白話講 SPRT 與哨兵。全形標點；讀 `_plainlang_styleguide.md`。
- `knowledge/rule_ledger.md`：2026-09-01／02 段 7 條 kill 的檢定文字改為「SPRT（p0 0.5／p1 0.65／α 0.05／β 0.10，n_eff ≥ 20）accept_h0 → 舉旗」；vol-control 條改「描述器，無行為 kill，只掛資料層 kill（RV 連 4 週算不出→gaps）」並註明改列日期與理由；新增 4 條：tsmom producer／vrp producer／dd-verdict producer／macro-falsifier source（kill 皆＝SPRT accept_h0 → 砍；dd-verdict 另加「PREREG offset 假設若 accept_h0，代表裁決對 3 月相對報酬無資訊，回饋 2026-10 校準輪」）；哨兵以註記登記（非規則）。加一提刪一候刪提名：**flowmap 月末再平衡模組**（理由：月頻 8 樣本／年，SPRT 下無技巧亦需約 6 年才能判紅，等於不可證偽；供持有人審視）。
- `.github/workflows/forecast-settle-weekly.yml`：settle 之後加 `generate_tsmom_forecasts.py --write`、`generate_vrp_forecasts.py --write`、`generate_dd_verdict_forecasts.py --write`（皆 `|| echo … continuing`），加三個 builder `--if-due`（tsmom／vrp／dd_verdict；macro builder 亦 `--if-due`），PATHS 加新 data 檔（`data/tsmom_base_rates*.json`、`data/vrp_base_rates*.json`、`data/dd_verdict_base_rates*.json`、`data/macro_base_rates*.json`）。macro harvest 不上 cron（p 為人工）。

## §7 分包與檔案所有權（並行，互不觸碰他人檔案）

| 包 | 模型 | 擁有檔案 |
|---|---|---|
| A1 帳簿核心 | sonnet | `knowledge/forecast_lib.py`（新）、`knowledge/settle_forecasts.py`、`knowledge/q.py`（--forecasts 段）、`knowledge/README.md`、`knowledge/forecasts.jsonl`（僅 migrate）、`scripts/generate_{rv,vix,cot}_forecasts.py`、`scripts/build_{rv,vixts,cot}_base_rates.py`、`data/{rv,vixts,cot}_base_rates.json`（--skip-fetch 重建） |
| A2 成績單與治理 | sonnet | `scripts/score_flowmap.py`、`docs/flowmap/index.html`（成績單 JS／方法論段）、`docs/flowmap/data/scorecard.json`、`knowledge/rule_ledger.md`、`.github/workflows/forecast-settle-weekly.yml` |
| B tsmom | sonnet | `scripts/build_tsmom_base_rates.py`、`scripts/generate_tsmom_forecasts.py`、`data/tsmom_base_rates*.json` |
| C vrp | sonnet | `scripts/build_vrp_base_rates.py`、`scripts/generate_vrp_forecasts.py`、`data/vrp_base_rates*.json` |
| D dd-verdict | sonnet | `scripts/build_dd_verdict_base_rates.py`、`scripts/generate_dd_verdict_forecasts.py`、`data/dd_verdict_base_rates*.json` |
| M macro 層 | sonnet | `scripts/build_macro_base_rates.py`、`scripts/harvest_macro_falsifiers.py`、`data/macro_base_rates*.json` |

B／C／D／M 的 `--write` 依賴 A1 的 forecast_lib；dry-run 不得依賴它（import 放在 --write 路徑）。整合測試由 orchestrator 做。**全部不 commit**，持有人複審後才 commit。

## §8 驗收清單（orchestrator）

1. `python knowledge/forecast_lib.py --migrate` 後 forecasts.jsonl 4 筆（2 本尊＋2 哨兵），欄位齊。
2. `python knowledge/settle_forecasts.py` 成功；`forecast_settlement.json` 有 `sources`；`--check-resolver monitor:sofr_iorb` 印 scale=100。
3. 六個 producer dry-run 皆輸出合法 JSONL 且 p_clim 非 null；`generate_dd_verdict_forecasts.py` 草案數＝符合條件的裁決數 × 2（列出跳過原因）。
4. `python scripts/score_flowmap.py` 產 v2 scorecard；頁面 JS 無語法錯（node --check 抽出段落或瀏覽器開啟）；白話抽查。
5. `python3 scripts/qc.py`（changed files）通過。
6. rule_ledger 新舊條文對讀；workflow YAML 語法。
7. 手算抽查：SPRT 常數；哨兵 seed 可重現；p_clim 與條件 p 同窗口。

## §9 明確不做／下一批

- **P2**：信用領先、市場內部結構、日曆效應三個 producer；Kelly paper 組合。
- **P2 追加（持有人 2026-09-02 核准）**：①**個股層新鮮度閘**——任何引用 dd-verdict 的判讀（q.py 摘要、成績單、orchestrator 口頭 read）必須附「最近 60 天裁決數」，低於門檻（暫定 10，PREREG 於下一批凍結）即輸出「個股層無新資料，本期不判讀」，不得拿舊裁決充數；②**個股層機械 producer**——把站上既有週更名單（engine GRP 席位／picks 精選榜／dd-screener 五條件通過者）每週自動轉成「91 天內跑贏 SPY」forecast（relspy 域、p 自各名單自建 base rate、p_clim 同 dd-verdict 宇宙表），給既有名單記分而非產生新名單，故不觸犯 2026-07-07「不蓋新收斂面」；同時回答各聚合層名單有無實績。③複審（rereview decision）為 dd-verdict 的低成本補給，靠 thesis monitor 節奏，不做機制。
- **P3**：CTA 尺規換 CFTC TFF leveraged funds（或 SG Trend Index）；dealer gamma。
- **intel 整合（持有人 2026-09-02 提問「/intel/ 可否一起整合」，列入下一批，順序如下）**：①**轉折雷達 ↔ 帳簿雙向接線**——`docs/intel/data/*.json` 的 `flags[]`（build_flags 機械算：theme／metric／value／threshold／distance_pct／as_of）成為 harvest 的門檻來源（取代自寫 regex，覆蓋面從 5 個 monitor key 擴到雷達全部 7＋條，含 DXY 102／USD/CNY 7.2／核心 PCE 3.5／breakeven 2.6），新 resolver 域 `intel:<theme>|<metric>` 讀 intel 每日 JSON 的 flag value 序列（any_close／at_expiry）；雷達頁面反向顯示帳簿的 p／p_clim／resolve_by（「距門檻 4.9%，系統認為 36 天內觸及機率 23%」）。②**新聞閱讀 LLM 進淘汰賽**——summarize.py 每日 prompt 追加「至多提出 2 條帶 monitor／price resolver＋p 的可判命題」，落 `docs/intel/pending/` 草案佇列，每週由 orchestrator 依持有人授權（2026-09-02：不介入）核入 source=`intel-llm`，與其他 source 同尺記分——目的是誠實檢驗「每天讀新聞對預測有無增量」（預期為零，值得證明）。改 scripts/intel 的 prompt 屬另一條 pipeline，實作前列為持有人核准項。③**intel calendar（FF 經濟事件含 forecast／previous／impact）＝P2 日曆效應 producer 的資料源**（FOMC 前漂移、CPI 日），不另抓。④gauges 13 項分位只作條件變數（與 monitor 重疊），不當 producer。
- **macro 報告**：不重寫。refresh_due 2026-10-08～10 到期時走 refresh（持有人指示：writer sonnet、orchestrator review；與路由表「macro writer 維持 opus」衝突，以持有人本次指示為準並在該輪 commit 註記）。建議同輪把 macro-analyst 升 v1.3：kill_metrics 每條可選機器欄 `{series, op, value, unit, window}`，讓 harvest 免 regex（改 skill 檔需持有人另行核准）。
- **monitor tp10y 標籤**：`build_monitor.py` 把 THREEFYTP10（Kim–Wright）標成「ACM」，本批不動 monitor 管線，只在 harvest note 註明；建議另案一行修正。
- 六筆 macro 草案的 p：已於 2026-09-02 由 orchestrator 以**條件式歷史頻率**賦值（持有人授權不介入）：同序列近 20 年、25 交易日窗，條件＝一年分位桶（≥90／≤10，sofr_iorb ≥70）× 21 日動能同向［× 窗含季末］，向較寬桶以 60 樣本先驗收縮，下限 0.01。結果：SOFR−IORB 0.84／HY OAS 0.03／TP>1.0 0.24／10Y>5.0 0.30／30Y>5.5 0.23／TP<0.2 0.01。此為 macro-falsifier 的 p 標準程序，下次 harvest 沿用（可寫成 `--p-mode conditional` 機械化，列下一批）。
