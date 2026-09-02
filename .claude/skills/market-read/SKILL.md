---
name: market-read
description: market-read — 市況主控台判讀層（週頻＋事件觸發）。orchestrator 讀證據包後寫 docs/market/data/read.json（三股力量／傳導／部位／類比／三框架機率／證偽表），機械 critic 過後把 5–8 張命題落進帳簿（source market-read），頁面 /market/ 第一屏渲染。觸發：「跑市況判讀」「market read」「本週市況判讀」「更新市況主控台判讀」。
---

# market-read v1.0（2026-09-03）

**定位**：`/market/` 是機械證據層（日更、零 LLM）＋判讀層（本 skill）兩層。判讀層回答「未來 3／6／12 個月股市的可能方向與背後邏輯」，每一個機率都進帳簿被 SPRT 打分；判紅即降為評論。設計凍結稿：`notes/site-internal/root/_market_read_design_20260903.md`。**判讀者＝orchestrator（opus 級），不外包給 sonnet、不上 cron。**

**白話關卡（持有人 2026-09-03 指出漏掉，列為硬規則）**：判讀文字＝外資券商白話，照 `_plainlang_styleguide.md` 四句式——每個術語在同一欄位首次出現必附「術語（一句白話）」（期限溢價（投資人要求多付的長債補償）、解壓縮（頂端無事、底層失血）、NAAIM（主動經理人曝險調查）…），先講為什麼再列數字，短句、一句一個意思；頁面永遠不露 `monitor:dgs10` 這類代碼與 SPRT／LLR／n_eff／orchestrator 等內部詞（顯示層用「序貫檢定」「累積證據分」「有效樣本」「站方判讀」）。`check_market_read.py` 的 `jargon_gloss` WARN 必須清零才算完成。

**憲法**：描述器紀律（只講機率與條件；禁「買／賣／加碼／減碼／避開／進場／出場／建議」）；不是收斂面；每個判斷句錨定一個 ref（`monitor:<key>`／`internals:<key>`／`stress:<欄>`／`cot:<市場>`／`flow:<欄>`）並帶 as_of；與帳簿表格分歧必明寫；白話全形（`_plainlang_styleguide.md`）；不改任何機械層檔案。

## 步驟

1. **讀證據**（全部唯讀）
   - `python3 scripts/build_market_state.py --evidence-pack`（純文字證據包：利率／信用／內部分裂／勞動與通膨／流動性／匯率與商品／部位與流量／事件與地緣，每數字帶 as_of）。
   - `docs/market/data/state.json`：`council`／`council_summary`（表格 p）、`fuses`、`anomalies`、`stock_pulse`、`scoreboard`。
   - 最新 `docs/intel/data/YYYY-MM-DD.json` 的 `brief_zh`；`docs/macro/` 各報告的 kill 表現值（state.fuses 已含）。
   - **上一期** `docs/market/data/read.json` 與 `docs/market/data/read_history.jsonl`：判讀要對上期負責——哪些證偽被觸發、三框架機率為何改、上期命題現況（`python knowledge/q.py --forecasts` 看 market-read 段）。
2. **寫 `docs/market/data/read.json`**（schema `market-read-v1`，逐欄照首份 2026-09-02 版）：
   - `thesis_zh` 一句主張；`path_zh` 路徑句（先弱後強／先強後弱／區間…＋觸發者）。
   - `horizons` 三筆：p_up 相對基準的偏離必須在 `logic_zh` 講清楚；3 個月附 p_dd10、12 個月附 p_dd20。
   - `forces` 2–4 張，每張 refs ≥2、每個 ref 一句「為什麼看它」。
   - `transmission` 四格（erp／credit／split／liquidity）各一句判讀。
   - `positioning_zh`：機械賣家 vs 裁量避險、波動錯價。
   - `analogs` 2–4 個：吻合特徵各附 today_ref，**必附不同之處**與當年結果。
   - `falsifiers` 6–10 條，**至少 2 條轉多**；可用 `field: "chg30_pct"` 對 30 天變化設門檻。
   - `deviations_from_tables`：對議會 summary 與帳上同序列 open 命題，|判讀 p − 表格 p| ≥ 0.05 者逐條寫理由。
   - `forecasts` 5–8 張，**前四張型別凍結**：3m 方向（pxd:SPY at_expiry）、6m 方向、12m 方向、3m 回撤 10%（pxd:SPY any_close "<"）；其餘取自證偽表（monitor／internals 域 any_close）。
   - `assumptions.spx_fwd_pe` 寫來源。
3. **機械 critic**：`python3 scripts/check_market_read.py` 必須 PASS（FAIL 不得落帳；WARN 要在複審時說明）。
4. **落帳**：`python3 scripts/ledger_from_editorial.py --source market-read --file docs/market/data/read.json`（先 dry-run 看 7 張 p／p_clim）→ `--write`（自動回填 `claim_ids[]`）；把 id 依序填進 `horizons[].claim_ids`（前三張＋第四張進 3m）與對應 `falsifiers[].claim_id`；append 一行到 `docs/market/data/read_history.jsonl`：`{as_of, thesis_zh, path_zh, p_up_3m, p_up_6m, p_up_12m, n_claims, claim_ids}`。
5. **重建合成層**：`python3 scripts/build_market_state.py`；本機 `python3 -m http.server` 開 `/market/` 看第一屏與證偽表現值。
6. **停下複審**：列出主張、三框架 p 與基準、與表格分歧、落帳 id；持有人說 push 才 commit（只 stage：read.json、read_history.jsonl、state.json、forecasts.jsonl）。

## 節奏與觸發
- 週頻：每週一台北上午（週日 crossasset／crowding 已更新）。
- 事件觸發（任一）：壓力分數週變動 ≥10；任一引信觸及；VIX 收 ≥25；判讀 as_of 超過 10 天（頁面已灰化）。
- 不因單日新聞改判讀；新聞進 `forces` 的證據列，不進機率，除非它改變了某個 ref 的數字。

## 記分與 kill（rule_ledger 已登記）
- source `market-read`：SPRT（p0 .5／p1 .65／α .05／β .10，n_eff≥20）accept_h0 → 判讀層降為評論、頁面拿掉機率，只留文字與證據；校準輪才可重設。
- 正面義務：一週一次；無命題視為未完成。
- 判讀者的自我校準：每期先看上期命題哪些已結算、命中率與 BSS，再寫新判讀。

## Auto 模式（2026-09-03 全自動化；雲端 routine `market-read-auto`）

**定位**：以上步驟 1–6 是手動模式（orchestrator 對話中執行）。Auto 模式是同一套判讀邏輯搬進雲端 routine：每天固定時間喚醒、自己判斷要不要跑、跑完自己 commit push、寄 email 摘要。兩種模式記分同一個 source（`market-read`），SPRT 判紅時一起降級。設計稿：`notes/site-internal/root/_market_read_design_20260903.md` §5。**判讀本身的骨架、憲法、白話關卡與手動模式完全相同**——auto 模式只是「誰喚醒、誰審、失敗怎麼辦」不同，不是另一套判讀邏輯。

### 步驟（比照設計稿 §5.1／§5.4）

1. `bash scripts/install_hooks.sh`（讓 pre-commit／pre-push 生效；auto 模式不得 `--no-verify`）。
2. `python3 scripts/check_read_triggers.py --json`：`run_read` 為 false 就印 `reasons[]` 後直接結束——不改任何檔、不 commit（幾百 token 的喚醒成本）。觸發條件（任一）：①台北週一；②壓力分數 s 較 5 個交易日前變動 ≥10；③`kill_watch.breached` 非空，或 `state.fuses` 任一 `dist_pct` ≤ 0；④VIX（`evidence.quotes["monitor:vix"].num`）≥ 25；⑤判讀過期（today − as_of > valid_days）；⑥上次失敗（`read_status.json.status=="failed"`，隔天重試）。同一天不重跑：`read.json.as_of` 為今天則直接結束（reason `already_read_today`）。
3. `run_read` 為 true 才進入判讀：
   a. 讀證據（同手動模式步驟 1）：`--evidence-pack`、`state.json`、最新 intel brief、上一期 `read.json`／`read_history.jsonl`。
   b. 依固定骨架寫 `docs/market/data/read.json`（同手動模式步驟 2）。
   c. **冷讀 subagent**：依下方 §5.2 模型配對表用 `Agent` 工具開一個 subagent，職責書逐字照下方 §5.3（不得改寫、不得省略檢查項）；subagent 只回報不改稿，輸出 JSON `review = {model, verdict, round, findings[]}`。
   d. 判讀者依 findings 修稿，**最多 2 輪**；第 2 輪後仍有 🔴 → 本次判讀視為失敗，跳到步驟 4。
   e. `python3 scripts/check_market_read.py` 必須 PASS（FAIL → 失敗處置）。
   f. `python3 scripts/ledger_from_editorial.py --source market-read --file docs/market/data/read.json --write`，回填 `claim_ids[]`；append 一行到 `docs/market/data/read_history.jsonl`。
   g. `python3 scripts/build_market_state.py` 重建合成層；`python3 scripts/qc.py` 必須 PASS。
   h. 把最後一輪 `review`（模型、verdict、輪次、findings）寫入 `read.json.review`（供頁面「判讀記分」區與 email 摘要顯示）。
4. **寫 `docs/market/data/read_status.json`**：
   - 全部關卡通過 → `{"as_of": ..., "status": "ok", "stage": "auto", "reasons": []}`。
   - 任一關卡失敗（冷讀 2 輪後仍 🔴／機械 critic FAIL／落帳 0 張／qc 失敗／push 三次失敗）→ **不改 `read.json`、不落帳**，寫 `{"as_of": ..., "status": "failed", "stage": "<失敗的關卡>", "reasons": [...]}`，只 stage 這一個檔並單獨 commit push（`.github/workflows/market-read-notify.yml` 偵測到會寄失敗信）。
5. 成功時只 stage：`read.json`、`read_history.jsonl`、`read_status.json`、`state.json`、`knowledge/forecasts.jsonl`、`knowledge/forecast_settlement.json`（若 settle 有跑）——**不得 `git add -A`**。
6. commit（訊息含 `as_of` 與主張前 30 字）→ `git pull --rebase origin main` → `git push origin main`，push 失敗重試 3 次。

**硬規則（與手動模式共用＋新增）**：描述器紀律、白話全形、每數字帶 as_of、與表格分歧必寫、不改機械層任何檔（沿用）；auto 模式額外：不得 `--no-verify`；不得改 routine 排程本身；judge/writer 永不同模型（見下）。

### §5.2 模型配對（寫與審永不同模型）

| 判讀者（routine 的 session model） | 冷讀者（Agent subagent model） |
|---|---|
| `claude-fable-5-1`（優先，建立 routine 時先試此值） | `claude-opus-5` |
| `claude-opus-5`（fable 不被接受時的退路） | `claude-sonnet-5` |
| 手動由 orchestrator（Fable）跑 | `claude-opus-5` |

routine 的 `allowed_tools` 須含 `Agent`（冷讀 subagent）、`Skill`、`Bash`、`Read`、`Write`、`Edit`、`Glob`、`Grep`。

### §5.3 冷讀職責書（逐字傳給 Agent subagent；subagent 只回報不改稿，輸出 JSON `review`）

輸入：`docs/market/data/read.json`、`python3 scripts/build_market_state.py --evidence-pack` 的證據包、`docs/market/data/state.json` 的 council_summary 與 fuses、上一期 read.json（若有）。

六項檢查，每項列 findings `{severity: "🔴"|"🟡", field, issue, suggestion}`：
1. **錨定**：每個 ref 引用的數字、分位、方向是否與證據包現值一致；判斷句有無無錨的數字。
2. **內部一致性**：三框架 p 與回撤 p 是否互相說得通；證偽表方向與主張一致；**每張命題的 p 是否與主張方向一致**（2026-09-02 初稿 30 年期 25% 對財政主導論即為此類 🔴）。
3. **分歧理由**：`deviations_from_tables` 每條理由是否具體到可證偽，而非「我認為」。
4. **類比誠實**：每個歷史類比是否附不同之處，且不同之處是否真的削弱類比（若削弱卻仍當主要類比→🟡）。
5. **紀律與白話**：禁語、術語首現括號、全形標點、無流程劇場。
6. **遺漏**：證據包中分位 ≥95 或 ≤5、或 30 天變化 |Δ|≥10% 的數字，有無被判讀完全忽略；列出未被引用的極端值。

`verdict`：任一 🔴 → `revise`；否則 `pass`。判讀者依 findings 修稿，最多 2 輪；第 2 輪後仍有 🔴 → 本次判讀失敗（見上方步驟 4）。`review`（模型、verdict、輪次、最後一輪 findings）寫入 read.json 供頁面「判讀記分」區與 email 顯示。

**Spawn 方式**（比照 repo CLAUDE.md 的 industry-thesis-critic 慣例；`{職責書}` 是上面這段文字逐字貼上，不得改寫或省略檢查項）：
```
Agent({
  description: "Cold review market-read {as_of}",
  subagent_type: "general-purpose",
  model: "<依上表配對>",
  prompt: "You are operating as the market-read cold-read subagent. {職責書逐字}. 附上 docs/market/data/read.json、evidence-pack 內容、state.json 的 council_summary 與 fuses、上一期 read.json（若有）。只回報 JSON review={model, verdict, round, findings[]}，不得修改任何檔案。"
})
```

## 版本
- v1.1 2026-09-03：新增 Auto 模式（雲端 routine `market-read-auto`，見 §5）——`check_read_triggers.py` 判定觸發、冷讀 subagent 模型配對與職責書、失敗寫 `read_status.json`、email 摘要交 `market-read-notify.yml`。手動模式（步驟 1–6）不變。
- v1.0 2026-09-03：首版；首份判讀 2026-09-02（先弱後強；3m 0.52／6m 0.55／12m 0.60；7 張命題）。
