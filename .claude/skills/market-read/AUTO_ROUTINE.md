# market-read-auto 雲端排程指令

雲端 routine `market-read-auto`（`trig_01Tz5DNBvZRjM9LoFQhr5vui`，台北週一至週五 17:15）的完整指令。routine 本身的 prompt 只叫 session 讀這個檔照做；要改排程行為就改這個檔（2026-09-24 起，原本整段寫在 routine prompt 裡）。

你在 InvestMQuest research repo（keigoks-ivan/financial-analysis-bot）的雲端 session，任務是市況主控台判讀層的自動判讀（訂閱版，2026-09-13 起改為固定證據版本流程；2026-09-15 起改為每日 17:15 台北檢查、有新證據版本就判讀）。只用本帳戶訂閱額度，沒有 API 或額外用量備援；額度耗盡、輸入缺失、數字不一致或審核未通過就停止，不換 API、不改舊判讀日期、不繞過驗證。對話輸出保持精簡：進度一兩句＋最終一行總結。

## 步驟

① `bash scripts/install_hooks.sh`；`git log -1 --oneline` 確認在最新 main。

② 零成本狀態檢查：`python3 scripts/check_read_triggers.py --json` 只作紀錄（把 run_read 與 reasons 寫進最終總結），不作為是否研究的門檻。若 `docs/market/data/read.json` 的 as_of 已是今天（台北），結束（同日不重做，不改檔、不 commit）。其餘情況一律進③，是否研究由 prepare 的證據版本判定決定。

③ 固定證據：不要抓來源（GitHub Actions 每天 07:30／16:30 台北已把 `data/market_sources/` 與 `docs/market/data/state.json` 更新並保存版本）。執行 `python3 scripts/market_refresh.py prepare`（預設讀 docs/market/data/state.json）。讀 stdout 的 run_dir、snapshot_id、run_analysis、mode、errors、warnings。errors 非空就回報來源失敗並結束，不研究；run_analysis=false（證據版本與上次判讀相同）也結束（不改檔、不 commit）。mode=weekly（台北週一）時，研究要重讀前期假設、來源缺口與已結算結果。

④ 研究：讀 run_dir 內 evidence.json（唯一證據）與 request.json（前期判讀、期間比較、缺口）、`python3 scripts/build_market_state.py --evidence-pack --source-evidence data/market_sources/latest.json` 的純文字證據包、最新 `docs/intel/data/YYYY-MM-DD.json` 的 brief_zh、上一期 `docs/market/data/read.json` 與 `read_history.jsonl`。依 `.claude/skills/market-read/SKILL.md` 的骨架、憲法與「可讀性硬規則」寫候選稿到 run_dir/candidate.json（schema market-read-v1 全部必要欄位），另加：
- snapshot_id（取自 request.json）、billing="subscription_only"。
- vs_prior_zh：哪些論點得到支持／被削弱／被推翻，上期改判條件逐條現況，預測的計算基準若有變動要明寫。全部用白話，不寫命題、證偽表、口徑、參考點這類內部用語。
- data_gaps_zh：只寫會影響本期判斷的缺口，≤ 150 字。request.json 的 warnings 逐條清單頁面已自動列出，不重抄。
- observations[]：每個被引用的 ref 帶 field=num／pctile／chg30_pct、value 與 as_of，必須逐字等於 evidence.json 的 quotes 同欄位。
- scenarios[]：基準／偏強／偏弱各含 name_zh、horizon、conditions_zh、falsifiers_zh、asset_implications_zh、refs。

as_of 必須是今天（台北）。同源指標不當多份獨立證據；沒有可辯護依據的機率不要編；命題表不因命題沒有優勢就抽掉（記分需要沒有優勢的樣本）。正文裡每一個數字（含週變動、日變動、差距）都必須在 evidence.json 或 request.json 的 history_context 逐字可查；查不到的數字一律不寫，不得用心算、外推或站內其他檔案補上。

④b 可讀性先過（2026-09-24 新增）：`python3 scripts/check_market_read.py --file <run_dir>/candidate.json`。第 11 項（術語白話）與第 13–17 項（標題句、句長與數字、內部用語與比喻、出處位置、缺口字數）沒過就照訊息改寫再跑，最多 3 輪，過了才進⑤。改寫時數字只能刪，不能換成證據裡查不到的數字。其他項目若因候選稿尚未落帳而 FAIL（如 claim_ids），這裡先不管，以⑥ validate 為準。3 輪仍不過就寫 read_status.json（status failed、stage readability、reasons 列出沒過的項目）並結束，不落帳、不改 read.json。

⑤ `python3 scripts/market_refresh.py fingerprint --candidate <run_dir>/candidate.json` 取得 content_hash。用 Agent 工具開冷讀 subagent（2026-09-23 起：本 session 是 claude-opus-5-5，冷讀 subagent 用 claude-fable-5-1；SKILL §5.2 的配對表尚未列這一組，以本行為準，寫與審仍然永不同模型），職責書逐字照 SKILL §5.3，附上 candidate.json、evidence.json、state 的 council_summary 與 fuses、上一期 read.json；subagent 只回報 JSON review。把 review 寫進 candidate.json 的 review 欄（model、snapshot_id、content_hash、verdict、round、findings）。有 🔴 或 blocking 就修稿一次、重跑④b、重算 fingerprint、重審一次；修稿時被指出無錨的數字要直接刪掉或改寫成不帶數字的句子，不得換成另一個證據包裡查不到的數字（2026-09-15 第 2 輪就是這樣失敗的）。仍不合格就寫 read_status.json（status failed、stage cold_read）並結束，不落帳、不改 read.json。

⑥ 驗收與落帳，順序固定：
- `python3 scripts/market_refresh.py validate --candidate <run_dir>/candidate.json`（必須 status=validated，errors 為空）
- `TZ=Asia/Taipei python3 scripts/ledger_from_editorial.py --source market-read --file <run_dir>/candidate.json`（乾跑，有拒絕就停止）
- `TZ=Asia/Taipei python3 scripts/ledger_from_editorial.py --source market-read --file <run_dir>/candidate.json --write`（回填 claim_ids[]；把 id 依序填進 horizons[].claim_ids（前三張＋第四張進 3m）與對應 falsifiers[].claim_id）
- `python3 scripts/market_refresh.py accept --candidate <run_dir>/candidate.json`（乾跑）
- `python3 scripts/market_refresh.py accept --candidate <run_dir>/candidate.json --write`（保存新判讀、快照與發布包；status 應為 ok 或 degraded）
- `python3 scripts/qc.py` 必須 PASS。

⑦ `docs/market/data/read_status.json` 寫 {"as_of": "<今天>", "status": "ok", "stage": "auto", "reasons": []}；任一關卡失敗則不改 read.json、不落帳，寫 status failed 與 stage、reasons，只 stage 這一個檔並單獨 commit push。

⑧ 成功時只 stage：docs/market/data/read.json、read_history.jsonl、read_status.json、refresh.json、docs/market/data/snapshots/、docs/market/data/releases/、knowledge/forecasts.jsonl（不得 git add -A）。`git config user.name "github-actions[bot]"`、`git config user.email "github-actions[bot]@users.noreply.github.com"`，commit 訊息 `market-read 自動判讀 {as_of}：{thesis 前 30 字}`，結尾 `Co-Authored-By: Claude <noreply@anthropic.com>`；`git pull --rebase origin main` 後 `git push origin main`，失敗重試 3 次。推送前若 read.json 已被更新（refresh.json 的 snapshot_id 改變），重新 prepare 與驗證，不覆蓋較新成果。

## 硬規則

描述器紀律（不下買賣指令）、白話（術語首現括號；照 SKILL「可讀性硬規則」）、每個判斷句錨定活數字並帶資料日期、不改機械層任何檔、不用 --no-verify、不改 routine 以外的排程。

最終一行總結：是否判讀、snapshot_id 前 8 碼、主張一句、落帳張數、accept 狀態、push 是否成功。
