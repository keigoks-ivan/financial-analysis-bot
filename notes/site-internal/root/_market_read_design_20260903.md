# 設計凍結稿 v4：市況主控台 ＝ 判讀層在上、證據層在下、判讀進帳簿被打分（2026-09-03）

- 狀態：**持有人 2026-09-02 深夜指示「把 /market/ 變成這樣，你設計、交給 sonnet 實作」**。判斷在此凍結；sonnet 實作 K1–K3；skill 與首份判讀由 orchestrator 自寫；做完停下複審，持有人說 push 才 commit。
- 前稿：`_market_cockpit_design_20260902.md`（v3，§1–§11 仍有效，本稿只寫差異）、`_forecast_p2_design_20260902.md`（P2，同批未 commit）。
- 樣本＝orchestrator 2026-09-02 深夜對持有人的跨資產判讀（三股力量／傳導算術／內部訊號／部位與流量／歷史類比／三框架機率／證偽表），持有人說「這就是我要的東西」。本稿把那份判讀拆成**可機械化的證據**與**只能由判讀者給的判斷**兩層，並讓判斷可證偽。

## §0 拍板（三條）

1. **判讀層是頁面主體**，機械層降為證據層。頁面第一屏＝本週判讀（一句主張＋路徑＋三框架機率表），往下是三股力量、傳導與內部訊號、部位與流量、歷史類比、證偽表、判讀記分；再往下才是原 v3 的證據區塊（環境五磚／預測議會／機械賣家／引信／異常／個股脈搏／觸發數字／記分板／新鮮度／曝險規則），一個不刪。
2. **判讀必進帳簿**：每次判讀至少 5 張、至多 8 張命題（三框架方向各一、3 個月回撤一、其餘來自證偽表），source `market-read`，走 `ledger_from_editorial.py`，同尺 SPRT 記分、哨兵 twin。判讀層有自己的記分卡；SPRT 判紅＝判讀層降為「評論」（頁面拿掉機率、只留文字與證據）。**這是把 orchestrator 的總經判斷放進淘汰賽**——不留命題等於沒說話。
3. **判讀由 orchestrator 寫（opus 級），週頻＋事件觸發**，用 skill `market-read` 執行；不上 cron（判斷不外包給 API 批次；日後若要自動化列 P3 另議）。判讀 as_of 超過 10 天頁面標「已過期」並把機率灰掉、只顯示機械讀法。描述器紀律不變：只講機率與條件、不下買賣指令（禁「買／賣／加碼／減碼／避開／進場／出場」；「風險最集中的一格」可以）。

## §1 頁面 IA（`docs/market/index.html` v4）

頂部 sticky 小導覽：判讀 · 力量 · 傳導 · 部位 · 類比 · 證偽 · 記分 · 證據 · 曝險。

| 序 | 區塊 | 內容 | 資料 |
|---|---|---|---|
| 1 | **本週判讀** | 一句主張（thesis_zh）＋路徑句（path_zh）＋判讀 as_of／有效期／作者；右側三顆數字：3 個月收高 p、6 個月 p、12 個月 p，各附「基準」；過期時整塊灰、標「判讀已過期 {as_of}，以下為機械讀法」並顯示原 `read_zh.headline` | `read.json`＋`state.json.read_zh` |
| 2 | **三個時間框架** | 表：框架／SPY 收高 p（判讀）／基準／10%（12 個月加 20%）回撤 p／基準／一句邏輯／帳簿命題連結（id→ `/flowmap/#ledger` 或 q.py 說明）；p 與基準同列 dumbbell | `read.json.horizons` |
| 3 | **三股力量** | 2–4 張卡：標題、機制段（2–4 句）、證據列（ref → 由 `state.json.evidence.quotes` 即時取現值／分位／30 天變化／as_of；判讀寫死的是「看哪個數字、為什麼」，數字本身永遠是活的） | `read.json.forces` × `evidence.quotes` |
| 4 | **傳導與內部訊號** | 四格：估值緩衝（EY、實質 ERP、名目差）／信用分裂（HY、IG、CCC、CCC−HY、解壓縮旗）／指數 vs 平均股（壓力 s、內部 int_s、廣度、五條利率敏感比率的「衰退票數」）／流動性（RRP、TGA、準備金分位、SOFR−IORB、Fed 資產負債表 30 天）——四格數字全機械，每格底下一句判讀 | `evidence.erp/credit/split/liquidity`＋`read.json.transmission` |
| 5 | **部位與流量** | 左：機械賣家（CTA 翻轉距離、vol-control 下一階、庫藏股靜默四週、月末方向）；中：COT 極端表（三年分位 ≤10 或 ≥90 的市場，方向與分位）；右：波動錯價（VIX、9 日 VIX、VIX3M、MOVE 分位、OVX；一句「股票波動 vs 總經風險地圖」）＋NAAIM／個股賣權比／VRP；底一句判讀 | `evidence.positioning`＋`read.json.positioning_zh` |
| 6 | **歷史類比** | 每個類比：年份、吻合特徵（3–5 條，各附今日對應數字）、不同之處（1–2 條）、當年結果一句；另一張「期中選舉年」小卡（機械：自 SPY 25 年序列算期中年最大回撤中位數與低點後 12 個月報酬，P2 再做；v4 先由判讀給數字並標來源） | `read.json.analogs` |
| 7 | **什麼會改變這個判讀** | 證偽表：方向（轉空／轉多／中性轉向）、訊號、現值（機械即時，ref）、門檻、距離 %、判讀一句、帳簿命題 p（若有）——與引信區同款式但這是判讀者選的 | `read.json.falsifiers` × `evidence.quotes` |
| 8 | **與帳簿表格的分歧** | 表：命題、表格 p、判讀 p、理由——判讀者必須明寫自己和機械表格不同的地方 | `read.json.deviations_from_tables` |
| 9 | **判讀記分** | `market-read` 來源的 SPRT 卡（同記分板卡）＋歷次判讀列表（as_of、主張一句、命題數、已結算命中）；首期顯示「首次判讀，尚無成績」 | `scoreboard.ledger_sources["market-read"]`＋`read_history.jsonl` |
| 10 | **證據層** | 原 v3 十個區塊原樣搬到下方，標題前加「證據層 ·」；環境五磚仍在最前 | 既有 |

首頁市況卡：第一行改為判讀主張一句（過期時退回機械 headline），其餘不動。

## §2 資料契約

### 2.1 `docs/market/data/read.json`（schema `market-read-v1`，判讀者寫、skill 驗）
以本稿同日落地的首份 `read.json` 為 schema 範本（逐欄）：`schema／as_of／generated_at／author／model／valid_days(10)／thesis_zh／path_zh／assumptions{spx_fwd_pe, source}／horizons[]{key, label, resolve_by, p_up, p_clim_up, p_dd10|p_dd20, p_clim_dd, logic_zh, claim_ids[]}／forces[]{title, mechanism_zh, refs[]{ref, why}}／transmission[]{key, read_zh}／positioning_zh／analogs[]{period, matches[]{feature, today_ref}, differs[], outcome_zh}／falsifiers[]{direction, label, ref, op, threshold, unit, read_zh, claim_id}／deviations_from_tables[]{claim, table_p, my_p, why}／forecasts[]（`ledger_from_editorial` 既有 schema：claim, p, horizon_days, resolver{series, op, value, window}, why）／claim_ids[]（落帳後回填）`。
`ref` 格式＝`monitor:<key>`／`internals:<key>`／`stress:<s|int_s|int|b.rates|…>`／`cot:<market>`／`flow:<cta_flip_dist|vc_next_rv|…>`，頁面全部到 `evidence.quotes` 查。

### 2.2 `state.json.evidence`（`build_market_state.py` 新塊，日更零 LLM；K1）
- `quotes`：扁平字典，monitor 全部 key＋internals 全部 key＋stress 六欄＋COT 15 市場＋flowmap 五個流量數，值＝`{label, val(顯示), num, pctile, chg30_pct, z, as_of}`（chg30 由 spark 首尾算；無 spark 者 null）。
- `erp`：`{fwd_pe（讀 read.json.assumptions.spx_fwd_pe，缺則 22.0 並標 assumed）, ey_pct, real10y, real_erp_pp, dgs10, nominal_gap_pp, as_of}`。
- `credit`：`{hy_oas, ig_oas, ccc_oas, ccc_minus_hy_pp, hy_pctile, ccc_pctile, decompression: ccc_pctile≥90 且 hy_pctile≤20, hyg_lqd_pctile}`。
- `split`：`{stress_s, int_s, int_long, brd_above200, brd_above50, brd_sec_above50, recession_votes: {n, of:5, members:[{key, pctile}]}（itb_spy／xly_xlp／kre_xlf／djt_dji／iwm_spy 分位 ≤25 者算一票）, surface_calm_internal_riskoff: s<60 且 int_s≥75}`。
- `labor_inflation`：`{payems_3m, claims, sahm, cpi_yoy, core_pce_yoy, bei10y, bei5y5y, oil_chg30, ags_chg30:{soybean,corn,wheat}, dgs3mo, dgs2, hike_pricing_bp: (dgs2−dgs3mo)×100}`。
- `liquidity`：`{rrp, tga, reserves, reserves_pctile, sofr_iorb_bp, walcl_chg30, nfci}`。
- `fx_commod`：`{dxy(+chg30), usdjpy, usdcny, usdkrw, usdtwd, gold, copper, copper_gold, wti, brent, bad_yields_signature: dgs10 chg30>0 且 dxy chg30<0 且 gold chg30>0}`。
- `positioning`：`{cot_extremes:[{market, net_pct_oi, pctile_3y, side}] (≤10 或 ≥90), naaim, pc_equity(+pctile), vrp_20d(+z), short_vol_ratio, vol_mispricing:{vix, vix9d, vix3m, move, move_pctile, ovx}, flows:{cta_flip_dist_pct, cta_flip_level, vc_next_rv, vc_next_flow_bn, buyback_cov_next4[], month_end_dir}}`。
- `events`：`internals.upcoming_events`＋`macro_calendar` 未來 30 天；`geo_headline`：intel brief_zh 第一則純文字（去 HTML，≤120 字）。
- `--evidence-pack`：CLI 旗標，把 evidence 印成給判讀者讀的純文字包（分區、每數字帶 as_of），stdout。

### 2.3 帳簿（K3）
- `scripts/ledger_from_editorial.py` 加 `--source market-read`；`resolve_by` 由 horizon_days 算；p_clim：**pxd:SPY 一律改用 `data/calendar_base_rates_raw_cache.json`（25 年）**——at_expiry 用同 horizon 交易日數（H_td=round(h×252/365)）無條件上漲頻率；**any_close 新增**：op "<" 用「H_td 內任一收盤 ≤ value 相對今收比例」的無條件頻率（比例＝value／今收，今收＝快取最後收盤），op ">" 對稱；monitor 域沿用 climatology。其他 source 不變。
- 回填：`--write` 後把落帳 id 依序寫回 `read.json.claim_ids[]`（與 forecasts[] 同序）並印出；`horizons[].claim_ids`／`falsifiers[].claim_id` 由 skill 步驟依序對應（forecasts 順序凍結：3m 方向、6m 方向、12m 方向、3m 回撤 10%、其餘證偽表）。
- `scripts/check_market_read.py`（機械 critic，取代 LLM critic）：schema 齊；每個 `ref` 可在 evidence.quotes 解析；forces ≥2、每力量 refs ≥2；horizons 三筆且 p_up ∈ [0.2, 0.9]；forecasts 5–8 張且前四張型別固定；禁語掃描（買／賣／加碼／減碼／避開／進場／出場／建議）；每個 falsifier 有 ref＋threshold；deviations 對「帳上已有同 series＋op 的 open 命題且 |判讀 p − 表格 p| ≥ 0.05」者必填；全形標點。exit 非零＝不得落帳。
- `docs/market/data/read_history.jsonl`：每次落帳 append `{as_of, thesis_zh, path_zh, p_up_3m, p_up_6m, p_up_12m, claim_ids}`；頁面「判讀記分」讀它。
- `knowledge/rule_ledger.md`：新增 source `market-read`（kill＝SPRT accept_h0 → 判讀層降為評論、頁面拿掉機率；正面義務：每週一次、無命題視為未完成；過期 10 天灰化）；加一提刪一候刪提名：`stock_pulse.fresh` 門檻（60 天 10 筆）——判讀層上線後「個股層要不要說話」改由判讀者負責，機械門檻是否還需要交校準輪審。

### 2.4 skill `market-read`（orchestrator 自寫，`.claude/skills/market-read/SKILL.md`；CLAUDE.md 加 workflow 條目）
觸發：「跑市況判讀」「market read」「本週市況判讀」「更新市況主控台判讀」。步驟：①`python3 scripts/build_market_state.py --evidence-pack` 讀證據包，並讀 `docs/market/data/state.json`（council／fuses／anomalies／stock_pulse）、最新 intel brief、`docs/macro/` 各報告 kill 表現值、上一期 `read.json` 與 `read_history.jsonl`（判讀要對上期負責：哪些證偽被觸發、機率怎麼改）；②依固定骨架寫 `read.json`（骨架＝§1 的 2–8 區，每個判斷句錨定一個 ref；三框架 p 必須說明相對基準偏離的理由；歷史類比必附「不同之處」；證偽表 6–10 條至少 2 條轉多）；③`python3 scripts/check_market_read.py` 過；④`python3 scripts/ledger_from_editorial.py --source market-read --file docs/market/data/read.json --write`，回填 id，append history；⑤`python3 scripts/build_market_state.py`；⑥停下複審，持有人說 push 才 commit。硬規則：描述器紀律、白話全形、每數字帶 as_of、與表格分歧必寫、不改機械層任何檔。事件觸發：壓力分數週變動 ≥10、任一引信觸及、VIX 收 ≥25、判讀已過期。

## §3 分包（sonnet，並行；全部不 commit）

| 包 | 擁有檔案 |
|---|---|
| K1 evidence | `scripts/build_market_state.py`（evidence 塊＋`--evidence-pack`＋首頁卡用的 `read_headline`）、`docs/market/data/state.json` |
| K2 page v4 | `docs/market/index.html`、`docs/index.html`（市況卡第一行） |
| K3 ledger＋critic | `scripts/ledger_from_editorial.py`、新 `scripts/check_market_read.py`、`knowledge/rule_ledger.md`、`knowledge/README.md`（source 表） |
| orchestrator | 本稿、`docs/market/data/read.json`（首份判讀）、`.claude/skills/market-read/SKILL.md`、`CLAUDE.md` 條目、`docs/market/data/read_history.jsonl`（首筆）、落帳、驗收 |

K2 依本稿同日的 `read.json` 與 K1 的 evidence 欄位名渲染；K1 未完成前 K2 以 `state.json` 現有欄位＋read.json 先做版面，evidence 欄位名以本稿 §2.2 為準。

## §4 驗收

1. `build_market_state.py` 產 evidence 全塊非 null（缺 crowding 時 cot_extremes 為空＋gap）；`--evidence-pack` 可讀；erp 用 read.json 的 22 倍。
2. `check_market_read.py` 對首份 read.json 通過；對故意塞「建議加碼」的副本失敗。
3. `ledger_from_editorial.py --source market-read` dry-run 7 張 p_clim 全非 null（SPY 25 年表）；`--write` 到 scratch 帳簿 7＋7 張；真帳簿落帳由 orchestrator 在驗收最後執行。
4. 本機 http.server 開 `/market/`：第一屏是判讀；ref 現值全部解析（無「—」）；證偽表距離 % 正確；過期模擬（把 read.json as_of 改成 30 天前）整塊灰化；首頁卡第一行是主張。
5. `qc.py`、py_compile、node --check。
