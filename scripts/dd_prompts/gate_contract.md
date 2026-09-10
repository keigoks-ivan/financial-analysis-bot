# gate_contract.md｜v17 判斷層閘（gate）checklist 條文權威（2026-09-10 WP-A）

> **取代對象**：`.claude/skills/stock-analyst/references/critic-gates.md`。critic-gates.md 是 v15.2
> 「寫稿後 critic」（QC-41／QC-48／QC-50／QC-51）的協議全文，要求讀 `dd_sections.py text` 全文、
> WebSearch 10–14 輪查證、輸出 `## FINDINGS` 表格——這是**寫完 HTML 散文後**對已成稿報告的冷讀，
> 與 v17 閘（判斷物定案前、**只審 `judgment.json` 一份物件**、禁 WebSearch、禁讀 HTML、輸出固定
> `## AUDIT: 判斷級🔴 = N` 表格）是兩種不同流程階段的兩份不同協議。v17 三步制裡 gate 之後還有一
> 個獨立的散文層（prose，`prose.md.tmpl`），`--full` 模式下散文寫完仍可能觸發 QC-41 等舊 critic——
> **critic-gates.md 本身不廢棄、不刪除**，只是不再是「判斷層閘」的條文權威，改由本檔取代。
>
> **為什麼要換**：舊版 gate bundle 附 critic-gates.md 全文（64 行、13KB），但 gate.md.tmpl 的「禁」
> 一節明講「禁 WebSearch／WebFetch、禁開 bundle 以外任何檔」——附一份要求查證與讀 HTML 的協議給
> 一個被禁止查證與讀檔的 agent，是純粹的 token 浪費：閘從未真的照 critic-gates.md 的 checklist 或
> 輸出格式作答，一直是照 gate.md.tmpl 自己內嵌的 ①–⑧ 逐條複核清單作答。本檔把「為什麼要查這一
> 條」的條文權威留下來（多數改寫自 critic-gates.md QC-41 的對應 rationale），把「怎麼查證」「輸出
> 成什麼格式」兩件事整個拿掉——那兩件事 gate.md.tmpl 自己已經講清楚，不需要第二份文件重複。

## checklist 條目 → gate_view／judgment 欄位對照表（硬條件：每條都要能在下面兩處找到資料）

| # | 軸 | gate_view 欄位（`dd_bundle.py cmd_gate` 機械抽出） | judgment.json 欄位 |
|---|---|---|---|
| ① | 競爭惡化 | (a)+(b) findings 表（`axis` ∈ `competitive_share_entrants`／`customer_second_source`／`customer_concentration_credit` 的列） | `moat.threats`／`moat.competitors`／`contradictions[]`／`decision_inputs.bear` |
| ② | 供需 durability | (a)+(b) findings 表（`axis=supply_demand_durability`） | `moat.roic_durability`／`decision_inputs.cycle_position`／`decision_inputs.cycle_verdict`／`premortem` |
| ③ | 其他結構變數 | (c) coverage 逐軸總覽（`regulatory_antitrust`／`reg_tariff_export`／`geo_supply_chain`／`end_markets`／`substitute_technology`／`channel_business_model_shift`／`capital_markets_pricing`）＋ (a)+(b) 表中對應列 | `contradictions[]`／`premortem.blind_spots`／`triggers[]` |
| ④ | priced-in | (d) numbers 摘要（`valuation_current`／`latest_quarter_kpis[].vs_consensus`） | `valuation`／`decision_inputs.valuation_dependent`／`decision_inputs.market_wrong_reason_given` |
| ⑤ | 覆蓋面掃描 | (c) coverage 逐軸總覽＋ status=none／not_applicable 的查詢詞明細 | （逐軸核對 `contradictions`／`premortem`／`triggers` 是否接住，同 ①③） |
| ⑥ | 量化模組完整性抽查 | (e) `scenario_meta.json` sidecar（`scenario_tree.eps.{bull,base,bear}`／`p_bull_pct`／`p_bear_pct`／`asym_ratio`／`ev5y_pct`／`irr_base_pct`） | `moat.roic_durability.{reinvest_rate,roiic,endo_ceiling,formula_note}`／`valuation`（共識 EPS CAGR）／`decision_inputs.{irr_base_pct,ev5y_pct,asym_ratio}`／`scenario_ref` |
| ⑦ | 數字新鮮度 | (d) numbers 摘要（`latest_quarter_kpis[].as_of`／`price_as_of`／`earnings_recency`） | 判斷物引用的每個營運數字（`oneliner`／`reasoning`／`appendix_a` 等）＋ `decision_inputs.consensus_rev_3m_pct` |
| ⑧ | QC-49 前份漂移歸因 | (f) `prior_dd`（`drift_watch` 20 欄／`prior_meta`／`H`／`R`／`triggers`） | `contradictions[]`（逐欄變動是否有獨立條目歸因）｜前份不存在時填 🟢 |

> (a)–(g) 對照 `dd_bundle.py::_gate_view_section` 的小節標籤；`###` 標題內就標了 `(a)` `(b)` … 字樣，
> 對照時直接找 `### (X)` 開頭的段落即可，不需要另外查行號。

## 各軸條文權威（條件、口徑、rationale——怎麼查證與輸出格式見 gate.md.tmpl 本體，不重複）

**① 競爭惡化**：份額流失／新進入者／客戶 second-source／大客戶轉單。gate_view (a)+(b) 表已把
`competitive_share_entrants`／`customer_second_source`／`customer_concentration_credit` 三軸裡「負向、
或被判斷引用、或 affects 命中 decision_inputs/thesis/moat_trend」的 finding 全部列出——逐列核對
`被引用` 欄是 N 卻是負向的，就是判斷漏接的候選。

**② 供需 durability**：緊缺或過剩是結構還是週期，供給可逆性是否寫進 bear 機率。gate_view (a)+(b)
表 `axis=supply_demand_durability` 的負向列若 `被引用=N` 且 `evidence_dismissed=N`，需在
`premortem`／`decision_inputs.bear` 找對應處理；找不到即 🔴。

**③ 其他結構變數**（開放軸）：法規／政策／關稅／反壟斷／補貼、通路重構、商業模式轉移、替代技術、
客戶結構轉移。這是 critic-gates.md QC-41 保留下來語意最接近原樣的一條——**重點找 gate_view (c)
coverage 總覽裡「有 findings 卻沒人接住」的軸**，不是重新去查有沒有漏掉的產業變化（閘禁搜尋，那是
Stage 0 evidence 收集的職責，不是閘的職責）。

**④ priced-in**：共識與賣方目標價 vs 現價，裁決是否只是把市場已知的事再說一次。看
`decision_inputs.market_wrong_reason_given` 是否有具體內容（非空泛套話），對照 gate_view (d)
`latest_quarter_kpis[].vs_consensus` 與 `valuation_current` 判斷判斷物有沒有正面處理「這件事場上是
否已經知道」。

**⑤ 覆蓋面掃描（強制）**：gate_view (c) 表逐軸點名 `status="none"`／`"not_applicable"` 的每一軸——
理由站得住嗎？`n_queries` 是否 <2 條或（看下方查詢詞明細）不相關？**缺軸本身即 🔴，不需先證明結論
錯**——這是 critic-gates.md QC-41 ⑤ 原文的核心主張，v17 版唯一差異是查詢詞明細已經機械列在 gate_view
裡，閘不必自己去猜「查了什麼」。

**⑥ 量化模組完整性抽查（強制）**：
- (i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」
  無算式＝🔴）；`.endo_ceiling` 是否與 `valuation` 隱含的共識 EPS CAGR 交叉檢查（天花板 < CAGR
  ＝ sanity 失敗，須在 `reasoning` 處理，沒處理＝🔴）。
- (ii) gate_view (e) `scenario_meta.scenario_tree.eps.{bull,base,bear}` 是否有實質價差（Bull EPS
  幾乎等於 Base、幾乎全靠 `pe.bull` 撐估值＝退化，🔴）。
- (iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 與 gate_view (e) `scenario_meta` 對應
  欄位是否一致（不吻合＝🔴；`decision_inputs` 三欄若透過 `evidence_dismissed` 明確聲明「腳本回填、
  不手填以免編造」且 gate_view (e) 確有對應腳本值，屬合規處理方式，不算 🔴）。

**⑦ 數字新鮮度**：判斷物引用的每一個營運指標，是否都不比 gate_view (d)
`numbers.latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct`
若標示或依附 `stale=true` 的來源，確認判斷物沒有把它當成唯一依據；引用 digest 內容（gate_view (g)）
的欄位要標「來源：摘要」。

**⑧ QC-49 前份漂移歸因**：gate_view (f) `prior_dd.prior_meta` 存在時，`drift_watch` 20 欄中有變動的
每一欄是否都在 `contradictions[]` 有帶對應歸因的獨立條目、且有三元排序主因；漏欄或無歸因＝🔴；
**前份該欄本身為空或缺欄（前一版格式沒有）者不計**，只給 🟡 提醒或 🟢。gate_view (f) 為空物件或
`status` 非 `"ok"` 時（無前份）填 🟢 並註「無前份」。

## 🔴／🟡／🟢 口徑（與 gate.md.tmpl 本體「## 🔴 的口徑」一節一字不改，此處僅重申不得脫鉤）

判斷級 🔴 限三種形狀：①證據包已有而判斷未接；②算術或機率防線失守；③裁決與自身輸入矛盾。
**資料級不算 🔴**（evidence/digest 本身缺料、來源不夠新、某軸查不到）——那是 Stage 0 的問題，最多
給 🟡 並在附註點名。這條口徑定義權威在 `gate.md.tmpl` 本體，本檔不重複展開，只在此處提醒：checklist
①-⑧ 每一條答案都要先套這個口徑再決定燈號，不是「有發現就是 🔴」。
