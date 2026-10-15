---
name: ddreport
version: v5.2
released: 2026-09-23
description: "任何 DD 觸發語 → `python3 scripts/dd2/run.py {T}`（v20 管線，2026-09-17 起預設；舊鏈 `scripts/ddreport.py run`／`batch` 於 2026-10-13 退役）。四通 LLM：sonnet 每軸一通採證 → opus 單輪判斷 → sonnet 單輪閘（紅燈一通 patch map 再閘一次，仍紅停下交人）→ sonnet 前後半並行散文；其餘零 LLM，完成自動 finish＋commit＋push。觸發：『{ticker} DD』『個股分析 {ticker}』『{ticker} 定見』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』『conviction analysis {ticker}』『{ticker} dca』『{ticker} 全套』『{ticker} 走完整流程』『ddreport {ticker}』『/ddreport {ticker}』。裸 ticker 與『這檔如何／值不值得研究／先篩一下 {ticker}／{ticker} 快篩』仍走 stock-screen-v1。"
---

# ddreport v5.2（v20 管線，dd2）

> v5.2（2026-09-23）：stage0 多做舊逐字稿摘要（前一季＋投資人日／分析師日，sonnet 每篇一通，永久快取），判斷與閘 bundle 加「④b 舊逐字稿摘錄」段；normalize_v20 自動修 `eps_meta.base_eps_path`（基期鍵補 A、陣列改用事實表共識重建）。AMD 實測：摘要兩篇 $2.07（之後免費），判斷引用舊場次 16 處，閘 0 紅。
> 2026-09-24：plan 前自動跑 Koyfin 下載（最新 30 篇新稿、逾時 240 秒；沒新稿約 6 秒）。登入過期會印重新登入指令並改用磁碟既有逐字稿；`--skip-koyfin`／`--offline` 不抓。

> v5.1（2026-09-23）：判斷／修補改 opus（Fable 太貴），閘換 sonnet（跨模型冷讀，照 `GATE_MODEL_FOR`）。模型用 CLI 簡稱，自動指向最新版。要回舊組合：`--judgment-model fable`（閘自動回 opus）。

```bash
python3 scripts/dd2/run.py {T}                              # 預設＝全流程到 finish（commit＋push）
python3 scripts/dd2/run.py {T} --archetype "循環/商品"       # 前份無 archetype 或要換尺時指定
python3 scripts/dd2/run.py {T} --until gated                 # 只到閘就停
python3 scripts/dd2/run.py {T} --dry-run                     # 產物留 run 目錄，不寫 docs/、不 commit
python3 scripts/dd2/run.py {T} --resume [--redo judged,gated,prose] [--reuse-judgment] [--reuse-prose]
```

一條指令跑完：plan（零 LLM，Koyfin 磁碟快路徑）→ stage0（sonnet，只查證據庫過期的軸，每軸一通、12 並行、不重試）→ facts（零 LLM 事實表，含程式算的週線均線六態 `f_ma_state`）→ judged（opus 單輪無工具，串流接回覆；形狀錯 normalize 一次即停）→ gated（sonnet 單輪；🔴 → 一通 patch map → 再閘；仍 🔴 停下交指揮者）→ brief（零 LLM）→ prose（sonnet 前後半兩通並行）→ finish（沿用 `ddreport.py finish`：update_dd_index 同步、archive、commit、push）。互動 session 只下這一行，再讀回報。

**判斷契約＝v19 judge-owned 欄**（`scripts/dd_schema/judgment.schema.json` 的 `v19_contract`）；規則卡在 `scripts/dd2/cards/`（來源 `references/`，`cards.py check` 驗來源戳）。**程式擁有的欄**：`decision_inputs.ma`（週線六態）、`price_at_dd`、以及因 ma 變動導致的裁決／角色漂移歸因，判斷者填什麼都會被覆寫。**判斷通維持預設思考**（2026-09-17 MU A/B：`--judge-effort medium` 便宜 $0.33 但自觸發硬否決、閘多一紅）。

**證據庫** `facts/{T}/`：按軸保存期限（財報數字到下一季、競爭客戶 90 天、法規地緣 180 天、資本市場 30 天、重大事件 14 天），重跑只查過期軸。

**exit code**：0 成功；2＝遠端領先（push 被拒），開 worktree cherry-pick 後再推；其餘＝FAIL，看 stderr 與 `.dd_build/runs/{T}_{D}/manifest.json`（`stages.*.note` 有 FAIL 原文，`gate_audit.md` 有閘清單）。

## 回報格式

報告路徑、統一裁決（＋倉位角色）、三個數字（5Y EV%／IRR base%／Max DD%）、帳（spawns／cache_write／output／cache_read／cost）、閘 🔴 n 🟡 n、修補輪數。run.py 結尾已印這六項，照抄。

## 停下交人的情況（不要自己再開 LLM 修）

- 閘兩輪後仍 🔴：紅燈是可查證的事實錯（數字、期別、標籤）→ 照下方「錯一處只修一處」局部修後續跑；其餘把 `gate_audit.md` 的紅燈列給持有人，由持有人決定重判（`--redo judged --resume`）或改規則。
- 判斷形狀錯 normalize 後仍 FAIL：貼 `judge_check.txt` 的 ✗ 行。**例外（2026-10-13 持有人拍板）**：✗ 只是說明欄缺漏（note／理由類），且內容可從同一份 `judgment.json` 已寫的文字直接取得 → 指揮者直接補該欄：`--reuse-judgment` 是從 `agents/judge_1.json` 的原始回覆重建（不讀 `judgment.json`），所以要補在 judge_1.json 回覆文字裡的對應欄位（如 `"denominator_note": null` 改成那句說明），先備份成 `agents/judge_1.before_manual_note.json`、在 run 目錄寫 `manual_patch_note.md`（補了哪欄、文字出處），再 `--resume --reuse-judgment` 續跑；缺的是判斷值（裁決、角色、數字、情境 EPS 等）仍交持有人，不得代填。
- 散文篇幅或白名單 FAIL：貼 `stages.prose.note`；重跑 `--redo prose --resume --reuse-judgment`（不重花判斷）。

## 錯一處只修一處（2026-10-14 持有人拍板，DD／ID 通用）

- 閘、審稿或持有人抓到的錯，只改錯的那一欄，不 `--redo judged` 整份重判。
- 不改結論的錯（過期數字、期別錯、口徑不一、標籤錯）：先查證（事實表、證據庫或一手來源，算術自己對一次），查實就直接改，事後列清單；查不實的不改。
- 改到結論欄位的（裁決、角色、情境數字）：只重定受影響的那一欄，連帶改相關文字，修完明列給持有人。
- **整份重判只留在一種情況：判斷所依據的證據本身錯了**（證據庫或事實表錯，不是判斷文字錯）。
- 作法：`--reuse-judgment` 從 `agents/judge_1.json` 原始回覆重建，所以改在 judge_1.json 回覆文字的對應欄位；先備份成 `agents/judge_1.before_local_fix.json`，在 run 目錄寫 `manual_patch_note.md`（改了哪欄、前後值、出處），再 `--resume --redo gated,prose --reuse-judgment`。

此為流程紀律非裁決閘，不適用 rule_ledger kill-condition 登記。

## 不做的事

- 不讀 bundle／報告全文，不手敲 `dd_*.py`。
- 不重做分析、不改判斷（局部修見上節；門檻與矩陣權威在 `references/`；均線 ✅/🟡 合併等規則變更走 rule_ledger）。
- 不在鏈外另跑 critic（閘已在鏈內且跨模型）。

## 舊鏈退役（2026-10-13）

並行期 9/17 起，42 份 DD 全部走 v20，沒有任何一檔回退舊鏈，舊鏈正式退役。`scripts/ddreport.py` 不刪：dd2 import 它的共用函式，`finish`／同步也沿用它；只是不再用 `run`／`batch` 產 DD。未結兩件：設計稿 §10 驗收 MU 閘剩 2 紅（`scripts/dd2/README.md`）；v20 的 90 天 kill condition（設計稿 `notes/site-internal/dd/_dd_v20_clean_design_20260916.md`）尚未登記 `knowledge/rule_ledger.md`，併入 2026-10 校準輪處理。

**回退**：`git checkout dd-v16.2-final -- .claude/skills scripts`（舊鏈整套），或只改本檔指令行回 `scripts/ddreport.py run`。
