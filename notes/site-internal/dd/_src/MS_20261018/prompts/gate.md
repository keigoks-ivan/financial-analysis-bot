你是 DD 管線 v20 的判斷層閘（gate），標的 MS（20261018）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

## 任務

依 bundle 內 `gate_card.md` 的 ①–⑧ checklist 逐條複核 `judgment.json`，只揪判斷級的錯，不判斷寫得好不好。判斷級 🔴 限三形狀：①證據包已有而判斷未接；②算術或機率防線失守；③裁決與自身輸入矛盾。資料級問題（facts.json 本身缺料、來源不夠新、某軸查不到）不算 🔴，最多 🟡；無實質問題給 🟢。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：`gate_card.md`（①–⑧ checklist 全文與 🔴／🟡／🟢 口徑）、被引用事實與負向條目子集（核對 `fact_refs` 用）、`scenario_meta.json`（情境樹權威值，對帳 `decision_inputs.irr_base_pct`／`ev5y_pct` 用）、`judgment.json` 全文（被審對象，原樣）。

## 禁

- 禁 WebSearch／WebFetch、禁開 bundle 以外任何檔（包含 `docs/dd/`、`.dd_build/` 下的其他產物）。
- 禁跑任何腳本（`validate_judgment.py`／`dd_decision.py`／`dd_scenario.py` 已在判斷端跑過，機械層不歸你）。
- 禁提整段改寫判斷、禁自己動手修補 `judgment.json`——你只出稽核，修補是另一支流程的事。
- 證據包裡沒有的東西不得臆測補白，只講證據包內找得到依據的話。


===== BUNDLE =====

## ① gate_card.md（判斷層閘卡）

<!-- source: scripts/dd_prompts/gate_contract.md sha256:90928128665c694a; .claude/skills/stock-analyst/references/critic-gates.md sha256:8dff4ac45280acfd git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->

你是 DD 管線 v20 的判斷層閘（gate），sonnet，單輪、無工具。你未參與寫判斷，這是一次跨模型冷讀。
輸入：`judgment.json`（待審判斷物）＋ `facts.json`（事實表，每軸 finding 帶 source／as_of／direction）。
任務只有一件：依下列 checklist 逐條複核 `judgment.json`，只揪**判斷級**的錯，不判斷寫得好不好。
判斷級 🔴 限三形狀：①證據包已有而判斷未接；②算術或機率防線失守；③裁決與自身輸入矛盾。資料級（facts.json 本身缺料、來源不夠新、某軸查不到）不算 🔴，最多 🟡。
禁 WebSearch／WebFetch、禁讀輸入以外任何檔、禁改 `judgment.json`，只出稽核清單。

## checklist（①–⑧ 全出，不得跳號、不得「同上」帶過）

① 競爭惡化——份額流失／新進入者／客戶 second-source／大客戶轉單。查 facts.json 對應軸（competitive_share_entrants／customer_second_source／customer_concentration_credit）裡負向、或應被引用的 finding，核對 judgment.json 的 `moat.threats`／`moat.competitors`／`contradictions[]`／`decision_inputs.bear` 是否接住；被引用=N 卻是負向的 finding 即漏接。[gate_contract §①]

② 供需 durability——緊缺或過剩是結構還是週期，供給可逆性是否寫進 bear 機率。facts.json 的 supply_demand_durability 軸負向 finding，若未被引用且未列 `evidence_dismissed`，須在 `premortem`／`decision_inputs.bear` 找到對應處理，找不到即 🔴。[gate_contract §②]

③ 其他結構變數（開放軸）——法規／政策／關稅／反壟斷／補貼、通路重構、商業模式轉移、替代技術、客戶結構轉移。找 facts.json 覆蓋總覽裡「有 finding 卻沒人接住」的軸，對照 `contradictions[]`／`premortem.blind_spots`／`triggers[]`；閘禁搜尋，不重新查有沒有漏掉的產業變化。[gate_contract §③]

④ priced-in——共識與賣方目標價 vs 現價，裁決是否只是把市場已知的事再說一次。看 `decision_inputs.market_wrong_reason_given` 是否有具體內容（非空泛套話），對照 facts.json 的 `latest_quarter_kpis[].vs_consensus` 與 `valuation_current`。判斷寫「不追／等價格」而裁決是進場、`decision_inputs.wait_for_price` 卻沒填 true ＝ 矛盾；填了 true 時裁決落觀望是規則結果，不算矛盾，只看 `wait_for_price_condition` 是否具體可驗。[gate_contract §④]

⑤ 覆蓋面掃描（強制）——facts.json 逐軸點名 status="none"／"not_applicable" 的每一軸：理由站得住嗎？查詢是否切題且足以支撐該軸結論（不以查詢次數計）？**缺軸本身即 🔴，不需先證明結論錯**。[gate_contract §⑤]

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤，缺軸本身即 🔴。
(b) 量化模組完整性抽查：ROIC×再投資率真算與否、內生天花板對帳共識 CAGR、情境樹 Bull/Base/Bear EPS 價差是否實質、IRR 內部對帳，做法同 checklist ⑥。
(c) 數字可回溯：判斷引用的歷史數字逐一核對 facts.json 原文的期間與單位；反證條目要查採納理由與後果是否成立，不能只因編號存在就算過。[gate.md.tmpl 2026-09-11 註腳]

## 🔴／🟡／🟢 口徑

判斷級 🔴 限下列三種形狀：

1. **證據包已有而判斷未接**——證據包內存在的 finding／數字，判斷物完全沒接進 `contradictions`／`moat.threats`／`premortem`／`triggers`／`thesis.R`，也沒寫進 `evidence_dismissed[]`；
2. **算術或機率防線失守**——推導不可複算、內部恆等式不對帳、情境樹退化、機率與其自身依據矛盾；
3. **裁決與自身輸入矛盾**——`decision_inputs`／`scenario_meta`／`decision_out` 三者互斥，或裁決與判斷物自己寫下的理由相反。

**資料級不算 🔴**（證據包本身缺料、來源不夠新、某軸查不到）——那是 Stage 0 的問題，最多給 🟡 並在附註點名。無實質問題給 🟢；有實質但不改裁決方向的給 🟡。

## 輸出格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```


---

## ②b 被引用的事實與負向條目（v19；閘要查數字時不必猜）

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_gaap`（q1_business）｜淨營收（GAAP）＝20338 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi1_gaap`（q1_business）｜稅前利益（GAAP）＝6478 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi2_non_gaap`（q1_business）｜稅前利益率（營業利益率對應，銀行無 non-GAAP 營業利益）＝31.9 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi3`（q1_business）｜費用效率比＝67 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi5_rotce`（q1_business）｜ROTCE＝22.6 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi6`（q1_business）｜薪酬與福利費用＝7997 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi7`（q1_business）｜財富管理淨營收＝9065 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi8`（q1_business）｜財富管理淨新增資產＝232.4 十億美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi9`（q1_business）｜機構證券淨營收＝10029 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi10`（q1_business）｜投資管理淨營收＝1459 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_kpi12`（q1_business）｜股票買回＝1540 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[12]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝12.75 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1570.57 m shares｜期間與口徑：2026-10-18／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_ms_fcf_margin_pct`（q2_moat）｜MS FCF 利潤率＝-25.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gs_fcf_margin_pct`（q2_moat）｜GS FCF 利潤率＝-62.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jpm_fcf_margin_pct`（q2_moat）｜JPM FCF 利潤率＝-83.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JPM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝13.57 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝14.56 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_kpi4_eps`（q4_capital）｜稀釋後 EPS＝3.03 美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝82176.77 USD m｜期間與口徑：2026-10-18／yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝86675.37 USD m｜期間與口徑：2026-10-18／yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi11_cet1`（q1_business）｜標準法 CET1 比率＝14.9 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm（numbers.latest_quarter_kpis.items[11]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-14））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.298 %｜期間與口徑：2026-10-18／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-18）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝152017.15 USD m｜期間與口徑：2026-10-18／市值 283597.18 ＋ 淨負債 -131580.03｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝14.9 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 12.75，分子＝快照價 190.02｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝180.57 USD｜期間與口徑：2026-10-16（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝14.32 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝34.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝34.1 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.59 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 12.19 → 12.75（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_rsi14`（q5_valuation）｜RSI(14)＝25.42｜期間與口徑：2026-10-16（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-16（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-3.33 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-16（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Goldman 2026 上半年投銀費用年增 52% 至 62.4 億美元（股票承銷 +90%），為同業對手動能數據；未找到 MS 同期份額數字
  - 來源：Zacks via yourwyominglink: Goldman's IB fees jump 52% in 1H26（as_of 2026-07-20）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：MS 10-Q（2026-06-30）列示私人反壟斷訴訟：VRDO 集體訴訟（最高法院 2026-04-20 駁回調卷，2026-07-13 被告提出簡易判決動議）與利率交換訴訟（2026-03-12 被告提出簡易判決動議）仍在進行；搜尋未見 2026 年新的 DOJ／FTC 反壟斷調查
  - 來源：Morgan Stanley Form 10-Q for period ended 2026-06-30 (SEC)（as_of 2026-06-30）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：第三方彙整的 MS 風險揭露（標示 2026）：機構證券部門業績受全球貿易政策、關稅、保護主義、貿易制裁或投資限制變動影響；屬常設風險因子，無量化關稅衝擊。
  - 來源：policyrisk.com MS company page（SEC 揭露彙整）（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2025 年 4 月關稅宣布後 MS 股價單日跌 9.5%；評論稱客戶可能延後大型併購。
  - 來源：Motley Fool: why morgan stanley stock sank today（as_of 2025-04-03）｜affects：decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：現金掃款（cash sweep）客戶集體訴訟已合併為 SDNY 單一案件 Estate of Sherlip v. Morgan Stanley；2025-08-15 提出修正訴狀，2025-09-12 MSSB 聲請駁回。性質為契約／受託／法定請求，非證券詐欺。
  - 來源：Morgan Stanley Form 10-Q (2025-09-30)（as_of 2025-09-12）｜affects：decision_inputs.bear、triggers
- `financial_capital_credit_cycle#0`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：MS 3Q26 全公司信用損失撥備 1.48 億美元，去年同期為零；9 個月累計 3.44 億 vs 去年同期 3.31 億；2Q26 為 9,800 萬。
  - 來源：Morgan Stanley 3Q26 Quarterly Financial Supplement / 3Q26 shareholder letter (morganstanley.com IR)（as_of 2026-10-14）｜affects：decision_inputs.bear、thesis.R
- `financial_capital_credit_cycle#1`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：3Q26 撥備高於市場預期（共識約 8,400 萬）；季內有 1.05 億美元沖銷，對應特定企業與商用不動產放款，且先前季度已大部分提列。
  - 來源：Private Banker International 摘要；roic.ai「Morgan Stanley Q3 earnings beat estimates but trading and credit signals diverge」（as_of 2026-10-14）｜affects：decision_inputs.bear、thesis.R
- `financial_capital_credit_cycle#3`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：產業面：Fitch 報告私募信貸違約率創 6% 紀錄（至 2Q26）；Morningstar DBRS 12 個月借款人違約率 4%（前年 2.8%）、1Q26 降級／升級比 3.3 倍、2026 展望為負面；美國銀行對私募信貸提供者放款近 3,000 億美元（Moody's，至 2025 年 6 月）。
  - 來源：alternativecreditinvestor.com／Morningstar DBRS／Reuters 引述 Moody's 彙整（as_of 2026-02-17）｜affects：decision_inputs.bear、thesis.R
- `financial_regulatory_capital_rules#2`（financial_regulatory_capital_rules｜方向 -｜狀態 ok）：2026-06-18 參議院民主黨議員要求 Bowman、Gould、Hill 撤回三項資本提案，主張重新提出更嚴規則；屬提案翻轉風險。
  - 來源：Senate Banking Committee, letter to financial regulators re Basel III proposal（as_of 2026-06-18）｜affects：decision_inputs.bear、thesis.R、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：現金掃款客戶集體訴訟合併為 SDNY Estate of Sherlip v. Morgan Stanley；2025-08-15 修正訴狀，2025-09-12 聲請駁回；NJ 案合併為 In re E*TRADE Cash Sweep Litigation。非證券詐欺。
  - 來源：Morgan Stanley Form 10-Q (2025-09-30)（as_of 2025-09-12）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MS_20261018/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":320.0,"bear_5y_price":146.3,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":31.0,"ev5y_pct":27.6,"irr_base_pct":5.6,"asym_ratio":3.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":12.75,"pe":14.16,"basis":"FY2026E 共識 EPS（Koyfin 2026-10-08）對判斷日收盤 180.57；終端倍數乘 FY2031E EPS，口徑同為一年期盈餘"},"eps":{"bull":[14.4,15.9,17.2,18.6,20.0],"base":[13.5,14.4,15.0,15.9,16.9],"bear":[11.3,10.5,11.4,12.4,13.3]},"pe":{"bull":16,"base":14,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.298,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MS_Q2_2026_Earnings_Call_20260715.md
- 2026-07-15｜Sharon Yeshaya (CFO)｜guidance：CFO 對第三季財富管理 NII 的指引：小幅季增。（原話："we expect a modest sequential increase in NII."）
- 2026-07-15｜Sharon Yeshaya (CFO)｜guidance：CFO 重申全年稅率區間 22%–23%。（原話："expect our annual tax rate to be between 22% and"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜guidance：CFO 稱投行展望正面、pipeline 健康。（原話："The Investment Banking outlook is constructive and"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：財富管理稅前利潤率 30.5%。（原話："The pretax margin was 30.5%, a reflection of the scale"）
- 2026-07-15｜Ted Pick (CEO)｜margin：CEO 說 30% 是已達成多次的基準，但不是求解目標。（原話："30% is a benchmark now we've hit a number of times"）
- 2026-07-15｜Ted Pick (CEO)｜margin：CEO 稱若門檻不足、有需要才會調高，留待年底處理。（原話："the margin hurdle is not enough, and we want to take it up"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：CFO 報上半年效率比 65%。（原話："efficiency ratio was 65%."）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：NII 優於預期，原因為掃入餘額與放款成長。（原話："NII outperformed on higher-than-expected sweep balances"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：其他收入虧損主因為待售企業貸款的評價損失（含避險）。（原話："mark-to-market losses on corporate loans held for sale"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：外匯波動度處於歷史低點附近，外匯收入下滑。（原話："where volatility traded near historic lows."）
- 2026-07-15｜Ted Pick (CEO)｜commitment：CEO 說年中不調整策略目標。（原話："not moving the targets during the course of the year,"）
- 2026-07-15｜Ted Pick (CEO)｜commitment：CEO 重申「更高的高點與更高的低點」。（原話："delivering higher highs and importantly, higher lows"）
- 2026-07-15｜Ted Pick (CEO)｜commitment：CEO 稱下一塊錢資產優先投入整合式公司。（原話："the next dollar of assets should go straight into feeding"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜capital_allocation：CET1 比率季末 14.8%。（原話："our standardized CET1 ratio ended the quarter at 14.8%."）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：宣布季股息調升 15% 至 1.15 美元。（原話："a 15% increase in our quarterly dividend to $1.15 per share."）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：CEO 稱超額 CET1 約 300–350 bps。（原話："300 to 350 basis points of excess CET1 capital depending"）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：CEO 稱對資本運用「相當嚴格」，不每季擠壓到極限。（原話："But we are quite ruthless about how we are playing this"）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：CEO 稱目前偏向有機成長而非併購。（原話："the bias continues to be to go organic."）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：併購門檻：策略合理性與文化契合。（原話："cultural fit continue to be threshold criteria"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜customer：CFO 稱職場通路涵蓋前 100 大獨角獸約 70%。（原話："we have about 70% of the top 100"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜customer：IPO 的股票計畫資金流占本季淨新增資產略過半。（原話："Stock plan IPO flows represented just over half of"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜customer：客戶關係達 2,000 萬。（原話："We're currently at 20 million relationships."）
- 2026-07-15｜Sharon Yeshaya (CFO)｜competition：回應小型 RIA 低價競爭：CFO 稱小機構無此廣度。（原話："institutions, they will not have that type of breadth."）
- 2026-07-15｜Ted Pick (CEO)｜competition：CEO 稱融資提供者有一些定價槓桿，但生態系內資本充裕者多。（原話："I would say there is some pricing leverage"）
- 2026-07-15｜Ted Pick (CEO)｜competition：CEO 強調亞洲業務，與 MUFG 合作。（原話："But we're also an Asia house, very much an Asia house."）
- 2026-07-15｜Sharon Yeshaya (CFO)｜product：Parametric 管理資產規模。（原話："$760 billion in AUM today."）
- 2026-07-15｜Ted Pick (CEO)｜risk：CEO 估 AI 資本支出進度約 10%–15%。（原話："around 10% to 15% of the way through the investment cycle."）
- 2026-07-15｜Ted Pick (CEO)｜risk：CEO 承認可能出現科技與電力瓶頸。（原話："there will be technology and power bottlenecks"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜risk：CEO 稱 sponsor 週期尚未完整出現。（原話："we have not yet seen that complete"）
- 2026-07-15｜Ted Pick (CEO)｜risk：CEO 描述經濟背景。（原話："the economy is in great shape."）

### 問答異常語氣（迴避／改口／保留）
- MS_Q2_2026_Earnings_Call_20260715.md｜問：Poonawala：財富管理稅前利潤率是否會走向 30% 中段？｜答法：CEO 未給方向或數字，回到不在年中調整目標、30% 非求解目標，留待年底。
- MS_Q2_2026_Earnings_Call_20260715.md｜問：Mayo：以 10 兆美元 AI 資本支出為例，MS 在募資中占幾成？｜答法：CEO 明說 I wouldn't attach a percentage to it，只稱 meaningful。
- MS_Q2_2026_Earnings_Call_20260715.md｜問：Schorr：為何維持高資本而不更積極運用？｜答法：CEO 未給回購節奏或數字，改談客戶需求、緩衝價值與有機優先。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 3 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 1 | 3 |
| end_markets | found | 5 | 3 |
| substitute_technology | none | 0 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 2 | 5 |
| financial_capital_credit_cycle | found | 4 | 3 |
| financial_regulatory_capital_rules | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Morgan Stanley largest client concentration in-house OR insourcing OR second source 2026；Morgan Stanley largest customer concentration second source OR in-house 2026
- **substitute_technology**（none）：Morgan Stanley AI disruption threat wealth management investment banking 2026；Morgan Stanley stablecoin tokenization crypto trading threat to brokerage 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260716","verdict":"觀望","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"WM 年金流第二曲線兌現（客戶資產 $10T→$12T+、pre-tax margin 守 ~30%）","columns":{"2Y 驗證":"FY26–27 WM rev YoY ≥ 8%，NNA ≥ $50B/季","5Y 驗證":"FY30 WM+IM 客戶資產 ≥ $12T","10Y 驗證":"FY35 財管費收占 group rev > 55%","數字門檻":"NNA 維持 $200B+/年；WM margin ≥ 28%","來源":"Q2 26 法說 + 2Q26 ARS","漂移觸發（QC-35）":"連 4 季 NNA"}},{"id":"H2","text":"機構證券週期上行支撐 group ROTCE 高位（但本假設本質是週期性，非結構）","columns":{"2Y 驗證":"FY26 IS rev 維持 $40B+","5Y 驗證":"FY30 IS through-cycle ROE ≥ 14%","10Y 驗證":"2030+ IB fee pool 正成長","數字門檻":"IS 季 rev 不連 2 季 YoY","來源":"Q2 26 法說（IS $11.0B 紀錄）","漂移觸發（QC-35）":"連 2 季 IS rev TTM 偏離 ≥ 5% → 削弱（2Y 假設）"}},{"id":"H3","text":"估值：market 持續 capitalize peak-cycle ROTCE，P/TBV 守 3.5–4.4x（本假設是本裁決最脆弱環節）","columns":{"2Y 驗證":"P/TBV 2026 不破 3.2x","5Y 驗證":"5Y 末 P/TBV ~3.0–3.5x（視 through-cycle ROTCE）","10Y 驗證":"through-cycle ROTCE ≥ 18%","數字門檻":"正常化 ROTCE ≥ 18%","來源":"GuruFocus P/TBV + ROE-P/B regression","漂移觸發（QC-35）":"連 4 季 TTM ROTCE 偏離 ≥ 5% → 削弱（5Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"WM NNA 從 $148B 高位失速 → 財管年金曲線 thesis 受重創","columns":{"對應":"H1","時間尺度":"⚡ 短期（1–2 季）","監測":"季度 NNA 金額","警戒閾值":"連 2 季"}},{"id":"R2","text":"capital-markets 週期 2026H2–2027 反轉 → IS rev 失墜、blended ROTCE 從 27% 回落 → §12 核心矛盾兌現","columns":{"對應":"H2 / H3","時間尺度":"週期（2–5 季）","監測":"IS 季 rev YoY + P/TBV","警戒閾值":"IS 連 2 季 YoY"}},{"id":"R3","text":"AML 監管程序升級（FinCEN/OCC/SEC/FINRA 客戶審查 2021–2024 窗）→ consent order + 罰金 + 財管展業限制","columns":{"對應":"治理","時間尺度":"事件（不定）","監測":"docket 進展 / 8-K 揭露","警戒閾值":"升級為 consent order 或罰金 > $500M"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"P/TBV 回落至 ≤3.3x（≈$180，等 warranted 錨）或 through-cycle ROTCE 連 3 季 >20%（弱市確認結構性步階）或 SEC/FinCEN/OCC AML 程序結案","irr_base_pct":5.5,"ev5y_pct":21.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"核心","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.5,"ev5y_pct":21.0,"irr_base_pct":5.5,"max_dd_pct":-55.0,"bull_5y_price":389.0,"bear_5y_price":142.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"P/TBV 回落至 ≤3.3x（≈$180，等 warranted 錨）或 through-cycle ROTCE 連 3 季 >20%（弱市確認結構性步階）或 SEC/FinCEN/OCC AML 程序結案","price_at_dd":228.55,"archetype":"金融","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MS","date":"2026-10-18","schema":"v15.2","contract":"v19","company_name":"Morgan Stanley"},"oneliner":"財富管理的資產累積撐住報酬，但 2026 年盈餘含股票交易與 AI 融資的週期高點；股價跌到前瞻 14.2 倍只算合理，先不建倉，等 166 美元或第四季確認信用與淨新增資產再分批","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MS_20261018/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MS_20261018/scenario.json","answers":{"q1_business":{"verdict":"MS 賺兩種錢。一是財富管理按資產收費的年金型收入（第三季淨營收 90.65 億美元，約占 45%），二是機構證券靠市場活動量的交易與投行收入（100.29 億，約占 49%）。錢卡在兩個節點：客戶資產規模與市場交易量","reasoning":"分部：第三季淨營收 203.38 億美元，財富管理 90.65 億、機構證券 100.29 億、投資管理 14.59 億（三者相加略高於總數，差額為分部間沖銷）。最新一季獲利：稅前利益 64.78 億，稅前利益率 31.9%，效率比 67%，ROTCE 22.6%，連 5 季高於 20%。財富管理稅前利益 28 億，約占全公司稅前的 43%，稅前利益率 30.4%（本季法說財務長）。收入品質分兩層。財富管理的資產管理收入 55 億（年增 16%），是收費型資產 3.155 兆乘費率的年金收入；機構證券裡，股票交易 58 億（年增 41%）、投行 22 億（+2%）、固定收益約 20 億（−7%），隨市場量能起落。產業時鐘判為擴張期，依據是第三季全公司營收年增約 12%、投行管線被管理層形容為高檔，但 9 月起量能轉弱，晚期訊號已出現。供需持久性屬混合型：機構證券是週期性，會隨市場量能反轉；財富管理的資產累積屬結構性持久，執行長本季說收購 E*TRADE 後三年累積一兆美元淨新增資產，之後三年又一兆。議價權：上游是人才，本季薪酬福利 79.97 億，占淨營收約 39%，顧問與交易員拿走價值鏈的一大塊；下游客戶分散。單點依賴：FY2025 年報把集中風險定義為單一發行人、國家或產業的部位集中，沒有單一客戶營收占比揭露。最大的依賴是資本市場活動量，以及管理層自稱「雙倍加碼」的 AI 相關融資與 IPO 流量。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_non_gaap","f_kpi3","f_kpi5_rotce","f_kpi6","f_kpi7","f_kpi8","f_kpi9","f_kpi10"],"verdict_values":{"revenue_quality":"雙層：財富管理資產管理費約占該部門六成，屬年金型；機構證券約占全公司一半，隨市場量能波動，本季股票交易年增 41% 屬週期高檔","unit_econ_note":"財富管理資產管理收入年化約 220 億美元，除以收費型資產 3.155 兆，費率約 0.70%（用期末資產粗算，非平均資產）；部門稅前利益率 30.4%","archetype":{"primary":"金融","secondary":"品質複利成長","confidence":"高","fingerprint":"券商加財富管理平台，旗下有銀行子公司；報酬看 ROTCE 與 CET1，不看 FCF"},"industry":{"clock_phase":"II","sd_verdict_source":"混合：機構證券屬週期性、將隨市場量能反轉（9 月已轉弱）；財富管理資產累積屬結構性持久（六年兩兆淨新增資產，本季法說）","bargaining":{"up":"人才環節議價強，薪酬福利約占淨營收 39%","down":"客戶分散，年報未揭露單一客戶營收占比；議價集中在費率與掃款利率","geo":"全球布局，亞洲與日本（與 MUFG 合作）是管理層點名的優勢區"},"profit_pool_dir":"投行利潤池往大型整合行集中：前十大投行份額合計年增 3.4pp，MS 排第三，落後摩根大通與高盛","tam_table":{"expanded":false,"reason":"金融業跑道看客戶資產、放款與存款成長，不看 TAM 滲透率；美國財富管理總資產池事實表未涵蓋，滲透率無法計算"}}}},"q2_moat":{"verdict":"護城河 B 級，方向持平（→）。財富管理的規模漏斗是真的，但最近兩季的向上動能主要來自 IPO 事件，同業報酬差距也證不出正在擴大","reasoning":"機制是規模漏斗：E*TRADE 自主交易、職場股票計畫、顧問三層通路，把新財富從上游一路導進收費帳戶。機構端有股票業務 9 宮格（現貨、衍生品、主經紀乘三大地區）的規模效應。執行力給 8 分，理由是股票交易接近 2024 年的兩倍（分析師於本季法說提問所述，執行長未反駁），衍生品業務補齊，顧問留任率 99% 以上。定價力給 7 分，理由有三：另類產品有獨家條件，但掃款利差正被訴訟挑戰，投行份額動能又落後高盛。綜合 7.5 分，屬 B 級。方向從前份的 ↑ 改為 →。執行面在擴大，定價面持穩；但兩季紀錄級淨新增資產都有過半與 IPO 相關，有機加速還沒證實。高盛 2026 上半年投行費用年增 52%，MS 第三季投行只 +2% 且低於預期。同業 ROTCE 事實表未涵蓋，報酬差距的方向無法驗證。當期報酬：ROTCE 22.6%。稅前利益率 31.9% 乘資產周轉約 4.8%（年化營收約 814 億，除以總資產 1.7 兆），屬高利益率乘低周轉的象限，靠資本槓桿放大，所以要盯資本要求。再投資空間：內生成長約 7.5%，等於 ROTCE 22.6% 乘保留率約 33%。保留率的算法：股息 4.60 美元除以 FY2026 共識 EPS 12.75，股息發放率約 36%；年化回購約 62 億，除以 FY2026 共識淨利約 200 億（12.75 美元乘 15.71 億股），回購約占 31%；扣掉兩者剩約 33%。增量 ROTCE 需要有形普通股權益序列，事實表未涵蓋，以當期值代理，結果偏樂觀。同業對照表只有 FCF 利潤率，銀行的 FCF 由交易資產與放款變動主導，不能用來比較。","fact_refs":["f_kpi5_rotce","f_kpi2_non_gaap","f_kpi6","f_kpi8","f_kpi12","f_consensus_eps_fy1","f_shares_diluted_m","f_peer_ms_fcf_margin_pct","f_peer_gs_fcf_margin_pct","f_peer_jpm_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"財富管理三層漏斗（自主交易、職場股票計畫、顧問）把新財富導入收費帳戶，加上機構股票業務的全球規模；資產規模帶來另類產品通路與資料優勢","execution":8,"pricing":7,"combined":7.5,"score":7.5,"grade":"B","trend":"→","trend_evidence":"執行面擴大：六年累計逾 2 兆淨新增資產、顧問留任率 99% 以上。定價面持穩：掃款利差受訴訟挑戰，投行份額動能落後高盛。最近兩季淨新增資產皆過半與 IPO 相關，同業報酬差距事實表未涵蓋，向上方向證不出來","competitor_notes":[{"name":"JPM","strategy_note":"投行費用榜首（101 億美元），有綜合銀行的資產負債表與低成本存款，是投行與企業放款最強的對手"},{"name":"GS","strategy_note":"2026 上半年投行費用年增 52%、股票承銷 +90%，MS 第三季投行僅 +2%；投行份額動能目前領先 MS"},{"name":"BAC","strategy_note":"旗下 Merrill 是財富管理的正面對手，存款基礎厚；其淨新增資產事實表未涵蓋，份額無法比較"},{"name":"WFC","strategy_note":"財富管理有規模，但投行與交易業務小；FCF 利潤率對銀行不具可比性"}],"spread_notes":null,"peer_na_reason":"同業對照只有 FCF 利潤率，銀行的 FCF 由交易資產與放款變動主導，不具可比性；同業 ROTCE 與 P/TBV 事實表未涵蓋","threats":[{"level":"🟡","text":"高盛投行動能領先：上半年投行費用年增 52%，MS 第三季投行僅 +2% 且低於預期。屬點對點份額競爭，不扣分，但壓住投行定價力","p":0.35,"evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"掃款利差受法律壓力：紐約南區合併集體訴訟以契約與受託義務為由，主張掃款利率過低；若敗訴或和解，財富管理利差下修","p":0.25,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"level":"🟡","text":"AI 代理式理財與代幣化股票可能壓低顧問費率。管理層本季主張規模、獨家產品與資料會讓科技站在 MS 這邊；費率趨勢事實表未涵蓋","p":0.15,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是家戶（決策時有顧問參與），三者一致；財富傳承、退休與稅務規劃屬於需要，不是想要。代理讀數：客戶關係近 2,100 萬，六年累計淨新增資產逾 2 兆美元（本季法說）"},{"item":"決策層級","level":"🟡","text":"替代性要在家戶與單一顧問之間衡量。顧問留任率 99% 以上（執行長本季說法），但 IPO 相關資產解禁後可被賣出或移走；管理層只說保留率穩定，未給數字。漲價後的流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"MS 是資產管理業最大的經銷商，另類產品有獨家條件，在經銷環節有議價力；但人才環節拿走很大一份，本季薪酬福利約占淨營收 39%，顧問與交易員是最難取代的一環"},{"item":"社會容忍度","level":"🟡","text":"掃款利率已引發集體訴訟，客戶現金的利差有法律與社會上限。資本規則屬監管授權：2026-03 提案放寬，但參議院民主黨議員 2026-06 要求撤回，政策可以翻轉"}],"roiic":"事實表未涵蓋有形普通股權益序列，無法算增量報酬；以當期 ROTCE 22.6% 代理，結果偏樂觀","reinvest_rate":0.33,"endo_ceiling":7.5,"formula_note":"內生成長＝ROTCE 22.6%×保留率約 33%。保留率＝1−股息發放率約 36%（4.60÷12.75）−回購占淨利約 31%（年化回購 61.6 億÷FY2026 共識淨利約 200 億）；季股息 1.15 美元見 2026-07-15 前一季法說"}}}},"q3_growth":{"verdict":"五年後跑道中等（🟡）。資產累積可以延續，但滲透率算不出來；共識三年 EPS 年化 12.6%，高於內生天花板 7.5%，差額來自 2026 年的週期性利潤率擴張","reasoning":"成長來源以量為主：客戶資產 10.5 兆、存款季增近 300 億、銀行放款季增 50 億。其次是價格，資產管理費隨市值上升。再加上回購減股。沒有併購，管理層 2026-07-15 表示偏向有機成長。共識三年 EPS：FY2025A 10.21 到 FY2028E 14.56，年化 12.6%（Koyfin 快照，分析師家數事實表未涵蓋）。內生天花板 7.5%，見護城河段。缺口約 5.1pp，歸因於兩項：FY2026 單年 EPS 年增 24.9% 的週期性利潤率擴張（股票交易 +41%、營業槓桿），以及淨回購。若只看 FY2026 到 FY2028，共識斜率 6.9%，落在天花板內。跑道：若剔除 IPO 後仍維持三年一兆的節奏，財富管理可再走十年以上；但美國財富管理總資產池事實表未涵蓋，滲透率無法計算，也沒有已證實的第二條曲線，所以給中等。衰退訊號亮一項：FY2022 到 FY2025 稀釋 EPS 年化 18.4%，營收年化 9.5%，差距 8.9pp。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi4_eps","f_kpi8","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量（客戶資產、存款與放款成長）為主，價（資產費隨市值）其次，再加回購減股每年約 2%；無併購","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段內生成長 7.5%（ROTCE 22.6%×保留率 33%），不另算","segments":[{"item":"財富管理","value":"第三季淨營收 90.65 億美元，稅前利益率 30.4%，淨新增資產 2,324 億（過半與 IPO 相關），收費型流入 805 億"},{"item":"機構證券","value":"第三季淨營收 100.29 億，年增 18%；股票 58 億（+41%）、投行 22 億（+2%）、固定收益約 20 億（−7%）"},{"item":"投資管理","value":"第三季淨營收 14.59 億，低於去年的 17 億，主因私募基金附帶權益回沖；長期淨流入 158 億"}],"decay_signals":[{"signal":"EPS CAGR 顯著高於營收 CAGR","lit":true,"note":"FY2022→FY2025 稀釋 EPS 年化 18.4%、營收 9.5%，差 8.9pp，部分來自回購與週期利潤率"},{"signal":"FCF／淨利 < 0.75 連 2 年","lit":false,"note":"金融業不適用：FCF 由交易資產與放款變動主導"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"投行份額動能落後高盛，但 MS 同期份額數字事實表未涵蓋，未亮燈"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"trailing 本益比落在 4 個年度端點的 34 分位，未見系統性下移"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置穩健，但三項計分能驗證的有限。超額 CET1 約 300bp，本季回購 15.4 億，股東回報約占淨利三分之二；公債殖利率與股權稀釋的資料事實表未涵蓋","reasoning":"FCF 換算率對銀行不適用：FY2022 到 FY2025 年度 FCF 都是負值，由交易資產與放款變動主導，不代表現金流失。改看資本：標準法 CET1 14.9%，要求 11.8%（2026-03-31 口徑），超額約 300bp，執行長本季確認。第三季回購 15.4 億美元，年化約 62 億，約占市值 2.2%。季股息在 2026-07-15 宣布調升 15% 至 1.15 美元，過去 12 個月股息殖利率 2.3%。股息加回購約占 FY2026 共識淨利的 67%，保留約 33%。現金去向四分：營運再投資、併購、回購、股息；後兩項約三分之二，併購近六年沒有（E*TRADE 為六年前收購，增量報酬事實表未涵蓋）。回購買入收益率約 6.7%（共識 EPS 除以快照價），但 10 年期公債殖利率事實表未涵蓋，無法判斷是否過關。股權激勵稀釋事實表未涵蓋。","fact_refs":["f_kpi11_cet1","f_kpi12","f_dividend_yield_ttm","f_ev_m","f_shares_diluted_m","f_consensus_eps_fy1","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近六年無重大併購；管理層 2026-07-15 表示偏向有機成長，E*TRADE 的增量報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購買入收益率約 6.7%（FY2026 共識 EPS 12.75÷快照價 190.02）；10 年期公債殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"股權激勵淨稀釋率事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；股東回報以回購與股息為主，金額已在說明中列出"}}}},"q5_valuation":{"verdict":"現價要求 ROTCE 長期守在 20% 上下才划算，我只部分相信。前瞻 14.2 倍屬合理但不便宜，因為分母可能是週期高點的 2026 年盈餘","reasoning":"現價 180.57 美元，對 FY2026 共識 EPS 12.75 是 14.2 倍，對 FY2027 共識 13.57 是 13.3 倍；10-08 快照價 190.02 時是 14.9 倍。trailing 本益比 14.32，落在 4 個年度端點的 34 分位（不是五年分位）。金融業主錨用合理 P/TBV＝(ROTCE−g)÷(COE−g)，取成長率 5%、資本成本 10%：ROTCE 22.6% 時約 3.5 倍，跨循環 18% 時約 2.6 倍。每股有形淨值事實表未涵蓋，前份以 180 美元對應約 3.3 倍。現價落在兩者之間，靠近高點報酬下的合理值。PEG 1.12，用 FY2025A 到 FY2028E 的共識年化 12.6% 計；若只看 FY2026 到 FY2028 的 6.9%，PEG 約 2.05。金融業不以 PEG 為主錨。賣方均價目標 222 美元（26 位，區間 184–262），高於本份基準。短期上檔用 FY2027 基準 EPS 13.5 乘 14 倍；中期用 FY2031 基準 EPS 16.9 乘 14 倍。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi5_rotce","f_dividend_yield_ttm","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比搭配合理 P/TBV 對 ROTCE（金融業主錨）","tier":"大型整合券商與投行","peers":{"expanded":false,"reason":"事實表同業對照只有 FCF 利潤率，沒有同業本益比、P/TBV 或 ROTCE，不能當估值錨"},"fwd_pe":14.16,"peg":1.12,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 14.2 倍。合理 P/TBV 在跨循環 ROTCE 18% 時約 2.6 倍、在 22.6% 時約 3.5 倍，現價約 3.3 倍（前份換算，本包無每股有形淨值），落在中間偏高；年度端點分位 34 只有 4 個點，不是五年分位，所以五年分位留空。結論：合理不便宜","upside_short_pct":4.7,"upside_mid_pct":31.0,"denominator_disputed":true,"denominator_note":"FY2026 EPS 含股票交易接近 2024 年兩倍的週期高檔，以及過半與 IPO 相關的財富管理流量；若機構證券回到常態，正常化 EPS 會更低，實際倍數高於 14.2 倍"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把週期高點當成常態。股票交易近 2024 年兩倍、IPO 帶動淨新增資產，一旦 AI 融資與資本市場同步退潮，EPS 與倍數會一起下修","reasoning":"三個視角的反證都寫在反證紀錄，這裡只交結論。論點失敗的故事是：AI 資本支出降速，加上信用撥備升高（第三季撥備 1.48 億，去年同期為零，高於預期），把 EPS 拉回 10 到 11 美元，倍數壓到 10 倍。論點成功但股東經濟變差的故事是：存款靠較高成本的種類成長，淨利息收入不升反降，掃款訴訟壓利差。價格已反映太多的故事是：合理 P/TBV 在跨循環報酬下只有約 2.6 倍。陷阱風險維持 🟡：衰退訊號亮一項，業務品質與資本緩衝沒有實質惡化。","fact_refs":["f_kpi5_rotce","f_kpi9","f_kpi8","f_rsi14","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點盈餘被當成常態"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":12.75,"pe":14.16,"basis":"FY2026E 共識 EPS（Koyfin 2026-10-08）對判斷日收盤 180.57；終端倍數乘 FY2031E EPS，口徑同為一年期盈餘"},"eps":{"bull":[14.4,15.9,17.2,18.6,20.0],"base":[13.5,14.4,15.0,15.9,16.9],"bear":[11.3,10.5,11.4,12.4,13.3]},"pe":{"bull":16,"base":14,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.3,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-45,"hi":-30,"basis":"事實表未涵蓋歷史最大回撤，改用三點推：一，前份判斷日 228.55 到現價 180.57，三個月已回撤約 21%；二，2025-04 關稅宣布當日股價跌 9.5%；三，Bear 情境 EPS 由 12.75 跌到 10.5（−18%），疊加本益比由 14.2 倍壓到 10 倍（−30%），合計約 −42%。綜合取 −30% 至 −45%","trigger_time":null},"basis":{"bull":"AI 與資本市場循環延續，財富管理稅前利益率升向 33%，ROTCE 維持 23% 以上；終端 16 倍","base":"機構證券在 2027–2028 小幅正常化，財富管理維持約 8% 成長，每股 EPS 年化約 5.8%（已含回購減股，所以淨回購殖利率填 0，避免重複計算）；終端 14 倍，貼近現值 14.2 倍","bear":"2027 年資本市場退潮加上信用撥備升高，EPS 先跌到 10.5，再靠財富管理回升；終端 11 倍，取成長熄火情境的壓縮倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"本季股票交易年增 41%，分析師稱股票營收接近 2024 年兩倍；淨新增資產過半與 IPO 相關；第三季撥備 1.48 億，高於預期約 8,400 萬；私募信貸違約率創 6% 紀錄；2025-04 關稅宣布當日股價跌 9.5%；高盛投行動能領先","assumption":"財富管理的盈餘地板能抵銷機構證券的回落","consequence":"AI 融資與資本市場同步退潮時，EPS 回到 10 到 11 美元，倍數壓到 10 倍，五年後股價約在 105 到 145 美元，加股息仍虧損","ruling":"部分採納：Bear 機率給 30%，不一次買足。反駁的部分：財富管理稅前利益已占全公司約 43%，2022 年那種營收持平的年份 EPS 仍有 5 美元以上，盈餘不會歸零","watch":"機構證券季營收年增率、全公司撥備、IPO 相關占淨新增資產比重","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#3","reg_tariff_export#1","competitive_share_entrants#2"],"fact_refs":["f_kpi9","f_kpi8"]},{"view":"論點成功但股東經濟變差","evidence":"本季存款季增近 300 億，主要是較高成本的種類，淨利息收入 22 億不升反降（前一季財務長原指引小幅季增）；掃款集體訴訟主張利率過低；參議院民主黨議員要求撤回放寬資本的提案","assumption":"資產增加會等比例轉成利差與費收，超額資本可自由回饋股東","consequence":"資產照樣成長，但每塊錢的利差被壓縮，超額資本被更嚴的規則鎖住，回購放慢，每股 EPS 成長低於資產成長","ruling":"採納為監測項，不改基準。財務長稱融資效益明年才顯現，第四季淨利息收入指引小幅回升；先標未證，若 2027 上半年仍季減，就視為歸因證偽","watch":"財富管理淨利息收入季增率、掃款訴訟程序、資本規則定案內容","evidence_refs":["major_events#0","lawsuit_class_action#0","financial_regulatory_capital_rules#2"],"fact_refs":["f_kpi11_cet1"]},{"view":"價格已反映太多","evidence":"現價約 3.3 倍有形淨值（前份換算）；ROTCE 22.6% 下的合理值約 3.5 倍，跨循環 18% 下約 2.6 倍；賣方均價目標 222 美元","assumption":"市場會繼續按高點報酬定價","consequence":"若 ROTCE 回到 18%，合理倍數下修約兩成，即使盈餘持平，股價也沒有空間","ruling":"採納部分：估值結論只給合理、不給便宜，加碼價設在前瞻 13 倍（約 166 美元）","watch":"季度 ROTCE 是否在機構證券回落時仍守 18%","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_kpi5_rotce"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 228.55 → 本次 180.57（-21.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=228.55","side_b":"本次 price_at_dd=180.57","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 228.55 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 228.55 美元：Bull 價 389、Bear 價 142，五年期望值 +21.0%，基準年化 5.5%，不對稱比 1.5","side_b":"本次情境、股價仍用 228.55 美元：Bull 價 320、Bear 價 146.3，五年期望值 +0.8%，基準年化 0.7%，不對稱比 0.93","ruling":"先換情境、股價不動：五年期望值少 20.2 個百分點，基準年化少 4.8 個百分點。不對稱比由 1.5 變為 0.93。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 228.55 美元：五年期望值 +0.8%，基準年化 0.7%，不對稱比 0.93","side_b":"本次情境、股價 180.57 美元：五年期望值 +27.6%，基準年化 5.6%，不對稱比 3.39","ruling":"再換股價、情境不動：起點價下跌 21.0%，五年期望值多 26.8 個百分點，基準年化多 4.9 個百分點，不對稱比由 0.93 升到 3.39。合計五年期望值比前份多 6.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：資本與獲利品質","cause":null,"prior_field":null,"side_a":"ROTCE 22.6%，連 5 季高於 20%；CET1 14.9%，高於要求約 300bp","side_b":"管理層與前份都認為資本緩衝充足、財富管理稅前利益率守在 30%","ruling":"兩邊一致：資本與獲利品質不是本份的爭點","evidence_level":"一手財報","settle_metric":"季度 ROTCE 與 CET1","if_then":[],"evidence_refs":[]},{"axis":"管理層指引與兌現","cause":null,"prior_field":null,"side_a":"2026-07-15 前一季法說：財務長 Sharon Yeshaya 指引第三季財富管理淨利息收入小幅季增；執行長 Ted Pick 說投行展望正面；上半年效率比 65%","side_b":"2026-10-14 本季法說：財務長說淨利息收入 22 億小幅下降，原因是存款增加且結構轉向較高成本；投行只年增 2%，低於預期約 1.1 億；年初至今效率比升到 66%","ruling":"可調和，屬程度差異。淨利息收入落差來自主動吸收存款，第四季指引小幅回升，先標未證、監測。投行落差屬時點問題，管線說法沒變","evidence_level":"一手逐字稿","settle_metric":"2026 第四季與 2027 第一季財富管理淨利息收入季增率","if_then":["若 2027 第一季淨利息收入仍季減，則把存款策略視為壓利差，停止加碼","反向：若連 2 季季增且存款續增，則確認銀行融資效益，按原計畫加碼第二批"],"evidence_refs":[]},{"axis":"淨新增資產的結構性","cause":null,"prior_field":null,"side_a":"執行長：收購 E*TRADE 後三年一兆、再三年一兆，漏斗會自我強化；財務長：IPO 資產保留率穩定","side_b":"2026-07-15 前一季：IPO 相關約占淨新增資產略過半；2026-10-14 本季：再度略過半，收費型流入 805 億裡近半來自單一企業退休金委託","ruling":"可調和：六年兩兆是多年實績，結構性成立；但最近兩季的紀錄有過半屬事件性來源，2,324 億不能當新的季度常態。H1 門檻用年化 3,000 億（對應三年一兆），不用單季紀錄","evidence_level":"一手逐字稿","settle_metric":"剔除 IPO 相關後的淨新增資產（看公司是否揭露）","if_then":["若剔除 IPO 後連 2 季年化低於 2,000 億，則減碼一半","反向：若 IPO 冷卻季的淨新增資產仍有年化 3,000 億，則加碼第二批"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：資本規則提案估計最大型銀行 CET1 要求降約 4.8%，前十大投行份額合計年增 3.4pp","side_b":"競爭惡化：高盛上半年投行費用 +52%，MS 第三季 +2%；其他結構變數（法規軸）：參議院民主黨議員要求撤回放寬提案、反壟斷與掃款訴訟仍在進行","ruling":"雙向拉鋸：結構面轉好，競爭面在投行一塊轉差，法規軸可能翻轉。淨效果不足以改變基準情境","evidence_level":"一手文件加二手彙整","settle_metric":"資本規則最終版本、MS 投行份額排名","if_then":["若最終規則使 CET1 要求上升至少 50bp，則下修回購假設並減碼","反向：若 2026 年內按提案定案，則上調回購假設"],"evidence_refs":["competitive_share_entrants#2","financial_regulatory_capital_rules#2","regulatory_antitrust#0"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣方：股票營收接近 2024 年兩倍，IPO 撐起淨新增資產，撥備高於預期，私募信貸違約創紀錄；9 月量能已轉弱，執行長自己說第四季到 2027 上半年是關鍵十字路口，現在的 EPS 就是高點","side_b":"買方：財富管理稅前利益已占約 43%，股價三個月跌 21% 到前瞻 14.2 倍，RSI 25 屬超賣，超額資本 300bp 可在回檔時回購","ruling":"部分採納賣方：現價先不建倉，等 166 美元或第四季確認後才建首批，不一次買足；Bear 機率給 30%","evidence_level":"一手財報加產業數據","settle_metric":"機構證券營收年增率與全公司撥備","if_then":["若機構證券營收連 2 季年減，且撥備單季至少 3 億，則減碼一半","反向：若股價續跌但 ROTCE 守在 18% 以上、CET1 至少 14%，則分批反買到目標倉位"],"evidence_refs":["financial_capital_credit_cycle#1","financial_capital_credit_cycle#3"]},{"axis":"前份漂移：估值與裁決","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-07-16：股價 228.55，估值結論 🔴，訊號 B，觀望；Bull 25%、Bear 30%","side_b":"本份：股價 180.57（−21%），前瞻 14.2 倍，估值結論改 🟡；訊號維持 B；機率維持 Bull 25%、Bear 30%、Base 45%；裁決與倉位角色由程式依新價格重算","ruling":"估值改善全部來自價格下跌，基本面沒有同幅改善：FY2026 共識三個月上修 4.6%，但最近一週下修 1.5%。機率不動，因為下行來源（資本市場循環與信用）沒有消失","evidence_level":"事實表價格與共識","settle_metric":"前瞻本益比與共識修正方向","if_then":["若共識連 2 個月下修，則 Bear 機率上調至 35%"],"evidence_refs":[]},{"axis":"前份漂移：護城河與跑道","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河趨勢 ↑，陷阱風險 🟡，五年後跑道 🟡","side_b":"本份：護城河趨勢改為 →；陷阱 🟡、跑道 🟡 不變","ruling":"改 → 的新證據：兩季紀錄級淨新增資產都有過半屬 IPO 事件性來源，有機加速沒有證實；高盛投行動能領先；同業報酬差距事實表未涵蓋，向上方向證不出來。陷阱維持 🟡，衰退訊號亮一項","evidence_level":"一手逐字稿加同業二手數據","settle_metric":"剔除 IPO 後的淨新增資產、投行份額排名","if_then":["若剔除 IPO 後年化淨新增資產連 2 季超過 3,000 億，則護城河趨勢回到 ↑"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"前份漂移：回撤與循環判讀","cause":"方法變動","prior_field":["max_dd_pct","cycle_position","archetype"],"side_a":"前份最大回撤為點值 −55%，循環位置未填，業務類型為金融","side_b":"本份最大回撤改為範圍 −30% 至 −45%，循環位置填中循環，業務類型仍為金融","ruling":"最大回撤改用範圍，並由 Bear 情境 EPS 乘倍數推導，前份點值沒有推導過程。新增循環判讀的依據：sponsor 退場尚未完成（執行長本季說法），股票交易在高檔，屬中循環","evidence_level":"方法調整","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：加碼重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"P/TBV 回落至 ≤3.3x（≈$180，等 warranted 錨）或 through-cycle ROTCE 連 3 季 >20%（弱市確認結構性步階）或 SEC/FinCEN/OCC AML 程序結案","side_b":"股價 ≤166 美元（前瞻 13 倍）加碼；或 2026 第四季與 2027 第一季剔除 IPO 後淨新增資產年化 ≥3,000 億，且撥備每季 <2 億","ruling":"前份的價格錨（約 180 美元）本週已觸及，這就是本份重跑的原因；前份判斷日距今 94 天，超過 90 天的沿用期限。新條件把價格錨下移到前瞻 13 倍，並把跨循環 ROTCE 改成每季可驗證的淨新增資產與撥備條件。AML 結案條件移出重啟條件，因為本包沒有 AML 程序的新證據（資料缺口）；門檻改放在訴訟監管風險，罰金 >5 億照舊保留。觸及新條件就加碼第二批","evidence_level":"價格事實加方法調整","settle_metric":"股價、季度淨新增資產與撥備","if_then":["若股價 ≤166 美元且 ROTCE 仍 ≥18%，則加碼第二批","反向：若股價回到 220 美元以上而基本面沒有新證據，則不追"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定 Single Thing（null）","side_b":"AI 資本支出循環在 2027 年底前實質降速，同時帶走股票交易、IPO 承銷與 IPO 相關淨新增資產","ruling":"前份沒有設唯一致命點。本份按敏感度挑選：這件事同時打到三條收入線，是 Bear 情境 EPS 最大的單一來源；一旦發生就減碼一半","evidence_level":"一手逐字稿","settle_metric":"大型雲端業者資本支出指引、MS 股票交易年增率","if_then":["若大型雲端業者資本支出年增轉負，且 MS 股票交易年減，則減碼一半"],"evidence_refs":[]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定（null）","side_b":"ROTCE 連 2 季 <15%；CET1 <13%；剔除 IPO 後淨新增資產連 2 季年化 <2,000 億；撥備單季 ≥3 億且連 2 季","ruling":"前份只有假設與風險表，沒有可執行的停損門檻，本份補上四條。命中任兩條就減碼一半；CET1 跌破 12.3% 或 ROTCE 連 4 季低於 10% 就清倉","evidence_level":"方法調整","settle_metric":"季度財報","if_then":["命中任兩條，則減碼一半","CET1 <12.3% 或 ROTCE 連 4 季 <10%，則清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"財富管理淨新增資產的結構性","type":"假設驗證","maps_to":"H1","metric":"剔除 IPO 相關後的淨新增資產（年化）","threshold":"連 2 季年化低於 3,000 億美元","action":"停止加碼","source_freq":"季報與法說，每季","date":"2027-01","evidence_refs":[]},{"n":2,"text":"資本市場量能回落","type":"風險","maps_to":"R1","metric":"機構證券季營收年增率","threshold":"連 2 季年減","action":"減碼","source_freq":"季報新聞稿，每季","date":"2027-01","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":3,"text":"信用撥備升高","type":"風險","maps_to":"R2","metric":"全公司信用損失撥備","threshold":"單季至少 3 億美元且連 2 季","action":"減碼","source_freq":"季度財務補充資料，每季","date":"2027-01","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#3"]},{"n":4,"text":"資本規則翻轉","type":"風險","maps_to":"R3","metric":"最終規則下的標準法 CET1 要求","threshold":"較現行 11.8% 上升至少 50bp","action":"停止加碼","source_freq":"Fed／OCC／FDIC 公告，事件","date":null,"evidence_refs":["financial_regulatory_capital_rules#2"]},{"n":5,"text":"訴訟與監管升級","type":"風險","maps_to":"R4","metric":"掃款與反壟斷訴訟程序、AML 程序","threshold":"進入集體認證，或和解、罰金超過 5 億美元，或出現 AML 同意令","action":"減碼","source_freq":"10-Q／8-K，每季","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0"]},{"n":6,"text":"AI 資本支出降速同時打擊三條收入線","type":"Single Thing","maps_to":null,"metric":"大型雲端業者資本支出年增率與 MS 股票交易年增率","threshold":"兩者同時轉負","action":"減碼","source_freq":"雲端業者財報與 MS 季報，每季","date":null,"evidence_refs":[]},{"n":7,"text":"價格回到加碼區","type":"估值rearm","maps_to":null,"metric":"股價（前瞻本益比）","threshold":"≤166 美元（FY2026 共識 EPS 12.75 乘 13 倍），且 ROTCE ≥18%","action":"加碼","source_freq":"日線收盤","date":null,"evidence_refs":[]},{"n":8,"text":"報酬跌破中段","type":"減碼","maps_to":"H2","metric":"全公司季度 ROTCE","threshold":"連 2 季低於 15%","action":"減碼","source_freq":"季報新聞稿，每季","date":null,"evidence_refs":[]},{"n":9,"text":"資本或報酬失守","type":"清倉","maps_to":"H3","metric":"標準法 CET1／ROTCE","threshold":"CET1 <12.3%，或 ROTCE 連 4 季 <10%","action":"清倉","source_freq":"季報新聞稿，每季","date":null,"evidence_refs":[]},{"n":10,"text":"第四季財報複審","type":"複審日期","maps_to":null,"metric":"淨利息收入、撥備、IPO 相關淨新增資產占比","threshold":"無","action":"重跑判斷","source_freq":"季報","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"全公司季度 ROTCE","bear_threshold":"連 2 季 <15%","window":"2026Q4–2027Q4","source":"MS 季報新聞稿","last_status":"ok"},{"metric":"標準法 CET1 比率","bear_threshold":"<13.0%（要求 11.8%）","window":"每季","source":"MS 季報新聞稿與 10-Q","last_status":"ok"},{"metric":"剔除 IPO 相關後的財富管理淨新增資產","bear_threshold":"連 2 季年化 <2,000 億美元","window":"2026Q4–2027Q4","source":"MS 季度法說","last_status":"unknown"},{"metric":"全公司信用損失撥備","bear_threshold":"單季 ≥3 億美元且連 2 季","window":"2026Q4–2027Q4","source":"MS 季度財務補充資料","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤166 美元（前瞻 13 倍）加碼；或 2026Q4 與 2027Q1 剔除 IPO 後淨新增資產年化 ≥3,000 億且撥備每季 <2 億","exec_line":"現價先不建倉。股價 ≤166 美元，或 2026Q4 與 2027Q1 確認淨新增資產與撥備（條件同加碼條件）時建首批（目標倉位三分之一）；ROTCE ≥18% 時加碼第二批。kill 指標命中任兩條就減碼一半；CET1 <12.3% 或 ROTCE 連 4 季 <10% 就清倉"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 MS 當成純資本市場週期股，在 9 月量能轉弱、利率走高時三個月殺了 21%。但第三季財富管理稅前利益 28 億美元，已占全公司稅前 64.78 億的約 43%，六年兩兆淨新增資產也是多年實績；週期回落時，盈餘地板有財富管理撐住","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤166 美元（前瞻 13 倍），或 2026Q4 與 2027Q1 剔除 IPO 後淨新增資產年化 ≥3,000 億且撥備每季 <2 億"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 MS 當成純資本市場週期股，在 9 月量能轉弱、利率走高時三個月殺了 21%。但第三季財富管理稅前利益 28 億美元，已占全公司稅前 64.78 億的約 43%，六年兩兆淨新增資產也是多年實績；週期回落時，盈餘地板有財富管理撐住"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-3.33, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"財富管理是結構性複利：漏斗（E*TRADE、職場股票計畫、顧問）持續把新資產轉進收費帳戶，稅前利益率隨規模擴張","2y":null,"5y":"FY2031 前財富管理淨營收年化成長 ≥7%，稅前利益率 ≥30%","10y":null,"threshold":"淨新增資產年化 ≥3,000 億美元（對應三年一兆）；財富管理稅前利益率 ≥28%","source":"季報新聞稿財富管理分部、季度法說","drift_rule":"TTM 淨新增資產低於 3,000 億：連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"},{"id":"H2","text":"全公司報酬穿越循環仍高於資本成本：機構證券回落時，財富管理撐住 ROTCE 不跌破 15%","2y":null,"5y":"2027–2031 每年 ROTCE ≥15%，跨循環平均 ≥18%","10y":null,"threshold":"季度 ROTCE ≥15%；機構證券季營收 ≥80 億美元","source":"季報新聞稿 ROTCE 與分部營收","drift_rule":"TTM ROTCE 低於 18%：連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"},{"id":"H3","text":"超額資本轉成股東回報：資本規則定案後，超額 CET1 支撐每年至少 60 億回購與股息成長","2y":"2027–2028 回購合計 ≥120 億美元，CET1 維持 ≥13.5%","5y":null,"10y":null,"threshold":"CET1 ≥13.5%；年回購 ≥60 億美元","source":"季報新聞稿資本段、Fed 年度壓力測試結果","drift_rule":"TTM 回購低於 60 億：連 2 季偏離 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"資本市場量能回落：9 月起各資產類別量能轉弱；關稅或地緣事件會讓客戶延後併購，2025-04 關稅宣布當日股價跌 9.5%","h_ref":"H2","clock":"⚡","threshold":"機構證券季營收連 2 季年減","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R2","text":"信用循環轉差：第三季撥備 1.48 億（去年同期為零），沖銷集中在企業與商用不動產放款；私募信貸違約率創紀錄","h_ref":"H2","clock":"🔥","threshold":"全公司撥備單季 ≥3 億美元且連 2 季，或淨沖銷單季 ≥2 億","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#3"]},{"id":"R3","text":"資本規則翻轉：放寬提案尚未定案，參議院民主黨議員要求撤回並重提更嚴版本","h_ref":"H3","clock":"🐢","threshold":"最終規則使標準法 CET1 要求較 11.8% 上升 ≥50bp","evidence_refs":["financial_regulatory_capital_rules#2"]},{"id":"R4","text":"訴訟與監管：掃款集體訴訟、VRDO 與利率交換反壟斷訴訟仍在進行；前份列的 AML 程序在本包沒有新進展","h_ref":"H1","clock":"🔥","threshold":"進入集體認證，或任一案和解、罰金超過 5 億美元，或出現 AML 同意令（本包無新進展，資料缺口）","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0"]}],"single_thing":{"description":"AI 資本支出循環在 2027 年底前實質降速（大型雲端業者資本支出年增轉負），同時帶走股票交易、IPO 承銷與 IPO 相關的淨新增資產","why_fatal":"本季股票交易年增 41%，淨新增資產過半與 IPO 相關，管理層自稱對 AI「雙倍加碼」。三條收入線共用同一個驅動因子，是 Bear 情境 EPS 由 12.75 跌到 10.5 的最大單一來源，無法靠業務分散","if_happens":"減碼一半，暫停加碼，直到剔除 IPO 後的淨新增資產連 2 季守住年化 3,000 億","how_monitor":"每季看三個數字：大型雲端業者資本支出指引、MS 股票交易營收年增率、IPO 相關占淨新增資產比重。執行長本季估 AI 年資本支出約 1 兆美元，並說未必再加速","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.31,"peg_fy2":1.06,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":10.21,"FY2026E":12.75,"FY2027E":13.57,"FY2028E":14.56},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識取 Koyfin 2026-10-08 快照，基期為 FY2025 年報稀釋 EPS"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"2026 第四季財報與法說：淨利息收入是否回升、信用撥備與 IPO 相關淨新增資產占比","impact":"高","watch":"財富管理淨利息收入季增、撥備 <2 億、剔除 IPO 後淨新增資產"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"美國資本規則三項提案是否定案（MS 促請 2026 年內定案，2028-01-01 生效）","impact":"高","watch":"最終 CET1 要求的變動幅度"},{"date":"2027-06","date_precision":"month","type":"regulatory","event":"Fed 2027 年度壓力測試結果，決定 2027-10-01 起的壓力資本緩衝","impact":"中","watch":"壓力資本緩衝是否低於現行 4.3%"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
