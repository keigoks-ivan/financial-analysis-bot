你是 DD 管線 v20 的判斷層閘（gate），標的 ATI（20261013）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_sales_gaap`（q1_business）｜Sales (GAAP)＝1261.1 USD M｜期間與口徑：Q2 2026（季末 2026-06-28，公告 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-28，公告 2026-08-06））
  - 註記：未取得
- `f_kpi1_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代之）＝284.4 USD M（利益率 22.6%）｜期間與口徑：Q2 2026（季末 2026-06-28，公告 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-28，公告 2026-08-06））
  - 註記：超出公司自家 Q2 指引上緣（標題：Exceeds the High End of Q2 Guidance）；分析師共識數字未取得
- `f_kpi2_operating_income_gaap`（q1_business）｜Operating income (GAAP)＝220.0 USD M（利益率 17.4%，由新聞稿數字推算）｜期間與口徑：Q2 2026（季末 2026-06-28，公告 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）；含 9.9M 廠房出售利得、23.6M 特殊項目稅前費用（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-28，公告 2026-08-06））
  - 註記：未取得
- `f_kpi5_backlog`（q1_business）｜Backlog＝4400 USD M（YoY +18%，創高）｜期間與口徑：Q2 2026（季末 2026-06-28，公告 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-28，公告 2026-08-06））
  - 註記：不適用
- `f_peer_ati_gross_margin_pct`（q2_moat）｜ATI 毛利率＝23.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ATI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ati_operating_margin_pct`（q2_moat）｜ATI 營業利益率＝15.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ATI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi6_guidance_q3_2026`（q1_business）｜Guidance：Q3 2026＝Adj EBITDA 305–315M；Adj EPS 1.31–1.37 USD｜期間與口徑：Q2 2026 新聞稿（2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）；未提供營收指引（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026 新聞稿（2026-08-06））
  - 註記：未取得
- `f_kpi7_guidance_fy2026`（q1_business）｜Guidance：FY2026（上修）＝Adj EBITDA 1,135–1,185M；Adj EPS 4.90–5.18；Adj FCF 550–600M USD｜期間與口徑：Q2 2026 新聞稿（2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026 新聞稿（2026-08-06））
  - 註記：本站 FY1 EPS 共識 5.12（2026-10-08 快照，位於指引區間內）
- `f_peer_hwm_operating_margin_pct`（q2_moat）｜HWM 營業利益率＝27.31 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HWM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_crs_operating_margin_pct`（q2_moat）｜CRS 營業利益率＝22.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hwm_gross_margin_pct`（q2_moat）｜HWM 毛利率＝36.03 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HWM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_crs_gross_margin_pct`（q2_moat）｜CRS 毛利率＝30.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ati_fcf_margin_pct`（q2_moat）｜ATI FCF 利潤率＝11.16 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ATI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hwm_fcf_margin_pct`（q2_moat）｜HWM FCF 利潤率＝19.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HWM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_crs_fcf_margin_pct`（q2_moat）｜CRS FCF 利潤率＝11.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cstm_operating_margin_pct`（q2_moat）｜CSTM 營業利益率＝8.5 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSTM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mtrn_operating_margin_pct`（q2_moat）｜MTRN 營業利益率＝6.35 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTRN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.12 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.37 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝7.5 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5143.96 USD m｜期間與口徑：2026-10-13／yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝5651.62 USD m｜期間與口徑：2026-10-13／yfinance revenue_estimate +1y 平均（8 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_adjusted_free_cash_flow`（q1_business）｜Adjusted free cash flow＝68.6 USD M｜期間與口徑：Q2 2026（季末 2026-06-28，公告 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）；營業現金流 131.8M，capex 68.6M（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-28，公告 2026-08-06））
  - 註記：未取得
- `f_kpi4_sbc_0_6`（q4_capital）｜SBC（上半年累計，占上半年營收約 0.6%）＝14.1 USD M｜期間與口徑：2026 上半年（至 2026-06-28，公告 2026-08-06）；新聞稿未單列 Q2／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）；占比 = 14.1 ÷ (1,261.1+1,151.5)（numbers.latest_quarter_kpis.items[4]，as_of 2026 上半年（至 2026-06-28，公告 2026-08-06）；新聞稿未單列 Q2）
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1409.0 USD m｜期間與口徑：2026-10-13／yfinance 最新一季：總債務 2192.0、現金 783.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-10-13／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-13）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝136.17 m shares｜期間與口徑：2026-10-13／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝187.98 USD｜期間與口徑：2026-10-12（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-12（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝37.47 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 5.12，分子＝快照價 191.84｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝55.13 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝14.54 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 4.47 → 5.12（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.73 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.25 x｜期間與口徑：2026-10-13／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Carpenter Technology 預期 2026 資本支出 2.2–2.4 億美元，投向自有引擎合金與高毛利機會，訂單連續數季成長（Zacks）。
  - 來源：Zacks: ATI vs. CRS: which specialty metals stock should you invest in now（as_of 2026-01-01）｜affects：decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：ATI FY2025 10-K 指出 HPMC 分部約 92% 營收來自航太與國防市場，並點名 Boeing、Airbus、Embraer（機身）與 GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran（發動機）為少數大型客戶群；搜尋摘要未取得單一客戶占營收百分比。
  - 來源：ATI INC - Form 10-K - FY2025 (SEC EDGAR)（as_of 2026-02-01）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#6`（supply_demand_durability｜方向 -｜狀態 ok）：Argus 稱引擎瓶頸正在緩解（Airbus 與 Pratt & Whitney GTF 交付爭議為例外）；ATI 集中於少數大型航太 OEM 為風險；HPMC 約 $30–40M 出貨因認證時程遞延至下半年。
  - 來源：Argus Media 2860247；Panabee／MarketBeat 彙整（as_of 2026-08-07）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：ATI 持有中國合資 STAL 60% 股權（寶武 40%），產品為精密軋製不鏽鋼帶，主要供亞洲電子與汽車市場；另 Section 232 對不鏽鋼板胚的排除申請曾遭商務部否決、25% 關稅仍在（舊案，非 2026 新事件）。
  - 來源：ATI Form ARS FY2022（as_of 2023-03-01）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：ATI 10-K FY2025 揭露：鎳、海綿鈦、鈷、鉻鐵等原料多來自可能政經不穩的外國；鎳來源列加拿大、挪威、日本、芬蘭、南非；海綿鈦來源列日本、哈薩克、沙烏地、中國；公司稱原料可由多家供應商取得、目前供給足夠。
  - 來源：ATI INC Form 10-K FY2025 (SEC)（as_of 2025-12-28）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：ATI 年報（FY2024 ARS）警告中國已實施且未來可能續行出口管制，可能限制或顯著延遲取得相關材料。
  - 來源：ATI INC Form ARS FY2024 (SEC)（as_of 2024-12-29）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：ATI 10-K 列出『替代材料使用增加或價格下降』為影響其市場地位與獲利波動的因子之一（FY2022–FY2025 10-K 皆有）；未見具體量化的替代技術威脅。
  - 來源：ATI INC Form 10-K FY2025 (ati-20251228.htm)（as_of 2025-12-28）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：GKN Aerospace 與美國空軍研究實驗室啟動 TITAN-AM（840 萬美元），推進線材雷射金屬沉積用於大型鈦機身結構的工業化，屬鈦鍛件的近淨形替代/補充路徑。
  - 來源：aeromorning.com: GKN Aerospace and U.S. Air Force advance additive manufacturing（as_of 2026-04-13）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：投資人撰寫的敘事（非公司揭露/非分析師研究）主張複合材料、陶瓷、奈米材料與積層製造長期可能侵蝕 ATI 合金與鈦產品需求。
  - 來源：Simply Wall St community narrative: additive manufacturing and composite substitutes will disrupt future prospects（as_of 2025-05-01）｜affects：decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：ATI 與 State Street Global Advisors Trust Co. 在賓州西區聯邦法院面臨兩宗與 2023 年退休金義務轉移相關的集體訴訟（2:24-cv-01109、2:24-cv-01214），2024 年底合併、ATI 已提動議駁回；2026 年 Q2 10-Q 仍列為進行中。搜尋摘要未見結果。
  - 來源：ATI Inc. Form 10-Q (period ended 2026-06-28)（as_of 2026-06-28）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：退休金義務轉移相關的兩宗集體訴訟（ERISA 性質參與人訴訟）在賓州西區進行中，被告含 ATI 與 State Street Global Advisors Trust Co.；2026 年 Q2 10-Q 仍列示。非證券詐欺案。
  - 來源：ATI Inc. Form 10-Q (period ended 2026-06-28)（as_of 2026-06-28）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261013/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":348.0,"bear_5y_price":79.5,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":18.7,"ev5y_pct":12.4,"irr_base_pct":3.5,"asym_ratio":1.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.12,"pe":36.71,"basis":"FY2026 共識調整後 EPS（FY1）；終端倍數同樣乘在終端年度 FY2031 的全年調整後 EPS；回購效果已含在 EPS 路徑內，淨回購殖利率填 0 避免重複計算"},"eps":{"bull":[6.9,8.2,9.4,10.5,11.6],"base":[6.4,7.4,8.05,8.65,9.3],"bear":[5.8,5.4,4.4,4.7,5.3]},"pe":{"bull":30,"base":24,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ATI_Q1_2026_Earnings_Call_20260430.md
- 2026-04-30｜CEO Kim Fields｜guidance：全年調整後 EBITDA 財測上調至 10.1–10.6 億美元（原話："adjusted EBITDA of $1.01 billion to $1.06 billion"）
- 2026-04-30｜CFO Rob Foster｜guidance：Q2 調整後 EBITDA 財測 2.45–2.55 億美元（原話："adjusted EBITDA of $245 million to $255 million"）
- 2026-04-30｜CFO Rob Foster｜guidance：全年自由現金流區間中點上調 3,500 萬美元（原話："We are raising the midpoint of our range by $35 million"）
- 2026-04-30｜CFO Rob Foster｜guidance：全年資本支出區間維持不變（原話："Our CapEx range remains consistent with our prior guidance."）
- 2026-04-30｜CFO Rob Foster｜guidance：CFO 對 2027 既有財測區間的信心與偏向，並預告 Q4 時段更新（原話："I have a bias towards the upper end of that 2027 guide"）
- 2026-04-30｜CFO Rob Foster｜guidance：國防成長指引為低至中十位數，CFO 偏向區間上緣（原話："my bias is towards the upper end of that guide"）
- 2026-04-30｜CEO Kim Fields｜guidance：特殊能源全年成長指引為中十位數，且接單與出貨呈塊狀（原話："lumpy as the orders come in, in an intermittent"）
- 2026-04-30｜CFO Rob Foster｜guidance：工業、醫療、電子市場全年預期下滑（原話："Sales for our industrial, medical and electronics"）
- 2026-04-30｜CEO Kim Fields｜guidance：機身（airframe）上半年持平、下半年加速，更大增幅在 2027（原話："is going to be flattish as that inventory"）
- 2026-04-30｜CFO Rob Foster｜margin：全年合併 EBITDA 利潤率指引 20% 以上（原話："year consolidated margins in the range of 20% plus"）
- 2026-04-30｜CFO Rob Foster｜margin：Q2 利潤率與 Q1 相近，下半年擴大至 20% 以上（原話："Q2 margins are tracking to be similar"）
- 2026-04-30｜CFO Rob Foster｜margin：全年合併增量利潤率平均 40%，下半年高於上半年（原話："Full year consolidated incremental margins will average 40%"）
- 2026-04-30｜CFO Rob Foster｜margin：分部全年利潤率口徑：HPMC 中 20%、AA&S 高 10%（原話："full year margins for HPMC will be in the range of mid-20s"）
- 2026-04-30｜CFO Rob Foster｜margin：Q1 利潤率優於預期的歸因為 80/20 與投資組合精簡帶來的較佳組合（原話："we realized a richer mix from 80/20 initiatives"）
- 2026-04-30｜CFO Rob Foster｜margin：管理層稱 2026 增量利潤率 40% 高於歷史指引區間（原話："pretty confident in that 40% year-over-year incremental"）
- 2026-04-30｜CEO Kim Fields｜margin：管理層預期加速效果更多體現在利潤與 EBITDA 而非營收（原話："our margin and EBITDA line more so than the revenue line"）
- 2026-04-30｜CEO Kim Fields｜product：訂單積壓季增 10% 創新高（原話："order backlog growing by 10% sequentially to an all-time"）
- 2026-04-30｜CEO Kim Fields｜product：飛彈相關營收年增超過一倍（原話："revenue in missiles and missile systems more than doubled"）
- 2026-04-30｜CEO Kim Fields｜product：ATI 供應七種最先進噴射引擎鎳合金中的六種（原話："We supply 6 of the 7"）
- 2026-04-30｜CEO Kim Fields｜product：預期明年鈦的銷售成長更強（原話："titanium sales growth in '27"）
- 2026-04-30｜CEO Kim Fields｜customer：與 Cameco 新簽五年協議，金額 2.5 億美元（原話："This $250 million agreement includes meaningful improvements"）
- 2026-04-30｜CFO Rob Foster｜customer：Cameco 合約 Q1 貢獻有限，屬未來效益（原話："There wasn't much benefit accrued into the Q1."）
- 2026-04-30｜CEO Kim Fields｜customer：海軍核動力計畫五年續約，預計營收 10 億美元（原話："This agreement is projected to generate $1 billion in"）
- 2026-04-30｜CEO Kim Fields｜customer：管理層稱 Middle East 衝突目前對需求與訂單無實質影響（原話："We've seen no material impact on demand or order activity."）
- 2026-04-30｜CEO Kim Fields｜competition：管理層稱定價屬長期合約內建，非僅短期稀缺（原話："but it's long term and contractual"）
- 2026-04-30｜CEO Kim Fields｜competition：管理層對 OE 與 MRO 不作價格區分，回應 OE 放量期價格不降反升的提問（原話："we don't really see a differentiation between OE versus"）
- 2026-04-30｜CEO Kim Fields｜competition：新世代引擎的 ATI 含量約為舊引擎的兩倍（原話："We've got twice the content, as I've shared"）
- 2026-04-30｜CFO Rob Foster｜capital_allocation：Q1 回購 7,500 萬美元股票（原話："we repurchased $75 million in shares"）
- 2026-04-30｜CFO Rob Foster｜capital_allocation：Q1 增加 5 億美元回購授權（原話："We increased our share authorization by $500 million in Q1"）
- 2026-04-30｜CEO Kim Fields｜capital_allocation：目前不宣布新的重大產能專案（原話："announce any new significant projects today"）
- 2026-04-30｜CEO Kim Fields｜capital_allocation：產能調配：降低工業、醫療、電子比重，轉往高利潤市場（原話："we are deemphasizing those and moving the capacity"）
- 2026-04-30｜CEO Kim Fields｜risk：噴射引擎仍為最高利潤業務，但差距快速縮小（原話："although that's been rapidly shrinking"）
- 2026-04-30｜CFO Rob Foster｜risk：Q1 機身營收年減 9%（原話："airframe revenue declined by 9%"）
- 2026-04-30｜CEO Kim Fields｜risk：關稅全數透過合約轉嫁，退稅政策進展不大（原話："there has not been a lot of progress in that regard"）
- 2026-04-30｜CEO Kim Fields｜risk：通膨成本透過合約轉嫁（原話："we do pass through all of those"）
- 2026-04-30｜CFO Rob Foster｜commitment：CFO 承諾 2026 年每季自由現金流為正（原話："generate positive cash flow in every quarter of 2026"）
- 2026-04-30｜CEO Kim Fields｜commitment：管理層稱 50 億美元營收、20% 以上利潤率在望（原話："$5 billion of revenue at 20%-plus margins is in clear sight"）
- 2026-04-30｜CEO Kim Fields｜commitment：管理層稱 A&D 占比將持續提高並高於 70%（原話："A&D mix is going to continue to go higher"）
- 2026-04-30｜CEO Kim Fields｜commitment：明年初鎳產能約增 5% 產量釋出（原話："where we really unleash, call it, 5% or so more volumes"）

### ATI_Shareholder_Analyst_Call_ATI_Inc_20260514.md
- 2026-05-14｜Robert S. Wetherbee｜risk：執行董事長 Wetherbee 表示這是他擔任董事長的最後一次正式行動（領導層交接）。（原話："This is my last official act as the Executive Chairman"）
- 2026-05-14｜Robert S. Wetherbee｜risk：Kim Fields 自即日起兼任董事會主席，並仍為總裁暨 CEO。（原話："Fields as President, CEO, and, as of now, Board Chair."）
- 2026-05-14｜Robert S. Wetherbee｜competition：Wetherbee 稱團隊已轉型並成為有差異化的市場領導者（無數字佐證）。（原話："differentiated itself as a market leader."）
- 2026-05-14｜Robert S. Wetherbee｜product：Wetherbee 以航空應用說明 ATI 產品的重要性（無細節）。（原話："And you can't fly without ATI either."）

### ATI_Morgan_Stanley_s_14th_Annual_Laguna_Conference_20260917.md
- 2026-09-17｜Kimberly Fields｜margin：CEO 引述第二季 AA&S 與全公司利潤率（AA&S 一年前為 14%）（原話："about 22% margin in AA&S segment, 23% across the business"）
- 2026-09-17｜Kimberly Fields｜margin：CEO 表示目前增量利潤率約 50%，並預期全年持續（原話："we're at 50% incrementals today, and that's phenomenal"）
- 2026-09-17｜Kimberly Fields｜guidance：CEO 提到進入 2027 的隱含 EBITDA run rate 為 13.5 億美元（原話："run rate of going into 2027 at $1.35 billion of EBITDA"）
- 2026-09-17｜Kimberly Fields｜guidance：2027 年將有今年價格與合約重設的全年效應（原話："a full year of these price and contractual resets"）
- 2026-09-17｜Kimberly Fields｜guidance：今年 CapEx 區間 2.8–3.0 億美元，約 20% 為客戶出資（原話："between $280 million to $300 million"）
- 2026-09-17｜Kimberly Fields｜commitment：CEO 說 11 月將舉辦投資人日，屆時分享前瞻細節（原話："we've got an Investor Day that's going to be in November"）
- 2026-09-17｜Kimberly Fields｜commitment：內部資本專案報酬率門檻為 30% IRR（未計客戶出資前）（原話："So that's a 30% IRR target."）
- 2026-09-17｜Kimberly Fields｜commitment：合約續約／重設預定在年底前進行（原話："resetting and renewing these contracts"）
- 2026-09-17｜Kimberly Fields｜capital_allocation：鎳超合金重熔設備已進入試車，初熔設備明年底試車（原話："we are in commissioning for the remelt assets today"）
- 2026-09-17｜Kimberly Fields｜capital_allocation：擴產順序：先以 Elevation 擠出現有資產產能，再與客戶談新產能（原話："First thing we do is we start with Elevation."）
- 2026-09-17｜Kimberly Fields｜customer：客戶出資換取工程資源優先排序，加速新資產認證（原話："the scarce resource they have is their engineering talent"）
- 2026-09-17｜Kimberly Fields｜customer：客戶為搶產能願意接受漲價；噴射引擎與其他市場的獲利差距在縮小（原話："narrowing of the gap between jet engine and our"）
- 2026-09-17｜Kimberly Fields｜customer：客戶分散供應商而要求 ATI 認證，仍見市占與 mix 改善（原話："still seeing share gains, mix improvements"）
- 2026-09-17｜Kimberly Fields｜customer：國防上季成長 36%，飛彈成長 4 倍，Tomahawk 與 THAAD 開始下單（原話："Defense, defense has been a bright spot."）
- 2026-09-17｜Kimberly Fields｜customer：噴射引擎業務目前 50% 為 MRO（原話："jet engine being 50% MRO today for us"）
- 2026-09-17｜Kimberly Fields｜competition：熱區 7 種專有合金中 ATI 獨家供應 5 種（原話："We make 5 of them sole-source providers"）
- 2026-09-17｜Kimberly Fields｜competition：ATI 是全球兩家具等溫鍛造能力之一（原話："We're 1 of 2 globally that have that capability."）
- 2026-09-17｜Kimberly Fields｜competition：鉿鋯為三家西方合格供應商之一，且是唯一無自有商用核能業務者（原話："We're the only independent."）
- 2026-09-17｜Kimberly Fields｜competition：對 GE 收購 CPP 的看法：ATI 不做鑄件、不供貨 CPP，影響很小（原話："we don't really supply to CPP at all"）
- 2026-09-17｜Kimberly Fields｜product：Richland 新鈦資產正在認證（原話："qualifying our new asset that we just brought online"）
- 2026-09-17｜Kimberly Fields｜product：太空應用目前占比仍小，管理層預期大幅成長（原話："Small today, still a very small part."）
- 2026-09-17｜Kimberly Fields｜risk：中國貿易限制（含鉿鋯）被管理層視為價格與 mix 的背景因素（原話："trade restrictions with China"）
- 2026-09-17｜Kimberly Fields｜product：管理層稱現有 HPMC 與 AA&S 兩個利潤結構相近的成長引擎（原話："Now we have 2 that are very similar in margin profiles"）

### 問答異常語氣（迴避／改口／保留）
- ATI_Q1_2026_Earnings_Call_20260430.md｜問：Strauss：EBITDA 財測上調的來源為何（分部利潤率指引幾乎未變）｜答法：CFO 回答對財測有信心，稱終端市場成長指引未改、偏向國防與噴射引擎區間上緣，未量化 3,500 萬美元上調的拆解
- ATI_Q1_2026_Earnings_Call_20260430.md｜問：Safran：規劃中的產能擴充與上線時程｜答法：僅重述既有鈦與鎳投資按期，表示未到可宣布新重大專案的階段，不給新增產能數字
- ATI_Q1_2026_Earnings_Call_20260430.md｜問：Khanna：2027 年增量利潤率框架｜答法：CFO 不談 2027 細節，僅表示偏向既有 2027 指引區間上緣，更新留待 Q4
- ATI_Q1_2026_Earnings_Call_20260430.md｜問：Walton：向 CFO 詢問 2026 關稅展望為正或負｜答法：由 CEO 接話答「status quo」與全數轉嫁，未給正負或金額

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 3 |
| supply_demand_durability | found | 7 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 2 |
| substitute_technology | found | 3 | 4 |
| channel_business_model_shift | none | 0 | 4 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 1 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：ATI Inc. antitrust OR monopoly investigation 2026；ATI Inc. specialty materials regulation OR regulatory scrutiny 2026 titanium nickel tariff；ATI Inc. DOJ OR FTC OR EU competition 2026
- **channel_business_model_shift**（none）：ATI Inc. distribution channel shift 2026；ATI Inc. business model transition long-term agreements aerospace 2026；ATI Inc. go-to-market change 2026 specialty materials；specialty metals direct-to-customer disintermediation distributors titanium nickel 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"B（衛星候選·thesis 完整 Q1 26 Adj EPS $1.00 +39% Beat / HPMC margin 24.9% +250bp / AA&S 18.1% +320bp / FY26 guide raised Adj EBITDA $1.010-1.060B + Adj EPS $4.20-4.48 / Bakers South VIM 2H 2027 +8-10% / $1.20B buyback expanded；但 HPMC margin vs CRS SAO 35.6% 差距 11pp 反映議價權較弱 + AA&S 非純航太業務拖累；估值🟡 Fwd PE 28.4x（FY27, 5Y 分位 64%）+ PEG 1.29 合理 + Pure MA ✅ 強勢進場 W250 +14.2%；R:R 短期負追高風險；等回測 BB 中軌 $146 再加碼）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"HPMC adj segment margin 達 normalised 25%+ baseline（從 FY22 ~8% 升至 FY26 Q1 24.9%）","columns":{"2Y 驗證點":"FY27-28 HPMC margin TTM 維持 23-27%","5Y 驗證點":"FY30 HPMC margin ≥ 22%（Bakers South 上線後產能稀釋 ~2-3pp）","10Y 驗證點":"FY35 normalised HPMC margin ≥ 18%","具體數字門檻":"2Y: 連 4 季 TTM ≥ 23%；5Y: 滾動 8 季均 ≥ 22%","信息來源":"Q1 FY26 法說 + Bernstein 2025 投資人簡報 + mgmt guidance","漂移觸發條件":"連 4 季 TTM"}},{"id":"H2","text":"Bakers South VIM 2H 2027 commission on schedule + 80% LTA 鎖定不變","columns":{"2Y 驗證點":"2026 Q2-Q4 commission ETA 維持 2H 2027 + LTA 比例 ≥ 75%","5Y 驗證點":"FY28-30 Bakers South ramp 達 management guided rate（+8-10% capacity = +$300-400M Rev）","10Y 驗證點":"2030+ 新容量在下次 cycle 仍 ≥ 70% utilization","具體數字門檻":"2Y: 季度 capex 維持 $70-90M/qtr (FY26 high $300s annual)；5Y: incremental Rev ≥ $300M","信息來源":"2026-04 metalnomist 確認 +9,000 tonnes/yr + 2H 2027 + 80% LTA secured","漂移觸發條件":"commission 延後 > 6 個月 或 LTA 比例"}},{"id":"H3","text":"AA&S margin 維持 ≥ 15%（從 FY22 ~5% 升至 FY26 Q1 18.1%）— 不會在 cycle 反轉時急轉直下","columns":{"2Y 驗證點":"FY27-28 AA&S margin TTM 維持 15-18%","5Y 驗證點":"FY30 AA&S margin ≥ 13%（即使工業景氣放緩）","10Y 驗證點":"FY35 AA&S 或被分拆 / 維持 ≥ 10%","具體數字門檻":"2Y: 連 2 季 TTM","信息來源":"Q1 FY26 法說 + 10-K 細分","漂移觸發條件":"連 2 季 TTM"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Pratt & Whitney GTF 供應問題持續影響 Airbus（2026/02/05 仍無 2026-27 供應協議）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Airbus monthly A320neo delivery + Pratt GTF resolution timeline","警戒閾值":"連 2 季 Airbus monthly delivery"}},{"id":"R2","text":"HPMC margin reversion + AA&S margin 雙重壓縮","columns":{"對應假設":"H1 + H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"HPMC 季度 adj margin + AA&S 季度 adj margin（TTM 化避免季節 noise）","警戒閾值":"HPMC 連 4 季"}},{"id":"R3","text":"下一輪航太 cycle 反轉（FY29-32 期間 EPS 可能下修 40-60%）","columns":{"對應假設":"H1 + H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"Boeing/Airbus order intake + IATA RPK growth + 全球商用機 backlog","警戒閾值":"需 ≥ 50% 機率才砍倉；backlog 從 14 年降至"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":153.55,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ATI","date":"2026-10-13","schema":"v15.2","contract":"v19","company_name":"ATI Inc."},"oneliner":"航太熱區合金與鉿鋯稀缺讓 ATI 兩大事業利潤率同步創高、全年指引兩度上修，護城河在擴大；但股價已是 2027 年共識 29.5 倍、2026 年 36.7 倍，基準情境五年年化僅約 3.5%，等回到約 153 美元再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261013/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261013/scenario.json","answers":{"q1_business":{"verdict":"賺航太引擎與機身製造商、海軍核能與飛彈計畫的錢：靠少數合格廠才做得出的鎳基超合金、高階鈦、等溫鍛件與高純度鉿鋯收稀缺溢價，錢卡在熔煉與客戶認證產能這一節點","reasoning":"兩個分部各占約一半營收。Q2 2026 營收 12.61 億美元（年增 11%），調整後 EBITDA 2.84 億美元、利潤率 22.6%（年增 440 個基點，2007 年以來最強單季），GAAP 營業利益 2.2 億美元（約 17.4%，含 990 萬美元廠房出售利得與 2,360 萬美元特殊費用）；近四季毛利率 23.4%、營業利益率 15.2%。HPMC 營收 6.37 億美元（年增 5%），分部利潤率 24.1%，約 93% 來自航太國防；AA&S 營收 6.24 億美元（年增 17%），分部利潤率 23.7% 創新高，航太國防占 44%。終端市場：噴射引擎年增 13%（其中一半為維修件）、國防年增 36%（飛彈營收四倍）、特殊能源年減 6%（產能讓給海軍核能）、機身小降。積壓訂單 44 億美元創高（年增 18%），約七成 12 個月內轉營收。產業位置屬擴張期：引擎 OEM 上半年出貨大增、交期拉長，但 Airbus A320 月產 75 架延到 2027 年，製造端仍在爬坡。供需屬結構性持久至 2027–2028 年，之後同業與 OEM 新產能投產、供給可逆性中等。單點依賴：HPMC 高度集中航太國防，客戶為少數大廠，但無單一客戶超過營收 10%，五種獨家合金是集中度的對價。","fact_refs":["f_kpi0_sales_gaap","f_kpi1_adjusted_ebitda_non_gaap","f_kpi2_operating_income_gaap","f_kpi5_backlog","f_peer_ati_gross_margin_pct","f_peer_ati_operating_margin_pct","f_kpi6_guidance_q3_2026","f_kpi7_guidance_fy2026"],"verdict_values":{"revenue_quality":"約七成積壓訂單 12 個月內轉營收，長約、獨家供應與客戶出資擴產比重提高；引擎業務一半為維修件，比新機出貨穩；特殊能源與國防訂單呈塊狀","unit_econ_note":"全年增量利潤率由 40% 上調到約 50%；Q2 遞延的 HPMC 出貨增量利潤率 40–50%；海軍核能新約五年約 10 億美元、為前約兩倍，增幅三分之二來自價格與組合","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"航太循環擴張段加上長約價格重設，利潤率創 2007 年以來新高；客戶認證門檻帶來部分品質特徵，但歷史上隨航太循環大起大落"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久至 2027–2028 年：引擎 OEM 2026 上半年出貨大增，鎳合金交期約 12 個月、高階鈦 20 個月、等溫鍛件逾 24 個月，航空級鈦錠報價交期 3–6 個月（Argus 2026-08；Q2 2026 法說）；之後新合金產能 2027 下半年至 2030 年陸續投產、引擎瓶頸已見緩解，供給可逆性中等","bargaining":{"up":"鎳、海綿鈦、鈷、鉻鐵多自國外採購（鎳來自加拿大、挪威、日本等；海綿鈦來自日本、哈薩克、沙烏地、中國），通膨與關稅成本透過合約轉嫁","down":"客戶為 Boeing、Airbus、GE、Rolls-Royce、Pratt & Whitney、Safran 等少數大廠，HPMC 約 92–93% 營收來自航太國防，但無單一客戶超過營收 10%；七種先進鎳合金做六種、五種獨家，客戶為搶產能接受漲價並出資擴產","geo":"中國限制鉿、鋯出口，ATI 是西方三家合格廠中唯一沒有自有商用核能業務的獨立供應商，價格順風；同一批中國出口管制也是原料端延遲風險；持有中國合資 STAL 60%"},"profit_pool_dir":"利潤池往熔煉、熱區合金與後段檢測、等溫鍛造集中（目前瓶頸所在）；2027 下半年起新產能投產後可能回流引擎 OEM","tam_table":{"expanded":false,"reason":"成長來自既有市場的價格重設與自有產能擴充，不是低滲透或新品類；可用的規模訊號只有新世代引擎占機隊比重（約 35% 升至 2030 年逾 50%），已寫在成長段，市場總額事實表未涵蓋"}}}},"q2_moat":{"verdict":"護城河擴大、評 B 級：熱區鎳合金獨家供應與多年客戶認證，讓 ATI 在產能吃緊時拿到漲價，執行面與定價面同步擴大；但利潤率仍落後 Howmet 與 Carpenter，部分定價權來自本輪週期性稀缺","reasoning":"機制：熱區合金與等溫鍛件需要多年客戶認證，ATI 生產七種最先進引擎鎳合金中的六種、五種為獨家，是全球兩家具等溫鍛造能力之一，也是西方三家合格的高純度鉿鋯供應商之一。方向：執行面擴大（超音波檢測產能年增 30%、等溫鍛造與一次鎳熔煉各增 15%），定價面擴大（海軍核能新約年營收翻倍、三分之二來自價格與組合；客戶為搶產能接受漲價；交期鎳合金 12 個月、高階鈦 20 個月、等溫鍛件逾 24 個月），因此判擴大。限制：近四季營業利益率 15.2%，仍落後 Carpenter 22.5% 與 Howmet 27.3%，同業差距的歷史方向事實表未涵蓋，合併分不給到 8 分以上；部分定價權來自本輪產能吃緊，2027 下半年起同業擴產後要重驗。執行 8 分、定價 7 分。","fact_refs":["f_peer_ati_operating_margin_pct","f_peer_hwm_operating_margin_pct","f_peer_crs_operating_margin_pct","f_peer_ati_gross_margin_pct","f_peer_hwm_gross_margin_pct","f_peer_crs_gross_margin_pct","f_peer_ati_fcf_margin_pct","f_peer_hwm_fcf_margin_pct","f_peer_crs_fcf_margin_pct","f_peer_cstm_operating_margin_pct","f_peer_mtrn_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"認證型轉換成本加稀缺產能：引擎熱區合金與等溫鍛件換供應商需重新認證、週期以年計；七種先進鎳合金做六種、五種獨家；全球兩家具等溫鍛造能力之一；西方三家合格鉿鋯廠之一","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"定價：Q2 AA&S 利潤率年增 930 個基點至 23.7%，海軍核能新約年營收翻倍且三分之二來自價格組合，客戶為搶產能接受漲價，年底前續約重設（2026-09-17 Laguna 會議）；執行：超音波檢測產能年增 30%、等溫鍛造與一次鎳熔煉各 15%；份額：管理層稱客戶分散供應商時 ATI 仍見市占與組合改善。反向：營業利益率 ATI 15.2% 對 Carpenter 22.5%、Howmet 27.3%，差距歷史趨勢事實表未涵蓋","competitor_notes":[{"name":"HWM","strategy_note":"利潤率最高的直接對手（近四季營業利益率 27.3%、FCF 率 19.6%），在鈦合金與鍛件正面競爭，是 ATI 拉近利潤率的標竿"},{"name":"CRS","strategy_note":"傳統鎳基與特殊鋼主要對手，營業利益率 22.5%，2026 年資本支出 2.2–2.4 億美元投向引擎合金，是產能吃緊何時結束的最大變數"},{"name":"CSTM","strategy_note":"以鋁材為主，營業利益率 8.5%，與 ATI 熱區合金重疊有限，屬較低利潤層級"},{"name":"MTRN","strategy_note":"特殊合金與電子材料，營業利益率 6.4%，與 ATI 引擎合金重疊有限"},{"name":"Precision Castparts","strategy_note":"鑄件與精密鍛件大廠；管理層稱 ATI 不做鑄件、也幾乎不供貨給 CPP，其所有權變動對 ATI 影響小（2026-09-17）"}],"threats":[{"level":"🟡","text":"Carpenter 與引擎 OEM 擴充熔煉、鍛造產能或鎖定既有供給，2027 下半年至 2030 年陸續投產，產能吃緊帶來的漲價空間可能收斂；屬點對點競爭","p":"35%","evidence_refs":["competitive_share_entrants#3","supply_demand_durability#6"]},{"level":"🟡","text":"替代材料與積層製造：10-K 長年把替代材料列為風險因子；GKN 與美國空軍 840 萬美元計畫推進線材雷射沉積的大型鈦機身結構，屬鈦鍛件的近淨形補充路徑，量級尚小","p":"10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉（調整後 EBITDA 利潤率約 22%、營運資金約營收 34%，重資產；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是引擎與機身製造商，決策者是其材料工程與採購，付款者最終是航空公司與國防預算；新世代引擎 ATI 含量為舊機兩倍，引擎業務一半為維修件，延後購買等於飛機停飛，代價高；Airbus 2025 年底積壓 8,754 架"},{"item":"決策層級","level":"🟢","text":"替代性要在單一零件的合金認證層級衡量：熱區合金換供應商需重新認證、週期以年計，客戶甚至出資並調派工程人力協助認證新資產；七種先進鎳合金中五種獨家，零件層級幾乎無替代"},{"item":"價值鏈分配","level":"🟡","text":"目前瓶頸在熔煉與後段檢測、等溫鍛造，ATI 拿到漲價；但 GE 稱限制在供給端，OEM 與同業正擴產或鎖定供給，2027 下半年後瓶頸若移轉，價值會回流 OEM；長期需求存在不等於這一環節能一直多拿"},{"item":"社會容忍度","level":"🟢","text":"買方為大型企業與政府，未見政治或社會壓價訊號；海軍核能新約經談判後價格上調（年營收翻倍）；中國限制鉿鋯出口反而提高西方合格供應商的價值"}],"roiic":"約 30%（以管理層資本專案 30% IRR 門檻作代理，未計客戶出資；非已實現值）","reinvest_rate":"約 30%（粗估：2026 年淨資本支出約 2.3 億美元扣折舊約 1.65 億，加營運資金增量約 1.7 億，對稅後營業利益約 7.8 億美元）","endo_ceiling":9,"formula_note":"內生成長率＝增量報酬 30%×再投資率 30%，約 9%。輸入：資本支出總額 2.8–3.0 億美元扣客戶出資 5,500–6,500 萬；折舊由 Q2 調整後 EBITDA 2.844 億減 GAAP 營業利益 2.2 億加特殊費用 2,360 萬回推約 4,100 萬美元／季；營運資金以營收 34% 乘 FY2027 共識營收增量約 5 億美元；稅後營業利益以 2026 年 EBITDA 指引中點 11.6 億扣折舊、假設稅率 22%。當期 ROIC 與投入資本事實表未涵蓋。2026 年獲利跳升主要來自價格重設、不需新增資本，不計入內生成長"}}}},"q3_growth":{"verdict":"五年後成長空間中等：新世代引擎占機隊比重由約 35% 升至 2030 年逾 50%、鎳產能 2028 年初增 15–20%，五年內成長有據；但五年後機隊滲透落入 35–70% 區間，國防與太空尚不足以構成第二條曲線","reasoning":"成長是價先於量：2026 年指引調整後 EPS 中點 5.04（年增 56%），共識營收 FY2026 約 51.4 億美元、年增約 12%，差距來自長約重設、組合與約 50% 的增量利潤率；2027–2028 年轉為量，鎳產能 2028 年初較 2025 年底增 15–20%、新增年營收約 3.5 億美元，新世代引擎 ATI 含量為舊機兩倍。共識三年 EPS 由 FY2025 調整後約 3.23 到 FY2028 7.50，年化約 32%；扣掉 2026 年跳升，FY2026→FY2028 年化約 21%，營收 FY2026→FY2027 年增約 10%。內生上界約 9%（見競爭優勢段），缺口約 12 個百分點：利潤率擴張約 10–11 個百分點、淨回購約 1 個百分點，可歸因，但屬週期高點的利潤率，不外推到 2028 年後。成長空間：新世代引擎機隊比重 2030 年過半，五年後落在 35–70% 區間；國防（飛彈、海軍核能）與太空有成長但規模尚小。衰退信號十類亮一個：EPS 成長率高於營收逾 5 個百分點。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_backlog","f_kpi7_guidance_fy2026"],"verdict_values":{"growth":{"driver_mix":"價為主、量為輔：2026 年靠長約漲價、組合與 50% 增量利潤率；2027–2028 年轉向鎳擴產帶來的量（約 3.5 億美元新增營收）；淨回購每年約 1%；無併購","runway_years":5,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 9%（增量報酬 30%×再投資率 30%）；共識 FY2026→FY2028 EPS 年化約 21%，缺口約 12 個百分點歸因利潤率擴張（合約價格重設、增量利潤率 50%）與淨回購，可歸因但屬週期高點，不能外推到 2028 年後","segments":[{"item":"HPMC（高性能材料與零組件）","value":"Q2 2026 營收 6.37 億美元（年增 5%），分部利潤率 24.1%；約 93% 來自航太國防；全年利潤率指引 25% 上下；墨西哥新廠與 EB2 認證延後遞延 3,000–4,000 萬美元出貨"},{"item":"AA&S（先進合金與解決方案）","value":"Q2 2026 營收 6.24 億美元（年增 17%），分部利潤率 23.7% 創新高（年增 930 個基點）；航太國防占 44%、年增 34%；全年指引 20% 出頭，管理層稱中長期 25% 上下"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"年度毛利率由 18.6% 逐年升至 22.0%，近四季 23.4%"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱仍有市占與組合改善，未見第三方反證"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"特殊能源年減 6% 為產能讓給海軍核能，非價格造成"},{"item":"EPS 成長率高於營收逾 5 個百分點","lit":true,"note":"2026 年 EPS 指引年增約 56%、營收約 12%；FY2026→FY2028 EPS 年化 21% 對營收約 10%"},{"item":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2023、2024 年曾低於，2025 年回到約 0.83"},{"item":"SBC／營收逾 5% 且上升","lit":false,"note":"約 0.6%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"積層製造屬長期補充路徑，量級小"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"ATI 自身倍數處近四年高點；同業倍數事實表未涵蓋"},{"item":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"回推折舊約 1.65 億美元對 2026 年 FCF 指引中點 5.75 億，約三成"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"鎳、鈦與墨西哥廠擴產進行中"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"中等：回購為唯一股東回饋、無股息、無併購；SBC 稀釋極低，但近期回購在本益比 30 倍以上執行，買入收益率偏低","reasoning":"現金流轉好但仍在爬坡：FCF 2022–2025 年分別為 0.94、−1.15、1.68、3.34 億美元，對淨利轉換率由負值升到 2025 年約 0.83；2026 年指引調整後 FCF 5.5–6 億美元（上半年 1.43 億，下半年需約 4.3 億），管理層目標轉換率 90% 以上。資本支出總額 2.8–3.0 億美元、其中 5,500–6,500 萬由客戶出資；新專案門檻 30% IRR。股東回饋只有回購：Q1 7,500 萬、Q2 5,000 萬美元，剩餘授權 4.95 億美元，無股息、近期無併購。SBC 上半年 1,410 萬美元，約營收 0.6%。淨負債 14.09 億美元，債務到期結構與利率事實表未涵蓋。營運槓桿為正：Q2 營收年增 11%、調整後 EBITDA 年增 37%。扣分在回購價位：在 FY2026 本益比 30 倍以上買回，盈餘殖利率約 3%。","fact_refs":["f_kpi3_adjusted_free_cash_flow","f_kpi4_sbc_0_6","f_net_debt_m","f_dividend_yield_ttm","f_kpi7_guidance_fy2026","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近三年未見併購（事件掃描無併購紀錄），不適用"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購均價事實表未涵蓋；以現價對 FY2026 共識 5.12 計盈餘殖利率約 2.7%，即使十年期殖利率只有 1%，門檻也有 3%，不過；上半年回購 1.25 億美元"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"上半年 SBC 1,410 萬美元，約營收 0.6%、年化約市值 0.1%，遠低於每年 1.5% 稀釋上限"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠定價重設與自有產能擴充，事件掃描未見併購；股東回饋只有回購，已在回購買入收益率一項處理"}}}},"q5_valuation":{"verdict":"現價要求 2026 年的漲價紅利在 2027 年全年生效、2028 年鎳擴產如期貢獻，而且 2031 年前不碰上航太下行；我只信到基準情境，五年年化約 3.5%，偏貴，等回到約 153 美元（FY2027 共識 24 倍）","reasoning":"以 FY2031 EPS 9.30、24 倍終端本益比的基準情境，五年終值約 223 美元、年化約 3.5%；要拿到 8% 年化，24 倍下 FY2031 EPS 須達約 11.5 美元（2026→2031 年化約 17.6%），等於多頭情境。2027 年有合約撐，我信；2028 年後利潤率屬週期高點，我不信能一路外推。賣方平均目標價依來源 177–232 美元，現價落在區間內，不提供安全邊際。同業本益比事實表未涵蓋，終端倍數缺少同業錨，改以 ATI 自身 FY2027 本益比 29.5 倍與前份 28.4 倍為參照。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_ev_s_current","f_ev_s_fwd","f_ps_percentile"],"verdict_values":{"valuation":{"basis":"FY2027 共識預估本益比為主尺、PEG 為輔（品質轉型中的循環股；淨值比事實表未涵蓋）","tier":"航太特殊材料（與 Howmet、Carpenter 同層；Constellium、Materion 利潤率低一層，不作錨）","peers":{"expanded":false,"reason":"事實表只有同業利潤率（Howmet、Carpenter、Constellium、Materion），沒有同業本益比，無法建倍數對照；終端倍數改以 ATI 自身 FY2027 本益比與前份倍數為錨，屬資料缺口"},"fwd_pe":36.71,"peg":1.13,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價 187.98 對 FY2026 共識 5.12 為 36.7 倍、對 FY2027 6.37 為 29.5 倍；追蹤本益比 55.1 倍高於近四個年度端點全部（五年高低點事實表未涵蓋，分位留空）；PEG 以 FY2025 調整後 EPS 約 3.23 到 FY2028 共識 7.50 的三年年化 32% 計約 1.13，扣掉 2026 年跳升後 FY2026→FY2028 年化 21%，對應約 1.75；基準情境五年年化約 3.5%；賣方平均目標價 177–232 美元與現價相近。倍數不算離譜，但五年報酬回推偏低，判偏貴","upside_short_pct":2.4,"upside_mid_pct":18.7,"denominator_disputed":false,"denominator_note":"分母採 FY2026 共識 EPS 5.12（36.7 倍），並以 FY2027 共識 6.37（29.5 倍）對照；追蹤本益比 55.1 倍落在 2026 年 EPS 跳升之前的低基期，故改用前瞻分母；含與不含 2026 年跳升的成長差異已在 PEG 拆解中列出（1.13／1.75），分母本身不構成爭點。"}}},"q6_how_wrong":{"verdict":"中度風險：最可能看錯在把 2026 年的漲價紅利當成新常態；若 2027 下半年起同業與 OEM 新產能投產、交期縮短，利潤率回落而倍數仍在 30 倍上下，股價可跌四到六成","reasoning":"最強三個反駁：一，定價權有一部分是週期性稀缺，Argus 已指引擎瓶頸緩解，Carpenter 與 OEM 擴產 2027 下半年起投產，續約漲價可能在 2028 年後停止；二，HPMC 新產能（墨西哥廠、EB2）認證延誤已遞延 3,000–4,000 萬美元出貨，最大成長平台的執行仍有變數；三，追蹤本益比 55 倍、FY2027 29.5 倍，近三個月 FY2026 共識已上修 14.5%，市場已計入 13.5 億美元年化 EBITDA。另有退休金義務轉移集體訴訟未決（金額未揭露），屬財務尾部風險。熊市情境五年跌約 58%，路徑上可能回撤四到六成。","fact_refs":["f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點利潤率外推"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.12,"pe":36.71,"basis":"FY2026 共識調整後 EPS（FY1）；終端倍數同樣乘在終端年度 FY2031 的全年調整後 EPS；回購效果已含在 EPS 路徑內，淨回購殖利率填 0 避免重複計算"},"eps":{"bull":[6.9,8.2,9.4,10.5,11.6],"base":[6.4,7.4,8.05,8.65,9.3],"bear":[5.8,5.4,4.4,4.7,5.3]},"pe":{"bull":30,"base":24,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-65,"hi":-35,"basis":"高點 −35%：EPS 照共識、FY2027 本益比由 29.5 倍回到約 19 倍（約 121 美元），屬循環股常見的去倍數；低點 −65%：同業新產能投產加航太下行讓 EPS 回落到約 4.4、本益比壓到 15 倍（約 66 美元）。熊市終點跌幅約 58% 落在範圍內；ATI 歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"2027 年價格重設全年生效、增量利潤率維持 50%，鎳擴產 2028 年如期貢獻、航太循環延續到 2031 年，市場給 30 倍品質航太倍數","base":"2027 年 EPS 約等於共識，2028 年鎳擴產貢獻後成長放緩到每年 7–8%，利潤率持平於 2027 年水準，本益比由 36.7 倍收斂到 24 倍","bear":"2027 下半年起同業與 OEM 新產能投產、交期縮短、續約漲價停止，2029 年航太下行使 EPS 回落到約 4.4，本益比壓到 15 倍（成長熄火降至 10% 以下的倍數）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Argus 指引擎瓶頸正在緩解；同業與引擎 OEM 擴熔煉、鍛造產能於 2027 下半年至 2030 年投產；Carpenter 2026 年資本支出 2.2–2.4 億美元；HPMC 約 92–93% 營收集中航太國防","assumption":"交期縮短、年底後續約價格持平或下修，同時航太循環在 2029–2031 年反轉","consequence":"EPS 由 2027 年約 6.4 回落至 4.5 上下、本益比壓到 15 倍，股價約 70–80 美元，五年虧 55–60%","ruling":"採納為熊市情境，機率 30%；與唯一致命點部分重疊（價格重設），已回補成交期與積壓訂單觸發器","watch":"鎳合金交期（現約 12 個月）、高階鈦交期（20 個月）、季度積壓訂單年增率（現 +18%）","evidence_refs":["supply_demand_durability#6","competitive_share_entrants#3","customer_concentration_credit#0"],"fact_refs":["f_kpi5_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"成長靠重資產擴產（2026 年資本支出總額 2.8–3.0 億美元、營運資金約營收 34%），並在 30 倍以上本益比回購（上半年 1.25 億美元）；退休金義務轉移集體訴訟未決","assumption":"營收成長兌現，但新增產能報酬低於 30% 門檻、回購價格過高、訴訟和解吃掉部分現金，每股價值成長慢於營收","consequence":"FCF 轉換率停在 80% 上下，回購盈餘殖利率約 3% 拉低股東報酬","ruling":"部分採納：客戶出資約兩成資本支出與 30% IRR 門檻降低擴產風險，但回購時點不佳列為資本配置扣分；訴訟金額未揭露，列觸發器","watch":"FCF／調整後淨利轉換率（管理層目標 90% 以上）、回購金額對當季本益比、10-Q 法律程序附註","evidence_refs":["major_events#0","lawsuit_class_action#0"],"fact_refs":["f_kpi3_adjusted_free_cash_flow","f_kpi4_sbc_0_6"]},{"view":"價格已反映太多","evidence":"股價 187.98 為 FY2026 共識 36.7 倍、FY2027 29.5 倍，追蹤本益比 55 倍高於近四個年度端點；近三個月 FY2026 共識已上修 14.5%","assumption":"市場已把 Q4 2026 隱含 13.5 億美元年化 EBITDA 與 2028 年鎳擴產全數計入","consequence":"基準情境五年終值約 223 美元、年化約 3.5%；即使結果符合預期，報酬也平庸","ruling":"採納：這是本次不追價的主因","watch":"FY2027 本益比回到 24 倍以下（約 153 美元），或 2027 指引大幅高於共識使倍數自然下降","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 153.55 → 本次 187.98（+22.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=153.55","side_b":"本次 price_at_dd=187.98","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 153.55 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 153.55 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 153.55 美元：Bull 價 348、Bear 價 79.5，五年期望值 +37.6%，基準年化 7.8%，不對稱比 2.19","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.19。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 153.55 美元：五年期望值 +37.6%，基準年化 7.8%，不對稱比 2.19","side_b":"本次情境、股價 187.98 美元：五年期望值 +12.4%，基準年化 3.5%，不對稱比 1.23","ruling":"再換股價、情境不動：起點價上漲 22.4%，五年期望值少 25.2 個百分點，基準年化少 4.3 個百分點，不對稱比由 2.19 降到 1.23。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"定價權持續性","cause":null,"prior_field":null,"side_a":"管理層：定價屬長期合約內建、非短期稀缺（2026-04-30 Q1 法說 CEO）；Q2 法說稱最差異化產品交期仍在拉長，鎳合金 12 個月、高階鈦 20 個月、等溫鍛件逾 24 個月","side_b":"Argus（2026-08）：引擎瓶頸正在緩解；同業與 OEM 擴產 2027 下半年至 2030 年投產，Carpenter 2026 年資本支出 2.2–2.4 億美元","ruling":"不可調和（方向相反），依時間切開裁決：2026–2027 年採管理層一側，依據是 Q2 實際交期數字與已簽續約；2028 年後採 Argus 一側，熊市機率 30% 即反映此風險","evidence_level":"法說實際數字對第三方產業報導","settle_metric":"鎳合金與高階鈦交期、季度積壓訂單年增率","if_then":["若 2027 年任兩季鎳合金交期縮短至 9 個月以下且積壓訂單年增轉負 → 已持有部位減碼一半","反向：若 2027 年中交期仍 ≥ 12 個月且新續約價格續漲 → 熊市機率下調至 25%，股價 ≤ 165 美元即分批反買首筆"],"evidence_refs":["supply_demand_durability#6","competitive_share_entrants#3"]},{"axis":"觀望的最強反方（現在就買的論證）","cause":null,"prior_field":null,"side_a":"現在就買：Q3 EPS 指引 1.31–1.37 遠高於事前共識 1.12；Q4 隱含 13.5 億美元年化 EBITDA，若增量利潤率維持 50%，FY2027 EPS 可能落在 6.8 上下、高於共識 6.37；近三個月共識上修 14.5%；前份等 146 美元，股價反而漲 22%","side_b":"即使 FY2027 EPS 達 6.8，現價仍是 27.6 倍；基準情境五年年化約 3.5%；利潤率處 2007 年以來高點，2028 年後供給轉鬆","ruling":"維持觀望；約束只有一個：價格。多頭情境 25% 已涵蓋上修路徑，另設 2027 指引 EPS ≥ 7 美元時可在 175 美元以下分批反買的條件","evidence_level":"公司指引與共識快照","settle_metric":"2027 指引 EPS 與 EBITDA 中點","if_then":["若 2027 指引 EPS 中點 ≥ 7.0 美元且股價 ≤ 175 美元 → 分批反買首筆","反向：若股價續漲而 2027 指引只等於共識 → 不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"管理層承諾對帳","cause":null,"prior_field":null,"side_a":"2026-04-30 Q1 法說（CEO Fields、CFO Foster）：Q2 EBITDA 指引 2.45–2.55 億美元、全年 10.1–10.6 億、AA&S 全年利潤率高 10% 段、增量利潤率 40%、2026 年每季 FCF 為正","side_b":"2026-08-06 Q2 法說：Q2 實際 2.84 億美元，全年上修至 11.35–11.85 億，AA&S 改為 20% 出頭、增量利潤率 50%，Q1、Q2 FCF 皆為正；但 HPMC 因墨西哥廠與 EB2 認證延後，遞延 3,000–4,000 萬美元出貨，Q1 時未預告","ruling":"可調和：整體可信度上升；HPMC 新產能認證時程是唯一落空項，列短期風險監測","evidence_level":"公司兩季法說原文","settle_metric":"Q3＋Q4 2026 HPMC 季營收","if_then":["若 Q3＋Q4 2026 HPMC 平均營收低於 6.5 億美元 → 停止加碼並調降管理層指引的可信度"],"evidence_refs":["supply_demand_durability#6"]},{"axis":"產業態勢（競爭／結構／其他）","cause":null,"prior_field":null,"side_a":"競爭惡化訊號：Carpenter 擴產、OEM 鎖定供給、引擎瓶頸緩解，主要在 2027 下半年後發酵；其他結構變數：積層製造長期補充鈦鍛件、原料進口與中國出口管制、中國合資 STAL、退休金集體訴訟","side_b":"結構轉好：交期拉長、五種獨家合金、新世代引擎含量兩倍、中國限制鉿鋯出口提高西方供應商價值、海軍核能新約翻倍","ruling":"雙向拉鋸：2026–2027 年結構性轉好占上風，2028 年後競爭供給增加可能轉為主導","evidence_level":"公司揭露與第三方報導","settle_metric":"交期與續約價格","if_then":["若 2028 年前已出現兩家以上新合格熔煉供應商且交期縮短 → 減碼"],"evidence_refs":["competitive_share_entrants#3","substitute_technology#1","reg_tariff_export#2"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["archetype","cycle_position","moat_trend","runway_post_y5"],"side_a":"前份未填 DCA 結論、DCA 角色、公司類型、循環位置、護城河方向與五年後成長空間（皆空白）","side_b":"本次：公司類型判循環/商品、輔以品質複利成長；循環位置中循環；護城河方向擴大；五年後成長空間中等；DCA 兩欄本次仍不適用","ruling":"屬方法補齊而非看法改變；護城河擴大的依據是本季漲價與產能提升的新數字","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"價值陷阱風險","cause":"方法變動","prior_field":["trap"],"side_a":"前份 🟢","side_b":"本次 🟡：十類衰退信號亮一個，2026 年 EPS 指引年增約 56%、營收約 12%，差距逾 5 個百分點","ruling":"前份 EPS 指引 4.20–4.48 已高於營收成長，本次按同一清單逐項計數才亮燈，屬方法變動；亮燈原因是利潤率擴張而非需求衰退，風險在週期高點外推","evidence_level":"公司指引","settle_metric":"EPS 與營收成長率差距","if_then":["若 2027 年 EPS 與營收成長率差距收斂至 5 個百分點內且利潤率不降 → 改回 🟢"],"evidence_refs":[]},{"axis":"估值結論","cause":"方法變動","prior_field":["val"],"side_a":"前份 🟡：FY27 預估本益比 28.4 倍、五年分位 64%、PEG 1.29，股價 153.55","side_b":"本次 🟠：FY2027 共識本益比 29.5 倍幾乎未變，但改以五年情境回推，基準情境（FY2031 EPS 9.30、24 倍）年化約 3.5%，且扣掉 2026 年跳升後 PEG 約 1.75","ruling":"倍數只小升，偏貴判斷主要來自本輪改以五年報酬回推並排除 2026 年一次性跳升；採本次結論","evidence_level":"方法","settle_metric":"FY2027 本益比與基準情境年化報酬","if_then":["若 2027 指引使 FY2027 EPS 達 7 美元以上而股價不動（本益比降到 27 倍以下）→ 估值結論改回合理，按重新進場條件執行"],"evidence_refs":[]},{"axis":"綜合評級","cause":"價格變動","prior_field":["signal"],"side_a":"前份評級 B，股價 153.55","side_b":"本次維持 B，股價 187.98（+22%）","ruling":"股價上漲與 FY2027 共識由約 5.4 美元（由前份 28.4 倍回推）升到 6.37 大致同步，品質面改善與價格變貴相抵，評級不變","evidence_level":"價格與共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未給情境機率與最大回撤","side_b":"本次多頭 25%、基準 45%、熊市 30%；最大回撤 −35% 至 −65%","ruling":"共識成長率超過內生上界，熊市機率不低於 30%；回撤範圍由熊市低點 EPS 與倍數推出","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場、減碼與清倉門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件與減碼、清倉門檻（空白；文字結論為等回測約 146 美元再加碼）","side_b":"本次重新進場：股價 ≤ 153 美元（FY2027 共識 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元；減碼：AA&S 利潤率連 3 季 < 18%、HPMC 滾動四季 < 22%、或交期縮短加積壓訂單年增轉負連 2 季；清倉：2027 指引 EBITDA 中點 < 13 億美元，或主力機型降產且積壓訂單年減逾 10%","ruling":"前份 146 美元為技術面價位，本次改用 FY2027 共識 24 倍的估值價位，並加上 2027 指引作事件條件；門檻改為可量測的分部利潤率、交期與積壓訂單","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"2027 指引（2026 年 11 月投資人日或 Q4 法說）調整後 EBITDA 中點低於 13 億美元","ruling":"新設 Single Thing：情境樹中最大的單一敏感度是 2027 年價格重設能否全年生效；發生即清倉並取消重新進場條件","evidence_level":"方法","settle_metric":"2027 EBITDA 指引中點","if_then":[],"evidence_refs":[]},{"axis":"假設門檻（AA&S 利潤率）","cause":"新證據","prior_field":["H"],"side_a":"前份：AA&S 利潤率維持 ≥ 15%（連 2 季 TTM 觀察）","side_b":"本次：AA&S 分部利潤率單季 ≥ 20%，連 2 季低於 19% 為削弱、連 3 季低於 18% 減碼","ruling":"Q2 2026 AA&S 利潤率 23.7%（年增 930 個基點），管理層把全年指引由高 10% 段改為 20% 出頭、中長期 25% 上下，門檻跟著上調；15% 已無法偵測結構性轉型失敗","evidence_level":"公司分部資料與法說","settle_metric":"AA&S 分部利潤率","if_then":["若 AA&S 連 3 季低於 18% → 減碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"重新進場：股價回到 153 美元以下（FY2027 共識 6.37 的 24 倍），且 2027 指引 EBITDA 中點不低於 13 億美元，兩者同時成立才重跑判斷後建首筆","type":"估值rearm","maps_to":"H3","metric":"股價對 FY2027 共識本益比＋2027 EBITDA 指引","threshold":"≤ 24 倍（約 153 美元）且指引中點 ≥ 13 億美元","action":"分批反買（首筆，重跑判斷後）","source_freq":"每日股價；指引於 2026-11 投資人日或 2027-02 Q4 法說","date":null,"evidence_refs":[]},{"n":2,"text":"2027 指引調整後 EBITDA 中點低於 13 億美元：取消重新進場條件，熊市機率上調至 40%；若已持有則清倉","type":"Single Thing","maps_to":"H3","metric":"2027 調整後 EBITDA 指引中點","threshold":"< 13 億美元","action":"清倉","source_freq":"一次性：2026-11 投資人日或 2027-02 Q4 法說","date":"2026-11","evidence_refs":[]},{"n":3,"text":"AA&S 分部利潤率連 3 季低於 18%，代表結構性轉型失敗、回到循環事業","type":"減碼","maps_to":"H2","metric":"AA&S 分部利潤率（單季）","threshold":"連 3 季 < 18%","action":"減碼","source_freq":"每季新聞稿","date":null,"evidence_refs":[]},{"n":4,"text":"HPMC 分部利潤率滾動四季低於 22%，或新 VIM 熔煉爐上線較 2027 年底延後逾 6 個月","type":"假設驗證","maps_to":"H1","metric":"HPMC 分部利潤率（滾動四季）／VIM 上線時程","threshold":"< 22% 或延後 > 6 個月","action":"減碼","source_freq":"每季新聞稿與法說","date":null,"evidence_refs":[]},{"n":5,"text":"Q2 遞延的 3,000–4,000 萬美元 HPMC 出貨在下半年未補回，新廠認證延誤擴大","type":"風險","maps_to":"R1","metric":"HPMC 季營收","threshold":"Q3＋Q4 2026 平均 < 6.5 億美元","action":"停止加碼","source_freq":"每季新聞稿","date":"2027-02","evidence_refs":["supply_demand_durability#6"]},{"n":6,"text":"交期縮短加上積壓訂單轉負，代表產能吃緊結束、漲價空間收斂","type":"風險","maps_to":"R2","metric":"鎳合金與高階鈦交期、積壓訂單年增率","threshold":"鎳合金 < 9 個月或高階鈦 < 12 個月，且積壓訂單年增 < 0 連 2 季","action":"減碼","source_freq":"每季法說問答與新聞稿","date":null,"evidence_refs":["competitive_share_entrants#3","supply_demand_durability#6"]},{"n":7,"text":"航太循環反轉：Airbus 或 Boeing 正式下修月產率目標，且 ATI 積壓訂單年減逾 10%","type":"清倉","maps_to":"R3","metric":"OEM 月產率目標、ATI 積壓訂單年增率","threshold":"降產公告＋積壓訂單年減 > 10%","action":"清倉","source_freq":"OEM 公告不定期；積壓訂單每季","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":8,"text":"原料或關稅成本轉嫁失敗：調整後 EBITDA 利潤率年減逾 200 個基點，且管理層歸因原料、出口管制或關稅","type":"風險","maps_to":"R4","metric":"調整後 EBITDA 利潤率年變動＋管理層歸因","threshold":"年減 > 200 個基點","action":"減碼","source_freq":"每季","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","reg_tariff_export#2"]},{"n":9,"text":"退休金義務轉移集體訴訟：法院否決 ATI 的駁回動議，或公司認列和解或準備逾 3,000 萬美元（約全年 FCF 指引 5%）","type":"風險","maps_to":null,"metric":"訴訟程序進度、認列金額","threshold":"駁回動議被否決或認列 > 3,000 萬美元","action":"停止加碼","source_freq":"每季 10-Q 法律程序附註","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":10,"text":"2027 指引調整後 EPS 中點 ≥ 7.0 美元（高於共識約 10%），且股價 ≤ 175 美元（約 25 倍）","type":"加碼","maps_to":"H3","metric":"2027 EPS 指引中點與股價","threshold":"EPS 中點 ≥ 7.0 且股價 ≤ 175 美元","action":"分批反買","source_freq":"一次性：2026-11 投資人日或 2027-02 Q4 法說","date":null,"evidence_refs":[]},{"n":11,"text":"投資人日後複審：核對 2027 指引、年底續約價格與 HPMC 新產能認證進度","type":"複審日期","maps_to":null,"metric":"2027 指引全套","threshold":"指引發布即複審","action":"不追（複審前不動作）","source_freq":"一次性","date":"2026-11","evidence_refs":[]}],"kill_metrics":[{"metric":"2027 調整後 EBITDA 指引中點","bear_threshold":"< 13 億美元 → 清倉","window":"2026-11 投資人日至 2027-02 Q4 法說","source":"公司指引","last_status":"unknown"},{"metric":"AA&S 分部利潤率（單季）","bear_threshold":"連 3 季 < 18% → 減碼","window":"2027–2028 各季","source":"季度新聞稿分部資料","last_status":"ok"},{"metric":"HPMC 分部利潤率（滾動四季）","bear_threshold":"< 22% → 減碼","window":"2027–2030","source":"季度新聞稿分部資料","last_status":"ok"},{"metric":"積壓訂單年增率","bear_threshold":"連 2 季 < 0% 且交期縮短 → 減碼；年減 > 10% 且 OEM 降產 → 清倉","window":"2027–2030 各季","source":"季度新聞稿與法說","last_status":"ok"},{"metric":"鎳合金交期","bear_threshold":"< 9 個月（現約 12 個月）","window":"2027–2028 各季法說","source":"法說問答","last_status":"ok"}],"evidence_dismissed":[{"ref":"substitute_technology#2","reason":"來源為投資人社群自撰敘事，非公司揭露也非研究報告，未附任何替代比例、時程或成本數據，無法形成可監測門檻；同方向的可查證證據（10-K 風險因子、GKN 積層製造計畫）已列入威脅"}],"action_conditions":{"rearm_trigger":"股價 ≤ 153 美元（FY2027 共識 6.37 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","exec_line":"現價不追；條件成立先重跑判斷，再以小部位首筆分批反買；基本面無損的下跌不停損，觸及清倉門檻才出場"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 153 美元以下（FY2027 共識 24 倍），且 2027 指引 EBITDA 中點不低於 13 億美元"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=None, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"新世代引擎放量與鎳產能擴充，讓 HPMC 維持 25% 上下的分部利潤率，並在 2028 年前帶來約 3.5 億美元新增鎳營收","2y":null,"5y":"2028 年鎳產能較 2025 年底增 15–20%、新增年營收約 3.5 億美元；HPMC 分部利潤率滾動四季 ≥ 22%","10y":null,"threshold":"HPMC 分部利潤率滾動四季 ≥ 22%；新 VIM 熔煉爐 2027 年底前上線（延後不超過 6 個月）","source":"季度新聞稿分部資料、法說產能進度（2026-08-06 Q2 法說：鎳產能 2028 年初增 15–20%、新增約 3.5 億美元營收）","drift_rule":"HPMC 利潤率滾動四季連 4 季低於門檻 5% 以上為削弱；連 6 季低於 10% 以上或 VIM 延後逾 6 個月為反轉"},{"id":"H2","text":"AA&S 已由低利潤循環事業轉為第二個穩定獲利引擎：航太國防占比 44% 以上，鉿鋯稀缺定價與海軍核能新約撐住 20% 以上利潤率","2y":"2027 年 AA&S 分部利潤率全年 ≥ 20%，航太國防占比 ≥ 44%","5y":null,"10y":null,"threshold":"AA&S 分部利潤率單季 ≥ 20%（Q2 2026 為 23.7%）","source":"季度新聞稿分部資料；2026-08-06 Q2 法說 CEO 稱中長期 25% 上下","drift_rule":"連 2 季低於門檻 5% 以上（約 19%）為削弱；連 3 季低於 10% 以上（18% 以下）為反轉"},{"id":"H3","text":"長約價格重設在 2027 年全年生效，2027 年調整後 EBITDA 至少達到 Q4 2026 隱含的 13.5 億美元年化水準，FCF 轉換率 ≥ 85%","2y":"2027 年調整後 EBITDA ≥ 13.5 億美元、調整後 EPS 不低於共識 6.37 的 95%；2026 年調整後 FCF ≥ 5.5 億美元","5y":null,"10y":null,"threshold":"2027 指引 EBITDA 中點 ≥ 13 億美元；2026 全年調整後 FCF ≥ 5.5 億美元","source":"2026 年 11 月投資人日與 Q4 法說的 2027 指引；2026-08-06 Q2 法說 Q4 隱含 3.35 億美元 EBITDA","drift_rule":"實際或指引低於門檻 5% 以上連 2 季為削弱；連 3 季低於 10% 以上為反轉"}],"R":[{"id":"R1","text":"墨西哥 Chihuahua 新廠與 EB2 鈦電子束爐認證延誤擴大，Q2 遞延的 3,000–4,000 萬美元 HPMC 出貨下半年未補回","h_ref":"H1","clock":"⚡","threshold":"Q3＋Q4 2026 HPMC 營收平均 < 6.5 億美元","evidence_refs":["supply_demand_durability#6"]},{"id":"R2","text":"同業與引擎 OEM 新熔煉、鍛造產能於 2027 下半年至 2030 年投產，交期縮短，續約漲價空間收斂","h_ref":"H3","clock":"🔥","threshold":"鎳合金交期 < 9 個月或高階鈦 < 12 個月，且積壓訂單年增 < 0 連 2 季","evidence_refs":["competitive_share_entrants#3","supply_demand_durability#6"]},{"id":"R3","text":"航太循環反轉：HPMC 約 92–93% 營收來自航太國防，客戶集中於 Boeing、Airbus、GE、Rolls-Royce、Pratt & Whitney、Safran 等少數大廠，任一主力機型降產或停飛都直接打到訂單","h_ref":"H1","clock":"🐢","threshold":"Airbus 或 Boeing 正式下修月產率目標，且 ATI 積壓訂單年減 > 10%","evidence_refs":["customer_concentration_credit#0"]},{"id":"R4","text":"原料與地緣：鎳、海綿鈦多自國外（含中國、哈薩克）進口，中國出口管制可能延遲取得材料；另有中國合資 STAL 與舊有 232 關稅爭議","h_ref":"H2","clock":"🐢","threshold":"調整後 EBITDA 利潤率年減 > 200 個基點，且管理層歸因原料或關稅轉嫁失敗","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","reg_tariff_export#2"]}],"single_thing":{"description":"2027 年合約價格重設的結果：2026 年 11 月投資人日或 Q4 法說給出的 2027 指引，調整後 EBITDA 中點低於 13 億美元（低於 Q4 2026 隱含的 13.5 億美元年化水準）","why_fatal":"現價 29.5 倍的 FY2027 本益比建立在 2026 年漲價紅利全年延續；EBITDA 每少 1 億美元，EPS 約少 0.58 美元（稅率假設 22%、約 1.35 億股），FY2027 EPS 落到 6 美元以下，倍數與 EPS 同時下修，是情境樹中最大的單一敏感度","if_happens":"熊市機率由 30% 上調至 40%，取消重新進場條件並重跑判斷；若已持有則清倉","how_monitor":"2026 年 11 月投資人日指引、2027 年 2 月 Q4 法說；中間看 Q3 2026 調整後 EBITDA 是否落在 3.05–3.15 億美元指引內","probability":"約 15%：Q2 實績超過指引上緣 2,900 萬美元、上半年兩度上修，續約多已談定；主要風險在 HPMC 新產能認證"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":29.51,"peg_fy2":1.41,"stress":{"pass":9,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":3.23,"FY2026E":5.12,"FY2027E":6.37,"FY2028E":7.5},"fy_end_month":12,"eps_basis":"調整後 EPS（非 GAAP），與共識同口徑；FY2025A 基期由 2026-08-06 Q2 法說「中點 5.04、年增 56%」回推約 3.23，GAAP 稀釋 EPS 為 2.85；共識為 Koyfin 2026-10-08 快照"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"投資人日：預計給出 2027 年以後展望，揭露年底續約重設結果","impact":"高","watch":"2027 調整後 EBITDA 是否 ≥ 13.5 億美元、EPS 是否高於共識 6.37"},{"date":"2026-Q4","date_precision":"quarter","type":"guidance","event":"Q3 2026 財報（指引調整後 EBITDA 3.05–3.15 億美元、EPS 1.31–1.37）","impact":"中","watch":"HPMC 遞延出貨是否補回、AA&S 利潤率是否維持 20% 以上"},{"date":"2027-12","date_precision":"month","type":"capacity","event":"新 VIM 一次熔煉爐預定 2027 年底上線，鎳產能 2028 年初增 15–20%","impact":"中","watch":"是否延後逾 6 個月"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
