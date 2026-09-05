# DD 生產流程重設計（v17 草案，2026-09-05）：報告不動、流程全換、用量最少

> 狀態：**草案，待持有人裁定**。前身：`_v16_design_spec_20260903.md`（§13／§16）、`_handoff_dd_skill_redesign_20260905.md`、`_audit_BE_20260905.md`。本稿寫的是 v16.2 之後的整條生產鏈，**不動現行任何檔**；落地前先過 §9 的回溯考卷。
> 持有人拍板（不可推翻，本稿全程遵守）：任何 DD 觸發語預設走最新版管線；判斷機器語意（QC 門檻、決策矩陣 rows 1–10、dd-meta v15.0、篇幅帶 75–105KB、三詞裁決）零變動；writer／判斷與 critic／抽查永不同模型；規則加刪走 `knowledge/rule_ledger.md`。
> 本稿新增的持有人目標（2026-09-05）：**報告架構與內容保留，流程整條重設計，品質維持或更好，月租方案下用量最少；內容可同步微調**。

---

> **2026-09-05 持有人拍板**：三題皆採本稿建議（①A ②A ③A）；§8 的 C-1／C-2 啟用；WP0 已於同日執行（四份 `_src/` 補 `parts/`）。持有人同時指出實跑用量遠大於設計帳，已補 §1.1 全帳、§4.1 熔斷、§9.1 WP 執行紀律。

> **2026-09-05 持有人第二次拍板：「把力氣花在判斷而不是寫報告」。** 預設產物改為 **快速版**（judgment.json 的一頁渲染，零 LLM）；完整散文報告降為選配 `--full`。用量與工程優先序全部向判斷層傾斜：Stage 0 證據深度不砍、判斷 agent 與跨模型閘不砍、散文可不跑。快速版位置採工作假設 `docs/dd/brief/BRIEF_{T}_{D}.html`（帶同欄位 dd-meta，研究頁標「速判」），持有人未明示反對即照此做（§8 C-5）。

## 0. 三個待裁定題，本稿採用的工作假設（已拍板，留作理由紀錄）

| 題 | 本稿採用 | 替代案 | 翻案影響 |
|---|---|---|---|
| ① 退場訊號②兩度命中後的處置 | **A：負向證據可追溯 validator（擋 FAIL）＋跨模型判斷層閘搬到上站前（只對判斷級 🔴 擋）**，ledger 第 21 列改寫成新的可證偽條件 | B：只補 validator，抽查維持事後計數；C：恢復 v15 式讀全文 critic | B → 刪 §3.4、§6 的閘與修補段；C → 成本模型全改 |
| ② v15.2 去留 | **A：從路由退役，SKILL.md／html-output.md／data-collection.md 歸檔＋git tag `dd-v15.2-final`**；v17 仍載入的 reference 原地保留 | B：留 `--v15` 旗標並存到 2026-10 | B → §7 檔案收斂只做一半，技術債 1 不解 |
| ③ 入口與 skill 合併 | **A：`scripts/ddreport.py` 承接全部零 LLM 區段；`stock-analyst`＋`ddreport` 合併成一個 skill（`ddreport`），stock-analyst 降為 redirect stub** | B：兩個 skill 分立，stock-analyst 只剩路由表 | B → §7.2 改成兩檔，其餘不變 |

理由摘要（詳見 2026-09-05 對話評估）：①BE 的 🔴 是「證據在、沒接線」，validator 可攔；SNOW dry-run 的 🔴 是「接了線、季數算法分歧」，validator 攔不到，兩次命中兩種類型，只有跨模型的眼睛能覆蓋第二類，而抽查本來就在跑，搬到上站前不多花 token。②兩套規則本體並存就是「路由靠散文」的根源；回退手段是 git tag，不是活旗標。③Python 不能 spawn sub-agent，skill 必然存在；兩個 skill 的差異「要不要 commit」已因拍板消失。

---

## 1. 用量的物理模型（本稿所有設計決定的依據）

`dd_token_report.py` 去重尺量的是 cache_read。**每個 agent 每一輪 tool call 的 cache_read ≈ 當時的 context 大小**。因此：

- 判斷 agent context 約 85K token（evidence 116KB＋最新一季逐字稿 46KB＋digest 16KB＋規則 41KB＋schema）。CRDO 20 分 30 輪 → 2.4M；BE 因 verify_dd_math 在 HTML 階段才攔到恆等式、外加三個瑣碎 schema FAIL，輪次翻倍 → 4.8M。**同樣的輸入，差的是輪次，不是 context。**
- 散文 agent：CRDO 54 次呼叫（18 次段落 Write＋19 次驗證修補＋13 次讀規則）→ 6.8M；BE 收斂後 2.4M。**18 段各一次 Write 就是 18 輪，每輪付一次 40K context。**
- Stage 0 fan-out：4 批各 14 軸 × ≤3 輪搜尋，每個子 agent 的 context 隨搜尋結果累積到 50–60K，總 cache_read ≈ Σ(輪次 × 當時 context)。**批越小、agent 越多，總 cache_read 越低**（同樣輪次，但每輪 context 只有一半）。
- Orchestrator（opus）：本輪逐條敲 Bash、先讀 25KB 派工模板才知道怎麼跑，每敲一次付一次自己的 context。

### 1.1 實跑全帳 vs 設計帳（2026-09-05 補量，持有人指出「實跑遠大於設計」）

v16.2 的用量報表只加總子 agent，**沒算 orchestrator 主線程與事後抽查**。用 `dd_token_report.dedup_sum` 對 session 主 jsonl 與全部子 agent 重算（去重尺 cache_read）：

| 項目 | BE（session 693486c0） | CIEN（session 0d3b08c3） | v16.2 報表原本算的 |
|---|---|---|---|
| orchestrator 主線程（opus） | **11.0M／61 輪** | **11.7M／69 輪** | 未計 |
| Stage 0＋0e（sonnet，7 個子 agent） | 5.5M | 10.1M | 有 |
| 判斷（Fable） | 4.8M／23 輪 | 2.6M／15 輪 | 有 |
| 散文（sonnet） | 2.4M／18 輪 | **13.5M／69 輪** | 有 |
| 誤啟 v15.2 writer 後 kill | 0.3M | — | 未計 |
| 事後抽查（opus） | **12.6M／67 輪** | 4.1M／29 輪 | 未計 |
| **全帳** | **36.6M** | **42.0M** | 13.0M／16.9M |

三個結論：
- **orchestrator 是第二大甚至最大單項**。它的每一輪都付整個 context（系統提示＋41KB CLAUDE.md＋記憶＋對話），本輪 61–69 輪的來源是手敲 Stage 0 Bash、讀 25KB 派工模板與四份 draft、讀 validator 全文。壓它的唯一方法是輪次：§3 的 `ddreport.py` 把 orchestrator 壓到 ≤20 輪。
- **同一段的用量離散度極大**（散文 2.4M vs 13.5M、抽查 4.1M vs 12.6M），差別全在輪次。沒有熔斷的預算等於沒有預算（§4.1）。
- **開發 WP 本身是最大的用量黑洞**：同期的 v15.2／v16 建置子 agent，單一「SKILL.md 瘦身」agent 287 輪 117M、「規則拆分」207 輪 93M、「AVGO patch」243 輪 89M。§9.1 對 WP 執行另立紀律。

**由此推出四條設計原則**：
1. **一次讀、一次寫、一次驗**：每個 LLM agent 的輸入由腳本預先打包成單一 bundle 檔，輸出一次（或兩次）Write，驗證一次複合腳本。目標輪次：判斷 ≤8、散文 ≤7、覆蓋子 agent ≤12。
2. **能算的恆等式全在該層驗**：判斷層算得出的東西不准留到 HTML 階段才攔（BE 教訓），part 檔在子 agent 交稿時就驗（as_of／source 缺漏不留到 merge 後）。
3. **Orchestrator 零內容**：只呼叫 `ddreport.py` 子命令與 spawn；spawn prompt 是一句「讀 `{run}/prompts/{stage}.md` 照做」，模板不進 orchestrator context；validator 輸出只回一行狀態＋路徑。
4. **省在輪次，不省在證據**：不對 evidence 去重瘦身（BE 🔴 正是漏一條負向 finding），只做無損壓縮（bundle 內 findings 以緊湊表格呈現，不縮排 JSON）。

---

## 2. 保留與改動的邊界

**零變動（讀者面與判斷機器）**：`docs/dd/DD_{T}_{D}.html` 的章序 §1–§14＋附錄 A／B、canonical section id、E1–E12 表格、dd-meta `schema:"v15.0"` 全欄語意、篇幅帶 75–105KB 與分章 byte 預算、決策矩陣 rows 1–10 與 `dd_decision.py` 翻譯、QC 門檻、三詞裁決、INDEX.md 列格式、下游聚合器讀 dd-meta 的方式。

**改動（生產流程與內部契約）**：誰在什麼 context 做什麼、交接檔格式（judgment.json 加追溯欄）、驗證分工、目錄慣例、入口、skill 檔案數、規則檔去重、commit 內容集。

**內容微調（持有人授權，選配，§8）**：機械段由腳本生成、負向證據處置表進附錄。

---

## 3. 新流程（v17 五段制）

```
ddreport.py plan {T} [--date D]            ← 零 LLM：建 run 目錄、前份三區塊、archetype hint、
                                              軸清單分批、逐字稿清單、寫好每個子 agent 的 prompt 檔
Stage 0  證據包（sonnet fan-out；批次由 plan 決定，預設每批 2 軸）
  (a)  覆蓋軸子 agent × N   → {run}/parts/axes_{k}.json   ← 交稿前自跑 ddreport.py part check
  (a1) 數字包補值子 agent    → {run}/parts/numbers_collect.json
  (a2) 逐字稿摘要子 agent    → {run}/digest.json（validate_digest 逐字驗）
  (k)  Koyfin 增量下載子任務 → 逐字稿路徑清單
ddreport.py stage0 finalize                ← 零 LLM：逐 part 驗證後 merge、給 finding 編 id、
                                              validate_evidence --strict、印「哪一批要重派」
ddreport.py judge prepare                  ← 零 LLM：打包 judgment bundle（evidence 緊湊版＋最新一季
                                              逐字稿＋digest＋judgment-rules＋條件載入 reference＋
                                              schema 速查）成單一檔；寫 prompt
Stage 1  判斷 agent（Fable，一次讀 bundle、兩次 Write、一次複合驗證）
ddreport.py judge check                    ← dd_scenario → dd_decision → validate_judgment（含全部
                                              恆等式＋負向證據可追溯）→ 機械正規化；FAIL 回判斷 agent
ddreport.py gate prepare                   ← 打包 gate bundle（evidence＋judgment＋digest＋最新一季
                                              逐字稿）；寫 prompt
Stage 1G 跨模型判斷層閘（opus；讀 bundle，輸出 FINDINGS 表對準 JSON 路徑；只計判斷級）
ddreport.py gate check {audit.md}          ← 解析：判斷級 🔴＝0 → 放行；>0 → 寫 patch prompt
                                              （只含 findings＋受影響子樹），重 spawn 判斷 agent patch 模式
                                              （≤1 輪），再跑 judge check；第二次仍 🔴 → 停下給持有人
ddreport.py brief                          ← 零 LLM：gen_dd_tables → 一頁模板渲染 judgment.json 成
                                              docs/dd/brief/BRIEF_{T}_{D}.html（dd-meta 同欄位）；
                                              **預設到此為止**（2026-09-05 第二次拍板），接 finish
—— 以下僅 `--full` 時執行 ——
ddreport.py prose prepare                  ← gen_dd_tables → dd_prose_budget → 數字白名單 → 機械段
                                              生成（§8 選配）→ 打包 prose bundle；寫 prompt
Stage 2  散文 agent（sonnet，一次讀 bundle、兩次 Write〔s1–s7／s8–附錄〕、一次 ddreport.py gates）
ddreport.py prose split                    ← 把兩個合併檔切成 prose/{sid}.html
ddreport.py gates                          ← render_dd --assemble＋六支閘（即 dd_gates.sh 內容）；
                                              FAIL 只回該段 sid 清單，散文 agent 只重寫那幾段（≤1 輪）
ddreport.py finish                         ← INDEX 列由 dd-meta 生成、update_dd_index、算 DD commit
                                              檔案集、存 _src/、token 報表、commit＋push
```

### 3.1 `plan`（零 LLM，取代本輪 orchestrator 手敲的十幾條 Bash）
- 建 `.dd_build/runs/{T}_{D}/`，寫 `manifest.json`（狀態機：planned → stage0 → judged → gated → rendered → finished；每步記 validator exit code 與時間）。
- 跑 `dd_prior.py`、`dd_evidence.py init/axes`、`dd_numbers_extra.py`（含 `--peers` 規則：有前份沿用，無前份由 orchestrator 給一次）。
- 依 archetype 展開軸清單，**預設每批 2 軸**（§1 原則：小批省 cache_read；批數由 `--axes-per-batch` 可調，試點期回填最佳值）。`major_events` 軸單獨一批並負責頂層 `events` 五組。
- 把每個子 agent 的完整 prompt 寫進 `{run}/prompts/a_{k}.md`、`a1.md`、`a2.md`、`k.md`，內容＝現行 `agent-prompts.md` 對應模板＋該批軸的 query 模板＋**JSON 回傳契約**（取代 v15 的 Markdown ≤6KB 模板，技術債 6）。
- 印出 spawn 清單：`{agent 名, model, prompt 路徑}`，orchestrator 逐項 spawn，prompt 只寫一句「讀 `{路徑}`，照做，交稿前跑 `python3 scripts/ddreport.py part check {你的輸出路徑}` 過了才回報」。

### 3.2 `part check`／`stage0 finalize`
- `part check FILE`：對單一 part 檔跑 validate_evidence 的**同一套**軸規則（findings 必有 `claim/source/as_of/direction/affects`，as_of 可解析、none 軸 queries_run ≥2、KPI items 必有 as_of/source）。同一份程式碼、兩個入口，不另寫 `validate_part.py`。
- `finalize`：逐 part 再驗一次（不信任子 agent 自報）→ merge → **給每條 finding 編 id**（`{axis}#{n}`，機械、穩定）→ `validate_evidence --strict` → 印 PASS 或「重派 a_3、a2」。重派 ≤2 次，超過就停下回報。

### 3.3 `judge prepare`／判斷 agent／`judge check`
- **bundle**：單一 Markdown 檔，依序含：①任務頭（T／D／archetype／前份裁決一行）；②schema 速查（必填欄、enum、字數上限、路徑格式、洩漏詞表，**把本輪三個瑣碎 FAIL 寫成事前約束**）；③evidence 緊湊版（numbers 原樣、findings 逐軸列表 `id｜direction｜as_of｜claim｜source｜affects`）；④最新一季逐字稿全文；⑤digest；⑥judgment-rules.md；⑦條件載入 reference（archetype 決定，由 plan 選）。約 85–95K token。
- 判斷 agent 只做：Read bundle（1 輪）→ Write judgment.json（1 輪）→ Write scenario.json（1 輪）→ `ddreport.py judge check`（1 輪）→ FAIL 時改欄位重跑（≤2 輪）→ 回報（1 輪）。**取消交稿前自查①-⑦**（BE 實證自查給供需 durability 🟢、跨模型抽查給 🔴，自查與自己的盲點同源；其機械可驗部分已進 validator，判斷部分交 Stage 1G）。
- **judgment.json 新增追溯欄**（schema v16→v17，dd-meta 不動）：`contradictions[]`／`moat.threats[]`／`premortem.blind_spots[]`／`triggers[]`／`thesis.R[]` 每項可帶 `evidence_refs: ["axis#n", …]`；頂層新增 `evidence_dismissed: [{ref, reason}]`。
- **`judge check` 內容**（全部零 LLM）：dd_scenario → dd_decision run → validate_judgment，後者新增：
  - **(J1) 負向證據可追溯**：每條 `direction="-"` 的 finding，須出現在任一 `evidence_refs` 或 `evidence_dismissed`，否則 FAIL 並列出未處置清單（BE 的 Crossroads 1,500 噸即在此攔下）。
  - **(J2) 判斷層恆等式全集**：把 `verify_dd_math.py` 檢查 A–E 中凡是能從 judgment＋scenario 算的（Max DD 下限 ≥ Bear 終點跌幅、EV／IRR／AR 對 scenario_meta、情境樹年期、Bull EPS 退化）搬進來，HTML 階段的 verify_dd_math 只剩「judgment ↔ 產出 dd-meta 一致」。
  - **(J3) 機械正規化**：scenario_ref 相對路徑轉絕對、半形標點轉全形（沿用 qc 規則）、`scenario_meta.valuation_dependent` 與 `decision_inputs` 同名欄互檢（BE 🟡⑥）。可自動修的直接改檔並印出，不回判斷 agent。

### 3.4 Stage 1G 跨模型判斷層閘（取代事後抽查，成本相同、位置前移）
- 模型：與判斷 agent 不同（Fable → opus；旗標改 opus 判斷時 → sonnet）。
- 輸入 bundle：evidence 緊湊版＋judgment＋digest＋**最新一季逐字稿全文**（SNOW 教訓：冷讀者缺逐字稿會誤判親讀得到的正確判斷為無據）。禁外部檢索。
- checklist：現行 `_audit_*.md` 的①–⑦（判斷級）逐條，⑧散文不在此閘。輸出固定格式：`## GATE: 判斷級🔴 = N`＋FINDINGS 表（燈／JSON 路徑／一句依據／建議改法）。
- `gate check`：只解析標頭與表；🔴＝0 放行，🟡 只存檔進 `_src/`；🔴>0 → 寫 `{run}/prompts/b1_patch.md`（findings＋`jq` 抽出的受影響子樹＋「只准改這些欄位、可不採納但須寫進 evidence_dismissed」）→ 重 spawn 判斷 agent（Fable，patch 模式，context 只有 judgment.json＋子樹＋findings，約 30K token）→ `judge check`。**不 re-gate**（一輪修補後直接進散文；第二眼的價值在首輪，re-gate 是 v15 的錢坑），除非修補後 `dd_decision` 的 verdict 翻面，翻面才重跑 Stage 1G 一次。
- 修補後判斷 agent 若堅持不採納：`evidence_dismissed` 寫理由即可過 J1；分歧原文存 `_src/{T}_{D}/gate_dissent.md`，供 2026-10 校準輪對質。

### 3.5 `prose prepare`／散文 agent／`prose split`／`gates`
- bundle：judgment.json（含 reasoning）＋render-rules.md＋表格產物清單（含注入標記）＋各段目標 bytes 表＋數字白名單＋§8 機械段（若啟用）已生成的 sid 清單（散文 agent 不寫這些段）。
- 散文 agent：Read bundle → Write `prose_A.html`（s1–s7，段間用 `<!-- SID:sX -->` 標記）→ Write `prose_B.html`（s8–s14、decision、appA、revlog）→ `ddreport.py prose split && ddreport.py gates`（一次）→ FAIL 只重寫回報的 sid（把那幾段合成一個檔再 Write，再 split＋gates，≤1 輪）→ 回報。**取消交稿前自查⑧**（validate_prose 的數字集合檢查已是它的機械版；白話開場交 QC-54 的 leaks 詞表）。
- `gates`：即現行 `dd_gates.sh` 的內容併入 Python（單一 python 路徑，解決 `/tmp/ddvenv` 與系統 python3 混用：`ddreport.py` 啟動時自檢 import，缺件印一行重建指令）。FAIL 輸出改為「sid 清單＋原因」而非六支腳本全文，散文 agent 不需 grep 原始碼。

### 3.6 `finish`
- **INDEX 列由 dd-meta 生成**（`ddreport.py index-row {HTML}`）：八欄取值表照 ddreport v3 draft 步驟 5，「備註」欄由 judgment `oneliner`＋三個決策數字機械組句；INDEX.md 保留（update_dd_index 仍以它當舊報告 fallback 與 universe）。
- `update_dd_index.py` 照跑，但 finish 只 stage **DD commit 檔案集**：`docs/dd/DD_*`、`docs/dd/INDEX.md`、`docs/research/_body.html`、`docs/dd-screener/latest.json`、`docs/picks/candidates.json`、`_src/{T}_{D}/`。`data/weekly_cache/*`、rss、search-index、track-record、site_nav self-heal **不進 DD commit**（由既有排程 workflow 自己 commit；finish 印出這些被略過的檔數供核對）。這需要 `update_dd_index.py` 加一個 `--print-dd-commit-set` 或 finish 端以白名單 stage，前者較穩（清單權威在 update_dd_index）。
- 存 `_src/{T}_{D}/`：judgment／scenario／scenario_meta／evidence／digest／prose／**parts/**（新增，讓 Stage 0 可重放）／gate audit／gate_dissent／token.json／manifest.json。
- `dd_token_report.py --run {run}` 從 manifest 記的 agent id 直接算三欄，寫 `token.json`，回報格式沿用 SKILL.v16.draft §五。
- commit 訊息固定樣式，附 `[v17]` 與 token 三欄。push 前 `git pull --rebase` 與並行 session 四步自檢照舊。

### 3.8 無頭模式（2026-09-05 持有人拍板「釜底抽薪」；WP1 直接做此版）
指揮者不用 LLM。`ddreport.py run {T}` 是一支 Python 程式，四個需要腦的時刻（覆蓋軸子 agent、0e 摘要、判斷、閘、散文）由程式以 `claude -p` 無頭呼叫，prompt 從檔案餵入，產物寫回 run 目錄。已驗證（2026-09-05，Claude Code 2.1.258）：
- 登入為 claude.ai 訂閱（`authMethod: claude.ai`，無 `ANTHROPIC_API_KEY`），無頭呼叫走同一額度。
- `-p --allowedTools WebSearch --max-turns N --output-format json` 可上網：3 輪 11.7 秒查得 BE Q2 營收。
- 回傳 JSON 含 `num_turns`、`usage.cache_read_input_tokens`、`modelUsage{model: {cacheReadInputTokens, outputTokens, webSearchRequests}}`：**計量直接從回傳拿**，`dd_token_report.py` 退為歷史工具。
- 基準 context 約 78K／輪（系統提示＋家規＋工具），是每輪固定成本；`--max-turns` 就是熔斷的硬上限，程式另以目標 2× 判 `over_budget`。
- 待 WP1c 實測：`--setting-sources user` 能否略過 41KB 專案 CLAUDE.md 以壓基準 context；並行 spawn（subprocess 同時起 N 個 `claude -p`）是否受額度節流。

互動 session 只剩：`python3 scripts/ddreport.py run BE` → 看一行結果。§3.7 的 skill 縮為 2KB 包裝；§4 的 orchestrator 一列歸零。

### 3.7 Orchestrator 契約（合併後的 `ddreport` skill 本體，無頭版 ≤2KB；以下為退路版 ≤8KB）
只含：觸發語與短路檢查（90 天內同檔提示）、模型表、`plan → spawn(list) → stage0 finalize → judge prepare → spawn(b1) → judge check → gate prepare → spawn(g) → gate check [→ spawn(b1 patch) → judge check] → prose prepare → spawn(b2) → finish` 的呼叫序、每步的「FAIL 怎麼辦」（重派上限、何時停下問持有人）、最終回報格式。**禁**：讀任何 bundle／報告／validator 全文、手敲 `dd_*.py`。

---

## 4. 模型分工與用量目標

**全帳口徑**（§1.1）：預算含 orchestrator 主線程與判斷層閘，不再有「未計」項。

| 段 | 模型 | 實跑全帳（BE／CIEN，去重尺 cache_read） | v17 目標 | 熔斷線（2×） | 依據 |
|---|---|---|---|---|---|
| orchestrator 主線程 | opus | **11.0／11.7M**（61／69 輪） | **≤2.0M** | 4.0M | 零內容、≤20 輪；每輪 context 由 CLAUDE.md＋記憶決定，本稿管不到，只能管輪次 |
| Stage 0 覆蓋＋數字（a／a1） | sonnet | 5.5／10.1M（含 0e） | **≤3.5M** | 7.0M | 每批 2 軸，context 減半；part check 讓 finalize 零回補；子 agent ≤12 輪 |
| 0e 摘要（a2） | sonnet | 0.9／1.5M | ≤1.0M | 2.0M | 不變 |
| 判斷（b1） | **Fable** | 4.8／2.6M（23／15 輪） | **≤1.2M** | 2.4M | ≤8 輪 × 90K；恆等式前移，瑣碎 FAIL 事前約束 |
| 判斷層閘（g） | opus | 事後抽查 12.6／4.1M（67／29 輪） | **≤2.5M** | 5.0M | 一次讀 bundle、一次寫；抽查模板現行讓 opus 自己 cat 檔、跑腳本，輪次失控，改為只讀 bundle |
| patch（b1 patch，僅 🔴>0） | Fable | — | ≤0.4M | 0.8M | 30K context × ≤6 輪 |
| 散文（b2） | sonnet | 2.4／13.5M（18／69 輪） | **≤1.5M** | 3.0M | ≤7 輪 × 45K；兩次 Write 取代 18 次 |
| **全帳合計（`--full`）** | | **36.6／42.0M** | **≤12M** | — | 較實跑 −70%；Fable −60%、opus −85% |
| **快速版全帳（預設）** | | — | **≤8M** | — | 無散文段、無頭模式 orchestrator 歸零；證據、判斷、閘三段一毛不省 |

目標是估算，不是實測；WP6 前三份回填。**Fable 目標由 ≤3M 改為 ≤1.2M**，且新增 KPI「每個 agent 的輪次上限」（表內）——token 是輪次的函數，管輪次比管 token 直接。

### 4.1 用量熔斷（實跑離散度太大，沒有熔斷的預算不是預算）
- `manifest.json` 記每個 spawn 的 agent id 與段別；每段結束 `ddreport.py` 立即呼叫 `dd_token_report.dedup_sum` 回填該段 cache_read／輪次，並印一行「段／實測／目標／狀態」。
- **超過熔斷線（目標 2×）→ 該段標 `over_budget`，流程停下回報持有人**，不自動重試、不自動進下一段；持有人可下 `ddreport.py resume --accept-over-budget` 續跑。理由：CIEN 散文 69 輪、BE 抽查 67 輪都是「agent 迷路」型失控，早停比事後檢討便宜。
- 子 agent prompt 檔頭寫明自己的輪次上限與「超過即停下回報現況」，讓失控在 agent 端先煞車。
- orchestrator 的輪次由 skill 的呼叫序固定（§3.7 共約 14 次 `ddreport.py`＋N 次 spawn），超過 20 輪本身就是流程偏離的訊號。
- 全帳數字進 `token.json` 與 commit 訊息，退場訊號③以全帳計。

---

## 5. 品質保險（新增與搬家）

| 層 | 現況 | v17 |
|---|---|---|
| 證據完整性 | merge 後 `--strict` 才擋，orchestrator 手剪 as_of | part 交稿即驗；finalize 二驗；缺口自動指名重派 |
| 負向證據接線 | 無（BE 🔴 根因） | **J1 可追溯 validator**（判斷類規則，登記 ledger，§6） |
| 判斷層算術 | 一半在 HTML 階段（verify_dd_math） | **J2 全在 judge check** |
| 判斷層冷讀 | 事後抽查、只計數 | **Stage 1G 上站前閘**，🔴 擋、一輪修補、分歧存檔 |
| 判斷 agent 自查 | ①-⑦ 自評 | 取消（同源盲點；機械部分入 J1–J3） |
| 散文 | 六支閘＋自查⑧ | 六支閘（不變）；自查⑧取消 |
| 同源一致 | gen_dd_tables＋verify D/E | 不變；QC-7／14／36 正式退役（已提名） |
| 覆蓋缺軸 | `--strict` | 不變（退場底線） |

---

## 6. 規則治理（`knowledge/rule_ledger.md` 本稿要登記的條目）

1. **新增：J1 負向證據可追溯**（判斷類，強制判斷 agent 對每條負向 finding 採納或書面不採納）。kill condition：連續 8 份 J1 命中的項目全部以 `evidence_dismissed` 帶過、且 Stage 1G 未再出現「證據在未接線」類 🔴 → 降為 WARN；反向若 Stage 1G 仍出現同類 🔴 ≥2 例 → J1 的判定範圍擴到 `direction="0"`。**加一提刪一**：提名 QC-17／QC-18（`dd_prior.py` 架構性排除，retire-candidates 已列）。
2. **改寫第 21 列**（v16.1 移除流程內 critic）：改為「v17 Stage 1G 判斷層閘」。kill condition：連續 6 份 Stage 1G 首輪判斷級 🔴＝0 → 閘降為抽樣（每 3 份跑 1 份）；任一份 Stage 1G 的 🔴 經判斷 agent 對質不成立（gate_dissent）連續 3 份 ≥2 例 → 檢討 checklist 而非撤閘。兩度命中一次覆寫的舊條文以「PREREG 破例已結案」註記。
3. **退役執行**（retire-candidates.md 已提名，本稿正式提請 2026-10 校準輪前先降級）：QC-7／14／36（gen_dd_tables 單一來源）、QC-17／18（dd_prior）、QC-8（一次寫條款）、QC-2／10／24／25 的「禁自算」警語（Stage 1 無工具權限）。門檻數字全部保留在 judgment-rules。
4. 不新增任何門檻、機率防線、矩陣語意；Bull 可行性壓測（BE 🔴 的後半句）**不**另立規則——J1 已迫使 Crossroads 那條進 `decision_inputs.bear` 或 dismissed，Bull 壓測屬 Stage 1G ⑥ 既有 checklist。

---

## 7. 版本與檔案收斂

### 7.1 退役與歸檔（工作假設②）
- `_archived/skills/stock-analyst-v15.2/`：SKILL.md（125.8KB）、references/html-output.md、references/data-collection.md（v15 Markdown 模板）、SKILL.v16.draft.md、ddreport/SKILL.v3.draft.md。打 tag `dd-v15.2-final` 與 `dd-v16.2-final`。
- `ddreport/SKILL.md` v2.3 內容整份被 §3.7 取代。

### 7.2 合併後的檔案地圖（工作假設③）
```
.claude/skills/ddreport/SKILL.md            ≤8KB  orchestrator 編舞（§3.7）＋觸發語＋模型表
.claude/skills/stock-analyst/SKILL.md       ≤2KB  redirect stub（觸發語 → ddreport），references/ 留在此
.claude/skills/stock-analyst/references/
  judgment-rules.md（41KB→目標 ≤35KB：刪自查①-⑦段與 v16.1 沿革、§16 改指向 Stage 1G）
  render-rules.md（15.9KB，不動）
  archetype-gatesets／cyclical-lens／roic-durability／judgment-playbook／timing-appendix／
  decision-layer／dd-meta-schema／changelog（不動；decision-layer 與 dd-meta-schema 是腳本維護者的權威文件）
  coverage-axes.md、evidence-pack.md（合併成一檔 coverage-axes.md：軸清單＋query 模板＋JSON 契約）
  critic-gates.md → gate-checklist.md（只剩 Stage 1G 的①-⑦與輸出格式；spawn prompt 由 ddreport.py 產）
  delta-refresh.md（不動，待 WP7）
  v16/agent-prompts.md → 拆成 prompts/*.md.tmpl（ddreport.py 的模板來源，不再由人讀）
  v16/validators.md、rule-migration-map.md、retire-candidates.md → 併入 changelog 或 notes/（設計史料）
scripts/ddreport.py                          單一入口（§3）；內部 import 既有 dd_*.py／validate_*.py，不重寫
scripts/dd_gates.sh                          內容併入 ddreport.py gates 後退役
scripts/dd_schema/judgment.schema.json       v17（加 evidence_refs／evidence_dismissed）
scripts/dd_schema/section_map.json           不動（gates FAIL → sid、patch → 段落重寫共用）
.dd_build/runs/{T}_{D}/                      per-run 目錄（gitignored，不變）
notes/site-internal/dd/_src/{T}_{D}/         存查（加 parts/、gate 檔、token.json、manifest）
```
「always-on 讀本」只剩三份：judgment-rules（判斷 agent）、render-rules（散文 agent）、gate-checklist（閘）。SKILL.md 本身不再是任何 agent 的輸入。

### 7.3 CLAUDE.md 同步
模型路由表「v16.2 DD（試點中）」列改為 v17 一列（Stage 0／0e／散文 sonnet、判斷 Fable、判斷層閘 opus、orchestrator opus）；「DD writer 路由」與「writer↔critic 對調」兩段標註「v17 起判斷層＝Fable、閘＝opus，kill condition 見 ledger 第 21 列改寫版」；篇幅預算表不動。

---

## 8. 內容微調（持有人授權範圍內的選配，各自獨立可關）

| 編號 | 內容 | 讀者面變化 | 用量影響 | 建議 |
|---|---|---|---|---|
| C-1 機械段由腳本生成 | `revlog`、`s14`（複審表）、`appA` 敘述、E12 觸發器說明段：全部是 judgment 欄位的復述，由 `gen_dd_tables.py` 擴充成模板生成 | 無（文字更一致） | 散文 agent 少寫約 15–20KB，輸出 token 與一輪 Write 內容減少 | **啟用**，篇幅帶計算不變 |
| C-2 附錄 B 新增「負向證據處置表」 | 由 `evidence_refs`／`evidence_dismissed` 生成：每條負向 finding → 進了哪個欄位／不採納理由 | 新增一張表（約 2–3KB），讀者看得到「哪些壞消息被考慮過」 | 零 | **啟用**（透明度是品質） |
| C-3 `reasoning` 段直接渲染 | 現行已把 reasoning 鋪進 `<div class="reasoning">`；改為散文 agent 對 §5／§6／§11 只准擴寫不准改寫 | 無 | 略減 | 維持現狀即可 |
| C-4 §8 財報章由 KPI 表機械生成骨架 | `latest_quarter_kpis` 已結構化，可先生成表，散文只寫解讀 | 無 | 散文少寫 3–5KB | 可延後 |
| **C-5 快速版（預設產物）** | `ddreport.py brief`：judgment.json → 一頁 `docs/dd/brief/BRIEF_{T}_{D}.html`，零 LLM。內容固定＝dashboard、統一裁決＋倉位角色＋rearm、thesis H／R、決策矩陣命中列與稽核表、contradictions 裁定表、情境樹 E11、triggers E12、pre-mortem 與 Max DD、負向證據處置表（C-2）、reasoning 各模組原文、閘的 🟡 清單、前份漂移歸因。帶與完整版**同欄位** dd-meta（`schema:"v15.0"` 語意不變，另加 `"brief":true`），noindex | 新頁型；研究頁表可收並標「速判」（動到既有聚合面讀法，持有人 2026-09-05 默示同意，反對即改為不入表） | 每份省散文段全部（目標 1.5M，實跑 2.4–13.5M） | **啟用且為預設**；完整版 `--full` 隨時可從同一 judgment.json 補跑散文，不重做證據與判斷 |
| **C-6 白話欄 `judgment.plain`（2026-09-05 第三次拍板，樣張核可）** | 判斷 agent 寫判斷時一併寫五句話、這門生意、我押的三件事／最怕的三件事、市場錯在哪、成長靠什麼、三種未來故事、改變主意的三件事、跟上一份比的主因、怎麼賠、證據品質；快速版照此順序重排，先講人話再給數字；validator 只 WARN；契約見 `_wp_spec_v17_batch3_20260905.md` | 快速版整頁白話化 | Fable 輸出多約 1–2K token | **啟用** |

---

## 9. 工作包與驗收（回溯考卷＝四份 `_src/` 重放）

**前提：`.dd_build/` 已 gitignore，四組 Stage 0 part 檔（`evidence_parts`〔BE〕／`_cien`／`_crdo_20260904`／`_panw`）只存在本機，隨時會被清掉。**

| WP | 內容 | 模型 | 驗收（可機械判定） |
|---|---|---|---|
| **WP0 fixture 搶救** | 把四組 parts 目錄複製進 `_src/{T}_{D}/parts/`，加 README 註明批次對應；commit | sonnet | 四份 `_src/` 各有 parts/；`dd_evidence.py merge` 重放後與 `_src` 的 evidence.json 在 findings 集合上一致（允許 key 順序差） |
| **WP1 入口與 Stage 0** | `ddreport.py` 骨架、manifest 狀態機、`plan`／`part check`／`stage0 finalize`、finding id、prompt 模板化與 JSON 派工契約、per-run 目錄 | sonnet（腳本）；prompt 模板文字 opus | 用 WP0 fixture 重放 CRDO／BE／CIEN：finalize PASS；plan 對三檔產出的軸清單與批數與當時一致；`part check` 對 BE 當時手剪前的 part（若可還原）能指出缺 as_of 的項目 |
| **WP2 判斷層** | schema v17（evidence_refs／dismissed）、J1／J2／J3 進 validate_judgment、bundle 生成、judge prepare／check、判斷 prompt 改寫（刪自查） | sonnet（腳本）；prompt／規則文字 opus | (i) BE 原 judgment 跑 J1 → 列出 Crossroads `supply_demand_durability#0` 未處置（真陽性）；CRDO／CIEN 的未處置清單存檔當校準基線；(ii) BE 原 judgment 跑 J2 → 重現當時 verify_dd_math 攔到的 Max DD 恆等式 FAIL；(iii) `dd_decision --check` 對四份 v16 與 30 份 v15 DD 裁決全同（不變的既有考卷） |
| **WP3 判斷層閘** | gate bundle、gate prompt（沿 `_audit_*` 格式）、`gate check` 解析器、patch prompt 生成（section_map 抽子樹）、dissent 存檔 | sonnet（腳本）；checklist 文字 opus | 解析 `_audit_BE` → 🔴=1、路徑 `supply_demand_durability`；解析 `_audit_CIEN` → 🔴=0；對 BE 產出的 patch prompt 只含 `decision_inputs.bear`／`contradictions[1]`／`scenario` 子樹 |
| **WP4a 快速版與 finish（優先）** | `ddreport.py brief` 一頁模板（C-5 欄目）、C-2 負向證據處置表、index-row、DD commit 檔案集、`_src` 存查、token.json、研究頁「速判」標記 | sonnet | (i) 四份 `_src` judgment → brief 全部渲染成功、qc.py 過、dd-meta 與原 DD 的 dd-meta 逐欄相同（多 `brief:true`）；(ii) `index-row` 對四份 v16 DD 生成的列與 INDEX.md 既有列在前七欄相同；(iii) 對 BE 的 update_dd_index 產物，commit 集排除 weekly_cache 229 檔 |
| WP4b 散文層（選配，`--full`，排最後） | prose bundle、兩檔合併 Write＋split、gates 併入 Python、C-1 機械段 | sonnet | (i) 四份 `_src` 的 prose 合併成 A／B 再 split → 與原 prose/ 逐檔相同；(ii) gates 對四份原 HTML 全過 |
| **WP5 收斂** | §7 歸檔與 tag、skill 合併、judgment-rules 瘦身、ledger 三條登記、CLAUDE.md 同步、retire 執行 | opus（規則文字）；搬檔 sonnet | `ls` 後 always-on 讀本只剩三份；`grep -r "v15.2\|--v16" .claude/skills CLAUDE.md` 無殘留路由語；qc.py 全過 |
| **WP6 試點** | 三份實跑上站（建議含一份同檔重跑、一份無前份新檔、一份爆發候選） | 依 §4 | 退場訊號 §10 四條 |
| WP7（後續） | delta 模式接 `dd_delta.py`；C-4 | — | 另案 |

### 9.1 WP 執行本身的用量紀律（§1.1 第三條結論：建置 agent 是最大黑洞）
- **每個 WP 拆成 ≤40 輪可完成的子任務**再派工；派工 prompt 必須含：要改的檔名清單、驗收指令（一條 Bash）、輪次上限、「超過上限停下回報」。一個 sonnet agent 跑到 100 輪以上就是任務切太大，不是 agent 不夠努力。
- **文字瘦身、規則搬家、格式轉換一律用腳本或 orchestrator 給定的逐字對照表**，不派 LLM「讀完整檔自己想辦法壓縮」（117M 的教訓）。judgment-rules 瘦身（§7.2）由 opus 先列「刪哪幾段」的行號清單，sonnet 只執行刪除。
- 腳本類 WP 先寫測試（§9 驗收欄就是測試），agent 對著測試改到綠，禁止對著整個 pipeline 試跑找 bug。
- 每個 WP 收工時附 `dd_token_report` 三欄，寫進本稿 §12 實測欄；單一 WP 超過 15M 即檢討切法。
- 建置期間不做「順手清理」（並行 session 與 259 檔未 commit 的 working tree 是現況，只 add 自己列出的檔）。

順序（2026-09-05 第二次拍板後）：WP0 已做 → WP1＋WP2 並行（進行中）→ WP3 閘 → WP4a 快速版與 finish → WP5 收斂 → WP6 試點（以快速版跑）→ WP4b 散文層最後、可延後。力氣順序＝證據 → 判斷 → 閘 → 快速版 → 其他。WP1–WP4 全程不動現行檔，新腳本以 `ddreport.py` 為入口、既有 `dd_*.py` 只加參數不改語意；WP5 才切換路由。

---

## 10. 退場訊號（v17，可證偽）

1. 覆蓋缺軸 0（底線，不變）。
2. WP6 三份 Stage 1G 首輪判斷級 🔴 合計 ≤2 且修補後 0；上站後 30 天內另抽一份做第二次冷讀，🔴＝0。**任一份修補兩輪仍 🔴 → 停下給持有人，不上站。**
3. **全帳**去重尺（含 orchestrator 主線程與判斷層閘）：Fable ≤1.2M／份、opus（orchestrator＋閘）≤4.5M／份、全帳 ≤12M／份；三份中兩份未達 → 回頭查輪次而非砍證據；任一段觸發 §4.1 熔斷兩次 → 該段的 agent 契約重寫。
4. 回溯考卷（§9 各 WP 驗收）全綠才切路由；切換後首份若 `dd_decision --check` 與最終 dd-meta 不一致 → 立即回 tag。

## 11. 不做的事
- 不改任何門檻、矩陣、dd-meta 欄位語意、篇幅帶。
- 不對 evidence 去重瘦身作為省 token 手段。
- 不恢復讀 80KB 散文的 critic、不做 re-gate 迴圈。
- 不新建收斂面、不動下游聚合器讀法。
- 不在本輪處理 delta 模式與台股獨立系統。

## 12. 實測回填（WP 收工與 WP6 試點逐筆填，去重尺、全帳）

| 日期 | 項目（WP 或 DD） | orchestrator | sonnet | Fable | opus | 全帳 | 輪次備註 |
|---|---|---|---|---|---|---|---|
| 2026-09-05 | WP0 fixture 搶救 | 本對話內完成，零子 agent | — | — | — | — | 複製＋README；WP1b 重放查出 CRDO parts 實為 SNOW dry-run，已修正（2d42d47ed） |
| 2026-09-05 | WP1a ddreport.py plan／status | — | 0.16M（總 token）／40 tool uses／12 分 | — | — | — | commit 24657e01d |
| 2026-09-05 | WP1b part check＋finalize | — | 0.17M／31／11 分 | — | — | — | 同上；BE batch2 因自然語言 as_of 整批拒收（設計內） |
| 2026-09-05 | WP1c dd_headless.py | — | 0.12M／26／7 分 | — | — | — | 同上；真呼叫 4 次（超規 1 次，已據實回報） |
| 2026-09-05 | WP2 J1／J2／J3＋bundle | — | 0.22M／61／15 分 | — | — | — | commit ad4204a5c；J1 基線 BE 18／CIEN 15／CRDO 14 |

| 2026-09-05 | WP-text 三份 prompt 模板（opus） | — | — | — | 0.10M／20／4 分 | — | commit 85ad2dc84；判斷 70／閘 70／修補 40 行 |
| 2026-09-05 | WP3 dd_gate.py | — | 0.15M／26／9 分 | — | — | — | 同上；BE 抽查解析 red=1 |
| 2026-09-05 | WP4a dd_brief.py | — | 0.17M／47／10 分 | — | — | — | commit d526900d2；四份 fixture dd-meta 逐欄同 |
| 2026-09-05 | WP1d ddreport.py run＋replay | — | 0.28M／**98**／28 分 | — | 誤呼叫真 opus 閘 1 次（≈$0.85） | — | commit f4154f428；超出 40 輪上限（串接任務切太大，下次拆 stage0／judge／gate 三件）；查出 dd_decision 與洩漏檢查打架，已修 |
| 2026-09-05 | **AVGO 第一份真跑（快速版，上站 8b4246fb5）** | 0（無頭） | 6.01M（Stage 0 含摘要重派） | 0.90M（判斷 9 輪＋修補 2 輪；輸出 65K） | 0.41M（閘兩次） | **7.3M**（≈$17） | 裁決 進場｜衛星 row 10，與前份同向；閘首輪 🔴 1（第③軸兩條證據未接）修補後 0；三次撞牆重跑約 1.2M 屬流程缺陷（第五批修正單） |
| 2026-09-05 | **HPE 第二份真跑（快速版，第五批修正後）** | 0（無頭） | 7.90M（Stage 0，摘要 2.54M 超預算放行） | 1.55M（判斷 7 輪一次過＋修補 7 輪；輸出 73K） | 0.14M（閘一次） | **9.6M**（≈$19） | 觀望｜追蹤 row 8 估值爭議；閘 🔴 3（③通路兩條、⑥IRR 含息算術、⑧前份缺欄）修補後 0、裁決未翻；peers 早停一次（手動給）；驗證器兩處自相矛盾已修 |
| 2026-09-05 | **WDAY 第三份真跑（快速版，摘要拆篇後，全程無人接手）** | 0（無頭） | 6.92M（Stage 0；摘要 3 篇各 4 輪 0.25–0.27M，兩次重派各 0.6–0.8M） | 1.31M（判斷 9 輪一次過＋修補 2 輪；輸出 65K） | 0.16M（閘一次） | **8.4M**（≈$21） | 進場｜衛星 row 9b；peers 自動由 ID 推（PLTR／CRM／MSFT／NOW）；閘 🔴 2（R2 減倉線方向與觸發器相反、再投資率 45%→53.8%）修補後 0；熔斷線 1×→2× 修正後續跑 |

八個建置子任務合計 ≈1.4M、除 WP1d 外皆 ≤61 tool uses，對照 v15.2／v16 建置期單一 agent 50–117M：§9.1 的「≤40 輪、驗收即測試」紀律有效。**整條線已可零 LLM 重放**：CIEN fixture stage0→judged→gated（red 0／yellow 4，與抽查一致）→brief 75KB；BE 到 gated red=1 走修補路徑。`scripts/tests` 44 passed。
