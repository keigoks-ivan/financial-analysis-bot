# 委託書：P0 閘修復＋Git 分岔整併（給 Codex）

> 用法：在 Codex 開 `~/financial-analysis-bot`，第一句「先讀 AGENTS.md 的『角色分工』與『寫程式 agent 的改動紀律』兩節，再讀本檔全文」。本檔是唯一任務來源；有衝突以本檔為準，仍不確定就停下來問，不要猜。
> 日期：2026-09-07。委託人：持有人。指揮者：Claude Code 主 session（放行與 push 的決定權在指揮者，不在你）。
> 依據報告：`notes/site-internal/dd/_review_v17_pipeline_20260907.md`（你自己上一輪交的複審，錨點行號以該檔為準）。

## 〇、這份委託的兩件事

**2026-09-07 修訂（指揮者）：改成大批交件，中途不要回來問。** 原本一階段一交件的節奏太碎，且階段 1 被一個我寫錯的基準數字擋住——那次停得對，但代價是一整輪往返。以下把可以自己決定的都先決定掉。

| 交件批 | 內容 | 交件後 |
|---|---|---|
| **批 A** | 階段 1b（brief 段 fail-closed）＋階段 2（P0-2）＋階段 3（P0-3），**一次做完一起交** | 停下交 diff 等審 |
| **批 B** | 階段 4 Git 分岔：依複審 §4.2 方案 A，在獨立 clone 建 integration branch 並逐檔驗收 | 停下交驗收報告等審，**不得推 main** |

階段 1（P0-1）已於 `96a51716c` 放行並 commit，不用再動。

**批 A 內部不要停下來問**：1b、2、3 三段連續做完再交。三段之間互相影響（都動 `ddreport.py` 與 pre-commit 鏈）時，以「不改判準、只擴大覆蓋與收緊失敗處置」為裁量原則自己決定，把選擇與理由寫進報告即可。

**批 A 做完可以直接接批 B**，不必等批 A 放行——批 B 全程在獨立 clone，不碰現有 repo，失敗回退成本是零。兩批可以一起交。

`scripts/ddreport.py` 同時只能一人動——開工前先 `git status --short scripts/`，若有別人的改動，先回報再說。

## 一、絕對不能動的（動了整份工作作廢）

沿用 `_codex_brief_dd_overhaul_20260906.md` 第二節全部八條，重述關鍵四條：

1. **判斷規則語意**：`.claude/skills/` 下任何檔一字不改（含 `references/v16/*.md`、SKILL.md）。
2. **決策矩陣**：`scripts/dd_decision.py` 的裁決邏輯與 `scripts/dd_schema/decision_inputs.md`。
3. **judgment schema 的 required 集合**：`scripts/dd_schema/judgment.schema.json` 可加選填欄，不可刪、不可改名、不可改 enum。
4. **dd-meta 契約**：brief 與完整版內嵌的 dd-meta 欄位名與型別。本委託只擴大「誰會被檢查」，不改「檢查什麼欄位」。

另加本委託專屬三條：

5. **不得調整任何閘的閾值或判準內容**。本委託全部是「讓既有閘掃得到、失敗時擋得住」，不是改判準。要改判準得走 `knowledge/rule_ledger.md` 的 kill condition 程序。
6. **不得 force push、不得 rebase、不得 `reset --hard`、不得 stash**。本機 main 與 origin/main 早已分岔且多 session 共用工作樹，任何一個都會吃掉別人未 commit 的編輯。
7. **不得跑 `ddreport.py run／finish／batch`，不得 spawn 模型（`claude -p`）**。驗證一律走 `--dry-run`、`--replay-from`、`scripts/tests/fake_claude.py` 與單元測試。

## 二、階段 1：P0-1 critic gate fail-closed

**現況**（複審 §1 P0-1 錨點）：`scripts/ddreport.py:2089-2098` 在 `dd_gate.py` 不存在時記 `SKIPPED` 回 0；`:2169-2183` 在 parse rc 非 0 或 JSON 壞掉時 `parsed=None`，下一行 `(parsed or {}).get("red", 0)` 得 0；`:2283-2299` 見 red=0 記 `PASS`；`:3630-3635, 3675-3679` 兩處 loop 把 `SKIPPED` 當成功。

**要做到**：

- parse 子行程 rc 非 0、stdout 不是 dict、必要計數鍵（至少 `red`）缺失 —— 一律 stage＝**FAIL**，並把 parser 的原始 stdout／stderr 原文印出來（截斷可以，但要看得出是什麼壞掉）。
- `dd_gate.py` 檔案缺失 —— **FAIL**，不是 SKIPPED。
- `SKIPPED` 只保留給「該段在此模式下明確不適用」，且 v17 必經的四個 critic gate 不得使用。
- 兩處 loop 對 FAIL 的處置與現有 FAIL 路徑一致。

**驗收（你自己先跑，把原始輸出貼回報）**：

- 新增至少兩個零 LLM 單元測試：①parse rc 非 0 ②rc 0 但 stdout 是壞 JSON。兩者都必須讓 `_gate_finalize_from_audit()` 回非 0 且 stage＝FAIL。
- `python3 -m pytest scripts/tests -q`（基準 127 passed，新增測試後應為 129+，不得有 fail）。
- 確認既有測試「已有 audit 時不重派」「無 audit 時回完整 gate」仍過。

### 階段 1b（指揮者 2026-09-07 審 diff 時新發現，併入階段 2 一起做）

`scripts/ddreport.py:2372-2378, 2408`：`dd_brief.py` 不存在時 brief 段記 `SKIPPED` 並回 0，而 `cmd_run` 對非 gated 段仍把 `SKIPPED` 當成功——**快速版是 v17 的預設產物，這段與 P0-1 是同一類 fail-open**。目前 `scripts/dd_brief.py` 存在，所以沒有實際觸發，但保護不該建立在「檔案剛好還在」上。

要做到：`dd_brief.py` 缺失時 brief 段 FAIL（比照 gated），且 `cmd_run` 的 `stage_succeeded` 把 `brief` 一併排除在 `SKIPPED` 之外。補一個對應單元測試。

## 三、階段 2：P0-2 brief 接進 schema gate

**現況**（複審 §1 P0-2 錨點）：`scripts/hooks/pre-commit:55-56, 170-180` 有抓 `STAGED_BRIEF`，但 `TARGETS_DD` 只在 `STAGED_DD` 非空時設定；`scripts/verify_dd_math.py:71-90, 194-210` 對缺 dd-meta 或壞 JSON 回 `None` 後 `continue`，rc 仍 0；`scripts/qc.py:402-425` 只認父目錄 `dd` 且檔名 `DD_` 開頭；`scripts/validate_dd_meta.py:447-465` 無參數全掃只 glob 根目錄；`.github/workflows/validate_dd_meta.yml:15-29, 42-43` path trigger 不含 brief。

**要做到（五處，缺一不可）**：

1. `validate_dd_meta.py` 預設 targets 納入 `docs/dd/brief/BRIEF_*.html`。
2. pre-commit 的 `TARGETS_DD` 納入 `STAGED_BRIEF`（只改 brief 的 commit 也要送進 validator）。
3. `qc.py::is_dd_html()` 認得 brief 路徑。
4. CI workflow 的 path trigger 加 `docs/dd/brief/**`，且執行的 validator 參數涵蓋 brief。
5. `verify_dd_math.py`：**明示傳入**的 v15／BRIEF 檔若無法解析 dd-meta，一律 FAIL，不得顯示「驗算 0 檔，全數通過」。`--all` 掃描模式對非目標檔可維持略過，但 checked=0 時的訊息不得是「全數通過」。

**驗收**：

- 造兩個 `/tmp` fixture（**放 `/tmp`，不得放 `docs/`**，見 CLAUDE.md 並行 session 紀律第 4 條）：`/tmp/BRIEF_NOMETA.html`（無 dd-meta）、`/tmp/BRIEF_BADJSON.html`（dd-meta 壞掉）。兩者傳給 `verify_dd_math.py` 必須 rc 非 0。
- `python3 scripts/verify_dd_math.py --all` 仍應掃到 48 份 v15+（含 13 份 brief）且全過。數字若不是 48／13，先回報再繼續。
- `python3 scripts/validate_dd_meta.py`（無參數）輸出的檔數應含 brief；貼出前後對照。
- `python3 -m pytest scripts/tests -q`、`python3 scripts/qc.py --all`（errors 必須 0；warnings 存量 4796 是既有基準，不在修復範圍）。
- 用 `git stash` 以外的方式驗 pre-commit：在暫時 worktree 或用 `GIT_INDEX_FILE` 造一次只 staged brief 的情境，確認 validator 真的被呼叫。**不要用 stash。**

## 四、階段 3：P0-3 finish 同步失敗必須擋住發布

**現況**（複審 §1 P0-3 錨點）：`scripts/ddreport.py:3488-3505` 先寫 INDEX、再跑 `update_dd_index.py`，rc 非 0 只 warn 就繼續 archive／commit／push；`scripts/update_dd_index.py:3068-3077, 3103-3118, 3135-3148, 3150-3164, 3166-3187` 的 screener、供應鏈、picks、consumer layer 失敗全部只警告。

**要做到**：

1. **「DD 必須同步的最小權威集合」＝ `docs/research/index.html` 主表 ＋ `docs/dd-screener/latest.json`（指揮者 2026-09-07 已決，不用再問）**。理由：finish 的 commit subject 寫的就是 `resync research+screener`，這兩支是發布承諾本身；其餘（供應鏈、picks、consumer layer）維持 warn，但失敗必須在 finish 結尾明列，不得只印在中間被刷掉。若你在實作中發現某支其實也屬於發布承諾，**照你的判斷加進去並在報告說明**，不要停下來問。
2. `update_dd_index.py` 對該集合聚合 rc；集合內任一失敗 → 整體回非 0。
3. `_do_finish()` 收到非 0 → **停止，不 archive、不 git add、不 commit、不 push**，並印出是哪一支失敗。
4. INDEX 寫入改成暫存後原子替換，或在失敗時可恢復——不得留下半寫狀態。

**驗收**：

- 單元測試 monkeypatch `subprocess.run(update_dd_index)` 回 rc 1，斷言：沒有 archive、沒有 `git add`、沒有 commit、沒有 push，且 INDEX 不是半寫。
- 反向測試：rc 0 時流程與現在完全相同。
- 與 Phase 3 `--sync-later` 崩潰不變量（複審 §3 第 2 點）**做成同一個可恢復的 finish state，不要各造一個旗標**——這是硬約束，做法由你定。**不用先送設計等核可**，直接實作，把一頁設計寫進交件報告即可。
- `python3 -m pytest scripts/tests -q` 全過。

## 五、階段 4：Git 分岔整併（方案 A，只做到 integration branch）

**現況快照（2026-09-07，會漂移，開工時重取）**：

- `merge-base HEAD origin/main` ＝ `89e11fca6779bc9f4f7c9af445a91e2b4e463138`
- `rev-list --left-right --count HEAD...origin/main` ＝ `54  58`
- local-only（無遠端 patch-equivalent）9 顆：

```
25589b2c0  ddreport：WP4b 散文層（--full）落地
e9a87c419  dd_flash：閃判（即時裁決層）
f74194269  dd_flash：WDC 首跑修三處
0d52b1bbf  AGENTS.md：寫程式 agent 的改動紀律
44c796ca8  AGENTS.md＋Codex 委託書（此條已被 09-07 角色分工作廢，移植前先問）
90d127d95  ddreport：30 天結構證據沿用＋平行度 8＋批尾同步＋分段帳
90081f51d  機械驗算閘接回快速版
5e8cc8b14  CLAUDE.md：改產物路徑必須點名既有閘
95f35ba54  ddreport：finish 三方一致性硬閘＋三個衍生欄改由腳本算回
```

- remote-only 13 顆。兩端 tree 仍差 800+ 檔，大宗是 `data/weekly_cache_universe/*.json`。

**要做到（嚴格照複審 §4.2）**：

1. 在 repo **之外**建立獨立 clone（例如 `/tmp/fab-integration`），以 `origin/main` 為底開 `integration/20260907` branch。**不碰現有 repo 的 `.git`、index、working tree。**
2. 對 9 顆 local-only 逐顆判斷：先用 `git show origin/main:<path>` 或 blob hash 比對相關檔，**內容已相同就略過**；真的缺才以 cherry-pick 或檔案 patch 移植。**按檔案清單與 blob hash 驗收，不得按 commit subject 猜。**
3. 對 13 顆 remote-only 做同樣的檔案級審核。
4. 生成資料（`data/weekly_cache*`、`data/*_prices.json`）不是真相來源，以 origin/main 為準，不要為了 tree 一致而移植本機 cache。
5. 跑全套測試與 qc；確認 integration tree 是預期真相。
6. **到此停下。** 交一份驗收報告：每顆 commit 的處置（略過／移植／待裁決）、理由、blob 對照證據、測試輸出。**不得推 main、不得 fast-forward、不得碰現有 repo 的分支指標或 checkout。**

**失敗回退**：廢棄該 clone／branch 即可，現有 repo 完全不變。

**明著邀請你反對**：若你認為方案 B（真 merge 保留雙方 topology）或方案 C 更好，或你在逐檔比對中發現複審 §4.1 的證據有誤，把分歧點列出來交給指揮者裁決——分歧本身是訊號，不要為了跟指揮者一致而收回意見。

## 六、工作方式與回報

- Python 3.9 相容；中文全形標點；每處改動附「2026-09-07：為什麼」一行註解。
- **你只交 diff 與報告，不 commit、不 push。** 放行權在指揮者。這條不放寬。
- 每批回報固定四段：①改了哪些檔（逐檔一行）②驗收命令與**原始輸出**（不要摘要成「全過」）③你自己做了哪些裁量決定、理由是什麼④你不同意或認為指揮者寫錯的地方。

### 什麼時候該自己決定，什麼時候該停

**自己決定，寫進報告就好**（不要為這些回來問）：

- 實作細節、函式切法、測試怎麼寫、錯誤訊息文字。
- 型別／契約層的額外防呆（例如階段 1 你自己加的「`red` 必須是整數」——那是對的，繼續這樣做）。
- 本委託寫的數字或行號與實際不符（檔案漂移了、我抄錯了）：**以實際程式碼為準往下做**，在報告第④段點名哪裡不符。
- 基準數字對不上，但 **errors 仍為 0、pytest 無 fail、`verify_dd_math` 無 FAIL**：往下做，在報告記下新舊數字。warnings 存量不是本委託的修復範圍。
- 委託書某一小步你認為做法更好：照你的做法做，理由寫報告第③段。

**一定要停下來**（這四條不放寬，是真的安全網）：

1. **errors 級失敗**：`qc.py` errors > 0、`pytest` 有 fail、`verify_dd_math.py` 有 FAIL、`validate_dd_meta.py` 報錯。
2. **要動第一節禁區**才能完成任務——包含發現「不改判準就修不好」的情況。
3. **要碰現有 repo 的分支指標、index、checkout，或要 push**。
4. **機械檢查與 LLM 閘的結論方向不同**，或閘 🔴 ／🟡 指向數字口徑。

WHY 這樣分：2026-09-06 WDC 那次的失效不是「沒停下來問」，是**明知數字對不上還照樣 push**。真正的安全網是上面四條，不是每一步都回報。反過來，把「任何一個數字對不上」當阻斷級，會讓一個我抄錯的 warning 計數擋掉一整輪工作——那已經發生過一次。

- 判斷登入狀態不要用 `claude auth status`（不是子指令）；用 `claude -p "Reply with exactly: OK" --model claude-haiku-4-5-20251001 --output-format json` 看 `is_error`。

## 七、基準數字（驗收時對照）

**用法改了（2026-09-07）：不要拿本表的數字當硬條件。** 開工第一件事是自己跑一次下列四條取得**當下快照**，收工再跑一次比對；本表只是給你一個量級參考，工作樹每天都在被別的 session 改。

| 項目 | 2026-09-07 參考值 | 判定方式 |
|---|---|---|
| `python3 -m pytest scripts/tests -q` | 133 passed | **不得有 fail**；passed 數只增不減 |
| `python3 scripts/qc.py`（changed 模式） | 529 檔／0 errors／361 warnings | **errors 必須 0**；warnings 變動只需記錄 |
| `python3 scripts/qc.py --all` | 2462 檔／0 errors／4796 warnings | **errors 必須 0**；warnings 變動只需記錄 |
| `python3 scripts/verify_dd_math.py --all` | 48 份 v15+（含 13 份 brief）全過 | **不得有 FAIL**；份數變動只需記錄 |

**只有粗體那一欄是阻斷級。** warnings 計數、檔案份數、passed 總數的變動一律是「記錄下來繼續做」，不是停下來問。

**2026-09-07 沿革**：本表原把 361 warnings 誤標為 `--all` 的基準，實際 361 是 changed 模式（529 檔）的數字，`--all`（2462 檔）本來就是 4796。階段 1 因此被擋下一輪——停在數字對不上是**當時規則下的正確動作**，錯的是委託書。這次修訂把「數字對不上就停」收窄成「errors／fail／FAIL 才停」，就是為了不再讓抄錯的計數吃掉一整輪工作。

## 八、批 A 補件（指揮者 2026-09-07 審完 diff 後開的五件，跟批 B 一起做，不必分開交）

批 A 已放行並 commit（`f5e57eba1`）。指揮者獨立重跑四道閘，數字與回報**完全一致**，設計（單一 `finish.site_sync` 狀態機、INDEX 回滾、screener rc=0 仍驗 latest.json 是合法 object）也接受。以下是審 diff 時找到的落差，都不推翻已放行的部分。

### 8.1 `--skip-dd-screener` 單獨使用不該回非零（優先）

現況：`update_dd_index.py` 收到該旗標一律 `required_failures` → rc 1。但 `ddreport finish`／`batch-sync` 已經在**呼叫端**直接拒絕這個旗標了，這是真正的閘；讓旗標本身永遠回非零，等於把 CLAUDE.md 明文記載的離線 maintenance 路徑（「要離線跑加 `--skip-dd-screener`」）變成永遠失敗。

要做到：單獨執行時回 **0**，但在結尾印一行明確的「本次不是發布級同步，`latest.json` 未重建」；發布路徑的保護維持在 `ddreport` 呼叫端。CLAUDE.md 對應段落我已改成「降為 maintenance 旗標，不得用於發布」，語意要對得上。

### 8.2 pending 同步失敗會鎖死所有後續 run（優先）

`_recover_pending_site_sync()` 在 `cmd_run`／`cmd_batch` 開頭跑，rc 非 0 就直接 return。若某個 pending manifest 進入無法自癒的狀態（報告檔被手動刪、screener 持續失敗），**每一次 `ddreport run` 都會拒絕開工**，而且錯誤訊息沒告訴人怎麼解。

要做到：①錯誤訊息明列是哪一檔、哪個 manifest、怎麼清；②給一個逃生口（`--skip-pending-sync` 或連續失敗 N 次後自動 quarantine 該筆並降為警告）。做法你定，但「一筆壞資料鎖死整條管線」不可以留著。

### 8.3 INDEX.md 回滾後 `_body.html` 仍留著該列

`_remove_index_row()` 只回滾 `INDEX.md`。但 `update_dd_index` 是先重生 `_body.html`、後跑 screener；screener 失敗時 `_body.html` 已經含該列。結果是兩檔不一致的半完成狀態，雖然都未 commit，但在多 session 共用工作樹下有被別人 `git add docs/` 掃進去的風險（CLAUDE.md 並行 session 紀律第 2 條）。

要做到：回滾時一併把 `_body.html` 還原（最簡單是回滾 INDEX.md 後重跑一次純 research 重生，或先備份原檔再原子還原）。

### 8.4 `brief` 鍵造成 13 個永久 warning，且每新增一份 brief 就多一個

`validate_dd_meta.py` 對每份 brief 報 `unknown dd-meta key: 'brief'`。這是 v17 的正當欄位，不是異常。**把 `brief` 加進 validator 的 whitelist**——這是動 validator 的白名單，不是動 dd-meta 契約欄位，不在第一節禁區。warning 存量會回到批 A 之前的量級，訊號才不會被雜訊蓋掉。

### 8.5 CI 的 glob 在 brief 目錄為空時會傳字面字串

`.github/workflows/validate_dd_meta.yml` 的 `python scripts/validate_dd_meta.py docs/dd/DD_*.html docs/dd/brief/BRIEF_*.html` 在 shell 展不到檔時會把字面路徑傳進去。今天有 13 份所以不會發生。低優先，順手處理即可（`shopt -s nullglob`，或改回讓 validator 用自己的預設 targets）。
