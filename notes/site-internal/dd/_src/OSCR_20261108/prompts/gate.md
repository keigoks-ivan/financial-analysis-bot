你是 DD 管線 v20 的判斷層閘（gate），標的 OSCR（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
<!-- 2026-10-20 ⑤ 改程式判定；來源 gate_contract §⑤／critic-gates ⑤ 同日改成同一條規則（核心軸 none 🔴、非核心 🟡）；重新濃縮時以本卡 ⑤ 為準 -->

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

⑤ 覆蓋面掃描——**燈號由程式判定**（核心軸 none→🔴；只有非核心軸 none→🟡；全 found／not_applicable→🟢），bundle 附程式結果，你回的 ⑤ 燈號會被覆寫。你只評論：facts.json 點名 status="none"／"not_applicable" 的軸，查詢是否切題（不以查詢次數計）、判斷有沒有交代缺口對結論的影響；不得因缺軸自行升 🔴。

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤（燈號由程式判定，你只評論）。
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

### 判斷檔 `fact_refs` 引到的事實（28 條）
- `f_kpi0_total_revenue_gaap`（q1_business）｜Total revenue (GAAP)＝5139.3 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Q3 2026（SEC URL 同 quarter 欄）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：新聞稿未列共識；媒體稱優於預期（未驗證）
- `f_kpi2_gaap_earnings_from_opera`（q1_business）｜GAAP earnings from operations＝178.0 USD M（利益率 3.46%，自算）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Q3 2026（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：新聞稿未列共識
- `f_kpi4_medical_loss_ratio_sg_a_`（q1_business）｜Medical loss ratio / SG&A ratio＝MLR 84.0%；SG&A 14.0% %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Q3 2026（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：新聞稿未列共識
- `f_kpi7_effectuated_membership`（q1_business）｜Effectuated membership＝2691885 members｜期間與口徑：2026-09-30（公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Q3 2026（numbers.latest_quarter_kpis.items[7]，as_of 2026-09-30（公告於 2026-11-05））
  - 註記：n/a
- `f_kpi8_fy2026_guidance`（q1_business）｜FY2026 guidance（上修）＝營收 19.0–19.3B；MLR 80.5–81.5%；SG&A 15.1–15.6%；營業利益 850–950M USD / %｜期間與口徑：Q3 2026 公告（2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Q3 2026（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026 公告（2026-11-05））
  - 註記：yfinance FY1 營收共識均值約 18.99B（財報前快照，見 capital_structure）
- `f_peer_oscr_fcf_margin_pct`（q2_moat）｜OSCR FCF 利潤率＝43.41 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.OSCR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cnc_operating_margin_pct`（q2_moat）｜CNC 營業利益率＝0.75 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CNC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_moh_operating_margin_pct`（q2_moat）｜MOH 營業利益率＝0.6 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MOH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_clov_operating_margin_pct`（q2_moat）｜CLOV 營業利益率＝0.3 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CLOV.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.94 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.22 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝2.84 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝18990.59 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（8 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝20796.33 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_free_cash_flow`（q1_business）｜Free cash flow（前九個月，自算）＝3478.9 USD M｜期間與口徑：前九個月至 2026-09-30（公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿營運現金流 3,510.7M 減資本支出（含資本化軟體）31.9M，自算；公司未報 FCF，Q3 單季現金流未揭露（numbers.latest_quarter_kpis.items[5]，as_of 前九個月至 2026-09-30（公告於 2026-11-05））
  - 註記：n/a
- `f_kpi6_sbc`（q4_capital）｜SBC 占營業利益 / 營收＝12.5 % of earnings from operations（占營收 0.43%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿 SBC 22.3M ÷ 營業利益 178.0M，自算（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-7006.86 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 481.73、現金 7488.59（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝30.65 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.8 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.94，分子＝快照價 30.65｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝50.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝69.8 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝2515.67 USD m｜期間與口徑：2026-11-08／市值 9522.53 ＋ 淨負債 -7006.86｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝310.69 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝43.83 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w104`（q5_valuation）｜104 週均線＝19.03 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝13.36 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w52`（q5_valuation）｜52 週均線＝22.28 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2022 10-K：2022 年約 85%、2021 年約 73% 的會員保費由 APTC 補貼（對聯邦補貼依賴度，非單一客戶占比；無單一客戶營收占比數字）
  - 來源：Oscar Health 10-K FY2022 (SEC)（as_of 2023-02-28）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K 將 eAPTC 到期與 CMS program integrity rules 列為影響估計的法規變動
  - 來源：Oscar Health 10-K FY2025 (SEC)（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素：Oscar 因收取聯邦付款，受 DOJ／HHS-OIG／CMS 的詐欺、浪費與濫用法規（含 FCA）管轄，預期持續受審查；10-K 未點名具體反壟斷調查。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素：部分市場的醫院或醫師團體具near monopoly地位，削弱 Oscar 議價力（供給端集中，非 Oscar 自身被調查）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：搜尋未發現 2026 年針對 Oscar 的 DOJ／FTC／EU 反壟斷調查或拆分風險；產業監管面向為 eAPTC 補貼 2025 年底到期、CMS 2025 年 Program Integrity 規則（部分條款遭 Maryland 聯邦地院 2025-08-22 暫停）。依 Q2 2026 10-Q 摘要，公司業務受州與聯邦監管機關審查。
  - 來源：SEC EDGAR 10-Q（截至 2026-06-30）搜尋摘要（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K：公司表示川普政府可能對藥品、原料、醫療器材與耗材課關稅，可能推高醫療院所成本、藥價與醫療器材成本，並造成藥品與醫療用品短缺，進而影響醫療成本估計。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K MD&A 列「Proposed Tariffs」：關稅的不確定性可能影響公司估計與管理醫療費用的能力。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-13）｜affects：thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2026-04 Section 232 公告對專利藥及藥品原料課 100% 關稅；Oscar 後續 10-Q 稱關稅生效後藥品回扣可能同步或更大幅下降。
  - 來源：Oscar Health 10-Q 2026-09-30（as_of 2026-11-05）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Oscar 10-K（FY2025）揭露依賴第三方供應商營運多數通訊、網路與電腦軟硬體；失去供應商可能造成重大中斷。未見地緣（台灣/中國）暴露的搜尋摘要。
  - 來源：Oscar Health Form 10-K FY2025（as_of 2026-02-28）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Oscar 將藥局理賠與網絡管理委外給單一 PBM（CVS/Caremark），並用 AWS、Google Cloud 託管（FY2021 10-K）。
  - 來源：Oscar Health Form 10-K FY2021（as_of 2022-03-01）｜affects：thesis.R、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：2027 逆風：KFF 資料顯示個人市場 2026 年 6 月約 2,050 萬人，年減約 18%；保險公司 2027 提案保費中位數漲約 15%，Oscar 喬治亞州申請約 29%。UBS 降評 Sell，預估 2027 營收 $122 億、EPS $1.25（低於共識 $1.46），指定價能力有限；Piper 認為即使加強補貼失效 Oscar 仍可能拿下份額。
  - 來源：Weiss Ratings 引 KFF；AllMind（UBS）；Asianet Newsable（Piper/Jefferies）（as_of 2026-10-31）｜affects：thesis.R、decision_inputs.bear、valuation
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：公司核心技術與基礎設施為自建，關鍵技術人員流失可能干擾營運；且未申請專利保護其專有技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `unprofitable_dilution_trajectory#0`（unprofitable_dilution_trajectory｜方向 -｜狀態 ok）：聚合站顯示 OSCR 2026 Q1 稀釋加權股數 329.8M，年增 7.8%（305.9M→329.8M）；來源未對照 10-Q 原文
  - 來源：opencapital.sh weighted shares diluted / stockanalysis.com OSCR financials（as_of 2026-05-07）｜affects：valuation、decision_inputs.bear
- `unprofitable_dilution_trajectory#1`（unprofitable_dilution_trajectory｜方向 -｜狀態 ok）：稀釋股數年度序列（聚合站）：FY2021 179M、FY2022 212M、FY2023 222M、FY2024 266M、FY2025 262M；各站數字有出入
  - 來源：stockanalysis.com OSCR financials / alphaquery annual diluted weighted shares（as_of 2026-05-07）｜affects：valuation

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":99.2,"bear_5y_price":12.8,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":56.6,"ev5y_pct":55.6,"irr_base_pct":9.4,"asym_ratio":2.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.94,"pe":15.8,"basis":"2026 年共識 EPS（FY1，看來尚未反映 11-05 上修）；終端倍數同樣以當年度 EPS 為分母。"},"eps":{"bull":[2.9,3.6,4.6,5.4,6.2],"base":[2.35,2.75,3.2,3.6,4.0],"bear":[1.2,0.35,0.9,1.3,1.6]},"pe":{"bull":16,"base":12,"bear":8},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### OSCR_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：全年營運盈餘財測上調至 5 億～7 億美元，較先前上調 2.5 億（原話："an increase of $250 million from our prior outlook."）
- 2026-08-06｜CFO｜guidance：全年營收財測維持 187 億～190 億美元（原話："to expect total revenues of $18.7 billion to $19 billion."）
- 2026-08-06｜CFO｜guidance：全年 MLR 財測 81.5%–82.5%,中點改善 90bp（原話："an improvement of 90 basis points at the midpoint"）
- 2026-08-06｜CFO｜guidance：SG&A 費用率財測中點改善 20bp（原話："an improvement of 20 basis points at the midpoint."）
- 2026-08-06｜CFO｜guidance：調整後 EBITDA 約高於營運盈餘 1.15 億（原話："run roughly $115 million above earnings from operations."）
- 2026-08-06｜CFO｜guidance：財測未全額計入 Wakely 早期有利數據（原話："we have not taken full credit for that"）
- 2026-08-06｜CFO｜guidance：若有利趨勢持續，可能是全年財測順風（原話："that could present a tailwind to our full year outlook."）
- 2026-08-06｜CEO｜guidance：下半年預期會員流失(churn)約為先前 1–2% 的兩倍，屬時間遞延（原話："It's probably going to be closer to twice that amount."）
- 2026-08-06｜CFO｜guidance：Q4 SG&A 費用率預期為全年最高（原話："the fourth quarter will be the highest SG&A ratio"）
- 2026-08-06｜CEO｜guidance：管理層預期 MLR 隨季節性逐季走高（原話："as members burn through their deductibles."）
- 2026-08-06｜CFO｜margin：Q2 MLR 79.2%（原話："The second quarter medical loss ratio was 79.2%"）
- 2026-08-06｜CFO｜margin：前六個月風險調整占直接保費約 20%,與全年預期一致（原話："approximately 20%, consistent with our expectations"）
- 2026-08-06｜CFO｜margin：2025 年 CMS 最終風險調整報告較 Q1 應計有利約 1.6 億，Q2 全額認列（原話："approximately $160 million favorable to our first"）
- 2026-08-06｜CFO｜margin：Q2 有利前期準備金發展 1.64 億，上半年累計 2.32 億，為調整 MLR 時應剔除的數字（原話："Year-to-date, that's $232 million."）
- 2026-08-06｜CFO｜margin：上半年門診利用率偏高，其餘類別有利（原話："we're basically getting there a year ahead of plan."）
- 2026-08-06｜CEO｜margin：Q2 SG&A 費用率創歷史新低 14.2%,稅與交易所費用上升被變動成本效率抵銷（原話："we're basically getting there a year ahead of plan."）
- 2026-08-06｜CFO｜margin：風險調整付款方屬性來自會員較年輕健康、偏都會（原話："we're a risk adjustment payer because"）
- 2026-08-06｜CEO｜competition：管理層稱單一平台單一資料集，AI 規模化部署領先同業（原話："we have one platform, we have one data set."）
- 2026-08-06｜CEO｜competition：2027 費率環境至今被管理層描述為理性（原話："We believe the market so far has been rational."）
- 2026-08-06｜CEO｜product：Oswell 放射科試點：會員選推薦院所比例與節省金額（原話："1 in 4 members choose Oswell's recommended site of care and"）
- 2026-08-06｜CEO｜product：ICHRAx 提供 ICHRA 運行軌道（原話："which has not been the case in the past."）
- 2026-08-06｜CEO｜product：AI 藥局醫務經濟方案預期年節省數千萬美元（原話："We expect these capabilities to generate tens of millions"）
- 2026-08-06｜CEO｜product：銅級/金級新產品，會員由銀級轉移（原話："from silver into higher deductible Bronze"）
- 2026-08-06｜CFO｜risk：CMS 計畫完整性相關影響已納入全年財測（原話："I don't think this is an area that we see as a risk to"）
- 2026-08-06｜CEO｜risk：IDR 不是成本趨勢驅動因素（原話："IDR is not a trend driver."）
- 2026-08-06｜CEO｜risk：預期會被取消註冊的會員不認列營收（原話："we don't recognize revenue for members that we"）
- 2026-08-06｜CEO｜customer：Q2 末 296 萬有效會員，季增約持平（原話："which is basically flat in the second quarter."）
- 2026-08-06｜CEO｜customer：Wakely 首份 2026 理賠型市場罹病率報告有利於預期（原話："market morbidity is also favorable to our expectations,"）
- 2026-08-06｜CFO｜capital_allocation：現金與投資約 102 億美元（原話："approximately $10.2 billion of cash and investments"）
- 2026-08-06｜CFO｜capital_allocation：保險子公司超額資本 9.94 億（原話："including $994 million of excess capital"）
- 2026-08-06｜CEO｜commitment：將於 9/16 投資人日說明持久成長與長期價值（原話："We will outline how we translate that performance into"）
- 2026-08-06｜CEO｜commitment：管理層稱 2027 若有 NBPP 變動，有能力調整產品與定價（原話："we have an opportunity to change product and pricing"）
- 2026-08-06｜CEO｜commitment：管理層稱 2026 稅收抵免影響已過（原話："We think we're through all the enhanced premium tax credits"）

### OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md
- 2026-09-16｜CEO Mark Bertolini｜guidance：2026 營業盈餘財測上修（原話："guidance is up $600 million to $800 million"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2026 全年 MLR 財測上修 50bp 至 81–82%（原話："50 basis points to 81% to 82%"）
- 2026-09-16｜CFO Scott Blackley｜guidance：營業盈餘新區間為原財測的兩倍（原話："which is double our original guidance"）
- 2026-09-16｜CFO Scott Blackley｜guidance：其餘 2026 財測不變（原話："guidance that we have for the year remains unchanged"）
- 2026-09-16｜CEO Mark Bertolini｜guidance：2026 SG&A 比率區間不變、營收 187–190 億（原話："$18.7 billion to $19 billion in revenue"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 營業利益率預期高於 5%（原話："our 2027 operating margin will be greater than 5% next year"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 EPS 預期高於 2.25 美元（原話："our 2027 EPS will be greater than $2.25 a share"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 有效稅率預期維持個位數中段（原話："continue to be in the mid-single digits"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 正式財測留待明年二月法說（原話："specific guidance on 2027 at our investor call next February"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2029 目標：營業利益率 5–7%（原話："5% to 7% operating margin by 2029"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2029 目標：EPS 大於 4 美元（原話："EPS of greater than $4 per share by 2029"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2029 假設稅率與股數（原話："diluted share count will grow at around 2% to 3% per year"）
- 2026-09-16｜CFO Scott Blackley｜guidance：投資收益 2029 前年增 10–15%（原話："at a rate of around 10% to 15% per year"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2026 底 ACA 市場約 1,700 萬人並持平至 2027（原話："around 17 million lives in the total ACA"）
- 2026-09-16｜CFO Scott Blackley｜guidance：2027 費率調幅與全國平均大致相當（原話："rate increases are largely in line with national averages"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜guidance：2027 Oscar 調幅 14%，競爭者平均 15%（原話："14% rate increase and the competitors are on average of 15%"）
- 2026-09-16｜CFO Scott Blackley｜guidance：CMS 100 萬人清查已處理並反映於 Q3；另有約 50 萬人第二輪（原話："a second smaller CMS program later this year"）
- 2026-09-16｜CFO Scott Blackley｜guidance：CMS 清查影響已完整反映於財測（原話："we have fully reflected the impact of these programs"）
- 2026-09-16｜CFO Scott Blackley｜margin：MLR 目標接近 80%（原話："approaching 80% is our target"）
- 2026-09-16｜CFO Scott Blackley｜margin：管理層說明 2029 利潤率區間高於歷史 3–5%（原話："higher than what we've seen historically in the 3% to 5%"）
- 2026-09-16｜CFO Scott Blackley｜margin：固定成本占比 2024 年 30% 降至今年約 25%（原話："gone from 30% back in 2024 to around 25% this year"）
- 2026-09-16｜CFO Scott Blackley｜margin：約 10% 的 SG&A 屬 ACA 結構性成本（原話："about 10% of our SG&A is structural to the ACA"）
- 2026-09-16｜CFO Scott Blackley｜margin：Lucie 規模化後利潤率為核心保險的 5–6 倍（原話："5 to 6x greater than our core insurance business"）
- 2026-09-16｜CEO Mark Bertolini｜margin：每 10 萬會員的 Lucie 利潤率假設（原話："35% on the first 2 and 80% in Consumer Health Products"）
- 2026-09-16｜CFO Scott Blackley｜margin：每 10 萬會員 Lucie 營收機會 1.5 億美元（原話："$150 million revenue opportunity per 100,000 members"）
- 2026-09-16｜CEO Mark Bertolini｜margin：AI 同時影響成本與營收（風險調整、再保回收）（原話："It's a revenue enhancer because now we have the ability"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜margin：網路與技術在兩年內帶來 30 億美元的可負擔性（原話："$3 billion in affordability"）
- 2026-09-16｜CEO Mark Bertolini｜margin：AI 累計醫療成本節省（原話："$3-plus billion in total medical cost savings"）
- 2026-09-16｜Mario Schlosser｜margin：藥局理賠 agent 揪出約 2,800 萬美元藥費（原話："$28 million or so in drug costs that we probably shouldn't"）
- 2026-09-16｜CEO Mark Bertolini｜commitment：重申 2027 營業利益率至少 5%（原話："a commitment which we are reaffirming of at least 5% in 2027"）
- 2026-09-16｜CEO Mark Bertolini｜commitment：2029 營收 CAGR 20%+、利潤率 5–7%、EPS 4 美元以上（原話："continue to deliver on our 20% plus revenue CAGR"）
- 2026-09-16｜CFO Scott Blackley｜commitment：不論 Lucie 成敗，2029 EPS 目標不變（原話："deliver more than $4 of EPS in 2029"）
- 2026-09-16｜CEO Mark Bertolini｜commitment：Lucie 未納入數字（原話："We don't have Lucie in the numbers"）
- 2026-09-16｜CFO Scott Blackley｜commitment：Lucie 預期支出已計入計畫（原話："significant amount of expected spend there"）
- 2026-09-16｜CEO Mark Bertolini｜commitment：規劃流程：風險機會各配對槓桿，2025 年未撤回財測（原話："So we didn't withdraw guidance."）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：母公司現金（原話："$460 million of parent cash"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：計畫期間預計產生 40–45 億美元資本（原話："$4 billion to $4.5 billion across the parent"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：約 60% 資本留在保險子公司（原話："60% of our capital generation will stay within"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：上繳母公司資金用途（原話："pursue opportunistic M&A and manage share dilution"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：再保（quota share）日後預期減少使用（原話："over time, we will use them to a lesser extent"）
- 2026-09-16｜CFO Scott Blackley｜capital_allocation：資本優先順序首項為有機成長（原話："capital priorities start with organic growth"）
- 2026-09-16｜CEO Mark Bertolini｜competition：稱 ACA 不是終點，因 TAM 與競爭（原話："the competition would be too fierce"）
- 2026-09-16｜CEO Mark Bertolini｜competition：競爭對手將付費使用 Oscar 技術平台（原話："they will pay rents on that capability"）
- 2026-09-16｜CEO Mark Bertolini｜competition：ICHRAx 以成本加成收費，對比他家 4 美元（原話："cost-plus unlike the $4 they're paying"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜competition：Oscar 在現有區域市占約 30%，目標 35%（原話："mature our market share from 30% to 35%"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜competition：2029 全國市占目標 18%（原話："national share by 2029 of 18%"）
- 2026-09-16｜CEO Mark Bertolini｜competition：網路為 ACA 原生建構，對比同業改造（原話："retrofit those networks for ACA"）
- 2026-09-16｜CEO Mark Bertolini｜competition：價差本身不足以搶走客戶（原話："the price differential in and of itself is not enough"）
- 2026-09-16｜CFO Scott Blackley｜competition：收入成長拆解：現有區域 17–19%（原話："between 17% and 19% growth per year"）
- 2026-09-16｜CFO Scott Blackley｜competition：新市場以 5–7% 市占進入，貢獻 2–4% 成長（原話："2% to 4% revenue growth through 2029"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜competition：每年擴張 400–600 個新縣（原話："roughly 400 to 600 new counties"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：生活型產品 NPS 71 vs 產業 12（原話："Net Promoter Score of 71 versus an industry average of 12"）
- 2026-09-16｜CEO Mark Bertolini｜product：同場另一說法：產業 NPS 平均為 0（原話："in an industry that averages 0"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：生活型產品占會員不到 10%（原話："just under 10% of our total membership"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：HelloMeno 直接報名提升 2.5 倍（原話："2.5x increase in direct enrollment"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：與 Allstate 合作，2027 年銷售（原話："about 30,000 new brokers who have not written Oscar medical"）
- 2026-09-16｜CEO Mark Bertolini｜product：補充險 2027 開放投保期已有 80 萬張保單（原話："We already have 800,000 policies for open enrollment"）
- 2026-09-16｜CEO Mark Bertolini｜product：CHOICE 2026 約 50 萬人，2029 預期 250 萬（原話："We think it's 2.5 million lives by 2029."）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜product：CHOICE 2029 市占預期 3 倍（原話："we will be at 3x market share in CHOICE"）
- 2026-09-16｜CEO Mark Bertolini｜product：CHOICE 已納入數字有限，轉折點時間未知（原話："We haven't put a lot in the numbers other than these"）
- 2026-09-16｜CEO Mark Bertolini｜product：Lucie 平台 70 家以上承保人（原話："over 70 other carriers"）
- 2026-09-16｜Mario Schlosser｜product：AI 撰寫程式碼占比由 16% 升至近三分之二（原話："almost up to 2/3s of all the lines of code"）
- 2026-09-16｜Mario Schlosser｜product：Oswell 直接處理 30–40% 會員訊息（原話："solves about 30% to 40% of all member messages"）
- 2026-09-16｜Mario Schlosser｜product：事前授權：只自動核准，不自動拒絕（原話："We don't do automated disapprovals ever"）
- 2026-09-16｜Mario Schlosser｜product：AI 在稀疏資料上表現不佳（原話："They're not very good at sparse data and making that up."）
- 2026-09-16｜CEO Mark Bertolini｜risk：Medicaid 示範計畫仍在早期（原話："we're still early in that process"）
- 2026-09-16｜CEO Mark Bertolini｜risk：顧問端預期出現長期對抗（原話："is going to be a fight over time"）
- 2026-09-16｜CFO Scott Blackley｜risk：2026 定價已假設市場萎縮 30%（原話："We priced for a market that we expected to contract by 30%."）
- 2026-09-16｜CFO Scott Blackley｜risk：成員自付額進度符合預期（原話："are in line with our expectations"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜customer：2025 年營收與會員各成長 60%、利潤率擴 7 點（原話："60% membership growth, 60% revenue growth and 7 points"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜customer：經紀分銷成長 60%（原話："we grew our distribution by 60%"）
- 2026-09-16｜Janet Liang (President, Oscar Insurance)｜customer：生活型產品每年為會員省近 1,000 美元（原話："saved nearly $1,000 on average each year"）
- 2026-09-16｜CEO Mark Bertolini｜customer：2029 ACA 約 2,300 萬人（原話："a total of 23 million lives in the ACA in 2029"）

### 問答異常語氣（迴避／改口／保留）
- OSCR_Q2_2026_Earnings_Call_20260806.md｜問：Justin Lake(Wolfe):CMS 100 萬名單中有多少為 Oscar 會員、能留住多少、財務影響｜答法：未給會員數或比例，改談 CMS 重視資格驗證、正在逐檔審查、影響已在財測內
- OSCR_Q2_2026_Earnings_Call_20260806.md｜問：Michael Ha(Baird):剔除 PPD 後 Q2 底層 MLR 是否約 85.2%｜答法：CFO 稱自己算約 82%,未確認 85.2%,表示會後再對帳
- OSCR_Q2_2026_Earnings_Call_20260806.md｜問：Michael Ha:下半年隱含風險調整比例與 Wakely 上行空間幅度、哪些情境會威脅全年｜答法：CEO 僅重申上半年 20% 與全年 20% 預期，未量化上行空間也未談威脅情境
- OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md｜問：Goldman：投影片 45/46 的利潤率與 MLR 150bp 改善如何對應｜答法：CFO 稱想不起投影片 45 內容，改以泛稱的負擔能力措施與 2029 年 80% MLR 目標回答，未逐項拆解 150bp
- OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md｜問：UBS：2029 年 G&A 降至 15% 以下需要什麼｜答法：CEO 只答「Scale, AI」，未給 SG&A 拆解或數字
- OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md｜問：BofA：CHOICE 方案是否承受立法/費率風險｜答法：CEO 答以「依預期組合定價」並描述雇主定額做法，未直接回應立法風險；CFO 改談 ACA 長期趨勢
- OSCR_Analyst_Investor_Day_Oscar_Health_Inc_20260916.md｜問：Jefferies：市場由 2,300 萬降到 1,700 萬、逾 900 萬人流失對風險組合的影響｜答法：CFO 回以事前假設市場收縮 30% 與定價準備，未回應流失者與留存者 MLR 差異的具體數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 4 | 2 |
| reg_tariff_export | found | 4 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 2 | 3 |
| unprofitable_nrr_rule40_band | none | 0 | 3 |
| unprofitable_dilution_trajectory | found | 4 | 3 |
| unprofitable_path_to_profitability | found | 3 | 2 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **unprofitable_nrr_rule40_band**（none）：OSCR Oscar Health net revenue retention NRR 2026；Oscar Health Rule of 40 peers comparison 2026；Healthcare Plans SaaS peers NRR benchmark 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"觀察池 — C 級護城河 5.5 (execution 7 / pricing power 4) + ACA 補貼到期 binary 風險 + Pure MA 🟠 暫不（盲點 2 救援失效）+ 4 週 +66% 動能透支；等 2025-Q4 PTC 立法 + H2 MLR ≤84% 雙信號明朗化再評估","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"ACA Marketplace 在政策層面持續存在（無 repeal、無 single-payer）","columns":{"2Y 驗證點":"2025-Q4 enhanced PTC 立法延長 ≥ 1 年","5Y 驗證點":"2030 前無重大 ACA 結構改革","10Y 驗證點":"2035 前無 single-payer transition","具體數字門檻":"marketplace enrollment ≥ 22M（CBO 基準），OSCR 市占維持 8-12%","信息來源":"CBO / KFF 估算、CMS 月報；公司法說","漂移觸發條件":"連 2 季 OSCR 會員 YoY 下滑 ≥ 10% → 削弱"}},{"id":"H2","text":"underwriting discipline 持續，全年 MLR 落在 82-84% 區間","columns":{"2Y 驗證點":"FY2026 全年 MLR ≤ 84%","5Y 驗證點":"3 年滾動均 MLR ≤ 83%（保險業 best-in-class）","10Y 驗證點":"10 年累積 underwriting 信心建立","具體數字門檻":"全年 MLR 82.4-83.4%（管理層指引上下緣）","信息來源":"公司季報 + Earnings Call 數字","漂移觸發條件":"連 2 季 MLR 偏離指引上緣 ≥ 2pp → 削弱；連 3 季 → 反轉"}},{"id":"H3","text":"規模優勢轉化為 unit economics，SG&A 比率持續壓縮，FCF/Rev ≥ 5% 可持續","columns":{"2Y 驗證點":"FY2026 SG&A ratio ≤ 16%；FCF ≥ $1.2B","5Y 驗證點":"3 年滾動均 OIM > 2.5%（FY26 指引 1.5-2.4%）","10Y 驗證點":"10 年 ROIC 平均 > 15%","具體數字門檻":"SG&A 15.8-16.3% 指引；EBIT $250-450M","信息來源":"公司指引 / 同業對比 ELV ROIC 12-15%","漂移觸發條件":"SG&A ratio 連 2 季 > 17% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"2025 Q4 enhanced PTC 立法失敗 / 僅延 6 個月","columns":{"對應假設":"H1","時間尺度":"⚡ 短期","監測指標":"國會表決結果、CBO/Pres release","警戒閾值":"未通過 → 立即觸發；僅延 6 個月 → 部分削弱"}},{"id":"R2","text":"2026 H2 MLR 結構性超指引（utilization 飆升）","columns":{"對應假設":"H2","時間尺度":"🔥 中期","監測指標":"季度 MLR、Earnings Call utilization 描述","警戒閾值":"任一季 MLR > 86% → 削弱；> 88% → 反轉"}},{"id":"R3","text":"UNH / ELV / CNC 戰術性回歸高 OSCR 市占州","columns":{"對應假設":"H1 + H3","時間尺度":"🐢 長期","監測指標":"競爭對手 2027 ACA 計畫宣告、CMS 州別 enrollment 數據","警戒閾值":"UNH 或 ELV 宣告重返 FL/TX 任一州 → 觸發"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"C","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":23.32,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"OSCR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Oscar Health, Inc."},"oneliner":"2026 獲利創新高，但全年營業利益近半來自前期項目。現價要靠 2027 利潤率站上 5% 才划算，等 2027 年 2 月財測與開年會員數驗證，不追。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是 ACA 個人保單的承保利差，錢卡在 CMS 風險調整與聯邦補貼兩個節點。","reasoning":"Oscar 幾乎只有一條業務線：賣 ACA 個人健康險，收保費，付醫療支出與行政費。2026 第三季營收 51.4 億美元、營業利益 1.78 億（利益率 3.46%）、MLR 84.0%、SG&A 14.0%，季末會員 269 萬，年增 27%。保險業沒有毛利率口徑，這裡用 MLR 代替；分部營收事實表未涵蓋。全年指引營收 190–193 億、MLR 80.5–81.5%、營業利益 8.5–9.5 億。單點依賴有三個：聯邦補貼是主要付款方（最新可查的 2022 年約 85% 會員領補貼，近年比例事實表未涵蓋）；經紀人通路帶來絕大多數會員；CMS 風險調整全年約占保費 17–18%，是損益表最大的估計項。供需持久性判斷為供給可逆性高：對手退出有利，但也有對手同時加縣市，利潤回來後供給可以回來。","fact_refs":["f_kpi0_total_revenue_gaap","f_kpi2_gaap_earnings_from_opera","f_kpi4_medical_loss_ratio_sg_a_","f_kpi7_effectuated_membership","f_kpi8_fy2026_guidance"],"verdict_values":{"revenue_quality":"營收受風險調整估計影響大：第三季含 2.5 億美元風險調整更新利益，全年風險調整占保費比由 20% 下修到 17–18%。","unit_econ_note":"每 1 個百分點 MLR 約 1.9 億美元營業利益，約合每股 0.55 美元（自算：全年營收中點 191.5 億×1%，稀釋股約 341 百萬，由第三季淨利 167.3 百萬÷EPS 0.49 推得）。","archetype":{"primary":"金融","secondary":"未獲利高成長","confidence":"中","fingerprint":"ACA 健保承保商，損益由損失率與風險調整決定；2025 年仍虧損，2026 才大幅轉盈。"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高。Cigna、Aetna 與 UnitedHealthcare（喬治亞）退出帶來份額，Centene、AmeriHealth Caritas 同時加縣市（Fierce Healthcare、Healthcare Dive、Becker's，2026-10）。階段判為擴張：承保利潤率由 2025 年虧損回到 2026 指引約 4.7%，2027 費率加 14% 並放入利潤擴張，但人數仍在縮。","bargaining":{"up":"上游議價弱：部分市場醫院與醫師團體接近獨占，藥局理賠委外 CVS/Caremark。","down":"下游議價中等：會員每年比價，經紀人是主要通路，佣金不必最高但要有競爭力。","geo":"只在美國營運，事實表未見地緣暴露。"},"profit_pool_dir":"短期由退出的大型保險商流向留下的 ACA 業者；五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"ACA 全國投保人數","value":"2025 年 2,430 萬 → 2026 開放投保 2,280 萬 → 2026-06 約 2,050 萬（KFF）→ 2026 年底約 1,700 萬（CFO，2027 大致不變）→ 2029 約 2,300 萬（CEO 預估）"},{"item":"Oscar 可服務市場","value":"2027 年 21 州 713 個縣，約 1,000 萬人（CEO，2026-11-05）"},{"item":"Oscar 份額","value":"現有區域由 2025 年 17% 到 2026 年 30%，目標 35%；全國目標 2029 年 18%；以年底 250 萬會員÷1,700 萬計，現約 15%（自算）"},{"item":"第二曲線","value":"CHOICE 2026 約 50 萬人，CEO 預估 2029 年 250 萬；Lucie 未納入財務目標"},{"item":"分段 CAGR 與五年營業利益池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河趨勢穩定，等級 C：執行力在擴大，定價權沒有變，份額增加還沒有證明優勢變寬。","reasoning":"機制是成本與通路，不是客戶鎖定：為 ACA 建的窄網絡、經紀人工具與單一資料平台。同業 ROIC 利差算不出來，方向只能用份額證明。自報區域份額 17%→30%，第三季 SG&A 率 14.0% 創新低，2027 調幅 14% 對競爭者平均 15%，執行力評 7、定價權評 5，保險業以綜合判斷給分。報酬屬低利益率高周轉：2026 ROIC 約 32%，扣掉前期項目約 16.5%，兩者的差距就是爭議所在。TTM FCF 利潤率 43% 是應付風險調整累積的浮存金，不能和同業比。持續期最弱一環是社會容忍度。新增資本報酬約 25%，內生成長上限約 15%，都用管理層目標推算。AI 降費是真的，但對手也做得到，公司也沒有申請專利。","fact_refs":["f_peer_oscr_fcf_margin_pct","f_peer_cnc_operating_margin_pct","f_peer_moh_operating_margin_pct","f_peer_clov_operating_margin_pct","f_kpi4_medical_loss_ratio_sg_a_"],"verdict_values":{"moat":{"mechanism":"ACA 原生窄網絡、經紀人工具與單一資料平台形成的成本與通路優勢，不是客戶鎖定。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：自報區域份額由 17% 升到 30%，SG&A 率創新低。定價權穩定：2027 調幅與全國平均相當，CFO 說價格必須在最低價的合理範圍內。份額是單一年度、公司自報，又發生在對手退出的年份。2027 開放投保若在費率相近下仍拿到份額，才上調。","competitor_notes":[{"name":"CNC","strategy_note":"2027 反向加縣市，是份額爭奪的主要對手；TTM 利潤率偏低，用價格換量的空間要看其他業務能否支撐，事實表未涵蓋分部資料。"},{"name":"MOH","strategy_note":"同業表只有利潤率，事實表沒有其 ACA 布局，無法判斷對 Oscar 的直接壓力。"},{"name":"ELV","strategy_note":"同業表只有 FCF 利潤率，營業利益率空缺，事實表未涵蓋其重疊市場。"},{"name":"CLOV","strategy_note":"事實表未涵蓋其與 Oscar 的業務重疊，不視為直接競爭證據。"},{"name":"UNH","strategy_note":"2027 退出喬治亞 ACA 市場，並預期流失約 50 萬 ACA 會員，短期是份額來源，也是利潤回升後最可能回補的大型對手。"}],"peer_na_reason":"事實表沒有投入資本與同業 ROIC，OSCR 的營業利益率在同業表也是空值，ROIC 利差無法計算，改用份額做方向證據。","threats":[{"level":"🟡","text":"對手回補與低價：Centene、AmeriHealth Caritas 2027 加縣市，UBS 分析師在法說指出有對手以最低價進場。","p":"35%","evidence_refs":["end_markets#1","competitive_share_entrants#2"]},{"level":"🟡","text":"上游議價：部分市場的醫院或醫師團體接近獨占，窄網絡的談判力受限。","p":"30%","evidence_refs":["regulatory_antitrust#1"]},{"level":"🟡","text":"技術沒有專利保護，關鍵人員流失會干擾營運，AI 帶來的成本優勢對手可以追上。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"外包依賴：藥局理賠與網絡委外單一 PBM（2021 年 10-K 揭露，近年是否變動事實表未涵蓋），多數通訊與軟硬體由第三方營運。","p":"15%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是會員，決定者多半是經紀人加會員，付款方大半是聯邦補貼。保險需求成立，但付款方一退人數就掉：市場由 2,430 萬縮到 2026 年底約 1,700 萬。"},{"item":"決策層級","level":"🟡","text":"每年重選一次，轉換成本低，經紀人用比價平台。留存較佳的說法沒有數字。2026 費率上調後會員仍年增 27%，顯示相對價格比絕對價格重要，這是競爭力，不是鎖定。"},{"item":"價值鏈分配","level":"🟡","text":"醫院與醫師團體在部分市場接近獨占，藥局理賠委外，經紀人拿佣金。管理層把 MLR 目標放在接近 80%，再扣約 15% 行政費。2029 年 5–7% 利潤率目標已高於其自述的歷史區間 3–5%。"},{"item":"社會容忍度","level":"🔴","text":"定價上限由政治決定：2027 提案保費中位數漲約 15%，Oscar 喬治亞州申請約 29%，補貼仍在國會爭議中，CEO 於 2026-11-05 表示對 2027–28 恢復補貼不抱太大期待，公司也預期持續受 DOJ 與 HHS-OIG 審查。"}],"roiic":25,"reinvest_rate":60,"endo_ceiling":15,"formula_note":"當期 ROIC：2026 指引中點營業利益 9 億美元，稅率按個位數中段，投入資本用保險子公司資本 23 億加母公司現金 3.6 億，約 32%；扣掉前期項目 4.37 億（2025 風險調整結算 1.6 億＋前期準備金有利發展 2.77 億）約 16.5%。保險業沒有常規投入資本口徑，此為近似。增量報酬：2026 淨利約 8.4 億（9 億×九個月淨利對營業利益比 0.93），2029 目標 EPS 4 美元×約 367 百萬股（341 百萬每年增 2.5%）＝14.7 億，增量 6.3 億，除以留存資本 25.5 億（計畫資本 40–45 億中點×60%）≈25%。內生上限 25%×60%＝15%；資本配置若評為最低級，再打八折為 12%。數字由管理層目標推出，是上限，不是實績。"}}}},"q3_growth":{"verdict":"五年後跑道中等：現有區域份額到時會達到公司自訂的 35% 成熟水準，第二曲線管理層自己也沒有放進數字。","reasoning":"成長主要靠價，其次靠量：第三季營收年增約 70%，會員年增 27%。2027 費率約加 14%，市場人數預期與 2026 年底相當。共識 EPS 2026–2028 為 1.94、2.22、2.84 美元；基期 2025 虧損，三年 CAGR 無法計算，以 2026→2028 兩年計約 21%。若改用指引推估的 2026 EPS 2.45 美元，只剩約 8%。內生上限約 15%，缺口約 6 個百分點，歸因於利潤率擴張（由約 4.7% 到 2029 年目標 5–7%）。全國份額約 15%，現有區域約 30%，目標 35%，每年擴 400–600 縣，到第五年後現有區域已達成熟水準。CHOICE 與 Lucie 是第二曲線的候選，但 CEO 說 Lucie 未進數字、CHOICE 放進的也有限，因此不計入。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_effectuated_membership"],"verdict_values":{"growth":{"driver_mix":"價大於量；併購與回購不是成長來源。","runway_years":"約 6 年（全國份額口徑；現有區域已約 30%）","runway_post_y5":"🟡","endo_ceiling_basis":"見護城河段推導：增量報酬約 25%×留存率 60%≈15%，來自管理層 2029 目標與資本規劃。","segments":{"expanded":false,"reason":"公司只揭露單一保險業務，Lucie 與 CHOICE 沒有營收數字，分部三年成長事實表未涵蓋。"},"decay_signals":["EPS 成長顯著高於營收成長：2026→2028 共識 EPS 年增約 21%，2027 共識營收僅增約 9.5%，差距超過 5 個百分點。","TAM 萎縮：ACA 人數由 2,430 萬降到 2026 年底約 1,700 萬。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏弱：沒有回購，股數持續增加，新增資本多半要留在保險子公司。","reasoning":"前九個月 FCF 34.8 億美元，約為淨利 12.1 億的 2.9 倍，但主要是應付風險調整的時間差：第三季付掉 2025 年應付款後，現金與投資由 102 億降到約 90 億。真正可動用的是母公司現金與投資 3.6 億，加子公司超額資本 14 億。第三季 SBC 只占營收 0.43%，但管理層指引稀釋股數每年增 2–3%，超過每年 1.5% 的標準。2030 年到期的 3.55 億美元可轉債轉換價 24.82 美元已在價內，capped call 上限 37.46 美元。投資人日規劃 40–45 億美元資本，約 60% 留在子公司，其餘用於併購與管理稀釋。近三年現金去向四分事實表未涵蓋。","fact_refs":["f_kpi5_free_cash_flow","f_kpi6_sbc","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"2025 年收購 Lucie、IHC Specialty Benefits，金額與報酬事實表未涵蓋；近 12 個月無併購 8-K。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未見回購；上繳母公司資金的用途是併購與管理稀釋。"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"管理層指引稀釋股數年增 2–3%，高於 1.5%；聚合站顯示 2021–2025 稀釋股數由 179 百萬增到 262 百萬，口徑未核對財報。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，公司沒有配息與回購，近三年現金去向與併購金額事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求每股盈餘穩在 2.0–2.5 美元、不再回到虧損才划算。方向上相信，幅度上還不能確認，估值看成中性。","reasoning":"現價 30.65 美元，對 2026 共識 15.8 倍，對 2027 共識 13.8 倍；以 12–15 倍計，現價對應約 2.0–2.5 美元的可持續 EPS。分母有兩個相反的問題。第一，1.94 美元看來尚未反映 11-05 上修；用新指引中點推算（營業利益 9 億×0.93÷341 百萬股）約 2.45 美元，倍數約 12.5。第二，全年營業利益中有 4.37 億美元屬前期項目，扣除後 EPS 約 1.26 美元，倍數約 24。EV/S 0.14 倍也不能用：70 億美元淨現金主要對應理賠準備與應付風險調整。改用母公司現金加子公司超額資本 17.6 億計，EV 約 82 億美元，EV/S 約 0.43 倍。股數方面，事實表 310.69 百萬未含完整稀釋，第三季隱含稀釋股約 341 百萬，市值會高約 10%。保險業常用的 P/TBV 因事實表沒有帳面淨值而無法使用。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_ev_m","f_shares_diluted_m"],"verdict_values":{"valuation":{"basis":"Forward P/E（2026 共識 EPS），P/TBV 因事實表沒有帳面淨值而無法使用。","tier":"單一 ACA 業務、獲利波動大的健保承保商","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比，無從比較，列為資料缺口。"},"fwd_pe":15.8,"peg":0.75,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"2026 為 15.8 倍、2027 為 13.8 倍，PEG 0.75（2026→2028 共識 CAGR 21%），表面便宜；但分母有爭議，便宜論證不成立，所以看成中性。五年分位無法計算：本益比只有 1 個年度端點，P/S 在 4 個年度端點中最高，EV/S 位於 69.8 分位。短期空間以 2027 Base EPS 2.35×14 倍＝32.9 美元計；中期以 2029 Base EPS 3.20×12 倍＝38.4 美元計。","upside_short_pct":7.3,"upside_mid_pct":25.3,"denominator_disputed":true,"denominator_note":"2026 共識 1.94 美元看來尚未反映上修，按新指引推算約 2.45 美元，扣掉前期項目 4.37 億美元後約 1.26 美元，對應本益比 15.8、12.5、24 倍；未定的是哪一個代表常態。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把 2026 當成常態獲利；價值陷阱風險中等。","reasoning":"依據見反證紀錄。亮燈兩項：EPS 成長高於營收成長、市場人數萎縮。對 2027 Base EPS 2.35 美元做五項壓力測試：MLR 多 2 個百分點（約 −1.1）、風險調整不利 2 個百分點（約 −1.35）、市場人數少 15%（約 −0.45）、稅率回到 20%（約 −0.4），單獨發生時 EPS 都還是正的；MLR 與風險調整同時發生則轉負，五項過四項。歷史最大回撤、空方數字、訴訟與監管金額事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_kpi8_fy2026_guidance","f_ma_w104","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"獲利品質待驗，市場人數仍在縮"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.94,"pe":15.8,"basis":"2026 年共識 EPS（FY1，看來尚未反映 11-05 上修）；終端倍數同樣以當年度 EPS 為分母。"},"eps":{"bull":[2.9,3.6,4.6,5.4,6.2],"base":[2.35,2.75,3.2,3.6,4.0],"bear":[1.2,0.35,0.9,1.3,1.6]},"pe":{"bull":16,"base":12,"bear":8},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-65,"hi":-40,"basis":"Bear 終點 12.8 美元相當於 −58%，250 週均線 13.36 美元相當於 −56%，再加財報跳空，下緣取 −65%；較輕的路徑是跌回 104 週均線 19.03 美元，約 −38%，上緣取 −40%。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"2029 年 EPS 超過管理層 4 美元目標：部分補貼恢復，CHOICE 與 Lucie 開始貢獻，營業利益率 6–7%。終端 16 倍略高於現值 15.8 倍；事實表未涵蓋同業本益比，只能對照自身。機率 20%，因第二曲線連管理層都沒放進數字。","base":"2027 營業利益率略低於管理層 5% 的承諾，EPS 比 2029 目標晚兩年到 4 美元，期間稅率回升。終端 12 倍低於現值 15.8 倍與 2027 的 13.8 倍，反映獲利波動與政策依賴。機率 50%。","bear":"2026 的有利估計回吐，2028 年接近損益兩平，之後回到約 2–3% 利潤率與較小人數，2031 年 EPS 1.60 美元×8 倍。機率 30%：共識成長超過內生上限，近四個財年有三年虧損（2022、2023、2025），補貼與資格審查仍在收緊。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"前九個月營業利益 13 億美元，其中 4.37 億屬前期項目；第三季另有 2.5 億風險調整更新。Piper 估第三季每人醫療支出年增 19.9%，CFO 說會員月數有扭曲，但沒有給自己的數字。2025 全年虧損 4.43 億美元。","assumption":"2026 的罹病率與風險調整應計都準確，2027 的 14% 調幅足以涵蓋高個位數趨勢與罹病率上升，還留有利潤擴張。","consequence":"2027 MLR 多 2 個百分點，EPS 少約 1.1 美元；Bear 五年後 12.8 美元，較現價跌約 58%。","ruling":"採納。Bear 機率訂 30%，這是不追的主因。","watch":"第四季 MLR、2027 財測、2027 年中風險調整結算。","evidence_refs":["end_markets#1"],"fact_refs":["f_kpi8_fy2026_guidance","f_kpi0_total_revenue_gaap"]},{"view":"論點失敗","evidence":"社會容忍度是最弱一環。聯邦補貼是主要付款方，2022 年約 85% 會員領補貼。增強補貼 2025 年底到期，CMS 資格審查還在繼續，CEO 於 11-05 表示對 2027–28 恢復補貼不抱太大期待。公司也受 DOJ、HHS-OIG 的詐欺與濫用法規審查。","assumption":"2027 市場人數與 2026 年底相當，且調幅已涵蓋資格審查造成的風險池惡化。","consequence":"若市場再縮 15% 且留下者風險更高，營收與 MLR 兩邊同時受壓，2028 接近損益兩平（Bear 路徑 0.35 美元）。","ruling":"採納。但前份最擔心的補貼到期已經發生，公司挺過來了；這條風險由單一事件改為逐年的政策侵蝕。","watch":"CMS 投保人數、2028 年規則、兩黨補貼協商。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","regulatory_antitrust#0","regulatory_antitrust#2"],"fact_refs":["f_kpi7_effectuated_membership"]},{"view":"論點成功但股東經濟變差","evidence":"CFO 於投資人日指引稀釋股數每年增 2–3%，計畫期間資本約 60% 留在保險子公司。聚合站顯示稀釋股數 2021–2025 由 179 百萬增到 262 百萬，2026 第一季 329.8 百萬，口徑未核對。可轉債已在價內。2027 稅率仍是個位數中段，假設回到 20%，EPS 少約 16%。","assumption":"營收與份額目標達成，利潤就會全部歸股東。","consequence":"即使 2029 年 EPS 達 4 美元，新增資本也只有約四成回到母公司，倍數難以上升。","ruling":"採納。Base 終端倍數設 12 倍，低於現值，報酬只來自盈餘成長。","watch":"稀釋股數年增率、母公司現金、有效稅率。","evidence_refs":["unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#1"],"fact_refs":["f_shares_diluted_m","f_kpi6_sbc"]},{"view":"價格已反映太多","evidence":"前份以來股價漲 31%，26 週漲 43.83%，高於 52 週均線 37.6%，P/S 在 4 個年度端點中最高。看似便宜的 EV/S 與 FCF 利潤率都受浮存金影響：第三季付掉 2025 年風險調整應付款後，現金與投資由 102 億降到約 90 億美元。","assumption":"市場用的是約 2.0–2.5 美元的可持續 EPS。","consequence":"若底層 EPS 其實是扣前期項目後的約 1.26 美元，現價約 24 倍。","ruling":"部分採納。2027 的 13.8 倍本身不貴，但分母有爭議，便宜論證不成立，估值只算中性。","watch":"2027 財測的營業利益率與稅率。","fact_refs":["f_week26_return_pct","f_ps_percentile","f_ma_w52","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"管理層有多次沒有正面回答：2026-08-06 沒答 CMS 百萬名單中有多少是 Oscar 會員，也未確認剔除前期項目後的第二季 MLR；2026-09-16 未拆解 MLR 改善 150bp，SG&A 降到 15% 以下只答規模與 AI，未回應 CHOICE 的立法風險，也未給流失者與留存者的 MLR 差異。","assumption":"這些沒講的數字不會改變結論。","consequence":"風險池變化與成本改善的拆解都拿不到，只能靠財報結果反推。","ruling":"採納，列為資料缺口；在 2027 財測前不採信利潤率擴張的拆解。","watch":"2027 年 2 月財報是否揭露費用與 MLR 的拆解。"}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 23.32 → 本次 30.65（+31.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=23.32","side_b":"本次 price_at_dd=30.65","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 23.32 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 23.32 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 23.32 美元：Bull 價 99.2、Bear 價 12.8，五年期望值 +104.5%，基準年化 15.5%，不對稱比 4.81","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 4.81。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 23.32 美元：五年期望值 +104.5%，基準年化 15.5%，不對稱比 4.81","side_b":"本次情境、股價 30.65 美元：五年期望值 +55.6%，基準年化 9.4%，不對稱比 2.56","ruling":"再換股價、情境不動：起點價上漲 31.4%，五年期望值少 48.9 個百分點，基準年化少 6.1 個百分點，不對稱比由 4.81 降到 2.56。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2026 獲利是結構改善，還是估計有利","cause":null,"prior_field":null,"side_a":"CEO 與 CFO（2026-11-05）：改善主要來自定價紀律、費用控管與 AI，風險調整是業務的一部分，不該剔除。","side_b":"全年營業利益中點 9 億美元，其中 4.37 億屬前期項目；第三季另有 2.5 億風險調整更新，全年風險調整占保費比一次改了 2–3 個百分點。","ruling":"兩邊是程度差異，可以調和。定價改善是真的，但不把 2026 當常態，Base 的 2027 營業利益率略低於 5%。管理層的歸因標為未證、持續監測。","evidence_level":"高，公司揭露數字；前期項目合計為自算","settle_metric":"2026 年度風險調整結算差額、2027 全年營業利益率","if_then":["如果結算差額不利不超過保費 1 個百分點，且 2027 營業利益率指引維持 5% 以上，重做完整研究後首筆建倉不超過組合 2%。","如果不利超過保費 2 個百分點，或 2027 指引低於 3%，清倉並移出觀察名單。","反向：如果 2027 連續兩季前期項目歸零、營業利益率仍達 5%，改認定為結構改善，上調 Base。"],"evidence_refs":["end_markets#0","unprofitable_path_to_profitability#0"]},{"axis":"風險調整利多與 MLR 上修對不上","cause":null,"prior_field":null,"side_a":"Wells Fargo 分析師（2026-11-05）：風險調整應付比例下修 2–3 個百分點，全年 MLR 只改善 0.5 個百分點；Piper 分析師估第三季每人醫療支出年增 19.9%。","side_b":"CFO（2026-11-05）：部分風險調整利益被相應的理賠抵銷，Wakely 資料只到 7 月，指引保留了罹病率空間。","ruling":"不採信也不否定。若差額是保守，第四季會超指引；若是真實理賠，底層成本比「溫和有利」的說法差。","evidence_level":"中，分析師估算與管理層口頭說明","settle_metric":"第四季實際 MLR 是否落在九成出頭，2026 全年 MLR 是否不高於 81.5%","if_then":["如果 2026 全年 MLR 高於 81.5%，管理層保守的說法證偽，不追，Bear 機率上調到 35%。","反向：如果全年 MLR 低於 80.5%，保守的說法成立，Bear 機率維持 30% 並等 2027 財測。"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-09-16 投資人日，CEO：開放投保已有 80 萬張保單；CFO：母公司現金 4.6 億美元；同場 NPS 產業平均一說 12，一說 0。","side_b":"2026-11-05 法說，CEO：Lucie 有望在 2027 年賣出約 80 萬張新保單；CFO：母公司現金與投資 3.6 億美元。財測方面，全年營業利益指引由 5–7 億、6–8 億上修到 8.5–9.5 億。","ruling":"「已有」變成「有望」，用語降了一級，Lucie 與 NPS 都不計入 Base。母公司現金少 1 億美元沒有解釋，事實表未涵蓋。財測上修顯示指引偏保守，這點給予肯定。","evidence_level":"中，逐字稿比對","settle_metric":"2027 年 2 月揭露的 Lucie 保單數與母公司現金","if_then":["如果 Lucie 保單數低於 80 萬，Bull 機率由 20% 下修到 15%，差額加到 Base。"]},{"axis":"賣方對 2027 的分歧","cause":null,"prior_field":null,"side_a":"UBS（聚合站轉述）評賣出：2027 營收 122 億美元、EPS 1.25 美元，並稱共識 1.46 美元。","side_b":"Koyfin 共識 2027 EPS 2.22 美元、yfinance 共識營收 208 億美元；管理層說 2027 EPS 超過 2.25 美元。目標價由 11 美元到 Barclays 49 美元，三個聚合站均值 16.78–24.20 美元。","ruling":"UBS 的 122 億營收與全年指引 190 億差距過大，1.46 美元共識也對不上，只取方向，並把 1.25 美元當 Bear 第一年的參考。目標價全距 4.5 倍且日期分散，不用來支持裁決，只下調信心。分歧屬框架層：2026 是常態還是高點。","evidence_level":"低，聚合站轉述，未核原文","settle_metric":"2027 年 2 月公司財測","if_then":["如果 2027 EPS 指引低於 1.50 美元，採信 UBS 的框架，不追並把 Bear 機率上調到 40%。"],"evidence_refs":["end_markets#1","capital_markets_pricing#2"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭面：Cigna、Aetna 退出，UnitedHealthcare 2027 退出喬治亞，約 85 萬人重新進入市場；另一方面 Centene、AmeriHealth Caritas 加縣市。","side_b":"結構面：補貼到期、資格審查延續，市場人數減少，留下者風險較高；ICHRA 經紀人採用度由 15% 升到 37%，但調查由 Oscar 贊助。","ruling":"雙向拉鋸。對留下的業者，競爭在短期轉好；對整個市場，法規與補貼仍在縮小分母。","evidence_level":"中，產業媒體與公司說法","settle_metric":"2027 全國有效投保人數與對手的 2028 縣市布局","if_then":["如果全國有效投保人數低於 1,600 萬，改判為法規結構惡化，不追。"],"evidence_refs":["competitive_share_entrants#2","customer_concentration_credit#1","channel_business_model_shift#1"]},{"axis":"現在就買的最強論證，以及前份觀察以來股價漲 31% 為何仍不追","cause":null,"prior_field":null,"side_a":"現在就買：補貼到期這個最大風險已過，指引連三次上修，2027 倍數 13.8 倍，管理層承諾 2027 EPS 超過 2.25 美元、2029 年至少 4 美元，對手退出放出約 85 萬人，RSI 45 沒有過熱，等到 2 月可能已經漲上去。","side_b":"2027 倍數用的是未經驗證的預期，2026 利潤近半來自前期項目，開放投保在法說時只過了 4–5 天；2 月就有第一份驗證，等待的成本有限。","ruling":"選不追。翻面的部分是評級上調一級，因為前份的補貼風險已經過去；進場沒有翻面，因為 Base 年化報酬約 9%，不足以補償 30% 機率、約 58% 的跌幅。束縛條件只有一個：2027 利潤率能否站住。","evidence_level":"中，情境推算","settle_metric":"2027 年 2 月財測與開年會員","if_then":["如果股價先漲、財測還沒出來，不追。","如果股價下跌但重啟條件成立，分批反買；條件未成立前不動作。","反向：如果 2027 營業利益率指引低於 3%，清倉。"]},{"axis":"評級、估值與價值陷阱的變動","cause":"新證據","prior_field":["signal","val","trap"],"side_a":"前份：評級 C、估值中性、價值陷阱中等，論點卡在補貼立法。","side_b":"本次：評級 B、估值中性、價值陷阱中等。補貼已到期，公司三度上修，2026 指引營業利益 8.5–9.5 億美元。","ruling":"評級上調一級：前份最怕的事發生了，結果是公司賺錢。估值維持中性：股價上漲，盈餘預期也上升，但分母仍有爭議。價值陷阱維持中等：亮燈的是市場萎縮與 EPS 成長高於營收成長。","evidence_level":"高，公司財報","settle_metric":"2027 財測","if_then":["如果 2027 財測達標，維持目前評級並重新研究；如果低於 3%，評級下調並清倉。"]},{"axis":"前份留空的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這幾項都沒有填。","side_b":"本次填入：護城河趨勢穩定、五年後跑道中等、類型為金融、循環位置中循環，最大回撤區間 −65%～−40%，Bull 20%、Bear 30%。","ruling":"前份沒有基準可比，差異來自填寫方式，不是基本面變化。","evidence_level":"不適用","settle_metric":"無","if_then":[]},{"axis":"行動門檻更新：重新研究、減碼、清倉","cause":"新證據","prior_field":["rearm_trigger","kill_metrics"],"side_a":"等 2025-Q4 PTC 立法 + H2 MLR ≤84% 雙信號明朗化再評估；前份 MLR 警戒為任一季 MLR > 86% 削弱，> 88% 反轉；重啟條件與停損指標欄位未設。","side_b":"2027 年 2 月財報同時達到 2027 營業利益率指引至少 5%、開年會員至少 260 萬、2026 全年 MLR 不高於 81.5% 才重新研究；全年 MLR 指引高於 83% 減碼；2027 營業利益率指引低於 3% 清倉。","ruling":"舊門檻失效：補貼立法已有結果。單季 MLR 季節性很強（第二季 79.2%、第三季 84.0%、第四季隱含九成出頭），單季門檻會誤判，改看全年。","evidence_level":"高，公司財報與法說","settle_metric":"2027 年 2 月財報","if_then":["如果三項都達到，重新研究；任一項未達，繼續不追。"]},{"axis":"Single Thing 由補貼立法改為風險調整結算","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（欄位為空），當時最大風險是 2025 Q4 增強補貼立法失敗。","side_b":"CMS 在 2027 年年中公布的 2026 年度風險調整結算，與帳上應計相比不利超過保費 2 個百分點。","ruling":"補貼到期已經發生，不再是未來的二元事件。按敏感度排序，風險調整 2 個百分點約每股 1.36 美元，會員少 10% 只影響約每股 0.3 美元，前者才是最大單項。","evidence_level":"中，敏感度為自算","settle_metric":"2027 年第二季財報揭露的結算差額","if_then":["如果差額不利超過保費 2 個百分點，清倉。"]},{"axis":"前份假設的驗證結果","cause":"新證據","prior_field":["H1","R1"],"side_a":"前份 H1 門檻為 ACA 人數至少 2,200 萬、Oscar 份額 8–12%；R1 為補貼立法失敗即觸發。","side_b":"補貼確實到期，市場預計 2026 年底約 1,700 萬；但 Oscar 會員年增 27%，全年 MLR 指引 80.5–81.5%，SG&A 率 15.1–15.6%，前份 H2、H3 的門檻都已達到。","ruling":"前份把人數當成獲利前提，這點看錯了：人數掉下來時，定對價的業者反而賺得更多。新 H1 改看利潤率。","evidence_level":"高，公司財報與法說","settle_metric":"2027 全年營業利益率","if_then":["如果 2027 利潤率低於 3%，代表 2026 只是一年的定價紅利，回到前份的謹慎立場並清倉。"]}],"triggers":[{"n":1,"text":"2027 年 2 月財報的 2027 財測、開年會員與 2026 全年 MLR 同時達標","type":"估值rearm","maps_to":"H1","metric":"2027 營業利益率指引、開年會員、2026 全年 MLR","threshold":"至少 5%、至少 260 萬、不高於 81.5%，三項都要","action":"三項全過才重做完整研究，通過後首筆不超過組合 2%","source_freq":"季度財報","date":"2027-02"},{"n":2,"text":"CMS 公布 2026 年度風險調整結算，不利超過保費 2 個百分點","type":"Single Thing","maps_to":"Single Thing","metric":"結算差額占保費比","threshold":"不利超過 2 個百分點（約 4.6 億美元，自算）","action":"清倉並移出觀察名單","source_freq":"一年一次，第二季財報揭露","date":"2027-08"},{"n":3,"text":"2027 第一季有效會員驗證份額論點","type":"假設驗證","maps_to":"H2","metric":"季末有效會員","threshold":"至少 260 萬過關，低於 240 萬削弱","action":"低於 240 萬則不進場，已持有者減碼一半","source_freq":"季度新聞稿","date":"2027-05"},{"n":4,"text":"2027 全年 SG&A 率驗證費用論點","type":"假設驗證","maps_to":"H3","metric":"全年 SG&A 率","threshold":"不高於 15.1% 過關，高於 15.6% 削弱","action":"高於 15.6% 則停止加碼","source_freq":"年度財報","date":"2028-02"},{"n":5,"text":"ACA 全國投保人數再度明顯萎縮","type":"風險","maps_to":"R2","metric":"全國有效投保人數","threshold":"低於 1,600 萬","action":"不追，已持有者減碼一半","source_freq":"CMS、KFF 不定期","date":"2027-12","evidence_refs":["customer_concentration_credit#1","regulatory_antitrust#2"]},{"n":6,"text":"關稅或藥品回扣下降未被定價吸收","type":"風險","maps_to":"R4","metric":"全年 MLR 對指引上緣，且管理層點名藥費或回扣","threshold":"超過指引上緣 1 個百分點","action":"減碼一半","source_freq":"季度財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"n":7,"text":"2027 全年 MLR 指引明顯惡化","type":"減碼","maps_to":"R1","metric":"全年 MLR 指引","threshold":"高於 83%","action":"已持有者減碼一半，未持有者不追","source_freq":"季度財報","date":"2027-08"},{"n":8,"text":"2027 營業利益率指引跌破 3%","type":"清倉","maps_to":"H1","metric":"全年營業利益率指引","threshold":"低於 3%","action":"清倉","source_freq":"季度財報","date":"2027-02"},{"n":9,"text":"第四季財報後完整複審","type":"複審日期","maps_to":"H1","metric":"2027 財測與開放投保結果","threshold":"無","action":"財報公布後一週內重做完整研究","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"2027 全年 MLR 指引","bear_threshold":"高於 83%","window":"2027 年 2 月起每季","source":"公司財報與法說","last_status":"unknown"},{"metric":"2027 全年營業利益率指引","bear_threshold":"低於 3%","window":"2027 年 2 月起每季","source":"公司財報與法說","last_status":"unknown"},{"metric":"2026 年度風險調整結算與帳上應計差額","bear_threshold":"不利超過保費 2 個百分點","window":"2027 年第二季財報","source":"CMS 報告、公司 10-Q","last_status":"unknown"},{"metric":"季末有效會員","bear_threshold":"2027 第一季低於 240 萬","window":"2027 年第一季","source":"公司新聞稿","last_status":"unknown"},{"metric":"ACA 全國有效投保人數","bear_threshold":"低於 1,600 萬","window":"2027 全年","source":"CMS、KFF","last_status":"unknown"},{"metric":"2026 全年 MLR","bear_threshold":"高於 81.5%（指引上緣）","window":"2027 年 2 月","source":"公司財報","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"2027 年 2 月財報同時達到：2027 營業利益率指引至少 5%、開年會員至少 260 萬、2026 全年 MLR 不高於 81.5%","exec_line":"未持有：2027 年 2 月財報前不建倉，條件成立後重做完整研究，通過後首筆不超過組合 2%。已持有：不加碼；全年 MLR 指引高於 83% 減碼一半；2027 營業利益率指引低於 3% 清倉。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月財報驗證 2027 財測、開年會員與 2026 全年 MLR，不設進場價。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"2026 的利潤不是一次性：2027 在沒有大額前期利益下，營業利益率仍達 5%。","2y":"2027 全年營業利益率至少 5%，MLR 不高於 81.5%","5y":"三年滾動營業利益率至少 4.5%，期間沒有虧損年度","10y":null,"threshold":"2027 MLR 加 SG&A 率合計不高於 96.5%；風險調整結算不利不超過保費 1 個百分點","source":"公司季報與法說、CMS 風險調整報告、Wakely","drift_rule":"TTM 營業利益率低於門檻 5% 以上連 2 季削弱，低於 10% 以上連 3 季反轉"},{"id":"H2","text":"2027 在費率與對手相近時仍拿到份額，證明份額不是只靠對手撤退。","2y":"2027 第一季會員至少 260 萬，全國份額至少 15%","5y":"2029 全國份額接近 18%，現有區域達 35%","10y":null,"threshold":"2027 第一季會員至少 260 萬","source":"公司季報、CMS 投保資料、KFF","drift_rule":"會員數低於門檻 5% 以上連 2 季削弱，低於 10% 以上連 3 季反轉"},{"id":"H3","text":"固定成本攤提與 AI 讓 SG&A 率繼續下降，且不必靠提高佣金換成長。","2y":"2027 全年 SG&A 率不高於 15.1%","5y":"2029 年 SG&A 率低於 15%","10y":null,"threshold":"2027 全年 SG&A 率不高於 15.1%（2026 指引下緣）","source":"公司季報與法說","drift_rule":"TTM SG&A 率高於門檻 5% 以上連 2 季削弱，高於 10% 以上連 3 季反轉"}],"R":[{"id":"R1","text":"風險調整或罹病率估計反轉，2026 的利多回吐。","h_ref":"H1","clock":"⚡","threshold":"單次估計變動不利至少 2.5 億美元，或全年 MLR 指引高於 83%","evidence_refs":["end_markets#1"]},{"id":"R2","text":"聯邦補貼與資格審查繼續壓縮市場，留下的人風險更高。","h_ref":"H1","clock":"🔥","threshold":"全國有效投保人數低於 1,600 萬，或 Wakely 資料否定 2027 定價的罹病率假設","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","regulatory_antitrust#2","end_markets#1"]},{"id":"R3","text":"對手回補或低價搶市，份額增加無法維持。","h_ref":"H2","clock":"🔥","threshold":"2027 第一季會員低於 240 萬","evidence_refs":["end_markets#1"]},{"id":"R4","text":"藥品關稅與回扣下降推高醫療成本，超出定價假設。","h_ref":"H1","clock":"🔥","threshold":"全年 MLR 超過指引上緣 1 個百分點，且管理層點名藥費或回扣","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R5","text":"DOJ、HHS-OIG 持續審查詐欺與濫用，包括遠距醫療的給付做法。","h_ref":"H1","clock":"🐢","threshold":"收到具名調查或和解金額超過 1 億美元","evidence_refs":["regulatory_antitrust#0"]}],"single_thing":{"description":"CMS 在 2027 年年中公布的 2026 年度風險調整結算，與公司帳上應計相比不利超過保費 2 個百分點（約 4.6 億美元，自算：全年營收中點÷(1−17.5%)×2%）。","why_fatal":"本次法說把風險調整占保費比一次改了 2–3 個百分點，這是損益表最大的估計項。2 個百分點約每股 1.36 美元，超過 2027 共識 2.22 美元的一半；會員少 10% 只影響約 1 億美元營業利益，敏感度差四到五倍。","if_happens":"2027 財測下修，當年營業利益率回到 3% 以下，Bear 路徑成立，五年目標約 12.8 美元。持有者清倉，未持有者移出觀察名單。","how_monitor":"每季風險調整占保費比、Wakely 報告（本次只到 7 月資料）、2027 年第二季財報揭露的結算差額。","probability":"約 20%（12–24 個月）。2026 的結算方向目前有利，但 Wakely 的有利程度已由「相當有利」降到「溫和有利」，且公司 2025 年才虧損 4.43 億美元。"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.8,"peg_fy2":0.66,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-1.69,"FY2026E":1.94,"FY2027E":2.22,"FY2028E":2.84},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；2025 為 yfinance 年報，2026–2028 為 Koyfin 共識（2026-11-07 快照，家數事實表未涵蓋，看來尚未反映 11-05 上修）。"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"CMS 第二輪資格審查造成第四季會員再減少","impact":"中","watch":"年底會員是否約 250 萬"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 正式財測","impact":"高","watch":"營業利益率指引、開年會員、2026 全年 MLR"},{"date":"2027-05","date_precision":"quarter","type":"guidance","event":"第一季財報","impact":"中","watch":"有效會員是否至少 260 萬、Wakely 資料"},{"date":"2027-08","date_precision":"month","type":"regulatory","event":"第二季財報揭露 2026 年度風險調整結算差額","impact":"高","watch":"不利是否超過保費 2 個百分點"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=43.83, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：unprofitable_nrr_rule40_band（NRR／Rule of 40 同業帶）（尾部風險或事件型，不擋）。plan 時 archetype 為「未獲利高成長」、判斷者歸「金融」，金融 的專屬核心軸未採證（不計燈號）：financial_capital_credit_cycle。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
