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

## §5 判讀層全自動化（2026-09-03 持有人拍板：「你按 merge 上站也變成全自動化，好了之後寄重點摘要給我 email，全部交給 sonnet 完成」；全部在 Claude 月租內，不用 API 計費）

### 5.1 架構
- **雲端 routine `market-read-auto`**（`/schedule`，每日 08:00 台北＝`0 0 * * 1-5` UTC，週一至週五）：fresh checkout → `python3 scripts/check_read_triggers.py --json` → `run_read` 為 false 就結束（幾百 token）；為 true 才跑 `market-read` skill 的 **auto 模式**：寫判讀 → 冷讀 subagent → 修稿（≤2 輪）→ 機械 critic → 落帳 → 重建 state → qc → commit → `pull --rebase` → push main。
- **通知工作流 `.github/workflows/market-read-notify.yml`**（GitHub Actions，零 LLM）：`on: push` 到 main 且 paths 含 `docs/market/data/read.json` 或 `docs/market/data/read_status.json` → `python3 scripts/market_read_summary.py` 產生主旨與信文 → `dawidd6/action-send-mail@v3`（smtp.gmail.com 465，`secrets.MAIL_USERNAME`／`MAIL_APP_PASSWORD`，to 與 from 照抄 `daily-non-fundamental-refresh.yml` 的既有寫法）。判讀成功寄摘要；`read_status.json.status=failed` 寄失敗信（含原因）。
- **事件觸發**由純腳本判定，不花用量。`check_read_triggers.py` 讀 `docs/market/data/state.json`、`docs/monitor/data/score_history.json`、`docs/detective/data/kill_watch.json`、`docs/market/data/read.json`，輸出 `{run_read, reasons[], as_of, taipei_date}`；`run_read` 為真的條件（任一）：①台北週一；②壓力分數 s 較 5 個交易日前變動 ≥10；③kill_watch `breached` 非空，或 state.fuses 任一 `dist_pct ≤ 0`；④VIX（`evidence.quotes["monitor:vix"].num`）≥ 25；⑤判讀過期（today − read.as_of > valid_days）；⑥`read_status.json` 存在且 status=failed（上次失敗，隔天重試）。**同一天不重跑**：若 read.json 的 as_of＝今天則 `run_read=false`（reason `already_read_today`）。

### 5.2 模型配對（寫與審永不同模型）
| 判讀者（routine 的 session model） | 冷讀者（Agent subagent model） |
|---|---|
| `claude-fable-5-1`（優先，建立 routine 時先試此值） | `claude-opus-5` |
| `claude-opus-5`（fable 不被接受時的退路） | `claude-sonnet-5` |
| 手動由 orchestrator（Fable）跑 | `claude-opus-5` |
routine 的 `allowed_tools` 須含 `Agent`（冷讀 subagent）、`Skill`、`Bash`、`Read`、`Write`、`Edit`、`Glob`、`Grep`。

### 5.3 冷讀職責書（skill 內逐字；subagent 只回報不改稿，輸出 JSON `review`）
輸入：`docs/market/data/read.json`、`python3 scripts/build_market_state.py --evidence-pack` 的證據包、`docs/market/data/state.json` 的 council_summary 與 fuses、上一期 read.json（若有）。
六項檢查，每項列 findings `{severity: "🔴"|"🟡", field, issue, suggestion}`：
1. **錨定**：每個 ref 引用的數字、分位、方向是否與證據包現值一致；判斷句有無無錨的數字。
2. **內部一致性**：三框架 p 與回撤 p 是否互相說得通；證偽表方向與主張一致；**每張命題的 p 是否與主張方向一致**（2026-09-02 初稿 30 年期 25% 對財政主導論即為此類 🔴）。
3. **分歧理由**：`deviations_from_tables` 每條理由是否具體到可證偽，而非「我認為」。
4. **類比誠實**：每個歷史類比是否附不同之處，且不同之處是否真的削弱類比（若削弱卻仍當主要類比→🟡）。
5. **紀律與白話**：禁語、術語首現括號、全形標點、無流程劇場。
6. **遺漏**：證據包中分位 ≥95 或 ≤5、或 30 天變化 |Δ|≥10% 的數字，有無被判讀完全忽略；列出未被引用的極端值。
`verdict`：任一 🔴 → `revise`；否則 `pass`。判讀者依 findings 修稿，最多 2 輪；第 2 輪後仍有 🔴 → 本次判讀**失敗**（見 5.4）。`review`（模型、verdict、輪次、最後一輪 findings）寫入 read.json 供頁面「判讀記分」區與 email 顯示。

### 5.4 失敗處置與硬規則
- 任一關卡（冷讀 2 輪後仍 🔴／機械 critic FAIL／落帳 0 張／qc 失敗／push 三次失敗）→ 不改 read.json、不落帳，寫 `docs/market/data/read_status.json` `{as_of, status:"failed", stage, reasons[]}` 並單獨 commit push 該檔（通知工作流寄失敗信）；成功時同檔寫 `status:"ok"`。
- routine 內不得 `--no-verify`；先 `bash scripts/install_hooks.sh` 讓 pre-commit／pre-push 生效；commit 只 stage：`read.json`、`read_history.jsonl`、`read_status.json`、`state.json`、`knowledge/forecasts.jsonl`、`knowledge/forecast_settlement.json`（若 settle 有跑）。
- 描述器紀律、白話關卡、不改機械層檔案、加一提刪一，全部照舊；routine 的判讀與手動判讀同尺記分（同一 source `market-read`）。kill：market-read SPRT 判紅 → 停用 routine（`enabled:false`）並在 rule_ledger 註記。

### 5.5 Email 內容（`scripts/market_read_summary.py`，純文字）
主旨：`市況判讀 {as_of}｜{thesis_zh 前 28 字}…`（失敗：`市況判讀失敗 {as_of}｜{stage}`）。信文依序：主張／路徑；三框架表（收高 p 對基準、回撤 p 對基準）；三股力量標題各一句；證偽表前 5 條（現值→門檻、距離）；與表格分歧條數＋最大一條；冷讀結果（模型、輪次、剩餘 🟡 數）；落帳編號；連結 `https://research.investmquest.com/market/`。全形標點。

### 5.6 分包（sonnet 一包做完，含建 routine、煙霧測試、commit & push）
擁有：`.claude/skills/market-read/SKILL.md`（auto 模式＋§5.3 職責書＋模型配對）、新 `scripts/check_read_triggers.py`、新 `scripts/market_read_summary.py`、新 `.github/workflows/market-read-notify.yml`、`docs/market/data/read_status.json`（首筆 ok）、routine 建立（`RemoteTrigger create`，environment `env_017VN8k12DeEt359CtkKbgMv`，repo `https://github.com/keigoks-ivan/financial-analysis-bot`）、routine 煙霧測試（非週一無觸發→應立即結束不改檔）、本稿 §5 完成紀錄、CLAUDE.md 條目一句「已自動化」。驗收：`check_read_triggers.py --json` 今日輸出 `run_read=false`／`already_read_today`；summary 腳本對現行 read.json 印出合法信文；workflow YAML 合法；routine 列表可見且 enabled。

### §5 完成紀錄（repo 側，2026-09-02 sonnet 執行；routine 建立留給 orchestrator）

**檔案**：`.claude/skills/market-read/SKILL.md`（新增「Auto 模式」＋ §5.2 模型配對＋ §5.3 冷讀職責書，手動模式步驟 1–6 原文不動）、新 `scripts/check_read_triggers.py`（六條件＋同日守門，stdlib、缺檔降級不 crash）、新 `scripts/market_read_summary.py`（印主旨＋信文，讀 read.json 或失敗時讀 read_status.json）、新 `.github/workflows/market-read-notify.yml`（`on: push` 到 `docs/market/data/read.json`／`read_status.json`，跑 summary 腳本→`$GITHUB_OUTPUT`→`dawidd6/action-send-mail@v3`）、`docs/market/data/read_status.json`（首筆 `status:"ok"`）。**本包不建立雲端 routine、不寄任何 email**——僅完成 repo 側可被 routine 呼叫的腳本／skill／workflow。

**routine 建立後預期做的事**：`market-read-auto` 每日 08:00 台北喚醒後應直接執行下方逐字 prompt；prompt 內已包含觸發判定（不 run 就零成本結束）、auto 模式全流程（讀證據→寫 read.json→冷讀 subagent→修稿≤2 輪→機械 critic→落帳→重建 state→qc）、成功／失敗兩種 `read_status.json` 寫法、只 stage SKILL 列出的檔案、commit＋rebase＋push（失敗重試 3 次）。orchestrator 建立 routine 時把下方整段貼進 routine 的 prompt 欄位即可，不需另外改寫。

**建立 routine 時貼入的逐字 prompt**：

> 你在 InvestMQuest research repo（keigoks-ivan/financial-analysis-bot）的雲端 session，任務是市況主控台判讀層的自動判讀。步驟：①`bash scripts/install_hooks.sh`；②`python3 scripts/check_read_triggers.py --json`，若 run_read 為 false，印出 reasons 後直接結束，不改任何檔、不 commit；③若為 true，打開 `.claude/skills/market-read/SKILL.md`，依其「auto 模式」逐步執行：讀證據包與上一期判讀 → 寫 docs/market/data/read.json → 依 SKILL 的模型配對表用 Agent 工具開冷讀 subagent（職責書逐字照 SKILL）→ 依 findings 修稿最多 2 輪 → `python3 scripts/check_market_read.py` 必須 PASS → `python3 scripts/ledger_from_editorial.py --source market-read --file docs/market/data/read.json --write` → 回填 claim_ids 並 append docs/market/data/read_history.jsonl → `python3 scripts/build_market_state.py` → `python3 scripts/qc.py`；④寫 docs/market/data/read_status.json（成功 status ok；任一關卡失敗則不改 read.json、不落帳，寫 status failed 與 stage、reasons）；⑤只 stage SKILL 列出的檔案，commit（訊息：`market-read 自動判讀 {as_of}：{thesis 前 30 字}`，結尾加 `Co-Authored-By: Claude <noreply@anthropic.com>`），`git pull --rebase origin main` 後 `git push origin main`，失敗重試 3 次。硬規則：描述器紀律（不下買賣指令）、白話（術語首現括號）、每個判斷句錨定活數字、不改機械層任何檔、不用 --no-verify、不改 routine 以外的排程。
