---
name: market-read
description: market-read — 市況主控台判讀層（週頻＋事件觸發，2026-10-13 起降為文字評論）。orchestrator 讀證據包後寫 docs/market/data/read.json（三股力量／傳導／部位／類比／各期限文字判讀／證偽表；不寫機率、不落帳），機械 critic 過後頁面 /market/ 第一屏渲染。觸發：「跑市況判讀」「market read」「本週市況判讀」「更新市況主控台判讀」。
---

# market-read v1.6（2026-10-15，加那斯達克與半導體段落）

**2026-10-13 降級（持有人拍板，rule_ledger #137 判紅）**：market-read 的序貫檢定（SPRT）已判紅（21 筆、累積證據分 −4.66、技巧分 −0.66），判讀層降為**文字評論**。從此：①`read.json` 不再寫任何機率與命題（`mode: "commentary"`，`forecasts`、`claim_ids`、`deviations_from_tables` 皆為空，`horizons[]` 只留 `key`／`label`／`logic_zh`）；②不再執行 `ledger_from_editorial.py --source market-read`（腳本已直接略過）；③頁面不顯示判讀機率；④歷史命題與記分保留在帳簿，照常結算。以下步驟中凡涉及機率、命題、落帳、與帳簿表格分歧的項目，一律以本段為準（跳過）。

**定位**：`/market/` 是機械證據層（日更、零 LLM）＋判讀層（本 skill）兩層。判讀層回答「未來 3／6／12 個月股市的可能方向與背後邏輯」，只給文字判讀，不給機率。設計凍結稿：`notes/site-internal/root/_market_read_design_20260903.md`（機率與記分部分已作廢）。**判讀者＝orchestrator（opus 級），不外包給 sonnet、不上 cron。**

**白話關卡（持有人 2026-09-03 指出漏掉，列為硬規則）**：判讀文字＝外資券商白話，照 `_plainlang_styleguide.md` 四句式——每個術語在同一欄位首次出現必附「術語（一句白話）」（期限溢價（投資人要求多付的長債補償）、解壓縮（頂端無事、底層失血）、NAAIM（主動經理人曝險調查）…），先講為什麼再列數字，短句、一句一個意思；頁面永遠不露 `monitor:dgs10` 這類代碼與 SPRT／LLR／n_eff／orchestrator 等內部詞（顯示層用「序貫檢定」「累積證據分」「有效樣本」「站方判讀」）。`check_market_read.py` 的 `jargon_gloss` 必須通過（2026-09-24 起為 FAIL）。**適用範圍不只 `read.json`**——同一把尺也涵蓋 `docs/market/index.html` 的手寫文案與 `scripts/build_market_state.py` 的機械模板句（`judge_word()`／`build_read_zh()` 等）；任何一處新增讀者可見字串，動筆前都要先過這關（對照表見 `_plainlang_styleguide.md` §2.11「市況主控台」）。

**可讀性硬規則（持有人 2026-09-24 看 9/24 判讀「很不通順」後加；`check_market_read.py` 第 13–17 項 FAIL 擋下）**：
- **標題句**：`thesis_zh`、`path_zh`、`vs_prior_zh`、每筆 `horizons[].logic_zh` 的第一句是頁面上的標題，≤ 40 字、最多 1 個數字，直接講結論。例：「長天期利率也開始漲了，股市短線偏弱的理由出現。」
- **其他句子**：一句只講一件事。去掉括號後 ≤ 60 字、最多 3 個數字（日期、年期、「3 個月」「200 日線」這類名稱不算；括號裡的分位數要算）。「；」也算一句的結尾，不要拿它把好幾件事黏成一句。數字放不下就挑最重要的，其餘留給頁面上的數據區。
- **不用內部用語**：命題→預測；證偽表→改判條件；參考點→「9/23 收盤價」這類具體說法；官方序列／監測序列→官方資料；判讀者→「我」或省略。帳簿、帳上、口徑、型別、結算、交代、裁量、觸發者、「弱的那段」都不寫。
- **不用比喻**：門口、骨牌、到場、掩護、雪崩、天花板、煞車。直述事實。
- **出處放句尾**，寫成「（鉅亨 9/24）」；不寫「情報摘要」。
- **`data_gaps_zh` ≤ 150 字**：只寫會影響本期判斷的缺口。逐條缺料清單頁面上方已機械列出，不重抄。
- **同一件事全頁只講一次**：主張、路徑、相較前期不要各換一種說法重講同一個結論。
- 寫完先跑 `python3 scripts/check_market_read.py --file <稿>`，第 13–17 項沒過就照訊息改寫再跑，改到過為止（最多 3 輪）；**這一步在冷讀之前做**，因為冷讀後改正文要重審。

**憲法**：描述器紀律（只講條件與事實；不寫機率；禁「買／賣／加碼／減碼／避開／進場／出場／建議」）；不是收斂面；每個判斷句錨定一個 ref（`monitor:<key>`／`internals:<key>`／`stress:<欄>`／`cot:<市場>`／`flow:<欄>`／`theme:<主題>`／`book:<欄>`）並帶 as_of；白話全形（`_plainlang_styleguide.md`）；不改任何機械層檔案。

## 步驟

1. **讀證據**（全部唯讀）
   - `python3 scripts/build_market_state.py --evidence-pack`（純文字證據包：利率／信用／內部分裂／勞動與通膨／流動性／匯率與商品／部位與流量／事件與地緣，每數字帶 as_of）。
   - `docs/market/data/state.json`：`council`／`council_summary`（表格 p）、`fuses`、`anomalies`、`stock_pulse`、`scoreboard`。
   - 最新 `docs/intel/data/YYYY-MM-DD.json` 的 `brief_zh`；`docs/macro/` 各報告的 kill 表現值（state.fuses 已含）。
   - **上一期** `docs/market/data/read.json` 與 `docs/market/data/read_history.jsonl`：判讀要對上期負責——哪些證偽被觸發、上期各期限文字判讀是否被證據撐住。
2. **寫 `docs/market/data/read.json`**（schema `market-read-v1`，逐欄照首份 2026-09-02 版）：
   - `thesis_zh` 第一句是一句主張（標題句規則），後面才是撐它的證據；`path_zh` 路徑句（先弱後強／先強後弱／區間…＋觸發者）。
   - `vs_prior_zh`（相較前期）：**第一句必須是一句白話結論**，≤ 40 字、最多 1 個數字、以句號收，讀者不看後文就知道上期看法對不對、方向有沒有變（例：「上期的看法大多被這週的證據撐住，方向沒變。」）。不得用「對上期負責」「N 張命題未到期」「證偽表十條有一條觸發」這類記帳語開頭。記帳明細從第二句起寫，也要用白話：「上期八個預測都還沒到期；十個改判條件都沒碰到，其中三個接近了。」頁面「本期重點」直接取這一句當首句；`check_market_read.py` 第 12 項 `vs_prior_lead` 會 FAIL 擋下超過 60 字或含「命題／負責／證偽表／到期／觸發」的首句（2026-09-17 持有人指出舊寫法沒人看得懂）。
   - `headline_zh`、`thesis_points`（2026-10-27 起每期必寫，`check_market_read.py` 第 19 項；機械層缺這兩欄時仍可過，舊判讀不用補）：首頁、/market/、email 共用的卡片來源。`headline_zh`＝首頁一句結論，≤ 40 字、只有一句、最多 1 個數字、句號收；沒有它，卡片會退回 `thesis_zh` 第一句。`thesis_points`＝把 `thesis_zh` 拆成 2–4 條 `{claim_zh, refs[{ref, why}]}`：`claim_zh` ≤ 30 字的完整主張，每條 1–3 個 ref，ref 必須在同一份稿的 `observations`；`thesis_zh` 提到的每個論點（如油價）都要有對應一條。白話規則同上方「白話關卡」與 `zh-analyst-prose`：一句一個主數字、術語首現就地解釋、半形空格隔中文與數字、全形標點、不用比喻、不寫「不是 A，是 B」收尾句、數字只取自證據。
   - `horizons` 三筆（key 依序 `3m`／`6m`／`12m`）：只寫 `key`、`label`、`logic_zh`，**不寫** p_up／p_dd10／p_dd20／p_clim／claim_ids／resolve_by；`logic_zh` 講清楚該期限的方向看法與理由，第一句是結論標題句，文字裡也不出現機率或歷史頻率數字。
   - `forces` 2–4 張，每張 refs ≥2、每個 ref 一句「為什麼看它」。
   - `transmission` 四格（erp／credit／split／liquidity）各一句判讀。
   - `positioning_zh`：機械賣家 vs 裁量避險、波動錯價。
   - `sector`（2026-10-15 起每期必寫，`check_market_read.py` 第 18 項；起因：10/05–10/14 費半領跌、判讀只看 SPY 而漏看）：`{"body_zh": "…", "refs": [{"ref": "…", "why": "…"}]}`。`body_zh` 講三件事：①費半與那斯達克的走勢與集中度（`monitor:sox`／`monitor:sox_ndx`／`monitor:ndx`／`internals:qqew_qqq`）；②那斯達克期貨投機部位與主題擁擠（`cot:Nasdaq-100 E-mini`、`theme:*`）；③實盤指數部押在半導體的比例與離週線閘門多遠（`book:*`，例如 SMH 現持 50%、SMH 每跌 10% 美股指數部少 5%）。只描述集中程度與距離，不寫任何加減部位的話。refs ≥3，費半、那斯達克、實盤部位各至少一條；第一句是標題句（≤ 40 字、最多 1 個數字）；被引用的 ref 一樣要進 `observations`。
   - `analogs` 2–4 個：吻合特徵各附 today_ref，**必附不同之處**與當年結果。
   - `falsifiers` 6–10 條，**至少 2 條轉多**；可用 `field: "chg30_pct"` 對 30 天變化設門檻。
   - `deviations_from_tables`：固定 `[]`（不再有機率可比）。頂層加 `"mode": "commentary"`。
   - `forecasts`、`claim_ids`：固定 `[]`。證偽表 `falsifiers[]` 照寫，但不帶 `claim_id`。
   - `assumptions.spx_fwd_pe` 寫來源。
3. **機械 critic**：`python3 scripts/check_market_read.py` 必須 PASS（FAIL 不得落帳；WARN 要在複審時說明）。可讀性（第 13–17 項）沒過就改寫再跑，最多 3 輪。
4. **不落帳**：2026-10-13 起不再執行 `ledger_from_editorial.py --source market-read`。只 append 一行到 `docs/market/data/read_history.jsonl`（`claim_ids` 為空）。
5. **重建合成層**：`python3 scripts/build_market_state.py`；本機 `python3 -m http.server` 開 `/market/` 看第一屏與證偽表現值。
6. **停下複審**：列出主張、各期限文字判讀、證偽表；持有人說 push 才 commit（只 stage：read.json、read_history.jsonl、state.json）。

## 節奏與觸發
- 週頻：每週一台北上午（週日 crossasset／crowding 已更新）。
- 事件觸發（任一）：壓力分數週變動 ≥10；任一引信觸及；VIX 收 ≥25；判讀 as_of 超過 10 天（頁面已灰化）。
- 不因單日新聞改判讀；新聞進 `forces` 的證據列，不進機率，除非它改變了某個 ref 的數字。

## 記分與 kill（rule_ledger 已登記）
- source `market-read`：SPRT 已於 2026-10-13 accept_h0，判讀層降為評論（上述）；歷史命題照舊結算。若要恢復機率判讀，須經校準輪重設並在 rule_ledger 重新登記。
- 正面義務：一週一次（降為評論後，不再有「無命題視為未完成」）。
- 判讀者的自我校準：先看上期文字判讀哪些論點被證據撐住、哪些被推翻（`vs_prior_zh`），再寫新判讀。

## Auto 模式（2026-09-03 全自動化；雲端 routine `market-read-auto`）

**2026-09-24 起 routine 實際執行的指令在同目錄 `AUTO_ROUTINE.md`**（routine prompt 只叫 session 讀該檔照做）；下面的步驟是 09-03 版設計紀錄，兩者不一致時以 `AUTO_ROUTINE.md` 為準。

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
   f. （2026-10-13 起不再落帳）append 一行到 `docs/market/data/read_history.jsonl`，`claim_ids` 為空。
   g. `python3 scripts/build_market_state.py` 重建合成層；`python3 scripts/qc.py` 必須 PASS。
   h. 把最後一輪 `review`（模型、verdict、輪次、findings）寫入 `read.json.review`（供頁面「判讀記分」區與 email 摘要顯示）。
4. **寫 `docs/market/data/read_status.json`**：
   - 全部關卡通過 → `{"as_of": ..., "status": "ok", "stage": "auto", "reasons": []}`。
   - 任一關卡失敗（冷讀 2 輪後仍 🔴／機械 critic FAIL／qc 失敗／push 三次失敗）→ **不改 `read.json`、不落帳**，寫 `{"as_of": ..., "status": "failed", "stage": "<失敗的關卡>", "reasons": [...]}`，只 stage 這一個檔並單獨 commit push（`.github/workflows/market-read-notify.yml` 偵測到會寄失敗信）。
5. 成功時只 stage：`read.json`、`read_history.jsonl`、`read_status.json`、`state.json`——**不得 `git add -A`**。
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
2. **內部一致性**：三個期限的文字判讀互相說得通；證偽表方向與主張一致；各期限文字不得出現機率或歷史頻率數字（2026-10-13 起降為評論）。
3. **（已停用）** 2026-10-13 起無機率，不再有與帳簿表格的分歧可審。
4. **類比誠實**：每個歷史類比是否附不同之處，且不同之處是否真的削弱類比（若削弱卻仍當主要類比→🟡）。
5. **紀律與白話**：禁語、術語首現括號、全形標點、無流程劇場；讀者看不懂的內部用語、比喻、同一結論換句話重講（機械檢查抓不到的部分）列 🟡。
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
- v1.6 2026-10-15：新增必寫段落 `sector`（那斯達克與半導體，`check_market_read.py` 第 18 項；as_of 2026-10-16 起缺段 FAIL）；證據包新增 `book:*`（實盤四條腿現持曝險、距週線閘門）與 `theme:*`（主題擁擠度前 8 名）。仍是文字評論，不寫機率。
- v1.5 2026-10-13：市況判讀 SPRT 判紅（rule_ledger #137），降為文字評論：`mode: commentary`，不寫機率、不落帳；`check_market_read.py` 第 4、5、6、9 項改為「必須沒有」；`ledger_from_editorial.py --source market-read` 直接略過；頁面拿掉機率呈現。
- v1.4 2026-09-24：新增「可讀性硬規則」（標題句 ≤ 40 字＋1 個數字、每句 ≤ 60 字＋3 個數字、內部用語與比喻詞禁用、出處放句尾、data_gaps_zh ≤ 150 字），`check_market_read.py` 第 13–17 項 FAIL 擋下；術語白話註解（第 11 項）由 WARN 升為 FAIL；vs_prior 首句上限 60→40 字。
- v1.3 2026-09-17：`vs_prior_zh` 第一句必須是白話結論（頁面「本期重點」直接引用）；改判條件在首屏改為各取一條轉多與轉空門檻附現值。
- v1.2 2026-09-08：白話關卡適用範圍明文擴大到 `docs/market/index.html` 手寫文案與 `build_market_state.py` 機械模板句（原本只管 `read.json`）；本輪清查對照表落 `_plainlang_styleguide.md` §2.11。
- v1.1 2026-09-03：新增 Auto 模式（雲端 routine `market-read-auto`，見 §5）——`check_read_triggers.py` 判定觸發、冷讀 subagent 模型配對與職責書、失敗寫 `read_status.json`、email 摘要交 `market-read-notify.yml`。手動模式（步驟 1–6）不變。
- v1.0 2026-09-03：首版；首份判讀 2026-09-02（先弱後強；3m 0.52／6m 0.55／12m 0.60；7 張命題）。
