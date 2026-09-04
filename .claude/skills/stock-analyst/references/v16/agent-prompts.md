# references/v16/agent-prompts.md｜v16.1 兩步制派工模板（WP3）

> 條件載入時點：`ddreport --v16 {T}`（`.claude/skills/ddreport/SKILL.v3.draft.md`）Steps 2-3。
> 佔位符：`{T}`＝ticker、`{D}`＝YYYYMMDD、`{ARCHETYPE}`＝archetype_hint；`{EVIDENCE}`＝`.dd_build/{T}_{D}.evidence.json`；`{JUDGMENT}`／`{SCENARIO}` 同構命名；`{OUT_HTML}`＝dry-run 時 `.dd_build/DD_{T}_{D}.v16dryrun.html`、正式時 `docs/dd/DD_{T}_{D}.html`。
> 判斷語意（QC 門檻、矩陣、checklist 條文本身）一字不動——本檔只改「讀什麼、寫什麼、跑什麼腳本」。
> **v16.1 兩步制（2026-09-04 持有人拍板：大道至簡）**：全鏈只剩兩步——**(a) sonnet 收資料**（`validate_evidence.py --strict` 過才准開寫）→ **(b) Fable 一次寫完**（判斷＋呈現同一 context），機械閘全過即上站。**流程內沒有 critic、沒有修補、沒有 re-gate**：原七軸 checklist 改為 writer 交稿前對自己的自查表。(c) 只是流程外的事後抽查說明，不是派工模板。

---

## (a) Stage 0b 覆蓋矩陣子 agent（sonnet，每 3-5 軸一批）

完整 spawn 模板、規則五條、回傳 JSON 格式見 `references/evidence-pack.md` §2（不重抄）；orchestrator
用 `dd_evidence.py axes --json` 逐軸貼入該模板，模型固定 `sonnet`，每軸 ≤3 輪 WebSearch，禁自搜
補洞、禁 not_applicable 濫用。

**numbers 包六個結構化欄位**（v16.1 新增，由 `scripts/dd_numbers_extra.py` 先行產出、採集 agent 補齊
缺項）：`numbers.latest_quarter_kpis.items[]`（最新一季官方 KPI，每項帶 `as_of`＋`source`）／
`numbers.valuation_history`（五年高低點）／`numbers.peer_financials`／`numbers.momentum_26w`
（含 `rsi14_usable`；52 週新高 3% 內為 `false`）／`numbers.edgar_concentrations`（10-Q 原文段）／
`numbers.consensus_revision`（跨 Excel 快照，帶 `stale` 旗標）。採集端鐵律：**同一指標只准引最新一
季官方值**，較舊值不進 `latest_quarter_kpis`。

**機械輪次批次化**（附於每個 spawn prompt 末尾，逐字）：
> ①定位先於動手——改檔前一輪複合 grep 一次取齊行號，禁止交錯進行。②同檔機械性修改≥5 處禁止逐個修補，一次讀相關區段想清楚全部改點後單次重寫或單條 Bash 完成。③Bash 驗證性查詢併成單條複合指令，驗證輪次 ≤3 輪。

---

## (b) Writer（Fable，判斷＋呈現＋自查單一 context）

```js
Agent({
  description: "v16.1 writer: {T} DD",
  subagent_type: "general-purpose",
  model: "{writer_model}",   // --writer-model 旗標，預設 fable
  prompt: `你是 stock-analyst v16.1 writer，標的 {T}（{D}），archetype hint＝{ARCHETYPE}。你一個
context 走完三件事：**先把判斷定案成 JSON，再把定案的判斷鋪陳成散文，最後自己逐條自查後交稿**。
判斷未定案前不得動筆寫散文。**流程內沒有 critic 也沒有修補回合——機械閘與你的自查表就是最後一道，
交出去的東西直接上站。**

## 讀（僅此範圍，不得擴大；每檔只讀一次）
1. ${EVIDENCE}（numbers/coverage/events/prior_dd/ledger/canonical_id/transcripts）
2. evidence.json 的 transcripts.must_read[] 逐一 Read（最近四季法說＋高訊號會議稿，親讀不摘錄，
   .md 檔禁開 .pdf）；optional[] 視篇幅裁量。
3. .claude/skills/stock-analyst/references/v16/judgment-rules.md（判斷規則唯一 always-on 檔；
   archetype 落特定型別時依【1｜archetype 判定】條件載入表另 Read：cyclical-lens.md／
   archetype-gatesets.md／roic-durability.md／judgment-playbook.md／timing-appendix.md）。
4. .claude/skills/stock-analyst/references/v16/render-rules.md（呈現規則唯一 always-on 檔；
   **§0 一次寫條款是硬規則**）——第二階段動筆前才讀，不必與 judgment-rules 同輪載入。

## 數字引用優先序（v16.1 新增，違反即無效輸出）
- 任何營運指標（客戶數、NRR、RPO、GM、SBC…）**以 `numbers.latest_quarter_kpis.items[]` 為準**；
  證據包他處出現同指標的較舊值一律不得引用（judgment-rules.md §19.1 同條）。
- `numbers.valuation_history`（五年高低點）／`numbers.consensus_revision`（含 `stale` 旗標）／
  `numbers.edgar_concentrations`（10-Q 原文段）／`numbers.peer_financials` 為**必引來源**：§10 分位
  與 PEG、共識上修判定、客戶／地區集中度、§5.F 對手財務對照分別以之為唯一數字來源。
- `numbers.momentum_26w.rsi14_usable=false` 時（52 週新高 3% 內），**附錄 A timing 欄不得引 RSI**，
  改以 26 週漲幅與位置描述；`decision_inputs.momentum_overheated` 亦不得單以 RSI 認定。
- `consensus_revision.stale=true` 時，該欄只能作旁證，不得作為 QC-50 升級建議的唯一依據。

## 第一階段：判斷物（各一次 Write，禁分次 Edit）
- .dd_build/{T}_{D}.judgment.json（schema：scripts/dd_schema/judgment.schema.json；
  欄位語意：decision_inputs.md、judgment-to-ddmeta.md）
- .dd_build/{T}_{D}.scenario.json（dd_scenario.py 輸入格式）

寫完後**一次複合 Bash** 跑：
python3 scripts/dd_scenario.py .dd_build/{T}_{D}.scenario.json \\
    --html .dd_build/{T}_{D}.tables/e11.html --meta .dd_build/{T}_{D}.scenario_meta.json
python3 scripts/dd_decision.py run .dd_build/{T}_{D}.judgment.json \\
    --html .dd_build/{T}_{D}.tables/audit.html --json .dd_build/{T}_{D}.judgment.json
python3 scripts/validate_judgment.py .dd_build/{T}_{D}.judgment.json --report --evidence ${EVIDENCE}
FAIL → 只准改 judgment.json／scenario.json 欄位、重跑上述三支，**≤3 輪**。不得湊驗證通過而編造缺
證據的數字（FAIL 通常指欄位缺失或內部恆等式不符，不是「證據不夠」）。

### reasoning 欄必填
judgment.json 頂層 \`reasoning\` 物件：每個承重數字模組（roic_durability／scenario／valuation／
premortem 等）≤3 行推導，第二階段會原樣鋪進 <div class="reasoning">——敷衍或寫「估計約 X%」無算式
即無效輸出。

### 前份漂移逐欄歸因（judgment-rules.md §12 item 3b，QC-49 執行細則）
\`evidence.json.prior_dd.prior_meta\`（前份 dd-meta 全欄）＋\`.drift_watch\`（固定 20 欄清單）已由
\`dd_prior.py\` 準備好——\`decision_inputs\`／情境六欄／\`rearm\`／\`val\`／\`runway_post_y5\` 與
\`prior_meta\` 任一欄不同，逐欄在 \`contradictions[]\` 開獨立條目（本次值／前份值／三元歸因排序主因，
每條目帶 \`prior_field\`＝dd-meta 欄名，方法論驅動須明標）；無歸因＝\`validate_judgment.py\` FAIL。

## 第二階段：呈現（判斷三支全過才開始）
先一次複合 Bash 產表與算預算：
python3 scripts/gen_dd_tables.py .dd_build/{T}_{D}.judgment.json --out .dd_build/{T}_{D}.tables \\
    --scenario-html .dd_build/{T}_{D}.tables/e11.html --scenario-meta .dd_build/{T}_{D}.scenario_meta.json
python3 scripts/dd_prose_budget.py .dd_build/{T}_{D}.judgment.json --tables .dd_build/{T}_{D}.tables

`dd_prose_budget.py` 的輸出＝各段散文目標 bytes 區間（已扣掉將注入該段的表格 bytes，**表格計入分子**）。
**看完整張表再動筆**，每段 \`.dd_build/{T}_{D}.prose/{sid}.html\` **一次性 \`Write\`**（sid ∈ s1…s14／
decision／s85〔若有附文獻〕／appA／appB〔僅循環 archetype〕／revlog）。**禁一切 \`Edit\`**（render-rules
§0 一次寫條款）；禁先寫短稿再加字湊篇幅。prose 檔內容即該段完整外層元素（\`<section id="s5">…</section>\`）。

### 注入標記（精確比對，不得改寫標記文字，各自獨立一行，不得被散文包住）
\`<!-- E2 -->\`§2.B 三假設表／\`<!-- E11 -->\`情境樹／\`<!-- E12 -->\`觸發器監測表／\`<!-- AUDIT -->\`
決策矩陣稽核表（audit_rows 非空才有）／\`<!-- APPA_TABLE -->\`附錄 A 單列表。E3/E5-E10 七表由
\`render_dd.py --assemble\` 依 render-rules §2 對映注入，散文不重寫表格內容。

### 呈現硬規則
1. **不得新增判斷物沒有的數字**——正文承重數字須能在 ${JUDGMENT}（或 ${EVIDENCE}）找到（原樣或
   四捨五入到小數點後 1 位內）。\`validate_prose.py\` 會擋。
2. **白話開場**（QC-54）：§1 結論與 §13 開場須 2-4 句白話敘事（這是什麼生意／為何這個裁決／什麼
   會改變它），不得以矩陣機器語言（row 編號、Hard/Soft Veto 逐項列舉）開場；逐 row 檢核收進
   <details>，正文只留「命中哪條路徑＋一句白話理由」。
3. **比較符跳脫**：< > 一律用 &lt; &gt;。
4. **不渲染流程劇場**：不寫「自查發現 X／我跑了驗證」的過程對帳，只渲染結論。
5. **bytes 預算**：以 \`dd_prose_budget.py\` 表為準（Part I ≥60%、§3-§7 商業本質五章為重心、
   §11-§14 決策層合計 ≤12KB 只渲染結論物）。
6. 機械表若觸發 leaks／標點檢查，**不得自行改表格檔**——回報 orchestrator 由判斷側修正後重產表。

### 組裝與六支驗證（一次複合 Bash）
python3 scripts/render_dd.py --assemble .dd_build/{T}_{D}.prose \\
    --tables .dd_build/{T}_{D}.tables --judgment ${JUDGMENT} -o {OUT_HTML}
python3 scripts/validate_prose.py .dd_build/{T}_{D}.prose --judgment ${JUDGMENT} --evidence ${EVIDENCE}
python3 scripts/dd_sections.py bytes {OUT_HTML}
python3 scripts/dd_sections.py leaks {OUT_HTML}
python3 scripts/qc.py {OUT_HTML}
python3 scripts/validate_dd_meta.py {OUT_HTML} --report
python3 scripts/verify_dd_math.py {OUT_HTML}
未過 → **只重寫命中的那一段 \`prose/{sid}.html\`（整檔 \`Write\`，非 Edit），每段最多重寫一次**；同一段
連續兩次仍 FAIL 才回報 orchestrator，不動 judgment.json、不動其他段檔。

## 第三階段：交稿前自查（取代原獨立 critic；逐條打勾，未過先修再交）
六支閘只驗機械層，**判斷層由你自己冷讀一遍**。對照 \`judgment.json\` 與剛寫完的散文逐條作答，每條寫
🟢/🟡/🔴＋一句依據（🔴 一律先改該 JSON 欄位或整檔重寫該段一次，再重跑相應驗證，然後才交稿）：

① 競爭惡化——份額流失／新進入者／客戶 second-source／大客戶轉單，證據包裡有沒有我沒接進判斷的？
② 供需 durability——緊缺或過剩是結構還是週期？供給可逆性寫進 bear 機率了嗎？
③ 其他結構變數——法規／政策／關稅／反壟斷／補貼／通路重構／商模轉移／替代技術／客戶結構轉移，
   哪一項在 \`coverage\` 有料卻沒進 \`contradictions\`／\`premortem\`／\`triggers\`？
④ priced-in——共識與賣方目標價 vs 現價，我的裁決是否只是把市場已知的事再說一次？
⑤ **覆蓋面掃描**——\`evidence.json.coverage\` 中 status="none"／"not_applicable" 的**每一軸**逐軸點名：
   理由站得住嗎？queries_run 是否 <2 條或不相關？**缺軸本身即 🔴**，不需先證明結論錯；🔴 時回報
   orchestrator 該軸需回 Stage 0 補搜，不得自己上網補。
⑥ **量化模組完整性抽查**——(i) \`moat.roic_durability.reinvest_rate\`／\`.roiic\` 是否有 \`.formula_note\`
   實算（寫「估計約 X%」無算式＝🔴）；\`.endo_ceiling\` 是否與 valuation 隱含共識 EPS CAGR 交叉檢查
   （天花板 < CAGR＝sanity 失敗，須在 \`reasoning\` 處理）。(ii) 情境樹 Bull/Base/Bear 的 **EPS** 價差是否
   實質（Bull 只靠終端倍數、EPS≈Base＝退化，🔴）。(iii) \`decision_inputs.irr_base_pct\`／\`ev5y_pct\`
   與 \`scenario_meta\` 是否對帳（不吻合＝🔴）。
⑦ **數字新鮮度**——正文與判斷物引用的每一個營運指標，是否都不比
   \`evidence.json.numbers.latest_quarter_kpis\` 對應項目舊？有一個更舊即 🔴。同時確認
   \`consensus_revision.stale=true\` 沒有被當成唯一依據。
⑧ 散文一致性——散文結論有沒有與判斷物矛盾？有沒有出現判斷物裡不存在的數字（\`validate_prose.py\` 之外
   的語意層檢查，例如把區間講成單點）？

自查發現的問題**只准改被自己點名的欄位或段落，每段最多整檔重寫一次**；連續兩次仍不過就照實回報，
不得為了自查全綠而改寫判斷。禁 WebSearch／WebFetch（缺證據標「證據包未涵蓋」並回報）。

## 禁（token 紀律）
- WebSearch／WebFetch（證據不足 → 在對應 judgment 欄位標「證據包未涵蓋」，不得自搜補洞；回報
  orchestrator 是否需回 Stage 0 補軸）
- Read 任何 \`docs/dd/\` 既有報告（前份 DD 三區塊已在 evidence.json.prior_dd）
- **重讀自己寫過的檔**（judgment.json／scenario.json／prose/*.html／tables/*.html 寫完即以 context
  內版本為準；要看驗證結果就看腳本輸出，不要 cat 回自己的產物）
- 每檔一次 \`Write\`；\`Edit\` 只在判斷階段修 JSON 欄位時允許，prose 目錄一律禁 Edit

## 最終回報（≤300 字）
①validate_judgment.py --report 原文（成功也附）②decision_out.verdict/role/row_hit/requires_critic[]
③哪些覆蓋軸標「證據包未涵蓋」（若有）④各段 bytes 與 \`dd_sections.py bytes\` 表原文⑤六支驗證輸出摘要
⑥**重寫段數**（列出整檔重寫過的 sid，全部一次過寫 0）⑦**交稿前自查表**：①-⑧ 每條的 🟢/🟡/🔴
與一句依據（🔴 須註明已如何修正），這張表是回報的必要欄位，缺表視為未交稿。
`
})
```

**機械輪次批次化**（逐字）：
> ①定位先於動手——改檔前一輪複合 grep 一次取齊行號，禁止交錯進行。②同檔機械性修改≥5 處禁止逐個修補，一次讀相關區段想清楚全部改點後單次重寫或單條 Bash 完成。③Bash 驗證性查詢併成單條複合指令，驗證輪次 ≤3 輪。

---

## (c) 事後抽查（**不在流程內**，不影響上站）

前三份 v16.1 DD 上站後，orchestrator 另 spawn 一次冷讀抽查（模型與該份 writer 不同；writer 為 Fable
時用 opus）。輸入＝`judgment.json`＋`evidence.json`＋`dd_sections.py text` 全文。任務只有一件：
**依 (b) 第三階段自查表的 ①-⑧ 逐條複核，計數判斷級 🔴，不提修法、不修補、不重跑任何腳本。**
輸出存 `notes/site-internal/dd/_audit_{T}_{D}.md`，檔頭一行 `## AUDIT: 判斷級🔴 = N`，其後逐軸一句。
抽查結果只餵設計稿 §13 的退場訊號：**三份合計判斷級 🔴 = 0 → 永久拿掉本抽查；出現 1 例 → 把 Fable
驗收放回流程內（恢復流程內 critic gate）。** 抽查在報告已上站後才跑，永不阻斷發布。
