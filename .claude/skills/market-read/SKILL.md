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

## 版本
- v1.0 2026-09-03：首版；首份判讀 2026-09-02（先弱後強；3m 0.52／6m 0.55／12m 0.60；7 張命題）。
