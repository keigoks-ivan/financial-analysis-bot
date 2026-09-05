# industry-analyst v4.0 裁決級 refresh — orchestrator playbook（HBM 2026-09-04 實跑固化）

**權威順序**：`.claude/skills/industry-analyst/SKILL.md`（現行 v4.0，含 2026-09-04 eee867b2e 的兩條流程紀律）與其 templates／references 是規則權威，本 playbook 只是把流程固化成可重複的派工順序；兩者衝突時 SKILL.md 為準，**除了**持有人本輪明講的三件事：可見字目標 12,000–13,000、修補全交乾淨 sonnet patch agent、雙閘要一撮合價一外部驗證器。開工第一步就 Read SKILL.md 全文。

Repo：/Users/ivanchang/financial-analysis-bot（git main）。Scratchpad（SP）：/private/tmp/claude-501/-Users-ivanchang-financial-analysis-bot/f38855d4-c146-4be7-94a9-ecad6efed8f3/scratchpad
py3.9 跑不動的 script 用 `/tmp/ddvenv/bin/python`（有 yfinance）。

## 分工鐵律
- Orchestrator（你，opus）：只派工、量測、做一行級機械修正；**不寫稿、不當 critic**。
- writer＝opus 子 agent（Phase 1 sketch → Phase 2 寫稿 → 若 critic 有 🔴 只出「判斷備忘」不改檔，≤6 輪）。
- 採集／completeness／id-review critic／re-gate／patch／發布＝sonnet 子 agent。修補一律乾淨 sonnet patch agent，不續用 writer。
- 前版只讀 prior_brief（id-meta＋kill 表＋非共識標題），禁讀前版 HTML 全文（防錨定）。
- 站上 DD 只 grep dd-meta；不餵 dd-screener 即時本益比當證據。
- **並行模式（2026-09-05 起）**：多個 orchestrator 同時跑各自主題。步驟 0–7 完全獨立（只寫自己 Tag 的 scratchpad 檔與自己的 `docs/id/ID_{Theme}_{TODAY}.html`／`notes/site-internal/id/_*_{Tag}_{TODAY}.md`；`git status` 看到別的主題的未提交 ID 檔一律不碰不 add）。**步驟 8 發布＋commit 必須持有發布鎖**（見 §8a），鎖內先 `git pull --rebase` 再重生 cat 頁／mapping／banner，commit＋push 後立刻釋放。

## 每份 ID 的步驟

### 0. 前置（bash，零 token）
```
python3 $SP/prior_brief.py docs/id/ID_{Theme}_{OLDDATE}.html $SP/prior_brief_{Tag}.md
/tmp/ddvenv/bin/python $SP/returns.py $SP/returns_{Tag}.md T1 T2 ...   # related_tickers（前版＋你判斷該加的）＋QQQ
ls docs/dd/ | grep -E "^DD_(T1|T2|...)_2026"   # 列出可 grep dd-meta 的 DD 檔
```
mega／sub_group 從 `docs/id/taxonomy.md`；T1 floor 依 `references/sources.md` 分型（macro／cloud／space 45，其餘含 semi 60；可 `--t1-floor 45` 覆蓋但要在 check 報告尾與 summary 折疊各寫一句理由；45 以下不灌來源、停下）。
輸出檔名 `docs/id/ID_{Theme}_{TODAY}.html`（Theme 沿用前版 slug）。

### 1. writer Phase 1（Agent，model=opus）
提示要點：身分＝industry-analyst v4.0 writer；Read SKILL.md 全文＋templates/report_template.md 全文＋references/sources.md；Read prior_brief 與 returns；只准 grep 指定 DD 的 dd-meta 決策欄（一條複合 python 抽 dca_verdict／dca_role／moat_trend／ev5y_pct／irr_base_pct，存 $SP/dd_meta_{Tag}.md）；輸出 `$SP/writer_phase1_{Tag}.md`：(a) thesis sketch＋與前版非共識的承接／翻面／新增＋暫定五格燈號猜想 (b) id-meta 草稿欄位 (c) **封閉式問題清單給採集 agent**（Axis A–E 每題一行，寫明數字／官方源／as-of；Axis E 五條不得跳過；換相雙閘要準備「一個市場撮合價＋一個外部驗證器」的數據；承重數字直讀 10-Q／8-K／法說稿／官方新聞稿；附錄用歷史錨點）(d) Phase 2 判斷性搜尋清單 (e) T1 floor 聲明。回報 ≤200 字後停下等 SendMessage。

### 2. 採集（Agent，model=sonnet）
讀 references/research-queries.md＋sources.md＋writer 問題清單 (c)。每題 `{題號}｜{數字}｜{URL}｜{as-of}｜{T1/T2/T3-A/B/C/T4}`；承重數字直讀官方源，彙整站只當 T2／T3；查不到就寫「查不到」，禁推估；市場撮合價序列盡量給 TrendForce／原始機構新聞稿逐期數字；末尾附 T1 自估比例＋仍缺官方源的承重數字清單。輸出 `$SP/evidence_{Tag}.md`。不改 repo。

### 3. writer Phase 2（SendMessage 給同一 writer）
給 evidence 路徑＋採集端缺口清單。要求：先做判斷性搜尋＋直讀官方源覆核缺口，T1 拉到 ≥60（不行則 45 覆蓋＋兩處理由；<45 停下回報）；**可見字目標 12,000–13,000，硬上界 14,000（HBM 教訓：writer 交 13,881，修補後撐到 15,462；請寫在 12,500 附近留餘裕）**；表 ≤12；CSS `../assets/id-v4.css`；輸出檔名；id-meta 依 references/id-meta-schema.md，sister_ids 指向各主題最新版（HBM→ID_HBM_Supercycle_20260904、算力 capex→ID_AIComputeCapexCycle_20260903、Agentic→ID_AgenticAIPlatform_20260903）；summary 加前版連結；**D8 priced-in 與 3.4 時鐘雙閘為重心：換相充分條件＝兩個獨立訊號，一個市場撮合價、一個外部驗證器（同源撮合價換品類不算兩個；預估值不算實績）**；kill 表 ≥1 撮合價＋≥1 外部驗證器，每條現值＋as-of＋門檻＋window；站內 DD 裁決與其後報酬的矛盾要正面處理；寫 3.4／valuation／risks 前 Read judgment-playbook 觸發索引；白話、全形標點、禁流程劇場；寫完跑 validate_id_meta.py＋`check_id.py FILE [--t1-floor 45] --report notes/site-internal/id/_check_{Tag}_{TODAY}.md --excerpt $SP/_excerpt_{Tag}.md`，只修機械 FAIL、驗證 ≤3 輪、不 Read 整份 HTML；回報 ≤300 字含「自知未解的三個弱點」。

### 4. completeness（sonnet）與 id-review critic（sonnet）——**並行 spawn**
- completeness：只知主題、先獨立列一階變數清單、再讀草稿（可用 check_id --excerpt）、輸出 `notes/site-internal/id/_completeness_{Tag}_{TODAY}.md`（格式比照 _completeness_HBMSupercycle_20260904.md），分必補／宜補／可忽略。
- critic：「You are operating as the id-review sub-agent. Read spec at /Users/ivanchang/.claude/skills/id-review/SKILL.md（【ID v4 Mode】J1–J10）」；先跑 `check_id.py FILE [--t1-floor 45] --excerpt /tmp/_excerpt_{Tag}_critic.md --report /tmp/_check_{Tag}_critic.md` 只讀這兩檔，禁 Read 整份 HTML；額外重點：雙閘獨立性、kill 表結構、抽 5 個承重數字上網獨立查證、writer 自報的三個弱點判定；輸出 `notes/site-internal/id/_critic_{Tag}_{TODAY}.md`（比照 _critic_HBMSupercycle_20260904.md），每條 🔴🟡🟢＋定位（錨點＋行號）＋可直接執行的修法。不改草稿。

### 5. 有 🔴 → writer 判斷備忘（SendMessage 給 writer，≤6 輪，不改檔）
對每個 🔴 判定：(a) 有證據支撐原判→指名證據；(b) 沒有→改判，並列出每處「檔案定位（grep 關鍵字）｜原句｜新句」含 id-meta／燈號／summary 判斷卡／thesis／3.4／kill window／stocks 行動框的連動。🟡 與 completeness 必補也給可貼文字。輸出 `$SP/writer_fix_memo_{Tag}.md`。無 🔴 時跳過此步，patch 直接照 critic 🟡＋completeness 必補做。

### 6. patch（sonnet，乾淨）
權威順序：備忘 > critic 報告 > completeness（只做必補）。禁 Read 整份 HTML（grep -n／sed -n／Edit）。**新增內容要在同段落砍等量冗句，讓可見字不淨增（HBM 教訓）**。若 summary 無折疊而 T1 用 45 覆蓋，加一個沿用檔內 `<details>` 樣式的折疊寫一句理由。check_id 重複掃描列出的 5 次以上同句改寫 2–3 處。修完跑 validate_id_meta → check_id（--report 會覆寫，先存檔尾「T1 floor 覆蓋說明」節再 append 回去）→ qc.py；grep 自驗。不 commit。回報套用處數／驗證結果／KB／可見字／跳過項。

### 7. re-gate（sonnet，僅當第 4 步有 🔴）
同 critic 身分，驗每個 🔴🟡 是否真解（機器欄↔內文同步是重點）＋修補是否引入新矛盾；在 critic 報告檔尾 append「## Re-gate」。殘留只剩一行級 → orchestrator 自己用 python replace 修並在 critic 報告 append 處置紀錄；否則再一輪 patch。

### 8a. 發布鎖（並行必守）
發布 agent 開工第一條指令（用 Bash `run_in_background: true`，等它結束的通知再往下）：
```
LOCK=$SP/publish.lock
until mkdir "$LOCK" 2>/dev/null; do
  if [ -f "$LOCK/ts" ] && [ $(( $(date +%s) - $(cat "$LOCK/ts") )) -gt 2400 ]; then rm -rf "$LOCK"; continue; fi   # 逾 40 分鐘視為死鎖
  sleep 30
done
date +%s > "$LOCK/ts"; echo "{Tag}" > "$LOCK/owner"; echo LOCK_ACQUIRED
```
取得鎖後：`git pull --rebase`（若 rebase 因工作樹髒而拒絕，先 `git stash push -- <只含自己檔案的清單>` 再 pull 再 `git stash pop`；別的主題的檔不動）→ 做 §8 全部步驟（cat 頁／mapping／banner 都在合併後的樹上重生）→ `git add <明列> && git commit -F msg.txt && git push`（同一條指令）→ `git log -1 --stat` 確認 → **`rm -rf $SP/publish.lock`**（無論成功失敗都要釋放；失敗也要在回報說明鎖已釋放）。

### 8. 發布（sonnet）
依 SKILL.md【發布流程】4–10：INDEX.md append 一列（比照 L127–129 的 v4 列；備注含流程、燈號前版→本版、KEY CALL、kill 表 N 條標撮合價／外部驗證器、critic 計數、可見字／KB／表／T1、**「涵蓋 T1 / T2 …」全部 related_tickers**）；index.html 對應卡片**原地改**（href、移除該檔 STALE_PILL 標記段、v2-badge→「v4 敘事版」、tc-phase、tc-thesis-short＝oneliner＋燈號句、tc-children＝前版／完整考證版 chip、tc-tags、tc-meta 三個 chip、data-search；母題卡若有指向本檔的子題 chip 同步改）；`/tmp/ddvenv/bin/python scripts/build_id_category_pages.py`（零 churn，應只動一張 cat 頁）；`python3 scripts/id_dd_mapping.py`＋`/tmp/ddvenv/bin/python scripts/retrofit_dd_id_banner.py`（mapping 已全站刷新過，這次只保留 diff 含新檔名的 DD，其餘 `git checkout --`）；`check_tier_matrix.py --inject-html`（既有錨點缺失會跳過，屬 pre-existing）；`inject_report_primer.py --family id`；`qc.py`。
**然後 commit＋push（持有人已授權）**：`git status` 排除其他 session 的檔（docs/learn/**、notes/site-internal/learn/**、scripts/learn/**、.claude/skills/stock-analyst/** 等），只 `git add` 明列：新 ID、INDEX.md、index.html、cat-*.html（有動的）、portfolio/id_dd_map.json、保留的 DD 檔、notes/site-internal/id/ 的 _check／_completeness／_critic 三份、tier matrix／primer 若有改。commit 訊息中文，比照 `git log --oneline -5 -- docs/id/` 既有格式（含燈號變化與 critic 計數），結尾：
```
Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019m4dsyeMzEwnWcsRdrAA3d
```
`git pull --rebase` 後 push；hook 失敗回報原因不繞。

### 8b. 併行 session 防搶（AdvancedPackaging 教訓）
發布 agent 的 `git add` 與 `git commit` 必須在**同一條 Bash 指令**內連續執行（`git add A B C && git commit -F msg.txt`），commit 後立刻 `git log -1 --stat` 確認檔案掛在自己的 commit 下；若被別的 session 掃走，記在回報即可、不拆 commit。

### 8c. 其他教訓
- Phase 1 要核對前版 related_tickers 的 ticker↔公司對應（前版把 6146.T 標成 Ibiden，實為 DISCO；Ibiden＝4062.T），錯的在 sketch 階段就更正。
- `/tmp/ddvenv` 可能失效；先試 `python3.12`，再試系統 `python3`。
- patch agent 範圍要小：critic 🔴0 時只做 🟡＋completeness 必補，目標 ≤40 輪；不要為 🟢 cosmetic 動檔。

### 9. 量測（bash）
`python3 $SP/tok.py <每個 sub-agent 的 .output 路徑> <你自己的 transcript 若能取得>`：.output 路徑在 Agent 回傳的 output_file（`/private/tmp/claude-501/-Users-ivanchang-financial-analysis-bot/<session>/tasks/<agentId>.output`）。已知 jsonl 對 >100KB 的 Write 沒落最後 usage，writer output 面值要用「CJK×1.3＋ASCII/3.5」估算補回（HBM：面值 30K、實際約 62K）。回報：總 token、writer／採集／completeness／critic＋re-gate／patch／發布拆分、可見字、KB、check_id 各項、critic 🔴🟡🟢、五格燈號（前版→本版）。

## 三份的對照基線（供最終回報）
| 份 | 可見字／KB | T1 | critic 首輪 | 燈號 | 子 agent token（面值） |
|---|---|---|---|---|---|
| Agentic 20260903 | 13,999／75.7 | 45.8% | 🔴0 🟡2 🟢1 | split·II·mid·mid·×4.0 | writer 20.1M（83 輪） |
| 算力 capex 20260903 | 13,879／77.7 | 45.2% | 🔴0 🟡2 🟢3 | shortage·II·mid·high·×2.5 | writer 19.9M＋patch 6.3M |
| HBM 20260904 | 15,462／80.9 | 65.2% | 🔴2 🟡1 🟢1→re-gate 0 | shortage·II 末段·mid·high·×2.1 | writer 6.0M（32 輪）＋採集 1.7＋完整性 0.7＋critic 3.8＋re-gate 1.5＋patch 11.3（93 輪）＋發布 4.2 |
