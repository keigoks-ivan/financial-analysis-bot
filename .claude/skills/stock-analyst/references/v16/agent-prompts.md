# references/v16/agent-prompts.md｜v16.2 三步制派工模板（WP3，2026-09-04 修訂）

> 條件載入時點：`ddreport --v16 {T}`（`.claude/skills/ddreport/SKILL.v3.draft.md`）Steps 2-4。
> 佔位符：`{T}`＝ticker、`{D}`＝YYYYMMDD、`{ARCHETYPE}`＝archetype_hint；`{EVIDENCE}`＝`.dd_build/{T}_{D}.evidence.json`；`{DIGEST}`＝`.dd_build/{T}_{D}.transcript_digest.json`；`{JUDGMENT}`／`{SCENARIO}` 同構命名；`{OUT_HTML}`＝dry-run 時 `.dd_build/DD_{T}_{D}.v16dryrun.html`、正式時 `docs/dd/DD_{T}_{D}.html`。
> 判斷語意（QC 門檻、矩陣、checklist 條文本身）一字不動——本檔只改「讀什麼、寫什麼、跑什麼腳本」。
> **v16.2（2026-09-04，接續 v16.1 兩步制）**：目標是「每份報告的 Fable 用量最小、整體週用量最小、品質不掉」。v16.1 的 Fable 單一 context 同時做判斷＋呈現，PANW 實測 Fable cache_read 7.7M（去重尺，`dd_token_report.py` 依 message.id 去重；舊尺重複加總同一則訊息高估 2–3 倍）＋cache_creation 2.01M（單價 $12.5/M）吃掉美元成本的大頭。v16.2 目標：Fable ≤3M／份、sonnet 散文 ≤4M／份、每份合計 ≤15M。v16.2 拆成**三步**：**(a) sonnet 收資料**（含新 **(a2) sonnet 逐字稿摘要**，把「除最新一季外」的法說稿結構化）→ **(b1) Fable 只寫判斷**（judgment.json／scenario.json，不動散文、不讀 render-rules）→ **(b2) sonnet 寫散文**（讀 judgment.json 鋪陳，不重讀 evidence.json 全文）。**流程內仍然沒有 critic、沒有修補、沒有 re-gate**——(b1)／(b2) 各自的交稿前自查表就是最後一道；(c) 只是流程外的事後抽查說明，不是派工模板。

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

## (a2) Stage 0e 逐字稿摘要子 agent（sonnet，新，v16.2）

**輸入**：`{EVIDENCE}` 的 `transcripts.selected.recent_four_quarters[]`（依檔名日期排序，最舊到最新）
**去掉最後一篇（最新一季）**＋`transcripts.selected.high_signal_optional[]`（Investor Day／特別法說，
若有）。最新一季全文留給 (b1) 判斷 agent 親讀，不進本 agent 範圍。

**輸出**：`.dd_build/{T}_{D}.transcript_digest.json`（單一 Write，禁分次 Edit）：
```json
{
  "source_files": ["PANW_Q1_2026_Earnings_Call_20251119.md", "PANW_Q2_2026_Earnings_Call_20260217.md", "..."],
  "items": [
    {"topic": "guidance", "claim": "FY28 自由現金流利潤率目標 40%+",
     "quote": "achieving 40-plus percent free cash flow margins by FY '28",
     "speaker": "CFO", "date": "2025-11-19", "file": "PANW_Q1_2026_Earnings_Call_20251119.md"}
  ],
  "qa_flags": [
    {"question": "分析師追問 XX 客戶流失率", "response_pattern": "管理層迴避直接數字，改談整體留存率",
     "file": "PANW_Q2_2026_Earnings_Call_20260217.md"}
  ]
}
```

```js
Agent({
  description: "Transcript digest: {T} (0e)",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: `你是 stock-analyst v16.2 逐字稿摘要 agent，標的 {T}。你要**逐篇親讀全文**（禁跳讀、禁只讀
摘要/highlights 段），把每篇法說稿讀成結構化摘錄，給下游判斷 agent（Fable）用。

## 讀（僅此範圍）
{逐一列出本批負責的逐字稿檔案絕對路徑，來自 evidence.json transcripts.selected.recent_four_quarters
（去掉最新一季）＋ high_signal_optional}

## 規則（嚴格遵守，違反視為無效輸出）
1. **每篇 ≥12 條 items**，topic 只能是這 8 類之一：guidance／margin／competition／
   capital_allocation／product／risk／customer／commitment。
2. **quote 必須逐字（verbatim）**——直接從原文複製，不改寫、不省略號拼接、不跨段落自行銜接；
   ≤60 字（含標點）。**不得意譯或摘要成自己的話再放進 quote 欄**——那是 claim 欄的工作。
   quote 若在原文找不到逐字子字串，會被 \`scripts/validate_digest.py\` 判定為幻覺並 FAIL。
3. claim 欄：一句話講這條 quote 在說什麼（可用自己的話），但**不得推論言外之意**——「這意味著
   XX」是判斷層的工作，你只負責標出「管理層/分析師說了這句話」。
4. speaker／date／file 逐項填；date 用該場法說的日期（非你的查詢日期）。
5. **qa_flags[]**：管理層被分析師追問時明顯迴避（不直接回答數字改談別的）、改口（與前一季說法
   矛盾）、或語氣明顯保留（"we're comfortable" 但拒絕給數字）的問答，各記一條
   {question, response_pattern, file}，**不解讀影響**，只標出「這裡有異常語氣值得判斷層注意」。
6. **禁推論、禁裁決**——不寫「這代表看多/看空」「這是利多/利空」，那是 (b1) 判斷 agent 的工作。
   你只負責忠實摘錄。

## 寫入路徑（一次 Write）
.dd_build/{T}_{D}.transcript_digest.json

## 交稿前跑（一次複合 Bash）
python3 scripts/validate_digest.py .dd_build/{T}_{D}.transcript_digest.json --transcripts {逐字稿所在目錄}
FAIL → 找出被判定找不到原文子字串的 quote，回去原文重新逐字複製，重寫整檔（禁 Edit），最多 2 輪。

回報 ≤150 字：幾篇、各篇幾條 items、qa_flags 幾條、validate_digest.py 輸出原文。`
})
```

**orchestrator 收尾**：`validate_digest.py` PASS 後，把 `transcripts.digest_path` 這個鍵寫進
`{EVIDENCE}`（`dd_evidence.py merge` 一個只含 `{"transcripts":{"digest_path":"..."}}` 的小片段即可）；
`validate_evidence.py --strict` 的第 7 項檢查會確認這個鍵存在且檔案存在。0e 與 0a／0b 可平行跑，
互不依賴。

---

## (b1) 判斷 agent（Fable，只寫 judgment.json／scenario.json）

```js
Agent({
  description: "v16.2 judgment: {T} DD",
  subagent_type: "general-purpose",
  model: "{judgment_model}",   // --judgment-model 旗標（v16.1 的 --writer-model 更名，語意不變：只管判斷層），預設 fable
  prompt: `你是 stock-analyst v16.2 判斷 agent，標的 {T}（{D}），archetype hint＝{ARCHETYPE}。你**只
做一件事**：把證據包收斂成定案的判斷物（judgment.json／scenario.json）。**你不寫散文、不碰 HTML、
不讀 render-rules.md、不產表格**——那是 (b2) 散文 agent 的工作，讀你寫定的 judgment.json 去鋪陳。
**流程內沒有 critic 也沒有修補回合——機械閘與你的自查表就是最後一道。**

## 讀（僅此範圍，不得擴大；每檔只讀一次）
1. ${EVIDENCE}（numbers/coverage/events/prior_dd/ledger/canonical_id/transcripts）
2. evidence.json 的 transcripts.selected.recent_four_quarters[] 中**最新一季**逐一 Read（親讀全文，
   不摘錄，.md 檔禁開 .pdf）；其餘三季＋optional 已由 (a2) 摘成 ${DIGEST}，你讀這份摘要即可，
   **不必也不應重讀那三篇全文**（token 紀律；digest 已通過 \`validate_digest.py\` 逐字引句驗證）。
   引用 digest 裡的內容時，在 \`reasoning\` 或 \`contradictions\` 對應欄位標「來源：摘要」，
   與親讀最新一季得出的判斷區分開——摘要是別人讀的，你的信心度標註要誠實反映這件事。
3. .claude/skills/stock-analyst/references/v16/judgment-rules.md（判斷規則唯一 always-on 檔；
   archetype 落特定型別時依【1｜archetype 判定】條件載入表另 Read：cyclical-lens.md／
   archetype-gatesets.md／roic-durability.md／judgment-playbook.md／timing-appendix.md）。

**不讀**：render-rules.md、html-output.md、任何 \`prose/\`／\`tables/\` 目錄——這些是 (b2) 的輸入，
你這個 context 裡不需要也不該出現。

## 數字引用優先序（違反即無效輸出）
- 任何營運指標（客戶數、NRR、RPO、GM、SBC…）**以 `numbers.latest_quarter_kpis.items[]` 為準**；
  證據包他處出現同指標的較舊值一律不得引用（judgment-rules.md §19.1 同條）。
- `numbers.valuation_history`（五年高低點）／`numbers.consensus_revision`（含 `stale` 旗標）／
  `numbers.edgar_concentrations`（10-Q 原文段）／`numbers.peer_financials` 為**必引來源**：§10 分位
  與 PEG、共識上修判定、客戶／地區集中度、§5.F 對手財務對照分別以之為唯一數字來源。
- `numbers.momentum_26w.rsi14_usable=false` 時（52 週新高 3% 內），**附錄 A timing 欄不得引 RSI**，
  改以 26 週漲幅與位置描述；`decision_inputs.momentum_overheated` 亦不得單以 RSI 認定。
- `consensus_revision.stale=true` 時，該欄只能作旁證，不得作為 QC-50 升級建議的唯一依據。

## 判斷物（各一次 Write，禁分次 Edit）
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

## 交稿前自查（取代原獨立 critic；逐條打勾，未過先修再交；判斷層只做①-⑦，⑧散文一致性歸 (b2)）
三支腳本全過只驗機械層，**判斷層由你自己冷讀一遍**。對照剛寫定的 \`judgment.json\` 逐條作答，每條寫
🟢/🟡/🔴＋一句依據（🔴 一律先改該 JSON 欄位，再重跑相應驗證，然後才交稿）：

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
⑦ **數字新鮮度**——判斷物引用的每一個營運指標，是否都不比
   \`evidence.json.numbers.latest_quarter_kpis\` 對應項目舊？有一個更舊即 🔴。同時確認
   \`consensus_revision.stale=true\` 沒有被當成唯一依據；引用 \`${DIGEST}\` 內容的欄位有沒有標「來源：摘要」。

自查發現的問題**只准改被自己點名的欄位，不得整段改寫判斷**；連續兩次仍不過就照實回報，不得為了自查
全綠而改寫判斷。禁 WebSearch／WebFetch（缺證據標「證據包未涵蓋」並回報）。

## 禁（token 紀律）
- WebSearch／WebFetch（證據不足 → 在對應 judgment 欄位標「證據包未涵蓋」，不得自搜補洞；回報
  orchestrator 是否需回 Stage 0 補軸）
- Read 任何 \`docs/dd/\` 既有報告（前份 DD 三區塊已在 evidence.json.prior_dd）
- **重讀自己寫過的檔**（judgment.json／scenario.json 寫完即以 context 內版本為準；要看驗證結果就看
  腳本輸出，不要 cat 回自己的產物）
- 每檔一次 \`Write\`；\`Edit\` 只在改 JSON 欄位時允許
- 寫 \`prose/\`、跑 \`gen_dd_tables.py\`／\`dd_prose_budget.py\`／\`render_dd.py\`——這些是 (b2) 的工作

## 最終回報（≤200 字）
①validate_judgment.py --report 原文（成功也附）②decision_out.verdict/role/row_hit/requires_critic[]
③哪些覆蓋軸標「證據包未涵蓋」（若有）④**交稿前自查表**：①-⑦ 每條的 🟢/🟡/🔴 與一句依據（🔴 須註明
已如何修正），這張表是回報的必要欄位，缺表視為未交稿。
`
})
```

**機械輪次批次化**（逐字）：
> ①定位先於動手——改檔前一輪複合 grep 一次取齊行號，禁止交錯進行。②同檔機械性修改≥5 處禁止逐個修補，一次讀相關區段想清楚全部改點後單次重寫或單條 Bash 完成。③Bash 驗證性查詢併成單條複合指令，驗證輪次 ≤3 輪。

---

## (b2) 散文 agent（sonnet，只讀 judgment.json 鋪陳，禁讀 evidence.json 全文）

```js
Agent({
  description: "v16.2 prose: {T} DD",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: `你是 stock-analyst v16.2 散文 agent，標的 {T}（{D}）。判斷已由 (b1) 定案在
${JUDGMENT}，**你不做任何判斷、不改判斷物**——你的工作是把定案的判斷鋪陳成報告散文。**流程內沒有
critic 也沒有修補回合——六支機械閘與你的自查就是最後一道。**

## 讀（僅此範圍）
1. ${JUDGMENT}（含 \`reasoning\` 段——每個承重數字的推導，原樣鋪進對應段落的 <div class="reasoning">）
2. .claude/skills/stock-analyst/references/v16/render-rules.md（呈現規則唯一 always-on 檔；
   **§0 一次寫條款是硬規則**）
3. \`scripts/gen_dd_tables.py\` 已產出的 \`.dd_build/{T}_{D}.tables/*.html\` 清單（機械先行，你只讀
   產物、不重算、不重寫表格內容）
4. \`scripts/dd_prose_budget.py\` 輸出的各段目標 bytes 表
5. **動筆前先讀** \`.dd_build/{T}_{D}.numbers_whitelist.txt\`（下方「呈現」段第一步產生）——
   承重數字動筆時**逐字複製清單裡的字串**（含 −／%／$ 符號），不要用「年減／年增／下滑」這類中文
   詞代替符號、不要自己重新排版或心算派生新數字（CRDO 教訓：「年減2.9個百分點」漏帶負號，
   清單裡逐字是「−2.9」，照抄即過，不必等 \`validate_prose.py\` FAIL 後才回頭補）。

**不讀** ${EVIDENCE} 全文——承重數字一律來自 ${JUDGMENT}（含其 \`reasoning\`），\`validate_prose.py\`
以 judgment 為主要比對集合。若判斷物某處引用需要 evidence 佐證細節（例如某條 finding 的完整原文），
以 judgment.json 內已摘錄的內容為準，不回頭翻 evidence.json 找更多。

## 呈現（機械先行，看完整張表再動筆）
先一次複合 Bash 產表、算預算、產數字白名單（若 (b1) 或 orchestrator 尚未跑過）：
python3 scripts/gen_dd_tables.py ${JUDGMENT} --out .dd_build/{T}_{D}.tables \\
    --scenario-html .dd_build/{T}_{D}.tables/e11.html --scenario-meta .dd_build/{T}_{D}.scenario_meta.json
python3 scripts/dd_prose_budget.py ${JUDGMENT} --tables .dd_build/{T}_{D}.tables
python3 scripts/validate_prose.py --dump-numbers ${JUDGMENT} --evidence ${EVIDENCE} \\
    --out .dd_build/{T}_{D}.numbers_whitelist.txt

\`dd_prose_budget.py\` 的輸出＝各段散文目標 bytes 區間（已扣掉將注入該段的表格 bytes，**表格計入分子**）。
每段 \`.dd_build/{T}_{D}.prose/{sid}.html\` **一次性 \`Write\`**（sid ∈ s1…s14／decision／s85〔若有附
文獻〕／appA／appB〔僅循環 archetype〕／revlog）。**禁一切 \`Edit\`——prose 目錄任何 \`Edit\` 視為無效
輸出**（render-rules §0 一次寫條款；CRDO 教訓：三次用 \`Edit\` 局部補標點/符號違反本條，正確做法是
整檔重寫，見下方「組裝與驗證」）；禁先寫短稿再加字湊篇幅。prose 檔內容即該段完整外層元素
（\`<section id="s5">…</section>\`）。

### 注入標記（精確比對，不得改寫標記文字，各自獨立一行，不得被散文包住）
\`<!-- E2 -->\`§2.B 三假設表／\`<!-- E11 -->\`情境樹／\`<!-- E12 -->\`觸發器監測表／\`<!-- AUDIT -->\`
決策矩陣稽核表（audit_rows 非空才有）／\`<!-- APPA_TABLE -->\`附錄 A 單列表。E3/E5-E10 七表由
\`render_dd.py --assemble\` 依 render-rules §2 對映注入，散文不重寫表格內容。

### 呈現硬規則
1. **不得新增判斷物沒有的數字**——正文承重數字須能在 ${JUDGMENT} 找到（原樣或四捨五入到小數點後 1
   位內）。\`validate_prose.py\` 會擋。
2. **白話開場**（QC-54）：§1 結論與 §13 開場須 2-4 句白話敘事（這是什麼生意／為何這個裁決／什麼
   會改變它），不得以矩陣機器語言（row 編號、Hard/Soft Veto 逐項列舉）開場；逐 row 檢核收進
   <details>，正文只留「命中哪條路徑＋一句白話理由」。
3. **比較符跳脫**：< > 一律用 &lt; &gt;。
4. **不渲染流程劇場**：不寫「自查發現 X／我跑了驗證」的過程對帳，只渲染結論。
5. **bytes 預算**：以 \`dd_prose_budget.py\` 表為準（Part I ≥60%、§3-§7 商業本質五章為重心、
   §11-§14 決策層合計 ≤12KB 只渲染結論物）。
6. 機械表若觸發 leaks／標點檢查，**不得自行改表格檔**——回報 orchestrator 由 (b1) 判斷側修正後重產表。

### 動筆前速查表（≤15 行，不必外部讀檔；權威仍在 \`dd_sections.py\`／\`validate_prose.py\` 原始碼）
**洩漏詞（動筆時不要寫，事後 \`leaks\` 才抓就多一輪）**：\`row ?\\d\`／Hard Veto／Soft Veto／
\`signal ?[ABCX]\`／估值燈／\`val ?[🟢🟡🟠🔴]\`／\`MA ?[✅❌🟢🟡🟠]\`／Pure MA／\`盲點 ?\\d\`／PREREG／
dd-meta／runway_post_y5／capalloc／\`QC-\\d\`／archetype／metadata／硬接線／接線[:：]／Guardrail／
校驗紀錄／判定規則／gate／F2／row 8a→改寫「爆發候選路徑」／row 8b→「循環衛星進場路徑」。
**符號慣例（\`validate_prose.py\` 的正規化規則，逐字對齊白名單就不用記細節）**：
①負數一律在數字前直接放 \`−\`（或 \`-\`）——**不要**只用「年減／下滑／衰退」等中文詞代替符號，
沒有符號的正數會被判定方向錯誤；②百分比一律 \`%\` 緊接數字，不留空格；③金額 \`$\` 緊接數字；
④千分位逗號、全形數字/％/．都可以但不強制，兩種寫法驗證器都認；⑤**不要自己心算生出白名單裡
沒有的衍生數字**（如兩個既有數字的差值百分比）——那不是符號問題，是新數字，一律 FAIL。

### 組裝與驗證（一次複合 Bash，只呼叫 \`dd_gates.sh\`）
bash scripts/dd_gates.sh {T} {D} {OUT_HTML}

\`dd_gates.sh\` 依序跑 render_dd 組裝 → 六支驗證（validate_prose／dd_sections bytes／dd_sections
leaks／qc／validate_dd_meta／verify_dd_math），彙總輸出、任一真正擋下的閘 exit 1（bytes 與
dd_meta 維持既有 WARN／\`--report\`診斷慣例，不因合成腳本改變各閘既有 pass/warn/fail 語意）。
**只准呼叫這一支**，不要拆開個別跑（CRDO 教訓：拆開跑導致漏掉幾支閘、驗證輪次吃到 3 輪）。
未過 → **只重寫命中的那一段 \`prose/{sid}.html\`（整檔 \`Write\`，非 \`Edit\`），每段最多重寫一次**；
同一段連續兩次仍 FAIL 才回報 orchestrator，不動 judgment.json、不動其他段檔。**驗證輪次 ≤2**
（第 1 輪找出 FAIL 段、第 2 輪確認全過；仍不過才回報，不第 3 輪）。

## 交稿前自查（只做 ⑧＋QC-54，判斷層自查已在 (b1) 做過，不重複）
⑧ **散文一致性**——散文結論有沒有與 \`judgment.json\` 矛盾？有沒有出現判斷物裡不存在的數字
   （\`validate_prose.py\` 之外的語意層檢查，例如把區間講成單點、把「約」講成精確值）？
**QC-54 白話開場**——§1／§13 開場是否通過「唸給非分析師朋友聽，聽得懂為什麼」的測試，而非矩陣機器語言？

🔴 先重寫該段 prose 檔一次（整檔 Write）再重跑對應驗證，才交稿；連續兩次仍不過照實回報。

## 禁（token 紀律）
- WebSearch／WebFetch、Read 任何 \`docs/dd/\`、重讀自己寫過的 prose/tables 檔
- 每檔一次 \`Write\`；**prose 目錄任何 \`Edit\` 一律視為無效輸出**（機制上不擋——\`dd_gates.sh\` 不驗
  寫入方式，靠這條硬規則自律；發現自己剛用了 \`Edit\` 補字，立刻整檔 \`Write\` 重寫該段蓋過去）
- 拆開個別呼叫 \`dd_gates.sh\` 內的六支腳本（那是 orchestrator／除錯用，(b2) 只准呼叫 \`dd_gates.sh\`）
- 改 \`judgment.json\` 任何欄位（發現判斷有問題只能回報 orchestrator，不得自行修改判斷）

## 最終回報（≤200 字）
①各段 bytes 與 \`dd_sections.py bytes\` 表原文②\`dd_gates.sh\` 輸出摘要（七步任一 FAIL 標明）
③**重寫段數**（列出整檔重寫過的 sid，全部一次過寫 0）④自查⑧與 QC-54 的 🟢/🟡/🔴 與一句依據
（🔴 須註明已如何修正）。
`
})
```

**機械輪次批次化**（逐字，同 (b1)）：
> ①定位先於動手——改檔前一輪複合 grep 一次取齊行號，禁止交錯進行。②同檔機械性修改≥5 處禁止逐個修補，一次讀相關區段想清楚全部改點後單次重寫或單條 Bash 完成。③Bash 驗證性查詢併成單條複合指令，驗證輪次 ≤3 輪。

---

## (c) 事後抽查（**不在流程內**，不影響上站）

前三份 v16.2 DD 上站後，orchestrator 另 spawn 一次冷讀抽查（模型與 (b1) 判斷 agent 不同；判斷層為
Fable 時用 opus）。輸入＝`judgment.json`＋`evidence.json`＋`transcript_digest.json`（SNOW dry-run
教訓：冷讀者若只拿證據包沒拿逐字稿/摘要，會把 writer 親讀逐字稿得到的正確判斷誤判為無據，見設計稿
§14）＋`dd_sections.py text` 全文。任務只有一件：**依 (b1) 交稿前自查表的 ①-⑦ 逐條複核，計數判斷級
🔴，不提修法、不修補、不重跑任何腳本。**
輸出存 `notes/site-internal/dd/_audit_{T}_{D}.md`，檔頭一行 `## AUDIT: 判斷級🔴 = N`，其後逐軸一句。
抽查結果只餵設計稿 §13 的退場訊號：**三份合計判斷級 🔴 = 0 → 永久拿掉本抽查；出現 1 例 → 把判斷層
驗收放回流程內（恢復流程內 critic gate）。** 抽查在報告已上站後才跑，永不阻斷發布。
