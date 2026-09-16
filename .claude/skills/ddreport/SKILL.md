---
name: ddreport
version: v5.0
released: 2026-09-17
description: "任何 DD 觸發語 → `python3 scripts/dd2/run.py {T}`（v20 管線，2026-09-17 起預設；並行期一週，舊鏈 `scripts/ddreport.py run {T}` 保留可叫）。四通 LLM：sonnet 每軸一通採證 → Fable 單輪判斷 → opus 單輪閘（紅燈一通 patch map 再閘一次，仍紅停下交人）→ sonnet 前後半並行散文；其餘零 LLM，完成自動 finish＋commit＋push。觸發：『{ticker} DD』『個股分析 {ticker}』『{ticker} 定見』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』『conviction analysis {ticker}』『{ticker} dca』『{ticker} 全套』『{ticker} 走完整流程』『ddreport {ticker}』『/ddreport {ticker}』。裸 ticker 與『這檔如何／值不值得研究／先篩一下 {ticker}／{ticker} 快篩』仍走 stock-screen-v1。"
---

# ddreport v5.0（v20 管線，dd2）

```bash
python3 scripts/dd2/run.py {T}                              # 預設＝全流程到 finish（commit＋push）
python3 scripts/dd2/run.py {T} --archetype "循環/商品"       # 前份無 archetype 或要換尺時指定
python3 scripts/dd2/run.py {T} --until gated                 # 只到閘就停
python3 scripts/dd2/run.py {T} --dry-run                     # 產物留 run 目錄，不寫 docs/、不 commit
python3 scripts/dd2/run.py {T} --resume [--redo judged,gated,prose] [--reuse-judgment] [--reuse-prose]
python3 scripts/ddreport.py run {T}                          # 舊鏈（v17／v19），並行期一週內可叫
```

一條指令跑完：plan（零 LLM，Koyfin 磁碟快路徑）→ stage0（sonnet，只查證據庫過期的軸，每軸一通、12 並行、不重試）→ facts（零 LLM 事實表，含程式算的週線均線六態 `f_ma_state`）→ judged（Fable 單輪無工具，串流接回覆；形狀錯 normalize 一次即停）→ gated（opus 單輪；🔴 → 一通 patch map → 再閘；仍 🔴 停下交指揮者）→ brief（零 LLM）→ prose（sonnet 前後半兩通並行）→ finish（沿用 `ddreport.py finish`：update_dd_index 同步、archive、commit、push）。互動 session 只下這一行，再讀回報。

**判斷契約＝v19 judge-owned 欄**（`scripts/dd_schema/judgment.schema.json` 的 `v19_contract`）；規則卡在 `scripts/dd2/cards/`（來源 `references/`，`cards.py check` 驗來源戳）。**程式擁有的欄**：`decision_inputs.ma`（週線六態）、`price_at_dd`、以及因 ma 變動導致的裁決／角色漂移歸因，判斷者填什麼都會被覆寫。**判斷通維持預設思考**（2026-09-17 MU A/B：`--judge-effort medium` 便宜 $0.33 但自觸發硬否決、閘多一紅）。

**證據庫** `facts/{T}/`：按軸保存期限（財報數字到下一季、競爭客戶 90 天、法規地緣 180 天、資本市場 30 天、重大事件 14 天），重跑只查過期軸。

**exit code**：0 成功；2＝遠端領先（push 被拒），開 worktree cherry-pick 後再推；其餘＝FAIL，看 stderr 與 `.dd_build/runs/{T}_{D}/manifest.json`（`stages.*.note` 有 FAIL 原文，`gate_audit.md` 有閘清單）。

## 回報格式

報告路徑、統一裁決（＋倉位角色）、三個數字（5Y EV%／IRR base%／Max DD%）、帳（spawns／cache_write／output／cache_read／cost）、閘 🔴 n 🟡 n、修補輪數。run.py 結尾已印這六項，照抄。

## 停下交人的情況（不要自己再開 LLM 修）

- 閘兩輪後仍 🔴：把 `gate_audit.md` 的紅燈列給持有人，由持有人決定重判（`--redo judged --resume`）或改規則。
- 判斷形狀錯 normalize 後仍 FAIL：貼 `judge_check.txt` 的 ✗ 行。
- 散文篇幅或白名單 FAIL：貼 `stages.prose.note`；重跑 `--redo prose --resume --reuse-judgment`（不重花判斷）。

## 不做的事

- 不讀 bundle／報告全文，不手敲 `dd_*.py`。
- 不重做分析、不改判斷（門檻與矩陣權威在 `references/`；均線 ✅/🟡 合併等規則變更走 rule_ledger）。
- 不在鏈外另跑 critic（閘已在鏈內且跨模型）。

## 並行期（2026-09-17 起一週）

每跑一檔記三樣：帳單、閘紅黃燈數、裁決是否與前份同向（`scripts/dd2/README.md` §8 系列表格）。任一檔出現舊鏈不會有的失敗，回 `python3 scripts/ddreport.py run {T}` 並記錄。設計稿 `notes/site-internal/dd/_dd_v20_clean_design_20260916.md`。

**回退**：`git checkout dd-v16.2-final -- .claude/skills scripts`（舊鏈整套），或只改本檔指令行回 `scripts/ddreport.py run`。
